from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from source_capture.session_profiles import (
    resolve_session_profile,
    sanitized_session_profile_preflight,
    validate_session_profile_auth_state,
)


BLOCKED_PREFIX = "BLOCKED_SESSION_PROFILE_UNAVAILABLE"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Validate a machine-local Source Capture session profile without "
            "opening a browser or exposing cookie values or secret paths."
        )
    )
    parser.add_argument("--session-profile", required=True)
    parser.add_argument("--session-profile-config", type=Path)
    parser.add_argument("--auth-state-root", type=Path, help=argparse.SUPPRESS)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        profile = resolve_session_profile(
            args.session_profile,
            config_path=args.session_profile_config,
        )
        validate_session_profile_auth_state(
            profile,
            auth_state_root=args.auth_state_root,
        )
    except ValueError as exc:
        print(
            json.dumps(
                {
                    "status": "blocked",
                    "blocker": BLOCKED_PREFIX,
                    "session_profile": args.session_profile,
                    "detail": str(exc),
                    "secret_values_exposed": False,
                },
                sort_keys=True,
            )
        )
        return 2
    print(json.dumps(sanitized_session_profile_preflight(profile), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
