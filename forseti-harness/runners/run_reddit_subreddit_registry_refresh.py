"""Refresh the Reddit Subreddit Registry from committed grid packets (read-only scan).

The one authorized registry writer for grid evidence: reads explicitly
supplied ``reddit_subreddit_grid`` Source Capture Packets (hash-verified) and
applies the registry spec's two-speed rule. Re-running over the same packet
is a no-op (observations dedupe by provenance pointer). Unknown subreddits
are reported, never silently added.

Owner contract:
- forseti/product/spines/capture/core/source_families/social_media/reddit/reddit_subreddit_registry_spec_v0.md
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from capture_spine.reddit_subreddit_grid import (
    RegistryRefreshError,
    refresh_registry_from_grid_packets,
)
from runners._scaffold import exit_on_failure

DEFAULT_REGISTRY_PATH = (
    Path(__file__).resolve().parents[2]
    / "forseti"
    / "product"
    / "spines"
    / "capture"
    / "core"
    / "source_families"
    / "social_media"
    / "reddit"
    / "reddit_subreddit_registry_v0.json"
)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Apply committed reddit_subreddit_grid packets to the Reddit Subreddit Registry "
            "under the two-speed rule (observations append; status updates on change)."
        )
    )
    parser.add_argument(
        "--registry",
        type=Path,
        default=DEFAULT_REGISTRY_PATH,
        help="Path to reddit_subreddit_registry_v0.json (defaults to the repo copy).",
    )
    parser.add_argument(
        "--packet",
        action="append",
        required=True,
        dest="packets",
        type=Path,
        help="Path to a committed grid packet directory or its manifest.json (repeatable).",
    )
    parser.add_argument("--dry-run", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    with exit_on_failure(
        parser,
        runner_name="registry refresh",
        expected=(RegistryRefreshError,),
        expected_status=3,
        format_expected=lambda exc: f"registry refresh refused [{exc.code}]: {exc.message}",
        unexpected_status=2,
    ):
        outcome = refresh_registry_from_grid_packets(
            registry_path=args.registry,
            packet_paths=args.packets,
            dry_run=args.dry_run,
        )

    print(json.dumps(outcome.to_dict(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
