"""Emit Silver Vault creator-metric records from the TikTok batch-admission
metric document.

This producer makes TikTok creator metrics lake-native. Mirroring the merged
Instagram and YouTube producers' Silver-envelope discipline (both now built on
the shared ``silver_envelope_core``), it re-emits each metric observation and
each per-account rollup from the seed-shaped document built by
``tiktok_metric_seed.build_tiktok_batch_creator_metric_seed_document`` as a
formal Silver Vault derived record (``record_kind: observation``) conforming to
the Silver Vault record contract (common header, content-hash discipline,
posture/value coupling).

Boundary: this producer does NOT compute metrics. Every number comes from the
TikTok metric-seed builder; this module only wraps those values in Silver Vault
envelopes and appends them through the lake writer. It does NOT regenerate the
``creator_profile_current`` read model, does NOT introduce cross-platform
creator identity, and does NOT write to the real lake by itself -- callers pass
a ``DataLakeRoot`` (tests use ``DataLakeRoot.for_test``); running it against
the production lake is an operational step outside this module.

TikTok-specific anchoring (mirroring IG, not YouTube): one batch-admission
packet preserves ALL of a creator's captured videos, so every observation for
an account and its rollup anchor to that single packet id (the IG shape). The
observation ``raw_refs`` point at the preserved ``tiktok_batch_capture.json``
(packet id + file id + packet-relative path + json_pointer + the manifest's
preserved-file sha256), which is the hash-checkable source material per the
Silver Vault ``raw_refs`` rule.

Scope (v0), mirroring the IG/YT slices:
- emits MetricObservation + MetricRollupObservation observation records only;
- per-platform account subjects only; no cross-platform creator rollups;
- these records share the platform-agnostic ``creator_metric_silver`` /
  ``creator_metric_rollup_silver`` lanes (records stay distinguishable by
  ``source_family``/``source_surface``/subject namespace).

Accepted residuals (named, not hidden):
- No Bronze Attachment Record raw_ref upgrade path: no generated Bronze AR
  catalog exists for the TikTok batch-admission surface yet. Upgrade trigger:
  the tiktok surface gains catalog rows and this producer grows the same
  ``use_bronze_attachment_records`` seam as IG/YT.
- shareCount/collectCount observations are emitted but are never rollup
  ``derived_refs`` inputs (the engagement recipe consumes the view/like/comment
  trio only; the seed layer owns that selection).
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, Mapping

from capture_spine.creator_profile_current.silver_envelope_core import (
    BASE_NON_CLAIMS as _REQUIRED_NON_CLAIMS,
    CONTENT_HASH_BASIS as _CONTENT_HASH_BASIS,
    METRIC_OBSERVATION_LANE,
    METRIC_OBSERVATION_PAYLOAD_KIND,
    METRIC_ROLLUP_LANE,
    METRIC_ROLLUP_PAYLOAD_KIND,
    SILVER_VAULT_RECORD_SCHEMA_VERSION,
    SOURCE_FAMILY as _SOURCE_FAMILY,
    assert_posture_value_coupling as _assert_posture_value_coupling,
    content_hash as _content_hash,
    metric_posture as _metric_posture,
    require_source_packet_id as _require_source_packet_id,
    required_subject_native_id as _required_subject_native_id,
    rollup_metric as _rollup_metric,
)
from capture_spine.creator_profile_current.silver_subject_ref import (
    platform_account_ref_field as _platform_account_ref_field,
)
from capture_spine.creator_profile_current.tiktok_metric_seed import (
    TIKTOK_BATCH_CREATOR_METRIC_SEED_WRAPPER,
)
from harness_utils import generate_ulid
from data_lake.silver_record import append_silver_record
from source_capture.tiktok.batch_packet import TIKTOK_BATCH_CAPTURE_SURFACE

if TYPE_CHECKING:
    from data_lake.root import DataLakeRoot


SEED_WRAPPER_KEY = TIKTOK_BATCH_CREATOR_METRIC_SEED_WRAPPER

METRIC_OBSERVATION_PRODUCER_SCHEMA_VERSION = "tiktok_creator_metric_silver_metricobservation_v0"
METRIC_ROLLUP_PRODUCER_SCHEMA_VERSION = "tiktok_creator_metric_silver_metricrollupobservation_v0"

_OBS_PRODUCER_ID = (
    "forseti-harness.capture_spine.creator_profile_current.tiktok_silver_metric_producer"
    ".derive_tiktok_creator_metric_silver_records_from_seed#metric_observation"
)
_ROLLUP_PRODUCER_ID = (
    "forseti-harness.capture_spine.creator_profile_current.tiktok_silver_metric_producer"
    ".derive_tiktok_creator_metric_silver_records_from_seed#metric_rollup"
)
_PLATFORM_NAMESPACE = "tiktok"
_SOURCE_SURFACE = TIKTOK_BATCH_CAPTURE_SURFACE


@dataclass(frozen=True)
class TiktokCreatorMetricSilverResult:
    """Outputs of one TikTok creator-metric Silver derivation."""

    observation_records: list[dict[str, Any]]
    observation_paths: list[Path]
    rollup_records: list[dict[str, Any]]
    rollup_paths: list[Path]
    seed_document: dict[str, Any]


def derive_tiktok_creator_metric_silver_records_from_seed(
    *,
    data_root: "DataLakeRoot",
    seed_document: Mapping[str, Any],
) -> TiktokCreatorMetricSilverResult:
    """Wrap the TikTok metric document's observations + per-account rollups in
    Silver Vault envelopes and append them through the lake writer.

    Observations are appended first so each rollup can thread its source
    observation records' content hashes into ``derived_refs`` (the canonical
    Silver lineage, mirroring the IG/YT producers)."""
    seed = seed_document[SEED_WRAPPER_KEY]
    observations_by_id = {
        observation["metric_observation_id"]: observation
        for observation in seed["metric_observations"]
    }

    observation_records: list[dict[str, Any]] = []
    observation_paths: list[Path] = []
    ref_by_seed_observation_id: dict[str, dict[str, str]] = {}
    for seed_observation in seed["metric_observations"]:
        record = build_metric_observation_record(seed_observation=seed_observation)
        path = append_silver_record(
            data_root,
            raw_anchor=_require_source_packet_id(seed_observation),
            lane=METRIC_OBSERVATION_LANE,
            record_id=record["record_id"],
            record=record,
        )
        observation_records.append(record)
        observation_paths.append(path)
        ref_by_seed_observation_id[seed_observation["metric_observation_id"]] = {
            "lane_namespace": METRIC_OBSERVATION_LANE,
            "record_id": record["record_id"],
            "content_hash": record["content_hash"],
        }

    rollup_records: list[dict[str, Any]] = []
    rollup_paths: list[Path] = []
    for seed_rollup in seed["metric_rollups"]:
        rollup_raw_anchor = _rollup_raw_anchor(seed_rollup, observations_by_id)
        record = build_metric_rollup_record(
            seed_rollup=seed_rollup,
            ref_by_seed_observation_id=ref_by_seed_observation_id,
            raw_anchor=rollup_raw_anchor,
        )
        path = append_silver_record(
            data_root,
            raw_anchor=rollup_raw_anchor,
            lane=METRIC_ROLLUP_LANE,
            record_id=record["record_id"],
            record=record,
        )
        rollup_records.append(record)
        rollup_paths.append(path)

    return TiktokCreatorMetricSilverResult(
        observation_records=observation_records,
        observation_paths=observation_paths,
        rollup_records=rollup_records,
        rollup_paths=rollup_paths,
        seed_document=dict(seed_document),
    )


def build_metric_observation_record(
    *,
    seed_observation: Mapping[str, Any],
) -> dict[str, Any]:
    """Wrap one TikTok seed metric observation in a Silver Vault
    MetricObservation record."""
    posture = seed_observation["metric_posture"]
    value = seed_observation.get("metric_value_or_none")
    reason = seed_observation.get("posture_reason_or_none")
    _assert_posture_value_coupling(
        posture=posture,
        value=value,
        reason=reason,
        what=f"observation {seed_observation.get('metric_observation_id')!r}",
    )
    observed_at = seed_observation["observed_at"]
    record: dict[str, Any] = {
        "record_id": f"{generate_ulid()}.json",
        "raw_anchor": _require_source_packet_id(seed_observation),
        "lane_namespace": METRIC_OBSERVATION_LANE,
        "producer_id": _OBS_PRODUCER_ID,
        "schema_version": SILVER_VAULT_RECORD_SCHEMA_VERSION,
        "producer_schema_version": METRIC_OBSERVATION_PRODUCER_SCHEMA_VERSION,
        "content_hash": "",
        "content_hash_basis": _CONTENT_HASH_BASIS,
        "record_kind": "observation",
        "payload_kind": METRIC_OBSERVATION_PAYLOAD_KIND,
        "producer_row_kind": "tiktok_media_metric",
        "source_family": _SOURCE_FAMILY,
        "source_surface": _SOURCE_SURFACE,
        "observed_at": observed_at,
        "captured_at": observed_at,
        "raw_refs": [_raw_ref(seed_observation)],
        "derived_refs": [],
        "payload": {
            "observation": {
                "subject": _observation_subject(seed_observation),
                "metric_name": seed_observation["metric_name"],
                "metric_value": value,
                "metric_posture": _metric_posture(posture, reason),
                "coverage_window": {
                    "start": seed_observation.get("capture_window_start_or_none"),
                    "end": seed_observation.get("capture_window_end_or_none"),
                },
                "source_surface": _SOURCE_SURFACE,
                "source_publication_or_event": seed_observation.get(
                    "content_publication_or_event_time_or_none"
                ),
                "unit": seed_observation["metric_unit"],
                "content_url": seed_observation.get("content_url_or_none"),
            }
        },
        "provenance": {
            "seed_metric_observation_id": seed_observation["metric_observation_id"],
            "metric_registry_version": seed_observation.get("metric_registry_version"),
            "source_pointer": seed_observation.get("source_pointer"),
            "source_field": seed_observation.get("source_field"),
            "creator_handle_query": seed_observation.get("creator_handle_query"),
            "observed_at_source": seed_observation.get("observed_at_source"),
        },
        "non_claims": sorted(set(_REQUIRED_NON_CLAIMS)),
    }
    record["content_hash"] = f"sha256:{_content_hash(record)}"
    return record


def build_metric_rollup_record(
    *,
    seed_rollup: Mapping[str, Any],
    ref_by_seed_observation_id: Mapping[str, Mapping[str, str]],
    raw_anchor: str,
) -> dict[str, Any]:
    """Wrap one TikTok per-account rollup in a Silver Vault
    MetricRollupObservation record whose ``derived_refs`` point at its source
    observation records.

    ``raw_anchor`` is the single batch-packet id shared by the rollup's source
    observations (resolved by the orchestrator and reused for the append path,
    so the in-record anchor and the on-disk location agree -- the IG shape)."""
    derived_refs: list[dict[str, Any]] = []
    for source_id in seed_rollup["source_metric_observation_ids"]:
        ref = ref_by_seed_observation_id.get(source_id)
        if ref is None:
            raise ValueError(
                f"rollup {seed_rollup.get('metric_rollup_id')!r} references unknown "
                f"source observation id: {source_id!r}"
            )
        derived_refs.append(
            {
                "edge_type": "derived_from_record",
                "lane_namespace": ref["lane_namespace"],
                "record_id": ref["record_id"],
                "content_hash": ref["content_hash"],
                "content_hash_basis": _CONTENT_HASH_BASIS,
            }
        )

    computed_at = seed_rollup["computed_at"]
    record: dict[str, Any] = {
        "record_id": f"{generate_ulid()}.json",
        "raw_anchor": raw_anchor,
        "lane_namespace": METRIC_ROLLUP_LANE,
        "producer_id": _ROLLUP_PRODUCER_ID,
        "schema_version": SILVER_VAULT_RECORD_SCHEMA_VERSION,
        "producer_schema_version": METRIC_ROLLUP_PRODUCER_SCHEMA_VERSION,
        "content_hash": "",
        "content_hash_basis": _CONTENT_HASH_BASIS,
        "record_kind": "observation",
        "payload_kind": METRIC_ROLLUP_PAYLOAD_KIND,
        "producer_row_kind": "creator_account_metric_rollup",
        "source_family": _SOURCE_FAMILY,
        "source_surface": _SOURCE_SURFACE,
        "observed_at": computed_at,
        "captured_at": computed_at,
        "raw_refs": [],
        "derived_refs": derived_refs,
        "payload": {
            "observation": {
                "subject": _rollup_subject(seed_rollup),
                "rollup_kind": "creator_account_metric_rollup",
                "platform_scope": seed_rollup["platform_scope"],
                "platform_account_ids": list(seed_rollup["platform_account_ids"]),
                "rollup_window": seed_rollup["rollup_window"],
                "rollup_window_description": seed_rollup["rollup_window_description"],
                "content_kind_inclusion_rule": seed_rollup["content_kind_inclusion_rule"],
                "derivation": {
                    "kind": "computed_metric_rollup",
                    "source_record_ref_kind": "derived_refs",
                    "metric_posture_semantics": "source_input_support_not_raw_aggregate_visibility",
                    "calculation_recipe_version": seed_rollup["calculation_recipe_version"],
                },
                "metric_rollups": {
                    name: _rollup_metric(
                        metric, what=f"rollup {seed_rollup.get('metric_rollup_id')!r} metric {name!r}"
                    )
                    for name, metric in seed_rollup["metric_rollups"].items()
                },
                "observation_count": seed_rollup["observation_count"],
                "view_count_min": seed_rollup["view_count_min"],
                "view_count_max": seed_rollup["view_count_max"],
                "calculation_recipe_version": seed_rollup["calculation_recipe_version"],
                "computed_at": computed_at,
                "freshness_state": seed_rollup["freshness_state"],
                "sample_support": seed_rollup["sample_support"],
                "limitations": list(seed_rollup["limitations"]),
                "source_metric_observation_ids": list(seed_rollup["source_metric_observation_ids"]),
            }
        },
        "provenance": {
            "seed_metric_rollup_id": seed_rollup["metric_rollup_id"],
            "public_handle": seed_rollup.get("public_handle"),
        },
        "non_claims": sorted(set(_REQUIRED_NON_CLAIMS)),
    }
    record["content_hash"] = f"sha256:{_content_hash(record)}"
    return record


# ---------------------------------------------------------------------------
# Subject / ref helpers
# ---------------------------------------------------------------------------

def _observation_subject(seed_observation: Mapping[str, Any]) -> dict[str, Any]:
    """Every TikTok seed metric observation is a per-video stats fact: the
    subject is the public content object (stable video id), published by the
    creator's public handle account."""
    ref: dict[str, Any] = {
        "namespace": _PLATFORM_NAMESPACE,
        "kind": "public_content_object",
        "native_id": _required_subject_native_id(
            seed_observation.get("content_id_or_none"),
            what=f"observation {seed_observation.get('metric_observation_id')!r} content subject",
        ),
        "native_id_kind": "tiktok_video_id",
        "published_by_account_native_id": _required_subject_native_id(
            seed_observation.get("platform_subject_key"),
            what=f"observation {seed_observation.get('metric_observation_id')!r} publisher subject",
        ),
        "published_by_account_native_id_kind": seed_observation.get("platform_subject_key_type"),
        **_platform_account_ref_field(
            seed_observation["platform_account_id"],
            what=f"observation {seed_observation.get('metric_observation_id')!r} platform account id",
        ),
    }
    return {"ref_type": "entity_key", "ref": ref}


