"""gather() child-call coverage for session_context_capsule.py (PR #611 residual).

The cross-vendor review of PR #611 (docs/review-outputs/
session_start_hook_latency_adversarial_code_review_v0.md, Residual Risks) noted
that gather()'s child-call orchestration is not unit-covered: --selftest only
exercises pure helpers, and a child failure collapsing to "" renders as
"0 modified, 0 untracked" (pre-existing fail-open). These tests pin the
contract at the gather() boundary, deliberately agnostic to whether the eight
child calls (six _git reads + retrieval_health_line + ontology_expansion_line)
run serially (pre-#611) or through a ThreadPoolExecutor (#611):

  (a) given fixed child outputs, gather() renders exactly the serial
      construction from the pure helpers, and dispatches each git child once;
  (b) an UNexpected child exception (outside the declared catch tuples) still
      exits 0 through the module-level fail-open handler, loud on stderr and
      with no partial capsule on stdout (real __main__ block via runpy);
  (c) per-child timeouts render the documented fail-open sentinels: branch
      UNKNOWN, tree 0/0, config-surface clean, doctrine "matches" (the
      empty-on-error default documented in gather()), health lines omitted.

Child calls are monkeypatched in-process; no subprocess is spawned and no hook
behavior is changed.
"""
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

# The six git child-call arg tuples gather() dispatches (the config-surface
# status tuple is derived from the module's CONFIG_SURFACE inside the test).
BRANCH_ARGS = ("rev-parse", "--abbrev-ref", "HEAD")
HEAD_ARGS = ("log", "-1", "--format=%h %s")
SUBJECTS_ARGS = ("log", "-3", "--format=%s")
STATUS_ARGS = ("status", "--porcelain")
DIFF_ARGS = ("diff", "--name-only", "origin/main", "--", "AGENTS.md", ".agents")

HEALTH_LINE = "retrieval health: 2 missing headers, 0 orphans"
EXPANSION_LINE = "ontology expansion: 1 type due (Observation)"


