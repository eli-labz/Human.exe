"""Minimal supervisor web console server.

Provides RBAC login, approval queue operations, audit visibility,
trace browsing, and live SSE updates.
"""

from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from datetime import UTC, datetime
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler
from http.server import ThreadingHTTPServer
import json
from pathlib import Path
import threading
from time import sleep
from typing import Any
from urllib.parse import parse_qs
from urllib.parse import urlparse
from uuid import uuid4

from human_exe.agents.supervisor_interface_agent import HumanSupervisionLayer
from human_exe.models.supervision import ApprovalRequest
from human_exe.models.supervision import DecisionType
from human_exe.models.supervision import SupervisorDecision

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


_ROLE_PERMISSIONS: dict[str, set[str]] = {
    "supervisor": {
        "queue.read",
        "audit.read",
        "trace.read",
        "request.create",
        "decision.approve",
        "decision.reject",
        "decision.modify",
        "decision.override",
    },
    "auditor": {
        "queue.read",
        "audit.read",
        "trace.read",
    },
}


@dataclass(slots=True)
class ConsoleState:
    supervision: HumanSupervisionLayer
    traces_dir: Path
    lock: threading.Lock


@dataclass(slots=True)
class AuthSession:
    token: str
    username: str
    role: str
    created_at: str


class ConsoleAuth:
    """Simple in-memory session auth with RBAC checks."""

    def __init__(self, users_file: Path | None = None) -> None:
        self._users = self._load_users(users_file)
        self._sessions: dict[str, AuthSession] = {}

    @staticmethod
    def _load_users(users_file: Path | None) -> dict[str, dict[str, str]]:
        if users_file and users_file.exists() and yaml is not None:
            parsed = yaml.safe_load(users_file.read_text(encoding="utf-8"))
            if isinstance(parsed, dict) and isinstance(parsed.get("users"), list):
                out: dict[str, dict[str, str]] = {}
                for item in parsed["users"]:
                    if isinstance(item, dict):
                        username = str(item.get("username", "")).strip()
                        password = str(item.get("password", ""))
                        role = str(item.get("role", "auditor"))
                        if username:
                            out[username] = {"password": password, "role": role}
                if out:
                    return out
        # Demo-safe fallback credential, suitable only for local MVP.
        return {
            "admin": {"password": "admin", "role": "supervisor"},
            "auditor": {"password": "auditor", "role": "auditor"},
        }

    def login(self, username: str, password: str) -> dict[str, str]:
        user = self._users.get(username)
        if user is None or user.get("password") != password:
            raise PermissionError("invalid_credentials")
        token = str(uuid4())
        role = str(user.get("role", "auditor"))
        self._sessions[token] = AuthSession(
            token=token,
            username=username,
            role=role,
            created_at=datetime.now(UTC).isoformat(),
        )
        return {"token": token, "role": role, "username": username}

    def authorize(self, token: str | None, permission: str) -> bool:
        if not token:
            return False
        session = self._sessions.get(token)
        if session is None:
            return False
        allowed = _ROLE_PERMISSIONS.get(session.role, set())
        return permission in allowed


