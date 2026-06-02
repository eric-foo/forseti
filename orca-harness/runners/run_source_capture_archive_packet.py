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
    unknown_with_reason,
    write_local_source_capture_packet,
)
from source_capture.adapters import (
    ArchiveOrgCaptureFailure,
    fetch_archive_org_capture,
)
from source_capture.adapters.archive_org import (
    DEFAULT_CDX_ENDPOINT,
    DEFAULT_SNAPSHOT_BASE_URL,
    ArchiveOrgCaptureSuccess,
)
from source_capture.adapters.direct_http import DirectHttpCaptureFailure, DirectHttpCaptureSuccess
from source_capture.cli_support import build_optional_fact


ARCHIVE_ORG_NON_CLAIMS = [
    "not archive completeness proof",
    "not source-state truth proof",
    "not browser automation",
    "not API SDK use",
    "not Archive.org package use",
    "not HTML meaning extraction",
    "not OCR or image analysis",
    "not scraper framework use",
    "not proxy or session injection",
    "not ECR design",
    "not Cleaning implementation",
    "not Judgment scoring",
    "not buyer proof",
    "not commercial-readiness logic",
]


def run_source_capture_archive_packet(
    *,
    original_url: str,
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
    cutoff_timestamp: str | None,
    cdx_endpoint: str,
    snapshot_base_url: str,
    timeout_seconds: float,
    max_bytes: int,
) -> tuple[int, str]:
    capture = fetch_archive_org_capture(
        original_url=original_url,
        cutoff_timestamp=cutoff_timestamp,
        cdx_endpoint=cdx_endpoint,
        snapshot_base_url=snapshot_base_url,
        timeout_seconds=timeout_seconds,
        max_bytes=max_bytes,
    )
    if isinstance(capture, ArchiveOrgCaptureFailure):
        return 3, capture.availability_result.message

    staging_parent = output_directory.parent
    staging_parent.mkdir(parents=True, exist_ok=True)
    staged_paths: list[Path] = []
    packet_warnings = list(warnings)
    packet_limitations = list(limitations)
    packet_slices: list[SourceCaptureSlice] = []

    try:
        availability_path = staging_parent / "archive_availability_metadata.json"
        if availability_path.exists():
            raise ValueError(
                "archive availability staging file already exists in the output parent; clear it before rerunning"
            )
        staged_paths.append(availability_path)
        availability_path.write_text(
            f"{json.dumps(_availability_metadata(capture), indent=2, sort_keys=True)}\n",
            encoding="utf-8",
            newline="\n",
        )

        packet_warnings.extend(capture.availability_result.warning_notes)
        packet_limitations.extend(capture.availability_result.limitation_notes)
        if capture.parse_warning is not None:
            packet_limitations.append(capture.parse_warning)

        packet_timing = PacketTiming(
            source_publication_or_event=source_publication_or_event
            or unknown_with_reason("Archive.org adapter did not infer original source publication or event timing"),
            source_edit_or_version=source_edit_or_version
            or _source_version_from_snapshot(capture),
            capture_time=known_fact(str(capture.availability_result.metadata["capture_timestamp"])),
            recapture_time=recapture_time
            or not_applicable("archive packet did not model an earlier capture by default"),
            cutoff_posture=cutoff_posture
            or _cutoff_posture_from_timestamp(cutoff_timestamp),
        )
        archive_posture = _archive_posture(capture)
        recapture_posture = re_capture_relationship or not_applicable(
            "no prior source capture packet was supplied for this archive capture"
        )

        packet_slices.append(
            SourceCaptureSlice(
                slice_id="archive_availability",
                locator=known_fact(capture.availability_url),
                timing=_availability_timing(packet_timing=packet_timing),
                access_posture=_access_posture_for_success(
                    prefix="archive_org availability",
                    result=capture.availability_result,
                ),
                archive_history_posture=archive_posture,
                media_modality_posture=not_applicable("archive availability metadata is not a media asset"),
                re_capture_relationship=recapture_posture,
                limitations=list(capture.availability_result.limitation_notes)
                + ([capture.parse_warning] if capture.parse_warning is not None else []),
                warning_notes=list(capture.availability_result.warning_notes),
                preserved_file_ids=["file_01"],
            )
        )

        body_file_ids: list[str] = []
        if isinstance(capture.body_result, DirectHttpCaptureSuccess):
            body_path = staging_parent / "archive_snapshot_body.bin"
            body_metadata_path = staging_parent / "archive_snapshot_body_metadata.json"
            if body_path.exists() or body_metadata_path.exists():
                raise ValueError(
                    "archive snapshot body staging files already exist in the output parent; clear them before rerunning"
                )
            staged_paths.extend([body_path, body_metadata_path])
            body_path.write_bytes(capture.body_result.body)
            body_metadata_path.write_text(
                f"{json.dumps(_body_metadata(capture), indent=2, sort_keys=True)}\n",
                encoding="utf-8",
                newline="\n",
            )
            body_file_ids = ["file_02", "file_03"]
            packet_warnings.extend(capture.body_result.warning_notes)
            packet_limitations.extend(capture.body_result.limitation_notes)

        if capture.selected_snapshot is not None:
            packet_slices.append(
                SourceCaptureSlice(
                    slice_id="archive_snapshot_body",
                    locator=known_fact(capture.selected_snapshot.snapshot_url),
                    timing=_body_timing(capture, packet_timing=packet_timing),
                    access_posture=_body_access_posture(capture.body_result),
                    archive_history_posture=_body_archive_posture(capture),
                    media_modality_posture=not_applicable("archive snapshot body is preserved as raw response body"),
                    re_capture_relationship=recapture_posture,
                    limitations=_body_limitations(capture.body_result),
                    warning_notes=_body_warnings(capture.body_result),
                    preserved_file_ids=body_file_ids,
                )
            )
            if isinstance(capture.body_result, DirectHttpCaptureFailure):
                packet_limitations.append(f"archive_snapshot_body_not_preserved: {capture.body_result.message}")

        result = write_local_source_capture_packet(
            output_directory=output_directory,
            input_files=staged_paths,
            source_family=source_family,
            source_surface=source_surface,
            source_locator=known_fact(capture.original_url),
            decision_question=decision_question,
            capture_context=capture_context,
            actor_audience_context=actor_audience_context
            or unknown_with_reason("actor or audience context was not supplied to the archive runner"),
            capture_mode=capture_mode,
            operator_category=operator_category,
            session_identity=session_id,
            visible_mode_changes=visible_mode_changes,
            source_publication_or_event=packet_timing.source_publication_or_event,
            source_edit_or_version=packet_timing.source_edit_or_version,
            cutoff_posture=packet_timing.cutoff_posture,
            recapture_time=packet_timing.recapture_time,
            access_posture=_packet_access_posture(capture),
            archive_history_posture=archive_posture,
            media_modality_posture=not_applicable("archive runner does not retrieve linked media assets"),
            re_capture_relationship=recapture_posture,
            source_slices=packet_slices,
            warnings=packet_warnings,
            limitations=packet_limitations,
            receipt_summary=_receipt_summary(capture),
            receipt_non_claims=ARCHIVE_ORG_NON_CLAIMS,
        )
    finally:
        for staging_path in staged_paths:
            try:
                staging_path.unlink()
            except FileNotFoundError:
                pass
    return 0, result.output_directory