@pytest.fixture
def capsule():
    """Fresh module instance per test so monkeypatched child calls never leak."""
    spec = importlib.util.spec_from_file_location(
        "session_context_capsule_under_test", HOOK_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_gather_matches_serial_construction_from_fixed_child_outputs(
    capsule, monkeypatch
) -> None:
    root = Path("fake-root")
    cfg_args = ("status", "--porcelain", "--", *capsule.CONFIG_SURFACE)
    git_outputs = {
        BRANCH_ARGS: "feature-x\n",
        HEAD_ARGS: "abc1234 fix: capsule thing\n",
        SUBJECTS_ARGS: "s1\ns2\ns3\n",
        STATUS_ARGS: " M a.md\n?? b.md\n?? c.md\n",
        cfg_args: "?? .agents/hooks/new_hook.py\n",
        DIFF_ARGS: "AGENTS.md\n.agents/workflow-overlay/source-of-truth.md\n",
    }
    calls: list[tuple[str, ...]] = []

    def fake_git(git_root: Path, *args: str) -> str:
        assert git_root == root
        calls.append(args)
        return git_outputs[args]  # unknown dispatch fails loud (KeyError)

    monkeypatch.setattr(capsule, "_git", fake_git)
    monkeypatch.setattr(capsule, "retrieval_health_line", lambda r: HEALTH_LINE)
    monkeypatch.setattr(capsule, "ontology_expansion_line", lambda r: EXPANSION_LINE)

    out = capsule.gather(root, "startup")

    expected = capsule.build_capsule(
        "startup", str(root),
        git_outputs[BRANCH_ARGS].strip(),
        git_outputs[HEAD_ARGS].strip(),
        [s for s in git_outputs[SUBJECTS_ARGS].splitlines() if s],
        capsule.tree_counts(git_outputs[STATUS_ARGS]),
        capsule.config_dirt(git_outputs[cfg_args]),
        doctrine=capsule.doctrine_lag_line(git_outputs[DIFF_ARGS]),
        retrieval_health=HEALTH_LINE,
        ontology_expansion=EXPANSION_LINE,
    )
    assert out == expected
    # every git child dispatched exactly once, none dropped or duplicated
    assert sorted(calls) == sorted(git_outputs)
    # spot-pin load-bearing lines so the equivalence assertion is not vacuous
    assert "branch: feature-x @ abc1234 fix: capsule thing" in out
    assert "tree: 1 modified, 2 untracked" in out
    assert ".agents/hooks/new_hook.py" in out
    assert "DIFFERS" in out
    assert HEALTH_LINE in out
    assert EXPANSION_LINE in out


def test_unexpected_child_exception_fails_open_exit_zero(monkeypatch, capsys) -> None:
    def boom(cmd, **kwargs):
        raise RuntimeError("forced unexpected child failure")

    # RuntimeError is outside every child's declared catch tuple, so it must
    # surface through gather()/main() into the module-level fail-open handler.
    monkeypatch.setattr(subprocess, "run", boom)
    monkeypatch.setattr(sys, "argv", [str(HOOK_PATH), "--hook"])
    monkeypatch.setattr(sys, "stdin", io.StringIO('{"source": "startup"}'))

    with pytest.raises(SystemExit) as excinfo:
        runpy.run_path(str(HOOK_PATH), run_name="__main__")

    assert excinfo.value.code == 0
    captured = capsys.readouterr()
    assert "internal error, allowing" in captured.err
    assert captured.out == ""  # no partial capsule masquerading as success


def test_all_child_timeouts_render_documented_failopen_sentinels(
    capsule, monkeypatch
) -> None:
    def timeout_run(cmd, **kwargs):
        raise subprocess.TimeoutExpired(cmd, kwargs.get("timeout", 5))

    monkeypatch.setattr(capsule.subprocess, "run", timeout_run)

    lines = capsule.gather(Path("fake-root"), "startup").splitlines()

    assert lines[0] == "[lane-state capsule | source=startup]"
    assert "branch: UNKNOWN @ UNKNOWN" in lines
    assert "tree: 0 modified, 0 untracked" in lines
    assert ("config-surface dirt (CLAUDE.md/AGENTS.md/.claude/.agents): clean"
            in lines)
    # "" on git error reads as an empty diff -> "matches" (documented default)
    assert "doctrine state: matches last-fetched origin/main" in lines
    assert not any(line.startswith("recent:") for line in lines)
    assert not any("retrieval health" in line for line in lines)
    assert not any("ontology expansion" in line for line in lines)
    assert not any("not on main" in line for line in lines)
    assert lines[-1].startswith("capsule is observed git state only")


def test_status_child_timeout_collapses_tree_counts_only(capsule, monkeypatch) -> None:
    def dispatch_run(cmd, **kwargs):
        if cmd[0] == "git":
            # the plain-status child has no "--" separator; the config-surface
            # status and the doctrine diff both carry one
            if "status" in cmd and "--" not in cmd:
                raise subprocess.TimeoutExpired(cmd, kwargs.get("timeout", 5))
            if "rev-parse" in cmd:
                stdout = "feature-x\n"
            elif "--format=%h %s" in cmd:
                stdout = "abc1234 fix: capsule thing\n"
            elif "--format=%s" in cmd:
                stdout = "s1\n"
            else:  # config-surface status, doctrine diff
                stdout = ""
            return subprocess.CompletedProcess(cmd, 0, stdout, "")
        child = {"header_index.py": HEALTH_LINE + "\n",
                 "check_ontology_expansion.py": EXPANSION_LINE + "\n"}
        return subprocess.CompletedProcess(cmd, 0, child[Path(cmd[1]).name], "")

    monkeypatch.setattr(capsule.subprocess, "run", dispatch_run)

    lines = capsule.gather(Path("fake-root"), "startup").splitlines()

    # the timed-out child collapses to the documented ""-> (0, 0) sentinel ...
    assert "tree: 0 modified, 0 untracked" in lines
    # ... while every sibling child still renders its real output
    assert "branch: feature-x @ abc1234 fix: capsule thing" in lines
    assert "recent: s1" in lines
    assert HEALTH_LINE in lines
    assert EXPANSION_LINE in lines
