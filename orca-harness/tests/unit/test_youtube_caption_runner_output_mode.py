from __future__ import annotations

from pathlib import Path

import pytest

from runners import run_source_capture_youtube_caption_packet as runner

_VIDEO_ID = "vid12345678"
_LEADING_DASH_VIDEO_ID = "-V7MN2IWMpA"


def test_youtube_caption_runner_rejects_explicit_output_and_data_root_before_fetch(monkeypatch, tmp_path: Path) -> None:
    def fail_fetch(_video_id: str):  # pragma: no cover - must not be reached
        raise AssertionError("fetch should not run when output mode is invalid")

    monkeypatch.setattr(runner, "fetch_youtube_caption_artifacts", fail_fetch)

    with pytest.raises(SystemExit) as exc:
        runner.main(
            [
                "--video-id",
                _VIDEO_ID,
                "--output",
                str(tmp_path / "packet"),
                "--data-root",
                str(tmp_path / "lake"),
            ]
        )

    assert exc.value.code == 2


def test_youtube_caption_runner_ignores_env_data_root_when_output_is_explicit(monkeypatch, tmp_path: Path) -> None:
    output = tmp_path / "packet"
    monkeypatch.setenv("ORCA_DATA_ROOT", str(tmp_path / "lake"))

    def fake_fetch(video_id: str) -> object:
        assert video_id == _VIDEO_ID
        return object()

    def fake_write(cap, *, output_directory, data_root, decision_question):
        assert output_directory == output
        assert data_root is None
        assert decision_question
        return 0, str(output)

    monkeypatch.setattr(runner, "fetch_youtube_caption_artifacts", fake_fetch)
    monkeypatch.setattr(runner, "write_caption_packet", fake_write)

    assert runner.main(["--video-id", _VIDEO_ID, "--output", str(output)]) == 0


def test_youtube_caption_runner_accepts_leading_dash_video_id(monkeypatch, tmp_path: Path) -> None:
    output = tmp_path / "packet"

    def fake_fetch(video_id: str) -> object:
        assert video_id == _LEADING_DASH_VIDEO_ID
        return object()

    def fake_write(cap, *, output_directory, data_root, decision_question):
        assert output_directory == output
        assert data_root is None
        assert decision_question
        return 0, str(output)

    monkeypatch.setattr(runner, "fetch_youtube_caption_artifacts", fake_fetch)
    monkeypatch.setattr(runner, "write_caption_packet", fake_write)

    assert runner.main(["--video-id", _LEADING_DASH_VIDEO_ID, "--output", str(output)]) == 0


def test_youtube_caption_runner_rejects_data_root_flag_as_missing_video_id(monkeypatch, tmp_path: Path) -> None:
    resolved_root = object()
    monkeypatch.setenv("ORCA_DATA_ROOT", str(tmp_path / "lake"))

    class FakeDataLakeRoot:
        @staticmethod
        def resolve(*, explicit):
            assert explicit is None
            return resolved_root

    def fail_fetch(_video_id: str):  # pragma: no cover - must not be reached
        raise AssertionError("fetch should not run when video id is missing")

    from data_lake import root as root_module

    monkeypatch.setattr(root_module, "DataLakeRoot", FakeDataLakeRoot)
    monkeypatch.setattr(runner, "fetch_youtube_caption_artifacts", fail_fetch)

    with pytest.raises(SystemExit) as exc:
        runner.main(["--video-id", "--data-root"])

    assert exc.value.code == 2
