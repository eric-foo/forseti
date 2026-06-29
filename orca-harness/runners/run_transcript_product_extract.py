"""Daemon-ready runner: extract product mentions from every committed YouTube transcript.

Decoupled / choreography (not a call-chain): this independently scans the lake for committed
transcripts and extracts any that lack a completed mentions record-set. Daemon-ready by the
spec contract — idempotent (skip-if-done via the completion marker), stateless/resumable
(work is re-derived from the lake each run; a record-set left half-written by a process crash
before its completion marker surfaces as `partial_needs_cleanup` for operator remediation, not
silent auto-resume), per-item failure isolated at BOTH grains (a corrupt packet -> a
`discovery_failed` status; a transcript whose extraction raises -> a `failed` status; the batch
never aborts), single entrypoint (`run_extraction`). A cron/daemon just calls `run_extraction`
on a timer (zero rework).

No-LLM zone (`runners/`): this file imports the cleaning driver but no LLM SDK
(`tests/contract/test_no_llm_imports.py`). The Transport is INJECTED, so the live caller
(subscription- or API-routed) is wired separately and this stays offline-testable.

Spec: youtube_transcript_product_extraction_spec_v0.md (daemon-readiness contract).
"""

from __future__ import annotations

import hashlib
import json

from cleaning.transcript_product_extractor import TranscriptInput
from cleaning.transcript_product_lake import (
    PRODUCT_MENTIONS_LANE,
    PRODUCT_MENTIONS_SET_LANE,
    build_transcript_source_lineage,
    cues_from_asr_record,
    cues_from_json3,
    extract_products_into_lake,
    mentions_record_id,
)
from data_lake.silver_lineage import SilverAnchor, SilverDerivedRef, SilverRawRef

_ASR_LANE = "transcript_asr"


def _file_paths(manifest: dict) -> dict[str, str]:
    return {
        pf.get("file_id", ""): pf.get("relative_packet_path", "")
        for pf in manifest.get("preserved_files", [])
        if isinstance(pf, dict)
    }


def _body_ending_with(loaded, files: dict[str, str], suffix: str) -> bytes | None:
    for file_id, path in files.items():
        if path.endswith(suffix):
            return loaded.bodies.get(file_id)
    return None


def _file_id_ending_with(files: dict[str, str], suffix: str) -> str | None:
    """The preserved file_id whose packet-relative path ends with ``suffix`` (for a raw_ref)."""
    for file_id, path in files.items():
        if path.endswith(suffix):
            return file_id
    return None


def _preserved_by_id(manifest: dict) -> dict[str, dict]:
    """Map preserved file_id -> its manifest entry (carries relative_packet_path + sha256)."""
    return {
        pf["file_id"]: pf
        for pf in manifest.get("preserved_files", [])
        if isinstance(pf, dict) and pf.get("file_id")
    }


def _capture_metadata(loaded, files: dict[str, str]) -> dict:
    body = _body_ending_with(loaded, files, "capture_metadata.json")
    if body is None:
        return {}
    try:
        meta = json.loads(body.decode("utf-8"))
        return meta if isinstance(meta, dict) else {}
    except ValueError:
        return {}


def _asr_records(data_root, audio_packet_id: str) -> list[tuple[dict, str, str]]:
    """Read transcript_asr derived records by path, returning ``(record, record_id, sha256)``.

    The record_id (file name) and content sha256 let a consumer reference the EXACT
    consumed transcript record (closing same-shortcode ambiguity). Derived records carry
    no by-key hash, so sha256 is computed from the record file bytes -- equal to the
    derivation-time member_sha256 the lake committed in the transcript_asr set marker.
    """
    lane_dir = data_root.lane_dir(subtree="derived", raw_anchor=audio_packet_id, lane=_ASR_LANE)
    if not lane_dir.is_dir():
        return []
    records: list[tuple[dict, str, str]] = []
    # transcript_asr record ids carry no extension (asr_packet.py), so read every file, not *.json.
    for record_file in sorted(lane_dir.iterdir()):
        if not record_file.is_file():
            continue
        try:
            body = record_file.read_bytes()
            data = json.loads(body.decode("utf-8"))
        except (OSError, ValueError):
            continue
        if isinstance(data, dict):
            records.append((data, record_file.name, hashlib.sha256(body).hexdigest()))
    return records


def _candidate_packet_ids(data_root) -> list[str]:
    """Committed YouTube packet ids. Rebuilds the availability index from raw first so
    discovery does not depend on the index being pre-populated. The rebuild is best-effort:
    a single corrupt manifest must not abort the whole run (it just goes un-indexed/skipped)."""
    try:
        data_root.rebuild_availability()
    except Exception:  # noqa: BLE001 - a corrupt manifest must not abort the run; index is best-effort
        pass
    return list(data_root.list_available(source_family="youtube"))


