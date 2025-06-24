"""
Email template builder for motivational quotes.
"""

from datetime import datetime

from app.config import settings


class EmailTemplateBuilder:
    """Builder for creating HTML email templates."""
    
    WEEKDAYS_FR = [
        "Lundi", "Mardi", "Mercredi", "Jeudi", 
        "Vendredi", "Samedi", "Dimanche"
    ]
    
    MONTHS_FR = [
        "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
        "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"
    ]
    
    @classmethod
    def _get_formatted_date(cls) -> str:
        """Get current date formatted in French."""
        today = datetime.now()
        weekday = cls.WEEKDAYS_FR[today.weekday()]
        month = cls.MONTHS_FR[today.month - 1]
        return f"{weekday} {today.day} {month} {today.year}"
    
    @classmethod
    def build_motivational_email(cls, quote: str) -> str:
        """
        Build HTML email template for motivational quote.
        
        Args:
            quote: The motivational quote to include in the email
            
        Returns:
            str: Complete HTML email content
        """
        date_display = cls._get_formatted_date()
        sender_name = settings.SENDER_NAME
        
        html = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ta citation du jour</title>
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
                {sender_name} 💌
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

