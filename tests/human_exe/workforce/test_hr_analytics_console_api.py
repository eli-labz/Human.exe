import pytest

from human_exe.workforce.services.hr_analytics_approval import request_hr_analytics_approval_via_console_api


def test_hr_analytics_console_api_approval_success() -> None:
    state = {"request_id": "REQ-1", "status": "PENDING"}

    def fake_post(url: str, token: str, payload: dict[str, object]) -> dict[str, object]:
        assert url.endswith("/api/requests")
        assert token == "token-1"
        assert payload["workflow_id"] == "workforce-hr-analytics"
        return {"request": {"request_id": state["request_id"], "status": state["status"]}}

    def fake_get(url: str, token: str) -> dict[str, object]:
        assert url.endswith("/api/queue")
        assert token == "token-1"
        state["status"] = "APPROVE"
        return {"items": [{"request_id": state["request_id"], "status": state["status"]}]}

    status = request_hr_analytics_approval_via_console_api(
        console_base_url="http://localhost:8765",
        token="token-1",
        requested_by="tester",
        purpose="Enable hr analytics",
        timeout_seconds=2,
        poll_interval_seconds=1,
        post_fn=fake_post,
        get_fn=fake_get,
    )

    assert status == "APPROVE"


def test_hr_analytics_console_api_rejection() -> None:
    def fake_post(url: str, token: str, payload: dict[str, object]) -> dict[str, object]:
        return {"request": {"request_id": "REQ-2", "status": "PENDING"}}

    def fake_get(url: str, token: str) -> dict[str, object]:
        return {"items": [{"request_id": "REQ-2", "status": "REJECT"}]}

    with pytest.raises(PermissionError):
        request_hr_analytics_approval_via_console_api(
            console_base_url="http://localhost:8765",
            token="token-1",
            requested_by="tester",
            purpose="Enable hr analytics",
            timeout_seconds=1,
            poll_interval_seconds=1,
            post_fn=fake_post,
            get_fn=fake_get,
        )
