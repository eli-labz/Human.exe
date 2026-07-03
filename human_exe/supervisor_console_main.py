"""CLI entrypoint for the Human.exe supervisor web console."""

from __future__ import annotations

import argparse
from pathlib import Path

from human_exe.agents.supervisor_interface_agent import HumanSupervisionLayer
from human_exe.supervisor_console.server import run_supervisor_console


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Human.exe supervisor web console")
    parser.add_argument(
        "--artifacts-root",
        type=Path,
        default=Path(".artifacts/human_exe"),
        help="Artifacts root containing audit and trace files",
    )
    parser.add_argument("--host", type=str, default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument(
        "--users-file",
        type=Path,
        default=Path("human_exe/config/supervisor_users.yaml"),
        help="YAML file containing console usernames, passwords, and roles",
    )
    args = parser.parse_args()

    supervision = HumanSupervisionLayer(args.artifacts_root / "audit" / "audit.jsonl")
    run_supervisor_console(
        supervision=supervision,
        traces_dir=args.artifacts_root / "traces",
        users_file=args.users_file,
        host=args.host,
        port=args.port,
    )


if __name__ == "__main__":
    main()
