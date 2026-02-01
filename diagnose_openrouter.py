import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("LLM_API_KEY")
print(f"Loaded API Key: {API_KEY[:10]}... (Length: {len(API_KEY) if API_KEY else 0})")

MODELS_TO_TRY = [
    "microsoft/phi-4:free",
    "google/gemini-2.0-flash-exp:free",
    "meta-llama/llama-3.1-8b-instruct:free",
    "huggingfaceh4/zephyr-7b-beta:free",
    "openchat/openchat-7:free"
]

def test_model(model_id):
    print(f"\nTesting Model: {model_id} ...")
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "Diagnosis Script"
    }
    payload = {
        "model": model_id,
        "messages": [{"role": "user", "content": "Hi"}],
        "max_tokens": 10
    }
    
    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            print("  ✅ SUCCESS!")
            print(f"  Response: {response.json()['choices'][0]['message']['content']}")
            return True
        else:
            print(f"  ❌ FAILED (Status {response.status_code})")
            print(f"  Response: {response.text}")
    except Exception as e:
        print(f"  ❌ FAILED (Exception): {e}")
    return False

print("\n--- Starting Diagnostics ---")
working_model = None

for model in MODELS_TO_TRY:
    if test_model(model):
        working_model = model
        break

if working_model:
    print(f"\n\n🎉 FOUND WORKING MODEL: {working_model}")
    print("Please update your .env file with this model ID.")
else:
    print("\n\n❌ NO WORKING MODELS FOUND. Check your API Key or Internet Connection.")
