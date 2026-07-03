"""Agent wrapper for AI opportunity classification and scoring."""

from __future__ import annotations

from human_exe.workforce.models.opportunity import AIOpportunity
from human_exe.workforce.models.workflow import TaskProfile, WorkflowProfile
from human_exe.workforce.services.opportunity_scoring import OpportunityScoreInputs, score_ai_opportunity


class AIOpportunityAgent:
    def evaluate(self, task: TaskProfile, workflow: WorkflowProfile) -> AIOpportunity:
        inputs = OpportunityScoreInputs(
            value_score=min(1.0, (task.weekly_volume * task.average_minutes) / 1500.0),
            repeatability_score=1.0 if not task.requires_human_judgment else 0.55,
            data_availability_score=0.9 if task.data_structured else 0.45,
            workflow_stability_score=max(0.2, 1.0 - workflow.exception_rate),
            verification_score=max(0.2, 1.0 - task.error_rate),
            risk_score=0.75 if task.requires_human_judgment else 0.35,
            reversibility_score=0.75 if task.data_structured else 0.45,
            human_supervision_score=0.9,
            integration_feasibility_score=0.8 if workflow.approval_steps <= 3 else 0.55,
            employee_acceptance_score=0.7,
        )
        return score_ai_opportunity(task, workflow, inputs)
