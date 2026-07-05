from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from harness_utils import generate_ulid
from source_capture import (
    CaptureModeCategory,
    PacketTiming,
    SourceCaptureSlice,
    VisibleFact,
    known_fact,
    not_applicable,
    unknown_with_reason,
    write_local_source_capture_packet,
)

if TYPE_CHECKING:
    from data_lake.root import DataLakeRoot

from source_capture.adapters.archive_org import (
    DEFAULT_CDX_ENDPOINT,
    DEFAULT_MAX_ATTEMPTS,
    DEFAULT_RETRY_BACKOFF_SECONDS,
    DEFAULT_SNAPSHOT_BASE_URL,
    ArchiveOrgCaptureSuccess,
)
from source_capture.adapters.archive_today import (
    DEFAULT_TIMEMAP_BASE_URL,
    ArchiveTodayCaptureSuccess,
)
from source_capture.adapters.direct_http import DirectHttpCaptureSuccess
from source_capture.adapters.publisher_history import PublisherHistoryCaptureSuccess
from source_capture.cli_support import build_optional_fact
from source_capture.historical_capture import (
    GitHubRung,
    HistoricalCaptureResult,
    MediaWikiRung,
    PublisherHistoryRung,
    RungOutcome,
    fetch_historical_capture,
)


HISTORICAL_NON_CLAIMS = [
    "not archive completeness proof",
    "not source-state truth proof",
    "not cross-archive coverage proof",
    "not browser automation",
    "not API SDK use",
    "not archive package use",
    "not gate-defeat (auth/CAPTCHA/Cloudflare-challenge solving)",
    "not HTML meaning extraction",
    "not OCR or image analysis",
    "not scraper framework use",
    "not proxy or session injection",
    "not ECR design",
    "not Cleaning implementation",
    "not Judgment scoring",
    "not source-quality admission verdict",
    "not buyer proof",
    "not commercial-readiness logic",
]


