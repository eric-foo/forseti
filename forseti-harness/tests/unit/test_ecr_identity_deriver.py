from ecr.deriver import derive_identity_postures
from ecr.models import IdentityState
from source_capture.models import (
    OBLIGATION_CONTRACT_VERSION,
    SOURCE_CAPTURE_MANIFEST_VERSION,
    CaptureModeCategory,
    PacketTiming,
    PreservedFile,
    ReceiptMetadata,
    SourceCapturePacket,
    SourceCaptureSlice,
    VisibleFact,
    known_fact,
    not_applicable,
    not_attempted,
)


def _timing() -> PacketTiming:
    na = not_applicable("test")
    return PacketTiming(
        source_publication_or_event=na,
        source_edit_or_version=na,
        capture_time=na,
        recapture_time=na,
        cutoff_posture=na,
    )


def _slice() -> SourceCaptureSlice:
    return SourceCaptureSlice(
        slice_id="s0",
        locator=not_applicable("test"),
        timing=_timing(),
        access_posture=not_applicable("test"),
        archive_history_posture=not_applicable("test"),
        media_modality_posture=not_applicable("test"),
        re_capture_relationship=not_applicable("test"),
        preserved_file_ids=["f0"],
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
    return SourceCapturePacket(
        packet_id="pkt-test",
        manifest_version=SOURCE_CAPTURE_MANIFEST_VERSION,
        obligation_contract_version=OBLIGATION_CONTRACT_VERSION,
        source_family=source_family,
        source_surface=source_surface,
        source_locator=(locator if locator is not None else known_fact("https://x/1")),
        requested_decision_context=not_applicable("test"),
        capture_context=not_applicable("test"),
        actor_audience_context=not_applicable("test"),
        capture_mode=CaptureModeCategory.MIXED,
        operator_category="test",
        session_identity="test",
        timing=_timing(),
        access_posture=not_applicable("test"),
        archive_history_posture=not_applicable("test"),
        media_modality_posture=not_applicable("test"),
        re_capture_relationship=not_applicable("test"),
        source_slices=[_slice()],
        preserved_files=[
            PreservedFile(
                file_id="f0",
                original_path="/tmp/x",
                relative_packet_path="f0",
                sha256="a" * 64,
                hash_basis="raw_stored_bytes",
                size_bytes=0,
            )
        ],
        receipt_metadata=ReceiptMetadata(
            title="t", generated_at="2026-01-01T00:00:00Z", summary="s"
        ),
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
