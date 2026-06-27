import io
import csv
import json
import os
import logging
import datetime
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import (
    Job, Candidate, Ranking, User, Application, Goal, LearningItem, 
    InterviewSession, Notification, AgentMemory
)
from app.schemas import (
    JobOut, CandidateOut, RankRequest, RankResponse, 
    CandidateRankingOut
)
from app.parser import parse_job_description
from app.vector_db import vector_db
from app.scorer import score_candidate
from app.agents.framework import AgentState, LLMProviderFactory
from app.agents.implementations import (
    ExecutiveAgent, CareerCoachAgent, ResumeAgent, SkillGapAgent, JobDiscoveryAgent,
    RecruiterAgent, NetworkingAgent, InterviewAgent, LearningAgent, SalaryIntelligenceAgent,
    CareerForecastAgent, OpportunityMonitor
)
from app.services.vector_service import vector_service
from app.services.graph_service import graph_service
from app.websocket_manager import manager

logger = logging.getLogger(__name__)
router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUTPUTS_DIR, exist_ok=True)

def candidate_to_dict(c: Candidate) -> dict:
    return {
        "candidate_id": c.candidate_id,
        "name": c.name,
        "email": c.email,
        "current_title": c.current_title,
        "current_company": c.current_company,
        "total_exp_years": c.total_exp_years,
        "skills": json.loads(c.skills or "[]"),
        "education": json.loads(c.education or "[]"),
        "certifications": json.loads(c.certifications or "[]"),
        "projects": json.loads(c.projects or "[]"),
        "industry_experience": [i.strip() for i in (c.industry_experience or "").split(",") if i.strip()],
        "activity_signals": json.loads(c.activity_signals or "{}"),
        "career_growth_score": c.career_growth_score,
        "engagement_score": c.engagement_score,
        "ats_score": c.ats_score,
        "skill_index": c.skill_index,
        "interview_score": c.interview_score,
        "location": c.location,
        "expected_ctc_lpa": c.expected_ctc_lpa
    }

# ─── EXISTING CORE MATCHING ROUTES ────────────────────────────────────────────

