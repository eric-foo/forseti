"""Recompute every creator-metric rollup in the lake from its source
observations -- the formula-at-scale validation the genesis no-drift oracle
cannot give.

The genesis oracle proves ONE thing: the first lake snapshot is value-equal to
the committed hand-checked seed. It says nothing about the second, tenth, or
thousandth rollup a live recapture run appends. This module walks EVERY
``creator_metric_rollup_silver`` record in the lake (all history, not just the
latest per account -- the longitudinal series is the asset being guarded),
resolves each rollup's ``derived_refs`` to its source MetricObservation records,
and independently recomputes the rollup formulas per
``calculation_recipe_version``:

- ``creator_metric_rollup_admitted_youtube_shorts_average_v0`` (YT genesis):
  view-count-only; average/median/min/max over the referenced view
  observations; every engagement-family metric must be non-observed.
- ``creator_metric_rollup_instagram_reels_grid_engagement_v0`` (IG): complete
  reel trios (view/like/comment per reel); averages round 2; engagement_rate =
  (sum(likes) + sum(comments)) / sum(views), round 6.
- ``creator_metric_rollup_admitted_youtube_shorts_watch_packet_engagement_v0``
  (YT live watch packets): per-metric observed subsets for averages;
  engagement_rate over complete-input videos only (grouped by content id),
  round 6.

The recompute here is an INDEPENDENT restatement of each recipe (mirroring how
the producer tests re-implement the content hash) -- it deliberately does not
import the builders' computation helpers, so a builder-side formula bug cannot
validate itself. An unknown recipe version is a FAILURE, not a skip: a formula
this module cannot restate is a formula the lake cannot claim is validated.

Integrity checks ride along (they are what make the recompute trustworthy):
every rollup and referenced observation record must reproduce its own
``content_hash``; every ``derived_ref`` must resolve and hash-match; the
``observation_count`` / ``source_metric_observation_ids`` / ``derived_refs``
cardinalities must agree; and every rollup metric must obey posture/value
coupling.

Boundary: PURE read-and-compare -- writes nothing, mutates nothing, claims no
readiness. It runs against any ``DataLakeRoot`` (tests use ``for_test``); the
operator runner (``run_creator_rollup_formula_revalidation``) is the only
real-lake-bound path.
"""
from __future__ import annotations

import hashlib
import json
import statistics
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, Iterator, Mapping

from data_lake.canonical_json import canonical_record_bytes

if TYPE_CHECKING:
    from data_lake.root import DataLakeRoot

METRIC_OBSERVATION_LANE = "creator_metric_silver"
METRIC_ROLLUP_LANE = "creator_metric_rollup_silver"

_YT_GENESIS_RECIPE = "creator_metric_rollup_admitted_youtube_shorts_average_v0"
_IG_RECIPE = "creator_metric_rollup_instagram_reels_grid_engagement_v0"
_YT_WATCH_PACKET_RECIPE = (
    "creator_metric_rollup_admitted_youtube_shorts_watch_packet_engagement_v0"
)
_NEVER_COMPUTED_METRICS = ("posting_cadence", "recent_velocity")


@dataclass(frozen=True)
class RollupRevalidationFinding:
    """The verdict for one rollup record. ``failures`` empty == the record's
    formulas, lineage, and integrity all recomputed clean."""

    record_id: str
    raw_anchor: str
    account_id: str
    recipe_version: str
    failures: tuple[str, ...]

    @property
    def ok(self) -> bool:
        return not self.failures


@dataclass(frozen=True)
class RollupRevalidationReport:
    """The outcome of one lake-wide revalidation pass."""

    findings: tuple[RollupRevalidationFinding, ...]
    rollups_checked: int
    failures_total: int

    @property
    def ok(self) -> bool:
        return self.failures_total == 0


