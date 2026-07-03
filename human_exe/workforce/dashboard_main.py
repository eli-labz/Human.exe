"""Serve generated workforce demo dashboard artifacts."""

from __future__ import annotations

from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


def run_dashboard(artifacts_dir: Path, host: str = "127.0.0.1", port: int = 8787) -> None:
    if not artifacts_dir.exists():
        raise FileNotFoundError(artifacts_dir)

    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(artifacts_dir), **kwargs)

    server = ThreadingHTTPServer((host, port), Handler)
    print(f"Workforce dashboard available at http://{host}:{port}/workforce_dashboard.html")  # noqa: T201
    server.serve_forever()


def main() -> None:
    run_dashboard(Path(".artifacts/human_exe/workforce_demo"))


if __name__ == "__main__":
    main()