def run_source_capture_historical_packet(
    *,
    original_url: str,
    decision_question: str,
    output_directory: Path | None = None,
    data_root: "DataLakeRoot | None" = None,
    source_family: str,
    source_surface: str | None,
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
    cutoff_timestamp_iso: str | None,
    include_archive_today: bool,
    publisher_history_rung: PublisherHistoryRung | None,
    wayback_cdx_endpoint: str,
    wayback_snapshot_base_url: str,
    archive_today_timemap_base_url: str,
    archive_today_hosts: frozenset[str] | None,
    timeout_seconds: float,
    max_bytes: int,
    max_attempts: int = DEFAULT_MAX_ATTEMPTS,
    retry_backoff_seconds: float = DEFAULT_RETRY_BACKOFF_SECONDS,
) -> tuple[int, str]:
    if (output_directory is None) == (data_root is None):
        raise ValueError("exactly one of output_directory or data_root is required")

    capture = fetch_historical_capture(
        original_url=original_url,
        cutoff_timestamp_iso=cutoff_timestamp_iso,
        include_archive_today=include_archive_today,
        publisher_history_rung=publisher_history_rung,
        wayback_cdx_endpoint=wayback_cdx_endpoint,
        wayback_snapshot_base_url=wayback_snapshot_base_url,
        archive_today_timemap_base_url=archive_today_timemap_base_url,
        archive_today_hosts=archive_today_hosts,
        timeout_seconds=timeout_seconds,
        max_bytes=max_bytes,
        max_attempts=max_attempts,
        retry_backoff_seconds=retry_backoff_seconds,
    )

    payload = _selected_payload(capture.selected_outcome)
    verified = payload is not None

    staging_root: Path | None = None
    if data_root is not None:
        staging_parent = data_root.stage_raw_packet(generate_ulid())
        staging_root = staging_parent
    else:
        assert output_directory is not None
        staging_parent = output_directory.parent
        staging_parent.mkdir(parents=True, exist_ok=True)
    staged_paths: list[Path] = []
    packet_warnings = list(warnings)
    packet_limitations = list(limitations)
    packet_slices: list[SourceCaptureSlice] = []

    try:
        # The thin ladder receipt -- always preserved (the cross-archive locate trace is the packet's
        # core value, and guarantees >=1 preserved file even on an honest NO-GO). NEUTRAL FACTS only.
        locate_path = staging_parent / "archive_locate_metadata.json"
        if locate_path.exists():
            raise ValueError(
                "archive locate staging file already exists in the output parent; clear it before rerunning"
            )
        staged_paths.append(locate_path)
        locate_path.write_text(
            f"{json.dumps(_locate_metadata(capture), indent=2, sort_keys=True)}\n",
            encoding="utf-8",
            newline="\n",
        )

        packet_timing = _packet_timing(
            capture,
            payload=payload,
            cutoff_timestamp_iso=cutoff_timestamp_iso,
            source_publication_or_event=source_publication_or_event,
            source_edit_or_version=source_edit_or_version,
            cutoff_posture=cutoff_posture,
            recapture_time=recapture_time,
        )
        recapture_posture = re_capture_relationship or not_applicable(
            "no prior source capture packet was supplied for this historical capture"
        )
        ladder_posture = known_fact("archived") if verified else known_fact("attempt_failed")

        packet_slices.append(
            SourceCaptureSlice(
                slice_id="historical_locate_ladder",
                locator=known_fact(original_url),
                timing=_ladder_timing(packet_timing),
                access_posture=_ladder_access_posture(capture),
                archive_history_posture=ladder_posture,
                media_modality_posture=not_applicable("locate-ladder metadata is not a media asset"),
                re_capture_relationship=recapture_posture,
                limitations=_ladder_limitations(capture),
                warning_notes=[],
                preserved_file_ids=["file_01"],
            )
        )

        body_file_ids: list[str] = []
        if verified:
            assert payload is not None
            body_path = staging_parent / "historical_capture_body.bin"
            body_metadata_path = staging_parent / "historical_capture_body_metadata.json"
            if body_path.exists() or body_metadata_path.exists():
                raise ValueError(
                    "historical capture body staging files already exist in the output parent; clear them before rerunning"
                )
            staged_paths.extend([body_path, body_metadata_path])
            body_path.write_bytes(payload["body"])
            body_metadata_path.write_text(
                f"{json.dumps(_body_metadata(capture, payload), indent=2, sort_keys=True)}\n",
                encoding="utf-8",
                newline="\n",
            )
            body_file_ids = ["file_02", "file_03"]

            packet_slices.append(
                SourceCaptureSlice(
                    slice_id="historical_capture_body",
                    locator=known_fact(str(payload["locator"])),
                    timing=_body_timing(packet_timing, payload=payload),
                    access_posture=known_fact(
                        f"{capture.archive_selected} verified pre-cutoff body preserved "
                        f"(served {payload['served_timestamp_native']})"
                    ),
                    archive_history_posture=known_fact("archived"),
                    media_modality_posture=not_applicable(
                        "historical capture body is preserved as raw response body"
                    ),
                    re_capture_relationship=recapture_posture,
                    limitations=[],
                    warning_notes=[],
                    preserved_file_ids=body_file_ids,
                )
            )

        packet_limitations.extend(_ladder_limitations(capture))
        if not verified:
            packet_limitations.append(
                "historical_capture_no_go: cross-archive locate ladder exhausted with no verified "
                "pre-cutoff body; locate trace preserved (archive_locate_metadata.json)"
            )

        result = write_local_source_capture_packet(
            output_directory=output_directory,
            data_root=data_root,
            input_files=staged_paths,
            source_family=source_family,
            source_surface=source_surface or f"cross_archive::{capture.archive_selected or 'no_go'}",
            source_locator=known_fact(original_url),
            decision_question=decision_question,
            capture_context=capture_context,
            actor_audience_context=actor_audience_context
            or unknown_with_reason("actor or audience context was not supplied to the historical runner"),
            capture_mode=capture_mode,
            operator_category=operator_category,
            session_identity=session_id,
            visible_mode_changes=visible_mode_changes,
            source_publication_or_event=packet_timing.source_publication_or_event,
            source_edit_or_version=packet_timing.source_edit_or_version,
            cutoff_posture=packet_timing.cutoff_posture,
            recapture_time=packet_timing.recapture_time,
            archive_snapshot_time=packet_timing.archive_snapshot_time,
            access_posture=_ladder_access_posture(capture),
            archive_history_posture=known_fact("archived") if verified else known_fact("attempt_failed"),
            media_modality_posture=not_applicable("historical runner does not retrieve linked media assets"),
            re_capture_relationship=recapture_posture,
            source_slices=packet_slices,
            warnings=packet_warnings,
            limitations=packet_limitations,
            receipt_summary=_receipt_summary(capture, payload),
            receipt_non_claims=HISTORICAL_NON_CLAIMS,
        )
    finally:
        for staging_path in staged_paths:
            try:
                staging_path.unlink()
            except FileNotFoundError:
                pass
        if staging_root is not None:
            shutil.rmtree(staging_root, ignore_errors=True)
    return 0, result.output_directory