def revalidate_creator_metric_rollups(
    data_root: "DataLakeRoot", *, platform: str | None = None
) -> RollupRevalidationReport:
    """Walk every rollup record in the lake (optionally one ``platform_scope``)
    and recompute it from its source observations. Returns a report; raising is
    reserved for an unreadable lake, not a failed check (failures stay visible
    per record so one bad record cannot hide the rest)."""
    observations_by_record_id = {
        record["record_id"]: record
        for record in _iter_lane_records(data_root, lane=METRIC_OBSERVATION_LANE)
    }
    findings: list[RollupRevalidationFinding] = []
    for rollup in _iter_lane_records(data_root, lane=METRIC_ROLLUP_LANE):
        observation = rollup.get("payload", {}).get("observation", {})
        if platform is not None and observation.get("platform_scope") != platform:
            continue
        failures = _revalidate_one_rollup(rollup, observations_by_record_id)
        findings.append(
            RollupRevalidationFinding(
                record_id=str(rollup.get("record_id")),
                raw_anchor=str(rollup.get("raw_anchor")),
                account_id=str(
                    observation.get("subject", {})
                    .get("ref", {})
                    .get("orca_platform_account_id", "")
                ),
                recipe_version=str(observation.get("calculation_recipe_version")),
                failures=tuple(failures),
            )
        )
    return RollupRevalidationReport(
        findings=tuple(findings),
        rollups_checked=len(findings),
        failures_total=sum(len(finding.failures) for finding in findings),
    )


def _iter_lane_records(data_root: "DataLakeRoot", *, lane: str) -> Iterator[dict[str, Any]]:
    """Walk every record in ``lane`` across all anchors. Mirrors the physical
    ``derived/<anchor_shard>/<raw_anchor>/<lane>/<record_id>.json`` layout that
    ``DataLakeRoot.lane_dir`` resolves -- an O(N) read-scan (the accepted
    Option-1 discovery posture; a discovery index is a later, swappable layer)."""
    derived = data_root.path / "derived"
    if not derived.is_dir():
        return
    for shard_dir in sorted(path for path in derived.iterdir() if path.is_dir()):
        for anchor_dir in sorted(path for path in shard_dir.iterdir() if path.is_dir()):
            lane_path = anchor_dir / lane
            if not lane_path.is_dir():
                continue
            for record_path in sorted(lane_path.glob("*.json")):
                yield _load_record(record_path)


def _load_record(record_path: Path) -> dict[str, Any]:
    record = json.loads(record_path.read_text(encoding="utf-8"))
    if not isinstance(record, dict):
        raise ValueError(f"lake record must be a JSON object: {record_path}")
    return record


# -- per-rollup checks --------------------------------------------------------

def _revalidate_one_rollup(
    rollup: Mapping[str, Any],
    observations_by_record_id: Mapping[str, Mapping[str, Any]],
) -> list[str]:
    failures: list[str] = []
    if not _content_hash_ok(rollup):
        failures.append("rollup content_hash does not reproduce from the record's own content")

    observation = rollup.get("payload", {}).get("observation")
    if not isinstance(observation, Mapping):
        failures.append("rollup payload.observation missing")
        return failures

    source_rows, ref_failures = _resolve_source_rows(rollup, observations_by_record_id)
    failures.extend(ref_failures)

    source_ids = observation.get("source_metric_observation_ids")
    observation_count = observation.get("observation_count")
    derived_refs = rollup.get("derived_refs", [])
    if (
        not isinstance(source_ids, list)
        or observation_count != len(source_ids)
        or len(derived_refs) != len(source_ids)
    ):
        failures.append(
            "cardinality mismatch: observation_count="
            f"{observation_count!r}, source_metric_observation_ids="
            f"{len(source_ids) if isinstance(source_ids, list) else source_ids!r}, "
            f"derived_refs={len(derived_refs)}"
        )

    metrics = observation.get("metric_rollups")
    if not isinstance(metrics, Mapping):
        failures.append("rollup metric_rollups missing")
        return failures
    failures.extend(_posture_coupling_failures(metrics))

    if ref_failures:
        # The source set is unreliable; recomputing formulas from it would
        # produce noise on top of the real (lineage) failure.
        return failures

    recipe = observation.get("calculation_recipe_version")
    if recipe == _YT_GENESIS_RECIPE:
        failures.extend(_recompute_yt_genesis(observation, metrics, source_rows))
    elif recipe == _IG_RECIPE:
        failures.extend(_recompute_ig(observation, metrics, source_rows))
    elif recipe == _YT_WATCH_PACKET_RECIPE:
        failures.extend(_recompute_yt_watch_packet(observation, metrics, source_rows))
    else:
        failures.append(
            f"unknown calculation_recipe_version {recipe!r}: this recipe has no independent "
            "recompute rule, so the rollup cannot be claimed formula-validated"
        )
    return failures


