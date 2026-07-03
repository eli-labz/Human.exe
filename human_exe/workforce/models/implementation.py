"""Implementation roadmap models."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class ImplementationMilestone:
    milestone_id: str
    name: str
    owner: str
    timeframe: str
    dependencies: list[str]
    deliverables: list[str]
    exit_criteria: list[str]
    risks: list[str]
    decision_gate: str


@dataclass(slots=True)
class ImplementationPhase:
    phase_name: str
    duration: str
    owners: list[str]
    milestones: list[ImplementationMilestone] = field(default_factory=list)
