import pytest
from app.agents.framework import AgentState, LLMProviderFactory
from app.agents.implementations import (
    ExecutiveAgent, CareerCoachAgent, ResumeAgent, SkillGapAgent, JobDiscoveryAgent
)

def test_llm_provider_factory():
    res = LLMProviderFactory.generate_response("test prompt", provider="openai")
    assert res is not None

def test_executive_agent_orchestration():
    state = AgentState("TEST-USER")
    agent = ExecutiveAgent()
    res = agent.orchestrate_user_onboarding(state, {"name": "Test User"})
    assert res["orchestration_status"] == "Completed"

def test_resume_agent():
    state = AgentState("TEST-USER")
    agent = ResumeAgent()
    res = agent.analyze_and_rewrite(state, "Python engineer with 5 years experience.")
    assert "ats_score" in res or "strengths" in res
