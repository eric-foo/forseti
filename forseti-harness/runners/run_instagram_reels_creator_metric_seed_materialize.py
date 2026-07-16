from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from capture_spine.creator_profile_current.instagram_metric_seed import (
    build_instagram_reels_creator_metric_seed_from_files,
    discover_instagram_reels_projection_paths_from_lake,
    dump_instagram_reels_creator_metric_seed,
    load_json,
)
from data_lake.root import DataLakeRoot
from harness_utils import utc_now_z


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = (
    ROOT
    / "forseti"
    / "product"
    / "spines"
    / "capture"
    / "core"
    / "source_families"
    / "social_media"
    / "instagram"
    / "instagram_reels_creator_metric_seed_v0.json"
)
DEFAULT_ACCOUNT_LEDGER = (
    ROOT
    / "forseti"
    / "product"
    / "spines"
    / "capture"
    / "core"
    / "source_families"
    / "social_media"
    / "creator_registry"
    / "creator_public_handle_linkage_ledger_v0.json"
)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Materialize the static Instagram reels creator metric seed from IG projection JSON files."
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--account-ledger", type=Path, default=DEFAULT_ACCOUNT_LEDGER)
    parser.add_argument(
        "--projection",
        type=Path,
        action="append",
        default=[],
        help="IG reels-grid projection JSON file. Repeat for multiple projections.",
    )
    parser.add_argument(
        "--from-lake",
        action="store_true",
        help="Discover IG reels-grid projections from the data lake derived layout.",
    )
    parser.add_argument(
        "--data-root",
        type=Path,
        help="Data lake root for --from-lake. Defaults to FORSETI_DATA_ROOT (legacy ORCA_DATA_ROOT)/config resolution.",
    )
    parser.add_argument(
        "--generated-at-utc",
        help="Timestamp for generated_at_utc. Defaults to the existing output timestamp when present.",
    )
    parser.add_argument("--check", action="store_true", help="Fail if the output is stale.")
    parser.add_argument("--write", action="store_true", help="Write the materialized output JSON.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    if args.check == args.write:
        parser.error("choose exactly one of --check or --write")

    if args.from_lake and args.projection:
        parser.error("--from-lake cannot be combined with explicit --projection files")
    if args.data_root is not None and not args.from_lake:
        parser.error("--data-root requires --from-lake")
    if not args.from_lake and not args.projection:
        parser.error("provide at least one --projection or use --from-lake")

    generated_at = args.generated_at_utc or _existing_generated_at(args.output) or utc_now_z()
    try:
        projection_paths = list(args.projection)
        if args.from_lake:
            data_root = DataLakeRoot.resolve(explicit=args.data_root)
            projection_paths = discover_instagram_reels_projection_paths_from_lake(data_root)
        account_document = load_json(args.account_ledger)
        document = build_instagram_reels_creator_metric_seed_from_files(
            projection_paths=projection_paths,
            account_ledger=account_document["creator_public_handle_linkage_ledger"],
            generated_at_utc=generated_at,
        )
        rendered = dump_instagram_reels_creator_metric_seed(document)
        if args.check:
            if not args.output.exists():
                raise ValueError(f"output does not exist: {args.output}")
            current = args.output.read_text(encoding="utf-8")
            if current != rendered:
                raise ValueError(f"instagram reels creator metric seed is stale: {args.output}")
            print(f"up to date: {args.output}")
            return 0

        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
        print(args.output)
        return 0
    except Exception as exc:
        parser.exit(status=2, message=f"instagram reels creator metric seed materialization failed: {exc}\n")


def _existing_generated_at(path: Path) -> str | None:
    if not path.exists():
        return None
    try:
        document = load_json(path)
        value = document["instagram_reels_creator_metric_seed"]["generated_at_utc"]
    except (KeyError, TypeError, ValueError):
        return None
    return value if isinstance(value, str) and value.strip() else None


if __name__ == "__main__":
    raise SystemExit(main())