@dataclass(frozen=True)
class _SourceRow:
    metric_name: str
    value: Any
    content_id: str


def _resolve_source_rows(
    rollup: Mapping[str, Any],
    observations_by_record_id: Mapping[str, Mapping[str, Any]],
) -> tuple[list[_SourceRow], list[str]]:
    failures: list[str] = []
    rows: list[_SourceRow] = []
    for edge in rollup.get("derived_refs", []):
        record_id = edge.get("record_id")
        record = observations_by_record_id.get(record_id)
        if record is None:
            failures.append(f"derived_ref {record_id!r} does not resolve to a lake observation record")
            continue
        if edge.get("content_hash") != record.get("content_hash"):
            failures.append(
                f"derived_ref {record_id!r} content_hash does not match the stored observation record"
            )
            continue
        if not _content_hash_ok(record):
            failures.append(
                f"observation {record_id!r} content_hash does not reproduce from the record's own content"
            )
            continue
        observation = record.get("payload", {}).get("observation", {})
        posture = observation.get("metric_posture", {}).get("kind")
        if posture != "observed":
            failures.append(
                f"observation {record_id!r} feeding the rollup carries posture {posture!r}, not observed"
            )
            continue
        rows.append(
            _SourceRow(
                metric_name=str(observation.get("metric_name")),
                value=observation.get("metric_value"),
                content_id=str(observation.get("subject", {}).get("ref", {}).get("native_id")),
            )
        )
    return rows, failures


def _content_hash_ok(record: Mapping[str, Any]) -> bool:
    canonical = dict(record)
    stored = canonical.pop("content_hash", None)
    digest = hashlib.sha256(
        json.dumps(
            canonical, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
        ).encode("utf-8")
    ).hexdigest()
    return stored == f"sha256:{digest}"


def _posture_coupling_failures(metrics: Mapping[str, Any]) -> list[str]:
    failures: list[str] = []
    for name, metric in metrics.items():
        if not isinstance(metric, Mapping):
            failures.append(f"metric {name!r} is not an object")
            continue
        posture = metric.get("metric_posture", {})
        kind = posture.get("kind") if isinstance(posture, Mapping) else None
        value = metric.get("metric_value")
        if kind == "observed":
            if value is None or isinstance(value, bool) or not isinstance(value, (int, float)):
                failures.append(f"observed metric {name!r} lacks a numeric value")
        else:
            if value is not None:
                failures.append(f"non-observed metric {name!r} carries a value ({value!r})")
    return failures


# -- recipe recomputes (independent restatements, not builder imports) --------

def _recompute_yt_genesis(
    observation: Mapping[str, Any],
    metrics: Mapping[str, Any],
    rows: list[_SourceRow],
) -> list[str]:
    failures: list[str] = []
    non_view = sorted({row.metric_name for row in rows if row.metric_name != "view_count"})
    if non_view:
        failures.append(f"genesis view-count recipe references non-view observations: {non_view}")
    views = [row.value for row in rows if row.metric_name == "view_count"]
    failures.extend(_check_view_stats(observation, metrics, views))
    for name in ("engagement_rate", "average_like_count", "average_comment_count"):
        failures.extend(_check_not_observed(metrics, name))
    failures.extend(_check_never_computed(metrics))
    return failures


def _recompute_ig(
    observation: Mapping[str, Any],
    metrics: Mapping[str, Any],
    rows: list[_SourceRow],
) -> list[str]:
    failures: list[str] = []
    views = [row.value for row in rows if row.metric_name == "view_count"]
    likes = [row.value for row in rows if row.metric_name == "like_count"]
    comments = [row.value for row in rows if row.metric_name == "comment_count"]
    if not (len(views) == len(likes) == len(comments)) or not views:
        failures.append(
            "IG recipe requires complete reel trios: "
            f"views={len(views)}, likes={len(likes)}, comments={len(comments)}"
        )
        return failures
    failures.extend(_check_view_stats(observation, metrics, views))
    failures.extend(_check_observed(metrics, "average_like_count", round(statistics.mean(likes), 2)))
    failures.extend(
        _check_observed(metrics, "average_comment_count", round(statistics.mean(comments), 2))
    )
    denominator = sum(views)
    if denominator > 0:
        failures.extend(
            _check_observed(
                metrics,
                "engagement_rate",
                round((sum(likes) + sum(comments)) / denominator, 6),
            )
        )
    else:
        failures.extend(_check_not_observed(metrics, "engagement_rate"))
    failures.extend(_check_never_computed(metrics))
    return failures


