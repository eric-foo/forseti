from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from source_capture import (
    CaptureModeCategory,
    PacketTiming,
    SourceCaptureSlice,
    known_fact,
    not_applicable,
    not_attempted,
    unknown_with_reason,
    write_local_source_capture_packet,
)
from source_capture.adapters import DirectHttpCaptureFailure, fetch_direct_http_capture


DIRECT_HTTP_NON_CLAIMS = [
    "not browser automation",
    "not API SDK use",
    "not archive retrieval",
    "not media preservation",
    "not scraper framework use",
    "not proxy or session injection",
    "not ECR design",
    "not Cleaning implementation",
    "not Judgment scoring",
    "not buyer proof",
    "not commercial-readiness logic",
]


def build_optional_fact(
    *,
    label: str,
    value: str | None = None,
    unknown_reason: str | None = None,
    not_attempted_reason: str | None = None,
    not_applicable_reason: str | None = None,
):
    supplied = [
        item
        for item in (value, unknown_reason, not_attempted_reason, not_applicable_reason)
        if item is not None
    ]
    if len(supplied) > 1:
        raise ValueError(f"{label} accepts only one value/reason flag")
    if value is not None:
        return known_fact(value)
    if unknown_reason is not None:
        return unknown_with_reason(unknown_reason)
    if not_attempted_reason is not None:
        return not_attempted(not_attempted_reason)
    if not_applicable_reason is not None:
        return not_applicable(not_applicable_reason)
    return None


