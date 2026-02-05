import requests
import json
from typing import List, Dict

GUVI_CALLBACK_URL = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"

def send_final_result(session_id: str, 
                      scam_detected: bool, 
                      total_messages: int, 
                      intelligence: dict, 
                      agent_notes: str = "Scam detected and intelligence extracted."):
    """
    Sends the final extracted intelligence to the mandated callback URL.
    """
    payload = {
        "sessionId": session_id,
        "scamDetected": scam_detected,
        "totalMessagesExchanged": total_messages,
        "extractedIntelligence": {
            "bankAccounts": intelligence.get("bank_accounts", []),
            "upiIds": intelligence.get("upi_ids", []),
            "phishingLinks": intelligence.get("phishing_urls", []),
            "phoneNumbers": intelligence.get("phone_numbers", []),
            "suspiciousKeywords": intelligence.get("suspicious_keywords", [])
        },
        "agentNotes": agent_notes
    }
    
    try:
        print(f"[Callback] Sending result for session {session_id}...")
        response = requests.post(GUVI_CALLBACK_URL, json=payload, timeout=5)
        if response.status_code == 200:
            print("[Callback] Success.")
        else:
            print(f"[Callback] Failed with Status {response.status_code}")
    except Exception as e:
        print(f"[Callback] Exception: {e}")
