"""Flow helpers for supervisor approval lifecycle."""

from __future__ import annotations

from human_exe.agents.supervisor_interface_agent import HumanSupervisionLayer
from human_exe.models.supervision import ApprovalRequest, SupervisorDecision


def run_supervised_approval_flow(
    supervision_layer: HumanSupervisionLayer,
    request: ApprovalRequest,
    supervisor_id: str,
) -> SupervisorDecision:
    supervision_layer.enqueue(request)
    decision = supervision_layer.default_auto_decision(request, supervisor_id=supervisor_id)
    return supervision_layer.resolve(request.request_id, decision)
