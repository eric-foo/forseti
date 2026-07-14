"""Persist quote-backed audience evidence in Silver and profiles as analysis."""
from __future__ import annotations
import hashlib, json, re
from cleaning.tiktok_audience_evidence_extractor import AudienceExtractionResult, AudienceTranscript, RUBRIC_VERSION
from data_lake.canonical_json import canonical_record_bytes
from data_lake.silver_lineage import validate_silver_lineage
from data_lake.silver_record import (
    CONTENT_HASH_BASIS,
    SILVER_VAULT_RECORD_SCHEMA_VERSION,
    TEXT_OBSERVATION_SET_PAYLOAD_KIND,
    append_silver_record_set,
    silver_content_hash,
)
from schemas.tiktok_audience_evidence_models import TikTokAudienceProfile

AUDIENCE_EVIDENCE_LANE = "tiktok_audience_evidence_silver"
AUDIENCE_EVIDENCE_SET_LANE = "tiktok_audience_evidence_completion"
RECORD_SCHEMA_VERSION = "tiktok_audience_evidence_record_v1"
AUDIENCE_PROFILE_LANE = "tiktok_audience_profile_analysis"
AUDIENCE_PROFILE_SET_LANE = "tiktok_audience_profile_analysis_completion"
PROFILE_SCHEMA_VERSION = "tiktok_audience_profile_analysis_v0"
LEGACY_AUDIENCE_EVIDENCE_LANE = "silver__cleaning__tiktok_audience_evidence"
LEGACY_AUDIENCE_EVIDENCE_SET_LANE = "silver__cleaning__tiktok_audience_evidence__set"
LEGACY_AUDIENCE_PROFILE_LANE = "silver__cleaning__tiktok_audience_profile"
LEGACY_AUDIENCE_PROFILE_SET_LANE = "silver__cleaning__tiktok_audience_profile__set"
AUDIENCE_POLICY_FINGERPRINT = hashlib.sha256(RUBRIC_VERSION.encode("utf-8")).hexdigest()


def audience_record_id(item: AudienceTranscript, model: str) -> str:
    token = re.sub(r"[^A-Za-z0-9_-]", "-", model)[:40]
    digest = hashlib.sha256(
        f"{item.creator_id}\0{item.transcript.transcript_source_key}\0{item.transcript.joined_text}\0{model}\0{RUBRIC_VERSION}".encode()
    ).hexdigest()[:18]
    return f"audience_{token}__{digest}.json"


def write_result(*, data_root, item: AudienceTranscript, result: AudienceExtractionResult, model: str):
    transcript = item.transcript
    rid = audience_record_id(item, model)
    if transcript.source_lineage is None:
        raise ValueError("TikTok audience evidence requires transcript lineage")
    lineage = validate_silver_lineage(transcript.source_lineage)
    rows = []
    for evidence in result.evidence:
        body = evidence.model_dump(mode="json")
        quote = body["source_pointer"]
        rows.append(
            {
                "row_id": body["evidence_id"],
                "text_artifact_type": "transcript_quote",
                "text_value": quote,
                "text_ref": None,
                "text_hash": f"sha256:{hashlib.sha256(quote.encode('utf-8')).hexdigest()}",
                "text_posture": {"kind": "observed", "reason_code": None, "reason_detail": None},
                "coverage_window": {"start": None, "end": None},
                "source_span": None,
                "audience_evidence": body,
            }
        )
    record = {
        "record_id": rid,
        "raw_anchor": transcript.transcript_anchor,
        "lane_namespace": AUDIENCE_EVIDENCE_LANE,
        "schema_version": SILVER_VAULT_RECORD_SCHEMA_VERSION,
        "content_hash": "",
        "content_hash_basis": CONTENT_HASH_BASIS,
        "record_kind": "observation",
        "payload_kind": TEXT_OBSERVATION_SET_PAYLOAD_KIND,
        "producer_row_kind": "tiktok_transcript_audience_evidence",
        "record_schema_version": RECORD_SCHEMA_VERSION,
        "source_family": "social_media",
        **lineage.to_record_fields(),
        "payload": {
            "observation": {
                "subject": {
                    "ref_type": "entity_key",
                    "ref": {
                        "namespace": "tiktok",
                        "kind": "public_content_object",
                        "native_id": transcript.video_id,
                    },
                },
                "observation_set_kind": "tiktok_transcript_audience_evidence",
                "policy_version": RUBRIC_VERSION,
                "policy_fingerprint_sha256": AUDIENCE_POLICY_FINGERPRINT,
                "row_count": len(rows),
                "rows": rows,
            }
        },
        "provenance": {
            "creator_id": item.creator_id,
            "transcript_source_key": transcript.transcript_source_key,
            "source_route": transcript.source_route,
            "model": model,
            "rubric_version": RUBRIC_VERSION,
            "rejected_count": len(result.rejected),
        },
        "non_claims": [
            "not actual audience measurement",
            "not demographics",
            "not buyer or conversion proof",
            "not a creator recommendation",
        ],
    }
    record["content_hash"] = f"sha256:{silver_content_hash(record)}"
    return append_silver_record_set(
        data_root, raw_anchor=transcript.transcript_anchor, record_id=rid,
        records={AUDIENCE_EVIDENCE_LANE: record},
        completion_lane=AUDIENCE_EVIDENCE_SET_LANE,
    )


def profile_record_id(creator_id: str, model: str, evidence_record_ids: list[str]) -> str:
    token = re.sub(r"[^A-Za-z0-9_-]", "-", model)[:32]
    digest = hashlib.sha256((creator_id + "\0" + "\0".join(sorted(evidence_record_ids)) + "\0" + model + "\0" + RUBRIC_VERSION).encode()).hexdigest()[:18]
    return f"audience_profile_{token}__{digest}.json"


def write_profile(*, data_root, raw_anchor: str, profile: TikTokAudienceProfile, model: str,
                  evidence_records: list[tuple[str, str]]) -> dict[str, object]:
    ids = [record_id for record_id, _sha in evidence_records]
    rid = profile_record_id(profile.creator_id, model, ids)
    payload = {
        "schema_version": PROFILE_SCHEMA_VERSION,
        "record_id": rid,
        "role_posture": "non_authoritative_analysis",
        "creator_id": profile.creator_id,
        "model": model,
        "rubric_version": RUBRIC_VERSION,
        "policy_fingerprint_sha256": AUDIENCE_POLICY_FINGERPRINT,
        "profile": profile.model_dump(mode="json"),
        "source_silver_evidence_refs": [
            {
                "raw_anchor": raw_anchor,
                "lane_namespace": AUDIENCE_EVIDENCE_LANE,
                "record_id": record_id,
                "sha256": sha,
                "hash_basis": "derived_record_bytes",
            }
            for record_id, sha in evidence_records
        ],
        "non_claims": [
            "not Silver Authority",
            "not actual audience measurement",
            "not demographics",
            "not a creator recommendation",
        ],
    }
    return data_root.append_record_set(subtree="derived", raw_anchor=raw_anchor, record_id=rid,
        members={AUDIENCE_PROFILE_LANE: canonical_record_bytes(payload)},
        completion_lane=AUDIENCE_PROFILE_SET_LANE)


__all__ = ["AUDIENCE_EVIDENCE_LANE", "AUDIENCE_EVIDENCE_SET_LANE", "AUDIENCE_PROFILE_LANE", "AUDIENCE_PROFILE_SET_LANE", "RECORD_SCHEMA_VERSION", "PROFILE_SCHEMA_VERSION", "audience_record_id", "profile_record_id", "write_profile", "write_result"]
