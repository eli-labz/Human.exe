"""Browser adapter with bounded simulated actions for tests and local demo."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class BrowserAdapter:
    allow_live_actions: bool = False

    def observe(self) -> dict[str, Any]:
        return {"active_url": "about:blank", "dom_summary": "sandbox"}

    def open_url(self, url: str) -> dict[str, Any]:
        if not self.allow_live_actions:
            return {"status": "sandbox", "url": url}
        return {"status": "opened", "url": url}

    def click(self, selector: str) -> dict[str, Any]:
        return {"status": "clicked", "selector": selector}
