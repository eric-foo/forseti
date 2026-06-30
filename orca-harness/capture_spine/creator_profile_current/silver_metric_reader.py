"""Read creator-metric Silver Vault records back into the creator_profile_current
rollup shape -- the READ half of the creator-metric lake path.

The producer (``silver_metric_producer.py``) writes MetricObservation +
MetricRollupObservation Silver records into the lake. This module reads the
rollup records back and reconstructs the per-account ``metric_rollup`` dicts in
the exact shape the static metric seeds carry (the shape that
``creator_profile_current`` materialize already consumes). It proves the lake
path is no-drift: a rollup reconstructed from its Silver record equals the seed
rollup the producer wrapped.

Boundary: this module does NOT recompute metrics and does NOT regenerate the
committed ``creator_profile_current`` view. It is a pure reader -- lake rollup
record -> seed-shaped rollup dict. Re-pointing the committed read model onto
these records (and lake-wide record discovery) is a later, separate step; this
reader takes the source packet anchors it should read.

It also provides ``select_latest_rollup_per_account`` -- the pure
latest-rollup-per-account selection rule (run order is primary; it fails closed
on a regressed/reused ``computed_at`` and on unorderable ties) -- which the
snapshot step feeds with discovered records. The rule itself does no lake
discovery and no view regeneration.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any, Iterable, Mapping

from capture_spine.creator_profile_current.silver_metric_producer import (
    METRIC_ROLLUP_LANE,
    METRIC_ROLLUP_PAYLOAD_KIND,
)

if TYPE_CHECKING:
    from data_lake.root import DataLakeRoot


def read_creator_metric_rollups_from_lake(
    data_root: "DataLakeRoot", *, raw_anchors: Iterable[str]
) -> list[dict[str, Any]]:
    """Read every creator-metric rollup Silver record anchored to ``raw_anchors``
    and reconstruct the seed-shaped ``metric_rollup`` dicts that
    ``creator_profile_current`` materialize consumes.

    Reads the actual on-disk records (a real lake read), not the producer's
    in-memory result. ``raw_anchors`` are the source packet ids the rollups are
    anchored to; the production caller supplies the anchors it is building from
    (lake-wide discovery is a separate concern). Records are de-duplicated by
    ``record_id`` so a shared anchor is never double-counted.
    """
    rollups: list[dict[str, Any]] = []
    seen_record_ids: set[str] = set()
    for raw_anchor in raw_anchors:
        lane_dir = data_root.lane_dir(
            subtree="derived", raw_anchor=raw_anchor, lane=METRIC_ROLLUP_LANE
        )
        if not lane_dir.is_dir():
            continue
        for record_path in sorted(lane_dir.glob("*.json")):
            record = json.loads(record_path.read_text(encoding="utf-8"))
            if record.get("payload_kind") != METRIC_ROLLUP_PAYLOAD_KIND:
                continue
            record_id = record.get("record_id")
            if record_id in seen_record_ids:
                continue
            seen_record_ids.add(record_id)
            rollups.append(_seed_rollup_from_silver_record(record))
    return rollups


def _seed_rollup_from_silver_record(record: dict[str, Any]) -> dict[str, Any]:
    """Reverse ``build_metric_rollup_record``: map a MetricRollupObservation Silver
    record back to the seed-native rollup dict (the shape the metric seeds and
    the creator_profile_current view consume)."""
    observation = record["payload"]["observation"]
    subject_ref = observation["subject"]["ref"]
    return {
        "metric_rollup_id": record["provenance"]["seed_metric_rollup_id"],
        "profile_subject_kind": "platform_account",
        "profile_subject_id": subject_ref["orca_platform_account_id"],
        "creator_record_id_or_none": None,
        "platform_scope": observation["platform_scope"],
        "platform_account_ids": list(observation["platform_account_ids"]),
        "rollup_window": observation["rollup_window"],
        "rollup_window_description": observation["rollup_window_description"],
        "content_kind_inclusion_rule": observation["content_kind_inclusion_rule"],
        "metric_rollups": {
            name: _seed_metric_from_silver(metric)
            for name, metric in observation["metric_rollups"].items()
        },
        "source_metric_observation_ids": list(observation["source_metric_observation_ids"]),
        "observation_count": observation["observation_count"],
        "view_count_min": observation["view_count_min"],
        "view_count_max": observation["view_count_max"],
        "calculation_recipe_version": observation["calculation_recipe_version"],
        "computed_at": observation["computed_at"],
        "freshness_state": observation["freshness_state"],
        "limitations": list(observation["limitations"]),
        "sample_support": observation["sample_support"],
    }


def _seed_metric_from_silver(metric: dict[str, Any]) -> dict[str, Any]:
    """Map a Silver rollup metric back to the seed metric shape. Observed metrics
    carry no posture reason (matching the seed's ``_observed_metric``);
    non-observed metrics carry ``posture_reason_or_none`` (matching the seed's
    ``_unavailable_metric``/``_not_attempted_metric``)."""
    posture = metric["metric_posture"]["kind"]
    seed_metric: dict[str, Any] = {
        "value_or_none": metric["metric_value"],
        "posture": posture,
        "metric_unit": metric["unit"],
    }
    if posture != "observed":
        seed_metric["posture_reason_or_none"] = metric["metric_posture"]["reason_detail"]
    return seed_metric


@dataclass(frozen=True)
class RollupRunCandidate:
    """One rollup Silver record as offered by a specific snapshot run.

    ``selection_run_id`` is the monotonic append/run-order signal the
    snapshot-run manifest stamps (higher == newer run). It -- not the semantic
    ``computed_at`` -- defines which rollup is "latest", because
    ``DataLakeRoot.append_record`` is write-once and carries no append sequence,
    and ``computed_at`` (the caller-supplied ``generated_at_utc``) can be
    regressed or reused. ``record`` is the on-disk MetricRollupObservation record
    (top-level ``record_id`` + ``content_hash`` plus the observation payload).
    """

    selection_run_id: int
    record: Mapping[str, Any]


@dataclass(frozen=True)
class SelectedRollup:
    """The latest rollup chosen for one account, with the provenance the
    snapshot-run manifest records: the chosen ``record_id`` + ``content_hash``
    and the run that chose it. ``rollup`` is the seed-shaped rollup dict that
    ``creator_profile_current`` materialize consumes.
    """

    account_id: str
    rollup: dict[str, Any]
    record_id: str
    content_hash: str
    selection_run_id: int


class LatestRollupSelectionError(ValueError):
    """Raised when latest-per-account selection cannot resolve to a single
    rollup. Subclasses ``ValueError`` so existing fail-closed ``except
    ValueError`` paths still catch it; ``reason`` is the machine-readable code
    (``computed_at_regression`` or ``ambiguous_latest_rollup``) and
    ``account_id`` is the account it failed on.
    """

    def __init__(self, reason: str, account_id: str, detail: str) -> None:
        self.reason = reason
        self.account_id = account_id
        super().__init__(f"{reason} for account {account_id!r}: {detail}")


def select_latest_rollup_per_account(
    candidates: Iterable[RollupRunCandidate],
) -> dict[str, SelectedRollup]:
    """Select the single latest rollup per account from candidates spanning one
    or more snapshot runs, failing closed when "latest" is not well-defined.

    "Latest" is the rollup from the newest ``selection_run_id`` covering the
    account -- NOT the largest semantic ``computed_at`` (which can regress or be
    reused, so it cannot be the sole key). The same unchanged rollup re-selected
    by later runs (identical ``content_hash``) collapses to one. Selection fails
    closed, per account, when latest is ambiguous:

    - ``computed_at_regression``: the newer run's rollup carries a ``computed_at``
      strictly older than an earlier run's rollup (a regressed/reused timestamp);
      selection refuses rather than silently keeping the older record.
    - ``ambiguous_latest_rollup``: two distinct-``content_hash`` rollups cannot be
      ordered -- they tie on the newest ``selection_run_id``, or a newer run
      reuses an earlier run's exact ``computed_at`` with different content.

    Returns ``{account_id: SelectedRollup}``. Discovering the candidate records
    and stamping ``selection_run_id`` (the snapshot-run manifest) is a separate
    step; this is the pure selection rule, with no lake discovery and no view
    regeneration.
    """
    grouped: dict[str, list[_ResolvedCandidate]] = {}
    for candidate in candidates:
        resolved = _resolve_candidate(candidate)
        grouped.setdefault(resolved.account_id, []).append(resolved)
    return {
        account_id: _select_one_account(account_id, group)
        for account_id, group in grouped.items()
    }


@dataclass(frozen=True)
class _ResolvedCandidate:
    account_id: str
    selection_run_id: int
    record_id: str
    content_hash: str
    computed_at: str
    rollup: dict[str, Any]


def _resolve_candidate(candidate: RollupRunCandidate) -> _ResolvedCandidate:
    record = candidate.record
    rollup = _seed_rollup_from_silver_record(dict(record))
    return _ResolvedCandidate(
        account_id=rollup["profile_subject_id"],
        selection_run_id=candidate.selection_run_id,
        record_id=record["record_id"],
        content_hash=record["content_hash"],
        computed_at=rollup["computed_at"],
        rollup=rollup,
    )


def _select_one_account(account_id: str, group: list[_ResolvedCandidate]) -> SelectedRollup:
    # Fold candidates in run order: each newer run is checked against the
    # currently-selected record, exactly as the AR-04 contract states ("if a
    # newer-appended rollup carries a computed_at older than the currently-selected
    # record ... fails").
    selected: _ResolvedCandidate | None = None
    for candidate in sorted(group, key=lambda item: item.selection_run_id):
        if selected is None:
            selected = candidate
            continue
        if candidate.content_hash == selected.content_hash:
            # Same rollup re-selected by a same-or-newer run -> collapse; keep the
            # newest run that still covers the account.
            selected = candidate
            continue
        if candidate.selection_run_id == selected.selection_run_id:
            raise LatestRollupSelectionError(
                "ambiguous_latest_rollup",
                account_id,
                f"distinct rollups tie on selection_run_id {candidate.selection_run_id} "
                f"({selected.content_hash} vs {candidate.content_hash})",
            )
        order = _compare_instants(candidate.computed_at, selected.computed_at)
        if order < 0:
            raise LatestRollupSelectionError(
                "computed_at_regression",
                account_id,
                f"run {candidate.selection_run_id} computed_at {candidate.computed_at!r} is older "
                f"than earlier run {selected.selection_run_id} computed_at {selected.computed_at!r}",
            )
        if order == 0:
            raise LatestRollupSelectionError(
                "ambiguous_latest_rollup",
                account_id,
                f"run {candidate.selection_run_id} reuses computed_at {candidate.computed_at!r} "
                f"with content_hash distinct from earlier run {selected.selection_run_id}",
            )
        selected = candidate
    assert selected is not None  # grouped never creates an empty group
    return SelectedRollup(
        account_id=account_id,
        rollup=selected.rollup,
        record_id=selected.record_id,
        content_hash=selected.content_hash,
        selection_run_id=selected.selection_run_id,
    )


def _compare_instants(left: str, right: str) -> int:
    left_dt = _parse_instant(left)
    right_dt = _parse_instant(right)
    if left_dt < right_dt:
        return -1
    if left_dt > right_dt:
        return 1
    return 0


def _parse_instant(value: str) -> datetime:
    """Parse an ISO-8601 UTC ``computed_at`` into an aware datetime for ordering,
    mirroring the harness-wide ``fromisoformat`` idiom: a trailing ``Z`` is only
    accepted natively on Python 3.11+ so normalize it, and a naive value is
    treated as UTC for deterministic ordering."""
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


_IG_RAW_SOURCE_FAMILY = "instagram_creator"
_SUPPORTED_PLATFORMS = ("instagram", "youtube")


class CreatorRollupDiscoveryError(ValueError):
    """Raised when platform-aware discovery cannot resolve the expected account
    set to rollup records. Subclasses ``ValueError`` for fail-closed
    compatibility; ``reason`` is the machine code (currently
    ``missing_account_rollup``) and ``account_id`` is an expected account that
    resolved to no rollup record.
    """

    def __init__(self, reason: str, account_id: str, detail: str) -> None:
        self.reason = reason
        self.account_id = account_id
        super().__init__(f"{reason} for account {account_id!r}: {detail}")


def discover_creator_metric_rollup_records(
    data_root: "DataLakeRoot", *, account_ledger: Mapping[str, Any]
) -> dict[str, list[dict[str, Any]]]:
    """Discover the creator-metric rollup Silver records currently in the lake,
    per expected account, with platform-aware discovery driven by the account
    ledger. Returns ``{account_id: [raw rollup records]}`` -- ALL current records
    per account; reducing each account to its single latest rollup is
    ``select_latest_rollup_per_account``'s job.

    Discovery is platform-aware because the two producers anchor rollups
    differently (verified against ``origin/main``):

    - **Instagram** (packet-anchored): ``list_available(source_family=
      "instagram_creator")`` -> packet ids -> ``lane_dir(raw_anchor=<packet_id>)``;
      map each rollup to its account via ``subject.ref.orca_platform_account_id``
      and keep the expected IG accounts. The ``instagram_creator`` family also
      holds packets with no rollup record (e.g. grid-metadata), which are simply
      skipped.
    - **YouTube** (account-anchored): for each expected YT account, read
      ``lane_dir(raw_anchor=<platform_account_id>)`` directly.

    Fail closed on the EXPECTED account set (the ledger), not on "did we find any
    packets": every ledger account must resolve to >= 1 rollup record, else raise
    ``CreatorRollupDiscoveryError("missing_account_rollup", account_id)``. So a
    non-empty ``instagram_creator`` packet set that holds observations but no
    rollup for an expected account still fails closed.

    The caller ensures the availability index is current (the IG capture pipeline
    records availability at commit; the operator snapshot runner rebuilds it
    first). This function does not write.
    """
    accounts_by_platform = _expected_accounts_by_platform(account_ledger)
    found: dict[str, list[dict[str, Any]]] = {
        account_id: [] for ids in accounts_by_platform.values() for account_id in ids
    }
    seen_record_ids: dict[str, set[str]] = {account_id: set() for account_id in found}

    expected_ig = accounts_by_platform.get("instagram", set())
    if expected_ig:
        for packet_id in data_root.list_available(source_family=_IG_RAW_SOURCE_FAMILY):
            lane_dir = data_root.lane_dir(
                subtree="derived", raw_anchor=packet_id, lane=METRIC_ROLLUP_LANE
            )
            for record in _read_rollup_records(lane_dir):
                account_id = _rollup_record_account(record)
                if account_id in expected_ig:
                    _add_unique_record(found, seen_record_ids, account_id, record)

    for account_id in accounts_by_platform.get("youtube", set()):
        lane_dir = data_root.lane_dir(
            subtree="derived", raw_anchor=account_id, lane=METRIC_ROLLUP_LANE
        )
        for record in _read_rollup_records(lane_dir):
            # Account-anchored: the rollup's subject account must equal the anchor.
            if _rollup_record_account(record) == account_id:
                _add_unique_record(found, seen_record_ids, account_id, record)

    missing = sorted(account_id for account_id, records in found.items() if not records)
    if missing:
        raise CreatorRollupDiscoveryError(
            "missing_account_rollup",
            missing[0],
            f"{len(missing)} expected account(s) resolved to no rollup record: {missing}",
        )
    return found


def _expected_accounts_by_platform(account_ledger: Mapping[str, Any]) -> dict[str, set[str]]:
    accounts = account_ledger.get("platform_accounts")
    if not isinstance(accounts, list) or not accounts:
        raise ValueError(
            "discover_creator_metric_rollup_records: account ledger has no platform_accounts"
        )
    by_platform: dict[str, set[str]] = {}
    for entry in accounts:
        account_id = entry.get("platform_account_id")
        platform = entry.get("platform")
        if not account_id:
            continue
        if platform not in _SUPPORTED_PLATFORMS:
            raise ValueError(
                f"discover_creator_metric_rollup_records: account {account_id!r} has unsupported "
                f"platform {platform!r} (expected one of {_SUPPORTED_PLATFORMS})"
            )
        by_platform.setdefault(platform, set()).add(account_id)
    return by_platform


def _read_rollup_records(lane_dir: Path) -> list[dict[str, Any]]:
    if not lane_dir.is_dir():
        return []
    records: list[dict[str, Any]] = []
    for record_path in sorted(lane_dir.glob("*.json")):
        record = json.loads(record_path.read_text(encoding="utf-8"))
        if record.get("payload_kind") == METRIC_ROLLUP_PAYLOAD_KIND:
            records.append(record)
    return records


def _rollup_record_account(record: Mapping[str, Any]) -> str:
    return record["payload"]["observation"]["subject"]["ref"]["orca_platform_account_id"]


def _add_unique_record(
    found: dict[str, list[dict[str, Any]]],
    seen_record_ids: dict[str, set[str]],
    account_id: str,
    record: Mapping[str, Any],
) -> None:
    record_id = record.get("record_id")
    if record_id in seen_record_ids[account_id]:
        return
    seen_record_ids[account_id].add(record_id)
    found[account_id].append(dict(record))


__all__ = [
    "CreatorRollupDiscoveryError",
    "LatestRollupSelectionError",
    "RollupRunCandidate",
    "SelectedRollup",
    "discover_creator_metric_rollup_records",
    "read_creator_metric_rollups_from_lake",
    "select_latest_rollup_per_account",
]
