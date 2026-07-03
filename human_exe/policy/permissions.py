"""Role-based permission checks for supervised execution."""

from __future__ import annotations

from dataclasses import dataclass

from human_exe.models.tokens import ActionType


@dataclass(slots=True)
class RolePermissions:
    role: str
    allowed_actions: set[ActionType]


DEFAULT_ROLE_PERMISSIONS: dict[str, RolePermissions] = {
    "agent": RolePermissions(
        role="agent",
        allowed_actions={
            ActionType.READ_FILE,
            ActionType.WRITE_FILE,
            ActionType.CREATE_DOCUMENT,
            ActionType.CREATE_SPREADSHEET,
            ActionType.OPEN_URL,
            ActionType.CLICK,
            ActionType.TYPE_TEXT,
            ActionType.SCROLL,
            ActionType.SEND_DRAFT_FOR_APPROVAL,
            ActionType.WAIT_FOR_HUMAN_APPROVAL,
            ActionType.ESCALATE_TO_HUMAN,
        },
    ),
    "supervisor": RolePermissions(
        role="supervisor",
        allowed_actions=set(ActionType),
    ),
}


def has_permission(role: str, action: ActionType) -> bool:
    role_permissions = DEFAULT_ROLE_PERMISSIONS.get(role)
    if role_permissions is None:
        return False
    return action in role_permissions.allowed_actions
