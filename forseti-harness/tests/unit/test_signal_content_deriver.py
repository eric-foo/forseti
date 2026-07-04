"""Tests for the v0 Signal Content Record deriver (carry-supplied-or-residualize).

Validation focus: residualize-honestly (the headline -- a fully-residual record is
constructible and emitted with authored_interpretation=None); per-slice grain with
the no-body emit gate; never-invent (no family from prose); the D2=(b1) event-time
residual default; key-integrity + deterministic content_id over keys only;
re-derive determinism + purity; multi-body concatenation; the dormant authored
seam. Every negative asserts a real raise.
"""
from __future__ import annotations

import pytest

from source_capture.models import VisibleFactStatus
from signal_content.deriver import _BODY_BOUNDARY, _content_id, derive_signal_content
from signal_content.models import (
    DecisionRelevance,
    SignalContentRecord,
    SignalEventTimeStatus,
    SignalFamily,
)
from _ecr_builders import build_packet


def _packet(slice_specs=None, **kwargs):
    if slice_specs is None:
        slice_specs = [{"id": "s1", "files": [("f1", "a" * 64)]}]
    return build_packet(slice_specs, **kwargs)


# --- the headline: residualize honestly ---


def test_residualize_honestly_with_no_authored_input() -> None:
    packet = _packet()
    records = derive_signal_content(
        packet, preserved_bodies={"f1": "Pro plan now $25/mo (was $20)."}
    )
    assert len(records) == 1
    rec = records[0]
    assert rec.signal_family is SignalFamily.RESIDUAL_FAMILY_UNRESOLVED
    assert rec.decision_relevance is DecisionRelevance.UNRESOLVED
    assert rec.subject_entity.status is VisibleFactStatus.UNKNOWN_WITH_REASON
    assert rec.subject_entity.reason
    assert rec.event_or_claim.status is VisibleFactStatus.UNKNOWN_WITH_REASON
    assert rec.event_or_claim.reason
    assert rec.raw_observation == "Pro plan now $25/mo (was $20)."
    assert rec.references.packet_id == packet.packet_id
    assert rec.references.slice_id == "s1"
    assert rec.references.ecr_posture_ref_ids == []


def test_event_time_residual_is_the_v0_default() -> None:
    # D2=(b1): the deriver never selects publication-vs-edit; it residualizes.
    rec = derive_signal_content(_packet(), preserved_bodies={"f1": "x"})[0]
    et = rec.signal_event_time
    assert et.status is SignalEventTimeStatus.UNKNOWN_WITH_REASON
    assert et.packet_timing_field is None
    assert et.reason


def test_derived_record_round_trips_under_extra_forbid() -> None:
    rec = derive_signal_content(_packet(), preserved_bodies={"f1": "body"})[0]
    assert SignalContentRecord.model_validate(rec.model_dump()) == rec


# --- per-slice grain + the emit gate ---


def test_one_record_per_body_bearing_slice_in_order() -> None:
    packet = _packet(
        [
            {"id": "s1", "files": [("f1", "a" * 64)]},
            {"id": "s2", "files": [("f2", "a" * 64)]},
        ]
    )
    records = derive_signal_content(packet, preserved_bodies={"f1": "one", "f2": "two"})
    assert [r.references.slice_id for r in records] == ["s1", "s2"]
    assert [r.raw_observation for r in records] == ["one", "two"]


def test_slice_with_no_files_emits_no_record() -> None:
    packet = _packet(
        [
            {"id": "s_body", "files": [("f1", "a" * 64)]},
            {"id": "s_nofile", "files": [], "locator_known": True},
        ]
    )
    records = derive_signal_content(packet, preserved_bodies={"f1": "body"})
    assert [r.references.slice_id for r in records] == ["s_body"]


def test_referenced_but_unsupplied_body_emits_no_record() -> None:
    packet = _packet(
        [
            {"id": "s_supplied", "files": [("f1", "a" * 64)]},
            {"id": "s_missing", "files": [("f2", "a" * 64)]},
        ]
    )
    records = derive_signal_content(packet, preserved_bodies={"f1": "body"})
    assert [r.references.slice_id for r in records] == ["s_supplied"]


