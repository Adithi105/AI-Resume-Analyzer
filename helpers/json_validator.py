import json
import re
from typing import Dict, Any
from helpers.scoring_engine import compute_weighted_ats_score

DEFAULT_RESUME_SCHEMA: Dict[str, Any] = {
    # Core Candidate Info
    "Name": "Not Specified",
    "Email": "Not Specified",
    "Phone": "Not Specified",
    "ATS_Score": 0,
    
    # Weighted ATS Breakdown
    "ATS_Breakdown": {
        "Overall_ATS_Score": 0,
        "Skills_Score": 0,
        "Experience_Score": 0,
        "Projects_Score": 0,
        "Keyword_Match_Score": 0,
        "Education_Score": 0,
        "Formatting_Score": 0,
        "Certifications_Score": 0,
        "Readability_Score": 0
    },

    # Recruiter Decision & Overview
    "Executive_Summary": "Not Provided",
    "Resume_Overview": "Not Provided",
    "Recruiter_Verdict": "Under Review",
    "Hiring_Probability": "0%",
    "Candidate_Level": "Not Specified",
    
    # Strengths & Weaknesses Matrix
    "Skills": [],
    "Technical_Strengths": [],
    "Soft_Skill_Strengths": [],
    "Strengths": [],
    "Weaknesses": [],
    "Missing_Skills": [],
    "Resume_Risks": [],
    
    # Growth & Recommendations
    "Suggestions": [],
    "Career_Suggestions": [],
    "Learning_Roadmap": [],
    "Recommended_Certifications": [],
    "Suggested_Projects": [],
    "Resume_Rewrite_Suggestions": [],
    
    # Detailed Sections
    "Education": [],
    "Projects": [],
    "Certifications": [],
    "Experience": []
}

DEFAULT_JD_MATCH_SCHEMA: Dict[str, Any] = {
    "Match_Score": 0,
    "Matching_Skills": [],
    "Missing_Skills": [],
    "Suggestions": []
}

DEFAULT_REWRITE_SCHEMA: Dict[str, Any] = {
    "Professional_Summary": "Professional summary optimized for ATS scanning.",
    "Skills": [],
    "Experience": [],
    "Projects": [],
    "Achievements": [],
    "Education": []
}

def extract_json_string(text: str) -> str:
    """
    Extracts JSON content from raw LLM output text, eliminating markdown wrappers
    or leading/trailing commentary.
    """
    if not text:
        return "{}"
    
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1)

    match_braces = re.search(r"\{.*\}", text, re.DOTALL)
    if match_braces:
        return match_braces.group(0)

    return text.strip()

def repair_json_string(json_str: str) -> str:
    """
    Applies regex sanitization fixes for trailing commas or minor LLM JSON syntax bugs.
    """
    json_str = re.sub(r",\s*([\]\}])", r"\1", json_str)
    return json_str

def parse_and_clean_json(raw_response: str) -> Dict[str, Any]:
    """
    Parses LLM response string into a python dictionary with robust error recovery.
    """
    cleaned_str = extract_json_string(raw_response)
    cleaned_str = repair_json_string(cleaned_str)

    try:
        data = json.loads(cleaned_str)
        if isinstance(data, dict):
            return data
    except json.JSONDecodeError:
        pass

    try:
        start_idx = raw_response.find('{')
        end_idx = raw_response.rfind('}')
        if start_idx != -1 and end_idx != -1 and start_idx < end_idx:
            candidate = raw_response[start_idx:end_idx + 1]
            candidate = repair_json_string(candidate)
            data = json.loads(candidate)
            if isinstance(data, dict):
                return data
    except Exception:
        pass

    return {}

