"""Verification agent."""

from __future__ import annotations

from human_exe.tools.verification_tools import verify_action_result, verify_non_empty_text


class VerificationAgent:
    def verify_text(self, text: str) -> dict[str, object]:
        return verify_non_empty_text(text)

    def verify_action(self, result: dict[str, object]) -> dict[str, object]:
        return verify_action_result(result)
