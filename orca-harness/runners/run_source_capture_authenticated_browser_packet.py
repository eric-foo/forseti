from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from harness_utils import generate_ulid
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

if TYPE_CHECKING:
    from data_lake.root import DataLakeRoot

from source_capture.adapters import BrowserSnapshotFailure, fetch_browser_snapshot_capture
from source_capture.adapters.browser_snapshot import (
    ALLOWED_WAIT_UNTIL,
    DEFAULT_MAX_ARTIFACT_BYTES,
    DEFAULT_TIMEOUT_SECONDS,
    DEFAULT_VIEWPORT_HEIGHT,
    DEFAULT_VIEWPORT_WIDTH,
)
from source_capture.auth_state import AuthenticatedSessionMode, validate_auth_state_session_mode
from source_capture.cli_support import build_optional_fact


AUTHENTICATED_BROWSER_SNAPSHOT_NON_CLAIMS = [
    "not password-driven login automation",
    "not credential capture or storage",
    "not storage-state preservation",
    "not cookie or session export",
    "not undisclosed session use",
    "not no-entitlement bypass",
    "not login-wall absence proof",
    "not content sufficiency proof",
    "not anti-detect behavior",
    "not proxy behavior",
    "not CAPTCHA solving",
    "not crawler or source discovery",
    "not API SDK use",
    "not OCR or image analysis",
    "not ECR design",
    "not Cleaning implementation",
    "not Judgment scoring",
    "not buyer proof",
    "not commercial-readiness logic",
]


def run_source_capture_authenticated_browser_packet(
    *,
    url: str,
    state_label: str,
    session_mode: AuthenticatedSessionMode,
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
    wait_until: str,
    viewport_width: int,
    viewport_height: int,
    max_artifact_bytes: int,
    auth_state_root: Path | None = None,
) -> tuple[int, str]:
    if (output_directory is None) == (data_root is None):
        raise ValueError("exactly one of output_directory or data_root is required")

    storage_state_path = validate_auth_state_session_mode(
        state_label,
        session_mode=session_mode,
        auth_state_root=auth_state_root,
    )
    capture_result = fetch_browser_snapshot_capture(
        url=url,
        timeout_seconds=timeout_seconds,
        wait_until=wait_until,
        viewport_width=viewport_width,
        viewport_height=viewport_height,
        max_artifact_bytes=max_artifact_bytes,
        storage_state_path=storage_state_path,
    )
    if isinstance(capture_result, BrowserSnapshotFailure):
        return 3, capture_result.message

    packet_warnings = list(warnings) + capture_result.warning_notes
    packet_limitations = list(limitations) + capture_result.limitation_notes
    possible_login_wall_limitation = _possible_login_wall_limitation(
        title=capture_result.title,
        visible_text=capture_result.visible_text,
    )
    if possible_login_wall_limitation is not None:
        packet_limitations.append(possible_login_wall_limitation)

    staging_root: Path | None = None
    if data_root is not None:
        staging_parent = data_root.stage_raw_packet(generate_ulid())
        staging_root = staging_parent
    else:
        assert output_directory is not None
        staging_parent = output_directory.parent
        staging_parent.mkdir(parents=True, exist_ok=True)
    staged_paths = [
        staging_parent / "authenticated_browser_rendered_dom.html",
        staging_parent / "authenticated_browser_visible_text.txt",
        staging_parent / "authenticated_browser_viewport_screenshot.png",
        staging_parent / "authenticated_browser_snapshot_metadata.json",
    ]
    if any(path.exists() for path in staged_paths):
        raise ValueError(
            "authenticated browser snapshot staging files already exist in the output parent; clear them before rerunning"
        )

    written_paths: list[Path] = []
    try:
        _write_text(staged_paths[0], capture_result.rendered_dom)
        written_paths.append(staged_paths[0])
        _write_text(staged_paths[1], capture_result.visible_text)
        written_paths.append(staged_paths[1])
        staged_paths[2].write_bytes(capture_result.screenshot_png)
        written_paths.append(staged_paths[2])
        _write_text(staged_paths[3], json.dumps(capture_result.metadata, indent=2, sort_keys=True))
        written_paths.append(staged_paths[3])

        timing = PacketTiming(
            source_publication_or_event=source_publication_or_event
            or unknown_with_reason(
                "authenticated browser snapshot adapter did not infer source publication or event timing"
            ),
            source_edit_or_version=source_edit_or_version
            or unknown_with_reason(
                "authenticated browser snapshot adapter did not infer source edit or version timing"
            ),
            capture_time=known_fact(str(capture_result.metadata["capture_timestamp"])),
            recapture_time=recapture_time
            or not_applicable("authenticated browser snapshot packet did not model an earlier capture by default"),
            cutoff_posture=cutoff_posture
            or unknown_with_reason("authenticated browser snapshot runner did not receive cutoff posture metadata"),
        )
        archive_posture = not_attempted(
            "authenticated browser snapshot adapter does not query archive or history services"
        )
        media_posture = known_fact(
            "authenticated_browser_snapshot preserved a viewport screenshot; linked media files were not independently preserved"
        )
        access_posture = known_fact(
            f"authenticated_browser_snapshot used {session_mode.value} via ignored local Playwright storage state; "
            "content sufficiency and login-wall absence are not asserted"
        )
        recapture_posture = re_capture_relationship or not_applicable(
            "no prior source capture packet was supplied for this authenticated browser snapshot capture"
        )
        mode_changes = [
            *visible_mode_changes,
            f"authenticated_browser_storage_state_loaded:{session_mode.value}:{state_label}",
        ]

        result = write_local_source_capture_packet(
            output_directory=output_directory,
            data_root=data_root,
            input_files=written_paths,
            source_family=source_family,
            source_surface=source_surface,
            source_locator=known_fact(capture_result.requested_url),
            decision_question=decision_question,
            capture_context=(
                f"{capture_context}; session_mode={session_mode.value}; "
                f"auth_state_label={state_label}; no password automation"
            ),
            actor_audience_context=actor_audience_context
            or unknown_with_reason(
                "actor or audience context was not supplied to the authenticated browser snapshot runner"
            ),
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
            source_slices=[
                SourceCaptureSlice(
                    slice_id="authenticated_browser_snapshot_01",
                    locator=known_fact(capture_result.final_url),
                    timing=timing,
                    access_posture=access_posture,
                    archive_history_posture=archive_posture,
                    media_modality_posture=media_posture,
                    re_capture_relationship=recapture_posture,
                    limitations=packet_limitations,
                    warning_notes=packet_warnings,
                    preserved_file_ids=["file_01", "file_02", "file_03", "file_04"],
                )
            ],
            warnings=packet_warnings,
            limitations=packet_limitations,
            receipt_summary=(
                f"Authenticated Browser Snapshot packet for {source_family} using {session_mode.value} "
                "with rendered DOM, visible text, viewport screenshot, and metadata preserved for one supplied URL."
            ),
            receipt_non_claims=AUTHENTICATED_BROWSER_SNAPSHOT_NON_CLAIMS,
        )
    finally:
        for staging_path in written_paths:
            try:
                staging_path.unlink()
            except FileNotFoundError:
                pass
        if staging_root is not None:
            shutil.rmtree(staging_root, ignore_errors=True)
    return 0, result.output_directory


