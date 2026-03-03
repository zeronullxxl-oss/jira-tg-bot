# Deploy on Render.com

## Step 1: GitHub

Create a GitHub repo and push the code:

```
git init
git add .
git commit -m "init"
git remote add origin https://github.com/YOUR_USERNAME/jira-tg-bot.git
git push -u origin main
```

## Step 2: Render

1. Go to https://render.com and sign up (GitHub login works)
2. Dashboard -> New -> Web Service
3. Connect your GitHub repo (jira-tg-bot)
4. Settings:
   - Name: jira-tg-bot
   - Runtime: Python
   - Build Command: pip install -r requirements.txt
   - Start Command: python server.py
   - Instance Type: Free

5. Environment Variables (click "Add Environment Variable"):

   PORT = 10000
   BOT_TOKEN = (leave empty for now, or paste your bot token)
   WEBAPP_URL = (will fill after deploy, see step 3)
   JIRA_URL = https://your-domain.atlassian.net
   JIRA_EMAIL = (your jira email)
   JIRA_API_TOKEN = (your jira token)
   JIRA_PROJECT_KEY = PROJ
   WEBHOOK_SECRET = (any random string)

6. Click "Create Web Service"

## Step 3: Get your URL

After deploy, Render gives you a URL like:
https://jira-tg-bot-xxxx.onrender.com

1. Copy this URL
2. Go to Environment -> WEBAPP_URL -> paste the URL -> Save
3. Render will auto-redeploy

## Step 4: Test

Open your Render URL in browser:
https://jira-tg-bot-xxxx.onrender.com

You should see the Mini App in dev mode.

## Step 5: Connect Telegram Bot

1. Go to @BotFather -> /newbot -> get token
2. Paste token into WEBAPP_URL env var on Render
3. Open bot in Telegram -> /start
4. Menu button "Open Tasks" should appear

## Step 6: Connect Jira (when ready)

1. Fill JIRA_URL, JIRA_EMAIL, JIRA_API_TOKEN on Render
2. Setup webhook in Jira:
   URL: https://jira-tg-bot-xxxx.onrender.com/webhook/jira?secret=YOUR_SECRET
   Events: Issue Updated

## Notes

- Free tier sleeps after 15 min of inactivity (first request takes ~30 sec to wake up)
- For production, upgrade to $7/mo Starter plan (no sleep)
- HTTPS is automatic on Render
- SQLite database resets on redeploy (for production, switch to PostgreSQL)
