"""CLI: supervised one-creator TikTok onboarding in one browser context."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from source_capture.session_profiles import (
    default_session_profile_auth_state_root,
    resolve_session_profile,
)
from source_capture.tiktok.batch_packet import write_tiktok_batch_packet
from source_capture.tiktok.creator_onboarding import (
    DEFAULT_MAX_GRID_SCROLL_PASSES,
    DEFAULT_SELECTION_FRACTION,
    DEFAULT_WINDOW_SIZE,
    TikTokCreatorOnboardingError,
    run_tiktok_creator_onboarding,
)
from source_capture.tiktok.live_batch_probe import (
    TIKTOK_SUPERVISED_DEFAULT_CADENCE_GAP_SECONDS,
)


SUMMARY_PREFIX = "tiktok_creator_onboarding_summary_json="


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Attempt suggested-account capture, freeze a bounded TikTok creator grid, "
            "select the reach-proven top fraction, and deep-capture it sequentially "
            "without relaunching the browser."
        ),
        epilog=(
            "Cold-agent default session alias: chowdakr_sg_tiktok. "
            "A missing or invalid alias blocks; this runner never downgrades to logged-out mode."
        ),
    )
    parser.add_argument("--creator-handle", required=True)
    parser.add_argument(
        "--session-profile",
        default="chowdakr_sg_tiktok",
        help="Machine-local cookie-backed TikTok session alias.",
    )
    parser.add_argument("--session-profile-config", type=Path)
    parser.add_argument("--auth-state-root", type=Path, help=argparse.SUPPRESS)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--window-size", type=int, default=DEFAULT_WINDOW_SIZE)
    parser.add_argument(
        "--selection-fraction",
        type=float,
        default=DEFAULT_SELECTION_FRACTION,
    )
    parser.add_argument(
        "--max-grid-scroll-passes",
        type=int,
        default=DEFAULT_MAX_GRID_SCROLL_PASSES,
        help="Safety cap only; collection stops earlier when the response target is reached.",
    )
    parser.add_argument("--timeout-seconds", type=float, default=30.0)
    parser.add_argument("--settle-seconds", type=float, default=2.0)
    parser.add_argument(
        "--cadence-min-gap-seconds",
        type=float,
        default=TIKTOK_SUPERVISED_DEFAULT_CADENCE_GAP_SECONDS,
    )
    parser.add_argument(
        "--cadence-max-gap-seconds",
        type=float,
        default=TIKTOK_SUPERVISED_DEFAULT_CADENCE_GAP_SECONDS,
    )
    parser.add_argument("--cadence-window-seconds", type=float)
    parser.add_argument("--random-seed", type=int)
    admission = parser.add_mutually_exclusive_group()
    admission.add_argument("--admit-output", type=Path)
    admission.add_argument("--data-root")
    parser.add_argument("--batch-label", default="tiktok_creator_onboarding")
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
    try:
        auth_state_root = args.auth_state_root or default_session_profile_auth_state_root()
        session_profile = resolve_session_profile(
            args.session_profile,
            config_path=args.session_profile_config,
        )
        paths = run_tiktok_creator_onboarding(
            creator_handle=args.creator_handle,
            session_profile=session_profile,
            output_dir=args.output_dir,
            auth_state_root=auth_state_root,
            window_size=args.window_size,
            selection_fraction=args.selection_fraction,
            timeout_seconds=args.timeout_seconds,
            settle_seconds=args.settle_seconds,
            max_grid_scroll_passes=args.max_grid_scroll_passes,
            cadence_min_gap_seconds=args.cadence_min_gap_seconds,
            cadence_max_gap_seconds=args.cadence_max_gap_seconds,
            cadence_window_seconds=args.cadence_window_seconds,
            random_seed=args.random_seed,
        )
    except (OSError, ValueError, TikTokCreatorOnboardingError) as exc:
        parser.exit(
            status=2,
            message=f"source capture tiktok creator onboarding failed: {exc}\n",
        )
        return 2
    except Exception as exc:
        parser.exit(
            status=3,
            message=f"source capture tiktok creator onboarding failed: {type(exc).__name__}: {exc}\n",
        )
        return 3

    admitted_path: str | None = None
    if args.admit_output is not None or args.data_root is not None:
        try:
            data_root = None
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
                output_directory=args.admit_output if data_root is None else None,
                data_root=data_root,
                decision_question=args.decision_question,
                batch_label=args.batch_label,
                source_file_receipts=[
                    _source_receipt(paths.live_grid_json_path, "grid_result_json"),
                    _source_receipt(
                        paths.live_cadence_json_path, "cadence_result_json_1"
                    ),
                ],
            )
        except Exception as exc:
            parser.exit(
                status=3,
                message=(
                    "source capture tiktok creator onboarding admission failed: "
                    f"{type(exc).__name__}: {exc}\n"
                ),
            )
            return 3
        if exit_code != 0:
            parser.exit(
                status=exit_code,
                message=f"source capture tiktok creator onboarding admission failed: {output}\n",
            )
        admitted_path = str(output)

    receipt = json.loads(paths.onboarding_receipt_json_path.read_text(encoding="utf-8"))
    print(
        SUMMARY_PREFIX
        + json.dumps(
            {
                "status": receipt["status"],
                "creator_handle": receipt["creator_handle"],
                "session_profile": receipt["session_profile"],
                "window_size": receipt["window_size"],
                "selection_fraction": receipt["selection_fraction"],
                "selected_count": receipt["selected_count"],
                "completed_deep_capture_count": receipt[
                    "completed_deep_capture_count"
                ],
                "suggested_accounts_status": receipt[
                    "suggested_accounts_status_or_none"
                ],
                "output_dir": str(args.output_dir),
                "admitted_path_or_none": admitted_path,
            },
            sort_keys=True,
        )
    )
    return 0


def _source_receipt(path: Path, role: str) -> dict[str, object]:
    raw = path.read_bytes()
    return {
        "role": role,
        "file_name": path.name,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "size_bytes": len(raw),
    }


if __name__ == "__main__":
    raise SystemExit(main())
