from __future__ import annotations

import argparse
import sys
from importlib import import_module
from pathlib import Path
from typing import Protocol, Sequence
from urllib.parse import urlparse

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
from source_capture.adapters.browser_snapshot import DEFAULT_TIMEOUT_SECONDS


class BrowserSessionBootstrapEngine(Protocol):
    def save_storage_state(
        self,
        *,
        login_url: str,
        timeout_seconds: float,
        state_path: Path,
    ) -> str:
        ...


def run_browser_session_bootstrap(
    *,
    login_url: str,
    state_label: str,
    session_mode: AuthenticatedSessionMode,
    timeout_seconds: float,
    auth_state_root: Path | None = None,
    engine: BrowserSessionBootstrapEngine | None = None,
) -> tuple[int, str]:
    normalized_url = _validate_http_url(login_url)
    if timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be greater than zero")

    auth_state_directory = ensure_auth_state_directory(auth_state_root=auth_state_root)
    state_path = auth_state_path_for_label(state_label, auth_state_root=auth_state_directory)
    metadata_path = auth_state_metadata_path_for_label(state_label, auth_state_root=auth_state_directory)
    if state_path.exists():
        raise ValueError(f"auth-state file already exists for label: {state_label}")
    if metadata_path.exists():
        raise ValueError(f"auth-state metadata already exists for label: {state_label}")

    bootstrap_engine = engine or _PlaywrightSessionBootstrapEngine()
    final_url = bootstrap_engine.save_storage_state(
        login_url=normalized_url,
        timeout_seconds=timeout_seconds,
        state_path=state_path,
    )
    validate_auth_state_file(state_label, auth_state_root=auth_state_directory)
    write_auth_state_metadata(
        state_label,
        session_mode=session_mode,
        auth_state_root=auth_state_directory,
    )
    return (
        0,
        (
            f"auth-state saved for {session_mode.value} with label {state_label} "
            f"after manual browser session ending at {final_url}"
        ),
    )


class _PlaywrightSessionBootstrapEngine:
    def save_storage_state(
        self,
        *,
        login_url: str,
        timeout_seconds: float,
        state_path: Path,
    ) -> str:
        try:
            sync_api = import_module("playwright.sync_api")
        except ModuleNotFoundError as exc:
            raise RuntimeError(
                "Playwright is not installed. Install the browser optional dependency before bootstrapping sessions."
            ) from exc

        timeout_ms = timeout_seconds * 1000
        with sync_api.sync_playwright() as playwright:
            try:
                browser = playwright.chromium.launch(headless=False)
            except Exception as exc:
                if _looks_like_missing_browser_binary(exc):
                    raise RuntimeError(
                        "Playwright Chromium browser binary is not installed. "
                        "Run `python -m playwright install chromium` before bootstrapping sessions."
                    ) from exc
                raise
            try:
                context = browser.new_context()
                try:
                    page = context.new_page()
                    page.goto(login_url, wait_until="load", timeout=timeout_ms)
                    print(
                        "Manual login bootstrap opened a browser window. "
                        "Complete the permitted login there, then press Enter here to save storage state.",
                        flush=True,
                    )
                    input()
                    final_url = page.url
                    context.storage_state(path=str(state_path))
                    return final_url
                finally:
                    context.close()
            finally:
                browser.close()


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Open a headed Playwright browser for manual login and save local ignored storage-state JSON. "
            "This writes no Source Capture Packet."
        )
    )
    parser.add_argument("--login-url", required=True)
    parser.add_argument("--state-label", required=True)
    parser.add_argument(
        "--session-mode",
        choices=[item.value for item in AuthenticatedSessionMode],
        required=True,
    )
    parser.add_argument("--timeout-seconds", type=float, default=DEFAULT_TIMEOUT_SECONDS)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        exit_code, message = run_browser_session_bootstrap(
            login_url=args.login_url,
            state_label=args.state_label,
            session_mode=AuthenticatedSessionMode(args.session_mode),
            timeout_seconds=args.timeout_seconds,
        )
    except ValueError as exc:
        parser.exit(status=2, message=f"source capture browser session bootstrap failed: {exc}\n")
    except Exception as exc:
        parser.exit(status=3, message=f"source capture browser session bootstrap failed: {exc}\n")

    if exit_code == 0:
        print(message)
        return 0

    parser.exit(status=exit_code, message=f"source capture browser session bootstrap failed: {message}\n")
    return exit_code


def _validate_http_url(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("browser session bootstrap requires an absolute http:// or https:// URL")
    if parsed.username is not None or parsed.password is not None:
        raise ValueError("browser session bootstrap does not accept URLs with embedded credentials")
    return parsed.geturl()


def _looks_like_missing_browser_binary(error: Exception) -> bool:
    text = f"{type(error).__name__}: {error}".lower()
    return (
        "executable doesn't exist" in text
        or "browser has not been installed" in text
        or "playwright install" in text
    )


if __name__ == "__main__":
    raise SystemExit(main())
