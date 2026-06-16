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
)
from source_capture.cadence import build_cadence_plan
from source_capture.cli_support import build_optional_fact
from source_capture.packet_assembly import stage_and_write_packet, staged_file_id_map
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
    session_visibility_pin=None,
    locale_pin=None,
    currency_pin=None,
    variant_pin=None,
    series_id: str | None = None,
    cold_start_at=None,
    pre_coverage_history_posture=None,
    intended_cadence: dict[str, object] | None = None,
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

    artifacts: list[tuple[str, bytes]] = [
        ("http_response_body.bin", capture_result.body),
        (
            "http_response_metadata.json",
            (json.dumps(capture_result.metadata, indent=2, sort_keys=True) + "\n").encode("utf-8"),
        ),
    ]
    file_ids = staged_file_id_map(artifacts)

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
    archive_posture = not_attempted("direct HTTP adapter does not query archive or history services")
    media_posture = not_attempted(
        "direct HTTP adapter preserves the response body only and does not fetch linked media assets"
    )
    recapture_posture = re_capture_relationship or not_applicable(
        "no prior source capture packet was supplied for this direct HTTP capture"
    )

    result = stage_and_write_packet(
        output_directory=output_directory,
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
                session_visibility_pin=session_visibility_pin,
                locale_pin=locale_pin,
                currency_pin=currency_pin,
                variant_pin=variant_pin,
                limitations=packet_limitations,
                warning_notes=packet_warnings,
                preserved_file_ids=[
                    file_ids["http_response_body.bin"],
                    file_ids["http_response_metadata.json"],
                ],
            )
        ],
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
        archive_history_posture=archive_posture,
        media_modality_posture=media_posture,
        re_capture_relationship=recapture_posture,
        series_id=series_id,
        cold_start_at=cold_start_at,
        pre_coverage_history_posture=pre_coverage_history_posture,
        intended_cadence=intended_cadence,
        warnings=packet_warnings,
        limitations=packet_limitations,
        receipt_summary=(
            f"Direct HTTP packet for {source_family} with HTTP {capture_result.status} "
            f"and {len(capture_result.body)} preserved body bytes."
        ),
        receipt_non_claims=DIRECT_HTTP_NON_CLAIMS,
    )
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
    _add_durability_arguments(parser)
    return parser


def _add_durability_arguments(parser: argparse.ArgumentParser) -> None:
    """Add the optional demand-durability series flags (Ob.17 Elements 1, 2 & 4).

    All flags are optional; when none are supplied the packet's durability fields stay
    ``None`` (a non-durability capture, back-compat preserved). The four pins and the
    cold-start / pre-coverage postures are ``VisibleFact``s built by ``build_optional_fact``
    so an operator can record an honest gap (``unknown_with_reason`` / ``not_applicable``)
    instead of fabricating a value. ``--series-id`` is a plain identifier. The cadence flags
    build ``intended_cadence`` from ``cadence.build_cadence_plan(...).to_dict()`` -- the
    declared (not realized) sampling plan. These are observed facts, never weights or a
    durable-vs-hollow verdict (INV-1).
    """
    group = parser.add_argument_group("demand-durability series (optional)")
    group.add_argument("--series-id", default=None)
    # Element 1 pins (ride on the slice). Each pin accepts one of value / unknown / not-applicable.
    for pin in ("session-visibility-pin", "locale-pin", "currency-pin", "variant-pin"):
        group.add_argument(f"--{pin}", default=None)
        group.add_argument(f"--{pin}-unknown-reason", default=None)
        group.add_argument(f"--{pin}-not-applicable-reason", default=None)
    # Element 2 series-origin postures (ride on the packet).
    group.add_argument("--cold-start-at", default=None)
    group.add_argument("--cold-start-at-unknown-reason", default=None)
    group.add_argument("--cold-start-at-not-applicable-reason", default=None)
    group.add_argument("--pre-coverage-history-posture", default=None)
    group.add_argument("--pre-coverage-history-posture-unknown-reason", default=None)
    group.add_argument("--pre-coverage-history-posture-not-applicable-reason", default=None)
    # Element 4 declared cadence (built via cadence.build_cadence_plan).
    group.add_argument(
        "--intended-cadence-mode", choices=["fixed", "bounded_jitter"], default=None
    )
    group.add_argument("--intended-cadence-slot-count", type=int, default=None)
    group.add_argument("--intended-cadence-delay-seconds", type=float, default=None)
    group.add_argument("--intended-cadence-window-seconds", type=float, default=None)
    group.add_argument("--intended-cadence-min-gap-seconds", type=float, default=None)
    group.add_argument("--intended-cadence-max-gap-seconds", type=float, default=None)
    group.add_argument("--intended-cadence-random-seed", type=int, default=None)


def _build_intended_cadence(args: argparse.Namespace) -> dict[str, object] | None:
    """Build the declared ``intended_cadence`` dict from cadence flags, or ``None`` if absent.

    Reuses ``cadence.build_cadence_plan`` so the shape is the canonical
    ``CadencePlan.to_dict()`` (no invented shape). ``--intended-cadence-mode`` gates the build:
    without it the field stays ``None``. ``build_cadence_plan`` itself validates slot count and
    gap/window constraints and raises ``ValueError`` for an incoherent plan.
    """
    if args.intended_cadence_mode is None:
        return None
    if args.intended_cadence_slot_count is None:
        raise ValueError("--intended-cadence-slot-count is required when --intended-cadence-mode is set")
    plan = build_cadence_plan(
        slot_count=args.intended_cadence_slot_count,
        mode=args.intended_cadence_mode,
        delay_seconds=(
            args.intended_cadence_delay_seconds
            if args.intended_cadence_delay_seconds is not None
            else 0.0
        ),
        window_seconds=args.intended_cadence_window_seconds,
        min_gap_seconds=args.intended_cadence_min_gap_seconds,
        max_gap_seconds=args.intended_cadence_max_gap_seconds,
        random_seed=args.intended_cadence_random_seed,
    )
    return plan.to_dict()


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
            session_visibility_pin=build_optional_fact(
                label="session visibility pin",
                value=args.session_visibility_pin,
                unknown_reason=args.session_visibility_pin_unknown_reason,
                not_applicable_reason=args.session_visibility_pin_not_applicable_reason,
            ),
            locale_pin=build_optional_fact(
                label="locale pin",
                value=args.locale_pin,
                unknown_reason=args.locale_pin_unknown_reason,
                not_applicable_reason=args.locale_pin_not_applicable_reason,
            ),
            currency_pin=build_optional_fact(
                label="currency pin",
                value=args.currency_pin,
                unknown_reason=args.currency_pin_unknown_reason,
                not_applicable_reason=args.currency_pin_not_applicable_reason,
            ),
            variant_pin=build_optional_fact(
                label="variant pin",
                value=args.variant_pin,
                unknown_reason=args.variant_pin_unknown_reason,
                not_applicable_reason=args.variant_pin_not_applicable_reason,
            ),
            series_id=args.series_id,
            cold_start_at=build_optional_fact(
                label="cold-start timing",
                value=args.cold_start_at,
                unknown_reason=args.cold_start_at_unknown_reason,
                not_applicable_reason=args.cold_start_at_not_applicable_reason,
            ),
            pre_coverage_history_posture=build_optional_fact(
                label="pre-coverage history posture",
                value=args.pre_coverage_history_posture,
                unknown_reason=args.pre_coverage_history_posture_unknown_reason,
                not_applicable_reason=args.pre_coverage_history_posture_not_applicable_reason,
            ),
            intended_cadence=_build_intended_cadence(args),
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
