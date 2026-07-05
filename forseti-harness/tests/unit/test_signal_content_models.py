"""Tests for the v0 Signal Content Record data model.

Validation focus (no deriver/persistence/binding here): round-trip under
extra=forbid; closed-enum rejection; key-integrity; residual-degrades-honestly;
reuse of VisibleFact honesty semantics; plus post-review hardening -- version
Literal pin, event-time by-reference (not capture/cutoff), non-empty generic
anchors, and duplicate posture-ref rejection. Every negative asserts a real raise.
"""
from __future__ import annotations

import pytest
from pydantic import ValidationError

from source_capture.models import VisibleFact, VisibleFactStatus
from signal_content.models import (
    SIGNAL_CONTENT_MANIFEST_VERSION,
    ContentReferences,
    DecisionRelevance,
    Delta,
    FamilyDetailBase,
    Reaction,
    SignalContentRecord,
    SignalEventTimeField,
    SignalEventTimeReference,
    SignalEventTimeStatus,
    SignalFamily,
)


def _known(value: str) -> VisibleFact:
    return VisibleFact(status=VisibleFactStatus.KNOWN, value=value)


def _event_time() -> SignalEventTimeReference:
    return SignalEventTimeReference(
        packet_timing_field=SignalEventTimeField.SOURCE_PUBLICATION_OR_EVENT
    )


def _record(**overrides) -> SignalContentRecord:
    fields = dict(
        content_id="sc-0001",
        signal_family=SignalFamily.COMPETITOR_PRICE_PACKAGING_MOVE,
        decision_relevance=DecisionRelevance.DECIDE_CANDIDATE,
        subject_entity=_known("Competitor X"),
        event_or_claim=_known("raised Pro tier from $20 to $25"),
        signal_event_time=_event_time(),
        raw_observation="Pro plan now $25/mo (was $20).",
        references=ContentReferences(packet_id="pkt-1", slice_id="slc-1"),
    )
    fields.update(overrides)
    return SignalContentRecord(**fields)


def test_round_trip_under_extra_forbid_with_default_version() -> None:
    rec = _record()
    assert rec.manifest_version == SIGNAL_CONTENT_MANIFEST_VERSION
    rebuilt = SignalContentRecord.model_validate(rec.model_dump())
    assert rebuilt == rec


def test_extra_forbid_rejects_unknown_field() -> None:
    with pytest.raises(ValidationError):
        _record(surprise_field="nope")


def test_closed_enum_rejects_non_member_family() -> None:
    with pytest.raises(ValidationError):
        _record(signal_family="some_unlisted_family")


def test_closed_enum_rejects_graded_relevance_verdict() -> None:
    with pytest.raises(ValidationError):
        _record(decision_relevance="strong_for")


def test_unknown_family_degrades_to_residual_not_an_error() -> None:
    rec = _record(signal_family=SignalFamily.RESIDUAL_FAMILY_UNRESOLVED)
    assert rec.signal_family is SignalFamily.RESIDUAL_FAMILY_UNRESOLVED


def test_signal_quality_meta_is_not_a_content_family() -> None:
    assert not hasattr(SignalFamily, "SIGNAL_QUALITY_META")
    assert "signal_quality_meta" not in {member.value for member in SignalFamily}


def test_manifest_version_literal_rejects_other_versions() -> None:
    # read-checked _vN: a v0 model strictly admits only v0 records
    with pytest.raises(ValidationError):
        _record(manifest_version="signal_content_record_v1")


def test_signal_event_time_requires_a_reference_not_a_visible_fact() -> None:
    # event time is by-reference, not a copied VisibleFact value
    with pytest.raises(ValidationError):
        _record(signal_event_time=_known("2026-05-01"))


def test_signal_event_time_field_excludes_capture_and_cutoff() -> None:
    members = {m.value for m in SignalEventTimeField}
    assert members == {"source_publication_or_event", "source_edit_or_version"}
    for excluded in ("capture_time", "recapture_time", "cutoff_posture"):
        assert excluded not in members
        with pytest.raises(ValidationError):
            SignalEventTimeReference(packet_timing_field=excluded)