class SupervisorConsoleService:
    def __init__(self, supervision: HumanSupervisionLayer, traces_dir: Path) -> None:
        self.supervision = supervision
        self.traces_dir = traces_dir
        self.lock = threading.Lock()
        self._event_lock = threading.Lock()
        self._event_id = 0
        self._events: list[dict[str, object]] = []

    def _publish(self, event_type: str, payload: dict[str, object]) -> None:
        with self._event_lock:
            self._event_id += 1
            event = {"id": self._event_id, "type": event_type, "payload": payload}
            self._events.append(event)
            if len(self._events) > 500:
                self._events = self._events[-500:]

    def list_events_since(self, since_id: int) -> list[dict[str, object]]:
        with self._event_lock:
            return [e for e in self._events if int(e["id"]) > since_id]

    def list_queue(self) -> dict[str, object]:
        with self.lock:
            items = self.supervision.list_requests()
        return {"items": items, "count": len(items)}

    def list_audit(self, limit: int = 100) -> dict[str, object]:
        items = _read_json_lines(self.supervision.audit_logger.log_file, limit=limit)
        return {"items": items, "count": len(items)}

    def list_traces(self, limit: int = 20) -> dict[str, object]:
        items = _list_traces(self.traces_dir, limit=limit)
        return {"items": items, "count": len(items)}

    def get_trace(self, workflow_id: str) -> dict[str, object]:
        return {"trace": _load_trace(self.traces_dir, workflow_id)}

    def submit_decision(
        self,
        request_id: str,
        supervisor_id: str,
        decision_raw: str,
        reason: str,
        modified_action: dict[str, Any] | None = None,
    ) -> dict[str, object]:
        decision_kind = DecisionType(decision_raw.upper())
        if decision_kind == DecisionType.MODIFY and not modified_action:
            raise ValueError("modified_action_required")

        decision = SupervisorDecision(
            request_id=request_id,
            supervisor_id=supervisor_id,
            decision=decision_kind,
            reason=reason,
            modified_action=modified_action,
        )
        with self.lock:
            resolved = self.supervision.resolve(request_id, decision)
        output = {"decision": asdict(resolved)}
        self._publish("decision_resolved", output)
        return output

    def create_request(
        self,
        workflow_id: str,
        action: dict[str, Any],
        risk_score: float,
        reason: str,
    ) -> dict[str, object]:
        approval = ApprovalRequest(
            workflow_id=workflow_id,
            action=action,
            risk_score=risk_score,
            reason=reason,
        )
        with self.lock:
            self.supervision.enqueue(approval)
        output = {"request": asdict(approval)}
        self._publish("request_created", output)
        return output


def _read_json_lines(path: Path, limit: int = 100) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8").splitlines()
    selected = lines[-max(1, limit):]
    records: list[dict[str, Any]] = []
    for line in selected:
        if line.strip():
            records.append(json.loads(line))
    return records


def _trace_summary(trace_data: dict[str, Any]) -> dict[str, Any]:
    return {
        "workflow_id": trace_data.get("workflow_id"),
        "final_status": trace_data.get("final_status"),
        "trace_quality_score": trace_data.get("trace_quality_score"),
        "updated_at": trace_data.get("updated_at"),
        "intent": trace_data.get("intent", {}).get("objective"),
    }


def _list_traces(traces_dir: Path, limit: int = 20) -> list[dict[str, Any]]:
    if not traces_dir.exists():
        return []
    files = sorted(traces_dir.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    summaries: list[dict[str, Any]] = []
    for file_path in files[: max(1, limit)]:
        data = json.loads(file_path.read_text(encoding="utf-8"))
        summaries.append(_trace_summary(data))
    return summaries


def _load_trace(traces_dir: Path, workflow_id: str) -> dict[str, Any]:
    path = traces_dir / f"{workflow_id}.json"
    if not path.exists():
        raise FileNotFoundError(workflow_id)
    return json.loads(path.read_text(encoding="utf-8"))


def _json_response(handler: BaseHTTPRequestHandler, status: HTTPStatus, body: dict[str, Any]) -> None:
    payload = json.dumps(body).encode("utf-8")
    handler.send_response(status.value)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(payload)))
    handler.end_headers()
    handler.wfile.write(payload)


def _html_response(handler: BaseHTTPRequestHandler, html: str) -> None:
    payload = html.encode("utf-8")
    handler.send_response(HTTPStatus.OK.value)
    handler.send_header("Content-Type", "text/html; charset=utf-8")
    handler.send_header("Content-Length", str(len(payload)))
    handler.end_headers()
    handler.wfile.write(payload)


