from human_exe.models.tokens import ActionType, HumanActionToken, IntentToken, OutcomeToken, PerceptionToken


def test_token_models_roundtrip_fields() -> None:
    intent = IntentToken(task_id="w1", objective="obj", business_goal="goal", created_by="user")
    perception = PerceptionToken(task_id="w1", source="obs", state={"a": 1})
    action = HumanActionToken(task_id="w1", action_type=ActionType.CLICK, parameters={"selector": "#x"}, actor="agent")
    outcome = OutcomeToken(task_id="w1", action_token_id=action.token_id, success=True, verification_passed=True, result={"status": "ok"})
    assert intent.task_id == "w1"
    assert perception.state["a"] == 1
    assert outcome.action_token_id == action.token_id
