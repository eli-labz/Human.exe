"""AI readiness and workforce adoption models."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class AIReadinessScore:
    people: float
    process: float
    data: float
    technology: float
    governance: float
    security: float
    change_management: float
    overall: float
    level: str
    rationale: str


@dataclass(slots=True)
class TrainingPathway:
    pathway_id: str
    role_id: str
    title: str
    modules: list[str]
    duration_hours: float
    target_outcome: str
