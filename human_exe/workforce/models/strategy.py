"""Strategic planning and executive output models."""

from __future__ import annotations

from dataclasses import dataclass, field

from human_exe.workforce.models.anomaly import AnomalyFinding
from human_exe.workforce.models.opportunity import AIOpportunity
from human_exe.workforce.models.readiness import AIReadinessScore
from human_exe.workforce.models.workforce import KPI


@dataclass(slots=True)
class StrategicObjective:
    objective_id: str
    statement: str
    owner: str
    target_metric: str
    target_value: float
    due_period: str


@dataclass(slots=True)
class ChangeManagementPlan:
    stakeholder_map: list[str]
    communication_plan: list[str]
    manager_enablement: list[str]
    ai_literacy_actions: list[str]
    champions_network: list[str]
    feedback_loops: list[str]
    resistance_mitigation: list[str]


@dataclass(slots=True)
class StrategicPlan:
    title: str
    executive_summary: str
    current_state_assessment: str
    anomaly_findings: list[AnomalyFinding]
    ai_opportunity_map: list[AIOpportunity]
    readiness: AIReadinessScore
    target_operating_model: str
    strategic_objectives: list[StrategicObjective]
    governance_model: str
    phased_roadmap: list[str]
    investment_plan: str
    risk_register: list[str]
    kpi_model: list[KPI]
    change_management_plan: ChangeManagementPlan
    implementation_plan: str
    scale_plan: str
    notes: list[str] = field(default_factory=list)


@dataclass(slots=True)
class ExecutiveReport:
    company_name: str
    top_anomalies: list[str]
    top_opportunities: list[str]
    expected_value_summary: str
    risk_posture: str
    recommended_first_move: str
    decision_support_notice: str
