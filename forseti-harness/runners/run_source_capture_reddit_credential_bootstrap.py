from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from source_capture.reddit_credentials import (
    RedditCredentialMode,
    ensure_reddit_credential_directory,
    reddit_credential_metadata_path_for_label,
    reddit_credential_path_for_label,
    validate_reddit_credential_file,
    write_reddit_credential_metadata,
)


def run_reddit_credential_bootstrap(
    *,
    credential_label: str,
    credential_mode: RedditCredentialMode,
    credential_root: Path | None = None,
) -> tuple[int, str]:
    """Validate an owner-placed credential file and write its mode-binding sidecar.

    The operator places ``<label>.json`` (client_id/client_secret) in the ignored
    store out-of-band; this step never receives secrets as arguments. It writes no
    Source Capture Packet -- only the non-secret sidecar that binds the label to a
    credential mode for later mode-mismatch enforcement.
    """
    root = ensure_reddit_credential_directory(credential_root=credential_root)
    state_path = reddit_credential_path_for_label(credential_label, credential_root=root)
    metadata_path = reddit_credential_metadata_path_for_label(credential_label, credential_root=root)
    if not state_path.exists():
        raise ValueError(
            f"reddit-credential file does not exist for label: {credential_label}; "
            f"place the client_id/client_secret JSON as {state_path.name} in the ignored "
            "credential store before registering"
        )
    if metadata_path.exists():
        raise ValueError(f"reddit-credential metadata already exists for label: {credential_label}")
    validate_reddit_credential_file(credential_label, credential_root=root)
    write_reddit_credential_metadata(
        credential_label,
        credential_mode=credential_mode,
        credential_root=root,
    )
    return (
        0,
        f"reddit-credential mode {credential_mode.value} bound for label {credential_label}",
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Validate an owner-placed Reddit API credential file and write its mode-binding sidecar. "
            "Writes no Source Capture Packet and never accepts secrets as flags."
        )
    )
    parser.add_argument("--credential-label", required=True)
    parser.add_argument(
        "--credential-mode",
        choices=[item.value for item in RedditCredentialMode],
        required=True,
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        exit_code, message = run_reddit_credential_bootstrap(
            credential_label=args.credential_label,
            credential_mode=RedditCredentialMode(args.credential_mode),
        )
    except ValueError as exc:
        parser.exit(status=2, message=f"source capture reddit credential bootstrap failed: {exc}\n")
    except Exception as exc:
        parser.exit(status=3, message=f"source capture reddit credential bootstrap failed: {exc}\n")

    if exit_code == 0:
        print(message)
        return 0

    parser.exit(status=exit_code, message=f"source capture reddit credential bootstrap failed: {message}\n")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
