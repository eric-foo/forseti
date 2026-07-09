from _ecr_builders import build_packet
from ecr.deriver import derive_source_visibility_postures
from ecr.models import SourceVisibilityResidual, SourceVisibilityValue
from source_capture.models import known_fact, not_attempted, unknown_with_reason

_SHA = "a" * 64


def _archive_packet(*, cutoff, archive_history="archived", current=False):
    """An archive packet: the archive_snapshot_body slice carries D = cutoff; A is
    the packet-level archive_history_posture. Optionally add a current body."""
    specs = [{"id": "archive_snapshot_body", "files": [("f_arc", _SHA)], "cutoff": cutoff}]
    if current:
        specs.append({"id": "primary", "files": [("f_cur", _SHA)]})
    return build_packet(specs, archive_history=known_fact(archive_history))


def test_returns_one_posture_per_packet():
    postures = derive_source_visibility_postures(_archive_packet(cutoff="pre_cutoff"))
    assert len(postures) == 1
    assert postures[0].packet_id == "pkt-test"


def test_archived_pre_cutoff_no_current_is_archive_only():
    [p] = derive_source_visibility_postures(_archive_packet(cutoff="pre_cutoff"))
    assert p.value is SourceVisibilityValue.ARCHIVE_ONLY
    assert p.clears_source_visibility is True


def test_archived_post_cutoff_no_current_is_archive_post_cutoff_only():
    [p] = derive_source_visibility_postures(_archive_packet(cutoff="post_cutoff"))
    assert p.value is SourceVisibilityValue.ARCHIVE_POST_CUTOFF_ONLY
    assert p.clears_source_visibility is False


def test_archived_pre_cutoff_with_current_is_comparison_residual():
    [p] = derive_source_visibility_postures(
        _archive_packet(cutoff="pre_cutoff", current=True)
    )
    assert p.residual is SourceVisibilityResidual.RESIDUAL_COMPARISON_NOT_RECORDED
    assert p.clears_source_visibility is False


def test_archived_post_cutoff_with_current_is_post_cutoff_with_current_residual():
    [p] = derive_source_visibility_postures(
        _archive_packet(cutoff="post_cutoff", current=True)
    )
    assert p.residual is SourceVisibilityResidual.RESIDUAL_ARCHIVE_POST_CUTOFF_WITH_CURRENT


def test_archived_mixed_cutoff_is_date_unknown():
    [p] = derive_source_visibility_postures(_archive_packet(cutoff="mixed"))
    assert p.residual is SourceVisibilityResidual.RESIDUAL_ARCHIVE_DATE_UNKNOWN


def test_archived_residual_cutoff_is_date_unknown():
    [p] = derive_source_visibility_postures(_archive_packet(cutoff=None))
    assert p.residual is SourceVisibilityResidual.RESIDUAL_ARCHIVE_DATE_UNKNOWN


def test_attempt_failed():
    [p] = derive_source_visibility_postures(
        _archive_packet(cutoff="pre_cutoff", archive_history="attempt_failed")
    )
    assert p.value is SourceVisibilityValue.ATTEMPT_FAILED
    assert p.clears_source_visibility is False


def test_archive_posture_unknown_residualizes():
    packet = build_packet(
        [{"id": "archive_snapshot_body", "files": [("f0", _SHA)], "cutoff": "pre_cutoff"}],
        archive_history=unknown_with_reason("archive status unknown"),
    )
    [p] = derive_source_visibility_postures(packet)
    assert p.residual is SourceVisibilityResidual.RESIDUAL_ARCHIVE_POSTURE_UNKNOWN


def test_current_capture_only():
    # a not-archived packet with a current (non-archive) body
    packet = build_packet([{"id": "primary", "files": [("f0", _SHA)]}])
    [p] = derive_source_visibility_postures(packet)
    assert p.value is SourceVisibilityValue.CURRENT_CAPTURE_ONLY
    assert p.clears_source_visibility is False


def test_not_attempted_no_current():
    packet = build_packet(
        [{"id": "archive_snapshot_body", "files": [("f0", _SHA)], "cutoff": "pre_cutoff"}],
        archive_history=not_attempted("archive not attempted"),
    )
    [p] = derive_source_visibility_postures(packet)
    assert p.value is SourceVisibilityValue.NOT_ATTEMPTED


def test_no_visibility_basis():
    # not_applicable archive (default), only an archive slice, no current body
    packet = build_packet(
        [{"id": "archive_snapshot_body", "files": [("f0", _SHA)], "cutoff": "pre_cutoff"}]
    )
    [p] = derive_source_visibility_postures(packet)
    assert p.residual is SourceVisibilityResidual.RESIDUAL_NO_VISIBILITY_BASIS


def test_not_attempted_with_current_is_current_capture_only():
    # precedence pin: current-body presence is graded before the NOT_ATTEMPTED branch
    packet = build_packet(
        [{"id": "primary", "files": [("f0", _SHA)]}],
        archive_history=not_attempted("archive not attempted"),
    )
    [p] = derive_source_visibility_postures(packet)
    assert p.value is SourceVisibilityValue.CURRENT_CAPTURE_ONLY
    assert p.clears_source_visibility is False


def test_archived_known_unknown_cutoff_is_date_unknown():
    # KNOWN "unknown" D-class collapses to date-unknown, not a distinct value
    [p] = derive_source_visibility_postures(_archive_packet(cutoff="unknown"))
    assert p.residual is SourceVisibilityResidual.RESIDUAL_ARCHIVE_DATE_UNKNOWN


def test_archived_absent_archive_body_is_date_unknown():
    # archived posture but no archive_snapshot_body slice -> D unresolvable
    packet = build_packet(
        [{"id": "primary", "files": [("f0", _SHA)], "cutoff": "pre_cutoff"}],
        archive_history=known_fact("archived"),
    )
    [p] = derive_source_visibility_postures(packet)
    assert p.residual is SourceVisibilityResidual.RESIDUAL_ARCHIVE_DATE_UNKNOWN


def test_pure_input_unchanged_and_deterministic():
    packet = _archive_packet(cutoff="pre_cutoff")
    before = packet.model_dump()
    first = derive_source_visibility_postures(packet)
    second = derive_source_visibility_postures(packet)
    assert packet.model_dump() == before
    assert first == second
