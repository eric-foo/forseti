"""Transcript acquisition (Capture layer) — cross-source.

Per-platform fetchers return RAW artifacts (the authoritative bytes) + capture
metadata; `caption_packet.write_caption_packet` stages them into a
SourceCapturePacket. The clean/readable transcript is a downstream Cleaning
transform, never produced here. ASR-derived output is gated on the FileDerivation
manifest extension and is NOT in this v0.
"""
from source_capture.transcript.caption_packet import (
    CAPTION_NON_CLAIMS,
    write_caption_packet,
)
from source_capture.transcript.youtube_captions import (
    CaptionFetch,
    fetch_youtube_caption_artifacts,
    flatten_json3,
)

__all__ = [
    "CaptionFetch",
    "fetch_youtube_caption_artifacts",
    "flatten_json3",
    "write_caption_packet",
    "CAPTION_NON_CLAIMS",
]
