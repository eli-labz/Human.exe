"""Agent wrapper for workforce anomaly detection."""

from __future__ import annotations

from human_exe.workforce.models.anomaly import AnomalyFinding
from human_exe.workforce.models.company import EmployeeAggregate, SkillProfile
from human_exe.workforce.models.workflow import SystemProfile, TaskProfile, WorkflowProfile
from human_exe.workforce.services.anomaly_detection import detect_anomalies


class WorkforceAnomalyAgent:
    def run(
        self,
        employee_aggregates: list[EmployeeAggregate],
        tasks: list[TaskProfile],
        workflows: list[WorkflowProfile],
        skills: list[SkillProfile],
        systems: list[SystemProfile],
    ) -> list[AnomalyFinding]:
        return detect_anomalies(employee_aggregates, tasks, workflows, skills, systems)
