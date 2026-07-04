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
from source_capture.proxy_profiles import ProxyProfile, load_proxy_profile_by_label


class CloakBrowserProfileWarmupEngine(Protocol):
    def warm_profile(
        self,
        *,
        login_url: str,
        user_data_dir: Path,
        proxy_profile: ProxyProfile | None,
    ) -> str:
        ...


def run_cloakbrowser_profile_warmup(
    *,
    login_url: str,
    user_data_label: str,
    user_data_root: Path | None = None,
    proxy_profile_label: str | None = None,
    proxy_profile_root: Path | None = None,
    engine: CloakBrowserProfileWarmupEngine | None = None,
) -> tuple[int, str]:
    normalized_url = _validate_http_url(login_url)
    user_data_dir = ensure_browser_user_data_directory(user_data_label, user_data_root=user_data_root)
    proxy_profile = (
        load_proxy_profile_by_label(label=proxy_profile_label, profile_root=proxy_profile_root)
        if proxy_profile_label
        else None
    )
    warmup_engine = engine or _DirectCloakBrowserProfileWarmupEngine()
    final_url = warmup_engine.warm_profile(
        login_url=normalized_url,
        user_data_dir=user_data_dir,
        proxy_profile=proxy_profile,
    )
    proxy_clause = (
        f" with proxy profile label {proxy_profile_label} ({proxy_profile.proxy_category.value})"
        if proxy_profile is not None
        else ""
    )
    return (
        0,
        (
            f"CloakBrowser profile warmup completed for user-data label {user_data_label}{proxy_clause}; "
            f"no auth-state saved; final warmup URL {final_url}"
        ),
    )


class _DirectCloakBrowserProfileWarmupEngine:
    def warm_profile(
        self,
        *,
        login_url: str,
        user_data_dir: Path,
        proxy_profile: ProxyProfile | None,
    ) -> str:
        try:
            cloakbrowser = import_module("cloakbrowser")
        except ModuleNotFoundError as exc:
            raise RuntimeError("CloakBrowser is not installed. Install cloakbrowser before warming profiles.") from exc

        binary_path = cloakbrowser.ensure_binary()
        chrome_args = _direct_chrome_args(cloakbrowser, proxy_profile=proxy_profile)
        process = subprocess.Popen(
            [str(binary_path), *chrome_args, f"--user-data-dir={user_data_dir}", login_url]
        )
        proxy_note = (
            " A label-indirected proxy profile is active; endpoint and credentials are not printed."
            if proxy_profile is not None
            else ""
        )
        print(
            "Direct CloakBrowser profile warmup opened without Playwright/CDP attachment. "
            "Complete the permitted login, close that browser window, then press Enter here."
            f"{proxy_note}",
            flush=True,
        )
        input()
        if process.poll() is None:
            raise RuntimeError(
                "direct CloakBrowser warmup browser is still running; close it before pressing Enter "
                "so the dedicated profile can be reused by the harness"
            )
        return login_url


def _direct_chrome_args(cloakbrowser: object, *, proxy_profile: ProxyProfile | None) -> list[str]:
    extra_args = [
        "--disable-popup-blocking",
        "--no-first-run",
        "--no-default-browser-check",
    ]
    timezone = None
    locale = None
    if proxy_profile is not None:
        timezone, locale, exit_ip = _resolve_proxy_geo(cloakbrowser, proxy_profile=proxy_profile)
        extra_args.append(f"--proxy-server={proxy_profile.proxy_endpoint}")
        if exit_ip:
            extra_args.append(f"--fingerprint-webrtc-ip={exit_ip}")
    return cloakbrowser.build_args(  # type: ignore[attr-defined]
        True,
        extra_args,
        timezone=timezone,
        locale=locale,
        headless=False,
    )


def _resolve_proxy_geo(
    cloakbrowser: object, *, proxy_profile: ProxyProfile
) -> tuple[str | None, str | None, str | None]:
    try:
        return cloakbrowser.maybe_resolve_geoip(  # type: ignore[attr-defined]
            proxy_profile.geoip_enabled,
            proxy_profile.proxy_endpoint,
            proxy_profile.timezone,
            proxy_profile.locale,
        )
    except Exception as exc:
        raise RuntimeError(
            "CloakBrowser proxy geo resolution failed for the label-indirected proxy profile"
        ) from exc


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
    parser.add_argument(
        "--proxy-profile-label",
        default=None,
        help="Optional local Source Capture proxy profile label; endpoint JSON is loaded from the ignored store.",
    )
    parser.add_argument(
        "--proxy-profile-root",
        type=Path,
        default=None,
        help="Optional local proxy-profile store root. Never recorded in output.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        exit_code, message = run_cloakbrowser_profile_warmup(
            login_url=args.login_url,
            user_data_label=args.user_data_label,
            proxy_profile_label=args.proxy_profile_label,
            proxy_profile_root=args.proxy_profile_root,
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