"""Generate a demo workforce transformation strategy package."""

from __future__ import annotations

from dataclasses import asdict
import csv
from pathlib import Path

from human_exe.observability.audit_logger import AuditLogger
from human_exe.workforce.agents.ai_opportunity_agent import AIOpportunityAgent
from human_exe.workforce.agents.ai_readiness_agent import AIReadinessAgent
from human_exe.workforce.agents.implementation_roadmap_agent import ImplementationRoadmapAgent
from human_exe.workforce.agents.roi_model_agent import ROIModelAgent
from human_exe.workforce.agents.strategic_planning_agent import StrategicPlanningAgent
from human_exe.workforce.agents.workforce_anomaly_agent import WorkforceAnomalyAgent
from human_exe.workforce.models.company import CompanyProfile, Department, EmployeeAggregate, RoleProfile, SkillProfile
from human_exe.workforce.models.workflow import SystemProfile, TaskProfile, WorkflowProfile
from human_exe.workforce.reports.dashboard_exporter import export_csv, export_json, models_to_dicts
from human_exe.workforce.reports.executive_report_generator import generate_executive_report
from human_exe.workforce.reports.implementation_plan_generator import generate_implementation_plan
from human_exe.workforce.reports.strategic_plan_generator import generate_strategic_plan
from human_exe.workforce.reports.workforce_dashboard_generator import generate_dashboard_html
from human_exe.workforce.services.kpi_builder import build_kpis
from human_exe.workforce.services.strategic_plan_builder import build_executive_report


def _build_demo_dataset() -> tuple[
    CompanyProfile,
    list[Department],
    list[RoleProfile],
    list[EmployeeAggregate],
    list[SkillProfile],
    list[TaskProfile],
    list[WorkflowProfile],
    list[SystemProfile],
]:
    company = CompanyProfile(
        company_id="cmp-001",
        name="Northstar Manufacturing Group",
        industry="Industrial Manufacturing",
        employee_count=1850,
        geography="US + EU",
        strategic_priorities=["margin expansion", "customer responsiveness", "quality consistency"],
    )

    departments = [
        Department("D-OPS", "Operations", 520, ["on-time production", "throughput"]),
        Department("D-CS", "Customer Support", 290, ["response time", "resolution quality"]),
        Department("D-FIN", "Finance", 180, ["close efficiency", "controls"]),
        Department("D-HR", "Human Resources", 120, ["talent enablement", "compliance"]),
        Department("D-SALES", "Sales", 340, ["pipeline conversion", "forecast accuracy"]),
    ]

    role_titles = [
        "Operations Coordinator", "Scheduler", "Quality Analyst", "Support Specialist", "Support Lead",
        "Billing Analyst", "AP Specialist", "HR Generalist", "Recruiting Coordinator", "Sales Operations Analyst",
        "Account Executive", "Revenue Analyst", "Procurement Specialist", "Inventory Analyst", "Compliance Reviewer",
        "Reporting Analyst", "Workflow Supervisor", "Customer Onboarding Specialist", "Data Steward", "Training Specialist",
    ]

    roles: list[RoleProfile] = []
    employee_aggregates: list[EmployeeAggregate] = []
    skills: list[SkillProfile] = []
    tasks: list[TaskProfile] = []
    workflows: list[WorkflowProfile] = []

    department_ids = [department.department_id for department in departments]

    for index, title in enumerate(role_titles):
        role_id = f"R-{index+1:02d}"
        dept_id = department_ids[index % len(department_ids)]
        roles.append(
            RoleProfile(
                role_id=role_id,
                department_id=dept_id,
                title=title,
                headcount=12 + (index % 6) * 3,
                core_tasks=["intake", "validation", "update records", "reporting"],
                required_skills=["workflow tools", "data quality", "communication"],
            )
        )

        task_volume = 180 + (index * 17)
        overtime = 0.08 + (index % 5) * 0.05
        error_rate = 0.03 + (index % 4) * 0.015
        employee_aggregates.append(
            EmployeeAggregate(
                role_id=role_id,
                population_size=12 + (index % 6) * 3,
                avg_weekly_hours=39 + (index % 4) * 2,
                overtime_ratio=overtime,
                task_volume=task_volume,
                error_rate=error_rate,
                notes={"source": "demo"},
            )
        )

        skills.append(
            SkillProfile(
                skill_name="AI workflow literacy",
                role_id=role_id,
                required_level=0.75,
                observed_level=max(0.2, 0.75 - (index % 5) * 0.12),
                training_completion_rate=max(0.3, 0.82 - (index % 6) * 0.09),
            )
        )

        task_id = f"T-{index+1:02d}"
        tasks.append(
            TaskProfile(
                task_id=task_id,
                role_id=role_id,
                workflow_id=f"W-{(index % len(departments)) + 1:02d}",
                name=f"{title} recurring workflow task",
                category="reporting" if index % 3 == 0 else "operations",
                weekly_volume=float(task_volume),
                average_minutes=12.0 + (index % 7) * 4.0,
                error_rate=error_rate,
                rework_rate=0.06 + (index % 4) * 0.05,
                handoff_count=float(1 + (index % 5)),
                requires_human_judgment=index % 4 == 0,
                data_structured=index % 5 != 0,
            )
        )

    for i, department in enumerate(departments, start=1):
        workflows.append(
            WorkflowProfile(
                workflow_id=f"W-{i:02d}",
                department_id=department.department_id,
                process_owner_role_id=f"R-{i:02d}",
                linked_role_ids=[f"R-{i:02d}", f"R-{i+5:02d}", f"R-{i+10:02d}"],
                name=f"{department.name} core process",
                systems_used=["ERP", "CRM", "Ticketing"] if i % 2 == 0 else ["ERP", "Spreadsheet", "Email"],
                cycle_time_hours=22.0 + i * 6.5,
                backlog_items=110 + i * 42,
                approval_steps=2 + (i % 3),
                exception_rate=0.08 + i * 0.03,
                manual_handoffs=float(2 + i),
            )
        )

    systems = [
        SystemProfile("S-ERP", "ERP", "ERP", department_ids, automation_capability=0.82, adoption_rate=0.62),
        SystemProfile("S-CRM", "CRM", "CRM", ["D-SALES", "D-CS"], automation_capability=0.78, adoption_rate=0.58),
        SystemProfile("S-TICK", "Ticketing", "Support", ["D-CS", "D-OPS"], automation_capability=0.73, adoption_rate=0.54),
        SystemProfile("S-LMS", "LMS", "Learning", ["D-HR"], automation_capability=0.66, adoption_rate=0.46),
        SystemProfile("S-SS", "Spreadsheet", "End-user", department_ids, automation_capability=0.3, adoption_rate=0.91),
    ]

    return company, departments, roles, employee_aggregates, skills, tasks, workflows, systems