# --------------------------------------------------------------------------------------------------
# Selected-rung body extraction (per-rung branching -- the runner side of the no-uniform-protocol rule)
# --------------------------------------------------------------------------------------------------


def _selected_payload(outcome: RungOutcome | None) -> dict[str, object] | None:
    """Extract body bytes + locator + served timestamp from the selected rung's raw result.

    Returns ``None`` when there is no verified body (NO-GO). A verified ``RungOutcome`` always carries
    a ``DirectHttpCaptureSuccess`` body on its result, so the body bytes are present.
    """
    if outcome is None or not outcome.verified_body:
        return None
    result = outcome.result
    if isinstance(result, ArchiveOrgCaptureSuccess):
        body = result.body_result
        assert isinstance(body, DirectHttpCaptureSuccess)
        snapshot = result.selected_snapshot
        assert snapshot is not None
        served_native = (
            result.body_verification.served_timestamp
            if result.body_verification is not None and result.body_verification.served_timestamp
            else snapshot.timestamp
        )
        return {
            "rung": outcome.rung,
            "body": body.body,
            "locator": snapshot.snapshot_url,
            "served_timestamp_native": served_native,
            "served_timestamp_iso": _wayback_to_iso(served_native),
            "identity": None,
            "http_metadata": body.metadata,
        }
    if isinstance(result, ArchiveTodayCaptureSuccess):
        body = result.body_result
        assert isinstance(body, DirectHttpCaptureSuccess)
        memento = result.selected_memento
        assert memento is not None
        served_native = (
            result.body_verification.served_timestamp
            if result.body_verification is not None and result.body_verification.served_timestamp
            else memento.timestamp
        )
        return {
            "rung": outcome.rung,
            "body": body.body,
            "locator": memento.memento_url,
            "served_timestamp_native": served_native,
            "served_timestamp_iso": _wayback_to_iso(served_native),
            "identity": None,
            "http_metadata": body.metadata,
        }
    if isinstance(result, PublisherHistoryCaptureSuccess):
        body = result.body_result
        assert isinstance(body, DirectHttpCaptureSuccess)
        revision = result.selected_revision
        assert revision is not None
        return {
            "rung": outcome.rung,
            "body": body.body,
            "locator": revision.content_url,
            "served_timestamp_native": revision.served_timestamp,
            "served_timestamp_iso": revision.served_timestamp,  # publisher-history is already ISO-8601 Z
            "identity": revision.identity,
            "http_metadata": body.metadata,
        }
    return None


# --------------------------------------------------------------------------------------------------
# Neutral locate-ladder receipt (INV-1)
# --------------------------------------------------------------------------------------------------


def _locate_metadata(capture: HistoricalCaptureResult) -> dict[str, object]:
    return {
        "original_url": capture.original_url,
        "cutoff_timestamp": capture.cutoff_timestamp_iso,
        "archive_selected": capture.archive_selected,
        "body_rung_used": _body_rung_used(capture.selected_outcome),
        "archives_tried": [
            {
                "rung": outcome.rung,
                "located": outcome.located,
                "verified_body": outcome.verified_body,
                "selected_timestamp": outcome.selected_timestamp,
                "locate_detail": outcome.locate_detail,
                "body_detail": outcome.body_detail,
                "gate_defeat_stop": outcome.gate_defeat_stop,
            }
            for outcome in capture.archives_tried
        ],
    }


