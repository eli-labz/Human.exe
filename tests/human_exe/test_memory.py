from pathlib import Path

from human_exe.memory.trace_store import TraceStore
from human_exe.models.tokens import IntentToken
from human_exe.models.workflow import WorkflowTrace


def test_trace_store_saves_quality_scored_trace(tmp_path: Path) -> None:
    trace = WorkflowTrace(
        workflow_id="wf-test",
        intent=IntentToken(
            task_id="wf-test",
            objective="summarize doc",
            business_goal="save time",
            created_by="user",
        ),
        context={},
        final_status="COMPLETED",
    )
    store = TraceStore(tmp_path)
    file_path = store.save_trace(trace)
    assert file_path.exists()
    assert trace.trace_quality_score >= 0.0
