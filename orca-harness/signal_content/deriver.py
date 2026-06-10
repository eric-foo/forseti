"""Signal Content Record (v0) deriver -- the carry-supplied-or-residualize pass.

Per the ratified architecture
(``docs/product/signal_content_record_deriver_architecture_plan_v0.md`` v0.1),
the deriver is a PURE function of its FROZEN inputs but is NOT packet-only: the
verbatim body (``raw_observation``), the ECR posture keys, and the authored
interpretation are explicit caller-supplied inputs -- the ``SourceCapturePacket``
carries only pointers (preserved-file ids + hashes), never the body text, never
an interpretation, never an ECR posture id. For every interpretive field whose
frozen input is absent, the deriver emits an HONEST RESIDUAL; it never
synthesizes, selects, or infers an interpretive value from packet prose.

v0 scope: the mechanical carry-shell + the residualize path, with the authored
interpretive core fully residualized (no authored-classification input exists in
source). One record per source slice that has a supplied body. Pure: no I/O, no
packet mutation, binds no ``EvidenceUnit``; no JSG-01, scoring, or readiness
claim. The authored interpretation lane is a declared-but-dormant seam.
"""
from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping, Sequence

from source_capture.models import (
    SourceCapturePacket,
    SourceCaptureSlice,
    VisibleFact,
    VisibleFactStatus,
)
from signal_content.models import (
    ContentReferences,
    DecisionRelevance,
    SignalContentRecord,
    SignalEventTimeReference,
    SignalEventTimeStatus,
    SignalFamily,
)

# State-1 honesty marker (the pipeline owes interpretive work). It is kept
# distinct from a state-2 EXTRACTED-BUT-ABSENT marker -- which only an authored
# input could legitimately produce and is therefore never reachable in v0. This
# is the brief's "not-extracted != no-such-content" honesty requirement.
_NOT_EXTRACTED = "NOT-EXTRACTED"
_EXTRACTED_ABSENT = "EXTRACTED-BUT-ABSENT"  # reserved; never emitted in v0

# Multi-body slice: the slice's supplied bodies are concatenated in
# ``preserved_file_ids`` order, joined by this labeled boundary. ``raw_observation``
# is an OPAQUE display/honesty anchor -- the boundary is display-only glue, NOT a
# reversible parser delimiter (a body could legitimately contain this string, so no
# consumer should reverse-parse ``raw_observation``). A single-body slice -- the
# common case -- carries its body purely verbatim. (v0 build decision.)
_BODY_BOUNDARY = "\n\n[signal_content_record: preserved-file boundary]\n\n"