def _body_rung_used(outcome: RungOutcome | None) -> str | None:
    if outcome is None or not outcome.verified_body:
        return None
    return "direct_http"


def _ladder_limitations(capture: HistoricalCaptureResult) -> list[str]:
    notes: list[str] = []
    for outcome in capture.archives_tried:
        if capture.archive_selected == outcome.rung and outcome.verified_body:
            continue  # the selected, verified rung is not a limitation
        note = f"historical_ladder[{outcome.rung}]: {outcome.locate_detail}; {outcome.body_detail}"
        if outcome.gate_defeat_stop is not None:
            note += f"; gate_defeat_stop={outcome.gate_defeat_stop}"
        notes.append(note)
    return notes


# --------------------------------------------------------------------------------------------------
# Timing / posture / receipt
# --------------------------------------------------------------------------------------------------


def _packet_timing(
    capture: HistoricalCaptureResult,
    *,
    payload: dict[str, object] | None,
    cutoff_timestamp_iso: str | None,
    source_publication_or_event,
    source_edit_or_version,
    cutoff_posture,
    recapture_time,
) -> PacketTiming:
    if payload is not None:
        capture_time = known_fact(str(payload["http_metadata"].get("capture_timestamp")))  # type: ignore[union-attr]
        archive_snapshot_time = known_fact(str(payload["served_timestamp_iso"]))
        default_edit = known_fact(
            f"{capture.archive_selected} served {payload['served_timestamp_native']}"
        )
    else:
        capture_time = unknown_with_reason(
            "no verified body retrieved across the cross-archive locate ladder"
        )
        archive_snapshot_time = unknown_with_reason(
            "no pre-cutoff snapshot/revision yielded a verified body across the locate ladder"
        )
        default_edit = unknown_with_reason("no archive selected across the locate ladder")
    return PacketTiming(
        source_publication_or_event=source_publication_or_event
        or unknown_with_reason("historical orchestrator did not infer original source publication or event timing"),
        source_edit_or_version=source_edit_or_version or default_edit,
        capture_time=capture_time,
        archive_snapshot_time=archive_snapshot_time,
        recapture_time=recapture_time
        or not_applicable("historical packet did not model an earlier capture by default"),
        cutoff_posture=cutoff_posture or _cutoff_posture(cutoff_timestamp_iso),
    )


def _ladder_timing(packet_timing: PacketTiming) -> PacketTiming:
    return PacketTiming(
        source_publication_or_event=packet_timing.source_publication_or_event,
        source_edit_or_version=known_fact(
            "cross-archive locate ladder trace for the requested original URL; the selected archive "
            "and served timestamp are recorded separately"
        ),
        capture_time=packet_timing.capture_time,
        archive_snapshot_time=packet_timing.archive_snapshot_time,
        recapture_time=packet_timing.recapture_time,
        cutoff_posture=packet_timing.cutoff_posture,
    )


def _body_timing(packet_timing: PacketTiming, *, payload: dict[str, object]) -> PacketTiming:
    return PacketTiming(
        source_publication_or_event=packet_timing.source_publication_or_event,
        source_edit_or_version=packet_timing.source_edit_or_version,
        capture_time=known_fact(str(payload["http_metadata"].get("capture_timestamp"))),  # type: ignore[union-attr]
        archive_snapshot_time=known_fact(str(payload["served_timestamp_iso"])),
        recapture_time=packet_timing.recapture_time,
        cutoff_posture=packet_timing.cutoff_posture,
    )


