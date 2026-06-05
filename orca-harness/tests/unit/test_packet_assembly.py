from __future__ import annotations

from pathlib import Path

import pytest

from source_capture.models import (
    PacketTiming,
    SourceCaptureSlice,
    known_fact,
    not_applicable,
    not_attempted,
    unknown_with_reason,
)
from source_capture.packet_assembly import (
    stage_and_write_packet,
    staged_file_id_map,
    validate_capture_posture_honesty,
)


def _timing() -> PacketTiming:
    return PacketTiming(
        source_publication_or_event=unknown_with_reason("not supplied"),
        source_edit_or_version=unknown_with_reason("not supplied"),
        capture_time=known_fact("2026-06-02T00:00:00Z"),
        recapture_time=not_applicable("first capture"),
        cutoff_posture=unknown_with_reason("not supplied"),
    )


def _slice(
    *,
    slice_id: str = "slice_01",
    access=None,
    archive=None,
    media=None,
    recapture=None,
    limitations=None,
) -> SourceCaptureSlice:
    return SourceCaptureSlice(
        slice_id=slice_id,
        locator=known_fact("https://example.test/resource"),
        timing=_timing(),
        access_posture=access or known_fact("direct_http succeeded with HTTP 200"),
        archive_history_posture=archive or not_attempted("archive not queried"),
        media_modality_posture=media or not_attempted("linked media not fetched"),
        re_capture_relationship=recapture or not_applicable("first capture"),
        limitations=list(limitations or []),
        preserved_file_ids=["file_01"],
    )


def _capture_postures(*, access=None, archive=None, media=None, recapture=None) -> dict[str, object]:
    return {
        "access_posture": access or known_fact("direct_http succeeded with HTTP 200"),
        "archive_history_posture": archive or not_attempted("archive not queried"),
        "media_modality_posture": media or not_attempted("linked media not fetched"),
        "re_capture_relationship": recapture or not_applicable("first capture"),
    }


# --- staged_file_id_map ------------------------------------------------------


def test_staged_file_id_map_orders_by_position() -> None:
    mapping = staged_file_id_map([("body.bin", b"x"), ("metadata.json", b"{}")])
    assert mapping == {"body.bin": "file_01", "metadata.json": "file_02"}


def test_staged_file_id_map_rejects_duplicate_filename() -> None:
    with pytest.raises(ValueError, match="duplicate staged artifact filename"):
        staged_file_id_map([("body.bin", b"x"), ("body.bin", b"y")])


# --- validate_capture_posture_honesty ---------------------------------------


def test_honesty_accepts_clean_http_like_postures() -> None:
    # The reviewer's "direct HTTP same-posture case remains valid" check:
    # access=known, archive/media=not_attempted, recapture=not_applicable, no
    # limitations anywhere. not_attempted / not_applicable are honest scope, not
    # limitations, so this must NOT raise.
    validate_capture_posture_honesty(
        source_slices=[_slice()],
        capture_postures=_capture_postures(),
        limitations=[],
    )


def test_honesty_rejects_slice_limitation_hidden_by_empty_rollup() -> None:
    with pytest.raises(ValueError, match="surface slice-level limitations"):
        validate_capture_posture_honesty(
            source_slices=[_slice(limitations=["asset_02_not_preserved: timeout"])],
            capture_postures=_capture_postures(),
            limitations=[],
        )


def test_honesty_accepts_slice_limitation_surfaced_by_rollup() -> None:
    validate_capture_posture_honesty(
        source_slices=[_slice(limitations=["asset_02_not_preserved: timeout"])],
        capture_postures=_capture_postures(),
        limitations=["preserved 1 of 2 assets"],
    )


def test_honesty_rejects_unknown_posture_hidden_by_clean_rollup() -> None:
    # The core red case: a slice carries an unknown_with_reason posture but
    # leaves slice.limitations empty AND the capture-level rollup is clean.
    with pytest.raises(ValueError, match="hides a slice gap on 'access_posture'"):
        validate_capture_posture_honesty(
            source_slices=[_slice(access=unknown_with_reason("got 200 but body was a login wall"))],
            capture_postures=_capture_postures(),  # capture access = known
            limitations=[],
        )


def test_honesty_accepts_unknown_posture_surfaced_by_matching_capture_posture() -> None:
    # Surfaced because the capture-level posture on the same axis also reports
    # unknown_with_reason -- the rollup is not claiming clean.
    validate_capture_posture_honesty(
        source_slices=[_slice(access=unknown_with_reason("got 200 but body was a login wall"))],
        capture_postures=_capture_postures(access=unknown_with_reason("at least one slice access is unverified")),
        limitations=[],
    )


def test_honesty_accepts_unknown_posture_surfaced_by_capture_limitation() -> None:
    # Surfaced because the capture-level limitations list is non-empty.
    validate_capture_posture_honesty(
        source_slices=[_slice(media=unknown_with_reason("could not determine media modality"))],
        capture_postures=_capture_postures(),
        limitations=["media modality could not be determined for one slice"],
    )


def test_honesty_ignores_not_attempted_and_not_applicable_axes() -> None:
    # not_attempted / not_applicable on every axis with empty limitations stays
    # valid -- they are honest scope statements, never a hidden gap.
    validate_capture_posture_honesty(
        source_slices=[
            _slice(
                access=not_attempted("access not attempted for this slice"),
                archive=not_attempted("archive not queried"),
                media=not_applicable("no media on this surface"),
                recapture=not_applicable("first capture"),
            )
        ],
        capture_postures=_capture_postures(access=not_attempted("access not attempted")),
        limitations=[],
    )


# --- stage_and_write_packet enforcement + collision routing ------------------


def test_stage_and_write_rejects_hidden_gap_before_writing(tmp_path: Path) -> None:
    output_directory = tmp_path / "packet"
    with pytest.raises(ValueError, match="hides a slice gap"):
        stage_and_write_packet(
            output_directory=output_directory,
            staged_artifacts=[("body.bin", b"payload")],
            source_slices=[_slice(access=unknown_with_reason("ambiguous access result"))],
            limitations=[],
            **_capture_postures(),  # capture access = known -> hidden gap
        )
    # Honesty check runs before any byte is staged or the packet is written.
    assert not output_directory.exists()
    assert not (tmp_path / "body.bin").exists()


def test_stage_and_write_collision_message_names_conflicting_path(tmp_path: Path) -> None:
    output_directory = tmp_path / "packet"
    conflict = tmp_path / "body.bin"
    conflict.write_bytes(b"stale")
    with pytest.raises(ValueError) as excinfo:
        stage_and_write_packet(
            output_directory=output_directory,
            staged_artifacts=[("body.bin", b"new")],
            source_slices=[],
        )
    message = str(excinfo.value)
    assert "staging files already exist" in message  # preserved for media-runner test
    assert "body.bin" in message  # self-routing: names the conflicting path


def test_stage_and_write_rejects_writer_owned_kwargs(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="owned by stage_and_write_packet"):
        stage_and_write_packet(
            output_directory=tmp_path / "packet",
            staged_artifacts=[("body.bin", b"x")],
            source_slices=[_slice()],
            input_files=["smuggled"],
        )
