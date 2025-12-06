"""
Configuration module for Daily Motivation Bot.
Handles environment variables and application settings.
"""

import os
from typing import Dict, List, Optional

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
    RECIPIENT_EMAILS: List[str] = [
        email.strip() 
        for email in os.getenv("RECIPIENT_EMAILS", "").split(",") 
        if email.strip()
    ] if os.getenv("RECIPIENT_EMAILS") else []
    SENDER_NAME: str = os.getenv("SENDER_NAME", "Mehdi")
    
    # Scheduler Configuration
    SCHEDULE_HOUR: int = int(os.getenv("SCHEDULE_HOUR", "6"))
    SCHEDULE_MINUTE: int = int(os.getenv("SCHEDULE_MINUTE", "30"))
    
    # Groq API Configuration
    GROQ_API_KEY: Optional[str] = os.getenv("GROQ_API_KEY")
    GROQ_API_URL: str = "https://api.groq.com/openai/v1/chat/completions"
    GROQ_MODEL: str = "llama-3.1-8b-instant"
    GROQ_TEMPERATURE: float = 0.9
    GROQ_MAX_TOKENS: int = 200
    
    @classmethod
    def get_recipient_emails(cls) -> List[str]:
        """Get list of recipient emails, prioritizing RECIPIENT_EMAILS over GIRLFRIEND_EMAIL."""
        if cls.RECIPIENT_EMAILS:
            return cls.RECIPIENT_EMAILS
        elif cls.GIRLFRIEND_EMAIL:
            return [cls.GIRLFRIEND_EMAIL]
        return []
    
    @classmethod
    def get_required_vars(cls) -> Dict[str, Optional[str]]:
        """Get dictionary of required environment variables."""
        return {
            "SMTP_USER": cls.SMTP_USER,
            "SMTP_PASSWORD": cls.SMTP_PASSWORD,
            "GROQ_API_KEY": cls.GROQ_API_KEY,
        }
    
    @classmethod
    def validate_config(cls) -> None:
        """Validate that all required environment variables are set."""
        required_vars = cls.get_required_vars()
        missing_vars = [var for var, value in required_vars.items() if not value]
        
        recipient_emails = cls.get_recipient_emails()
        if not recipient_emails:
            print("⚠️  WARNING: No recipient emails configured. Set RECIPIENT_EMAILS or GIRLFRIEND_EMAIL")
        
        if missing_vars:
            print(f"⚠️  WARNING: Missing required environment variables: {', '.join(missing_vars)}")
        else:
            print("✅ All required environment variables are set")
            if recipient_emails:
                print(f"📧 Recipient emails: {', '.join(recipient_emails)}")
    
    @classmethod
    def is_valid(cls) -> bool:
        """Check if all required configuration is valid."""
        required_vars = cls.get_required_vars()
        return all(value is not None for value in required_vars.values())


# Initialize settings and validate on import
settings = Settings()
settings.validate_config()

