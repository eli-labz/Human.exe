"""CLI helper to run the supervised Human.exe demo workflow."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from human_exe.flows.computer_use_flow import run_demo_workflow


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Human.exe supervised digital labor demo")
    parser.add_argument("--document", type=Path, required=True, help="Path to input document")
    parser.add_argument("--recipient", type=str, required=True, help="Email recipient for draft")
    parser.add_argument(
        "--artifacts-root",
        type=Path,
        default=Path(".artifacts/human_exe"),
        help="Directory for traces, audit logs, and reports",
    )
    parser.add_argument("--supervisor-id", type=str, default="supervisor-1")
    args = parser.parse_args()

    result = run_demo_workflow(
        document_path=args.document,
        recipient=args.recipient,
        supervisor_id=args.supervisor_id,
        artifacts_root=args.artifacts_root,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