def _ladder_access_posture(capture: HistoricalCaptureResult) -> VisibleFact:
    if capture.archive_selected is not None:
        return known_fact(
            f"cross-archive locate ladder selected {capture.archive_selected}; verified pre-cutoff "
            "body preserved; full ladder trace preserved in archive_locate_metadata.json"
        )
    return known_fact(
        "cross-archive locate ladder exhausted with no verified pre-cutoff body (NO-GO); "
        "locate trace preserved in archive_locate_metadata.json"
    )


def _cutoff_posture(cutoff_timestamp_iso: str | None) -> VisibleFact:
    if cutoff_timestamp_iso is None:
        return unknown_with_reason("historical runner did not receive a cutoff timestamp")
    return known_fact("pre_cutoff")


def _receipt_summary(capture: HistoricalCaptureResult, payload: dict[str, object] | None) -> str:
    tried = ", ".join(outcome.rung for outcome in capture.archives_tried)
    if payload is not None:
        return (
            f"Cross-archive historical capture: ladder tried [{tried}]; selected "
            f"{capture.archive_selected}; verified pre-cutoff body preserved "
            f"(served {payload['served_timestamp_native']})."
        )
    return (
        f"Cross-archive historical capture: ladder tried [{tried}]; NO-GO -- no verified pre-cutoff "
        f"body across the ladder; locate trace preserved."
    )


def _body_metadata(capture: HistoricalCaptureResult, payload: dict[str, object]) -> dict[str, object]:
    return {
        "original_url": capture.original_url,
        "archive_selected": capture.archive_selected,
        "selected_locator": payload["locator"],
        "served_timestamp_native": payload["served_timestamp_native"],
        "served_timestamp_iso": payload["served_timestamp_iso"],
        "selected_identity": payload["identity"],
        "body_http_metadata": payload["http_metadata"],
    }


def _wayback_to_iso(raw: str) -> str | None:
    # 14-digit Wayback/archive.today form -> ISO-8601 UTC "...Z". None if not a parseable 14-digit ts.
    if len(raw) != 14 or not raw.isdigit():
        return None
    try:
        parsed = datetime.strptime(raw, "%Y%m%d%H%M%S")
    except ValueError:
        return None
    return parsed.strftime("%Y-%m-%dT%H:%M:%SZ")


# --------------------------------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------------------------------