def _build_anomaly_report(anomalies: list[dict[str, object]]) -> str:
    lines = ["# Workforce Anomaly Report", "", "Decision support only. Human review required.", ""]
    for anomaly in sorted(anomalies, key=lambda x: float(x.get("severity", 0.0)), reverse=True):
        lines.append(
            f"- {anomaly['anomaly_type']} | category={anomaly['category']} | severity={anomaly['severity']:.2f} | confidence={anomaly['confidence']:.2f}"
        )
        lines.append(f"  - Evidence: {', '.join(anomaly.get('evidence_sources', []))}")
        lines.append(f"  - Recommended response: {anomaly['recommended_response']}")
    return "\n".join(lines)


def _build_readiness_markdown(readiness: dict[str, object]) -> str:
    return "\n".join(
        [
            "# AI Readiness Scorecard",
            "",
            f"- People: {readiness['people']}",
            f"- Process: {readiness['process']}",
            f"- Data: {readiness['data']}",
            f"- Technology: {readiness['technology']}",
            f"- Governance: {readiness['governance']}",
            f"- Security: {readiness['security']}",
            f"- Change: {readiness['change_management']}",
            f"- Overall: {readiness['overall']}",
            f"- Level: {readiness['level']}",
            "",
            "> Decision support only. Human review and approval required.",
        ]
    )


