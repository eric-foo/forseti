"""Daemon-ready runner: extract product mentions from every committed Instagram Reel transcript.

The IG analogue of `run_transcript_product_extract` (YouTube). Decoupled / choreography (not a
call-chain): independently scans the lake for committed IG-Reel audio packets and extracts any
whose transcript lacks a completed mentions record-set. Daemon-ready by the same contract —
idempotent (skip-if-done via the completion marker), stateless/resumable, per-item failure
isolated at BOTH grains (a corrupt packet -> `discovery_failed`; a transcript whose extraction
raises -> `failed`; the batch never aborts), single entrypoint (`run_extraction`).

IG is its OWN runner (not an edit to the YouTube runner, which hardcodes
`list_available(source_family="youtube")`): discovery keys on source_family=instagram_creator and
the ig_reels_audio surface. IG Reels have no caption track, so the ASR path is the only route. The
extract+persist seam (`cleaning.transcript_product_lake`) and the schema are source-family-agnostic
and reused verbatim.

No-LLM zone (`runners/`): imports the cleaning driver but no LLM SDK
(`tests/contract/test_no_llm_imports.py`). The Transport is INJECTED, so the live caller
(subscription- or API-routed) is wired separately and this stays offline-testable.

Spec: orca/product/spines/capture/core/source_families/social_media/instagram/
ig_reels_transcript_product_extraction_spec_v0.md (IG delta; daemon-readiness inherited).
"""

from __future__ import annotations

import json

from cleaning.transcript_product_extractor import TranscriptInput
from cleaning.transcript_product_lake import (
    PRODUCT_MENTIONS_LANE,
    PRODUCT_MENTIONS_SET_LANE,
    cues_from_asr_record,
    extract_products_into_lake,
    mentions_record_id,
)

_ASR_LANE = "transcript_asr"
_IG_SOURCE_FAMILY = "instagram_creator"
_IG_AUDIO_SURFACE = "ig_reels_audio"


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


def _capture_metadata(loaded, files: dict[str, str]) -> dict:
    body = _body_ending_with(loaded, files, "capture_metadata.json")
    if body is None:
        return {}
    try:
        meta = json.loads(body.decode("utf-8"))
        return meta if isinstance(meta, dict) else {}
    except ValueError:
        return {}


def _lane_dir(data_root, *, raw_anchor: str, lane: str):
    resolver = getattr(data_root, "lane_dir", None)
    if resolver is not None:
        return resolver(subtree="derived", raw_anchor=raw_anchor, lane=lane)
    return data_root.path / "derived" / raw_anchor / lane


def _record_path(data_root, *, raw_anchor: str, lane: str, record_id: str):
    resolver = getattr(data_root, "record_path", None)
    if resolver is not None:
        return resolver(
            subtree="derived", raw_anchor=raw_anchor, lane=lane, record_id=record_id
        )
    return data_root.path / "derived" / raw_anchor / lane / record_id

def _asr_records(data_root, audio_packet_id: str) -> list[dict]:
    """Read transcript_asr derived records by path (derived records carry no by-key hash)."""
    lane_dir = _lane_dir(data_root, raw_anchor=audio_packet_id, lane=_ASR_LANE)
    if not lane_dir.is_dir():
        return []
    records: list[dict] = []
    for record_file in sorted(lane_dir.iterdir()):
        if not record_file.is_file():
            continue
        try:
            data = json.loads(record_file.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if isinstance(data, dict):
            records.append(data)
    return records


def _candidate_packet_ids(data_root) -> list[str]:
    """Committed instagram_creator packet ids. Rebuilds availability from raw first so discovery
    does not depend on a pre-populated index. Best-effort: a single corrupt manifest must not
    abort the run (it just goes un-indexed/skipped)."""
    try:
        data_root.rebuild_availability()
    except Exception:  # noqa: BLE001 - a corrupt manifest must not abort the run; index is best-effort
        pass
    return list(data_root.list_available(source_family=_IG_SOURCE_FAMILY))


def _transcripts_for_packet(data_root, packet_id: str) -> list[TranscriptInput]:
    """Normalize one committed IG packet into TranscriptInput(s). MAY RAISE on a corrupt packet
    (fail-closed `load_raw_packet` sha mismatch) — the caller isolates per packet.

    Only the ig_reels_audio surface carries a transcript (as a derived `transcript_asr` record);
    the instagram_creator family also holds grid-metadata packets with NO audio, which are skipped
    here. Only `transcribed` records with cues are used.
    """
    loaded = data_root.load_raw_packet(packet_id)
    manifest = loaded.manifest
    if manifest.get("source_surface") != _IG_AUDIO_SURFACE:
        return []  # e.g. ig_reels_grid_dom_passive_json: no audio/transcript -> not a transcript source
    files = _file_paths(manifest)
    meta = _capture_metadata(loaded, files)
    meta_shortcode = str(meta.get("platform_shortcode") or "")

    transcripts: list[TranscriptInput] = []
    for record in _asr_records(data_root, packet_id):
        if record.get("posture") != "transcribed":
            continue
        cues = cues_from_asr_record(record)
        shortcode = str(record.get("video_id") or meta_shortcode)
        if cues and shortcode:
            transcripts.append(TranscriptInput(shortcode, packet_id, "asr", cues))
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
    """The single daemon entrypoint: extract mentions for every not-yet-done IG-Reel transcript.

    Failure-isolated at both grains (corrupt packet -> `discovery_failed`; per-transcript raise ->
    `failed`; the batch always continues). Idempotent (skip-if-done). A record-set half-written
    before its completion marker (process crash) yields `partial_needs_cleanup`. Returns one status
    dict per packet/transcript.
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
                member_path = _record_path(
                    data_root, raw_anchor=anchor, lane=PRODUCT_MENTIONS_LANE, record_id=rid
                )
                if member_path.exists():
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
