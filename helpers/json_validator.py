import json
import re
from typing import Dict, Any

DEFAULT_RESUME_SCHEMA: Dict[str, Any] = {
    "Name": "Not Provided",
    "Email": "Not Provided",
    "Phone": "Not Provided",
    "ATS_Score": 0,
    "Skills": [],
    "Missing_Skills": [],
    "Strengths": [],
    "Suggestions": [],
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

def extract_json_string(text: str) -> str:
    """
    Extracts JSON content from raw LLM output text, eliminating markdown wrappers
    or leading/trailing commentary.
    """
    if not text:
        return "{}"
    
    # Try finding markdown ```json ... ``` code block
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1)

    # Try finding outer braces {}
    match_braces = re.search(r"\{.*\}", text, re.DOTALL)
    if match_braces:
        return match_braces.group(0)

    return text.strip()

def repair_json_string(json_str: str) -> str:
    """
    Applies regex sanitization fixes for trailing commas or minor LLM JSON syntax bugs.
    """
    # Remove trailing commas inside lists or objects e.g. [1, 2,] or {"a": 1,}
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

    # Secondary aggressive repair: try finding first '{' and last '}'
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
    and contain no None values.
    """
    sanitized = {}

    # String fields
    for field in ["Name", "Email", "Phone"]:
        val = data.get(field)
        if not val or val is None or str(val).strip().lower() in ["none", "null", "n/a", ""]:
            sanitized[field] = "Not Specified"
        else:
            sanitized[field] = str(val).strip()

    # Numeric score field
    try:
        score = int(data.get("ATS_Score", 0))
        sanitized["ATS_Score"] = max(0, min(100, score))
    except (ValueError, TypeError):
        sanitized["ATS_Score"] = 0

    # List fields
    list_fields = ["Skills", "Missing_Skills", "Strengths", "Suggestions", "Education", "Projects", "Certifications", "Experience"]
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
            # Filter out None values in list
            sanitized[list_field] = [item for item in raw_list if item is not None]

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
