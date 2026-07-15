"""Packet-first persistence for one-render Instagram Reel deep capture.

The rendered comment substrate and downloaded audio bytes are committed as a
``SourceCapturePacket`` before any Silver record is admitted.  Audience comments
and transcript cues then use the official ``silver_vault_record_v0`` envelope and
point to the exact preserved packet file/hash that proves that evidence leg.

Historical shortcode-anchored grammar-B records remain on disk for audit.  This
writer never wraps or rewrites them, and never persists the signed/expiring media
URL used to obtain the audio bytes.
"""
from __future__ import annotations

from collections.abc import Iterator, Mapping
from dataclasses import dataclass
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlparse

from data_lake.silver_lineage import (
    SOURCE_BACKED_COMPLETE_STATUS,
    SilverAnchor,
    SilverLineage,
    SilverRawRef,
    SilverSourceObject,
    silver_record_source_backed_status,
)
from data_lake.silver_record import (
    CONTENT_HASH_BASIS,
    SILVER_VAULT_RECORD_SCHEMA_VERSION,
    TEXT_OBSERVATION_SET_PAYLOAD_KIND,
    append_silver_record_set,
    silver_content_hash,
    validate_silver_vault_record,
)
from source_capture import (
    CaptureModeCategory,
    PacketTiming,
    SourceCaptureSlice,
    known_fact,
    not_applicable,
    not_attempted,
    unknown_with_reason,
)
from source_capture.ig_reels_deep_capture import ReelDeepCaptureResult
from source_capture.ig_reels_comments import parse_comments_from_rendered_dom
from source_capture.packet_assembly import stage_and_write_packet, staged_file_id_map

AUDIENCE_COMMENTS_LANE = "silver__capture__audience_comments"
REEL_TRANSCRIPT_LANE = "silver__capture__reel_transcript"
DEEP_CAPTURE_SET_LANE = "silver__capture__reel_deep_capture__set"

DEEP_CAPTURE_PACKET_SURFACE = "ig_reels_deep_capture"
DEEP_CAPTURE_PRODUCER_SCHEMA_VERSION = "ig_reels_deep_capture_silver_v1"
COMMENTS_POLICY_VERSION = "ig_rendered_comment_substrate_v1"
TRANSCRIPT_POLICY_VERSION = "ig_rendered_audio_asr_cues_v1"
_PRODUCER_ID = "forseti-harness.source_capture.ig_reels_deep_capture_lake"
_COMMENT_FILE = "rendered_comment_substrate.jsonl"
_METADATA_FILE = "capture_metadata.json"
_SAFE_EXT = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,15}")
_SUCCESS_POSTURES = frozenset({"transcribed"})


@dataclass(frozen=True)
class DeepCaptureLakeWrite(Mapping[str, Path]):
    packet_id: str
    record_id: str
    paths: Mapping[str, Path]
    excluded_legs: tuple[str, ...] = ()

    def __getitem__(self, key: str) -> Path:
        return self.paths[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self.paths)

    def __len__(self) -> int:
        return len(self.paths)


def deep_capture_record_id(result: ReelDeepCaptureResult) -> str:
    """Deterministic id over derived facts and their exact retained evidence."""
    digest = hashlib.sha256()
    digest.update(result.reel_shortcode.encode("utf-8"))
    digest.update(result.transcript_posture.encode("utf-8"))
    digest.update(result.comment_substrate or b"")
    digest.update(result.audio_bytes or b"")
    for comment in result.comments:
        digest.update(b"\x00")
        digest.update(
            json.dumps(
                comment.model_dump(mode="json"),
                sort_keys=True,
                ensure_ascii=False,
                separators=(",", ":"),
            ).encode("utf-8")
        )
    for cue in result.transcript_cues:
        digest.update(b"\x01")
        digest.update(json.dumps(cue, sort_keys=True, ensure_ascii=False).encode("utf-8"))
    return f"deepcap_{result.reel_shortcode}__{digest.hexdigest()[:16]}.json"