def _rollup_subject(seed_rollup: Mapping[str, Any]) -> dict[str, Any]:
    """The rollup subject is the platform account, keyed by the creator's
    public handle (the only source-native TikTok account key this surface
    exposes)."""
    ref: dict[str, Any] = {
        "namespace": _PLATFORM_NAMESPACE,
        "kind": "platform_public_account",
        "native_id": _required_subject_native_id(
            seed_rollup.get("platform_subject_key"),
            what=f"rollup {seed_rollup.get('metric_rollup_id')!r} account subject",
        ),
        "native_id_kind": seed_rollup.get("platform_subject_key_type"),
        **_platform_account_ref_field(
            seed_rollup["profile_subject_id"],
            what=f"rollup {seed_rollup.get('metric_rollup_id')!r} platform account id",
        ),
    }
    return {"ref_type": "entity_key", "ref": ref}


def _raw_ref(seed_observation: Mapping[str, Any]) -> dict[str, Any]:
    """Build the hash-checkable raw ref from the seed observation's
    ``raw_anchor`` (the manifest-backed provenance of the preserved
    ``tiktok_batch_capture.json``) -- the IG raw_ref shape."""
    anchor = seed_observation.get("raw_anchor") or {}
    return {
        "packet_id": seed_observation.get("source_packet_id_or_none"),
        "file_id": anchor.get("file_id"),
        "relative_packet_path": anchor.get("relative_packet_path"),
        "json_pointer": anchor.get("json_pointer"),
        "sha256": anchor.get("sha256"),
        "hash_basis": anchor.get("hash_basis"),
    }


