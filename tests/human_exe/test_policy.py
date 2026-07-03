from human_exe.models.tokens import ActionType, HumanActionToken
from human_exe.policy.approval_rules import evaluate_action_policy


def test_forbidden_action_requires_approval_and_is_blocked() -> None:
    token = HumanActionToken(
        task_id="t1",
        action_type=ActionType.ABORT_TASK,
        parameters={},
        actor="agent",
    )
    result = evaluate_action_policy(token, risk_score=0.1, threshold=0.65)
    assert result.allowed is False
    assert result.requires_approval is True


def test_high_risk_action_requires_approval() -> None:
    token = HumanActionToken(
        task_id="t2",
        action_type=ActionType.CLICK,
        parameters={"selector": "#submit"},
        actor="agent",
    )
    result = evaluate_action_policy(token, risk_score=0.9, threshold=0.65)
    assert result.allowed is True
    assert result.requires_approval is True
