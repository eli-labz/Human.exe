"""Text task crew composition."""

from __future__ import annotations

from human_exe.agents.text_task_agent import TextTaskAgent
from human_exe.agents.verification_agent import VerificationAgent


class TextTaskCrew:
    def __init__(self) -> None:
        self.text_agent = TextTaskAgent()
        self.verifier = VerificationAgent()

    def summarize_and_draft(self, content: str, recipient: str) -> dict[str, object]:
        summary = self.text_agent.summarize(content)
        draft = self.text_agent.draft_email(summary, recipient)
        verification = self.verifier.verify_text(draft)
        return {"summary": summary, "draft": draft, "verification": verification}
