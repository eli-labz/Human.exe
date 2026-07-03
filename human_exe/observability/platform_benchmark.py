"""Competitive benchmark scoring for supervised digital labor readiness."""

from __future__ import annotations

import json
from dataclasses import asdict
from dataclasses import dataclass
from pathlib import Path

from human_exe.models.metrics import ReliabilityMetrics


@dataclass(slots=True)
class PlatformBenchmarkInputs:
    supervised_task_coverage: float
    approval_traceability: float
    policy_enforcement: float
    bounded_recovery: float
    verification_coverage: float
    human_override_control: float


def _clamp_unit(value: float) -> float:
    return max(0.0, min(1.0, value))


def benchmark_competitiveness(
    reliability: ReliabilityMetrics,
    benchmark: PlatformBenchmarkInputs,
    output_file: Path,
) -> dict[str, object]:
    """Generate a platform competitiveness report and persist it as JSON."""
    weighted_score = (
        _clamp_unit(benchmark.supervised_task_coverage) * 0.20
        + _clamp_unit(benchmark.approval_traceability) * 0.20
        + _clamp_unit(benchmark.policy_enforcement) * 0.20
        + _clamp_unit(benchmark.bounded_recovery) * 0.10
        + _clamp_unit(benchmark.verification_coverage) * 0.20
        + _clamp_unit(benchmark.human_override_control) * 0.10
    )

    reliability_modifier = (
        _clamp_unit(reliability.task_completion_rate) * 0.35
        + _clamp_unit(reliability.action_success_rate) * 0.20
        + _clamp_unit(reliability.verification_success_rate) * 0.20
        + _clamp_unit(1.0 - reliability.policy_violation_rate) * 0.25
    )

    competitiveness_score = round((weighted_score * 0.7 + reliability_modifier * 0.3) * 100, 2)

    report = {
        "competitiveness_score": competitiveness_score,
        "segment": _score_segment(competitiveness_score),
        "benchmark_inputs": asdict(benchmark),
        "reliability_metrics": asdict(reliability),
        "governance_gate": {
            "policy_violation_rate_ok": reliability.policy_violation_rate <= 0.02,
            "human_override_rate_min": reliability.human_override_rate >= 0.01,
            "escalation_rate_healthy": reliability.escalation_rate >= 0.01,
        },
    }

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


def _score_segment(score: float) -> str:
    if score >= 85:
        return "differentiated"
    if score >= 70:
        return "competitive"
    if score >= 55:
        return "emerging"
    return "prototype"
