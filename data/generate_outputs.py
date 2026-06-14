import os
import sys
import json
import csv
import logging

# Add project root to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "backend"))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("generate_outputs")

def generate_outputs():
    from app.database import SessionLocal
    from app.models import Job, Candidate
    from app.schemas import RankingWeights
    from app.scorer import score_candidate
    from app.vector_db import vector_db
    
    db = SessionLocal()
    try:
        # Load Senior ML Engineer job
        job = db.query(Job).filter(Job.job_id == "JD001").first()
        if not job:
            logger.error("Job JD001 not found. Run seed.py first.")
            return
            
        logger.info(f"Loaded job: {job.title} ({job.job_id})")
        
        # Load all candidates
        candidates = db.query(Candidate).all()
        logger.info(f"Loaded {len(candidates)} candidates.")
        
        # Perform semantic query search
        semantic_scores = vector_db.search_candidates(job.description, top_n=100)
        
        job_dict = {
            "title": job.title,
            "required_skills": json.loads(job.required_skills or "[]"),
            "preferred_skills": json.loads(job.preferred_skills or "[]"),
            "min_exp_years": job.min_exp_years,
            "preferred_exp_years": job.preferred_exp_years,
            "industry_domain": job.industry_domain or ""
        }
        
        weights = RankingWeights()
        scored_candidates = []
        
        for c in candidates:
            # Reconstruct candidate dict
            c_dict = {
                "candidate_id": c.candidate_id,
                "name": c.name,
                "email": c.email,
                "current_title": c.current_title,
                "current_company": c.current_company,
                "total_exp_years": c.total_exp_years,
                "skills": json.loads(c.skills or "[]"),
                "industry_experience": [i.strip() for i in (c.industry_experience or "").split(",") if i.strip()],
                "activity_signals": json.loads(c.activity_signals or "{}"),
                "career_growth_score": c.career_growth_score,
                "engagement_score": c.engagement_score,
                "location": c.location,
                "expected_ctc_lpa": c.expected_ctc_lpa
            }
            sem_score = semantic_scores.get(c.candidate_id, 0.5)
            scored = score_candidate(c_dict, job_dict, sem_score, weights)
            scored_candidates.append(scored)
            
        # Sort and rank
        scored_candidates.sort(key=lambda x: x["composite_score"], reverse=True)
        for i, item in enumerate(scored_candidates):
            item["rank"] = i + 1
            
        # Write to outputs
        outputs_dir = os.path.join(BASE_DIR, "outputs")
        os.makedirs(outputs_dir, exist_ok=True)
        
        csv_path = os.path.join(outputs_dir, "ranked_candidates.csv")
        xlsx_path = os.path.join(outputs_dir, "ranked_candidates.xlsx")
        
        # Write CSV
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Rank", "Candidate ID", "Name", "Email", "Current Title", "Current Company", 
                             "Total Experience (Yrs)", "Composite Score", "Semantic Match Score", 
                             "Experience Match Score", "Skills Match Score", "Industry Match Score", 
                             "Activity Score", "Growth Score", "Hiring Recommendation", "Summary"])
            for r in scored_candidates:
                writer.writerow([
                    r["rank"], r["candidate_id"], r["name"], r["email"], r["current_title"], r["current_company"],
                    r["total_exp_years"], r["composite_score"], r["semantic_fit_score"], 
                    r["experience_score"], r["skills_score"], r["industry_score"],
                    r["activity_score"], r["growth_score"], r["xai"].recommendation, r["xai"].summary
                ])
        logger.info(f"Generated ranked CSV: {csv_path}")
        
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
            for r in scored_candidates:
                ws.append([
                    r["rank"], r["candidate_id"], r["name"], r["email"], r["current_title"], r["current_company"],
                    r["total_exp_years"], r["composite_score"], r["semantic_fit_score"], 
                    r["experience_score"], r["skills_score"], r["industry_score"],
                    r["activity_score"], r["growth_score"], r["xai"].recommendation, r["xai"].summary
                ])
            wb.save(xlsx_path)
            logger.info(f"Generated ranked Excel (openpyxl): {xlsx_path}")
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
                } for r in scored_candidates])
                df.to_excel(xlsx_path, index=False)
                logger.info(f"Generated ranked Excel (pandas): {xlsx_path}")
            except Exception as ex:
                logger.warning(f"Pandas write to excel failed ({ex}). Copying CSV instead.")
                import shutil
                shutil.copyfile(csv_path, xlsx_path)
            
    finally:
        db.close()

if __name__ == "__main__":
    generate_outputs()