@router.post("/jobs/upload", response_model=JobOut)
def upload_job(description_text: str, title: Optional[str] = None, db: Session = Depends(get_db)):
    try:
        parsed = parse_job_description(description_text)
        if title:
            parsed["title"] = title
        existing_count = db.query(Job).count()
        job_id = f"JD{existing_count + 1:03d}"
        job = Job(
            job_id=job_id,
            title=parsed["title"],
            description=description_text,
            required_skills=json.dumps(parsed.get("required_skills", [])),
            preferred_skills=json.dumps(parsed.get("preferred_skills", [])),
            soft_skills=json.dumps(parsed.get("soft_skills", [])),
            min_exp_years=parsed.get("min_exp_years", 0),
            preferred_exp_years=parsed.get("preferred_exp_years", 5),
            seniority_level=parsed.get("seniority_level", "Mid"),
            industry_domain=parsed.get("industry_domain", "General")
        )
        db.add(job)
        db.commit()
        db.refresh(job)
        return JobOut(
            id=job.id,
            job_id=job.job_id,
            title=job.title,
            description=job.description,
            required_skills=json.loads(job.required_skills),
            preferred_skills=json.loads(job.preferred_skills),
            soft_skills=json.loads(job.soft_skills),
            min_exp_years=job.min_exp_years,
            preferred_exp_years=job.preferred_exp_years,
            seniority_level=job.seniority_level,
            industry_domain=job.industry_domain,
            created_at=job.created_at
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/jobs", response_model=List[JobOut])
def get_jobs(db: Session = Depends(get_db)):
    jobs = db.query(Job).all()
    if not jobs:
        # Provide seed jobs if empty
        seed = [
            Job(job_id="JOB-101", title="Lead AI Autonomous Systems Engineer", company="ScaleAI Next", location="Remote / SF", salary_range="$160k - $210k", description="Build scalable multi-agent frameworks.", required_skills=json.dumps(["FastAPI", "LangGraph", "Python"]), preferred_skills=json.dumps(["Qdrant", "Neo4j"]), soft_skills=json.dumps(["Leadership"]), min_exp_years=4, preferred_exp_years=6, seniority_level="Senior", industry_domain="AI SaaS"),
            Job(job_id="JOB-102", title="Senior Staff Backend Engineer", company="DeepMind Partner", location="Remote", salary_range="$150k - $190k", description="High throughput python backend microservices.", required_skills=json.dumps(["FastAPI", "PostgreSQL", "Redis"]), preferred_skills=json.dumps(["Docker", "Kubernetes"]), soft_skills=json.dumps(["Communication"]), min_exp_years=5, preferred_exp_years=8, seniority_level="Staff", industry_domain="Cloud Systems"),
            Job(job_id="JOB-103", title="Full-Stack AI Architect", company="Redrob Global", location="Hybrid / NY", salary_range="$140k - $180k", description="Next.js 15 and FastAPI AI portal.", required_skills=json.dumps(["Next.js", "React", "TypeScript", "Tailwind"]), preferred_skills=json.dumps(["Python", "FastAPI"]), soft_skills=json.dumps(["Agile"]), min_exp_years=3, preferred_exp_years=5, seniority_level="Senior", industry_domain="Enterprise SaaS")
        ]
        for s in seed:
            db.add(s)
        db.commit()
        jobs = db.query(Job).all()

    results = []
    for job in jobs:
        results.append(JobOut(
            id=job.id,
            job_id=job.job_id,
            title=job.title,
            description=job.description,
            required_skills=json.loads(job.required_skills or "[]"),
            preferred_skills=json.loads(job.preferred_skills or "[]"),
            soft_skills=json.loads(job.soft_skills or "[]"),
            min_exp_years=job.min_exp_years,
            preferred_exp_years=job.preferred_exp_years,
            seniority_level=job.seniority_level,
            industry_domain=job.industry_domain,
            created_at=job.created_at
        ))
    return results

@router.get("/candidates", response_model=List[CandidateOut])
def get_candidates(db: Session = Depends(get_db)):
    candidates = db.query(Candidate).all()
    results = []
    for c in candidates:
        results.append(CandidateOut(
            id=c.id,
            candidate_id=c.candidate_id,
            name=c.name,
            email=c.email,
            current_title=c.current_title,
            current_company=c.current_company,
            total_exp_years=c.total_exp_years,
            skills=json.loads(c.skills or "[]"),
            education=json.loads(c.education or "[]"),
            certifications=json.loads(c.certifications or "[]"),
            projects=json.loads(c.projects or "[]"),
            industry_experience=[i.strip() for i in (c.industry_experience or "").split(",") if i.strip()],
            activity_signals=json.loads(c.activity_signals or "{}"),
            career_growth_score=c.career_growth_score,
            engagement_score=c.engagement_score,
            location=c.location,
            expected_ctc_lpa=c.expected_ctc_lpa,
            created_at=c.created_at
        ))
    return results

# ─── REDROB MULTI-AGENT & DASHBOARD ENDPOINTS ─────────────────────────────────

@router.post("/agents/chat")
def agent_chat(payload: Dict[str, Any]):
    message = payload.get("message", "")
    provider = payload.get("provider", "openai")
    agent_type = payload.get("agent_type", "General AI Career Assistant")
    
    system_prompt = f"You are Redrob's autonomous {agent_type}. Provide actionable, high-impact career guidance."
    response_text = LLMProviderFactory.generate_response(message, system_message=system_prompt, provider=provider)
    
    return {
        "agent": agent_type,
        "provider": provider,
        "response": response_text,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

@router.post("/agents/orchestrate")
def orchestrate_career(payload: Dict[str, Any]):
    user_id = payload.get("user_id", "USR-001")
    state = AgentState(user_id=user_id)
    exec_agent = ExecutiveAgent()
    result = exec_agent.orchestrate_user_onboarding(state, payload.get("profile", {}))
    return result

@router.get("/agents/opportunity-monitor")
def check_opportunities():
    monitor = OpportunityMonitor()
    opportunities = monitor.check_new_opportunities()
    return {"status": "Active 24x7", "opportunities": opportunities}

@router.post("/agents/interview/evaluate")
def evaluate_interview(payload: Dict[str, Any]):
    agent = InterviewAgent()
    res = agent.evaluate_response(payload.get("response", ""), payload.get("question_type", "Behavioral"))
    return res

@router.get("/agents/salary-intelligence")
def get_salary_intelligence(role: str = "Senior AI Engineer", location: str = "Remote", experience_years: float = 5.0):
    agent = SalaryIntelligenceAgent()
    return agent.analyze_compensation(role, location, experience_years)

@router.get("/agents/forecast")
def get_career_forecast(user_id: str = "USR-001"):
    state = AgentState(user_id=user_id)
    agent = CareerForecastAgent()
    return agent.forecast_trajectory(state)

@router.get("/dashboard/candidate")
def get_candidate_dashboard(db: Session = Depends(get_db)):
    return {
        "career_health_score": 88.5,
        "ats_score": 84.0,
        "skill_index": 90.0,
        "interview_score": 86.5,
        "application_success_rate": "38%",
        "learning_progress": "65%",
        "network_growth": "+14 connections this week",
        "salary_growth_projection": "+24% ($165,000 median)",
        "active_jobs_count": db.query(Job).count(),
        "recent_applications": [
            {"id": "APP-1", "job_title": "Lead AI Autonomous Systems Engineer", "company": "ScaleAI Next", "status": "Applied", "fit_score": 96.2},
            {"id": "APP-2", "job_title": "Senior Staff Backend Engineer", "company": "DeepMind Partner", "status": "Interviewing", "fit_score": 92.8}
        ]
    }

@router.get("/dashboard/recruiter")
def get_recruiter_dashboard(db: Session = Depends(get_db)):
    candidates = db.query(Candidate).all()
    recruiter_agent = RecruiterAgent()
    cand_dicts = [candidate_to_dict(c) for c in candidates]
    ranked = recruiter_agent.rank_candidates("JOB-101", cand_dicts)
    
    return {
        "total_applicants": len(candidates) or 12,
        "top_matches_count": len(ranked),
        "avg_match_score": "91.4%",
        "interviews_scheduled": 4,
        "ranked_candidates": ranked
    }

@router.get("/graph/candidate/{candidate_id}")
def get_candidate_graph(candidate_id: str):
    return graph_service.get_candidate_skill_graph(candidate_id)

@router.get("/vector/search")
def vector_job_search(query: str):
    return vector_service.search_similar_jobs(query)

# ─── REALTIME WEBSOCKET ───────────────────────────────────────────────────────

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message({"event": "agent_ack", "received": data}, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
