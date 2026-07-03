"""Trace quality scoring for curated memory."""

from __future__ import annotations

from human_exe.models.workflow import WorkflowTrace


def score_trace_quality(trace: WorkflowTrace) -> float:
    has_verification = 1.0 if trace.verification_results else 0.0
    has_supervisor = 1.0 if trace.supervisor_decisions else 0.0
    success = 1.0 if trace.final_status == "COMPLETED" else 0.0
    bounded_actions = 1.0 if len(trace.actions) <= 50 else 0.4
    score = (has_verification + has_supervisor + success + bounded_actions) / 4.0
    return round(score, 3)
