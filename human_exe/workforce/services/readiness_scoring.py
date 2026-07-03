"""AI readiness scoring service."""

from __future__ import annotations

from human_exe.workforce.models.readiness import AIReadinessScore


def score_readiness(
    people: float,
    process: float,
    data: float,
    technology: float,
    governance: float,
    security: float,
    change_management: float,
) -> AIReadinessScore:
    values = [people, process, data, technology, governance, security, change_management]
    bounded = [max(0.0, min(1.0, v)) for v in values]
    overall = sum(bounded) / len(bounded)

    if overall < 0.2:
        level = "Level 0: Not ready"
    elif overall < 0.35:
        level = "Level 1: AI literacy foundation"
    elif overall < 0.5:
        level = "Level 2: AI-assisted workflow pilots"
    elif overall < 0.65:
        level = "Level 3: Supervised AI Agent pilots"
    elif overall < 0.8:
        level = "Level 4: Department-scale agent workflows"
    else:
        level = "Level 5: Enterprise AI Agent operating model"

    return AIReadinessScore(
        people=bounded[0],
        process=bounded[1],
        data=bounded[2],
        technology=bounded[3],
        governance=bounded[4],
        security=bounded[5],
        change_management=bounded[6],
        overall=round(overall, 4),
        level=level,
        rationale="Readiness score blends people, process, data, technology, governance, security, and change dimensions.",
    )
