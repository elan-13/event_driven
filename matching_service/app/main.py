import redis
import json
import time
import random
import os

# Redis Configuration
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_CHANNEL = "ride_requests"

# List of available drivers
AVAILABLE_DRIVERS = ["driver_1", "driver_2", "driver_3"]

def start_worker():
    print(f"Connecting to Redis at {REDIS_HOST}:{REDIS_PORT}...")
    try:
        # decode_responses=True ensures we get strings back from Redis instead of bytes
        redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        # Test connection
        redis_client.ping()
        print("Connected to Redis successfully.")
    except Exception as e:
        print(f"Failed to connect to Redis: {e}")
        return

    # Setup Redis PubSub
    pubsub = redis_client.pubsub()
    pubsub.subscribe(REDIS_CHANNEL)
    
    print(f"Started Matching Service. Listening on channel: '{REDIS_CHANNEL}'...")

    # Infinite loop to listen for messages continuously
    try:
        for message in pubsub.listen():
            # A message of type 'message' contains actual published data
            if message['type'] == 'message':
                try:
                    # Parse the JSON string from Redis message data
                    ride_data = json.loads(message['data'])
                    ride_id = ride_data.get('ride_id')
                    
                    print(f"\n--- [MATCHING IN PROGRESS] ---")
                    print(f"Received ride request: {ride_id} for User {ride_data.get('user_id')}")
                    
                    # Simulate processing/matching delay
                    time.sleep(2.0)
                    
                    # Assign a random driver
                    assigned_driver = random.choice(AVAILABLE_DRIVERS)
                    
                    # Update ride object
                    ride_data['driver_id'] = assigned_driver
                    ride_data['status'] = 'matched'
                    
                    print(f"Assigned driver: {assigned_driver}")
                    print(f"Final ride status:")
                    print(json.dumps(ride_data, indent=2))
                    print(f"------------------------------")
                    
                except json.JSONDecodeError:
                    print("Received invalid JSON payload.")
                except Exception as e:
                    print(f"Error processing message: {e}")
    except KeyboardInterrupt:
        print("\nShutting down Matching Service Worker...")

if __name__ == "__main__":
    start_worker()