def _write_text(path: Path, text: str) -> None:
    path.write_text(f"{text}\n", encoding="utf-8", newline="\n")


def _possible_login_wall_limitation(*, title: str | None, visible_text: str) -> str | None:
    haystack = f"{title or ''}\n{visible_text}".lower()
    auth_action_visible = any(
        marker in haystack
        for marker in (
            "log in",
            "login",
            "sign in",
            "sign-in",
            "verify your identity",
            "authentication",
        )
    )
    credential_visible = any(
        marker in haystack
        for marker in ("password", "captcha", "two-factor", "2fa", "otp", "totp", "verification code")
    )
    if auth_action_visible and credential_visible:
        return (
            "possible_login_wall_or_auth_challenge_visible: authenticated Browser Snapshot preserved visible "
            "browser artifacts, but title/text matched generic login or challenge markers; operator must inspect "
            "raw artifacts before treating content as unlocked"
        )
    return None


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Capture one URL through a Playwright browser context loaded from a manual-login storage-state file "
            "and write a Source Capture Packet."
        )
    )
    parser.add_argument("--url", required=True)
    parser.add_argument("--state-label", required=True)
    parser.add_argument(
        "--session-mode",
        choices=[item.value for item in AuthenticatedSessionMode],
        required=True,
    )
    parser.add_argument("--source-family", default="authenticated_web_page")
    parser.add_argument("--source-surface", default="authenticated_browser_snapshot")
    parser.add_argument("--decision-question", required=True)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument(
        "--data-root",
        default=None,
        help="Commit into the Orca data lake at this root; explicit --data-root is mutually exclusive with --output. ORCA_DATA_ROOT is used only when --output is omitted.",
    )
    parser.add_argument(
        "--capture-context",
        default="authenticated browser snapshot source capture using operator-created Playwright storage state",
    )
    parser.add_argument("--operator-category", default="authenticated_browser_snapshot_cli_operator")
    parser.add_argument(
        "--capture-mode",
        choices=[item.value for item in CaptureModeCategory],
        default=CaptureModeCategory.MULTIMODAL.value,
    )
    parser.add_argument("--session-id", default=None)
    parser.add_argument("--timeout-seconds", type=float, default=DEFAULT_TIMEOUT_SECONDS)
    parser.add_argument("--wait-until", choices=sorted(ALLOWED_WAIT_UNTIL), default="load")
    parser.add_argument("--viewport-width", type=int, default=DEFAULT_VIEWPORT_WIDTH)
    parser.add_argument("--viewport-height", type=int, default=DEFAULT_VIEWPORT_HEIGHT)
    parser.add_argument("--max-artifact-bytes", type=int, default=DEFAULT_MAX_ARTIFACT_BYTES)
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
                message="source capture authenticated browser snapshot failed: exactly one of --output or --data-root/ORCA_DATA_ROOT is required\n",
            )
        if args.output is None and not data_root_requested:
            parser.exit(
                status=2,
                message="source capture authenticated browser snapshot failed: exactly one of --output or --data-root/ORCA_DATA_ROOT is required\n",
            )
        if data_root_requested:
            from data_lake.root import DataLakeRoot

            data_root = DataLakeRoot.resolve(explicit=args.data_root)
        exit_code, message = run_source_capture_authenticated_browser_packet(
            url=args.url,
            state_label=args.state_label,
            session_mode=AuthenticatedSessionMode(args.session_mode),
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
            wait_until=args.wait_until,
            viewport_width=args.viewport_width,
            viewport_height=args.viewport_height,
            max_artifact_bytes=args.max_artifact_bytes,
        )
    except ValueError as exc:
        parser.exit(status=2, message=f"source capture authenticated browser snapshot failed: {exc}\n")
    except Exception as exc:
        parser.exit(status=3, message=f"source capture authenticated browser snapshot failed: {exc}\n")

    if exit_code == 0:
        print(message)
        return 0

    parser.exit(status=exit_code, message=f"source capture authenticated browser snapshot failed: {message}\n")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
