"""Agent wrapper for implementation roadmap generation."""

from __future__ import annotations

from human_exe.workforce.models.implementation import ImplementationPhase
from human_exe.workforce.services.roadmap_builder import build_roadmap


class ImplementationRoadmapAgent:
    def build(self) -> list[ImplementationPhase]:
        return build_roadmap()