def _write_demo_ledger(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = [
        ["period", "account", "category", "amount"],
        ["2026-Q1", "50010", "labor", "1250000"],
        ["2026-Q1", "50020", "overtime", "240000"],
        ["2026-Q1", "50030", "rework", "310000"],
        ["2026-Q1", "50040", "operations", "860000"],
        ["2026-Q1", "50050", "support", "430000"],
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerows(rows)
    return path


def generate_strategy(output_dir: Path | None = None) -> dict[str, Path]:
    root = output_dir or Path(".artifacts/human_exe/workforce_demo")
    root.mkdir(parents=True, exist_ok=True)

    company, _departments, _roles, employee_aggregates, skills, tasks, workflows, systems = _build_demo_dataset()

    anomaly_agent = WorkforceAnomalyAgent()
    opportunity_agent = AIOpportunityAgent()
    readiness_agent = AIReadinessAgent()
    strategy_agent = StrategicPlanningAgent()
    roadmap_agent = ImplementationRoadmapAgent()
    roi_agent = ROIModelAgent()

    anomalies = anomaly_agent.run(employee_aggregates, tasks, workflows, skills, systems)
    opportunities = [
        opportunity_agent.evaluate(task, workflows[index % len(workflows)])
        for index, task in enumerate(tasks)
    ]
    readiness = readiness_agent.assess(
        {
            "people": 0.52,
            "process": 0.58,
            "data": 0.49,
            "technology": 0.61,
            "governance": 0.55,
            "security": 0.66,
            "change_management": 0.5,
        }
    )

    strategic_plan = strategy_agent.build(
        company_name=company.name,
        current_state_assessment=(
            "Five departments with mixed workflow maturity and high dependence on manual handoffs and spreadsheet operations."
        ),
        anomalies=anomalies,
        opportunities=opportunities,
        readiness=readiness,
    )

    roadmap = roadmap_agent.build()
    ledger_csv = _write_demo_ledger(root / "financial_ledger_demo.csv")
    roi = roi_agent.build_from_ledger(
        ledger_csv_path=ledger_csv,
        implementation_cost=580_000,
        labor_hours_saved=14_000,
        blended_hourly_cost=62,
        quality_gain_percent=0.18,
    )

    executive_report = build_executive_report(company.name, anomalies, opportunities)

    anomaly_report_path = root / "workforce_anomaly_report.md"
    anomaly_report_path.write_text(
        _build_anomaly_report([asdict(item) for item in anomalies]),
        encoding="utf-8",
    )

    ai_map_path = export_csv(models_to_dicts(opportunities), root / "ai_opportunity_map.csv")

    readiness_path = root / "ai_readiness_scorecard.md"
    readiness_path.write_text(_build_readiness_markdown(asdict(readiness)), encoding="utf-8")

    strategic_path = generate_strategic_plan(strategic_plan, root / "strategic_plan.md")
    implementation_path = generate_implementation_plan(roadmap, root / "implementation_roadmap.md")

    roi_path = export_csv(models_to_dicts(roi), root / "roi_model.csv")
    executive_path = generate_executive_report(executive_report, root / "executive_summary.md")
    kpi_payload = {"kpis": [asdict(kpi) for kpi in build_kpis()]}
    kpi_path = export_json(kpi_payload, root / "kpi_dashboard.json")
    dashboard_path = generate_dashboard_html(
        {
            "anomalies": [asdict(item) for item in anomalies],
            "opportunities": [asdict(item) for item in opportunities],
            "readiness": asdict(readiness),
            "roi": models_to_dicts(roi),
            "kpis": kpi_payload["kpis"],
        },
        root / "workforce_dashboard.html",
    )

    audit = AuditLogger(root / "audit_log.jsonl")
    audit.log(
        "workforce_strategy_generated",
        {
            "company": company.name,
            "anomaly_count": len(anomalies),
            "opportunity_count": len(opportunities),
            "readiness_level": readiness.level,
        },
    )

    return {
        "workforce_anomaly_report.md": anomaly_report_path,
        "ai_opportunity_map.csv": ai_map_path,
        "ai_readiness_scorecard.md": readiness_path,
        "strategic_plan.md": strategic_path,
        "implementation_roadmap.md": implementation_path,
        "roi_model.csv": roi_path,
        "executive_summary.md": executive_path,
        "kpi_dashboard.json": kpi_path,
        "workforce_dashboard.html": dashboard_path,
    }


def main() -> None:
    outputs = generate_strategy()
    for name, path in outputs.items():
        print(f"{name}: {path}")  # noqa: T201


if __name__ == "__main__":
    main()
