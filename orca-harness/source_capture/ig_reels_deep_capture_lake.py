"""Persist a one-render reel deep-capture into the Data Lake (silver, no-LLM).

Mirrors ``cleaning/transcript_product_lake.py``'s append-only record-set pattern,
adapted for the deep-capture: ONE render yields BOTH the audience comments and the
creator transcript, so they persist together as a single per-reel record-set keyed
on the reel shortcode:

- ``silver__capture__audience_comments`` : the ``AudienceComment`` evidence (durable)
- ``silver__capture__reel_transcript``   : the ASR transcript posture + ms-timed cues

with an all-or-nothing completion marker so a re-run can skip an already-persisted
reel. The TRANSIENT media URL is never persisted (it is signed + expiring); only a
redacted provenance note (CDN host + a used-flag) is kept.

No LLM. Capture-layer evidence only -- not Cleaning, not Judgment.
"""
from __future__ import annotations

import hashlib
import json
from urllib.parse import urlparse

from source_capture.ig_reels_deep_capture import ReelDeepCaptureResult

AUDIENCE_COMMENTS_LANE = "silver__capture__audience_comments"
REEL_TRANSCRIPT_LANE = "silver__capture__reel_transcript"
DEEP_CAPTURE_SET_LANE = "silver__capture__reel_deep_capture__set"


def deep_capture_record_id(result: ReelDeepCaptureResult) -> str:
    """Deterministic per (reel, comment set, transcript) so a re-run checks/skips the same record."""
    digest = hashlib.sha256()
    digest.update(result.reel_shortcode.encode("utf-8"))
    digest.update(result.transcript_posture.encode("utf-8"))
    for comment in result.comments:
        digest.update(b"\x00")
        digest.update(f"{comment.comment_id}:{comment.like_count}:{comment.text}".encode("utf-8"))
    for cue in result.transcript_cues:
        digest.update(b"\x01")
        digest.update(json.dumps(cue, sort_keys=True, ensure_ascii=False).encode("utf-8"))
    return f"deepcap_{result.reel_shortcode}__{digest.hexdigest()[:16]}.json"


def _media_provenance(media_url_used: str | None) -> dict:
    """Redacted handle provenance: the signed URL is transient, so keep only host + a used-flag."""
    if not media_url_used:
        return {"audio_handle_used": False, "media_host": None}
    host = (urlparse(media_url_used).hostname or "").lower() or None
    return {"audio_handle_used": True, "media_host": host}


def write_reel_deep_capture_into_lake(
    *,
    data_root,
    result: ReelDeepCaptureResult,
    generated_at: str,
    record_id: str | None = None,
) -> dict:
    """Append the silver deep-capture record-set (comments + transcript) for one reel.

    Re-appending the same ``record_id`` is refused by the lake (write-once); the caller
    should check ``is_record_set_complete`` first to skip an already-persisted reel.
    """
    rid = record_id or deep_capture_record_id(result)
    provenance = _media_provenance(result.media_url_used)
    comments_payload = {
        "reel_shortcode": result.reel_shortcode,
        "generated_at": generated_at,
        "comment_count": len(result.comments),
        "comments": [comment.model_dump(mode="json") for comment in result.comments],
        "media_provenance": provenance,
    }
    transcript_payload = {
        "reel_shortcode": result.reel_shortcode,
        "generated_at": generated_at,
        "transcript_posture": result.transcript_posture,
        "cue_count": len(result.transcript_cues),
        "cues": [dict(cue) for cue in result.transcript_cues],
        "media_provenance": provenance,
    }
    members = {
        # allow_nan=False: a non-finite float fails closed rather than writing invalid JSON.
        AUDIENCE_COMMENTS_LANE: (
            json.dumps(comments_payload, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
        ).encode("utf-8"),
        REEL_TRANSCRIPT_LANE: (
            json.dumps(transcript_payload, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
        ).encode("utf-8"),
    }
    return data_root.append_record_set(
        subtree="derived",
        raw_anchor=result.reel_shortcode,
        record_id=rid,
        members=members,
        completion_lane=DEEP_CAPTURE_SET_LANE,
    )
