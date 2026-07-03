"""Dependency checks for workforce ingestion paths."""

from __future__ import annotations


def ensure_openpyxl_available() -> None:
    try:
        import openpyxl  # noqa: F401
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError(
            "Excel ingestion requires openpyxl. Install with: uv add --dev openpyxl~=3.1.5"
        ) from exc
