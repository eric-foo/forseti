from __future__ import annotations

import json
import re
from enum import StrEnum
from pathlib import Path


AUTH_STATE_DIRNAME = "_auth_state"
AUTH_STATE_METADATA_SUFFIX = ".meta.json"
MAX_AUTH_STATE_BYTES = 5_000_000
_AUTH_STATE_LABEL_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")


class AuthenticatedSessionMode(StrEnum):
    FREE_ACCOUNT_CREATED = "free_account_created_session"
    PAID_ENTITLED = "paid_entitled_session"
    CLIENT_PROVIDED = "client_provided_session"
    CONSENTING_COWORKER = "consenting_coworker_session"


def default_auth_state_root() -> Path:
    return Path(__file__).resolve().parents[1] / AUTH_STATE_DIRNAME


def auth_state_path_for_label(state_label: str, *, auth_state_root: Path | None = None) -> Path:
    filename = _auth_state_filename(state_label)
    root = auth_state_root or default_auth_state_root()
    path = root / filename
    _assert_under_root(path, root)
    return path


def auth_state_metadata_path_for_label(
    state_label: str, *, auth_state_root: Path | None = None
) -> Path:
    state_path = auth_state_path_for_label(state_label, auth_state_root=auth_state_root)
    path = state_path.with_suffix(AUTH_STATE_METADATA_SUFFIX)
    root = auth_state_root or default_auth_state_root()
    _assert_under_root(path, root)
    return path


def ensure_auth_state_directory(*, auth_state_root: Path | None = None) -> Path:
    root = auth_state_root or default_auth_state_root()
    root.mkdir(parents=True, exist_ok=True)
    return root


def validate_auth_state_file(state_label: str, *, auth_state_root: Path | None = None) -> Path:
    path = auth_state_path_for_label(state_label, auth_state_root=auth_state_root)
    if not path.exists():
        raise ValueError(f"auth-state file does not exist for label: {state_label}")
    if not path.is_file():
        raise ValueError(f"auth-state path is not a file for label: {state_label}")
    if path.stat().st_size <= 0:
        raise ValueError(f"auth-state file is empty for label: {state_label}")
    if path.stat().st_size > MAX_AUTH_STATE_BYTES:
        raise ValueError(
            f"auth-state file exceeds {MAX_AUTH_STATE_BYTES} byte cap for label: {state_label}"
        )
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        raise ValueError(f"auth-state file is not valid JSON for label: {state_label}") from None
    if not isinstance(payload, dict):
        raise ValueError(f"auth-state file must be a JSON object for label: {state_label}")
    cookies = payload.get("cookies")
    origins = payload.get("origins")
    if not isinstance(cookies, list) or not isinstance(origins, list):
        raise ValueError(
            "auth-state file must look like browser storage-state JSON "
            f"with cookies/origins lists for label: {state_label}"
        )
    return path


def write_auth_state_metadata(
    state_label: str,
    *,
    session_mode: AuthenticatedSessionMode,
    auth_state_root: Path | None = None,
) -> Path:
    state_path = validate_auth_state_file(state_label, auth_state_root=auth_state_root)
    metadata_path = auth_state_metadata_path_for_label(state_label, auth_state_root=auth_state_root)
    if metadata_path.exists():
        raise ValueError(f"auth-state metadata already exists for label: {state_label}")
    payload = {
        "auth_state_file": state_path.name,
        "session_mode": session_mode.value,
    }
    metadata_path.write_text(f"{json.dumps(payload, indent=2, sort_keys=True)}\n", encoding="utf-8")
    return metadata_path


def validate_auth_state_session_mode(
    state_label: str,
    *,
    session_mode: AuthenticatedSessionMode,
    auth_state_root: Path | None = None,
) -> Path:
    state_path = validate_auth_state_file(state_label, auth_state_root=auth_state_root)
    metadata_path = auth_state_metadata_path_for_label(state_label, auth_state_root=auth_state_root)
    if not metadata_path.exists():
        raise ValueError(
            "auth-state metadata sidecar does not exist for label: "
            f"{state_label}; re-bootstrap the session with an explicit session mode"
        )
    if not metadata_path.is_file():
        raise ValueError(f"auth-state metadata path is not a file for label: {state_label}")
    try:
        payload = json.loads(metadata_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        raise ValueError(f"auth-state metadata is not valid JSON for label: {state_label}") from None
    if not isinstance(payload, dict):
        raise ValueError(f"auth-state metadata must be a JSON object for label: {state_label}")
    if payload.get("auth_state_file") != state_path.name:
        raise ValueError(f"auth-state metadata file binding mismatch for label: {state_label}")
    bootstrapped_mode = payload.get("session_mode")
    if bootstrapped_mode != session_mode.value:
        raise ValueError(
            "auth-state session mode mismatch for label: "
            f"{state_label}; bootstrapped as {bootstrapped_mode!r} but capture declared {session_mode.value!r}"
        )
    return state_path


def _auth_state_filename(state_label: str) -> str:
    if not _AUTH_STATE_LABEL_RE.fullmatch(state_label):
        raise ValueError(
            "auth-state label must be 1-128 characters using letters, numbers, dot, underscore, or hyphen; "
            "it must start with a letter or number"
        )
    if "/" in state_label or "\\" in state_label or Path(state_label).name != state_label:
        raise ValueError("auth-state label must not contain path separators")
    return state_label if state_label.endswith(".json") else f"{state_label}.json"


def _assert_under_root(path: Path, root: Path) -> None:
    root_resolved = root.resolve()
    path_resolved = path.resolve()
    try:
        path_resolved.relative_to(root_resolved)
    except ValueError as exc:
        raise ValueError("auth-state path must stay under the local ignored auth-state directory") from exc
