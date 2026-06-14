import os
import sys
import json
import csv
import random
import logging

# Add project root to sys.path so we can import app modules
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "backend"))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("seed")

# Seed seed
random.seed(101)

FIRST_NAMES = ["Rohan", "Aisha", "Karan", "Priya", "Vikram", "Sneha", "Anil", "Meera", "Kabir", "Neha", 
               "Dev", "Riya", "Raj", "Aditi", "Amit", "Pooja", "Rahul", "Shreya", "Sanjay", "Tanvi"]
LAST_NAMES = ["Sharma", "Patel", "Verma", "Sen", "Gupta", "Nair", "Reddy", "Mehta", "Iyer", "Rao", 
              "Joshi", "Choudhury", "Das", "Singh", "Mishra", "Dubey", "Kapoor", "Roy", "Bose", "Trivedi"]

TITLES = ["Software Engineer", "Senior Software Engineer", "ML Engineer", "Senior ML Engineer", 
          "Data Scientist", "Lead Data Scientist", "DevOps Engineer", "Cloud Solutions Architect",
          "Full Stack Developer", "Backend Developer", "Frontend Developer", "AI Engineer"]

COMPANIES = ["TCS", "Infosys", "Wipro", "Cognizant", "Google", "Microsoft", "Amazon", "Razorpay", 
             "Paytm", "Flipkart", "CRED", "Zomato", "Swiggy", "Adobe", "Salesforce"]

TECH_SKILLS = ["Python", "Java", "JavaScript", "TypeScript", "React", "Node.js", "Django", "FastAPI", 
               "PostgreSQL", "MongoDB", "Redis", "Docker", "Kubernetes", "AWS", "GCP", "Terraform",
               "CI/CD", "Machine Learning", "Deep Learning", "PyTorch", "TensorFlow", "Pandas", "Spark"]

INDUSTRIES = ["Finance", "Healthcare", "E-commerce", "SaaS", "Telecommunications", "EdTech", "Logistics"]

UNIVERSITIES = ["IIT Bombay", "IIT Delhi", "BITS Pilani", "NIT Trichy", "Delhi University", "VIT Vellore", "PES University"]

def generate_csv_data(filepath: str, count: int = 100):
    logger.info(f"Generating {count} candidate rows in {filepath}...")
    candidates = []
    
    for i in range(1, count + 1):
        name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        email = f"{name.lower().replace(' ', '_')}{i}@talentmind.ai"
        title = random.choice(TITLES)
        company = random.choice(COMPANIES)
        exp = round(random.uniform(1.0, 15.0), 1)
        
        # Skills subset
        skills_count = random.randint(5, 10)
        skills = random.sample(TECH_SKILLS, skills_count)
        
        # Make ML Engineer profiles match ML skills
        if "ML" in title or "Data Scientist" in title:
            skills = list(set(skills + ["Python", "Machine Learning", "PyTorch", "Pandas"]))
            
        # Education dict
        edu = [{
            "degree": random.choice(["B.Tech Computer Science", "M.Tech Software Engineering", "M.Sc Data Science", "B.Sc CS"]),
            "institution": random.choice(UNIVERSITIES),
            "year": int(2026 - exp - random.randint(3, 4))
        }]
        
        # Certifications
        certs = []
        if random.random() > 0.4:
            certs.append({
                "title": random.choice(["AWS Certified Solutions Architect", "Google Cloud Professional Data Engineer", "TensorFlow Developer Certificate"]),
                "issuer": random.choice(["AWS", "Google Cloud", "DeepLearning.AI"]),
                "year": random.randint(2024, 2026)
            })
            
        # Projects
        projects = [{
            "title": f"Project {random.choice(['Alpha', 'Beta', 'Omega', 'Vanguard'])}",
            "description": f"Developed an automated pipeline using {', '.join(skills[:2])} for scalable matching.",
            "tech_stack": skills[:3]
        }]
        
        # Industries
        ind_experience = ",".join(random.sample(INDUSTRIES, random.randint(1, 3)))
        
        # Activity signals
        signals = {
            "recent_certifications": len(certs),
            "recent_projects": len(projects),
            "github_commits": random.randint(10, 250),
            "open_source_prs": random.randint(0, 8)
        }
        
        candidates.append({
            "candidate_id": f"CAND{i:04d}",
            "name": name,
            "email": email,
            "current_title": title,
            "current_company": company,
            "total_exp_years": exp,
            "skills": json.dumps(skills),
            "education": json.dumps(edu),
            "certifications": json.dumps(certs),
            "projects": json.dumps(projects),
            "industry_experience": ind_experience,
            "activity_signals": json.dumps(signals),
            "career_growth_score": round(random.uniform(0.4, 0.95), 2),
            "engagement_score": round(random.uniform(0.3, 0.98), 2),
            "location": random.choice(["Bangalore", "Mumbai", "Hyderabad", "Delhi", "Remote", "Pune"]),
            "expected_ctc_lpa": round(random.uniform(8.0, 50.0), 1)
        })
        
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=candidates[0].keys())
        writer.writeheader()
        writer.writerows(candidates)
        
    logger.info("CSV generation complete.")

