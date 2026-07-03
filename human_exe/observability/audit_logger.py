"""Immutable audit logger with hash chaining."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


class AuditLogger:
    def __init__(self, log_file: Path) -> None:
        self.log_file = log_file
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        self._last_hash = "GENESIS"

    def log(self, event_type: str, payload: dict[str, Any]) -> dict[str, Any]:
        entry = {"event_type": event_type, "payload": payload, "previous_hash": self._last_hash}
        raw = json.dumps(entry, sort_keys=True).encode("utf-8")
        current_hash = hashlib.sha256(raw).hexdigest()
        entry["hash"] = current_hash
        with self.log_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, sort_keys=True) + "\n")
        self._last_hash = current_hash
        return entry
