"""Observation adapters for accessibility and screenshot metadata."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class AccessibilityAdapter:
    def get_ui_tree(self) -> dict[str, Any]:
        return {"window": "sandbox", "nodes": 1, "focused": "main"}


@dataclass(slots=True)
class ScreenshotAdapter:
    store_sensitive_data: bool = False

    def capture_metadata(self, path: Path) -> dict[str, Any]:
        metadata = {"path": str(path), "stored": False, "sensitive_storage": self.store_sensitive_data}
        if self.store_sensitive_data:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("screenshot-bytes-redacted", encoding="utf-8")
            metadata["stored"] = True
        return metadata
