"""
Gemini Service

Responsibilities:
1. Initialize the Gemini API client.
2. Send prompts to the Gemini API.
3. Return the complete Gemini API response.
4. Keep Gemini-specific API code isolated from agents.
"""

from typing import Any, Optional

from google import genai

from config import Config


class GeminiService:
    """Wrapper around the Gemini API."""

    def __init__(self):
        Config.validate()
        self.gemini_client = genai.Client(api_key=Config.GEMINI_API_KEY)

    def generate_response(
        self,
        prompt: str,
        config: Optional[Any] = None,
    ) -> Any:
        """
        Send a prompt to the Gemini API and return its response.

        Args:
            prompt: The prompt to send to the Gemini API.
            config: Optional configuration for content generation.

        Returns:
            The complete response returned by the Gemini API.

        Raises:
            RuntimeError: If the Gemini API request fails.
        """
        try:
            response = self.gemini_client.models.generate_content(
                model=Config.MODEL_NAME,
                contents=prompt,
                config=config,
            )

            return response

        except Exception as ex:
            raise RuntimeError(f"Gemini API Error: {ex}") from ex