def run_source_capture_http_packet(
    *,
    url: str,
    source_family: str,
    source_surface: str,
    decision_question: str,
    output_directory: Path,
    capture_context: str,
    operator_category: str,
    capture_mode: CaptureModeCategory,
    session_id: str | None,
    actor_audience_context,
    visible_mode_changes: Sequence[str],
    source_publication_or_event,
    source_edit_or_version,
    cutoff_posture,
    recapture_time,
    re_capture_relationship,
    warnings: Sequence[str],
    limitations: Sequence[str],
    timeout_seconds: float,
    max_bytes: int,
) -> tuple[int, str]:
    capture_result = fetch_direct_http_capture(
        url=url,
        timeout_seconds=timeout_seconds,
        max_bytes=max_bytes,
    )
    if isinstance(capture_result, DirectHttpCaptureFailure):
        return 3, capture_result.message

    packet_warnings = list(warnings) + capture_result.warning_notes
    packet_limitations = list(limitations) + capture_result.limitation_notes

    if 200 <= capture_result.status < 300:
        access_posture = known_fact(
            f"direct_http succeeded with HTTP {capture_result.status} {capture_result.reason or 'without reason'}"
        )
    else:
        access_posture = known_fact(
            f"direct_http access_failed with HTTP {capture_result.status} {capture_result.reason or 'without reason'}; response body preserved"
        )

    staging_parent = output_directory.parent
    staging_parent.mkdir(parents=True, exist_ok=True)
    body_path = staging_parent / "http_response_body.bin"
    metadata_path = staging_parent / "http_response_metadata.json"
    if body_path.exists() or metadata_path.exists():
        raise ValueError(
            "direct HTTP staging files already exist in the output parent; clear them before rerunning"
        )
    try:
        body_path.write_bytes(capture_result.body)
        metadata_path.write_text(
            f"{json.dumps(capture_result.metadata, indent=2, sort_keys=True)}\n",
            encoding="utf-8",
            newline="\n",
        )

        timing = PacketTiming(
            source_publication_or_event=source_publication_or_event
            or unknown_with_reason("direct HTTP adapter did not infer source publication or event timing"),
            source_edit_or_version=source_edit_or_version
            or unknown_with_reason("direct HTTP adapter did not infer source edit or version timing"),
            capture_time=known_fact(str(capture_result.metadata["capture_timestamp"])),
            recapture_time=recapture_time
            or not_applicable("direct HTTP packet did not model an earlier capture by default"),
            cutoff_posture=cutoff_posture
            or unknown_with_reason("direct HTTP runner did not receive cutoff posture metadata"),
        )

        result = write_local_source_capture_packet(
            output_directory=output_directory,
            input_files=[body_path, metadata_path],
            source_family=source_family,
            source_surface=source_surface,
            source_locator=known_fact(capture_result.requested_url),
            decision_question=decision_question,
            capture_context=capture_context,
            actor_audience_context=actor_audience_context
            or unknown_with_reason("actor or audience context was not supplied to the direct HTTP runner"),
            capture_mode=capture_mode,
            operator_category=operator_category,
            session_identity=session_id,
            visible_mode_changes=visible_mode_changes,
            source_publication_or_event=timing.source_publication_or_event,
            source_edit_or_version=timing.source_edit_or_version,
            cutoff_posture=timing.cutoff_posture,
            recapture_time=timing.recapture_time,
            access_posture=access_posture,
            archive_history_posture=not_attempted(
                "direct HTTP adapter does not query archive or history services"
            ),
            media_modality_posture=not_attempted(
                "direct HTTP adapter preserves the response body only and does not fetch linked media assets"
            ),
            re_capture_relationship=re_capture_relationship
            or not_applicable("no prior source capture packet was supplied for this direct HTTP capture"),
            source_slices=[
                SourceCaptureSlice(
                    slice_id="slice_01",
                    locator=known_fact(capture_result.final_url),
                    timing=timing,
                    access_posture=access_posture,
                    archive_history_posture=not_attempted(
                        "direct HTTP adapter does not query archive or history services"
                    ),
                    media_modality_posture=not_attempted(
                        "direct HTTP adapter preserves the response body only and does not fetch linked media assets"
                    ),
                    re_capture_relationship=re_capture_relationship
                    or not_applicable("no prior source capture packet was supplied for this direct HTTP capture"),
                    limitations=packet_limitations,
                    warning_notes=packet_warnings,
                    preserved_file_ids=["file_01", "file_02"],
                )
            ],
            warnings=packet_warnings,
            limitations=packet_limitations,
            receipt_summary=(
                f"Direct HTTP packet for {source_family} with HTTP {capture_result.status} "
                f"and {len(capture_result.body)} preserved body bytes."
            ),
            receipt_non_claims=DIRECT_HTTP_NON_CLAIMS,
        )
    finally:
        for staging_path in (body_path, metadata_path):
            try:
                staging_path.unlink()
            except FileNotFoundError:
                pass
    return 0, result.output_directory


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Fetch one HTTP URL with stdlib urllib and write a Source Capture Packet when a non-empty body is returned."
    )
    parser.add_argument("--url", required=True)
    parser.add_argument("--source-family", default="web_page")
    parser.add_argument("--source-surface", default="direct_http")
    parser.add_argument("--decision-question", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--capture-context",
        default="direct HTTP source capture with stdlib urllib",
    )
    parser.add_argument("--operator-category", default="direct_http_cli_operator")
    parser.add_argument(
        "--capture-mode",
        choices=[item.value for item in CaptureModeCategory],
        default=CaptureModeCategory.STRUCTURED_ACCESS.value,
    )
    parser.add_argument("--session-id", default=None)
    parser.add_argument("--timeout-seconds", type=float, default=20.0)
    parser.add_argument("--max-bytes", type=int, default=5_000_000)
    parser.add_argument("--actor-audience-context", default=None)
    parser.add_argument("--actor-audience-context-unknown-reason", default=None)
    parser.add_argument("--visible-mode-change", action="append", default=[])
    parser.add_argument("--source-publication-or-event", default=None)
    parser.add_argument("--source-publication-or-event-unknown-reason", default=None)
    parser.add_argument("--source-edit-or-version", default=None)
    parser.add_argument("--source-edit-or-version-unknown-reason", default=None)
    parser.add_argument("--cutoff-posture", default=None)
    parser.add_argument("--cutoff-posture-unknown-reason", default=None)
    parser.add_argument("--recapture-time", default=None)
    parser.add_argument("--recapture-time-not-applicable-reason", default=None)
    parser.add_argument("--recapture-relationship", default=None)
    parser.add_argument("--recapture-relationship-not-applicable-reason", default=None)
    parser.add_argument("--warning", action="append", default=[])
    parser.add_argument("--limitation", action="append", default=[])
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        exit_code, message = run_source_capture_http_packet(
            url=args.url,
            source_family=args.source_family,
            source_surface=args.source_surface,
            decision_question=args.decision_question,
            output_directory=args.output,
            capture_context=args.capture_context,
            operator_category=args.operator_category,
            capture_mode=CaptureModeCategory(args.capture_mode),
            session_id=args.session_id,
            actor_audience_context=build_optional_fact(
                label="actor/audience context",
                value=args.actor_audience_context,
                unknown_reason=args.actor_audience_context_unknown_reason,
            ),
            visible_mode_changes=args.visible_mode_change,
            source_publication_or_event=build_optional_fact(
                label="source publication or event timing",
                value=args.source_publication_or_event,
                unknown_reason=args.source_publication_or_event_unknown_reason,
            ),
            source_edit_or_version=build_optional_fact(
                label="source edit or version timing",
                value=args.source_edit_or_version,
                unknown_reason=args.source_edit_or_version_unknown_reason,
            ),
            cutoff_posture=build_optional_fact(
                label="cutoff posture",
                value=args.cutoff_posture,
                unknown_reason=args.cutoff_posture_unknown_reason,
            ),
            recapture_time=build_optional_fact(
                label="re-capture timing",
                value=args.recapture_time,
                not_applicable_reason=args.recapture_time_not_applicable_reason,
            ),
            re_capture_relationship=build_optional_fact(
                label="re-capture relationship",
                value=args.recapture_relationship,
                not_applicable_reason=args.recapture_relationship_not_applicable_reason,
            ),
            warnings=args.warning,
            limitations=args.limitation,
            timeout_seconds=args.timeout_seconds,
            max_bytes=args.max_bytes,
        )
    except ValueError as exc:
        parser.exit(status=2, message=f"source capture direct HTTP failed: {exc}\n")
    except Exception as exc:
        parser.exit(status=3, message=f"source capture direct HTTP failed: {exc}\n")

    if exit_code == 0:
        print(message)
        return 0

    parser.exit(status=exit_code, message=f"source capture direct HTTP failed: {message}\n")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
