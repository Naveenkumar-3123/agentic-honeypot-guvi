"""
LLM Client - Groq API Integration

Handles communication with Groq LLM API for scam detection and agent engagement.
Automatically detects Groq API keys and routes to appropriate endpoint.
"""

import os
import requests
import json
import logging
from typing import Optional

logger = logging.getLogger(__name__)


def call_openrouter(prompt: str, system_prompt: Optional[str] = None, model: str = None) -> str:
    """
    Makes a request to Groq LLM API.
    
    Args:
        prompt: User prompt / message to analyze
        system_prompt: Optional system instructions for the LLM
        model: Optional model override (defaults to LLM_MODEL env var)
        
    Returns:
        str: LLM response text or fallback response on error
    """
    api_key = os.getenv("LLM_API_KEY")
    if not api_key:
        logger.error("LLM_API_KEY not found in environment")
        return "Error: No LLM_API_KEY found."
    
    target_model = model or os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    
    payload = {
        "model": target_model,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1000
    }
    
    # Auto-detect API endpoint based on key format
    target_url = "https://openrouter.ai/api/v1/chat/completions"
    if api_key.startswith("gsk_"):
        target_url = "https://api.groq.com/openai/v1/chat/completions"
    
    logger.debug(f"Calling LLM API: {target_url}")
    
    import time
    
    max_retries = 1
    for attempt in range(max_retries):
        try:
            response = requests.post(target_url, headers=headers, json=payload, timeout=5)
            
            # Handle rate limiting
            if response.status_code == 429:
                if attempt < max_retries - 1:
                    logger.warning(f"Rate limited (429). Retrying in 1s... ({attempt+1}/{max_retries})")
                    time.sleep(1)
                    continue
                else:
                    raise Exception("Rate limit (429) exceeded")
            
            response.raise_for_status()
            data = response.json()
            
            if "choices" in data and len(data["choices"]) > 0:
                result = data["choices"][0]["message"]["content"]
                logger.debug(f"LLM response received: {result[:50]}...")
                return result
            
            logger.error("Invalid LLM response structure")
            return "Error: Invalid response from LLM API."
            
        except Exception as e:
            error_msg = str(e)
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"LLM API error: {e.response.text}")
            
            logger.warning(f"LLM call failed: {error_msg} - Using fallback response")
            
            # Fallback responses for stability
            import random
            fallbacks = [
                "I am not understanding nicely. My grandson handles these things usually.",
                "Sir, I am a retired person. Please explain slowly.",
                "Why is it so urgent? I need to ask my son first.",
                "I am trying to open the link but it is not working properly."
            ]
            return random.choice(fallbacks)
