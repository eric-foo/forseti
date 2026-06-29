"""CLI: capture a YouTube public caption track into a SourceCapturePacket (transcript spine v0).

Thin wrapper: fetch the original-language caption json3 via yt-dlp (default token-free client),
then stage the RAW json3 + capture metadata into a contract-compliant SourceCapturePacket and
write a NON-AUTHORITATIVE flat-text view beside it. Packet-build logic lives in
source_capture.transcript.caption_packet (network-free, unit-tested). No-caption videos are
reported as ASR-required (ASR path gated on the FileDerivation manifest extension). Public data only.
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from source_capture.transcript import fetch_youtube_caption_artifacts, write_caption_packet


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Capture a YouTube caption track into a SourceCapturePacket.")
    parser.add_argument("--video-id", required=True)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument(
        "--data-root",
        default=None,
        help="Commit into the Orca data lake at this root; explicit --data-root is mutually exclusive with --output. ORCA_DATA_ROOT is used only when --output is omitted.",
    )
    parser.add_argument(
        "--decision-question",
        default="Capture YouTube public caption transcript for the creator-momentum signal (transcript spine v0).",
    )
    args = parser.parse_args(argv)

    data_root = None
    output_directory = args.output
    if output_directory is not None and args.data_root is not None:
        parser.exit(status=2, message="exactly one of --output or --data-root/ORCA_DATA_ROOT is required\n")
    data_root_requested = args.data_root is not None or (
        output_directory is None and os.environ.get("ORCA_DATA_ROOT")
    )
    if data_root_requested:
        from data_lake.root import DataLakeRoot

        data_root = DataLakeRoot.resolve(explicit=args.data_root)
        output_directory = None
    if (output_directory is None) == (data_root is None):
        parser.exit(status=2, message="exactly one of --output or --data-root/ORCA_DATA_ROOT is required\n")

    try:
        cap = fetch_youtube_caption_artifacts(args.video_id)
        exit_code, message = write_caption_packet(
            cap,
            output_directory=output_directory,
            data_root=data_root,
            decision_question=args.decision_question,
        )
    except Exception as exc:  # noqa: BLE001 - surface the real failure to the operator
        parser.exit(status=3, message=f"youtube caption capture failed: {type(exc).__name__}: {exc}\n")

    if exit_code == 0:
        print(message)
        return 0
    parser.exit(status=exit_code, message=f"youtube caption capture: {message}\n")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
