import json
import logging
from typing import Dict, List, Any
from app.schemas import CandidateRankingOut, ExplainableAI, RankingWeights

logger = logging.getLogger(__name__)

def calculate_skills_score(candidate_skills: List[str], req_skills: List[str], pref_skills: List[str]) -> float:
    if not req_skills and not pref_skills:
        return 0.8
    
    cand_set = set(s.strip().lower() for s in candidate_skills)
    req_set = set(s.strip().lower() for s in req_skills)
    pref_set = set(s.strip().lower() for s in pref_skills)
    
    req_weight = 1.0
    pref_weight = 0.4
    
    total_weight = (len(req_set) * req_weight) + (len(pref_set) * pref_weight)
    if total_weight == 0:
        return 0.8
        
    matched_req = len(cand_set & req_set) * req_weight
    matched_pref = len(cand_set & pref_set) * pref_weight
    
    score = (matched_req + matched_pref) / total_weight
    return min(1.0, max(0.0, score))

def calculate_experience_score(exp: float, min_exp: int, pref_exp: int) -> float:
    if exp < min_exp:
        if min_exp == 0:
            return 1.0
        return max(0.1, (exp / min_exp) * 0.6)
    elif exp <= pref_exp:
        # Linear scaling from 0.6 to 1.0
        if pref_exp == min_exp:
            return 1.0
        return 0.6 + 0.4 * (exp - min_exp) / (pref_exp - min_exp)
    else:
        # Slight decay for overqualification
        over_years = exp - pref_exp
        decay = over_years * 0.02
        return max(0.7, 1.0 - decay)

def calculate_industry_score(candidate_industries: List[str], job_domain: str) -> float:
    if not job_domain:
        return 0.8
    
    job_dom = job_domain.strip().lower()
    cand_ind = [ind.strip().lower() for ind in candidate_industries]
    
    if job_dom in cand_ind:
        return 1.0
        
    for ind in cand_ind:
        if job_dom in ind or ind in job_dom:
            return 0.7
        # Prefix match of words to handle cases like "Health Tech" vs "Healthcare"
        for w1 in ind.split():
            for w2 in job_dom.split():
                if len(w1) >= 4 and len(w2) >= 4:
                    if w1.startswith(w2[:4]) or w2.startswith(w1[:4]):
                        return 0.7
            
    return 0.2

def calculate_activity_score(activity_signals: Dict[str, Any], base_engagement: float) -> float:
    # Blend base engagement score with structured signals
    certs = int(activity_signals.get("recent_certifications", 0))
    projects = int(activity_signals.get("recent_projects", 0))
    commits = int(activity_signals.get("github_commits", 0))
    prs = int(activity_signals.get("open_source_prs", 0))
    
    cert_score = min(certs / 3.0, 1.0)
    proj_score = min(projects / 3.0, 1.0)
    commit_score = min(commits / 150.0, 1.0)
    pr_score = min(prs / 5.0, 1.0)
    
    signals_average = (cert_score + proj_score + commit_score + pr_score) / 4.0
    
    # 50% base score, 50% calculated from signals
    score = (base_engagement * 0.5) + (signals_average * 0.5)
    return min(1.0, max(0.0, score))

