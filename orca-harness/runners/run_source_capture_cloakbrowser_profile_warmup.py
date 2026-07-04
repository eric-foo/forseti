from __future__ import annotations

import argparse
import subprocess
import sys
from importlib import import_module
from pathlib import Path
from typing import Protocol, Sequence
from urllib.parse import urlparse

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from source_capture.browser_user_data import ensure_browser_user_data_directory


class CloakBrowserProfileWarmupEngine(Protocol):
    def warm_profile(
        self,
        *,
        login_url: str,
        user_data_dir: Path,
    ) -> str:
        ...


def run_cloakbrowser_profile_warmup(
    *,
    login_url: str,
    user_data_label: str,
    user_data_root: Path | None = None,
    engine: CloakBrowserProfileWarmupEngine | None = None,
) -> tuple[int, str]:
    normalized_url = _validate_http_url(login_url)
    user_data_dir = ensure_browser_user_data_directory(user_data_label, user_data_root=user_data_root)
    warmup_engine = engine or _DirectCloakBrowserProfileWarmupEngine()
    final_url = warmup_engine.warm_profile(login_url=normalized_url, user_data_dir=user_data_dir)
    return (
        0,
        (
            f"CloakBrowser profile warmup completed for user-data label {user_data_label}; "
            f"no auth-state saved; final warmup URL {final_url}"
        ),
    )


class _DirectCloakBrowserProfileWarmupEngine:
    def warm_profile(
        self,
        *,
        login_url: str,
        user_data_dir: Path,
    ) -> str:
        try:
            cloakbrowser = import_module("cloakbrowser")
        except ModuleNotFoundError as exc:
            raise RuntimeError("CloakBrowser is not installed. Install cloakbrowser before warming profiles.") from exc

        binary_path = cloakbrowser.ensure_binary()
        chrome_args = cloakbrowser.build_args(
            True,
            [
                "--disable-popup-blocking",
                "--no-first-run",
                "--no-default-browser-check",
            ],
            headless=False,
        )
        process = subprocess.Popen(
            [str(binary_path), *chrome_args, f"--user-data-dir={user_data_dir}", login_url]
        )
        print(
            "Direct CloakBrowser profile warmup opened without Playwright/CDP attachment. "
            "Complete the permitted login, close that browser window, then press Enter here.",
            flush=True,
        )
        input()
        if process.poll() is None:
            raise RuntimeError(
                "direct CloakBrowser warmup browser is still running; close it before pressing Enter "
                "so the dedicated profile can be reused by the harness"
            )
        return login_url


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Open a direct CloakBrowser window for manual profile warmup without Playwright/CDP. "
            "This writes no packet and saves no auth-state."
        )
    )
    parser.add_argument("--login-url", required=True)
    parser.add_argument(
        "--user-data-label",
        required=True,
        help="Create or reuse an ignored local CloakBrowser user-data directory by label; do not pass profile paths.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        exit_code, message = run_cloakbrowser_profile_warmup(
            login_url=args.login_url,
            user_data_label=args.user_data_label,
        )
    except ValueError as exc:
        parser.exit(status=2, message=f"source capture cloakbrowser profile warmup failed: {exc}\n")
    except Exception as exc:
        parser.exit(status=3, message=f"source capture cloakbrowser profile warmup failed: {exc}\n")

    if exit_code == 0:
        print(message)
        return 0

    parser.exit(status=exit_code, message=f"source capture cloakbrowser profile warmup failed: {message}\n")
    return exit_code


def _validate_http_url(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("CloakBrowser profile warmup requires an absolute http:// or https:// URL")
    if parsed.username is not None or parsed.password is not None:
        raise ValueError("CloakBrowser profile warmup does not accept URLs with embedded credentials")
    return parsed.geturl()


if __name__ == "__main__":
    raise SystemExit(main())