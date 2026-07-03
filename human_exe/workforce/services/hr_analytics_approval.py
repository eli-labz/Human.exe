"""Supervisor-gated workflow for approved HR analytics mode."""

from __future__ import annotations

from dataclasses import asdict
import json
from typing import Any, Callable
from urllib import request as urllib_request

from human_exe.agents.supervisor_interface_agent import HumanSupervisionLayer
from human_exe.models.supervision import ApprovalRequest, DecisionType, SupervisorDecision


def request_hr_analytics_approval(
    supervision_layer: HumanSupervisionLayer,
    supervisor_id: str,
    requested_by: str,
    purpose: str,
    auto_approve: bool = False,
) -> SupervisorDecision:
    request = ApprovalRequest(
        workflow_id="workforce-hr-analytics",
        action={
            "type": "HR_ANALYTICS_MODE_REQUEST",
            "requested_by": requested_by,
            "purpose": purpose,
        },
        risk_score=0.74,
        reason="HR analytics mode requires explicit human supervisor approval and audit log.",
    )
    supervision_layer.enqueue(request)

    if not auto_approve:
        raise PermissionError("hr_analytics_approval_pending")

    decision = SupervisorDecision(
        request_id=request.request_id,
        supervisor_id=supervisor_id,
        decision=DecisionType.APPROVE,
        reason="Approved for governed HR analytics mode.",
        modified_action=asdict(request),
    )
    return supervision_layer.resolve(request.request_id, decision)


def _http_post_json(url: str, token: str, payload: dict[str, Any]) -> dict[str, Any]:
    data = json.dumps(payload).encode("utf-8")
    req = urllib_request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
        method="POST",
    )
    with urllib_request.urlopen(req) as response:  # noqa: S310
        return json.loads(response.read().decode("utf-8"))


def _http_get_json(url: str, token: str) -> dict[str, Any]:
    req = urllib_request.Request(url, headers={"Authorization": f"Bearer {token}"}, method="GET")
    with urllib_request.urlopen(req) as response:  # noqa: S310
        return json.loads(response.read().decode("utf-8"))


def request_hr_analytics_approval_via_console_api(
    console_base_url: str,
    token: str,
    requested_by: str,
    purpose: str,
    timeout_seconds: int = 120,
    poll_interval_seconds: int = 2,
    post_fn: Callable[[str, str, dict[str, Any]], dict[str, Any]] | None = None,
    get_fn: Callable[[str, str], dict[str, Any]] | None = None,
) -> str:
    """Submit approval request to supervisor console API and wait for human decision.

    Returns final status: APPROVE, REJECT, MODIFY, or OVERRIDE.
    Raises PermissionError when rejected or timed out.
    """
    post = post_fn or _http_post_json
    get = get_fn or _http_get_json

    request_payload = {
        "workflow_id": "workforce-hr-analytics",
        "action": {
            "type": "HR_ANALYTICS_MODE_REQUEST",
            "requested_by": requested_by,
            "purpose": purpose,
        },
        "risk_score": 0.74,
        "reason": "HR analytics mode requires explicit human supervisor approval and audit log.",
    }
    create_response = post(f"{console_base_url.rstrip('/')}/api/requests", token, request_payload)
    request = create_response.get("request", {})
    request_id = str(request.get("request_id", ""))
    if not request_id:
        raise PermissionError("hr_analytics_approval_request_failed")

    max_loops = max(1, timeout_seconds // max(1, poll_interval_seconds))
    for _ in range(max_loops):
        queue_response = get(f"{console_base_url.rstrip('/')}/api/queue", token)
        for item in queue_response.get("items", []):
            if str(item.get("request_id", "")) == request_id:
                status = str(item.get("status", "PENDING")).upper()
                if status in {"APPROVE", "MODIFY", "OVERRIDE"}:
                    return status
                if status == "REJECT":
                    raise PermissionError("hr_analytics_approval_rejected")
                break

        # Sleep imported lazily to keep testability straightforward via loop count.
        from time import sleep

        sleep(poll_interval_seconds)

    raise PermissionError("hr_analytics_approval_timeout")
