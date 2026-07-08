"""Persist the pure Signal Content Record deriver's output into the Data Lake.

Parallel to ``ecr/lake.py``: the verified read half (by-key, hash-checked) lives
on ``DataLakeRoot``; this thin adapter reads a committed packet by key, decodes
the preserved bodies, runs the pure ``derive_signal_content`` deriver, and
appends the records as a single derived record at
``derived/<packet_id>/signal_content/<record_id>.json`` (append-only; re-derive =
new sibling).

``ecr_posture_refs`` is optional (default empty): SCR does not require ECR to be
persisted first -- the content<->integrity link rides on the shared
``packet_id`` / ``slice_id`` (see ``signal_content.deriver``). The body bytes are
decoded ``utf-8`` / ``replace`` because ``raw_observation`` is an opaque
display/honesty anchor, never reverse-parsed. Boundary: persists deriver output
only; binds no ``EvidenceUnit`` and performs no Cleaning or Judgment. All I/O is
isolated here so the deriver stays pure.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING, Sequence

from harness_utils import generate_ulid
from signal_content.deriver import derive_signal_content
from source_capture.models import SourceCapturePacket

if TYPE_CHECKING:
    from data_lake.root import DataLakeRoot


# Append-only derived lane namespace for the Signal Content Record.
SIGNAL_CONTENT_LANE = "signal_content"


def derive_signal_content_into_lake(
    *,
    data_root: "DataLakeRoot",
    packet_id: str,
    record_id: str | None = None,
    ecr_posture_refs: Sequence[str] = (),
) -> Path:
    """Derive the Signal Content Records for a committed raw packet -- read by key
    from the lake and hash-verified -- and append them as a single derived record
    at ``derived/<packet_id>/signal_content/<record_id>.json``. Append-only;
    re-derive = new sibling. ``ecr_posture_refs`` is optional provenance (SCR does
    not require ECR persisted). Persists deriver output only.
    """
    loaded = data_root.load_raw_packet(packet_id)
    packet = SourceCapturePacket.model_validate(loaded.manifest)
    preserved_bodies = {
        file_id: body.decode("utf-8", "replace") for file_id, body in loaded.bodies.items()
    }
    records = derive_signal_content(
        packet,
        preserved_bodies=preserved_bodies,
        ecr_posture_refs=tuple(ecr_posture_refs),
    )
    record = record_id if record_id is not None else generate_ulid()
    data = (
        f"{json.dumps([scr.model_dump(mode='json') for scr in records], indent=2, sort_keys=True)}\n"
    ).encode("utf-8")
    return data_root.append_record(
        subtree="derived",
        raw_anchor=packet_id,
        lane=SIGNAL_CONTENT_LANE,
        record_id=f"{record}.json",
        data=data,
    )


__all__ = ["SIGNAL_CONTENT_LANE", "derive_signal_content_into_lake"]
