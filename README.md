# 📊 Loophire EOS KPI Dashboard

**Production-ready EOS Weekly Scorecard System** with Python FastAPI backend, interactive dashboard, and automated Slack integration.

## 🚀 Features

### Core Functionality
- ✅ **Multi-role KPI tracking** (CEO, Recruiter, BDR, Marketing)
- ✅ **SQLite database** - Persistent storage with full history
- ✅ **Real-time status indicators** - 🟢 Green / 🟡 Yellow / 🔴 Red
- ✅ **RESTful API** - Submit and retrieve KPI data
- ✅ **Interactive web dashboard** - Beautiful, responsive UI

### Slack Integration
- 📲 **Automated reminders**:
  - Monday 7:30 AM - Weekly kickoff reminder
  - Monday 8:00 AM - Hard deadline alert
  - Wednesday 3:30 PM - Mid-week check-in
  - Wednesday 4:00 PM - Mid-week deadline
- 🚨 **Escalation alerts**:
  - ⚠️ Yellow alerts (2 weeks below target)
  - 🔴 Red alerts (4+ weeks below target)
- 🎯 **Leadership notifications** - Performance alerts sent to leadership channel

### Metrics Tracked

**CEO Metrics:**
- Monthly Revenue (Goal: $100K+)
- New Client Meetings (Goal: 4/week)
- Active Searches (Goal: 8-12)
- Placement Rate (Goal: 25%+)

**Recruiter Metrics:**
- Candidates Sourced (Goal: 15/week)
- Phone Screens (Goal: 10/week)
- Submittals (Goal: 5/week)
- Client Calls (Goal: 8/week)
- Interviews Scheduled (Goal: 3/week)
- Placements This Month (Goal: 1-2/month)
- Monthly Billings (Goal: $20K+)

**BDR Metrics:**
- Outreach Touches (Goal: 100/week)
- Conversations (Goal: 20/week)
- Discovery Calls Booked (Goal: 10/week)
- Qualified Meetings (Goal: 8/week)
- New Clients Onboarded (Goal: 3-4/month)
- Pipeline Value (Goal: $500K+)

**Marketing Metrics:**
- LinkedIn Posts (Goal: 5/week)
- Follower Growth (Goal: 50/week)
- Website Visitors (Goal: 200/week)
- Inbound Leads (Goal: 10/week)
- MQLs (Goal: 5/week)
- Engagement Rate (Goal: 4%+)

---

## 📋 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/LoophireTechHub/EOS-Dashboard.git
cd EOS-Dashboard
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` file with your Slack webhook URL:

```bash
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
SLACK_CHANNEL_GENERAL=#accountability
SLACK_CHANNEL_LEADERSHIP=#leadership
```

### 5. Run the Application

```bash
python main.py
```

The application will start on `http://localhost:8000`

---

## 🔧 Slack Setup

### Create Slack Webhook

1. Go to https://api.slack.com/apps
2. Click **"Create New App"** → **"From scratch"**
3. Name it "Loophire EOS KPI Bot"
4. Select your workspace
5. Click **"Incoming Webhooks"** → Enable
6. Click **"Add New Webhook to Workspace"**
7. Select the channel (`#accountability`)
8. Copy the webhook URL to your `.env` file

### Test Slack Integration

```bash
curl -X POST http://localhost:8000/api/slack/send-reminder?submission_type=weekly_kickoff
```

---

## 📖 API Documentation

Once running, visit:
- **Dashboard**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **OpenAPI Schema**: http://localhost:8000/redoc

### Key Endpoints

**Submit KPI**
```bash
POST /api/kpi/submit
Content-Type: application/json

{
  "role": "ceo",
  "week_of": "November 18, 2025",
  "metrics": {
    "email": "chris@loophire.com",
    "revenue": 120000,
    "client_meetings": 5,
    "active_searches": 10,
    "placement_rate": 28
  }
}
```

**Get Latest KPI**
```bash
GET /api/kpi/latest?email=chris@loophire.com&role=ceo
```

**Get KPI History**
```bash
GET /api/kpi/history?email=chris@loophire.com&role=ceo&weeks=4
```

**Get All Team KPIs**
```bash
GET /api/team/kpis?week_of=November%2018,%202025
```

**Trigger Slack Reminder**
```bash
POST /api/slack/send-reminder?submission_type=weekly_kickoff
```

