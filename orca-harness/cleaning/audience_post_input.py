"""Adapter: a committed audience-post packet -> the Pass-1 ``PostInput`` (cleaning lane).

The read half of the audience-input surface ("A4"): given a verified
``data_lake.root.LoadedRawPacket`` produced by
``source_capture/audience_post_packet.py``, reconstruct the ``PostInput`` that Pass-1
audience extraction consumes. Identity comes from the packet, never fabricated.

Lives in `cleaning/` (where ``PostInput`` is defined) rather than in the capture
module, mirroring the transcript lane (capture writes packets; the cleaning/runner
side reads them into the extractor's input). This module is deterministic and LLM-free
on its own; it only constructs a ``PostInput`` (a plain model), pulling in no LLM call.
"""

from __future__ import annotations

import json

from cleaning.audience_extractor import PostInput
from source_capture.audience_post_packet import (
    CAPTION_SUFFIX,
    METADATA_NAME,
    SURFACE_SUFFIX,
    body_by_suffix,
)


def post_input_from_packet(loaded, *, pillar_label: str | None = None) -> PostInput:
    """Map an audience-post ``LoadedRawPacket`` to a ``PostInput``.

    Raises ``ValueError`` on a non-audience-post packet (wrong ``source_surface``) or
    incomplete material (missing caption / metadata / identity)."""
    surface = loaded.manifest.get("source_surface")
    if not isinstance(surface, str) or not surface.endswith(SURFACE_SUFFIX):
        raise ValueError(f"not an audience-post packet (source_surface={surface!r})")
    meta_bytes = body_by_suffix(loaded, METADATA_NAME)
    caption_bytes = body_by_suffix(loaded, CAPTION_SUFFIX)
    if meta_bytes is None or caption_bytes is None:
        raise ValueError("audience-post packet missing caption or capture_metadata")
    meta = json.loads(meta_bytes.decode("utf-8"))
    caption = caption_bytes.decode("utf-8")
    creator = str(meta.get("creator_handle") or "")
    platform = str(meta.get("platform") or "")
    post_id = str(meta.get("post_id") or "")
    bio = meta.get("bio")
    if not (creator and platform and post_id and caption.strip()):
        raise ValueError("audience-post packet metadata incomplete (creator/platform/post_id/caption)")
    return PostInput(
        creator_id=creator,
        platform=platform,
        post_id=post_id,
        caption=caption,
        bio=bio if (isinstance(bio, str) and bio.strip()) else None,
        pillar_label=pillar_label,
    )
