import requests
import json
import time
import sys

BASE_URL = "http://localhost:8000"
API_KEY = "default_insecure_key_change_me"
HEADERS = {"X-API-Key": API_KEY, "Content-Type": "application/json"}

def test_root():
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Root Endpoint: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Root Endpoint Failed: {e}")

def test_scam_event():
    payload = {
        "conversation_id": "test_verification_01",
        "message": "URGENT: Your bank account is suspended. Transfer 5000 to upi: verify@sbi immediately to unblock.",
        "timestamp": "2026-02-01T12:00:00Z"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/scam-event", json=payload, headers=HEADERS)
        print("\n--- Scam Event Test ---")
        print(f"Status Code: {response.status_code}")
        print("Response:")
        print(json.dumps(response.json(), indent=2))
        
        data = response.json()
        if data["scam_detected"] and data["agent_engaged"]:
             print("\n[PASS] Scam Detected & Agent Engaged")
        else:
             print("\n[FAIL] Logic mismatch")

    except Exception as e:
        print(f"Scam Event Test Failed: {e}")

if __name__ == "__main__":
    print("Waiting for server to ensure it is up...")
    time.sleep(2) 
    test_root()
    test_scam_event()
