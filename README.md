# 💪 Daily Motivation Bot

A production-ready FastAPI service that sends beautiful, AI-generated famous motivational quotes in French via email. Perfect for sending daily inspiration to keep motivation high!

## ✨ Features

- 🤖 **AI-Powered Quotes**: Uses Groq LLM API to generate famous motivational quotes in French
- 🎨 **Beautiful HTML Emails**: Stunning gradient design with modern, inspiring styling
- 📧 **Yahoo SMTP Integration**: Reliable email delivery via Yahoo SMTP
- 🚀 **FastAPI Backend**: Clean, modern API with proper error handling
- ⏰ **Cron Job Ready**: Designed to work with Render Cron Jobs for automated daily sending
- 🔄 **Daily Variety**: Each day generates a different quote to keep it fresh and inspiring

## 📁 Project Structure

```
daily-motivation-bot/
├── app/
│   ├── __init__.py
│   └── main.py          # FastAPI application
├── requirements.txt     # Python dependencies
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Create a `.env` file in the project root:

```env
SMTP_HOST=smtp.mail.yahoo.com
SMTP_PORT=587
SMTP_USER=your_email@yahoo.com
SMTP_PASSWORD=your_yahoo_app_password
GIRLFRIEND_EMAIL=recipient@example.com
SENDER_NAME=Mehdi
GROQ_API_KEY=your_groq_api_key
```

**Important Notes:**
- `SMTP_PASSWORD` must be a **Yahoo App Password**, not your regular Yahoo password
- To generate a Yahoo App Password: Yahoo Account → Security → Generate App Password
- Get your Groq API key from [https://console.groq.com](https://console.groq.com)

### 3. Run Locally

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

### 4. Test the Endpoint

```bash
curl -X POST "http://127.0.0.1:8000/send-daily-love-email" \
  -H "Content-Type: application/json" \
  -d '{"to_email": "your_test_email@example.com"}'
```

Or test with a custom recipient:

```bash
curl -X POST "http://127.0.0.1:8000/send-daily-love-email" \
  -H "Content-Type: application/json" \
  -d '{}'
```

## 📡 API Endpoints

### `GET /`

Health check endpoint.

**Response:**
```json
{
  "message": "LoveMailBot API is running 🩷"
}
```

### `POST /send-daily-love-email`

Generates a famous motivational quote and sends it via email.

**Request Body (optional):**
```json
{
  "to_email": "custom@example.com"
}
```

If `to_email` is not provided, uses `GIRLFRIEND_EMAIL` from environment variables.

**Response:**
```json
{
  "status": "ok",
  "sent_to": "recipient@example.com",
  "quote": "Generated motivational quote text..."
}
```

**Error Responses:**
- `400`: Missing recipient email
- `500`: Error generating message or sending email

## ☁️ Deployment on Render

> 📖 **For a complete step-by-step guide, see [DEPLOYMENT.md](DEPLOYMENT.md)**

This section provides a quick overview. For detailed instructions with screenshots and troubleshooting, check the full deployment guide.

### Step 1: Push to GitHub

1. Initialize git repository (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Love Mail Bot"
   ```

2. Push to GitHub:
   ```bash
   git remote add origin https://github.com/yourusername/daily-motivation-bot.git
   git push -u origin main
   ```

### Step 2: Create Web Service on Render

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `daily-motivation-bot` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free tier is fine for this use case

### Step 3: Set Environment Variables

In the Render dashboard, go to your service → **Environment** tab, and add:

```
SMTP_HOST=smtp.mail.yahoo.com
SMTP_PORT=587
SMTP_USER=your_email@yahoo.com
SMTP_PASSWORD=your_yahoo_app_password
GIRLFRIEND_EMAIL=recipient@example.com
SENDER_NAME=Mehdi
GROQ_API_KEY=your_groq_api_key
```

### Step 4: Create Cron Job

1. In Render dashboard, click **"New +"** → **"Cron Job"**
2. Configure:
   - **Name**: `daily-love-email`
   - **Schedule**: `30 5 * * *` (06:30 Europe/Paris = 05:30 UTC)
   - **Command**: 
     ```bash
     curl -X POST "https://YOUR-RENDER-URL.onrender.com/send-daily-love-email" \
       -H "Content-Type: application/json" \
       -d '{}'
     ```
   - Replace `YOUR-RENDER-URL` with your actual Render service URL

**Note**: To convert Europe/Paris time to UTC:
- 06:30 Europe/Paris (CET) = 05:30 UTC (winter)
- 06:30 Europe/Paris (CEST) = 04:30 UTC (summer)
- For simplicity, you can use `30 5 * * *` which is 05:30 UTC (06:30 CET)

### ⚠️ Important: Free Tier Limitation

**Render Free tier services "spin down" after 15 minutes of inactivity.**

**Solutions:**
1. **Use UptimeRobot** (free): Set up a monitor to ping your service every 5 minutes
   - Go to [uptimerobot.com](https://uptimerobot.com)
   - Add a monitor for your Render URL
   - Set interval to 5 minutes
   - This keeps your service alive 24/7

2. **Upgrade to Starter plan** ($7/month): Services stay always-on

3. **The cron job will wake up the service**, but there might be a 30-60 second delay on the first request after spin-down.

### Step 5: Test Manually

Once deployed, test the endpoint:

```bash
curl -X POST "https://YOUR-RENDER-URL.onrender.com/send-daily-love-email" \
  -H "Content-Type: application/json" \
  -d '{"to_email": "your_test_email@example.com"}'
```

## 🎨 Email Design

The email template features:
- ✨ Soft gradient background (inspiring tones)
- 📅 Date pill at the top
- 💪 Beautiful card design with rounded corners
- 📱 Fully responsive (mobile-friendly)
- 🎯 Clean, modern typography
- ✨ Professional and inspiring styling

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `SMTP_HOST` | Yahoo SMTP host | No | `smtp.mail.yahoo.com` |
| `SMTP_PORT` | SMTP port | No | `587` |
| `SMTP_USER` | Yahoo email address | **Yes** | - |
| `SMTP_PASSWORD` | Yahoo app password | **Yes** | - |
| `GIRLFRIEND_EMAIL` | Recipient email | **Yes** | - |
| `SENDER_NAME` | Display name for sender | No | `Mehdi` |
| `GROQ_API_KEY` | Groq API key | **Yes** | - |

## 🐛 Troubleshooting

### Email Not Sending

1. **Check Yahoo App Password**: Make sure you're using an App Password, not your regular password
2. **Verify SMTP credentials**: Test with a simple SMTP connection
3. **Check Render logs**: View logs in Render dashboard for error messages

### Groq API Errors

1. **Verify API Key**: Make sure `GROQ_API_KEY` is set correctly
2. **Check API Limits**: Groq has rate limits on free tier
3. **View logs**: Check console output for detailed error messages

### Cron Job Not Running

1. **Verify Schedule**: Double-check the cron expression
2. **Test Endpoint**: Manually call the endpoint to ensure it works
3. **Check Render Cron Logs**: View execution logs in Render dashboard

## 📝 License

This project is open source and available for personal use.

## 💝 Made with Love

Built to spread daily love and motivation. Enjoy! 🩷