def _recompute_yt_watch_packet(
    observation: Mapping[str, Any],
    metrics: Mapping[str, Any],
    rows: list[_SourceRow],
) -> list[str]:
    failures: list[str] = []
    views = [row.value for row in rows if row.metric_name == "view_count"]
    likes = [row.value for row in rows if row.metric_name == "like_count"]
    comments = [row.value for row in rows if row.metric_name == "total_comment_count"]
    if not views:
        failures.append("watch-packet recipe rollup references no view_count observations")
        return failures
    failures.extend(_check_view_stats(observation, metrics, views))
    if likes:
        failures.extend(
            _check_observed(metrics, "average_like_count", round(statistics.mean(likes), 2))
        )
    else:
        failures.extend(_check_not_observed(metrics, "average_like_count"))
    if comments:
        failures.extend(
            _check_observed(metrics, "average_comment_count", round(statistics.mean(comments), 2))
        )
    else:
        failures.extend(_check_not_observed(metrics, "average_comment_count"))

    by_content: dict[str, dict[str, Any]] = {}
    for row in rows:
        by_content.setdefault(row.content_id, {})[row.metric_name] = row.value
    complete = [
        values
        for values in by_content.values()
        if all(name in values for name in ("view_count", "like_count", "total_comment_count"))
    ]
    denominator = sum(values["view_count"] for values in complete)
    if complete and denominator > 0:
        numerator = sum(
            values["like_count"] + values["total_comment_count"] for values in complete
        )
        failures.extend(
            _check_observed(metrics, "engagement_rate", round(numerator / denominator, 6))
        )
    else:
        failures.extend(_check_not_observed(metrics, "engagement_rate"))
    failures.extend(_check_never_computed(metrics))
    return failures


def _check_view_stats(
    observation: Mapping[str, Any],
    metrics: Mapping[str, Any],
    views: list[Any],
) -> list[str]:
    if not views:
        return ["rollup references no view_count observations"]
    failures = _check_observed(metrics, "average_views", round(statistics.mean(views), 2))
    failures.extend(_check_observed(metrics, "median_views", round(statistics.median(views), 2)))
    if observation.get("view_count_min") != min(views):
        failures.append(
            f"view_count_min stored {observation.get('view_count_min')!r} != recomputed {min(views)!r}"
        )
    if observation.get("view_count_max") != max(views):
        failures.append(
            f"view_count_max stored {observation.get('view_count_max')!r} != recomputed {max(views)!r}"
        )
    return failures


def _check_observed(metrics: Mapping[str, Any], name: str, expected: float) -> list[str]:
    metric = metrics.get(name)
    if not isinstance(metric, Mapping):
        return [f"metric {name!r} missing"]
    kind = metric.get("metric_posture", {}).get("kind")
    if kind != "observed":
        return [f"metric {name!r} expected observed (recomputed {expected!r}) but posture is {kind!r}"]
    if metric.get("metric_value") != expected:
        return [
            f"metric {name!r} stored {metric.get('metric_value')!r} != recomputed {expected!r}"
        ]
    return []


def _check_not_observed(metrics: Mapping[str, Any], name: str) -> list[str]:
    metric = metrics.get(name)
    if not isinstance(metric, Mapping):
        return [f"metric {name!r} missing"]
    kind = metric.get("metric_posture", {}).get("kind")
    if kind == "observed":
        return [
            f"metric {name!r} is observed but the recipe's source inputs cannot support it"
        ]
    return []


def _check_never_computed(metrics: Mapping[str, Any]) -> list[str]:
    failures: list[str] = []
    for name in _NEVER_COMPUTED_METRICS:
        failures.extend(_check_not_observed(metrics, name))
    return failures


__all__ = [
    "METRIC_OBSERVATION_LANE",
    "METRIC_ROLLUP_LANE",
    "RollupRevalidationFinding",
    "RollupRevalidationReport",
    "revalidate_creator_metric_rollups",
]
