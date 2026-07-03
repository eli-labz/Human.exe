"""Strategic plan builder for workforce transformation."""

from __future__ import annotations

from human_exe.workforce.models.anomaly import AnomalyFinding
from human_exe.workforce.models.opportunity import AIOpportunity
from human_exe.workforce.models.readiness import AIReadinessScore
from human_exe.workforce.models.strategy import ChangeManagementPlan, ExecutiveReport, StrategicObjective, StrategicPlan
from human_exe.workforce.services.kpi_builder import build_kpis
from human_exe.workforce.services.workforce_privacy_guard import validate_recommendation_text


def build_strategic_objectives() -> list[StrategicObjective]:
    return [
        StrategicObjective("SO-01", "Reduce cycle time in repetitive workflows by 25%.", "COO", "cycle_time_reduction", 0.25, "12 months"),
        StrategicObjective("SO-02", "Increase AI-assisted task adoption to 70% in candidate workflows.", "Transformation Office", "ai_adoption_rate", 0.7, "12 months"),
        StrategicObjective("SO-03", "Raise AI literacy completion to 85% for manager and analyst roles.", "L&D", "employee_confidence_score", 0.85, "6 months"),
        StrategicObjective("SO-04", "Maintain policy violation rate below 1% during scaling.", "Governance Council", "policy_violation_rate", 0.01, "ongoing"),
    ]


def default_change_management_plan() -> ChangeManagementPlan:
    return ChangeManagementPlan(
        stakeholder_map=[
            "Executive sponsors",
            "Department managers",
            "Frontline workflow owners",
            "IT and security leads",
            "Governance council",
        ],
        communication_plan=[
            "Monthly executive transformation briefing",
            "Bi-weekly department updates",
            "Pilot weekly office hours",
            "Quarterly workforce impact summary",
        ],
        manager_enablement=[
            "Manager decision-support playbook",
            "Approval gate coaching",
            "Pilot review facilitation training",
        ],
        ai_literacy_actions=[
            "Baseline AI literacy course",
            "Role-specific supervised-agent training",
            "Prompt quality and verification workshops",
        ],
        champions_network=[
            "One workflow champion per department",
            "Cross-functional transformation guild",
        ],
        feedback_loops=[
            "In-product feedback queue",
            "Monthly sentiment pulse",
            "Retrospective with governance team",
        ],
        resistance_mitigation=[
            "Explicit no-adverse-action policy",
            "Transparent KPI sharing",
            "Supervisor intervention path for concerns",
        ],
    )


def build_executive_report(
    company_name: str,
    anomalies: list[AnomalyFinding],
    opportunities: list[AIOpportunity],
) -> ExecutiveReport:
    top_anomalies = [f"{a.anomaly_type} ({a.severity:.2f})" for a in sorted(anomalies, key=lambda x: x.severity, reverse=True)[:5]]
    top_opportunities = [f"{o.task_id}: {o.recommended_ai_mode} ({o.overall_ai_fit_score:.2f})" for o in sorted(opportunities, key=lambda x: x.overall_ai_fit_score, reverse=True)[:5]]
    return ExecutiveReport(
        company_name=company_name,
        top_anomalies=top_anomalies,
        top_opportunities=top_opportunities,
        expected_value_summary="Expected value comes from cycle-time, rework, and backlog reduction with supervised AI execution.",
        risk_posture="Managed risk with mandatory approval gates, audit logging, and role-based access controls.",
        recommended_first_move="Start with data foundation and AI literacy while selecting two low-risk pilot workflows.",
        decision_support_notice="This report is decision support only; all actions require human review.",
    )


def build_strategic_plan(
    company_name: str,
    current_state_assessment: str,
    anomaly_findings: list[AnomalyFinding],
    ai_opportunities: list[AIOpportunity],
    readiness: AIReadinessScore,
) -> StrategicPlan:
    summary = (
        f"{company_name} can improve workflow quality and throughput by applying supervised AI augmentation in "
        f"high-repeatability processes while maintaining strong governance controls."
    )
    validate_recommendation_text(summary)

    plan = StrategicPlan(
        title=f"{company_name} Workforce AI Transformation Strategic Plan",
        executive_summary=summary,
        current_state_assessment=current_state_assessment,
        anomaly_findings=anomaly_findings,
        ai_opportunity_map=ai_opportunities,
        readiness=readiness,
        target_operating_model=(
            "Target model includes human role owners, AI copilot usage in knowledge workflows, "
            "supervised AI agents for bounded repetitive digital tasks, dedicated human approval roles, "
            "an AI product owner, and a governance council."
        ),
        strategic_objectives=build_strategic_objectives(),
        governance_model=(
            "Governance includes acceptable use policy, role-based permissions, data classification, "
            "human approval gates, audit logging, bias monitoring, security controls, and model/agent risk controls."
        ),
        phased_roadmap=[
            "Phase 1: Assessment and data foundation",
            "Phase 2: AI literacy and workflow redesign",
            "Phase 3: Pilot selection and proof of value",
            "Phase 4: Supervised AI Agent buildout",
            "Phase 5: Department deployment",
            "Phase 6: Enterprise scale and continuous improvement",
        ],
        investment_plan="Investment split across data foundation, enablement, pilot implementation, and governance operations.",
        risk_register=[
            "Data quality limitations can reduce recommendation confidence.",
            "Low change adoption may delay value realization.",
            "Insufficient governance staffing can increase compliance risk.",
        ],
        kpi_model=build_kpis(),
        change_management_plan=default_change_management_plan(),
        implementation_plan="Implementation follows 30/60/90-day plan then 6 and 12 month scaling milestones.",
        scale_plan="Scale by department readiness, KPI attainment, and governance maturity gates.",
        notes=[
            "Outputs are workforce augmentation guidance, not adverse employment recommendations.",
            "Protected class attributes are excluded from scoring and planning.",
        ],
    )
    return plan
