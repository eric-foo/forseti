from __future__ import annotations

import argparse
from pathlib import Path

from source_capture.auth_state import AuthenticatedSessionMode
from source_capture.tiktok.live_batch_probe import write_tiktok_live_batch_probe_outputs


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Capture sanitized local TikTok live staging JSON for one creator. "
            "This runner requires a pre-bootstrapped auth-state label and does not "
            "write a SourceCapturePacket directly."
        )
    )
    parser.add_argument("--creator-handle", required=True)
    parser.add_argument("--creator-profile-url", required=True)
    parser.add_argument("--video-url", action="append", required=True, dest="video_urls")
    parser.add_argument("--state-label", required=True)
    parser.add_argument(
        "--session-mode",
        required=True,
        choices=[mode.value for mode in AuthenticatedSessionMode],
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
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    paths = write_tiktok_live_batch_probe_outputs(
        creator_handle=args.creator_handle,
        creator_profile_url=args.creator_profile_url,
        video_urls=args.video_urls,
        state_label=args.state_label,
        session_mode=AuthenticatedSessionMode(args.session_mode),
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
    )
    print(f"grid_result_json={paths.grid_result_json_path}")
    print(f"cadence_result_json={paths.cadence_result_json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
