"""Capture-time content extraction and retention contracts.

Capture owns deterministic, source-family extraction before disposable source
envelopes are released.  The retained ``content_record.json`` is canonical
captured evidence for content-eligible routes; it is not a Projection packet.
Raw retention remains available for sources whose bytes are evidence and is
the fail-loud fallback whenever admission or extraction fails.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Literal

CAPTURE_RETENTION_MODES = ("content", "raw")
CONTENT_RECORD_FILENAME = "content_record.json"
CONTENT_EXTRACTION_FAILED_EXIT_CODE = 4

RequestedRetentionMode = Literal["content", "raw"]
RetentionOutcome = Literal["content", "raw", "raw_failure"]


@dataclass(frozen=True)
class ContentExtractionSpec:
    """Deterministic extraction contract for one direct-HTTP response."""

    requested_retention_mode: RequestedRetentionMode
    extractor_version: str
    extractor: Callable[[str, str], dict]
    # Raw retention normally skips extraction entirely, which also skips any
    # shape check the extractor performs.  A raw sample kept to AUDIT the
    # projection is then the one packet nobody audits -- it banks whatever the
    # server returned, including a login wall, and reports success.  Opt in to
    # run the extractor purely as a validity check: raw is still what gets
    # preserved, but a raising extractor marks the packet raw_failure instead
    # of clean.  Default False, so no existing caller changes behavior.
    validate_in_raw_mode: bool = False

    def __post_init__(self) -> None:
        if self.requested_retention_mode not in CAPTURE_RETENTION_MODES:
            raise ValueError(
                "requested_retention_mode must be one of "
                f"{CAPTURE_RETENTION_MODES}; got {self.requested_retention_mode!r}"
            )
        if not self.extractor_version.strip():
            raise ValueError("extractor_version must be a non-empty string")


@dataclass(frozen=True)
class RenderedContentExtractionSpec:
    """Deterministic extraction contract for rendered DOM/text capture."""

    requested_retention_mode: RequestedRetentionMode
    extractor_version: str
    extractor: Callable[[bytes, bytes, str], dict]
    json_indent: int | None = 2

    def __post_init__(self) -> None:
        if self.requested_retention_mode not in CAPTURE_RETENTION_MODES:
            raise ValueError(
                "requested_retention_mode must be one of "
                f"{CAPTURE_RETENTION_MODES}; got {self.requested_retention_mode!r}"
            )
        if not self.extractor_version.strip():
            raise ValueError("extractor_version must be a non-empty string")
        if self.json_indent is not None and self.json_indent < 0:
            raise ValueError("json_indent must be non-negative or None")


__all__ = [
    "CAPTURE_RETENTION_MODES",
    "CONTENT_EXTRACTION_FAILED_EXIT_CODE",
    "CONTENT_RECORD_FILENAME",
    "ContentExtractionSpec",
    "RenderedContentExtractionSpec",
    "RequestedRetentionMode",
    "RetentionOutcome",
]
