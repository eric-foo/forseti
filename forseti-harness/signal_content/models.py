"""Signal Content Record -- v0 source-side content model (the "what a signal says" layer).

The second derived-record kind after the ECR integrity postures
(``docs/product/core_spine_v0_signal_content_record_architecture_v0.md``): a
wedge-agnostic, structured record of a signal's CONTENT, keyed to a
``SourceCapturePacket`` and composed by the Evidence Unit by reference -- never
merged into provenance/integrity, never carrying a Judgment verdict.

v0 scope: the data model + validators only. No deriver (raw -> filled record),
no rich family payloads, no persistence/finalizer, no EvidenceUnit binding, no
Cleaning/Judgment. The final Evidence Unit field architecture remains
owner-reserved and JSG-01 stays frozen; this is the bounded content-field
ratification analogue of the SP-1/2/3/6 source-side ratification.
"""
from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import Field, model_validator

from schemas.case_models import StrictModel
from source_capture.models import VisibleFact


SIGNAL_CONTENT_MANIFEST_VERSION = "signal_content_record_v0"


def _require_non_empty(value: str, *, field_name: str) -> str:
    if not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value


def _require_optional_non_empty(value: str | None, *, field_name: str) -> str | None:
    if value is not None and not value.strip():
        raise ValueError(f"{field_name}, when present, must be a non-empty string")
    return value


class SignalFamily(StrEnum):
    """Closed, wedge-agnostic content-row families plus a mandatory residual.

    signal-quality meta is intentionally NOT a member: per the architecture
    direction it is carried by the ECR integrity postures, the ``VisibleFact``
    honesty fields, the ``decision_relevance`` tag, and Judgment -- it is not a
    content-row family. Adding a family later is an additive enum change; an
    unresolved family degrades to ``RESIDUAL_FAMILY_UNRESOLVED`` rather than
    being forced or rejected.
    """

    COMPETITOR_PRICE_PACKAGING_MOVE = "competitor_price_packaging_move"
    COMPETITIVE_NARRATIVE_POSITIONING = "competitive_narrative_positioning"
    DEMAND_REACTION = "demand_reaction"
    TRIGGER_TIMING_EVENT = "trigger_timing_event"
    RESIDUAL_FAMILY_UNRESOLVED = "RESIDUAL_FAMILY_UNRESOLVED"


class DecisionRelevance(StrEnum):
    """Neutral, mechanical, shape-derived routing tag (decide-vs-confirm).

    NOT a graded Signal Use verdict: the graded Signal Use Classification,
    Decision Strength, and Action Ceiling stay Judgment-owned and off this
    record.
    """

    DECIDE_CANDIDATE = "decide_candidate"
    CONFIRM_ONLY = "confirm_only"
    CONTEXT_ONLY = "context_only"
    UNRESOLVED = "unresolved"


class Delta(StrictModel):
    """Generic, family-agnostic before -> after. Optional; absent for point-in-time signals."""

    dimension: str
    before: VisibleFact
    after: VisibleFact
    change_basis: str | None = None

    @model_validator(mode="after")
    def validate_delta_anchors(self) -> "Delta":
        _require_non_empty(self.dimension, field_name="delta.dimension")
        _require_optional_non_empty(self.change_basis, field_name="delta.change_basis")
        return self


class Reaction(StrictModel):
    """Generic observed response, co-observed in the SAME capture only.

    Thin and local: any aggregate reaction (sentiment across N sources, a
    sensitivity curve) is Judgment-owned and is never a field here.
    """

    kind: str
    direction: str | None = None
    observed_magnitude_state: VisibleFact
    excerpt_ref: str | None = None

    @model_validator(mode="after")
    def validate_reaction_anchors(self) -> "Reaction":
        _require_non_empty(self.kind, field_name="reaction.kind")
        _require_optional_non_empty(self.direction, field_name="reaction.direction")
        _require_optional_non_empty(self.excerpt_ref, field_name="reaction.excerpt_ref")
        return self


class SignalEventTimeField(StrEnum):
    """Allowed ``PacketTiming`` fields for a signal's event time.

    Event time must point at source-side event/version timing
    (``PacketTiming.source_publication_or_event`` /
    ``PacketTiming.source_edit_or_version``), NOT ``capture_time``,
    ``recapture_time``, or ``cutoff_posture``. This keeps event time
    by-reference and distinct from capture/cutoff timing, which provenance and
    ECR already own.
    """

    SOURCE_PUBLICATION_OR_EVENT = "source_publication_or_event"
    SOURCE_EDIT_OR_VERSION = "source_edit_or_version"


