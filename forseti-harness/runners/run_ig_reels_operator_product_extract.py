"""Operator-assisted IG Reels product extraction packet/import runner.

This path is for Codex subscription/manual operation, not hidden provider API use. It exports
one strict packet for an already-committed IG transcript, then imports the operator's strict
JSON-array response through the same parser and silver product-mentions writer as the provider
runner.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cleaning.transcript_product_extractor import (
    TranscriptInput,
    build_extraction_prompt,
    parse_mentions,
)
from cleaning.transcript_product_lake import (
    mentions_record_id,
    write_product_mentions_result_into_lake,
)
from runners.run_ig_reels_product_extract import (
    _mentions_set_state,
    _result_identity,
    discover_transcript_candidates,
)

OPERATOR_PACKET_KIND = "ig_reels_operator_product_extract_v0"
OPERATOR_BACKEND = "operator_codex_assisted"
DEFAULT_OPERATOR_MODEL = "codex-operator-assisted-v0"


def transcript_content_sha256(transcript: TranscriptInput) -> str:
    body = {
        "video_id": transcript.video_id,
        "transcript_anchor": transcript.transcript_anchor,
        "transcript_source": transcript.transcript_source,
        "transcript_source_key": transcript.transcript_source_key,
        "source_route": transcript.source_route,
        "asr_record_id": transcript.asr_record_id,
        "cues": transcript.cues,
    }
    encoded = json.dumps(body, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def select_operator_transcript(
    *,
    data_root: Any,
    transcript_source_key: str | None = None,
    platform_item_id: str | None = None,
) -> TranscriptInput:
    if transcript_source_key and platform_item_id:
        raise ValueError("select by either transcript_source_key or platform_item_id, not both")

    matches: list[TranscriptInput] = []
    failures: list[dict[str, Any]] = []
    for transcript, failure in discover_transcript_candidates(data_root):
        if failure is not None:
            failures.append(failure)
            continue
        if transcript is None:
            continue
        if transcript_source_key is not None and transcript.transcript_source_key != transcript_source_key:
            continue
        if platform_item_id is not None and transcript.video_id != platform_item_id:
            continue
        matches.append(transcript)

    if not matches:
        suffix = f"; discovery_failures={len(failures)}" if failures else ""
        raise LookupError(f"no matching IG transcript found{suffix}")
    if len(matches) == 1:
        return matches[0]

    deep_capture_matches = [item for item in matches if item.source_route == "deep_capture_render_audio"]
    if platform_item_id is not None and len(deep_capture_matches) == 1:
        return deep_capture_matches[0]

    keys = ", ".join(str(item.transcript_source_key) for item in matches)
    raise ValueError(f"ambiguous IG transcript selection; supply --transcript-source-key ({keys})")


def build_operator_packet(*, transcript: TranscriptInput, model: str = DEFAULT_OPERATOR_MODEL) -> dict[str, Any]:
    identity = _result_identity(transcript)
    return {
        "packet_kind": OPERATOR_PACKET_KIND,
        "packet_version": "v0",
        "extraction_backend": OPERATOR_BACKEND,
        "model": model,
        "transcript_identity": identity,
        "transcript_content_sha256": transcript_content_sha256(transcript),
        "prompt": build_extraction_prompt(transcript),
        "response_contract": {
            "return_shape": "JSON array of product mention objects",
            "return_only": "No prose, no markdown fence, no timestamps.",
            "import_validator": "cleaning.transcript_product_extractor.parse_mentions",
            "write_lane": "silver__cleaning__product_mentions",
        },
        "transcript": {
            "joined_text": transcript.joined_text,
            "cue_count": len(transcript.cues),
            "cues": transcript.cues,
        },
    }


def export_operator_packet(
    *,
    data_root: Any,
    transcript_source_key: str | None = None,
    platform_item_id: str | None = None,
    model: str = DEFAULT_OPERATOR_MODEL,
    output_path: Path | None = None,
) -> dict[str, Any]:
    transcript = select_operator_transcript(
        data_root=data_root,
        transcript_source_key=transcript_source_key,
        platform_item_id=platform_item_id,
    )
    state = _mentions_set_state(data_root, transcript, model)
    result: dict[str, Any] = {**_result_identity(transcript), "status": state}
    if state != "extractable":
        return result

    packet = build_operator_packet(transcript=transcript, model=model)
    result["status"] = "operator_packet_exported"
    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(packet, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        result["packet_path"] = str(output_path)
    else:
        result["packet"] = packet
    return result


def import_operator_response(
    *,
    data_root: Any,
    packet: Mapping[str, Any],
    response_text: str,
    model: str | None = None,
) -> dict[str, Any]:
    if packet.get("packet_kind") != OPERATOR_PACKET_KIND:
        raise ValueError("operator packet kind mismatch")
    identity = packet.get("transcript_identity")
    if not isinstance(identity, Mapping):
        raise ValueError("operator packet missing transcript_identity")
    source_key = identity.get("transcript_source_key")
    if not isinstance(source_key, str) or not source_key:
        raise ValueError("operator packet missing transcript_source_key")

    transcript = select_operator_transcript(data_root=data_root, transcript_source_key=source_key)
    expected_sha = packet.get("transcript_content_sha256")
    actual_sha = transcript_content_sha256(transcript)
    if expected_sha != actual_sha:
        raise ValueError("operator packet transcript content no longer matches lake transcript")

    resolved_model = model or str(packet.get("model") or DEFAULT_OPERATOR_MODEL)
    state = _mentions_set_state(data_root, transcript, resolved_model)
    if state == "complete":
        return {**_result_identity(transcript), "status": "skipped_done"}
    if state == "partial_needs_cleanup":
        return {**_result_identity(transcript), "status": "partial_needs_cleanup"}

    parsed = parse_mentions(response_text, transcript, model=resolved_model)
    rid = mentions_record_id(transcript, resolved_model)
    paths = write_product_mentions_result_into_lake(
        data_root=data_root,
        transcript=transcript,
        result=parsed,
        model=resolved_model,
        record_id=rid,
        extraction_backend=OPERATOR_BACKEND,
        extraction_provenance={
            "packet_kind": OPERATOR_PACKET_KIND,
            "transcript_content_sha256": actual_sha,
            "operator_medium": "codex_subscription_or_manual_json",
            "response_contract": "strict_json_array",
        },
    )
    written = next(iter(paths.values()), None)
    return {
        **_result_identity(transcript),
        "status": "extracted",
        "path": str(written) if written is not None else None,
        "mention_count": len(parsed.mentions),
        "rejected_count": len(parsed.rejected),
    }


def _read_json_object(path: Path) -> dict[str, Any]:
    body = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(body, dict):
        raise ValueError(f"expected JSON object: {path}")
    return body


def _status_exit_code(payload: Any) -> int:
    if not isinstance(payload, Mapping):
        return 0
    status = payload.get("status")
    if status in {None, "operator_packet_exported", "extracted", "skipped_done", "complete"}:
        return 0
    if status == "partial_needs_cleanup":
        return 4
    return 3


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Export/import operator-assisted IG product extraction packets.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    export = subparsers.add_parser("export", help="Export one operator packet for an IG transcript.")
    export.add_argument("--data-root", default=None, help="Forseti data lake root. Defaults to FORSETI_DATA_ROOT (legacy ORCA_DATA_ROOT).")
    export.add_argument("--transcript-source-key", default=None, help="Exact transcript source key to export.")
    export.add_argument("--platform-item-id", default=None, help="IG Reel shortcode; deep capture is preferred if unique.")
    export.add_argument("--model", default=DEFAULT_OPERATOR_MODEL, help="Model token used in the mentions record_id.")
    export.add_argument("--out", type=Path, default=None, help="Write packet JSON here; stdout emits packet if omitted.")

    imp = subparsers.add_parser("import", help="Import an operator JSON-array response into the lake.")
    imp.add_argument("--data-root", default=None, help="Forseti data lake root. Defaults to FORSETI_DATA_ROOT (legacy ORCA_DATA_ROOT).")
    imp.add_argument("--packet", type=Path, required=True, help="Packet JSON previously exported by this runner.")
    imp.add_argument("--response", type=Path, required=True, help="Operator response file containing only the JSON array.")
    imp.add_argument("--model", default=None, help="Optional override for the packet model token.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    from data_lake.root import DataLakeRoot

    try:
        data_root = DataLakeRoot.resolve(explicit=args.data_root)
    except Exception as exc:  # noqa: BLE001 - CLI must surface root resolution failures
        parser.exit(status=2, message=f"data root required: {type(exc).__name__}: {exc}\n")

    try:
        if args.command == "export":
            result = export_operator_packet(
                data_root=data_root,
                transcript_source_key=args.transcript_source_key,
                platform_item_id=args.platform_item_id,
                model=args.model,
                output_path=args.out,
            )
            payload = result.get("packet") if args.out is None and "packet" in result else result
        else:
            packet = _read_json_object(args.packet)
            response_text = args.response.read_text(encoding="utf-8")
            payload = import_operator_response(
                data_root=data_root,
                packet=packet,
                response_text=response_text,
                model=args.model,
            )
    except (LookupError, ValueError) as exc:
        parser.exit(status=3, message=f"ig operator product extraction failed: {exc}\n")

    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return _status_exit_code(payload)


if __name__ == "__main__":
    raise SystemExit(main())
