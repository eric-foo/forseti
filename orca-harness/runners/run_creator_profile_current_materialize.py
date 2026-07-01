from __future__ import annotations

import argparse
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from capture_spine.creator_profile_current.materialize import (
    build_creator_profile_current_view_from_files,
    dump_creator_profile_current_view,
    load_json,
)


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = (
    ROOT
    / "orca"
    / "product"
    / "spines"
    / "capture"
    / "core"
    / "source_families"
    / "social_media"
    / "creator_registry"
    / "creator_profile_current_view_v0.json"
)
DEFAULT_ACCOUNT_LEDGER = (
    ROOT
    / "orca"
    / "product"
    / "spines"
    / "capture"
    / "core"
    / "source_families"
    / "social_media"
    / "creator_registry"
    / "creator_public_handle_linkage_ledger_v0.json"
)
# Lake cut-over §5/§8: both Instagram and YouTube materialize from their
# committed lake snapshots (each seed stays the no-drift value oracle).
DEFAULT_YOUTUBE_SNAPSHOT = (
    ROOT
    / "orca"
    / "product"
    / "spines"
    / "capture"
    / "core"
    / "source_families"
    / "social_media"
    / "youtube"
    / "youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json"
)
DEFAULT_INSTAGRAM_SNAPSHOT = (
    ROOT
    / "orca"
    / "product"
    / "spines"
    / "capture"
    / "core"
    / "source_families"
    / "social_media"
    / "instagram"
    / "instagram_reels_creator_metric_rollup_snapshot_v0.json"
)
DEFAULT_METRIC_SEEDS = (DEFAULT_YOUTUBE_SNAPSHOT, DEFAULT_INSTAGRAM_SNAPSHOT)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Materialize the static creator_profile_current view from the public-handle "
            "account ledger and creator metric seeds."
        )
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--account-ledger", type=Path, default=DEFAULT_ACCOUNT_LEDGER)
    parser.add_argument(
        "--metric-seed",
        type=Path,
        action="append",
        dest="metric_seeds",
        help="Metric seed/snapshot JSON file. Repeat for multiple platform sources. Defaults to current YouTube + Instagram lake snapshots.",
    )
    parser.add_argument(
        "--generated-at-utc",
        help="Timestamp for profile_view_computed_at. Defaults to the existing output timestamp when present.",
    )
    parser.add_argument("--check", action="store_true", help="Fail if the output is stale.")
    parser.add_argument("--write", action="store_true", help="Write the materialized output JSON.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    if args.check == args.write:
        parser.error("choose exactly one of --check or --write")

    generated_at = args.generated_at_utc or _existing_generated_at(args.output) or _now_utc()
    metric_seeds = tuple(args.metric_seeds) if args.metric_seeds else DEFAULT_METRIC_SEEDS
    try:
        document = build_creator_profile_current_view_from_files(
            account_ledger_path=args.account_ledger,
            metric_seed_paths=metric_seeds,
            generated_at_utc=generated_at,
        )
        rendered = dump_creator_profile_current_view(document)
        if args.check:
            if not args.output.exists():
                raise ValueError(f"output does not exist: {args.output}")
            current = args.output.read_text(encoding="utf-8")
            if current != rendered:
                raise ValueError(f"creator profile current view is stale: {args.output}")
            print(f"up to date: {args.output}")
            return 0

        args.output.parent.mkdir(parents=True, exist_ok=True)
        # newline="\n": keep the committed view LF on a Windows operator box.
        args.output.write_text(rendered, encoding="utf-8", newline="\n")
        print(args.output)
        return 0
    except Exception as exc:
        parser.exit(status=2, message=f"creator profile materialization failed: {exc}\n")


def _existing_generated_at(path: Path) -> str | None:
    if not path.exists():
        return None
    try:
        document = load_json(path)
        value = document["creator_profile_current_view"]["generated_at_utc"]
    except (KeyError, TypeError, ValueError):
        return None
    return value if isinstance(value, str) and value.strip() else None


def _now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
