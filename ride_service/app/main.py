from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import redis
import json
import uuid
import os

app = FastAPI(title="Ride Service", version="1.0.0")

# Redis Configuration
# Using environment variables for production readiness, with a fallback for local testing
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_CHANNEL = "ride_requests"

# Connect to Redis
try:
    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
except Exception as e:
    print(f"Error connecting to Redis: {e}")
    redis_client = None

# Pydantic model for incoming request
class RideRequest(BaseModel):
    user_id: str
    pickup_location: str
    drop_location: str
    distance_km: float

@app.post("/book-ride")
async def book_ride(request: RideRequest):
    # Fare Calculation Logic
    base_fare = 50.0
    per_km_rate = 10.0
    total_fare = base_fare + (request.distance_km * per_km_rate)

    # Generate unique Ride ID
    ride_id = str(uuid.uuid4())

    # Construct the Ride Object
    ride_event = {
        "ride_id": ride_id,
        "user_id": request.user_id,
        "pickup_location": request.pickup_location,
        "drop_location": request.drop_location,
        "distance_km": request.distance_km,
        "fare": round(total_fare, 2),
        "status": "pending"
    }

    # Publish to Redis
    if not redis_client:
        raise HTTPException(status_code=500, detail="Redis client is not connected.")

    try:
        # Convert dictionary to JSON string to publish
        redis_client.publish(REDIS_CHANNEL, json.dumps(ride_event))
        print(f"Published ride request to channel '{REDIS_CHANNEL}': {ride_id}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to publish event: {str(e)}")

    # Return structured response
    return {
        "message": "Ride booked successfully. Searching for drivers.",
        "ride_details": ride_event
    }
