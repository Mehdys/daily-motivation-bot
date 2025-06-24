"""
Email service for sending motivational quotes via SMTP.
"""

import smtplib
from email.message import EmailMessage
from typing import Optional

from app.config import settings


class EmailService:
    """Service for sending emails via SMTP."""
    
    def __init__(self):
        """Initialize email service with SMTP configuration."""
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.sender_name = settings.SENDER_NAME
        
        if not self.smtp_user or not self.smtp_password:
            raise ValueError("SMTP credentials are not set in environment variables")
    
    def _create_email_message(
        self,
        subject: str,
        plain_body: str,
        html_body: str,
        to_email: str
    ) -> EmailMessage:
        """Create an email message with both plain text and HTML content."""
        msg = EmailMessage()
        msg["From"] = f"{self.sender_name} <{self.smtp_user}>"
        msg["To"] = to_email
        msg["Subject"] = subject
        
        # Set plain text and HTML content
        msg.set_content(plain_body)
        msg.add_alternative(html_body, subtype="html")
        
        return msg
    
    def send_email(
        self,
        subject: str,
        plain_body: str,
        html_body: str,
        to_email: str
    ) -> None:
        """
        Send an HTML email via SMTP.
        
        Args:
            subject: Email subject line
            plain_body: Plain text version of the email
            html_body: HTML version of the email
            to_email: Recipient email address
            
        Raises:
            Exception: If SMTP connection or sending fails
        """
        print(f"📧 Preparing to send email to {to_email}...")
        
        msg = self._create_email_message(subject, plain_body, html_body, to_email)
        
        try:
            # Connect to SMTP server
            print(f"🔌 Connecting to {self.smtp_host}:{self.smtp_port}...")
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                
                print(f"✉️  Sending email to {to_email}...")
                server.send_message(msg)
                print(f"✅ Email sent successfully to {to_email}!")
                
        except smtplib.SMTPException as e:
            print(f"❌ SMTP error: {e}")
            raise Exception(f"Failed to send email: {str(e)}")
        except Exception as e:
            print(f"❌ Unexpected error sending email: {e}")
            raise Exception(f"Failed to send email: {str(e)}")


def get_email_service() -> EmailService:
    """Factory function to get email service instance."""
    return EmailService()

