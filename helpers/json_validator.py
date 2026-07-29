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
