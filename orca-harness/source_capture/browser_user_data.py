from __future__ import annotations

from pathlib import Path

from source_capture.local_secret_store import (
    assert_under_root,
    ensure_store_directory,
    label_to_filename,
    read_sidecar,
    sidecar_path_for,
    write_sidecar,
)


BROWSER_USER_DATA_DIRNAME = "_browser_user_data"
BROWSER_USER_DATA_PROVENANCE_SUFFIX = ".provenance.json"
_BROWSER_USER_DATA_KIND = "browser user-data"


def default_browser_user_data_root() -> Path:
    return Path(__file__).resolve().parents[1] / BROWSER_USER_DATA_DIRNAME


def browser_user_data_path_for_label(
    user_data_label: str, *, user_data_root: Path | None = None
) -> Path:
    root = user_data_root or default_browser_user_data_root()
    directory_name = label_to_filename(user_data_label, kind=_BROWSER_USER_DATA_KIND, suffix="")
    path = root / directory_name
    assert_under_root(path, root, kind=_BROWSER_USER_DATA_KIND)
    return path


def ensure_browser_user_data_directory(
    user_data_label: str, *, user_data_root: Path | None = None
) -> Path:
    root = ensure_store_directory(user_data_root or default_browser_user_data_root())
    path = browser_user_data_path_for_label(user_data_label, user_data_root=root)
    path.mkdir(parents=True, exist_ok=True)
    return path

def browser_user_data_provenance_path_for_label(
    user_data_label: str, *, user_data_root: Path | None = None
) -> Path:
    root = user_data_root or default_browser_user_data_root()
    user_data_path = browser_user_data_path_for_label(user_data_label, user_data_root=root)
    return sidecar_path_for(
        user_data_path,
        root=root,
        sidecar_suffix=BROWSER_USER_DATA_PROVENANCE_SUFFIX,
        kind=_BROWSER_USER_DATA_KIND,
    )


def write_browser_user_data_provenance(
    user_data_label: str,
    *,
    payload: dict,
    user_data_root: Path | None = None,
) -> Path:
    root = user_data_root or default_browser_user_data_root()
    provenance_path = browser_user_data_provenance_path_for_label(
        user_data_label, user_data_root=root
    )
    if provenance_path.exists():
        existing = read_sidecar(
            provenance_path,
            kind=_BROWSER_USER_DATA_KIND,
            label=user_data_label,
        )
        if existing != payload:
            raise ValueError(
                "browser user-data provenance already exists with different content "
                f"for label: {user_data_label}"
            )
        return provenance_path
    write_sidecar(
        provenance_path,
        payload=payload,
        kind=_BROWSER_USER_DATA_KIND,
        label=user_data_label,
    )
    return provenance_path


def read_browser_user_data_provenance(
    user_data_label: str, *, user_data_root: Path | None = None
) -> dict:
    root = user_data_root or default_browser_user_data_root()
    provenance_path = browser_user_data_provenance_path_for_label(
        user_data_label,
        user_data_root=root,
    )
    return read_sidecar(provenance_path, kind=_BROWSER_USER_DATA_KIND, label=user_data_label)
