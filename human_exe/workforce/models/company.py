"""Organization and workforce entity models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class CompanyProfile:
    company_id: str
    name: str
    industry: str
    employee_count: int
    geography: str
    strategic_priorities: list[str] = field(default_factory=list)


@dataclass(slots=True)
class Department:
    department_id: str
    name: str
    headcount: int
    primary_outcomes: list[str] = field(default_factory=list)


@dataclass(slots=True)
class RoleProfile:
    role_id: str
    department_id: str
    title: str
    headcount: int
    core_tasks: list[str] = field(default_factory=list)
    required_skills: list[str] = field(default_factory=list)


@dataclass(slots=True)
class EmployeeAggregate:
    role_id: str
    population_size: int
    avg_weekly_hours: float
    overtime_ratio: float
    task_volume: float
    error_rate: float
    notes: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class SkillProfile:
    skill_name: str
    role_id: str
    required_level: float
    observed_level: float
    training_completion_rate: float
