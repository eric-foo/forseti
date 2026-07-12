"""Persist per-transcript TikTok audience evidence as lineage-closed record sets."""
from __future__ import annotations
import hashlib, json, re
from cleaning.tiktok_audience_evidence_extractor import AudienceExtractionResult, AudienceTranscript, RUBRIC_VERSION
from data_lake.silver_lineage import validate_silver_lineage

AUDIENCE_EVIDENCE_LANE = "silver__cleaning__tiktok_audience_evidence"
AUDIENCE_EVIDENCE_SET_LANE = "silver__cleaning__tiktok_audience_evidence__set"
RECORD_SCHEMA_VERSION = "tiktok_audience_evidence_record_v0"


def audience_record_id(item: AudienceTranscript, model: str) -> str:
    token = re.sub(r"[^A-Za-z0-9_-]", "-", model)[:40]
    digest = hashlib.sha256(
        f"{item.creator_id}\0{item.transcript.transcript_source_key}\0{item.transcript.joined_text}\0{model}\0{RUBRIC_VERSION}".encode()
    ).hexdigest()[:18]
    return f"audience_{token}__{digest}.json"


def write_result(*, data_root, item: AudienceTranscript, result: AudienceExtractionResult, model: str):
    transcript = item.transcript
    rid = audience_record_id(item, model)
    payload = {
        "record_schema_version": RECORD_SCHEMA_VERSION,
        "record_id": rid,
        "creator_id": item.creator_id,
        "video_id": transcript.video_id,
        "transcript_anchor": transcript.transcript_anchor,
        "transcript_source_key": transcript.transcript_source_key,
        "source_route": transcript.source_route,
        "model": model,
        "rubric_version": RUBRIC_VERSION,
        "actual_audience": "not_estimated",
        "evidence": [row.model_dump(mode="json") for row in result.evidence],
        "rejected": result.rejected,
        "evidence_count": len(result.evidence),
        "rejected_count": len(result.rejected),
    }
    if transcript.source_lineage is None:
        raise ValueError("TikTok audience evidence requires transcript lineage")
    payload.update(validate_silver_lineage(transcript.source_lineage).to_record_fields())
    return data_root.append_record_set(
        subtree="derived", raw_anchor=transcript.transcript_anchor, record_id=rid,
        members={AUDIENCE_EVIDENCE_LANE: (json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()},
        completion_lane=AUDIENCE_EVIDENCE_SET_LANE,
    )


__all__ = ["AUDIENCE_EVIDENCE_LANE", "AUDIENCE_EVIDENCE_SET_LANE", "RECORD_SCHEMA_VERSION", "audience_record_id", "write_result"]
