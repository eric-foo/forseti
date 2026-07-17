"""Produce one packet-grain Silver metric observation set from a TikTok grid.

The packet-grain physicalization avoids one-file-per-metric explosion while
retaining strict posture/value semantics for every nested metric.  It is source
mechanics only: no ranking, velocity interpretation, or creator judgment.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any, Mapping

from capture_spine.creator_profile_current.silver_envelope_core import (
    BASE_NON_CLAIMS,
    CONTENT_HASH_BASIS,
    METRIC_OBSERVATION_LANE,
    METRIC_OBSERVATION_PAYLOAD_KIND,
    SILVER_VAULT_RECORD_SCHEMA_VERSION,
    content_hash,
)
from data_lake.canonical_json import canonical_record_bytes
from data_lake.silver_lineage import (
    SilverAnchor,
    SilverLineage,
    SilverRawRef,
    SilverSourceObject,
)
from data_lake.silver_record import (
    METRIC_OBSERVATION_SET_PAYLOAD_KIND,
    append_silver_record,
    validate_silver_vault_record,
)
from source_capture.tiktok.grid_packet import TIKTOK_GRID_PACKET_SOURCE_SURFACE
from source_capture.tiktok.creator_onboarding import (
    TIKTOK_PROFILE_METRIC_CAPTURE_POLICY_VERSION,
)

if TYPE_CHECKING:
    from data_lake.root import DataLakeRoot


SOCIAL_METRIC_OBSERVATION_SET_LANE = "social_metric_observation_set_silver"
TIKTOK_GRID_OBSERVATION_SOURCE_SURFACE = TIKTOK_GRID_PACKET_SOURCE_SURFACE
TIKTOK_GRID_OBSERVATION_POLICY_VERSION = "tiktok_grid_metric_observation_set_v1"
TIKTOK_GRID_OBSERVATION_PRODUCER_SCHEMA_VERSION = (
    "tiktok_grid_metric_observation_set_silver_v0"
)
TIKTOK_PROFILE_METRIC_OBSERVATION_POLICY_VERSION = (
    "tiktok_profile_metric_observation_v0"
)
TIKTOK_PROFILE_METRIC_OBSERVATION_PRODUCER_SCHEMA_VERSION = (
    "tiktok_profile_metric_observation_silver_v0"
)
TIKTOK_PROFILE_METRIC_FIELDS: tuple[tuple[str, str], ...] = (
    ("follower_count", "followerCount"),
    ("profile_total_like_count", "heartCount"),
)
TIKTOK_GRID_METRIC_FIELDS: tuple[tuple[str, str], ...] = (
    ("view_count", "playCount"),
    ("like_count", "diggCount"),
    ("comment_count", "commentCount"),
    ("share_count", "shareCount"),
    ("collect_count", "collectCount"),
)
_POLICY_BASIS = {
    "policy_version": TIKTOK_GRID_OBSERVATION_POLICY_VERSION,
    "source_surfaces": [
        TIKTOK_GRID_OBSERVATION_SOURCE_SURFACE,
        "tiktok_creator_batch_capture_v0",
    ],
    "identity": "creator_handle+tiktok_video_id",
    "metrics": dict(TIKTOK_GRID_METRIC_FIELDS),
    "missing": "unavailable_with_reason; never zero-fill",
    "real_zero": "observed",
    "physicalization": "one_atomic_silver_record_per_grid_packet",
}
TIKTOK_GRID_OBSERVATION_POLICY_FINGERPRINT = hashlib.sha256(
    json.dumps(_POLICY_BASIS, sort_keys=True, separators=(",", ":")).encode("utf-8")
).hexdigest()
_PROFILE_POLICY_BASIS = {
    "policy_version": TIKTOK_PROFILE_METRIC_OBSERVATION_POLICY_VERSION,
    "capture_policy_version": TIKTOK_PROFILE_METRIC_CAPTURE_POLICY_VERSION,
    "source_surface": TIKTOK_GRID_OBSERVATION_SOURCE_SURFACE,
    "identity": "creator_handle",
    "metrics": dict(TIKTOK_PROFILE_METRIC_FIELDS),
    "precision": "exact_integer_only",
    "missing": "unavailable_with_reason; never zero-fill",
    "physicalization": "one_metric_observation_record_per_profile_metric_per_packet",
}
TIKTOK_PROFILE_METRIC_OBSERVATION_POLICY_FINGERPRINT = hashlib.sha256(
    json.dumps(_PROFILE_POLICY_BASIS, sort_keys=True, separators=(",", ":")).encode(
        "utf-8"
    )
).hexdigest()
_PRODUCER_ID = (
    "forseti-harness.capture_spine.creator_profile_current."
    "tiktok_grid_observation_producer"
)


@dataclass(frozen=True)
class TiktokGridObservationResult:
    record: dict[str, Any]
    path: Path
    written: bool


@dataclass(frozen=True)
class TiktokProfileMetricObservationResult:
    record: dict[str, Any]
    path: Path
    written: bool


def observation_set_record_id(
    raw_anchor: str,
    *,
    source_surface: str = TIKTOK_GRID_OBSERVATION_SOURCE_SURFACE,
    policy_fingerprint: str = TIKTOK_GRID_OBSERVATION_POLICY_FINGERPRINT,
) -> str:
    digest = hashlib.sha256(
        f"{raw_anchor}\0{source_surface}\0{policy_fingerprint}".encode("utf-8")
    ).hexdigest()[:24]
    return f"social_metric_set_{digest}.json"


def profile_metric_record_id(
    raw_anchor: str,
    metric_name: str,
    *,
    policy_fingerprint: str = TIKTOK_PROFILE_METRIC_OBSERVATION_POLICY_FINGERPRINT,
) -> str:
    digest = hashlib.sha256(
        f"{raw_anchor}\0{metric_name}\0{policy_fingerprint}".encode("utf-8")
    ).hexdigest()[:24]
    return f"creator_metric_{digest}.json"


def build_tiktok_grid_observation_record(
    *,
    raw_anchor: str,
    grid_payload: Mapping[str, Any],
    raw_file_ref: Mapping[str, Any],
    observed_at: str,
    source_packet_surface: str,
) -> dict[str, Any]:
    observed_at = _required_utc(observed_at)
    creator_handle = _required_text(grid_payload.get("creator_handle"), "creator_handle").lstrip(
        "@"
    )
    items = grid_payload.get("items")
    if grid_payload.get("complete") is not True or not isinstance(items, list) or not items:
        raise ValueError("TikTok grid payload requires complete=true and a non-empty items list")
    if grid_payload.get("window_size") != len(items):
        raise ValueError("TikTok grid window_size does not match items length")

    rows: list[dict[str, Any]] = []
    seen_video_ids: set[str] = set()
    for index, item in enumerate(items):
        if not isinstance(item, Mapping):
            raise ValueError(f"TikTok grid item {index} must be an object")
        video_id = _required_text(item.get("video_id"), f"items[{index}].video_id")
        if video_id in seen_video_ids:
            raise ValueError(f"TikTok grid payload contains duplicate video_id {video_id!r}")
        seen_video_ids.add(video_id)
        stats = item.get("stats") if isinstance(item.get("stats"), Mapping) else item
        metrics = {
            metric_name: _metric(metric_name, source_field, stats.get(source_field))
            for metric_name, source_field in TIKTOK_GRID_METRIC_FIELDS
        }
        rows.append(
            {
                "subject": {
                    "ref_type": "entity_key",
                    "ref": {
                        "namespace": "tiktok",
                        "kind": "public_content_object",
                        "native_id": video_id,
                        "native_id_kind": "tiktok_video_id",
                        "published_by_account_native_id": creator_handle,
                    },
                },
                "source_position": index + 1,
                "content_url": item.get("video_url"),
                "metrics": metrics,
            }
        )

    lineage = SilverLineage(
        producer_id=_PRODUCER_ID,
        producer_schema_version=TIKTOK_GRID_OBSERVATION_PRODUCER_SCHEMA_VERSION,
        source_surface=TIKTOK_GRID_OBSERVATION_SOURCE_SURFACE,
        source_object=SilverSourceObject(
            namespace="tiktok",
            kind="platform_public_account",
            native_id=creator_handle,
            source_url=f"https://www.tiktok.com/@{creator_handle}",
        ),
        observed_at=observed_at,
        captured_at=observed_at,
        raw_refs=[
            SilverRawRef(
                packet_id=raw_anchor,
                file_id=_required_text(raw_file_ref.get("file_id"), "raw_file_ref.file_id"),
                relative_packet_path=_required_text(
                    raw_file_ref.get("relative_packet_path"),
                    "raw_file_ref.relative_packet_path",
                ),
                sha256=_required_text(raw_file_ref.get("sha256"), "raw_file_ref.sha256"),
                hash_basis=_required_text(
                    raw_file_ref.get("hash_basis") or "raw_stored_bytes",
                    "raw_file_ref.hash_basis",
                ),
                anchor=SilverAnchor(kind="file"),
                relation="observed_from",
            )
        ],
    )
    record_id = observation_set_record_id(raw_anchor)
    record: dict[str, Any] = {
        "record_id": record_id,
        "raw_anchor": raw_anchor,
        "lane_namespace": SOCIAL_METRIC_OBSERVATION_SET_LANE,
        "schema_version": SILVER_VAULT_RECORD_SCHEMA_VERSION,
        "content_hash": "",
        "content_hash_basis": CONTENT_HASH_BASIS,
        "record_kind": "observation",
        "payload_kind": METRIC_OBSERVATION_SET_PAYLOAD_KIND,
        "producer_row_kind": "tiktok_creator_grid_metric_set",
        "source_family": "social_media",
        **lineage.to_record_fields(),
        "payload": {
            "observation": {
                "subject": {
                    "ref_type": "entity_key",
                    "ref": {
                        "namespace": "tiktok",
                        "kind": "platform_public_account",
                        "native_id": creator_handle,
                    },
                },
                "observation_set_kind": "social_content_metric_grid",
                "platform": "tiktok",
                "policy_version": TIKTOK_GRID_OBSERVATION_POLICY_VERSION,
                "policy_fingerprint_sha256": TIKTOK_GRID_OBSERVATION_POLICY_FINGERPRINT,
                "coverage_window": {"start": observed_at, "end": observed_at},
                "row_count": len(rows),
                "rows": rows,
            }
        },
        "provenance": {
            "source_packet_surface": source_packet_surface,
            "policy_basis": _POLICY_BASIS,
            "raw_grid_file_id": raw_file_ref.get("file_id"),
        },
        "non_claims": sorted(
            set(
                BASE_NON_CLAIMS
                + (
                    "not a full creator-post history outside captured grids",
                    "not a ranking, velocity, or virality judgment",
                    "not proof that an absent day or metric equals zero",
                )
            )
        ),
    }
    record["content_hash"] = f"sha256:{content_hash(record)}"
    validate_silver_vault_record(record)
    return record


def derive_tiktok_grid_observation_set(
    *,
    data_root: "DataLakeRoot",
    raw_anchor: str,
    grid_payload: Mapping[str, Any],
    raw_file_ref: Mapping[str, Any],
    observed_at: str,
    source_packet_surface: str,
) -> TiktokGridObservationResult:
    record = build_tiktok_grid_observation_record(
        raw_anchor=raw_anchor,
        grid_payload=grid_payload,
        raw_file_ref=raw_file_ref,
        observed_at=observed_at,
        source_packet_surface=source_packet_surface,
    )
    path = data_root.record_path(
        subtree="derived",
        raw_anchor=raw_anchor,
        lane=SOCIAL_METRIC_OBSERVATION_SET_LANE,
        record_id=record["record_id"],
    )
    expected = canonical_record_bytes(record)
    if path.exists():
        if path.read_bytes() != expected:
            raise ValueError(
                f"existing social metric observation set differs for {record['record_id']}"
            )
        return TiktokGridObservationResult(record=record, path=path, written=False)
    written_path = append_silver_record(
        data_root,
        raw_anchor=raw_anchor,
        lane=SOCIAL_METRIC_OBSERVATION_SET_LANE,
        record_id=record["record_id"],
        record=record,
    )
    if written_path.read_bytes() != expected:
        raise ValueError(f"persisted social metric observation set failed byte readback: {written_path}")
    return TiktokGridObservationResult(record=record, path=written_path, written=True)


def build_tiktok_profile_metric_records(
    *,
    raw_anchor: str,
    grid_payload: Mapping[str, Any],
    raw_file_ref: Mapping[str, Any],
    observed_at: str,
    source_packet_surface: str,
) -> tuple[dict[str, Any], ...]:
    if (
        grid_payload.get("profile_metric_capture_policy_version")
        != TIKTOK_PROFILE_METRIC_CAPTURE_POLICY_VERSION
    ):
        return ()
    profile_metrics = grid_payload.get("profile_metrics")
    if not isinstance(profile_metrics, Mapping):
        raise ValueError("TikTok profile metric capture requires profile_metrics")
    observed_at = _required_utc(observed_at)
    creator_handle = _required_text(
        grid_payload.get("creator_handle"), "creator_handle"
    ).lstrip("@")
    heartbeat_binding = grid_payload.get("heartbeat_binding")
    platform_account_id = (
        heartbeat_binding.get("platform_account_id")
        if isinstance(heartbeat_binding, Mapping)
        else None
    )
    if platform_account_id is not None:
        platform_account_id = _required_text(
            platform_account_id, "heartbeat_binding.platform_account_id"
        )

    records: list[dict[str, Any]] = []
    for metric_name, source_field in TIKTOK_PROFILE_METRIC_FIELDS:
        cell = profile_metrics.get(metric_name)
        if not isinstance(cell, Mapping) or cell.get("source_field") != source_field:
            raise ValueError(f"TikTok profile metric {metric_name} has an invalid source binding")
        value = cell.get("exact_value_or_none")
        posture = cell.get("posture")
        reason = cell.get("reason_or_none")
        metric = _profile_metric(metric_name, source_field, posture, value, reason)
        lineage = SilverLineage(
            producer_id=f"{_PRODUCER_ID}#profile_metric",
            producer_schema_version=(
                TIKTOK_PROFILE_METRIC_OBSERVATION_PRODUCER_SCHEMA_VERSION
            ),
            source_surface=TIKTOK_GRID_OBSERVATION_SOURCE_SURFACE,
            source_object=SilverSourceObject(
                namespace="tiktok",
                kind="platform_public_account",
                native_id=creator_handle,
                source_url=f"https://www.tiktok.com/@{creator_handle}",
            ),
            observed_at=observed_at,
            captured_at=observed_at,
            raw_refs=[
                SilverRawRef(
                    packet_id=raw_anchor,
                    file_id=_required_text(
                        raw_file_ref.get("file_id"), "raw_file_ref.file_id"
                    ),
                    relative_packet_path=_required_text(
                        raw_file_ref.get("relative_packet_path"),
                        "raw_file_ref.relative_packet_path",
                    ),
                    sha256=_required_text(
                        raw_file_ref.get("sha256"), "raw_file_ref.sha256"
                    ),
                    hash_basis=_required_text(
                        raw_file_ref.get("hash_basis") or "raw_stored_bytes",
                        "raw_file_ref.hash_basis",
                    ),
                    anchor=SilverAnchor(
                        kind="json_pointer",
                        value=f"/profile_metrics/{metric_name}",
                    ),
                    relation="observed_from",
                )
            ],
        )
        subject_ref: dict[str, Any] = {
            "namespace": "tiktok",
            "kind": "platform_public_account",
            "native_id": creator_handle,
        }
        if platform_account_id is not None:
            subject_ref["platform_account_id"] = platform_account_id
        record: dict[str, Any] = {
            "record_id": profile_metric_record_id(raw_anchor, metric_name),
            "raw_anchor": raw_anchor,
            "lane_namespace": METRIC_OBSERVATION_LANE,
            "schema_version": SILVER_VAULT_RECORD_SCHEMA_VERSION,
            "content_hash": "",
            "content_hash_basis": CONTENT_HASH_BASIS,
            "record_kind": "observation",
            "payload_kind": METRIC_OBSERVATION_PAYLOAD_KIND,
            "producer_row_kind": "tiktok_creator_profile_metric",
            "source_family": "social_media",
            **lineage.to_record_fields(),
            "payload": {
                "observation": {
                    "subject": {"ref_type": "entity_key", "ref": subject_ref},
                    "metric_name": metric_name,
                    "metric_value": metric["metric_value"],
                    "metric_posture": metric["metric_posture"],
                    "coverage_window": {"start": observed_at, "end": observed_at},
                    "source_surface": TIKTOK_GRID_OBSERVATION_SOURCE_SURFACE,
                    "source_publication_or_event": None,
                    "source_surface_count_candidates": [
                        {
                            "source_route": cell.get("source_route"),
                            "source_field": source_field,
                            "raw_text_or_none": cell.get("raw_text_or_none"),
                        }
                    ],
                    "unit": "count",
                }
            },
            "provenance": {
                "source_packet_surface": source_packet_surface,
                "policy_basis": _PROFILE_POLICY_BASIS,
                "policy_fingerprint_sha256": (
                    TIKTOK_PROFILE_METRIC_OBSERVATION_POLICY_FINGERPRINT
                ),
                "raw_grid_file_id": raw_file_ref.get("file_id"),
            },
            "non_claims": sorted(
                set(
                    BASE_NON_CLAIMS
                    + (
                        "not an audience geography or demographic estimate",
                        "not an approximation from compact display text",
                        "not a growth judgment without multiple observations",
                    )
                )
            ),
        }
        record["content_hash"] = f"sha256:{content_hash(record)}"
        validate_silver_vault_record(record)
        records.append(record)
    return tuple(records)


def derive_tiktok_profile_metric_observations(
    *,
    data_root: "DataLakeRoot",
    raw_anchor: str,
    grid_payload: Mapping[str, Any],
    raw_file_ref: Mapping[str, Any],
    observed_at: str,
    source_packet_surface: str,
) -> tuple[TiktokProfileMetricObservationResult, ...]:
    results: list[TiktokProfileMetricObservationResult] = []
    for record in build_tiktok_profile_metric_records(
        raw_anchor=raw_anchor,
        grid_payload=grid_payload,
        raw_file_ref=raw_file_ref,
        observed_at=observed_at,
        source_packet_surface=source_packet_surface,
    ):
        path = data_root.record_path(
            subtree="derived",
            raw_anchor=raw_anchor,
            lane=METRIC_OBSERVATION_LANE,
            record_id=record["record_id"],
        )
        expected = canonical_record_bytes(record)
        if path.exists():
            if path.read_bytes() != expected:
                raise ValueError(
                    f"existing TikTok profile metric differs for {record['record_id']}"
                )
            results.append(
                TiktokProfileMetricObservationResult(
                    record=record, path=path, written=False
                )
            )
            continue
        written_path = append_silver_record(
            data_root,
            raw_anchor=raw_anchor,
            lane=METRIC_OBSERVATION_LANE,
            record_id=record["record_id"],
            record=record,
        )
        if written_path.read_bytes() != expected:
            raise ValueError(
                f"persisted TikTok profile metric failed byte readback: {written_path}"
            )
        results.append(
            TiktokProfileMetricObservationResult(
                record=record, path=written_path, written=True
            )
        )
    return tuple(results)


def _profile_metric(
    metric_name: str,
    source_field: str,
    posture: object,
    value: object,
    reason: object,
) -> dict[str, Any]:
    if posture == "observed":
        if type(value) is not int or value < 0 or reason is not None:
            raise ValueError(f"TikTok profile metric {metric_name} is not an exact count")
        return {
            "metric_value": value,
            "metric_posture": {
                "kind": "observed",
                "reason_code": None,
                "reason_detail": None,
            },
        }
    if posture != "unavailable_with_reason" or value is not None:
        raise ValueError(f"TikTok profile metric {metric_name} has invalid posture coupling")
    if not isinstance(reason, str) or not reason.strip():
        raise ValueError(f"TikTok profile metric {metric_name} lacks an unavailable reason")
    return {
        "metric_value": None,
        "metric_posture": {
            "kind": "unavailable_with_reason",
            "reason_code": reason,
            "reason_detail": (
                f"TikTok profile source field {source_field} did not yield an exact count"
            ),
        },
    }


def _metric(metric_name: str, source_field: str, value: object) -> dict[str, Any]:
    if type(value) is int and value >= 0:
        return {
            "metric_value": value,
            "metric_posture": {
                "kind": "observed",
                "reason_code": None,
                "reason_detail": None,
            },
            "unit": "count",
            "source_field": source_field,
        }
    if value is None:
        reason_code = "source_field_absent"
        reason_detail = f"TikTok grid row did not expose {source_field}; value was never zero-filled"
    elif isinstance(value, bool) or not isinstance(value, int):
        reason_code = "source_field_not_exact_integer"
        reason_detail = f"TikTok grid row exposed {source_field} without an exact integer value"
    else:
        reason_code = "source_field_negative"
        reason_detail = f"TikTok grid row exposed a negative {source_field} value"
    return {
        "metric_value": None,
        "metric_posture": {
            "kind": "unavailable_with_reason",
            "reason_code": reason_code,
            "reason_detail": reason_detail,
        },
        "unit": "count",
        "source_field": source_field,
    }


def _required_text(value: object, field: str) -> str:
    if not isinstance(value, (str, int)) or isinstance(value, bool):
        raise ValueError(f"{field} is missing or invalid")
    text = str(value).strip()
    if not text:
        raise ValueError(f"{field} is blank")
    return text


def _required_utc(value: object) -> str:
    text = _required_text(value, "observed_at")
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("observed_at must be a valid UTC timestamp") from exc
    if (
        parsed.tzinfo is None
        or parsed.utcoffset() is None
        or parsed.utcoffset().total_seconds() != 0
    ):
        raise ValueError("observed_at must be UTC")
    return parsed.isoformat().replace("+00:00", "Z")


__all__ = [
    "METRIC_OBSERVATION_LANE",
    "SOCIAL_METRIC_OBSERVATION_SET_LANE",
    "TIKTOK_GRID_OBSERVATION_POLICY_FINGERPRINT",
    "TIKTOK_GRID_OBSERVATION_POLICY_VERSION",
    "TIKTOK_GRID_OBSERVATION_SOURCE_SURFACE",
    "TIKTOK_PROFILE_METRIC_OBSERVATION_POLICY_FINGERPRINT",
    "TIKTOK_PROFILE_METRIC_OBSERVATION_POLICY_VERSION",
    "TiktokGridObservationResult",
    "TiktokProfileMetricObservationResult",
    "build_tiktok_profile_metric_records",
    "build_tiktok_grid_observation_record",
    "derive_tiktok_grid_observation_set",
    "derive_tiktok_profile_metric_observations",
    "observation_set_record_id",
    "profile_metric_record_id",
]
