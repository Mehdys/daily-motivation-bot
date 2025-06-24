import os
import time
import smtplib
import requests
from email.message import EmailMessage
from datetime import datetime

from dotenv import load_dotenv
import schedule

# Charger les variables d'environnement
load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

GIRLFRIEND_EMAIL = os.getenv("GIRLFRIEND_EMAIL")
SENDER_NAME = os.getenv("SENDER_NAME", "Ton amoureux")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not all([SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, GIRLFRIEND_EMAIL, GROQ_API_KEY]):
    raise RuntimeError("❌ Il manque une variable dans .env")


def generate_love_message() -> str:
    """
    Génère un message d'amour/motivation via Groq.
    """
    system_prompt = (
        "Tu es un petit ami aimant, simple et sincère. "
        "Tu écris chaque matin un message court pour motiver ta copine. "
        "Elle est ambitieuse mais souvent fatiguée et stressée. "
        "Ton ton est doux, moderne, jamais cringe."
    )

    today_str = datetime.now().strftime("%d/%m/%Y")

    user_prompt = (
        f"Nous sommes le {today_str}. "
        "Génère UN SEUL message en français, court, motivant, touchant.\n"
        "Contraintes :\n"
        "- Max 280 caractères\n"
        "- 1 ou 2 emojis max\n"
        "- Style simple, rassurant, intime\n"
        "- Ne commence PAS par 'Bonjour' ou 'Coucou'\n"
        "- Pas de hashtags, pas de guillemets.\n"
    )

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    body = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.9,
        "max_tokens": 200,
    }

    resp = requests.post(url, headers=headers, json=body, timeout=20)
    resp.raise_for_status()
    data = resp.json()

    text = data["choices"][0]["message"]["content"].strip()
    print("💌 Message généré par Groq:", text)
    return text


def send_email(subject: str, body: str):
    """
    Envoie un email via Yahoo SMTP.
    """
    msg = EmailMessage()
    msg["From"] = f"{SENDER_NAME} <{SMTP_USER}>"
    msg["To"] = GIRLFRIEND_EMAIL
    msg["Subject"] = subject
    msg.set_content(body)

    print("➡️ Envoi de l'email via Yahoo...")
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)
    print("✅ Email envoyé.")


def job():
    """
    Job exécuté chaque matin : génération + envoi.
    """
    now = datetime.now().isoformat()
    print(f"\n[{now}] Exécution du love-mail-bot...")

    try:
        message = generate_love_message()
        subject = "Un petit mot pour ta journée ❤️"
        send_email(subject, message)
    except Exception as e:
        print("❌ Erreur dans le job :", e)


def main():
    # Pour tester modifie l'heure ici, ex: "22:45"
    schedule.every().day.at("06:30").do(job)
    print("✨ Love-mail-bot démarré. Un mail sera envoyé chaque jour à 06:30.")

    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == "__main__":
    # Pour tester sans attendre l'heure :
    job()
    #main()