def sanitize_resume_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ensures all keys in DEFAULT_RESUME_SCHEMA exist, have correct types,
    and contain no None values. Computes professional weighted ATS breakdown.
    """
    sanitized = {}

    string_fields = [
        "Name", "Email", "Phone",
        "Executive_Summary", "Resume_Overview", "Recruiter_Verdict",
        "Hiring_Probability", "Candidate_Level"
    ]
    for field in string_fields:
        val = data.get(field)
        if not val or val is None or str(val).strip().lower() in ["none", "null", "n/a", ""]:
            sanitized[field] = DEFAULT_RESUME_SCHEMA.get(field, "Not Specified")
        else:
            sanitized[field] = str(val).strip()

    list_fields = [
        "Skills", "Technical_Strengths", "Soft_Skill_Strengths", "Strengths",
        "Weaknesses", "Missing_Skills", "Resume_Risks",
        "Suggestions", "Career_Suggestions", "Learning_Roadmap",
        "Recommended_Certifications", "Suggested_Projects", "Resume_Rewrite_Suggestions",
        "Education", "Projects", "Certifications", "Experience"
    ]
    for list_field in list_fields:
        raw_list = data.get(list_field)
        if not isinstance(raw_list, list):
            if raw_list is None:
                sanitized[list_field] = []
            elif isinstance(raw_list, (str, dict)):
                sanitized[list_field] = [raw_list]
            else:
                sanitized[list_field] = []
        else:
            sanitized[list_field] = [item for item in raw_list if item is not None]

    if not sanitized["Technical_Strengths"] and sanitized["Strengths"]:
        sanitized["Technical_Strengths"] = list(sanitized["Strengths"])
    elif not sanitized["Strengths"] and sanitized["Technical_Strengths"]:
        sanitized["Strengths"] = list(sanitized["Technical_Strengths"])

    if not sanitized["Career_Suggestions"] and sanitized["Suggestions"]:
        sanitized["Career_Suggestions"] = list(sanitized["Suggestions"])
    elif not sanitized["Suggestions"] and sanitized["Career_Suggestions"]:
        sanitized["Suggestions"] = list(sanitized["Career_Suggestions"])

    data_copy = dict(data)
    data_copy.update(sanitized)
    ats_breakdown = compute_weighted_ats_score(data_copy)
    sanitized["ATS_Breakdown"] = ats_breakdown
    sanitized["ATS_Score"] = ats_breakdown["Overall_ATS_Score"]

    return sanitized

def sanitize_jd_match_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ensures job description match response complies with expected schema.
    """
    sanitized = {}
    try:
        score = int(data.get("Match_Score", 0))
        sanitized["Match_Score"] = max(0, min(100, score))
    except (ValueError, TypeError):
        sanitized["Match_Score"] = 0

    for field in ["Matching_Skills", "Missing_Skills", "Suggestions"]:
        val = data.get(field)
        if not isinstance(val, list):
            sanitized[field] = [] if val is None else [str(val)]
        else:
            sanitized[field] = [str(item) for item in val if item is not None]

    return sanitized

