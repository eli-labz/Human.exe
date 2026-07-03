"""Planner agent for supervised workflow decomposition."""

from __future__ import annotations


class PlannerAgent:
    def plan(self, objective: str) -> list[str]:
        return [
            "observe",
            "read_document",
            "summarize",
            "draft_email",
            "request_approval",
            "verify",
            "finalize",
        ]
