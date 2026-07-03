"""AI opportunity scoring and recommendation engine."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4

from human_exe.workforce.models.opportunity import AIOpportunity
from human_exe.workforce.models.workflow import TaskProfile, WorkflowProfile


@dataclass(slots=True)
class OpportunityScoreInputs:
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


WEIGHTS = {
    "value_score": 0.15,
    "repeatability_score": 0.15,
    "data_availability_score": 0.10,
    "workflow_stability_score": 0.10,
    "verification_score": 0.10,
    "risk_score": -0.12,
    "reversibility_score": 0.10,
    "human_supervision_score": 0.08,
    "integration_feasibility_score": 0.06,
    "employee_acceptance_score": 0.08,
}


def _clamp(value: float, lower: float = 0.0, upper: float = 1.0) -> float:
    return max(lower, min(upper, value))


def overall_ai_fit_score(inputs: OpportunityScoreInputs) -> float:
    score = 0.0
    for field, weight in WEIGHTS.items():
        score += getattr(inputs, field) * weight
    return round(_clamp(score), 4)


def _recommended_mode(task: TaskProfile, score: float, risk_score: float) -> str:
    if task.requires_human_judgment and score < 0.55:
        return "Human-only judgment task"
    if risk_score > 0.65 and task.requires_human_judgment:
        return "Not recommended for AI"
    if score >= 0.78 and risk_score <= 0.45 and not task.requires_human_judgment:
        return "Supervised AI Agent task"
    if score >= 0.65 and task.requires_human_judgment:
        return "AI-copilot task"
    if score >= 0.58:
        return "AI-assisted knowledge task"
    if score >= 0.5 and not task.requires_human_judgment:
        return "RPA or deterministic automation task"
    return "Not recommended for AI"


def _supervision_level(mode: str) -> str:
    if mode == "Supervised AI Agent task":
        return "High"
    if mode in {"AI-copilot task", "AI-assisted knowledge task"}:
        return "Medium"
    return "Low"


def _complexity(score: float, integration: float, data_readiness: float) -> str:
    if score > 0.75 and integration > 0.7 and data_readiness > 0.7:
        return "Moderate"
    if score > 0.6:
        return "Medium"
    return "High"


def _phase(score: float, risk: float) -> str:
    if score > 0.75 and risk < 0.45:
        return "Phase 3: Pilot selection and proof of value"
    if score > 0.6:
        return "Phase 4: Supervised AI Agent buildout"
    return "Phase 2: AI literacy and workflow redesign"


def score_ai_opportunity(task: TaskProfile, workflow: WorkflowProfile, inputs: OpportunityScoreInputs) -> AIOpportunity:
    fit = overall_ai_fit_score(inputs)
    mode = _recommended_mode(task, fit, inputs.risk_score)
    automation_low = int(max(5, fit * 40))
    automation_high = int(min(65, automation_low + 20))
    return AIOpportunity(
        opportunity_id=str(uuid4()),
        task_id=task.task_id,
        workflow_id=workflow.workflow_id,
        recommended_ai_mode=mode,
        value_score=inputs.value_score,
        repeatability_score=inputs.repeatability_score,
        data_availability_score=inputs.data_availability_score,
        workflow_stability_score=inputs.workflow_stability_score,
        verification_score=inputs.verification_score,
        risk_score=inputs.risk_score,
        reversibility_score=inputs.reversibility_score,
        human_supervision_score=inputs.human_supervision_score,
        integration_feasibility_score=inputs.integration_feasibility_score,
        employee_acceptance_score=inputs.employee_acceptance_score,
        overall_ai_fit_score=fit,
        expected_automation_range=f"{automation_low}% - {automation_high}%",
        human_supervision_level=_supervision_level(mode),
        implementation_complexity=_complexity(fit, inputs.integration_feasibility_score, inputs.data_availability_score),
        recommended_phase=_phase(fit, inputs.risk_score),
        evidence=f"Task {task.name} in workflow {workflow.name} scored {fit}",
    )
