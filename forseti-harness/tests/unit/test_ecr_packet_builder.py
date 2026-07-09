"""Structural self-check for the shared ECR source-side packet builder.

Asserts only that the builder faithfully encodes its spec into a producer-valid
packet -- it calls no deriver. Proving how the derivers compose over the builder
is the downstream mixed-grain integration test, not this file.
"""
from _ecr_builders import build_packet, varied_packet
from source_capture.models import (
    SourceCapturePacket,
    VisibleFactStatus,
    not_attempted,
)

_SHA = "a" * 64


def test_build_packet_is_producer_valid_and_round_trips():
    packet = build_packet([{"id": "s0", "files": [("f0", _SHA)], "cutoff": "pre_cutoff"}])
    assert isinstance(packet, SourceCapturePacket)
    # construction passing means every producer invariant held; confirm round-trip
    assert SourceCapturePacket.model_validate(packet.model_dump()) == packet


def test_cutoff_token_is_carried_as_known_fact():
    [s] = build_packet(
        [{"id": "s0", "files": [("f0", _SHA)], "cutoff": "post_cutoff"}]
    ).source_slices
    assert s.timing.cutoff_posture.status is VisibleFactStatus.KNOWN
    assert s.timing.cutoff_posture.value == "post_cutoff"


def test_cutoff_none_is_a_non_known_residual():
    [s] = build_packet(
        [{"id": "s0", "files": [("f0", _SHA)], "cutoff": None}]
    ).source_slices
    assert s.timing.cutoff_posture.status is not VisibleFactStatus.KNOWN
    assert s.timing.cutoff_posture.reason  # the residual carries a reason


def test_locator_known_flag_controls_slice_locator_status():
    packet = build_packet(
        [
            {"id": "known", "files": [("f0", _SHA)], "locator_known": True},
            {"id": "dark", "files": [], "locator_known": False},
        ]
    )
    by_id = {s.slice_id: s for s in packet.source_slices}
    assert by_id["known"].locator.status is VisibleFactStatus.KNOWN
    assert by_id["dark"].locator.status is not VisibleFactStatus.KNOWN


def test_identity_fields_are_parameterizable():
    resolved = build_packet([{"id": "s0", "files": [("f0", _SHA)]}])
    assert resolved.source_family == "reddit"
    assert resolved.source_locator.status is VisibleFactStatus.KNOWN

    # SP-1 unresolved input (empty family) is constructible by override
    unresolved = build_packet([{"id": "s0", "files": [("f0", _SHA)]}], source_family="")
    assert unresolved.source_family == ""

    # SP-1 family_only input (specific family, missing surface / non-KNOWN locator)
    family_only = build_packet(
        [{"id": "s0", "files": [("f0", _SHA)]}],
        source_surface="",
        source_locator=not_attempted("no id"),
    )
    assert family_only.source_surface == ""
    assert family_only.source_locator.status is not VisibleFactStatus.KNOWN


def test_varied_packet_spans_all_branches():
    packet = varied_packet()
    assert [s.slice_id for s in packet.source_slices] == [
        "s_clean",
        "s_placeholder",
        "s_residual",
        "s_dark",
    ]
    by_id = {s.slice_id: s for s in packet.source_slices}
    files = {pf.file_id: pf for pf in packet.preserved_files}

    # s_clean: verifiable file, KNOWN locator, pre_cutoff
    assert by_id["s_clean"].preserved_file_ids == ["f_clean"]
    assert files["f_clean"].sha256 == "a" * 64
    assert by_id["s_clean"].locator.status is VisibleFactStatus.KNOWN
    assert by_id["s_clean"].timing.cutoff_posture.value == "pre_cutoff"

    # s_placeholder: all-zero sha, post_cutoff
    assert files["f_ph"].sha256 == "0" * 64
    assert by_id["s_placeholder"].timing.cutoff_posture.value == "post_cutoff"

    # s_residual: no files, KNOWN locator, cutoff residual
    assert by_id["s_residual"].preserved_file_ids == []
    assert by_id["s_residual"].locator.status is VisibleFactStatus.KNOWN
    assert (
        by_id["s_residual"].timing.cutoff_posture.status is not VisibleFactStatus.KNOWN
    )

    # s_dark: no files, locator not KNOWN, mixed cutoff
    assert by_id["s_dark"].preserved_file_ids == []
    assert by_id["s_dark"].locator.status is not VisibleFactStatus.KNOWN
    assert by_id["s_dark"].timing.cutoff_posture.value == "mixed"

    # producer-valid: exactly the two referenced files, no orphans
    assert set(files) == {"f_clean", "f_ph"}
