# ⚡ Quick Start - Deploy in 10 Minutes

## 🎯 Goal: Run 24/7 Without Your PC

Follow these steps to deploy your **Daily Motivation Bot** to the cloud:

---

## ✅ Checklist

### 1. Push Code to GitHub (2 min)
```bash
cd /Users/mehdigribaa/Desktop/WhsMsg
git init
git add app/ requirements.txt .gitignore README.md render.yaml
git commit -m "Daily Motivation Bot"
# Create repo on github.com, then:
git remote add origin https://github.com/YOUR_USERNAME/daily-motivation-bot.git
git push -u origin main
```

### 2. Deploy to Render (3 min)
- Go to [dashboard.render.com](https://dashboard.render.com)
- Click **"New +"** → **"Web Service"**
- Connect GitHub repo
- Settings:
  - Build: `pip install -r requirements.txt`
  - Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
  - Plan: **Free**

### 3. Add Environment Variables (2 min)
In Render → Your Service → Environment tab, add:
```
SMTP_USER=your_email@yahoo.com
SMTP_PASSWORD=your_yahoo_app_password
GIRLFRIEND_EMAIL=recipient@example.com
SENDER_NAME=Mehdi
GROQ_API_KEY=your_groq_key
```

### 4. Create Cron Job (2 min)
- Render → **"New +"** → **"Cron Job"**
- Schedule: `30 5 * * *` (06:30 Paris time)
- Command: `curl -X POST "https://YOUR-URL.onrender.com/send-daily-love-email" -H "Content-Type: application/json" -d '{}'`

### 5. Keep Service Alive (1 min) ⚠️ IMPORTANT
**Free tier spins down after 15 min!**

Use [UptimeRobot](https://uptimerobot.com) (free):
- Add monitor for your Render URL
- Interval: 5 minutes
- This keeps it alive 24/7

---

## 🎉 Done!

Your bot now runs automatically every day at 06:30, even when your PC is off!

---

**Need detailed instructions?** See [DEPLOYMENT.md](DEPLOYMENT.md)

