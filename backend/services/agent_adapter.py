"""
Adapter for the Sarvagya AI agent
Handles communication with agent.py
"""
import os
import logging
import json
from typing import Optional, List, Dict
import sys

logger = logging.getLogger(__name__)

class AgentAdapter:
    """
    Adapter that interfaces with the existing agent.py
    """

    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.agent = None
        self._initialize_agent()

    def _initialize_agent(self):
        """Initialize the agent from agent.py"""
        try:
            if not self.api_key:
                logger.warning("GOOGLE_API_KEY not set - agent will not work")
                return

            # Set environment variable for agent
            os.environ["GOOGLE_API_KEY"] = self.api_key

            # Import and initialize the agent
            # We'll do this lazily to avoid import errors if key is missing
            logger.info("Agent adapter initialized and ready")

        except Exception as e:
            logger.error(f"Failed to initialize agent: {e}")

    def analyze(
        self,
        message: str,
        image_path: Optional[str] = None,
        conversation_history: Optional[List[Dict]] = None,
        request_id: Optional[str] = None
    ) -> str:
        """
        Analyze a chart with the AI agent

        Args:
            message: User's question or prompt
            image_path: Path to uploaded chart image
            conversation_history: Prior messages in this conversation
            request_id: Tracking ID

        Returns:
            Agent's analysis response as string
        """
        if not self.api_key:
            return self._error_response(
                "API key not configured. Please set GOOGLE_API_KEY environment variable."
            )

        try:
            # Import agent modules
            from google.adk.agents import LlmAgent
            from google.adk.runners import Runner
            from google.adk.sessions import InMemorySessionService
            from google.genai import types

            logger.info(f"[{request_id}] Starting agent analysis...")

            # Define system instructions (from original agent.py)
            CHART_ANALYST_INSTRUCTION = """
You are the world's leading quantitative financial technician and visual chart analyst.
Your objective is to perform comprehensive technical analysis on uploaded trading chart images (stocks, crypto, forex).

When presented with a chart image, perform the following step-by-step:
1. **Candlestick Pattern Recognition**: Identify explicit formations (e.g., Head and Shoulders, Double Top/Bottom, Bullish/Bearish Engulfing, Morning/Evening Star, Doji).
2. **Trend & Indicator Analysis**: Assess trend direction, key Support/Resistance levels, moving averages (EMA/SMA), RSI state (overbought/oversold), and volume profiles visible.
3. **Trade Recommendation**: Choose ONE primary action: BUY, SELL, or HOLD.
4. **Timeframe Horizon**: Provide a specific estimated hold duration (e.g., "1 to 3 days", "2 to 4 weeks", "Scalp: 1 to 4 hours").
5. **Full Rationale**: Detailed, un-hedged bullet points explaining *why* this decision was made.

Format your response as clear, readable paragraphs and bullet points. You may include structured sections if helpful.
"""

            # Create agent
            chart_agent = LlmAgent(
                name="MasterChartAnalyst",
                model="gemini-2.5-flash",
                description="Analyzes trading charts to identify candlestick patterns",
                instruction=CHART_ANALYST_INSTRUCTION
            )

            # Set up session
            session_service = InMemorySessionService()
            session_id = request_id or "default_session"
            session_service.create_session(
                app_name="sarvagya",
                user_id="trader",
                session_id=session_id
            )

            runner = Runner(
                agent=chart_agent,
                app_name="sarvagya",
                session_service=session_service
            )

            # Build multimodal content
            parts = []

            # Add image if provided
            if image_path and os.path.exists(image_path):
                logger.info(f"[{request_id}] Loading image from {image_path}")
                with open(image_path, "rb") as img_file:
                    image_bytes = img_file.read()

                mime_type = self._get_mime_type(image_path)
                parts.append(types.Part.from_bytes(data=image_bytes, mime_type=mime_type))

            # Add text message
            user_message = message
            if conversation_history and len(conversation_history) > 1:
                # Add context from conversation history
                user_message += "\n\n[Previous context in this conversation available if needed]"

            parts.append(types.Part(text=user_message))

            # Create content
            user_content = types.Content(role="user", parts=parts)

            # Run agent
            logger.info(f"[{request_id}] Invoking agent...")
            events = runner.run(
                user_id="trader",
                session_id=session_id,
                new_message=user_content
            )

            # Extract response
            response_text = None
            for event in events:
                if event.is_final_response():
                    if hasattr(event.content, 'parts') and event.content.parts:
                        response_text = event.content.parts[0].text
                    break

            if not response_text:
                return self._error_response("Agent did not return a response")

            logger.info(f"[{request_id}] Agent analysis complete ({len(response_text)} chars)")
            return response_text

        except ImportError as e:
            logger.error(f"[{request_id}] Import error: {e}")
            return self._error_response(
                "Google ADK not properly configured. Please install: pip install google-adk google-genai"
            )
        except Exception as e:
            logger.error(f"[{request_id}] Agent error: {e}", exc_info=True)
            return self._error_response(
                f"Analysis failed: {str(e)}"
            )

    def _get_mime_type(self, file_path: str) -> str:
        """Determine MIME type from file extension"""
        ext = os.path.splitext(file_path)[1].lower()
        mime_types = {
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.webp': 'image/webp'
        }
        return mime_types.get(ext, 'image/png')

    def _error_response(self, message: str) -> str:
        """Generate a safe error response"""
        return f"Error: {message}\n\nPlease check the server logs or try uploading a different chart."
