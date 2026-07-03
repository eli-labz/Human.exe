"""ROI estimation models."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ROIModel:
    scenario: str
    baseline_cost: float
    implementation_cost: float
    annual_savings: float
    productivity_recapture_hours: float
    quality_gain_percent: float
    payback_months: float
    assumptions: list[str]
