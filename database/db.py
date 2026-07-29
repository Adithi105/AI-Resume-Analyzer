"""
SQLite Database Layer — Handles persistent storage for the Enterprise Recruitment Platform.
Database file: database/recruitment.db
"""
import os
import sqlite3
import json
import hashlib
from typing import List, Dict, Any, Optional
from datetime import datetime

DB_DIR = os.path.dirname(__file__)
DB_FILE = os.path.join(DB_DIR, "recruitment.db")


def get_connection():
    """Returns a SQLite database connection with row factory configured."""
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def hash_password(password: str) -> str:
    """Hashes a password string using SHA-256."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def init_db():
    """Initializes SQLite database tables and seeds default demo accounts if empty."""
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        name TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('Admin', 'Recruiter', 'Candidate')),
        company TEXT DEFAULT 'Enterprise Talent Corp',
        created_at TEXT NOT NULL
    )
    """)

    # 2. Resumes Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resumes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        candidate_name TEXT NOT NULL,
        email TEXT,
        phone TEXT,
        ats_score INTEGER DEFAULT 0,
        recruiter_verdict TEXT DEFAULT 'Under Review',
        hiring_probability TEXT DEFAULT '0%',
        candidate_level TEXT DEFAULT 'Not Specified',
        raw_text TEXT,
        full_json TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    # 3. Interviews Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS interviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate_name TEXT NOT NULL,
        candidate_email TEXT,
        recruiter_name TEXT NOT NULL,
        role TEXT NOT NULL,
        interview_date TEXT NOT NULL,
        time_slot TEXT NOT NULL,
        interview_type TEXT DEFAULT 'Technical',
        status TEXT DEFAULT 'Scheduled' CHECK(status IN ('Scheduled', 'Completed', 'Cancelled')),
        notes TEXT,
        created_at TEXT NOT NULL
    )
    """)

    # 4. Companies Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS companies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        industry TEXT NOT NULL,
        domain TEXT,
        location TEXT,
        requisitions_count INTEGER DEFAULT 1,
        created_at TEXT NOT NULL
    )
    """)

    # 5. System Logs Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS system_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_type TEXT NOT NULL,
        user_email TEXT,
        details TEXT,
        created_at TEXT NOT NULL
    )
    """)

    conn.commit()

    # Seed Default Users if empty
    cursor.execute("SELECT COUNT(*) as cnt FROM users")
    count = cursor.fetchone()["cnt"]

    if count == 0:
        now = datetime.now().isoformat()
        default_users = [
            ("admin@recruimind.ai", hash_password("admin123"), "System Admin", "Admin", "Enterprise Talent HQ", now),
            ("recruiter@recruimind.ai", hash_password("recruiter123"), "Sarah Jenkins (Lead Recruiter)", "Recruiter", "Global Tech Recruiter", now),
            ("candidate@recruimind.ai", hash_password("candidate123"), "Alex Morgan", "Candidate", "Job Seeker", now),
        ]
        cursor.executemany(
            "INSERT INTO users (email, password_hash, name, role, company, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            default_users
        )
        conn.commit()

        # Seed Sample Companies
        default_companies = [
            ("Datadog Systems", "Cloud & Observability", "datadog.com", "New York, USA", 5, now),
            ("Stripe Financial", "Fintech Infrastructure", "stripe.com", "San Francisco, USA", 8, now),
            ("HashiCorp", "DevOps & IaC", "hashicorp.com", "Remote / USA", 3, now),
        ]
        cursor.executemany(
            "INSERT INTO companies (name, industry, domain, location, requisitions_count, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            default_companies
        )
        conn.commit()

    conn.close()


# ─── USER OPERATIONS ─────────────────────────────────────────────────────────

def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE LOWER(email) = LOWER(?)", (email.strip(),)).fetchone()
    conn.close()
    return dict(row) if row else None


def create_user(email: str, password: str, name: str, role: str = "Candidate", company: str = "") -> bool:
    try:
        conn = get_connection()
        conn.execute(
            "INSERT INTO users (email, password_hash, name, role, company, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (email.strip().lower(), hash_password(password), name.strip(), role, company.strip(), datetime.now().isoformat())
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False


def get_all_users() -> List[Dict[str, Any]]:
    conn = get_connection()
    rows = conn.execute("SELECT id, email, name, role, company, created_at FROM users ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ─── RESUME OPERATIONS ───────────────────────────────────────────────────────

def save_resume_record(
    candidate_name: str,
    email: str,
    phone: str,
    ats_score: int,
    verdict: str,
    hiring_prob: str,
    candidate_level: str,
    raw_text: str,
    full_json: Dict[str, Any],
    user_id: Optional[int] = None
) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO resumes (user_id, candidate_name, email, phone, ats_score, recruiter_verdict, hiring_probability, candidate_level, raw_text, full_json, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        candidate_name,
        email,
        phone,
        ats_score,
        verdict,
        hiring_prob,
        candidate_level,
        raw_text,
        json.dumps(full_json),
        datetime.now().isoformat()
    ))
    res_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return res_id


def get_all_resumes() -> List[Dict[str, Any]]:
    conn = get_connection()
    rows = conn.execute("SELECT * FROM resumes ORDER BY ats_score DESC, id DESC").fetchall()
    conn.close()
    result = []
    for r in rows:
        d = dict(r)
        try:
            d["full_json"] = json.loads(d["full_json"]) if d["full_json"] else {}
        except Exception:
            d["full_json"] = {}
        result.append(d)
    return result


def get_resumes_by_user_id(user_id: int) -> List[Dict[str, Any]]:
    conn = get_connection()
    rows = conn.execute("SELECT * FROM resumes WHERE user_id = ? ORDER BY id DESC", (user_id,)).fetchall()
    conn.close()
    result = []
    for r in rows:
        d = dict(r)
        try:
            d["full_json"] = json.loads(d["full_json"]) if d["full_json"] else {}
        except Exception:
            d["full_json"] = {}
        result.append(d)
    return result


# ─── INTERVIEW OPERATIONS ────────────────────────────────────────────────────

def schedule_interview(
    candidate_name: str,
    candidate_email: str,
    recruiter_name: str,
    role: str,
    interview_date: str,
    time_slot: str,
    interview_type: str = "Technical",
    notes: str = ""
) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO interviews (candidate_name, candidate_email, recruiter_name, role, interview_date, time_slot, interview_type, status, notes, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, 'Scheduled', ?, ?)
    """, (
        candidate_name, candidate_email, recruiter_name, role,
        interview_date, time_slot, interview_type, notes, datetime.now().isoformat()
    ))
    int_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return int_id


