import ollama
from typing import Dict, Any
from helpers.json_validator import (
    parse_and_clean_json,
    sanitize_resume_data,
    sanitize_jd_match_data,
    DEFAULT_RESUME_SCHEMA,
    DEFAULT_JD_MATCH_SCHEMA
)

MODEL_NAME = "llama3.2:3b"

def analyze_resume(resume_text: str) -> Dict[str, Any]:
    """
    Analyzes extracted resume text using Ollama (Llama 3.2 3B) and evaluates
    candidate metrics, skills, missing skills, ATS score, experience, education,
    and projects into strict structured JSON.
    """
    if not resume_text or not resume_text.strip():
        return sanitize_resume_data({"error": "Empty resume text."})

    prompt = f"""
You are an expert ATS (Applicant Tracking System) Resume Auditor and Talent AI Specialist.

Analyze the resume provided below and return ONLY a valid raw JSON object.

CRITICAL CONSTRAINTS:
1. Return strictly a raw JSON object.
2. Do NOT use markdown code blocks like ```json or ```.
3. Do NOT include any intro, commentary, explanations, or conclusions.
4. Output MUST conform to this exact JSON schema:

{{
  "Name": "Candidate Name",
  "Email": "Email Address",
  "Phone": "Phone Number",
  "ATS_Score": 85,
  "Skills": ["Skill1", "Skill2"],
  "Missing_Skills": ["MissingSkill1"],
  "Strengths": ["Strength1", "Strength2"],
  "Suggestions": ["Suggestion1", "Suggestion2"],
  "Education": [
    {{
      "Degree": "Degree Name",
      "Institution": "University Name",
      "Session": "2020-2024",
      "Score": "3.8/4.0"
    }}
  ],
  "Projects": [
    {{
      "Title": "Project Title",
      "TechStack": "Python, React",
      "Description": "Brief summary of achievements"
    }}
  ],
  "Certifications": [
    {{
      "Certificate": "Certification Title",
      "Institution": "Issuing Body"
    }}
  ],
  "Experience": [
    {{
      "Company": "Company Name",
      "Role": "Job Title",
      "Duration": "2021 - Present",
      "Description": "Key responsibilities and achievements"
    }}
  ]
}}

ATS SCORE CALCULATOR RULES:
- Calculate ATS_Score (0-100) rigorously based on:
  * Section clarity & formatting
  * Technical skills & key industry keywords
  * Quantitative project & work experience achievements
  * Education credentials

RESUME TEXT:
{resume_text}
"""

    try:
        response = ollama.chat(
            model=MODEL_NAME,
            format="json",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        content = response.get("message", {}).get("content", "")
        raw_data = parse_and_clean_json(content)
        sanitized = sanitize_resume_data(raw_data)
        return sanitized

    except Exception as e:
        # Retry without format="json" if ollama server format enforcement errored
        try:
            response = ollama.chat(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}]
            )
            content = response.get("message", {}).get("content", "")
            raw_data = parse_and_clean_json(content)
            return sanitize_resume_data(raw_data)
        except Exception:
            # Fallback mock schema if Ollama service is unavailable
            fallback = dict(DEFAULT_RESUME_SCHEMA)
            fallback["Suggestions"] = [
                f"Ollama connection error ({str(e)}). Please ensure Ollama service is running (`ollama run llama3.2:3b`)."
            ]
            return sanitize_resume_data(fallback)


def compare_resume_with_jd(resume_text: str, job_description: str) -> Dict[str, Any]:
    """
    Compares candidate resume text against a Job Description and returns match percentage,
    matching skills, missing skills, and suggestions.
    """
    if not resume_text or not job_description:
        return sanitize_jd_match_data(DEFAULT_JD_MATCH_SCHEMA)

    prompt = f"""
You are an expert HR Specialist & Applicant Tracking System (ATS) Job Match Engine.

Compare the Candidate Resume against the target Job Description (JD).

Return ONLY raw valid JSON conforming strictly to this format:

{{
  "Match_Score": 85,
  "Matching_Skills": ["Python", "SQL"],
  "Missing_Skills": ["AWS", "Docker"],
  "Suggestions": [
    "Highlight experience with cloud infrastructure",
    "Add metrics for software deployment project"
  ]
}}

CRITICAL RULES:
- Do NOT include markdown code blocks.
- Do NOT include any intro or commentary.
- Match_Score must be an integer between 0 and 100 based on overlap of required skills, qualifications, and domain experience.

CANDIDATE RESUME:
{resume_text}

TARGET JOB DESCRIPTION:
{job_description}
"""

    try:
        response = ollama.chat(
            model=MODEL_NAME,
            format="json",
            messages=[{"role": "user", "content": prompt}]
        )
        content = response.get("message", {}).get("content", "")
        raw_data = parse_and_clean_json(content)
        return sanitize_jd_match_data(raw_data)

    except Exception as e:
        try:
            response = ollama.chat(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}]
            )
            content = response.get("message", {}).get("content", "")
            raw_data = parse_and_clean_json(content)
            return sanitize_jd_match_data(raw_data)
        except Exception:
            return sanitize_jd_match_data(DEFAULT_JD_MATCH_SCHEMA)