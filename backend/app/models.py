import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from app.database import Base

class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    
    # Store structured lists as JSON strings
    required_skills = Column(Text, nullable=True)  # JSON list
    preferred_skills = Column(Text, nullable=True) # JSON list
    soft_skills = Column(Text, nullable=True)      # JSON list
    
    min_exp_years = Column(Integer, default=0)
    preferred_exp_years = Column(Integer, default=0)
    seniority_level = Column(String, nullable=True)
    industry_domain = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Candidate(Base):
    __tablename__ = "candidates"
    
    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    current_title = Column(String, index=True, nullable=True)
    current_company = Column(String, nullable=True)
    total_exp_years = Column(Float, default=0.0)
    
    skills = Column(Text, nullable=True)              # JSON list/comma string
    education = Column(Text, nullable=True)           # JSON list of dicts
    certifications = Column(Text, nullable=True)      # JSON list of dicts
    projects = Column(Text, nullable=True)            # JSON list of dicts
    industry_experience = Column(Text, nullable=True) # Comma separated
    activity_signals = Column(Text, nullable=True)    # JSON dict of signals
    
    career_growth_score = Column(Float, default=0.0)
    engagement_score = Column(Float, default=0.0)
    location = Column(String, nullable=True)
    expected_ctc_lpa = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Ranking(Base):
    __tablename__ = "rankings"
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, index=True, nullable=False)
    candidate_id = Column(String, index=True, nullable=False)
    
    composite_score = Column(Float, nullable=False)
    semantic_fit_score = Column(Float, nullable=False)
    experience_score = Column(Float, nullable=False)
    skills_score = Column(Float, nullable=False)
    industry_score = Column(Float, nullable=False)
    activity_score = Column(Float, nullable=False)
    growth_score = Column(Float, nullable=False)
    
    strengths = Column(Text, nullable=True)            # JSON list of strings
    weaknesses = Column(Text, nullable=True)           # JSON list of strings
    recommendation = Column(String, nullable=True)     # Hiring recommendation
    summary = Column(Text, nullable=True)              # Recruiter summary
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
