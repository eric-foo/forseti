from _ecr_builders import build_packet
from ecr.deriver import derive_inspectability_postures
from ecr.models import InspectabilityState
from source_capture.models import SourceCapturePacket, not_applicable

_REAL_SHA = "a" * 64  # 64 hex, not all-zero -> verifiable
_ZERO_SHA = "0" * 64  # all-zero sentinel -> placeholder
_BAD_SHA = "not-a-real-hash"  # not 64 hex -> placeholder


def _packet(slice_specs: list[dict]) -> SourceCapturePacket:
    """Build a minimal valid packet from per-slice specs (see ``_ecr_builders``)."""
    # helper-delta vs _ecr_builders.build_packet defaults: this file keeps its
    # original neutral packet identity (test_family / test_surface / n-a locator).
    return build_packet(
        slice_specs,
        source_family="test_family",
        source_surface="test_surface",
        source_locator=not_applicable("test"),
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
