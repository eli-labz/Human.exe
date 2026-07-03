from human_exe.workforce.models.anomaly import AnomalyFinding
from human_exe.workforce.models.opportunity import AIOpportunity
from human_exe.workforce.services.readiness_scoring import score_readiness
from human_exe.workforce.services.strategic_plan_builder import build_strategic_plan


def test_strategy_builder_contains_required_sections() -> None:
    anomalies = [
        AnomalyFinding(
            finding_id="A1",
            anomaly_type="Backlog Spike",
            category="workload",
            severity=0.8,
            confidence=0.7,
            affected_roles=["R1"],
            affected_workflows=["W1"],
            business_impact="Delay risk",
            evidence_sources=["workflow.backlog"],
            recommended_response="Pilot supervised triage.",
        )
    ]
    opportunities = [
        AIOpportunity(
            opportunity_id="O1",
            task_id="T1",
            workflow_id="W1",
            recommended_ai_mode="Supervised AI Agent task",
            value_score=0.8,
            repeatability_score=0.9,
            data_availability_score=0.8,
            workflow_stability_score=0.7,
            verification_score=0.8,
            risk_score=0.3,
            reversibility_score=0.9,
            human_supervision_score=0.9,
            integration_feasibility_score=0.8,
            employee_acceptance_score=0.7,
            overall_ai_fit_score=0.81,
            expected_automation_range="30% - 50%",
            human_supervision_level="High",
            implementation_complexity="Moderate",
            recommended_phase="Phase 3",
            evidence="demo",
        )
    ]
    readiness = score_readiness(0.6, 0.6, 0.55, 0.65, 0.6, 0.68, 0.58)

    plan = build_strategic_plan(
        company_name="DemoCo",
        current_state_assessment="Current state mapped",
        anomaly_findings=anomalies,
        ai_opportunities=opportunities,
        readiness=readiness,
    )

    assert "Executive" in plan.executive_summary or plan.executive_summary
    assert plan.phased_roadmap
    assert plan.kpi_model
    assert plan.change_management_plan.communication_plan
