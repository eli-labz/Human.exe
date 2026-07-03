"""Authenticated HRIS connector flow for workforce data ingestion."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
from uuid import uuid4

from human_exe.workforce.ingestion.hris_loader import load_hris_export


@dataclass(slots=True)
class HRISConnectorConfig:
    connector_name: str
    export_root: Path
    client_id: str
    client_secret: str


@dataclass(slots=True)
class HRISSession:
    access_token: str
    connector_name: str


class HRISConnectorClient:
    """Local authenticated connector wrapper for HRIS export ingestion.

    This client models an auth flow and export fetch lifecycle so production connectors
    can replace local filesystem reads without changing caller orchestration.
    """

    def __init__(self, config: HRISConnectorConfig) -> None:
        self.config = config
        self.session: HRISSession | None = None

    def authenticate(self, client_id: str, client_secret: str) -> HRISSession:
        if client_id != self.config.client_id or client_secret != self.config.client_secret:
            raise PermissionError("invalid_hris_credentials")
        self.session = HRISSession(access_token=str(uuid4()), connector_name=self.config.connector_name)
        return self.session

    def fetch_export(self, export_name: str) -> list[dict[str, Any]]:
        if self.session is None:
            raise PermissionError("hris_session_required")
        path = self.config.export_root / export_name
        if not path.exists():
            raise FileNotFoundError(path)
        return load_hris_export(path)
