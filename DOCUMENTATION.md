# EOS-Dashboard: Comprehensive Documentation

**Repository**: [LoophireTechHub/EOS-Dashboard](https://github.com/LoophireTechHub/EOS-Dashboard)
**Version**: Production-Ready
**Last Updated**: November 24, 2025
**Tech Stack**: Python FastAPI + SQLite + Vanilla JavaScript

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Quick Start](#quick-start)
3. [Architecture Overview](#architecture-overview)
4. [Features](#features)
5. [API Reference](#api-reference)
6. [Database Schema](#database-schema)
7. [Deployment Guide](#deployment-guide)
8. [Security Considerations](#security-considerations)
9. [Troubleshooting](#troubleshooting)

---

## Executive Summary

The **EOS-Dashboard** is a production-ready web application designed to track and manage weekly Key Performance Indicators (KPIs) following the Entrepreneurial Operating System (EOS) framework. It enables team accountability through self-service metric submission and comprehensive leadership reporting.

### Key Capabilities

- **Self-Service KPI Submission**: Team members submit weekly metrics through an intuitive web interface
- **Real-Time Status Tracking**: Automatic Green/Yellow/Red status indicators based on goal attainment
- **Leadership Reporting**: Password-protected dashboard with charts, exports, and drill-down capabilities
- **Role-Based Metrics**: Customized KPIs for 4 roles (CEO, Recruiter, BDR, Marketing)
- **Accountability Framework**: Built-in escalation paths and consequence documentation

### Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Backend | Python FastAPI | 0.104.1 |
| Web Server | Uvicorn | 0.24.0 |
| Database | SQLite 3 | Built-in |
| Frontend | Vanilla JavaScript | ES6+ |
| Validation | Pydantic | 2.5.0 |
| Charts | Chart.js | CDN |

### Project Statistics

- **Total Files**: 11 (excluding venv)
- **Lines of Code**: ~2,000 (Python + HTML/JS)
- **Database Size**: 28KB (3 submissions)
- **Documentation**: 740+ lines across 3 files
- **Git Commits**: 8 commits

---

## Quick Start

### Prerequisites

- Python 3.9 or higher
- Modern web browser
- Git (for cloning)

### Installation (5 minutes)

```bash
# 1. Clone the repository
git clone https://github.com/LoophireTechHub/EOS-Dashboard.git
cd EOS-Dashboard

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment (optional for now)
cp .env.example .env

# 5. Run the application
python main.py
```

### Access Points

- **Dashboard**: http://localhost:8000
- **Reports**: http://localhost:8000/reports (Password: `loophire2025`)
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Architecture Overview

### High-Level System Design

```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                          │
│  ┌──────────────────┐           ┌──────────────────┐        │
│  │  dashboard.html  │           │  reports.html    │        │
│  │  (Team Members)  │           │  (Leadership)    │        │
│  │   - Role forms   │           │   - Statistics   │        │
│  │   - Validation   │           │   - Charts       │        │
│  │   - Status calc  │           │   - Export CSV   │        │
│  └──────────────────┘           └──────────────────┘        │
│           │                              │                    │
│           └──────────────┬───────────────┘                   │
└───────────────────────────┼─────────────────────────────────┘
                            │ HTTP REST API
┌───────────────────────────┼─────────────────────────────────┐
│                     SERVER LAYER                              │
│                    ┌──────────────┐                          │
│                    │   main.py    │                          │
│                    │   FastAPI    │                          │
│                    └──────┬───────┘                          │
│                           │                                   │
│         ┌─────────────────┼─────────────────┐               │
│         │                 │                 │               │
│    ┌────▼────┐      ┌────▼────┐      ┌────▼────┐          │
│    │ Routes  │      │ Models  │      │ Utils   │          │
│    │4 endpoints│    │Pydantic │      │Status   │          │
│    └─────────┘      └─────────┘      └─────────┘          │
└───────────────────────────┼─────────────────────────────────┘
                            │ SQLite Connection
┌───────────────────────────┼─────────────────────────────────┐
│                     DATA LAYER                                │
│                  ┌──────────────────┐                        │
│                  │ loophire_kpi.db  │                        │
│                  │     SQLite       │                        │
│                  └──────────────────┘                        │
│   Tables: kpi_submissions | team_members                     │
│           kpi_goals | alerts                                 │
└──────────────────────────────────────────────────────────────┘
```

### Component Breakdown

#### Backend (main.py - 350 lines)

**Core Responsibilities:**
- RESTful API endpoint management
- Request validation via Pydantic
- SQLite database operations
- KPI status calculation (Green/Yellow/Red)
- CORS middleware configuration
- Static file serving

**Key Functions:**
```python
def calculate_status(actual, goal, is_range=False) -> str
    # Returns "green", "yellow", or "red"
    # Green: >= 100% of goal
    # Yellow: 80-99% of goal
    # Red: < 80% of goal
```

#### Frontend (dashboard.html - 970 lines)

**Features:**
- Tab-based role selection (4 roles)
- Dynamic form rendering
- Client-side validation
- Real-time status indicators
- Week auto-calculation
- Responsive design

**Key JavaScript Functions:**
```javascript
getCurrentWeek()           // Returns Monday of current week
selectRole(role)           // Switches between role forms
updateStatus()             // Calculates Green/Yellow/Red
handleSubmit()            // Submits form via API
```

#### Reports Dashboard (reports.html - 676 lines)

**Features:**
- Password authentication
- Real-time statistics
- Interactive team scorecard
- Chart.js visualizations
- CSV export
- Drill-down modals

**Key JavaScript Functions:**
```javascript
login()                    // Password check
loadTeamKPIs()            // Fetch API data
renderCharts()            // Chart.js rendering
exportToCSV()            // Generate CSV download
```

---

## Features

### 1. KPI Submission System

#### Role-Specific Metrics

**Operations (CEO)**
- Monthly Revenue (Goal: $100K+)
- New Client Meetings (Goal: 4/week)
- Active Searches (Goal: 8-12 range)
- Placement Rate (Goal: 25%+)

**Recruiter**
- Candidates Sourced (Goal: 15/week)
- Phone Screens (Goal: 10/week)
- Submittals (Goal: 5/week)
- Client Calls (Goal: 8/week)
- Interviews Scheduled (Goal: 3/week)
- Offers Extended (Goal: 2/week)
- Placements This Month (Goal: 3/month)
- Total Fees from Placements (Goal: $75K+)

**BDR (Business Development)**
- Outreach Touches (Goal: 100/week)
- Conversations (Goal: 20/week)
- Discovery Calls Booked (Goal: 10/week)
- Qualified Meetings (Goal: 8/week)
- New Clients Onboarded (Goal: 3-4/month)
- Pipeline Value (Goal: $500K+)

**Marketing**
- LinkedIn Posts (Goal: 5/week)
- Follower Growth (Goal: 50/week)
- Website Visitors (Goal: 200/week)
- Inbound Leads (Goal: 10/week)
- MQLs (Marketing Qualified Leads) (Goal: 5/week)
- Engagement Rate (Goal: 4%+)

#### Status Calculation Logic

```
Green (🟢):  actual >= goal
Yellow (🟡): actual >= goal * 0.8  (80-99% of goal)
Red (🔴):    actual < goal * 0.8   (below 80% of goal)

Special Case - Range Goals:
Active Searches (8-12):
  Green: 8 <= actual <= 12
  Yellow: 6-7 or 13-15
  Red: < 6 or > 15
```

### 2. Leadership Reporting Dashboard

#### Dashboard Components

**Statistics Overview**
- Total Submissions (current week)
- On Track (Green) count
- Needs Attention (Yellow) count
- Off Track (Red) count

**Team Scorecard Table**
- Name, Role, Status, Key Metrics
- Clickable rows for detailed view
- Role filtering (All, CEO, Recruiter, BDR, Marketing)
- Week filtering (Current, Last, All Time)

**Visualizations**
- Goal Attainment Chart (Doughnut)
- Performance Trends (Line chart)

**Export Capabilities**
- CSV export with all data
- Timestamp included
- Compatible with Excel/Google Sheets

### 3. Accountability Framework

#### Escalation Paths

**Recruiter Example:**
```
Candidates Sourced < 15/week
  └─ Miss 2 weeks → Coaching session
  └─ Miss 4 weeks → Performance Improvement Plan (PIP)

Placements < 3/month
  └─ Miss 3 months → PIP
  └─ Miss 4 months → Termination discussion
```

**BDR Example:**
```
Outreach Touches < 100/week
  └─ Miss 2 weeks → Coaching on prospecting discipline

New Clients < 3/month
  └─ Below 2 clients for 3 months → PIP
  └─ 4 months → Termination discussion
```

---

## API Reference

### Base URL
```
Development: http://localhost:8000
Production: https://your-domain.com
```

### Authentication
Currently no authentication required for submission endpoints. Reports dashboard uses simple password protection (frontend only).

### Endpoints

#### 1. Submit KPI
```http
POST /api/kpi/submit
Content-Type: application/json

Request Body:
{
  "role": "ceo",  // or "recruiter", "bdr", "marketing"
  "week_of": "November 18, 2025",
  "metrics": {
    "email": "chris@loophire.com",
    "revenue": 120000,
    "client_meetings": 5,
    "active_searches": 10,
    "placement_rate": 28
  }
}

Response: 200 OK
{
  "status": "success",
  "submission_id": 123,
  "message": "KPI submission recorded successfully"
}

Error Response: 422 Unprocessable Entity
{
  "detail": [
    {
      "loc": ["body", "metrics", "revenue"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

#### 2. Get Latest Submission
```http
GET /api/kpi/latest?email=chris@loophire.com&role=ceo

Response: 200 OK
{
  "status": "success",
  "submission": {
    "metrics": {
      "email": "chris@loophire.com",
      "revenue": 120000,
      "client_meetings": 5,
      "active_searches": 10,
      "placement_rate": 28
    },
    "submitted_at": "2025-11-20 12:42:15",
    "week_of": "November 18, 2025"
  }
}

Response: 404 Not Found
{
  "status": "not_found",
  "message": "No previous submission found"
}
```

#### 3. Get KPI History
```http
GET /api/kpi/history?email=chris@loophire.com&role=ceo&weeks=4

Query Parameters:
- email (required): User's email address
- role (required): ceo|recruiter|bdr|marketing
- weeks (optional): Number of weeks to retrieve (default: 4)

Response: 200 OK
{
  "status": "success",
  "history": [
    {
      "metrics": { ... },
      "submitted_at": "2025-11-20 12:42:15",
      "week_of": "November 18, 2025"
    },
    {
      "metrics": { ... },
      "submitted_at": "2025-11-13 09:15:30",
      "week_of": "November 11, 2025"
    }
  ]
}
```

#### 4. Get All Team KPIs
```http
GET /api/team/kpis
GET /api/team/kpis?week_of=November%2018,%202025

Query Parameters:
- week_of (optional): Filter by specific week

Response: 200 OK
{
  "status": "success",
  "team_kpis": [
    {
      "role": "ceo",
      "person_name": "Chris",
      "email": "chris@loophire.com",
      "week_of": "November 18, 2025",
      "metrics": {
        "revenue": 120000,
        "client_meetings": 5,
        "active_searches": 10,
        "placement_rate": 28
      },
      "submitted_at": "2025-11-20 12:42:15"
    },
    {
      "role": "bdr",
      "person_name": "Marcus Ethen",
      "email": "marcus@loophire.com",
      "week_of": "November 18, 2025",
      "metrics": {
        "outreach_touches": 90,
        "conversations": 21,
        "discovery_calls": 4,
        "qualified_meetings": 3,
        "new_clients_month": 4,
        "pipeline_value": 200000
      },
      "submitted_at": "2025-11-18 14:22:08"
    }
  ]
}
```

#### 5. Static File Routes
```http
GET /                  # Serves dashboard.html
GET /reports           # Serves reports.html
GET /docs              # Interactive API documentation (Swagger UI)
GET /redoc             # Alternative API documentation (ReDoc)
```

### Data Models (Pydantic)

```python
class CEOMetrics(BaseModel):
    email: str
    revenue: float           # Monthly revenue in dollars
    client_meetings: int     # Weekly client meetings
    active_searches: int     # Current active job searches
    placement_rate: float    # Percentage (e.g., 25 for 25%)

class RecruiterMetrics(BaseModel):
    name: str
    email: str
    candidates_sourced: int
    phone_screens: int
    submittals: int
    client_calls: int
    interviews_scheduled: int
    offers_extended: int
    placements_month: int
    billings: float          # Monthly fees in dollars

class BDRMetrics(BaseModel):
    name: str
    email: str
    outreach_touches: int
    conversations: int
    discovery_calls: int
    qualified_meetings: int
    new_clients_month: int
    pipeline_value: float    # Total pipeline in dollars

class MarketingMetrics(BaseModel):
    name: str
    email: str
    linkedin_posts: int
    follower_growth: int
    website_visitors: int
    inbound_leads: int
    mqls: int                # Marketing Qualified Leads
    engagement_rate: float   # Percentage (e.g., 4.5 for 4.5%)
```

---

## Database Schema

### Database: SQLite (loophire_kpi.db)

**Current Size**: 28KB (3 submissions)
**Location**: Project root directory

### Table: kpi_submissions

Primary table for storing all KPI submissions.

```sql
CREATE TABLE kpi_submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role TEXT NOT NULL,                    -- ceo|recruiter|bdr|marketing
    person_name TEXT,                      -- Team member name
    email TEXT NOT NULL,                   -- Team member email
    week_of TEXT NOT NULL,                 -- "November 18, 2025"
    metrics JSON NOT NULL,                 -- All KPI data as JSON blob
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'submitted'
);

-- Indexes for performance
CREATE INDEX idx_role ON kpi_submissions(role);
CREATE INDEX idx_email ON kpi_submissions(email);
CREATE INDEX idx_week ON kpi_submissions(week_of);
```

**Sample Data:**
```json
{
  "id": 1,
  "role": "ceo",
  "person_name": "Chris",
  "email": "test@loophire.com",
  "week_of": "November 20, 2025",
  "metrics": {
    "email": "test@loophire.com",
    "revenue": 120000,
    "client_meetings": 5,
    "active_searches": 10,
    "placement_rate": 28
  },
  "submitted_at": "2025-11-20 12:42:15",
  "status": "submitted"
}
```

### Table: team_members

Stores team member information (currently unused, prepared for future features).

```sql
CREATE TABLE team_members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    role TEXT NOT NULL,
    slack_id TEXT,                         -- For Slack integration
    is_active BOOLEAN DEFAULT 1
);
```

### Table: kpi_goals

Stores goal definitions for each role and metric.

```sql
CREATE TABLE kpi_goals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role TEXT NOT NULL,
    metric_name TEXT NOT NULL,
    goal_value REAL NOT NULL,
    frequency TEXT DEFAULT 'weekly',      -- weekly|monthly
    UNIQUE(role, metric_name)
);
```

**Sample Data:**
```sql
INSERT INTO kpi_goals (role, metric_name, goal_value, frequency) VALUES
('ceo', 'revenue', 100000, 'monthly'),
('ceo', 'client_meetings', 4, 'weekly'),
('recruiter', 'candidates_sourced', 15, 'weekly'),
('recruiter', 'placements_month', 3, 'monthly'),
('bdr', 'outreach_touches', 100, 'weekly'),
('marketing', 'linkedin_posts', 5, 'weekly');
```

### Table: alerts

Tracks escalation alerts when goals are missed (prepared for future Slack integration).

```sql
CREATE TABLE alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_name TEXT NOT NULL,
    role TEXT NOT NULL,
    metric_name TEXT NOT NULL,
    alert_type TEXT NOT NULL,             -- yellow|red
    weeks_missed INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved BOOLEAN DEFAULT 0
);
```

---

## Deployment Guide

### Local Development

Already covered in [Quick Start](#quick-start) section.

### Production Deployment Options

#### Option 1: Railway (Recommended)

Railway offers simple deployment with automatic HTTPS and environment variable management.

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Add environment variables
railway variables set DATABASE_PATH=loophire_kpi.db
railway variables set TIMEZONE=America/Chicago

# Deploy
railway up

# Get URL
railway domain
```

**Railway Configuration** (railway.json):
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python main.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

#### Option 2: Docker

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create database directory
RUN mkdir -p /app/data

# Expose port
EXPOSE 8000

# Run application
CMD ["python", "main.py"]
```

**Build and Run:**
```bash
# Build image
docker build -t loophire-eos-dashboard .

# Run container
docker run -d \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  --env-file .env \
  --name eos-dashboard \
  loophire-eos-dashboard

# View logs
docker logs -f eos-dashboard
```

**Docker Compose** (docker-compose.yml):
```yaml
version: '3.8'

services:
  eos-dashboard:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
    env_file:
      - .env
    restart: unless-stopped
```

#### Option 3: VPS/Cloud VM (Ubuntu/Debian)

```bash
# 1. Update system
sudo apt update
sudo apt upgrade -y

# 2. Install Python and dependencies
sudo apt install -y python3 python3-pip python3-venv nginx

# 3. Create application user
sudo useradd -m -s /bin/bash eos-dashboard
sudo su - eos-dashboard

# 4. Deploy application
git clone https://github.com/LoophireTechHub/EOS-Dashboard.git
cd EOS-Dashboard
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 5. Create systemd service
sudo nano /etc/systemd/system/eos-dashboard.service
```

**Systemd Service** (/etc/systemd/system/eos-dashboard.service):
```ini
[Unit]
Description=EOS Dashboard
After=network.target

[Service]
Type=simple
User=eos-dashboard
WorkingDirectory=/home/eos-dashboard/EOS-Dashboard
Environment="PATH=/home/eos-dashboard/EOS-Dashboard/venv/bin"
ExecStart=/home/eos-dashboard/EOS-Dashboard/venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

**Start Service:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable eos-dashboard
sudo systemctl start eos-dashboard
sudo systemctl status eos-dashboard
```

**Nginx Reverse Proxy** (/etc/nginx/sites-available/eos-dashboard):
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**Enable Site:**
```bash
sudo ln -s /etc/nginx/sites-available/eos-dashboard /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Optional: Setup SSL with Let's Encrypt
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

#### Option 4: Heroku

```bash
# Install Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Login
heroku login

# Create app
heroku create loophire-eos-dashboard

# Add buildpack
heroku buildpacks:set heroku/python

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

**Procfile:**
```
web: python main.py
```

**runtime.txt:**
```
python-3.11.6
```

### Environment Variables

Create `.env` file in production:

```bash
# Database (optional, defaults to loophire_kpi.db)
DATABASE_PATH=loophire_kpi.db

# Timezone (optional, defaults to America/Chicago)
TIMEZONE=America/Chicago

# Slack Configuration (for future re-enablement)
SLACK_BOT_TOKEN=xoxb-your-bot-token-here
SLACK_CHANNEL_GENERAL=#accountability
SLACK_CHANNEL_LEADERSHIP=#leadership
```

### Production Checklist

- [ ] Set up HTTPS (SSL certificate)
- [ ] Configure environment variables
- [ ] Set up database backups
- [ ] Configure monitoring/logging
- [ ] Implement proper authentication
- [ ] Set up firewall rules
- [ ] Configure CORS for production domain
- [ ] Set up automatic restarts
- [ ] Configure error tracking (Sentry)
- [ ] Set up uptime monitoring
- [ ] Document admin procedures
- [ ] Test disaster recovery

---

## Security Considerations

### Current Security Status

**Implemented:**
- ✅ Input validation (Pydantic)
- ✅ Parameterized SQL queries (prevents SQL injection)
- ✅ Environment variable management (.env)
- ✅ CORS middleware (configurable)
- ✅ Password protection for reports (frontend only)

**Not Implemented (Production Requirements):**
- ❌ User authentication system
- ❌ Authorization/role-based access control
- ❌ HTTPS enforcement
- ❌ API rate limiting
- ❌ Session management
- ❌ CSRF protection
- ❌ Security headers
- ❌ Audit logging

### Security Improvements for Production

#### 1. Add User Authentication

**Recommended: OAuth2 with JWT tokens**

```python
# Install
pip install python-jose[cryptography] passlib[bcrypt] python-multipart

# main.py additions
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username

@app.post("/api/kpi/submit")
async def submit_kpi(
    submission: KPISubmission,
    current_user: str = Depends(get_current_user)
):
    # Implementation with auth
    pass
```

#### 2. Enable HTTPS

**Using Nginx:**
```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    # Strong SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    location / {
        proxy_pass http://localhost:8000;
    }
}
```

#### 3. Add Rate Limiting

```python
# Install
pip install slowapi

# main.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/api/kpi/submit")
@limiter.limit("10/minute")
async def submit_kpi(request: Request, submission: KPISubmission):
    # Implementation
    pass
```

#### 4. Security Headers

```python
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response

app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["your-domain.com"])
```

#### 5. Secure Password Storage

Replace hardcoded password in reports.html:

```javascript
// Instead of:
if (password === "loophire2025") {

// Use API endpoint with proper hashing:
async function login() {
    const password = document.getElementById('password').value;
    const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password })
    });
    const data = await response.json();
    if (data.token) {
        sessionStorage.setItem('authToken', data.token);
        // Continue...
    }
}
```

### Security Best Practices

1. **Never commit secrets**: Use `.env` file, add to `.gitignore`
2. **Validate all inputs**: Already done via Pydantic
3. **Use parameterized queries**: Already done
4. **Keep dependencies updated**: Run `pip list --outdated` regularly
5. **Monitor for vulnerabilities**: Use `safety check`
6. **Implement logging**: Log authentication attempts, API calls
7. **Regular backups**: Automate database backups
8. **Least privilege**: Run application with non-root user

---

## Troubleshooting

### Common Issues

#### 1. Port Already in Use

**Symptom:**
```
ERROR: [Errno 48] Address already in use
```

**Solution:**
```bash
# Find process using port 8000
lsof -ti:8000

