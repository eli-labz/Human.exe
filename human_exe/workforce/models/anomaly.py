"""Anomaly and risk finding models."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class AnomalyFinding:
    finding_id: str
    anomaly_type: str
    category: str
    severity: float
    confidence: float
    affected_roles: list[str]
    affected_workflows: list[str]
    business_impact: str
    evidence_sources: list[str]
    recommended_response: str
    data_anomaly: bool = False


@dataclass(slots=True)
class RiskFinding:
    risk_id: str
    title: str
    severity: float
    likelihood: float
    impact: str
    mitigation: str
    owner: str
    decision_gate: str


@dataclass(slots=True)
class GovernanceControl:
    control_id: str
    name: str
    control_type: str
    description: str
    owner: str
    required: bool = True
    escalation_path: list[str] = field(default_factory=list)
