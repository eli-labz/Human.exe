"""ROI modeling agent."""

from __future__ import annotations

from pathlib import Path

from human_exe.workforce.models.roi import ROIModel
from human_exe.workforce.services.ledger_loader import load_ledger_entries
from human_exe.workforce.services.roi_calculator import build_roi_scenarios, build_roi_scenarios_from_ledger


class ROIModelAgent:
    def build(
        self,
        baseline_cost: float,
        implementation_cost: float,
        labor_hours_saved: float,
        blended_hourly_cost: float,
        quality_gain_percent: float,
    ) -> list[ROIModel]:
        return build_roi_scenarios(
            baseline_cost=baseline_cost,
            implementation_cost=implementation_cost,
            labor_hours_saved=labor_hours_saved,
            blended_hourly_cost=blended_hourly_cost,
            quality_gain_percent=quality_gain_percent,
        )

    def build_from_ledger(
        self,
        ledger_csv_path: Path,
        implementation_cost: float,
        labor_hours_saved: float,
        blended_hourly_cost: float,
        quality_gain_percent: float,
    ) -> list[ROIModel]:
        entries = load_ledger_entries(ledger_csv_path)
        return build_roi_scenarios_from_ledger(
            ledger_entries=entries,
            implementation_cost=implementation_cost,
            labor_hours_saved=labor_hours_saved,
            blended_hourly_cost=blended_hourly_cost,
            quality_gain_percent=quality_gain_percent,
        )