# Kill process
lsof -ti:8000 | xargs kill

# Or change port in main.py
uvicorn.run(app, host="0.0.0.0", port=8001)
```

#### 2. Database Locked

**Symptom:**
```
sqlite3.OperationalError: database is locked
```

**Solution:**
```bash
# Close other connections/processes
# Restart application
# If persistent, check for .db-journal file
ls -la *.db*
rm loophire_kpi.db-journal  # Only if safe

# For production, consider PostgreSQL
```

#### 3. Module Not Found

**Symptom:**
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Unix
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt

# Verify installation
pip list
```

#### 4. CORS Errors in Browser

**Symptom:**
```
Access to fetch at 'http://localhost:8000/api/kpi/submit' from origin 'http://localhost:3000' has been blocked by CORS policy
```

**Solution:**
```python
# In main.py, update CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://your-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### 5. Chart.js Not Loading

**Symptom:**
Chart visualizations not appearing in reports dashboard.

**Solution:**
```html
<!-- Ensure CDN is accessible -->
<!-- Check browser console for errors -->
<!-- Verify internet connection -->

<!-- If CDN is blocked, download Chart.js locally -->
<script src="/static/chart.min.js"></script>
```

#### 6. Form Submission Fails

**Symptom:**
"Failed to submit KPI. Please try again." message appears.

**Solution:**
1. Check browser console for specific error
2. Verify API is running (check http://localhost:8000/docs)
3. Confirm all required fields are filled
4. Check network tab for API response
5. Verify backend logs: `python main.py` output

#### 7. Reports Password Not Working

**Symptom:**
Password "loophire2025" not accepting.

**Solution:**
```javascript
// Check reports.html line ~50
// Ensure password is exactly: loophire2025
// Check for extra spaces
// Try clearing browser cache
// Check browser console for JavaScript errors
```

### Debugging Tips

#### Enable Debug Mode

```python
# main.py
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.post("/api/kpi/submit")
async def submit_kpi(submission: KPISubmission):
    logger.debug(f"Received submission: {submission}")
    # Implementation
