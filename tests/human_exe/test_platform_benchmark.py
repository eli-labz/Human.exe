from pathlib import Path

from human_exe.models.metrics import ReliabilityMetrics
from human_exe.observability.platform_benchmark import (
    PlatformBenchmarkInputs,
    benchmark_competitiveness,
)


def test_platform_benchmark_generates_competitive_report(tmp_path: Path) -> None:
    reliability = ReliabilityMetrics(
        task_completion_rate=0.92,
        action_success_rate=0.94,
        verification_success_rate=0.95,
        recovery_rate=0.80,
        escalation_rate=0.08,
        policy_violation_rate=0.0,
        human_override_rate=0.06,
        time_to_useful_result=28.0,
        approval_latency=14.0,
        repeated_failure_count=0,
    )
    benchmark = PlatformBenchmarkInputs(
        supervised_task_coverage=0.78,
        approval_traceability=1.0,
        policy_enforcement=1.0,
        bounded_recovery=0.82,
        verification_coverage=0.95,
        human_override_control=0.80,
    )

    out_file = tmp_path / "competitiveness.json"
    report = benchmark_competitiveness(reliability, benchmark, out_file)

    assert out_file.exists()
    assert report["competitiveness_score"] >= 70.0
    assert report["segment"] in {"competitive", "differentiated"}
