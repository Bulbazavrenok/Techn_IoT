# test the HTTP-endpoint to store the data
import requests
from app.entities.processed_agent_data import ProcessedAgentData
from app.entities.agent_data import AgentData, AccelerometerData, GpsData
from datetime import datetime
from config import STORE_API_BASE_URL
from fastapi.testclient import TestClient
from main import app


data = {
    "road_state": "good",
    "agent_data": {
        "agent_id": 5,
        "accelerometer": {
            "x": 4.0,
            "y": 5.0,
            "z": 6.0
        },
        "gps": {
            "latitude": 4.05,
            "longitude": 5.06
        },
        "timestamp": str(datetime.now())  # Convert to string
    }
}


response = requests.post(f"http://localhost:9000/processed_agent_data", json=data)


# Check the response
if response.status_code == 200:
    print("Data saved successfully!")
else:
    print("Failed to save data:", response.text, response.status_code)
