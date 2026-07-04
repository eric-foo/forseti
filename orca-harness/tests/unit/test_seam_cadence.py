"""Offline behavioral tests for the seam cadence runner (executable completion signal).

No network, no credentials, no ASR compute. Commits real packets into a temp
lake and asserts the cadence contract: cycle 1 drains the backlog, cycle 2 must
emit nothing, the final pending sweep must be zero (exit 0 = the bronze
completion signal), failures re-surface and fail the exit code, a skipped ASR
lane stays loud every cycle, and one broken entrypoint never silently aborts the
rest.
"""
from __future__ import annotations

import dataclasses
import hashlib
import json
from pathlib import Path

import pytest

from data_lake.root import DataLakeRoot
from runners import run_asr_transcript_catchup as asr_runner
from runners import run_seam_cadence as cadence
from runners.run_seam_cadence import CadenceContext, main, run_cadence, run_check
from source_capture.models import known_fact
from source_capture.writer import write_local_source_capture_packet


def _commit_packet(data_root, tmp_path: Path, name: str = "thread") -> str:
    src = tmp_path / f"{name}.json"
    src.write_text(json.dumps({"body": f"a reddit thread: {name}"}), encoding="utf-8")
    return write_local_source_capture_packet(
        data_root=data_root,
        input_files=[src],
        source_family="reddit",
        source_surface="r/test",
        source_locator=known_fact(f"https://www.reddit.com/r/test/comments/{name}/"),
        decision_question="q",
        capture_context="seam cadence test",
    ).packet.packet_id


def _ctx(data_root) -> CadenceContext:
    return CadenceContext(
        data_root=data_root,
        transcriber_policy=asr_runner.default_transcriber_policy(
            model_name="small", compute_type="int8"
        ),
        asr_model="small",
        asr_compute_type="int8",
    )


