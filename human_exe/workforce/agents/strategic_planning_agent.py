"""Agent wrapper for strategic planning output."""

from __future__ import annotations

from human_exe.workforce.models.anomaly import AnomalyFinding
from human_exe.workforce.models.opportunity import AIOpportunity
from human_exe.workforce.models.readiness import AIReadinessScore
from human_exe.workforce.models.strategy import StrategicPlan
from human_exe.workforce.services.strategic_plan_builder import build_strategic_plan


class StrategicPlanningAgent:
    def build(
        self,
        company_name: str,
        current_state_assessment: str,
        anomalies: list[AnomalyFinding],
        opportunities: list[AIOpportunity],
        readiness: AIReadinessScore,
    ) -> StrategicPlan:
        return build_strategic_plan(
            company_name=company_name,
            current_state_assessment=current_state_assessment,
            anomaly_findings=anomalies,
            ai_opportunities=opportunities,
            readiness=readiness,
        )
