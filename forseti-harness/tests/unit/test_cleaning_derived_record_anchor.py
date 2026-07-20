from __future__ import annotations

import hashlib

import pytest
from pydantic import ValidationError

from cleaning.core import (
    _group_id_for_identity,
    _source_anchor_identity,
    derive_exact_identity_duplicate_groups,
)
from cleaning.models import (
    CleaningDerivedRecordRef,
    CleaningEcrRef,
    CleaningInputHandle,
    CleaningSourceAnchor,
)

_SHA = hashlib.sha256(b"derived record bytes").hexdigest()


def _derived_anchor(**over):
    base = {
        "packet_id": "01ASRAUDIOPACKET00000000AB",
        "sha256": _SHA,
        "hash_basis": "derived_record_bytes",
        "anchor_kind": "derived_record",
        "derived_record_ref": CleaningDerivedRecordRef(
            lane="transcript_asr", record_id="asr_small__deadbeefdeadbeef"
        ),
    }
    base.update(over)
    return base


def test_derived_record_source_anchor_round_trips() -> None:
    anchor = CleaningSourceAnchor(**_derived_anchor())
    assert anchor.anchor_kind == "derived_record"
    assert anchor.slice_id is None
    assert anchor.file_id is None
    assert anchor.relative_packet_path is None
    assert anchor.anchor_value is None
    assert anchor.json_pointer is None
    assert CleaningSourceAnchor.model_validate(anchor.model_dump(mode="json")) == anchor


@pytest.mark.parametrize(
    "over",
    [
        {"slice_id": "slice_01"},
        {"file_id": "file_01"},
        {"relative_packet_path": "raw/01.json"},
        {"anchor_value": "something"},
        {"json_pointer": "/cues/0"},
        {"derived_record_ref": None},
    ],
)
def test_derived_record_source_anchor_rejects_mixed_shapes(over) -> None:
    with pytest.raises(ValidationError):
        CleaningSourceAnchor(**_derived_anchor(**over))


def test_file_source_anchor_rejects_derived_record_ref() -> None:
    with pytest.raises(ValidationError):
        CleaningSourceAnchor(
            packet_id="01CAPTIONPACKET000000000AB",
            slice_id="slice_01",
            file_id="file_01",
            relative_packet_path="raw/01_captions.json3",
            sha256=_SHA,
            hash_basis="raw_stored_bytes",
            derived_record_ref=CleaningDerivedRecordRef(
                lane="transcript_asr", record_id="asr_small__deadbeefdeadbeef"
            ),
        )


def test_derived_record_identity_is_stable_and_groups() -> None:
    anchor = CleaningSourceAnchor(**_derived_anchor())
    identity = _source_anchor_identity(anchor)
    assert all(isinstance(part, str) for part in identity)
    assert _group_id_for_identity(identity).startswith("exact_source_anchor:")

    def handle(handle_id: str) -> CleaningInputHandle:
        return CleaningInputHandle(
            handle_id=handle_id,
            source_family="youtube",
            source_surface="youtube_audio",
            source_anchor=anchor,
            ecr_ref=CleaningEcrRef(
                packet_id=anchor.packet_id,
                ref_id=f"ecr:{anchor.packet_id}:source_side_postures",
            ),
        )

    groups = derive_exact_identity_duplicate_groups([handle("h1"), handle("h2")])
    assert len(groups) == 1
    assert groups[0].member_handle_ids == ["h1", "h2"]


def test_distinct_derived_records_do_not_collide() -> None:
    first = CleaningSourceAnchor(**_derived_anchor())
    second = CleaningSourceAnchor(
        **_derived_anchor(
            derived_record_ref=CleaningDerivedRecordRef(
                lane="transcript_asr", record_id="asr_small__cafef00dcafef00d"
            )
        )
    )
    assert _source_anchor_identity(first) != _source_anchor_identity(second)
