"""File adapter for bounded local file operations."""

from __future__ import annotations

from pathlib import Path


class FileAdapter:
    def read_file(self, path: Path) -> str:
        return path.read_text(encoding="utf-8")

    def write_file(self, path: Path, content: str) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def create_document(self, path: Path, content: str) -> Path:
        return self.write_file(path, content)
