"""
Agentic Honey-Pot API - Main Application Entry Point

This module implements a FastAPI-based scam detection system that:
1. Detects scam intent in incoming messages using a two-brain architecture
2. Autonomously engages scammers using an AI agent with a human persona
3. Extracts actionable intelligence from scam conversations
4. Reports results to evaluation endpoints

Author: GUVI Hackathon Submission
Version: 2.0.0
"""

from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
import os
import logging
from dotenv import load_dotenv

from app.brain1.sentinel import Sentinel
from app.brain2.actor import Actor
from app.utils.extraction import extract_intelligence
from app.utils.callback import send_final_result

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize FastAPI application
app = FastAPI(
    title="Agentic Honey-Pot API",
    description="AI-powered scam detection and autonomous engagement system",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Security configuration
API_KEY_NAME = "X-API-Key"
API_KEY = os.getenv("API_KEY", "default_insecure_key_change_me")


async def get_api_key(api_key: str = Header(..., alias=API_KEY_NAME)) -> str:
    """
    Validate API key from request headers.
    
    Args:
        api_key: API key provided in X-API-Key header
        
    Returns:
        str: Validated API key
        
    Raises:
        HTTPException: 403 if API key is invalid
    """
    if api_key != API_KEY:
        logger.warning(f"Invalid API key attempt: {api_key[:10]}...")
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key


# --- Data Models ---

class Message(BaseModel):
    """Represents a single message in a conversation."""
    sender: str = Field(..., description="Message sender: 'scammer' or 'user'")
    text: str = Field(..., description="Message content")
    timestamp: str = Field(..., description="ISO-8601 formatted timestamp")


class Metadata(BaseModel):
    """Optional metadata about the conversation channel."""
    channel: Optional[str] = Field("SMS", description="Communication channel")
    language: Optional[str] = Field("English", description="Message language")
    locale: Optional[str] = Field("IN", description="Geographic locale")


class ScamEventRequest(BaseModel):
    """Request payload for scam event analysis."""
    sessionId: str = Field(..., description="Unique session identifier")
    message: Message = Field(..., description="Current incoming message")
    conversationHistory: List[Message] = Field(
        default=[],
        description="Previous messages in the conversation"
    )
    metadata: Optional[Metadata] = Field(None, description="Optional conversation metadata")


class AgentOutput(BaseModel):
    """API response for scam event processing."""
    status: str = Field(..., description="Processing status")
    reply: Optional[str] = Field(None, description="Agent's response message")


# Initialize AI brains
logger.info("Initializing AI components...")
sentinel = Sentinel()
actor = Actor()
logger.info("AI components initialized successfully")


@app.post("/scam-event", response_model=AgentOutput)
async def handle_scam_event(
    payload: ScamEventRequest,
    api_key: str = Depends(get_api_key)
) -> AgentOutput:
    """
    Process incoming message for scam detection and autonomous engagement.
    
    This endpoint implements a three-stage pipeline:
    1. Brain-1 (Sentinel): Detects scam intent using hybrid detection
    2. Brain-2 (Actor): Engages scammer if detected
    3. Intelligence Extraction: Extracts and reports scam intelligence
    
    Args:
        payload: Scam event request containing message and history
        api_key: Validated API key from dependency injection
        
    Returns:
        AgentOutput: Contains status and optional agent reply
        
    Raises:
        HTTPException: 500 if processing fails
    """
    try:
        logger.info(f"Processing scam event for session: {payload.sessionId}")
        
        # Stage 1: Scam Detection (Brain-1: Sentinel)
        analysis = sentinel.analyze(payload.message.text)
        is_scam = analysis["is_scam"]
        confidence = analysis["confidence"]
        
        logger.info(
            f"Session {payload.sessionId} - "
            f"Scam detected: {is_scam}, Confidence: {confidence}"
        )
        
        agent_reply = None
        extracted = {}
        
        # Stage 2: Agent Engagement (Brain-2: Actor)
        if is_scam and confidence >= 0.65:
            logger.info(f"Session {payload.sessionId} - Activating engagement agent")
            
            # Convert history to dictionary format
            history_dicts = [m.model_dump() for m in payload.conversationHistory]
            
            # Generate contextual response
            agent_reply = actor.engage(payload.message.text, history_dicts)
            logger.info(f"Session {payload.sessionId} - Agent generated response")
            
            # Stage 3: Intelligence Extraction & Callback
            extracted = extract_intelligence(payload.message.text)
            logger.info(
                f"Session {payload.sessionId} - "
                f"Extracted intelligence: {len(extracted.get('upi_ids', []))} UPIs, "
                f"{len(extracted.get('bank_accounts', []))} accounts"
            )
            
            # Send mandatory callback to evaluation endpoint
            total_messages = len(payload.conversationHistory) + 1
            send_final_result(
                session_id=payload.sessionId,
                scam_detected=True,
                total_messages=total_messages,
                intelligence=extracted
            )
            logger.info(f"Session {payload.sessionId} - Callback sent successfully")
        
        return AgentOutput(
            status="success",
            reply=agent_reply
        )
        
    except Exception as e:
        logger.error(
            f"Error processing session {payload.sessionId}: {str(e)}",
            exc_info=True
        )
        raise HTTPException(
            status_code=500,
            detail="Internal server error processing scam event"
        )


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint for monitoring.
    
    Returns:
        Dict: Health status
    """
    return {"status": "healthy", "service": "agentic-honeypot"}


if __name__ == " __main__":
    import uvicorn
    
    logger.info("Starting Agentic Honey-Pot API server...")
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8001,
        log_level="info"
    )
