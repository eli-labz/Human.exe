"""Verification primitives for action outcomes."""

from __future__ import annotations

from typing import Any


def verify_non_empty_text(content: str) -> dict[str, Any]:
    passed = bool(content.strip())
    return {"check": "non_empty_text", "passed": passed}


def verify_action_result(result: dict[str, Any]) -> dict[str, Any]:
    passed = "status" in result and result.get("status") not in {"error", None}
    return {"check": "action_result_status", "passed": passed}
