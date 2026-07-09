"""Local, ignored Reddit API credential store (token-side sibling of ``auth_state``).

Built on ``local_secret_store`` so the security boundary (directory confinement,
label sanitization, size-capped JSON read, sidecar mechanics) is single-source
with the browser storage-state store. This module adds only the Reddit-specific
parts: the credential payload shape, the closed ``RedditCredentialMode``
vocabulary, the sidecar key names, and the mode-mismatch comparison.

Scope (most-efficient legitimate read path): the supported mode is an
owner-registered Reddit *script* app used for **application-only**, read-only
access to public data. That path needs only ``client_id`` + ``client_secret`` --
no refresh token, no user password, no browser/redirect flow. Entitled/private
content stays with the authenticated-browser lane; a user-context Reddit mode can
be added later (the enum is closed but extendable).

HARD INVARIANT: nothing in this module writes secrets to a Source Capture Packet.
``load_reddit_credentials`` returns an in-memory ``RedditCredentials`` that flows
only to the API client's auth header; the packet records label + mode only.
"""

from __future__ import annotations

from dataclasses import dataclass
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


REDDIT_CREDENTIAL_DIRNAME = "_reddit_credentials"
REDDIT_CREDENTIAL_METADATA_SUFFIX = ".meta.json"
MAX_REDDIT_CREDENTIAL_BYTES = DEFAULT_MAX_SECRET_STORE_BYTES
_REDDIT_CREDENTIAL_KIND = "reddit-credential"
_REQUIRED_CREDENTIAL_KEYS = ("client_id", "client_secret")


class RedditCredentialMode(StrEnum):
    """Legitimate provenance of Reddit API access (capture-support only).

    Closed vocabulary; extend when a new legitimate access path is added. Carries
    no credibility or Judgment meaning -- it records *how access was obtained*,
    not anything about the source.
    """

    OWNER_REGISTERED_SCRIPT_APP = "owner_registered_script_app"


@dataclass(frozen=True, repr=False)
class RedditCredentials:
    """In-memory Reddit API credentials. Holds secrets; never serialize to a packet."""

    client_id: str
    client_secret: str
    credential_mode: RedditCredentialMode

    def __repr__(self) -> str:
        # Defense-in-depth: keep BOTH credential fields out of any repr/str/log/
        # traceback (str() falls back to this repr). Only the non-secret
        # credential_mode is shown.
        return (
            "RedditCredentials(client_id='<redacted>', client_secret='<redacted>', "
            f"credential_mode={self.credential_mode.value!r})"
        )


def default_reddit_credential_root() -> Path:
    return Path(__file__).resolve().parents[1] / REDDIT_CREDENTIAL_DIRNAME


def reddit_credential_path_for_label(label: str, *, credential_root: Path | None = None) -> Path:
    root = credential_root or default_reddit_credential_root()
    return store_path_for_label(label, root=root, kind=_REDDIT_CREDENTIAL_KIND)


def reddit_credential_metadata_path_for_label(
    label: str, *, credential_root: Path | None = None
) -> Path:
    root = credential_root or default_reddit_credential_root()
    state_path = reddit_credential_path_for_label(label, credential_root=root)
    return sidecar_path_for(
        state_path,
        root=root,
        sidecar_suffix=REDDIT_CREDENTIAL_METADATA_SUFFIX,
        kind=_REDDIT_CREDENTIAL_KIND,
    )


def ensure_reddit_credential_directory(*, credential_root: Path | None = None) -> Path:
    root = credential_root or default_reddit_credential_root()
    return ensure_store_directory(root)


def validate_reddit_credential_file(label: str, *, credential_root: Path | None = None) -> Path:
    root = credential_root or default_reddit_credential_root()
    path = reddit_credential_path_for_label(label, credential_root=root)
    payload = read_store_payload(
        path, max_bytes=MAX_REDDIT_CREDENTIAL_BYTES, kind=_REDDIT_CREDENTIAL_KIND, label=label
    )
    _validate_credential_shape(payload, label=label)
    return path


def write_reddit_credential_metadata(
    label: str,
    *,
    credential_mode: RedditCredentialMode,
    credential_root: Path | None = None,
) -> Path:
    root = credential_root or default_reddit_credential_root()
    state_path = validate_reddit_credential_file(label, credential_root=root)
    metadata_path = reddit_credential_metadata_path_for_label(label, credential_root=root)
    write_sidecar(
        metadata_path,
        payload={"credential_file": state_path.name, "credential_mode": credential_mode.value},
        kind=_REDDIT_CREDENTIAL_KIND,
        label=label,
    )
    return metadata_path


def load_reddit_credentials(
    label: str,
    *,
    credential_mode: RedditCredentialMode,
    credential_root: Path | None = None,
) -> RedditCredentials:
    """Validate the store file + mode sidecar and return in-memory credentials.

    Raises if the file is missing/malformed, the sidecar is missing, the sidecar
    is not bound to this file, or the registered mode does not match the declared
    mode. The returned object holds secrets -- callers must keep it out of packets.
    """
    root = credential_root or default_reddit_credential_root()
    state_path = reddit_credential_path_for_label(label, credential_root=root)
    payload = read_store_payload(
        state_path, max_bytes=MAX_REDDIT_CREDENTIAL_BYTES, kind=_REDDIT_CREDENTIAL_KIND, label=label
    )
    _validate_credential_shape(payload, label=label)

    metadata_path = reddit_credential_metadata_path_for_label(label, credential_root=root)
    if not metadata_path.exists():
        raise ValueError(
            "reddit-credential metadata sidecar does not exist for label: "
            f"{label}; register the credential with an explicit credential mode"
        )
    sidecar = read_sidecar(metadata_path, kind=_REDDIT_CREDENTIAL_KIND, label=label)
    if sidecar.get("credential_file") != state_path.name:
        raise ValueError(f"reddit-credential metadata file binding mismatch for label: {label}")
    registered_mode = sidecar.get("credential_mode")
    if registered_mode != credential_mode.value:
        raise ValueError(
            "reddit-credential mode mismatch for label: "
            f"{label}; registered as {registered_mode!r} but capture declared {credential_mode.value!r}"
        )
    return RedditCredentials(
        client_id=payload["client_id"],
        client_secret=payload["client_secret"],
        credential_mode=credential_mode,
    )


def _validate_credential_shape(payload: dict, *, label: str) -> None:
    for key in _REQUIRED_CREDENTIAL_KEYS:
        value = payload.get(key)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(
                f"reddit-credential file must contain a non-empty string {key!r} for label: {label}"
            )
    unexpected = sorted(set(payload) - set(_REQUIRED_CREDENTIAL_KEYS))
    if unexpected:
        raise ValueError(
            f"reddit-credential file has unexpected key(s) {unexpected} for label: {label}; "
            "the owner_registered_script_app mode is application-only and accepts exactly "
            "client_id + client_secret (no refresh_token, password, or user-context secrets)"
        )
