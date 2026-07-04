"""Shared multi-slice ``SourceCapturePacket`` builder for ECR source-side tests.

This is test-support code (underscore-prefixed so pytest does not collect it). It
builds real, producer-valid packets at the variety the ECR source-side derivers
need to be exercised *together*. It imports only the producer models -- it has no
``ecr`` import, calls no deriver, and encodes no ECR semantics; it is a pure
producer-packet builder. The downstream mixed-grain integration test (and the
future SP-6 / real-packet tests) import this module rather than re-deriving a
builder per file.

Each slice spec drives the slice-grain inputs the three derivers read::

    {
        "id": str,                     # slice_id
        "files": [(file_id, sha256)],  # SP-2 inspectability inputs
        "locator_known": bool,         # SP-2: is the slice locator KNOWN?
        "cutoff": str | None,          # SP-3: cutoff_posture
    }

``cutoff`` is a closed ``CUTOFF_POSTURE_VALUES`` token (carried as a KNOWN fact)
or ``None`` (carried as a ``not_attempted`` residual, status != KNOWN).
Packet-level identity (``source_family`` / ``source_surface`` /
``source_locator``) drives SP-1 and is set per call; defaults are fully specific
(SP-1 resolved). Reach the other SP-1 states by override: empty ``source_family``
-> unresolved; specific family but empty ``source_surface`` and/or a non-KNOWN
``source_locator`` -> family_only.

Read contract (for the downstream mixed-grain integration test)
---------------------------------------------------------------
The three derivers produce one parallel ECR record per packet, at mixed grain:

- SP-1 identity is keyed by ``packet_id`` -- exactly ONE posture per packet.
- SP-2 inspectability and SP-3 timing are keyed by ``slice_id`` -- exactly ONE
  posture per source slice, in ``source_slices`` order.
- The two slice-keyed posture lists align 1:1, by order and exact ``slice_id``,
  with ``packet.source_slices`` before the downstream test joins them.
- Each posture's concrete state/value and ``clears_*`` flag is independently
  readable at its own grain; composing them into any overall source-side verdict
  is the frozen conductor's job, not this record's.
"""
from __future__ import annotations

from source_capture.models import (
    OBLIGATION_CONTRACT_VERSION,
    SOURCE_CAPTURE_MANIFEST_VERSION,
    CaptureModeCategory,
    PacketTiming,
    PreservedFile,
    ReceiptMetadata,
    SourceCapturePacket,
    SourceCaptureSlice,
    VisibleFact,
    known_fact,
    not_applicable,
    not_attempted,
)

_VERIFIABLE_SHA = "a" * 64  # 64 hex, not all-zero -> SP-2 verifiable
_PLACEHOLDER_SHA = "0" * 64  # all-zero sentinel -> SP-2 not verifiable


def _cutoff_fact(cutoff: str | None) -> VisibleFact:
    """A KNOWN closed cutoff token, or a ``not_attempted`` residual when ``None``."""
    if cutoff is None:
        return not_attempted("no cutoff posture captured")
    return known_fact(cutoff)


def _slice_timing(cutoff: str | None) -> PacketTiming:
    """Slice timing whose only decision-bearing fact is ``cutoff_posture``."""
    na = not_applicable("test")
    return PacketTiming(
        source_publication_or_event=na,
        source_edit_or_version=na,
        capture_time=na,
        recapture_time=na,
        cutoff_posture=_cutoff_fact(cutoff),
    )


def _packet_timing() -> PacketTiming:
    """Packet-level timing (no deriver reads it; all not_applicable)."""
    na = not_applicable("test")
    return PacketTiming(
        source_publication_or_event=na,
        source_edit_or_version=na,
        capture_time=na,
        recapture_time=na,
        cutoff_posture=na,
    )


