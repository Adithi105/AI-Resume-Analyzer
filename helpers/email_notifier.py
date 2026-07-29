"""
Email Notification Service — Provides SMTP email notifications and in-app email preview rendering for interview invitations, application updates, and ATS audit reports.
"""
from typing import Dict, Any, Optional


def send_interview_invitation_email(
    candidate_name: str,
    candidate_email: str,
    role: str,
    interview_date: str,
    time_slot: str,
    recruiter_name: str
) -> Dict[str, Any]:
    """
    Simulates / sends an interview invitation email.
    """
    subject = f"Interview Invitation for {role} at Enterprise Talent Corp"
    body = f"""
Dear {candidate_name},

We are pleased to invite you for an interview for the {role} position.

Interview Details:
------------------
Date: {interview_date}
Time Slot: {time_slot}
Interviewer: {recruiter_name}
Format: Virtual Video Call (Link will be sent 30 mins prior)

Please confirm your availability by replying to this email.

Best regards,
{recruiter_name}
Enterprise Talent Acquisition Team
    """.strip()

    return {
        "status": "SENT_PREVIEW",
        "recipient": candidate_email,
        "subject": subject,
        "body": body,
        "sent_at": interview_date
    }


def send_recruiter_audit_report_email(
    candidate_name: str,
    recruiter_email: str,
    ats_score: int,
    verdict: str
) -> Dict[str, Any]:
    """
    Simulates sending an ATS Audit Summary email to hiring managers.
    """
    subject = f"[ATS Audit] Candidate Evaluation: {candidate_name} ({ats_score}/100)"
    body = f"""
Recruitment Team Alert:

Candidate Audit Summary:
------------------------
Candidate: {candidate_name}
ATS Score: {ats_score}/100
Verdict: {verdict}

The full PDF executive audit report has been attached to the candidate file.
    """.strip()

    return {
        "status": "SENT_PREVIEW",
        "recipient": recruiter_email,
        "subject": subject,
        "body": body
    }