def _media_provenance(media_url_used: str | None) -> dict[str, object]:
    if not media_url_used:
        return {"audio_handle_used": False, "media_host": None}
    host = (urlparse(media_url_used).hostname or "").lower() or None
    return {"audio_handle_used": True, "media_host": host}


def _policy_fingerprint(policy_version: str) -> str:
    return hashlib.sha256(
        json.dumps(
            {"policy_version": policy_version, "producer_schema_version": DEEP_CAPTURE_PRODUCER_SCHEMA_VERSION},
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()


def _safe_audio_ext(value: str | None) -> str:
    ext = (value or "bin").lstrip(".").lower()
    return ext if _SAFE_EXT.fullmatch(ext) else "bin"


def current_deep_capture_record(
    data_root,
    *,
    record: Mapping[str, object],
    raw_anchor: str,
    lane: str,
    record_id: str,
) -> bool:
    """True only for a valid envelope whose exact packet/file/hash resolves."""
    try:
        validate_silver_vault_record(record)
    except (TypeError, ValueError):
        return False
    if (
        record.get("raw_anchor") != raw_anchor
        or record.get("lane_namespace") != lane
        or record.get("record_id") != record_id
        or silver_record_source_backed_status(record) != SOURCE_BACKED_COMPLETE_STATUS
    ):
        return False
    try:
        loaded = data_root.load_raw_packet(raw_anchor)
    except Exception:  # noqa: BLE001 - read-side eligibility is fail-closed
        return False
    preserved = {
        item.get("file_id"): item
        for item in loaded.manifest.get("preserved_files", [])
        if isinstance(item, Mapping)
    }
    raw_refs = record.get("raw_refs")
    if not isinstance(raw_refs, list) or not raw_refs:
        return False
    for ref in raw_refs:
        if not isinstance(ref, Mapping) or ref.get("packet_id") != raw_anchor:
            return False
        item = preserved.get(ref.get("file_id"))
        if not isinstance(item, Mapping):
            return False
        if any(
            ref.get(field) != item.get(field)
            for field in ("relative_packet_path", "sha256", "hash_basis")
        ):
            return False
    return True


def deep_capture_shortcode(record: Mapping[str, object]) -> str | None:
    payload = record.get("payload")
    observation = payload.get("observation") if isinstance(payload, Mapping) else None
    subject = observation.get("subject") if isinstance(observation, Mapping) else None
    ref = subject.get("ref") if isinstance(subject, Mapping) else None
    value = ref.get("native_id") if isinstance(ref, Mapping) else None
    return value.strip() if isinstance(value, str) and value.strip() else None


def comments_compatibility_view(record: Mapping[str, object]) -> dict[str, object]:
    payload = record.get("payload")
    observation = payload.get("observation") if isinstance(payload, Mapping) else {}
    rows = observation.get("rows") if isinstance(observation, Mapping) else []
    comments = [row.get("comment") for row in rows if isinstance(row, Mapping) and isinstance(row.get("comment"), Mapping)]
    return {
        "record_id": record.get("record_id"),
        "reel_shortcode": deep_capture_shortcode(record),
        "generated_at": record.get("captured_at"),
        "comment_count": len(comments),
        "comments": comments,
        "source_backed_status": SOURCE_BACKED_COMPLETE_STATUS,
    }


def transcript_compatibility_view(record: Mapping[str, object]) -> dict[str, object]:
    payload = record.get("payload")
    observation = payload.get("observation") if isinstance(payload, Mapping) else {}
    rows = observation.get("rows") if isinstance(observation, Mapping) else []
    cues: list[dict[str, object]] = []
    for row in rows if isinstance(rows, list) else []:
        if not isinstance(row, Mapping) or not isinstance(row.get("text_value"), str):
            continue
        span = row.get("source_span") if isinstance(row.get("source_span"), Mapping) else {}
        cues.append({"start_ms": span.get("start_ms"), "end_ms": span.get("end_ms"), "text": row["text_value"]})
    return {
        "record_id": record.get("record_id"),
        "transcript_anchor": record.get("raw_anchor"),
        "reel_shortcode": deep_capture_shortcode(record),
        "generated_at": record.get("captured_at"),
        "transcript_posture": "transcribed",
        "cue_count": len(cues),
        "cues": cues,
        "source_backed_status": SOURCE_BACKED_COMPLETE_STATUS,
    }


def _text_row(*, row_id: str, text: str, artifact_type: str, extra: Mapping[str, object]) -> dict:
    return {
        "row_id": row_id,
        "text_artifact_type": artifact_type,
        "text_value": text,
        "text_ref": None,
        "text_hash": f"sha256:{hashlib.sha256(text.encode('utf-8')).hexdigest()}",
        "text_posture": {"kind": "observed", "reason_code": None, "reason_detail": None},
        **dict(extra),
    }


def _record(
    *,
    packet,
    file_id: str,
    record_id: str,
    lane: str,
    generated_at: str,
    shortcode: str,
    producer_row_kind: str,
    observation_set_kind: str,
    policy_version: str,
    rows: list[dict],
    provenance: Mapping[str, object],
) -> dict:
    preserved = next(item for item in packet.preserved_files if item.file_id == file_id)
    lineage = SilverLineage(
        producer_id=_PRODUCER_ID,
        producer_schema_version=DEEP_CAPTURE_PRODUCER_SCHEMA_VERSION,
        source_surface=packet.source_surface,
        source_object=SilverSourceObject(
            namespace="instagram",
            kind="platform_content",
            native_id=shortcode,
            source_url=f"https://www.instagram.com/reel/{shortcode}/",
        ),
        observed_at=generated_at,
        captured_at=generated_at,
        raw_refs=[
            SilverRawRef(
                packet_id=packet.packet_id,
                slice_id="slice_01",
                file_id=file_id,
                relative_packet_path=preserved.relative_packet_path,
                sha256=preserved.sha256,
                hash_basis=preserved.hash_basis,
                anchor=SilverAnchor(kind="file", value=preserved.relative_packet_path),
                relation="observed_from",
            )
        ],
    )
    record = {
        "record_id": record_id,
        "raw_anchor": packet.packet_id,
        "lane_namespace": lane,
        "schema_version": SILVER_VAULT_RECORD_SCHEMA_VERSION,
        "content_hash": "",
        "content_hash_basis": CONTENT_HASH_BASIS,
        "record_kind": "observation",
        "payload_kind": TEXT_OBSERVATION_SET_PAYLOAD_KIND,
        "producer_row_kind": producer_row_kind,
        "record_schema_version": DEEP_CAPTURE_PRODUCER_SCHEMA_VERSION,
        "source_family": packet.source_family,
        **lineage.to_record_fields(),
        "payload": {
            "observation": {
                "subject": {
                    "ref_type": "entity_key",
                    "ref": {
                        "namespace": "instagram",
                        "kind": "platform_content",
                        "native_id": shortcode,
                    },
                },
                "observation_set_kind": observation_set_kind,
                "policy_version": policy_version,
                "policy_fingerprint_sha256": _policy_fingerprint(policy_version),
                "row_count": len(rows),
                "rows": rows,
            }
        },
        "provenance": dict(provenance),
        "non_claims": [
            "not Cleaning",
            "not Judgment",
            "not a complete comment census",
            "ASR text is machine-generated when the transcript leg is present",
        ],
    }
    record["content_hash"] = f"sha256:{silver_content_hash(record)}"
    return record


def write_reel_deep_capture_into_lake(
    *,
    data_root,
    result: ReelDeepCaptureResult,
    generated_at: str,
    record_id: str | None = None,
) -> DeepCaptureLakeWrite:
    """Commit exact evidence, then append only the Silver legs it supports."""
    if result.comments and not result.comment_substrate:
        raise ValueError("audience comments cannot be admitted without retained rendered comment substrate")
    if result.comment_substrate:
        reparsed = tuple(
            parse_comments_from_rendered_dom(
                result.comment_substrate.decode("utf-8"),
                shortcode=result.reel_shortcode,
            )
        )
        if reparsed != result.comments:
            raise ValueError("audience comments do not match the exact retained rendered comment substrate")

    comment_admissible = bool(result.comments and result.comment_substrate)
    transcript_admissible = bool(
        result.transcript_posture in _SUCCESS_POSTURES
        and result.transcript_cues
        and result.audio_bytes
        and any(str(cue.get("text") or "").strip() for cue in result.transcript_cues)
    )
    if not comment_admissible and not transcript_admissible:
        raise ValueError("deep capture produced no source-backed comment or transcript evidence to admit")

    audio_name = f"reel_audio.{_safe_audio_ext(result.audio_ext)}"
    metadata = {
        "platform": "instagram",
        "platform_shortcode": result.reel_shortcode,
        "canonical_url": f"https://www.instagram.com/reel/{result.reel_shortcode}/",
        "capture_timestamp": generated_at,
        "comment_count": len(result.comments),
        "transcript_posture": result.transcript_posture,
        "cue_count": len(result.transcript_cues),
        "media_provenance": _media_provenance(result.media_url_used),
    }
    artifacts: list[tuple[str, bytes]] = []
    if comment_admissible:
        artifacts.append((_COMMENT_FILE, result.comment_substrate or b""))
    if result.audio_bytes:
        artifacts.append((audio_name, result.audio_bytes))
    artifacts.append((_METADATA_FILE, (json.dumps(metadata, sort_keys=True, indent=2) + "\n").encode("utf-8")))
    file_ids = staged_file_id_map(artifacts)

    canonical = f"https://www.instagram.com/reel/{result.reel_shortcode}/"
    timing = PacketTiming(
        source_publication_or_event=not_attempted("publish timing not fetched in deep capture"),
        source_edit_or_version=not_applicable("Instagram Reel render exposes no edit version"),
        capture_time=known_fact(generated_at),
        recapture_time=not_applicable("no prior deep-capture packet supplied"),
        cutoff_posture=not_applicable("cutoff posture does not apply"),
    )
    media_posture = (
        known_fact(f"downloaded audio bytes preserved ({len(result.audio_bytes or b'')} bytes)")
        if result.audio_bytes
        else unknown_with_reason(f"audio bytes not preserved: {result.transcript_posture}")
    )
    limitations = [] if result.audio_bytes else [f"audio leg not preserved: {result.transcript_posture}"]
    packet_result = stage_and_write_packet(
        data_root=data_root,
        staged_artifacts=artifacts,
        source_slices=[
            SourceCaptureSlice(
                slice_id="slice_01",
                locator=known_fact(canonical),
                timing=timing,
                access_posture=known_fact("public Reel rendered once in the browser-snapshot route"),
                archive_history_posture=not_attempted("deep capture does not query archives"),
                media_modality_posture=media_posture,
                re_capture_relationship=not_applicable("no prior deep-capture packet supplied"),
                preserved_file_ids=list(file_ids.values()),
                limitations=list(limitations),
            )
        ],
        source_family="instagram_creator",
        source_surface=DEEP_CAPTURE_PACKET_SURFACE,
        source_locator=known_fact(canonical),
        decision_question="Capture source-backed Instagram Reel audience comments and transcript evidence.",
        capture_context="one rendered Reel; exact comment objects plus downloaded audio bytes when available",
        actor_audience_context=not_applicable("public anonymous capture; no actor/audience inference"),
        capture_mode=CaptureModeCategory.AUTOMATED_EXTRACTION,
        operator_category="ig_reels_deep_capture_cli_operator",
        session_identity=None,
        visible_mode_changes=[],
        source_publication_or_event=timing.source_publication_or_event,
        source_edit_or_version=timing.source_edit_or_version,
        cutoff_posture=timing.cutoff_posture,
        recapture_time=timing.recapture_time,
        access_posture=known_fact("public Reel rendered once in the browser-snapshot route"),
        archive_history_posture=not_attempted("deep capture does not query archives"),
        media_modality_posture=media_posture,
        re_capture_relationship=not_applicable("no prior deep-capture packet supplied"),
        warnings=[],
        limitations=list(limitations),
        receipt_summary=(
            f"Instagram Reel deep-capture packet for {result.reel_shortcode}: "
            f"{len(result.comments)} retained comments; audio_bytes={len(result.audio_bytes or b'')}."
        ),
        receipt_non_claims=[
            "signed or expiring media URLs are not preserved",
            "not a complete comment census",
            "not Cleaning or Judgment",
        ],
    )
    packet = packet_result.packet
    rid = record_id or deep_capture_record_id(result)
    records: dict[str, dict] = {}
    excluded: list[str] = []

    if comment_admissible:
        comment_rows = [
            _text_row(
                row_id=comment.comment_id,
                text=comment.text,
                artifact_type="instagram_audience_comment",
                extra={"comment": comment.model_dump(mode="json")},
            )
            for comment in result.comments
        ]
        records[AUDIENCE_COMMENTS_LANE] = _record(
            packet=packet,
            file_id=file_ids[_COMMENT_FILE],
            record_id=rid,
            lane=AUDIENCE_COMMENTS_LANE,
            generated_at=generated_at,
            shortcode=result.reel_shortcode,
            producer_row_kind="instagram_audience_comment",
            observation_set_kind="instagram_reel_audience_comments",
            policy_version=COMMENTS_POLICY_VERSION,
            rows=comment_rows,
            provenance={"reel_shortcode": result.reel_shortcode, "comment_count": len(comment_rows)},
        )
    else:
        excluded.append("comments_not_admitted:no_retained_comment_substrate")

    if transcript_admissible:
        transcript_rows = [
            _text_row(
                row_id=f"cue_{index:06d}",
                text=str(cue.get("text") or ""),
                artifact_type="instagram_reel_asr_cue",
                extra={
                    "source_span": {
                        "start_ms": cue.get("start_ms"),
                        "end_ms": cue.get("end_ms"),
                    }
                },
            )
            for index, cue in enumerate(result.transcript_cues, start=1)
            if str(cue.get("text") or "")
        ]
        if transcript_rows:
            records[REEL_TRANSCRIPT_LANE] = _record(
                packet=packet,
                file_id=file_ids[audio_name],
                record_id=rid,
                lane=REEL_TRANSCRIPT_LANE,
                generated_at=generated_at,
                shortcode=result.reel_shortcode,
                producer_row_kind="instagram_reel_asr_cue",
                observation_set_kind="instagram_reel_asr_transcript",
                policy_version=TRANSCRIPT_POLICY_VERSION,
                rows=transcript_rows,
                provenance={
                    "reel_shortcode": result.reel_shortcode,
                    "transcript_posture": "transcribed",
                    "cue_count": len(transcript_rows),
                    "media_provenance": _media_provenance(result.media_url_used),
                },
            )
        else:
            excluded.append("transcript_not_admitted:no_nonempty_cues")
    else:
        excluded.append(f"transcript_not_admitted:{result.transcript_posture}:audio_bytes_required")

    if not records:
        raise ValueError("packet committed but no Silver record remained admissible")
    paths = append_silver_record_set(
        data_root,
        raw_anchor=packet.packet_id,
        record_id=rid,
        records=records,
        completion_lane=DEEP_CAPTURE_SET_LANE,
    )
    return DeepCaptureLakeWrite(packet.packet_id, rid, paths, tuple(excluded))


__all__ = [
    "AUDIENCE_COMMENTS_LANE",
    "COMMENTS_POLICY_VERSION",
    "comments_compatibility_view",
    "current_deep_capture_record",
    "deep_capture_shortcode",
    "DEEP_CAPTURE_PACKET_SURFACE",
    "DEEP_CAPTURE_SET_LANE",
    "DeepCaptureLakeWrite",
    "REEL_TRANSCRIPT_LANE",
    "TRANSCRIPT_POLICY_VERSION",
    "transcript_compatibility_view",
    "deep_capture_record_id",
    "write_reel_deep_capture_into_lake",
]
