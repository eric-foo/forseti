from __future__ import annotations

from pathlib import Path

from source_capture.local_secret_store import assert_under_root, ensure_store_directory, label_to_filename


BROWSER_USER_DATA_DIRNAME = "_browser_user_data"
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