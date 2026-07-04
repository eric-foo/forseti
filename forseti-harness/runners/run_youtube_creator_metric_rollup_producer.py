"""Operator runner: derive YouTube creator-metric Silver rollups from the
committed review-input CAPTURES -- the YouTube analog of the IG producer runner,
and the lake-population step the YouTube fold-in stage (s8 / AR-06) was missing.

Unlike the IG producer (which consumes raw grid projections), the merged YouTube
producer derives from a seed-shaped document. This runner closes the capture-fed
loop: it (1) rebuilds that document from the committed review-input capture files
via ``build_youtube_shorts_fragrance_creator_metric_seed_from_files`` (the builder
landed in PR #539, proven to reconstruct the committed seed VALUE-equal), then
(2) appends the MetricObservation + MetricRollupObservation records that the
snapshot runner's account-anchored discovery consumes. The captures -- not the
hand-authored seed -- are the source; the seed is retained only as the genesis
no-drift oracle.

Genesis timestamp: ``--generated-at-utc`` defaults to the committed seed's own
``generated_at_utc`` so the FIRST lake snapshot is value-equal to the seed it
supersedes (the no-drift bridge, mirroring IG s4). Override it for later
re-captures; a forgotten override fails CLOSED at snapshot selection (a distinct
rollup that reuses the old timestamp is ``ambiguous_latest_rollup``), never
silently wrong.

This runner WRITES to the lake: the producer is append-only with no dry-run, so
each invocation deposits durable records. CI never resolves the real lake; the
testable core (``run_youtube_producer``) runs against ``DataLakeRoot.for_test``,
and ``main``/``resolve`` is the only real-lake-bound path.

Boundary (smallest complete -- explicitly NOT pulled forward): generating the
committed snapshot/manifest/receipt is ``run_creator_metric_rollup_snapshot
--platform youtube`` (a later operator step, already wired), and re-pointing
``materialize`` from the YT seed onto the snapshot is a later step still. This
runner only populates the lake.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from capture_spine.creator_profile_current.youtube_metric_seed import (
    YOUTUBE_SHORTS_FRAGRANCE_CREATOR_METRIC_SEED_WRAPPER,
    build_youtube_shorts_fragrance_creator_metric_seed_from_files,
)
from capture_spine.creator_profile_current.youtube_silver_metric_producer import (
    YoutubeCreatorMetricSilverResult,
    derive_youtube_creator_metric_silver_records_from_seed,
)
from data_lake.root import DataLakeRoot, DataLakeRootError

ROOT = Path(__file__).resolve().parents[2]
_SOCIAL_MEDIA = (
    ROOT / "forseti" / "product" / "spines" / "capture" / "core" / "source_families" / "social_media"
)
DEFAULT_ACCOUNT_LEDGER = (
    _SOCIAL_MEDIA / "creator_registry" / "creator_public_handle_linkage_ledger_v0.json"
)
DEFAULT_COMMITTED_SEED = (
    _SOCIAL_MEDIA / "youtube" / "youtube_shorts_fragrance_creator_metric_seed_v0.json"
)


def _load_account_ledger(path: str | Path) -> Mapping[str, Any]:
    # The builder wants the inner {platform_accounts} block; the committed ledger
    # file wraps it under its top-level key (matches the IG producer runner).
    document = json.loads(Path(path).read_text(encoding="utf-8"))
    return document.get("creator_public_handle_linkage_ledger", document)


def _committed_seed_body() -> Mapping[str, Any]:
    # utf-8-sig tolerates a BOM, matching the seed's own loaders.
    document = json.loads(DEFAULT_COMMITTED_SEED.read_text(encoding="utf-8-sig"))
    return document[YOUTUBE_SHORTS_FRAGRANCE_CREATOR_METRIC_SEED_WRAPPER]


def default_source_files() -> list[Path]:
    """The committed seed's own ``source_inputs``, resolved to repo paths -- the
    exact capture set PR #539 proved rebuilds the seed value-equal."""
    return [ROOT / entry["source_pointer"] for entry in _committed_seed_body()["source_inputs"]]


def default_generated_at_utc() -> str:
    """The committed seed's ``generated_at_utc`` -- the genesis timestamp that
    makes the first lake snapshot value-equal to the seed it supersedes."""
    return _committed_seed_body()["generated_at_utc"]


def run_youtube_producer(
    data_root: DataLakeRoot,
    *,
    source_files: Sequence[str | Path],
    account_ledger: Mapping[str, Any],
    generated_at_utc: str,
) -> YoutubeCreatorMetricSilverResult:
    """Rebuild the seed document from the review-input captures, then append its
    observation + rollup records to the lake. The testable core --
    lake-parameterized so it runs against ``DataLakeRoot.for_test``."""
    seed_document = build_youtube_shorts_fragrance_creator_metric_seed_from_files(
        source_files=source_files,
        account_ledger=account_ledger,
        generated_at_utc=generated_at_utc,
    )
    return derive_youtube_creator_metric_silver_records_from_seed(
        data_root=data_root, seed_document=seed_document
    )


def _account_of(record: Mapping[str, Any]) -> str | None:
    try:
        return record["payload"]["observation"]["subject"]["ref"]["orca_platform_account_id"]
    except (KeyError, TypeError):
        return None


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Append YouTube creator-metric Silver rollups to the data lake from the "
            "committed review-input capture files (the YouTube lake-population step the "
            "snapshot runner consumes)."
        )
    )
    parser.add_argument(
        "--source",
        type=Path,
        action="append",
        dest="sources",
        default=None,
        help=(
            "Review-input capture / ledger source file. Repeatable. Defaults to the "
            "committed seed's source_inputs (the PR #539-proven capture set)."
        ),
    )
    parser.add_argument("--account-ledger", type=Path, default=DEFAULT_ACCOUNT_LEDGER)
    parser.add_argument("--data-root", default=None, help="Lake root; defaults to FORSETI_DATA_ROOT (legacy ORCA_DATA_ROOT).")
    parser.add_argument(
        "--generated-at-utc",
        default=None,
        help=(
            "computed_at for the derived rollups. Defaults to the committed seed's "
            "generated_at_utc (genesis no-drift); pass a fresh value for re-captures."
        ),
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        data_root = DataLakeRoot.resolve(explicit=args.data_root)
    except DataLakeRootError as exc:
        parser.exit(status=2, message=f"data lake unavailable: {exc}\n")

    source_files = args.sources if args.sources else default_source_files()
    generated_at = args.generated_at_utc or default_generated_at_utc()
    account_ledger = _load_account_ledger(args.account_ledger)

    try:
        result = run_youtube_producer(
            data_root,
            source_files=source_files,
            account_ledger=account_ledger,
            generated_at_utc=generated_at,
        )
    except Exception as exc:  # noqa: BLE001 - operator feedback; fail-closed, no partial-success masking
        parser.exit(
            status=2,
            message=f"youtube creator metric rollup producer failed: {type(exc).__name__}: {exc}\n",
        )

    accounts = sorted({a for a in (_account_of(r) for r in result.rollup_records) if a})
    print(
        f"appended {len(result.rollup_records)} rollup(s) + "
        f"{len(result.observation_records)} observation(s) for {len(accounts)} account(s)"
    )
    for path in result.rollup_paths:
        print(f"  rollup: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
