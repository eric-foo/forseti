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
"""
from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any, Iterable

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


__all__ = ["read_creator_metric_rollups_from_lake"]
