"""Family-agnostic parse-in-flight (content-mode) capture seam.

Owner doctrine (reddit_radar_grid_capture_maintenance_design_v0.md,
Storage and retention, 2026-07-17): fleet captures preserve the DERIVED
content record as the packet's hash-anchored file while the raw response
is hashed and then discarded; a rotating daily sample preserves BOTH raw
and derived in one packet so parser-fit drift checks have a stored target.
Content-mode capture is the standard posture, not a volume-triggered
exception; families flip by supplying their projector to this seam.

This module carries only the seam contract: the spec a capture runner
passes to ``run_source_capture_http_packet`` and the mode vocabulary.
Projectors stay with their source families; packet assembly stays with
``packet_assembly``; the provenance floor (raw sha256, parser version,
projection status) is recorded in the packet's preserved HTTP metadata.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

CAPTURE_ARTIFACT_MODES = ("raw", "content", "sample")
CONTENT_RECORD_FILENAME = "content_record.json"

# Exit code returned by the HTTP packet runner when in-flight projection
# fails: the raw response is preserved as a fallback packet (no evidence
# loss) and the failure stays visible to the calling batch runner.
CONTENT_PROJECTION_FAILED_EXIT_CODE = 4


@dataclass(frozen=True)
class ContentCaptureSpec:
    """What a runner supplies to capture in content or sample mode.

    ``projector`` maps ``(decoded_body, final_url)`` to a JSON-serializable
    content record and must be deterministic in its inputs (no timestamps,
    no randomness) so a parser-fit re-projection of sampled raw bytes can
    be compared byte-for-byte against the stored record.
    """

    capture_artifact_mode: str  # "content" | "sample"
    parser_version: str
    projector: Callable[[str, str], dict]

    def __post_init__(self) -> None:
        if self.capture_artifact_mode not in ("content", "sample"):
            raise ValueError(
                "ContentCaptureSpec covers content and sample modes only; "
                f"got {self.capture_artifact_mode!r} (raw mode passes no spec)"
            )
        if not self.parser_version or not self.parser_version.strip():
            raise ValueError("parser_version must be a non-empty string")


__all__ = [
    "CAPTURE_ARTIFACT_MODES",
    "CONTENT_RECORD_FILENAME",
    "CONTENT_PROJECTION_FAILED_EXIT_CODE",
    "ContentCaptureSpec",
]
