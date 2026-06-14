import sys
import os
import pytest

# Add backend app to python load path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "backend"))

from app.scorer import (
    calculate_skills_score, 
    calculate_experience_score, 
    calculate_industry_score,
    score_candidate
)
from app.schemas import RankingWeights

def test_skills_scoring():
    # Perfect match
    cand_skills = ["Python", "PyTorch", "Docker"]
    req = ["Python", "PyTorch"]
    pref = ["Docker"]
    score = calculate_skills_score(cand_skills, req, pref)
    assert score == 1.0

    # Half match
    cand_skills = ["Python"]
    req = ["Python", "Go"]
    pref = []
    score = calculate_skills_score(cand_skills, req, pref)
    assert pytest.approx(score, 0.01) == 0.5

    # Zero match
    cand_skills = ["React"]
    req = ["Python"]
    pref = []
    score = calculate_skills_score(cand_skills, req, pref)
    assert score == 0.0

def test_experience_scoring():
    # Ideal experience
    score = calculate_experience_score(6, min_exp=5, pref_exp=8)
    assert score >= 0.70 and score <= 0.80

    # Underqualified experience
    score = calculate_experience_score(2, min_exp=5, pref_exp=8)
    assert score < 0.60

    # Overqualified experience decay
    score = calculate_experience_score(15, min_exp=5, pref_exp=8)
    assert score < 1.0

def test_industry_scoring():
    # Exact match
    score = calculate_industry_score(["Finance", "Healthcare"], "Finance")
    assert score == 1.0

    # Substring match
    score = calculate_industry_score(["Health Tech"], "Healthcare")
    assert score == 0.7

    # No match
    score = calculate_industry_score(["Gaming"], "Finance")
    assert score == 0.2
