# IMPLEMENTATION.md
## Agentic Honey-Pot for Scam Detection & Intelligence Extraction

---

## 1. Introduction

Online scams such as bank fraud, UPI fraud, phishing, and fake offers are increasingly adaptive. Scammers dynamically change their tactics based on user responses, making static detection systems ineffective.

This project implements an **AI-powered Agentic Honey-Pot system** that detects scam intent and autonomously engages scammers in realistic multi-turn conversations to extract actionable intelligence **without revealing detection**.

The system is designed in full compliance with the GUVI Hackathon Problem Statement – Problem 2.

---

## 2. Objective

The primary objectives of the system are to:

- Detect scam or fraudulent intent in incoming messages
- Activate an autonomous AI agent upon scam detection
- Maintain a believable human-like persona
- Handle multi-turn conversations using conversation history
- Extract scam-related intelligence
- Return structured API responses
- Send a **mandatory final result callback** to GUVI for evaluation

---

## 3. System Architecture

The system follows a **two-brain agentic architecture**:

### Brain-1: Scam Detection Engine
Responsible for:
- Analyzing incoming messages
- Detecting scam intent using hybrid logic
- Evaluating scam intent using hybrid rule-based and AI-assisted logic with a predefined confidence threshold to trigger agent handoff
- Triggering agent handoff

### Brain-2: Autonomous AI Agent
Responsible for:
- Maintaining a realistic human persona
- Engaging scammers autonomously
- Handling multi-turn conversations
- Adapting responses dynamically
- Extracting scam intelligence
- Performing self-correction
- Avoiding exposure of detection

---

## 4. Technology Stack (Free & Open)

| Component | Technology |
|-----------|------------|
| API Framework | FastAPI |
| AI Model | Groq Llama 3.3 70B |
| Detection | Hybrid (Regex + LLM) |
| Extraction | Regex-based patterns |
| Callback | GUVI Endpoint |
| Conversation Memory | Platform-provided conversationHistory with optional internal session state |
| Intelligence Extraction | Regex + rule-based logic |
| Deployment | Render / Railway / Fly.io (Free tier) |

---

## 5. API Authentication

All requests must include:

x-api-key: YOUR_SECRET_API_KEY
Content-Type: application/json


Requests without a valid API key are rejected.

---

## 6. API Request Format (Input)

Each API request represents **one message event** in a conversation.

### 6.1 First Message (Start of Conversation)

```json
{
  "sessionId": "wertyu-dfghj-ertyui",
  "message": {
    "sender": "scammer",
    "text": "Your bank account will be blocked today. Verify immediately.",
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

### 6.2 Follow-Up Message
```json
{
  "sessionId": "wertyu-dfghj-ertyui",
  "message": {
    "sender": "scammer",
    "text": "Share your UPI ID to avoid account suspension.",
    "timestamp": "2026-01-21T10:17:10Z"
  },
  "conversationHistory": [
    {
      "sender": "scammer",
      "text": "Your bank account will be blocked today. Verify immediately.",
      "timestamp": "2026-01-21T10:15:30Z"
    },
    {
      "sender": "user",
      "text": "Why will my account be blocked?",
      "timestamp": "2026-01-21T10:16:10Z"
    }
  ],
  "metadata": {
    "channel": "SMS",
    "language": "English",
    "locale": "IN"
  }
}
```

---

## 7. Processing Flow
1. Platform sends an incoming message event
2. Scam Detection Engine analyzes the message
3. **If scam intent is detected:**
    - Autonomous AI Agent is activated
    - Agent uses provided conversationHistory to continue the interaction
    - Responses are generated dynamically
    - Intelligence is extracted incrementally
    - Agent reply is returned for this API call
4. **Once sufficient intelligence is collected and engagement criteria are met:**
    - Final result callback is sent to GUVI

---

## 8. Agent Behavior Expectations
The AI Agent is designed to:
- Handle multi-turn conversations
- Adapt responses dynamically
- Behave like a real human
- Use polite, cautious, and cooperative language
- Perform self-correction if needed
- **Avoid revealing scam detection at all times**

---

## 9. Agent API Output (Per API Call)
Each API call returns the agent’s reply in the required format:

```json
{
  "status": "success",
  "reply": "Why is my account being suspended?"
}
```

---

## 10. Intelligence Extraction
The system extracts the following intelligence:
- Bank account numbers
- UPI IDs
- Phishing URLs
- Phone numbers
- Suspicious keywords (e.g., urgency terms)

Extraction uses a combination of:
- Regular expressions
- Keyword analysis
- Context-aware parsing

---

## 11. Mandatory Final Result Callback (VERY IMPORTANT)
Once scam intent is confirmed and engagement is completed, the system must send a callback to the GUVI evaluation endpoint.

**Callback Endpoint**
`POST https://hackathon.guvi.in/api/updateHoneyPotFinalResult`

**Payload Format**
```json
{
  "sessionId": "abc123-session-id",
  "scamDetected": true,
  "totalMessagesExchanged": 18,
  "extractedIntelligence": {
    "bankAccounts": ["XXXX-XXXX-XXXX"],
    "upiIds": ["scammer@upi"],
    "phishingLinks": ["http://malicious-link.example"],
    "phoneNumbers": ["+91XXXXXXXXXX"],
    "suspiciousKeywords": ["urgent", "verify now", "account blocked"]
  },
  "agentNotes": "Scammer used urgency tactics and payment redirection"
}
```

**When This Is Sent**
The callback is triggered only when:
- Scam intent is confirmed
- Autonomous agent engagement is sufficient
- Intelligence extraction is complete
The callback is triggered only once per session and represents the final outcome of the conversation lifecycle.

⚠️ *If this callback is not sent, the submission will not be evaluated.*

---

## 12. Evaluation Criteria Alignment
| Evaluation Metric | Implementation |
|-------------------|----------------|
| Scam detection accuracy | Hybrid detection logic |
| Agentic engagement | Groq Llama 3.3 70B autonomous agent |
| Intelligence extraction | Structured extraction engine |
| API stability | FastAPI + stateless design |
| Ethical behavior | Silent detection, no exposure |

---

## 13. Ethics & Constraints
The system strictly follows ethical constraints:
- ❌ No impersonation of real individuals
- ❌ No illegal instructions
- ❌ No harassment
- ✅ Responsible data handling
- ✅ Simulated scammer interactions only

---

## 14. Deployment
The API is deployed as a public HTTPS endpoint using a free-tier cloud platform.

---

## 15. Final One-Line Summary
An AI-powered agentic honeypot API that detects scam messages, engages scammers in multi-turn conversations, extracts actionable intelligence, and reports final results to the GUVI evaluation system.
