"""Emit Silver Vault creator-metric records from Instagram reels-grid projections.

This producer makes creator metrics lake-native. It REUSES the tested
``instagram_reels_creator_metric_seed`` computation (so the numbers never drift
from the existing static seed) and re-emits each metric observation and each
per-account rollup as a formal Silver Vault derived record
(``record_kind: observation``), conforming to the Silver Vault record contract
(common header, content-hash discipline, posture/value coupling) and to the
sibling ``creator_metric_silver_record_contract_v0`` doc.

Boundary: this producer does NOT compute metrics. Every number comes from
``build_instagram_reels_creator_metric_seed_from_files``; this module only wraps
those values in Silver Vault envelopes and appends them through the lake writer.
When requested, observation ``raw_refs`` are upgraded from packet/file refs to
AR-backed refs by reading the public Bronze source-surface catalog helper; a
missing AR row stays visible as lineage limitation instead of becoming inferred
absence.

Scope (v0), kept deliberately small for a first reviewable slice:
- emits MetricObservation + MetricRollupObservation observation records only;
- does NOT emit entity or relationship records (the metric subject is carried as
  a self-describing ``entity_key`` reference; a future version may co-emit the
  PlatformAccountEntity / public_content_object entities and the
  ``content_published_by_account`` relationship);
- does NOT regenerate the ``creator_profile_current`` read model (separate step);
- does NOT introduce cross-platform creator identity;
- does NOT write to the real lake by itself: callers pass a ``DataLakeRoot``
  (tests use ``DataLakeRoot.for_test``); running it against the production lake
  is an operational step outside this module.

Accepted residuals (named for the delegated review, not hidden):
- Observations carry ``raw_refs`` to the raw packet by default, or to the
  generated Bronze Attachment Record when ``use_bronze_attachment_records`` is
  set. The intermediate IG reels grid projection is recorded in ``provenance``
  (pointer + row id), NOT as a formal ``derived_refs`` edge, because the reused
  seed observation does not carry the projection record's lake address
  (lane/record_id/content_hash).
- A computed rollup aggregate uses ``metric_posture.kind: observed`` when it is
  source-backed (inherited verbatim from the seed); this reuse of the
  observed posture for a derived value is the load-bearing contract choice.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, Mapping, Sequence

from capture_spine.creator_profile_current.instagram_metric_seed import (
    build_instagram_reels_creator_metric_seed_from_files,
)
from harness_utils import generate_ulid
from data_lake.catalog import source_surface_catalog_rows
from data_lake.silver_record import append_silver_record

if TYPE_CHECKING:
    from data_lake.root import DataLakeRoot


SILVER_VAULT_RECORD_SCHEMA_VERSION = "silver_vault_record_v0"
SEED_WRAPPER_KEY = "instagram_reels_creator_metric_seed"

METRIC_OBSERVATION_LANE = "creator_metric_silver"
METRIC_ROLLUP_LANE = "creator_metric_rollup_silver"
METRIC_OBSERVATION_PAYLOAD_KIND = "MetricObservation"
METRIC_ROLLUP_PAYLOAD_KIND = "MetricRollupObservation"
METRIC_OBSERVATION_PRODUCER_SCHEMA_VERSION = "creator_metric_silver_metricobservation_v0"
METRIC_ROLLUP_PRODUCER_SCHEMA_VERSION = "creator_metric_silver_metricrollupobservation_v0"

_CONTENT_HASH_BASIS = "canonical_json_excluding_content_hash"
_OBS_PRODUCER_ID = (
    "orca-harness.capture_spine.creator_profile_current.silver_metric_producer"
    ".derive_creator_metric_silver_records_from_projections#metric_observation"
)
_ROLLUP_PRODUCER_ID = (
    "orca-harness.capture_spine.creator_profile_current.silver_metric_producer"
    ".derive_creator_metric_silver_records_from_projections#metric_rollup"
)
_PLATFORM_NAMESPACE = "instagram"
_SOURCE_FAMILY = "social_media"
_IG_BRONZE_SOURCE_FAMILY = "instagram_creator"
_IG_BRONZE_SOURCE_SURFACE = "ig_reels_grid_dom_passive_json"
_BRONZE_AR_RAW_REF_KIND = "bronze_attachment_record"
_RAW_PACKET_FALLBACK_REF_KIND = "raw_packet_fallback_missing_attachment_record"
_MISSING_AR_LIMITATION = "typed_attachment_record_missing_for_raw_ref"

# Non-claims attached to every emitted record. The registry/profile boundaries
# already in the codebase are the source of truth for these tokens; the producer
# restates them so a record is never mistaken for representative or buyer truth.
_REQUIRED_NON_CLAIMS = (
    "not a representative creator average",
    "not channel-wide creator influence",
    "not cross-platform identity linkage",
    "not a follower graph or audience estimate",
    "not buyer proof",
)


@dataclass(frozen=True)
class CreatorMetricSilverResult:
    """Outputs of one creator-metric Silver derivation."""

    observation_records: list[dict[str, Any]]
    observation_paths: list[Path]
    rollup_records: list[dict[str, Any]]
    rollup_paths: list[Path]
    seed_document: dict[str, Any]


def derive_creator_metric_silver_records_from_projections(
    *,
    data_root: "DataLakeRoot",
    projection_paths: Sequence[str | Path],
    account_ledger: Mapping[str, Any],
    generated_at_utc: str,
    use_bronze_attachment_records: bool = False,
) -> CreatorMetricSilverResult:
    """Derive and append Silver Vault MetricObservation + MetricRollupObservation
    records from IG reels-grid projection files.

    Observations are appended first so each rollup can thread its source
    observation records' content hashes into ``derived_refs`` (mirroring the
    Silver lineage discipline of the Fragrantica cleaning lake producer).
    """
    seed_document = build_instagram_reels_creator_metric_seed_from_files(
        projection_paths=projection_paths,
        account_ledger=account_ledger,
        generated_at_utc=generated_at_utc,
    )
    seed = seed_document[SEED_WRAPPER_KEY]
    observations_by_id = {
        observation["metric_observation_id"]: observation
        for observation in seed["metric_observations"]
    }
    handle_by_account_id = {
        observation["platform_account_id"]: observation["platform_subject_key"]
        for observation in seed["metric_observations"]
    }
    bronze_attachment_records_by_raw_ref = (
        _bronze_attachment_records_by_raw_ref(data_root)
        if use_bronze_attachment_records
        else {}
    )

    observation_records: list[dict[str, Any]] = []
    observation_paths: list[Path] = []
    ref_by_seed_observation_id: dict[str, dict[str, str]] = {}
    for seed_observation in seed["metric_observations"]:
        record = build_metric_observation_record(
            seed_observation=seed_observation,
            bronze_attachment_records_by_raw_ref=bronze_attachment_records_by_raw_ref,
            use_bronze_attachment_records=use_bronze_attachment_records,
        )
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
            account_handle=handle_by_account_id.get(seed_rollup["profile_subject_id"]),
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

    return CreatorMetricSilverResult(
        observation_records=observation_records,
        observation_paths=observation_paths,
        rollup_records=rollup_records,
        rollup_paths=rollup_paths,
        seed_document=seed_document,
    )


def build_metric_observation_record(
    *,
    seed_observation: Mapping[str, Any],
    bronze_attachment_records_by_raw_ref: Mapping[tuple[str, str, str, str], Mapping[str, Any]] | None = None,
    use_bronze_attachment_records: bool = False,
) -> dict[str, Any]:
    """Wrap one seed metric observation in a Silver Vault MetricObservation record."""
    posture = seed_observation["metric_posture"]
    value = seed_observation.get("metric_value_or_none")
    _assert_posture_value_coupling(
        posture=posture,
        value=value,
        reason=seed_observation.get("posture_reason_or_none"),
        what=f"observation {seed_observation.get('metric_observation_id')!r}",
    )
    observed_at = seed_observation["observed_at"]
    raw_ref = _raw_ref(
        seed_observation,
        bronze_attachment_records_by_raw_ref=bronze_attachment_records_by_raw_ref or {},
        use_bronze_attachment_records=use_bronze_attachment_records,
    )
    lineage_limitations = _raw_ref_lineage_limitations(raw_ref)
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
        "producer_row_kind": (
            "ig_creator_metric" if seed_observation["content_kind"] == "profile" else "ig_media_metric"
        ),
        "source_family": _SOURCE_FAMILY,
        "source_surface": seed_observation.get("chosen_source_surface_or_none") or "instagram_reels_grid",
        "observed_at": observed_at,
        "captured_at": observed_at,
        "raw_refs": [raw_ref],
        "derived_refs": [],
        "payload": {
            "observation": {
                "subject": _observation_subject(seed_observation),
                "metric_name": seed_observation["metric_name"],
                "metric_value": value,
                "metric_posture": _metric_posture(posture, seed_observation.get("posture_reason_or_none")),
                "coverage_window": {
                    "start": seed_observation.get("capture_window_start_or_none"),
                    "end": seed_observation.get("capture_window_end_or_none"),
                },
                "source_surface": seed_observation.get("chosen_source_surface_or_none"),
                "source_publication_or_event": seed_observation.get("source_publication_or_event_time_or_none"),
                "source_surface_count_candidates": seed_observation.get("source_surface_count_candidates", []),
                "unit": seed_observation["metric_unit"],
            }
        },
        "provenance": {
            "seed_metric_observation_id": seed_observation["metric_observation_id"],
            "metric_registry_version": seed_observation.get("metric_registry_version"),
            "projection_source_pointer": seed_observation.get("source_pointer"),
            "projection_source_row_id": seed_observation.get("source_projection_row_id"),
        },
        "non_claims": sorted(set(_REQUIRED_NON_CLAIMS)),
    }
    if lineage_limitations:
        record["lineage_limitations"] = lineage_limitations
    record["content_hash"] = f"sha256:{_content_hash(record)}"
    return record


def build_metric_rollup_record(
    *,
    seed_rollup: Mapping[str, Any],
    ref_by_seed_observation_id: Mapping[str, Mapping[str, str]],
    account_handle: str | None,
    raw_anchor: str,
) -> dict[str, Any]:
    """Wrap one seed per-account rollup in a Silver Vault MetricRollupObservation
    record whose ``derived_refs`` point at its source observation records.

    ``raw_anchor`` is the single selected-projection packet id shared by the
    rollup's source observations (resolved by the orchestrator and reused for the
    append path, so the in-record anchor and the on-disk location agree)."""
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
        "source_surface": "instagram_reels_grid",
        "observed_at": computed_at,
        "captured_at": computed_at,
        "raw_refs": [],
        "derived_refs": derived_refs,
        "payload": {
            "observation": {
                "subject": _rollup_subject(seed_rollup, account_handle),
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
                    name: _rollup_metric(metric, what=f"rollup {seed_rollup.get('metric_rollup_id')!r} metric {name!r}")
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
        "provenance": {"seed_metric_rollup_id": seed_rollup["metric_rollup_id"]},
        "non_claims": sorted(set(_REQUIRED_NON_CLAIMS)),
    }
    record["content_hash"] = f"sha256:{_content_hash(record)}"
    return record


# ---------------------------------------------------------------------------
# Subject / posture / ref helpers
# ---------------------------------------------------------------------------

def _observation_subject(seed_observation: Mapping[str, Any]) -> dict[str, Any]:
    if seed_observation["content_kind"] == "profile":
        ref: dict[str, Any] = {
            "namespace": _PLATFORM_NAMESPACE,
            "kind": "platform_public_account",
            "native_id": _required_subject_native_id(
                seed_observation.get("platform_subject_key"),
                what=f"observation {seed_observation.get('metric_observation_id')!r} account subject",
            ),
        }
    else:
        ref = {
            "namespace": _PLATFORM_NAMESPACE,
            "kind": "public_content_object",
            "native_id": _required_subject_native_id(
                seed_observation.get("content_id_or_none"),
                what=f"observation {seed_observation.get('metric_observation_id')!r} content subject",
            ),
            "published_by_account_native_id": _required_subject_native_id(
                seed_observation.get("platform_subject_key"),
                what=f"observation {seed_observation.get('metric_observation_id')!r} publisher subject",
            ),
        }
    ref["orca_platform_account_id"] = seed_observation["platform_account_id"]
    return {"ref_type": "entity_key", "ref": ref}


def _rollup_subject(seed_rollup: Mapping[str, Any], account_handle: str | None) -> dict[str, Any]:
    ref: dict[str, Any] = {
        "namespace": _PLATFORM_NAMESPACE,
        "kind": "platform_public_account",
        "native_id": _required_subject_native_id(
            account_handle,
            what=f"rollup {seed_rollup.get('metric_rollup_id')!r} account subject",
        ),
        "orca_platform_account_id": seed_rollup["profile_subject_id"],
    }
    return {"ref_type": "entity_key", "ref": ref}


def _required_subject_native_id(value: Any, *, what: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{what} requires a non-empty entity_key native_id")
    return value


def _metric_posture(kind: str, reason: str | None) -> dict[str, Any]:
    return {"kind": kind, "reason_code": None, "reason_detail": reason}


def _rollup_metric(metric: Mapping[str, Any], *, what: str) -> dict[str, Any]:
    posture = metric["posture"]
    value = metric.get("value_or_none")
    reason = metric.get("posture_reason_or_none")
    _assert_posture_value_coupling(posture=posture, value=value, reason=reason, what=what)
    return {
        "metric_value": value,
        "metric_posture": _metric_posture(posture, reason),
        "unit": metric["metric_unit"],
    }


def _raw_ref(
    seed_observation: Mapping[str, Any],
    *,
    bronze_attachment_records_by_raw_ref: Mapping[tuple[str, str, str, str], Mapping[str, Any]],
    use_bronze_attachment_records: bool,
) -> dict[str, Any]:
    anchor = seed_observation.get("raw_anchor") or {}
    raw_ref = {
        "packet_id": seed_observation.get("source_packet_id_or_none"),
        "file_id": anchor.get("file_id"),
        "relative_packet_path": anchor.get("relative_packet_path"),
        "json_pointer": anchor.get("json_pointer"),
        "sha256": anchor.get("sha256"),
        "hash_basis": anchor.get("hash_basis"),
    }
    if not use_bronze_attachment_records:
        return raw_ref

    key = _raw_ref_key(raw_ref)
    attachment_record = (
        bronze_attachment_records_by_raw_ref.get(key) if key is not None else None
    )
    if attachment_record is None:
        raw_ref.update(
            {
                "raw_ref_kind": _RAW_PACKET_FALLBACK_REF_KIND,
                "typed_attachment_record_status": "missing",
                "attachment_record_residual": _MISSING_AR_LIMITATION,
            }
        )
        return raw_ref

    raw_ref.update(
        {
            "raw_ref_kind": _BRONZE_AR_RAW_REF_KIND,
            "attachment_record_id": attachment_record.get("attachment_record_id"),
            "attachment_record_schema_version": attachment_record.get(
                "attachment_record_schema_version"
            ),
            "attachment_record_physicalization": attachment_record.get(
                "attachment_record_physicalization"
            ),
            "body_ref_kind": attachment_record.get("body_ref_kind"),
            "body_ref": attachment_record.get("body_ref"),
            "body_sha256": attachment_record.get("body_sha256"),
            "source_family": attachment_record.get("source_family"),
            "source_surface": attachment_record.get("source_surface"),
            "source_slice_ids": attachment_record.get("source_slice_ids", []),
            "payload_kind": attachment_record.get("payload_kind"),
            "payload_schema_version": attachment_record.get("payload_schema_version"),
            "replay_version_pins": attachment_record.get("replay_version_pins"),
        }
    )
    return raw_ref


def _bronze_attachment_records_by_raw_ref(
    data_root: "DataLakeRoot",
) -> dict[tuple[str, str, str, str], Mapping[str, Any]]:
    rows = source_surface_catalog_rows(
        data_root,
        source_family=_IG_BRONZE_SOURCE_FAMILY,
        source_surface=_IG_BRONZE_SOURCE_SURFACE,
    )
    by_key: dict[tuple[str, str, str, str], Mapping[str, Any]] = {}
    for row in rows["attachment_record_rows"]:
        key = _attachment_record_key(row)
        if key is not None:
            by_key[key] = row
    return by_key


def _attachment_record_key(record: Mapping[str, Any]) -> tuple[str, str, str, str] | None:
    packet_id = record.get("packet_id")
    file_id = record.get("file_id")
    relative_packet_path = record.get("relative_packet_path")
    body_sha256 = record.get("body_sha256")
    if not all(
        isinstance(value, str) and value.strip()
        for value in (packet_id, file_id, relative_packet_path, body_sha256)
    ):
        return None
    return (packet_id, file_id, relative_packet_path, body_sha256)


def _raw_ref_key(record: Mapping[str, Any]) -> tuple[str, str, str, str] | None:
    packet_id = record.get("packet_id")
    file_id = record.get("file_id")
    relative_packet_path = record.get("relative_packet_path")
    sha256 = record.get("sha256")
    if not all(
        isinstance(value, str) and value.strip()
        for value in (packet_id, file_id, relative_packet_path, sha256)
    ):
        return None
    return (packet_id, file_id, relative_packet_path, sha256)


def _raw_ref_lineage_limitations(raw_ref: Mapping[str, Any]) -> list[dict[str, str]]:
    if raw_ref.get("typed_attachment_record_status") != "missing":
        return []
    return [
        {
            "reason": "other",
            "detail": _MISSING_AR_LIMITATION,
        }
    ]


def _assert_posture_value_coupling(*, posture: str, value: Any, reason: Any, what: str) -> None:
    """Enforce the Silver posture/value coupling: observed <=> numeric value and
    no reason; non-observed <=> null value and a reason. Booleans are not numbers.
    Fails loud rather than emitting a fake-shaped record."""
    if posture == "observed":
        if value is None or isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{what}: observed posture requires a numeric metric value, got {value!r}")
        if reason:
            raise ValueError(f"{what}: observed posture must not carry a posture reason")
    else:
        if value is not None:
            raise ValueError(f"{what}: non-observed posture must carry a null value, got {value!r}")
        if not reason:
            raise ValueError(f"{what}: non-observed posture requires a posture reason")


def _require_source_packet_id(seed_observation: Mapping[str, Any]) -> str:
    packet_id = seed_observation.get("source_packet_id_or_none")
    if not packet_id:
        raise ValueError(
            f"metric observation {seed_observation.get('metric_observation_id')!r} lacks a "
            "source packet id; cannot anchor a source-backed Silver record."
        )
    return packet_id


def _rollup_raw_anchor(seed_rollup: Mapping[str, Any], observations_by_id: Mapping[str, Mapping[str, Any]]) -> str:
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
            "a per-account rollup must anchor to a single selected projection packet."
        )
    return next(iter(packet_ids))


def _content_hash(record: dict[str, Any]) -> str:
    canonical = dict(record)
    canonical.pop("content_hash", None)
    return hashlib.sha256(_canonical_json_bytes(canonical)).hexdigest()


def _canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


__all__ = [
    "CreatorMetricSilverResult",
    "METRIC_OBSERVATION_LANE",
    "METRIC_OBSERVATION_PAYLOAD_KIND",
    "METRIC_ROLLUP_LANE",
    "METRIC_ROLLUP_PAYLOAD_KIND",
    "build_metric_observation_record",
    "build_metric_rollup_record",
    "derive_creator_metric_silver_records_from_projections",
]