def sanitize_rewrite_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ensures AI rewrite response complies with DEFAULT_REWRITE_SCHEMA.
    """
    sanitized = {}
    prof_sum = data.get("Professional_Summary")
    sanitized["Professional_Summary"] = str(prof_sum).strip() if prof_sum else DEFAULT_REWRITE_SCHEMA["Professional_Summary"]

    for list_field in ["Skills", "Experience", "Projects", "Achievements", "Education"]:
        val = data.get(list_field)
        if isinstance(val, list):
            sanitized[list_field] = [item for item in val if item is not None]
        elif val is not None:
            sanitized[list_field] = [val]
        else:
            sanitized[list_field] = []

    return sanitized


# ─────────────────────────────────────────────────────────────────────────────
# Interview Preparation Schema & Sanitizer
# ─────────────────────────────────────────────────────────────────────────────

_DEFAULT_QUESTION = {
    "Question": "Not Available",
    "Difficulty": "Medium",
    "Answer": "No AI-generated answer available.",
    "Tips": "",
}

DEFAULT_INTERVIEW_SCHEMA: Dict[str, Any] = {
    "Interview_Score": 0,
    "Score_Breakdown": {
        "Technical": 0,
        "HR": 0,
        "Behavioural": 0,
        "Coding": 0,
        "Project": 0,
    },
    "Score_Summary": "Interview simulation score unavailable.",
    "Technical_Questions": [],
    "HR_Questions": [],
    "Behavioural_Questions": [],
    "Coding_Questions": [],
    "Project_Questions": [],
}

_VALID_DIFFICULTIES = {"Easy", "Medium", "Hard"}
_QUESTION_CATEGORIES = [
    "Technical_Questions",
    "HR_Questions",
    "Behavioural_Questions",
    "Coding_Questions",
    "Project_Questions",
]


def _sanitize_question_list(raw: Any) -> list:
    """Ensure a list of question dicts is well-formed."""
    if not isinstance(raw, list):
        return []
    cleaned = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        q = {
            "Question": str(item.get("Question", "")).strip() or _DEFAULT_QUESTION["Question"],
            "Difficulty": item.get("Difficulty", "Medium"),
            "Answer": str(item.get("Answer", "")).strip() or _DEFAULT_QUESTION["Answer"],
            "Tips": str(item.get("Tips", "")).strip(),
        }
        if q["Difficulty"] not in _VALID_DIFFICULTIES:
            q["Difficulty"] = "Medium"
        cleaned.append(q)
    return cleaned


def sanitize_interview_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validates and normalises interview preparation AI response.
    Ensures all 5 question categories, difficulty tags, answers, score breakdown
    and simulation score are present and correctly typed.
    """
    sanitized: Dict[str, Any] = {}

    # Overall interview score
    try:
        score = int(data.get("Interview_Score", 0))
        sanitized["Interview_Score"] = max(0, min(100, score))
    except (ValueError, TypeError):
        sanitized["Interview_Score"] = 0

    # Per-category score breakdown
    raw_breakdown = data.get("Score_Breakdown", {})
    breakdown = {}
    for cat in ["Technical", "HR", "Behavioural", "Coding", "Project"]:
        try:
            breakdown[cat] = max(0, min(100, int(raw_breakdown.get(cat, 0))))
        except (ValueError, TypeError):
            breakdown[cat] = 0
    sanitized["Score_Breakdown"] = breakdown

    # Score narrative
    summary = data.get("Score_Summary", "")
    sanitized["Score_Summary"] = str(summary).strip() if summary else DEFAULT_INTERVIEW_SCHEMA["Score_Summary"]

# ─────────────────────────────────────────────────────────────────────────────
# Portfolio Analyzer Schema & Sanitizer
# ─────────────────────────────────────────────────────────────────────────────

DEFAULT_PORTFOLIO_SCHEMA: Dict[str, Any] = {
    "Overall_Portfolio_Score": 0,
    "GitHub_Score": 0,
    "LinkedIn_Score": 0,
    "Portfolio_Website_Score": 0,
    "Metrics_Breakdown": {
        "Repository_Quality": 0,
        "Project_Quality": 0,
        "Contribution_Activity": 0,
        "Code_Documentation": 0,
        "Profile_Completeness": 0,
        "UI_UX_Design": 0
    },
    "GitHub_Analysis": {
        "Repository_Quality": "Analysis of open-source repository organization, commit cadence, and code structure.",
        "Top_Languages": ["Python", "JavaScript"],
        "Highlights": ["Clean README files", "Consistent commit frequency"],
        "Risks": ["Few test files in repositories"]
    },
    "LinkedIn_Analysis": {
        "Profile_Completeness": "Evaluation of summary, experience bullets, endorsement density, and network signals.",
        "Strengths": ["Clear headline", "Detailed experience entries"],
        "Gaps": ["Sparse recommendation section"]
    },
    "Portfolio_Website_Analysis": {
        "Design_Quality": "Evaluation of UI/UX aesthetics, responsiveness, project showcases, and live demos.",
        "Strengths": ["Clean layout", "Fast load time"],
        "Areas_For_Improvement": ["Add live hosted project links"]
    },
    "Contribution_Analysis": "Detailed analysis of open-source contribution patterns, commit consistency, and project ownership.",
    "Improvement_Suggestions": ["Add comprehensive READMEs to top 3 repos", "Include live demo links on portfolio"],
    "Technology_Recommendations": ["Learn Docker & CI/CD workflows", "Add TypeScript to portfolio projects"]
}


