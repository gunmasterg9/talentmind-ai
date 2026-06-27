import os
import sys
import json
import logging
from sqlalchemy.orm import Session

# Add backend directory to path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "backend"))

from app.database import SessionLocal, engine, Base
from app.models import Candidate
from app.vector_db import vector_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("import_jsonl")

def extract_candidate_data(row, db_session):
    profile = row.get("profile") if isinstance(row.get("profile"), dict) else {}
    cid = str(row.get("candidate_id") or row.get("id") or f"CAND{db_session.query(Candidate).count() + 1:04d}")
    
    name = str(profile.get("anonymized_name") or profile.get("name") or row.get("name") or "Unknown Candidate")
    email = str(profile.get("email") or row.get("email") or f"{cid.lower().replace('-', '_')}@talentmind.ai")
    current_title = str(profile.get("current_title") or row.get("current_title") or "Software Engineer")
    current_company = str(profile.get("current_company") or row.get("current_company") or "Technology Corp")
    
    try:
        total_exp_years = float(profile.get("years_of_experience") if profile.get("years_of_experience") is not None else row.get("total_exp_years", 0.0))
    except (ValueError, TypeError):
        total_exp_years = 0.0

    raw_skills = row.get("skills")
    skills_list = []
    if isinstance(raw_skills, list):
        for s in raw_skills:
            if isinstance(s, dict) and "name" in s:
                skills_list.append(str(s["name"]))
            elif isinstance(s, str):
                skills_list.append(s)
    elif isinstance(raw_skills, str):
        if raw_skills.startswith("[") and raw_skills.endswith("]"):
            try:
                parsed = json.loads(raw_skills)
                if isinstance(parsed, list):
                    skills_list = [str(item.get("name", item) if isinstance(item, dict) else item) for item in parsed]
            except Exception:
                pass
        if not skills_list:
            skills_list = [v.strip() for v in raw_skills.split(",") if v.strip()]

    raw_edu = row.get("education")
    edu_list = raw_edu if isinstance(raw_edu, list) else []

    raw_certs = row.get("certifications")
    certs_list = raw_certs if isinstance(raw_certs, list) else []

    raw_projects = row.get("projects")
    projects_list = raw_projects if isinstance(raw_projects, list) else []
    if not projects_list and isinstance(row.get("career_history"), list):
        projects_list = row.get("career_history")

    ind_exp = profile.get("current_industry") or row.get("industry_experience")
    industry_exp = ", ".join(ind_exp) if isinstance(ind_exp, list) else str(ind_exp or "")

    redrob = row.get("redrob_signals") if isinstance(row.get("redrob_signals"), dict) else {}
    act_signals = row.get("activity_signals") if isinstance(row.get("activity_signals"), dict) else {}

    signals = {
        "recent_certifications": len(certs_list),
        "recent_projects": len(projects_list),
        "github_commits": int(redrob.get("github_activity_score") if redrob and redrob.get("github_activity_score", -1) != -1 else act_signals.get("github_commits", 20)),
        "open_source_prs": int(act_signals.get("open_source_prs", 2))
    }

    location = str(profile.get("location") or row.get("location") or "Remote")

    salary_range = redrob.get("expected_salary_range_inr_lpa") if redrob else None
    expected_ctc = 15.0
    if isinstance(salary_range, dict) and "min" in salary_range:
        try:
            expected_ctc = float(salary_range.get("min") or 15.0)
        except (ValueError, TypeError):
            expected_ctc = 15.0
    elif row.get("expected_ctc_lpa"):
        try:
            expected_ctc = float(row.get("expected_ctc_lpa") or 15.0)
        except (ValueError, TypeError):
            expected_ctc = 15.0

    growth_score = float(redrob.get("profile_completeness_score", 70) / 100.0) if redrob else float(row.get("career_growth_score", 0.7))
    eng_score = float(redrob.get("interview_completion_rate", 0.7)) if redrob and redrob.get("interview_completion_rate", -1) != -1 else float(row.get("engagement_score", 0.7))

    return {
        "candidate_id": cid,
        "name": name,
        "email": email,
        "current_title": current_title,
        "current_company": current_company,
        "total_exp_years": total_exp_years,
        "skills": skills_list,
        "education": edu_list,
        "certifications": certs_list,
        "projects": projects_list,
        "industry_experience": industry_exp,
        "activity_signals": signals,
        "career_growth_score": growth_score,
        "engagement_score": eng_score,
        "location": location,
        "expected_ctc_lpa": expected_ctc
    }

def import_candidates_file(file_path: str, max_records: int = None, batch_size: int = 500):
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return

    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    
    try:
        imported_count = 0
        batch_candidates = []
        batch_ids = []
        batch_texts = []
        batch_metas = []

        with open(file_path, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                if max_records and imported_count >= max_records:
                    break
                line_str = line.strip()
                if not line_str:
                    continue
                try:
                    row = json.loads(line_str)
                except Exception as err:
                    logger.warning(f"Line {line_num}: Invalid JSON. Skipping ({err})")
                    continue

                c_data = extract_candidate_data(row, db)
                
                # Check for existing email to avoid duplicates
                existing = db.query(Candidate).filter(Candidate.email == c_data["email"]).first()
                if existing:
                    continue

                candidate = Candidate(
                    candidate_id=c_data["candidate_id"],
                    name=c_data["name"],
                    email=c_data["email"],
                    current_title=c_data["current_title"],
                    current_company=c_data["current_company"],
                    total_exp_years=c_data["total_exp_years"],
                    skills=json.dumps(c_data["skills"]),
                    education=json.dumps(c_data["education"]),
                    certifications=json.dumps(c_data["certifications"]),
                    projects=json.dumps(c_data["projects"]),
                    industry_experience=c_data["industry_experience"],
                    activity_signals=json.dumps(c_data["activity_signals"]),
                    career_growth_score=c_data["career_growth_score"],
                    engagement_score=c_data["engagement_score"],
                    location=c_data["location"],
                    expected_ctc_lpa=c_data["expected_ctc_lpa"]
                )
                batch_candidates.append(candidate)
                
                profile_text = f"{candidate.current_title} at {candidate.current_company}. Skills: {', '.join(c_data['skills'][:10])}. Experience: {candidate.total_exp_years} years."
                batch_ids.append(candidate.candidate_id)
                batch_texts.append(profile_text)
                batch_metas.append({"name": candidate.name, "skills": ",".join(c_data['skills'][:10])})
                
                imported_count += 1

                if len(batch_candidates) >= batch_size:
                    db.add_all(batch_candidates)
                    db.commit()
                    vector_db.add_candidates_batch(batch_ids, batch_texts, batch_metas)
                    logger.info(f"Imported {imported_count} candidates...")
                    batch_candidates = []
                    batch_ids = []
                    batch_texts = []
                    batch_metas = []

        if batch_candidates:
            db.add_all(batch_candidates)
            db.commit()
            vector_db.add_candidates_batch(batch_ids, batch_texts, batch_metas)

        logger.info(f"Successfully finished importing {imported_count} candidates from {file_path}.")
    except Exception as e:
        db.rollback()
        logger.error(f"Error during import: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "candidates.json")
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else None
    import_candidates_file(path, max_records=limit)
