import pytest

from human_exe.workforce.services.workforce_privacy_guard import enforce_aggregate_mode, validate_recommendation_text


def test_privacy_guard_removes_identity_and_protected_fields() -> None:
    records = [
        {
            "employee_id": "E1",
            "employee_name": "Jane Doe",
            "role": "Analyst",
            "race": "redacted",
            "task_volume": 120,
        }
    ]
    sanitized = enforce_aggregate_mode(records, hr_analytics_mode=False)
    assert "employee_id" not in sanitized[0]
    assert "employee_name" not in sanitized[0]
    assert "race" not in sanitized[0]
    assert sanitized[0]["role"] == "Analyst"


def test_privacy_guard_blocks_adverse_action_language() -> None:
    with pytest.raises(ValueError):
        validate_recommendation_text("We should terminate this role immediately.")