def _rollup_raw_anchor(
    seed_rollup: Mapping[str, Any], observations_by_id: Mapping[str, Mapping[str, Any]]
) -> str:
    packet_ids = set()
    for source_id in seed_rollup["source_metric_observation_ids"]:
        observation = observations_by_id.get(source_id)
        if observation is None:
            raise ValueError(
                f"rollup {seed_rollup.get('metric_rollup_id')!r} references unknown source observation {source_id!r}"
            )
        packet_ids.add(_require_source_packet_id(observation))
    if len(packet_ids) != 1:
        raise ValueError(
            f"rollup {seed_rollup.get('metric_rollup_id')!r} spans multiple source packets {sorted(packet_ids)!r}; "
            "a per-account rollup must anchor to a single selected batch packet."
        )
    return next(iter(packet_ids))


__all__ = [
    "TiktokCreatorMetricSilverResult",
    "METRIC_OBSERVATION_LANE",
    "METRIC_OBSERVATION_PAYLOAD_KIND",
    "METRIC_ROLLUP_LANE",
    "METRIC_ROLLUP_PAYLOAD_KIND",
    "SEED_WRAPPER_KEY",
    "build_metric_observation_record",
    "build_metric_rollup_record",
    "derive_tiktok_creator_metric_silver_records_from_seed",
]
