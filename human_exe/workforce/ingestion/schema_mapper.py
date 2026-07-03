"""Schema mapper for normalized workforce records."""

from __future__ import annotations

from typing import Any


COMMON_FIELD_ALIASES: dict[str, str] = {
    "department": "department_name",
    "dept": "department_name",
    "role": "role_title",
    "job_title": "role_title",
    "tasks_per_week": "task_volume",
    "volume": "task_volume",
    "cycle_time": "cycle_time_hours",
    "cycle_time_h": "cycle_time_hours",
    "error_pct": "error_rate",
    "rework_pct": "rework_rate",
    "handoffs": "manual_handoffs",
    "tool": "system_name",
    "system": "system_name",
    "overtime_pct": "overtime_ratio",
}


def normalize_record(record: dict[str, Any]) -> dict[str, Any]:
    normalized: dict[str, Any] = {}
    for key, value in record.items():
        key_clean = str(key).strip().lower()
        mapped_key = COMMON_FIELD_ALIASES.get(key_clean, key_clean)
        normalized[mapped_key] = value
    return normalized


def normalize_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [normalize_record(record) for record in records]
