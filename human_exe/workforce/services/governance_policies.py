"""Governance helper rules for workforce transformation recommendations."""

from __future__ import annotations

from human_exe.workforce.models.anomaly import GovernanceControl


def baseline_governance_controls() -> list[GovernanceControl]:
    return [
        GovernanceControl("GC-001", "Human Approval Gates", "approval", "All strategic recommendations require supervisor review.", "Governance Council"),
        GovernanceControl("GC-002", "Role-based Permissions", "rbac", "Access to workforce outputs is role-scoped.", "Security"),
        GovernanceControl("GC-003", "Decision Support Labeling", "policy", "Outputs are advisory and not final decisions.", "Legal"),
        GovernanceControl("GC-004", "Bias and Protected Attribute Guard", "bias", "Protected attributes are excluded and cannot be inferred.", "HR Governance"),
        GovernanceControl("GC-005", "Audit Logging", "audit", "Strategic and operational decisions are logged immutably.", "Risk Office"),
    ]
