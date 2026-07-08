"""Persist the pure ECR source-side derivers' output into the Data Lake.

The verified read half (by-key, hash-checked) lives on ``DataLakeRoot``; this
thin adapter reads a committed packet by key, runs the four pure ECR derivers,
and appends each epistemic kind's posture list as a sibling derived record at
``derived/<packet_id>/ecr_<kind>/<record_id>.json``. The four siblings of one
derivation are written as an all-or-nothing set (``DataLakeRoot.append_record_set``)
with a completion marker in ``ecr_set`` written last in process order. Crash or
post-crash durable states are detectable as incomplete unless the marker exists
and every member it names is present. Re-derive = a new sibling set (fresh
``record_id``).

Boundary: this persists already-authorized deriver output only. It binds no
``EvidenceUnit``, runs no SP-5 finalizer, and performs no Cleaning or Judgment;
those stay separately gated (``.agents/workflow-overlay/safety-rules.md``). All
I/O is isolated here so the derivers in ``ecr.deriver`` stay pure.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING

from ecr.deriver import (
    derive_identity_postures,
    derive_inspectability_postures,
    derive_source_visibility_postures,
    derive_timing_postures,
)
from harness_utils import generate_ulid
from source_capture.models import SourceCapturePacket

if TYPE_CHECKING:
    from data_lake.root import DataLakeRoot


# Append-only derived lane namespace per ECR epistemic kind (siblings per kind).
ECR_LANES: dict[str, str] = {
    "timing": "ecr_timing",
    "inspectability": "ecr_inspectability",
    "identity": "ecr_identity",
    "source_visibility": "ecr_source_visibility",
}
# Lane carrying the per-derivation completion marker for the four sibling records.
ECR_COMPLETION_LANE = "ecr_set"


def _record_bytes(postures) -> bytes:
    return (
        f"{json.dumps([posture.model_dump(mode='json') for posture in postures], indent=2, sort_keys=True)}\n"
    ).encode("utf-8")


def derive_ecr_into_lake(
    *,
    data_root: "DataLakeRoot",
    packet_id: str,
    record_id: str | None = None,
) -> dict[str, Path]:
    """Derive the four source-side ECR postures for a committed raw packet -- read
    by key from the lake and hash-verified -- and append them as one all-or-nothing
    sibling set (four ``ecr_<kind>`` records plus an ``ecr_set`` completion marker,
    the marker written last). Returns ``{lane: path}`` for the four member records;
    the four siblings of one derivation share a single ``record_id``. Re-derive = a
    new sibling set; a crash mid-set is detectable via
    ``DataLakeRoot.is_record_set_complete``.

    Persists already-authorized deriver output only -- no EvidenceUnit binding,
    SP-5 finalizer, Cleaning, or Judgment.
    """
    loaded = data_root.load_raw_packet(packet_id)
    packet = SourceCapturePacket.model_validate(loaded.manifest)
    record = record_id if record_id is not None else generate_ulid()
    postures_by_kind = {
        "timing": derive_timing_postures(packet),
        "inspectability": derive_inspectability_postures(packet),
        "identity": derive_identity_postures(packet),
        "source_visibility": derive_source_visibility_postures(packet),
    }
    members = {
        ECR_LANES[kind]: _record_bytes(postures) for kind, postures in postures_by_kind.items()
    }
    return data_root.append_record_set(
        subtree="derived",
        raw_anchor=packet_id,
        record_id=f"{record}.json",
        members=members,
        completion_lane=ECR_COMPLETION_LANE,
    )


__all__ = ["ECR_LANES", "ECR_COMPLETION_LANE", "derive_ecr_into_lake"]
