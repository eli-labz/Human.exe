"""CSV workforce data loader."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


def load_csv(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return [dict(row) for row in reader]
