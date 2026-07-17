"""CLI: capture YouTube watch-page metadata/comments into a SourceCapturePacket.

Thin wrapper: fetch the incumbent logged-out watch-page route, then stage selected
source-visible metadata, metric/availability receipts, and bounded comment rows into a
contract-compliant SourceCapturePacket. Enclosing HTML/youtubei bodies remain transient.
The packet writer is network-free and unit-tested; this runner owns live acquisition and
the data-lake seam.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Callable, Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from source_capture.youtube_watch_packet import (
    YoutubeWatchCommentPage,
    YoutubeWatchFetch,
    write_youtube_watch_packet,
)
from youtube_capture.capture_youtube_v0 import fetch_youtube_watch
from runners._scaffold import SUPPLY_ONLY_ONE_DETAIL, exit_on_failure, resolve_output_root
from runners._youtube_cli import normalize_video_id_argv

_RUNNER_NAME = "source capture youtube watch"


def run_source_capture_youtube_watch_packet(
    *,
    video_id: str,
    output_directory: Path | None = None,
    data_root=None,
    decision_question: str,
    comment_pages: int = 2,
    capture_fetcher: Callable[..., object] = fetch_youtube_watch,
) -> tuple[int, str]:
    if (output_directory is None) == (data_root is None):
        raise ValueError("exactly one of output_directory or data_root is required")
    if comment_pages <= 0:
        raise ValueError("comment_pages must be greater than zero")

    fetched = capture_fetcher(video_id, comment_pages=comment_pages)
    comment_pages_out = tuple(
        YoutubeWatchCommentPage(filename=page.filename, raw_json_bytes=page.raw_json_bytes)
        for page in getattr(fetched, "comment_page_bodies", ())
    )
    fetch = YoutubeWatchFetch(
        video_id=video_id,
        raw_watch_html=getattr(fetched, "raw_watch_html"),
        packet=getattr(fetched, "packet"),
        comment_page_bodies=comment_pages_out,
    )
    return write_youtube_watch_packet(
        fetch,
        output_directory=output_directory,
        data_root=data_root,
        decision_question=decision_question,
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Capture YouTube watch-page metadata/comments into a SourceCapturePacket."
    )
    parser.add_argument("--video-id", required=True)
    target = parser.add_mutually_exclusive_group(required=False)
    target.add_argument("--output", type=Path, default=None)
    target.add_argument(
        "--data-root",
        default=None,
        help="Commit into the Forseti data lake at this root; FORSETI_DATA_ROOT is used only when --output is omitted; legacy ORCA_DATA_ROOT is also accepted.",
    )
    parser.add_argument(
        "--decision-question",
        default="Capture YouTube public watch-page metadata/comments for creator-momentum signal collection.",
    )
    parser.add_argument("--comment-pages", type=int, default=2)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    raw_argv = sys.argv[1:] if argv is None else argv
    args = parser.parse_args(
        normalize_video_id_argv(raw_argv, option_strings=parser._option_string_actions)
    )
    with exit_on_failure(parser, runner_name=_RUNNER_NAME, include_unexpected_type=True):
        data_root = resolve_output_root(
            args, parser, runner_name=_RUNNER_NAME, both_supplied_detail=SUPPLY_ONLY_ONE_DETAIL
        )
        exit_code, message = run_source_capture_youtube_watch_packet(
            video_id=args.video_id,
            output_directory=args.output if data_root is None else None,
            data_root=data_root,
            decision_question=args.decision_question,
            comment_pages=args.comment_pages,
        )

    if exit_code == 0:
        print(message)
        return 0
    parser.exit(status=exit_code, message=f"{_RUNNER_NAME} failed: {message}\n")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
