import requests
import time
import uuid
import datetime

# Configuration
API_URL = "http://localhost:8001/scam-event"
API_KEY = "change_this_to_a_strong_random_string"
HEADERS = {"X-API-Key": API_KEY}

class MockScammer:
    def __init__(self):
        self.session_id = str(uuid.uuid4())
        self.history = []
        self.turns = [
            "Your bank account will be blocked today. Verify immediately.",
            "Share your UPI ID to avoid account suspension.",
            "Why are you asking so many questions? Do it fast.",
            "Last warning. Police case will be filed."
        ]
        self.current_turn = 0

    def send_next_message(self):
        if self.current_turn >= len(self.turns):
            print("[Mock Scammer] No more scripts.")
            return False

        message_text = self.turns[self.current_turn]
        current_time = datetime.datetime.now(datetime.timezone.utc).isoformat()
        
        # New Payload Format
        payload = {
            "sessionId": self.session_id,
            "message": {
                "sender": "scammer",
                "text": message_text,
                "timestamp": current_time
            },
            "conversationHistory": self.history,
            "metadata": {
                "channel": "SMS",
                "language": "English",
                "locale": "IN"
            }
        }

        print(f"\n[Mock Scammer] Sending: {message_text}")
        try:
            response = requests.post(API_URL, json=payload, headers=HEADERS)
            if response.status_code == 200:
                data = response.json()
                print(f"[System Response] Status: {data.get('status')}")
                
                agent_reply = data.get("reply")
                if agent_reply:
                    print(f"[Agent]: {agent_reply}")
                    # Add both turns to history for next request
                    self.history.append({
                        "sender": "scammer",
                        "text": message_text,
                        "timestamp": current_time
                    })
                    self.history.append({
                        "sender": "user", # The platform calls the agent "user" in history context usually, or we can use "agent"
                        "text": agent_reply,
                        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
                    })
                else:
                    # If agent didn't reply, just add scammer message to history
                     self.history.append({
                        "sender": "scammer",
                        "text": message_text,
                        "timestamp": current_time
                    })
            else:
                print(f"[Error] Status: {response.status_code} | {response.text}")
        except Exception as e:
            print(f"[Connection Error] {e}")

        self.current_turn += 1
        return True

if __name__ == "__main__":
    scammer = MockScammer()
    print(f"Starting simulation for session: {scammer.session_id}")
    while scammer.send_next_message():
        time.sleep(3) # Wait for readability
