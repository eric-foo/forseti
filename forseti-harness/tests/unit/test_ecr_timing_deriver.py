import pytest

from ecr.deriver import derive_timing_postures
from source_capture.models import (
    CUTOFF_POSTURE_VALUES,
    OBLIGATION_CONTRACT_VERSION,
    SOURCE_CAPTURE_MANIFEST_VERSION,
    CaptureModeCategory,
    PacketTiming,
    PreservedFile,
    ReceiptMetadata,
    SourceCapturePacket,
    SourceCaptureSlice,
    VisibleFact,
    VisibleFactStatus,
    known_fact,
    not_applicable,
    not_attempted,
    unknown_with_reason,
)


def _timing(cutoff: VisibleFact) -> PacketTiming:
    return PacketTiming(
        source_publication_or_event=not_applicable("test"),
        source_edit_or_version=not_applicable("test"),
        capture_time=not_applicable("test"),
        recapture_time=not_applicable("test"),
        cutoff_posture=cutoff,
    )


def _packet(cutoffs: list[VisibleFact]) -> SourceCapturePacket:
    """Build a minimal valid packet whose slices carry the given cutoff facts.

    One preserved file is referenced by the first slice so the packet's
    preserved-file-reference invariants are satisfied without coupling the test
    to file plumbing.
    """
    slices = [
        SourceCaptureSlice(
            slice_id=f"s{i}",
            locator=not_applicable("test"),
            timing=_timing(cutoff),
            access_posture=not_applicable("test"),
            archive_history_posture=not_applicable("test"),
            media_modality_posture=not_applicable("test"),
            re_capture_relationship=not_applicable("test"),
            preserved_file_ids=(["f1"] if i == 0 else []),
        )
        for i, cutoff in enumerate(cutoffs)
    ]
    return SourceCapturePacket(
        packet_id="pkt-test",
        manifest_version=SOURCE_CAPTURE_MANIFEST_VERSION,
        obligation_contract_version=OBLIGATION_CONTRACT_VERSION,
        source_family="test_family",
        source_surface="test_surface",
        source_locator=not_applicable("test"),
        requested_decision_context=not_applicable("test"),
        capture_context=not_applicable("test"),
        actor_audience_context=not_applicable("test"),
        capture_mode=CaptureModeCategory.MIXED,
        operator_category="test",
        session_identity="test",
        timing=_timing(known_fact("pre_cutoff")),
        access_posture=not_applicable("test"),
        archive_history_posture=not_applicable("test"),
        media_modality_posture=not_applicable("test"),
        re_capture_relationship=not_applicable("test"),
        source_slices=slices,
        preserved_files=[
            PreservedFile(
                file_id="f1",
                original_path="/tmp/x",
                relative_packet_path="x",
                sha256="0" * 64,
                hash_basis="raw_stored_bytes",
                size_bytes=0,
            )
        ],
        receipt_metadata=ReceiptMetadata(
            title="t", generated_at="2026-01-01T00:00:00Z", summary="s"
        ),
    )


def test_known_pre_cutoff_clears():
    [posture] = derive_timing_postures(_packet([known_fact("pre_cutoff")]))
    assert posture.slice_id == "s0"
    assert posture.carried_cutoff_posture == "pre_cutoff"
    assert posture.residual is None
    assert posture.clears_pre_cutoff is True


@pytest.mark.parametrize("value", sorted(CUTOFF_POSTURE_VALUES - {"pre_cutoff"}))
def test_known_non_pre_cutoff_carried_not_cleared(value):
    [posture] = derive_timing_postures(_packet([known_fact(value)]))
    assert posture.carried_cutoff_posture == value
    assert posture.residual is None
    assert posture.clears_pre_cutoff is False


def test_known_source_cutoff_values_carried_without_recoining_vocabulary():
    postures = derive_timing_postures(
        _packet([known_fact(value) for value in sorted(CUTOFF_POSTURE_VALUES)])
    )
    assert [posture.carried_cutoff_posture for posture in postures] == sorted(
        CUTOFF_POSTURE_VALUES
    )
    assert [posture.clears_pre_cutoff for posture in postures] == [
        value == "pre_cutoff" for value in sorted(CUTOFF_POSTURE_VALUES)
    ]
    assert all(posture.residual is None for posture in postures)


def test_non_known_statuses_become_residual():
    facts = [
        unknown_with_reason("no visible timestamp"),
        not_attempted("did not check"),
        not_applicable("not applicable here"),
    ]
    postures = derive_timing_postures(_packet(facts))
    expected = [
        (VisibleFactStatus.UNKNOWN_WITH_REASON, "no visible timestamp"),
        (VisibleFactStatus.NOT_ATTEMPTED, "did not check"),
        (VisibleFactStatus.NOT_APPLICABLE, "not applicable here"),
    ]
    assert len(postures) == len(expected)
    for posture, (status, reason) in zip(postures, expected):
        assert posture.carried_cutoff_posture is None
        assert posture.residual is not None
        assert posture.residual.status == status
        assert posture.residual.reason == reason
        assert posture.clears_pre_cutoff is False


def test_multi_slice_order_and_ids():
    postures = derive_timing_postures(
        _packet([known_fact("pre_cutoff"), known_fact("post_cutoff"), not_attempted("x")])
    )
    assert [p.slice_id for p in postures] == ["s0", "s1", "s2"]
    assert postures[0].clears_pre_cutoff is True
    assert postures[1].clears_pre_cutoff is False
    assert postures[2].residual is not None


def test_pure_input_unchanged_and_deterministic():
    packet = _packet([known_fact("pre_cutoff"), not_attempted("x")])
    before = packet.model_dump()
    first = derive_timing_postures(packet)
    second = derive_timing_postures(packet)
    assert packet.model_dump() == before
    assert first == second
