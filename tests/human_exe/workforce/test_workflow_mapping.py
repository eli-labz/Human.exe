from human_exe.workforce.agents.workflow_mining_agent import WorkflowMiningAgent
from human_exe.workforce.models.workflow import TaskProfile, WorkflowProfile


def test_workflow_mapping_uses_explicit_foreign_keys() -> None:
    tasks = [
        TaskProfile("T1", "R1", "W1", "Task A", "ops", 100, 10, 0.01, 0.02, 1, False, True),
        TaskProfile("T2", "R2", "W1", "Task B", "ops", 80, 8, 0.02, 0.03, 1, False, True),
    ]
    workflows = [
        WorkflowProfile("W1", "D1", "R1", ["R1", "R2"], "Workflow 1", ["ERP"], 12, 40, 2, 0.05, 2),
    ]

    mapping = WorkflowMiningAgent().map_workflows(tasks, workflows)

    assert mapping["workflow_to_tasks"]["W1"] == ["T1", "T2"]
    assert "W1" in mapping["role_to_workflows"]["R1"]
    assert "W1" in mapping["role_to_workflows"]["R2"]
