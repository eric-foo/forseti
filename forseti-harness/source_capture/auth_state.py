from __future__ import annotations

from enum import StrEnum
from pathlib import Path

from source_capture.local_secret_store import (
    DEFAULT_MAX_SECRET_STORE_BYTES,
    ensure_store_directory,
    read_sidecar,
    read_store_payload,
    sidecar_path_for,
    store_path_for_label,
    write_sidecar,
)
from source_capture.source_access_provenance import (
    SOURCE_ACCESS_PROVENANCE_KEY,
    SOURCE_ACCESS_PROVENANCE_SCHEMA_VERSION,
    HarnessProxyProfilePosture,
    validate_auth_state_source_access_provenance as validate_source_access_provenance_payload,
)


AUTH_STATE_DIRNAME = "_auth_state"
AUTH_STATE_METADATA_SUFFIX = ".meta.json"
MAX_AUTH_STATE_BYTES = DEFAULT_MAX_SECRET_STORE_BYTES
_AUTH_STATE_KIND = "auth-state"


class AuthenticatedSessionMode(StrEnum):
    FREE_ACCOUNT_CREATED = "free_account_created_session"
    PAID_ENTITLED = "paid_entitled_session"
    CLIENT_PROVIDED = "client_provided_session"
    CONSENTING_COWORKER = "consenting_coworker_session"


def default_auth_state_root() -> Path:
    return Path(__file__).resolve().parents[1] / AUTH_STATE_DIRNAME


def auth_state_path_for_label(state_label: str, *, auth_state_root: Path | None = None) -> Path:
    root = auth_state_root or default_auth_state_root()
    return store_path_for_label(state_label, root=root, kind=_AUTH_STATE_KIND)


def auth_state_metadata_path_for_label(
    state_label: str, *, auth_state_root: Path | None = None
) -> Path:
    root = auth_state_root or default_auth_state_root()
    state_path = auth_state_path_for_label(state_label, auth_state_root=root)
    return sidecar_path_for(
        state_path, root=root, sidecar_suffix=AUTH_STATE_METADATA_SUFFIX, kind=_AUTH_STATE_KIND
    )


def ensure_auth_state_directory(*, auth_state_root: Path | None = None) -> Path:
    root = auth_state_root or default_auth_state_root()
    return ensure_store_directory(root)


def validate_auth_state_file(state_label: str, *, auth_state_root: Path | None = None) -> Path:
    root = auth_state_root or default_auth_state_root()
    path = auth_state_path_for_label(state_label, auth_state_root=root)
    payload = read_store_payload(
        path, max_bytes=MAX_AUTH_STATE_BYTES, kind=_AUTH_STATE_KIND, label=state_label
    )
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
    source_access_provenance: dict[str, object] | None = None,
) -> Path:
    root = auth_state_root or default_auth_state_root()
    state_path = validate_auth_state_file(state_label, auth_state_root=root)
    metadata_path = auth_state_metadata_path_for_label(state_label, auth_state_root=root)
    payload: dict[str, object] = {
        "auth_state_file": state_path.name,
        "session_mode": session_mode.value,
    }
    if source_access_provenance is not None:
        validate_source_access_provenance_payload(
            source_access_provenance,
            state_path=state_path,
            expected_source_access_posture=session_mode.value,
        )
        payload["schema_version"] = SOURCE_ACCESS_PROVENANCE_SCHEMA_VERSION
        payload[SOURCE_ACCESS_PROVENANCE_KEY] = source_access_provenance
    write_sidecar(
        metadata_path,
        payload=payload,
        kind=_AUTH_STATE_KIND,
        label=state_label,
    )
    return metadata_path


def validate_auth_state_session_mode(
    state_label: str,
    *,
    session_mode: AuthenticatedSessionMode,
    auth_state_root: Path | None = None,
) -> Path:
    root = auth_state_root or default_auth_state_root()
    state_path = validate_auth_state_file(state_label, auth_state_root=root)
    metadata_path = auth_state_metadata_path_for_label(state_label, auth_state_root=root)
    if not metadata_path.exists():
        raise ValueError(
            "auth-state metadata sidecar does not exist for label: "
            f"{state_label}; re-bootstrap the session with an explicit session mode"
        )
    payload = read_sidecar(metadata_path, kind=_AUTH_STATE_KIND, label=state_label)
    if payload.get("auth_state_file") != state_path.name:
        raise ValueError(f"auth-state metadata file binding mismatch for label: {state_label}")
    bootstrapped_mode = payload.get("session_mode")
    if bootstrapped_mode != session_mode.value:
        raise ValueError(
            "auth-state session mode mismatch for label: "
            f"{state_label}; bootstrapped as {bootstrapped_mode!r} but capture declared {session_mode.value!r}"
        )
    return state_path


def validate_auth_state_provenance_requirement(
    state_label: str,
    *,
    session_mode: AuthenticatedSessionMode,
    required_harness_proxy_profile_posture: str | HarnessProxyProfilePosture,
    auth_state_root: Path | None = None,
) -> Path:
    root = auth_state_root or default_auth_state_root()
    state_path = validate_auth_state_session_mode(
        state_label,
        session_mode=session_mode,
        auth_state_root=root,
    )
    metadata_path = auth_state_metadata_path_for_label(state_label, auth_state_root=root)
    payload = read_sidecar(metadata_path, kind=_AUTH_STATE_KIND, label=state_label)
    if payload.get("schema_version") != SOURCE_ACCESS_PROVENANCE_SCHEMA_VERSION:
        raise ValueError(
            "auth-state source-access provenance is missing or legacy-only for label: "
            f"{state_label}; re-export from a warmed user-data profile with provenance"
        )
    source_access_provenance = payload.get(SOURCE_ACCESS_PROVENANCE_KEY)
    if not isinstance(source_access_provenance, dict):
        raise ValueError(
            "auth-state source-access provenance is missing for label: "
            f"{state_label}; re-export from a warmed user-data profile with provenance"
        )
    validate_source_access_provenance_payload(
        source_access_provenance,
        state_path=state_path,
        expected_source_access_posture=session_mode.value,
        required_harness_proxy_profile_posture=required_harness_proxy_profile_posture,
    )
    return state_path