def test_event_time_known_requires_field_and_rejects_reason() -> None:
    # D2=(b1) XOR: a KNOWN reference names a field and carries no reason.
    ref = SignalEventTimeReference(
        status=SignalEventTimeStatus.KNOWN,
        packet_timing_field=SignalEventTimeField.SOURCE_PUBLICATION_OR_EVENT,
    )
    assert ref.packet_timing_field is SignalEventTimeField.SOURCE_PUBLICATION_OR_EVENT
    with pytest.raises(ValidationError):  # KNOWN without a field
        SignalEventTimeReference(status=SignalEventTimeStatus.KNOWN)
    with pytest.raises(ValidationError):  # KNOWN must not carry a reason
        SignalEventTimeReference(
            status=SignalEventTimeStatus.KNOWN,
            packet_timing_field=SignalEventTimeField.SOURCE_PUBLICATION_OR_EVENT,
            reason="not allowed when known",
        )


def test_event_time_residual_requires_reason_and_rejects_field() -> None:
    # D2=(b1) XOR: a non-KNOWN reference carries a reason and names no field.
    ref = SignalEventTimeReference(
        status=SignalEventTimeStatus.UNKNOWN_WITH_REASON,
        reason="no authored event-time anchor supplied",
    )
    assert ref.packet_timing_field is None
    with pytest.raises(ValidationError):  # non-KNOWN without a reason
        SignalEventTimeReference(status=SignalEventTimeStatus.UNKNOWN_WITH_REASON)
    with pytest.raises(ValidationError):  # non-KNOWN must not name a field
        SignalEventTimeReference(
            status=SignalEventTimeStatus.UNKNOWN_WITH_REASON,
            packet_timing_field=SignalEventTimeField.SOURCE_EDIT_OR_VERSION,
            reason="conflicting state",
        )
    with pytest.raises(ValidationError):  # whitespace-only reason is not a reason
        SignalEventTimeReference(
            status=SignalEventTimeStatus.UNKNOWN_WITH_REASON, reason="   "
        )


def test_event_time_status_is_tightened_to_two_states() -> None:
    # narrowed from VisibleFactStatus: not_attempted / not_applicable are not valid here
    for excluded in ("not_attempted", "not_applicable"):
        with pytest.raises(ValidationError):
            SignalEventTimeReference(status=excluded, reason="x")


def test_event_time_status_defaults_known_keeps_bare_reference_valid() -> None:
    # additive/non-breaking: the prior bare construction stays valid (status -> KNOWN).
    ref = SignalEventTimeReference(
        packet_timing_field=SignalEventTimeField.SOURCE_EDIT_OR_VERSION
    )
    assert ref.status is SignalEventTimeStatus.KNOWN


def test_key_integrity_rejects_empty_packet_id() -> None:
    with pytest.raises(ValidationError):
        ContentReferences(packet_id="   ")


def test_key_integrity_rejects_empty_posture_ref() -> None:
    with pytest.raises(ValidationError):
        ContentReferences(packet_id="pkt-1", ecr_posture_ref_ids=["ok", ""])


def test_key_integrity_rejects_duplicate_posture_refs() -> None:
    with pytest.raises(ValidationError):
        ContentReferences(packet_id="pkt-1", ecr_posture_ref_ids=["a", "a"])


def test_visible_fact_honesty_known_requires_value() -> None:
    with pytest.raises(ValidationError):
        _record(subject_entity=VisibleFact(status=VisibleFactStatus.KNOWN))


def test_content_id_and_raw_observation_must_be_non_empty() -> None:
    with pytest.raises(ValidationError):
        _record(content_id="   ")
    with pytest.raises(ValidationError):
        _record(raw_observation="")


def test_delta_and_reaction_reject_empty_anchors() -> None:
    with pytest.raises(ValidationError):
        Delta(dimension="   ", before=_known("$20"), after=_known("$25"))
    with pytest.raises(ValidationError):
        Reaction(kind="", observed_magnitude_state=_known("spike"))


def test_optional_delta_and_reaction_round_trip() -> None:
    rec = _record(
        delta=Delta(dimension="price", before=_known("$20"), after=_known("$25")),
        reaction=Reaction(kind="complaint_volume", observed_magnitude_state=_known("spike")),
    )
    assert SignalContentRecord.model_validate(rec.model_dump()) == rec


def test_empty_family_detail_slot_accepts_none_and_empty_base() -> None:
    assert _record(family_detail=None).family_detail is None
    assert _record(family_detail=FamilyDetailBase()).family_detail == FamilyDetailBase()
