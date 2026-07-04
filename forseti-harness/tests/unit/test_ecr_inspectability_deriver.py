from ecr.deriver import derive_inspectability_postures
from ecr.models import InspectabilityState
from source_capture.models import (
    OBLIGATION_CONTRACT_VERSION,
    SOURCE_CAPTURE_MANIFEST_VERSION,
    CaptureModeCategory,
    PacketTiming,
    PreservedFile,
    ReceiptMetadata,
    SourceCapturePacket,
    SourceCaptureSlice,
    known_fact,
    not_applicable,
)

_REAL_SHA = "a" * 64  # 64 hex, not all-zero -> verifiable
_ZERO_SHA = "0" * 64  # all-zero sentinel -> placeholder
_BAD_SHA = "not-a-real-hash"  # not 64 hex -> placeholder


def _timing() -> PacketTiming:
    na = not_applicable("test")
    return PacketTiming(
        source_publication_or_event=na,
        source_edit_or_version=na,
        capture_time=na,
        recapture_time=na,
        cutoff_posture=na,
    )


def _packet(slice_specs: list[dict]) -> SourceCapturePacket:
    """Build a minimal valid packet from per-slice specs.

    Each spec: ``{"id": str, "files": [(file_id, sha256)], "locator_known": bool}``.
    Every preserved file is referenced by the slice that lists it, so the packet's
    no-orphan invariant holds. At least one slice must list a file (the packet
    requires >=1 preserved file).
    """
    preserved: dict[str, str] = {}
    slices: list[SourceCaptureSlice] = []
    for spec in slice_specs:
        files = spec.get("files", [])
        for file_id, sha in files:
            preserved[file_id] = sha
        slices.append(
            SourceCaptureSlice(
                slice_id=spec["id"],
                locator=(
                    known_fact("loc") if spec.get("locator_known") else not_applicable("test")
                ),
                timing=_timing(),
                access_posture=not_applicable("test"),
                archive_history_posture=not_applicable("test"),
                media_modality_posture=not_applicable("test"),
                re_capture_relationship=not_applicable("test"),
                preserved_file_ids=[file_id for file_id, _ in files],
            )
        )
    preserved_files = [
        PreservedFile(
            file_id=file_id,
            original_path="/tmp/x",
            relative_packet_path=file_id,
            sha256=sha,
            hash_basis="raw_stored_bytes",
            size_bytes=0,
        )
        for file_id, sha in preserved.items()
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
        timing=_timing(),
        access_posture=not_applicable("test"),
        archive_history_posture=not_applicable("test"),
        media_modality_posture=not_applicable("test"),
        re_capture_relationship=not_applicable("test"),
        source_slices=slices,
        preserved_files=preserved_files,
        receipt_metadata=ReceiptMetadata(
            title="t", generated_at="2026-01-01T00:00:00Z", summary="s"
        ),
    )


def test_single_referenced_file_real_hash_is_verifiable():
    [posture] = derive_inspectability_postures(
        _packet([{"id": "s0", "files": [("f0", _REAL_SHA)]}])
    )
    assert posture.slice_id == "s0"
    assert posture.state is InspectabilityState.INSPECTABLE_VERIFIABLE
    assert posture.clears_inspectable is True
    assert posture.reason is None


def test_all_files_must_verify_one_placeholder_demotes_to_reference_only():
    [posture] = derive_inspectability_postures(
        _packet([{"id": "s0", "files": [("f0", _REAL_SHA), ("f1", _ZERO_SHA)]}])
    )
    assert posture.state is InspectabilityState.INSPECTABLE_REFERENCE_ONLY
    assert posture.clears_inspectable is False
    assert "f1" in posture.reason
    assert "f0" not in posture.reason  # only the failing file is named


def test_all_zero_sha_is_placeholder():
    [posture] = derive_inspectability_postures(
        _packet([{"id": "s0", "files": [("f0", _ZERO_SHA)]}])
    )
    assert posture.state is InspectabilityState.INSPECTABLE_REFERENCE_ONLY
    assert posture.clears_inspectable is False


def test_malformed_sha_is_placeholder():
    [posture] = derive_inspectability_postures(
        _packet([{"id": "s0", "files": [("f0", _BAD_SHA)]}])
    )
    assert posture.state is InspectabilityState.INSPECTABLE_REFERENCE_ONLY
    assert posture.clears_inspectable is False


def test_uppercase_hex_is_verifiable():
    [posture] = derive_inspectability_postures(
        _packet([{"id": "s0", "files": [("f0", "A" * 64)]}])
    )
    assert posture.state is InspectabilityState.INSPECTABLE_VERIFIABLE


def test_no_files_locator_known_is_reference_only():
    postures = derive_inspectability_postures(
        _packet(
            [
                {"id": "s0", "files": [], "locator_known": True},
                {"id": "carrier", "files": [("fc", _REAL_SHA)]},
            ]
        )
    )
    by_id = {p.slice_id: p for p in postures}
    assert by_id["s0"].state is InspectabilityState.INSPECTABLE_REFERENCE_ONLY
    assert by_id["s0"].clears_inspectable is False


def test_no_files_locator_unknown_is_not_inspectable():
    postures = derive_inspectability_postures(
        _packet(
            [
                {"id": "s0", "files": [], "locator_known": False},
                {"id": "carrier", "files": [("fc", _REAL_SHA)]},
            ]
        )
    )
    by_id = {p.slice_id: p for p in postures}
    assert by_id["s0"].state is InspectabilityState.NOT_INSPECTABLE
    assert by_id["s0"].clears_inspectable is False
    assert by_id["carrier"].state is InspectabilityState.INSPECTABLE_VERIFIABLE


def test_multi_slice_order_and_ids():
    postures = derive_inspectability_postures(
        _packet(
            [
                {"id": "s0", "files": [("f0", _REAL_SHA)]},
                {"id": "s1", "files": [("f1", _ZERO_SHA)]},
                {"id": "s2", "files": [], "locator_known": False},
            ]
        )
    )
    assert [p.slice_id for p in postures] == ["s0", "s1", "s2"]
    assert postures[0].state is InspectabilityState.INSPECTABLE_VERIFIABLE
    assert postures[1].state is InspectabilityState.INSPECTABLE_REFERENCE_ONLY
    assert postures[2].state is InspectabilityState.NOT_INSPECTABLE


def test_pure_input_unchanged_and_deterministic():
    packet = _packet(
        [
            {"id": "s0", "files": [("f0", _REAL_SHA)]},
            {"id": "s1", "files": [], "locator_known": True},
        ]
    )
    before = packet.model_dump()
    first = derive_inspectability_postures(packet)
    second = derive_inspectability_postures(packet)
    assert packet.model_dump() == before
    assert first == second
