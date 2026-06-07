"""Mixed-grain composition (I1): the SP-1 / SP-2 / SP-3 derivers read together.

Proves the three source-side derivers compose into one coherent parallel ECR
record over a single packet at mixed grain (SP-1 per-packet; SP-2/SP-3
per-slice). It asserts STRUCTURAL composition only -- each dimension's clears_*
read at its own grain -- and deliberately computes NO aggregate source-side
verdict: combining the dimensions is the frozen JSG-01 conductor's job, not this
record's. The frozen conductor is never imported or exercised here, and nothing
in this file is a JSG-01 readiness claim.
"""
from _ecr_builders import build_packet, varied_packet
from ecr.deriver import (
    derive_identity_postures,
    derive_inspectability_postures,
    derive_timing_postures,
)
from ecr.models import IdentityState, InspectabilityState
from source_capture.models import VisibleFactStatus, not_attempted

_SHA = "a" * 64


def _read_record(packet):
    """Join the three derivers' output the way a reader would (the read contract).

    Returns ``(identity, by_slice)`` where ``identity`` is the single per-packet
    posture and ``by_slice`` maps ``slice_id -> {"timing", "inspectability"}``.
    The join asserts slice-order alignment before indexing. It lives here, not in
    production, until a real consumer needs it.
    """
    [identity] = derive_identity_postures(packet)
    slice_ids = [s.slice_id for s in packet.source_slices]
    timing_postures = derive_timing_postures(packet)
    inspect_postures = derive_inspectability_postures(packet)
    assert [p.slice_id for p in timing_postures] == slice_ids
    assert [p.slice_id for p in inspect_postures] == slice_ids
    timing = {p.slice_id: p for p in timing_postures}
    inspect = {p.slice_id: p for p in inspect_postures}
    by_slice = {
        s.slice_id: {"timing": timing[s.slice_id], "inspectability": inspect[s.slice_id]}
        for s in packet.source_slices
    }
    return identity, by_slice


def test_grain_and_count_align_across_dimensions():
    packet = varied_packet()
    identity = derive_identity_postures(packet)
    timing = derive_timing_postures(packet)
    inspect = derive_inspectability_postures(packet)

    # SP-1 is per-packet: exactly one posture, keyed by packet_id
    assert len(identity) == 1
    assert identity[0].packet_id == packet.packet_id

    # SP-2 / SP-3 are per-slice: one posture each, in source_slices order, 1:1
    slice_ids = [s.slice_id for s in packet.source_slices]
    assert [p.slice_id for p in timing] == slice_ids
    assert [p.slice_id for p in inspect] == slice_ids


def test_each_dimension_is_independently_readable_at_its_grain():
    packet = varied_packet()  # SP-1 resolved identity
    identity, by_slice = _read_record(packet)

    # packet-grain identity clears (resolved), independent of any slice
    assert identity.state is IdentityState.RESOLVED
    assert identity.clears_identity is True

    # s_clean: pre_cutoff + verifiable -> both slice dimensions clear
    assert by_slice["s_clean"]["timing"].carried_cutoff_posture == "pre_cutoff"
    assert by_slice["s_clean"]["timing"].residual is None
    assert by_slice["s_clean"]["timing"].clears_pre_cutoff is True
    assert (
        by_slice["s_clean"]["inspectability"].state
        is InspectabilityState.INSPECTABLE_VERIFIABLE
    )
    assert by_slice["s_clean"]["inspectability"].clears_inspectable is True

    # s_placeholder: post_cutoff + placeholder sha -> neither slice dimension clears
    assert by_slice["s_placeholder"]["timing"].carried_cutoff_posture == "post_cutoff"
    assert by_slice["s_placeholder"]["timing"].residual is None
    assert by_slice["s_placeholder"]["timing"].clears_pre_cutoff is False
    assert (
        by_slice["s_placeholder"]["inspectability"].state
        is InspectabilityState.INSPECTABLE_REFERENCE_ONLY
    )
    assert by_slice["s_placeholder"]["inspectability"].clears_inspectable is False

    # s_residual: cutoff residual + no-files/locator-known -> neither clears
    assert by_slice["s_residual"]["timing"].carried_cutoff_posture is None
    assert by_slice["s_residual"]["timing"].clears_pre_cutoff is False
    assert by_slice["s_residual"]["timing"].residual is not None
    assert (
        by_slice["s_residual"]["timing"].residual.status
        is VisibleFactStatus.NOT_ATTEMPTED
    )
    assert (
        by_slice["s_residual"]["inspectability"].state
        is InspectabilityState.INSPECTABLE_REFERENCE_ONLY
    )
    assert by_slice["s_residual"]["inspectability"].clears_inspectable is False

    # s_dark: mixed cutoff + not_inspectable -> neither clears
    assert by_slice["s_dark"]["timing"].carried_cutoff_posture == "mixed"
    assert by_slice["s_dark"]["timing"].residual is None
    assert by_slice["s_dark"]["timing"].clears_pre_cutoff is False
    assert (
        by_slice["s_dark"]["inspectability"].state
        is InspectabilityState.NOT_INSPECTABLE
    )


def test_packet_identity_does_not_alter_slice_dimensions():
    # Cross-grain orthogonality: a packet-grain identity change must not bleed
    # into the per-slice SP-2/SP-3 postures (no dimension overwrites another).
    specs = [
        {
            "id": "s_clean",
            "files": [("f_clean", _SHA)],
            "locator_known": True,
            "cutoff": "pre_cutoff",
        },
        {"id": "s_dark", "files": [], "locator_known": False, "cutoff": "mixed"},
    ]
    resolved = build_packet(specs)
    unresolved = build_packet(specs, source_family="")

    [r_id] = derive_identity_postures(resolved)
    [u_id] = derive_identity_postures(unresolved)
    assert r_id.state is IdentityState.RESOLVED
    assert u_id.state is IdentityState.UNRESOLVED  # only the packet grain changed

    # the per-slice dimensions are identical regardless of packet identity
    assert derive_timing_postures(resolved) == derive_timing_postures(unresolved)
    assert (
        derive_inspectability_postures(resolved)
        == derive_inspectability_postures(unresolved)
    )


def test_identity_variants_compose_at_packet_grain():
    base = [
        {"id": "s0", "files": [("f0", _SHA)], "locator_known": True, "cutoff": "pre_cutoff"}
    ]

    [resolved] = derive_identity_postures(build_packet(base))
    assert resolved.state is IdentityState.RESOLVED
    assert resolved.clears_identity is True

    [family_only] = derive_identity_postures(
        build_packet(base, source_surface="", source_locator=not_attempted("no id"))
    )
    assert family_only.state is IdentityState.FAMILY_ONLY
    assert family_only.clears_identity is True  # clears WITH a named limitation

    [unresolved] = derive_identity_postures(build_packet(base, source_family=""))
    assert unresolved.state is IdentityState.UNRESOLVED
    assert unresolved.clears_identity is False


def test_purity_and_determinism_end_to_end():
    packet = varied_packet()
    before = packet.model_dump()
    first = _read_record(packet)
    second = _read_record(packet)
    # all three derivers leave the packet unmutated
    assert packet.model_dump() == before
    # the assembled record is deterministic
    assert first == second


def test_each_posture_round_trips():
    packet = varied_packet()
    postures = (
        list(derive_identity_postures(packet))
        + list(derive_timing_postures(packet))
        + list(derive_inspectability_postures(packet))
    )
    for posture in postures:
        assert type(posture).model_validate(posture.model_dump()) == posture
