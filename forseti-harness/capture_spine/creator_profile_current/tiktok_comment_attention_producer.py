"""Source-backed TikTok comment-attention Silver observations.

The metric is deliberately mechanical:

    comment_like_to_video_like_ratio = comment_like_count / video_like_count

It does not decide whether a comment is credible, relevant, or important.  Those
are later Cleaning/Judgment concerns.  Missing or zero denominators fail loud via
metric posture rather than becoming a numeric zero.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, Mapping

from capture_spine.creator_profile_current.silver_envelope_core import (
    BASE_NON_CLAIMS,
    CONTENT_HASH_BASIS,
    SILVER_VAULT_RECORD_SCHEMA_VERSION,
    content_hash,
)
from data_lake.silver_record import append_silver_record
from data_lake.canonical_json import canonical_record_bytes
from source_capture.tiktok.batch_packet import TIKTOK_BATCH_CAPTURE_SURFACE

if TYPE_CHECKING:
    from data_lake.root import DataLakeRoot


COMMENT_ATTENTION_LANE = "tiktok_comment_attention_silver"
COMMENT_ATTENTION_METRIC = "comment_like_to_video_like_ratio"
COMMENT_ATTENTION_RECIPE_VERSION = "tiktok_comment_attention_ratio_v0"
COMMENT_ATTENTION_PRODUCER_SCHEMA_VERSION = "tiktok_comment_attention_metric_observation_v0"
COMMENT_ATTENTION_POLICY_FINGERPRINT = hashlib.sha256(
    json.dumps(
        {
            "recipe_version": COMMENT_ATTENTION_RECIPE_VERSION,
            "numerator": "captured_comment.digg_count",
            "denominator": "video.stats.diggCount",
            "zero_denominator": "unavailable_with_reason",
            "rounding": "none_binary64_division",
        },
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
).hexdigest()
_PRODUCER_ID = (
    "forseti-harness.capture_spine.creator_profile_current."
    "tiktok_comment_attention_producer"
)


@dataclass(frozen=True)
class CommentAttentionSilverResult:
    records: list[dict[str, Any]]
    paths: list[Path]
    skipped_record_ids: list[str]


def _record_id(raw_anchor: str, video_id: str, comment_id: str) -> str:
    digest = hashlib.sha256(
        f"{raw_anchor}\0{video_id}\0{comment_id}\0{COMMENT_ATTENTION_POLICY_FINGERPRINT}".encode(
            "utf-8"
        )
    ).hexdigest()[:24]
    return f"comment_attention_{digest}.json"


def _posture(comment_likes: object, video_likes: object) -> tuple[float | None, dict[str, Any]]:
    if type(comment_likes) is not int or comment_likes < 0:
        return None, {
            "kind": "unavailable_with_reason",
            "reason_code": "comment_like_count_unavailable",
            "reason_detail": "captured comment did not carry a non-negative integer like count",
        }
    if type(video_likes) is not int or video_likes < 0:
        return None, {
            "kind": "unavailable_with_reason",
            "reason_code": "video_like_count_unavailable",
            "reason_detail": "video did not carry a non-negative integer like count",
        }
    if video_likes == 0:
        return None, {
            "kind": "unavailable_with_reason",
            "reason_code": "video_like_count_zero_denominator",
            "reason_detail": "comment attention ratio is undefined when video like count is zero",
        }
    return comment_likes / video_likes, {
        "kind": "observed",
        "reason_code": None,
        "reason_detail": None,
    }


def build_comment_attention_records(
    *,
    raw_anchor: str,
    batch_payload: Mapping[str, Any],
    raw_file_ref: Mapping[str, Any],
) -> list[dict[str, Any]]:
    videos = batch_payload.get("videos")
    if not isinstance(videos, list):
        raise ValueError("TikTok batch payload requires a videos list")
    captured_at = str(batch_payload.get("capture_timestamp") or "").strip() or None
    records: list[dict[str, Any]] = []
    for video_index, video in enumerate(videos):
        if not isinstance(video, Mapping):
            raise ValueError(f"TikTok batch video {video_index} must be an object")
        video_id = str(video.get("video_id") or video.get("id") or "").strip()
        if not video_id:
            raise ValueError(f"TikTok batch video {video_index} lacks video_id")
        stats = video.get("stats") if isinstance(video.get("stats"), Mapping) else {}
        video_likes = stats.get("diggCount")
        comment_block = video.get("comments") if isinstance(video.get("comments"), Mapping) else {}
        comments = comment_block.get("comments")
        if not isinstance(comments, list):
            continue
        observed_at = str(comment_block.get("observed_utc") or captured_at or "").strip() or None
        for comment_index, comment in enumerate(comments):
            if not isinstance(comment, Mapping):
                raise ValueError(
                    f"TikTok batch video {video_id} comment {comment_index} must be an object"
                )
            source_order = comment.get("source_order")
            native_comment_id = str(comment.get("cid") or "").strip()
            comment_id = native_comment_id or f"dom:{video_id}:{source_order}"
            comment_likes = comment.get("digg_count")
            value, metric_posture = _posture(comment_likes, video_likes)
            record_id = _record_id(raw_anchor, video_id, comment_id)
            record: dict[str, Any] = {
                "record_id": record_id,
                "raw_anchor": raw_anchor,
                "lane_namespace": COMMENT_ATTENTION_LANE,
                "producer_id": _PRODUCER_ID,
                "schema_version": SILVER_VAULT_RECORD_SCHEMA_VERSION,
                "producer_schema_version": COMMENT_ATTENTION_PRODUCER_SCHEMA_VERSION,
                "content_hash": "",
                "content_hash_basis": CONTENT_HASH_BASIS,
                "record_kind": "observation",
                "payload_kind": "MetricObservation",
                "producer_row_kind": "tiktok_comment_attention_metric",
                "source_family": "social_media",
                "source_surface": TIKTOK_BATCH_CAPTURE_SURFACE,
                "lineage_schema_version": "silver_lineage_v0",
                "source_object": {
                    "namespace": "tiktok",
                    "kind": "public_comment",
                    "native_id": comment_id,
                },
                "observed_at": observed_at,
                "captured_at": captured_at,
                "raw_refs": [
                    {
                        "ref_type": "raw_packet",
                        "packet_id": raw_anchor,
                        "file_id": raw_file_ref.get("file_id"),
                        "relative_packet_path": raw_file_ref.get("relative_packet_path"),
                        "sha256": raw_file_ref.get("sha256"),
                        "hash_basis": raw_file_ref.get("hash_basis", "raw_stored_bytes"),
                        "anchor": {"kind": "json_pointer", "value": f"/videos/{video_index}"},
                        "relation": "observed_from",
                    }
                ],
                "derived_refs": [],
                "lineage_limitations": [],
                "payload": {
                    "observation": {
                        "subject": {
                            "ref_type": "entity_key",
                            "ref": {
                                "namespace": "tiktok",
                                "kind": "public_comment",
                                "native_id": comment_id,
                                "comment_on_content_native_id": video_id,
                                "comment_on_content_native_id_kind": "tiktok_video_id",
                            },
                        },
                        "metric_name": COMMENT_ATTENTION_METRIC,
                        "metric_value": value,
                        "metric_posture": metric_posture,
                        "coverage_window": {"start": None, "end": None},
                        "source_surface": TIKTOK_BATCH_CAPTURE_SURFACE,
                        "source_publication_or_event": comment.get("create_time_utc"),
                        "unit": "ratio",
                        "numerator": {
                            "metric_name": "comment_like_count",
                            "metric_value": comment_likes if type(comment_likes) is int else None,
                        },
                        "denominator": {
                            "metric_name": "video_like_count",
                            "metric_value": video_likes if type(video_likes) is int else None,
                        },
                    }
                },
                "provenance": {
                    "calculation_recipe_version": COMMENT_ATTENTION_RECIPE_VERSION,
                    "policy_fingerprint_sha256": COMMENT_ATTENTION_POLICY_FINGERPRINT,
                    "video_id": video_id,
                    "comment_id": native_comment_id or None,
                    "source_order": source_order,
                },
                "non_claims": sorted(
                    set(
                        BASE_NON_CLAIMS
                        + (
                            "not comment relevance, credibility, or decision impact",
                            "not a calibrated prioritization threshold",
                            "not a full comment census",
                        )
                    )
                ),
            }
            record["content_hash"] = f"sha256:{content_hash(record)}"
            records.append(record)
    return records


def derive_comment_attention_silver_records(
    *,
    data_root: "DataLakeRoot",
    raw_anchor: str,
    batch_payload: Mapping[str, Any],
    raw_file_ref: Mapping[str, Any],
) -> CommentAttentionSilverResult:
    records = build_comment_attention_records(
        raw_anchor=raw_anchor,
        batch_payload=batch_payload,
        raw_file_ref=raw_file_ref,
    )
    paths: list[Path] = []
    skipped: list[str] = []
    for record in records:
        existing = data_root.record_path(
            subtree="derived",
            raw_anchor=raw_anchor,
            lane=COMMENT_ATTENTION_LANE,
            record_id=record["record_id"],
        )
        if existing.exists():
            if existing.read_bytes() != canonical_record_bytes(record):
                raise ValueError(
                    f"existing comment-attention record differs for {record['record_id']}"
                )
            skipped.append(record["record_id"])
            continue
        paths.append(
            append_silver_record(
                data_root,
                raw_anchor=raw_anchor,
                lane=COMMENT_ATTENTION_LANE,
                record_id=record["record_id"],
                record=record,
            )
        )
    return CommentAttentionSilverResult(records=records, paths=paths, skipped_record_ids=skipped)


__all__ = [
    "COMMENT_ATTENTION_LANE",
    "COMMENT_ATTENTION_METRIC",
    "COMMENT_ATTENTION_POLICY_FINGERPRINT",
    "COMMENT_ATTENTION_RECIPE_VERSION",
    "CommentAttentionSilverResult",
    "build_comment_attention_records",
    "derive_comment_attention_silver_records",
]
