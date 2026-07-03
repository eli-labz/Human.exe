"""Change management planning agent."""

from __future__ import annotations

from human_exe.workforce.models.strategy import ChangeManagementPlan
from human_exe.workforce.services.strategic_plan_builder import default_change_management_plan


class ChangeManagementAgent:
    def build(self) -> ChangeManagementPlan:
        return default_change_management_plan()
