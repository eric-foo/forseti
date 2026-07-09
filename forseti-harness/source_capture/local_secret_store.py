"""Shared mechanics for local, ignored, label-indirected secret stores.

This module owns the *security-critical, type-agnostic* boundary that every
local credential store reuses: directory confinement, label-to-filename
sanitization (path-traversal rejection), the size-capped JSON-object read, and
the metadata sidecar read/write. Type-specific concerns -- the payload shape, the
mode vocabulary, the sidecar key names, and the mode-mismatch comparison -- stay
in each specialization (``auth_state`` for browser storage state,
``reddit_credentials`` for Reddit API credentials).

Confinement is enforced at *path construction*: ``store_path_for_label`` and
``sidecar_path_for`` both call ``assert_under_root``. The read/write helpers
(``read_store_payload``, ``read_sidecar``, ``write_sidecar``) trust the path they
are given -- callers MUST pass only paths obtained from the two construction
helpers above, never an unsanitized path.

The ``kind`` argument is a human-readable noun (e.g. ``"auth-state"``,
``"reddit-credential"``) used only to phrase error messages, so each store's
errors stay self-identifying while the confinement/label logic stays single-
source. No secrets are ever returned to logs or packets by this module; callers
own where the parsed payload flows.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


DEFAULT_MAX_SECRET_STORE_BYTES = 5_000_000
_LABEL_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
# Reserved across stores: metadata sidecars are named ``<data-stem>.meta.json``.
# A data filename ending in this suffix could shadow another label's sidecar, so
# such labels are rejected at construction (closes the with_suffix collision class).
_RESERVED_SIDECAR_SUFFIX = ".meta.json"


def label_to_filename(label: str, *, kind: str, suffix: str = ".json") -> str:
    """Validate a store label and map it to a safe filename.

    Rejects anything that could escape the store directory (path separators,
    traversal) before it is ever joined to a root, and rejects any label whose
    resulting filename would collide with the metadata sidecar namespace. The
    ``kind`` noun is folded into the error message so callers' tests can assert
    on it.
    """
    if not _LABEL_RE.fullmatch(label):
        raise ValueError(
            f"{kind} label must be 1-128 characters using letters, numbers, dot, underscore, or hyphen; "
            "it must start with a letter or number"
        )
    if "/" in label or "\\" in label or Path(label).name != label:
        raise ValueError(f"{kind} label must not contain path separators")
    filename = label if label.endswith(suffix) else f"{label}{suffix}"
    if filename.endswith(_RESERVED_SIDECAR_SUFFIX):
        raise ValueError(
            f"{kind} label is reserved: the resulting filename {filename!r} ends with "
            f"'{_RESERVED_SIDECAR_SUFFIX}', which is used only for metadata sidecars"
        )
    return filename


def assert_under_root(path: Path, root: Path, *, kind: str) -> None:
    """Refuse any path that does not resolve to inside ``root``.

    Also refuse a store root that is itself a symlink: ``resolve()`` follows it, so
    a credential file could physically land outside the intended ignored directory
    (e.g. a tracked location) while still passing the resolved-root containment
    check. The default roots are real subdirectories; this guards a tampered or
    mistakenly-symlinked store root.
    """
    if root.is_symlink():
        raise ValueError(f"{kind} store root must not be a symlink: {root}")
    root_resolved = root.resolve()
    path_resolved = path.resolve()
    try:
        path_resolved.relative_to(root_resolved)
    except ValueError as exc:
        raise ValueError(
            f"{kind} path must stay under its local ignored store directory"
        ) from exc


def store_path_for_label(label: str, *, root: Path, kind: str, suffix: str = ".json") -> Path:
    path = root / label_to_filename(label, kind=kind, suffix=suffix)
    assert_under_root(path, root, kind=kind)
    return path


def sidecar_path_for(state_path: Path, *, root: Path, sidecar_suffix: str, kind: str) -> Path:
    path = state_path.with_suffix(sidecar_suffix)
    assert_under_root(path, root, kind=kind)
    return path


def ensure_store_directory(root: Path) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    return root


def read_store_payload(path: Path, *, max_bytes: int, kind: str, label: str) -> dict:
    """Read a stored secret file as a JSON object, enforcing size + shape floor.

    Returns the parsed ``dict``; the caller applies its own type-specific shape
    validation. Does not inspect or log values. ``path`` must come from
    ``store_path_for_label`` (confinement is enforced there).
    """
    if not path.exists():
        raise ValueError(f"{kind} file does not exist for label: {label}")
    if not path.is_file():
        raise ValueError(f"{kind} path is not a file for label: {label}")
    size = path.stat().st_size
    if size <= 0:
        raise ValueError(f"{kind} file is empty for label: {label}")
    if size > max_bytes:
        raise ValueError(f"{kind} file exceeds {max_bytes} byte cap for label: {label}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        raise ValueError(f"{kind} file is not valid JSON for label: {label}") from None
    if not isinstance(payload, dict):
        raise ValueError(f"{kind} file must be a JSON object for label: {label}")
    return payload


def write_sidecar(sidecar_path: Path, *, payload: dict, kind: str, label: str) -> None:
    """Write a metadata sidecar (non-secret), refusing to overwrite an existing one.

    ``sidecar_path`` must come from ``sidecar_path_for`` (confinement enforced there).
    """
    if sidecar_path.exists():
        raise ValueError(f"{kind} metadata already exists for label: {label}")
    sidecar_path.write_text(f"{json.dumps(payload, indent=2, sort_keys=True)}\n", encoding="utf-8")


def read_sidecar(sidecar_path: Path, *, kind: str, label: str) -> dict:
    """Read a metadata sidecar as a JSON object; caller compares fields.

    ``sidecar_path`` must come from ``sidecar_path_for`` (confinement enforced there).
    """
    if not sidecar_path.is_file():
        raise ValueError(f"{kind} metadata path is not a file for label: {label}")
    try:
        payload = json.loads(sidecar_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        raise ValueError(f"{kind} metadata is not valid JSON for label: {label}") from None
    if not isinstance(payload, dict):
        raise ValueError(f"{kind} metadata must be a JSON object for label: {label}")
    return payload


__all__ = [
    "DEFAULT_MAX_SECRET_STORE_BYTES",
    "assert_under_root",
    "ensure_store_directory",
    "label_to_filename",
    "read_sidecar",
    "read_store_payload",
    "sidecar_path_for",
    "store_path_for_label",
    "write_sidecar",
]
