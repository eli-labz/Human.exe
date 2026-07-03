"""Workflow mining and mapping agent."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from human_exe.workforce.models.workflow import TaskProfile, WorkflowProfile


class WorkflowMiningAgent:
    def map_workflows(self, tasks: list[TaskProfile], workflows: list[WorkflowProfile]) -> dict[str, Any]:
        role_to_tasks: dict[str, list[str]] = defaultdict(list)
        workflow_to_tasks: dict[str, list[str]] = defaultdict(list)
        for task in tasks:
            role_to_tasks[task.role_id].append(task.task_id)
            workflow_to_tasks[task.workflow_id].append(task.task_id)

        role_to_workflows: dict[str, list[str]] = defaultdict(list)
        for workflow in workflows:
            if workflow.process_owner_role_id:
                role_to_workflows[workflow.process_owner_role_id].append(workflow.workflow_id)
            for role_id in workflow.linked_role_ids:
                role_to_workflows[role_id].append(workflow.workflow_id)

        system_to_workflow: dict[str, list[str]] = defaultdict(list)
        for workflow in workflows:
            for system in workflow.systems_used:
                system_to_workflow[system].append(workflow.workflow_id)

        return {
            "role_to_tasks": dict(role_to_tasks),
            "workflow_to_tasks": dict(workflow_to_tasks),
            "role_to_workflows": dict(role_to_workflows),
            "system_to_workflows": dict(system_to_workflow),
            "workflow_count": len(workflows),
            "task_count": len(tasks),
        }
