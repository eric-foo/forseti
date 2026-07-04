"""Live-lake freshness gate -- the sole proof that the committed creator-metric
rollup snapshot still matches the live external lake (AR-02 of the lake cut-over).

The committed snapshot is a frozen read model. Between regenerations the operator
can append new rollups to the lake, leaving the registry silently behind. This
gate re-runs latest-per-account selection against the live lake (reusing the pure
snapshot generator) and compares the resulting content-addressed watermark +
per-account ``content_hash`` set to the committed snapshot's. Equal -> the
snapshot is fresh; different -> ``snapshot_behind_lake`` (the lake advanced past
the committed snapshot).

The verdict is content-addressed only (no producer clock), so it re-imports no
clock trust. This module is PURE: it reads and compares, and writes nothing. It
runs only where a real lake exists (operator box / scheduled job); CI exercises
the testable core against ``DataLakeRoot.for_test`` and never resolves the real
lake.

Bound at both AR-02 triggers of the same check: the write-time receipt gate
(already in ``run_creator_metric_rollup_snapshot``) keeps a just-written snapshot
honest against the lake it was generated from; this standalone check is what a
scheduled drift job runs to catch staleness accruing *between* regenerations --
the silent-drift case the write-time gate alone cannot close.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Mapping

from capture_spine.creator_profile_current.silver_metric_snapshot import (
    SNAPSHOT_WRAPPER_KEY,
    generate_creator_metric_rollup_snapshot,
)

if TYPE_CHECKING:
    from data_lake.root import DataLakeRoot

SNAPSHOT_BEHIND_LAKE = "snapshot_behind_lake"


@dataclass(frozen=True)
class FreshnessCheckResult:
    """The verdict of one live-lake freshness check. ``is_fresh`` True means the
    committed snapshot's selection still matches the live lake; otherwise
    ``reason`` is ``snapshot_behind_lake`` and ``drifted_accounts`` names the
    accounts whose live ``content_hash`` differs from (or is present on only one
    side of) the committed snapshot."""

    is_fresh: bool
    reason: str | None
    committed_watermark: str
    live_watermark: str
    drifted_accounts: tuple[str, ...]


def _provenance(snapshot: Mapping[str, Any]) -> Mapping[str, Any]:
    return snapshot[SNAPSHOT_WRAPPER_KEY]["snapshot_provenance"]


def _per_account_hashes(snapshot: Mapping[str, Any]) -> dict[str, str]:
    return {
        entry["profile_subject_id"]: entry["content_hash"]
        for entry in _provenance(snapshot)["per_account"]
    }


def check_live_lake_freshness(
    data_root: "DataLakeRoot",
    *,
    account_ledger: Mapping[str, Any],
    platform: str,
    committed_snapshot: Mapping[str, Any],
    committed_manifest: Mapping[str, Any] | None,
) -> FreshnessCheckResult:
    """Compare the committed snapshot against a fresh live-lake selection.

    Re-runs the pure snapshot generator against ``data_root`` (the live lake)
    using the committed manifest as the prior run-order memory, then compares the
    content-addressed watermark + per-account ``content_hash`` set. Returns a
    verdict; propagates the generator's fail-closed errors (a
    regressed/ambiguous/broken lake state is a freshness failure to surface, not
    a silent pass). Writes nothing. The testable core -- lake-parameterized so it
    runs against ``DataLakeRoot.for_test``."""
    fresh = generate_creator_metric_rollup_snapshot(
        data_root,
        account_ledger=account_ledger,
        platform=platform,
        # The verdict is content-addressed (watermark + per-account content_hash);
        # snapshot_generated_at is provenance metadata only, so reuse the committed
        # value -- no wall-clock, fully deterministic.
        snapshot_generated_at=_provenance(committed_snapshot)["snapshot_generated_at"],
        prior_manifest=committed_manifest,
    )

    committed_hashes = _per_account_hashes(committed_snapshot)
    live_hashes = _per_account_hashes(fresh.snapshot)
    drifted = tuple(
        sorted(
            account
            for account in set(committed_hashes) | set(live_hashes)
            if committed_hashes.get(account) != live_hashes.get(account)
        )
    )
    committed_watermark = _provenance(committed_snapshot)["lake_high_watermark"]
    live_watermark = _provenance(fresh.snapshot)["lake_high_watermark"]
    is_fresh = committed_watermark == live_watermark and not drifted
    return FreshnessCheckResult(
        is_fresh=is_fresh,
        reason=None if is_fresh else SNAPSHOT_BEHIND_LAKE,
        committed_watermark=committed_watermark,
        live_watermark=live_watermark,
        drifted_accounts=drifted,
    )


__all__ = ["FreshnessCheckResult", "SNAPSHOT_BEHIND_LAKE", "check_live_lake_freshness"]
