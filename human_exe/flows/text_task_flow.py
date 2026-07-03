"""Flow for text-centric tasks."""

from __future__ import annotations

from human_exe.crews.text_task_crew import TextTaskCrew


def run_text_task_flow(content: str, recipient: str) -> dict[str, object]:
    crew = TextTaskCrew()
    return crew.summarize_and_draft(content, recipient)