def _lake_tree_state(data_root) -> dict[str, str]:
    return {
        str(p.relative_to(data_root.path)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(data_root.path.rglob("*"))
        if p.is_file()
    }


def _corrupt_manifest(data_root, packet_id: str) -> None:
    container = data_root.find_packet(packet_id)
    assert container is not None
    (container / "manifest.json").write_text("{not-json\n", encoding="utf-8")


def _output_lines(capsys) -> list[dict]:
    return [json.loads(line) for line in capsys.readouterr().out.strip().splitlines()]


def test_backlog_drains_in_cycle_one_and_second_cycle_is_zero(tmp_path, capsys) -> None:
    # The completion signal: cycle 1 may work; cycle 2 must emit nothing beyond
    # the sanctioned skip markers -> exit 0.
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    pid = _commit_packet(data_root, tmp_path)

    assert run_cadence(_ctx(data_root), skip_asr=True) == 0
    lines = _output_lines(capsys)

    cycle1_work = [
        l for l in lines if l["cycle"] == 1 and l.get("status") != "skipped_asr_compute"
    ]
    assert [(l["entrypoint"], l["packet_id"], l["status"]) for l in cycle1_work] == [
        ("run_ecr_catchup.py", pid, "derived")
    ]

    cycle2 = [l for l in lines if l["cycle"] == 2]
    assert all(l["status"] == "skipped_asr_compute" for l in cycle2)

    # A skipped lane stays loud EVERY cycle, carrying its pending count.
    markers = [l for l in lines if l.get("status") == "skipped_asr_compute"]
    assert [(l["cycle"], l["entrypoint"], l["pending"]) for l in markers] == [
        (1, "run_asr_transcript_catchup.py", 0),
        (2, "run_asr_transcript_catchup.py", 0),
    ]

    # A caught-up lake keeps passing byte-unchanged (idempotent signal).
    before = _lake_tree_state(data_root)
    assert run_cadence(_ctx(data_root), skip_asr=True) == 0
    assert _lake_tree_state(data_root) == before


def test_undrainable_work_fails_the_signal(tmp_path, capsys) -> None:
    # A corrupt manifest surfaces as availability_reconcile_failed every cycle;
    # cycle 2 is nonempty -> the completion signal must fail.
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    pid = _commit_packet(data_root, tmp_path)
    _corrupt_manifest(data_root, pid)

    assert run_cadence(_ctx(data_root), skip_asr=True) == 1
    cycle2 = [
        l
        for l in _output_lines(capsys)
        if l["cycle"] == 2 and l.get("status") != "skipped_asr_compute"
    ]
    assert cycle2
    # The driven lanes surface the corrupt packet per-packet; the skipped ASR
    # lane's compute-free pending check also fails loud on the same reconcile
    # fault (a skipped lane never becomes silently uncheckable).
    assert {l["status"] for l in cycle2} == {
        "availability_reconcile_failed",
        "skipped_asr_pending_check_failed",
    }


def test_check_reports_per_entrypoint_backlog(tmp_path, capsys) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _commit_packet(data_root, tmp_path)

    assert run_check(_ctx(data_root)) == 1
    by_entrypoint = {l["entrypoint"]: l["pending"] for l in _output_lines(capsys)}
    assert len(by_entrypoint) == len(cadence.CADENCE_ENTRYPOINTS)
    assert by_entrypoint["run_ecr_catchup.py"] == 1
    assert all(
        count == 0
        for name, count in by_entrypoint.items()
        if name != "run_ecr_catchup.py"
    )

    assert run_cadence(_ctx(data_root), skip_asr=True) == 0
    capsys.readouterr()
    assert run_check(_ctx(data_root)) == 0
    assert all(l["pending"] == 0 for l in _output_lines(capsys))


def test_one_broken_entrypoint_is_loud_and_never_aborts_the_rest(
    tmp_path, capsys, monkeypatch
) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")

    def _boom(_ctx) -> list:
        raise RuntimeError("entrypoint exploded")

    patched = tuple(
        dataclasses.replace(e, run=_boom) if e.runner == "run_ecr_catchup.py" else e
        for e in cadence.CADENCE_ENTRYPOINTS
    )
    monkeypatch.setattr(cadence, "CADENCE_ENTRYPOINTS", patched)

    assert run_cadence(_ctx(data_root), skip_asr=True) == 1
    lines = _output_lines(capsys)
    failures = [l for l in lines if l.get("status") == "entrypoint_failed"]
    assert [(l["cycle"], l["entrypoint"]) for l in failures] == [
        (1, "run_ecr_catchup.py"),
        (2, "run_ecr_catchup.py"),
    ]
    assert "RuntimeError" in failures[0]["error"]
    # The loop continued past the broken entrypoint: the ASR skip marker (last
    # in the registry) still printed in both cycles.
    assert [l["cycle"] for l in lines if l.get("status") == "skipped_asr_compute"] == [1, 2]


def test_skip_asr_visible_backlog_fails_completion_signal(
    tmp_path, capsys, monkeypatch
) -> None:
    # A skipped ASR lane stays compute-free and visible, but pending ASR work is
    # still remaining work, so it cannot produce an exit-0 completion signal.
    data_root = DataLakeRoot.for_test(tmp_path / "lake")

    patched = tuple(
        dataclasses.replace(e, pending=lambda _ctx: 3) if e.needs_asr_compute else e
        for e in cadence.CADENCE_ENTRYPOINTS
    )
    monkeypatch.setattr(cadence, "CADENCE_ENTRYPOINTS", patched)

    assert run_cadence(_ctx(data_root), skip_asr=True) == 1
    lines = _output_lines(capsys)
    markers = [l for l in lines if l.get("status") == "skipped_asr_compute"]
    assert [(l["cycle"], l["pending"]) for l in markers] == [(1, 3), (2, 3)]
    assert [
        (l["cycle"], l["entrypoint"], l["pending"])
        for l in lines
        if l.get("status") == "post_cycle_pending"
    ] == [("post", "run_asr_transcript_catchup.py", 3)]


def test_post_cycle_pending_sweep_catches_empty_result_fake_pass(
    tmp_path, capsys, monkeypatch
) -> None:
    # Even if a composed runner incorrectly emits no status, the cadence cannot
    # exit 0 while that runner's pending surface still reports backlog.
    data_root = DataLakeRoot.for_test(tmp_path / "lake")

    patched = tuple(
        dataclasses.replace(e, pending=lambda _ctx: 1, run=lambda _ctx: [])
        if e.runner == "run_ecr_catchup.py"
        else e
        for e in cadence.CADENCE_ENTRYPOINTS
    )
    monkeypatch.setattr(cadence, "CADENCE_ENTRYPOINTS", patched)

    assert run_cadence(_ctx(data_root), skip_asr=True) == 1
    assert [
        (l["cycle"], l["entrypoint"], l["pending"])
        for l in _output_lines(capsys)
        if l.get("status") == "post_cycle_pending"
    ] == [("post", "run_ecr_catchup.py", 1)]


def test_failed_skip_pending_check_fails_the_signal(tmp_path, capsys, monkeypatch) -> None:
    # Skipping execution never skips checkability: if the skipped lane's
    # pending check cannot even run, the no-work claim is invalid.
    data_root = DataLakeRoot.for_test(tmp_path / "lake")

    def _boom(_ctx) -> int:
        raise RuntimeError("pending check exploded")

    patched = tuple(
        dataclasses.replace(e, pending=_boom) if e.needs_asr_compute else e
        for e in cadence.CADENCE_ENTRYPOINTS
    )
    monkeypatch.setattr(cadence, "CADENCE_ENTRYPOINTS", patched)

    assert run_cadence(_ctx(data_root), skip_asr=True) == 1
    failures = [
        l
        for l in _output_lines(capsys)
        if l.get("status") == "skipped_asr_pending_check_failed"
    ]
    assert [l["cycle"] for l in failures] == [1, 2]


def test_cli_check_run_check_roundtrip(tmp_path, monkeypatch, capsys) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _commit_packet(data_root, tmp_path)

    def fake_resolve(cls, *, explicit=None, **_kwargs):  # noqa: ANN001
        assert explicit is None
        return data_root

    monkeypatch.setattr(DataLakeRoot, "resolve", classmethod(fake_resolve))

    assert main(["--check"]) == 1
    capsys.readouterr()
    assert main(["--run", "--skip-asr"]) == 0
    capsys.readouterr()
    assert main(["--check"]) == 0
    capsys.readouterr()


def test_cli_usage_errors(tmp_path) -> None:
    with pytest.raises(SystemExit) as excinfo:
        main([])
    assert excinfo.value.code == 2

    with pytest.raises(SystemExit) as excinfo:
        main(["--check", "--run"])
    assert excinfo.value.code == 2

    with pytest.raises(SystemExit) as excinfo:
        main(["--check", "--skip-asr"])
    assert excinfo.value.code == 2
