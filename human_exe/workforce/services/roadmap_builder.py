"""Roadmap builder for 30/60/90-day and 6/12-month implementation plans."""

from __future__ import annotations

from human_exe.workforce.models.implementation import ImplementationMilestone, ImplementationPhase


def build_roadmap() -> list[ImplementationPhase]:
    return [
        ImplementationPhase(
            phase_name="30-day",
            duration="Week 1-4",
            owners=["Transformation Lead", "Data Lead"],
            milestones=[
                ImplementationMilestone(
                    milestone_id="M30-1",
                    name="Assessment and data foundation",
                    owner="Data Lead",
                    timeframe="Week 1-2",
                    dependencies=[],
                    deliverables=["baseline workforce dataset", "data quality report"],
                    exit_criteria=["critical data gaps documented", "governance intake approved"],
                    risks=["source system inconsistency"],
                    decision_gate="DG-30",
                ),
            ],
        ),
        ImplementationPhase(
            phase_name="60-day",
            duration="Week 5-8",
            owners=["Transformation Lead", "L&D"],
            milestones=[
                ImplementationMilestone(
                    milestone_id="M60-1",
                    name="AI literacy and workflow redesign",
                    owner="L&D",
                    timeframe="Week 5-8",
                    dependencies=["M30-1"],
                    deliverables=["role learning pathways", "workflow redesign backlog"],
                    exit_criteria=["pilot candidate workflows signed-off"],
                    risks=["manager bandwidth"],
                    decision_gate="DG-60",
                ),
            ],
        ),
        ImplementationPhase(
            phase_name="90-day",
            duration="Week 9-12",
            owners=["AI Product Owner", "Supervisor Team"],
            milestones=[
                ImplementationMilestone(
                    milestone_id="M90-1",
                    name="Pilot selection and proof of value",
                    owner="AI Product Owner",
                    timeframe="Week 9-12",
                    dependencies=["M60-1"],
                    deliverables=["pilot charter", "measurement dashboard"],
                    exit_criteria=["pilot KPI baseline established"],
                    risks=["limited adoption"],
                    decision_gate="DG-90",
                ),
            ],
        ),
        ImplementationPhase(
            phase_name="6-month",
            duration="Month 4-6",
            owners=["AI Product Owner", "Governance Council"],
            milestones=[
                ImplementationMilestone(
                    milestone_id="M6-1",
                    name="Supervised AI Agent buildout",
                    owner="AI Product Owner",
                    timeframe="Month 4-6",
                    dependencies=["M90-1"],
                    deliverables=["agent playbooks", "approval gate matrix"],
                    exit_criteria=["policy compliance above 99%"],
                    risks=["integration complexity"],
                    decision_gate="DG-6M",
                ),
            ],
        ),
        ImplementationPhase(
            phase_name="12-month",
            duration="Month 7-12",
            owners=["Transformation Office", "Department Leads"],
            milestones=[
                ImplementationMilestone(
                    milestone_id="M12-1",
                    name="Department deployment and enterprise scale",
                    owner="Transformation Office",
                    timeframe="Month 7-12",
                    dependencies=["M6-1"],
                    deliverables=["department playbooks", "continuous improvement cadence"],
                    exit_criteria=["target KPI attainment trend positive"],
                    risks=["change fatigue"],
                    decision_gate="DG-12M",
                ),
            ],
        ),
    ]
