from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from source_capture.auth_state import AuthenticatedSessionMode
from source_capture.source_access_provenance import HarnessProxyProfilePosture
from source_capture.tiktok.admission import COMPLETE_LANE_NOTE
from source_capture.tiktok.batch_packet import write_tiktok_batch_packet
from source_capture.tiktok.live_batch_probe import (
    TIKTOK_BROWSER_BACKEND_CLOAKBROWSER,
    write_tiktok_live_batch_probe_outputs,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Capture sanitized local TikTok staging JSON for one creator. "
            "Sessioned mode requires a pre-bootstrapped auth-state label; "
            "--logged-out uses no storage state. By default this runner writes "
            "staging JSON only; --admit-output or --data-root chains the "
            "existing TikTok batch admission gate after staging."
        )
    )
    parser.add_argument("--creator-handle", required=True)
    parser.add_argument("--creator-profile-url", required=True)
    parser.add_argument("--video-url", action="append", required=True, dest="video_urls")
    parser.add_argument("--state-label")
    parser.add_argument(
        "--session-mode",
        choices=[mode.value for mode in AuthenticatedSessionMode],
    )
    parser.add_argument(
        "--logged-out",
        action="store_true",
        help="Use no auth storage state; measure public logged-out TikTok access only.",
    )
    parser.add_argument("--output-dir", required=True, type=Path)
    admission_target = parser.add_mutually_exclusive_group(required=False)
    admission_target.add_argument(
        "--admit-output",
        type=Path,
        default=None,
        help=(
            "After live staging, admit through the network-free TikTok batch gate "
            "into this local SourceCapturePacket directory."
        ),
    )
    admission_target.add_argument(
        "--data-root",
        default=None,
        help=(
            "After live staging, admit through the network-free TikTok batch gate "
            "into this explicit Orca data lake root. ORCA_DATA_ROOT is not read "
            "by this live runner."
        ),
    )
    parser.add_argument("--batch-label", default="tiktok_creator_batch")
    parser.add_argument(
        "--decision-question",
        default="Admit TikTok creator-batch comment, subtitle, source-text, and typed extraction seed signals.",
        help="Decision question for the optional batch-admission packet.",
    )
    parser.add_argument("--timeout-seconds", type=float, default=30.0)
    parser.add_argument(
        "--wait-until",
        choices=("commit", "domcontentloaded", "load", "networkidle"),
        default="domcontentloaded",
    )
    parser.add_argument("--viewport-width", type=int, default=1280)
    parser.add_argument("--viewport-height", type=int, default=720)
    parser.add_argument("--max-response-bytes", type=int, default=5_000_000)
    parser.add_argument("--settle-seconds", type=float, default=2.0)
    parser.add_argument("--selector-timeout-seconds", type=float, default=5.0)
    parser.add_argument("--browser-channel")
    parser.add_argument(
        "--browser-backend",
        choices=("playwright", "cloakbrowser"),
        default=TIKTOK_BROWSER_BACKEND_CLOAKBROWSER,
        help=(
            "Browser backend for rendered page observation. TikTok packet-grade "
            "capture defaults to cloakbrowser; playwright is diagnostic-only."
        ),
    )
    parser.add_argument(
        "--allow-diagnostic-browser-backend",
        action="store_true",
        help=(
            "Allow non-CloakBrowser backend use for explicit diagnostics. "
            "Diagnostic backend runs are not the TikTok packet-grade route."
        ),
    )
    parser.add_argument(
        "--require-harness-proxy-posture",
        choices=[
            HarnessProxyProfilePosture.NO_PROXY_PROFILE_LOADED.value,
            HarnessProxyProfilePosture.PROXY_PROFILE_LOADED.value,
        ],
        default=None,
        help=(
            "Require the auth-state provenance sidecar to attest the Source Capture "
            "harness proxy-profile posture before opening TikTok. This is not a "
            "full-network no-proxy egress proof."
        ),
    )
    parser.add_argument(
        "--cloakbrowser-humanize",
        action="store_true",
        help="Enable CloakBrowser humanized pointer/keyboard timing when using the cloakbrowser backend.",
    )
    parser.add_argument(
        "--human-challenge-handoff",
        action="store_true",
        help=(
            "After scripted challenge X/Close followthrough actions, prompt the "
            "operator to solve a remaining slider/captcha in the visible browser. "
            "The receipt marks this as a source-access intervention."
        ),
    )
    parser.add_argument(
        "--human-challenge-handoff-timeout-seconds",
        type=float,
        default=180.0,
    )
    parser.add_argument("--cadence-min-gap-seconds", type=float, default=75.0)
    parser.add_argument("--cadence-max-gap-seconds", type=float, default=120.0)
    parser.add_argument("--cadence-window-seconds", type=float)
    parser.add_argument("--random-seed", type=int)
    parser.add_argument(
        "--allow-challenge-close-diagnostic",
        action="store_true",
        help=(
            "Diagnostic only: use a bounded pointer click on a TikTok challenge "
            "modal X/Close control before the comment route. Any resulting "
            "capture is not clean admission proof."
        ),
    )
    parser.add_argument(
        "--allow-challenge-close-followthrough",
        action="store_true",
        help=(
            "Owner-authorized public challenge X/Close follow-through: click a "
            "dismiss control, then attempt the page-owned comment route. This "
            "does not solve a puzzle and receipts preserve the intervention."
        ),
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.allow_challenge_close_diagnostic and args.allow_challenge_close_followthrough:
        parser.error(
            "--allow-challenge-close-diagnostic and "
            "--allow-challenge-close-followthrough are mutually exclusive"
        )
    if (
        args.browser_backend != TIKTOK_BROWSER_BACKEND_CLOAKBROWSER
        and not args.allow_diagnostic_browser_backend
    ):
        parser.error(
            "--browser-backend playwright is diagnostic-only for TikTok; pass "
            "--allow-diagnostic-browser-backend to opt in"
        )
    if (
        args.browser_backend == TIKTOK_BROWSER_BACKEND_CLOAKBROWSER
        and args.browser_channel is not None
    ):
        parser.error("--browser-channel cannot be combined with --browser-backend cloakbrowser")
    if (
        args.cloakbrowser_humanize
        and args.browser_backend != TIKTOK_BROWSER_BACKEND_CLOAKBROWSER
    ):
        parser.error("--cloakbrowser-humanize requires --browser-backend cloakbrowser")
    if args.human_challenge_handoff and not args.allow_challenge_close_followthrough:
        parser.error("--human-challenge-handoff requires --allow-challenge-close-followthrough")
    cloakbrowser_humanize = (
        args.cloakbrowser_humanize
        or args.browser_backend == TIKTOK_BROWSER_BACKEND_CLOAKBROWSER
    )
    if args.logged_out:
        if args.state_label is not None or args.session_mode is not None:
            parser.error("--logged-out cannot be combined with --state-label or --session-mode")
        if args.require_harness_proxy_posture is not None:
            parser.error("--require-harness-proxy-posture requires sessioned mode with --state-label")
        session_mode = None
    else:
        if args.state_label is None or args.session_mode is None:
            parser.error("sessioned mode requires --state-label and --session-mode; use --logged-out for public logged-out capture")
        session_mode = AuthenticatedSessionMode(args.session_mode)
    required_harness_proxy_profile_posture = (
        HarnessProxyProfilePosture(args.require_harness_proxy_posture)
        if args.require_harness_proxy_posture is not None
        else None
    )
    paths = write_tiktok_live_batch_probe_outputs(
        creator_handle=args.creator_handle,
        creator_profile_url=args.creator_profile_url,
        video_urls=args.video_urls,
        state_label=args.state_label,
        session_mode=session_mode,
        logged_out=args.logged_out,
        output_dir=args.output_dir,
        timeout_seconds=args.timeout_seconds,
        wait_until=args.wait_until,
        viewport_width=args.viewport_width,
        viewport_height=args.viewport_height,
        max_response_bytes=args.max_response_bytes,
        settle_seconds=args.settle_seconds,
        selector_timeout_seconds=args.selector_timeout_seconds,
        browser_channel=args.browser_channel,
        browser_backend=args.browser_backend,
        required_harness_proxy_profile_posture=required_harness_proxy_profile_posture,
        cloakbrowser_humanize=cloakbrowser_humanize,
        human_challenge_handoff=args.human_challenge_handoff,
        human_challenge_handoff_timeout_seconds=args.human_challenge_handoff_timeout_seconds,
        cadence_min_gap_seconds=args.cadence_min_gap_seconds,
        cadence_max_gap_seconds=args.cadence_max_gap_seconds,
        cadence_window_seconds=args.cadence_window_seconds,
        random_seed=args.random_seed,
        allow_challenge_close_diagnostic=args.allow_challenge_close_diagnostic,
        allow_challenge_close_followthrough=args.allow_challenge_close_followthrough,
    )
    print(f"grid_result_json={paths.grid_result_json_path}")
    print(f"cadence_result_json={paths.cadence_result_json_path}")
    if args.admit_output is not None or args.data_root is not None:
        try:
            data_root = None
            if args.data_root is not None:
                from data_lake.root import DataLakeRoot

                data_root = DataLakeRoot.resolve(explicit=args.data_root)
            exit_code, admitted_path = write_tiktok_batch_packet(
                creator_handle=args.creator_handle,
                creator_profile_url=args.creator_profile_url,
                grid_result_json=paths.grid_result_json_path.read_bytes(),
                cadence_result_jsons=[paths.cadence_result_json_path.read_bytes()],
                output_directory=args.admit_output if data_root is None else None,
                data_root=data_root,
                decision_question=args.decision_question,
                batch_label=args.batch_label,
                source_file_receipts=[
                    _source_receipt(paths.grid_result_json_path, "grid_result_json"),
                    _source_receipt(paths.cadence_result_json_path, "cadence_result_json_1"),
                ],
            )
        except ValueError as exc:
            parser.exit(status=2, message=f"source capture tiktok live batch admission failed: {exc}\n")
        except Exception as exc:  # noqa: BLE001 - keep admission/lake failures visible
            parser.exit(
                status=3,
                message=(
                    "source capture tiktok live batch admission failed: "
                    f"{type(exc).__name__}: {exc}\n"
                ),
            )
        if exit_code != 0:
            parser.exit(
                status=exit_code,
                message=f"source capture tiktok live batch admission failed: {admitted_path}\n",
            )
        print(COMPLETE_LANE_NOTE)
        print(f"admitted_packet={admitted_path}")
    return 0


def _source_receipt(path: Path, role: str) -> dict[str, object]:
    raw = path.read_bytes()
    resolved = str(path.resolve())
    return {
        "role": role,
        "file_name": path.name,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "size_bytes": len(raw),
        "source_path_sha256": hashlib.sha256(resolved.encode("utf-8")).hexdigest(),
    }


if __name__ == "__main__":
    raise SystemExit(main())
