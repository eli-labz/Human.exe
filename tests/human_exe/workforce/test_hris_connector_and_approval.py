from pathlib import Path

import pytest

from human_exe.agents.supervisor_interface_agent import HumanSupervisionLayer
import human_exe.workforce.agents.workforce_data_agent as workforce_data_agent_module
from human_exe.workforce.agents.workforce_data_agent import WorkforceDataAgent
from human_exe.workforce.ingestion.hris_connector import HRISConnectorConfig


def test_authenticated_hris_ingestion_and_approval(tmp_path: Path) -> None:
    export = tmp_path / "hris.csv"
    export.write_text("employee_id,role,task_volume\nE1,Analyst,120\n", encoding="utf-8")

    agent = WorkforceDataAgent()
    supervision = HumanSupervisionLayer(tmp_path / "audit" / "audit.jsonl")

    records = agent.ingest_from_authenticated_hris(
        connector_config=HRISConnectorConfig(
            connector_name="demo",
            export_root=tmp_path,
            client_id="cid",
            client_secret="secret",
        ),
        export_name="hris.csv",
        client_id="cid",
        client_secret="secret",
        hr_analytics_mode=True,
        supervision_layer=supervision,
        auto_approve_hr_mode=True,
    )

    assert records
    assert "employee_id" in records[0]


def test_hr_analytics_mode_requires_explicit_approval(tmp_path: Path) -> None:
    data = tmp_path / "input.csv"
    data.write_text("employee_id,role,task_volume\nE1,Analyst,120\n", encoding="utf-8")

    agent = WorkforceDataAgent()
    supervision = HumanSupervisionLayer(tmp_path / "audit" / "audit.jsonl")

    with pytest.raises(PermissionError):
        agent.ingest(
            data,
            hr_analytics_mode=True,
            supervision_layer=supervision,
            auto_approve_hr_mode=False,
        )


def test_hr_analytics_mode_console_api_requires_credentials(tmp_path: Path) -> None:
    data = tmp_path / "input.csv"
    data.write_text("employee_id,role,task_volume\nE1,Analyst,120\n", encoding="utf-8")

    with pytest.raises(PermissionError):
        WorkforceDataAgent().ingest(
            data,
            hr_analytics_mode=True,
            use_console_api_approval=True,
            console_api_base_url=None,
            console_api_token=None,
        )


def test_hr_analytics_mode_console_api_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    data = tmp_path / "input.csv"
    data.write_text("employee_id,role,task_volume\nE1,Analyst,120\n", encoding="utf-8")

    calls: list[dict[str, object]] = []

    def fake_console_approval(**kwargs: object) -> str:
        calls.append(dict(kwargs))
        return "APPROVE"

    monkeypatch.setattr(
        workforce_data_agent_module,
        "request_hr_analytics_approval_via_console_api",
        fake_console_approval,
    )

    records = WorkforceDataAgent().ingest(
        data,
        hr_analytics_mode=True,
        use_console_api_approval=True,
        console_api_base_url="http://localhost:8765",
        console_api_token="token-1",
        requested_by="qa-test",
    )

    assert calls
    assert records
    assert "employee_id" in records[0]