def _availability_metadata(capture: ArchiveOrgCaptureSuccess) -> dict[str, object]:
    return {
        "original_url": capture.original_url,
        "availability_url": capture.availability_url,
        "availability_http_metadata": capture.availability_result.metadata,
        "snapshot_count": len(capture.snapshots),
        "selected_snapshot": _snapshot_metadata(capture.selected_snapshot),
        "snapshots": [_snapshot_metadata(snapshot) for snapshot in capture.snapshots],
        "parse_warning": capture.parse_warning,
    }


def _body_metadata(capture: ArchiveOrgCaptureSuccess) -> dict[str, object]:
    if not isinstance(capture.body_result, DirectHttpCaptureSuccess):
        raise ValueError("archive snapshot body metadata requires a preserved body")
    return {
        "original_url": capture.original_url,
        "selected_snapshot": _snapshot_metadata(capture.selected_snapshot),
        "snapshot_body_http_metadata": capture.body_result.metadata,
    }


def _snapshot_metadata(snapshot) -> dict[str, object] | None:
    if snapshot is None:
        return None
    return {
        "timestamp": snapshot.timestamp,
        "original_url": snapshot.original_url,
        "snapshot_url": snapshot.snapshot_url,
        "status_code": snapshot.status_code,
        "mime_type": snapshot.mime_type,
        "digest": snapshot.digest,
    }


