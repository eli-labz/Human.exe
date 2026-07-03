"""Desktop adapter with bounded no-op execution by default."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class DesktopAdapter:
    sandbox_mode: bool = True

    def open_app(self, app_name: str) -> dict[str, str]:
        state = "sandbox_open" if self.sandbox_mode else "opened"
        return {"status": state, "app": app_name}

    def close_app(self, app_name: str) -> dict[str, str]:
        state = "sandbox_close" if self.sandbox_mode else "closed"
        return {"status": state, "app": app_name}

    def type_text(self, text: str) -> dict[str, str]:
        return {"status": "typed", "length": str(len(text))}
