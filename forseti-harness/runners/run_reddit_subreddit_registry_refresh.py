"""Refresh the Reddit Subreddit Registry from committed grid packets (read-only scan).

The one authorized registry writer for grid evidence: reads explicitly
supplied ``reddit_subreddit_grid`` Source Capture Packets (hash-verified) and
appends one observation record per packet to lake authority. Re-running over
the same packet is a no-op (observations dedupe by provenance pointer).
Unknown subreddits are reported, never silently added.

Registry authority is the lake, not the checked-in JSON: this runner writes
append-only records under ``derived/`` and never mutates a tracked file.

Owner contracts:
- forseti/product/spines/capture/core/source_families/social_media/reddit/reddit_subreddit_registry_spec_v0.md
- forseti/product/spines/capture/core/source_families/social_media/reddit/reddit_subreddit_registry_lake_cutover_architecture_v0.md
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
    refresh_lake_registry_from_grid_packets,
)
from data_lake.reddit_subreddit_registry import RedditSubredditRegistryLakeError
from data_lake.root import DataLakeRoot
from runners._scaffold import exit_on_failure

def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Append committed reddit_subreddit_grid packets to lake registry authority "
            "under the two-speed rule (observations append; status updates on change)."
        )
    )
    parser.add_argument(
        "--data-root",
        type=Path,
        default=None,
        help="Lake root holding registry authority (defaults to FORSETI_DATA_ROOT resolution).",
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
        expected=(RegistryRefreshError, RedditSubredditRegistryLakeError),
        expected_status=3,
        format_expected=lambda exc: f"registry refresh refused [{exc.code}]: {exc.message}",
        unexpected_status=2,
    ):
        data_root = (
            # resolve() is keyword-only; positional raised TypeError and made
            # --data-root unusable (same defect #1299 fixed in the lake runner).
            DataLakeRoot.resolve(explicit=args.data_root)
            if args.data_root is not None
            else DataLakeRoot.resolve()
        )
        outcome = refresh_lake_registry_from_grid_packets(
            data_root=data_root,
            packet_paths=args.packets,
            dry_run=args.dry_run,
        )

    print(json.dumps(outcome.to_dict(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
