"""Supervisor interface and governance layer."""

from __future__ import annotations

from collections import deque
from dataclasses import asdict
from pathlib import Path

from human_exe.models.supervision import ApprovalRequest, DecisionType, SupervisorDecision
from human_exe.observability.audit_logger import AuditLogger


class HumanSupervisionLayer:
    def __init__(self, audit_log_file: Path) -> None:
        self.approval_queue: deque[ApprovalRequest] = deque()
        self.audit_logger = AuditLogger(audit_log_file)

    def enqueue(self, request: ApprovalRequest) -> None:
        self.approval_queue.append(request)
        self.audit_logger.log("approval_requested", asdict(request))

    def resolve(self, request_id: str, decision: SupervisorDecision) -> SupervisorDecision:
        for request in self.approval_queue:
            if request.request_id == request_id:
                request.status = decision.decision.value
                self.audit_logger.log("approval_resolved", asdict(decision))
                return decision
        raise ValueError(f"Unknown approval request: {request_id}")

    def list_requests(self, status: str | None = None) -> list[dict[str, object]]:
        items = [asdict(request) for request in self.approval_queue]
        if status is None:
            return items
        target = status.upper()
        return [item for item in items if str(item.get("status", "")).upper() == target]

    @staticmethod
    def default_auto_decision(request: ApprovalRequest, supervisor_id: str) -> SupervisorDecision:
        # Demo default: safe auto-approval to keep workflow executable in tests.
        return SupervisorDecision(
            request_id=request.request_id,
            supervisor_id=supervisor_id,
            decision=DecisionType.APPROVE,
            reason="Auto-approved in sandbox demo.",
        )
