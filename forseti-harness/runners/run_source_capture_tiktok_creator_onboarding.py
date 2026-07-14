"""CLI: supervised one-creator TikTok onboarding in one browser context."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from capture_spine.creator_profile_current.registry_match_preflight import (
    RECEIPT_WRAPPER_KEY,
    build_creator_registry_match_preflight_receipt,
    dump_creator_registry_match_preflight_receipt,
)
from capture_spine.creator_profile_current.validation import (
    load_creator_profile_current_view,
)
from capture_spine.tiktok_creator_discovery_frontier import (
    LinkHubOutcome,
    RefreshOutcome,
    ScanReceipt,
    SuggestedAccountObservation,
    build_tiktok_creator_discovery_frontier_register,
    write_tiktok_creator_discovery_frontier_register,
)
from source_capture.session_profiles import (
    default_session_profile_auth_state_root,
    resolve_session_profile,
)
from source_capture.tiktok.batch_packet import write_tiktok_batch_packet
from source_capture.tiktok.creator_onboarding import (
    DEFAULT_MAX_GRID_SCROLL_PASSES,
    DEFAULT_SELECTION_COUNT,
    DEFAULT_WINDOW_SIZE,
    TikTokCreatorOnboardingError,
    run_tiktok_creator_onboarding,
)
from source_capture.tiktok.live_batch_probe import (
    TIKTOK_SUPERVISED_DEFAULT_CADENCE_MAX_GAP_SECONDS,
    TIKTOK_SUPERVISED_DEFAULT_CADENCE_MIN_GAP_SECONDS,
)


SUMMARY_PREFIX = "tiktok_creator_onboarding_summary_json="
PROGRESS_PREFIX = "tiktok_creator_onboarding_progress_json="
BLOCKER_PREFIX = "tiktok_creator_onboarding_blocker_json="
ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CREATOR_REGISTRY = (
    ROOT
    / "forseti/product/spines/capture/core/source_families/social_media"
    / "creator_registry/creator_profile_current_view_v0.json"
)
REGISTRY_PREFLIGHT_JSON_NAME = "creator_registry_match_preflight.json"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Attempt suggested-account capture, freeze a bounded TikTok creator grid, "
            "select the reach-proven top eight, and deep-capture every selection through "
            "a visible grid-tile overlay on the already-running dedicated Chrome CDP session."
        ),
        epilog=(
            "Cold-agent default session alias: chowdakr_sg_tiktok. "
            "A missing or invalid alias blocks; this runner never downgrades to logged-out mode."
        ),
    )
    parser.add_argument("--creator-handle", required=True)
    parser.add_argument(
        "--creator-intent",
        choices=("new_capture", "update_existing"),
        default="new_capture",
        help=(
            "New capture blocks exact Creator Registry matches; update existing "
            "requires an exact match."
        ),
    )
    parser.add_argument(
        "--creator-registry", type=Path, default=DEFAULT_CREATOR_REGISTRY
    )
    parser.add_argument(
        "--session-profile",
        default="chowdakr_sg_tiktok",
        help="Machine-local retained Chrome CDP TikTok session alias.",
    )
    parser.add_argument("--session-profile-config", type=Path)
    parser.add_argument("--auth-state-root", type=Path, help=argparse.SUPPRESS)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--window-size", type=int, default=DEFAULT_WINDOW_SIZE)
    parser.add_argument(
        "--max-grid-scroll-passes",
        type=int,
        default=DEFAULT_MAX_GRID_SCROLL_PASSES,
        help=(
            "Safety cap per selected-tile lookup during deep-capture grid pagination; "
            "initial acquisition uses zero wheels for an already-loaded 27-video "
            "window, otherwise stops after its first sufficient new DOM batch."
        ),
    )
    parser.add_argument("--timeout-seconds", type=float, default=30.0)
    parser.add_argument("--settle-seconds", type=float, default=2.0)
    parser.add_argument(
        "--cadence-min-gap-seconds",
        type=float,
        default=TIKTOK_SUPERVISED_DEFAULT_CADENCE_MIN_GAP_SECONDS,
    )
    parser.add_argument(
        "--cadence-max-gap-seconds",
        type=float,
        default=TIKTOK_SUPERVISED_DEFAULT_CADENCE_MAX_GAP_SECONDS,
    )
    parser.add_argument("--cadence-window-seconds", type=float)
    parser.add_argument("--random-seed", type=int)
    admission = parser.add_mutually_exclusive_group()
    admission.add_argument("--admit-output", type=Path)
    admission.add_argument("--data-root")
    parser.add_argument("--batch-label", default="tiktok_creator_onboarding")
    parser.add_argument(
        "--prior-capture-pointer",
        help=(
            "Optional prior Bronze packet pointer. When supplied, this run writes a "
            "separate supplement and never rewrites the prior packet provenance."
        ),
    )
    parser.add_argument(
        "--decision-question",
        default=(
            "Admit the selected TikTok onboarding videos' public comments, "
            "subtitles, source text, and typed extraction seeds."
        ),
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    _emit_progress(
        "preflight_started",
        {
            "creator_handle": args.creator_handle.strip().lstrip("@").lower(),
            "session_profile": args.session_profile,
        },
    )
    try:
        preflight_path, preflight_result = _write_creator_registry_preflight(
            creator_handle=args.creator_handle,
            creator_intent=args.creator_intent,
            registry_path=args.creator_registry,
            output_dir=args.output_dir,
        )
        if preflight_result["action_status"] != "allowed":
            raise TikTokCreatorOnboardingError(
                f"Creator Registry preflight blocked: {preflight_result['action_blockers']}"
            )
        auth_state_root = args.auth_state_root or default_session_profile_auth_state_root()
        _emit_progress("registry_preflight_complete", {"status": "allowed"})
        session_profile = resolve_session_profile(
            args.session_profile,
            config_path=args.session_profile_config,
        )
        _emit_progress(
            "session_profile_resolved",
            {"session_profile": args.session_profile},
        )
        paths = run_tiktok_creator_onboarding(
            creator_handle=args.creator_handle,
            session_profile=session_profile,
            output_dir=args.output_dir,
            auth_state_root=auth_state_root,
            window_size=args.window_size,
            selection_count=DEFAULT_SELECTION_COUNT,
            timeout_seconds=args.timeout_seconds,
            settle_seconds=args.settle_seconds,
            max_grid_scroll_passes=args.max_grid_scroll_passes,
            cadence_min_gap_seconds=args.cadence_min_gap_seconds,
            cadence_max_gap_seconds=args.cadence_max_gap_seconds,
            cadence_window_seconds=args.cadence_window_seconds,
            random_seed=args.random_seed,
            progress_fn=_emit_progress,
        )
    except (OSError, ValueError, TikTokCreatorOnboardingError) as exc:
        if str(exc) == "account_safety_stop":
            _emit_blocker("ACCOUNT_SAFETY_STOP", "deep_capture")
        else:
            _emit_blocker(
                "ONBOARDING_PRECHECK_OR_CAPTURE_FAILED", "onboarding"
            )
        parser.exit(
            status=2,
            message=f"source capture tiktok creator onboarding failed: {exc}\n",
        )
        return 2
    except Exception as exc:
        _emit_blocker("ONBOARDING_UNEXPECTED_FAILURE", "onboarding")
        parser.exit(
            status=3,
            message=f"source capture tiktok creator onboarding failed: {type(exc).__name__}: {exc}\n",
        )
        return 3

    admitted_path: str | None = None
    frontier_path: str | None = None
    if args.admit_output is not None or args.data_root is not None:
        _emit_progress("admission_started", {})
        data_root = None
        try:
            if args.data_root is not None:
                from data_lake.root import DataLakeRoot

                data_root = DataLakeRoot.resolve(explicit=args.data_root)
            exit_code, output = write_tiktok_batch_packet(
                creator_handle=args.creator_handle,
                creator_profile_url=(
                    f"https://www.tiktok.com/@{args.creator_handle.strip().lstrip('@')}"
                ),
                grid_result_json=paths.live_grid_json_path.read_bytes(),
                cadence_result_jsons=[paths.live_cadence_json_path.read_bytes()],
                grid_window_json=paths.grid_window_json_path.read_bytes(),
                selection_result_json=paths.selection_json_path.read_bytes(),
                suggested_accounts_json=paths.suggested_accounts_json_path.read_bytes(),
                output_directory=args.admit_output if data_root is None else None,
                data_root=data_root,
                decision_question=args.decision_question,
                batch_label=args.batch_label,
                source_file_receipts=[
                    _source_receipt(paths.live_grid_json_path, "grid_result_json"),
                    _source_receipt(
                        paths.live_cadence_json_path, "cadence_result_json_1"
                    ),
                    _source_receipt(
                        paths.grid_window_json_path, "grid_window_json"
                    ),
                    _source_receipt(
                        paths.selection_json_path, "selection_result_json"
                    ),
                    _source_receipt(
                        paths.suggested_accounts_json_path,
                        "suggested_accounts_json",
                    ),
                ],
                prior_capture_pointer=args.prior_capture_pointer,
            )
        except Exception as exc:
            _emit_blocker("ADMISSION_FAILED", "admission")
            parser.exit(
                status=3,
                message=(
                    "source capture tiktok creator onboarding admission failed: "
                    f"{type(exc).__name__}: {exc}\n"
                ),
            )
            return 3
        if exit_code != 0:
            _emit_blocker("ADMISSION_FAILED", "admission")
            parser.exit(
                status=exit_code,
                message=f"source capture tiktok creator onboarding admission failed: {output}\n",
            )
        admitted_path = str(output)
        if data_root is not None:
            try:
                frontier_path = _write_suggested_frontier(
                    creator_handle=args.creator_handle,
                    session_profile=args.session_profile,
                    suggested_receipt_path=paths.suggested_accounts_json_path,
                    admitted_path=Path(admitted_path),
                    data_root=data_root,
                )
            except Exception as exc:
                _emit_blocker("SUGGESTED_FRONTIER_WRITE_FAILED", "admission")
                parser.exit(
                    status=3,
                    message=(
                        "source capture tiktok suggested frontier write failed: "
                        f"{type(exc).__name__}: {exc}\n"
                    ),
                )
                return 3

    receipt = json.loads(paths.onboarding_receipt_json_path.read_text(encoding="utf-8"))
    browser_lifecycle = receipt.get("browser_lifecycle")
    if not isinstance(browser_lifecycle, dict):
        browser_lifecycle = {}
    print(
        SUMMARY_PREFIX
        + json.dumps(
            {
                "status": receipt["status"],
                "creator_handle": receipt["creator_handle"],
                "session_profile": receipt["session_profile"],
                "window_size": receipt["window_size"],
                "selection_count": receipt["selection_count"],
                "window_cap": receipt["window_cap"],
                "creator_intent": args.creator_intent,
                "registry_preflight_path": str(preflight_path),
                "selected_count": receipt["selected_count"],
                "completed_deep_capture_count": receipt[
                    "completed_deep_capture_count"
                ],
                "suggested_accounts_status": receipt[
                    "suggested_accounts_status_or_none"
                ],
                "suggested_outer_ui_route": receipt.get(
                    "suggested_outer_ui_route_or_none"
                ),
                "page_acquisition_policy": browser_lifecycle.get(
                    "page_acquisition_policy"
                ),
                "initial_platform_match_count": browser_lifecycle.get(
                    "initial_platform_match_count"
                ),
                "initial_exact_match_count": browser_lifecycle.get(
                    "initial_exact_match_count"
                ),
                "page_adoption_count": browser_lifecycle.get(
                    "page_adoption_count"
                ),
                "page_creation_count": browser_lifecycle.get(
                    "page_creation_count"
                ),
                "page_navigation_count": browser_lifecycle.get(
                    "page_navigation_count"
                ),
                "same_url_navigation_suppression_count": browser_lifecycle.get(
                    "same_url_navigation_suppression_count"
                ),
                "humanized_input_preset": browser_lifecycle.get(
                    "humanized_input_preset"
                ),
                "initial_deep_capture_wait": receipt.get(
                    "initial_deep_capture_wait_or_none"
                ),
                "grid_deep_entry": receipt.get("grid_deep_entry_or_none"),
                "output_dir": str(args.output_dir),
                "admitted_path_or_none": admitted_path,
                "suggested_frontier_path_or_none": frontier_path,
            },
            sort_keys=True,
        )
    )
    return 0



def _emit_progress(event: str, fields: dict[str, object]) -> None:
    print(
        PROGRESS_PREFIX
        + json.dumps({"event": event, **fields}, sort_keys=True),
        flush=True,
    )


def _emit_blocker(code: str, phase: str) -> None:
    print(
        BLOCKER_PREFIX
        + json.dumps({"code": code, "phase": phase}, sort_keys=True),
        flush=True,
    )


def _write_creator_registry_preflight(
    *,
    creator_handle: str,
    creator_intent: str,
    registry_path: Path,
    output_dir: Path,
) -> tuple[Path, dict[str, object]]:
    normalized_handle = creator_handle.strip().lstrip("@").lower()
    registry_document = load_creator_profile_current_view(registry_path)
    receipt = build_creator_registry_match_preflight_receipt(
        candidates=[
            {
                "candidate_id": f"tiktok-{normalized_handle}",
                "platform": "tiktok",
                "public_handle_or_none": normalized_handle,
                "public_profile_url_or_none": (
                    f"https://www.tiktok.com/@{normalized_handle}"
                ),
                "intended_action": creator_intent,
            }
        ],
        registry_document=registry_document,
        registry_source_pointer=str(registry_path),
        registry_sha256=hashlib.sha256(registry_path.read_bytes()).hexdigest(),
        generated_at_utc=(
            datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
        ),
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    receipt_path = output_dir / REGISTRY_PREFLIGHT_JSON_NAME
    receipt_path.write_text(
        dump_creator_registry_match_preflight_receipt(receipt),
        encoding="utf-8",
        newline="\n",
    )
    result = receipt[RECEIPT_WRAPPER_KEY]["results"][0]
    if not isinstance(result, dict):
        raise ValueError("Creator Registry preflight result must be an object")
    return receipt_path, result


def _source_receipt(path: Path, role: str) -> dict[str, object]:
    raw = path.read_bytes()
    return {
        "role": role,
        "file_name": path.name,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "size_bytes": len(raw),
    }


def _write_suggested_frontier(
    *,
    creator_handle: str,
    session_profile: str,
    suggested_receipt_path: Path,
    admitted_path: Path,
    data_root: object,
) -> str | None:
    suggested_receipt = json.loads(
        suggested_receipt_path.read_text(encoding="utf-8")
    )
    rows = suggested_receipt.get("suggested_accounts")
    if suggested_receipt.get("status") != "captured" or not isinstance(rows, list) or not rows:
        return None

    handle = creator_handle.strip().lstrip("@").lower()
    packet_id = admitted_path.name
    capture_timestamp = (
        suggested_receipt.get("attempt_receipt", {}).get("capture_timestamp")
    )
    if not isinstance(capture_timestamp, str) or not capture_timestamp:
        raise ValueError("captured suggested accounts require capture_timestamp")
    external_links = suggested_receipt.get("profile_external_links")
    link_hub_url = None
    if isinstance(external_links, list):
        for row in external_links:
            if isinstance(row, dict) and isinstance(row.get("url"), str):
                link_hub_url = row["url"]
                break

    run_id = f"tiktok_creator_onboarding_{packet_id.lower()}"
    register_id = f"tiktok_creator_discovery_frontier_{handle}_{packet_id.lower()}"
    scan_receipt = ScanReceipt(
        receipt_id=f"receipt_{run_id}",
        run_id=run_id,
        register_id=register_id,
        root_seed={
            "platform": "tiktok",
            "handle": handle,
            "url": f"https://www.tiktok.com/@{handle}",
        },
        source_surface="tiktok_followers_dialog_suggested_existing_chrome_cdp",
        captured_at_utc=capture_timestamp,
        method_mode="existing_chrome_cdp_dom_extraction",
        access_mode="owner_authorized_retained_session_screen_light_dom_read",
        extraction_method="visible_dialog_suggested_profile_rows_or_profile_fallback",
        browser_session_label_or_none=session_profile,
        parent_grid_packet_id_or_none=packet_id,
        parent_grid_packet_path_or_none=str(admitted_path),
        source_packet_id_or_none=packet_id,
        source_packet_path_or_none=str(admitted_path),
        parent_profile_capture_status="tiktok_parent_profile_grid_packet_available",
        suggested_accounts_capture_status="tiktok_suggested_accounts_packet_available",
        link_hub_capture_status=(
            LinkHubOutcome.CAPTURED if link_hub_url else LinkHubOutcome.NONE_VISIBLE
        ),
        link_hub_url_or_none=link_hub_url,
        browser_closed_by_runner=False,
        refresh_attempt_count=0,
        refresh_outcome=RefreshOutcome.NOT_NEEDED,
        pagination_bound=len(rows),
        suggested_accounts_observed=len(rows),
        candidate_profiles_opened=0,
        follow_unfollow_actions_taken=0,
        screenshots_emitted_to_chat=0,
        caps_applied={
            "root_profiles": 1,
            "suggested_accounts_observed": len(rows),
            "candidate_profiles_opened": 0,
            "screenshots_emitted_to_chat": 0,
        },
        stop_reason="bounded_suggested_accounts_observation_complete",
        exclusions=(
            "no_candidate_profile_open",
            "no_follow_unfollow_action",
            "no_metric_rollup",
            "no_registry_mutation",
            "no_screenshot_chat_output",
        ),
    ).to_dict()
    outer_ui_route = suggested_receipt.get("outer_ui_route")
    observed_sections = (
        ("followers_dialog_suggested_tab",)
        if outer_ui_route == "followers_dialog_suggested_tab_primary"
        else ("profile_suggested_accounts_view_all_fallback",)
    )
    observations = [
        SuggestedAccountObservation(
            handle=str(row["handle"]),
            display_name_or_none=(
                str(row["display_text_or_none"])
                if row.get("display_text_or_none")
                else None
            ),
            source_url_or_locator=(
                str(row["profile_url"]) if row.get("profile_url") else None
            ),
            observed_sections=observed_sections,
        )
        for row in rows
        if isinstance(row, dict) and row.get("handle")
    ]
    register = build_tiktok_creator_discovery_frontier_register(
        scan_receipt=scan_receipt,
        suggested_accounts=observations,
        prior_register_pointer=(
            f"{admitted_path}/raw/04_tiktok_suggested_accounts_attempt.json"
        ),
    )
    written = write_tiktok_creator_discovery_frontier_register(
        register,
        data_root,
        record_id=f"{register_id}.json",
    )
    if written is None:
        raise RuntimeError(
            "captured suggested accounts did not produce a frontier artifact"
        )
    written_path = Path(written)
    if not written_path.is_file():
        raise RuntimeError(
            f"suggested frontier writer returned a missing artifact: {written_path}"
        )
    return str(written_path)


if __name__ == "__main__":
    raise SystemExit(main())
