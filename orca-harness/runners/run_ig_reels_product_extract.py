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

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

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
DEFAULT_EXTRACTION_MODEL = "codex-extraction-v0"


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


def _mentions_set_state(data_root, transcript: TranscriptInput, model: str) -> str:
    rid = mentions_record_id(transcript, model)
    if data_root.is_record_set_complete(
        subtree="derived",
        raw_anchor=transcript.transcript_anchor,
        record_id=rid,
        completion_lane=PRODUCT_MENTIONS_SET_LANE,
    ):
        return "complete"
    member_path = _record_path(
        data_root,
        raw_anchor=transcript.transcript_anchor,
        lane=PRODUCT_MENTIONS_LANE,
        record_id=rid,
    )
    if member_path.exists():
        return "partial_needs_cleanup"
    return "extractable"


def pending_extraction_counts(*, data_root, model: str = DEFAULT_EXTRACTION_MODEL) -> dict[str, int]:
    """Count extractable and crash-partial IG Reel transcript mention sets.

    Scheduler gate helper: no LLM and no network. Discovery may best-effort
    rebuild the disposable availability index, matching ``run_extraction``.
    Corrupt packets are isolated the same way discovery is isolated there.
    """
    counts = {"extractable": 0, "partial_needs_cleanup": 0}
    for packet_id in _candidate_packet_ids(data_root):
        try:
            transcripts = _transcripts_for_packet(data_root, packet_id)
        except Exception:  # noqa: BLE001 - corrupt packet discovery must not abort the poll
            continue
        for transcript in transcripts:
            state = _mentions_set_state(data_root, transcript, model)
            if state in counts:
                counts[state] += 1
    return counts


def count_pending_extractions(*, data_root, model: str = DEFAULT_EXTRACTION_MODEL) -> int:
    """Count transcripts that can be extracted now without manual cleanup."""
    return pending_extraction_counts(data_root=data_root, model=model)["extractable"]


def count_partial_extractions(*, data_root, model: str = DEFAULT_EXTRACTION_MODEL) -> int:
    """Count incomplete mention sets that need operator cleanup before retry."""
    return pending_extraction_counts(data_root=data_root, model=model)["partial_needs_cleanup"]


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


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="IG Reels product extraction runner utilities."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Print the LLM-free count of extractable IG Reel transcripts.",
    )
    parser.add_argument(
        "--check-partials",
        action="store_true",
        help="Print the LLM-free count of partial mentions sets needing cleanup.",
    )
    parser.add_argument(
        "--data-root",
        default=None,
        help="Orca data lake root. Defaults to ORCA_DATA_ROOT.",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_EXTRACTION_MODEL,
        help="Model token used in the deterministic mentions record_id.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    if args.check and args.check_partials:
        parser.exit(status=2, message="choose exactly one of --check or --check-partials\n")
    if not args.check and not args.check_partials:
        parser.exit(status=2, message="no action requested; use --check or --check-partials\n")

    from data_lake.root import DataLakeRoot

    try:
        data_root = DataLakeRoot.resolve(explicit=args.data_root)
    except Exception as exc:  # noqa: BLE001 - CLI must surface root resolution failures
        parser.exit(status=2, message=f"data root required: {type(exc).__name__}: {exc}\n")
    counts = pending_extraction_counts(data_root=data_root, model=args.model)
    key = "extractable" if args.check else "partial_needs_cleanup"
    print(counts[key])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
