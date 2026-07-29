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
    sanitize_interview_data,
    sanitize_portfolio_data,
    DEFAULT_RESUME_SCHEMA,
    DEFAULT_JD_MATCH_SCHEMA,
    DEFAULT_REWRITE_SCHEMA,
    DEFAULT_INTERVIEW_SCHEMA,
    DEFAULT_PORTFOLIO_SCHEMA
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


_INTERVIEW_PROMPT = """
You are an expert Chief Technical Interviewer, Hiring Manager, and Interview Performance Simulation Engine.

Based on the Candidate Resume and optional Target Job Description provided below, generate a comprehensive Interview Preparation package and simulate an Interview Readiness Score.

Generate realistic questions with difficulty levels (Easy, Medium, Hard), high-impact AI model answers (using STAR methodology where applicable), and interviewer tips.

Return ONLY raw valid JSON conforming strictly to this format:

{{
  "Interview_Score": 84,
  "Score_Breakdown": {{
    "Technical": 85,
    "HR": 90,
    "Behavioural": 80,
    "Coding": 82,
    "Project": 88
  }},
  "Score_Summary": "Candidate demonstrates strong technical fundamentals and project ownership, with slight room for improvement in STAR-framed behavioural responses.",
  "Technical_Questions": [
    {{
      "Question": "Technical question specific to candidate skills/JD",
      "Difficulty": "Easy",
      "Answer": "Comprehensive model answer showing deep technical knowledge",
      "Tips": "Key concepts to highlight during response"
    }},
    {{
      "Question": "In-depth technical architecture question",
      "Difficulty": "Medium",
      "Answer": "Detailed model answer",
      "Tips": "Focus on trade-offs and scalability"
    }},
    {{
      "Question": "Advanced edge-case / performance tuning question",
      "Difficulty": "Hard",
      "Answer": "Expert-level model answer",
      "Tips": "Quantify benchmarks and memory considerations"
    }}
  ],
  "HR_Questions": [
    {{
      "Question": "Why do you want to join our organization?",
      "Difficulty": "Easy",
      "Answer": "Articulate alignment with company mission and technological stack",
      "Tips": "Reference specific achievements and growth goals"
    }},
    {{
      "Question": "Where do you see yourself in 3-5 years?",
      "Difficulty": "Medium",
      "Answer": "Balanced answer showing technical leadership aspirations",
      "Tips": "Emphasize continuous learning and mentorship"
    }}
  ],
  "Behavioural_Questions": [
    {{
      "Question": "Describe a scenario where you resolved a severe technical conflict with a team member.",
      "Difficulty": "Medium",
      "Answer": "STAR model response (Situation, Task, Action, Result) showcasing empathy and objective decision making",
      "Tips": "Structure cleanly using Situation, Task, Action, Result"
    }},
    {{
      "Question": "Tell me about a project failure and what you learned from it.",
      "Difficulty": "Hard",
      "Answer": "Honest STAR answer highlighting root cause analysis and post-mortem improvements",
      "Tips": "Focus heavily on lessons learned and preventative steps implemented"
    }}
  ],
  "Coding_Questions": [
    {{
      "Question": "How would you design and implement a thread-safe LRU cache with O(1) ops?",
      "Difficulty": "Medium",
      "Answer": "Optimal data structure choice (HashMap + Doubly Linked List) with concurrency locking",
      "Tips": "Discuss time & space complexity clearly"
    }},
    {{
      "Question": "Write an algorithm to detect cycles in a directed graph.",
      "Difficulty": "Hard",
      "Answer": "DFS state traversal (Unvisited, Visiting, Visited) or Kahn's algorithm algorithm outline",
      "Tips": "State edge cases e.g. self-loops and disconnected components"
    }}
  ],
  "Project_Questions": [
    {{
      "Question": "Walk me through the architecture of your top project mentioned on your resume.",
      "Difficulty": "Medium",
      "Answer": "High-level component breakdown, data flow, API layer, database design, and key bottleneck solutions",
      "Tips": "Focus on your individual contributions and technical choices"
    }},
    {{
      "Question": "How did you measure and ensure system performance in your key projects?",
      "Difficulty": "Hard",
      "Answer": "Metrics monitoring approach (latency percentiles, throughput, error rates) and load testing setup",
      "Tips": "Provide concrete numbers and monitoring tool details"
    }}
  ]
}}

CANDIDATE RESUME:
{resume_text}

TARGET JOB DESCRIPTION:
{job_description}
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


_PORTFOLIO_PROMPT = """
You are an expert Developer Advocate, Technical Recruiter, and Engineering Brand Architect.

Analyze the developer's candidate profile across their GitHub Profile, LinkedIn Profile, and Portfolio Website.

