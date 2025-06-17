# 🚀 Complete Deployment Guide - Run 24/7 Without Your PC

This guide will help you deploy your **Daily Motivation Bot** to Render so it runs **automatically every day at 06:30** without needing your computer to be on.

---

## 📋 Prerequisites

Before starting, make sure you have:

1. ✅ **GitHub account** (free) - [github.com](https://github.com)
2. ✅ **Render account** (free tier available) - [render.com](https://render.com)
3. ✅ **Yahoo App Password** (not your regular password)
4. ✅ **Groq API Key** - [console.groq.com](https://console.groq.com)

---

## 🎯 Step-by-Step Deployment

### Step 1: Prepare Your Code for GitHub

1. **Initialize Git** (if not already done):
   ```bash
   cd /Users/mehdigribaa/Desktop/WhsMsg
   git init
   ```

2. **Add all files**:
   ```bash
   git add app/ requirements.txt .gitignore README.md render.yaml
   ```

3. **Commit**:
   ```bash
   git commit -m "Initial commit: Daily Motivation Bot ready for deployment"
   ```

### Step 2: Push to GitHub

1. **Create a new repository on GitHub**:
   - Go to [github.com/new](https://github.com/new)
   - Name it: `daily-motivation-bot` (or any name you like)
   - Make it **Public** (free Render tier requires public repos, or you can use private with paid plan)
   - **Don't** initialize with README (you already have one)

2. **Connect and push**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/daily-motivation-bot.git
   git branch -M main
   git push -u origin main
   ```
   Replace `YOUR_USERNAME` with your actual GitHub username.

### Step 3: Deploy to Render (Web Service)

1. **Go to Render Dashboard**:
   - Visit [dashboard.render.com](https://dashboard.render.com)
   - Sign up or log in (you can use GitHub to sign in)

2. **Create New Web Service**:
   - Click **"New +"** button (top right)
   - Select **"Web Service"**
   - Click **"Connect GitHub"** and authorize Render
   - Select your `love-mail-bot` repository

3. **Configure the Service**:
   - **Name**: `daily-motivation-bot` (or your choice)
   - **Environment**: `Python 3`
   - **Region**: Choose closest to you (e.g., `Frankfurt` for Europe)
   - **Branch**: `main`
   - **Root Directory**: Leave empty (or `./` if needed)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Select **Free** (or Starter if you want better performance)

4. **Click "Create Web Service"**

   ⚠️ **Wait for deployment** - This takes 2-5 minutes. You'll see build logs.

### Step 4: Set Environment Variables

Once your service is deployed:

1. **Go to your service** in Render dashboard
2. Click **"Environment"** tab (left sidebar)
3. **Add these variables** (click "Add Environment Variable" for each):

   ```
   SMTP_HOST = smtp.mail.yahoo.com
   SMTP_PORT = 587
   SMTP_USER = your_email@yahoo.com
   SMTP_PASSWORD = your_yahoo_app_password_here
   GIRLFRIEND_EMAIL = recipient@example.com
   SENDER_NAME = Mehdi
   GROQ_API_KEY = your_groq_api_key_here
   ```

   ⚠️ **Important**: 
   - `SMTP_PASSWORD` must be a **Yahoo App Password** (not your regular password)
   - To get Yahoo App Password: Yahoo Account → Security → Generate App Password
   - Get Groq API key from: [console.groq.com](https://console.groq.com)

4. **Save** - Render will automatically restart your service with new env vars.

### Step 5: Test Your Deployment

1. **Get your service URL**:
   - In Render dashboard, your service URL is shown at the top
   - It looks like: `https://love-mail-bot-xxxx.onrender.com`

2. **Test the health endpoint**:
   ```bash
   curl https://YOUR-SERVICE-URL.onrender.com/
   ```
   Should return: `{"message":"LoveMailBot API is running 🩷"}`

3. **Test sending an email** (replace with your test email):
   ```bash
   curl -X POST "https://YOUR-SERVICE-URL.onrender.com/send-daily-love-email" \
     -H "Content-Type: application/json" \
     -d '{"to_email": "your_test_email@example.com"}'
   ```

   ✅ If successful, you'll receive an email!

### Step 6: Set Up Automatic Daily Cron Job

This is the **key step** to make it run automatically every day:

1. **In Render Dashboard**, click **"New +"** → **"Cron Job"**

2. **Configure the Cron Job**:
   - **Name**: `daily-love-email`
   - **Schedule**: `30 5 * * *` 
     - This means: Every day at 05:30 UTC = 06:30 Europe/Paris (winter time)
     - For summer time (CEST), use: `30 4 * * *` (04:30 UTC = 06:30 CEST)
   - **Command**: 
     ```bash
     curl -X POST "https://YOUR-SERVICE-URL.onrender.com/send-daily-love-email" -H "Content-Type: application/json" -d '{}'
     ```
     ⚠️ **Replace `YOUR-SERVICE-URL`** with your actual Render service URL!

3. **Click "Create Cron Job"**

4. **Verify**:
   - The cron job will appear in your dashboard
   - You can click on it to see execution logs
   - It will run automatically every day at the scheduled time

---

## ⏰ Time Zone Notes

**Europe/Paris time zones:**
- **Winter (CET)**: UTC+1 → 06:30 Paris = 05:30 UTC → Use: `30 5 * * *`
- **Summer (CEST)**: UTC+2 → 06:30 Paris = 04:30 UTC → Use: `30 4 * * *`

**To handle both automatically**, you can:
- Use `30 5 * * *` (winter time) and manually change it twice a year, OR
- Use a service like [cron-job.org](https://cron-job.org) that supports time zones

---

## ✅ Verification Checklist

After deployment, verify:

- [ ] Web service is running (green status in Render)
- [ ] Health endpoint works: `GET /`
- [ ] Manual test email was received
- [ ] Environment variables are all set
- [ ] Cron job is created and scheduled
- [ ] Cron job has the correct service URL

---

## 🔍 Monitoring & Logs

**View logs in Render**:
1. Go to your Web Service
2. Click **"Logs"** tab
3. You'll see:
   - Startup logs
   - API request logs
   - Error messages (if any)

**View Cron Job execution**:
1. Go to your Cron Job
2. Click **"Logs"** tab
3. You'll see execution history and results

---

## 🐛 Troubleshooting

### Service won't start
- Check **Logs** tab for error messages
- Verify all environment variables are set correctly
- Make sure `requirements.txt` is correct

### Email not sending
- Check **Logs** for SMTP errors
- Verify Yahoo App Password (not regular password)
- Test SMTP credentials locally first

### Cron job not running
- Verify the schedule syntax: `30 5 * * *`
- Check the command has the correct URL
- View Cron Job logs to see execution history
- Make sure the Web Service is running (not sleeping)

### Free tier limitations
- **Render Free tier**: Services "spin down" after 15 minutes of inactivity
- **Solution**: 
  - Use a free service like [UptimeRobot](https://uptimerobot.com) to ping your service every 5 minutes, OR
  - Upgrade to Starter plan ($7/month) for always-on service

---

## 🎉 You're Done!

Once deployed, your Daily Motivation Bot will:
- ✅ Run 24/7 in the cloud
- ✅ Send emails automatically every day at 06:30
- ✅ Work even when your PC is off
- ✅ Handle errors gracefully

**No more manual intervention needed!** 🚀

---

## 📞 Need Help?

- Render Docs: [render.com/docs](https://render.com/docs)
- Render Support: [community.render.com](https://community.render.com)
- Check your service logs for detailed error messages

