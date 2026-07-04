"""CLI: admit sanitized TikTok single-video comments/subtitles into a packet.

This lean SCI runner does not automate TikTok. It consumes already captured
page-owned artifacts, enforces parser/sanitizer contracts, and writes the
normalized single-video admission packet. See the complete-lane note printed by
the runner before expanding to live browser/profile-grid/batch capture.
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from source_capture.tiktok import COMPLETE_LANE_NOTE, write_tiktok_video_packet


def run_source_capture_tiktok_video_packet(
    *,
    video_id: str,
    video_url: str,
    output_directory: Path | None = None,
    data_root=None,
    decision_question: str,
    comment_list_json_path: Path | None = None,
    video_item_json_path: Path | None = None,
    profile_list_json_path: Path | None = None,
    profile_list_source_surface: str = "/api/post/item_list/",
    subtitle_webvtt_path: Path | None = None,
) -> tuple[int, str]:
    if (output_directory is None) == (data_root is None):
        raise ValueError("exactly one of output_directory or data_root is required")
    return write_tiktok_video_packet(
        video_id=video_id,
        video_url=video_url,
        comment_list_json=_read_optional_bytes(comment_list_json_path),
        video_item_json=_read_optional_bytes(video_item_json_path),
        profile_list_json=_read_optional_bytes(profile_list_json_path),
        profile_list_source_surface=profile_list_source_surface,
        subtitle_webvtt=_read_optional_bytes(subtitle_webvtt_path),
        output_directory=output_directory,
        data_root=data_root,
        decision_question=decision_question,
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Admit sanitized TikTok single-video comments/subtitles into a SourceCapturePacket.",
        epilog=f"Complete-lane note: {COMPLETE_LANE_NOTE}",
    )
    parser.add_argument("--video-id", required=True)
    parser.add_argument("--video-url", required=True, help="Canonical TikTok video URL without query string.")
    target = parser.add_mutually_exclusive_group(required=False)
    target.add_argument("--output", type=Path, default=None)
    target.add_argument(
        "--data-root",
        default=None,
        help="Commit into the Forseti data lake at this root; FORSETI_DATA_ROOT is used only when --output is omitted; legacy ORCA_DATA_ROOT is also accepted.",
    )
    parser.add_argument("--comment-list-json", type=Path, default=None)
    parser.add_argument("--video-item-json", type=Path, default=None)
    parser.add_argument("--profile-list-json", type=Path, default=None)
    parser.add_argument("--profile-list-source-surface", default="/api/post/item_list/")
    parser.add_argument("--subtitle-webvtt", type=Path, default=None)
    parser.add_argument(
        "--decision-question",
        default="Admit TikTok page-owned comment/subtitle/profile-list artifacts for behavioral capture.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        data_root = None
        data_root_requested = args.data_root is not None or (args.output is None and (os.environ.get("FORSETI_DATA_ROOT") or os.environ.get("ORCA_DATA_ROOT")))
        if args.output is not None and args.data_root is not None:
            parser.exit(status=2, message="source capture tiktok video failed: supply only one of --output or --data-root\n")
        if args.output is None and not data_root_requested:
            parser.exit(
                status=2,
                message="source capture tiktok video failed: exactly one of --output or --data-root/FORSETI_DATA_ROOT/ORCA_DATA_ROOT is required\n",
            )
        if data_root_requested:
            from data_lake.root import DataLakeRoot

            data_root = DataLakeRoot.resolve(explicit=args.data_root)
        exit_code, message = run_source_capture_tiktok_video_packet(
            video_id=args.video_id,
            video_url=args.video_url,
            output_directory=args.output if data_root is None else None,
            data_root=data_root,
            decision_question=args.decision_question,
            comment_list_json_path=args.comment_list_json,
            video_item_json_path=args.video_item_json,
            profile_list_json_path=args.profile_list_json,
            profile_list_source_surface=args.profile_list_source_surface,
            subtitle_webvtt_path=args.subtitle_webvtt,
        )
    except ValueError as exc:
        parser.exit(status=2, message=f"source capture tiktok video failed: {exc}\n")
    except Exception as exc:  # noqa: BLE001 - surface capture/lake failures visibly
        parser.exit(status=3, message=f"source capture tiktok video failed: {type(exc).__name__}: {exc}\n")

    if exit_code == 0:
        print(COMPLETE_LANE_NOTE)
        print(message)
        return 0
    parser.exit(status=exit_code, message=f"source capture tiktok video failed: {message}\n")
    return exit_code


def _read_optional_bytes(path: Path | None) -> bytes | None:
    if path is None:
        return None
    return path.read_bytes()


if __name__ == "__main__":
    raise SystemExit(main())
