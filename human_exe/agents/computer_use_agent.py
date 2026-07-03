"""Computer-use agent with bounded supervised execution."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from human_exe.models.tokens import ActionType, HumanActionToken, OutcomeToken, PerceptionToken
from human_exe.tools.browser_tools import BrowserAdapter
from human_exe.tools.desktop_tools import DesktopAdapter
from human_exe.tools.file_tools import FileAdapter
from human_exe.tools.observation_tools import AccessibilityAdapter, ScreenshotAdapter
from human_exe.tools.verification_tools import verify_action_result


@dataclass(slots=True)
class ExecutionResult:
    perception: PerceptionToken
    action: HumanActionToken
    outcome: OutcomeToken


class ComputerUseAgent:
    def __init__(self) -> None:
        self.browser = BrowserAdapter()
        self.desktop = DesktopAdapter()
        self.files = FileAdapter()
        self.accessibility = AccessibilityAdapter()
        self.screenshots = ScreenshotAdapter()

    def observe(self, task_id: str) -> PerceptionToken:
        state = {
            "browser": self.browser.observe(),
            "accessibility": self.accessibility.get_ui_tree(),
        }
        metadata = self.screenshots.capture_metadata(Path(".artifacts/screenshot-meta.txt"))
        return PerceptionToken(
            task_id=task_id,
            source="computer_use_agent",
            state=state,
            screenshot_metadata=metadata,
        )

    def execute(self, action: HumanActionToken, max_retries: int = 2) -> OutcomeToken:
        last_error: str | None = None
        for _ in range(max_retries + 1):
            try:
                result = self._dispatch(action)
                verification = verify_action_result(result)
                if verification["passed"]:
                    return OutcomeToken(
                        task_id=action.task_id,
                        action_token_id=action.token_id,
                        success=True,
                        verification_passed=True,
                        result=result,
                    )
                last_error = "Verification failed"
            except ValueError as exc:
                last_error = str(exc)
                break
        return OutcomeToken(
            task_id=action.task_id,
            action_token_id=action.token_id,
            success=False,
            verification_passed=False,
            result={"status": "error"},
            error=last_error,
        )

    def _dispatch(self, action: HumanActionToken) -> dict[str, Any]:
        if action.action_type == ActionType.OPEN_URL:
            return self.browser.open_url(str(action.parameters.get("url", "about:blank")))
        if action.action_type == ActionType.CLICK:
            return self.browser.click(str(action.parameters.get("selector", "body")))
        if action.action_type == ActionType.TYPE_TEXT:
            return self.desktop.type_text(str(action.parameters.get("text", "")))
        if action.action_type == ActionType.OPEN_APP:
            return self.desktop.open_app(str(action.parameters.get("app", "unknown")))
        if action.action_type == ActionType.CLOSE_APP:
            return self.desktop.close_app(str(action.parameters.get("app", "unknown")))
        raise ValueError(f"Unsupported action: {action.action_type.value}")
