# Agentic Honey-Pot for Scam Detection & Intelligence Extraction

**GUVI Hackathon Submission - Problem Statement 2**

---

## 📋 Project Overview

An AI-powered honeypot system that detects scam messages and autonomously engages scammers to extract actionable intelligence without revealing detection.

**Live Demo**: [Deploy Instructions](#-deployment)

---

## 🏗️ Architecture

### Two-Brain Agentic System

```
┌─────────────────────────────────────────────────────────┐
│                    Incoming Message                      │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │   Brain-1: Sentinel   │
         │   (Scam Detector)     │
         │  Regex + LLM Hybrid   │
         └───────────┬───────────┘
                     │
              Scam Detected?
                     │
        Yes ─────────┴────────── No
         │                        │
         ▼                        ▼
┌────────────────────┐    Return: Neutral Reply
│ Brain-2: Actor     │    (No Agent Engagement)
│ (Engagement Agent) │    
│ Llama-3.3-70b      │
└─────────┬──────────┘
          │
          ├─► Generate Persona Reply
          ├─► Extract Intelligence
          └─► Send GUVI Callback
```

---

## 🧠 Core Components

### 1. Brain-1: Sentinel (Scam Detector)
**File**: `app/brain1/sentinel.py`

**Method**: Hybrid Detection
- **Regex Patterns**: Urgency keywords, verification requests, account threats
- **LLM Analysis**: Semantic understanding of scam intent
- **Threshold**: 0.65 confidence triggers agent activation

### 2. Brain-2: Actor (Engagement Agent)
**File**: `app/brain2/actor.py`

**Persona**: Confused elderly retired railway clerk
- **AI Model**: Llama-3.3-70b (via Groq API)
- **Behavior**: 
  - *"I am having doubt, kindly tell me what is the procedur..."*

### 3. Intelligence Extraction
**File**: `app/utils/extraction.py`

**Extracts**:
- UPI IDs (`user@bank`, `+919876543210@paytm`)
- Bank Account Numbers (4-18 digits)
- Phishing URLs (`http://`, `.com`, `.in`)
- Phone Numbers
- Suspicious Keywords

---

## 🏆 Competitive Advantages

1. **Advanced AI**: High-performance Llama inference via Groq
2. **Hybrid Detection**: Robust combination of rule-based logic + LLM semantic analysis
3. **Robust Architecture**: Fallback safety mechanism
4. **100% Spec Compliance**: Exact match to problem statement

### 4. Mandatory Callback
**File**: `app/utils/callback.py`

Sends final intelligence to: `https://hackathon.guvi.in/api/updateHoneyPotFinalResult`

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Groq API Key (free from https://console.groq.com)

### Installation

```bash
# Clone/Navigate to project
cd "Scam Dectection"

# Install dependencies
pip install -r requirements.txt

# Configure environment
# Edit .env file:
API_KEY=your_secure_api_key
LLM_API_KEY=your_groq_api_key
LLM_MODEL=llama-3.3-70b-versatile
```

### Run Locally

```bash
# Terminal 1: Start API Server
python main.py

# Terminal 2: Run Simulation
python mock_scammer_simulation.py
```

**Expected Output**:
```
[Mock Scammer] Sending: Your bank account will be blocked...
[System Response] Status: success
[Agent]: I am having doubt, kindly tell me what is the reason...
```

---

## 📡 API Specification

### Endpoint
`POST /scam-event`

### Headers
```http
X-API-Key: your_api_key
Content-Type: application/json
```

### Request Body
```json
{
  "sessionId": "unique-session-id",
  "message": {
    "sender": "scammer",
    "text": "Your account will be blocked!",
    "timestamp": "2026-01-21T10:15:30Z"
  },
  "conversationHistory": [],
  "metadata": {
    "channel": "SMS",
    "language": "English",
    "locale": "IN"
  }
}
```

### Response
```json
{
  "status": "success",
  "reply": "Why is my account being suspended?"
}
```

> **Note**: Scam detection status, engagement metrics, and extracted intelligence are reported **only via the mandatory GUVI final result callback**, not in per-message API responses.

---

## ✅ Testing & Verification

### Local Test Results (Session: 476886fc)

| Turn | Input | Detection | Agent Response |
|------|-------|-----------|----------------|
| 1 | "Your bank account will be blocked..." | ✅ True | "I am having doubt, kindly tell me..." |
| 2 | "Share your UPI ID..." | ✅ True | "I am not understanding what is this UPI ID..." |
| 3 | "Why are you asking questions?" | ❌ False | (No reply - low confidence) |
| 4 | "Last warning. Police case..." | ✅ True | (Agent engaged) |

**Callback Status**: ✅ Sent successfully

**Latency**: < 1 second per turn (Groq acceleration)

---

## 🌐 Deployment

### Render.com (Recommended)

1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Agentic Honey-Pot Submission"
   git remote add origin https://github.com/YOUR_USERNAME/honeypot.git
   git push -u origin main
   ```

2. **Deploy on Render**:
   - Go to https://render.com → "New +" → "Web Service"
   - Connect GitHub repo
   - Set environment variables:
     - `LLM_API_KEY` = Your Groq key
     - `LLM_MODEL` = `llama-3.3-70b-versatile`
   - Click "Deploy"

3. **Get Public URL**: `https://your-app.onrender.com`

---

## 📁 Project Structure

```
Scam Dectection/
├── app/
│   ├── brain1/
│   │   └── sentinel.py          # Scam detection engine
│   ├── brain2/
│   │   └── actor.py              # Engagement agent
│   └── utils/
│       ├── llm_client.py         # Groq API integration
│       ├── extraction.py         # Intelligence extraction
│       ├── callback.py           # GUVI callback
│       └── patterns.py           # Regex patterns
├── main.py                       # FastAPI application
├── requirements.txt              # Dependencies
├── .env.example                  # Environment variables template
├── Procfile                      # Deployment config
├── render.yaml                   # Render.com config
├── IMPLEMENTATION.md             # Detailed documentation
└── mock_scammer_simulation.py    # Testing script
```

---

## 🔒 Security & Ethics

- ✅ No real person impersonation
- ✅ Generic "retired clerk" persona
- ✅ No illegal instructions
- ✅ Responsible data handling
- ✅ API key authentication
- ✅ Honeypot-only purpose

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| API Framework | FastAPI |
| AI Model | Groq Llama 3.3 70B |
| Detection | Regex + LLM Hybrid |
| Intelligence | Pattern Matching |
| Deployment | Render/Railway/Fly.io |

---

## 🏆 Competitive Advantages

1. **Advanced AI**: Groq Llama 3.3 70B (industry-leading performance)
2. **Hybrid Detection**: Best of rule-based + ML
3. **Robust Architecture**: Fallback safety if API fails
4. **100% Spec Compliance**: Exact match to problem statement
5. **Production Ready**: Full deployment configs included

---

## 📞 Support & Documentation

- **Implementation Details**: `IMPLEMENTATION.md`
- **Code Walkthrough**: `walkthrough.md` (in artifacts)

---

## 🎯 One-Line Summary

An AI-powered agentic honeypot API that detects scam messages, engages scammers in multi-turn conversations using Groq Llama 3.3 70B, extracts intelligence, and reports results to the GUVI evaluation system.

---

**Built for GUVI Hackathon - Problem Statement 2**
