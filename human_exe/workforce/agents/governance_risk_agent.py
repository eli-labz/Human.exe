"""Governance and risk controls agent."""

from __future__ import annotations

from human_exe.workforce.models.anomaly import GovernanceControl
from human_exe.workforce.services.governance_policies import baseline_governance_controls


class GovernanceAndRiskAgent:
    def controls(self) -> list[GovernanceControl]:
        return baseline_governance_controls()
