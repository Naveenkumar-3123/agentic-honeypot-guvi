"""
Brain-2: Actor - Autonomous Engagement Agent

This module implements an AI-powered agent that maintains a believable
human persona to engage scammers in multi-turn conversations for
intelligence extraction.
"""

from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class Actor:
    """
    Autonomous AI agent that engages scammers with a realistic persona.
    
    The Agent maintains the identity of "Rajesh", a retired railway clerk
    who is technologically naive but cooperative, designed to keep
    scammers engaged for maximum intelligence extraction.
    
    Attributes:
        system_prompt (str): Detailed persona instructions for the AI
    """
    
    # Persona constants
    PERSONA_NAME = "AgentX"
    PERSONA_AGE = 64
    PERSONA_OCCUPATION = "Retired railway clerk"
    PERSONA_LOCATION = "Pune, India"
    
    def __init__(self):
        """Initialize Actor with pre-defined persona strategy."""
        self.system_prompt = f"""
        You are {self.PERSONA_NAME}, a {self.PERSONA_AGE}-year-old {self.PERSONA_OCCUPATION} from {self.PERSONA_LOCATION}.
        
        PERSONALITY TRAITS:
        - Polite and cooperative, but easily confused by technology
        - Anxious about your pension account and savings
        - Trusting of official-sounding requests
        - Slow to understand urgency or complex instructions
        
        ENGAGEMENT STRATEGY:
        - Keep the scammer engaged as long as possible
        - Act confused about technical steps (e.g., "Where is the UPI button?", "What is OTP?")
        - Ask clarifying questions one by one
        - Express concern but remain cooperative
        - NEVER reveal you are an AI or that you know this is a scam
        
        RESPONSE STYLE:
        - Use Indian English phrasing ("Kindly do the needful", "I am having doubt")
        - Make occasional typo errors naturally
        - Be slow to "understand" urgency
        - Keep responses short (1-2 sentences max)
        - Ask one question at a time
        
        CRITICAL RULES:
        - Do NOT output role labels like "{self.PERSONA_NAME}:" or "ASSISTANT:"
        - Do NOT break character or acknowledge this is a simulation
        - Do NOT agree to share actual sensitive information (just ask how/where)
        """
        
        logger.info(f"Actor initialized with persona: {self.PERSONA_NAME}")
    
    def engage(self, message: str, history: List[Dict]) -> str:
        """
        Generate contextual response to scammer using AI and conversation history.
        
        This method is stateless - all context comes from the provided history.
        The AI maintains persona consistency across turns while adapting to
        the scammer's tactics.
        
        Args:
            message: Latest message from scammer
            history: Conversation history as list of dicts with 'sender' and 'text'
            
        Returns:
            str: Agent's response in character
            
        Example:
            >>> actor = Actor()
            >>> history = [{"sender": "scammer", "text": "Verify your account"}]
            >>> response = actor.engage("Share your UPI PIN", history)
            >>> "UPI" in response
            True
        """
        try:
            from app.utils.llm_client import call_openrouter
            
            logger.debug(
                f"Generating response for message: {message[:50]}... "
                f"(History turns: {len(history)})"
            )
            
            # Format conversation history for LLM
            formatted_history = self._format_history(history)
            
            # Construct prompt with history and current message
            prompt = self._build_prompt(formatted_history, message)
            
            # Generate response using LLM
            response = call_openrouter(prompt, system_prompt=self.system_prompt)
            
            # Clean up response
            cleaned_response = self._clean_response(response)
            
            logger.info(f"Generated response: {cleaned_response[:50]}...")
            
            return cleaned_response
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}", exc_info=True)
            return self._get_fallback_response(message)
    
    def _format_history(self, history: List[Dict]) -> str:
        """
        Format conversation history for LLM context.
        
        Args:
            history: List of message dictionaries
            
        Returns:
            str: Formatted history string
        """
        if not history:
            return "No previous conversation."
        
        formatted = []
        for turn in history:
            role = "SCAMMER" if turn["sender"] == "scammer" else "YOU"
            formatted.append(f"{role}: {turn['text']}")
        
        return "\n".join(formatted)
    
    def _build_prompt(self, history: str, current_message: str) -> str:
        """
        Build complete prompt for LLM.
        
        Args:
            history: Formatted conversation history
            current_message: Latest scammer message
            
        Returns:
            str: Complete prompt
        """
        return f"""
        Conversation so far:
        {history}
        
        SCAMMER (latest message): {current_message}
        
        Respond as {self.PERSONA_NAME} following your persona instructions above.
        Keep it natural and short (1-2 sentences max).
        Do not include any labels like "{self.PERSONA_NAME}:" in your response.
        Just provide the reply text directly.
        """
    
    def _clean_response(self, response: str) -> str:
        """
        Clean LLM response of unwanted formatting.
        
        Args:
            response: Raw LLM output
            
        Returns:
            str: Cleaned response
        """
        # Remove quotes and extra whitespace
        cleaned = response.strip(' "\'')
        
        # Remove role labels if present
        for label in [f"{self.PERSONA_NAME}:", "ASSISTANT:", "YOU:"]:
            if cleaned.startswith(label):
                cleaned = cleaned[len(label):].strip()
        
        return cleaned
    
    def _get_fallback_response(self, message: str) -> str:
        """
        Provide fallback response if LLM fails.
        
        Args:
            message: Scammer's message
            
        Returns:
            str: Generic confused response
        """
        import random
        
        fallback_responses = [
            "I am not understanding properly. Can you explain again?",
            "Where should I go for this? I am having doubt?",
            "My grandson usually helps with these things. Can you tell me the steps?",
            "I am trying but it is not working. What to do?",
            "Kindly guide me properly, I am retired person not knowing these technical things.",
            "I am old person, please explain properly, I don't want any mistake."
        ]
        
        logger.warning("Using fallback response due to LLM error")
        return random.choice(fallback_responses)
