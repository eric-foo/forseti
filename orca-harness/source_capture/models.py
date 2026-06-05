from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import Field, field_validator, model_validator

from schemas.case_models import StrictModel


OBLIGATION_CONTRACT_VERSION = "core_spine_v0_data_capture_spine_obligation_contract_v0"
SOURCE_CAPTURE_MANIFEST_VERSION = "source_capture_packet_manifest_v1"


class CaptureModeCategory(StrEnum):
    HUMAN_LED = "human-led"
    AGENT_ASSISTED = "agent-assisted"
    STRUCTURED_ACCESS = "structured access"
    ARCHIVE_HISTORY = "archive/history"
    AUTOMATED_EXTRACTION = "automated extraction"
    MULTIMODAL = "multimodal"
    MIXED = "mixed"


class VisibleFactStatus(StrEnum):
    KNOWN = "known"
    UNKNOWN_WITH_REASON = "unknown_with_reason"
    NOT_ATTEMPTED = "not_attempted"
    NOT_APPLICABLE = "not_applicable"


class VisibleFact(StrictModel):
    status: VisibleFactStatus
    value: str | None = None
    reason: str | None = None

    @model_validator(mode="after")
    def validate_fact(self) -> "VisibleFact":
        if self.status == VisibleFactStatus.KNOWN:
            if not self.value:
                raise ValueError("known facts require a value")
            return self
        if not self.reason:
            raise ValueError("non-known facts require a reason")
        return self


# Ob.9 / Ob.10 / Ob.15 closed posture vocabularies, enforced at write-time. A
# posture is closed only on its known VALUE; not_attempted / not_applicable /
# unknown_with_reason are carried by VisibleFactStatus + reason (AR-05). Closing
# these once, at the source, stops every downstream reader from re-interpreting
# free text. access_posture (Ob.11) is intentionally left open.
CUTOFF_POSTURE_VALUES = frozenset({"pre_cutoff", "post_cutoff", "mixed", "unknown"})
ARCHIVE_HISTORY_POSTURE_VALUES = frozenset({"archived", "attempt_failed"})
RE_CAPTURE_RELATIONSHIP_VALUES = frozenset({"supersede", "supplement", "conflict", "mixed"})

# AR-04: every PreservedFile declares the recomputation basis of its sha256 as a
# closed, source-visible token -- never arbitrary prose (an unconstrained string just
# recreates the "hash-shaped string" problem under a new field name). The token names
# what the hash COVERS; the bytes are named by relative_packet_path and the algorithm
# by the sha256 field, so the basis need not repeat them. raw_stored_bytes = the sha256
# is computed over the complete, unmodified stored bytes of the file at
# relative_packet_path (recompute: sha256(read_bytes(packet_dir / relative_packet_path))).
# Add a value only when a writer path actually produces that basis (e.g. an owner-bound
# acquisition receipt); invent none ahead of a real producer.
HASH_BASIS_VALUES = frozenset({"raw_stored_bytes"})


def _require_closed_posture(
    fact: VisibleFact, *, allowed: frozenset[str], field: str, obligation: str
) -> None:
    if fact.status == VisibleFactStatus.KNOWN and fact.value not in allowed:
        allowed_list = ", ".join(sorted(allowed))
        raise ValueError(
            f"{field} known value must be one of {{{allowed_list}}} ({obligation} closed "
            f"vocabulary); got {fact.value!r}. Record capture context elsewhere (e.g. "
            f"capture_context) and use unknown_with_reason / not_attempted / not_applicable "
            f"for non-closed cases."
        )


class PacketTiming(StrictModel):
    source_publication_or_event: VisibleFact
    source_edit_or_version: VisibleFact
    capture_time: VisibleFact
    recapture_time: VisibleFact
    cutoff_posture: VisibleFact

    @model_validator(mode="after")
    def validate_closed_postures(self) -> "PacketTiming":
        _require_closed_posture(
            self.cutoff_posture, allowed=CUTOFF_POSTURE_VALUES, field="cutoff_posture", obligation="Ob.9"
        )
        return self


class PreservedFile(StrictModel):
    file_id: str
    original_path: str
    relative_packet_path: str
    sha256: str
    hash_basis: str
    size_bytes: int = Field(ge=0)

    @field_validator("hash_basis")
    @classmethod
    def validate_hash_basis(cls, value: str) -> str:
        if value not in HASH_BASIS_VALUES:
            allowed_list = ", ".join(sorted(HASH_BASIS_VALUES))
            raise ValueError(
                f"hash_basis must be one of {{{allowed_list}}} (AR-04 recomputation-bound "
                f"basis); got {value!r}. Add a value only when a writer produces that basis."
            )
        return value


