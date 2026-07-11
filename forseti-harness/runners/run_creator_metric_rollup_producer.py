"""Operator runner: derive creator-metric Silver rollups from IG grid projections.

Wires the merged-but-unwired IG producer
(``derive_creator_metric_silver_records_from_projections``) into a runnable step:
resolve the real lake, read RAW IG reels-grid projection files, and APPEND the
MetricObservation + MetricRollupObservation records that the snapshot runner
consumes. Nothing else deposits ``creator_metric_rollup_silver`` records into the
lake -- this is the lake-population step the cut-over was missing.

Input is RAW grid projections (``{packet_id, rows}``) -- the same shape the seed
builder reads (the producer re-derives the seed internally). Produce one with
``run_ig_reels_grid_projection --packet <dir> --output raw.json``. (The lake-mode
``--packet-id`` of that runner writes an *enveloped* derived record, which the
producer does NOT consume; it needs the raw projection.)

This runner WRITES to the lake: the producer is append-only and has no dry-run,
so each invocation deposits durable records. CI never resolves the real lake; the
testable core (``run_producer``) is exercised against ``DataLakeRoot.for_test``,
and ``main``/``resolve`` is the only real-lake-bound path.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from capture_spine.creator_profile_current.silver_metric_producer import (
    CreatorMetricSilverResult,
    derive_creator_metric_silver_records_from_projections,
)
from capture_spine.creator_profile_current.silver_subject_ref import (
    platform_account_id_from_subject_ref as _platform_account_id_from_subject_ref,
)
from data_lake.root import DataLakeRoot, DataLakeRootError

ROOT = Path(__file__).resolve().parents[2]
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


def _now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _load_account_ledger(path: Path) -> Mapping[str, Any]:
    # The producer (via the seed builder) wants the inner {platform_accounts}
    # block; the committed ledger file wraps it under its top-level key.
    document = json.loads(Path(path).read_text(encoding="utf-8"))
    return document.get("creator_public_handle_linkage_ledger", document)


def run_producer(
    data_root: DataLakeRoot,
    *,
    projection_paths: Sequence[str | Path],
    account_ledger: Mapping[str, Any],
    generated_at_utc: str,
    use_bronze_attachment_records: bool = False,
) -> CreatorMetricSilverResult:
    """Append rollup + observation records to the lake from raw grid projections.
    The testable core -- lake-parameterized so it runs against ``for_test``."""
    return derive_creator_metric_silver_records_from_projections(
        data_root=data_root,
        projection_paths=projection_paths,
        account_ledger=account_ledger,
        generated_at_utc=generated_at_utc,
        use_bronze_attachment_records=use_bronze_attachment_records,
    )


def _account_of(record: Mapping[str, Any]) -> str | None:
    try:
        return _platform_account_id_from_subject_ref(
            record["payload"]["observation"]["subject"]["ref"], what="rollup subject ref"
        )
    except (KeyError, TypeError):
        return None


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Append creator-metric Silver rollups to the data lake from RAW IG reels-grid "
            "projection files (the lake-population step the snapshot runner consumes)."
        )
    )
    parser.add_argument(
        "--projection",
        type=Path,
        action="append",
        dest="projections",
        required=True,
        help="RAW IG reels-grid projection JSON ({packet_id, rows}). Repeat per account.",
    )
    parser.add_argument("--account-ledger", type=Path, default=DEFAULT_ACCOUNT_LEDGER)
    parser.add_argument("--data-root", default=None, help="Lake root; defaults to FORSETI_DATA_ROOT (legacy ORCA_DATA_ROOT).")
    parser.add_argument(
        "--generated-at-utc",
        help="Timestamp for the derived records. Defaults to now (UTC).",
    )
    parser.add_argument(
        "--use-bronze-attachment-records",
        action="store_true",
        help=(
            "Upgrade observation raw_refs from packet/file refs to public Bronze "
            "Attachment Record refs when generated catalog rows exist."
        ),
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    generated_at = args.generated_at_utc or _now_utc()

    try:
        data_root = DataLakeRoot.resolve(explicit=args.data_root)
    except DataLakeRootError as exc:
        parser.exit(status=2, message=f"data lake unavailable: {exc}\n")

    account_ledger = _load_account_ledger(args.account_ledger)
    try:
        result = run_producer(
            data_root,
            projection_paths=args.projections,
            account_ledger=account_ledger,
            generated_at_utc=generated_at,
            use_bronze_attachment_records=args.use_bronze_attachment_records,
        )
    except Exception as exc:  # noqa: BLE001 - operator feedback; fail-closed, no partial-success masking
        parser.exit(status=2, message=f"creator metric rollup producer failed: {type(exc).__name__}: {exc}\n")

    accounts = sorted({a for a in (_account_of(r) for r in result.rollup_records) if a})
    print(
        f"appended {len(result.rollup_records)} rollup(s) + "
        f"{len(result.observation_records)} observation(s) for accounts: "
        f"{', '.join(accounts) or '(none)'}"
    )
    for path in result.rollup_paths:
        print(f"  rollup: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
