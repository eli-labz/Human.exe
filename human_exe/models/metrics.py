"""Reliability and supervision quality metrics."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ReliabilityMetrics:
    task_completion_rate: float = 0.0
    action_success_rate: float = 0.0
    verification_success_rate: float = 0.0
    recovery_rate: float = 0.0
    escalation_rate: float = 0.0
    policy_violation_rate: float = 0.0
    human_override_rate: float = 0.0
    time_to_useful_result: float = 0.0
    approval_latency: float = 0.0
    repeated_failure_count: int = 0


@dataclass(slots=True)
class CognitiveDebtIndex:
    review_depth: float = 0.0
    override_frequency: float = 0.0
    approval_speed: float = 0.0
    escalation_quality: float = 0.0
    ability_to_complete_without_agent: float = 0.0
    strategic_engagement: float = 0.0

    def likely_rubber_stamp(self) -> bool:
        return (
            self.approval_speed > 0.85
            and self.override_frequency < 0.1
            and self.review_depth < 0.3
        )
