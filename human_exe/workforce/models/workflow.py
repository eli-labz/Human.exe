"""Workflow, task, and system models."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class TaskProfile:
    task_id: str
    role_id: str
    workflow_id: str
    name: str
    category: str
    weekly_volume: float
    average_minutes: float
    error_rate: float
    rework_rate: float
    handoff_count: float
    requires_human_judgment: bool
    data_structured: bool


@dataclass(slots=True)
class WorkflowProfile:
    workflow_id: str
    department_id: str
    process_owner_role_id: str
    linked_role_ids: list[str]
    name: str
    systems_used: list[str]
    cycle_time_hours: float
    backlog_items: float
    approval_steps: int
    exception_rate: float
    manual_handoffs: float


@dataclass(slots=True)
class SystemProfile:
    system_id: str
    name: str
    system_type: str
    departments: list[str]
    automation_capability: float
    adoption_rate: float
    notes: list[str] = field(default_factory=list)
