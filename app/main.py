"""
Daily Motivation Bot - FastAPI Application
Sends daily famous motivational quotes in French using Groq LLM and Yahoo SMTP.
"""

import os
import smtplib
from datetime import datetime
from email.message import EmailMessage
from typing import Optional

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Load environment variables from .env file (for local development)
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Daily Motivation Bot API", version="1.0.0")

# Environment variables
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.mail.yahoo.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
GIRLFRIEND_EMAIL = os.getenv("GIRLFRIEND_EMAIL")
SENDER_NAME = os.getenv("SENDER_NAME", "Mehdi")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Check required environment variables on startup
REQUIRED_VARS = {
    "SMTP_USER": SMTP_USER,
    "SMTP_PASSWORD": SMTP_PASSWORD,
    "GIRLFRIEND_EMAIL": GIRLFRIEND_EMAIL,
    "GROQ_API_KEY": GROQ_API_KEY,
}

missing_vars = [var for var, value in REQUIRED_VARS.items() if not value]
if missing_vars:
    print(f"⚠️  WARNING: Missing required environment variables: {', '.join(missing_vars)}")
else:
    print("✅ All required environment variables are set")


def generate_motivational_quote() -> str:
    """
    Generates a famous motivational quote in French using Groq LLM API.
    Each day generates a different quote to keep it fresh.
    
    Returns:
        str: The generated quote text (stripped of quotes and whitespace)
    """
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is not set")
    
    # Get current date in French format - using date to ensure variety
    today = datetime.now()
    date_str = today.strftime("%d %B %Y")
    day_of_year = today.timetuple().tm_yday  # Day of year (1-365) for variety
    
    system_prompt = (
        "Tu es un expert en citations motivationnelles ultra-positives et énergisantes. "
        "Tu connais les meilleures citations de personnalités inspirantes : "
        "Nelson Mandela, Steve Jobs, Oprah Winfrey, Albert Einstein, Maya Angelou, "
        "Tony Robbins, Les Brown, et bien d'autres. "
        "Tu adaptes ces citations en français de manière naturelle, énergique et ultra-positive. "
        "Tu ne mentionnes JAMAIS de termes négatifs comme échec, difficulté, problème, obstacle, peur, doute, etc. "
        "Tu te concentres uniquement sur la positivité, l'énergie, le succès, la force, la joie, la détermination."
    )
    
    user_prompt = (
        f"Nous sommes le {date_str} (jour {day_of_year} de l'année). "
        "Génère UNE SEULE citation motivationnelle ultra-positive et énergisante en français. "
        "Contraintes strictes :\n"
        "- Maximum 200 caractères\n"
        "- Citation d'une personnalité célèbre (auteur, entrepreneur, leader, coach, etc.)\n"
        "- Style ultra-positif, énergique, puissant, motivant pour démarrer la journée\n"
        "- Format : Citation suivie de \"— Nom de l'auteur\"\n"
        "- INTERDICTION ABSOLUE de mentionner : échec, difficulté, problème, obstacle, peur, doute, négativité, défis négatifs\n"
        "- Seulement des messages sur : succès, force, énergie, détermination, joie, passion, victoire, excellence, croissance, possibilités infinies\n"
        "- Exemple positif : \"Crois en tes rêves et ils se réaliseront. L'énergie suit l'intention. — Tony Robbins\"\n"
        "- Ne pas répéter les mêmes citations chaque jour (utilise la date pour varier)\n"
        "- Pas de guillemets autour de la citation complète\n"
        "- 1-2 emojis énergiques si approprié (💪 ✨ 🚀 ⭐)"
    )
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.9,
        "max_tokens": 200,
    }
    
    try:
        print("🤖 Calling Groq API to generate motivational quote...")
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        quote = data["choices"][0]["message"]["content"].strip()
        
        # Remove quotes if the quote is wrapped in them
        if quote.startswith('"') and quote.endswith('"'):
            quote = quote[1:-1]
        if quote.startswith("'") and quote.endswith("'"):
            quote = quote[1:-1]
        
        print(f"✨ Generated quote: {quote}")
        return quote
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error calling Groq API: {e}")
        raise Exception(f"Failed to generate message: {str(e)}")


