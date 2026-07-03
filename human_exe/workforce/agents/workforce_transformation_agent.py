"""End-to-end orchestration agent for workforce AI transformation."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

from human_exe.workforce.agents.ai_opportunity_agent import AIOpportunityAgent
from human_exe.workforce.agents.ai_readiness_agent import AIReadinessAgent
from human_exe.workforce.agents.governance_risk_agent import GovernanceAndRiskAgent
from human_exe.workforce.agents.implementation_roadmap_agent import ImplementationRoadmapAgent
from human_exe.workforce.agents.roi_model_agent import ROIModelAgent
from human_exe.workforce.agents.strategic_planning_agent import StrategicPlanningAgent
from human_exe.workforce.agents.workflow_mining_agent import WorkflowMiningAgent
from human_exe.workforce.agents.workforce_anomaly_agent import WorkforceAnomalyAgent
from human_exe.workforce.models.company import CompanyProfile, EmployeeAggregate, SkillProfile
from human_exe.workforce.models.opportunity import AIOpportunity
from human_exe.workforce.models.workflow import SystemProfile, TaskProfile, WorkflowProfile
from human_exe.workforce.services.workforce_privacy_guard import validate_recommendation_text


class WorkforceTransformationAgent:
    def __init__(self) -> None:
        self.anomaly_agent = WorkforceAnomalyAgent()
        self.workflow_agent = WorkflowMiningAgent()
        self.opportunity_agent = AIOpportunityAgent()
        self.readiness_agent = AIReadinessAgent()
        self.strategy_agent = StrategicPlanningAgent()
        self.roadmap_agent = ImplementationRoadmapAgent()
        self.governance_agent = GovernanceAndRiskAgent()
        self.roi_agent = ROIModelAgent()

    def run(
        self,
        company: CompanyProfile,
        employee_aggregates: list[EmployeeAggregate],
        tasks: list[TaskProfile],
        workflows: list[WorkflowProfile],
        skills: list[SkillProfile],
        systems: list[SystemProfile],
        readiness_inputs: dict[str, float],
    ) -> dict[str, Any]:
        anomalies = self.anomaly_agent.run(employee_aggregates, tasks, workflows, skills, systems)
        workflow_map = self.workflow_agent.map_workflows(tasks, workflows)

        workflow_lookup = {wf.workflow_id: wf for wf in workflows}
        opportunities: list[AIOpportunity] = []
        for task in tasks:
            workflow = workflow_lookup.get(task.workflow_id)
            if workflow is None and workflows:
                workflow = workflows[0]
            if workflow is None:
                continue
            opportunities.append(self.opportunity_agent.evaluate(task, workflow))

        readiness = self.readiness_agent.assess(readiness_inputs)
        current_state = (
            f"Company has {company.employee_count} employees across mapped workflows. "
            f"Workflow map includes {workflow_map['workflow_count']} workflows and {workflow_map['task_count']} tasks."
        )
        validate_recommendation_text(current_state)

        strategic_plan = self.strategy_agent.build(
            company_name=company.name,
            current_state_assessment=current_state,
            anomalies=anomalies,
            opportunities=opportunities,
            readiness=readiness,
        )
        roadmap = self.roadmap_agent.build()
        governance = self.governance_agent.controls()
        roi = self.roi_agent.build(
            baseline_cost=4_200_000,
            implementation_cost=580_000,
            labor_hours_saved=14_000,
            blended_hourly_cost=62,
            quality_gain_percent=0.18,
        )

        return {
            "company": asdict(company),
            "anomalies": [asdict(a) for a in anomalies],
            "opportunities": [asdict(o) for o in opportunities],
            "readiness": asdict(readiness),
            "strategic_plan": asdict(strategic_plan),
            "roadmap": [asdict(phase) for phase in roadmap],
            "governance_controls": [asdict(control) for control in governance],
            "roi": [asdict(model) for model in roi],
            "workflow_map": workflow_map,
        }
