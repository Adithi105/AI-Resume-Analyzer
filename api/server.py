"""
FastAPI REST API Server — Exposes RESTful endpoints for Enterprise Recruitment integrations.

Endpoints:
  GET  /api/v1/health
  GET  /api/v1/candidates
  POST /api/v1/analyze
  POST /api/v1/rank
  GET  /api/v1/interviews
"""
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import os
import sys

# Ensure root dir is in python path
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from database.db import get_all_resumes, get_all_interviews, save_resume_record
from ai_engine import analyze_resume

app = FastAPI(
    title="ResuMind Enterprise Recruitment REST API",
    description="RESTful API endpoints for AI resume auditing, candidate databases, batch ranking, and interview management.",
    version="1.0.0"
)


class ResumeAnalysisRequest(BaseModel):
    resume_text: str
    candidate_name: Optional[str] = "Candidate"
    email: Optional[str] = "candidate@example.com"
    phone: Optional[str] = "N/A"


class BatchRankRequest(BaseModel):
    resumes: List[str]


@app.get("/api/v1/health")
def health_check():
    return {"status": "ONLINE", "service": "ResuMind Enterprise REST API", "version": "1.0.0"}


@app.get("/api/v1/candidates")
def list_candidates():
    records = get_all_resumes()
    return {"count": len(records), "candidates": records}


@app.post("/api/v1/analyze")
def analyze_resume_endpoint(req: ResumeAnalysisRequest):
    if not req.resume_text or not req.resume_text.strip():
        raise HTTPException(status_code=400, detail="Empty resume text provided.")

    ai_res = analyze_resume(req.resume_text)

    # Save to DB
    record_id = save_resume_record(
        candidate_name=req.candidate_name or ai_res.get("Name", "Candidate"),
        email=req.email or ai_res.get("Email", ""),
        phone=req.phone or ai_res.get("Phone", ""),
        ats_score=ai_res.get("ATS_Score", 0),
        verdict=ai_res.get("Recruiter_Verdict", "Under Review"),
        hiring_prob=ai_res.get("Hiring_Probability", "0%"),
        candidate_level=ai_res.get("Candidate_Level", "Not Specified"),
        raw_text=req.resume_text,
        full_json=ai_res
    )

    return {"status": "SUCCESS", "resume_id": record_id, "analysis": ai_res}


@app.get("/api/v1/interviews")
def list_interviews():
    interviews = get_all_interviews()
    return {"count": len(interviews), "interviews": interviews}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
