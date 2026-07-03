"""Default prohibited autonomy zones."""

from human_exe.models.tokens import ActionType


DEFAULT_PROHIBITED_ACTIONS: set[ActionType] = {
    ActionType.ABORT_TASK,
}

PROHIBITED_AUTONOMY_ZONES: tuple[str, ...] = (
    "sending external messages without approval",
    "deleting files",
    "changing financial records",
    "approving budgets",
    "making legal, HR, medical, or regulatory commitments",
    "accepting risk above a configured threshold",
    "changing security settings",
    "sharing secrets, credentials, tokens, or private data",
)
