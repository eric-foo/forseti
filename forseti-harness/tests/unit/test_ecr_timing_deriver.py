import pytest

from _ecr_builders import build_packet
from ecr.deriver import derive_timing_postures
from source_capture.models import (
    CUTOFF_POSTURE_VALUES,
    SourceCapturePacket,
    VisibleFact,
    VisibleFactStatus,
    known_fact,
    not_applicable,
    not_attempted,
    unknown_with_reason,
)


def _packet(cutoffs: list[VisibleFact]) -> SourceCapturePacket:
    """Build a minimal valid packet whose slices carry the given cutoff facts.

    One preserved file is referenced by the first slice so the packet's
    preserved-file-reference invariants are satisfied without coupling the test
    to file plumbing. Cutoff facts pass through ``build_packet`` unchanged.
    """
    # helper-delta vs _ecr_builders.build_packet defaults: this file keeps its
    # original neutral packet identity (test_family / test_surface / n-a locator).
    return build_packet(
        [
            {
                "id": f"s{i}",
                "files": ([("f1", "0" * 64)] if i == 0 else []),
                "cutoff": cutoff,
            }
            for i, cutoff in enumerate(cutoffs)
        ],
        source_family="test_family",
        source_surface="test_surface",
        source_locator=not_applicable("test"),
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
