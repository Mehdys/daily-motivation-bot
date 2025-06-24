"""
Daily Motivation Bot - FastAPI Application
Main entry point for the API server.
"""

from fastapi import FastAPI, HTTPException

from app.config import settings
from app.models.schemas import EmailResponse, TriggerRequest
from app.services.email_service import get_email_service
from app.services.groq_client import get_groq_client
from app.templates.email_templates import EmailTemplateBuilder

# Initialize FastAPI app
app = FastAPI(
    title="Daily Motivation Bot API",
    version="1.0.0",
    description="API for sending daily AI-generated motivational quotes via email"
)


@app.get("/")
async def root():
    """
    Health check endpoint.
    
    Returns:
        dict: API status message
    """
    return {"message": "Daily Motivation Bot API is running 💪"}


@app.post("/send-daily-love-email", response_model=EmailResponse)
async def send_daily_motivation_email(request: TriggerRequest):
    """
    Generate a motivational quote and send it via email.
    
    Args:
        request: Request body with optional to_email override
        
    Returns:
        EmailResponse: Status, recipient email, and generated quote
        
    Raises:
        HTTPException: If email address is missing or sending fails
    """
    try:
        # Determine recipient email
        to_email = request.to_email or settings.GIRLFRIEND_EMAIL
        
        if not to_email:
            raise HTTPException(
                status_code=400,
                detail="No recipient email found. Provide to_email in request or set GIRLFRIEND_EMAIL env var."
            )
        
        # Generate motivational quote
        groq_client = get_groq_client()
        quote = groq_client.generate_quote()
        
        # Build email template
        html_body = EmailTemplateBuilder.build_motivational_email(quote)
        subject = "Ta citation motivationnelle du jour 💪"
        
        # Send email
        email_service = get_email_service()
        email_service.send_email(
            subject=subject,
            plain_body=quote,
            html_body=html_body,
            to_email=to_email
        )
        
        return EmailResponse(
            status="ok",
            sent_to=to_email,
            quote=quote
        )
        
    except HTTPException:
        raise
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Configuration error: {str(e)}"
        )
    except Exception as e:
        print(f"❌ Error in send_daily_motivation_email: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to send email: {str(e)}"
        )
