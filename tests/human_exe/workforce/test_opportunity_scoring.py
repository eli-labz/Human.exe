from human_exe.workforce.models.workflow import TaskProfile, WorkflowProfile
from human_exe.workforce.services.opportunity_scoring import OpportunityScoreInputs, overall_ai_fit_score, score_ai_opportunity


def test_opportunity_scoring_produces_fit_and_mode() -> None:
    task = TaskProfile("T1", "R1", "W1", "Invoice validation", "finance", 300, 18, 0.04, 0.08, 2, False, True)
    workflow = WorkflowProfile("W1", "D1", "R1", ["R1"], "Invoice workflow", ["ERP"], 16, 80, 2, 0.08, 2)
    inputs = OpportunityScoreInputs(
        value_score=0.8,
        repeatability_score=0.9,
        data_availability_score=0.85,
        workflow_stability_score=0.75,
        verification_score=0.8,
        risk_score=0.25,
        reversibility_score=0.85,
        human_supervision_score=0.9,
        integration_feasibility_score=0.8,
        employee_acceptance_score=0.7,
    )

    fit = overall_ai_fit_score(inputs)
    opportunity = score_ai_opportunity(task, workflow, inputs)

    assert fit > 0.6
    assert opportunity.overall_ai_fit_score == fit
    assert opportunity.recommended_ai_mode in {
        "Supervised AI Agent task",
        "AI-assisted knowledge task",
        "RPA or deterministic automation task",
    }
