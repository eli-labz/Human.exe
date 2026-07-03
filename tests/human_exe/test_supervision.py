from pathlib import Path

from human_exe.agents.supervisor_interface_agent import HumanSupervisionLayer
from human_exe.models.supervision import ApprovalRequest


def test_approval_queue_and_resolution(tmp_path: Path) -> None:
    layer = HumanSupervisionLayer(tmp_path / "audit.jsonl")
    req = ApprovalRequest(
        workflow_id="wf1",
        action={"type": "SEND_DRAFT_FOR_APPROVAL"},
        risk_score=0.8,
        reason="high risk",
    )
    layer.enqueue(req)
    decision = layer.default_auto_decision(req, supervisor_id="sup1")
    resolved = layer.resolve(req.request_id, decision)
    assert resolved.request_id == req.request_id
