"""CLI: capture Instagram Reel audio + write an ASR transcript derived record (IG transcript spine v0).

IG Reels have no caption API, so ASR is the only transcript route. Data-lake-mode only (the
transcript is a derived record via DataLakeRoot.append_record). Downloads bestaudio anonymously
(yt-dlp, no login / no proxy), captures it as a SourceCapturePacket
(source_family=instagram_creator, source_surface=ig_reels_audio), then writes
derived/<audio-packet_id>/transcript_asr/<id> with VAD-gated faster-whisper output + provenance.

An audience-restricted Reel ("can't be seen by certain audiences") is a TYPED SKIP (exit 7),
not a hard failure — anonymous-only capture honestly cannot see it. Public data only; captured
/derived data lives in the lake (never the repo).

No-LLM zone (`runners/`): imports the IG audio module + the agnostic transcriber, but no LLM SDK.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from source_capture.transcript.audio_asr import transcribe_audio
from source_capture.transcript.ig_reels_audio_packet import (
    download_ig_reel_audio,
    ig_shortcode_from_url,
    write_ig_reels_asr_transcript,
)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Capture Instagram Reel audio + write an ASR transcript derived record."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--shortcode", default=None, help="IG Reel shortcode (e.g. DZ69knlsDb1).")
    group.add_argument("--url", default=None, help="IG Reel URL (/reel/<shortcode>/ or /p/<shortcode>/).")
    parser.add_argument("--data-root", default=None, help="Forseti data lake root (or FORSETI_DATA_ROOT (legacy ORCA_DATA_ROOT)). ASR is data-lake-mode.")
    parser.add_argument("--model", default="small")
    args = parser.parse_args(argv)

    shortcode = args.shortcode or ig_shortcode_from_url(args.url or "")
    if not shortcode:
        parser.exit(status=2, message=f"could not resolve an IG shortcode from {args.url or args.shortcode!r}\n")

    from data_lake.root import DataLakeRoot

    try:
        root = DataLakeRoot.resolve(explicit=args.data_root)
    except Exception as exc:  # noqa: BLE001
        parser.exit(status=2, message=f"data root required (ASR writes a derived record): {exc}\n")

    fetch = download_ig_reel_audio(shortcode)
    if fetch.status == "access_gated":
        # Anonymous-only capture cannot see an audience-restricted Reel: a typed skip, not a failure.
        parser.exit(status=7, message=f"skipped (access_gated, anonymous cannot view): {shortcode} :: {fetch.detail}\n")
    if fetch.status != "ok" or fetch.audio_bytes is None:
        parser.exit(status=4, message=f"audio unavailable for {shortcode}: {fetch.detail}\n")

    try:
        code, msg = write_ig_reels_asr_transcript(
            shortcode=shortcode,
            audio_bytes=fetch.audio_bytes,
            audio_ext=fetch.audio_ext or "bin",
            transcribe_fn=lambda path: transcribe_audio(path, model_name=args.model),
            data_root=root,
        )
    except Exception as exc:  # noqa: BLE001 - capture/lake errors surface here
        parser.exit(status=3, message=f"ig asr transcript failed: {type(exc).__name__}: {exc}\n")

    if code == 0:
        print(msg)
        return 0
    parser.exit(status=code, message=f"ig asr: {msg}\n")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
