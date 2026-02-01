# Deployment Guide - Agentic Honey-Pot

## 🚀 Quick Deploy Options

### Option 1: Render.com (Recommended - Easiest)

1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/scam-detection.git
   git push -u origin main
   ```

2. **Deploy on Render**:
   - Go to https://render.com
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Render auto-detects `render.yaml`
   - Set environment variables:
     - `LLM_API_KEY` = Your Groq key
     - `LLM_MODEL` = `llama-3.3-70b-versatile`
   - Click "Deploy"

3. **Get Public URL**:
   - Example: `https://scam-detection-api.onrender.com`

### Option 2: Railway.app

1. **Push to GitHub** (same as above)

2. **Deploy**:
   - Go to https://railway.app
   - "New Project" → "Deploy from GitHub"
   - Select your repo
   - Add environment variables:
     - `API_KEY` = (auto-generated or set manually)
     - `LLM_API_KEY` = Your Groq key
     - `LLM_MODEL` = llama-3.3-70b-versatile

3. **Get Public URL**:
   - Railway provides: `https://YOUR_APP.railway.app`

### Option 3: Fly.io

1. **Install Fly CLI**:
   ```bash
   powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
   ```

2. **Deploy**:
   ```bash
   fly launch --name scam-detection-api
   fly secrets set LLM_API_KEY=your_groq_key
   fly secrets set API_KEY=your_secure_key
   fly deploy
   ```

## ✅ Post-Deployment

### Test Your API:
```bash
curl -X POST https://YOUR_PUBLIC_URL/scam-event \
  -H "X-API-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "sessionId": "test-001",
    "message": {
      "sender": "scammer",
      "text": "Your account will be blocked!",
      "timestamp": "2026-01-21T10:15:30Z"
    },
    "conversationHistory": []
  }'
```

### Submit to GUVI:
Provide your public URL in the hackathon portal:
- Example: `https://scam-detection-api.onrender.com`

## 📝 Important Notes

- **Free Tier Limits**: Render/Railway free tier may sleep after inactivity
- **First Request**: May take 30-60s to wake up
- **Groq Key**: Must be set as environment variable
- **API Key**: Set a secure key for authentication
