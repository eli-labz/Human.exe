"""Strategic plan markdown and artifact generators."""

from __future__ import annotations

from pathlib import Path

from human_exe.workforce.models.strategy import StrategicPlan


def generate_strategic_plan(plan: StrategicPlan, output_file: Path) -> Path:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        f"# {plan.title}",
        "",
        "## 1. Executive Summary",
        plan.executive_summary,
        "",
        "## 2. Current-State Workforce Assessment",
        plan.current_state_assessment,
        "",
        "## 3. Anomaly Findings",
    ]
    for finding in sorted(plan.anomaly_findings, key=lambda x: x.severity, reverse=True):
        lines.append(
            f"- {finding.anomaly_type} | severity={finding.severity:.2f} | confidence={finding.confidence:.2f} | impact={finding.business_impact}"
        )
    lines.extend([
        "",
        "## 4. AI and AI Agent Opportunity Map",
    ])
    for opportunity in sorted(plan.ai_opportunity_map, key=lambda x: x.overall_ai_fit_score, reverse=True):
        lines.append(
            f"- {opportunity.task_id}: mode={opportunity.recommended_ai_mode}, fit={opportunity.overall_ai_fit_score:.2f}, "
            f"automation={opportunity.expected_automation_range}, supervision={opportunity.human_supervision_level}"
        )

    lines.extend([
        "",
        "## 5. AI Readiness Assessment",
        f"Overall={plan.readiness.overall:.2f}, Level={plan.readiness.level}",
        "",
        "## 6. Target Operating Model",
        plan.target_operating_model,
        "",
        "## 7. Strategic Objectives",
    ])
    for objective in plan.strategic_objectives:
        lines.append(f"- {objective.statement} ({objective.target_metric} -> {objective.target_value})")

    lines.extend([
        "",
        "## 8. Governance and Risk Model",
        plan.governance_model,
        "",
        "## 9. Implementation Roadmap",
    ])
    for phase in plan.phased_roadmap:
        lines.append(f"- {phase}")

    lines.extend([
        "",
        "## 10. Detailed 30/60/90-Day Plan",
        plan.implementation_plan,
        "",
        "## 11. 6-Month and 12-Month Plan",
        plan.scale_plan,
        "",
        "## 12. ROI and Business Case",
        plan.investment_plan,
        "",
        "## 13. Change Management Plan",
    ])
    for item in plan.change_management_plan.communication_plan:
        lines.append(f"- {item}")

    lines.extend([
        "",
        "## 14. KPI Dashboard",
    ])
    for kpi in plan.kpi_model:
        lines.append(f"- {kpi.name}: target={kpi.target_value} {kpi.unit}")

    lines.extend([
        "",
        "## 15. Implementation Backlog",
        "- Epic: Workflow Mining Foundation | User story: As operations, I need clean workflow telemetry so AI pilots are evidence-based.",
        "- Epic: Supervised Agent Pilot | User story: As a supervisor, I need approval gates and rollback options.",
        "- Epic: AI Literacy | User story: As a manager, I need role-specific training and adoption metrics.",
        "",
        "> Decision support only. Final decisions require human review and governance approval.",
    ])

    output_file.write_text("\n".join(lines), encoding="utf-8")
    return output_file
