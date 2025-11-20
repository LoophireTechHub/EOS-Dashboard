"""
Loophire EOS KPI Tracking System
FastAPI backend with Slack integration
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List, Dict
import sqlite3
import json
from datetime import datetime, timedelta
import pytz
import os
from pathlib import Path
import requests
from apscheduler.schedulers.background import BackgroundScheduler
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Loophire EOS KPI System")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# CONFIGURATION
# ============================================================================

DATABASE_PATH = "loophire_kpi.db"
TIMEZONE = pytz.timezone("America/Chicago")

# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class CEOMetrics(BaseModel):
    email: str
    revenue: float
    client_meetings: int
    active_searches: int
    placement_rate: float

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
    billings: float

class BDRMetrics(BaseModel):
    name: str
    email: str
    outreach_touches: int
    conversations: int
    discovery_calls: int
    qualified_meetings: int
    new_clients_month: int
    pipeline_value: float

class MarketingMetrics(BaseModel):
    name: str
    email: str
    linkedin_posts: int
    follower_growth: int
    website_visitors: int
    inbound_leads: int
    mqls: int
    engagement_rate: float

class KPISubmission(BaseModel):
    role: str
    week_of: str
    metrics: Dict
    timestamp: Optional[str] = None

# ============================================================================
# DATABASE SETUP
# ============================================================================

def init_database():
    """Initialize SQLite database with tables"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # KPI Submissions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS kpi_submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            person_name TEXT,
            email TEXT NOT NULL,
            week_of TEXT NOT NULL,
            metrics JSON NOT NULL,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'submitted'
        )
    ''')

    # Team members table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS team_members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            role TEXT NOT NULL,
            slack_id TEXT,
            is_active BOOLEAN DEFAULT 1
        )
    ''')

    # KPI Goals table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS kpi_goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            metric_name TEXT NOT NULL,
            goal_value REAL NOT NULL,
            frequency TEXT DEFAULT 'weekly'
        )
    ''')

    # Alerts/Escalations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_name TEXT NOT NULL,
            role TEXT NOT NULL,
            metric_name TEXT NOT NULL,
            alert_type TEXT NOT NULL,
            weeks_missed INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            resolved BOOLEAN DEFAULT 0
        )
    ''')

    conn.commit()
    conn.close()

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_current_week():
    """Get formatted current week"""
    today = datetime.now(TIMEZONE)
    monday = today - timedelta(days=today.weekday())
    return monday.strftime("%B %d, %Y")

def calculate_status(actual: float, goal: float, metric_type: str = "min") -> str:
    """Calculate 🟢/🟡/🔴 status"""
    if metric_type == "range":
        min_val, max_val = goal, goal  # Adjust as needed
        if actual >= min_val and actual <= max_val:
            return "🟢"
        elif actual >= min_val * 0.8:
            return "🟡"
        return "🔴"

    if actual >= goal:
        return "🟢"
    elif actual >= goal * 0.8:
        return "🟡"
    return "🔴"

# Escalation tracking removed with Slack integration

# ============================================================================
# ROUTES
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize database"""
    init_database()

@app.get("/")
async def root():
    """Return dashboard HTML"""
    return FileResponse("dashboard.html")

@app.post("/api/kpi/submit")
async def submit_kpi(submission: KPISubmission):
    """Submit KPI metrics"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO kpi_submissions (role, person_name, email, week_of, metrics)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            submission.role,
            submission.metrics.get("name") or "Chris",
            submission.metrics.get("email"),
            submission.week_of,
            json.dumps(submission.metrics)
        ))

        conn.commit()
        submission_id = cursor.lastrowid
        conn.close()

        return {
            "status": "success",
            "submission_id": submission_id,
            "message": "KPI submission recorded"
        }

    except Exception as e:
        logger.error(f"Error submitting KPI: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/kpi/latest")
async def get_latest_kpi(email: str, role: str):
    """Get latest KPI submission for a person"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT metrics, submitted_at FROM kpi_submissions
            WHERE email = ? AND role = ?
            ORDER BY submitted_at DESC
            LIMIT 1
        ''', (email, role))

        result = cursor.fetchone()
        conn.close()

        if not result:
            return {"status": "not_found"}

        return {
            "status": "success",
            "metrics": json.loads(result[0]),
            "submitted_at": result[1]
        }

    except Exception as e:
        logger.error(f"Error fetching KPI: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/kpi/history")
async def get_kpi_history(email: str, role: str, weeks: int = 4):
    """Get KPI submission history"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT metrics, submitted_at, week_of FROM kpi_submissions
            WHERE email = ? AND role = ?
            ORDER BY submitted_at DESC
            LIMIT ?
        ''', (email, role, weeks))

        results = cursor.fetchall()
        conn.close()

        history = [
            {
                "metrics": json.loads(r[0]),
                "submitted_at": r[1],
                "week_of": r[2]
            }
            for r in results
        ]

        return {"status": "success", "history": history}

    except Exception as e:
        logger.error(f"Error fetching history: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/team/kpis")
async def get_all_team_kpis(week_of: Optional[str] = None):
    """Get all team KPIs for leadership view"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        if week_of:
            cursor.execute('''
                SELECT role, person_name, email, metrics FROM kpi_submissions
                WHERE week_of = ?
                ORDER BY role, person_name
            ''', (week_of,))
        else:
            # Get latest submission for each person
            cursor.execute('''
                SELECT role, person_name, email, metrics FROM kpi_submissions
                WHERE submitted_at >= datetime('now', '-7 days')
                ORDER BY role, person_name, submitted_at DESC
            ''')

        results = cursor.fetchall()
        conn.close()

        kpis = [
            {
                "role": r[0],
                "person_name": r[1],
                "email": r[2],
                "metrics": json.loads(r[3])
            }
            for r in results
        ]

        return {"status": "success", "team_kpis": kpis}

    except Exception as e:
        logger.error(f"Error fetching team KPIs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Slack integration removed - dashboard-only mode

# ============================================================================
# RUN
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