def get_all_interviews() -> List[Dict[str, Any]]:
    conn = get_connection()
    rows = conn.execute("SELECT * FROM interviews ORDER BY interview_date ASC, time_slot ASC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_interview_status(interview_id: int, status: str):
    conn = get_connection()
    conn.execute("UPDATE interviews SET status = ? WHERE id = ?", (status, interview_id))
    conn.commit()
    conn.close()


# ─── COMPANY OPERATIONS ──────────────────────────────────────────────────────

def get_all_companies() -> List[Dict[str, Any]]:
    conn = get_connection()
    rows = conn.execute("SELECT * FROM companies ORDER BY id ASC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_company(name: str, industry: str, domain: str = "", location: str = "", reqs: int = 1) -> bool:
    try:
        conn = get_connection()
        conn.execute(
            "INSERT INTO companies (name, industry, domain, location, requisitions_count, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (name.strip(), industry.strip(), domain.strip(), location.strip(), reqs, datetime.now().isoformat())
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False


# ─── SYSTEM LOGS ─────────────────────────────────────────────────────────────

def log_system_event(event_type: str, user_email: str, details: str):
    try:
        conn = get_connection()
        conn.execute(
            "INSERT INTO system_logs (event_type, user_email, details, created_at) VALUES (?, ?, ?, ?)",
            (event_type, user_email, details, datetime.now().isoformat())
        )
        conn.commit()
        conn.close()
    except Exception:
        pass


def get_system_logs() -> List[Dict[str, Any]]:
    conn = get_connection()
    rows = conn.execute("SELECT * FROM system_logs ORDER BY id DESC LIMIT 100").fetchall()
    conn.close()
    return [dict(r) for r in rows]
