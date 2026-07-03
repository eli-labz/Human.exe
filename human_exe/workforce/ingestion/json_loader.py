"""JSON workforce data loader."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    if isinstance(data, dict):
        if isinstance(data.get("records"), list):
            return [item for item in data["records"] if isinstance(item, dict)]
        return [data]
    return []
