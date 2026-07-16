"""Build one Instagram platform-account audience bundle from admitted Reel Silver."""
from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Mapping, Sequence
from typing import Any

from source_capture.ig_reels_deep_capture_lake import (
    comments_compatibility_view,
    transcript_compatibility_view,
)

EVIDENCE_BUNDLE_SCHEMA_VERSION = "creator_audience_evidence_bundle_v1"
_WS = re.compile(r"\s+")


def _canonical_bytes(value: Mapping[str, Any]) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def _stable_id(prefix: str, *parts: object, size: int = 20) -> str:
    payload = "\0".join(str(part) for part in parts).encode("utf-8")
    return f"{prefix}_{hashlib.sha256(payload).hexdigest()[:size]}"


def _view(record: Mapping[str, Any], *, kind: str) -> dict[str, Any]:
    if isinstance(record.get("payload"), Mapping):
        return dict(
            comments_compatibility_view(record)
            if kind == "comments"
            else transcript_compatibility_view(record)
        )
    return dict(record)


def _index(
    records: Sequence[Mapping[str, Any]], *, kind: str
) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    indexed: dict[str, dict[str, Any]] = {}
    residuals: list[dict[str, Any]] = []
    for record in records:
        view = _view(record, kind=kind)
        shortcode = str(view.get("reel_shortcode") or "").strip()
        if not shortcode:
            raise ValueError(f"Instagram {kind} record lacks reel_shortcode")
        if shortcode in indexed:
            raise ValueError(f"duplicate Instagram {kind} record for {shortcode}")
        if not isinstance(record.get("payload"), Mapping):
            residuals.append(
                {
                    "shortcode": shortcode,
                    "kind": kind,
                    "status": "legacy_compatibility_view",
                }
            )
        indexed[shortcode] = view
    return indexed, residuals


