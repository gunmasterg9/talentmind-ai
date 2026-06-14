# TalentMind AI — Hackathon Submission Presentation Guide

Use the slide outlines below to fill out your PPT/deck template before converting it to PDF for your submission.

---

## Slide 1: Project Title & Team Information
*   **Slide Title**: TalentMind AI: Intelligent Candidate Discovery and Ranking
*   **Subtitle**: Next-Generation Recruiter Matching Platform
*   **Content**:
    *   **Team Name / ID**: [Your Team Name / ID]
    *   **Submission Date**: June 14, 2026
    *   **Core Objective**: Build a robust, scalable Proof of Concept (PoC) that interprets job descriptions semantically and ranks candidates using multi-signal weighted algorithms.

---

## Slide 2: The Recruiting Challenge & Market Gaps
*   **Slide Title**: The Problem: Why Keyword Sourcing Fails
*   **Key Points**:
    *   **Shallow Keyword Filtering**: Standard applicant systems search for exact words (e.g., matching "NLP" but ignoring a profile with "Transformers" or "Language Models").
    *   **Ignoring Key Quality Signals**: Resumes list work history, but platforms miss behavioral data, recent commits, hackathon wins, and certification recency.
    *   **Rigid Recruiting Controls**: Recruiters cannot customize the scoring balance. They get a binary (Yes/No) list instead of an interactive, weighted match.

---

## Slide 3: Our Approach (TalentMind AI Solution)
*   **Slide Title**: The Solution: Multi-Signal Sourcing Engine
*   **Key Points**:
    *   **Semantic Matching Layer**: Sentence Transformers (`BAAI/bge-large-en-v1.5`) map job descriptions to candidate experience profiles in a vector space.
    *   **Data Enrichment & Activity Integration**: Normalizes profile attributes, years of experience, and behavioral metrics from developer ecosystems (e.g., LeetCode, GitHub, Kaggle).
    *   **Explainable AI (XAI)**: Generates human-readable recruiter summaries, highlighting matching strengths, weaknesses, and clear hiring recommendations.

---

## Slide 4: Technical Architecture & System Flow
*   **Slide Title**: Architecture Overview
*   **Key Points**:
    *   **Frontend**: Next.js 15, TypeScript, TailwindCSS, Shadcn UI.
    *   **Backend**: FastAPI (Python) for fast, concurrent REST endpoints.
    *   **Vector DB**: ChromaDB for storing and retrieving high-dimensional candidate embeddings.
    *   **Database**: PostgreSQL (with automatic SQLite fallback for simple offline local evaluation).
    *   **Deployment**: Docker Compose orchestration for multi-container configurations.

---

## Slide 5: The Intelligent Ranking Formula
*   **Slide Title**: Core Scoring Methodology
*   **Formula**:
    $$\text{Final Score} = 0.35 \cdot S_{semantic} + 0.20 \cdot S_{experience} + 0.15 \cdot S_{skill} + 0.10 \cdot S_{industry} + 0.10 \cdot S_{activity} + 0.10 \cdot S_{growth}$$
*   **Signal Descriptions**:
    1.  **Semantic Match (35%)**: Cosine similarity between job description text and candidate profiles.
    2.  **Experience Match (20%)**: Grades candidate's tenure against minimum and preferred job range with penalties for under-qualification.
    3.  **Skill Match (15%)**: Weighted Jaccard index based on required and preferred skill overlap.
    4.  **Industry Match (10%)**: Prefix-matched word similarity on candidate's industry history.
    5.  **Activity Score (10%)**: Normalized metric of commits, certifications, open-source PRs, and learning hours.
    6.  **Career Growth Score (10%)**: Trajectory evaluation using company tiers and title promotions.

---

## Slide 6: Business Impact & Recruiter Benefits
*   **Slide Title**: Why Recruiter's Choose TalentMind AI
*   **Key Points**:
    *   **Explainable Matching**: Demystifies black-box ML matching by detailing specific reasons (e.g., "Matches core PyTorch requirements but lacks MLOps").
    *   **Dynamic Weight Controls**: Recruiter can adjust sliders (e.g., value activity higher for startup roles, or tenure higher for staff positions).
    *   **Lightning-Fast Shortlist**: Delivers ranked lists in under 10ms. Instant PDF, CSV, and Excel reports.