def generate_xai_feedback(
    name: str,
    title: str,
    exp: float,
    scores: Dict[str, float],
    cand_skills: List[str],
    req_skills: List[str],
    pref_skills: List[str],
    job_domain: str
) -> ExplainableAI:
    strengths = []
    weaknesses = []
    
    # Analyze Semantic Match
    if scores["semantic"] >= 0.80:
        strengths.append(f"Strong overall semantic alignment with the {title} profile description.")
    elif scores["semantic"] < 0.60:
        weaknesses.append("Semantic profile matching is moderate; work history context differs slightly.")
        
    # Analyze Skills Match
    cand_skills_lower = [s.lower() for s in cand_skills]
    matched_req = [s for s in req_skills if s.lower() in cand_skills_lower]
    missing_req = [s for s in req_skills if s.lower() not in cand_skills_lower]
    
    if len(matched_req) == len(req_skills) and req_skills:
        strengths.append("Possesses 100% of the strictly required technical core skills.")
    elif matched_req:
        strengths.append(f"Matches key required technical skills, including: {', '.join(matched_req[:3])}.")
        
    if missing_req:
        weaknesses.append(f"Lacks match for required skills: {', '.join(missing_req[:3])}.")
        
    # Analyze Experience Match
    if scores["experience"] >= 0.90:
        strengths.append(f"Ideal tenure profile with {exp} years of relevant experience.")
    elif scores["experience"] < 0.60:
        weaknesses.append(f"Experience level ({exp} years) is below the preferred minimum.")
        
    # Analyze Activity & Growth Match
    if scores["activity"] >= 0.80:
        strengths.append("High developer/community activity score, demonstrating continuous skill building.")
    if scores["growth"] >= 0.80:
        strengths.append("Strong career trajectory showing progressive ownership and promotion history.")
    elif scores["growth"] < 0.50:
        weaknesses.append("Career growth trajectory is relatively flat; limited leadership or promotion signals.")
        
    # Recommendation logic
    overall = scores["composite"]
    if overall >= 0.85:
        recommendation = "Highly Recommended"
        summary = f"{name} is an elite fit for this role, showing exceptional skills match and active industry engagement."
    elif overall >= 0.70:
        recommendation = "Recommended"
        summary = f"{name} is a solid candidate meeting most requirements with clear potential to perform well."
    elif overall >= 0.50:
        recommendation = "Consider with Reservations"
        summary = f"{name} is a potential match but has noticeable gaps in either experience tenure or critical skills."
    else:
        recommendation = "Not Recommended"
        summary = f"{name} is not a suitable fit due to significant skills and experience misalignment."
        
    if not strengths:
        strengths.append("Meets baseline criteria for candidate sourcing.")
    if not weaknesses:
        weaknesses.append("No critical gaps identified compared to core requirement parameters.")
        
    return ExplainableAI(
        strengths=strengths[:3],
        weaknesses=weaknesses[:3],
        recommendation=recommendation,
        summary=summary
    )

def score_candidate(
    candidate: Dict[str, Any],
    job: Dict[str, Any],
    semantic_score: float,
    weights: RankingWeights
) -> Dict[str, Any]:
    # Parse candidate lists
    skills = candidate.get("skills", [])
    industries = candidate.get("industry_experience", [])
    activity_signals = candidate.get("activity_signals", {})
    
    # Parse job lists
    req_skills = job.get("required_skills", [])
    pref_skills = job.get("preferred_skills", [])
    job_domain = job.get("industry_domain", "")
    
    # Individual Scores
    skills_score = calculate_skills_score(skills, req_skills, pref_skills)
    exp_score = calculate_experience_score(
        float(candidate.get("total_exp_years", 0)),
        int(job.get("min_exp_years", 0)),
        int(job.get("preferred_exp_years", 5))
    )
    ind_score = calculate_industry_score(industries, job_domain)
    act_score = calculate_activity_score(activity_signals, float(candidate.get("engagement_score", 0.5)))
    growth_score = float(candidate.get("career_growth_score", 0.5))
    
    # Weights configuration
    w = weights
    composite = (
        w.semantic_match * semantic_score +
        w.experience_match * exp_score +
        w.skill_match * skills_score +
        w.industry_match * ind_score +
        w.activity_score * act_score +
        w.career_growth_score * growth_score
    )
    
    scores = {
        "semantic": semantic_score,
        "experience": exp_score,
        "skills": skills_score,
        "industry": ind_score,
        "activity": act_score,
        "growth": growth_score,
        "composite": composite
    }
    
    xai = generate_xai_feedback(
        name=candidate["name"],
        title=job["title"],
        exp=float(candidate.get("total_exp_years", 0)),
        scores=scores,
        cand_skills=skills,
        req_skills=req_skills,
        pref_skills=pref_skills,
        job_domain=job_domain
    )
    
    return {
        "candidate_id": candidate["candidate_id"],
        "name": candidate["name"],
        "email": candidate["email"],
        "current_title": candidate.get("current_title"),
        "current_company": candidate.get("current_company"),
        "total_exp_years": float(candidate.get("total_exp_years", 0)),
        "skills": skills,
        "location": candidate.get("location"),
        "composite_score": round(composite, 4),
        "semantic_fit_score": round(semantic_score, 4),
        "experience_score": round(exp_score, 4),
        "skills_score": round(skills_score, 4),
        "industry_score": round(ind_score, 4),
        "activity_score": round(act_score, 4),
        "growth_score": round(growth_score, 4),
        "xai": xai
    }