def _transcripts_for_packet(data_root, packet_id: str) -> list[TranscriptInput]:
    """Normalize one committed packet into TranscriptInput(s). MAY RAISE on a corrupt packet
    (e.g. a fail-closed `load_raw_packet` sha mismatch) — the caller isolates per packet.

    Caption packets carry the transcript json3 directly (bronze); audio packets carry it as a
    derived `transcript_asr` record (only `transcribed` records with cues are used).
    """
    loaded = data_root.load_raw_packet(packet_id)
    manifest = loaded.manifest
    surface = manifest.get("source_surface")
    files = _file_paths(manifest)
    meta = _capture_metadata(loaded, files)
    meta_video_id = str(meta.get("platform_video_id") or "")

    transcripts: list[TranscriptInput] = []
    if surface == "youtube_captions":
        json3 = _body_ending_with(loaded, files, ".json3")
        json3_file_id = _file_id_ending_with(files, ".json3")
        if json3 is not None and json3_file_id and meta_video_id:
            cues = cues_from_json3(json3)
            if cues:
                # Caption transcript is read from a raw json3 preserved file -> raw_ref to it.
                preserved = _preserved_by_id(manifest).get(json3_file_id, {})
                raw_ref = SilverRawRef(
                    packet_id=packet_id,
                    file_id=json3_file_id,
                    relative_packet_path=str(preserved.get("relative_packet_path") or "") or None,
                    sha256=str(preserved.get("sha256") or "") or None,
                    hash_basis="raw_stored_bytes",
                    anchor=SilverAnchor(kind="file"),
                    relation="consumed",
                )
                lineage = build_transcript_source_lineage(
                    namespace="youtube",
                    source_surface=surface,
                    video_id=meta_video_id,
                    raw_ref=raw_ref,
                )
                transcripts.append(
                    TranscriptInput(meta_video_id, packet_id, "caption", cues, source_lineage=lineage)
                )
    elif surface == "youtube_audio":
        for record, record_id, record_sha in _asr_records(data_root, packet_id):
            if record.get("posture") != "transcribed":
                continue
            cues = cues_from_asr_record(record)
            video_id = str(record.get("video_id") or meta_video_id)
            if cues and video_id:
                # The ASR transcript IS a derived record -> derived_ref to the EXACT record consumed.
                derived_ref = SilverDerivedRef(
                    raw_anchor=packet_id,
                    lane=_ASR_LANE,
                    record_id=record_id,
                    sha256=record_sha,
                    hash_basis="derived_record_bytes",
                    relation="consumed",
                )
                lineage = build_transcript_source_lineage(
                    namespace="youtube",
                    source_surface=surface,
                    video_id=video_id,
                    derived_ref=derived_ref,
                    captured_at=str(record.get("retrieval_time_utc") or "") or None,
                )
                transcripts.append(
                    TranscriptInput(video_id, packet_id, "asr", cues, source_lineage=lineage)
                )
    return transcripts


def run_extraction(
    *,
    data_root,
    transport,
    provider,
    model: str,
    api_key: str,
    max_tokens: int = 2048,
) -> list[dict]:
    """The single daemon entrypoint: extract mentions for every not-yet-done transcript.

    Failure-isolated at both grains: a corrupt packet yields a `discovery_failed` status; a
    transcript whose check/extraction raises yields a `failed` status — the batch always
    continues. Idempotent (skip-if-done). A record-set half-written before its completion marker
    (process crash) yields `partial_needs_cleanup` rather than a re-colliding `failed` forever.
    Returns one status dict per packet/transcript.
    """
    results: list[dict] = []
    for packet_id in _candidate_packet_ids(data_root):
        try:
            transcripts = _transcripts_for_packet(data_root, packet_id)
        except Exception as exc:  # noqa: BLE001 - a corrupt packet -> discovery_failed, batch continues
            results.append(
                {"packet_id": packet_id, "status": "discovery_failed", "error": f"{type(exc).__name__}: {exc}"[:200]}
            )
            continue
        for transcript in transcripts:
            anchor = transcript.transcript_anchor
            try:
                rid = mentions_record_id(transcript, model)
                if data_root.is_record_set_complete(
                    subtree="derived",
                    raw_anchor=anchor,
                    record_id=rid,
                    completion_lane=PRODUCT_MENTIONS_SET_LANE,
                ):
                    results.append(
                        {"anchor": anchor, "video_id": transcript.video_id, "status": "skipped_done"}
                    )
                    continue
                member_path = data_root.record_path(
                    subtree="derived", raw_anchor=anchor, lane=PRODUCT_MENTIONS_LANE, record_id=rid
                )
                if member_path.exists():
                    # Member record written but the completion marker is absent: a crash between the
                    # two writes. The deterministic record_id would re-collide on every rerun, so
                    # surface it for operator cleanup rather than looping forever on `failed`.
                    results.append(
                        {"anchor": anchor, "video_id": transcript.video_id, "status": "partial_needs_cleanup"}
                    )
                    continue
                paths = extract_products_into_lake(
                    data_root=data_root,
                    transcript=transcript,
                    transport=transport,
                    provider=provider,
                    model=model,
                    api_key=api_key,
                    record_id=rid,
                    max_tokens=max_tokens,
                )
                written = next(iter(paths.values()), None)
                results.append(
                    {
                        "anchor": anchor,
                        "video_id": transcript.video_id,
                        "status": "extracted",
                        "path": str(written) if written is not None else None,
                    }
                )
            except Exception as exc:  # noqa: BLE001 - per-item failure isolation (daemon-ready)
                results.append(
                    {"anchor": anchor, "video_id": transcript.video_id, "status": "failed", "error": f"{type(exc).__name__}: {exc}"[:200]}
                )
    return results
