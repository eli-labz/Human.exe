"""HRIS export loader wrapper (CSV/JSON/XLSX)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from human_exe.workforce.ingestion.csv_loader import load_csv
from human_exe.workforce.ingestion.excel_loader import load_excel
from human_exe.workforce.ingestion.json_loader import load_json


def load_hris_export(path: Path) -> list[dict[str, Any]]:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return load_csv(path)
    if suffix in {".xlsx", ".xlsm"}:
        return load_excel(path)
    if suffix == ".json":
        return load_json(path)
    raise ValueError(f"Unsupported HRIS export format: {suffix}")
