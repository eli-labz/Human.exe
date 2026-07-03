"""Memory agent for saving and querying curated traces."""

from __future__ import annotations

from pathlib import Path

from human_exe.memory.trace_store import TraceStore
from human_exe.memory.vector_memory import VectorMemory
from human_exe.models.workflow import WorkflowTrace


class MemoryAgent:
    def __init__(self, root: Path) -> None:
        self.trace_store = TraceStore(root)
        self.vector_memory = VectorMemory(root)

    def save(self, trace: WorkflowTrace) -> Path:
        return self.trace_store.save_trace(trace)

    def search(self, query: str) -> list[dict[str, object]]:
        return self.vector_memory.search(query)
