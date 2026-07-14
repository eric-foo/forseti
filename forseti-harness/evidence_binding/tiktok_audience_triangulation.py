"""Build one creator-isolated, pre-Judgment TikTok audience evidence bundle."""
from __future__ import annotations

import hashlib
import json
import re
from collections import defaultdict
from typing import Any, Mapping, Sequence

from capture_spine.creator_profile_current.tiktok_comment_attention_producer import (
    COMMENT_ATTENTION_POLICY_FINGERPRINT,
    COMMENT_ATTENTION_RECIPE_VERSION,
)

EVIDENCE_BUNDLE_SCHEMA_VERSION = "creator_audience_evidence_bundle_v0"
ASSEMBLY_RECEIPT_SCHEMA_VERSION = "creator_audience_evidence_assembly_receipt_v0"
ASSEMBLY_RECEIPT_LANE = "creator_audience_evidence_assembly_receipt"
_WS = re.compile(r"\s+")


def normalized_creator(value: str) -> str:
    text = value.strip().casefold()
    if text.startswith("tiktok:@"):
        return text
    return f"tiktok:@{text.lstrip('@')}"


def _stable_id(prefix: str, *parts: object, size: int = 20) -> str:
    payload = "\0".join(str(part) for part in parts).encode("utf-8")
    return f"{prefix}_{hashlib.sha256(payload).hexdigest()[:size]}"


def _canonical_bytes(value: Mapping[str, Any]) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _selected_videos(payload: Mapping[str, Any], *, limit: int) -> tuple[list[Mapping[str, Any]], int]:
    rows = payload.get("videos")
    if not isinstance(rows, list) or not all(isinstance(row, Mapping) for row in rows):
        raise ValueError("TikTok audience packet requires a videos list")
    if not rows:
        raise ValueError("TikTok audience packet contains no videos")
    if len(rows) <= limit:
        return list(rows), 0

    def reach_key(row: Mapping[str, Any]) -> tuple[int, int, int, str]:
        stats = row.get("stats") if isinstance(row.get("stats"), Mapping) else {}
        plays = stats.get("playCount") if type(stats.get("playCount")) is int else -1
        likes = stats.get("diggCount") if type(stats.get("diggCount")) is int else -1
        source_index = row.get("source_index") if type(row.get("source_index")) is int else 10**9
        return (-plays, -likes, source_index, str(row.get("video_id") or ""))

    selected = sorted(rows, key=reach_key)[:limit]
    return selected, len(rows) - len(selected)


def _attention_index(records: Sequence[Mapping[str, Any]], raw_anchor: str) -> dict[tuple[str, str], Mapping[str, Any]]:
    result: dict[tuple[str, str], Mapping[str, Any]] = {}
    for record in records:
        if record.get("raw_anchor") != raw_anchor:
            raise ValueError("comment-attention records mix raw anchors")
        provenance = record.get("provenance") if isinstance(record.get("provenance"), Mapping) else {}
        if provenance.get("policy_fingerprint_sha256") != COMMENT_ATTENTION_POLICY_FINGERPRINT:
            raise ValueError("comment-attention policy fingerprint is stale or mismatched")
        if provenance.get("calculation_recipe_version") != COMMENT_ATTENTION_RECIPE_VERSION:
            raise ValueError("comment-attention recipe version is stale or mismatched")
        video_id = str(provenance.get("video_id") or "").strip()
        comment_id = str(provenance.get("comment_id") or "").strip()
        source_order = provenance.get("source_order")
        key_id = comment_id or f"source_order:{source_order}"
        if not video_id or not key_id:
            raise ValueError("comment-attention record lacks video/comment identity")
        key = (video_id, key_id)
        if key in result:
            raise ValueError(f"duplicate comment-attention record for {video_id}:{key_id}")
        result[key] = record
    return result


def _mechanics(record: Mapping[str, Any]) -> dict[str, Any]:
    payload = record.get("payload") if isinstance(record.get("payload"), Mapping) else {}
    observation = payload.get("observation") if isinstance(payload.get("observation"), Mapping) else {}
    context = observation.get("engagement_context") if isinstance(observation.get("engagement_context"), Mapping) else {}
    pairing = observation.get("temporal_pairing") if isinstance(observation.get("temporal_pairing"), Mapping) else {}
    return {
        "comment_attention_record_id": record.get("record_id"),
        "comment_attention_content_hash": record.get("content_hash"),
        "comment_likes": (observation.get("numerator") or {}).get("metric_value") if isinstance(observation.get("numerator"), Mapping) else None,
        "video_likes": (observation.get("denominator") or {}).get("metric_value") if isinstance(observation.get("denominator"), Mapping) else None,
        "comment_like_to_video_like_ratio": observation.get("metric_value"),
        "comment_like_to_video_like_ratio_posture": observation.get("metric_posture"),
        "comment_like_to_video_comment_count_ratio": context.get("comment_like_to_video_comment_count_ratio"),
        "comment_like_to_video_comment_count_ratio_posture": context.get("comment_like_to_video_comment_count_ratio_posture"),
        "comment_like_rank_within_captured": context.get("comment_like_rank_within_captured"),
        "comment_like_percentile_within_captured": context.get("comment_like_percentile_within_captured"),
        "comment_observed_at": pairing.get("comment_observed_at"),
        "video_stats_observed_at": pairing.get("video_stats_observed_at"),
        "temporal_alignment": pairing.get("alignment"),
    }


