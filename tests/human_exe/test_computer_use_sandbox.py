from pathlib import Path

from human_exe.agents.computer_use_agent import ComputerUseAgent
from human_exe.flows.computer_use_flow import run_demo_workflow
from human_exe.models.tokens import ActionType, HumanActionToken


def test_computer_use_agent_sandbox_open_url() -> None:
    agent = ComputerUseAgent()
    action = HumanActionToken(
        task_id="wf1",
        action_type=ActionType.OPEN_URL,
        parameters={"url": "https://example.com"},
        actor="agent",
    )
    outcome = agent.execute(action)
    assert outcome.success is True
    assert outcome.result["status"] in {"sandbox", "opened"}


def test_demo_workflow_end_to_end(tmp_path: Path) -> None:
    doc = tmp_path / "input.txt"
    doc.write_text("Sentence one. Sentence two. Sentence three.", encoding="utf-8")
    result = run_demo_workflow(doc, recipient="ops@example.com", artifacts_root=tmp_path / "artifacts")
    assert "workflow_id" in result
    assert Path(result["trace_path"]).exists()
