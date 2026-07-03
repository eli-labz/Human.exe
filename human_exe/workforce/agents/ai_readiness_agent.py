"""Agent wrapper for AI readiness scoring."""

from __future__ import annotations

from human_exe.workforce.models.readiness import AIReadinessScore
from human_exe.workforce.services.readiness_scoring import score_readiness


class AIReadinessAgent:
    def assess(self, dimensions: dict[str, float]) -> AIReadinessScore:
        return score_readiness(
            people=dimensions.get("people", 0.0),
            process=dimensions.get("process", 0.0),
            data=dimensions.get("data", 0.0),
            technology=dimensions.get("technology", 0.0),
            governance=dimensions.get("governance", 0.0),
            security=dimensions.get("security", 0.0),
            change_management=dimensions.get("change_management", 0.0),
        )
