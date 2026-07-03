"""Text task agent for deterministic summarization and drafting."""

from __future__ import annotations


class TextTaskAgent:
    def summarize(self, content: str, max_sentences: int = 3) -> str:
        sentences = [s.strip() for s in content.replace("\n", " ").split(".") if s.strip()]
        selected = sentences[:max_sentences]
        if not selected:
            return "No meaningful content found."
        return ". ".join(selected) + "."

    def draft_email(self, summary: str, recipient: str) -> str:
        return (
            f"To: {recipient}\n"
            "Subject: Document Summary Draft\n\n"
            "Hello,\n\n"
            f"Here is the requested summary:\n{summary}\n\n"
            "Please review and advise if any changes are needed.\n"
        )
