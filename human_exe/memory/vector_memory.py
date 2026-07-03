"""Lightweight trace retrieval based on token overlap."""

from __future__ import annotations

import json
from pathlib import Path


class VectorMemory:
    def __init__(self, store_root: Path) -> None:
        self.store_root = store_root

    def search(self, query: str, top_k: int = 3) -> list[dict[str, object]]:
        query_tokens = set(query.lower().split())
        scored: list[tuple[float, dict[str, object]]] = []
        for item in self.store_root.glob("*.json"):
            payload = json.loads(item.read_text(encoding="utf-8"))
            objective = str(payload.get("intent", {}).get("objective", ""))
            tokens = set(objective.lower().split())
            if not tokens:
                continue
            overlap = len(query_tokens & tokens) / len(tokens)
            scored.append((overlap, payload))
        scored.sort(key=lambda row: row[0], reverse=True)
        return [payload for _, payload in scored[:top_k]]
