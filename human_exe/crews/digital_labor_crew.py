"""Top-level supervised digital labor crew."""

from __future__ import annotations

from pathlib import Path

from human_exe.agents.memory_agent import MemoryAgent
from human_exe.agents.planner_agent import PlannerAgent
from human_exe.agents.risk_gate_agent import RiskGateAgent
from human_exe.agents.supervisor_interface_agent import HumanSupervisionLayer
from human_exe.crews.computer_use_crew import ComputerUseCrew
from human_exe.crews.text_task_crew import TextTaskCrew


class DigitalLaborCrew:
    def __init__(self, artifacts_root: Path) -> None:
        self.planner = PlannerAgent()
        self.text_crew = TextTaskCrew()
        self.computer_crew = ComputerUseCrew()
        self.risk_gate = RiskGateAgent()
        self.memory = MemoryAgent(artifacts_root / "traces")
        self.supervision = HumanSupervisionLayer(artifacts_root / "audit" / "audit.jsonl")