def _publisher_history_rung_from_args(args: argparse.Namespace) -> PublisherHistoryRung | None:
    has_mediawiki = bool(args.mediawiki_api_base or args.mediawiki_title)
    has_github = bool(args.github_owner or args.github_repo or args.github_path)
    if has_mediawiki and has_github:
        raise ValueError("supply only one publisher-history rung: MediaWiki OR GitHub, not both")
    if has_mediawiki:
        if not (args.mediawiki_api_base and args.mediawiki_title):
            raise ValueError("MediaWiki publisher-history rung requires --mediawiki-api-base and --mediawiki-title")
        return MediaWikiRung(wiki_api_base=args.mediawiki_api_base, title=args.mediawiki_title)
    if has_github:
        if not (args.github_owner and args.github_repo and args.github_path):
            raise ValueError(
                "GitHub publisher-history rung requires --github-owner, --github-repo and --github-path"
            )
        return GitHubRung(owner=args.github_owner, repo=args.github_repo, path=args.github_path)
    return None


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Run the cross-archive historical-capture locate ladder (Wayback -> archive.today -> "
            "publisher-history) and write a Source Capture Packet with a locate-ladder receipt."
        )
    )
    parser.add_argument("--url", required=True)
    parser.add_argument("--cutoff-timestamp", default=None, help="ISO-8601 cutoff (e.g. 2024-06-01T00:00:00Z)")
    parser.add_argument("--decision-question", required=True)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument(
        "--data-root",
        default=None,
        help="Commit into the Forseti data lake at this root; explicit --data-root is mutually exclusive with --output. FORSETI_DATA_ROOT is used only when --output is omitted; legacy ORCA_DATA_ROOT is also accepted.",
    )
    parser.add_argument("--source-family", default="historical_capture")
    parser.add_argument("--source-surface", default=None)
    parser.add_argument(
        "--capture-context",
        default="Cross-archive historical-capture locate ladder with Direct HTTP helper",
    )
    parser.add_argument("--operator-category", default="historical_capture_cli_operator")
    parser.add_argument(
        "--capture-mode",
        choices=[item.value for item in CaptureModeCategory],
        default=CaptureModeCategory.ARCHIVE_HISTORY.value,
    )
    parser.add_argument("--session-id", default=None)
    # Ladder controls.
    parser.add_argument("--no-archive-today", action="store_true", help="skip the archive.today rung")
    parser.add_argument("--mediawiki-api-base", default=None)
    parser.add_argument("--mediawiki-title", default=None)
    parser.add_argument("--github-owner", default=None)
    parser.add_argument("--github-repo", default=None)
    parser.add_argument("--github-path", default=None)
    # Endpoint overrides (production: a specific mirror/proxy; tests: a local fake server).
    parser.add_argument("--wayback-cdx-endpoint", default=DEFAULT_CDX_ENDPOINT)
    parser.add_argument("--wayback-snapshot-base-url", default=DEFAULT_SNAPSHOT_BASE_URL)
    parser.add_argument("--archive-today-timemap-base-url", default=DEFAULT_TIMEMAP_BASE_URL)
    parser.add_argument(
        "--archive-today-host",
        action="append",
        default=[],
        help="extra host accepted as an archive.today mirror (repeatable); empty => the built-in family",
    )
    parser.add_argument("--timeout-seconds", type=float, default=20.0)
    parser.add_argument("--max-bytes", type=int, default=5_000_000)
    parser.add_argument("--max-attempts", type=int, default=DEFAULT_MAX_ATTEMPTS)
    parser.add_argument("--retry-backoff-seconds", type=float, default=DEFAULT_RETRY_BACKOFF_SECONDS)
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
        publisher_history_rung = _publisher_history_rung_from_args(args)
        archive_today_hosts = frozenset(args.archive_today_host) if args.archive_today_host else None
        data_root = None
        data_root_requested = args.data_root is not None or (args.output is None and (os.environ.get("FORSETI_DATA_ROOT") or os.environ.get("ORCA_DATA_ROOT")))
        if args.output is not None and args.data_root is not None:
            parser.exit(
                status=2,
                message="source capture historical failed: exactly one of --output or --data-root/FORSETI_DATA_ROOT/ORCA_DATA_ROOT is required\n",
            )
        if args.output is None and not data_root_requested:
            parser.exit(
                status=2,
                message="source capture historical failed: exactly one of --output or --data-root/FORSETI_DATA_ROOT/ORCA_DATA_ROOT is required\n",
            )
        if data_root_requested:
            from data_lake.root import DataLakeRoot

            data_root = DataLakeRoot.resolve(explicit=args.data_root)
        exit_code, message = run_source_capture_historical_packet(
            original_url=args.url,
            decision_question=args.decision_question,
            output_directory=args.output if data_root is None else None,
            data_root=data_root,
            source_family=args.source_family,
            source_surface=args.source_surface,
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
            cutoff_timestamp_iso=args.cutoff_timestamp,
            include_archive_today=not args.no_archive_today,
            publisher_history_rung=publisher_history_rung,
            wayback_cdx_endpoint=args.wayback_cdx_endpoint,
            wayback_snapshot_base_url=args.wayback_snapshot_base_url,
            archive_today_timemap_base_url=args.archive_today_timemap_base_url,
            archive_today_hosts=archive_today_hosts,
            timeout_seconds=args.timeout_seconds,
            max_bytes=args.max_bytes,
            max_attempts=args.max_attempts,
            retry_backoff_seconds=args.retry_backoff_seconds,
        )
    except ValueError as exc:
        parser.exit(status=2, message=f"source capture historical failed: {exc}\n")
    except Exception as exc:  # noqa: BLE001 -- surface any unexpected failure honestly, non-zero
        parser.exit(status=3, message=f"source capture historical failed: {exc}\n")

    if exit_code == 0:
        print(message)
        return 0

    parser.exit(status=exit_code, message=f"source capture historical failed: {message}\n")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
