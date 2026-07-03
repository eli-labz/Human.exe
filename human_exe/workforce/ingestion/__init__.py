"""Workforce data ingestion utilities."""

from human_exe.workforce.ingestion.csv_loader import load_csv
from human_exe.workforce.ingestion.dependency_check import ensure_openpyxl_available
from human_exe.workforce.ingestion.excel_loader import load_excel
from human_exe.workforce.ingestion.hris_connector import HRISConnectorClient, HRISConnectorConfig
from human_exe.workforce.ingestion.hris_loader import load_hris_export
from human_exe.workforce.ingestion.json_loader import load_json
from human_exe.workforce.ingestion.schema_mapper import normalize_record, normalize_records

__all__ = [
    "load_csv",
    "ensure_openpyxl_available",
    "load_excel",
    "HRISConnectorClient",
    "HRISConnectorConfig",
    "load_hris_export",
    "load_json",
    "normalize_record",
    "normalize_records",
]
