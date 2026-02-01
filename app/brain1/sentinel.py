"""
Brain-1: Sentinel - Scam Detection Engine

This module implements a hybrid scam detection system combining:
1. Rule-based pattern matching for known scam signals
2. LLM-powered semantic analysis for contextual understanding

The Sentinel analyzes incoming messages and determines scam probability
with a confidence score to trigger autonomous engagement.
"""

import os
import requests
import json
import logging
from typing import Dict, Any
from app.utils.patterns import check_rule_based_signals

logger = logging.getLogger(__name__)


class Sentinel:
    """
    Hybrid scam detection engine using rule-based and AI analysis.
    
    Attributes:
        llm_api_key (str): API key for LLM service
        llm_model (str): Model identifier for LLM
        confidence_threshold (float): Minimum confidence to classify as scam
    """
    
    # Class constants
    CONFIDENCE_THRESHOLD = 0.6
    LLM_WEIGHT = 0.8
    RULES_WEIGHT = 0.2
    
    def __init__(self):
        """Initialize Sentinel with configuration from environment."""
        self.llm_api_key = os.getenv("LLM_API_KEY")
        self.llm_model = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")
        
        if not self.llm_api_key:
            logger.warning("LLM_API_KEY not set - using fallback detection only")
        
        logger.info(f"Sentinel initialized with model: {self.llm_model}")
    
    def analyze(self, message: str) -> Dict[str, Any]:
        """
        Analyze message for scam intent using hybrid detection.
        
        Combines rule-based pattern matching (20% weight) with LLM semantic
        analysis (80% weight) to produce a final confidence score.
        
        Args:
            message: Incoming message text to analyze
            
        Returns:
            Dict containing:
                - is_scam (bool): Whether message is classified as scam
                - confidence (float): Detection confidence (0.0-1.0)
                - reason (str): Human-readable explanation
                - signals (dict): Rule-based signals detected
                
        Example:
            >>> sentinel = Sentinel()
            >>> result = sentinel.analyze("Share your UPI PIN now!")
            >>> result['is_scam']
            True
            >>> result['confidence']
            0.92
        """
        logger.debug(f"Analyzing message: {message[:50]}...")
        
        # Stage 1: Rule-based signal detection
        signals = check_rule_based_signals(message)
        base_score = self._calculate_rule_score(signals)
        
        logger.debug(f"Rule-based score: {base_score}, Signals: {signals}")
        
        # Stage 2: LLM semantic analysis
        llm_result = self._call_llm(message, signals)
        
        # Stage 3: Weighted combination
        final_confidence = min(
            (llm_result["confidence"] * self.LLM_WEIGHT) + 
            (base_score * self.RULES_WEIGHT),
            1.0
        )
        
        is_scam = final_confidence > self.CONFIDENCE_THRESHOLD
        
        result = {
            "is_scam": is_scam,
            "confidence": round(final_confidence, 2),
            "reason": llm_result["reason"],
            "signals": signals
        }
        
        logger.info(
            f"Analysis complete - Scam: {is_scam}, "
            f"Confidence: {result['confidence']}"
        )
        
        return result
    
    def _calculate_rule_score(self, signals: Dict[str, bool]) -> float:
        """
        Calculate base confidence score from rule-based signals.
        
        Args:
            signals: Dictionary of detected signals
            
        Returns:
            float: Base score between 0.0 and 1.0
        """
        score = 0.0
        if signals.get("payment_keywords"):
            score += 0.3
        if signals.get("urgency_keywords"):
            score += 0.3
        if signals.get("contains_url"):
            score += 0.2
        if signals.get("upi_scam_specific"):
            score += 0.4  # strong indicator
        
        return min(score, 1.0)
    
    def _call_llm(self, message: str, signals: Dict[str, bool]) -> Dict[str, Any]:
        """
        Call LLM for semantic scam analysis.
        
        Args:
            message: Message text to analyze
            signals: Pre-detected rule-based signals
            
        Returns:
            Dict with 'confidence' (float) and 'reason' (str)
        """
        try:
            from app.utils.llm_client import call_openrouter
            
            system_prompt = """
            You are a Scam Detection Engine. Analyze the user's message for scam intent.
            Output MUST be valid JSON with keys: "confidence" (0.0 to 1.0) and "reason" (string).
            
            Scam categories to detect:
            - Phishing/credential theft
            - Investment/lottery scams
            - Urgent payment requests
            - KYC/verification fraud
            - Impersonation (bank/government)
            
            If the message appears legitimate, confidence should be low (< 0.3).
            """
            
            prompt = f"""
            Analyze this message for scam intent: "{message}"
            
            Pre-detected signals: {signals}
            
            Return ONLY valid JSON format:
            {{"confidence": 0.0-1.0, "reason": "brief explanation"}}
            """
            
            logger.debug("Calling LLM for analysis...")
            response_text = call_openrouter(prompt, system_prompt=system_prompt)
            
            # Parse JSON response
            cleaned_text = response_text.replace("```json", "").replace("```", "").strip()
            data = json.loads(cleaned_text)
            
            return {
                "confidence": float(data.get("confidence", 0.5)),
                "reason": data.get("reason", "LLM Analysis")
            }
            
        except Exception as e:
            logger.warning(f"LLM call failed: {str(e)} - Using fallback logic")
            return self._fallback_logic(message, signals)
    
    def _fallback_logic(self, message: str, signals: Dict[str, bool]) -> Dict[str, Any]:
        """
        Heuristic fallback when LLM is unavailable.
        
        Args:
            message: Message text
            signals: Detected signals
            
        Returns:
            Dict with confidence and reason
        """
        signal_count = sum(signals.values())
        
        # High-risk: Payment request
        if signals.get("payment_keywords"):
            return {
                "confidence": 0.85,
                "reason": "Explicit payment/credential request detected (High Risk)"
            }
        
        # Medium-risk: Multiple signals
        if signal_count >= 2:
            return {
                "confidence": 0.75,
                "reason": "Multiple scam indicators present (urgency + payment/URL)"
            }
            
        # Medium-risk: Urgency detected (even alone, it's suspicious in this context)
        if signals.get("urgency_keywords"):
             return {
                "confidence": 0.65, # Just enough to trigger agent
                "reason": "High urgency detected - engaging to delay/clarify."
            }
        
        # Low-risk: Other single signal
        if signal_count == 1:
            return {
                "confidence": 0.50,
                "reason": "Single suspicious indicator, context unclear"
            }
        
        # Minimal risk
        return {
            "confidence": 0.10,
            "reason": "No obvious scam patterns detected"
        }