def test_empty_supplied_body_emits_no_record() -> None:
    records = derive_signal_content(_packet(), preserved_bodies={"f1": "   "})
    assert records == []


# --- never invent ---


def test_never_invents_family_from_prose() -> None:
    # a body that "reads like" a price move must NOT populate signal_family
    rec = derive_signal_content(
        _packet(),
        preserved_bodies={"f1": "Competitor raised Pro from $20 to $25 -- price move!"},
    )[0]
    assert rec.signal_family is SignalFamily.RESIDUAL_FAMILY_UNRESOLVED


# --- key integrity + content_id ---


def test_content_id_is_deterministic_over_keys_only() -> None:
    packet = _packet([{"id": "s1", "files": [("f1", "a" * 64)]}], packet_id="pkt-9")
    rec_a = derive_signal_content(packet, preserved_bodies={"f1": "body A"})[0]
    rec_b = derive_signal_content(packet, preserved_bodies={"f1": "DIFFERENT body B"})[0]
    # same keys -> same content_id regardless of body (re-derive stability)
    assert rec_a.content_id == rec_b.content_id
    assert rec_a.content_id.startswith("scr::sha256::")


def test_content_id_is_tuple_safe_for_separator_bearing_keys() -> None:
    # distinct key tuples must not collide even when an id contains "::"
    assert _content_id("a::b", "c") != _content_id("a", "b::c")


def test_ecr_posture_refs_default_empty_and_deduped() -> None:
    rec_default = derive_signal_content(_packet(), preserved_bodies={"f1": "b"})[0]
    assert rec_default.references.ecr_posture_ref_ids == []
    rec_refs = derive_signal_content(
        _packet(), preserved_bodies={"f1": "b"}, ecr_posture_refs=["r1", "r1", "r2"]
    )[0]
    assert rec_refs.references.ecr_posture_ref_ids == ["r1", "r2"]


# --- re-derive determinism + purity ---


def test_re_derive_determinism_and_purity() -> None:
    packet = _packet()
    bodies = {"f1": "stable body"}
    before = packet.model_dump()
    first = derive_signal_content(packet, preserved_bodies=bodies)
    second = derive_signal_content(packet, preserved_bodies=bodies)
    assert first == second
    assert isinstance(first, list)
    assert packet.model_dump() == before  # no packet mutation


# --- multi-body slice ---


def test_multi_body_slice_concatenates_in_order_with_boundary() -> None:
    packet = _packet([{"id": "s1", "files": [("f_a", "a" * 64), ("f_b", "a" * 64)]}])
    records = derive_signal_content(
        packet, preserved_bodies={"f_a": "PART A", "f_b": "PART B"}
    )
    assert len(records) == 1
    assert records[0].raw_observation == "PART A" + _BODY_BOUNDARY + "PART B"


def test_multi_body_slice_with_one_missing_body_emits_no_record() -> None:
    # all-or-nothing: a partial multi-body slice is NOT emitted as whole-slice evidence
    packet = _packet([{"id": "s1", "files": [("f_a", "a" * 64), ("f_b", "a" * 64)]}])
    assert derive_signal_content(packet, preserved_bodies={"f_a": "PART A"}) == []


# --- honesty states ---


def test_residual_reasons_carry_state1_not_state2_marker() -> None:
    rec = derive_signal_content(_packet(), preserved_bodies={"f1": "b"})[0]
    for reason in (
        rec.subject_entity.reason,
        rec.event_or_claim.reason,
        rec.signal_event_time.reason,
    ):
        assert "NOT-EXTRACTED" in reason
        assert "EXTRACTED-BUT-ABSENT" not in reason


# --- the dormant authored seam ---


def test_authored_interpretation_seam_raises_not_implemented() -> None:
    with pytest.raises(NotImplementedError):
        derive_signal_content(
            _packet(),
            preserved_bodies={"f1": "b"},
            authored_interpretation={"family": "x"},
        )
