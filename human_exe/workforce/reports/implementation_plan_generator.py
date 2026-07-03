"""Implementation roadmap markdown generator."""

from __future__ import annotations

from pathlib import Path

from human_exe.workforce.models.implementation import ImplementationPhase


def generate_implementation_plan(phases: list[ImplementationPhase], output_file: Path) -> Path:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# Workforce AI Implementation Roadmap", ""]
    for phase in phases:
        lines.append(f"## {phase.phase_name} ({phase.duration})")
        lines.append(f"Owners: {', '.join(phase.owners)}")
        for milestone in phase.milestones:
            lines.append(f"- {milestone.name} | Owner: {milestone.owner} | Gate: {milestone.decision_gate}")
            lines.append(f"  - Deliverables: {', '.join(milestone.deliverables)}")
            lines.append(f"  - Exit criteria: {', '.join(milestone.exit_criteria)}")
            lines.append(f"  - Risks: {', '.join(milestone.risks)}")
        lines.append("")
    output_file.write_text("\n".join(lines), encoding="utf-8")
    return output_file
