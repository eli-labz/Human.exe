"""Executive report markdown generator."""

from __future__ import annotations

from pathlib import Path

from human_exe.workforce.models.strategy import ExecutiveReport


def generate_executive_report(report: ExecutiveReport, output_file: Path) -> Path:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        f"# Executive Summary - {report.company_name}",
        "",
        f"- Expected value: {report.expected_value_summary}",
        f"- Risk posture: {report.risk_posture}",
        f"- Recommended first move: {report.recommended_first_move}",
        "",
        "## Top Anomalies",
    ]
    lines.extend([f"- {item}" for item in report.top_anomalies])
    lines.append("")
    lines.append("## Top AI Opportunities")
    lines.extend([f"- {item}" for item in report.top_opportunities])
    lines.append("")
    lines.append(f"> {report.decision_support_notice}")
    output_file.write_text("\n".join(lines), encoding="utf-8")
    return output_file