class SignalEventTimeStatus(StrEnum):
    """Closed two-state status for a signal's event-time anchor.

    Deliberately tighter than ``VisibleFactStatus``: the anchor is either KNOWN
    (a source-side ``PacketTiming`` field is the event time) or
    ``UNKNOWN_WITH_REASON`` (no anchor resolved -- the v0 residual default).
    Further states (e.g. not-applicable for a timeless signal) are an additive
    enum growth if a future authored lane needs them; v0 admits only the two it
    uses.
    """

    KNOWN = "known"
    UNKNOWN_WITH_REASON = "unknown_with_reason"


class SignalEventTimeReference(StrictModel):
    """By-reference pointer to the ``PacketTiming`` field that carries the event time.

    Carries no copied timestamp: the actual value lives on the referenced
    packet's ``PacketTiming``; this names WHICH source-timing field is the event
    time (never capture/cutoff).

    Honesty under absence (D2 = b1): naming which source-timing field is *the
    signal's event time* is an interpretive act the deriver must not perform from
    packet prose. So the reference is ``VisibleFact``-shaped -- a KNOWN status
    names a field; any non-KNOWN status carries a ``reason`` and names no field
    (the residual the deriver defaults to when no authored anchor is supplied).
    ``status`` defaults KNOWN, so existing constructions and records are
    unchanged (additive, non-breaking).
    """

    status: SignalEventTimeStatus = SignalEventTimeStatus.KNOWN
    packet_timing_field: SignalEventTimeField | None = None
    reason: str | None = None

    @model_validator(mode="after")
    def validate_event_time(self) -> "SignalEventTimeReference":
        if self.status == SignalEventTimeStatus.KNOWN:
            if self.packet_timing_field is None:
                raise ValueError(
                    "a KNOWN event-time reference must name a packet_timing_field"
                )
            if self.reason is not None:
                raise ValueError(
                    "a KNOWN event-time reference must not carry a reason; reasons "
                    "are carried only by non-known (residual) references"
                )
            return self
        if self.packet_timing_field is not None:
            raise ValueError(
                "a non-KNOWN event-time reference must not name a packet_timing_field "
                "(the anchor is unresolved)"
            )
        if self.reason is None or not self.reason.strip():
            raise ValueError(
                "a non-KNOWN event-time reference requires a non-empty reason"
            )
        return self


class FamilyDetailBase(StrictModel):
    """Empty v0 extension slot for family-specific content.

    No fields in v0. Families add typed subclasses later under the
    two-non-overlapping-families promotion rule. The slot is the scalability
    hinge; payloads are additive and never touch the common spine.
    """


class ContentReferences(StrictModel):
    """By-KEY references to provenance + integrity -- never embedded, never merged.

    Content links to "can I trust the saying" (the ``SourceCapturePacket`` and
    the ECR postures) by key; it never copies those records in. One-directional:
    content -> provenance, never the reverse.
    """

    packet_id: str
    slice_id: str | None = None
    ecr_posture_ref_ids: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_keys(self) -> "ContentReferences":
        if not self.packet_id.strip():
            raise ValueError("packet_id reference must be a non-empty key")
        if self.slice_id is not None and not self.slice_id.strip():
            raise ValueError("slice_id reference, when present, must be a non-empty key")
        for ref in self.ecr_posture_ref_ids:
            if not ref.strip():
                raise ValueError("ecr_posture_ref_ids must not contain an empty key")
        if len(set(self.ecr_posture_ref_ids)) != len(self.ecr_posture_ref_ids):
            raise ValueError("ecr_posture_ref_ids must not contain duplicate keys")
        return self


class SignalContentRecord(StrictModel):
    """v0 wedge-agnostic structured record of WHAT a signal says.

    One record == one observed event/claim from one source slice. Any
    cross-source aggregate is Judgment-owned and is never a field here. The
    record references provenance/integrity by key and stops strictly below
    interpretation.
    """

    manifest_version: Literal["signal_content_record_v0"] = SIGNAL_CONTENT_MANIFEST_VERSION
    content_id: str
    signal_family: SignalFamily
    decision_relevance: DecisionRelevance

    # The SUBJECT of the signal (who/what it is about) -- not the source identity
    # (that is SP-1 / ECR). Honesty carried by VisibleFact (known / unknown-with-reason).
    subject_entity: VisibleFact
    event_or_claim: VisibleFact
    # By-reference to the source-side event/version timing on the referenced packet
    # (never a copied value, never capture/cutoff).
    signal_event_time: SignalEventTimeReference
    raw_observation: str

    # By-key links to provenance + integrity (never embedded).
    references: ContentReferences

    # Optional generic shapes -- family richness lives in their VALUES, not new columns.
    delta: Delta | None = None
    reaction: Reaction | None = None

    # Empty v0 extension slot for family-specific detail.
    family_detail: FamilyDetailBase | None = None

    @model_validator(mode="after")
    def validate_anchors(self) -> "SignalContentRecord":
        _require_non_empty(self.content_id, field_name="content_id")
        if not self.raw_observation.strip():
            raise ValueError("raw_observation must be a non-empty source-language anchor")
        return self
