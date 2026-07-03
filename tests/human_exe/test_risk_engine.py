from human_exe.policy.risk_engine import AllocationInputs, compute_ai_share, compute_risk_score


def test_ai_share_is_clamped() -> None:
    inputs = AllocationInputs(
        repeatability=1.0,
        task_maturity=1.0,
        historical_success_rate=1.0,
        action_reversibility=1.0,
        data_sensitivity=0.0,
        business_risk=0.0,
        human_approval_requirement=0.0,
        observed_ui_stability=1.0,
        recovery_reliability=1.0,
    )
    assert 0.20 <= compute_ai_share(inputs) <= 0.50


def test_risk_score_increases_with_sensitivity() -> None:
    low = AllocationInputs(0.9, 0.9, 0.9, 0.9, 0.1, 0.1, 0.1, 0.9, 0.9)
    high = AllocationInputs(0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9)
    assert compute_risk_score(high) > compute_risk_score(low)
