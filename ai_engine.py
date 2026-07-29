"""
AI Engine — provider-agnostic interface for all AI inference calls.

All functions delegate to the active provider resolved by config_manager,
which may be Ollama, OpenAI, Gemini, or Claude. No provider-specific code
lives in this file.
"""
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


def _get_provider():
    """Resolve the active provider from the current session config."""
    from helpers.config_manager import get_active_provider
    return get_active_provider()


def _call_provider(prompt: str) -> str:
    """
    Send a prompt to the active provider and return the raw text response.
    Raises on provider errors — callers are responsible for catching.
    """
    provider = _get_provider()
    return provider.chat_completion(prompt)


# ─────────────────────────────────────────────────────────────
#  PROMPTS (unchanged from original — only dispatch layer changed)
# ─────────────────────────────────────────────────────────────

_ANALYZE_PROMPT = """
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

_JD_MATCH_PROMPT = """
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

_REWRITE_PROMPT = """
You are a Master ATS Resume Writer, Professional Executive Editor, and Talent AI Coach.

Transform and rewrite the candidate resume provided below into a high-impact, ATS-optimized resume.

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
        "Optimized database query performance by 45% using PostgreSQL index tuning and Redis caching"
      ]
    }}
  ],
  "Projects": [
    {{
      "Title": "Real-Time Analytics Pipeline",
      "TechStack": "Python, Apache Kafka, PyTorch",
      "Bullet_Points": [
        "Designed real-time event streaming pipeline processing 10k events/sec with sub-50ms latency"
      ]
    }}
  ],
  "Achievements": [
    "Awarded Top Innovator 2024 for reducing cloud infrastructure expenditures by $120k annually"
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

_BUILDER_PROMPT = """
You are an expert ATS Resume Architect and Career AI Strategist.

Refine and polish the user-submitted candidate details below into a professional, ATS-optimized resume structure.

Generate action-verb-led bullet points, quantified metric achievements, and an executive professional summary.

Return ONLY raw valid JSON matching this exact structure:

{{
  "Name": "{name}",
  "Email": "{email}",
  "Phone": "{phone}",
  "Location": "{location}",
  "LinkedIn": "{linkedin}",
  "Professional_Summary": "Polished high-impact professional summary...",
  "Skills": ["Skill 1", "Skill 2"],
  "Experience": [
    {{
      "Company": "Company Name",
      "Role": "Job Role",
      "Duration": "2021 - Present",
      "Bullet_Points": [
        "Engineered scalable solution resulting in 30% performance boost",
        "Led cross-functional team of engineers to deliver high-priority feature"
      ]
    }}
  ],
  "Projects": [
    {{
      "Title": "Project Title",
      "TechStack": "Python, React",
      "Bullet_Points": [
        "Architected full-stack web application serving 10k active users"
      ]
    }}
  ],
  "Certifications": [
    {{
      "Certificate": "Certification Title",
      "Institution": "Issuing Body"
    }}
  ],
  "Education": [
    {{
      "Degree": "Degree Title",
      "Institution": "University Name",
      "Session": "2020 - 2024",
      "Score": "3.8/4.0",
      "Highlights": "Specialized in Computer Science & System Design"
    }}
  ]
}}

RAW USER SUBMITTED DRAFT DETAILS:
{user_inputs}
"""


# ─────────────────────────────────────────────────────────────
#  PUBLIC API
# ─────────────────────────────────────────────────────────────

def analyze_resume(resume_text: str) -> Dict[str, Any]:
    """
    Analyzes extracted resume text using the active AI provider acting as an
    Intelligent ATS Recruiter. Returns weighted ATS sub-scores across 8 categories
    and 16 recruiter intelligence metrics in structured JSON.
    """
    if not resume_text or not resume_text.strip():
        return sanitize_resume_data({"error": "Empty resume text."})

    prompt = _ANALYZE_PROMPT.format(resume_text=resume_text)

    try:
        content = _call_provider(prompt)
        raw_data = parse_and_clean_json(content)
        return sanitize_resume_data(raw_data)
    except Exception as e:
        fallback = dict(DEFAULT_RESUME_SCHEMA)
        fallback["Executive_Summary"] = (
            f"AI provider error: {str(e)[:200]}. "
            "Please check Settings → AI Provider and verify your API key or Ollama is running."
        )
        fallback["Recruiter_Verdict"] = "Pending AI Service"
        fallback["Suggestions"] = [
            "Go to Settings (⚙️ in sidebar) to configure or switch AI providers."
        ]
        return sanitize_resume_data(fallback)


def compare_resume_with_jd(resume_text: str, job_description: str) -> Dict[str, Any]:
    """
    Compares candidate resume text against a Job Description and returns match
    percentage, matching skills, missing skills, and suggestions.
    """
    if not resume_text or not job_description:
        return sanitize_jd_match_data(DEFAULT_JD_MATCH_SCHEMA)

    prompt = _JD_MATCH_PROMPT.format(
        resume_text=resume_text,
        job_description=job_description
    )

    try:
        content = _call_provider(prompt)
        raw_data = parse_and_clean_json(content)
        return sanitize_jd_match_data(raw_data)
    except Exception:
        return sanitize_jd_match_data(DEFAULT_JD_MATCH_SCHEMA)


def rewrite_resume(resume_text: str) -> Dict[str, Any]:
    """
    Rewrites and transforms resume text into an optimized, ATS-friendly version.
    """
    if not resume_text or not resume_text.strip():
        return sanitize_rewrite_data(DEFAULT_REWRITE_SCHEMA)

    prompt = _REWRITE_PROMPT.format(resume_text=resume_text)

    try:
        content = _call_provider(prompt)
        raw_data = parse_and_clean_json(content)
        return sanitize_rewrite_data(raw_data)
    except Exception:
        return sanitize_rewrite_data(DEFAULT_REWRITE_SCHEMA)


def generate_builder_resume(user_inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Takes user form inputs from the AI Resume Builder and uses the active provider
    to polish and generate professional ATS-friendly bullet points across all sections.
    """
    prompt = _BUILDER_PROMPT.format(
        name=user_inputs.get("Name", "Candidate Name"),
        email=user_inputs.get("Email", ""),
        phone=user_inputs.get("Phone", ""),
        location=user_inputs.get("Location", ""),
        linkedin=user_inputs.get("LinkedIn", ""),
        user_inputs=user_inputs,
    )

    try:
        content = _call_provider(prompt)
        raw_data = parse_and_clean_json(content)

        # Merge contact info from user inputs if provider didn't include them
        for field in ["Name", "Email", "Phone", "Location", "LinkedIn"]:
            if not raw_data.get(field) and user_inputs.get(field):
                raw_data[field] = user_inputs[field]

        return raw_data
    except Exception:
        fallback = dict(user_inputs)
        if "Skills" in fallback and isinstance(fallback["Skills"], str):
            fallback["Skills"] = [s.strip() for s in fallback["Skills"].split(",") if s.strip()]
        return fallback