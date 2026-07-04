"""Operator runner: the standalone live-lake freshness gate (AR-02).

Resolves the real external lake (fail-closed when ``FORSETI_DATA_ROOT``/``ORCA_DATA_ROOT`` is unset),
loads the committed creator-metric rollup snapshot + selection manifest for one
platform, and re-runs latest-per-account selection against the live lake to check
the committed snapshot still matches it. Exit ``0`` == fresh; exit ``2`` == drift
(``snapshot_behind_lake``) or a fail-closed lake error. The parseable line + exit
code are what a scheduled drift job wraps (open/update an issue on non-zero) --
this runner builds the check, not the scheduler.

CI never resolves the real lake: the testable core (``check_live_lake_freshness``)
runs against ``DataLakeRoot.for_test``; ``main``/``resolve`` is the only
real-lake-bound path (operator-local; ``pytest.skip`` in CI).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from capture_spine.creator_profile_current.live_lake_freshness_gate import (
    check_live_lake_freshness,
)
from capture_spine.creator_profile_current.silver_metric_reader import (
    CreatorRollupDiscoveryError,
    LatestRollupSelectionError,
)
from capture_spine.creator_profile_current.silver_metric_snapshot import (
    SnapshotGenerationError,
)
from data_lake.root import DataLakeRoot, DataLakeRootError

ROOT = Path(__file__).resolve().parents[2]
_SOCIAL_MEDIA = (
    ROOT / "orca" / "product" / "spines" / "capture" / "core" / "source_families" / "social_media"
)
DEFAULT_ACCOUNT_LEDGER = (
    _SOCIAL_MEDIA / "creator_registry" / "creator_public_handle_linkage_ledger_v0.json"
)

# Committed artifacts per platform -- what this gate verifies against the live
# lake (the snapshot + its selection manifest the snapshot runner wrote).
_PLATFORM_ARTIFACTS: dict[str, dict[str, Path]] = {
    "instagram": {
        "snapshot": _SOCIAL_MEDIA / "instagram" / "instagram_reels_creator_metric_rollup_snapshot_v0.json",
        "manifest": _SOCIAL_MEDIA / "instagram" / "instagram_reels_creator_metric_rollup_selection_manifest_v0.json",
    },
    "youtube": {
        "snapshot": _SOCIAL_MEDIA / "youtube" / "youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json",
        "manifest": _SOCIAL_MEDIA / "youtube" / "youtube_shorts_fragrance_creator_metric_rollup_selection_manifest_v0.json",
    },
}


def _load_json(path: Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _load_account_ledger(path: Path) -> Mapping[str, Any]:
    # The generator wants the inner {platform_accounts} block; the committed
    # ledger wraps it under its top-level key (matches the producer/snapshot runners).
    document = _load_json(path)
    return document.get("creator_public_handle_linkage_ledger", document)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Check that the committed creator-metric rollup snapshot still matches the "
            "live external data lake (the standalone/scheduled freshness gate, AR-02)."
        )
    )
    parser.add_argument("--platform", choices=sorted(_PLATFORM_ARTIFACTS), default="instagram")
    parser.add_argument("--account-ledger", type=Path, default=DEFAULT_ACCOUNT_LEDGER)
    parser.add_argument("--snapshot", type=Path, default=None, help="Committed snapshot path; defaults to the platform's.")
    parser.add_argument("--manifest", type=Path, default=None, help="Committed selection manifest path; defaults to the platform's.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    artifacts = _PLATFORM_ARTIFACTS[args.platform]
    snapshot_path = args.snapshot or artifacts["snapshot"]
    manifest_path = args.manifest or artifacts["manifest"]

    missing = next((p for p in (snapshot_path, manifest_path) if not p.is_file()), None)
    if missing is not None:
        parser.exit(status=2, message=f"no committed snapshot/manifest to verify for {args.platform}: {missing}\n")

    try:
        data_root = DataLakeRoot.resolve()
    except DataLakeRootError as exc:
        parser.exit(
            status=2,
            message=f"data lake unavailable (the freshness gate reconciles against the live lake): {exc}\n",
        )

    data_root.rebuild_availability()  # IG discovery reads the availability index
    account_ledger = _load_account_ledger(args.account_ledger)
    committed_snapshot = _load_json(snapshot_path)
    committed_manifest = _load_json(manifest_path)

    try:
        result = check_live_lake_freshness(
            data_root,
            account_ledger=account_ledger,
            platform=args.platform,
            committed_snapshot=committed_snapshot,
            committed_manifest=committed_manifest,
        )
    except (SnapshotGenerationError, LatestRollupSelectionError, CreatorRollupDiscoveryError) as exc:
        parser.exit(
            status=2,
            message=f"live-lake freshness gate failed closed ({args.platform}): {type(exc).__name__}: {exc}\n",
        )

    if result.is_fresh:
        print(f"FRESH: {args.platform} snapshot matches the live lake (watermark {result.committed_watermark})")
        return 0
    print(
        f"DRIFT ({result.reason}): {args.platform} snapshot is behind the live lake; "
        f"drifted accounts: {', '.join(result.drifted_accounts) or '(watermark only)'}; "
        f"committed={result.committed_watermark} live={result.live_watermark}"
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
