"""Generate the committed creator-metric rollup SNAPSHOT (+ its selection
manifest) that ``creator_profile_current`` reads -- STEP 2b of the lake cut-over.

This is the orchestrator the merged primitives were built to feed:
``discover_creator_metric_rollup_records`` (STEP 2a) finds an account's rollup
records, this module assigns each a run-order signal and calls
``select_latest_rollup_per_account`` (STEP 1) to pick the latest, then emits a
committed snapshot (the read model) plus a selection manifest (the run-order
memory).

The ordering authority (the load-bearing decision, hardened by a cross-vendor
review):

- ``selection_run_id`` is a monotonic integer **owned by the snapshot run**
  (``max(prior selection ids) + 1``), NOT derived from any record field. A
  forward-skewed producer clock cannot touch it, so STEP 1's ``computed_at``
  guards become a load-bearing cross-check (an independent axis) instead of
  colluding with the clock.
- **Bootstrap never clock-orders.** With no prior manifest, every discovered
  record is "new" and shares run id 1; if an account presents >1 distinct
  ``content_hash`` there, STEP 1 fails ``ambiguous_latest_rollup`` -- a human (or
  an owner-authored initial manifest) resolves it. At one-rollup-per-account
  (today's shape) this never fires.
- **Steady-state advance is double-gated.** The manifest remembers, per account,
  the chosen record and the set of ``content_hash``es already seen. A record
  whose hash is *not* in that seen-set is "new this run" and gets the current run
  id; it competes only with the prior-selected record (which carries its old run
  id), so STEP 1's regression guard fires if the "advance" is not genuinely
  newer. Old non-chosen records need no run id -- they are dominated by the prior
  selection and excluded.

Boundary: this module is PURE generation -- it returns the snapshot + manifest
dicts and writes nothing. The operator runner (``DataLakeRoot.resolve``,
``rebuild_availability`` first, freshness receipt, the capture->snapshot
coupling that keeps the one-new-per-account precondition, and the manifest-chain
recovery block) is a later step, as is re-pointing ``materialize`` onto the
snapshot and the live-lake freshness gate. ``snapshot_generated_at`` is supplied
by the caller (no wall-clock here), so generation is deterministic.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Mapping

from capture_spine.creator_profile_current.silver_metric_producer import METRIC_ROLLUP_LANE
from capture_spine.creator_profile_current.silver_metric_reader import (
    RollupRunCandidate,
    SelectedRollup,
    discover_creator_metric_rollup_records,
    select_latest_rollup_per_account,
)
from data_lake.canonical_json import canonical_record_bytes as _canonical_bytes

if TYPE_CHECKING:
    from data_lake.root import DataLakeRoot

SNAPSHOT_SCHEMA_VERSION = "creator_metric_rollup_snapshot_v0"
MANIFEST_SCHEMA_VERSION = "creator_metric_rollup_selection_manifest_v0"
SNAPSHOT_WRAPPER_KEY = "creator_metric_rollup_snapshot"
MANIFEST_WRAPPER_KEY = "creator_metric_rollup_selection_manifest"

# Lake-provenance keys that must NEVER appear inside a ``metric_rollups`` entry:
# the consumed array stays byte-equal to the seed-shaped rollups, and provenance
# lives in the sibling ``snapshot_provenance`` block (the view validator rejects
# these keys, and embedding them would break the no-drift byte-equality bridge).
_FORBIDDEN_ROLLUP_KEYS = frozenset(
    {"source_record", "content_hash", "record_id", "raw_anchor", "lane_namespace"}
)


class SnapshotGenerationError(ValueError):
    """Raised when the snapshot generator cannot produce a trustworthy snapshot
    and must fail closed. Subclasses ``ValueError`` for fail-closed
    compatibility; ``reason`` is the machine code and ``account_id`` is the
    account it failed on (``""`` for a run-level failure).
    """

    def __init__(self, reason: str, account_id: str, detail: str) -> None:
        self.reason = reason
        self.account_id = account_id
        prefix = f"{reason} for account {account_id!r}" if account_id else reason
        super().__init__(f"{prefix}: {detail}")


@dataclass(frozen=True)
class SnapshotRun:
    """The outputs of one snapshot generation: the committed read-model snapshot
    and the selection manifest (the run-order memory for the next run). Both are
    plain dicts; the operator runner is what serializes and commits them."""

    snapshot: dict[str, Any]
    manifest: dict[str, Any]


def generate_creator_metric_rollup_snapshot(
    data_root: "DataLakeRoot",
    *,
    account_ledger: Mapping[str, Any],
    platform: str,
    snapshot_generated_at: str,
    prior_manifest: Mapping[str, Any] | None = None,
) -> SnapshotRun:
    """Generate one per-platform snapshot + selection manifest from the lake.

    ``platform`` selects which ledger accounts to cover (snapshots are
    per-platform). ``prior_manifest`` is the previous committed manifest for this
    platform (``None`` at genesis). Fails closed (``SnapshotGenerationError`` or
    STEP 1's ``LatestRollupSelectionError``/``CreatorRollupDiscoveryError``)
    rather than ever committing a wrong or ambiguous selection.
    """
    platform_ledger = _platform_ledger(account_ledger, platform)
    discovered = discover_creator_metric_rollup_records(data_root, account_ledger=platform_ledger)

    prior = _index_prior_manifest(prior_manifest, platform)
    current_run_id = _next_run_id(prior)

    candidates: list[RollupRunCandidate] = []
    for account_id, records in discovered.items():
        candidates.extend(_account_candidates(account_id, records, prior.get(account_id), current_run_id))

    selected = select_latest_rollup_per_account(candidates)

    record_by_id = {
        record["record_id"]: record for records in discovered.values() for record in records
    }
    snapshot = _build_snapshot(platform, snapshot_generated_at, current_run_id, selected, record_by_id)
    manifest = _build_manifest(platform, current_run_id, selected, discovered, prior_manifest)
    return SnapshotRun(snapshot=snapshot, manifest=manifest)


# -- run-order assignment ----------------------------------------------------

@dataclass(frozen=True)
class _PriorEntry:
    selected_record_id: str
    selection_run_id: int
    seen_content_hashes: frozenset[str]


def _account_candidates(
    account_id: str,
    records: list[dict[str, Any]],
    prior: "_PriorEntry | None",
    current_run_id: int,
) -> list[RollupRunCandidate]:
    if prior is None:
        # Bootstrap (or a newly-added account): every record is new this run and
        # shares ``current_run_id``. One record -> trivially latest. >1 distinct
        # -> STEP 1 fails ``ambiguous_latest_rollup`` (we never clock-order at
        # bootstrap).
        return [RollupRunCandidate(current_run_id, record) for record in records]

    by_id = {record["record_id"]: record for record in records}
    prior_selected = by_id.get(prior.selected_record_id)
    if prior_selected is None:
        raise SnapshotGenerationError(
            "manifest_selected_record_missing",
            account_id,
            f"manifest selected_record_id {prior.selected_record_id!r} is not present in the lake",
        )
    # The prior selection (at its old run id) competes only with records new
    # since the manifest's seen-set; older non-chosen records are dominated by it
    # and need no run id.
    candidates = [RollupRunCandidate(prior.selection_run_id, prior_selected)]
    for record in records:
        if record["content_hash"] not in prior.seen_content_hashes:
            candidates.append(RollupRunCandidate(current_run_id, record))
    return candidates


def _index_prior_manifest(
    prior_manifest: Mapping[str, Any] | None, platform: str
) -> dict[str, _PriorEntry]:
    if prior_manifest is None:
        return {}
    body = prior_manifest.get(MANIFEST_WRAPPER_KEY)
    if not isinstance(body, dict):
        raise SnapshotGenerationError(
            "invalid_prior_manifest", "", f"prior manifest missing {MANIFEST_WRAPPER_KEY!r} wrapper"
        )
    if body.get("platform_scope") != platform:
        raise SnapshotGenerationError(
            "manifest_platform_mismatch",
            "",
            f"prior manifest platform_scope {body.get('platform_scope')!r} != requested {platform!r}",
        )
    out: dict[str, _PriorEntry] = {}
    for entry in body.get("entries", []):
        out[entry["profile_subject_id"]] = _PriorEntry(
            selected_record_id=entry["selected_record_id"],
            selection_run_id=entry["selection_run_id"],
            seen_content_hashes=frozenset(entry.get("seen_content_hashes", ())),
        )
    return out


def _next_run_id(prior: dict[str, _PriorEntry]) -> int:
    if not prior:
        return 1
    return max(entry.selection_run_id for entry in prior.values()) + 1


# -- artifact construction ---------------------------------------------------

def _build_snapshot(
    platform: str,
    snapshot_generated_at: str,
    current_run_id: int,
    selected: dict[str, SelectedRollup],
    record_by_id: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    per_account: list[dict[str, Any]] = []
    metric_rollups: list[dict[str, Any]] = []
    for account_id in sorted(selected):
        chosen = selected[account_id]
        record = record_by_id[chosen.record_id]
        per_account.append(
            {
                "profile_subject_id": chosen.account_id,
                "record_id": chosen.record_id,
                "content_hash": chosen.content_hash,
                "raw_anchor": record["raw_anchor"],
                "lane_namespace": record.get("lane_namespace", METRIC_ROLLUP_LANE),
                "selection_run_id": chosen.selection_run_id,
            }
        )
        metric_rollups.append(chosen.rollup)
    return {
        SNAPSHOT_WRAPPER_KEY: {
            "schema_version": SNAPSHOT_SCHEMA_VERSION,
            "platform_scope": platform,
            "snapshot_provenance": {
                "snapshot_generated_at": snapshot_generated_at,
                "selection_run_id": current_run_id,
                "lake_high_watermark": _content_watermark(selected),
                "per_account": per_account,
            },
            "metric_rollups": metric_rollups,
        }
    }


def _build_manifest(
    platform: str,
    current_run_id: int,
    selected: dict[str, SelectedRollup],
    discovered: dict[str, list[dict[str, Any]]],
    prior_manifest: Mapping[str, Any] | None,
) -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    for account_id in sorted(selected):
        chosen = selected[account_id]
        # The records are append-only and never deleted, so the current
        # discovered set already contains everything the prior seen-set held plus
        # anything new -- it IS the next seen-set.
        seen = sorted({record["content_hash"] for record in discovered[account_id]})
        entries.append(
            {
                "profile_subject_id": chosen.account_id,
                "selected_record_id": chosen.record_id,
                "selected_content_hash": chosen.content_hash,
                "selection_run_id": chosen.selection_run_id,
                "seen_content_hashes": seen,
            }
        )
    return {
        MANIFEST_WRAPPER_KEY: {
            "schema_version": MANIFEST_SCHEMA_VERSION,
            "platform_scope": platform,
            "selection_run_id": current_run_id,
            "parent_manifest_sha256": (
                None if prior_manifest is None else manifest_content_hash(prior_manifest)
            ),
            "entries": entries,
        }
    }


def _platform_ledger(account_ledger: Mapping[str, Any], platform: str) -> dict[str, Any]:
    accounts = account_ledger.get("platform_accounts")
    if not isinstance(accounts, list):
        raise SnapshotGenerationError(
            "invalid_account_ledger", "", "account ledger has no platform_accounts list"
        )
    return {"platform_accounts": [a for a in accounts if a.get("platform") == platform]}


def _content_watermark(selected: dict[str, SelectedRollup]) -> str:
    # A content-addressed watermark (the selected per-account content_hash set),
    # NOT a clock/position value -- so the freshness gate that compares it can
    # never re-import producer-clock trust.
    pairs = sorted(f"{chosen.account_id}:{chosen.content_hash}" for chosen in selected.values())
    return "sha256:" + hashlib.sha256("\n".join(pairs).encode("utf-8")).hexdigest()


def manifest_content_hash(manifest: Mapping[str, Any]) -> str:
    """Canonical content hash of a manifest, for the parent-manifest chain."""
    return "sha256:" + hashlib.sha256(_canonical_bytes(dict(manifest))).hexdigest()


# -- validators (the schema/validator deliverable) ---------------------------

def validate_snapshot(snapshot: Mapping[str, Any]) -> list[str]:
    """Return a list of human-readable schema violations (empty == valid). The
    load-bearing check: no provenance keys leak into ``metric_rollups`` (which
    must stay byte-equal to the seed-shaped rollups)."""
    errors: list[str] = []
    body = snapshot.get(SNAPSHOT_WRAPPER_KEY)
    if not isinstance(body, dict):
        return [f"snapshot missing {SNAPSHOT_WRAPPER_KEY!r} wrapper"]
    if body.get("schema_version") != SNAPSHOT_SCHEMA_VERSION:
        errors.append(f"snapshot schema_version is not {SNAPSHOT_SCHEMA_VERSION!r}")
    provenance = body.get("snapshot_provenance")
    if not isinstance(provenance, dict) or not isinstance(provenance.get("per_account"), list):
        errors.append("snapshot_provenance.per_account must be a list")
    rollups = body.get("metric_rollups")
    if not isinstance(rollups, list):
        errors.append("metric_rollups must be a list")
    else:
        for index, rollup in enumerate(rollups):
            leaked = _FORBIDDEN_ROLLUP_KEYS & set(rollup)
            if leaked:
                errors.append(
                    f"metric_rollups[{index}] carries provenance keys {sorted(leaked)} "
                    "(provenance must live in snapshot_provenance, not the consumed rollup)"
                )
    return errors


def validate_manifest(manifest: Mapping[str, Any]) -> list[str]:
    """Return a list of human-readable selection-manifest schema violations."""
    errors: list[str] = []
    body = manifest.get(MANIFEST_WRAPPER_KEY)
    if not isinstance(body, dict):
        return [f"manifest missing {MANIFEST_WRAPPER_KEY!r} wrapper"]
    if body.get("schema_version") != MANIFEST_SCHEMA_VERSION:
        errors.append(f"manifest schema_version is not {MANIFEST_SCHEMA_VERSION!r}")
    if "parent_manifest_sha256" not in body:
        errors.append("manifest missing parent_manifest_sha256 (the chain link)")
    entries = body.get("entries")
    if not isinstance(entries, list):
        errors.append("manifest entries must be a list")
    else:
        required = {"profile_subject_id", "selected_record_id", "selected_content_hash", "selection_run_id", "seen_content_hashes"}
        for index, entry in enumerate(entries):
            missing = required - set(entry)
            if missing:
                errors.append(f"manifest entries[{index}] missing {sorted(missing)}")
    return errors


__all__ = [
    "MANIFEST_SCHEMA_VERSION",
    "MANIFEST_WRAPPER_KEY",
    "SNAPSHOT_SCHEMA_VERSION",
    "SNAPSHOT_WRAPPER_KEY",
    "SnapshotGenerationError",
    "SnapshotRun",
    "generate_creator_metric_rollup_snapshot",
    "manifest_content_hash",
    "validate_manifest",
    "validate_snapshot",
]
