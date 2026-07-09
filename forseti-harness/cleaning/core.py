"""Pure helpers for the Cleaning Spine v0 source-invariant core."""
from __future__ import annotations

from collections import defaultdict
import hashlib

from cleaning.models import (
    CleaningDedupeBasis,
    CleaningDedupeGroup,
    CleaningInputHandle,
    CleaningRawAnchor,
)


def _raw_anchor_identity(anchor: CleaningRawAnchor) -> tuple[str, ...]:
    return (
        anchor.packet_id,
        anchor.slice_id,
        anchor.file_id,
        anchor.relative_packet_path,
        anchor.sha256,
        anchor.hash_basis,
        anchor.anchor_kind,
        anchor.anchor_value or "",
        anchor.json_pointer or "",
    )


def _group_id_for_identity(identity: tuple[str, ...]) -> str:
    digest = hashlib.sha256("\x1f".join(identity).encode("utf-8")).hexdigest()[:16]
    return f"exact_raw_anchor:{digest}"


def derive_exact_identity_duplicate_groups(
    handles: list[CleaningInputHandle],
) -> list[CleaningDedupeGroup]:
    """Group handles whose full raw-anchor identity is exactly identical.

    This is the only dedupe derivation in core v0. It does not compute
    similarity, copied-language grouping, clustering, or any Judgment effect.
    """
    grouped: dict[tuple[str, ...], list[str]] = defaultdict(list)
    for handle in handles:
        grouped[_raw_anchor_identity(handle.raw_anchor)].append(handle.handle_id)

    duplicate_groups: list[CleaningDedupeGroup] = []
    for identity, member_ids in grouped.items():
        if len(member_ids) < 2:
            continue
        sorted_members = sorted(member_ids)
        duplicate_groups.append(
            CleaningDedupeGroup(
                group_id=_group_id_for_identity(identity),
                basis=CleaningDedupeBasis.RAW_ANCHOR_IDENTITY,
                member_handle_ids=sorted_members,
                instance_count=len(sorted_members),
            )
        )
    return sorted(duplicate_groups, key=lambda group: group.group_id)
