"""Exports opportunity, ROI, and KPI artifacts."""

from __future__ import annotations

import csv
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any


def export_csv(records: list[dict[str, Any]], output_file: Path) -> Path:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    if not records:
        output_file.write_text("", encoding="utf-8")
        return output_file
    fieldnames = sorted({key for record in records for key in record.keys()})
    with output_file.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for record in records:
            writer.writerow(record)
    return output_file


def export_json(payload: dict[str, Any], output_file: Path) -> Path:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return output_file


def models_to_dicts(models: list[object]) -> list[dict[str, Any]]:
    return [asdict(item) for item in models]
