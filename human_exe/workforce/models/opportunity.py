"""AI opportunity and classification models."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class AIOpportunity:
    opportunity_id: str
    task_id: str
    workflow_id: str
    recommended_ai_mode: str
    value_score: float
    repeatability_score: float
    data_availability_score: float
    workflow_stability_score: float
    verification_score: float
    risk_score: float
    reversibility_score: float
    human_supervision_score: float
    integration_feasibility_score: float
    employee_acceptance_score: float
    overall_ai_fit_score: float
    expected_automation_range: str
    human_supervision_level: str
    implementation_complexity: str
    recommended_phase: str
    evidence: str
