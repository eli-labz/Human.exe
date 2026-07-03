"""Token models for supervised human-action traces."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any
from uuid import uuid4


class ActionType(str, Enum):
    OPEN_APP = "OPEN_APP"
    CLOSE_APP = "CLOSE_APP"
    CLICK = "CLICK"
    DOUBLE_CLICK = "DOUBLE_CLICK"
    TYPE_TEXT = "TYPE_TEXT"
    HOTKEY = "HOTKEY"
    SCROLL = "SCROLL"
    SELECT_TEXT = "SELECT_TEXT"
    SELECT_RANGE = "SELECT_RANGE"
    COPY = "COPY"
    PASTE = "PASTE"
    OPEN_URL = "OPEN_URL"
    DOWNLOAD_FILE = "DOWNLOAD_FILE"
    UPLOAD_FILE = "UPLOAD_FILE"
    READ_FILE = "READ_FILE"
    WRITE_FILE = "WRITE_FILE"
    CREATE_DOCUMENT = "CREATE_DOCUMENT"
    CREATE_SPREADSHEET = "CREATE_SPREADSHEET"
    SEND_DRAFT_FOR_APPROVAL = "SEND_DRAFT_FOR_APPROVAL"
    WAIT_FOR_HUMAN_APPROVAL = "WAIT_FOR_HUMAN_APPROVAL"
    ESCALATE_TO_HUMAN = "ESCALATE_TO_HUMAN"
    ABORT_TASK = "ABORT_TASK"


@dataclass(slots=True)
class IntentToken:
    task_id: str
    objective: str
    business_goal: str
    created_by: str
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


@dataclass(slots=True)
class PerceptionToken:
    task_id: str
    source: str
    state: dict[str, Any]
    screenshot_metadata: dict[str, Any] | None = None
    accessibility_metadata: dict[str, Any] | None = None
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


@dataclass(slots=True)
class HumanActionToken:
    task_id: str
    action_type: ActionType
    parameters: dict[str, Any]
    actor: str
    token_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


@dataclass(slots=True)
class OutcomeToken:
    task_id: str
    action_token_id: str
    success: bool
    verification_passed: bool
    result: dict[str, Any]
    error: str | None = None
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