def build_creator_audience_evidence_bundle(
    *,
    creator_id: str,
    profile_subject_id: str,
    raw_anchor: str,
    batch_payload: Mapping[str, Any],
    comment_attention_records: Sequence[Mapping[str, Any]],
    grid_observation_refs: Sequence[Mapping[str, Any]],
    question: str,
    evidence_cutoff: str,
    silver_selection_residuals: Sequence[Mapping[str, Any]] = (),
    video_limit: int = 8,
) -> dict[str, Any]:
    creator_id = normalized_creator(creator_id)
    handle = str(batch_payload.get("creator_handle") or "").strip()
    if not handle or normalized_creator(handle) != creator_id:
        raise ValueError("TikTok batch creator does not match requested creator")
    if not profile_subject_id.strip() or not raw_anchor.strip() or not question.strip() or not evidence_cutoff.strip():
        raise ValueError("profile_subject_id, raw_anchor, question, and evidence_cutoff are required")

    videos, excluded_count = _selected_videos(batch_payload, limit=video_limit)
    raw_video_indexes = {
        str(row.get("video_id") or ""): index
        for index, row in enumerate(batch_payload["videos"])
        if isinstance(row, Mapping)
    }
    attention = _attention_index(comment_attention_records, raw_anchor)
    transcript_rows: list[dict[str, Any]] = []
    comments: list[dict[str, Any]] = []
    cluster_members: dict[str, list[str]] = defaultdict(list)
    cluster_text: dict[str, str] = {}

    for video in videos:
        video_id = str(video.get("video_id") or "").strip()
        if not video_id:
            raise ValueError("selected video lacks video_id")
        raw_video_index = raw_video_indexes[video_id]
        subtitles = video.get("subtitles") if isinstance(video.get("subtitles"), Mapping) else {}
        cues = subtitles.get("cues") if isinstance(subtitles.get("cues"), list) else []
        for cue_index, cue in enumerate(cues):
            if not isinstance(cue, Mapping):
                raise ValueError(f"video {video_id} subtitle cue {cue_index} must be an object")
            text = str(cue.get("text") or "").strip()
            if not text:
                continue
            transcript_rows.append({
                "evidence_id": _stable_id("ttte", creator_id, video_id, cue_index, text),
                "creator_id": creator_id,
                "video_id": video_id,
                "text": text,
                "start_ms": cue.get("start_ms"),
                "end_ms": cue.get("end_ms"),
                "source_pointer": f"/videos/{raw_video_index}/subtitles/cues/{cue_index}",
                "transcript_text_sha256": subtitles.get("transcript_text_sha256"),
            })

        block = video.get("comments") if isinstance(video.get("comments"), Mapping) else {}
        comment_rows = block.get("comments") if isinstance(block.get("comments"), list) else []
        for source_index, raw in enumerate(comment_rows):
            if not isinstance(raw, Mapping):
                raise ValueError(f"video {video_id} comment {source_index} must be an object")
            text = str(raw.get("text") or "").strip()
            if not text:
                continue
            comment_id = str(raw.get("cid") or f"source_order:{raw.get('source_order')}")
            record = attention.get((video_id, comment_id))
            if record is None:
                raise ValueError(f"missing persisted Silver comment attention for {video_id}:{comment_id}")
            evidence_id = _stable_id("ttce", creator_id, video_id, comment_id, text)
            cluster_id = _stable_id("ttcc", _WS.sub(" ", text.casefold()).strip(), size=16)
            cluster_members[cluster_id].append(evidence_id)
            cluster_text[cluster_id] = text
            comments.append({
                "evidence_id": evidence_id,
                "creator_id": creator_id,
                "video_id": video_id,
                "comment_id": comment_id,
                "text": text,
                "source_order": raw.get("source_order"),
                "source_pointer": (
                    f"/videos/{raw_video_index}/comments/comments/{source_index}"
                ),
                "duplicate_cluster_id": cluster_id,
                **_mechanics(record),
            })

    if not transcript_rows:
        raise ValueError("INCOMPLETE_AUDIENCE_EVIDENCE: no captured transcript cues")
    if not comments:
        raise ValueError("INCOMPLETE_AUDIENCE_EVIDENCE: no captured top-level comments")

    core: dict[str, Any] = {
        "schema_version": EVIDENCE_BUNDLE_SCHEMA_VERSION,
        "creator_id": creator_id,
        "profile_subject_kind": "platform_account",
        "profile_subject_id": profile_subject_id.strip(),
        "platform_scope": "tiktok",
        "raw_anchor": raw_anchor.strip(),
        "question": question.strip(),
        "evidence_cutoff": evidence_cutoff.strip(),
        "capture_scope": {
            "selected_video_ids": [str(video.get("video_id")) for video in videos],
            "selected_video_count": len(videos),
            "excluded_video_count": excluded_count,
            "video_selection_policy": "captured_selection_or_reach_ranked_top_8_v0",
            "comment_selection_posture": "all_captured_top_level_comments_from_selected_videos",
            "limitations": [
                "not_platform_wide_comment_census",
                "captured_video_selection_may_be_ranked_or_truncated",
                "not_reply_thread_analysis",
            ],
        },
        "transcript_evidence": sorted(transcript_rows, key=lambda row: row["evidence_id"]),
        "comment_evidence": sorted(comments, key=lambda row: row["evidence_id"]),
        "exact_duplicate_clusters": [
            {
                "cluster_id": cluster_id,
                "representative_text": cluster_text[cluster_id],
                "evidence_ids": sorted(ids),
                "multiplicity": len(ids),
            }
            for cluster_id, ids in sorted(cluster_members.items())
        ],
        "source_refs": {
            "raw_packet_id": raw_anchor,
            "comment_attention_record_ids": sorted(str(row.get("record_id")) for row in comment_attention_records),
            "grid_observation_refs": list(grid_observation_refs),
            "comment_attention_policy_fingerprint_sha256": COMMENT_ATTENTION_POLICY_FINGERPRINT,
            "comment_attention_recipe_version": COMMENT_ATTENTION_RECIPE_VERSION,
            "silver_selection_residuals": list(silver_selection_residuals),
        },
        "judgment_status": "not_evaluated",
    }
    bundle_hash = f"sha256:{hashlib.sha256(_canonical_bytes(core)).hexdigest()}"
    core["bundle_hash"] = bundle_hash
    core["bundle_id"] = _stable_id("caeb", raw_anchor, bundle_hash)
    core["serialized_utf8_bytes"] = len(_canonical_bytes(core))
    return core


