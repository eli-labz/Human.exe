"""Privacy guardrails for responsible workforce analytics outputs."""

from __future__ import annotations

from copy import deepcopy
from typing import Any


PROHIBITED_RECOMMENDATION_TERMS = {
    "terminate",
    "firing",
    "fire",
    "demote",
    "pay cut",
    "salary reduction",
    "adverse employment action",
}

PROTECTED_FIELDS = {
    "race",
    "ethnicity",
    "religion",
    "gender",
    "sex",
    "age",
    "disability",
    "pregnancy",
    "sexual_orientation",
    "national_origin",
}


def enforce_aggregate_mode(records: list[dict[str, Any]], hr_analytics_mode: bool = False) -> list[dict[str, Any]]:
    sanitized: list[dict[str, Any]] = []
    for record in records:
        row = deepcopy(record)
        for field in list(row.keys()):
            key = str(field).strip().lower()
            if key in PROTECTED_FIELDS:
                row.pop(field, None)
            if not hr_analytics_mode and key in {"employee_id", "employee_name", "email"}:
                row.pop(field, None)
        sanitized.append(row)
    return sanitized


def validate_recommendation_text(text: str) -> None:
    lowered = text.lower()
    for term in PROHIBITED_RECOMMENDATION_TERMS:
        if term in lowered:
            raise ValueError(f"Unsafe workforce recommendation blocked: {term}")
