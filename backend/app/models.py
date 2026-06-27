import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, index=True, nullable=False)
    company = Column(String, index=True, nullable=True, default="Redrob Tech")
    location = Column(String, nullable=True, default="Remote")
    salary_range = Column(String, nullable=True, default="$120k - $160k")
    description = Column(Text, nullable=True)
    
    # Store structured lists as JSON strings
    required_skills = Column(Text, nullable=True)  # JSON list
    preferred_skills = Column(Text, nullable=True) # JSON list
    soft_skills = Column(Text, nullable=True)      # JSON list
    
    min_exp_years = Column(Integer, default=0)
    preferred_exp_years = Column(Integer, default=0)
    seniority_level = Column(String, nullable=True)
    industry_domain = Column(String, nullable=True)
    job_type = Column(String, default="Full-time") # Full-time, Internship, Hackathon, Freelance
    match_probability = Column(Float, default=0.85)
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
    
    career_growth_score = Column(Float, default=88.5)
    engagement_score = Column(Float, default=92.0)
    ats_score = Column(Float, default=84.0)
    skill_index = Column(Float, default=90.0)
    interview_score = Column(Float, default=86.5)
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

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(String, default="candidate") # candidate, recruiter, admin
    is_premium = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Application(Base):
    __tablename__ = "applications"
    
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(String, index=True, nullable=False)
    job_id = Column(String, index=True, nullable=False)
    job_title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    status = Column(String, default="Applied") # Applied, Interviewing, Offered, Rejected
    fit_score = Column(Float, default=90.0)
    applied_at = Column(DateTime, default=datetime.datetime.utcnow)

class Goal(Base):
    __tablename__ = "goals"
    
    id = Column(Integer, primary_key=True, index=True)
    goal_id = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(String, index=True, nullable=False)
    title = Column(String, nullable=False)
    category = Column(String, default="Career Growth")
    progress = Column(Integer, default=50) # 0-100
    target_date = Column(String, nullable=True)
    status = Column(String, default="In Progress")

class LearningItem(Base):
    __tablename__ = "learning_items"
    
    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(String, index=True, nullable=False)
    title = Column(String, nullable=False)
    type = Column(String, default="Course") # Course, YouTube, Project
    provider = Column(String, default="Coursera")
    url = Column(String, nullable=True)
    progress = Column(Integer, default=0)
    status = Column(String, default="Recommended") # Recommended, In Progress, Completed

class InterviewSession(Base):
    __tablename__ = "interview_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(String, index=True, nullable=False)
    role_title = Column(String, nullable=False)
    interview_type = Column(String, default="Behavioral") # Voice, Coding, Behavioral, HR
    score = Column(Float, default=85.0)
    feedback_json = Column(Text, nullable=True) # JSON evaluation
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    notification_id = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(String, index=True, nullable=False)
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    type = Column(String, default="info") # info, job, agent, alert
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class AgentMemory(Base):
    __tablename__ = "agent_memories"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False)
    agent_name = Column(String, index=True, nullable=False)
    memory_key = Column(String, nullable=False)
    memory_value = Column(Text, nullable=False) # JSON string or text
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
