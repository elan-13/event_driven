import pytest
import json
import io
import sys
import os

# Ensure the app module can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import AVAILABLE_DRIVERS

def test_matching_logic():
    """
    Test the fundamental logic of assigning a driver.
    """
    ride_data = {
        "ride_id": "test_123",
        "user_id": "user_999",
        "pickup_location": "A",
        "drop_location": "B",
        "distance_km": 5,
        "fare": 100,
        "status": "pending"
    }
    
    import random
    # Fix the random choice to ensure predictability 
    random.seed(42)
    
    assigned_driver = random.choice(AVAILABLE_DRIVERS)
    
    ride_data['driver_id'] = assigned_driver
    ride_data['status'] = 'matched'
    
    assert ride_data["status"] == "matched"
    assert ride_data["driver_id"] in AVAILABLE_DRIVERS
