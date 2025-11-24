# EOS-Dashboard: Code Reference Guide

**For Developers & Technical Stakeholders**

---

## Table of Contents

1. [Backend Code Reference (main.py)](#backend-code-reference)
2. [Frontend Code Reference (dashboard.html)](#frontend-code-reference)
3. [Reports Code Reference (reports.html)](#reports-code-reference)
4. [Database Operations](#database-operations)
5. [Code Patterns & Conventions](#code-patterns--conventions)
6. [Testing Guide](#testing-guide)
7. [Contributing Guidelines](#contributing-guidelines)

---

## Backend Code Reference

### File: main.py (350 lines)

**Location**: `/Users/loophire/EOS-Dashboard/main.py`

#### Imports & Dependencies

```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict, Optional, List
import sqlite3
from datetime import datetime
import pytz
import os
from dotenv import load_dotenv
```

#### Application Setup

```python
# Environment configuration
load_dotenv()

# FastAPI instance
app = FastAPI(
    title="Loophire KPI Dashboard",
    description="Track weekly KPIs following EOS framework",
    version="1.0.0"
)

# CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database configuration
DB_PATH = os.getenv("DATABASE_PATH", "loophire_kpi.db")
TIMEZONE = pytz.timezone(os.getenv("TIMEZONE", "America/Chicago"))
```

**Key Points:**
- Uses FastAPI for automatic OpenAPI documentation
- CORS enabled for development (needs restriction in production)
- Environment variables for configuration
- Timezone-aware datetime handling

#### Data Models

**1. CEO Metrics**
```python
class CEOMetrics(BaseModel):
    email: str
    revenue: float              # Monthly revenue ($100K+ goal)
    client_meetings: int        # Weekly meetings (4+ goal)
    active_searches: int        # Active job searches (8-12 range goal)
    placement_rate: float       # Percentage (25%+ goal)

# Example usage:
# ceo_data = CEOMetrics(
#     email="chris@loophire.com",
#     revenue=120000,
#     client_meetings=5,
#     active_searches=10,
#     placement_rate=28
# )
```

**2. Recruiter Metrics**
```python
class RecruiterMetrics(BaseModel):
    name: str
    email: str
    candidates_sourced: int     # Weekly (15+ goal)
    phone_screens: int          # Weekly (10+ goal)
    submittals: int            # Weekly (5+ goal)
    client_calls: int          # Weekly (8+ goal)
    interviews_scheduled: int   # Weekly (3+ goal)
    offers_extended: int       # Weekly (2+ goal)
    placements_month: int      # Monthly (3+ goal)
    billings: float            # Monthly fees ($75K+ goal)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Jane Doe",
                "email": "jane@loophire.com",
                "candidates_sourced": 18,
                "phone_screens": 12,
                "submittals": 6,
                "client_calls": 9,
                "interviews_scheduled": 4,
                "offers_extended": 2,
                "placements_month": 3,
                "billings": 80000
            }
        }
```

**3. BDR Metrics**
```python
class BDRMetrics(BaseModel):
    name: str
    email: str
    outreach_touches: int       # Weekly (100+ goal)
    conversations: int          # Weekly (20+ goal)
    discovery_calls: int        # Weekly (10+ goal)
    qualified_meetings: int     # Weekly (8+ goal)
    new_clients_month: int      # Monthly (3-4 goal)
    pipeline_value: float       # Total pipeline ($500K+ goal)
```

**4. Marketing Metrics**
```python
class MarketingMetrics(BaseModel):
    name: str
    email: str
    linkedin_posts: int         # Weekly (5+ goal)
    follower_growth: int        # Weekly (50+ goal)
    website_visitors: int       # Weekly (200+ goal)
    inbound_leads: int         # Weekly (10+ goal)
    mqls: int                  # Weekly MQLs (5+ goal)
    engagement_rate: float     # Percentage (4%+ goal)
```

**5. KPI Submission Wrapper**
```python
class KPISubmission(BaseModel):
    role: str                   # "ceo"|"recruiter"|"bdr"|"marketing"
    week_of: str               # "November 18, 2025"
    metrics: Dict              # Role-specific metrics as dict
    timestamp: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
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
        }
```

#### Database Operations

**1. Database Initialization**
```python
def init_db():
    """Initialize SQLite database with required tables."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Main KPI submissions table
    c.execute('''
        CREATE TABLE IF NOT EXISTS kpi_submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            person_name TEXT,
            email TEXT NOT NULL,
            week_of TEXT NOT NULL,
            metrics TEXT NOT NULL,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'submitted'
        )
    ''')

    # Team members table (for future use)
    c.execute('''
        CREATE TABLE IF NOT EXISTS team_members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            role TEXT NOT NULL,
            slack_id TEXT,
            is_active BOOLEAN DEFAULT 1
        )
    ''')

    # KPI goals table
    c.execute('''
        CREATE TABLE IF NOT EXISTS kpi_goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            metric_name TEXT NOT NULL,
            goal_value REAL NOT NULL,
            frequency TEXT DEFAULT 'weekly'
        )
    ''')

    # Alerts tracking table
    c.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_name TEXT NOT NULL,
            role TEXT NOT NULL,
            metric_name TEXT NOT NULL,
            alert_type TEXT NOT NULL,
            weeks_missed INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            resolved BOOLEAN DEFAULT 0
        )
    ''')

    conn.commit()
    conn.close()

# Initialize on startup
init_db()
```

**2. Insert Submission**
```python
def save_submission(role: str, person_name: str, email: str,
                   week_of: str, metrics: Dict) -> int:
    """
    Save KPI submission to database.

    Args:
        role: User role (ceo|recruiter|bdr|marketing)
        person_name: Team member name
        email: Team member email
        week_of: Week identifier (e.g., "November 18, 2025")
        metrics: Dictionary of role-specific metrics

    Returns:
        int: Submission ID
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Store metrics as JSON string
    import json
    metrics_json = json.dumps(metrics)

    c.execute('''
        INSERT INTO kpi_submissions
        (role, person_name, email, week_of, metrics)
        VALUES (?, ?, ?, ?, ?)
    ''', (role, person_name, email, week_of, metrics_json))

    submission_id = c.lastrowid
    conn.commit()
    conn.close()

    return submission_id
```

**3. Retrieve Submissions**
```python
def get_latest_submission(email: str, role: str) -> Optional[Dict]:
    """
    Get most recent submission for a user.

    Args:
        email: User's email address
        role: User's role

    Returns:
        Dict or None: Latest submission data
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('''
        SELECT metrics, submitted_at, week_of
        FROM kpi_submissions
        WHERE email = ? AND role = ?
        ORDER BY submitted_at DESC
        LIMIT 1
    ''', (email, role))

    result = c.fetchone()
    conn.close()

    if result:
        import json
        return {
            "metrics": json.loads(result[0]),
            "submitted_at": result[1],
            "week_of": result[2]
        }
    return None

def get_submission_history(email: str, role: str, weeks: int = 4) -> List[Dict]:
    """
    Get historical submissions for a user.

    Args:
        email: User's email address
        role: User's role
        weeks: Number of weeks to retrieve (default: 4)

    Returns:
        List[Dict]: Historical submissions
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('''
        SELECT metrics, submitted_at, week_of
        FROM kpi_submissions
        WHERE email = ? AND role = ?
        ORDER BY submitted_at DESC
        LIMIT ?
    ''', (email, role, weeks))

    results = c.fetchall()
    conn.close()

    import json
    return [
        {
            "metrics": json.loads(row[0]),
            "submitted_at": row[1],
            "week_of": row[2]
        }
        for row in results
    ]

def get_all_team_kpis(week_of: Optional[str] = None) -> List[Dict]:
    """
    Get KPI submissions for all team members.

    Args:
        week_of: Optional week filter

    Returns:
        List[Dict]: All team submissions
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    if week_of:
        query = '''
            SELECT role, person_name, email, week_of, metrics, submitted_at
            FROM kpi_submissions
            WHERE week_of = ?
            ORDER BY submitted_at DESC
        '''
        c.execute(query, (week_of,))
    else:
        query = '''
            SELECT role, person_name, email, week_of, metrics, submitted_at
            FROM kpi_submissions
            ORDER BY submitted_at DESC
        '''
        c.execute(query)

    results = c.fetchall()
    conn.close()

    import json
    return [
        {
            "role": row[0],
            "person_name": row[1],
            "email": row[2],
            "week_of": row[3],
            "metrics": json.loads(row[4]),
            "submitted_at": row[5]
        }
        for row in results
    ]
```

#### API Endpoints

**1. Static File Routes**
```python
@app.get("/")
async def serve_dashboard():
    """Serve main dashboard HTML."""
    return FileResponse("dashboard.html")

@app.get("/reports")
async def serve_reports():
    """Serve leadership reports HTML."""
    return FileResponse("reports.html")
```

**2. KPI Submission Endpoint**
```python
@app.post("/api/kpi/submit")
async def submit_kpi(submission: KPISubmission):
    """
    Submit weekly KPI metrics.

    Request Body:
        {
            "role": "ceo|recruiter|bdr|marketing",
            "week_of": "November 18, 2025",
            "metrics": { ... role-specific data ... }
        }

    Returns:
        {
            "status": "success",
            "submission_id": 123,
            "message": "KPI submission recorded successfully"
        }

    Raises:
        HTTPException: 422 if validation fails
        HTTPException: 500 if database error
    """
    try:
        # Validate role-specific metrics
        if submission.role == "ceo":
            validated_metrics = CEOMetrics(**submission.metrics)
        elif submission.role == "recruiter":
            validated_metrics = RecruiterMetrics(**submission.metrics)
        elif submission.role == "bdr":
            validated_metrics = BDRMetrics(**submission.metrics)
        elif submission.role == "marketing":
            validated_metrics = MarketingMetrics(**submission.metrics)
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid role: {submission.role}"
            )

        # Extract person info
        person_name = submission.metrics.get("name", "")
        email = submission.metrics.get("email", "")

        # Save to database
        submission_id = save_submission(
            role=submission.role,
            person_name=person_name,
            email=email,
            week_of=submission.week_of,
            metrics=submission.metrics
        )

        return {
            "status": "success",
            "submission_id": submission_id,
            "message": "KPI submission recorded successfully"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

**3. Latest Submission Endpoint**
```python
@app.get("/api/kpi/latest")
async def get_latest(email: str, role: str):
    """
    Get latest KPI submission for a user.

    Query Parameters:
        email: User's email address
        role: User's role (ceo|recruiter|bdr|marketing)

    Returns:
        {
            "status": "success",
            "submission": {
                "metrics": { ... },
                "submitted_at": "2025-11-20 12:42:15",
                "week_of": "November 18, 2025"
            }
        }

    Returns 404 if no submission found.
    """
    submission = get_latest_submission(email, role)

    if submission:
        return {
            "status": "success",
            "submission": submission
        }
    else:
        raise HTTPException(
            status_code=404,
            detail="No previous submission found"
        )
```

**4. History Endpoint**
```python
@app.get("/api/kpi/history")
async def get_history(email: str, role: str, weeks: int = 4):
    """
    Get KPI submission history for a user.

    Query Parameters:
        email: User's email address
        role: User's role
        weeks: Number of weeks to retrieve (default: 4)

    Returns:
        {
            "status": "success",
            "history": [
                {
                    "metrics": { ... },
                    "submitted_at": "2025-11-20 12:42:15",
                    "week_of": "November 18, 2025"
                },
                ...
            ]
        }
    """
    history = get_submission_history(email, role, weeks)

    return {
        "status": "success",
        "history": history
    }
```

**5. Team KPIs Endpoint**
```python
@app.get("/api/team/kpis")
async def get_team_kpis(week_of: Optional[str] = None):
    """
    Get KPI submissions for all team members.

    Query Parameters:
        week_of: Optional week filter (e.g., "November 18, 2025")

    Returns:
        {
            "status": "success",
            "team_kpis": [
                {
                    "role": "ceo",
                    "person_name": "Chris",
                    "email": "chris@loophire.com",
                    "week_of": "November 18, 2025",
                    "metrics": { ... },
                    "submitted_at": "2025-11-20 12:42:15"
                },
                ...
            ]
        }
    """
    team_kpis = get_all_team_kpis(week_of)

    return {
        "status": "success",
        "team_kpis": team_kpis
    }
```

#### Utility Functions

**Status Calculation (Client-side logic documented)**
```python
# Note: Status calculation is currently done client-side in JavaScript
# For future server-side implementation:

def calculate_status(actual: float, goal: float,
                    is_range: bool = False,
                    range_min: float = None,
                    range_max: float = None) -> str:
    """
    Calculate Green/Yellow/Red status.

    Args:
        actual: Actual value achieved
        goal: Goal value (or max for range)
        is_range: Whether this is a range goal
        range_min: Minimum for range goals
        range_max: Maximum for range goals

    Returns:
        str: "green", "yellow", or "red"

    Examples:
        >>> calculate_status(100, 100)
        "green"
        >>> calculate_status(85, 100)
        "yellow"
        >>> calculate_status(75, 100)
        "red"
        >>> calculate_status(10, 12, is_range=True, range_min=8, range_max=12)
        "green"
    """
    if is_range:
        if range_min <= actual <= range_max:
            return "green"
        elif (range_min * 0.8 <= actual < range_min or
              range_max < actual <= range_max * 1.25):
            return "yellow"
        else:
            return "red"
    else:
        if actual >= goal:
            return "green"
        elif actual >= goal * 0.8:
            return "yellow"
        else:
            return "red"
```

#### Server Startup

```python
if __name__ == "__main__":
    import uvicorn

    # Development server
    uvicorn.run(
        app,
        host="0.0.0.0",  # Listen on all interfaces
        port=8000,        # Default port
        reload=True       # Auto-reload on code changes (dev only)
    )

    # Production: Remove reload=True and consider:
    # - Multiple workers: workers=4
    # - Log level: log_level="info"
    # - SSL: ssl_keyfile="key.pem", ssl_certfile="cert.pem"
```

---

## Frontend Code Reference

### File: dashboard.html (970 lines)

**Location**: `/Users/loophire/EOS-Dashboard/dashboard.html`

#### Structure Overview

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Meta tags, styling -->
</head>
<body>
    <!-- Header -->
    <!-- Role Selection Tabs -->
    <!-- Role-Specific Forms (4 forms) -->
    <!-- JavaScript Logic -->
</body>
</html>
```

#### Key JavaScript Functions

**1. Week Calculation**
```javascript
/**
 * Get the Monday of the current week
 * @returns {string} Date string like "November 18, 2025"
 */
function getCurrentWeek() {
    const today = new Date();
    const day = today.getDay();
    const diff = today.getDate() - day + (day === 0 ? -6 : 1);
    const monday = new Date(today.setDate(diff));

    return monday.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// Usage: Auto-populate week_of fields
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('week-of-ceo').value = getCurrentWeek();
    document.getElementById('week-of-recruiter').value = getCurrentWeek();
    document.getElementById('week-of-bdr').value = getCurrentWeek();
    document.getElementById('week-of-marketing').value = getCurrentWeek();
});
```

**2. Role Selection**
```javascript
/**
 * Switch between role-specific forms
 * @param {string} role - Role identifier (ceo|recruiter|bdr|marketing)
 */
function selectRole(role) {
    // Hide all forms
    document.querySelectorAll('.form-container').forEach(form => {
        form.style.display = 'none';
    });

    // Remove active class from all tabs
    document.querySelectorAll('.role-tab').forEach(tab => {
        tab.classList.remove('active');
    });

    // Show selected form
    document.getElementById(`${role}-form`).style.display = 'block';

    // Activate selected tab
    event.target.classList.add('active');
}
```

**3. Status Calculation (Real-time)**
```javascript
/**
 * Update status indicator based on goal attainment
 * @param {string} inputId - Input field ID
 * @param {number} goal - Goal value
 * @param {string} statusId - Status span ID
 */
function updateStatus(inputId, goal, statusId) {
    const input = document.getElementById(inputId);
    const status = document.getElementById(statusId);
    const actual = parseFloat(input.value) || 0;

    // Calculate percentage
    const percentage = (actual / goal) * 100;

    // Set status and color
    if (percentage >= 100) {
        status.textContent = '🟢 Green';
        status.className = 'status green';
    } else if (percentage >= 80) {
        status.textContent = '🟡 Yellow';
        status.className = 'status yellow';
    } else {
        status.textContent = '🔴 Red';
        status.className = 'status red';
    }
}

/**
 * Update status for range-based goals (e.g., 8-12 active searches)
 * @param {string} inputId - Input field ID
 * @param {number} min - Minimum goal value
 * @param {number} max - Maximum goal value
 * @param {string} statusId - Status span ID
 */
function updateStatusRange(inputId, min, max, statusId) {
    const input = document.getElementById(inputId);
    const status = document.getElementById(statusId);
    const actual = parseFloat(input.value) || 0;

    if (actual >= min && actual <= max) {
        status.textContent = '🟢 Green';
        status.className = 'status green';
    } else if ((actual >= min * 0.8 && actual < min) ||
               (actual > max && actual <= max * 1.25)) {
        status.textContent = '🟡 Yellow';
        status.className = 'status yellow';
    } else {
        status.textContent = '🔴 Red';
        status.className = 'status red';
    }
}

// Example usage in HTML:
// <input type="number" id="revenue" oninput="updateStatus('revenue', 100000, 'status-revenue')">
// <span id="status-revenue" class="status"></span>
```

**4. Form Submission**
```javascript
/**
 * Handle KPI form submission
 * @param {Event} event - Form submit event
 * @param {string} role - Role identifier
 */
async function handleSubmit(event, role) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);

    // Build metrics object based on role
    let metrics = {};

    if (role === 'ceo') {
        metrics = {
            email: formData.get('email'),
            revenue: parseFloat(formData.get('revenue')),
            client_meetings: parseInt(formData.get('client_meetings')),
            active_searches: parseInt(formData.get('active_searches')),
            placement_rate: parseFloat(formData.get('placement_rate'))
        };
    } else if (role === 'recruiter') {
        metrics = {
            name: formData.get('name'),
            email: formData.get('email'),
            candidates_sourced: parseInt(formData.get('candidates_sourced')),
            phone_screens: parseInt(formData.get('phone_screens')),
            submittals: parseInt(formData.get('submittals')),
            client_calls: parseInt(formData.get('client_calls')),
            interviews_scheduled: parseInt(formData.get('interviews_scheduled')),
            offers_extended: parseInt(formData.get('offers_extended')),
            placements_month: parseInt(formData.get('placements_month')),
            billings: parseFloat(formData.get('billings'))
        };
    }
    // ... similar for bdr and marketing

    // Build submission payload
    const payload = {
        role: role,
        week_of: formData.get('week_of'),
        metrics: metrics
    };

    try {
        // Submit to API
        const response = await fetch('/api/kpi/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (response.ok) {
            // Success message
            alert('✅ KPI submitted successfully!');
            form.reset();
            // Repopulate week
            form.querySelector('[name="week_of"]').value = getCurrentWeek();
        } else {
            // Error message
            alert('❌ Failed to submit: ' + data.detail);
        }
    } catch (error) {
        console.error('Submission error:', error);
        alert('❌ Network error. Please try again.');
    }
}
```

#### CSS Styling Highlights

```css
/* Gradient background */
body {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Form container */
.form-container {
    background: white;
    border-radius: 12px;
    padding: 30px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.1);
}

/* Status indicators */
.status.green { color: #10b981; font-weight: bold; }
.status.yellow { color: #f59e0b; font-weight: bold; }
.status.red { color: #ef4444; font-weight: bold; }

/* Role tabs */
.role-tab {
    padding: 12px 24px;
    background: white;
    border: none;
    cursor: pointer;
    transition: all 0.3s;
}

.role-tab.active {
    background: #667eea;
    color: white;
    border-bottom: 3px solid #764ba2;
}

/* Input fields */
input[type="number"], input[type="email"], input[type="text"] {
    width: 100%;
    padding: 10px;
    border: 2px solid #e5e7eb;
    border-radius: 6px;
    font-size: 14px;
}

input:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}
```

---

## Reports Code Reference

### File: reports.html (676 lines)

**Location**: `/Users/loophire/EOS-Dashboard/reports.html`

#### Structure Overview

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Chart.js CDN -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <!-- Login Screen -->
    <div id="login-screen">...</div>

    <!-- Dashboard (hidden until login) -->
    <div id="dashboard" style="display: none;">
        <!-- Statistics Cards -->
        <!-- Filters -->
        <!-- Team Scorecard Table -->
        <!-- Charts -->
        <!-- Detail Modal -->
    </div>
</body>
</html>
```

#### Key JavaScript Functions

**1. Authentication**
```javascript
/**
 * Simple password-based login
 * NOTE: For production, replace with proper authentication
 */
function login() {
    const password = document.getElementById('password').value;

    // Hardcoded password (TODO: Move to backend auth)
    if (password === 'loophire2025') {
        document.getElementById('login-screen').style.display = 'none';
        document.getElementById('dashboard').style.display = 'block';
        sessionStorage.setItem('authenticated', 'true');
        loadDashboard();
    } else {
        alert('Incorrect password');
    }
}

function logout() {
    sessionStorage.removeItem('authenticated');
    location.reload();
}

// Check authentication on page load
window.addEventListener('DOMContentLoaded', () => {
    if (sessionStorage.getItem('authenticated') === 'true') {
        document.getElementById('login-screen').style.display = 'none';
        document.getElementById('dashboard').style.display = 'block';
        loadDashboard();
    }
});
```

**2. Data Loading**
```javascript
/**
 * Load dashboard data from API
 */
async function loadDashboard() {
    try {
        const response = await fetch('/api/team/kpis');
        const data = await response.json();

        if (data.status === 'success') {
            window.teamData = data.team_kpis;
            updateStats();
            renderTable();
            renderCharts();
        }
    } catch (error) {
        console.error('Failed to load dashboard:', error);
        alert('Failed to load data. Please refresh.');
    }
}

/**
 * Load KPIs for specific week
 */
async function loadTeamKPIs(weekOf = null) {
    const url = weekOf
        ? `/api/team/kpis?week_of=${encodeURIComponent(weekOf)}`
        : '/api/team/kpis';

    const response = await fetch(url);
    const data = await response.json();
    return data.team_kpis;
}
```

**3. Statistics Calculation**
```javascript
/**
 * Calculate and update dashboard statistics
 */
function updateStats() {
    const currentWeek = getCurrentWeek();
    const weekData = window.teamData.filter(kpi => kpi.week_of === currentWeek);

    // Count submissions
    const totalSubmissions = weekData.length;

    // Calculate statuses
    let greenCount = 0;
    let yellowCount = 0;
    let redCount = 0;

    weekData.forEach(kpi => {
        const status = calculateOverallStatus(kpi);
        if (status === 'green') greenCount++;
        else if (status === 'yellow') yellowCount++;
        else redCount++;
    });

    // Update DOM
    document.getElementById('total-submissions').textContent = totalSubmissions;
    document.getElementById('on-track').textContent = greenCount;
    document.getElementById('needs-attention').textContent = yellowCount;
    document.getElementById('off-track').textContent = redCount;
}

/**
 * Calculate overall status for a KPI submission
 * @param {Object} kpi - KPI submission object
 * @returns {string} Overall status (green|yellow|red)
 */
function calculateOverallStatus(kpi) {
    const metrics = kpi.metrics;
    const role = kpi.role;

    let greenCount = 0;
    let yellowCount = 0;
    let redCount = 0;
    let totalMetrics = 0;

    // Define goals based on role
    const goals = getGoalsForRole(role);

    // Calculate status for each metric
    Object.keys(metrics).forEach(key => {
        if (goals[key]) {
            totalMetrics++;
            const actual = metrics[key];
            const goal = goals[key];

            if (actual >= goal) greenCount++;
            else if (actual >= goal * 0.8) yellowCount++;
            else redCount++;
        }
    });

    // Overall status logic
    if (redCount > 0) return 'red';
    if (yellowCount > totalMetrics * 0.3) return 'yellow';
    return 'green';
}

/**
 * Get goal definitions for a role
 */
function getGoalsForRole(role) {
    const goals = {
        ceo: {
            revenue: 100000,
            client_meetings: 4,
            active_searches: { min: 8, max: 12 },
            placement_rate: 25
        },
        recruiter: {
            candidates_sourced: 15,
            phone_screens: 10,
            submittals: 5,
            interviews_scheduled: 3,
            placements_month: 3,
            billings: 75000
        },
        bdr: {
            outreach_touches: 100,
            conversations: 20,
            discovery_calls: 10,
            qualified_meetings: 8,
            new_clients_month: 3,
            pipeline_value: 500000
        },
        marketing: {
            linkedin_posts: 5,
            follower_growth: 50,
            website_visitors: 200,
            inbound_leads: 10,
            mqls: 5,
            engagement_rate: 4
        }
    };

    return goals[role] || {};
}
```

**4. Table Rendering**
```javascript
/**
 * Render team scorecard table
 */
function renderTable(filters = {}) {
    const tbody = document.getElementById('team-table-body');
    tbody.innerHTML = '';

    // Apply filters
    let filteredData = window.teamData;

    if (filters.role && filters.role !== 'all') {
        filteredData = filteredData.filter(kpi => kpi.role === filters.role);
    }

    if (filters.week) {
        filteredData = filteredData.filter(kpi => kpi.week_of === filters.week);
    }

    // Render rows
    filteredData.forEach((kpi, index) => {
        const row = document.createElement('tr');
        row.style.cursor = 'pointer';
        row.onclick = () => showPersonDetails(kpi);

        const status = calculateOverallStatus(kpi);
        const statusBadge = getStatusBadge(status);
        const keyMetrics = getKeyMetrics(kpi);

        row.innerHTML = `
            <td>${kpi.person_name || 'N/A'}</td>
            <td>${formatRole(kpi.role)}</td>
            <td>${formatDate(kpi.submitted_at)}</td>
            <td>${statusBadge}</td>
            <td>${keyMetrics}</td>
        `;

        tbody.appendChild(row);
    });
}

/**
 * Get status badge HTML
 */
function getStatusBadge(status) {
    const badges = {
        green: '<span class="badge badge-green">🟢 On Track</span>',
        yellow: '<span class="badge badge-yellow">🟡 Needs Attention</span>',
        red: '<span class="badge badge-red">🔴 Off Track</span>'
    };
    return badges[status] || '';
}

/**
 * Extract key metrics for display
 */
function getKeyMetrics(kpi) {
    const metrics = kpi.metrics;
    const role = kpi.role;

    if (role === 'ceo') {
        return `Revenue: $${(metrics.revenue / 1000).toFixed(0)}K, ` +
               `Meetings: ${metrics.client_meetings}`;
    } else if (role === 'recruiter') {
        return `Sourced: ${metrics.candidates_sourced}, ` +
               `Placements: ${metrics.placements_month}`;
    } else if (role === 'bdr') {
        return `Outreach: ${metrics.outreach_touches}, ` +
               `Meetings: ${metrics.qualified_meetings}`;
    } else if (role === 'marketing') {
        return `Posts: ${metrics.linkedin_posts}, ` +
               `Leads: ${metrics.inbound_leads}`;
    }
}
```

**5. Chart Rendering (Chart.js)**
```javascript
/**
 * Render dashboard charts
 */
function renderCharts() {
    renderGoalAttainmentChart();
    renderPerformanceTrends();
}

/**
 * Goal Attainment Doughnut Chart
 */
function renderGoalAttainmentChart() {
    const ctx = document.getElementById('goal-chart').getContext('2d');

    // Calculate data
    const currentWeek = getCurrentWeek();
    const weekData = window.teamData.filter(kpi => kpi.week_of === currentWeek);

    let greenCount = 0, yellowCount = 0, redCount = 0;
    weekData.forEach(kpi => {
        const status = calculateOverallStatus(kpi);
        if (status === 'green') greenCount++;
        else if (status === 'yellow') yellowCount++;
        else redCount++;
    });

    // Destroy existing chart if exists
    if (window.goalChart) window.goalChart.destroy();

    // Create chart
    window.goalChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['On Track', 'Needs Attention', 'Off Track'],
            datasets: [{
                data: [greenCount, yellowCount, redCount],
                backgroundColor: ['#10b981', '#f59e0b', '#ef4444'],
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                },
                title: {
                    display: true,
                    text: 'Team Goal Attainment'
                }
            }
        }
    });
}

/**
 * Performance Trends Line Chart
 */
function renderPerformanceTrends() {
    const ctx = document.getElementById('trend-chart').getContext('2d');

    // Get last 4 weeks
    const weeks = getLastNWeeks(4);

    // Calculate weekly averages
    const data = weeks.map(week => {
        const weekData = window.teamData.filter(kpi => kpi.week_of === week);
        const greenPercent = (weekData.filter(kpi =>
            calculateOverallStatus(kpi) === 'green'
        ).length / weekData.length) * 100 || 0;
        return greenPercent;
    });

    // Destroy existing chart
    if (window.trendChart) window.trendChart.destroy();

    // Create chart
    window.trendChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: weeks,
            datasets: [{
                label: '% On Track',
                data: data,
                borderColor: '#667eea',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        callback: value => value + '%'
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: '4-Week Performance Trend'
                }
            }
        }
    });
}
```

**6. CSV Export**
```javascript
/**
 * Export team data to CSV
 */
function exportToCSV() {
    // Build CSV header
    const headers = [
        'Name', 'Role', 'Week Of', 'Submitted At', 'Status',
        'Email', 'Metrics (JSON)'
    ];

    // Build CSV rows
    const rows = window.teamData.map(kpi => {
        const status = calculateOverallStatus(kpi);
        return [
            kpi.person_name || '',
            kpi.role,
            kpi.week_of,
            kpi.submitted_at,
            status,
            kpi.email,
            JSON.stringify(kpi.metrics)
        ];
    });

    // Combine into CSV string
    const csvContent = [
        headers.join(','),
        ...rows.map(row => row.map(cell => `"${cell}"`).join(','))
    ].join('\n');

    // Create download link
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `eos-dashboard-${new Date().toISOString().split('T')[0]}.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
}
```

**7. Detail Modal**
```javascript
/**
 * Show detailed view for a person's submission
 */
function showPersonDetails(kpi) {
    const modal = document.getElementById('detail-modal');
    const content = document.getElementById('modal-content');

    // Build detailed HTML
    let html = `
        <h2>${kpi.person_name} - ${formatRole(kpi.role)}</h2>
        <p><strong>Week:</strong> ${kpi.week_of}</p>
        <p><strong>Submitted:</strong> ${formatDate(kpi.submitted_at)}</p>
        <p><strong>Status:</strong> ${getStatusBadge(calculateOverallStatus(kpi))}</p>
        <hr>
        <h3>Metrics</h3>
        <table class="metrics-table">
    `;

    // Get goals for comparison
    const goals = getGoalsForRole(kpi.role);

    // Add each metric
    Object.keys(kpi.metrics).forEach(key => {
        if (key !== 'name' && key !== 'email') {
            const actual = kpi.metrics[key];
            const goal = goals[key];
            const status = goal ? calculateMetricStatus(actual, goal) : 'n/a';

            html += `
                <tr>
                    <td>${formatMetricName(key)}</td>
                    <td>${formatMetricValue(key, actual)}</td>
                    <td>${goal ? formatMetricValue(key, goal) : 'N/A'}</td>
                    <td>${getStatusBadge(status)}</td>
                </tr>
            `;
        }
    });

    html += '</table>';
    content.innerHTML = html;
    modal.style.display = 'block';
}

/**
 * Close detail modal
 */
function closeModal() {
    document.getElementById('detail-modal').style.display = 'none';
}
```

---

## Database Operations

### Common Queries

**1. Get all submissions for current week**
```sql
SELECT
    role, person_name, email, metrics, submitted_at
FROM kpi_submissions
WHERE week_of = 'November 18, 2025'
ORDER BY submitted_at DESC;
```

**2. Get historical data for trend analysis**
```sql
SELECT
    week_of,
    role,
    COUNT(*) as submission_count,
    AVG(CAST(json_extract(metrics, '$.revenue') AS REAL)) as avg_revenue
FROM kpi_submissions
WHERE role = 'ceo'
GROUP BY week_of, role
ORDER BY week_of DESC
LIMIT 4;
```

**3. Find missing submissions**
```sql
-- Team members who haven't submitted this week
SELECT
    tm.name, tm.email, tm.role
FROM team_members tm
LEFT JOIN kpi_submissions ks ON (
    tm.email = ks.email
    AND ks.week_of = 'November 18, 2025'
)
WHERE ks.id IS NULL
AND tm.is_active = 1;
```

**4. Get alerts for missed goals**
```sql
SELECT
    person_name,
    role,
    metric_name,
    alert_type,
    weeks_missed,
    created_at
FROM alerts
WHERE resolved = 0
ORDER BY weeks_missed DESC, created_at ASC;
```

**5. Calculate weekly compliance rate**
```sql
SELECT
    week_of,
    COUNT(DISTINCT email) as submitted_count,
    (SELECT COUNT(*) FROM team_members WHERE is_active = 1) as total_team,
    ROUND(
        (COUNT(DISTINCT email) * 100.0) /
        (SELECT COUNT(*) FROM team_members WHERE is_active = 1),
        2
    ) as compliance_rate
FROM kpi_submissions
GROUP BY week_of
ORDER BY week_of DESC;
```

### Database Maintenance

**Backup**
```bash
# Create backup
sqlite3 loophire_kpi.db ".backup loophire_kpi_backup_$(date +%Y%m%d).db"

# Or dump to SQL
sqlite3 loophire_kpi.db .dump > backup.sql
```

**Restore**
```bash
# From backup file
cp loophire_kpi_backup_20251124.db loophire_kpi.db

# From SQL dump
sqlite3 loophire_kpi.db < backup.sql
```

**Optimize**
```sql
-- Rebuild indexes
REINDEX;

-- Analyze query performance
ANALYZE;

-- Vacuum to reclaim space
VACUUM;
```

---

## Code Patterns & Conventions

### Naming Conventions

**Python (Backend)**
- Functions: `snake_case` (e.g., `get_latest_submission`)
- Classes: `PascalCase` (e.g., `CEOMetrics`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `DB_PATH`)
- Variables: `snake_case` (e.g., `submission_id`)

**JavaScript (Frontend)**
- Functions: `camelCase` (e.g., `getCurrentWeek`)
- Variables: `camelCase` (e.g., `teamData`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `API_URL`)
- DOM IDs: `kebab-case` (e.g., `week-of-ceo`)

**Database**
- Tables: `snake_case` (e.g., `kpi_submissions`)
- Columns: `snake_case` (e.g., `person_name`)

### Error Handling Patterns

**Backend**
```python
@app.post("/api/kpi/submit")
async def submit_kpi(submission: KPISubmission):
    try:
        # Validate
        if submission.role not in ['ceo', 'recruiter', 'bdr', 'marketing']:
            raise HTTPException(status_code=400, detail="Invalid role")

        # Process
        result = save_submission(...)

        return {"status": "success", "data": result}

    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
```

**Frontend**
```javascript
async function loadDashboard() {
    try {
        const response = await fetch('/api/team/kpis');

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();

        if (data.status !== 'success') {
            throw new Error('Invalid response format');
        }

        processData(data.team_kpis);

    } catch (error) {
        console.error('Load error:', error);
        alert('Failed to load dashboard. Please refresh.');
    }
}
```

### API Response Format

**Success Response**
```json
{
    "status": "success",
    "data": { ... },
    "message": "Optional success message"
}
```

**Error Response**
```json
{
    "status": "error",
    "detail": "Error description",
    "field": "Optional field name for validation errors"
}
```

---

## Testing Guide

### Unit Tests (Python)

**Setup**
```bash
pip install pytest pytest-cov

# Run tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=main --cov-report=html
```

**Example Test File: tests/test_api.py**
```python
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_submit_kpi_ceo():
    """Test CEO KPI submission"""
    payload = {
        "role": "ceo",
        "week_of": "November 18, 2025",
        "metrics": {
            "email": "test@loophire.com",
            "revenue": 120000,
            "client_meetings": 5,
            "active_searches": 10,
            "placement_rate": 28
        }
    }

    response = client.post("/api/kpi/submit", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "submission_id" in data

def test_submit_kpi_invalid_role():
    """Test invalid role rejection"""
    payload = {
        "role": "invalid",
        "week_of": "November 18, 2025",
        "metrics": {}
    }

    response = client.post("/api/kpi/submit", json=payload)
    assert response.status_code == 400

def test_get_latest_submission():
    """Test retrieving latest submission"""
    response = client.get(
        "/api/kpi/latest?email=test@loophire.com&role=ceo"
    )

    if response.status_code == 200:
        data = response.json()
        assert "submission" in data
    elif response.status_code == 404:
        # No submissions yet, acceptable
        pass
    else:
        pytest.fail(f"Unexpected status: {response.status_code}")

def test_get_team_kpis():
    """Test retrieving all team KPIs"""
    response = client.get("/api/team/kpis")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert isinstance(data["team_kpis"], list)
```

### Integration Tests

**Example: tests/test_integration.py**
```python
import pytest
import sqlite3
from main import init_db, save_submission, get_latest_submission

@pytest.fixture
def test_db():
    """Create test database"""
    test_db_path = "test_kpi.db"
    init_db()
    yield test_db_path
    # Cleanup
    import os
    if os.path.exists(test_db_path):
        os.remove(test_db_path)

def test_submission_flow(test_db):
    """Test end-to-end submission flow"""
    # Submit
    sub_id = save_submission(
        role="ceo",
        person_name="Test User",
        email="test@example.com",
        week_of="November 18, 2025",
        metrics={"revenue": 100000}
    )

    assert sub_id > 0

    # Retrieve
    submission = get_latest_submission("test@example.com", "ceo")

    assert submission is not None
    assert submission["metrics"]["revenue"] == 100000
```

### Frontend Tests (JavaScript)

**Setup with Jest**
```bash
npm install --save-dev jest @testing-library/dom

# Run tests
npm test
```

**Example: tests/dashboard.test.js**
```javascript
// Mock fetch
global.fetch = jest.fn();

describe('Dashboard Functions', () => {
    test('getCurrentWeek returns Monday', () => {
        const week = getCurrentWeek();
        const date = new Date(week);
        const day = date.getDay();
        expect(day).toBe(1); // Monday
    });

    test('calculateStatus returns correct status', () => {
        expect(calculateStatus(100, 100)).toBe('green');
        expect(calculateStatus(85, 100)).toBe('yellow');
        expect(calculateStatus(70, 100)).toBe('red');
    });

    test('API submission handles success', async () => {
        fetch.mockResolvedValueOnce({
            ok: true,
            json: async () => ({ status: 'success', submission_id: 123 })
        });

        const result = await submitKPI({...});
        expect(result.status).toBe('success');
    });
});
```

---

## Contributing Guidelines

### Development Workflow

1. **Clone repository**
   ```bash
   git clone https://github.com/LoophireTechHub/EOS-Dashboard.git
   cd EOS-Dashboard
   ```

2. **Create feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make changes**
   - Follow code conventions
   - Add tests
   - Update documentation

4. **Test changes**
   ```bash
   pytest tests/
   python main.py  # Manual testing
   ```

5. **Commit changes**
   ```bash
   git add .
   git commit -m "Add: Brief description of changes"
   ```

6. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   # Create pull request on GitHub
   ```

### Commit Message Format

```
<type>: <subject>

<body>

<footer>
```

**Types:**
- `Add:` New feature
- `Fix:` Bug fix
- `Update:` Modify existing feature
- `Refactor:` Code restructuring
- `Docs:` Documentation changes
- `Test:` Add/update tests
- `Style:` Formatting changes

**Example:**
```
Add: User authentication with JWT tokens

- Implement OAuth2 password flow
- Add JWT token generation
- Protect API endpoints
- Update documentation

Closes #42
```

### Code Review Checklist

- [ ] Code follows project conventions
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No hardcoded secrets
- [ ] Error handling implemented
- [ ] Security considerations addressed
- [ ] Performance impact assessed
- [ ] Backward compatibility maintained

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe testing performed

## Screenshots (if applicable)
Add screenshots

## Checklist
- [ ] Tests pass
- [ ] Documentation updated
- [ ] Code reviewed
```

---

## Additional Resources

### File Paths Reference
```
Backend:     /Users/loophire/EOS-Dashboard/main.py
Dashboard:   /Users/loophire/EOS-Dashboard/dashboard.html
Reports:     /Users/loophire/EOS-Dashboard/reports.html
Database:    /Users/loophire/EOS-Dashboard/loophire_kpi.db
Docs:        /Users/loophire/EOS-Dashboard/README.md
```

### External Documentation
- **FastAPI**: https://fastapi.tiangolo.com/
- **Pydantic**: https://docs.pydantic.dev/
- **Chart.js**: https://www.chartjs.org/docs/
- **SQLite**: https://www.sqlite.org/docs.html

### Contact
- **Email**: chris@loophire.com
- **GitHub**: https://github.com/LoophireTechHub/EOS-Dashboard

---

**Document Version**: 1.0
**Last Updated**: November 24, 2025
**Maintained By**: LoophireTechHub
