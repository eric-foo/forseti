"""Batched, daemon-ready TikTok subtitle audience-evidence runner."""
from __future__ import annotations
import json, sys
from pathlib import Path
from typing import Any, Mapping

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cleaning.tiktok_audience_evidence_extractor import AudienceTranscript, RUBRIC_VERSION, extract_batch, pack_transcripts
from cleaning.tiktok_audience_evidence_lake import AUDIENCE_EVIDENCE_LANE, AUDIENCE_EVIDENCE_SET_LANE, audience_record_id, write_result
from data_lake.consumption import append_ack, pickup, reconcile_availability_per_packet
from runners.run_tiktok_product_extract import _transcripts_for_packet
from source_capture.tiktok.batch_packet import TIKTOK_BATCH_CAPTURE_JSON_NAME

_ACK_NAMESPACE = AUDIENCE_EVIDENCE_LANE


def _obligation(data_root, packet_id: str, model: str) -> dict:
    availability = data_root.read_availability(packet_id) or {}
    return {"obligation_schema": 1, "consumer": "tiktok_audience_evidence", "model": model,
            "rubric_version": RUBRIC_VERSION, "manifest_sha256": str(availability.get("manifest_sha256") or "missing")}


def _creator_id(data_root, packet_id: str) -> str:
    loaded = data_root.load_raw_packet(packet_id)
    matches = [p for p in loaded.manifest.get("preserved_files", []) if isinstance(p, Mapping)
               and str(p.get("relative_packet_path") or "").endswith(TIKTOK_BATCH_CAPTURE_JSON_NAME)]
    if len(matches) != 1:
        raise ValueError(f"packet {packet_id} requires one TikTok batch JSON")
    body = loaded.bodies.get(str(matches[0].get("file_id") or ""))
    payload = json.loads(body.decode("utf-8")) if body is not None else None
    creator = str(payload.get("creator_handle") or "").strip().lstrip("@") if isinstance(payload, dict) else ""
    if not creator:
        raise ValueError(f"packet {packet_id} lacks creator_handle")
    return f"tiktok:@{creator.casefold()}"


def _audience_item(creator: str, transcript) -> AudienceTranscript:
    lineage = transcript.source_lineage
    if lineage is None:
        raise ValueError("TikTok transcript lacks lineage")
    transcript.source_lineage = lineage.model_copy(update={
        "producer_id": "cleaning.tiktok_audience_evidence_extractor",
        "producer_schema_version": RUBRIC_VERSION,
    })
    return AudienceTranscript(creator_id=creator, transcript=transcript)


def run_extraction(*, data_root, transport, provider, model: str, api_key: str,
                   max_tokens: int = 4096, max_input_chars: int = 48_000) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    results.extend(reconcile_availability_per_packet(data_root))
    pickup_items = list(pickup(data_root, ack_namespace=_ACK_NAMESPACE,
                               obligation_fn=lambda pid: _obligation(data_root, pid, model),
                               source_family="tiktok", reconcile=False))
    states = {item.raw_anchor: {"item": item, "complete": True, "evidence": []} for item in pickup_items}
    pending: list[AudienceTranscript] = []
    for pickup_item in pickup_items:
        packet_id = pickup_item.raw_anchor
        state = states[packet_id]
        try:
            creator = _creator_id(data_root, packet_id)
            transcripts, failures = _transcripts_for_packet(data_root, packet_id)
            if failures:
                results.extend(failures)
                state["complete"] = False
            for transcript in transcripts:
                item = _audience_item(creator, transcript)
                rid = audience_record_id(item, model)
                marker = {"kind": "record_set_complete", "completion_lane": AUDIENCE_EVIDENCE_SET_LANE,
                          "record_id": rid, "video_id": transcript.video_id}
                if data_root.is_record_set_complete(subtree="derived", raw_anchor=packet_id,
                                                    record_id=rid, completion_lane=AUDIENCE_EVIDENCE_SET_LANE):
                    results.append({"packet_id": packet_id, "creator_id": creator, "video_id": transcript.video_id, "status": "skipped_done"})
                    state["evidence"].append(marker)
                elif data_root.record_path(subtree="derived", raw_anchor=packet_id,
                                           lane=AUDIENCE_EVIDENCE_LANE, record_id=rid).exists():
                    results.append({"packet_id": packet_id, "creator_id": creator, "video_id": transcript.video_id, "status": "partial_needs_cleanup"})
                    state["complete"] = False
                else:
                    pending.append(item)
        except Exception as exc:
            results.append({"packet_id": packet_id, "status": "discovery_failed", "error": f"{type(exc).__name__}: {exc}"[:250]})
            state["complete"] = False

    def process(batch: list[AudienceTranscript]) -> None:
        try:
            extracted = extract_batch(items=batch, transport=transport, provider=provider, model=model,
                                      api_key=api_key, max_tokens=max_tokens)
        except Exception as exc:
            if len(batch) > 1:
                midpoint = len(batch) // 2
                process(batch[:midpoint]); process(batch[midpoint:])
                return
            item = batch[0]
            states[item.transcript.transcript_anchor]["complete"] = False
            results.append({"packet_id": item.transcript.transcript_anchor, "creator_id": item.creator_id,
                            "video_id": item.transcript.video_id, "status": "failed",
                            "error": f"{type(exc).__name__}: {exc}"[:250]})
            return
        for item in batch:
            key = (item.creator_id, item.transcript.video_id)
            state = states[item.transcript.transcript_anchor]
            try:
                rid = audience_record_id(item, model)
                paths = write_result(data_root=data_root, item=item, result=extracted[key], model=model)
                state["evidence"].append({"kind": "record_set_complete", "completion_lane": AUDIENCE_EVIDENCE_SET_LANE,
                                          "record_id": rid, "video_id": item.transcript.video_id})
                results.append({"packet_id": item.transcript.transcript_anchor, "creator_id": item.creator_id,
                                "video_id": item.transcript.video_id, "status": "extracted",
                                "evidence_count": len(extracted[key].evidence), "path": str(next(iter(paths.values())))})
            except Exception as exc:
                state["complete"] = False
                results.append({"packet_id": item.transcript.transcript_anchor, "creator_id": item.creator_id,
                                "video_id": item.transcript.video_id, "status": "failed",
                                "error": f"{type(exc).__name__}: {exc}"[:250]})

    for batch in pack_transcripts(pending, max_input_chars=max_input_chars):
        process(batch)

    for packet_id, state in states.items():
        if state["complete"]:
            append_ack(data_root, raw_anchor=packet_id, ack_namespace=_ACK_NAMESPACE,
                       obligation=state["item"].obligation,
                       evidence=state["evidence"] or [{"kind": "no_extractable_transcripts"}])
    return results


__all__ = ["run_extraction"]
