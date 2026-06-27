"""Model + adapter matrix for the derived_record cleaning anchor (AO-2).

Pins the two anchor shapes are never mixed (derived_record carries derived_record_ref and NONE of
the preserved-file fields / anchor_value / json_pointer; every preserved-file kind carries the
three preserved-file fields and NO derived_record_ref), that a derived_record never traverses the
projection adapter, and that the dedupe identity tuple is well-formed for derived records.

Spec: cleaning_derived_record_anchor_contract_v0.md (Contract A + E + core dedup).
"""
from __future__ import annotations

import hashlib

import pytest
from pydantic import ValidationError

from cleaning.core import (
    _group_id_for_identity,
    _raw_anchor_identity,
    derive_exact_identity_duplicate_groups,
)
from cleaning.models import (
    CleaningDerivedRecordRef,
    CleaningEcrRef,
    CleaningInputHandle,
    CleaningRawAnchor,
)
from cleaning.projection import cleaning_input_handle_from_projection_row


_SHA = hashlib.sha256(b"derived record bytes").hexdigest()


def _derived_anchor(**over):
    base = dict(
        packet_id="01ASRAUDIOPACKET00000000AB",
        sha256=_SHA,
        hash_basis="derived_record_bytes",
        anchor_kind="derived_record",
        derived_record_ref=CleaningDerivedRecordRef(
            lane="transcript_asr", record_id="asr_small__deadbeefdeadbeef"
        ),
    )
    base.update(over)
    return base


def test_derived_record_anchor_round_trips() -> None:
    anchor = CleaningRawAnchor(**_derived_anchor())
    assert anchor.anchor_kind == "derived_record"
    assert anchor.slice_id is None
    assert anchor.file_id is None
    assert anchor.relative_packet_path is None
    assert anchor.anchor_value is None
    assert anchor.json_pointer is None
    assert anchor.derived_record_ref is not None
    assert anchor.derived_record_ref.subtree == "derived"
    assert anchor.derived_record_ref.lane == "transcript_asr"
    # Survives a JSON dump/reload (the smoke runner persists the anchor through JSON).
    reloaded = CleaningRawAnchor.model_validate(anchor.model_dump(mode="json"))
    assert reloaded == anchor


def test_derived_record_anchor_with_anchor_value_none_round_trips() -> None:
    # anchor_value=None is the only valid form (a derived_record takes the whole record).
    anchor = CleaningRawAnchor(**_derived_anchor(anchor_value=None))
    assert anchor.anchor_value is None


@pytest.mark.parametrize(
    "over",
    [
        {"slice_id": "slice_01"},
        {"file_id": "file_01"},
        {"relative_packet_path": "raw/01.json"},
        {"anchor_value": "something"},
        {"json_pointer": "/cues/0"},
    ],
)
def test_derived_record_anchor_rejects_preserved_or_specific_fields(over) -> None:
    with pytest.raises(ValidationError):
        CleaningRawAnchor(**_derived_anchor(**over))


def test_derived_record_anchor_requires_derived_record_ref() -> None:
    with pytest.raises(ValidationError):
        CleaningRawAnchor(**_derived_anchor(derived_record_ref=None))


def test_preserved_file_anchor_rejects_derived_record_ref() -> None:
    # The inverse direction (F7): a preserved-file ("file") anchor must NOT carry a
    # derived_record_ref.
    with pytest.raises(ValidationError):
        CleaningRawAnchor(
            packet_id="01CAPTIONPACKET000000000AB",
            slice_id="slice_01",
            file_id="file_01",
            relative_packet_path="raw/01_captions.json3",
            sha256=_SHA,
            hash_basis="raw_stored_bytes",
            anchor_kind="file",
            derived_record_ref=CleaningDerivedRecordRef(
                lane="transcript_asr", record_id="asr_small__deadbeefdeadbeef"
            ),
        )


def test_derived_record_ref_rejects_blank_segments() -> None:
    with pytest.raises(ValidationError):
        CleaningDerivedRecordRef(lane="", record_id="asr_x")
    with pytest.raises(ValidationError):
        CleaningDerivedRecordRef(lane="transcript_asr", record_id="   ")


def test_projection_never_emits_derived_record_anchor() -> None:
    """A derived_record anchor must never originate from a projection row (Contract E). A row that
    names anchor_kind='derived_record' is rejected by the projection adapter (kind not allowed),
    so projection rows stay preserved-file-backed."""

    class _FakeAnchor:
        anchor_kind = "derived_record"
        file_id = "file_01"
        relative_packet_path = "raw/01.json"
        sha256 = _SHA
        hash_basis = "raw_stored_bytes"
        anchor_value = None
        json_pointer = None

    class _FakeRef:
        packet_id = "01PROJECTIONPACKET0000000A"
        slice_id = "slice_01"

    class _FakeRow:
        row_id = "row_1"
        row_kind = "retail_pdp_product"
        raw_ref = _FakeRef()
        raw_anchor = _FakeAnchor()

    class _FakeProjection:
        packet_id = "01PROJECTIONPACKET0000000A"
        projection_method = "fixture"
        projection_version = "v0"
        certification = "view_only; not_cleaned; not_judgment_ready"

    with pytest.raises(ValueError, match="unsupported projection raw anchor kind"):
        cleaning_input_handle_from_projection_row(
            handle_id="fixture:row_1",
            source_family="retail_pdp",
            source_surface="cloakbrowser_snapshot",
            projection_packet=_FakeProjection(),
            projection_row=_FakeRow(),
        )


def test_derived_record_dedupe_identity_is_str_only_and_groups() -> None:
    # The identity tuple must be str-only (None preserved-file fields coerced) so
    # _group_id_for_identity's join never crashes; distinct derived records must not collide.
    anchor = CleaningRawAnchor(**_derived_anchor())
    identity = _raw_anchor_identity(anchor)
    assert all(isinstance(part, str) for part in identity)
    # group-id minting does not crash on the (formerly None) preserved-file slots.
    assert _group_id_for_identity(identity).startswith("exact_raw_anchor:")


def test_two_identical_derived_record_handles_form_one_dedupe_group() -> None:
    def _handle(handle_id: str) -> CleaningInputHandle:
        return CleaningInputHandle(
            handle_id=handle_id,
            source_family="youtube",
            source_surface="youtube_audio",
            raw_anchor=CleaningRawAnchor(**_derived_anchor()),
            ecr_ref=CleaningEcrRef(
                packet_id="01ASRAUDIOPACKET00000000AB",
                ref_id="ecr:01ASRAUDIOPACKET00000000AB:source_side_postures",
            ),
        )

    groups = derive_exact_identity_duplicate_groups([_handle("h1"), _handle("h2")])
    assert len(groups) == 1
    assert groups[0].instance_count == 2
    assert sorted(groups[0].member_handle_ids) == ["h1", "h2"]


def test_distinct_derived_records_do_not_collide() -> None:
    a = CleaningRawAnchor(**_derived_anchor())
    b = CleaningRawAnchor(
        **_derived_anchor(
            derived_record_ref=CleaningDerivedRecordRef(
                lane="transcript_asr", record_id="asr_small__cafef00dcafef00d"
            )
        )
    )
    assert _raw_anchor_identity(a) != _raw_anchor_identity(b)
