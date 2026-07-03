"""Operator runner: derive YouTube creator-metric Silver rollups from LIVE lake
watch packets -- the live-recapture counterpart of the genesis
``run_youtube_creator_metric_rollup_producer`` (which rebuilds the committed seed
from the fixed checked-in review-input files and exists for the genesis no-drift
bridge only).

One live recapture cycle on the operator box:

1. capture the admitted pool's watch pages into the lake
   (``run_source_capture_youtube_watch_packet --video-id ... --data-root ...``);
2. THIS runner: build the live metric document from the latest committed watch
   packet per admitted video (fail-closed on a missing/ambiguous packet or a
   channel mismatch) and append MetricObservation + MetricRollupObservation
   Silver records with a FRESH ``--generated-at-utc`` (defaults to now -- unlike
   the genesis runner, which defaults to the seed's genesis timestamp);
3. ``run_creator_metric_rollup_snapshot --platform youtube`` to advance the
   committed snapshot (the selection manifest's run-order chain guards the
   advance);
4. ``run_creator_profile_current_materialize --write`` to refresh the view.

Each cycle appends -- never rewrites -- so the longitudinal per-account rollup
history accrues in the lake; ``run_creator_rollup_formula_revalidation`` can
recompute the whole history at any time.

This runner WRITES to the lake: the producer is append-only with no dry-run, so
each invocation deposits durable records (durable real-lake writes stay
owner-gated and operator-box-only). CI never resolves the real lake; the
testable core (``run_watch_packet_producer``) runs against
``DataLakeRoot.for_test``, and ``main``/``resolve`` is the only real-lake-bound
path.
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

from capture_spine.creator_profile_current.youtube_metric_seed import ledger_video_retirements
from capture_spine.creator_profile_current.youtube_silver_metric_producer import (
    YoutubeCreatorMetricSilverResult,
    derive_youtube_creator_metric_silver_records_from_seed,
)
from capture_spine.creator_profile_current.youtube_watch_packet_metric_document import (
    YOUTUBE_WATCH_PACKET_METRIC_RECIPE_VERSION,
    build_youtube_watch_packet_metric_document,
)
from data_lake.root import DataLakeRoot, DataLakeRootError

ROOT = Path(__file__).resolve().parents[2]
_SOCIAL_MEDIA = (
    ROOT / "orca" / "product" / "spines" / "capture" / "core" / "source_families" / "social_media"
)
DEFAULT_ACCOUNT_LEDGER = (
    _SOCIAL_MEDIA / "creator_registry" / "creator_public_handle_linkage_ledger_v0.json"
)
DEFAULT_CREATOR_LEDGER = (
    _SOCIAL_MEDIA / "youtube" / "youtube_shorts_fragrance_creator_observation_ledger_v0.json"
)


def _load_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def _now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def run_watch_packet_producer(
    data_root: DataLakeRoot,
    *,
    creator_ledger: Mapping[str, Any],
    account_ledger: Mapping[str, Any],
    generated_at_utc: str,
    use_bronze_attachment_records: bool = False,
    excluded_video_ids: Mapping[str, str] | None = None,
) -> YoutubeCreatorMetricSilverResult:
    """Build the live watch-packet metric document, then append its observation
    + rollup records to the lake. The testable core -- lake-parameterized so it
    runs against ``DataLakeRoot.for_test``. ``excluded_video_ids`` is the
    explicit operator-exclusion map for observably-dead admitted videos; the
    builder records every exclusion loudly and fails closed on unknown ids or
    an account-fatal exclusion set."""
    document = build_youtube_watch_packet_metric_document(
        data_root,
        creator_ledger=creator_ledger,
        account_ledger=account_ledger,
        generated_at_utc=generated_at_utc,
        excluded_video_ids=excluded_video_ids,
    )
    return derive_youtube_creator_metric_silver_records_from_seed(
        data_root=data_root,
        seed_document=document,
        use_bronze_attachment_records=use_bronze_attachment_records,
    )


def resolve_effective_exclusions(
    cli_exclusions: Mapping[str, str] | None,
    creator_ledger: Mapping[str, Any],
) -> tuple[dict[str, str] | None, dict[str, str]]:
    """Merge the ledger's attested ``operator_video_retirements`` with per-cycle
    CLI exclusions. Returns ``(effective_exclusions_or_none, ledger_retirements)``.
    Raises ``ValueError`` on a CLI/ledger overlap: retirements apply
    automatically, so a duplicate flag makes the recorded reason ambiguous."""
    ledger_retirements = ledger_video_retirements(creator_ledger)
    if cli_exclusions and ledger_retirements:
        overlap = sorted(set(cli_exclusions) & set(ledger_retirements))
        if overlap:
            raise ValueError(
                "--exclude-video duplicates ledger-retired video(s): "
                + ", ".join(overlap)
                + " (ledger retirements apply automatically; drop the flag or the ledger entry)"
            )
    if not ledger_retirements:
        return (dict(cli_exclusions) if cli_exclusions else None), {}
    return {**ledger_retirements, **(cli_exclusions or {})}, ledger_retirements


def _account_of(record: Mapping[str, Any]) -> str | None:
    try:
        return record["payload"]["observation"]["subject"]["ref"]["orca_platform_account_id"]
    except (KeyError, TypeError):
        return None


def _engagement_observed(record: Mapping[str, Any]) -> bool:
    try:
        metrics = record["payload"]["observation"]["metric_rollups"]
    except (KeyError, TypeError):
        return False
    return any(
        metrics.get(name, {}).get("metric_posture", {}).get("kind") == "observed"
        for name in ("engagement_rate", "average_like_count", "average_comment_count")
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Append YouTube creator-metric Silver rollups to the data lake from the latest "
            "committed LIVE watch packets for the ledger-admitted Shorts pool "
            f"(recipe {YOUTUBE_WATCH_PACKET_METRIC_RECIPE_VERSION})."
        )
    )
    parser.add_argument("--account-ledger", type=Path, default=DEFAULT_ACCOUNT_LEDGER)
    parser.add_argument(
        "--creator-ledger",
        type=Path,
        default=DEFAULT_CREATOR_LEDGER,
        help="YouTube creator observation ledger naming the admitted video pool.",
    )
    parser.add_argument("--data-root", default=None, help="Lake root; defaults to ORCA_DATA_ROOT.")
    parser.add_argument(
        "--generated-at-utc",
        default=None,
        help=(
            "computed_at for the derived rollups. Defaults to now (UTC) -- a fresh recapture "
            "timestamp, NOT the genesis seed timestamp."
        ),
    )
    parser.add_argument(
        "--use-bronze-attachment-records",
        action="store_true",
        help=(
            "Upgrade observation raw_refs from packet/file refs to public Bronze Attachment "
            "Record refs when generated catalog rows exist."
        ),
    )
    parser.add_argument(
        "--exclude-video",
        action="append",
        dest="excluded_videos",
        default=None,
        metavar="VIDEO_ID",
        help=(
            "Explicitly exclude an admitted video from this cycle (repeatable). Requires "
            "--exclusion-reason. Recorded loudly in the document and affected rollup "
            "limitations; fails closed on unknown ids or account-fatal exclusion sets."
        ),
    )
    parser.add_argument(
        "--exclusion-reason",
        default=None,
        help="Operator-attested reason applied to every --exclude-video id (required with exclusions).",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    generated_at = args.generated_at_utc or _now_utc()

    excluded_video_ids: dict[str, str] | None = None
    if args.excluded_videos:
        seen: set[str] = set()
        duplicate_videos: set[str] = set()
        for video_id in args.excluded_videos:
            if video_id in seen:
                duplicate_videos.add(video_id)
            seen.add(video_id)
        if duplicate_videos:
            parser.exit(
                status=2,
                message=(
                    "--exclude-video was provided more than once for: "
                    + ", ".join(sorted(duplicate_videos))
                    + "\n"
                ),
            )
        if not args.exclusion_reason or not args.exclusion_reason.strip():
            parser.exit(
                status=2,
                message="--exclude-video requires a non-empty --exclusion-reason\n",
            )
        excluded_video_ids = {
            video_id: args.exclusion_reason.strip() for video_id in args.excluded_videos
        }
    elif args.exclusion_reason:
        parser.exit(status=2, message="--exclusion-reason requires at least one --exclude-video\n")

    try:
        data_root = DataLakeRoot.resolve(explicit=args.data_root)
    except DataLakeRootError as exc:
        parser.exit(status=2, message=f"data lake unavailable: {exc}\n")

    data_root.rebuild_availability()  # watch-packet discovery reads the availability index

    creator_ledger = _load_json(args.creator_ledger)
    account_document = _load_json(args.account_ledger)
    account_ledger = account_document.get("creator_public_handle_linkage_ledger", account_document)

    try:
        excluded_video_ids, ledger_retirements = resolve_effective_exclusions(
            excluded_video_ids, creator_ledger
        )
    except ValueError as exc:
        parser.exit(status=2, message=f"{exc}\n")

    try:
        result = run_watch_packet_producer(
            data_root,
            creator_ledger=creator_ledger,
            account_ledger=account_ledger,
            generated_at_utc=generated_at,
            use_bronze_attachment_records=args.use_bronze_attachment_records,
            excluded_video_ids=excluded_video_ids,
        )
    except Exception as exc:  # noqa: BLE001 - operator feedback; fail-closed, no partial-success masking
        parser.exit(
            status=2,
            message=(
                "youtube watch-packet creator metric rollup producer failed: "
                f"{type(exc).__name__}: {exc}\n"
            ),
        )

    accounts = sorted({a for a in (_account_of(r) for r in result.rollup_records) if a})
    engagement_rollups = sum(1 for record in result.rollup_records if _engagement_observed(record))
    print(
        f"appended {len(result.rollup_records)} rollup(s) + "
        f"{len(result.observation_records)} observation(s) for {len(accounts)} account(s) "
        f"at computed_at={generated_at} "
        f"({engagement_rollups} rollup(s) carry observed engagement metrics)"
    )
    if excluded_video_ids:
        print(
            f"  operator exclusions ({len(excluded_video_ids)}, "
            f"{len(ledger_retirements)} from ledger operator_video_retirements): "
            + "; ".join(f"{vid} ({reason})" for vid, reason in sorted(excluded_video_ids.items()))
        )
    for path in result.rollup_paths:
        print(f"  rollup: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
