from human_exe.tools.verification_tools import verify_action_result, verify_non_empty_text


def test_verify_non_empty_text() -> None:
    assert verify_non_empty_text("hello")["passed"] is True
    assert verify_non_empty_text("   ")["passed"] is False


def test_verify_action_result() -> None:
    assert verify_action_result({"status": "ok"})["passed"] is True
    assert verify_action_result({})["passed"] is False
