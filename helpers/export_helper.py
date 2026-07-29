"""
Export Helper Module — Generates CSV files for candidate database exports and candidate ranking comparisons.
"""
import io
import csv
from typing import List, Dict, Any


def generate_candidates_csv(candidates: List[Dict[str, Any]]) -> bytes:
    """
    Generates a CSV file buffer containing candidate database records.
    """
    output = io.StringIO()
    writer = csv.writer(output)

    # Header
    writer.writerow([
        "ID", "Candidate Name", "Email", "Phone", "ATS Score",
        "Recruiter Verdict", "Hiring Probability", "Seniority Level", "Created At"
    ])

    for c in candidates:
        writer.writerow([
            c.get("id", ""),
            c.get("candidate_name", "N/A"),
            c.get("email", "N/A"),
            c.get("phone", "N/A"),
            c.get("ats_score", 0),
            c.get("recruiter_verdict", "Under Review"),
            c.get("hiring_probability", "0%"),
            c.get("candidate_level", "Not Specified"),
            c.get("created_at", "")
        ])

    return output.getvalue().encode("utf-8")


def generate_candidate_rankings_csv(ranked_candidates: List[Dict[str, Any]]) -> bytes:
    """
    Generates a CSV file buffer for batch-ranked candidates.
    """
    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "Rank", "Candidate Name", "Overall ATS Score", "Recruiter Verdict",
        "Skills Score", "Experience Score", "Projects Score", "Formatting Score"
    ])

    for idx, c in enumerate(ranked_candidates, 1):
        full_json = c.get("full_json", {})
        ats_breakdown = full_json.get("ATS_Breakdown", {})
        writer.writerow([
            idx,
            c.get("candidate_name", f"Candidate {idx}"),
            c.get("ats_score", 0),
            c.get("recruiter_verdict", "Under Review"),
            ats_breakdown.get("Skills_Score", 0),
            ats_breakdown.get("Experience_Score", 0),
            ats_breakdown.get("Projects_Score", 0),
            ats_breakdown.get("Formatting_Score", 0),
        ])

    return output.getvalue().encode("utf-8")