def _source_version_from_snapshot(capture: ArchiveOrgCaptureSuccess):
    if capture.selected_snapshot is None:
        return unknown_with_reason("no Archive.org snapshot was selected")
    return known_fact(f"Archive.org snapshot timestamp {capture.selected_snapshot.timestamp}")


def _cutoff_posture_from_timestamp(cutoff_timestamp: str | None):
    if cutoff_timestamp is None:
        return unknown_with_reason("archive runner did not receive a cutoff timestamp")
    return known_fact(f"Archive.org snapshot selection constrained at or before {cutoff_timestamp}")


def _archive_posture(capture: ArchiveOrgCaptureSuccess):
    if capture.parse_warning is not None:
        return known_fact("archive_org availability metadata preserved but could not be parsed")
    if capture.selected_snapshot is None:
        return known_fact("archive_org availability metadata preserved; no eligible snapshot selected")
    if isinstance(capture.body_result, DirectHttpCaptureSuccess):
        return known_fact(
            f"archive_org availability metadata preserved; snapshot body preserved for {capture.selected_snapshot.timestamp}"
        )
    return known_fact(
        f"archive_org availability metadata preserved; snapshot body not preserved for {capture.selected_snapshot.timestamp}"
    )


def _access_posture_for_success(*, prefix: str, result: DirectHttpCaptureSuccess):
    if 200 <= result.status < 300:
        return known_fact(f"{prefix} direct_http succeeded with HTTP {result.status} {result.reason or 'without reason'}")
    return known_fact(
        f"{prefix} access_failed with HTTP {result.status} {result.reason or 'without reason'}; response body preserved"
    )


def _body_access_posture(result: DirectHttpCaptureSuccess | DirectHttpCaptureFailure | None):
    if isinstance(result, DirectHttpCaptureSuccess):
        return _access_posture_for_success(prefix="archive_org snapshot body", result=result)
    if isinstance(result, DirectHttpCaptureFailure):
        return known_fact(f"archive_org snapshot body access_failed: {result.message}")
    return not_applicable("no Archive.org snapshot was selected for body retrieval")


def _body_archive_posture(capture: ArchiveOrgCaptureSuccess):
    if capture.selected_snapshot is None:
        return not_applicable("no Archive.org snapshot was selected")
    if isinstance(capture.body_result, DirectHttpCaptureSuccess):
        return known_fact(f"archive_org snapshot body preserved for {capture.selected_snapshot.timestamp}")
    return known_fact(f"archive_org snapshot body not preserved for {capture.selected_snapshot.timestamp}")


def _body_timing(capture: ArchiveOrgCaptureSuccess, *, packet_timing: PacketTiming) -> PacketTiming:
    if isinstance(capture.body_result, DirectHttpCaptureSuccess):
        capture_time = known_fact(str(capture.body_result.metadata["capture_timestamp"]))
    else:
        capture_time = unknown_with_reason("archive snapshot body was not preserved and did not produce response capture timing")
    return PacketTiming(
        source_publication_or_event=packet_timing.source_publication_or_event,
        source_edit_or_version=packet_timing.source_edit_or_version,
        capture_time=capture_time,
        recapture_time=packet_timing.recapture_time,
        cutoff_posture=packet_timing.cutoff_posture,
    )


