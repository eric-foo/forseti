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
from source_capture.cli_support import build_optional_fact
from source_capture.adapters import MediaAssetCaptureFailure, fetch_media_assets
from source_capture.adapters.direct_http import DirectHttpCaptureSuccess


MEDIA_ASSET_NON_CLAIMS = [
    "not asset discovery",
    "not gallery parsing",
    "not browser automation",
    "not API SDK use",
    "not archive retrieval",
    "not OCR or image analysis",
    "not scraper framework use",
    "not proxy or session injection",
    "not ECR design",
    "not Cleaning implementation",
    "not Judgment scoring",
    "not buyer proof",
    "not commercial-readiness logic",
]


def run_source_capture_media_packet(
    *,
    asset_urls: Sequence[str],
    source_family: str,
    source_surface: str,
    decision_question: str,
    output_directory: Path,
    capture_context: str,
    operator_category: str,
    capture_mode: CaptureModeCategory,
    session_id: str | None,
    source_locator,
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
    batch = fetch_media_assets(
        asset_urls=list(asset_urls),
        timeout_seconds=timeout_seconds,
        max_bytes=max_bytes,
    )
    if not batch.successes:
        failure_summary = "; ".join(_format_failure(failure) for failure in batch.failures)
        return 3, f"no media assets were preserved; {failure_summary}"

    staging_parent = output_directory.parent
    staging_parent.mkdir(parents=True, exist_ok=True)
    staged_paths: list[Path] = []
    packet_slices: list[SourceCaptureSlice] = []
    packet_warnings = list(warnings)
    packet_limitations = list(limitations)
    preserved_file_counter = 1

    try:
        packet_timing = PacketTiming(
            source_publication_or_event=source_publication_or_event
            or unknown_with_reason("media asset adapter did not infer source publication or event timing"),
            source_edit_or_version=source_edit_or_version
            or unknown_with_reason("media asset adapter did not infer source edit or version timing"),
            capture_time=known_fact(str(batch.successes[0].http_result.metadata["capture_timestamp"])),
            recapture_time=recapture_time
            or not_applicable("media asset packet did not model an earlier capture by default"),
            cutoff_posture=cutoff_posture
            or unknown_with_reason("media asset runner did not receive cutoff posture metadata"),
        )
        archive_posture = not_attempted("media asset adapter does not query archive or history services")
        recapture_posture = re_capture_relationship or not_applicable(
            "no prior source capture packet was supplied for this media asset capture"
        )

        for success in batch.successes:
            body_path = staging_parent / f"asset_{success.asset_index:02d}_body.bin"
            metadata_path = staging_parent / f"asset_{success.asset_index:02d}_metadata.json"
            if body_path.exists() or metadata_path.exists():
                raise ValueError(
                    "media asset staging files already exist in the output parent; clear them before rerunning"
                )
            body_path.write_bytes(success.http_result.body)
            staged_paths.append(body_path)
            metadata_path.write_text(
                f"{json.dumps(_asset_metadata(success.asset_index, success.asset_url, success.http_result), indent=2, sort_keys=True)}\n",
                encoding="utf-8",
                newline="\n",
            )
            staged_paths.append(metadata_path)

            access_posture = _access_posture_for_success(success.http_result)
            media_posture = known_fact(
                f"media_asset preserved asset {success.asset_index:02d} with "
                f"{len(success.http_result.body)} bytes"
            )
            file_ids = [
                f"file_{preserved_file_counter:02d}",
                f"file_{preserved_file_counter + 1:02d}",
            ]
            preserved_file_counter += 2
            packet_warnings.extend(success.http_result.warning_notes)
            packet_limitations.extend(success.http_result.limitation_notes)
            packet_slices.append(
                SourceCaptureSlice(
                    slice_id=f"asset_{success.asset_index:02d}",
                    locator=known_fact(success.http_result.final_url),
                    timing=_timing_for_success(
                        success.http_result,
                        source_publication_or_event=packet_timing.source_publication_or_event,
                        source_edit_or_version=packet_timing.source_edit_or_version,
                        recapture_time=packet_timing.recapture_time,
                        cutoff_posture=packet_timing.cutoff_posture,
                    ),
                    access_posture=access_posture,
                    archive_history_posture=archive_posture,
                    media_modality_posture=media_posture,
                    re_capture_relationship=recapture_posture,
                    limitations=list(success.http_result.limitation_notes),
                    warning_notes=list(success.http_result.warning_notes),
                    preserved_file_ids=file_ids,
                )
            )

        for failure in batch.failures:
            failure_note = _format_failure(failure)
            packet_limitations.append(f"asset_{failure.asset_index:02d}_not_preserved: {failure_note}")
            packet_slices.append(
                SourceCaptureSlice(
                    slice_id=f"asset_{failure.asset_index:02d}",
                    locator=known_fact(failure.asset_url),
                    timing=_timing_for_failure(
                        failure,
                        source_publication_or_event=packet_timing.source_publication_or_event,
                        source_edit_or_version=packet_timing.source_edit_or_version,
                        recapture_time=packet_timing.recapture_time,
                        cutoff_posture=packet_timing.cutoff_posture,
                    ),
                    access_posture=known_fact(f"media_asset access_failed: {failure.http_result.message}"),
                    archive_history_posture=archive_posture,
                    media_modality_posture=known_fact(
                        f"media_asset asset {failure.asset_index:02d} not preserved"
                    ),
                    re_capture_relationship=recapture_posture,
                    limitations=[failure_note],
                    warning_notes=[],
                    preserved_file_ids=[],
                )
            )

        packet_slices.sort(key=lambda item: item.slice_id)
        result = write_local_source_capture_packet(
            output_directory=output_directory,
            input_files=staged_paths,
            source_family=source_family,
            source_surface=source_surface,
            source_locator=source_locator or known_fact("explicit media asset URL set"),
            decision_question=decision_question,
            capture_context=capture_context,
            actor_audience_context=actor_audience_context
            or unknown_with_reason("actor or audience context was not supplied to the media asset runner"),
            capture_mode=capture_mode,
            operator_category=operator_category,
            session_identity=session_id,
            visible_mode_changes=visible_mode_changes,
            source_publication_or_event=packet_timing.source_publication_or_event,
            source_edit_or_version=packet_timing.source_edit_or_version,
            cutoff_posture=packet_timing.cutoff_posture,
            recapture_time=packet_timing.recapture_time,
            access_posture=known_fact(
                f"media_asset preserved {len(batch.successes)} of {len(asset_urls)} explicit asset URL(s)"
            ),
            archive_history_posture=archive_posture,
            media_modality_posture=known_fact(
                f"media_asset preserved {len(batch.successes)} asset body/bodies; "
                f"{len(batch.failures)} asset(s) not preserved"
            ),
            re_capture_relationship=recapture_posture,
            source_slices=packet_slices,
            warnings=packet_warnings,
            limitations=packet_limitations,
            receipt_summary=(
                f"Media asset packet for {source_family} with {len(batch.successes)} preserved "
                f"of {len(asset_urls)} explicit asset URL(s)."
            ),
            receipt_non_claims=MEDIA_ASSET_NON_CLAIMS,
        )
    finally:
        for staging_path in staged_paths:
            try:
                staging_path.unlink()
            except FileNotFoundError:
                pass
    return 0, result.output_directory


def _access_posture_for_success(result: DirectHttpCaptureSuccess):
    if 200 <= result.status < 300:
        return known_fact(f"media_asset direct_http succeeded with HTTP {result.status} {result.reason or 'without reason'}")
    return known_fact(
        f"media_asset access_failed with HTTP {result.status} {result.reason or 'without reason'}; asset body preserved"
    )


def _asset_metadata(asset_index: int, asset_url: str, result: DirectHttpCaptureSuccess) -> dict[str, object]:
    return {
        "asset_index": asset_index,
        "asset_url": asset_url,
        "direct_http_metadata": result.metadata,
    }


def _timing_for_success(
    success: DirectHttpCaptureSuccess,
    *,
    source_publication_or_event,
    source_edit_or_version,
    recapture_time,
    cutoff_posture,
) -> PacketTiming:
    return PacketTiming(
        source_publication_or_event=source_publication_or_event,
        source_edit_or_version=source_edit_or_version,
        capture_time=known_fact(str(success.metadata["capture_timestamp"])),
        recapture_time=recapture_time,
        cutoff_posture=cutoff_posture,
    )


def _timing_for_failure(
    failure: MediaAssetCaptureFailure,
    *,
    source_publication_or_event,
    source_edit_or_version,
    recapture_time,
    cutoff_posture,
) -> PacketTiming:
    return PacketTiming(
        source_publication_or_event=source_publication_or_event,
        source_edit_or_version=source_edit_or_version,
        capture_time=unknown_with_reason(
            f"media asset {failure.asset_index:02d} was not preserved and did not produce response capture timing"
        ),
        recapture_time=recapture_time,
        cutoff_posture=cutoff_posture,
    )


def _format_failure(failure: MediaAssetCaptureFailure) -> str:
    status = f" HTTP {failure.http_result.status}" if failure.http_result.status is not None else ""
    return f"asset {failure.asset_index:02d}{status} {failure.http_result.failure_kind}: {failure.http_result.message}"


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Fetch explicit media/asset URLs and write a Source Capture Packet for preserved asset bodies."
    )
    parser.add_argument("--asset-url", action="append", required=True)
    parser.add_argument("--source-family", default="media_asset")
    parser.add_argument("--source-surface", default="media_asset_explicit_url")
    parser.add_argument("--source-locator", default=None)
    parser.add_argument("--source-locator-unknown-reason", default=None)
    parser.add_argument("--decision-question", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--capture-context",
        default="explicit media asset source capture with Direct HTTP helper",
    )
    parser.add_argument("--operator-category", default="media_asset_cli_operator")
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
        source_locator = build_source_locator(
            source_locator=args.source_locator,
            unknown_reason=args.source_locator_unknown_reason,
        )
        exit_code, message = run_source_capture_media_packet(
            asset_urls=args.asset_url,
            source_family=args.source_family,
            source_surface=args.source_surface,
            decision_question=args.decision_question,
            output_directory=args.output,
            capture_context=args.capture_context,
            operator_category=args.operator_category,
            capture_mode=CaptureModeCategory(args.capture_mode),
            session_id=args.session_id,
            source_locator=source_locator,
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
        parser.exit(status=2, message=f"source capture media asset failed: {exc}\n")
    except Exception as exc:
        parser.exit(status=3, message=f"source capture media asset failed: {exc}\n")

    if exit_code == 0:
        print(message)
        return 0

    parser.exit(status=exit_code, message=f"source capture media asset failed: {message}\n")
    return exit_code


def build_source_locator(*, source_locator: str | None, unknown_reason: str | None):
    if source_locator is not None:
        return known_fact(source_locator)
    if unknown_reason is not None:
        return unknown_with_reason(unknown_reason)
    return None


if __name__ == "__main__":
    raise SystemExit(main())
