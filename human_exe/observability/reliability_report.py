"""Reliability report generation."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from human_exe.models.metrics import CognitiveDebtIndex, ReliabilityMetrics


def generate_reliability_report(
    metrics: ReliabilityMetrics,
    cognitive_debt: CognitiveDebtIndex,
    output_file: Path,
) -> dict[str, object]:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "reliability_metrics": asdict(metrics),
        "cognitive_debt_index": asdict(cognitive_debt),
        "rubber_stamp_flag": cognitive_debt.likely_rubber_stamp(),
    }
    output_file.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report