def _content_id(packet_id: str, slice_id: str) -> str:
    """Deterministic, re-derive-stable, collision-resistant id over the FROZEN
    KEY TUPLE only (never the body).

    A canonical JSON encoding of the ``(packet_id, slice_id)`` tuple is hashed, so
    distinct key tuples cannot collide even when an id itself contains the legacy
    ``"::"`` separator (e.g. ``("a::b", "c")`` vs ``("a", "b::c")``). Stable across
    body changes -> re-derive safe.
    """
    payload = json.dumps(
        {"packet_id": packet_id, "slice_id": slice_id},
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return "scr::sha256::" + hashlib.sha256(payload).hexdigest()


def _slice_body(
    source_slice: SourceCaptureSlice, preserved_bodies: Mapping[str, str]
) -> str | None:
    """The verbatim ``raw_observation`` for a slice, or ``None`` when the slice's
    full body was not supplied (the emit gate).

    All-or-nothing: a record is emitted only when **every** referenced preserved
    file has a supplied non-empty body, carried in ``preserved_file_ids`` order. A
    slice with no referenced files, or with any referenced body missing or empty,
    yields **no record** -- partial slice evidence is never silently collapsed into
    a whole-slice record, and an empty or invented anchor is never emitted.
    """
    if not source_slice.preserved_file_ids:
        return None
    supplied: list[str] = []
    for file_id in source_slice.preserved_file_ids:
        body = preserved_bodies.get(file_id)
        if body is None or not body.strip():
            return None
        supplied.append(body)
    return _BODY_BOUNDARY.join(supplied)


def _residual_record(
    packet_id: str,
    slice_id: str,
    raw_observation: str,
    posture_refs: Sequence[str],
) -> SignalContentRecord:
    """A structurally complete, honestly-residual record: real keys + the verbatim
    body carried, the entire interpretive core residualized at state-1."""
    return SignalContentRecord(
        content_id=_content_id(packet_id, slice_id),
        signal_family=SignalFamily.RESIDUAL_FAMILY_UNRESOLVED,
        decision_relevance=DecisionRelevance.UNRESOLVED,
        subject_entity=VisibleFact(
            status=VisibleFactStatus.UNKNOWN_WITH_REASON,
            reason=(
                f"subject not extracted: no authored interpretive input bound to "
                f"packet {packet_id} ({_NOT_EXTRACTED}); raw_observation carries "
                f"the verbatim substance."
            ),
        ),
        event_or_claim=VisibleFact(
            status=VisibleFactStatus.UNKNOWN_WITH_REASON,
            reason=(
                f"claim not extracted: no authored interpretive input bound to "
                f"packet {packet_id} ({_NOT_EXTRACTED}); raw_observation carries "
                f"the verbatim substance."
            ),
        ),
        signal_event_time=SignalEventTimeReference(
            status=SignalEventTimeStatus.UNKNOWN_WITH_REASON,
            reason=(
                f"event-time anchor not supplied; the deriver does not select "
                f"publication-vs-edit from packet timing ({_NOT_EXTRACTED})."
            ),
        ),
        raw_observation=raw_observation,
        references=ContentReferences(
            packet_id=packet_id,
            slice_id=slice_id,
            ecr_posture_ref_ids=list(posture_refs),
        ),
    )


def derive_signal_content(
    packet: SourceCapturePacket,
    *,
    preserved_bodies: Mapping[str, str],
    ecr_posture_refs: Sequence[str] = (),
    authored_interpretation: object | None = None,
) -> list[SignalContentRecord]:
    """Derive the v0 Signal Content Records for a captured packet.

    One record per source slice that has a supplied body, in slice order. With
    ``authored_interpretation=None`` (the only state that exists in source today)
    every record's interpretive core is residualized: ``signal_family`` is
    ``RESIDUAL_FAMILY_UNRESOLVED``; ``subject_entity`` / ``event_or_claim`` /
    ``signal_event_time`` carry honest ``unknown_with_reason`` residuals;
    ``decision_relevance`` is ``UNRESOLVED``. The verbatim ``raw_observation`` is
    carried from ``preserved_bodies``; a slice with no supplied body emits no
    record.

    Pure: no I/O, no packet mutation, binds no ``EvidenceUnit``; no JSG-01,
    scoring, or readiness claim.

    - ``preserved_bodies`` maps ``PreservedFile.file_id`` -> verbatim body text;
      a thin caller performs the file read (the packet carries only pointers).
    - ``ecr_posture_refs`` are caller-materialized ECR posture keys (default
      empty; deduped; never synthesized -- the content<->integrity link is
      already carried by the shared ``packet_id`` / ``slice_id``).
    - ``authored_interpretation`` is a declared-but-dormant seam with no producer
      in v0; a non-None value raises rather than silently no-op (the deriver
      carries or residualizes and never authors).
    """
    if authored_interpretation is not None:
        raise NotImplementedError(
            "the authored interpretation lane is declared but not built (v0); the "
            "deriver carries or residualizes and never authors -- pass "
            "authored_interpretation=None."
        )
    posture_refs = list(dict.fromkeys(ecr_posture_refs))
    records: list[SignalContentRecord] = []
    for source_slice in packet.source_slices:
        body = _slice_body(source_slice, preserved_bodies)
        if body is None:
            continue
        records.append(
            _residual_record(
                packet.packet_id, source_slice.slice_id, body, posture_refs
            )
        )
    return records
