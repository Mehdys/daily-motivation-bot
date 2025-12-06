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
    version="1.0.2",
    description="API for sending daily AI-generated motivational quotes via email",
    docs_url="/docs",
    redoc_url="/redoc"
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
    If to_email is provided, sends to that address only.
    Otherwise, sends to all configured recipients.
    
    This endpoint is designed to be called by Render Cron Job for serverless execution.
    
    Args:
        request: Request body with optional to_email override
        
    Returns:
        EmailResponse: Status, recipient email(s), and generated quote
        
    Raises:
        HTTPException: If email address is missing or sending fails
    """
    try:
        # Determine recipient emails
        if request.to_email:
            recipient_emails = [request.to_email]
        else:
            recipient_emails = settings.get_recipient_emails()
        
        if not recipient_emails:
            raise HTTPException(
                status_code=400,
                detail="No recipient email found. Provide to_email in request or set RECIPIENT_EMAILS env var."
            )
        
        print(f"📧 Sending emails to: {', '.join(recipient_emails)}")
        
        # Generate motivational quote
        groq_client = get_groq_client()
        quote = groq_client.generate_quote()
        
        # Build email template
        html_body = EmailTemplateBuilder.build_motivational_email(quote)
        subject = "Ta citation motivationnelle du jour 💪"
        
        # Send email to all recipients
        email_service = get_email_service()
        sent_to_list = []
        
        for email in recipient_emails:
            try:
                email_service.send_email(
                    subject=subject,
                    plain_body=quote,
                    html_body=html_body,
                    to_email=email
                )
                sent_to_list.append(email)
                print(f"✅ Email sent successfully to {email}")
            except Exception as e:
                print(f"❌ Failed to send email to {email}: {e}")
        
        if not sent_to_list:
            raise HTTPException(
                status_code=500,
                detail="Failed to send email to any recipient"
            )
        
        sent_to_str = ", ".join(sent_to_list) if len(sent_to_list) > 1 else sent_to_list[0]
        
        print(f"📊 Sent {len(sent_to_list)}/{len(recipient_emails)} emails successfully")
        
        return EmailResponse(
            status="ok",
            sent_to=sent_to_str,
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
