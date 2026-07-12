"""Batched, daemon-ready TikTok subtitle audience-evidence runner."""
from __future__ import annotations
import hashlib, json, sys
from pathlib import Path
from typing import Any, Mapping

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cleaning.tiktok_audience_evidence_extractor import AudienceTranscript, RUBRIC_VERSION, extract_batch, pack_transcripts, synthesize_profiles
from cleaning.tiktok_audience_evidence_lake import (
    AUDIENCE_EVIDENCE_LANE, AUDIENCE_EVIDENCE_SET_LANE, AUDIENCE_PROFILE_LANE, AUDIENCE_PROFILE_SET_LANE,
    audience_record_id, profile_record_id, write_profile, write_result,
)
from data_lake.consumption import append_ack, pickup, reconcile_availability_per_packet
from runners.run_tiktok_product_extract import _transcripts_for_packet
from source_capture.tiktok.batch_packet import TIKTOK_BATCH_CAPTURE_JSON_NAME
from schemas.tiktok_audience_evidence_models import TikTokAudienceEvidence

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
    states = {item.raw_anchor: {"item": item, "complete": True, "evidence": [], "rows": [], "record_refs": [], "creator": None} for item in pickup_items}
    pending: list[AudienceTranscript] = []
    for pickup_item in pickup_items:
        packet_id = pickup_item.raw_anchor
        state = states[packet_id]
        try:
            transcripts, failures = _transcripts_for_packet(data_root, packet_id)
            if not transcripts and not failures:
                # Not a TikTok batch-admission packet (e.g. a single-video SCI packet
                # sharing source_family="tiktok"), or a batch packet with zero videos.
                # Nothing for this consumer to do; leave state at its default
                # complete=True/empty-evidence so the packet acks as
                # no_extractable_transcripts below instead of re-surfacing as a
                # permanent discovery_failed retry on every future run.
                continue
            creator = _creator_id(data_root, packet_id)
            state["creator"] = creator
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
                    record_path = data_root.record_path(subtree="derived", raw_anchor=packet_id, lane=AUDIENCE_EVIDENCE_LANE, record_id=rid)
                    body = record_path.read_bytes()
                    stored = json.loads(body.decode("utf-8"))
                    state["rows"].extend(TikTokAudienceEvidence.model_validate(row) for row in stored.get("evidence", []))
                    state["record_refs"].append((rid, hashlib.sha256(body).hexdigest()))
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
                member_path = next(path for lane, path in paths.items() if lane == AUDIENCE_EVIDENCE_LANE)
                member_body = member_path.read_bytes()
                state["rows"].extend(extracted[key].evidence)
                state["record_refs"].append((rid, hashlib.sha256(member_body).hexdigest()))
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

    # Profile synthesis is per capture packet, but packets with distinct creators share
    # one call. Repeated captures of the same creator are placed in separate call groups.
    profile_groups: list[list[tuple[str, dict[str, Any]]]] = []
    for packet_id, state in states.items():
        if not state["complete"] or not state["rows"]:
            continue
        placed = False
        for group in profile_groups:
            if all(other["creator"] != state["creator"] for _pid, other in group):
                group.append((packet_id, state)); placed = True; break
        if not placed:
            profile_groups.append([(packet_id, state)])
    for group in profile_groups:
        # A crash between a prior run's profile write and its final ack loop leaves
        # the profile durably complete but the packet still unacknowledged, so it
        # resurfaces here on every retry. Resolve each creator's deterministic
        # profile record id up front and skip/flag it the same way the evidence
        # stage above does, instead of unconditionally re-synthesizing (a wasted
        # provider call) and then failing write_profile's create-only guard forever.
        pending_group: list[tuple[str, dict[str, Any]]] = []
        for packet_id, state in group:
            rid = profile_record_id(state["creator"], model, [ref_id for ref_id, _sha in state["record_refs"]])
            if data_root.is_record_set_complete(subtree="derived", raw_anchor=packet_id,
                                                record_id=rid, completion_lane=AUDIENCE_PROFILE_SET_LANE):
                state["evidence"].append({"kind": "record_set_complete", "completion_lane": AUDIENCE_PROFILE_SET_LANE,
                                          "record_id": rid})
                results.append({"packet_id": packet_id, "creator_id": state["creator"], "status": "profile_skipped_done"})
            elif data_root.record_path(subtree="derived", raw_anchor=packet_id,
                                       lane=AUDIENCE_PROFILE_LANE, record_id=rid).exists():
                results.append({"packet_id": packet_id, "creator_id": state["creator"], "status": "profile_partial_needs_cleanup"})
                state["complete"] = False
            else:
                pending_group.append((packet_id, state))
        if not pending_group:
            continue
        evidence_by_creator = {state["creator"]: state["rows"] for _pid, state in pending_group}
        try:
            profiles = synthesize_profiles(evidence_by_creator=evidence_by_creator, transport=transport,
                                           provider=provider, model=model, api_key=api_key, max_tokens=max_tokens)
        except Exception as exc:
            for packet_id, state in pending_group:
                state["complete"] = False
                results.append({"packet_id": packet_id, "creator_id": state["creator"], "status": "profile_failed",
                                "error": f"{type(exc).__name__}: {exc}"[:250]})
            continue
        for packet_id, state in pending_group:
            try:
                paths = write_profile(data_root=data_root, raw_anchor=packet_id,
                                      profile=profiles[state["creator"]], model=model,
                                      evidence_records=state["record_refs"])
                written_profile_record_id = next(iter(paths.values())).name
                state["evidence"].append({"kind": "record_set_complete", "completion_lane": AUDIENCE_PROFILE_SET_LANE,
                                          "record_id": written_profile_record_id})
                results.append({"packet_id": packet_id, "creator_id": state["creator"], "status": "profile_extracted",
                                "primary_hypothesis": profiles[state["creator"]].primary_hypothesis})
            except Exception as exc:
                state["complete"] = False
                results.append({"packet_id": packet_id, "creator_id": state["creator"], "status": "profile_failed",
                                "error": f"{type(exc).__name__}: {exc}"[:250]})

    for packet_id, state in states.items():
        if state["complete"]:
            append_ack(data_root, raw_anchor=packet_id, ack_namespace=_ACK_NAMESPACE,
                       obligation=state["item"].obligation,
                       evidence=state["evidence"] or [{"kind": "no_extractable_transcripts"}])
    return results


__all__ = ["run_extraction"]
