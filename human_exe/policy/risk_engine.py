"""Risk scoring and AI labor allocation engine."""

from __future__ import annotations

from dataclasses import dataclass


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


@dataclass(slots=True)
class AllocationInputs:
    repeatability: float
    task_maturity: float
    historical_success_rate: float
    action_reversibility: float
    data_sensitivity: float
    business_risk: float
    human_approval_requirement: float
    observed_ui_stability: float
    recovery_reliability: float


def compute_risk_score(inputs: AllocationInputs) -> float:
    positive = (
        inputs.repeatability
        + inputs.task_maturity
        + inputs.historical_success_rate
        + inputs.action_reversibility
        + inputs.observed_ui_stability
        + inputs.recovery_reliability
    ) / 6.0

    negative = (
        inputs.data_sensitivity + inputs.business_risk + inputs.human_approval_requirement
    ) / 3.0
    return clamp((negative * 0.65) + ((1 - positive) * 0.35), 0.0, 1.0)


def compute_ai_share(inputs: AllocationInputs) -> float:
    positive = (
        inputs.repeatability
        + inputs.task_maturity
        + inputs.historical_success_rate
        + inputs.action_reversibility
        + inputs.observed_ui_stability
        + inputs.recovery_reliability
    ) / 6.0
    negative = (
        inputs.data_sensitivity + inputs.business_risk + inputs.human_approval_requirement
    ) / 3.0
    base_score = 0.2 + (positive * 0.3) - (negative * 0.2)
    return clamp(base_score, 0.20, 0.50)