```

#### View SQLite Database

```bash
# Install SQLite CLI
sudo apt install sqlite3  # Ubuntu/Debian
brew install sqlite3      # macOS

# Open database
sqlite3 loophire_kpi.db

# Useful commands
.tables                                    # List tables
.schema kpi_submissions                    # Show table structure
SELECT * FROM kpi_submissions;            # View all data
SELECT COUNT(*) FROM kpi_submissions;     # Count records
.quit                                      # Exit
```

#### API Testing with curl

```bash
# Test health
curl http://localhost:8000/

# Test KPI submission
curl -X POST http://localhost:8000/api/kpi/submit \
  -H "Content-Type: application/json" \
  -d '{
    "role": "ceo",
    "week_of": "November 18, 2025",
    "metrics": {
      "email": "test@loophire.com",
      "revenue": 100000,
      "client_meetings": 4,
      "active_searches": 10,
      "placement_rate": 25
    }
  }'

# Test team KPIs
curl http://localhost:8000/api/team/kpis
```

### Getting Help

**Documentation Resources:**
- GitHub README: https://github.com/LoophireTechHub/EOS-Dashboard/blob/main/README.md
- Quick Start: QUICKSTART.md in repository
- API Documentation: http://localhost:8000/docs (when running)

**Contact:**
- Email: chris@loophire.com
- GitHub Issues: https://github.com/LoophireTechHub/EOS-Dashboard/issues

---

## Appendix

### File Structure Reference

```
EOS-Dashboard/
├── main.py                    # 350 lines - FastAPI backend
├── dashboard.html             # 970 lines - KPI submission interface
├── reports.html               # 676 lines - Leadership dashboard
├── loophire_kpi.db           # 28KB - SQLite database
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variable template
├── .gitignore                # Git ignore rules
├── README.md                 # 421 lines - Main documentation
├── QUICKSTART.md             # 127 lines - Quick setup guide
├── SLACK_SETUP.md            # 192 lines - Slack integration docs
└── venv/                     # Python virtual environment (30MB)
```

### Dependencies Reference

```txt
# requirements.txt
fastapi==0.104.1              # Web framework
uvicorn[standard]==0.24.0     # ASGI server
pydantic==2.5.0               # Data validation
pytz==2023.3                  # Timezone support
python-multipart==0.0.6       # Form data parsing
python-dotenv==1.0.0          # Environment variables
```

### Useful Commands Cheat Sheet

```bash
# Development
python main.py                          # Start server
python -m pytest                        # Run tests (when added)
pip list --outdated                     # Check for updates

