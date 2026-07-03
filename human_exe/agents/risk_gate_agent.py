"""Risk gate agent evaluates action risk and approval requirements."""

from __future__ import annotations

from human_exe.models.workflow import RiskAssessment
from human_exe.policy.approval_rules import evaluate_action_policy


class RiskGateAgent:
    def assess(self, action, risk_score: float, threshold: float) -> RiskAssessment:
        rule = evaluate_action_policy(action, risk_score, threshold)
        return RiskAssessment(
            score=risk_score,
            requires_approval=rule.requires_approval,
            reasons=[rule.reason],
        )
