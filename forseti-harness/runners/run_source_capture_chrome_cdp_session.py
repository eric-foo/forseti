"""Launch an operator-owned Chrome profile, then export its authenticated state."""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from importlib import import_module
from pathlib import Path
from typing import Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from source_capture.auth_state import (
    AuthenticatedSessionMode,
    auth_state_metadata_path_for_label,
    auth_state_path_for_label,
    ensure_auth_state_directory,
    validate_auth_state_file,
    write_auth_state_metadata,
)
from source_capture.browser_user_data import (
    ensure_browser_user_data_directory,
    read_browser_user_data_provenance,
    write_browser_user_data_provenance,
)
from source_capture.source_access_provenance import (
    build_auth_state_source_access_provenance,
    build_browser_user_data_source_access_provenance,
)


DEFAULT_CDP_PORT = 9222
DEFAULT_LOGIN_URL = "https://www.tiktok.com/login"


def launch_and_export_chrome_cdp_session(
    *,
    user_data_label: str,
    state_label: str,
    session_mode: AuthenticatedSessionMode,
    login_url: str = DEFAULT_LOGIN_URL,
    cdp_port: int = DEFAULT_CDP_PORT,
    auth_state_root: Path | None = None,
    browser_user_data_root: Path | None = None,
    chrome_executable: Path | None = None,
) -> tuple[int, str]:
    if not 1 <= int(cdp_port) <= 65535:
        raise ValueError("cdp_port must be in 1..65535")
    auth_root = ensure_auth_state_directory(auth_state_root=auth_state_root)
    state_path = auth_state_path_for_label(state_label, auth_state_root=auth_root)
    metadata_path = auth_state_metadata_path_for_label(
        state_label, auth_state_root=auth_root
    )
    if state_path.exists() or metadata_path.exists():
        raise ValueError(f"auth-state label already exists: {state_label}")

    profile_provenance = build_browser_user_data_source_access_provenance(
        user_data_label=user_data_label,
        browser_backend="chrome_cdp",
        proxy_category=None,
    )
    user_data_dir = ensure_browser_user_data_directory(
        user_data_label, user_data_root=browser_user_data_root
    )
    write_browser_user_data_provenance(
        user_data_label,
        payload=profile_provenance,
        user_data_root=browser_user_data_root,
    )
    executable = chrome_executable or _find_chrome_executable()
    subprocess.Popen(
        [
            str(executable),
            f"--remote-debugging-address=127.0.0.1",
            f"--remote-debugging-port={int(cdp_port)}",
            f"--user-data-dir={user_data_dir}",
            "--no-first-run",
            "--no-default-browser-check",
            login_url,
        ]
    )
    print(
        "Dedicated Chrome opened. Complete Google OAuth manually, confirm TikTok "
        "is logged in, then press Enter here. Chrome will remain open.",
        flush=True,
    )
    input()

    sync_api = import_module("playwright.sync_api")
    playwright = sync_api.sync_playwright().start()
    browser = playwright.chromium.connect_over_cdp(
        f"http://127.0.0.1:{int(cdp_port)}"
    )
    try:
        contexts = list(browser.contexts)
        if not contexts:
            raise RuntimeError("Chrome CDP browser exposed no persistent context")
        contexts[0].storage_state(path=str(state_path))
    finally:
        browser.close()
        playwright.stop()
    validate_auth_state_file(state_label, auth_state_root=auth_root)
    profile_provenance = read_browser_user_data_provenance(
        user_data_label, user_data_root=browser_user_data_root
    )
    auth_provenance = build_auth_state_source_access_provenance(
        user_data_label=user_data_label,
        session_mode_value=session_mode.value,
        state_path=state_path,
        browser_user_data_provenance=profile_provenance,
    )
    write_auth_state_metadata(
        state_label,
        session_mode=session_mode,
        auth_state_root=auth_root,
        source_access_provenance=auth_provenance,
    )
    return 0, (
        f"Chrome CDP session ready for state label {state_label}; "
        f"browser left open on http://127.0.0.1:{int(cdp_port)}"
    )


def _find_chrome_executable() -> Path:
    from_path = shutil.which("chrome.exe") or shutil.which("chrome")
    candidates = [
        Path(from_path) if from_path else None,
        Path(os.environ.get("PROGRAMFILES", ""))
        / "Google/Chrome/Application/chrome.exe",
        Path(os.environ.get("PROGRAMFILES(X86)", ""))
        / "Google/Chrome/Application/chrome.exe",
        Path(os.environ.get("LOCALAPPDATA", ""))
        / "Google/Chrome/Application/chrome.exe",
    ]
    for candidate in candidates:
        if candidate is not None and candidate.is_file():
            return candidate
    raise RuntimeError("Google Chrome executable was not found")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Launch a dedicated extension-free Chrome profile for manual OAuth, "
            "export storage state, and leave Chrome running for local CDP attachment."
        )
    )
    parser.add_argument("--user-data-label", required=True)
    parser.add_argument("--state-label", required=True)
    parser.add_argument(
        "--session-mode",
        choices=[item.value for item in AuthenticatedSessionMode],
        required=True,
    )
    parser.add_argument("--login-url", default=DEFAULT_LOGIN_URL)
    parser.add_argument("--cdp-port", type=int, default=DEFAULT_CDP_PORT)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        code, message = launch_and_export_chrome_cdp_session(
            user_data_label=args.user_data_label,
            state_label=args.state_label,
            session_mode=AuthenticatedSessionMode(args.session_mode),
            login_url=args.login_url,
            cdp_port=args.cdp_port,
        )
    except (OSError, ValueError) as exc:
        raise SystemExit(f"Chrome CDP session bootstrap failed: {exc}") from None
    print(message)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
