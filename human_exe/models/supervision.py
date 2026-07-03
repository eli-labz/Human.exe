"""Human supervision data models."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any
from uuid import uuid4


class DecisionType(str, Enum):
    APPROVE = "APPROVE"
    REJECT = "REJECT"
    MODIFY = "MODIFY"
    OVERRIDE = "OVERRIDE"


@dataclass(slots=True)
class SupervisorDecision:
    request_id: str
    supervisor_id: str
    decision: DecisionType
    reason: str
    modified_action: dict[str, Any] | None = None
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


@dataclass(slots=True)
class ApprovalRequest:
    workflow_id: str
    action: dict[str, Any]
    risk_score: float
    reason: str
    request_id: str = field(default_factory=lambda: str(uuid4()))
    status: str = "PENDING"
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
