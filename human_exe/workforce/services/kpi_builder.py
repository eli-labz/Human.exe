"""KPI model builder for workforce transformation tracking."""

from __future__ import annotations

from human_exe.workforce.models.workforce import KPI


def build_kpis() -> list[KPI]:
    return [
        KPI("task_completion_rate", 0.0, 0.92, "ratio", "Operations"),
        KPI("cycle_time_reduction", 0.0, 0.25, "percent", "Process Excellence"),
        KPI("hours_redirected_to_higher_value_work", 0.0, 1200.0, "hours/quarter", "Department Leads"),
        KPI("error_reduction", 0.0, 0.3, "percent", "Quality"),
        KPI("rework_reduction", 0.0, 0.25, "percent", "Quality"),
        KPI("ai_adoption_rate", 0.0, 0.7, "ratio", "Transformation Office"),
        KPI("ai_output_review_quality", 0.0, 0.9, "ratio", "Governance Council"),
        KPI("human_override_rate", 0.0, 0.1, "ratio", "Supervisor Team"),
        KPI("escalation_rate", 0.0, 0.08, "ratio", "Supervisor Team"),
        KPI("policy_violation_rate", 0.0, 0.01, "ratio", "Governance Council"),
        KPI("employee_confidence_score", 0.0, 0.8, "index", "HR Enablement"),
        KPI("customer_impact_score", 0.0, 0.85, "index", "CX"),
    ]
