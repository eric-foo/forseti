from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from source_capture.proxy_profiles import (
    ProxyCategory,
    ensure_proxy_profile_directory,
    proxy_profile_path_for_label,
    write_proxy_profile_metadata,
)


def run_proxy_profile_bootstrap(
    *,
    profile_label: str,
    proxy_category: ProxyCategory,
    geoip_enabled: bool,
    timezone: str | None = None,
    locale: str | None = None,
    profile_root: Path | None = None,
) -> tuple[int, str]:
    profile_directory = ensure_proxy_profile_directory(profile_root=profile_root)
    profile_path = proxy_profile_path_for_label(profile_label, profile_root=profile_directory)
    write_proxy_profile_metadata(
        profile_label,
        proxy_category=proxy_category,
        geoip_enabled=geoip_enabled,
        timezone=timezone,
        locale=locale,
        profile_root=profile_directory,
    )
    return (
        0,
        "registered proxy profile "
        f"{profile_label!r} as {proxy_category.value}; geoip_enabled={geoip_enabled}; "
        f"declared_geo timezone={timezone or 'none'}/locale={locale or 'none'}; "
        f"place endpoint JSON out-of-band at {profile_path.name}; no packet written",
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Register a local CloakBrowser proxy profile sidecar. The endpoint JSON must be "
            "placed in the ignored store out-of-band; this command accepts no proxy secrets."
        )
    )
    parser.add_argument("--profile-label", required=True)
    parser.add_argument(
        "--proxy-category",
        choices=[item.value for item in ProxyCategory],
        required=True,
    )
    parser.add_argument("--geoip-enabled", action="store_true")
    parser.add_argument(
        "--timezone",
        default=None,
        help="Declared IANA timezone for the proxy's target geo (e.g. America/New_York). Non-secret.",
    )
    parser.add_argument(
        "--locale",
        default=None,
        help="Declared locale for the proxy's target geo (e.g. en-US). Non-secret.",
    )
    parser.add_argument("--profile-root", type=Path, default=None)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        exit_code, message = run_proxy_profile_bootstrap(
            profile_label=args.profile_label,
            proxy_category=ProxyCategory(args.proxy_category),
            geoip_enabled=args.geoip_enabled,
            timezone=args.timezone,
            locale=args.locale,
            profile_root=args.profile_root,
        )
    except ValueError as exc:
        parser.exit(status=2, message=f"proxy profile bootstrap failed: {exc}\n")

    print(message)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
