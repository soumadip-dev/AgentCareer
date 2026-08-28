"""Configure module
Loads environment variables used across the project
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Central Configuration class"""

    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "gemini-2.5-flash-lite")

    @staticmethod
    def validate() -> None:
        """Validate mandatory configurations"""
        if not Config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is missing. Please check your .env file.")
