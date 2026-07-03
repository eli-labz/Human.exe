from pathlib import Path

from human_exe.agents.supervisor_interface_agent import HumanSupervisionLayer
from human_exe.supervisor_console.server import ConsoleAuth
from human_exe.supervisor_console.server import SupervisorConsoleService


def test_supervisor_console_queue_and_decision(tmp_path: Path) -> None:
    supervision = HumanSupervisionLayer(tmp_path / "audit" / "audit.jsonl")
    service = SupervisorConsoleService(supervision=supervision, traces_dir=tmp_path / "traces")

    created = service.create_request(
        workflow_id="wf-console",
        action={"type": "SEND_DRAFT_FOR_APPROVAL", "parameters": {"recipient": "ops@example.com"}},
        risk_score=0.74,
        reason="Requires supervisor confirmation",
    )
    request_id = str(created["request"]["request_id"])

    queue = service.list_queue()
    assert queue["count"] == 1

    decision = service.submit_decision(
        request_id=request_id,
        supervisor_id="supervisor-test",
        decision_raw="APPROVE",
        reason="Looks good",
    )
    assert decision["decision"]["decision"] == "APPROVE"

    queue_after = service.list_queue()
    items = queue_after["items"]
    assert isinstance(items, list)
    assert items[0]["status"] == "APPROVE"

    events = service.list_events_since(0)
    event_types = [str(event["type"]) for event in events]
    assert "request_created" in event_types
    assert "decision_resolved" in event_types


def test_supervisor_console_modify_requires_modified_action(tmp_path: Path) -> None:
    supervision = HumanSupervisionLayer(tmp_path / "audit" / "audit.jsonl")
    service = SupervisorConsoleService(supervision=supervision, traces_dir=tmp_path / "traces")
    created = service.create_request(
        workflow_id="wf-modify",
        action={"type": "WRITE_FILE", "parameters": {"path": "a.txt", "content": "v1"}},
        risk_score=0.8,
        reason="Needs human change",
    )
    request_id = str(created["request"]["request_id"])

    try:
        service.submit_decision(
            request_id=request_id,
            supervisor_id="supervisor-test",
            decision_raw="MODIFY",
            reason="Adjust content",
            modified_action=None,
        )
        raised = False
    except ValueError:
        raised = True
    assert raised is True

    accepted = service.submit_decision(
        request_id=request_id,
        supervisor_id="supervisor-test",
        decision_raw="MODIFY",
        reason="Adjust content",
        modified_action={"type": "WRITE_FILE", "parameters": {"path": "a.txt", "content": "v2"}},
    )
    assert accepted["decision"]["decision"] == "MODIFY"


def test_console_auth_login_and_rbac(tmp_path: Path) -> None:
    users_file = tmp_path / "users.yaml"
    users_file.write_text(
        "users:\n"
        "  - username: sup\n"
        "    password: sup123\n"
        "    role: supervisor\n"
        "  - username: aud\n"
        "    password: aud123\n"
        "    role: auditor\n",
        encoding="utf-8",
    )

    auth = ConsoleAuth(users_file=users_file)
    supervisor = auth.login("sup", "sup123")
    auditor = auth.login("aud", "aud123")

    assert auth.authorize(str(supervisor["token"]), "decision.approve") is True
    assert auth.authorize(str(auditor["token"]), "decision.approve") is False
    assert auth.authorize(str(auditor["token"]), "audit.read") is True


def test_supervisor_console_service_trace_listing(tmp_path: Path) -> None:
    supervision = HumanSupervisionLayer(tmp_path / "audit" / "audit.jsonl")
    traces_dir = tmp_path / "traces"
    traces_dir.mkdir(parents=True, exist_ok=True)
    trace_file = traces_dir / "wf1.json"
    trace_file.write_text(
        '{"workflow_id":"wf1","final_status":"COMPLETED","trace_quality_score":0.9,'
        '"updated_at":"2026-07-02T00:00:00+00:00","intent":{"objective":"demo"}}',
        encoding="utf-8",
    )

    service = SupervisorConsoleService(supervision=supervision, traces_dir=traces_dir)
    traces = service.list_traces(limit=5)
    assert traces["count"] == 1
    assert traces["items"][0]["workflow_id"] == "wf1"