Evaluate scores (0-100), repository quality, project complexity, open-source contribution activity, profile completeness, design/UI quality, improvement suggestions, and technology recommendations.

Return ONLY raw valid JSON conforming strictly to this format:

{{
  "Overall_Portfolio_Score": 88,
  "GitHub_Score": 85,
  "LinkedIn_Score": 90,
  "Portfolio_Website_Score": 89,
  "Metrics_Breakdown": {{
    "Repository_Quality": 84,
    "Project_Quality": 88,
    "Contribution_Activity": 82,
    "Code_Documentation": 90,
    "Profile_Completeness": 92,
    "UI_UX_Design": 86
  }},
  "GitHub_Analysis": {{
    "Repository_Quality": "Repositories display good architectural structure, clear directory organization, and informative README files.",
    "Top_Languages": ["Python", "TypeScript", "Go", "Docker"],
    "Highlights": ["Comprehensive README documentation with usage instructions", "Consistent commit history on main projects"],
    "Risks": ["A few repositories lack unit test coverage or CI workflow files"]
  }},
  "LinkedIn_Analysis": {{
    "Profile_Completeness": "Profile is well structured with executive summary, detailed experience entries, and relevant technical skill endorsements.",
    "Strengths": ["High-impact headline summarizing domain expertise", "Quantified achievement metrics across past roles"],
    "Gaps": ["Sparse recommendation entries from peers/managers"]
  }},
  "Portfolio_Website_Analysis": {{
    "Design_Quality": "Modern responsive layout with clean visual hierarchy, clear call to action, and interactive project cards.",
    "Strengths": ["Sleek dark/light theme", "Direct links to live hosted demos"],
    "Areas_For_Improvement": ["Add dynamic project search/filter by tech stack"]
  }},
  "Contribution_Analysis": "Candidate maintains steady open-source contribution activity with strong project ownership, clear commit messages, and good pull request etiquette.",
  "Improvement_Suggestions": [
    "Add GitHub Actions CI/CD workflows to top 3 public repositories",
    "Include a video walk-through or GIF preview in project README files",
    "Request 2-3 recommendations on LinkedIn from past tech leads or colleagues",
    "Add dynamic filter tags by technology stack on your portfolio website"
  ],
  "Technology_Recommendations": [
    "Adopt TypeScript for full-stack JavaScript projects for type safety",
    "Integrate Docker Compose files into all backend repositories",
    "Explore Kubernetes & Helm for cloud-native deployment demonstrations",
    "Implement automated unit and integration tests using pytest/Jest"
  ]
}}

CANDIDATE PORTFOLIO DETAILS:
GitHub URL / Username: {github_url}
LinkedIn Profile URL: {linkedin_url}
Portfolio Website URL: {portfolio_url}
Candidate Notes / Bio / Resume Context:
{candidate_notes}
"""


def generate_interview_prep(resume_text: str, job_description: str = "") -> Dict[str, Any]:
    """
    Generates a tailored interview preparation package featuring Technical, HR,
    Behavioural, Coding, and Project questions with difficulty levels (Easy, Medium, Hard),
    AI model answers, interviewer tips, and an interview simulation score breakdown.
    """
    if not resume_text or not resume_text.strip():
        return sanitize_interview_data(DEFAULT_INTERVIEW_SCHEMA)

    prompt = _INTERVIEW_PROMPT.format(
        resume_text=resume_text,
        job_description=job_description if job_description.strip() else "General Software & Technical Role"
    )

    try:
        content = _call_provider(prompt)
        raw_data = parse_and_clean_json(content)
        return sanitize_interview_data(raw_data)
    except Exception:
        return sanitize_interview_data(DEFAULT_INTERVIEW_SCHEMA)


def analyze_portfolio(
    github_url: str = "",
    linkedin_url: str = "",
    portfolio_url: str = "",
    candidate_notes: str = ""
) -> Dict[str, Any]:
    """
    Analyzes candidate's GitHub Profile, LinkedIn Profile, and Portfolio Website to
    generate comprehensive presence scores, repository quality, project quality,
    contribution analysis, improvement suggestions, and technology recommendations.
    """
    prompt = _PORTFOLIO_PROMPT.format(
        github_url=github_url if github_url.strip() else "Not Provided (Evaluate based on notes)",
        linkedin_url=linkedin_url if linkedin_url.strip() else "Not Provided",
        portfolio_url=portfolio_url if portfolio_url.strip() else "Not Provided",
        candidate_notes=candidate_notes if candidate_notes.strip() else "No extra notes provided."
    )

    try:
        content = _call_provider(prompt)
        raw_data = parse_and_clean_json(content)
        return sanitize_portfolio_data(raw_data)
    except Exception:
        return sanitize_portfolio_data(DEFAULT_PORTFOLIO_SCHEMA)