import ollama
from typing import Dict, Any
from helpers.json_validator import (
    parse_and_clean_json,
    sanitize_resume_data,
    sanitize_jd_match_data,
    sanitize_rewrite_data,
    DEFAULT_RESUME_SCHEMA,
    DEFAULT_JD_MATCH_SCHEMA,
    DEFAULT_REWRITE_SCHEMA
)

MODEL_NAME = "llama3.2:3b"

def analyze_resume(resume_text: str) -> Dict[str, Any]:
    """
    Analyzes extracted resume text using Ollama (Llama 3.2 3B) acting as an Intelligent
    ATS Recruiter. Evaluates candidate metrics and returns weighted ATS sub-scores across
    8 categories and 16 recruiter intelligence metrics in structured JSON.
    """
    if not resume_text or not resume_text.strip():
        return sanitize_resume_data({"error": "Empty resume text."})

    prompt = f"""
You are an expert Executive Talent Acquisition Partner, Chief Technical Recruiter, and Applicant Tracking System (ATS) Scoring Engine.

Analyze the candidate resume provided below and evaluate both general recruiter metrics and a weighted 8-category ATS breakdown.

Return ONLY a valid raw JSON object matching this exact structure:

{{
  "Name": "Candidate Full Name",
  "Email": "Email Address",
  "Phone": "Phone Number",
  "ATS_Breakdown": {{
    "Skills_Score": 85,
    "Experience_Score": 80,
    "Projects_Score": 90,
    "Keyword_Match_Score": 82,
    "Education_Score": 88,
    "Formatting_Score": 95,
    "Certifications_Score": 75,
    "Readability_Score": 90
  }},
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
2. Provide numeric values (0-100) for all 8 categories in ATS_Breakdown.
3. Recruiter_Verdict must be one of: "Strong Hire", "Shortlist / Interview", "Borderline Candidate", or "Reject / Re-align".

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
        try:
            response = ollama.chat(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}]
            )
            content = response.get("message", {}).get("content", "")
            raw_data = parse_and_clean_json(content)
            return sanitize_resume_data(raw_data)
        except Exception:
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


def rewrite_resume(resume_text: str) -> Dict[str, Any]:
    """
    Rewrites and transforms resume text into an optimized, ATS-friendly version with
    quantified action-verb bullet points across Professional Summary, Skills, Experience,
    Projects, Achievements, and Education.
    """
    if not resume_text or not resume_text.strip():
        return sanitize_rewrite_data(DEFAULT_REWRITE_SCHEMA)

    prompt = f"""
You are a Master ATS Resume Writer, Professional Executive Editor, and Talent AI Coach.

Transform and rewrite the candidate resume provided below into a high-impact, ATS-optimized resume.

CRITICAL REWRITING RULES:
1. Generate strong, action-verb-led bullet points for all experience and project entries (e.g. "Engineered...", "Optimized...", "Architected...").
2. Include quantified metrics and ROI estimates where possible (e.g., "boosted throughput by 35%").
3. Format Professional Summary, Skills, Experience, Projects, Key Achievements, and Education.

Return ONLY raw valid JSON matching this exact structure:

{{
  "Professional_Summary": "Results-driven Senior Software Engineer with 5+ years of experience engineering high-throughput distributed microservices, cloud infrastructure, and AI systems. Proven track record of reducing latency by 40% and scaling systems to 1M+ active users.",
  "Skills": ["Python", "Go", "Docker", "Kubernetes", "AWS", "SQL", "Microservices", "System Design"],
  "Experience": [
    {{
      "Company": "Tech Solutions Inc.",
      "Role": "Senior Backend Engineer",
      "Duration": "2021 - Present",
      "Bullet_Points": [
        "Architected scalable microservices infrastructure handling 50M+ daily API calls using Go and Docker",
        "Optimized database query performance by 45% using PostgreSQL index tuning and Redis caching",
        "Mentored a cross-functional team of 6 junior engineers on CI/CD GitOps best practices"
      ]
    }}
  ],
  "Projects": [
    {{
      "Title": "Real-Time Analytics Pipeline",
      "TechStack": "Python, Apache Kafka, PyTorch",
      "Bullet_Points": [
        "Designed real-time event streaming pipeline processing 10k events/sec with sub-50ms latency",
        "Integrated AI sentiment classification model improving anomaly detection accuracy by 28%"
      ]
    }}
  ],
  "Achievements": [
    "Awarded Top Innovator 2024 for reducing cloud infrastructure expenditures by $120k annually",
    "Authored core internal Python framework adopted across 15 engineering squads"
  ],
  "Education": [
    {{
      "Degree": "B.S. in Computer Science",
      "Institution": "University of Technology",
      "Session": "2017 - 2021",
      "Highlights": "Graduated Magna Cum Laude | Specialized in Distributed Systems & AI"
    }}
  ]
}}

CANDIDATE RESUME TEXT TO REWRITE:
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
        return sanitize_rewrite_data(raw_data)
    except Exception as e:
        try:
            response = ollama.chat(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}]
            )
            content = response.get("message", {}).get("content", "")
            raw_data = parse_and_clean_json(content)
            return sanitize_rewrite_data(raw_data)
        except Exception:
            return sanitize_rewrite_data(DEFAULT_REWRITE_SCHEMA)