def build_assembly_receipt(bundle: Mapping[str, Any]) -> dict[str, Any]:
    evidence_index = [
        {
            "evidence_id": row.get("evidence_id"),
            "evidence_kind": evidence_kind,
            "video_id": row.get("video_id"),
            "source_pointer": row.get("source_pointer"),
            **(
                {
                    "comment_attention_record_id": row.get("comment_attention_record_id"),
                    "comment_attention_content_hash": row.get("comment_attention_content_hash"),
                }
                if evidence_kind == "captured_top_level_comment"
                else {}
            ),
        }
        for evidence_kind, rows in (
            ("transcript_cue", bundle.get("transcript_evidence", [])),
            ("captured_top_level_comment", bundle.get("comment_evidence", [])),
        )
        for row in rows
        if isinstance(row, Mapping)
    ]
    return {
        "schema_version": ASSEMBLY_RECEIPT_SCHEMA_VERSION,
        "record_id": _stable_id("caer", bundle.get("raw_anchor"), bundle.get("bundle_hash")),
        "raw_anchor": bundle.get("raw_anchor"),
        "bundle_id": bundle.get("bundle_id"),
        "bundle_hash": bundle.get("bundle_hash"),
        "bundle_schema_version": bundle.get("schema_version"),
        "creator_id": bundle.get("creator_id"),
        "profile_subject_id": bundle.get("profile_subject_id"),
        "evidence_cutoff": bundle.get("evidence_cutoff"),
        "selected_video_ids": bundle.get("capture_scope", {}).get("selected_video_ids"),
        "transcript_evidence_count": len(bundle.get("transcript_evidence", [])),
        "comment_evidence_count": len(bundle.get("comment_evidence", [])),
        "evidence_index": sorted(evidence_index, key=lambda row: str(row["evidence_id"])),
        "source_refs": bundle.get("source_refs"),
        "judgment_status": "not_evaluated",
    }


__all__ = [
    "ASSEMBLY_RECEIPT_LANE",
    "ASSEMBLY_RECEIPT_SCHEMA_VERSION",
    "EVIDENCE_BUNDLE_SCHEMA_VERSION",
    "build_assembly_receipt",
    "build_creator_audience_evidence_bundle",
    "normalized_creator",
]