def sanitize_portfolio_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validates and normalises Portfolio Analyzer AI responses.
    Ensures scores, sub-breakdowns, and diagnostic analysis sections are safe.
    """
    sanitized: Dict[str, Any] = {}

    # Score helper
    def _safe_score(val: Any) -> int:
        try:
            return max(0, min(100, int(val)))
        except (ValueError, TypeError):
            return 0

    sanitized["Overall_Portfolio_Score"] = _safe_score(data.get("Overall_Portfolio_Score", 0))
    sanitized["GitHub_Score"] = _safe_score(data.get("GitHub_Score", 0))
    sanitized["LinkedIn_Score"] = _safe_score(data.get("LinkedIn_Score", 0))
    sanitized["Portfolio_Website_Score"] = _safe_score(data.get("Portfolio_Website_Score", 0))

    # Metrics Breakdown
    raw_mb = data.get("Metrics_Breakdown", {})
    sanitized["Metrics_Breakdown"] = {
        "Repository_Quality": _safe_score(raw_mb.get("Repository_Quality", 0)),
        "Project_Quality": _safe_score(raw_mb.get("Project_Quality", 0)),
        "Contribution_Activity": _safe_score(raw_mb.get("Contribution_Activity", 0)),
        "Code_Documentation": _safe_score(raw_mb.get("Code_Documentation", 0)),
        "Profile_Completeness": _safe_score(raw_mb.get("Profile_Completeness", 0)),
        "UI_UX_Design": _safe_score(raw_mb.get("UI_UX_Design", 0)),
    }

    # Re-calculate overall score if missing/0
    if sanitized["Overall_Portfolio_Score"] == 0:
        mb = sanitized["Metrics_Breakdown"]
        avg = sum(mb.values()) / max(1, len(mb))
        sanitized["Overall_Portfolio_Score"] = round(avg)

    # Sub-analyses
    gh = data.get("GitHub_Analysis", {})
    sanitized["GitHub_Analysis"] = {
        "Repository_Quality": str(gh.get("Repository_Quality", DEFAULT_PORTFOLIO_SCHEMA["GitHub_Analysis"]["Repository_Quality"])).strip(),
        "Top_Languages": [str(x) for x in gh.get("Top_Languages", []) if x] or DEFAULT_PORTFOLIO_SCHEMA["GitHub_Analysis"]["Top_Languages"],
        "Highlights": [str(x) for x in gh.get("Highlights", []) if x] or DEFAULT_PORTFOLIO_SCHEMA["GitHub_Analysis"]["Highlights"],
        "Risks": [str(x) for x in gh.get("Risks", []) if x] or DEFAULT_PORTFOLIO_SCHEMA["GitHub_Analysis"]["Risks"],
    }

    li = data.get("LinkedIn_Analysis", {})
    sanitized["LinkedIn_Analysis"] = {
        "Profile_Completeness": str(li.get("Profile_Completeness", DEFAULT_PORTFOLIO_SCHEMA["LinkedIn_Analysis"]["Profile_Completeness"])).strip(),
        "Strengths": [str(x) for x in li.get("Strengths", []) if x] or DEFAULT_PORTFOLIO_SCHEMA["LinkedIn_Analysis"]["Strengths"],
        "Gaps": [str(x) for x in li.get("Gaps", []) if x] or DEFAULT_PORTFOLIO_SCHEMA["LinkedIn_Analysis"]["Gaps"],
    }

    pw = data.get("Portfolio_Website_Analysis", {})
    sanitized["Portfolio_Website_Analysis"] = {
        "Design_Quality": str(pw.get("Design_Quality", DEFAULT_PORTFOLIO_SCHEMA["Portfolio_Website_Analysis"]["Design_Quality"])).strip(),
        "Strengths": [str(x) for x in pw.get("Strengths", []) if x] or DEFAULT_PORTFOLIO_SCHEMA["Portfolio_Website_Analysis"]["Strengths"],
        "Areas_For_Improvement": [str(x) for x in pw.get("Areas_For_Improvement", []) if x] or DEFAULT_PORTFOLIO_SCHEMA["Portfolio_Website_Analysis"]["Areas_For_Improvement"],
    }

# ─────────────────────────────────────────────────────────────────────────────
# AI Career Coach Schema & Sanitizer
# ─────────────────────────────────────────────────────────────────────────────

DEFAULT_CAREER_COACH_SCHEMA: Dict[str, Any] = {
    "Target_Role": "Software Engineer",
    "Current_Level": "Mid Level",
    "Salary_Estimation": {
        "Entry_Level": "$70,000 - $95,000",
        "Mid_Level": "$105,000 - $140,000",
        "Senior_Level": "$150,000 - $210,000",
        "Market_Outlook": "Very High Demand (+22% Growth rate)",
        "Currency": "USD"
    },
    "Suitable_Job_Roles": [
        {"Role": "Backend Systems Engineer", "Match_Percentage": 92},
        {"Role": "Cloud Solutions Architect", "Match_Percentage": 85},
        {"Role": "DevOps / Infrastructure Engineer", "Match_Percentage": 78}
    ],
    "Skill_Gap_Analysis": {
        "Current_Mastery": ["Python", "SQL", "REST APIs", "Docker"],
        "Gaps_To_Close": ["Kubernetes", "AWS Architecture", "Distributed Caching", "System Design"],
        "Critical_Focus_Area": "Cloud-native distributed systems design and container orchestration"
    },
    "Career_Roadmap": [
        {"Phase": "Phase 1 (Months 1-2)", "Focus": "Core Infrastructure & Cloud Basics", "Milestones": ["Master Docker & AWS Core", "Build 1 Cloud Microservice"]},
        {"Phase": "Phase 2 (Months 3-4)", "Focus": "Orchestration & System Scaling", "Milestones": ["CKA Certification Prep", "Implement Kafka Event Pipeline"]},
        {"Phase": "Phase 3 (Months 5-6)", "Focus": "Senior Positioning & Leadership", "Milestones": ["Lead Architecture Review", "Interview Prep & Portfolio Launch"]}
    ],
    "Learning_Path": [
        "Distributed Systems Foundations (Consensus algorithms, CAP theorem)",
        "Advanced Cloud Architecture on AWS/GCP",
        "Container Orchestration with Kubernetes & Helm",
        "Production Monitoring & Observability (Prometheus & Grafana)"
    ],
    "Weekly_Study_Plan": [
        {"Week": "Week 1", "Topic": "Advanced Python Concurrency & AsyncIO", "Hours": 10, "Deliverable": "Build async web crawler with Redis cache"},
        {"Week": "Week 2", "Topic": "Docker Networking & Multi-stage Builds", "Hours": 12, "Deliverable": "Containerize full stack application"},
        {"Week": "Week 3", "Topic": "Kubernetes Pods, Services & Deployments", "Hours": 15, "Deliverable": "Deploy K8s cluster on Minikube"},
        {"Week": "Week 4", "Topic": "System Design Mock Interviews & API Design", "Hours": 12, "Deliverable": "Design URL Shortener architecture"}
    ],
    "Monthly_Goals": [
        {"Month": "Month 1", "Goal": "Complete AWS Developer Associate course & deploy 2 microservices"},
        {"Month": "Month 2", "Goal": "Achieve Kubernetes CKA certification & contribute to 1 open-source repo"},
        {"Month": "Month 3", "Goal": "Polish portfolio, complete 15 System Design mocks, apply for target roles"}
    ],
    "Recommended_Courses": [
        {"Course": "Ultimate AWS Certified Solutions Architect Associate", "Platform": "Udemy / Coursera", "Skill_Target": "Cloud Infrastructure"},
        {"Course": "Certified Kubernetes Administrator (CKA) Mastery", "Platform": "Linux Foundation", "Skill_Target": "Container Orchestration"},
        {"Course": "Grokking the System Design Interview", "Platform": "DesignGurus / Educative", "Skill_Target": "System Architecture"}
    ],
    "Recommended_Certifications": [
        {"Certification": "AWS Certified Solutions Architect", "Provider": "Amazon Web Services", "Difficulty": "Intermediate"},
        {"Certification": "CKA - Certified Kubernetes Administrator", "Provider": "Linux Foundation", "Difficulty": "Hard"}
    ],
    "Internship_Suggestions": [
        {"Track": "Cloud Infrastructure Intern / Apprentice", "Company_Types": "Tech Unicorns / Cloud Native Startups", "Key_Focus": "Hands-on CI/CD & Terraform"},
        {"Track": "Backend Engineering Fellow", "Company_Types": "Enterprise SaaS", "Key_Focus": "High-throughput API development"}
    ],
    "Company_Recommendations": [
        {"Company": "Datadog", "Type": "Growth Unicorn", "Why_Fit": "Strong match for observability & infrastructure focus"},
        {"Company": "AWS / Amazon", "Type": "Big Tech / Enterprise", "Why_Fit": "Ideal environment for cloud scale engineering"},
        {"Company": "HashiCorp", "Type": "DevOps & Cloud Specialist", "Why_Fit": "Direct alignment with open-source infrastructure tools"}
    ]
}


def sanitize_career_coach_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validates and normalizes AI Career Coach response.
    Ensures all 11 required sections conform strictly to expected structures.
    """
    sanitized: Dict[str, Any] = {}

    sanitized["Target_Role"] = str(data.get("Target_Role", "Software Engineer")).strip()
    sanitized["Current_Level"] = str(data.get("Current_Level", "Mid Level")).strip()

    # Salary Estimation
    sal = data.get("Salary_Estimation", {})
    sanitized["Salary_Estimation"] = {
        "Entry_Level": str(sal.get("Entry_Level", DEFAULT_CAREER_COACH_SCHEMA["Salary_Estimation"]["Entry_Level"])).strip(),
        "Mid_Level": str(sal.get("Mid_Level", DEFAULT_CAREER_COACH_SCHEMA["Salary_Estimation"]["Mid_Level"])).strip(),
        "Senior_Level": str(sal.get("Senior_Level", DEFAULT_CAREER_COACH_SCHEMA["Salary_Estimation"]["Senior_Level"])).strip(),
        "Market_Outlook": str(sal.get("Market_Outlook", DEFAULT_CAREER_COACH_SCHEMA["Salary_Estimation"]["Market_Outlook"])).strip(),
        "Currency": str(sal.get("Currency", "USD")).strip(),
    }

    # Suitable Job Roles
    roles = data.get("Suitable_Job_Roles", [])
    sanitized_roles = []
    if isinstance(roles, list):
        for r in roles:
            if isinstance(r, dict):
                try:
                    pct = max(0, min(100, int(r.get("Match_Percentage", 80))))
                except (ValueError, TypeError):
                    pct = 80
                sanitized_roles.append({
                    "Role": str(r.get("Role", "Software Role")).strip(),
                    "Match_Percentage": pct
                })
    sanitized["Suitable_Job_Roles"] = sanitized_roles or DEFAULT_CAREER_COACH_SCHEMA["Suitable_Job_Roles"]

    # Skill Gap Analysis
    sg = data.get("Skill_Gap_Analysis", {})
    sanitized["Skill_Gap_Analysis"] = {
        "Current_Mastery": [str(x) for x in sg.get("Current_Mastery", []) if x] or DEFAULT_CAREER_COACH_SCHEMA["Skill_Gap_Analysis"]["Current_Mastery"],
        "Gaps_To_Close": [str(x) for x in sg.get("Gaps_To_Close", []) if x] or DEFAULT_CAREER_COACH_SCHEMA["Skill_Gap_Analysis"]["Gaps_To_Close"],
        "Critical_Focus_Area": str(sg.get("Critical_Focus_Area", DEFAULT_CAREER_COACH_SCHEMA["Skill_Gap_Analysis"]["Critical_Focus_Area"])).strip(),
    }

    # Career Roadmap
    roadmap = data.get("Career_Roadmap", [])
    sanitized_rm = []
    if isinstance(roadmap, list):
        for item in roadmap:
            if isinstance(item, dict):
                m_list = item.get("Milestones", [])
                if isinstance(m_list, list):
                    m_clean = [str(x) for x in m_list if x]
                else:
                    m_clean = [str(m_list)]
                sanitized_rm.append({
                    "Phase": str(item.get("Phase", "Phase 1")).strip(),
                    "Focus": str(item.get("Focus", "Core Skill Building")).strip(),
                    "Milestones": m_clean
                })
    sanitized["Career_Roadmap"] = sanitized_rm or DEFAULT_CAREER_COACH_SCHEMA["Career_Roadmap"]

    # Learning Path
    lp = data.get("Learning_Path", [])
    if isinstance(lp, list):
        sanitized["Learning_Path"] = [str(x) for x in lp if x]
    else:
        sanitized["Learning_Path"] = list(DEFAULT_CAREER_COACH_SCHEMA["Learning_Path"])

    # Weekly Study Plan
    wsp = data.get("Weekly_Study_Plan", [])
    sanitized_wsp = []
    if isinstance(wsp, list):
        for item in wsp:
            if isinstance(item, dict):
                try:
                    hrs = int(item.get("Hours", 10))
                except (ValueError, TypeError):
                    hrs = 10
                sanitized_wsp.append({
                    "Week": str(item.get("Week", "Week 1")).strip(),
                    "Topic": str(item.get("Topic", "Core Learning")).strip(),
                    "Hours": hrs,
                    "Deliverable": str(item.get("Deliverable", "Practical Exercise")).strip()
                })
    sanitized["Weekly_Study_Plan"] = sanitized_wsp or DEFAULT_CAREER_COACH_SCHEMA["Weekly_Study_Plan"]

    # Monthly Goals
    mg = data.get("Monthly_Goals", [])
    sanitized_mg = []
    if isinstance(mg, list):
        for item in mg:
            if isinstance(item, dict):
                sanitized_mg.append({
                    "Month": str(item.get("Month", "Month 1")).strip(),
                    "Goal": str(item.get("Goal", "Complete Core Milestone")).strip()
                })
    sanitized["Monthly_Goals"] = sanitized_mg or DEFAULT_CAREER_COACH_SCHEMA["Monthly_Goals"]

    # Recommended Courses
    courses = data.get("Recommended_Courses", [])
    sanitized_c = []
    if isinstance(courses, list):
        for item in courses:
            if isinstance(item, dict):
                sanitized_c.append({
                    "Course": str(item.get("Course", "Professional Certification Course")).strip(),
                    "Platform": str(item.get("Platform", "Online Learning")).strip(),
                    "Skill_Target": str(item.get("Skill_Target", "Core Competency")).strip()
                })
    sanitized["Recommended_Courses"] = sanitized_c or DEFAULT_CAREER_COACH_SCHEMA["Recommended_Courses"]

    # Recommended Certifications
    certs = data.get("Recommended_Certifications", [])
    sanitized_certs = []
    if isinstance(certs, list):
        for item in certs:
            if isinstance(item, dict):
                sanitized_certs.append({
                    "Certification": str(item.get("Certification", "Industry Certification")).strip(),
                    "Provider": str(item.get("Provider", "Vendor")).strip(),
                    "Difficulty": str(item.get("Difficulty", "Intermediate")).strip()
                })
    sanitized["Recommended_Certifications"] = sanitized_certs or DEFAULT_CAREER_COACH_SCHEMA["Recommended_Certifications"]

    # Internship Suggestions
    interns = data.get("Internship_Suggestions", [])
    sanitized_int = []
    if isinstance(interns, list):
        for item in interns:
            if isinstance(item, dict):
                sanitized_int.append({
                    "Track": str(item.get("Track", "Technical Internship")).strip(),
                    "Company_Types": str(item.get("Company_Types", "Tech Companies")).strip(),
                    "Key_Focus": str(item.get("Key_Focus", "Practical Experience")).strip()
                })
    sanitized["Internship_Suggestions"] = sanitized_int or DEFAULT_CAREER_COACH_SCHEMA["Internship_Suggestions"]

    # Company Recommendations
    comps = data.get("Company_Recommendations", [])
    sanitized_comp = []
    if isinstance(comps, list):
        for item in comps:
            if isinstance(item, dict):
                sanitized_comp.append({
                    "Company": str(item.get("Company", "Target Tech Firm")).strip(),
                    "Type": str(item.get("Type", "Growth Startup")).strip(),
                    "Why_Fit": str(item.get("Why_Fit", "Strong alignment with candidate skills")).strip()
                })
    sanitized["Company_Recommendations"] = sanitized_comp or DEFAULT_CAREER_COACH_SCHEMA["Company_Recommendations"]

    return sanitized
