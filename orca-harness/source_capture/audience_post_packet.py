#!/usr/bin/env python3
"""Build a SourceCapturePacket from a creator's POST TEXT (Capture layer; network-free).

This is the AUDIENCE-inference input surface ("A4"): a creator's own WRITTEN post
caption + profile bio + identity, staged as a contract-compliant SourceCapturePacket
and persisted to the data lake. It is the input that Pass-1 audience extraction
(`cleaning/audience_extractor.py`) reads as a `PostInput` -- the deterministic,
LLM-free bridge between capture and the audience lane (Slice C, deferred). The
packet -> PostInput adapter lives in the cleaning lane (`cleaning/audience_post_input.py`),
not here, so this capture module imports nothing from cleaning.

Distinct from the transcript spine: a transcript packet carries SPOKEN text (caption
track / ASR); this carries the creator's WRITTEN post text + bio. No transcription, no
LLM. Network-free: it takes an already-fetched `AudiencePostFetch` (the live fetch is
upstream -- YouTube video title+description via the existing watch capture; Instagram
post caption + profile bio), so it is fully unit-testable from a canned fetch -- the
same discipline as `source_capture/transcript/caption_packet.py`, which this mirrors.

Identity is per-platform and object-level: `creator_handle` is the public platform
handle/id, NOT a cross-platform or person identity (honors the medallion contract's
given-up cross-platform-identity limitation).

RESIDUAL: the Instagram profile-bio capture is a separate queued capture-add. An IG
fetch without a bio is still valid (bio is optional), but IG audience signal is thin
without it (the bio is IG's strongest positioning text); a bio-less packet records the
gap as a capture-level limitation.
"""
from __future__ import annotations

import datetime
import json
import re
from dataclasses import dataclass
from pathlib import Path

from source_capture.models import (
    CaptureModeCategory,
    PacketTiming,
    SourceCaptureSlice,
    known_fact,
    not_applicable,
    not_attempted,
    unknown_with_reason,
)
from source_capture.packet_assembly import stage_and_write_packet, staged_file_id_map

AUDIENCE_POST_NON_CLAIMS = [
    "not a cleaned or normalized caption (raw creator-authored text only)",
    "not audience inference (no positioning labels; that is the Pass-1 cleaning lane)",
    "not demographic, biometric, or person inference of any kind",
    "not a transcript (this is the creator's WRITTEN post text + bio, not spoken words)",
    "not media preservation, not follower data, not private/auth-gated data",
]

SUPPORTED_PLATFORMS = ("instagram", "youtube")
# Packet-shape constants -- the cleaning-lane adapter reads packets by these.
CAPTION_SUFFIX = ".post_caption.txt"
METADATA_NAME = "capture_metadata.json"
SURFACE_SUFFIX = "_post_text"


@dataclass(frozen=True)
class AudiencePostFetch:
    """One creator post's public WRITTEN text + identity -- the audience-input payload.

    `creator_handle` is the platform-public handle/id (object-level; NOT a cross-platform
    or person identity). `caption` is the creator's own post text; `bio` is the profile
    bio (optional -- the IG bio is a separate queued capture-add)."""

    platform: str
    post_id: str
    creator_handle: str
    caption: str
    bio: str | None = None
    canonical_url: str | None = None
    publish_date_iso: str | None = None
    tooling: str | None = None


