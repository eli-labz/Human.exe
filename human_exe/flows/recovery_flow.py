"""Bounded recovery flow."""

from __future__ import annotations


def run_recovery_flow(failure_reason: str, max_attempts: int = 2) -> dict[str, object]:
    attempts = min(max_attempts, 2)
    if attempts <= 0:
        return {"recovered": False, "steps": ["escalate"]}
    return {
        "recovered": False,
        "steps": [f"retry_{i + 1}" for i in range(attempts)] + ["escalate"],
        "reason": failure_reason,
    }