def _availability_timing(*, packet_timing: PacketTiming) -> PacketTiming:
    return PacketTiming(
        source_publication_or_event=packet_timing.source_publication_or_event,
        source_edit_or_version=known_fact(
            "Archive.org availability metadata for the requested original URL; selected snapshot timestamp is recorded separately"
        ),
        capture_time=packet_timing.capture_time,
        recapture_time=packet_timing.recapture_time,
        cutoff_posture=packet_timing.cutoff_posture,
    )


def _body_limitations(result: DirectHttpCaptureSuccess | DirectHttpCaptureFailure | None) -> list[str]:
    if isinstance(result, DirectHttpCaptureSuccess):
        return list(result.limitation_notes)
    if isinstance(result, DirectHttpCaptureFailure):
        return [result.message]
    return []


def _body_warnings(result: DirectHttpCaptureSuccess | DirectHttpCaptureFailure | None) -> list[str]:
    if isinstance(result, DirectHttpCaptureSuccess):
        return list(result.warning_notes)
    return []


def _packet_access_posture(capture: ArchiveOrgCaptureSuccess):
    if capture.selected_snapshot is None:
        return known_fact("archive_org availability metadata preserved; no eligible snapshot body requested")
    if isinstance(capture.body_result, DirectHttpCaptureSuccess):
        return known_fact("archive_org availability metadata and selected snapshot body preserved")
    return known_fact("archive_org availability metadata preserved; selected snapshot body access_failed")


def _receipt_summary(capture: ArchiveOrgCaptureSuccess) -> str:
    if capture.selected_snapshot is None:
        return "Archive.org packet with availability metadata preserved and no eligible snapshot body."
    if isinstance(capture.body_result, DirectHttpCaptureSuccess):
        return (
            f"Archive.org packet with availability metadata and snapshot body preserved "
            f"for {capture.selected_snapshot.timestamp}."
        )
    return (
        f"Archive.org packet with availability metadata preserved and snapshot body not preserved "
        f"for {capture.selected_snapshot.timestamp}."
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Query Archive.org-style availability metadata and write a Source Capture Packet."
    )
    parser.add_argument("--url", required=True)
    parser.add_argument("--cutoff-timestamp", default=None)
    parser.add_argument("--cdx-endpoint", default=DEFAULT_CDX_ENDPOINT)
    parser.add_argument("--snapshot-base-url", default=DEFAULT_SNAPSHOT_BASE_URL)
    parser.add_argument("--source-family", default="archive_org")
    parser.add_argument("--source-surface", default="archive_org_wayback")
    parser.add_argument("--decision-question", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--capture-context",
        default="Archive.org availability/body source capture with Direct HTTP helper",
    )
    parser.add_argument("--operator-category", default="archive_org_cli_operator")
    parser.add_argument(
        "--capture-mode",
        choices=[item.value for item in CaptureModeCategory],
        default=CaptureModeCategory.ARCHIVE_HISTORY.value,
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
        exit_code, message = run_source_capture_archive_packet(
            original_url=args.url,
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
            cutoff_timestamp=args.cutoff_timestamp,
            cdx_endpoint=args.cdx_endpoint,
            snapshot_base_url=args.snapshot_base_url,
            timeout_seconds=args.timeout_seconds,
            max_bytes=args.max_bytes,
        )
    except ValueError as exc:
        parser.exit(status=2, message=f"source capture Archive.org failed: {exc}\n")
    except Exception as exc:
        parser.exit(status=3, message=f"source capture Archive.org failed: {exc}\n")

    if exit_code == 0:
        print(message)
        return 0

    parser.exit(status=exit_code, message=f"source capture Archive.org failed: {message}\n")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
