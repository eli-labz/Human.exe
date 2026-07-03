"""ROI scenario calculator for workforce transformation."""

from __future__ import annotations

from human_exe.workforce.models.roi import ROIModel
from human_exe.workforce.services.ledger_loader import LedgerEntry, estimate_baseline_cost_from_ledger


def _payback_months(implementation_cost: float, annual_savings: float) -> float:
    if annual_savings <= 0:
        return 999.0
    return round((implementation_cost / annual_savings) * 12.0, 2)


def build_roi_scenarios(
    baseline_cost: float,
    implementation_cost: float,
    labor_hours_saved: float,
    blended_hourly_cost: float,
    quality_gain_percent: float,
) -> list[ROIModel]:
    base_savings = labor_hours_saved * blended_hourly_cost
    quality_bonus = baseline_cost * max(0.0, quality_gain_percent) * 0.2

    scenarios = {
        "conservative": 0.75,
        "expected": 1.0,
        "aggressive": 1.2,
    }

    output: list[ROIModel] = []
    for scenario, multiplier in scenarios.items():
        annual_savings = (base_savings + quality_bonus) * multiplier
        output.append(
            ROIModel(
                scenario=scenario,
                baseline_cost=round(baseline_cost, 2),
                implementation_cost=round(implementation_cost, 2),
                annual_savings=round(annual_savings, 2),
                productivity_recapture_hours=round(labor_hours_saved * multiplier, 2),
                quality_gain_percent=round(quality_gain_percent * multiplier, 4),
                payback_months=_payback_months(implementation_cost, annual_savings),
                assumptions=[
                    "Decision-support outputs remain human-reviewed.",
                    "No adverse employment action recommendations are used.",
                    "Savings realization depends on adoption and governance discipline.",
                ],
            )
        )
    return output


def build_roi_scenarios_from_ledger(
    ledger_entries: list[LedgerEntry],
    implementation_cost: float,
    labor_hours_saved: float,
    blended_hourly_cost: float,
    quality_gain_percent: float,
) -> list[ROIModel]:
    baseline_cost = estimate_baseline_cost_from_ledger(ledger_entries)
    return build_roi_scenarios(
        baseline_cost=baseline_cost,
        implementation_cost=implementation_cost,
        labor_hours_saved=labor_hours_saved,
        blended_hourly_cost=blended_hourly_cost,
        quality_gain_percent=quality_gain_percent,
    )
