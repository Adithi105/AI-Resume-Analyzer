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
    Analyzes extracted resume text using Ollama (Llama 3.2 3B) acting as an Intelligent
    ATS Recruiter and Executive Talent Specialist. Returns 16 rich recruiter intelligence
    metrics in structured JSON.
    """
    if not resume_text or not resume_text.strip():
        return sanitize_resume_data({"error": "Empty resume text."})

    prompt = f"""
You are an expert Executive Talent Acquisition Partner, Chief Technical Recruiter, and Applicant Tracking System (ATS) Auditor.

Analyze the candidate resume provided below and act as an Intelligent ATS Recruiter.

Return ONLY a valid raw JSON object matching this exact structure:

{{
  "Name": "Candidate Full Name",
  "Email": "Email Address",
  "Phone": "Phone Number",
  "Executive_Summary": "High-impact 2-3 sentence executive summary of the candidate's caliber, domain background, and overall positioning.",
  "Resume_Overview": "Concise 2-sentence summary of candidate professional background, years of experience, and key domain expertise.",
  "ATS_Score": 85,
  "Recruiter_Verdict": "Strong Hire",
  "Hiring_Probability": "88%",
  "Candidate_Level": "Senior Technical Specialist",
  "Technical_Strengths": ["Core technical skill 1", "Core technical skill 2"],
  "Soft_Skill_Strengths": ["Leadership", "Stakeholder Communication"],
  "Weaknesses": ["Identified weakness or gap 1", "Identified weakness 2"],
  "Missing_Skills": ["Missing skill 1", "Missing skill 2"],
  "Resume_Risks": ["Risk or red flag 1 e.g. lack of quantitative metrics", "Risk 2 e.g. employment gap"],
  "Career_Suggestions": ["Actionable career advice 1", "Actionable advice 2"],
  "Learning_Roadmap": [
    "Phase 1: Master advanced cloud architecture & Kubernetes",
    "Phase 2: Obtain AWS Solutions Architect Professional certification",
    "Phase 3: Lead large-scale microservices system design"
  ],
  "Recommended_Certifications": ["AWS Certified Solutions Architect", "CKA - Certified Kubernetes Administrator"],
  "Suggested_Projects": [
    "Build a distributed event-driven real-time streaming pipeline using Kafka and Go",
    "Implement an automated CI/CD pipeline with GitOps and ArgoCD"
  ],
  "Resume_Rewrite_Suggestions": [
    "Rewrite Work Experience bullet 1 to include quantified ROI (e.g. 'Improved throughput by 40%')",
    "Add a dedicated Core Competencies section near the top of page 1"
  ],
  "Skills": ["Python", "Docker", "SQL", "React"],
  "Strengths": ["System Architecture", "Performance Optimization"],
  "Suggestions": ["Quantify achievements in project descriptions"],
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

CRITICAL INSTRUCTIONS:
1. Return strictly raw valid JSON. Do NOT use markdown ```json wrappers or introductory text.
2. ATS_Score must be an integer between 0 and 100 calculated rigorously.
3. Recruiter_Verdict must be one of: "Strong Hire", "Shortlist / Interview", "Borderline Candidate", or "Reject / Re-align".
4. Hiring_Probability must be a percentage string (e.g., "85%").
5. Candidate_Level must evaluate candidate seniority (e.g., "Junior", "Mid-Level", "Senior", "Lead / Principal").

CANDIDATE RESUME TEXT:
{resume_text}
"""

    try:
        response = ollama.chat(
            model=MODEL_NAME,
            format="json",
            messages=[{"role": "user", "content": prompt}]
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
            fallback["Executive_Summary"] = "Unable to connect to Ollama AI service. Fallback preview mode active."
            fallback["Recruiter_Verdict"] = "Pending AI Service"
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