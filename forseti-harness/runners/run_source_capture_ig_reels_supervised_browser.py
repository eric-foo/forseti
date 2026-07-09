"""Launch a supervised persistent CloakBrowser window for IG reels grids.

This runner writes no Source Capture Packet. It is an operator-supervised browser
surface for keeping a local CloakBrowser user-data profile warm, visible, and
manually controllable before a separate capture route is run. It launches the
CloakBrowser binary directly rather than attaching a Playwright page controller.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import time
from importlib import import_module
from pathlib import Path
from typing import Protocol, Sequence
from urllib.parse import urljoin, urlparse

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from source_capture.browser_user_data import ensure_browser_user_data_directory


DEFAULT_VIEWPORT_WIDTH = 1080
DEFAULT_VIEWPORT_HEIGHT = 1920
DEFAULT_ZOOM = 0.67


class BrowserProcess(Protocol):
    def poll(self) -> int | None:
        ...


class ProcessFactory(Protocol):
    def __call__(self, args: Sequence[str]) -> BrowserProcess:
        ...


def run_ig_reels_supervised_browser(
    *,
    handles: Sequence[str] = (),
    profile_urls: Sequence[str] = (),
    browser_user_data_label: str,
    viewport_width: int = DEFAULT_VIEWPORT_WIDTH,
    viewport_height: int = DEFAULT_VIEWPORT_HEIGHT,
    zoom: float | None = DEFAULT_ZOOM,
    wait_for_operator: bool = True,
    hold_open_until_killed: bool = False,
    browser_user_data_root: Path | None = None,
    cloakbrowser_module: object | None = None,
    process_factory: ProcessFactory | None = None,
) -> tuple[int, str]:
    urls = _resolve_reels_urls(handles=handles, profile_urls=profile_urls)
    if not browser_user_data_label.strip():
        raise ValueError("browser_user_data_label must not be blank")
    _validate_positive_int("viewport_width", viewport_width)
    _validate_positive_int("viewport_height", viewport_height)
    if zoom is not None and zoom <= 0:
        raise ValueError("zoom must be greater than zero")
    if wait_for_operator and hold_open_until_killed:
        raise ValueError("wait_for_operator and hold_open_until_killed are mutually exclusive")

    user_data_dir = ensure_browser_user_data_directory(
        browser_user_data_label,
        user_data_root=browser_user_data_root,
    )
    cloakbrowser = cloakbrowser_module or _import_cloakbrowser()

    launch_args = _build_direct_launch_args(
        cloakbrowser,
        user_data_dir=user_data_dir,
        viewport_width=viewport_width,
        viewport_height=viewport_height,
        zoom=zoom,
        urls=urls,
    )
    process = (process_factory or subprocess.Popen)(launch_args)

    if hold_open_until_killed:
        print(
            "Persistent direct CloakBrowser IG window is open. "
            "Solve any challenge manually in the browser; this runner does not auto-solve. "
            "This process is holding until the browser closes or the process is terminated.",
            flush=True,
        )
        _hold_until_browser_exits(process)
    if wait_for_operator:
        print(
            "Persistent direct CloakBrowser IG window is open. "
            "Solve any challenge manually in the browser; this runner does not auto-solve. "
            "Press Enter here only when you are done supervising; the runner will not close the browser.",
            flush=True,
        )
        input()

    return (
        0,
        "opened persistent direct CloakBrowser IG reels window for "
        f"{len(urls)} url(s) using user-data label {browser_user_data_label}",
    )


def _import_cloakbrowser() -> object:
    try:
        return import_module("cloakbrowser")
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "CloakBrowser is not installed. Install cloakbrowser before launching the supervised IG browser."
        ) from exc


def _build_direct_launch_args(
    cloakbrowser: object,
    *,
    user_data_dir: Path,
    viewport_width: int,
    viewport_height: int,
    zoom: float | None,
    urls: Sequence[str],
) -> list[str]:
    ensure_binary = getattr(cloakbrowser, "ensure_binary", None)
    build_args = getattr(cloakbrowser, "build_args", None)
    if not callable(ensure_binary) or not callable(build_args):
        raise RuntimeError(
            "CloakBrowser is installed but does not expose ensure_binary/build_args. "
            "Install a compatible cloakbrowser package before launching the supervised IG browser."
        )
    extra_args = [
        "--disable-popup-blocking",
        "--no-first-run",
        "--no-default-browser-check",
        f"--user-data-dir={user_data_dir}",
        f"--window-size={viewport_width},{viewport_height}",
    ]
    if zoom is not None:
        # Direct binary launch cannot apply post-load CSS zoom without page control.
        # This display-scale hint preserves the no-Playwright supervised mode.
        extra_args.append(f"--force-device-scale-factor={zoom}")
    chrome_args = build_args(False, extra_args, headless=False)
    return [str(ensure_binary()), *[str(arg) for arg in chrome_args], *urls]


def _hold_until_browser_exits(process: BrowserProcess) -> None:
    while process.poll() is None:
        time.sleep(1.0)


def _resolve_reels_urls(*, handles: Sequence[str], profile_urls: Sequence[str]) -> list[str]:
    urls: list[str] = []
    for handle in handles:
        normalized = _normalize_handle(handle)
        urls.append(f"https://www.instagram.com/{normalized}/reels/")
    for profile_url in profile_urls:
        urls.append(_normalize_profile_url(profile_url))
    if not urls:
        raise ValueError("supply at least one --handle or --profile-url")
    return urls


def _normalize_handle(handle: str) -> str:
    normalized = handle.strip().lstrip("@")
    if not normalized or "/" in normalized or "\\" in normalized:
        raise ValueError("IG handle must be a non-empty handle, not a path")
    return normalized


def _normalize_profile_url(profile_url: str) -> str:
    parsed = urlparse(profile_url)
    if parsed.scheme not in {"http", "https"} or parsed.netloc.lower() not in {
        "www.instagram.com",
        "instagram.com",
    }:
        raise ValueError("--profile-url must be an absolute instagram.com /<handle>/reels/ URL")
    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) < 2 or parts[1] != "reels":
        raise ValueError("--profile-url must point at /<handle>/reels/")
    normalized = _normalize_handle(parts[0])
    return urljoin(f"https://www.instagram.com/{normalized}/", "reels/")


def _validate_positive_int(name: str, value: int) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be greater than zero")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Open a direct headed persistent CloakBrowser IG reels window for human-supervised use. "
            "This writes no Source Capture Packet and performs no automatic challenge solving."
        )
    )
    parser.add_argument("--handle", action="append", default=[], help="IG handle, with or without @. Repeatable.")
    parser.add_argument(
        "--profile-url",
        action="append",
        default=[],
        help="Absolute instagram.com/<handle>/reels/ URL. Repeatable.",
    )
    parser.add_argument("--browser-user-data-label", required=True)
    parser.add_argument("--viewport-width", type=int, default=DEFAULT_VIEWPORT_WIDTH)
    parser.add_argument("--viewport-height", type=int, default=DEFAULT_VIEWPORT_HEIGHT)
    parser.add_argument(
        "--zoom",
        type=float,
        default=DEFAULT_ZOOM,
        help=(
            "Browser display-scale hint for direct launch. Use 1.0 for no zoom-out hint; "
            "exact page zoom can be adjusted manually in the supervised browser."
        ),
    )
    parser.add_argument(
        "--no-wait",
        action="store_true",
        help="Do not hold the runner after launch. The direct browser process is not closed by this runner.",
    )
    parser.add_argument(
        "--hold-open-until-killed",
        action="store_true",
        help="Hold the runner until the browser closes or this process is terminated.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    if args.no_wait and args.hold_open_until_killed:
        parser.error("--no-wait and --hold-open-until-killed are mutually exclusive")
    try:
        exit_code, message = run_ig_reels_supervised_browser(
            handles=args.handle,
            profile_urls=args.profile_url,
            browser_user_data_label=args.browser_user_data_label,
            viewport_width=args.viewport_width,
            viewport_height=args.viewport_height,
            zoom=args.zoom,
            wait_for_operator=not args.no_wait and not args.hold_open_until_killed,
            hold_open_until_killed=args.hold_open_until_killed,
        )
    except ValueError as exc:
        parser.exit(status=2, message=f"supervised IG browser launch failed: {exc}\n")
    except Exception as exc:
        parser.exit(status=3, message=f"supervised IG browser launch failed: {exc}\n")
    print(message)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
