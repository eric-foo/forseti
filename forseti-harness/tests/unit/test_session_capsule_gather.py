"""Honesty and single-child coverage for the lean SessionStart capsule."""
from __future__ import annotations

import importlib.util
import io
import runpy
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
HOOK_PATH = REPO_ROOT / ".agents" / "hooks" / "session_context_capsule.py"


@pytest.fixture
def capsule():
    spec = importlib.util.spec_from_file_location(
        "session_context_capsule_under_test", HOOK_PATH
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_gather_uses_one_status_child_and_emits_only_bound_fields(
    capsule, monkeypatch
) -> None:
    calls = []
    output = "\n".join(
        (
            "# branch.oid 0123456789abcdef",
            "# branch.head feature-x",
            "1 .M N... 100644 100644 100644 abc def tracked.md",
            "2 R. N... 100644 100644 100644 abc def R100 renamed.md\told.md",
            "? new.md",
            "? second.md",
        )
    )

    def fake_run(command, **kwargs):
        calls.append((command, kwargs))
        return subprocess.CompletedProcess(command, 0, output, "")

    monkeypatch.setattr(capsule.subprocess, "run", fake_run)
    root = Path("fake-root")

    assert capsule.gather(root).splitlines() == [
        "repo: fake-root",
        "branch: feature-x",
        "tree: 2 modified, 2 untracked",
    ]
    assert len(calls) == 1
    command, kwargs = calls[0]
    assert command == [
        "git",
        "--no-optional-locks",
        "-C",
        "fake-root",
        "status",
        "--porcelain=v2",
        "--branch",
    ]
    assert kwargs["timeout"] == 2
    assert kwargs["capture_output"] is True
    assert kwargs["text"] is True


@pytest.mark.parametrize("failure", ["timeout", "nonzero"])
def test_git_failure_is_unknown_never_false_clean(
    capsule, monkeypatch, failure
) -> None:
    def failed_run(command, **kwargs):
        if failure == "timeout":
            raise subprocess.TimeoutExpired(command, kwargs["timeout"])
        return subprocess.CompletedProcess(command, 7, "", "git failed")

    monkeypatch.setattr(capsule.subprocess, "run", failed_run)
    output = capsule.gather(Path("fake-root"))

    assert output.splitlines() == [
        "repo: fake-root",
        "branch: UNKNOWN",
        "tree: UNKNOWN",
    ]
    assert "0 modified" not in output
    assert "clean" not in output.lower()
    assert "matches main" not in output.lower()


def test_unexpected_child_exception_fails_open_without_partial_capsule(
    monkeypatch, capsys
) -> None:
    def boom(command, **kwargs):
        raise RuntimeError("forced unexpected child failure")

    monkeypatch.setattr(subprocess, "run", boom)
    monkeypatch.setattr(sys, "argv", [str(HOOK_PATH), "--hook"])
    monkeypatch.setattr(sys, "stdin", io.StringIO('{"source": "startup"}'))

    with pytest.raises(SystemExit) as excinfo:
        runpy.run_path(str(HOOK_PATH), run_name="__main__")

    assert excinfo.value.code == 0
    captured = capsys.readouterr()
    assert "internal error, allowing" in captured.err
    assert captured.out == ""


def test_detached_head_is_explicit(capsule) -> None:
    branch, modified, untracked = capsule.parse_status(
        "# branch.head (detached)\n? new.md\n"
    )
    assert (branch, modified, untracked) == ("DETACHED", 0, 1)
