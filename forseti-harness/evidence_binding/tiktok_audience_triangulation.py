"""Deterministic, creator-isolated Gold-ready TikTok audience assembly."""
from __future__ import annotations

import hashlib
import json
import re
from collections import defaultdict
from typing import Any, Mapping, Sequence

from capture_spine.creator_profile_current.tiktok_comment_attention_producer import (
    mechanical_comment_attention,
)
from schemas.tiktok_audience_evidence_models import TikTokAudienceEvidence

GOLD_READY_AUDIENCE_SCHEMA_VERSION = "gold_ready_audience_evidence_v0"
_WS = re.compile(r"\s+")


def _normalized_creator(value: str) -> str:
    text = value.strip().casefold()
    if text.startswith("tiktok:@"):
        return text
    return f"tiktok:@{text.lstrip('@')}"


def _cluster_key(text: str) -> str:
    return _WS.sub(" ", text.strip().casefold())


def _comment_evidence_id(creator_id: str, video_id: str, comment_id: str, text: str) -> str:
    digest = hashlib.sha256(
        f"{creator_id}\0{video_id}\0{comment_id}\0{text}".encode("utf-8")
    ).hexdigest()[:20]
    return f"ttce_{digest}"


def build_gold_ready_audience_evidence(
    *,
    creator_id: str,
    batch_payloads: Sequence[Mapping[str, Any]],
    transcript_evidence: Sequence[Mapping[str, Any] | TikTokAudienceEvidence],
    question: str,
    evidence_cutoff: str,
    semantic_labels: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    creator_id = _normalized_creator(creator_id)
    if not question.strip() or not evidence_cutoff.strip():
        raise ValueError("question and evidence_cutoff must be non-blank")

    videos: dict[str, Mapping[str, Any]] = {}
    capture_times: list[str] = []
    for payload_index, payload in enumerate(batch_payloads):
        handle = str(payload.get("creator_handle") or "").strip()
        if not handle or _normalized_creator(handle) != creator_id:
            raise ValueError(f"batch payload {payload_index} creator does not match {creator_id}")
        capture_time = str(payload.get("capture_timestamp") or "").strip()
        if capture_time:
            capture_times.append(capture_time)
        rows = payload.get("videos")
        if not isinstance(rows, list):
            raise ValueError(f"batch payload {payload_index} requires a videos list")
        for row in rows:
            if not isinstance(row, Mapping):
                raise ValueError("batch video rows must be objects")
            video_id = str(row.get("video_id") or "").strip()
            if not video_id:
                raise ValueError("batch video row lacks video_id")
            if video_id in videos:
                raise ValueError(f"duplicate video_id across audience inputs: {video_id}")
            videos[video_id] = row

    transcript_rows: list[dict[str, Any]] = []
    for raw in transcript_evidence:
        row = raw if isinstance(raw, TikTokAudienceEvidence) else TikTokAudienceEvidence.model_validate(raw)
        if _normalized_creator(row.creator_id) != creator_id:
            raise ValueError("transcript evidence mixes creators")
        if row.video_id not in videos:
            raise ValueError(f"transcript evidence references unknown video {row.video_id}")
        transcript_rows.append(row.model_dump(mode="json"))

    comments: list[dict[str, Any]] = []
    cluster_members: dict[str, list[str]] = defaultdict(list)
    cluster_text: dict[str, str] = {}
    for video_id in sorted(videos):
        video = videos[video_id]
        block = video.get("comments") if isinstance(video.get("comments"), Mapping) else {}
        rows = block.get("comments") if isinstance(block.get("comments"), list) else []
        mechanics = mechanical_comment_attention(video)
        mechanics_by_id = {row["comment_id"]: row for row in mechanics["comments"]}
        for source_index, raw in enumerate(rows):
            if not isinstance(raw, Mapping):
                raise ValueError(f"video {video_id} comment {source_index} must be an object")
            comment_id = str(raw.get("cid") or f"source_order:{raw.get('source_order')}")
            text = str(raw.get("text") or "").strip()
            if not text:
                continue
            evidence_id = _comment_evidence_id(creator_id, video_id, comment_id, text)
            cluster_digest = hashlib.sha256(_cluster_key(text).encode("utf-8")).hexdigest()[:16]
            cluster_id = f"ttcc_{cluster_digest}"
            cluster_members[cluster_id].append(evidence_id)
            cluster_text[cluster_id] = text
            label_key = f"{video_id}:{comment_id}"
            labels = semantic_labels.get(label_key) if semantic_labels else None
            if labels is not None and (not isinstance(labels, list) or not all(isinstance(v, str) for v in labels)):
                raise ValueError(f"semantic labels for {label_key} must be a string list")
            mechanical = mechanics_by_id[comment_id]
            comments.append(
                {
                    "evidence_id": evidence_id,
                    "creator_id": creator_id,
                    "video_id": video_id,
                    "comment_id": comment_id,
                    "text": text,
                    "source_order": raw.get("source_order"),
                    "source_pointer": f"/videos/{video_id}/comments/{source_index}",
                    "duplicate_cluster_id": cluster_id,
                    "semantic_labels": sorted(set(labels)) if labels else [],
                    "semantic_posture": "classified" if labels else "not_attempted",
                    **mechanical,
                    "comment_observed_at": mechanics["comment_observed_at"],
                    "video_stats_observed_at": mechanics["video_stats_observed_at"],
                    "temporal_alignment": mechanics["temporal_alignment"],
                }
            )

    clusters = [
        {
            "cluster_id": cluster_id,
            "representative_text": cluster_text[cluster_id],
            "evidence_ids": sorted(members),
            "multiplicity": len(members),
        }
        for cluster_id, members in sorted(cluster_members.items())
    ]
    all_ids = [row["evidence_id"] for row in transcript_rows] + [row["evidence_id"] for row in comments]
    if not all_ids:
        raise ValueError("Gold-ready audience assembly requires transcript or comment evidence")
    assembly: dict[str, Any] = {
        "schema_version": GOLD_READY_AUDIENCE_SCHEMA_VERSION,
        "creator_id": creator_id,
        "question": question.strip(),
        "evidence_cutoff": evidence_cutoff.strip(),
        "capture_scope": {
            "batch_count": len(batch_payloads),
            "video_count": len(videos),
            "captured_top_level_comment_count": len(comments),
            "capture_timestamps": sorted(set(capture_times)),
            "comment_selection_posture": "all_captured_top_level_comments_from_selected_videos",
            "limitations": [
                "not_platform_wide_comment_census",
                "captured_video_selection_may_be_ranked_or_truncated",
                "not_reply_thread_analysis",
            ],
        },
        "transcript_evidence": sorted(transcript_rows, key=lambda row: row["evidence_id"]),
        "comment_evidence": sorted(comments, key=lambda row: row["evidence_id"]),
        "exact_duplicate_clusters": clusters,
        "assembly_receipt": {
            "evidence_ids": sorted(all_ids),
            "transcript_evidence_count": len(transcript_rows),
            "comment_evidence_count": len(comments),
            "distinct_video_count": len(videos),
            "judgment_status": "not_evaluated",
        },
    }
    assembly["assembly_receipt"]["serialized_utf8_bytes"] = len(
        json.dumps(assembly, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    )
    return assembly


__all__ = ["GOLD_READY_AUDIENCE_SCHEMA_VERSION", "build_gold_ready_audience_evidence"]
