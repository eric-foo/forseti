"""Creator Registry join contract for validated audience triangulation snapshots."""

from __future__ import annotations

import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from schemas.creator_audience_models import CreatorAudienceTriangulationSnapshotV1
from schemas.tiktok_audience_evidence_models import CreatorAudienceTriangulationSnapshot


SNAPSHOT_SCHEMA_VERSION = "creator_audience_triangulation_snapshot_v1"
LEGACY_SNAPSHOT_SCHEMA_VERSION = "creator_audience_triangulation_snapshot_v0"
SNAPSHOT_WRAPPER_KEY = "creator_audience_triangulation_snapshots"


def validate_creator_audience_triangulation_snapshot(
    snapshot: Mapping[str, Any],
) -> dict[str, Any]:
    """Validate one already-Judged snapshot without weakening its strict schema."""

    model = (
        CreatorAudienceTriangulationSnapshotV1
        if snapshot.get("schema_version") == SNAPSHOT_SCHEMA_VERSION
        else CreatorAudienceTriangulationSnapshot
    )
    return model.model_validate(snapshot).model_dump(mode="json")


def load_creator_audience_triangulation_snapshot_document(
    path: str | Path,
) -> list[dict[str, Any]]:
    value = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    if not isinstance(value, Mapping):
        raise ValueError(f"audience triangulation document must be an object: {path}")
    if value.get("schema_version") in {
        SNAPSHOT_SCHEMA_VERSION, LEGACY_SNAPSHOT_SCHEMA_VERSION
    }:
        return [validate_creator_audience_triangulation_snapshot(value)]
    wrapped = value.get(SNAPSHOT_WRAPPER_KEY)
    if not isinstance(wrapped, list) or not wrapped:
        raise ValueError(
            "audience triangulation document must be one snapshot or a non-empty "
            f"{SNAPSHOT_WRAPPER_KEY!r} list"
        )
    return [validate_creator_audience_triangulation_snapshot(item) for item in wrapped]


__all__ = [
    "SNAPSHOT_SCHEMA_VERSION",
    "SNAPSHOT_WRAPPER_KEY",
    "load_creator_audience_triangulation_snapshot_document",
    "validate_creator_audience_triangulation_snapshot",
]
