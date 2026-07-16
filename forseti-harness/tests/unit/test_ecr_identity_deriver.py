from _ecr_builders import build_packet
from ecr.deriver import derive_identity_postures
from ecr.models import IdentityState
from source_capture.models import (
    SourceCapturePacket,
    VisibleFact,
    known_fact,
    not_attempted,
)


def _packet(
    *,
    source_family: str = "reddit",
    source_surface: str = "r/example",
    locator: VisibleFact | None = None,
) -> SourceCapturePacket:
    """Build a minimal valid packet with controllable identity inputs.

    A fixed minimal slice + preserved file satisfy the packet's structural
    invariants; only the identity fields vary per test.
    """
    return build_packet(
        [{"id": "s0", "files": [("f0", "a" * 64)]}],
        source_family=source_family,
        source_surface=source_surface,
        source_locator=locator,
    )


def test_returns_one_posture_per_packet():
    postures = derive_identity_postures(_packet())
    assert len(postures) == 1
    assert postures[0].packet_id == "pkt-test"


def test_full_identity_is_resolved():
    [posture] = derive_identity_postures(_packet())
    assert posture.state is IdentityState.RESOLVED
    assert posture.clears_identity is True
    assert posture.reason is None


def test_no_specific_locator_is_family_only():
    [posture] = derive_identity_postures(_packet(locator=not_attempted("no id")))
    assert posture.state is IdentityState.FAMILY_ONLY
    assert posture.clears_identity is True
    assert posture.reason


def test_empty_surface_is_family_only():
    [posture] = derive_identity_postures(_packet(source_surface=""))
    assert posture.state is IdentityState.FAMILY_ONLY
    assert posture.clears_identity is True


def test_whitespace_locator_value_is_family_only():
    [posture] = derive_identity_postures(_packet(locator=known_fact("   ")))
    assert posture.state is IdentityState.FAMILY_ONLY
    assert posture.clears_identity is True


def test_empty_family_is_unresolved():
    [posture] = derive_identity_postures(_packet(source_family=""))
    assert posture.state is IdentityState.UNRESOLVED
    assert posture.clears_identity is False
    assert posture.reason


def test_whitespace_family_is_unresolved():
    [posture] = derive_identity_postures(_packet(source_family="   "))
    assert posture.state is IdentityState.UNRESOLVED
    assert posture.clears_identity is False


def test_pure_input_unchanged_and_deterministic():
    packet = _packet(locator=not_attempted("x"))
    before = packet.model_dump()
    first = derive_identity_postures(packet)
    second = derive_identity_postures(packet)
    assert packet.model_dump() == before
    assert first == second
