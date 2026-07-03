from pathlib import Path
from dataclasses import asdict

from human_exe.workforce.reports.workforce_dashboard_generator import generate_dashboard_html
from human_exe.workforce.services.ledger_loader import load_ledger_entries
from human_exe.workforce.services.roi_calculator import build_roi_scenarios_from_ledger


def test_roi_from_ledger_and_dashboard_generation(tmp_path: Path) -> None:
    ledger = tmp_path / "ledger.csv"
    ledger.write_text(
        "period,account,category,amount\n"
        "2026-Q1,50010,labor,1000000\n"
        "2026-Q1,50020,overtime,120000\n"
        "2026-Q1,50030,rework,90000\n",
        encoding="utf-8",
    )
    entries = load_ledger_entries(ledger)
    models = build_roi_scenarios_from_ledger(
        ledger_entries=entries,
        implementation_cost=200000,
        labor_hours_saved=3000,
        blended_hourly_cost=60,
        quality_gain_percent=0.1,
    )

    assert len(models) == 3
    assert models[0].baseline_cost > 0

    dashboard = tmp_path / "workforce_dashboard.html"
    generate_dashboard_html(
        {
            "anomalies": [{"anomaly_type": "Backlog Spike", "severity": 0.8, "confidence": 0.7}],
            "opportunities": [{"task_id": "T1", "recommended_ai_mode": "AI-copilot task", "overall_ai_fit_score": 0.7}],
            "readiness": {"level": "Level 3", "overall": 0.58},
            "roi": [asdict(m) for m in models],
            "kpis": [{"name": "cycle_time_reduction", "target_value": 0.25, "unit": "percent", "owner": "Ops"}],
        },
        dashboard,
    )
    assert dashboard.exists()
