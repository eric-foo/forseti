from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Sequence

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
)

if TYPE_CHECKING:
    from data_lake.root import DataLakeRoot

from source_capture.cli_support import build_optional_fact
from source_capture.packet_assembly import stage_and_write_packet, staged_file_id_map
from source_capture.block_shell import CaptureBodyClass, classify_capture_body
from source_capture.adapters import (
    AntiBlockingHttpCaptureFailure,
    fetch_anti_blocking_http_capture,
)


ANTI_BLOCKING_HTTP_NON_CLAIMS = [
    "not the honest direct_http baseline",
    "not anti-detect browser automation",
    "not TLS/JA3 fingerprint impersonation",
    "not proxy or session injection",
    "not API SDK use",
    "not archive retrieval",
    "not media preservation",
    "not scraper framework use",
    "does not certify a returned body as real source content",
    "not ECR design",
    "not Cleaning implementation",
    "not Judgment scoring",
    "not buyer proof",
    "not commercial-readiness logic",
]


def run_source_capture_antiblock_http_packet(
    *,
    url: str,
    source_family: str,
    source_surface: str,
    decision_question: str,
    output_directory: Path | None = None,
    data_root: "DataLakeRoot | None" = None,
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
    if (output_directory is None) == (data_root is None):
        raise ValueError("exactly one of output_directory or data_root is required")

    capture_result = fetch_anti_blocking_http_capture(
        url=url,
        timeout_seconds=timeout_seconds,
        max_bytes=max_bytes,
    )
    if isinstance(capture_result, AntiBlockingHttpCaptureFailure):
        return 3, capture_result.message

    classification = classify_capture_body(
        status=capture_result.status,
        headers=capture_result.response_headers,
        body=capture_result.body,
    )
    status_ok = 200 <= capture_result.status < 300

    posture_limitations: list[str] = []
    if classification.classification == CaptureBodyClass.BLOCK_SHELL:
        access_posture = known_fact(
            f"anti_blocking_http access blocked at HTTP {capture_result.status} "
            f"{capture_result.reason or 'without reason'}: {classification.detail}; "
            "block/challenge shell preserved, not source content"
        )
        posture_limitations.append(
            "visible_capture_limitation: anti_blocking_http preserved a block/challenge shell "
            f"({classification.signal}) at HTTP {capture_result.status}, not source body"
        )
    elif classification.classification == CaptureBodyClass.EMPTY:
        access_posture = known_fact(
            f"anti_blocking_http returned HTTP {capture_result.status} with an "
            "empty/whitespace-only body; no source content preserved"
        )
        posture_limitations.append(
            "visible_capture_limitation: anti_blocking_http preserved an "
            "empty/whitespace-only body, no source content"
        )
    elif not status_ok:
        access_posture = known_fact(
            f"anti_blocking_http access_failed with HTTP {capture_result.status} "
            f"{capture_result.reason or 'without reason'}; response body preserved"
        )
        posture_limitations.append(
            f"access_failed: anti_blocking_http HTTP {capture_result.status}; response body preserved"
        )
    elif classification.signal == "encoded_body_uninspectable":
        access_posture = known_fact(
            f"anti_blocking_http returned HTTP {capture_result.status}; encoded body preserved; "
            "block/challenge inspection limited by response encoding; body not certified as source content"
        )
        posture_limitations.append(
            "visible_capture_limitation: anti_blocking_http preserved an encoded body; "
            "block/challenge inspection is limited and source content is not certified"
        )
    else:
        access_posture = known_fact(
            f"anti_blocking_http returned HTTP {capture_result.status}; body preserved; "
            "no block/challenge signature detected; body not certified as source content"
        )

    packet_warnings = list(warnings) + capture_result.warning_notes
    packet_limitations = list(limitations) + capture_result.limitation_notes + posture_limitations

    metadata = dict(capture_result.metadata)
    metadata["body_classification"] = classification.classification.value
    metadata["body_classification_signal"] = classification.signal
    metadata["body_classification_detail"] = classification.detail

    artifacts: list[tuple[str, bytes]] = [
        ("anti_blocking_http_response_body.bin", capture_result.body),
        (
            "anti_blocking_http_response_metadata.json",
            (json.dumps(metadata, indent=2, sort_keys=True) + "\n").encode("utf-8"),
        ),
    ]
    file_ids = staged_file_id_map(artifacts)

    mode_changes = list(visible_mode_changes) + [
        f"anti_blocking_http_profile:{capture_result.impersonation_profile}"
    ]

    timing = PacketTiming(
        source_publication_or_event=source_publication_or_event
        or unknown_with_reason("anti_blocking_http adapter did not infer source publication or event timing"),
        source_edit_or_version=source_edit_or_version
        or unknown_with_reason("anti_blocking_http adapter did not infer source edit or version timing"),
        capture_time=known_fact(str(capture_result.metadata["capture_timestamp"])),
        recapture_time=recapture_time
        or not_applicable("anti_blocking_http packet did not model an earlier capture by default"),
        cutoff_posture=cutoff_posture
        or unknown_with_reason("anti_blocking_http runner did not receive cutoff posture metadata"),
    )
    archive_posture = not_attempted("anti_blocking_http adapter does not query archive or history services")
    media_posture = not_attempted(
        "anti_blocking_http adapter preserves the response body only and does not fetch linked media assets"
    )
    recapture_posture = re_capture_relationship or not_applicable(
        "no prior source capture packet was supplied for this anti_blocking_http capture"
    )

    result = stage_and_write_packet(
        output_directory=output_directory,
        data_root=data_root,
        staged_artifacts=artifacts,
        source_slices=[
            SourceCaptureSlice(
                slice_id="slice_01",
                locator=known_fact(capture_result.final_url),
                timing=timing,
                access_posture=access_posture,
                archive_history_posture=archive_posture,
                media_modality_posture=media_posture,
                re_capture_relationship=recapture_posture,
                limitations=packet_limitations,
                warning_notes=packet_warnings,
                preserved_file_ids=[
                    file_ids["anti_blocking_http_response_body.bin"],
                    file_ids["anti_blocking_http_response_metadata.json"],
                ],
            )
        ],
        source_family=source_family,
        source_surface=source_surface,
        source_locator=known_fact(capture_result.requested_url),
        decision_question=decision_question,
        capture_context=capture_context,
        actor_audience_context=actor_audience_context
        or unknown_with_reason("actor or audience context was not supplied to the anti_blocking_http runner"),
        capture_mode=capture_mode,
        operator_category=operator_category,
        session_identity=session_id,
        visible_mode_changes=mode_changes,
        source_publication_or_event=timing.source_publication_or_event,
        source_edit_or_version=timing.source_edit_or_version,
        cutoff_posture=timing.cutoff_posture,
        recapture_time=timing.recapture_time,
        access_posture=access_posture,
        archive_history_posture=archive_posture,
        media_modality_posture=media_posture,
        re_capture_relationship=recapture_posture,
        warnings=packet_warnings,
        limitations=packet_limitations,
        receipt_summary=(
            f"anti_blocking_http packet ({capture_result.impersonation_profile}) for {source_family} "
            f"with HTTP {capture_result.status}, body classification "
            f"'{classification.classification.value}', {len(capture_result.body)} preserved body bytes."
        ),
        receipt_non_claims=ANTI_BLOCKING_HTTP_NON_CLAIMS,
    )
    return 0, result.output_directory


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Fetch one HTTP URL with a full desktop-Chrome header profile "
            "(anti_blocking_http rung-1) and write a Source Capture Packet, classifying the "
            "body as block-shell vs uncertified content. Does not impersonate TLS and does "
            "not certify a body as source content."
        )
    )
    parser.add_argument("--url", required=True)
    parser.add_argument("--source-family", default="web_page")
    parser.add_argument("--source-surface", default="anti_blocking_http")
    parser.add_argument("--decision-question", required=True)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument(
        "--data-root",
        default=None,
        help="Commit into the Orca data lake at this root; explicit --data-root is mutually exclusive with --output. ORCA_DATA_ROOT is used only when --output is omitted.",
    )
    parser.add_argument(
        "--capture-context",
        default="anti-blocking HTTP source capture (header-complete stdlib, rung-1)",
    )
    parser.add_argument("--operator-category", default="anti_blocking_http_cli_operator")
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
        data_root = None
        data_root_requested = args.data_root is not None or (args.output is None and os.environ.get("ORCA_DATA_ROOT"))
        if args.output is not None and args.data_root is not None:
            parser.exit(
                status=2,
                message="source capture anti_blocking_http failed: exactly one of --output or --data-root/ORCA_DATA_ROOT is required\n",
            )
        if args.output is None and not data_root_requested:
            parser.exit(
                status=2,
                message="source capture anti_blocking_http failed: exactly one of --output or --data-root/ORCA_DATA_ROOT is required\n",
            )
        if data_root_requested:
            from data_lake.root import DataLakeRoot

            data_root = DataLakeRoot.resolve(explicit=args.data_root)
        exit_code, message = run_source_capture_antiblock_http_packet(
            url=args.url,
            source_family=args.source_family,
            source_surface=args.source_surface,
            decision_question=args.decision_question,
            output_directory=args.output if data_root is None else None,
            data_root=data_root,
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
        parser.exit(status=2, message=f"source capture anti_blocking_http failed: {exc}\n")
    except Exception as exc:  # noqa: BLE001 - surface any adapter/writer failure as exit 3
        parser.exit(status=3, message=f"source capture anti_blocking_http failed: {exc}\n")

    if exit_code == 0:
        print(message)
        return 0

    parser.exit(status=exit_code, message=f"source capture anti_blocking_http failed: {message}\n")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