def _read_json_body(handler: BaseHTTPRequestHandler) -> dict[str, Any]:
    length = int(handler.headers.get("Content-Length", "0"))
    raw = handler.rfile.read(length) if length > 0 else b"{}"
    data = json.loads(raw.decode("utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Body must be a JSON object")
    return data


def _parse_limit(query: str, fallback: int) -> int:
    parsed = parse_qs(query)
    raw = parsed.get("limit", [str(fallback)])[0]
    return max(1, min(int(raw), 500)) if raw.isdigit() else fallback


def _extract_token(handler: BaseHTTPRequestHandler, query: dict[str, list[str]]) -> str | None:
    auth = handler.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        return auth.split(" ", 1)[1].strip()
    token_list = query.get("token", [])
    return token_list[0] if token_list else None


def _permission_for_decision(decision_raw: str) -> str:
    normalized = decision_raw.upper()
    if normalized == "APPROVE":
        return "decision.approve"
    if normalized == "REJECT":
        return "decision.reject"
    if normalized == "MODIFY":
        return "decision.modify"
    if normalized == "OVERRIDE":
        return "decision.override"
    raise ValueError("invalid_decision")


def _handler_factory(state: ConsoleState, auth: ConsoleAuth) -> type[BaseHTTPRequestHandler]:
    service = SupervisorConsoleService(state.supervision, state.traces_dir)

    class ConsoleHandler(BaseHTTPRequestHandler):
        def log_message(self, format: str, *args: Any) -> None:  # noqa: A003
            return

        def _authorize(self, query: dict[str, list[str]], permission: str) -> bool:
            token = _extract_token(self, query)
            return auth.authorize(token, permission)

        def do_GET(self) -> None:  # noqa: N802
            parsed = urlparse(self.path)
            path = parsed.path
            query = parse_qs(parsed.query)

            if path == "/":
                _html_response(self, _CONSOLE_HTML)
                return

            if path == "/api/events":
                if not self._authorize(query, "queue.read"):
                    _json_response(self, HTTPStatus.UNAUTHORIZED, {"error": "unauthorized"})
                    return
                since = int(query.get("since", ["0"])[0]) if query.get("since", ["0"])[0].isdigit() else 0
                self.send_response(HTTPStatus.OK.value)
                self.send_header("Content-Type", "text/event-stream")
                self.send_header("Cache-Control", "no-cache")
                self.send_header("Connection", "keep-alive")
                self.end_headers()
                current = since
                try:
                    for _ in range(30):
                        events = service.list_events_since(current)
                        if events:
                            for event in events:
                                current = int(event["id"])
                                payload = json.dumps(event)
                                self.wfile.write(f"id: {current}\n".encode("utf-8"))
                                self.wfile.write(b"event: update\n")
                                self.wfile.write(f"data: {payload}\n\n".encode("utf-8"))
                        else:
                            self.wfile.write(b": keepalive\n\n")
                        self.wfile.flush()
                        sleep(1)
                except BrokenPipeError:
                    return
                return

            if path == "/api/queue":
                if not self._authorize(query, "queue.read"):
                    _json_response(self, HTTPStatus.UNAUTHORIZED, {"error": "unauthorized"})
                    return
                _json_response(self, HTTPStatus.OK, service.list_queue())
                return

            if path == "/api/audit":
                if not self._authorize(query, "audit.read"):
                    _json_response(self, HTTPStatus.UNAUTHORIZED, {"error": "unauthorized"})
                    return
                limit = _parse_limit(parsed.query, fallback=100)
                _json_response(self, HTTPStatus.OK, service.list_audit(limit=limit))
                return

            if path == "/api/traces":
                if not self._authorize(query, "trace.read"):
                    _json_response(self, HTTPStatus.UNAUTHORIZED, {"error": "unauthorized"})
                    return
                limit = _parse_limit(parsed.query, fallback=20)
                _json_response(self, HTTPStatus.OK, service.list_traces(limit=limit))
                return

            if path.startswith("/api/traces/"):
                if not self._authorize(query, "trace.read"):
                    _json_response(self, HTTPStatus.UNAUTHORIZED, {"error": "unauthorized"})
                    return
                workflow_id = path.split("/api/traces/", 1)[1]
                try:
                    data = service.get_trace(workflow_id)
                except FileNotFoundError:
                    _json_response(self, HTTPStatus.NOT_FOUND, {"error": "trace_not_found"})
                    return
                _json_response(self, HTTPStatus.OK, data)
                return

            _json_response(self, HTTPStatus.NOT_FOUND, {"error": "not_found"})

        def do_POST(self) -> None:  # noqa: N802
            parsed = urlparse(self.path)
            path = parsed.path
            query = parse_qs(parsed.query)

            if path == "/api/login":
                try:
                    payload = _read_json_body(self)
                    username = str(payload["username"])
                    password = str(payload["password"])
                    session = auth.login(username, password)
                except KeyError as exc:
                    _json_response(self, HTTPStatus.BAD_REQUEST, {"error": f"missing_field:{exc.args[0]}"})
                    return
                except PermissionError:
                    _json_response(self, HTTPStatus.UNAUTHORIZED, {"error": "invalid_credentials"})
                    return
                _json_response(self, HTTPStatus.OK, session)
                return

            if path == "/api/requests":
                if not self._authorize(query, "request.create"):
                    _json_response(self, HTTPStatus.UNAUTHORIZED, {"error": "unauthorized"})
                    return
                try:
                    payload = _read_json_body(self)
                    workflow_id = str(payload["workflow_id"])
                    action = payload["action"]
                    risk_score = float(payload["risk_score"])
                    reason = str(payload.get("reason", "Approval required"))
                    if not isinstance(action, dict):
                        raise ValueError("action must be a JSON object")
                except KeyError as exc:
                    _json_response(self, HTTPStatus.BAD_REQUEST, {"error": f"missing_field:{exc.args[0]}"})
                    return
                except ValueError as exc:
                    _json_response(self, HTTPStatus.BAD_REQUEST, {"error": str(exc)})
                    return

                _json_response(
                    self,
                    HTTPStatus.CREATED,
                    service.create_request(
                        workflow_id=workflow_id,
                        action=action,
                        risk_score=risk_score,
                        reason=reason,
                    ),
                )
                return

            if path == "/api/decisions":
                try:
                    payload = _read_json_body(self)
                    decision_raw = str(payload["decision"]).upper()
                    permission = _permission_for_decision(decision_raw)
                except KeyError as exc:
                    _json_response(self, HTTPStatus.BAD_REQUEST, {"error": f"missing_field:{exc.args[0]}"})
                    return
                except ValueError as exc:
                    _json_response(self, HTTPStatus.BAD_REQUEST, {"error": str(exc)})
                    return

                if not self._authorize(query, permission):
                    _json_response(self, HTTPStatus.UNAUTHORIZED, {"error": "unauthorized"})
                    return

                try:
                    request_id = str(payload["request_id"])
                    supervisor_id = str(payload["supervisor_id"])
                    reason = str(payload.get("reason", "No reason provided"))
                    modified_action = payload.get("modified_action")
                except KeyError as exc:
                    _json_response(self, HTTPStatus.BAD_REQUEST, {"error": f"missing_field:{exc.args[0]}"})
                    return

                try:
                    response = service.submit_decision(
                        request_id=request_id,
                        supervisor_id=supervisor_id,
                        decision_raw=decision_raw,
                        reason=reason,
                        modified_action=modified_action if isinstance(modified_action, dict) else None,
                    )
                except ValueError as exc:
                    _json_response(self, HTTPStatus.BAD_REQUEST, {"error": str(exc)})
                    return

                _json_response(self, HTTPStatus.OK, response)
                return

            _json_response(self, HTTPStatus.NOT_FOUND, {"error": "not_found"})

    return ConsoleHandler


def create_server(
    supervision: HumanSupervisionLayer,
    traces_dir: Path,
    users_file: Path | None = None,
    host: str = "127.0.0.1",
    port: int = 8765,
) -> ThreadingHTTPServer:
    """Create a threaded HTTP server for the supervisor console."""
    state = ConsoleState(supervision=supervision, traces_dir=traces_dir, lock=threading.Lock())
    auth = ConsoleAuth(users_file=users_file)
    return ThreadingHTTPServer((host, port), _handler_factory(state, auth))


def run_supervisor_console(
    supervision: HumanSupervisionLayer,
    traces_dir: Path,
    users_file: Path | None = None,
    host: str = "127.0.0.1",
    port: int = 8765,
) -> None:
    """Start the supervisor console server and block forever."""
    server = create_server(
        supervision=supervision,
        traces_dir=traces_dir,
        users_file=users_file,
        host=host,
        port=port,
    )
    print(f"Supervisor console running on http://{host}:{port}")  # noqa: T201
    server.serve_forever()


_CONSOLE_HTML = """<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>Human.exe Supervisor Console</title>
  <style>
    :root {
      --bg: #eef2f8;
      --panel: #ffffff;
      --ink: #17233a;
      --line: #d5dfed;
      --ok: #0f7a5f;
      --warn: #9a5b00;
      --bad: #a01f38;
      --muted: #596d8e;
    }
    body {
      font-family: Segoe UI, Tahoma, sans-serif;
      background: radial-gradient(circle at 0 0, #d5e4ff 0%, var(--bg) 30%);
      margin: 0;
      padding: 16px;
      color: var(--ink);
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(330px, 1fr));
      gap: 12px;
    }
    .card {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 12px;
      padding: 12px;
      max-height: 76vh;
      overflow: auto;
    }
    .row {
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 8px;
      margin-bottom: 8px;
      background: #fcfdff;
    }
    .meta { color: var(--muted); font-size: 12px; }
    pre {
      white-space: pre-wrap;
      word-break: break-word;
      background: #101827;
      color: #dce7fb;
      border-radius: 8px;
      padding: 8px;
    }
    textarea {
      width: 100%;
      min-height: 110px;
      font-family: Consolas, monospace;
      font-size: 12px;
    }
    button {
      border: none;
      border-radius: 8px;
      padding: 6px 10px;
      color: #fff;
      cursor: pointer;
      margin-right: 6px;
      margin-top: 6px;
    }
    .ok { background: var(--ok); }
    .warn { background: var(--warn); }
    .bad { background: var(--bad); }
    .login {
      display: flex;
      gap: 8px;
      margin-bottom: 12px;
      align-items: center;
    }
    .login input { padding: 6px; }
    .hidden { display: none; }
    .diff-added { color: #9ef4b7; }
    .diff-removed { color: #ff9fb0; }
  </style>
</head>
<body>
  <h1>Human.exe Supervisor Console</h1>
  <div class=\"login\">
    <input id=\"username\" placeholder=\"username\" value=\"admin\" />
    <input id=\"password\" placeholder=\"password\" type=\"password\" value=\"admin\" />
    <button class=\"ok\" id=\"loginBtn\">Login</button>
    <span id=\"sessionMeta\" class=\"meta\">Not logged in</span>
  </div>
  <div class=\"grid\">
    <section class=\"card\">
      <h2>Approval Queue</h2>
      <div id=\"queue\"></div>
    </section>
    <section class=\"card\">
      <h2>Audit Log</h2>
      <div id=\"audit\"></div>
    </section>
    <section class=\"card\">
      <h2>Workflow Traces</h2>
      <div id=\"traces\"></div>
    </section>
  </div>

  <script>
    let token = null;
    let role = null;
    let eventSource = null;
    const supervisorId = \"console-supervisor\";

    function authHeaders() {
      return token ? {\"Authorization\": `Bearer ${token}`} : {};
    }

    async function getJSON(url) {
      const res = await fetch(url, {headers: authHeaders()});
      const data = await res.json();
      if (!res.ok) throw new Error(JSON.stringify(data));
      return data;
    }

    async function postJSON(url, body) {
      const res = await fetch(url, {
        method: 'POST',
        headers: Object.assign({\"Content-Type\": \"application/json\"}, authHeaders()),
        body: JSON.stringify(body)
      });
      const data = await res.json();
      if (!res.ok) throw new Error(JSON.stringify(data));
      return data;
    }

    function renderDiff(originalObj, modifiedObj) {
      const original = JSON.stringify(originalObj, null, 2).split('\\n');
      const modified = JSON.stringify(modifiedObj, null, 2).split('\\n');
      const removed = original.filter(line => !modified.includes(line)).map(line => `<div class=\"diff-removed\">- ${line}</div>`);
      const added = modified.filter(line => !original.includes(line)).map(line => `<div class=\"diff-added\">+ ${line}</div>`);
      if (!removed.length && !added.length) {
        return '<div class=\"meta\">No diff</div>';
      }
      return removed.concat(added).join('');
    }

    async function submitDecision(item, decision, modifiedAction) {
      const reason = prompt('Decision reason', `Console ${decision}`) || `Console ${decision}`;
      const body = {
        request_id: item.request_id,
        supervisor_id: supervisorId,
        decision,
        reason
      };
      if (decision === 'MODIFY') {
        body.modified_action = modifiedAction;
      }
      await postJSON('/api/decisions', body);
      await refreshAll();
    }

    function renderQueue(items) {
      const root = document.getElementById('queue');
      root.innerHTML = '';
      if (!items.length) {
        root.innerHTML = '<p class=\"meta\">No pending approvals.</p>';
        return;
      }

      for (const item of items) {
        const row = document.createElement('div');
        row.className = 'row';
        const editorId = `editor-${item.request_id}`;
        const diffId = `diff-${item.request_id}`;

        row.innerHTML = `
          <div><strong>${item.request_id}</strong> <span class=\"meta\">${item.status}</span></div>
          <div class=\"meta\">Workflow: ${item.workflow_id} | Risk: ${item.risk_score}</div>
          <div>${item.reason}</div>
          <pre>${JSON.stringify(item.action, null, 2)}</pre>
          <button class=\"ok\">Approve</button>
          <button class=\"warn\">Modify</button>
          <button class=\"bad\">Reject</button>
          <div id=\"${editorId}\" class=\"hidden\">
            <p class=\"meta\">Decision diff editor (JSON)</p>
            <textarea>${JSON.stringify(item.action, null, 2)}</textarea>
            <button class=\"warn\">Submit MODIFY</button>
            <div id=\"${diffId}\"></div>
          </div>
        `;

        const buttons = row.querySelectorAll('button');
        const editor = row.querySelector(`#${editorId}`);
        const textarea = editor.querySelector('textarea');
        const diff = row.querySelector(`#${diffId}`);

        buttons[0].onclick = () => submitDecision(item, 'APPROVE');
        buttons[1].onclick = () => {
          editor.classList.toggle('hidden');
          try {
            const parsed = JSON.parse(textarea.value);
            diff.innerHTML = renderDiff(item.action, parsed);
          } catch {
            diff.innerHTML = '<div class=\"diff-removed\">Invalid JSON</div>';
          }
        };
        buttons[2].onclick = () => submitDecision(item, 'REJECT');
        buttons[3].onclick = async () => {
          let parsed = null;
          try {
            parsed = JSON.parse(textarea.value);
          } catch {
            alert('Modified action must be valid JSON.');
            return;
          }
          diff.innerHTML = renderDiff(item.action, parsed);
          await submitDecision(item, 'MODIFY', parsed);
        };

        textarea.oninput = () => {
          try {
            const parsed = JSON.parse(textarea.value);
            diff.innerHTML = renderDiff(item.action, parsed);
          } catch {
            diff.innerHTML = '<div class=\"diff-removed\">Invalid JSON</div>';
          }
        };

        root.appendChild(row);
      }
    }

    function renderAudit(items) {
      const root = document.getElementById('audit');
      root.innerHTML = '';
      for (const item of items.reverse()) {
        const row = document.createElement('div');
        row.className = 'row';
        row.innerHTML = `<div><strong>${item.event_type}</strong></div><pre>${JSON.stringify(item.payload, null, 2)}</pre>`;
        root.appendChild(row);
      }
    }

    function renderTraces(items) {
      const root = document.getElementById('traces');
      root.innerHTML = '';
      for (const item of items) {
        const row = document.createElement('div');
        row.className = 'row';
        row.innerHTML = `
          <div><strong>${item.workflow_id}</strong></div>
          <div class=\"meta\">Status: ${item.final_status} | Quality: ${item.trace_quality_score}</div>
          <div>${item.intent || ''}</div>
        `;
        root.appendChild(row);
      }
    }

    async function refreshAll() {
      if (!token) return;
      try {
        const queue = await getJSON('/api/queue');
        const audit = await getJSON('/api/audit?limit=50');
        const traces = await getJSON('/api/traces?limit=20');
        renderQueue(queue.items || []);
        renderAudit(audit.items || []);
        renderTraces(traces.items || []);
      } catch (err) {
        document.getElementById('sessionMeta').textContent = `Auth/API error: ${err}`;
      }
    }

    function connectSSE() {
      if (eventSource) eventSource.close();
      if (!token) return;
      eventSource = new EventSource(`/api/events?token=${encodeURIComponent(token)}&since=0`);
      eventSource.addEventListener('update', () => {
        refreshAll();
      });
      eventSource.onerror = () => {
        // Browser reconnects automatically; no polling fallback by design.
      };
    }

    async function login() {
      const username = document.getElementById('username').value.trim();
      const password = document.getElementById('password').value;
      try {
        const session = await postJSON('/api/login', {username, password});
        token = session.token;
        role = session.role;
        document.getElementById('sessionMeta').textContent = `Logged in as ${session.username} (${role})`;
        connectSSE();
        await refreshAll();
      } catch (err) {
        document.getElementById('sessionMeta').textContent = `Login failed: ${err}`;
      }
    }

    document.getElementById('loginBtn').onclick = login;
  </script>
</body>
</html>
"""
