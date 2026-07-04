from __future__ import annotations

from pathlib import Path

import pytest

from runners import run_source_capture_youtube_watch_packet as runner

_VIDEO_ID = "vid12345678"
_LEADING_DASH_VIDEO_ID = "-V7MN2IWMpA"


def test_youtube_watch_runner_rejects_explicit_output_and_data_root_before_fetch(
    monkeypatch, tmp_path: Path
) -> None:
    def fail_run(**_kwargs):  # pragma: no cover - must not be reached
        raise AssertionError("runner should not run when output mode is invalid")

    monkeypatch.setattr(runner, "run_source_capture_youtube_watch_packet", fail_run)

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


def test_youtube_watch_runner_ignores_env_data_root_when_output_is_explicit(
    monkeypatch, tmp_path: Path
) -> None:
    output = tmp_path / "packet"
    monkeypatch.setenv("ORCA_DATA_ROOT", str(tmp_path / "lake"))

    def fake_run(**kwargs):
        assert kwargs["video_id"] == _VIDEO_ID
        assert kwargs["output_directory"] == output
        assert kwargs["data_root"] is None
        assert kwargs["decision_question"]
        assert kwargs["comment_pages"] == 2
        return 0, str(output)

    monkeypatch.setattr(runner, "run_source_capture_youtube_watch_packet", fake_run)

    assert runner.main(["--video-id", _VIDEO_ID, "--output", str(output)]) == 0


def test_youtube_watch_runner_accepts_leading_dash_video_id(monkeypatch, tmp_path: Path) -> None:
    output = tmp_path / "packet"

    def fake_run(**kwargs):
        assert kwargs["video_id"] == _LEADING_DASH_VIDEO_ID
        assert kwargs["output_directory"] == output
        return 0, str(output)

    monkeypatch.setattr(runner, "run_source_capture_youtube_watch_packet", fake_run)

    assert runner.main(["--video-id", _LEADING_DASH_VIDEO_ID, "--output", str(output)]) == 0


def test_youtube_watch_runner_rejects_data_root_flag_as_missing_video_id(monkeypatch, tmp_path: Path) -> None:
    resolved_root = object()
    monkeypatch.setenv("ORCA_DATA_ROOT", str(tmp_path / "lake"))

    class FakeDataLakeRoot:
        @staticmethod
        def resolve(*, explicit):
            assert explicit is None
            return resolved_root

    def fail_run(**_kwargs):  # pragma: no cover - must not be reached
        raise AssertionError("runner should not run when video id is missing")

    from data_lake import root as root_module

    monkeypatch.setattr(root_module, "DataLakeRoot", FakeDataLakeRoot)
    monkeypatch.setattr(runner, "run_source_capture_youtube_watch_packet", fail_run)

    with pytest.raises(SystemExit) as exc:
        runner.main(["--video-id", "--data-root"])

    assert exc.value.code == 2
