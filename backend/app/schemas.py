from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime

class JobBase(BaseModel):
    job_id: str
    title: str
    description: Optional[str] = None
    required_skills: List[str] = []
    preferred_skills: List[str] = []
    soft_skills: List[str] = []
    min_exp_years: int = 0
    preferred_exp_years: int = 0
    seniority_level: Optional[str] = None
    industry_domain: Optional[str] = None

class JobCreate(JobBase):
    pass

class JobOut(JobBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class CandidateBase(BaseModel):
    candidate_id: str
    name: str
    email: str
    current_title: Optional[str] = None
    current_company: Optional[str] = None
    total_exp_years: float = 0.0
    skills: List[str] = []
    education: List[Dict[str, Any]] = []
    certifications: List[Dict[str, Any]] = []
    projects: List[Dict[str, Any]] = []
    industry_experience: List[str] = []
    activity_signals: Dict[str, Any] = {}
    career_growth_score: float = 0.0
    engagement_score: float = 0.0
    location: Optional[str] = None
    expected_ctc_lpa: float = 0.0

class CandidateCreate(CandidateBase):
    pass

class CandidateOut(CandidateBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class RankingWeights(BaseModel):
    semantic_match: float = 0.35
    experience_match: float = 0.20
    skill_match: float = 0.15
    industry_match: float = 0.10
    activity_score: float = 0.10
    career_growth_score: float = 0.10

class RankRequest(BaseModel):
    job_id: Optional[str] = None
    job_description: Optional[str] = None
    required_skills: Optional[List[str]] = None
    min_exp_years: Optional[int] = None
    preferred_exp_years: Optional[int] = None
    weights: Optional[RankingWeights] = None
    top_n: int = 20

class ExplainableAI(BaseModel):
    strengths: List[str] = []
    weaknesses: List[str] = []
    recommendation: str
    summary: str

class CandidateRankingOut(BaseModel):
    rank: int
    candidate_id: str
    name: str
    email: str
    current_title: Optional[str] = None
    current_company: Optional[str] = None
    total_exp_years: float
    skills: List[str]
    location: Optional[str] = None
    composite_score: float
    semantic_fit_score: float
    experience_score: float
    skills_score: float
    industry_score: float
    activity_score: float
    growth_score: float
    xai: ExplainableAI

class RankResponse(BaseModel):
    job_title: str
    total_ranked: int
    rankings: List[CandidateRankingOut]
