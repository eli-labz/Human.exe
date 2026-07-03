"""Workflow trace persistence for curated memory."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from human_exe.memory.trace_quality import score_trace_quality
from human_exe.models.workflow import WorkflowTrace


class TraceStore:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def save_trace(self, trace: WorkflowTrace) -> Path:
        trace.trace_quality_score = score_trace_quality(trace)
        trace.mark_updated()
        file_path = self.root / f"{trace.workflow_id}.json"
        file_path.write_text(json.dumps(asdict(trace), indent=2), encoding="utf-8")
        return file_path
