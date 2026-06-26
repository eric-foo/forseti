"""CLI: ONE-render IG reel deep-capture -- audience comments + creator transcript.

Renders a public reel ONCE via the browser-snapshot adapter, then derives BOTH
the audience comments (from the rendered DOM) AND the creator transcript (by
downloading the SAME render's audio handle and transcribing it) -- avoiding the
second yt-dlp page-resolve+fetch the standalone audio path costs.

No-LLM zone (``runners/``): imports the browser adapter, the deterministic
deep-capture parser, and the agnostic transcriber -- no LLM SDK. Public data only,
anonymous. The media handle is TRANSIENT (signed/expiring): it is downloaded into
a TemporaryDirectory for immediate transcription and is never persisted.
"""
from __future__ import annotations

import argparse
import os
import sys
import tempfile
import urllib.request
from pathlib import Path
from typing import Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from source_capture.adapters.browser_snapshot import (
    BrowserSnapshotFailure,
    fetch_browser_snapshot_capture,
)
from source_capture.ig_reels_deep_capture import run_reel_deep_capture
from source_capture.transcript.audio_asr import transcribe_audio

# A realistic desktop UA: the signed fbcdn handle is served to the same anonymous
# context the render used; a bare urllib UA is more likely to be refused.
_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)


def _render(shortcode: str) -> str | None:
    url = f"https://www.instagram.com/reel/{shortcode}/"
    res = fetch_browser_snapshot_capture(
        url=url,
        wait_until="networkidle",
        timeout_seconds=60.0,
        viewport_width=1280,
        viewport_height=2200,
        settle_seconds=6.0,
        headless=True,
    )
    if isinstance(res, BrowserSnapshotFailure):
        return None
    return res.rendered_dom or None


def _make_downloader(scratch_dir: str):
    def _download(url: str) -> str | None:
        try:
            request = urllib.request.Request(url, headers={"User-Agent": _UA})
            with urllib.request.urlopen(request, timeout=60) as response:
                data = response.read()
        except Exception:  # noqa: BLE001 - any fetch error is a typed miss, not a crash
            return None
        if not data:
            return None
        path = os.path.join(scratch_dir, "reel_audio.mp4")
        with open(path, "wb") as handle:
            handle.write(data)
        return path

    return _download


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="One-render IG reel deep-capture (audience comments + creator transcript)."
    )
    parser.add_argument("--shortcode", required=True, help="IG Reel shortcode (e.g. DaA8n7EhqTR).")
    parser.add_argument("--model", default="small", help="faster-whisper model size.")
    args = parser.parse_args(argv)

    with tempfile.TemporaryDirectory(prefix="orca_deepcap_") as scratch:
        result = run_reel_deep_capture(
            args.shortcode,
            render_fn=_render,
            download_fn=_make_downloader(scratch),
            transcribe_fn=lambda path: transcribe_audio(path, model_name=args.model),
        )
        # transcription happens inside this block, while the temp audio file still exists.

    print(
        f"reel={result.reel_shortcode} "
        f"comments={len(result.comments)} "
        f"transcript_posture={result.transcript_posture} "
        f"transcript_cues={len(result.transcript_cues)} "
        f"audio_handle={'used' if result.media_url_used else 'none'}"
    )
    for note in result.notes:
        print(f"  note: {note}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
