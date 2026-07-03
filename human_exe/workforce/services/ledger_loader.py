"""Financial ledger ingestion helpers for ROI grounding."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class LedgerEntry:
    period: str
    account: str
    category: str
    amount: float


def load_ledger_entries(path: Path) -> list[LedgerEntry]:
    entries: list[LedgerEntry] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            entries.append(
                LedgerEntry(
                    period=str(row.get("period", "")),
                    account=str(row.get("account", "")),
                    category=str(row.get("category", "other")).lower(),
                    amount=float(row.get("amount", 0.0)),
                )
            )
    return entries


def estimate_baseline_cost_from_ledger(entries: list[LedgerEntry]) -> float:
    relevant = {"labor", "overtime", "rework", "operations", "support"}
    total = sum(entry.amount for entry in entries if entry.category in relevant)
    return round(total, 2)
