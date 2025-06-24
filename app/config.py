"""
Configuration module for Daily Motivation Bot.
Handles environment variables and application settings.
"""

import os
from typing import Dict, Optional

from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""
    
    # SMTP Configuration
    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.mail.yahoo.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: Optional[str] = os.getenv("SMTP_USER")
    SMTP_PASSWORD: Optional[str] = os.getenv("SMTP_PASSWORD")
    
    # Email Configuration
    GIRLFRIEND_EMAIL: Optional[str] = os.getenv("GIRLFRIEND_EMAIL")
    SENDER_NAME: str = os.getenv("SENDER_NAME", "Mehdi")
    
    # Groq API Configuration
    GROQ_API_KEY: Optional[str] = os.getenv("GROQ_API_KEY")
    GROQ_API_URL: str = "https://api.groq.com/openai/v1/chat/completions"
    GROQ_MODEL: str = "llama-3.1-8b-instant"
    GROQ_TEMPERATURE: float = 0.9
    GROQ_MAX_TOKENS: int = 200
    
    @classmethod
    def get_required_vars(cls) -> Dict[str, Optional[str]]:
        """Get dictionary of required environment variables."""
        return {
            "SMTP_USER": cls.SMTP_USER,
            "SMTP_PASSWORD": cls.SMTP_PASSWORD,
            "GIRLFRIEND_EMAIL": cls.GIRLFRIEND_EMAIL,
            "GROQ_API_KEY": cls.GROQ_API_KEY,
        }
    
    @classmethod
    def validate_config(cls) -> None:
        """Validate that all required environment variables are set."""
        required_vars = cls.get_required_vars()
        missing_vars = [var for var, value in required_vars.items() if not value]
        
        if missing_vars:
            print(f"⚠️  WARNING: Missing required environment variables: {', '.join(missing_vars)}")
        else:
            print("✅ All required environment variables are set")


# Initialize settings and validate on import
settings = Settings()
settings.validate_config()

