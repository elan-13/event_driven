import pytest
from fastapi.testclient import TestClient
import sys
import os

# Ensure the app module can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app

client = TestClient(app)

def test_book_ride_success(monkeypatch):
    """
    Test booking a ride when Redis is available (mocked).
    """
    # Mock Redis client so we don't actually need Redis running
    class MockRedis:
        def publish(self, channel, message):
            pass

    import app.main
    monkeypatch.setattr(app.main, "redis_client", MockRedis())

    payload = {
        "user_id": "user_123",
        "pickup_location": "Downtown",
        "drop_location": "Airport",
        "distance_km": 15.5
    }

    response = client.post("/book-ride", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Ride booked successfully. Searching for drivers."
    assert "ride_details" in data
    assert data["ride_details"]["user_id"] == "user_123"
    assert data["ride_details"]["fare"] == 205.0  # 50 + (15.5 * 10)
    assert data["ride_details"]["status"] == "pending"

def test_book_ride_no_redis(monkeypatch):
    """
    Test booking a ride when Redis is unavailable.
    """
    import app.main
    monkeypatch.setattr(app.main, "redis_client", None)

    payload = {
        "user_id": "user_123",
        "pickup_location": "Downtown",
        "drop_location": "Airport",
        "distance_km": 15.5
    }

    response = client.post("/book-ride", json=payload)
    
    assert response.status_code == 500
    assert "Redis client is not connected" in response.json()["detail"]