def build_html_email(quote: str) -> str:
    """
    Builds a beautiful HTML email template with a motivational, modern design.
    
    Args:
        quote: The AI-generated motivational quote to include in the email
        
    Returns:
        str: Complete HTML email content
    """
    # Get current date in French format
    today = datetime.now()
    weekday_fr = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    month_fr = [
        "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
        "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"
    ]
    
    date_display = f"{weekday_fr[today.weekday()]} {today.day} {month_fr[today.month - 1]} {today.year}"
    
    html = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Un petit mot pour ta journée</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%);
            padding: 20px;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        .email-container {{
            max-width: 600px;
            width: 100%;
            margin: 0 auto;
        }}
        
        .card {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 24px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
            padding: 40px;
            margin: 20px 0;
        }}
        
        .date-pill {{
            display: inline-block;
            background: linear-gradient(135deg, #ff6b9d 0%, #c44569 100%);
            color: white;
            padding: 8px 20px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            letter-spacing: 0.5px;
            margin-bottom: 24px;
            text-transform: uppercase;
        }}
        
        .title {{
            font-size: 32px;
            font-weight: 700;
            color: #2d3436;
            margin-bottom: 12px;
            line-height: 1.2;
        }}
        
        .subtitle {{
            font-size: 16px;
            color: #636e72;
            margin-bottom: 32px;
            line-height: 1.6;
            font-weight: 400;
        }}
        
        .message {{
            font-size: 18px;
            color: #2d3436;
            line-height: 1.8;
            margin: 32px 0;
            padding: 24px;
            background: rgba(255, 182, 193, 0.1);
            border-left: 4px solid #ff6b9d;
            border-radius: 8px;
            font-weight: 400;
        }}
        
        .signature {{
            text-align: right;
            margin-top: 32px;
            font-size: 16px;
            color: #2d3436;
            font-weight: 500;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 24px;
            font-size: 11px;
            color: #636e72;
            opacity: 0.7;
        }}
        
        @media only screen and (max-width: 600px) {{
            .card {{
                padding: 24px;
                margin: 10px;
            }}
            
            .title {{
                font-size: 24px;
            }}
            
            .message {{
                font-size: 16px;
                padding: 16px;
            }}
        }}
    </style>
</head>
<body>
    <div class="email-container">
        <div class="card">
            <div class="date-pill">{date_display}</div>
            
            <h1 class="title">Ta citation du jour 💪</h1>
            
            <p class="subtitle">
                Une dose quotidienne d'inspiration pour démarrer ta journée du bon pied.
            </p>
            
            <div class="message">
                {quote}
            </div>
            
            <div class="signature">
                {SENDER_NAME} 💌
            </div>
            
            <div class="footer">
                Citation générée automatiquement pour t'inspirer chaque jour.
            </div>
        </div>
    </div>
</body>
</html>
"""
    return html


def send_email_html(subject: str, plain_body: str, html_body: str, to_email: str) -> None:
    """
    Sends an HTML email via Yahoo SMTP.
    
    Args:
        subject: Email subject line
        plain_body: Plain text version of the email
        html_body: HTML version of the email
        to_email: Recipient email address
        
    Raises:
        Exception: If SMTP connection or sending fails
    """
    if not SMTP_USER or not SMTP_PASSWORD:
        raise ValueError("SMTP credentials are not set")
    
    print(f"📧 Preparing to send email to {to_email}...")
    
    # Create email message
    msg = EmailMessage()
    msg["From"] = f"{SENDER_NAME} <{SMTP_USER}>"
    msg["To"] = to_email
    msg["Subject"] = subject
    
    # Set plain text and HTML content
    msg.set_content(plain_body)
    msg.add_alternative(html_body, subtype="html")
    
    try:
        # Connect to SMTP server
        print(f"🔌 Connecting to {SMTP_HOST}:{SMTP_PORT}...")
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            
            print(f"✉️  Sending email to {to_email}...")
            server.send_message(msg)
            print(f"✅ Email sent successfully to {to_email}!")
            
    except smtplib.SMTPException as e:
        print(f"❌ SMTP error: {e}")
        raise Exception(f"Failed to send email: {str(e)}")
    except Exception as e:
        print(f"❌ Unexpected error sending email: {e}")
        raise Exception(f"Failed to send email: {str(e)}")


# Pydantic models
class TriggerRequest(BaseModel):
    """Request model for triggering the daily motivational email."""
    to_email: Optional[str] = None


# API Routes
@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "Daily Motivation Bot API is running 💪"}


@app.post("/send-daily-love-email")
async def send_daily_motivation_email(request: TriggerRequest):
    """
    Generates a famous motivational quote using Groq LLM and sends it as a beautiful HTML email.
    
    Args:
        request: Optional request body with to_email override
        
    Returns:
        dict: Status, recipient email, and generated quote
        
    Raises:
        HTTPException: If email address is missing or sending fails
    """
    try:
        # Determine recipient email
        to_email = request.to_email or GIRLFRIEND_EMAIL
        
        if not to_email:
            raise HTTPException(
                status_code=400,
                detail="No recipient email found. Provide to_email in request or set GIRLFRIEND_EMAIL env var."
            )
        
        # Generate motivational quote
        quote = generate_motivational_quote()
        
        # Build email subject and HTML
        subject = "Ta citation motivationnelle du jour 💪"
        html_body = build_html_email(quote)
        
        # Send email
        send_email_html(subject, quote, html_body, to_email)
        
        return {
            "status": "ok",
            "sent_to": to_email,
            "quote": quote
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error in send_daily_motivation_email: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to send email: {str(e)}"
        )

