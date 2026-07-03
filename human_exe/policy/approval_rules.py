"""Approval rules and policy checks."""

from __future__ import annotations

from dataclasses import dataclass

from human_exe.models.tokens import ActionType, HumanActionToken


@dataclass(slots=True)
class ApprovalRuleResult:
    allowed: bool
    requires_approval: bool
    reason: str


APPROVAL_REQUIRED_ACTIONS: set[ActionType] = {
    ActionType.SEND_DRAFT_FOR_APPROVAL,
    ActionType.DOWNLOAD_FILE,
    ActionType.UPLOAD_FILE,
    ActionType.OPEN_APP,
    ActionType.CLOSE_APP,
}

FORBIDDEN_AGENT_ACTIONS: set[ActionType] = {
    ActionType.ABORT_TASK,
}


def evaluate_action_policy(action: HumanActionToken, risk_score: float, threshold: float) -> ApprovalRuleResult:
    if action.action_type in FORBIDDEN_AGENT_ACTIONS:
        return ApprovalRuleResult(
            allowed=False,
            requires_approval=True,
            reason=f"Action {action.action_type.value} is forbidden for autonomous execution.",
        )
    if action.action_type in APPROVAL_REQUIRED_ACTIONS:
        return ApprovalRuleResult(
            allowed=True,
            requires_approval=True,
            reason=f"Action {action.action_type.value} requires supervisor approval.",
        )
    if risk_score >= threshold:
        return ApprovalRuleResult(
            allowed=True,
            requires_approval=True,
            reason=f"Risk score {risk_score:.2f} exceeds threshold {threshold:.2f}.",
        )
    return ApprovalRuleResult(allowed=True, requires_approval=False, reason="Action is allowed.")
