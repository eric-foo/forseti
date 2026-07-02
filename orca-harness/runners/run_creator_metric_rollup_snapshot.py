"""Operator runner for the creator-metric rollup SNAPSHOT -- STEP 3 of the lake
cut-over.

The STEP-2b generator (``silver_metric_snapshot.py``) is PURE: it reads the lake
and returns the snapshot + selection-manifest dicts, writing nothing. This runner
is the operator-facing shell the generator was built to feed: it resolves the
real external lake (``DataLakeRoot.resolve``, fail-closed when ``ORCA_DATA_ROOT``
is unset), rebuilds the availability index first (IG discovery depends on it),
loads the prior committed manifest, runs the generator for ONE platform, gates
the result against the live lake, and writes the snapshot + manifest + a
durable freshness receipt.

Three fail-closed guards (the load-bearing safety of this step):

- **Manifest-chain co-presence block (AR-02).** A committed snapshot and its
  selection manifest must be BOTH present-and-valid (the manifest is loaded as
  ``prior_manifest`` so the run-id chain advances) or BOTH absent (genesis,
  ``prior_manifest=None``, run id 1). Any other combination BLOCKS rather than
  passing ``None`` while a snapshot exists -- which would silently reset
  ``selection_run_id`` to 1 and break the run-order chain. *Named limitation:*
  this verifies LOCAL co-presence/validity only (we retain just the latest
  manifest, not the full history), which is the smallest-complete fail-closed.
- **Write-time freshness gate.** After generating, the generator is re-run
  deterministically; if the live lake advanced between the two reads
  (``lake_high_watermark`` / per-account content hashes differ) the run fails
  ``lake_moved_during_snapshot`` rather than committing a snapshot the lake has
  already superseded. The durable freshness receipt records the reconciled
  watermark so a reviewer can see the registry's freshness epoch.
- **Generated-artifact validation.** The snapshot and manifest must pass their
  schema validators before anything is written.

Boundary (smallest complete -- explicitly NOT pulled forward): this runner does
NOT re-point ``materialize`` onto the snapshot (a later step), and the
write-time gate here is the runner's own inline reconciliation -- it does NOT
build the standalone ``live_lake_freshness_gate`` module or the scheduled drift
check. Per-platform by invocation (``--platform``): YouTube is a separate
fold-in stage and is never generated implicitly alongside Instagram. CI never
resolves the real lake; the runner's core is exercised against
``DataLakeRoot.for_test`` and only ``main``'s ``resolve`` touches the live lake.
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from capture_spine.creator_profile_current.silver_metric_reader import (
    CreatorRollupDiscoveryError,
    LatestRollupSelectionError,
)
from capture_spine.creator_profile_current.silver_metric_snapshot import (
    SNAPSHOT_WRAPPER_KEY,
    SnapshotGenerationError,
    generate_creator_metric_rollup_snapshot,
    validate_manifest,
    validate_snapshot,
)
from data_lake.root import DataLakeRoot, DataLakeRootError

ROOT = Path(__file__).resolve().parents[2]
_SOCIAL_MEDIA = (
    ROOT / "orca" / "product" / "spines" / "capture" / "core" / "source_families" / "social_media"
)
DEFAULT_ACCOUNT_LEDGER = (
    _SOCIAL_MEDIA / "creator_registry" / "creator_public_handle_linkage_ledger_v0.json"
)

RECEIPT_SCHEMA_VERSION = "creator_metric_rollup_freshness_receipt_v0"
RECEIPT_WRAPPER_KEY = "creator_metric_rollup_freshness_receipt"


@dataclass(frozen=True)
class _PlatformOutputs:
    snapshot: Path
    manifest: Path
    receipt: Path


# Snapshot/manifest/receipt co-locate per platform with the seed each supersedes
# (IG seed under instagram/, YT seed under youtube/). STEP 3 commits no data
# artifact; these are only the defaults the operator writes to at the §4 first
# snapshot.
_PLATFORM_OUTPUTS: dict[str, _PlatformOutputs] = {
    "instagram": _PlatformOutputs(
        snapshot=_SOCIAL_MEDIA / "instagram" / "instagram_reels_creator_metric_rollup_snapshot_v0.json",
        manifest=_SOCIAL_MEDIA / "instagram" / "instagram_reels_creator_metric_rollup_selection_manifest_v0.json",
        receipt=_SOCIAL_MEDIA / "instagram" / "instagram_reels_creator_metric_rollup_freshness_receipt_v0.json",
    ),
    "youtube": _PlatformOutputs(
        snapshot=_SOCIAL_MEDIA / "youtube" / "youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json",
        manifest=_SOCIAL_MEDIA / "youtube" / "youtube_shorts_fragrance_creator_metric_rollup_selection_manifest_v0.json",
        receipt=_SOCIAL_MEDIA / "youtube" / "youtube_shorts_fragrance_creator_metric_rollup_freshness_receipt_v0.json",
    ),
}


class SnapshotRunError(ValueError):
    """Runner-level fail-closed (distinct from the generator's
    ``SnapshotGenerationError``): the chain is locally broken or the lake moved
    under the run."""

    def __init__(self, reason: str, detail: str = "") -> None:
        self.reason = reason
        self.detail = detail
        super().__init__(f"{reason}: {detail}" if detail else reason)


def _load_json(path: Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _dump_json(obj: Any) -> str:
    # Canonical key ordering (sort_keys=True), consistent with how lake records
    # are stored. The file is therefore canonically keyed -- the later no-drift
    # bridge to the hand-authored seed must compare rollup VALUES (dict /
    # canonical-bytes equal), NOT raw file bytes, because the seed's key order is
    # independent of this dump.
    return json.dumps(obj, indent=2, ensure_ascii=False, sort_keys=True) + "\n"


def _now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _load_prior_manifest(snapshot_path: Path, manifest_path: Path) -> Mapping[str, Any] | None:
    """Manifest-chain co-presence block (AR-02). Returns the prior manifest to
    chain from, ``None`` at genesis, or BLOCKS on a locally broken chain. The
    snapshot and manifest must be co-present AND both schema-valid: a committed
    artifact that is unreadable (non-JSON) or schema-invalid fails closed rather
    than letting a broken chain through."""
    snapshot_present = snapshot_path.exists()
    manifest_present = manifest_path.exists()
    if not snapshot_present and not manifest_present:
        return None  # genesis -- the generator stamps run id 1
    if snapshot_present != manifest_present:
        raise SnapshotRunError(
            "manifest_chain_broken",
            f"snapshot present={snapshot_present} but manifest present={manifest_present}; "
            "a committed snapshot and its selection manifest must co-exist "
            "(refusing to reset selection_run_id to 1 against an existing snapshot)",
        )
    manifest = _load_committed(manifest_path)
    errors = validate_manifest(manifest) + [
        f"snapshot: {e}" for e in validate_snapshot(_load_committed(snapshot_path))
    ]
    if errors:
        raise SnapshotRunError(
            "manifest_chain_broken",
            f"committed snapshot/manifest is invalid: {errors}",
        )
    return manifest


def _load_committed(path: Path) -> Any:
    """Load a committed JSON artifact, failing closed (manifest_chain_broken) if
    it is unreadable -- so a truncated/corrupt committed file cannot crash the
    runner with an uncaught error."""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        raise SnapshotRunError(
            "manifest_chain_broken", f"committed artifact unreadable ({path.name}): {exc}"
        ) from exc


def _build_receipt(snapshot: Mapping[str, Any], platform: str, reconciled_at: str) -> dict[str, Any]:
    prov = snapshot[SNAPSHOT_WRAPPER_KEY]["snapshot_provenance"]
    return {
        RECEIPT_WRAPPER_KEY: {
            "schema_version": RECEIPT_SCHEMA_VERSION,
            "platform_scope": platform,
            "snapshot_generated_at": prov["snapshot_generated_at"],
            "reconciled_at": reconciled_at,
            "lake_high_watermark": prov["lake_high_watermark"],
            "selection_run_id": prov["selection_run_id"],
            "per_account": [
                {"profile_subject_id": e["profile_subject_id"], "content_hash": e["content_hash"]}
                for e in prov["per_account"]
            ],
        }
    }


def run_snapshot(
    data_root: DataLakeRoot,
    *,
    account_ledger: Mapping[str, Any],
    platform: str,
    snapshot_generated_at: str,
    reconciled_at: str,
    snapshot_path: Path,
    manifest_path: Path,
    receipt_path: Path,
    write: bool,
) -> dict[str, Any]:
    """Generate, gate, and (when ``write``) persist one platform's snapshot +
    manifest + freshness receipt. The testable core -- lake-parameterized so it
    runs against ``DataLakeRoot.for_test`` with no real lake."""
    prior_manifest = _load_prior_manifest(snapshot_path, manifest_path)

    run = generate_creator_metric_rollup_snapshot(
        data_root,
        account_ledger=account_ledger,
        platform=platform,
        snapshot_generated_at=snapshot_generated_at,
        prior_manifest=prior_manifest,
    )

    # Write-time freshness gate: re-run the (pure, deterministic) generator and
    # confirm the live lake did not advance between the two reads. Re-calling the
    # public generator avoids duplicating the run-order/selection internals.
    verify = generate_creator_metric_rollup_snapshot(
        data_root,
        account_ledger=account_ledger,
        platform=platform,
        snapshot_generated_at=snapshot_generated_at,
        prior_manifest=prior_manifest,
    )
    prov = run.snapshot[SNAPSHOT_WRAPPER_KEY]["snapshot_provenance"]
    vprov = verify.snapshot[SNAPSHOT_WRAPPER_KEY]["snapshot_provenance"]
    if prov["lake_high_watermark"] != vprov["lake_high_watermark"] or prov["per_account"] != vprov["per_account"]:
        raise SnapshotRunError(
            "lake_moved_during_snapshot",
            "the live lake advanced between generation and the freshness re-check; "
            "refusing to commit a snapshot the lake has already superseded",
        )

    snapshot_errors = validate_snapshot(run.snapshot)
    manifest_errors = validate_manifest(run.manifest)
    if snapshot_errors or manifest_errors:
        raise SnapshotRunError(
            "invalid_generated_artifact",
            f"snapshot={snapshot_errors} manifest={manifest_errors}",
        )

    receipt = _build_receipt(run.snapshot, platform, reconciled_at)

    if write:
        for path, obj in (
            (snapshot_path, run.snapshot),
            (manifest_path, run.manifest),
            (receipt_path, receipt),
        ):
            path.parent.mkdir(parents=True, exist_ok=True)
            # newline="\n": keep committed artifacts LF on a Windows operator box
            # (write_text would otherwise translate to CRLF and break the repo's
            # LF text convention + the view's lf_repo_text gate at §5).
            path.write_text(_dump_json(obj), encoding="utf-8", newline="\n")

    return {
        "platform": platform,
        "selection_run_id": prov["selection_run_id"],
        "lake_high_watermark": prov["lake_high_watermark"],
        "accounts": len(prov["per_account"]),
        "wrote": write,
        "snapshot": run.snapshot,
        "manifest": run.manifest,
        "receipt": receipt,
        "snapshot_path": snapshot_path,
        "manifest_path": manifest_path,
        "receipt_path": receipt_path,
    }


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Generate the committed creator-metric rollup snapshot + selection manifest + "
            "freshness receipt for ONE platform from the live external data lake."
        )
    )
    parser.add_argument(
        "--platform",
        choices=sorted(_PLATFORM_OUTPUTS),
        default="instagram",
        help="Which platform to snapshot (one per run; YouTube is a separate fold-in stage).",
    )
    parser.add_argument("--account-ledger", type=Path, default=DEFAULT_ACCOUNT_LEDGER)
    parser.add_argument(
        "--generated-at-utc",
        help="Timestamp for snapshot_generated_at / reconciled_at. Defaults to now (UTC).",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Persist the snapshot/manifest/receipt. Default is a dry-run (generate + gate + report).",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    generated_at = args.generated_at_utc or _now_utc()
    outputs = _PLATFORM_OUTPUTS[args.platform]

    try:
        data_root = DataLakeRoot.resolve()
    except DataLakeRootError as exc:
        parser.exit(
            status=2,
            message=f"data lake unavailable (this runner reconciles against the live external lake): {exc}\n",
        )

    data_root.rebuild_availability()  # IG discovery reads the availability index
    # The generator wants the inner {platform_accounts} block; the committed
    # ledger wraps it under its top-level key (matches the producer runner).
    document = _load_json(args.account_ledger)
    account_ledger = document.get("creator_public_handle_linkage_ledger", document)

    try:
        summary = run_snapshot(
            data_root,
            account_ledger=account_ledger,
            platform=args.platform,
            snapshot_generated_at=generated_at,
            reconciled_at=generated_at,
            snapshot_path=outputs.snapshot,
            manifest_path=outputs.manifest,
            receipt_path=outputs.receipt,
            write=args.write,
        )
    except (
        SnapshotRunError,
        SnapshotGenerationError,
        LatestRollupSelectionError,
        CreatorRollupDiscoveryError,
    ) as exc:
        parser.exit(status=2, message=f"creator metric rollup snapshot failed: {exc}\n")

    action = "wrote" if summary["wrote"] else "previewed (dry-run; pass --write to persist)"
    print(
        f"{action} {args.platform} snapshot: run_id={summary['selection_run_id']} "
        f"accounts={summary['accounts']} watermark={summary['lake_high_watermark']}"
    )
    if summary["wrote"]:
        print(f"  snapshot: {summary['snapshot_path']}")
        print(f"  manifest: {summary['manifest_path']}")
        print(f"  receipt:  {summary['receipt_path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