def write_audience_post_packet(
    fetch: AudiencePostFetch,
    *,
    output_directory: Path | None = None,
    data_root=None,
    decision_question: str,
    now_iso: str | None = None,
) -> tuple[int, str]:
    """Stage an AudiencePostFetch into a SourceCapturePacket. Returns (exit_code, message)."""
    if fetch.platform not in SUPPORTED_PLATFORMS:
        return 5, f"unsupported platform {fetch.platform!r} (expected one of {SUPPORTED_PLATFORMS})"
    if not (fetch.post_id or "").strip():
        return 5, "refusing to build packet: empty post_id"
    if not (fetch.creator_handle or "").strip():
        return 5, "refusing to build packet: empty creator_handle"
    if not (fetch.caption or "").strip():
        return 4, f"no caption text for {fetch.platform}:{fetch.post_id} (nothing to infer from)"

    # Never build filenames/paths from an unvalidated id (path-traversal guard).
    safe_post = re.sub(r"[^A-Za-z0-9_-]", "_", fetch.post_id)[:80] or "post"
    bio_present = bool(fetch.bio and fetch.bio.strip())
    capture_ts = now_iso or (datetime.datetime.utcnow().isoformat() + "Z")
    identity = {
        "platform": fetch.platform,
        "creator_handle": fetch.creator_handle,
        "post_id": fetch.post_id,
        "canonical_url": fetch.canonical_url,
        "bio": fetch.bio,
        "bio_present": bio_present,
        "publish_date_iso": fetch.publish_date_iso,
        "tooling": fetch.tooling,
        "capture_timestamp": capture_ts,
    }
    caption_name = f"{safe_post}{CAPTION_SUFFIX}"
    artifacts: list[tuple[str, bytes]] = [
        (caption_name, fetch.caption.encode("utf-8")),
        (METADATA_NAME, (json.dumps(identity, indent=2, sort_keys=True) + "\n").encode("utf-8")),
    ]
    file_ids = staged_file_id_map(artifacts)

    locator = (
        known_fact(fetch.canonical_url)
        if fetch.canonical_url
        else unknown_with_reason("no canonical post URL supplied by the fetch")
    )
    pub = (
        known_fact(fetch.publish_date_iso)
        if fetch.publish_date_iso
        else unknown_with_reason("fetch did not expose a post publish date")
    )
    timing = PacketTiming(
        source_publication_or_event=pub,
        source_edit_or_version=not_applicable("post text carries no source edit/version timing"),
        capture_time=known_fact(capture_ts),
        recapture_time=not_applicable("no prior post-text capture was supplied"),
        cutoff_posture=not_applicable("cutoff posture does not apply to a post-text capture"),
    )
    access_posture = known_fact(
        f"post caption text captured for {fetch.platform}:{fetch.post_id}"
        + ("; profile bio captured" if bio_present else "; no profile bio (residual)")
    )
    archive_posture = not_attempted("post-text capture does not query archive/history services")
    media_posture = not_attempted("post-text capture preserves written text only; no media assets fetched")
    recapture_posture = not_applicable("no prior post-text capture packet supplied")

    result = stage_and_write_packet(
        output_directory=output_directory,
        data_root=data_root,
        staged_artifacts=artifacts,
        source_slices=[
            SourceCaptureSlice(
                slice_id="slice_01",
                locator=locator,
                timing=timing,
                access_posture=access_posture,
                archive_history_posture=archive_posture,
                media_modality_posture=media_posture,
                re_capture_relationship=recapture_posture,
                preserved_file_ids=[file_ids[caption_name], file_ids[METADATA_NAME]],
            )
        ],
        source_family=fetch.platform,
        source_surface=f"{fetch.platform}{SURFACE_SUFFIX}",
        source_locator=locator,
        decision_question=decision_question,
        capture_context=(
            "Public creator post-text capture (written caption + profile bio) for the "
            "audience-inference input surface; deterministic, no transcription, no LLM"
        ),
        actor_audience_context=not_applicable(
            "object-level creator-content capture; no actor/audience modeling at capture"
        ),
        capture_mode=CaptureModeCategory.AUTOMATED_EXTRACTION,
        operator_category="audience_post_cli_operator",
        session_identity=None,
        visible_mode_changes=[],
        source_publication_or_event=timing.source_publication_or_event,
        source_edit_or_version=timing.source_edit_or_version,
        cutoff_posture=timing.cutoff_posture,
        recapture_time=timing.recapture_time,
        access_posture=access_posture,
        archive_history_posture=archive_posture,
        media_modality_posture=media_posture,
        re_capture_relationship=recapture_posture,
        warnings=[],
        limitations=(
            []
            if bio_present
            else ["profile bio not captured (queued IG bio-capture add); audience signal is thinner without it"]
        ),
        receipt_summary=(
            f"Audience post-text packet for {fetch.platform}:{fetch.post_id}: "
            f"{len(fetch.caption)} caption chars, bio={'yes' if bio_present else 'no'}."
        ),
        receipt_non_claims=AUDIENCE_POST_NON_CLAIMS,
    )
    return 0, result.output_directory


def body_by_suffix(loaded, suffix: str) -> bytes | None:
    """Return the preserved-file bytes whose packet-relative path ends with ``suffix``.

    A pure read helper over a ``data_lake.root.LoadedRawPacket`` (manifest + bodies);
    the cleaning-lane adapter uses it to locate the caption + metadata bodies by key."""
    for preserved in loaded.manifest.get("preserved_files", []):
        if not isinstance(preserved, dict):
            continue
        rel = preserved.get("relative_packet_path")
        if isinstance(rel, str) and rel.endswith(suffix):
            file_id = preserved.get("file_id")
            if isinstance(file_id, str) and file_id in loaded.bodies:
                return loaded.bodies[file_id]
    return None