def seed_database():
    csv_path = os.path.join(BASE_DIR, "data", "sample_candidates.csv")
    generate_csv_data(csv_path)
    
    # Import SQLAlchemy stuff
    from app.database import SessionLocal, Base, engine
    from app.models import Job, Candidate, Ranking
    from app.vector_db import vector_db
    
    # Re-create tables
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # 1. Seed Job Descriptions
        jobs_data = [
            {
                "job_id": "JD001",
                "title": "Senior ML Engineer",
                "description": "We are seeking a Senior Machine Learning Engineer to design, train, and productionize scalable deep learning and NLP models. The role involves setting up MLOps pipelines on AWS, developing API integration with FastAPI, and working with PyTorch/TensorFlow models.",
                "required_skills": json.dumps(["Python", "Machine Learning", "PyTorch", "Docker"]),
                "preferred_skills": json.dumps(["FastAPI", "Kubernetes", "AWS", "MLOps"]),
                "soft_skills": json.dumps(["Problem Solving", "Leadership"]),
                "min_exp_years": 5,
                "preferred_exp_years": 8,
                "seniority_level": "Senior",
                "industry_domain": "AI/ML"
            },
            {
                "job_id": "JD002",
                "title": "Full Stack Developer",
                "description": "Looking for a Full Stack Developer experienced in modern Javascript ecosystems. You will own front-end features in React/NextJS and back-end REST APIs in Node.js/PostgreSQL. Docker knowledge and cloud experience are major pluses.",
                "required_skills": json.dumps(["React", "TypeScript", "Node.js", "PostgreSQL"]),
                "preferred_skills": json.dumps(["Next.js", "Docker", "AWS", "TailwindCSS"]),
                "soft_skills": json.dumps(["Collaboration", "Agile"]),
                "min_exp_years": 3,
                "preferred_exp_years": 6,
                "seniority_level": "Mid",
                "industry_domain": "SaaS"
            }
        ]
        
        for jd in jobs_data:
            job_obj = Job(**jd)
            db.add(job_obj)
            
        logger.info("Seeded job descriptions.")
        
        # 2. Seed Candidates
        with open(csv_path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                skills = json.loads(row["skills"])
                edu = json.loads(row["education"])
                certs = json.loads(row["certifications"])
                projs = json.loads(row["projects"])
                signals = json.loads(row["activity_signals"])
                
                cand = Candidate(
                    candidate_id=row["candidate_id"],
                    name=row["name"],
                    email=row["email"],
                    current_title=row["current_title"],
                    current_company=row["current_company"],
                    total_exp_years=float(row["total_exp_years"]),
                    skills=row["skills"],
                    education=row["education"],
                    certifications=row["certifications"],
                    projects=row["projects"],
                    industry_experience=row["industry_experience"],
                    activity_signals=row["activity_signals"],
                    career_growth_score=float(row["career_growth_score"]),
                    engagement_score=float(row["engagement_score"]),
                    location=row["location"],
                    expected_ctc_lpa=float(row["expected_ctc_lpa"])
                )
                db.add(cand)
                
                # Seed into Vector DB
                profile_text = (
                    f"{cand.current_title} at {cand.current_company}. "
                    f"Skills: {', '.join(skills)}. "
                    f"Experience: {cand.total_exp_years} years. "
                    f"Education: {row['education']}"
                )
                vector_db.add_candidate(cand.candidate_id, profile_text, {"name": cand.name})
                count += 1
                
        db.commit()
        logger.info(f"Seeded {count} candidates into DB & Vector DB.")
        
    except Exception as e:
        logger.error(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
