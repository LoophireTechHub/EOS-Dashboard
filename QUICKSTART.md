# 🚀 Quick Start Guide

Get your Loophire EOS KPI Dashboard running in 5 minutes!

## Step 1: Get Your Slack Bot Token

1. **Go to:** https://api.slack.com/apps/A09V1G92CRW/oauth
2. **Look for:** "Bot User OAuth Token" section
3. **Click:** "Install to Workspace" (if not already done)
4. **Copy:** The token starting with `xoxb-`

## Step 2: Configure Your Application

```bash
cd /Users/loophire/EOS-Dashboard

# Copy the example env file
cp .env.example .env

# Edit with your token
nano .env
```

Paste your token:
```bash
SLACK_BOT_TOKEN=xoxb-paste-your-token-here
SLACK_CHANNEL_GENERAL=#accountability
SLACK_CHANNEL_LEADERSHIP=#leadership
```

Save: `Ctrl+X`, then `Y`, then `Enter`

## Step 3: Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

## Step 4: Add Bot Scopes (First Time Only)

1. Go to: https://api.slack.com/apps/A09V1G92CRW/oauth
2. Scroll to "Scopes" → "Bot Token Scopes"
3. Add these if not already added:
   - `chat:write`
   - `chat:write.public`
   - `channels:read`
4. Click "Reinstall to Workspace" if you added new scopes

## Step 5: Invite Bot to Channels

In Slack, type in each channel:
```
/invite @Loophire EOS KPI Bot
```

Channels:
- `#accountability`
- `#leadership`

## Step 6: Start the Server

```bash
python main.py
```

You should see:
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## Step 7: Test It!

Open another terminal and test the Slack integration:

```bash
curl -X POST http://localhost:8000/api/slack/send-reminder?submission_type=weekly_kickoff
```

Check your `#accountability` channel - you should see a message from the bot!

## Step 8: Use the Dashboard

Open in your browser:
```
http://localhost:8000
```

Try submitting some test KPIs!

---

## 🎉 You're Done!

Your EOS KPI Dashboard is now running!

### What's Next?

1. **Deploy to Production** - See README.md for Railway/Heroku/Docker deployment
2. **Customize Metrics** - Edit goals in `main.py`
3. **Test Reminders** - Reminders auto-send Mon/Wed at scheduled times
4. **Train Your Team** - Share the dashboard URL with your team

---

## 🆘 Need Help?

**Bot not sending messages?**
- Check your `.env` file has the correct token
- Make sure bot is invited to the channels
- Check the terminal for error messages

**Can't access dashboard?**
- Make sure the server is running (`python main.py`)
- Try http://127.0.0.1:8000 instead

**Other issues?**
- Check SLACK_SETUP.md for detailed troubleshooting
- Check README.md for full documentation
