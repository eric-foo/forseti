from __future__ import annotations

from pathlib import Path

import pytest

from data_lake.root import DataLakeRoot, FORSETI_DATA_ROOT_ENV, raw_shard
from runners.run_source_capture_packet import _build_parser, main, run_source_capture_packet
from source_capture.models import CaptureModeCategory, known_fact


@pytest.fixture(autouse=True)
def _isolate_from_operator_lake(monkeypatch: pytest.MonkeyPatch) -> None:
    # The CLI treats shell-inherited data-root env vars as implicit --data-root
    # when --output is omitted, so clear both the primary and legacy aliases.
    monkeypatch.delenv(FORSETI_DATA_ROOT_ENV, raising=False)
    monkeypatch.delenv("ORCA_DATA_ROOT", raising=False)


def _run(
    root: DataLakeRoot,
    tmp_path: Path,
    source_family: str = "reddit",
    cutoff_posture=None,
):
    src = tmp_path / "artifact.json"
    src.write_text('{"x": 1}', encoding="utf-8")
    return run_source_capture_packet(
        source_family=source_family,
        source_surface="r/test",
        source_locator=known_fact("https://www.reddit.com/r/test/comments/x/"),
        decision_question="q",
        input_files=[src],
        data_root=root,
        capture_context="generic runner lake test",
        operator_category="local_cli_operator",
        capture_mode=CaptureModeCategory.AGENT_ASSISTED,
        session_id=None,
        actor_audience_context=None,
        visible_mode_changes=[],
        source_publication_or_event=None,
        source_edit_or_version=None,
        cutoff_posture=cutoff_posture,
        recapture_time=None,
        access_posture=None,
        archive_history_posture=None,
        media_modality_posture=None,
        re_capture_relationship=None,
        warnings=[],
        limitations=[],
    )


def test_generic_runner_routes_to_lake(tmp_path: Path) -> None:
    # The generic envelope runner, given a data_root, commits into the lake and is
    # retrievable + verified by key -- the same seam the HTTP runner uses.
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    out_path = Path(_run(root, tmp_path))
    pid = out_path.name

    assert out_path == root.path / "raw" / raw_shard(pid) / pid
    assert root.find_packet(pid) is not None
    assert root.read_availability(pid) is not None
    assert root.load_raw_packet(pid).manifest["packet_id"] == pid


def test_generic_runner_cleans_its_staging_directory_when_validation_fails(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")

    with pytest.raises(ValueError, match="cutoff_posture"):
        _run(root, tmp_path, cutoff_posture=known_fact("before_decision"))

    staging = root.path / ".staging"
    assert not staging.exists() or not any(staging.iterdir())
    assert list((root.path / "raw").rglob("manifest.json")) == []


def test_cli_rejects_invalid_cutoff_before_resolving_lake(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    source = tmp_path / "artifact.json"
    source.write_text("{}", encoding="utf-8")
    lake = tmp_path / "uninitialized-lake"

    with pytest.raises(SystemExit) as exc_info:
        main(
            [
                "--source-family",
                "reddit",
                "--source-locator",
                "https://www.reddit.com/r/test/comments/x/",
                "--decision-question",
                "q",
                "--input-file",
                str(source),
                "--data-root",
                str(lake),
                "--cutoff-posture",
                "before_decision",
            ]
        )

    assert exc_info.value.code == 2
    assert (
        "cutoff posture must be one of: mixed, post_cutoff, pre_cutoff, unknown"
        in capsys.readouterr().err
    )
    assert not lake.exists()


def test_cli_help_lists_allowed_cutoff_postures() -> None:
    help_text = " ".join(_build_parser().format_help().split())

    assert "Known cutoff posture; one of: mixed, post_cutoff, pre_cutoff, unknown" in help_text


def test_cli_uses_forseti_env_when_output_omitted(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    resolve_calls: list[object] = []

    def resolve_stub(cls: type[DataLakeRoot], *, explicit: object = None, **_: object) -> DataLakeRoot:
        resolve_calls.append(explicit)
        return root

    monkeypatch.setattr(DataLakeRoot, "resolve", classmethod(resolve_stub))
    monkeypatch.setenv(FORSETI_DATA_ROOT_ENV, str(root.path))
    src = tmp_path / "a.json"
    src.write_text("{}", encoding="utf-8")

    assert main(
        [
            "--source-family",
            "reddit",
            "--source-locator",
            "https://www.reddit.com/r/test/comments/x/",
            "--decision-question",
            "q",
            "--input-file",
            str(src),
        ]
    ) == 0

    out_path = Path(capsys.readouterr().out.strip())
    pid = out_path.name
    assert resolve_calls == [None]
    assert out_path == root.path / "raw" / raw_shard(pid) / pid
    assert root.find_packet(pid) is not None


def test_cli_requires_exactly_one_target(tmp_path: Path) -> None:
    # Neither --output nor --data-root -> fail closed (exactly-one guard).
    src = tmp_path / "a.json"
    src.write_text("{}", encoding="utf-8")
    with pytest.raises(SystemExit):
        main(
            [
                "--source-family",
                "reddit",
                "--source-locator",
                "https://www.reddit.com/r/test/comments/x/",
                "--decision-question",
                "q",
                "--input-file",
                str(src),
            ]
        )
