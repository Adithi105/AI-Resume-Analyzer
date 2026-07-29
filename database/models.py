"""
Database Data Models & Dataclasses for Enterprise Recruitment Platform.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime


@dataclass
class User:
    id: Optional[int]
    email: str
    name: str
    role: str  # Admin, Recruiter, Candidate
    company: str = "Enterprise Talent Corp"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class ResumeRecord:
    id: Optional[int]
    candidate_name: str
    email: str
    phone: str
    ats_score: int
    recruiter_verdict: str
    hiring_probability: str
    candidate_level: str
    raw_text: str
    full_json: Dict[str, Any]
    user_id: Optional[int] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class Interview:
    id: Optional[int]
    candidate_name: str
    candidate_email: str
    recruiter_name: str
    role: str
    interview_date: str
    time_slot: str
    interview_type: str = "Technical"
    status: str = "Scheduled"  # Scheduled, Completed, Cancelled
    notes: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class Company:
    id: Optional[int]
    name: str
    industry: str
    domain: str = ""
    location: str = ""
    requisitions_count: int = 1
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
