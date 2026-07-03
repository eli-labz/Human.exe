"""Workflow and governance models."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from human_exe.models.tokens import HumanActionToken, IntentToken, OutcomeToken, PerceptionToken


@dataclass(slots=True)
class RiskAssessment:
    score: float
    requires_approval: bool
    reasons: list[str] = field(default_factory=list)


@dataclass(slots=True)
class ActionPolicy:
    allowed_actions: set[str]
    approval_required_actions: set[str]
    forbidden_actions: set[str]
    max_retry_attempts: int = 2
    risk_threshold: float = 0.65


@dataclass(slots=True)
class WorkflowTrace:
    workflow_id: str
    intent: IntentToken
    context: dict[str, Any]
    perceptions: list[PerceptionToken] = field(default_factory=list)
    actions: list[HumanActionToken] = field(default_factory=list)
    outcomes: list[OutcomeToken] = field(default_factory=list)
    verification_results: list[dict[str, Any]] = field(default_factory=list)
    supervisor_decisions: list[dict[str, Any]] = field(default_factory=list)
    failure_reason: str | None = None
    recovery_path: list[str] = field(default_factory=list)
    final_status: str = "PENDING"
    trace_quality_score: float = 0.0
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    def mark_updated(self) -> None:
        self.updated_at = datetime.now(UTC).isoformat()
