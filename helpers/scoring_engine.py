from typing import Dict, Any

# Enterprise ATS Weights Configuration (Total = 1.00 / 100%)
ATS_CATEGORY_WEIGHTS = {
    "Skills_Score": 0.25,
    "Experience_Score": 0.25,
    "Projects_Score": 0.15,
    "Keyword_Match_Score": 0.15,
    "Education_Score": 0.10,
    "Formatting_Score": 0.05,
    "Certifications_Score": 0.03,
    "Readability_Score": 0.02
}

def compute_weighted_ats_score(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Computes a professional weighted ATS score breakdown for 8 core categories:
    Skills, Experience, Projects, Keyword Match, Education, Formatting, Certifications, and Readability.
    
    Returns:
        Dict containing individual sub-category scores (0-100) and calculated Overall_ATS_Score.
    """
    raw_breakdown = data.get("ATS_Breakdown", {})
    if not isinstance(raw_breakdown, dict):
        raw_breakdown = {}

    def get_score_or_fallback(key: str, fallback_calc_fn) -> int:
        val = raw_breakdown.get(key, data.get(key))
        try:
            if val is not None:
                score = int(val)
                return max(0, min(100, score))
        except (ValueError, TypeError):
            pass
        return fallback_calc_fn()

    # 1. Skills Score (25% Weight)
    skills = data.get("Skills", [])
    tech_strengths = data.get("Technical_Strengths", [])
    skills_count = len(skills) + len(tech_strengths)
    skills_score = get_score_or_fallback(
        "Skills_Score",
        lambda: min(100, max(20, skills_count * 12 + 25)) if skills_count > 0 else 30
    )

    # 2. Experience Score (25% Weight)
    exp = data.get("Experience", [])
    exp_score = get_score_or_fallback(
        "Experience_Score",
        lambda: min(100, max(30, len(exp) * 25 + 30)) if exp else 40
    )

    # 3. Projects Score (15% Weight)
    projects = data.get("Projects", [])
    projects_score = get_score_or_fallback(
        "Projects_Score",
        lambda: min(100, max(20, len(projects) * 30 + 20)) if projects else 30
    )

    # 4. Keyword Match Score (15% Weight)
    missing = data.get("Missing_Skills", [])
    kw_score = get_score_or_fallback(
        "Keyword_Match_Score",
        lambda: max(30, 95 - len(missing) * 10)
    )

    # 5. Education Score (10% Weight)
    edu = data.get("Education", [])
    edu_score = get_score_or_fallback(
        "Education_Score",
        lambda: 90 if edu else 50
    )

    # 6. Formatting Score (5% Weight)
    name = data.get("Name", "")
    email = data.get("Email", "")
    phone = data.get("Phone", "")
    has_contact = (email != "Not Specified") and (phone != "Not Specified")
    risks = data.get("Resume_Risks", [])
    formatting_score = get_score_or_fallback(
        "Formatting_Score",
        lambda: max(30, 95 - len(risks) * 12) if has_contact else 60
    )

    # 7. Certifications Score (3% Weight)
    certs = data.get("Certifications", [])
    rec_certs = data.get("Recommended_Certifications", [])
    certs_score = get_score_or_fallback(
        "Certifications_Score",
        lambda: min(100, max(40, len(certs) * 30 + 40)) if certs else 50
    )

    # 8. Readability Score (2% Weight)
    readability_score = get_score_or_fallback(
        "Readability_Score",
        lambda: max(40, 92 - len(risks) * 8)
    )

    # Calculate Weighted Overall ATS Score
    weighted_sum = (
        skills_score * ATS_CATEGORY_WEIGHTS["Skills_Score"] +
        exp_score * ATS_CATEGORY_WEIGHTS["Experience_Score"] +
        projects_score * ATS_CATEGORY_WEIGHTS["Projects_Score"] +
        kw_score * ATS_CATEGORY_WEIGHTS["Keyword_Match_Score"] +
        edu_score * ATS_CATEGORY_WEIGHTS["Education_Score"] +
        formatting_score * ATS_CATEGORY_WEIGHTS["Formatting_Score"] +
        certs_score * ATS_CATEGORY_WEIGHTS["Certifications_Score"] +
        readability_score * ATS_CATEGORY_WEIGHTS["Readability_Score"]
    )
    overall_ats_score = max(0, min(100, round(weighted_sum)))

    return {
        "Overall_ATS_Score": overall_ats_score,
        "Skills_Score": skills_score,
        "Experience_Score": exp_score,
        "Projects_Score": projects_score,
        "Keyword_Match_Score": kw_score,
        "Education_Score": edu_score,
        "Formatting_Score": formatting_score,
        "Certifications_Score": certs_score,
        "Readability_Score": readability_score
    }
