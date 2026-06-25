"""Adapter: a committed audience-post packet -> the Pass-1 ``PostInput`` (cleaning lane).

The read half of the audience-input surface ("A4"): given a verified
``data_lake.root.LoadedRawPacket`` produced by
``source_capture/audience_post_packet.py``, reconstruct the ``PostInput`` that Pass-1
audience extraction consumes. Identity comes from the packet, never fabricated.

This is a FAIL-CLOSED read boundary over lake bytes: it accepts only known
audience-post surfaces, requires exactly one caption and one metadata body, and
validates identity as non-empty strings (no coercion of non-string metadata). It
raises ``ValueError`` on any mismatch rather than producing a synthetic ``PostInput``.

Lives in `cleaning/` (where ``PostInput`` is defined) rather than in the capture
module, mirroring the transcript lane (capture writes packets; the cleaning/runner
side reads them). Deterministic and LLM-free: it only constructs a ``PostInput``
(a plain model), pulling in no LLM call.
"""

from __future__ import annotations

import json

from cleaning.audience_extractor import PostInput
from source_capture.audience_post_packet import (
    CAPTION_SUFFIX,
    METADATA_NAME,
    SUPPORTED_PLATFORMS,
    SURFACE_SUFFIX,
    bodies_by_suffix,
)

# Only the surfaces the audience-post assembler emits are adaptable (exact set, not a
# loose `*_post_text` suffix -- a foreign `<other>_post_text` packet must not be adapted).
ALLOWED_SURFACES = frozenset(f"{platform}{SURFACE_SUFFIX}" for platform in SUPPORTED_PLATFORMS)


def _one_body(loaded, suffix: str, what: str) -> bytes:
    matches = bodies_by_suffix(loaded, suffix)
    if len(matches) != 1:
        raise ValueError(f"audience-post packet must carry exactly one {what} (found {len(matches)})")
    return matches[0]


def _required_str(meta: dict, key: str) -> str:
    value = meta.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"audience-post metadata field {key!r} must be a non-empty string")
    return value


def post_input_from_packet(loaded, *, pillar_label: str | None = None) -> PostInput:
    """Map an audience-post ``LoadedRawPacket`` to a ``PostInput``.

    Raises ``ValueError`` on a non-audience-post packet (unknown surface, or a platform
    inconsistent with the surface), a zero-or-many caption/metadata ambiguity, non-object
    metadata, or a missing/non-string identity field."""
    surface = loaded.manifest.get("source_surface")
    if surface not in ALLOWED_SURFACES:
        raise ValueError(f"not an audience-post packet (source_surface={surface!r})")
    caption_bytes = _one_body(loaded, CAPTION_SUFFIX, "post-caption file")
    meta_bytes = _one_body(loaded, METADATA_NAME, "capture_metadata file")
    meta = json.loads(meta_bytes.decode("utf-8"))
    if not isinstance(meta, dict):
        raise ValueError("audience-post capture_metadata must be a JSON object")
    creator = _required_str(meta, "creator_handle")
    platform = _required_str(meta, "platform")
    post_id = _required_str(meta, "post_id")
    if platform not in SUPPORTED_PLATFORMS or surface != f"{platform}{SURFACE_SUFFIX}":
        raise ValueError(
            f"audience-post platform {platform!r} inconsistent with surface {surface!r}"
        )
    caption = caption_bytes.decode("utf-8")
    if not caption.strip():
        raise ValueError("audience-post packet caption is empty")
    bio = meta.get("bio")
    return PostInput(
        creator_id=creator,
        platform=platform,
        post_id=post_id,
        caption=caption,
        bio=bio if (isinstance(bio, str) and bio.strip()) else None,
        pillar_label=pillar_label,
    )
