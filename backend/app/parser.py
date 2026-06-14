import json
import re
import logging
from typing import Dict, Any, List
from app.config import settings

logger = logging.getLogger(__name__)

# Predefined dictionary for fallback parser
TECH_SKILLS = [
    "python", "java", "javascript", "typescript", "go", "rust", "c++", "c#", "scala", "kotlin",
    "react", "angular", "vue", "node", "django", "fastapi", "flask", "spring",
    "machine learning", "deep learning", "nlp", "computer vision", "tensorflow", "pytorch",
    "scikit-learn", "keras", "xgboost", "lightgbm", "hugging face", "langchain",
    "sql", "postgresql", "mysql", "mongodb", "redis", "cassandra", "elasticsearch",
    "aws", "gcp", "azure", "docker", "kubernetes", "terraform", "ci/cd", "jenkins",
    "data engineering", "spark", "kafka", "airflow", "dbt", "pandas", "numpy"
]

SOFT_SKILLS = [
    "communication", "leadership", "collaboration", "agile", "scrum", "problem solving",
    "analytical", "teamwork", "mentoring", "critical thinking", "creativity"
]

INDUSTRIES = [
    "healthcare", "finance", "fintech", "ecommerce", "saas", "gaming", "automotive",
    "telecommunications", "cybersecurity", "ai/ml", "education", "retail"
]

def parse_job_description_rule_based(text: str) -> Dict[str, Any]:
    text_lower = text.lower()
    
    # 1. Extract experience
    min_exp = 0
    pref_exp = 0
    exp_matches = re.findall(r"(\d+)\+?\s*(?:-\s*(\d+)\+?\s*)?years?", text_lower)
    if exp_matches:
        try:
            # Take the first match
            first_match = exp_matches[0]
            min_exp = int(first_match[0])
            if first_match[1]:
                pref_exp = int(first_match[1])
            else:
                pref_exp = min_exp + 2
        except Exception:
            pass
            
    # 2. Extract required & preferred skills
    matched_skills = []
    for skill in TECH_SKILLS:
        # Match word boundaries to prevent matching subsets (e.g. "go" inside "good")
        if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
            matched_skills.append(skill.title())
            
    # Split required vs preferred simply (first 65% required, rest preferred)
    split_idx = int(len(matched_skills) * 0.65)
    req_skills = matched_skills[:split_idx] if matched_skills else ["Python", "SQL"]
    pref_skills = matched_skills[split_idx:] if matched_skills else ["AWS"]
    
    # 3. Extract seniority
    seniority = "Mid"
    if "senior" in text_lower or "sr." in text_lower or "lead" in text_lower:
        seniority = "Senior"
    elif "junior" in text_lower or "jr." in text_lower or "entry" in text_lower:
        seniority = "Junior"
    elif "staff" in text_lower or "principal" in text_lower:
        seniority = "Staff"
        
    # 4. Extract domain
    domain = "General Technology"
    for ind in INDUSTRIES:
        if ind in text_lower:
            domain = ind.title()
            break
            
    # 5. Extract soft skills
    matched_soft = []
    for soft in SOFT_SKILLS:
        if soft in text_lower:
            matched_soft.append(soft.title())
    if not matched_soft:
        matched_soft = ["Collaboration", "Problem Solving"]
        
    return {
        "title": "Parsed Position",
        "required_skills": req_skills,
        "preferred_skills": pref_skills,
        "soft_skills": matched_soft,
        "min_exp_years": min_exp or 2,
        "preferred_exp_years": pref_exp or 5,
        "seniority_level": seniority,
        "industry_domain": domain
    }

def parse_job_description(text: str) -> Dict[str, Any]:
    # Check if we have OpenAI or Gemini key and langchain is available
    has_key = settings.OPENAI_API_KEY or settings.GEMINI_API_KEY
    
    if has_key:
        try:
            # Implement simple LangChain parsing if keys are set
            from langchain_core.prompts import ChatPromptTemplate
            from langchain_core.output_parsers import JsonOutputParser
            
            parser = JsonOutputParser()
            
            prompt = ChatPromptTemplate.from_template(
                "You are an expert technical recruiter parser.\n"
                "Extract structured requirements from this job description: {text}\n"
                "Your response must be a valid JSON object matching this schema:\n"
                "{{\n"
                "  \"title\": \"job title\",\n"
                "  \"required_skills\": [\"skill1\", \"skill2\"],\n"
                "  \"preferred_skills\": [\"skill1\"],\n"
                "  \"soft_skills\": [\"skill1\"],\n"
                "  \"min_exp_years\": 5,\n"
                "  \"preferred_exp_years\": 8,\n"
                "  \"seniority_level\": \"Senior\",\n"
                "  \"industry_domain\": \"Healthcare\"\n"
                "}}\n"
                "Return ONLY the raw JSON block without formatting, markdown tags, or additional text."
            )
            
            # Simple model choosing
            if settings.OPENAI_API_KEY:
                from langchain_openai import ChatOpenAI
                model = ChatOpenAI(openai_api_key=settings.OPENAI_API_KEY, temperature=0)
            else:
                from langchain_google_genai import ChatGoogleGenerativeAI
                model = ChatGoogleGenerativeAI(google_api_key=settings.GEMINI_API_KEY, model="gemini-pro", temperature=0)
                
            chain = prompt | model | parser
            parsed = chain.invoke({"text": text})
            logger.info("Successfully parsed job description using LangChain LLM")
            return parsed
        except Exception as e:
            logger.error(f"LangChain parsing failed ({e}). Falling back to rule-based parser.")
            
    return parse_job_description_rule_based(text)
