import io
import csv
import json
import os
import logging
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models import Job, Candidate, Ranking
from app.schemas import (
    JobCreate, JobOut, CandidateOut, RankRequest, RankResponse, 
    CandidateRankingOut, ExplainableAI
)
from app.parser import parse_job_description
from app.vector_db import vector_db
from app.scorer import score_candidate

logger = logging.getLogger(__name__)
router = APIRouter()

# Directories configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUTPUTS_DIR, exist_ok=True)

# Helper function: Convert candidate DB model to dict
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
        "location": c.location,
        "expected_ctc_lpa": c.expected_ctc_lpa
    }

# ─── API Routes ───────────────────────────────────────────────────────────────

@router.post("/jobs/upload", response_model=JobOut)
def upload_job(description_text: str, title: Optional[str] = None, db: Session = Depends(get_db)):
    """Upload a raw job description, parse it using AI/Rules, and store it."""
    try:
        parsed = parse_job_description(description_text)
        if title:
            parsed["title"] = title
            
        # Generate new unique job id
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
        
        # Format response
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
        logger.error(f"Error uploading job: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/candidates/upload")
def upload_candidates_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload candidate database CSV file, parse columns, and seed DB & ChromaDB."""
    try:
        contents = file.file.read().decode("utf-8")
        reader = csv.DictReader(io.StringIO(contents))
        
        imported_count = 0
        for row in reader:
            cid = row.get("candidate_id") or f"CAND{db.query(Candidate).count() + 1:04d}"
            
            # Helper to parse lists/dicts from CSV safely
            def parse_csv_list(val):
                if not val:
                    return []
                if val.startswith("[") and val.endswith("]"):
                    try:
                        return json.loads(val)
                    except Exception:
                        pass
                return [v.strip() for v in val.split(",") if v.strip()]
            
            def parse_csv_dict(val):
                if not val:
                    return {}
                try:
                    return json.loads(val)
                except Exception:
                    pass
                return {}
                
            skills = parse_csv_list(row.get("skills", ""))
            education = parse_csv_list(row.get("education", ""))
            certs = parse_csv_list(row.get("certifications", ""))
            projects = parse_csv_list(row.get("projects", ""))
            industry_exp = row.get("industry_experience", "")
            signals = parse_csv_dict(row.get("activity_signals", ""))
            
            # Check for existing email to avoid duplicates
            email = row.get("email", f"{cid.lower()}@talentmind.ai")
            existing = db.query(Candidate).filter(Candidate.email == email).first()
            if existing:
                continue
                
            candidate = Candidate(
                candidate_id=cid,
                name=row.get("name", "Unknown Name"),
                email=email,
                current_title=row.get("current_title", "Software Engineer"),
                current_company=row.get("current_company", "Technology Corp"),
                total_exp_years=float(row.get("total_exp_years", 0.0) or 0.0),
                skills=json.dumps(skills),
                education=json.dumps(education),
                certifications=json.dumps(certs),
                projects=json.dumps(projects),
                industry_experience=industry_exp,
                activity_signals=json.dumps(signals),
                career_growth_score=float(row.get("career_growth_score", 0.5) or 0.5),
                engagement_score=float(row.get("engagement_score", 0.5) or 0.5),
                location=row.get("location", "Remote"),
                expected_ctc_lpa=float(row.get("expected_ctc_lpa", 15.0) or 15.0)
            )
            db.add(candidate)
            
            # Seed into vector DB
            profile_text = f"{candidate.current_title} at {candidate.current_company}. Skills: {', '.join(skills)}. Experience: {candidate.total_exp_years} years. Education: {row.get('education', '')}"
            vector_db.add_candidate(cid, profile_text, {"name": candidate.name, "skills": ",".join(skills)})
            imported_count += 1
            
        db.commit()
        return {"status": "success", "imported_count": imported_count}
    except Exception as e:
        db.rollback()
        logger.error(f"Error seeding CSV: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/rank", response_model=RankResponse)
def rank_candidates(req: RankRequest, db: Session = Depends(get_db)):
    """Rank candidates against a job description using weighted multi-signal scoring."""
    try:
        # Determine target JD requirements
        jd_text = ""
        required_skills = []
        preferred_skills = []
        min_exp = 0
        preferred_exp = 5
        job_title = "Custom Query"
        job_domain = ""
        job_id = "CUSTOM"
        
        if req.job_id:
            job = db.query(Job).filter(Job.job_id == req.job_id).first()
            if not job:
                raise HTTPException(status_code=404, detail="Job ID not found")
            jd_text = job.description or f"{job.title} position"
            required_skills = json.loads(job.required_skills or "[]")
            preferred_skills = json.loads(job.preferred_skills or "[]")
            min_exp = job.min_exp_years
            preferred_exp = job.preferred_exp_years
            job_title = job.title
            job_domain = job.industry_domain or ""
            job_id = job.job_id
        else:
            jd_text = req.job_description or ""
            required_skills = req.required_skills or []
            min_exp = req.min_exp_years or 0
            preferred_exp = req.preferred_exp_years or 5
            
        if not jd_text:
            raise HTTPException(status_code=400, detail="Either job_id or job_description is required")
            
        # Get semantic match scores from vector DB
        semantic_scores = vector_db.search_candidates(jd_text, top_n=100)
        
        # Load all candidates from DB
        candidates = db.query(Candidate).all()
        if not candidates:
            return RankResponse(job_title=job_title, total_ranked=0, rankings=[])
            
        # Score each candidate
        scored_candidates = []
        weights = req.weights or RankingWeights()
        
        job_dict = {
            "title": job_title,
            "required_skills": required_skills,
            "preferred_skills": preferred_skills,
            "min_exp_years": min_exp,
            "preferred_exp_years": preferred_exp,
            "industry_domain": job_domain
        }
        
        for c in candidates:
            c_dict = candidate_to_dict(c)
            sem_score = semantic_scores.get(c.candidate_id, 0.5)
            
            scored = score_candidate(c_dict, job_dict, sem_score, weights)
            scored_candidates.append(scored)
            
        # Sort by composite score
        scored_candidates.sort(key=lambda x: x["composite_score"], reverse=True)
        top_candidates = scored_candidates[:req.top_n]
        
        # Add rank indexes
        for i, item in enumerate(top_candidates):
            item["rank"] = i + 1
            
        # Clear previous rankings for this job_id, and save new rankings
        db.query(Ranking).filter(Ranking.job_id == job_id).delete()
        for r in top_candidates:
            ranking_db = Ranking(
                job_id=job_id,
                candidate_id=r["candidate_id"],
                composite_score=r["composite_score"],
                semantic_fit_score=r["semantic_fit_score"],
                experience_score=r["experience_score"],
                skills_score=r["skills_score"],
                industry_score=r["industry_score"],
                activity_score=r["activity_score"],
                growth_score=r["growth_score"],
                strengths=json.dumps(r["xai"].strengths),
                weaknesses=json.dumps(r["xai"].weaknesses),
                recommendation=r["xai"].recommendation,
                summary=r["xai"].summary
            )
            db.add(ranking_db)
        db.commit()
        
        # Generate export files (CSV & XLSX fallbacks)
        csv_path = os.path.join(OUTPUTS_DIR, "ranked_candidates.csv")
        xlsx_path = os.path.join(OUTPUTS_DIR, "ranked_candidates.xlsx")
        
        # Write CSV
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Rank", "Candidate ID", "Name", "Email", "Current Title", "Current Company", 
                             "Total Experience (Yrs)", "Composite Score", "Semantic Match Score", 
                             "Experience Match Score", "Skills Match Score", "Industry Match Score", 
                             "Activity Score", "Growth Score", "Hiring Recommendation", "Summary"])
            for r in top_candidates:
                writer.writerow([
                    r["rank"], r["candidate_id"], r["name"], r["email"], r["current_title"], r["current_company"],
                    r["total_exp_years"], r["composite_score"], r["semantic_fit_score"], 
                    r["experience_score"], r["skills_score"], r["industry_score"],
                    r["activity_score"], r["growth_score"], r["xai"].recommendation, r["xai"].summary
                ])
                
        # Write XLSX using openpyxl directly (pure python, no numpy dependencies)
        try:
            import openpyxl
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Ranked Candidates"
            ws.append(["Rank", "Candidate ID", "Name", "Email", "Current Title", "Current Company", 
                       "Total Experience (Yrs)", "Composite Score", "Semantic Match Score", 
                       "Experience Match Score", "Skills Match Score", "Industry Match Score", 
                       "Activity Score", "Growth Score", "Hiring Recommendation", "Summary"])
            for r in top_candidates:
                ws.append([
                    r["rank"], r["candidate_id"], r["name"], r["email"], r["current_title"], r["current_company"],
                    r["total_exp_years"], r["composite_score"], r["semantic_fit_score"], 
                    r["experience_score"], r["skills_score"], r["industry_score"],
                    r["activity_score"], r["growth_score"], r["xai"].recommendation, r["xai"].summary
                ])
            wb.save(xlsx_path)
        except Exception as e:
            logger.warning(f"openpyxl write to excel failed ({e}). Trying pandas fallback.")
            try:
                import pandas as pd
                df = pd.DataFrame([{
                    "Rank": r["rank"], "Candidate ID": r["candidate_id"], "Name": r["name"], "Email": r["email"],
                    "Current Title": r["current_title"], "Current Company": r["current_company"],
                    "Total Experience": r["total_exp_years"], "Composite Score": r["composite_score"],
                    "Semantic Match": r["semantic_fit_score"], "Experience Match": r["experience_score"],
                    "Skills Match": r["skills_score"], "Industry Match": r["industry_score"],
                    "Activity Score": r["activity_score"], "Growth Score": r["growth_score"],
                    "Recommendation": r["xai"].recommendation, "Summary": r["xai"].summary
                } for r in top_candidates])
                df.to_excel(xlsx_path, index=False)
            except Exception as ex:
                logger.warning(f"Failed to generate Excel file via pandas ({ex}). Copying CSV instead.")
                import shutil
                shutil.copyfile(csv_path, xlsx_path)
            
        return RankResponse(
            job_title=job_title,
            total_ranked=len(top_candidates),
            rankings=[CandidateRankingOut(**item) for item in top_candidates]
        )
    except Exception as e:
        logger.error(f"Error ranking candidates: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/candidates", response_model=List[CandidateOut])
def get_candidates(db: Session = Depends(get_db)):
    """Retrieve all candidates stored in database."""
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

@router.get("/jobs", response_model=List[JobOut])
def get_jobs(db: Session = Depends(get_db)):
    """Retrieve all job descriptions."""
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

@router.get("/rankings")
def get_rankings(job_id: str = "CUSTOM", db: Session = Depends(get_db)):
    """Retrieve the computed ranking table for a job position."""
    rankings = db.query(Ranking).filter(Ranking.job_id == job_id).order_by(Ranking.composite_score.desc()).all()
    results = []
    for i, r in enumerate(rankings):
        cand = db.query(Candidate).filter(Candidate.candidate_id == r.candidate_id).first()
        if not cand:
            continue
            
        results.append({
            "rank": i + 1,
            "candidate_id": r.candidate_id,
            "name": cand.name,
            "email": cand.email,
            "current_title": cand.current_title,
            "current_company": cand.current_company,
            "total_exp_years": cand.total_exp_years,
            "skills": json.loads(cand.skills or "[]"),
            "location": cand.location,
            "composite_score": r.composite_score,
            "semantic_fit_score": r.semantic_fit_score,
            "experience_score": r.experience_score,
            "skills_score": r.skills_score,
            "industry_score": r.industry_score,
            "activity_score": r.activity_score,
            "growth_score": r.growth_score,
            "xai": {
                "strengths": json.loads(r.strengths or "[]"),
                "weaknesses": json.loads(r.weaknesses or "[]"),
                "recommendation": r.recommendation,
                "summary": r.summary
            }
        })
    return results

@router.get("/candidate/{id}")
def get_candidate_by_id(id: str, db: Session = Depends(get_db)):
    """Get candidate detailed profile by ID/code."""
    c = db.query(Candidate).filter(Candidate.candidate_id == id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Candidate not found")
        
    return {
        "candidate": candidate_to_dict(c),
        "rankings_history": db.query(Ranking).filter(Ranking.candidate_id == id).all()
    }

@router.get("/download/{file_format}")
def download_ranked_file(file_format: str):
    """Download the latest generated ranked candidates list in CSV or XLSX format."""
    if file_format.lower() == "csv":
        path = os.path.join(OUTPUTS_DIR, "ranked_candidates.csv")
        media = "text/csv"
        dl_name = "ranked_candidates.csv"
    elif file_format.lower() in ["xlsx", "excel"]:
        path = os.path.join(OUTPUTS_DIR, "ranked_candidates.xlsx")
        media = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        dl_name = "ranked_candidates.xlsx"
    else:
        raise HTTPException(status_code=400, detail="Invalid format. Supported formats: csv, xlsx")
        
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="No ranking outputs found. Run a ranking query first.")
        
    return FileResponse(path, media_type=media, filename=dl_name)