---

## 🗓️ Scheduled Reminders

The system automatically sends Slack reminders at:

| Day | Time | Type | Message |
|-----|------|------|---------|
| Monday | 7:30 AM CST | Weekly Kickoff | 30-minute warning for scorecard submission |
| Monday | 8:00 AM CST | Hard Deadline | Final call before L10 meeting (9:00 AM) |
| Wednesday | 3:30 PM CST | Mid-week Check | Progress update reminder |
| Wednesday | 4:00 PM CST | Mid-week Deadline | Final call for mid-week status |

---

## 🚨 Escalation System

### Yellow Alert (⚠️ Coaching Alert)
- Triggered after **2 consecutive weeks** below target
- Sent to general channel
- Triggers 1-on-1 coaching conversation

### Red Alert (🔴 Performance Alert)
- Triggered after **4+ consecutive weeks** below target
- Sent to leadership channel only
- Triggers Performance Improvement Plan discussion

---

## 📊 Database Schema

### `kpi_submissions`
```sql
id INTEGER PRIMARY KEY
role TEXT
person_name TEXT
email TEXT
week_of TEXT
metrics JSON
submitted_at TIMESTAMP
status TEXT
```

### `team_members`
```sql
id INTEGER PRIMARY KEY
name TEXT
email TEXT UNIQUE
role TEXT
slack_id TEXT
is_active BOOLEAN
```

### `kpi_goals`
```sql
id INTEGER PRIMARY KEY
role TEXT
metric_name TEXT
goal_value REAL
frequency TEXT
```

### `alerts`
```sql
id INTEGER PRIMARY KEY
person_name TEXT
role TEXT
metric_name TEXT
alert_type TEXT
weeks_missed INTEGER
created_at TIMESTAMP
resolved BOOLEAN
```

---

## 🎨 Customization

### Update KPI Goals

Edit goals in `main.py`:

```python
# Example: Change CEO revenue goal
if actual >= 150000:  # Changed from 100000
    return "🟢"
```

### Change Reminder Schedule

Edit scheduler in `main.py`:

```python
scheduler.add_job(
    lambda: send_kpi_reminder("all", "weekly_kickoff"),
    "cron",
    day_of_week="mon",
    hour=8,  # Change time here
    minute=0,
    id="monday_reminder"
)
```

### Update Dashboard URL

Replace `https://your-domain.com/dashboard` in:
- `main.py` (Slack messages)
- Deploy to your production domain

---

## 🚀 Deployment

### Option 1: Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
railway up
```

### Option 2: Heroku

```bash
# Create Heroku app
heroku create loophire-eos-dashboard

# Set environment variables
heroku config:set SLACK_WEBHOOK_URL=https://hooks.slack.com/...

# Deploy
git push heroku main
```

### Option 3: Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

```bash
docker build -t loophire-eos-dashboard .
docker run -p 8000:8000 --env-file .env loophire-eos-dashboard
```

---

## 🔐 Security Notes

- Never commit `.env` file (already in `.gitignore`)
- Use environment variables for all sensitive data
- Restrict Slack webhook to specific channels
- Consider adding authentication for production deployment

---

## 📝 Usage

### For Team Members

1. Visit the dashboard URL
2. Select your role (CEO, Recruiter, BDR, Marketing)
3. Fill in your weekly metrics
4. Submit before Monday 8:00 AM deadline
5. Status indicators show:
   - 🟢 Green = On or above goal
   - 🟡 Yellow = 80-99% of goal
   - 🔴 Red = Below 80% of goal

### For Leadership

- Access team KPIs via API endpoint
- Receive escalation alerts in leadership channel
- Review historical trends for coaching conversations

---

## 🛠️ Troubleshooting

**Slack messages not sending**
- Verify `SLACK_WEBHOOK_URL` in `.env`
- Test webhook manually with curl
- Check Slack app permissions

**Database errors**
- Delete `loophire_kpi.db` and restart (dev only)
- Check file permissions

**Scheduler not running**
- Verify timezone setting in `.env`
- Check server logs for errors

---

## 📞 Support

For issues or questions:
- GitHub Issues: https://github.com/LoophireTechHub/EOS-Dashboard/issues
- Email: chris@loophire.com

---

## 📄 License

MIT License - See LICENSE file for details

---

**Built with ❤️ by Loophire Tech Team**
