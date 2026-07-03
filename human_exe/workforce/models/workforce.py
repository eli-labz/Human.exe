"""Operational workforce metrics and KPI models."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class WorkforceMetric:
    metric_name: str
    department_id: str
    role_id: str | None
    period: str
    value: float
    baseline: float | None = None


@dataclass(slots=True)
class KPI:
    name: str
    current_value: float
    target_value: float
    unit: str
    owner: str
    cadence: str = "monthly"
    notes: list[str] = field(default_factory=list)
