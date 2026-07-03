from __future__ import annotations

import argparse
from pathlib import Path

from source_capture.auth_state import AuthenticatedSessionMode
from source_capture.tiktok.live_batch_probe import write_tiktok_live_batch_probe_outputs


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Capture sanitized local TikTok staging JSON for one creator. "
            "Sessioned mode requires a pre-bootstrapped auth-state label; "
            "--logged-out uses no storage state. This runner does not write a "
            "SourceCapturePacket directly."
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
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.logged_out:
        if args.state_label is not None or args.session_mode is not None:
            parser.error("--logged-out cannot be combined with --state-label or --session-mode")
        session_mode = None
    else:
        if args.state_label is None or args.session_mode is None:
            parser.error("sessioned mode requires --state-label and --session-mode; use --logged-out for public logged-out capture")
        session_mode = AuthenticatedSessionMode(args.session_mode)
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
        cadence_min_gap_seconds=args.cadence_min_gap_seconds,
        cadence_max_gap_seconds=args.cadence_max_gap_seconds,
        cadence_window_seconds=args.cadence_window_seconds,
        random_seed=args.random_seed,
        allow_challenge_close_diagnostic=args.allow_challenge_close_diagnostic,
    )
    print(f"grid_result_json={paths.grid_result_json_path}")
    print(f"cadence_result_json={paths.cadence_result_json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
