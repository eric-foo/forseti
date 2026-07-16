"""Regression matrix for the shared cleaning ref helpers (cleaning/_shared.py).

Pins that raw_refs orders deterministically when ref keys mix None and str --
a packet carrying a derived_record anchor (None preserved-file fields) next to
a preserved-file anchor used to raise TypeError on None < str in both the old
per-module copies and the consolidated shared home. Policy: None sorts first.
"""
from __future__ import annotations

import hashlib

from cleaning._shared import raw_refs
from cleaning.models import (
    CleaningDerivedRecordRef,
    CleaningInputHandle,
    CleaningPacket,
    CleaningRawAnchor,
)

_SHA = hashlib.sha256(b"shared ref regression bytes").hexdigest()


def _derived_handle(handle_id: str) -> CleaningInputHandle:
    return CleaningInputHandle(
        handle_id=handle_id,
        source_family="youtube",
        source_surface="youtube_audio",
        raw_anchor=CleaningRawAnchor(
            packet_id="01ASRAUDIOPACKET00000000AB",
            sha256=_SHA,
            hash_basis="derived_record_bytes",
            anchor_kind="derived_record",
            derived_record_ref=CleaningDerivedRecordRef(
                lane="transcript_asr", record_id="asr_small__deadbeefdeadbeef"
            ),
        ),
    )


def _file_handle(handle_id: str) -> CleaningInputHandle:
    return CleaningInputHandle(
        handle_id=handle_id,
        source_family="youtube",
        source_surface="youtube_captions",
        raw_anchor=CleaningRawAnchor(
            packet_id="01CAPTIONPACKET000000000AB",
            slice_id="slice_01",
            file_id="file_01",
            relative_packet_path="raw/01_captions.json3",
            sha256=_SHA,
            hash_basis="raw_stored_bytes",
        ),
    )


def test_raw_refs_orders_mixed_none_and_str_keys_none_first() -> None:
    # file handle first on purpose: the sorted output must not depend on
    # handle order, and the None-keyed (derived_record) ref must sort first.
    packet = CleaningPacket(handles=[_file_handle("h_file"), _derived_handle("h_derived")])
    refs = raw_refs(packet)
    assert [ref["packet_id"] for ref in refs] == [
        "01ASRAUDIOPACKET00000000AB",
        "01CAPTIONPACKET000000000AB",
    ]
    assert refs[0]["file_id"] is None
    assert refs[1]["file_id"] == "file_01"


def test_raw_refs_still_dedupes_identical_mixed_anchor_refs() -> None:
    packet = CleaningPacket(
        handles=[
            _derived_handle("h_derived_1"),
            _file_handle("h_file"),
            _derived_handle("h_derived_2"),
        ]
    )
    refs = raw_refs(packet)
    assert len(refs) == 2