def build_packet(
    slice_specs: list[dict],
    *,
    packet_id: str = "pkt-test",
    source_family: str = "reddit",
    source_surface: str = "r/example",
    source_locator: VisibleFact | None = None,
    archive_history: VisibleFact | None = None,
) -> SourceCapturePacket:
    """Build a producer-valid packet from per-slice specs (see module docstring).

    Every preserved file is referenced by the slice that lists it, so the
    packet's uniqueness and no-orphan invariants hold. At least one slice must
    list a file (the packet requires >=1 preserved file).
    """
    preserved: dict[str, str] = {}
    slices: list[SourceCaptureSlice] = []
    for spec in slice_specs:
        files = spec.get("files", [])
        for file_id, sha in files:
            preserved[file_id] = sha
        slices.append(
            SourceCaptureSlice(
                slice_id=spec["id"],
                locator=(
                    known_fact("loc")
                    if spec.get("locator_known")
                    else not_applicable("test")
                ),
                timing=_slice_timing(spec.get("cutoff")),
                access_posture=not_applicable("test"),
                archive_history_posture=not_applicable("test"),
                media_modality_posture=not_applicable("test"),
                re_capture_relationship=not_applicable("test"),
                preserved_file_ids=[file_id for file_id, _ in files],
            )
        )
    preserved_files = [
        PreservedFile(
            file_id=file_id,
            original_path="/tmp/x",
            relative_packet_path=file_id,
            sha256=sha,
            hash_basis="raw_stored_bytes",
            size_bytes=0,
        )
        for file_id, sha in preserved.items()
    ]
    return SourceCapturePacket(
        packet_id=packet_id,
        manifest_version=SOURCE_CAPTURE_MANIFEST_VERSION,
        obligation_contract_version=OBLIGATION_CONTRACT_VERSION,
        source_family=source_family,
        source_surface=source_surface,
        source_locator=(
            source_locator if source_locator is not None else known_fact("https://x/1")
        ),
        requested_decision_context=not_applicable("test"),
        capture_context=not_applicable("test"),
        actor_audience_context=not_applicable("test"),
        capture_mode=CaptureModeCategory.MIXED,
        operator_category="test",
        session_identity="test",
        timing=_packet_timing(),
        access_posture=not_applicable("test"),
        archive_history_posture=(
            archive_history if archive_history is not None else not_applicable("test")
        ),
        media_modality_posture=not_applicable("test"),
        re_capture_relationship=not_applicable("test"),
        source_slices=slices,
        preserved_files=preserved_files,
        receipt_metadata=ReceiptMetadata(
            title="t", generated_at="2026-01-01T00:00:00Z", summary="s"
        ),
    )


def varied_packet() -> SourceCapturePacket:
    """The canonical all-branches packet the ECR source-side derivers compose over.

    Four slices, deliberately spanning every branch the slice-grain derivers
    take, with a fully specific (SP-1 resolved) packet identity:

    - ``s_clean``: verifiable file + KNOWN locator + pre_cutoff
      (SP-2 verifiable / clears; SP-3 pre_cutoff / clears).
    - ``s_placeholder``: all-zero-sha file + post_cutoff
      (SP-2 reference_only; SP-3 post_cutoff / does not clear).
    - ``s_residual``: no files + KNOWN locator + cutoff residual (status != KNOWN)
      (SP-2 reference_only; SP-3 residual / does not clear).
    - ``s_dark``: no files + locator not KNOWN + mixed cutoff
      (SP-2 not_inspectable; SP-3 mixed / does not clear).
    """
    return build_packet(
        [
            {
                "id": "s_clean",
                "files": [("f_clean", _VERIFIABLE_SHA)],
                "locator_known": True,
                "cutoff": "pre_cutoff",
            },
            {
                "id": "s_placeholder",
                "files": [("f_ph", _PLACEHOLDER_SHA)],
                "cutoff": "post_cutoff",
            },
            {"id": "s_residual", "files": [], "locator_known": True, "cutoff": None},
            {"id": "s_dark", "files": [], "locator_known": False, "cutoff": "mixed"},
        ]
    )