def build_instagram_creator_audience_evidence_bundle(
    *,
    creator_id: str,
    profile_subject_id: str,
    primary_raw_anchor: str,
    comment_records: Sequence[Mapping[str, Any]],
    transcript_records: Sequence[Mapping[str, Any]],
    question: str,
    evidence_cutoff: str,
) -> dict[str, Any]:
    """Assemble one deterministic audit bundle from 1-8 already-selected Reels."""

    required = (creator_id, profile_subject_id, primary_raw_anchor, question, evidence_cutoff)
    if any(not value.strip() for value in required):
        raise ValueError("creator, subject, anchor, question, and cutoff are required")
    normalized_creator = creator_id.strip().casefold()
    if not normalized_creator.startswith("instagram:@"):
        normalized_creator = f"instagram:@{normalized_creator.lstrip('@')}"

    comments_by_item, comment_residuals = _index(comment_records, kind="comments")
    transcripts_by_item, transcript_residuals = _index(
        transcript_records, kind="transcript"
    )
    comment_items = set(comments_by_item)
    transcript_items = set(transcripts_by_item)
    if comment_items != transcript_items:
        raise ValueError(
            "INCOMPLETE_AUDIENCE_EVIDENCE: Instagram comment/transcript Reel sets differ"
        )
    item_ids = sorted(comment_items)
    if not item_ids:
        raise ValueError("INCOMPLETE_AUDIENCE_EVIDENCE: no complete Instagram Reels")
    if len(item_ids) > 8:
        raise ValueError("Instagram audience adapter accepts at most 8 selected Reels")

    transcript_evidence: list[dict[str, Any]] = []
    comment_evidence: list[dict[str, Any]] = []
    cluster_members: dict[str, list[str]] = {}
    cluster_text: dict[str, str] = {}
    for shortcode in item_ids:
        transcript = transcripts_by_item[shortcode]
        cues = transcript.get("cues")
        if not isinstance(cues, list):
            raise ValueError(f"Instagram transcript record {shortcode} lacks cues")
        for cue_index, cue in enumerate(cues):
            if not isinstance(cue, Mapping):
                continue
            text = str(cue.get("text") or "").strip()
            if not text:
                continue
            transcript_evidence.append(
                {
                    "evidence_id": _stable_id(
                        "igte", normalized_creator, shortcode, cue_index, text
                    ),
                    "creator_id": normalized_creator,
                    "source_item_id": shortcode,
                    "video_id": shortcode,
                    "text": text,
                    "start_ms": cue.get("start_ms"),
                    "end_ms": cue.get("end_ms"),
                    "source_pointer": f"instagram:{shortcode}:transcript:{cue_index}",
                    "transcript_record_id": transcript.get("record_id"),
                }
            )

        comments = comments_by_item[shortcode].get("comments")
        if not isinstance(comments, list):
            raise ValueError(f"Instagram comment record {shortcode} lacks comments")
        for source_index, raw in enumerate(comments):
            if not isinstance(raw, Mapping):
                continue
            text = str(raw.get("text") or "").strip()
            if not text:
                continue
            comment_id = str(raw.get("comment_id") or f"source_order:{source_index}")
            evidence_id = _stable_id(
                "igce", normalized_creator, shortcode, comment_id, text
            )
            cluster_id = _stable_id(
                "igcc", _WS.sub(" ", text.casefold()).strip(), size=16
            )
            cluster_members.setdefault(cluster_id, []).append(evidence_id)
            cluster_text[cluster_id] = text
            comment_evidence.append(
                {
                    "evidence_id": evidence_id,
                    "creator_id": normalized_creator,
                    "source_item_id": shortcode,
                    "video_id": shortcode,
                    "comment_id": comment_id,
                    "text": text,
                    "source_order": source_index,
                    "source_pointer": f"instagram:{shortcode}:comment:{source_index}",
                    "duplicate_cluster_id": cluster_id,
                    "comment_likes": raw.get("like_count"),
                    "comment_like_rank_within_captured": None,
                    "temporal_alignment": "unproven",
                    "comment_attention_record_id": None,
                    "comment_record_id": comments_by_item[shortcode].get("record_id"),
                }
            )

    if not transcript_evidence:
        raise ValueError("INCOMPLETE_AUDIENCE_EVIDENCE: no Instagram transcript cues")
    if not comment_evidence:
        raise ValueError("INCOMPLETE_AUDIENCE_EVIDENCE: no Instagram comments")

    residuals = [*comment_residuals, *transcript_residuals]
    core: dict[str, Any] = {
        "schema_version": EVIDENCE_BUNDLE_SCHEMA_VERSION,
        "creator_id": normalized_creator,
        "profile_subject_kind": "platform_account",
        "profile_subject_id": profile_subject_id.strip(),
        "platform_scope": "instagram",
        "raw_anchor": primary_raw_anchor.strip(),
        "question": question.strip(),
        "evidence_cutoff": evidence_cutoff.strip(),
        "capture_scope": {
            "selected_source_item_ids": item_ids,
            "selected_video_ids": item_ids,
            "selected_item_count": len(item_ids),
            "item_selection_policy": "caller_selected_admitted_complete_reels_v1",
            "comment_selection_posture": "all_captured_top_level_comments_from_selected_reels",
            "limitations": [
                "not_platform_wide_comment_census",
                "selected_reels_may_be_ranked_or_truncated",
                "instagram_comment_engagement_temporal_alignment_unproven",
            ],
        },
        "transcript_evidence": sorted(
            transcript_evidence, key=lambda row: row["evidence_id"]
        ),
        "comment_evidence": sorted(comment_evidence, key=lambda row: row["evidence_id"]),
        "exact_duplicate_clusters": [
            {
                "cluster_id": cluster_id,
                "representative_text": cluster_text[cluster_id],
                "evidence_ids": sorted(evidence_ids),
                "multiplicity": len(evidence_ids),
            }
            for cluster_id, evidence_ids in sorted(cluster_members.items())
        ],
        "source_refs": {
            "primary_raw_anchor": primary_raw_anchor.strip(),
            "comment_record_ids": sorted(
                str(view.get("record_id")) for view in comments_by_item.values()
            ),
            "transcript_record_ids": sorted(
                str(view.get("record_id")) for view in transcripts_by_item.values()
            ),
            "compatibility_residuals": residuals,
        },
        "judgment_status": "not_evaluated",
    }
    bundle_hash = f"sha256:{hashlib.sha256(_canonical_bytes(core)).hexdigest()}"
    core["bundle_hash"] = bundle_hash
    core["bundle_id"] = _stable_id("caeb", primary_raw_anchor, bundle_hash)
    core["serialized_utf8_bytes"] = len(_canonical_bytes(core))
    return core


__all__ = [
    "EVIDENCE_BUNDLE_SCHEMA_VERSION",
    "build_instagram_creator_audience_evidence_bundle",
]