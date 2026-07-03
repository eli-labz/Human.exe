"""Computer-use crew orchestration."""

from __future__ import annotations

from human_exe.agents.computer_use_agent import ComputerUseAgent
from human_exe.agents.verification_agent import VerificationAgent


class ComputerUseCrew:
    def __init__(self) -> None:
        self.computer_agent = ComputerUseAgent()
        self.verifier = VerificationAgent()