class SourceCaptureSlice(StrictModel):
    slice_id: str
    locator: VisibleFact
    timing: PacketTiming
    access_posture: VisibleFact
    archive_history_posture: VisibleFact
    media_modality_posture: VisibleFact
    re_capture_relationship: VisibleFact
    limitations: list[str] = Field(default_factory=list)
    warning_notes: list[str] = Field(default_factory=list)
    preserved_file_ids: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_closed_postures(self) -> "SourceCaptureSlice":
        _require_closed_posture(
            self.archive_history_posture,
            allowed=ARCHIVE_HISTORY_POSTURE_VALUES,
            field="archive_history_posture",
            obligation="Ob.10",
        )
        _require_closed_posture(
            self.re_capture_relationship,
            allowed=RE_CAPTURE_RELATIONSHIP_VALUES,
            field="re_capture_relationship",
            obligation="Ob.15",
        )
        return self


class ReceiptMetadata(StrictModel):
    title: str
    generated_at: str
    summary: str
    non_claims: list[str] = Field(default_factory=list)

    @field_validator("generated_at", mode="before")
    @classmethod
    def normalize_generated_at(cls, value: object) -> object:
        if isinstance(value, datetime):
            return value.isoformat().replace("+00:00", "Z")
        return value


class SourceCapturePacket(StrictModel):
    packet_id: str
    manifest_version: str
    obligation_contract_version: str
    source_family: str
    source_surface: str
    source_locator: VisibleFact
    requested_decision_context: VisibleFact
    capture_context: VisibleFact
    actor_audience_context: VisibleFact
    capture_mode: CaptureModeCategory
    operator_category: str
    session_identity: str
    visible_mode_changes: list[str] = Field(default_factory=list)
    timing: PacketTiming
    access_posture: VisibleFact
    archive_history_posture: VisibleFact
    media_modality_posture: VisibleFact
    re_capture_relationship: VisibleFact
    source_slices: list[SourceCaptureSlice] = Field(min_length=1)
    preserved_files: list[PreservedFile] = Field(min_length=1)
    warnings: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    receipt_metadata: ReceiptMetadata

    @model_validator(mode="after")
    def validate_closed_postures(self) -> "SourceCapturePacket":
        _require_closed_posture(
            self.archive_history_posture,
            allowed=ARCHIVE_HISTORY_POSTURE_VALUES,
            field="archive_history_posture",
            obligation="Ob.10",
        )
        _require_closed_posture(
            self.re_capture_relationship,
            allowed=RE_CAPTURE_RELATIONSHIP_VALUES,
            field="re_capture_relationship",
            obligation="Ob.15",
        )
        return self

    @model_validator(mode="after")
    def validate_preserved_file_references(self) -> "SourceCapturePacket":
        preserved_ids = {item.file_id for item in self.preserved_files}
        if len(preserved_ids) != len(self.preserved_files):
            raise ValueError("preserved file IDs must be unique")

        referenced_ids: set[str] = set()
        for source_slice in self.source_slices:
            unknown_ids = set(source_slice.preserved_file_ids) - preserved_ids
            if unknown_ids:
                unknown_list = ", ".join(sorted(unknown_ids))
                raise ValueError(f"source slice references unknown preserved file IDs: {unknown_list}")
            referenced_ids.update(source_slice.preserved_file_ids)

        unreferenced_ids = preserved_ids - referenced_ids
        if unreferenced_ids:
            unreferenced_list = ", ".join(sorted(unreferenced_ids))
            raise ValueError(f"preserved files are not referenced by any source slice: {unreferenced_list}")
        return self


class PacketWriteResult(StrictModel):
    output_directory: str
    manifest_path: str
    receipt_path: str
    packet: SourceCapturePacket


def known_fact(value: str) -> VisibleFact:
    return VisibleFact(status=VisibleFactStatus.KNOWN, value=value)


def unknown_with_reason(reason: str) -> VisibleFact:
    return VisibleFact(status=VisibleFactStatus.UNKNOWN_WITH_REASON, reason=reason)


def not_attempted(reason: str) -> VisibleFact:
    return VisibleFact(status=VisibleFactStatus.NOT_ATTEMPTED, reason=reason)


def not_applicable(reason: str) -> VisibleFact:
    return VisibleFact(status=VisibleFactStatus.NOT_APPLICABLE, reason=reason)
