"""Statistical and rule-based workforce anomaly detection."""

from __future__ import annotations

from statistics import mean, pstdev
from uuid import uuid4

from human_exe.workforce.models.anomaly import AnomalyFinding
from human_exe.workforce.models.company import EmployeeAggregate, SkillProfile
from human_exe.workforce.models.workflow import SystemProfile, TaskProfile, WorkflowProfile


def _z_score(value: float, values: list[float]) -> float:
    if not values:
        return 0.0
    sigma = pstdev(values)
    if sigma == 0:
        return 0.0
    return (value - mean(values)) / sigma


def detect_anomalies(
    employee_aggregates: list[EmployeeAggregate],
    tasks: list[TaskProfile],
    workflows: list[WorkflowProfile],
    skills: list[SkillProfile],
    systems: list[SystemProfile],
) -> list[AnomalyFinding]:
    findings: list[AnomalyFinding] = []

    workload_values = [item.task_volume for item in employee_aggregates]
    overtime_values = [item.overtime_ratio for item in employee_aggregates]
    error_values = [item.error_rate for item in employee_aggregates]

    for aggregate in employee_aggregates:
        z_workload = _z_score(aggregate.task_volume, workload_values)
        if z_workload > 1.2:
            findings.append(
                AnomalyFinding(
                    finding_id=str(uuid4()),
                    anomaly_type="Workload Spike",
                    category="workload",
                    severity=min(1.0, 0.6 + (z_workload / 3.0)),
                    confidence=0.75,
                    affected_roles=[aggregate.role_id],
                    affected_workflows=[],
                    business_impact="High workload concentration raises cycle-time and burnout risk.",
                    evidence_sources=["employee_aggregate.task_volume"],
                    recommended_response="Rebalance queue routing and add supervised AI copilot for repetitive tasks.",
                )
            )
        if aggregate.task_volume < max(1.0, mean(workload_values) * 0.4):
            findings.append(
                AnomalyFinding(
                    finding_id=str(uuid4()),
                    anomaly_type="Underutilized Capacity",
                    category="workload",
                    severity=0.45,
                    confidence=0.7,
                    affected_roles=[aggregate.role_id],
                    affected_workflows=[],
                    business_impact="Potential role underutilization or role-task mismatch.",
                    evidence_sources=["employee_aggregate.task_volume"],
                    recommended_response="Review task allocation and cross-train for workflow support coverage.",
                )
            )
        if _z_score(aggregate.overtime_ratio, overtime_values) > 1.1:
            findings.append(
                AnomalyFinding(
                    finding_id=str(uuid4()),
                    anomaly_type="Overtime Concentration",
                    category="workload",
                    severity=0.72,
                    confidence=0.78,
                    affected_roles=[aggregate.role_id],
                    affected_workflows=[],
                    business_impact="Sustained overtime indicates throughput imbalance and hidden backlog.",
                    evidence_sources=["employee_aggregate.overtime_ratio"],
                    recommended_response="Introduce approval-light automation for repetitive throughput work and queue balancing.",
                )
            )
        if aggregate.task_volume < 0 or aggregate.error_rate < 0:
            findings.append(
                AnomalyFinding(
                    finding_id=str(uuid4()),
                    anomaly_type="Invalid Workforce Metric",
                    category="data_quality",
                    severity=0.8,
                    confidence=0.95,
                    affected_roles=[aggregate.role_id],
                    affected_workflows=[],
                    business_impact="Invalid records reduce reliability of transformation recommendations.",
                    evidence_sources=["employee_aggregate.task_volume", "employee_aggregate.error_rate"],
                    recommended_response="Correct data extract logic and rerun assessment before implementation commitments.",
                    data_anomaly=True,
                )
            )

    cycle_times = [wf.cycle_time_hours for wf in workflows]
    handoff_values = [wf.manual_handoffs for wf in workflows]
    backlog_values = [wf.backlog_items for wf in workflows]

    for workflow in workflows:
        if _z_score(workflow.cycle_time_hours, cycle_times) > 1.1:
            findings.append(
                AnomalyFinding(
                    finding_id=str(uuid4()),
                    anomaly_type="Long Cycle Time",
                    category="process",
                    severity=0.74,
                    confidence=0.8,
                    affected_roles=[],
                    affected_workflows=[workflow.workflow_id],
                    business_impact="Delayed workflow completion impacts customer and internal SLA outcomes.",
                    evidence_sources=["workflow.cycle_time_hours"],
                    recommended_response="Map handoff points and add supervised agent support for intake, triage, and status updates.",
                )
            )
        if _z_score(workflow.manual_handoffs, handoff_values) > 1.0:
            findings.append(
                AnomalyFinding(
                    finding_id=str(uuid4()),
                    anomaly_type="Excessive Handoffs",
                    category="process",
                    severity=0.68,
                    confidence=0.77,
                    affected_roles=[],
                    affected_workflows=[workflow.workflow_id],
                    business_impact="Multiple handoffs increase coordination costs and rework probability.",
                    evidence_sources=["workflow.manual_handoffs"],
                    recommended_response="Consolidate ownership and automate structured handoff packets.",
                )
            )
        if _z_score(workflow.backlog_items, backlog_values) > 1.1:
            findings.append(
                AnomalyFinding(
                    finding_id=str(uuid4()),
                    anomaly_type="Backlog Spike",
                    category="workload",
                    severity=0.79,
                    confidence=0.81,
                    affected_roles=[],
                    affected_workflows=[workflow.workflow_id],
                    business_impact="Backlog growth indicates throughput constraints and prioritization friction.",
                    evidence_sources=["workflow.backlog_items"],
                    recommended_response="Deploy triage copilot and supervised agent routing to reduce intake latency.",
                )
            )

    for task in tasks:
        if task.rework_rate > 0.2:
            findings.append(
                AnomalyFinding(
                    finding_id=str(uuid4()),
                    anomaly_type="Repeated Rework",
                    category="process",
                    severity=min(1.0, 0.4 + task.rework_rate),
                    confidence=0.73,
                    affected_roles=[task.role_id],
                    affected_workflows=[],
                    business_impact="Rework erodes capacity and quality predictability.",
                    evidence_sources=["task.rework_rate"],
                    recommended_response="Improve verification steps and introduce AI-assisted quality checks.",
                )
            )
        if task.data_structured and task.handoff_count >= 3 and task.average_minutes >= 20:
            findings.append(
                AnomalyFinding(
                    finding_id=str(uuid4()),
                    anomaly_type="Manual Work Despite Structured Data",
                    category="technology",
                    severity=0.7,
                    confidence=0.8,
                    affected_roles=[task.role_id],
                    affected_workflows=[],
                    business_impact="Manual handling of structured data increases avoidable labor and delay.",
                    evidence_sources=["task.data_structured", "task.average_minutes", "task.handoff_count"],
                    recommended_response="Evaluate supervised AI agent or deterministic automation for data handling path.",
                )
            )

    for skill in skills:
        if skill.required_level - skill.observed_level > 0.35 and skill.training_completion_rate < 0.65:
            findings.append(
                AnomalyFinding(
                    finding_id=str(uuid4()),
                    anomaly_type="Skill Gap with Low Training Completion",
                    category="skills",
                    severity=0.71,
                    confidence=0.76,
                    affected_roles=[skill.role_id],
                    affected_workflows=[],
                    business_impact="Capability gap blocks tool adoption and increases error rates.",
                    evidence_sources=["skill.required_level", "skill.observed_level", "skill.training_completion_rate"],
                    recommended_response="Launch role-specific AI literacy and applied workflow training.",
                )
            )

    for system in systems:
        if system.automation_capability >= 0.7 and system.adoption_rate <= 0.4:
            findings.append(
                AnomalyFinding(
                    finding_id=str(uuid4()),
                    anomaly_type="Low Use of Available Automation",
                    category="technology",
                    severity=0.66,
                    confidence=0.72,
                    affected_roles=[],
                    affected_workflows=[],
                    business_impact="Existing tools are underleveraged, reducing ROI on system spend.",
                    evidence_sources=["system.automation_capability", "system.adoption_rate"],
                    recommended_response="Target enablement and process redesign before adding net-new tools.",
                )
            )

    return findings
