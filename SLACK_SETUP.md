# 🔐 Slack Bot Token Setup Guide

## Step-by-Step Instructions

### 1. Access Your Slack App

Go to: https://api.slack.com/apps/A09V1G92CRW

### 2. Get Your Bot Token

1. Click **"OAuth & Permissions"** in the left sidebar
2. Look for **"Bot User OAuth Token"** section
3. You should see a token starting with `xoxb-`

**If you don't see a token:**
- Click **"Install to Workspace"** button at the top
- Authorize the app
- The token will appear after installation

### 3. Configure Required Permissions

Your bot needs these **Bot Token Scopes**:

#### Required Scopes:
- ✅ `chat:write` - Post messages to channels
- ✅ `chat:write.public` - Post to public channels without joining
- ✅ `channels:read` - View basic channel information

#### How to Add Scopes:

1. Scroll down to **"Scopes"** section
2. Under **"Bot Token Scopes"**, click **"Add an OAuth Scope"**
3. Add each scope listed above
4. If you added new scopes, click **"Reinstall to Workspace"** at the top

### 4. Install Bot to Workspace

1. At the top of the OAuth & Permissions page, click **"Install to Workspace"**
2. Review the permissions
3. Click **"Allow"**
4. Copy the **Bot User OAuth Token** (starts with `xoxb-`)

### 5. Add Token to Your .env File

```bash
cd /Users/loophire/EOS-Dashboard
nano .env
```

Add this line (replace with your actual token):
```
SLACK_BOT_TOKEN=xoxb-1851400766544-9987553080880-YOUR_ACTUAL_TOKEN_HERE
```

Save and exit (Ctrl+X, then Y, then Enter)

### 6. Invite Bot to Channels

The bot needs to be in the channels where it will post messages.

In Slack, go to each channel and type:
```
/invite @Loophire EOS KPI Bot
```

Channels to invite bot to:
- `#accountability` (for weekly reminders)
- `#leadership` (for escalation alerts)

### 7. Verify Bot Installation

Check if bot is installed:

1. Go to your Slack workspace
2. Click on your workspace name → **Settings & administration** → **Manage apps**
3. Search for "Loophire EOS KPI Bot"
4. It should show as "Installed"

---

## 🔍 Finding Your Bot Token

### Option A: Via Slack API Dashboard

1. https://api.slack.com/apps/A09V1G92CRW/oauth
2. Look for **"Bot User OAuth Token"**
3. Click **"Show"** to reveal the token
4. Copy it (starts with `xoxb-`)

### Option B: Via App Management

1. Go to https://api.slack.com/apps
2. Click on **"Loophire EOS KPI Bot"**
3. Click **"OAuth & Permissions"**
4. Find **"Bot User OAuth Token"**

---

## ✅ Testing Your Setup

### 1. Start the Application

```bash
cd /Users/loophire/EOS-Dashboard
source venv/bin/activate
python main.py
```

### 2. Test Slack Message

In a new terminal:

```bash
curl -X POST http://localhost:8000/api/slack/send-reminder?submission_type=weekly_kickoff
```

### 3. Check Slack

Go to `#accountability` channel in Slack. You should see a message from your bot!

---

## 🚨 Troubleshooting

### "SLACK_BOT_TOKEN not configured"

**Solution:** Check your `.env` file
```bash
cat /Users/loophire/EOS-Dashboard/.env
```

Make sure it has:
```
SLACK_BOT_TOKEN=xoxb-...
```

### "not_in_channel" error

**Solution:** Invite the bot to the channel
```
/invite @Loophire EOS KPI Bot
```

### "invalid_auth" error

**Solution:** Your token might be incorrect or expired
1. Go to https://api.slack.com/apps/A09V1G92CRW/oauth
2. Click **"Reinstall to Workspace"**
3. Copy the new token
4. Update your `.env` file

### "missing_scope" error

**Solution:** Add required scopes
1. Go to OAuth & Permissions
2. Add scopes: `chat:write`, `chat:write.public`, `channels:read`
3. Click **"Reinstall to Workspace"**
4. Copy the new token

---

## 📝 Your App Details

**App ID:** A09V1G92CRW
**Client ID:** 1851400766544.9987553080880
**Direct Link:** https://api.slack.com/apps/A09V1G92CRW

**Required Channels:**
- `#accountability` (General team notifications)
- `#leadership` (Escalation alerts)

**Token Format:**

Your Bot Token will start with `xoxb-` followed by numbers and letters. It should be approximately 50-60 characters long.

Copy it exactly as shown in the Slack dashboard.

---

## 🎯 Next Steps After Setup

1. ✅ Bot token added to `.env`
2. ✅ Bot invited to channels
3. ✅ Test message sent successfully
4. ⏭️ Set up your production deployment
5. ⏭️ Configure automated reminders schedule
6. ⏭️ Train your team on using the dashboard

---

**Need help?** Check the main README.md or contact chris@loophire.com
