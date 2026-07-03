"""Workforce data ingestion and normalization agent."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from human_exe.agents.supervisor_interface_agent import HumanSupervisionLayer
from human_exe.workforce.ingestion.csv_loader import load_csv
from human_exe.workforce.ingestion.excel_loader import load_excel
from human_exe.workforce.ingestion.hris_connector import HRISConnectorClient, HRISConnectorConfig
from human_exe.workforce.ingestion.json_loader import load_json
from human_exe.workforce.ingestion.schema_mapper import normalize_records
from human_exe.workforce.services.hr_analytics_approval import request_hr_analytics_approval
from human_exe.workforce.services.hr_analytics_approval import request_hr_analytics_approval_via_console_api
from human_exe.workforce.services.workforce_privacy_guard import enforce_aggregate_mode


class WorkforceDataAgent:
    def ingest(
        self,
        path: Path,
        hr_analytics_mode: bool = False,
        supervision_layer: HumanSupervisionLayer | None = None,
        use_console_api_approval: bool = False,
        console_api_base_url: str | None = None,
        console_api_token: str | None = None,
        approval_timeout_seconds: int = 120,
        supervisor_id: str = "workforce-supervisor",
        requested_by: str = "workforce-data-agent",
        auto_approve_hr_mode: bool = False,
    ) -> list[dict[str, Any]]:
        if hr_analytics_mode:
            if use_console_api_approval:
                if not console_api_base_url or not console_api_token:
                    raise PermissionError("console_api_approval_requires_base_url_and_token")
                request_hr_analytics_approval_via_console_api(
                    console_base_url=console_api_base_url,
                    token=console_api_token,
                    requested_by=requested_by,
                    purpose=f"Enable approved HR analytics mode for dataset {path.name}",
                    timeout_seconds=approval_timeout_seconds,
                )
            else:
                if supervision_layer is None:
                    raise PermissionError("hr_analytics_mode_requires_supervision_layer")
                request_hr_analytics_approval(
                    supervision_layer=supervision_layer,
                    supervisor_id=supervisor_id,
                    requested_by=requested_by,
                    purpose=f"Enable approved HR analytics mode for dataset {path.name}",
                    auto_approve=auto_approve_hr_mode,
                )

        suffix = path.suffix.lower()
        if suffix == ".csv":
            records = load_csv(path)
        elif suffix in {".xlsx", ".xlsm"}:
            records = load_excel(path)
        elif suffix == ".json":
            records = load_json(path)
        else:
            raise ValueError(f"Unsupported file format: {suffix}")
        normalized = normalize_records(records)
        return enforce_aggregate_mode(normalized, hr_analytics_mode=hr_analytics_mode)

    def ingest_from_authenticated_hris(
        self,
        connector_config: HRISConnectorConfig,
        export_name: str,
        client_id: str,
        client_secret: str,
        hr_analytics_mode: bool = False,
        supervision_layer: HumanSupervisionLayer | None = None,
        use_console_api_approval: bool = False,
        console_api_base_url: str | None = None,
        console_api_token: str | None = None,
        approval_timeout_seconds: int = 120,
        auto_approve_hr_mode: bool = False,
    ) -> list[dict[str, Any]]:
        if hr_analytics_mode:
            if use_console_api_approval:
                if not console_api_base_url or not console_api_token:
                    raise PermissionError("console_api_approval_requires_base_url_and_token")
                request_hr_analytics_approval_via_console_api(
                    console_base_url=console_api_base_url,
                    token=console_api_token,
                    requested_by="workforce-data-agent",
                    purpose="Enable approved HR analytics mode for HRIS connector export.",
                    timeout_seconds=approval_timeout_seconds,
                )
            else:
                if supervision_layer is None:
                    raise PermissionError("hr_analytics_mode_requires_supervision_layer")
                request_hr_analytics_approval(
                    supervision_layer=supervision_layer,
                    supervisor_id="workforce-supervisor",
                    requested_by="workforce-data-agent",
                    purpose="Enable approved HR analytics mode for HRIS connector export.",
                    auto_approve=auto_approve_hr_mode,
                )

        connector = HRISConnectorClient(connector_config)
        connector.authenticate(client_id=client_id, client_secret=client_secret)
        records = connector.fetch_export(export_name)
        normalized = normalize_records(records)
        return enforce_aggregate_mode(normalized, hr_analytics_mode=hr_analytics_mode)