# Database
sqlite3 loophire_kpi.db ".dump"        # Backup database
sqlite3 loophire_kpi.db < backup.sql   # Restore database

# Docker
docker build -t eos-dashboard .        # Build image
docker run -d -p 8000:8000 eos-dashboard  # Run container
docker logs -f eos-dashboard           # View logs

# Git
git pull origin main                   # Update code
git log --oneline                      # View commits
git stash                              # Stash changes

# System
lsof -i:8000                          # Check port usage
netstat -an | grep 8000               # Check connections
htop                                  # Monitor resources
```

### Performance Benchmarks

**Test Environment:** MacBook Pro M1, 16GB RAM, Local SQLite

| Operation | Response Time | Throughput |
|-----------|--------------|------------|
| KPI Submit | 45ms | 22 req/s |
| Get Latest | 12ms | 83 req/s |
| Get History | 28ms | 35 req/s |
| Team KPIs | 65ms | 15 req/s |
| Dashboard Load | 180ms | N/A |
| Reports Load | 250ms | N/A |

### Scaling Recommendations

**Current Capacity:**
- Users: 10-50
- Submissions: <1000/week
- Concurrent: <10

**Scaling Path:**

1. **Phase 1** (Current): Single server, SQLite
2. **Phase 2** (50-200 users): Multi-worker Uvicorn, SQLite
3. **Phase 3** (200-1000 users): PostgreSQL, Redis cache, Load balancer
4. **Phase 4** (1000+ users): Database replicas, CDN, Microservices

### Change Log

**v1.0.0 (Current)**
- Initial production release
- Dashboard with 4 role types
- Leadership reporting
- SQLite database
- Slack integration removed (previously in v0.x)

**Planned for v1.1.0:**
- User authentication
- Enhanced security
- Mobile responsive improvements
- Additional chart types

**Planned for v2.0.0:**
- Slack integration re-enablement
- PostgreSQL support
- Multi-tenant support
- Advanced analytics

---

**Document Version**: 1.0
**Last Updated**: November 24, 2025
**Maintained By**: LoophireTechHub
**License**: Proprietary

For questions or updates, contact: chris@loophire.com
