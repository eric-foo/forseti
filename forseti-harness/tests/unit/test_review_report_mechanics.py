from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys

import pytest


REPO_ROOT = Path(__file__).resolve().parents[3]
RUNNER = REPO_ROOT / ".github" / "scripts" / "review-report-mechanics.py"
TOKEN = b"{{REVIEW_MECHANICS_UNIFIED_DIFF}}"


def _git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        check=True,
        capture_output=True,
        text=True,
    )


def _draft_bytes(token: bytes = TOKEN) -> bytes:
    lines = [
        b"# Mechanical report",
        b"",
        b"```yaml",
        b"retrieval_header_version: 1",
        b"artifact_role: Adversarial review output",
        b"scope: Mechanical report fixture.",
        b"use_when:",
        b"  - Testing report assembly.",
        b"authority_boundary: retrieval_only",
        b"```",
        b"",
        b"reviewed_by: fixture-reviewer",
        b"authored_by: fixture-author",
        b"review_use_boundary: >",
        b"  Findings are decision input only, not approval, validation, mandatory remediation, or patch authority.",
        b"",
        b"Prose before the generated block.",
        b"",
        b"```diff",
        token,
        b"```",
        b"",
        b"Prose after the generated block.",
        b"",
    ]
    return b"\r\n".join(lines)


def _init_repo(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    root.mkdir()
    _git(root, "init", "--quiet")
    _git(root, "config", "user.email", "fixture@example.test")
    _git(root, "config", "user.name", "Fixture")
    _git(root, "config", "core.autocrlf", "false")

    hooks = root / ".agents" / "hooks"
    hooks.mkdir(parents=True)
    for name in (
        "check_review_output_provenance.py",
        "check_review_summary.py",
        "check_retrieval_header.py",
        "_hooklib.py",  # shared helper sibling; hooks are ported as a directory
    ):
        shutil.copy2(REPO_ROOT / ".agents" / "hooks" / name, hooks / name)

    source = root / "src" / "example.txt"
    source.parent.mkdir()
    source.write_bytes(b"old\n")
    (root / "docs" / "review-outputs").mkdir(parents=True)
    (root / "drafts").mkdir()
    _git(root, "add", ".")
    _git(root, "commit", "--quiet", "-m", "fixture baseline")
    source.write_bytes(b"new\n")
    return root


def _write_draft(root: Path, data: bytes | None = None) -> Path:
    path = root / "drafts" / "report.md"
    path.write_bytes(_draft_bytes() if data is None else data)
    return path


def _run(root: Path, mode: str, *extra: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(RUNNER),
            mode,
            "--worktree",
            str(root),
            *extra,
        ],
        check=False,
        capture_output=True,
        text=True,
    )


def _assemble(root: Path, *extra: str) -> subprocess.CompletedProcess[str]:
    _write_draft(root)
    return _run(
        root,
        "assemble",
        "--draft",
        "drafts/report.md",
        "--report",
        "docs/review-outputs/report.md",
        "--patch",
        "src/example.txt",
        *extra,
    )


def _receipt(result: subprocess.CompletedProcess[str]) -> dict[str, object]:
    lines = [line for line in result.stdout.splitlines() if line.strip()]
    assert len(lines) == 1, result.stdout
    return json.loads(lines[0])


def _load_runner_module():
    spec = importlib.util.spec_from_file_location("review_report_mechanics_test_module", RUNNER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_assemble_preserves_all_draft_bytes_outside_unique_token(tmp_path: Path) -> None:
    root = _init_repo(tmp_path)
    draft = _draft_bytes()
    _write_draft(root, draft)
    result = _run(
        root,
        "assemble",
        "--draft",
        "drafts/report.md",
        "--report",
        "docs/review-outputs/report.md",
        "--patch",
        "src/example.txt",
    )

    assert result.returncode == 0, result.stderr
    report = (root / "docs" / "review-outputs" / "report.md").read_bytes()
    before, after = draft.split(TOKEN)
    assert report.startswith(before)
    assert report.endswith(after)
    assert b"diff --git a/src/example.txt b/src/example.txt" in report
    assert _receipt(result)["status"] == "GATE PASS"


@pytest.mark.parametrize("token_count", [0, 2])
def test_assemble_requires_exactly_one_token(tmp_path: Path, token_count: int) -> None:
    root = _init_repo(tmp_path)
    data = _draft_bytes(b"no token") if token_count == 0 else _draft_bytes(TOKEN + b"\r\n" + TOKEN)
    _write_draft(root, data)
    result = _run(
        root,
        "assemble",
        "--draft",
        "drafts/report.md",
        "--report",
        "docs/review-outputs/report.md",
        "--patch",
        "src/example.txt",
    )

    assert result.returncode != 0
    assert _receipt(result)["status"] == "GATE FAIL"
    assert not (root / "docs" / "review-outputs" / "report.md").exists()


def test_assemble_includes_explicit_tracked_and_untracked_paths(tmp_path: Path) -> None:
    root = _init_repo(tmp_path)
    _write_draft(root)
    (root / "src" / "untracked.txt").write_bytes(b"untracked\n")
    result = _run(
        root,
        "assemble",
        "--draft",
        "drafts/report.md",
        "--report",
        "docs/review-outputs/report.md",
        "--patch",
        "src/example.txt",
        "--patch",
        "src/untracked.txt",
    )

    assert result.returncode == 0, result.stderr
    report = (root / "docs" / "review-outputs" / "report.md").read_text(encoding="utf-8")
    assert "diff --git a/src/example.txt b/src/example.txt" in report
    assert "diff --git a/src/untracked.txt b/src/untracked.txt" in report
    receipt = _receipt(result)
    assert set(receipt["hashes"]["patches"]) == {"src/example.txt", "src/untracked.txt"}


def test_empty_aggregate_diff_fails_without_writing_report(tmp_path: Path) -> None:
    root = _init_repo(tmp_path)
    (root / "src" / "example.txt").write_bytes(b"old\n")
    result = _assemble(root)

    assert result.returncode != 0
    assert _receipt(result)["status"] == "GATE FAIL"
    assert not (root / "docs" / "review-outputs" / "report.md").exists()


def test_paths_outside_worktree_are_rejected(tmp_path: Path) -> None:
    root = _init_repo(tmp_path)
    _write_draft(root)
    outside = tmp_path / "outside.txt"
    outside.write_bytes(b"outside\n")
    result = _run(
        root,
        "assemble",
        "--draft",
        "drafts/report.md",
        "--report",
        "docs/review-outputs/report.md",
        "--patch",
        str(outside),
    )

    assert result.returncode != 0
    assert _receipt(result)["status"] == "GATE FAIL"


def test_report_must_stay_under_review_outputs(tmp_path: Path) -> None:
    root = _init_repo(tmp_path)
    _write_draft(root)
    result = _run(
        root,
        "assemble",
        "--draft",
        "drafts/report.md",
        "--report",
        "drafts/final.md",
        "--patch",
        "src/example.txt",
    )

    assert result.returncode != 0
    assert _receipt(result)["status"] == "GATE FAIL"


def test_tracked_diff_check_failure_stops_before_write(tmp_path: Path) -> None:
    root = _init_repo(tmp_path)
    (root / "src" / "example.txt").write_bytes(b"new with trailing space \n")
    result = _assemble(root)

    assert result.returncode != 0
    assert _receipt(result)["status"] == "GATE FAIL"
    assert not (root / "docs" / "review-outputs" / "report.md").exists()


def test_checker_failure_is_nonzero_and_written_report_remains_visible(tmp_path: Path) -> None:
    root = _init_repo(tmp_path)
    (root / ".agents" / "hooks" / "check_review_output_provenance.py").write_text(
        "raise RuntimeError('fixture checker failure')\n", encoding="utf-8"
    )
    result = _assemble(root)

    assert result.returncode != 0
    assert _receipt(result)["status"] == "GATE FAIL"
    assert (root / "docs" / "review-outputs" / "report.md").exists()


def test_checker_missing_expected_callable_is_nonzero(tmp_path: Path) -> None:
    """Checker interface drift at call-time (module imports fine but lacks the
    expected callable), distinct from the import-time failure covered above."""
    root = _init_repo(tmp_path)
    (root / ".agents" / "hooks" / "check_review_summary.py").write_text(
        "# drifted checker interface: no scan_files() left to call\n", encoding="utf-8"
    )
    result = _assemble(root)

    assert result.returncode != 0
    assert _receipt(result)["status"] == "GATE FAIL"
    assert (root / "docs" / "review-outputs" / "report.md").exists()


def test_report_named_readme_is_rejected(tmp_path: Path) -> None:
    """docs/review-outputs/README.md is excluded from both downstream checkers'
    scope (check_review_output_provenance.py / check_review_summary.py), so
    accepting that basename would let a report bypass provenance/summary
    scanning while still reporting GATE PASS."""
    root = _init_repo(tmp_path)
    _write_draft(root)
    result = _run(
        root,
        "assemble",
        "--draft",
        "drafts/report.md",
        "--report",
        "docs/review-outputs/README.md",
        "--patch",
        "src/example.txt",
    )

    assert result.returncode != 0
    assert _receipt(result)["status"] == "GATE FAIL"
    assert not (root / "docs" / "review-outputs" / "README.md").exists()


def test_readback_mismatch_predicate_fails_closed() -> None:
    module = _load_runner_module()
    assert module.verify_assembled_bytes(b"actual", b"expected") is False
    assert module.verify_diff_occurrence(b"prefix-diff-suffix-diff", b"diff") is False


def test_receipt_has_no_review_domain_outputs(tmp_path: Path) -> None:
    root = _init_repo(tmp_path)
    result = _assemble(root)
    assert result.returncode == 0, result.stderr
    serialized = json.dumps(_receipt(result), sort_keys=True).lower()
    for forbidden in (
        "vulnerability",
        "severity",
        "verdict",
        "remediation",
        "recommendation",
        "patch_content_decision",
    ):
        assert forbidden not in serialized


def test_existing_report_requires_explicit_replace(tmp_path: Path) -> None:
    root = _init_repo(tmp_path)
    result = _assemble(root)
    assert result.returncode == 0, result.stderr
    first = (root / "docs" / "review-outputs" / "report.md").read_bytes()

    blocked = _assemble(root)
    assert blocked.returncode != 0
    assert (root / "docs" / "review-outputs" / "report.md").read_bytes() == first

    replaced = _assemble(root, "--replace")
    assert replaced.returncode == 0, replaced.stderr


def test_verify_is_read_only_and_rechecks_exact_diff(tmp_path: Path) -> None:
    root = _init_repo(tmp_path)
    assembled = _assemble(root)
    assert assembled.returncode == 0, assembled.stderr
    report = root / "docs" / "review-outputs" / "report.md"
    before = report.read_bytes()

    verified = _run(
        root,
        "verify",
        "--report",
        "docs/review-outputs/report.md",
        "--patch",
        "src/example.txt",
    )

    assert verified.returncode == 0, verified.stderr
    assert report.read_bytes() == before
    assert _receipt(verified)["mode"] == "verify"

    gate_names = {gate["name"] for gate in _receipt(verified)["gates"]}
    assert "readback_exact_not_applicable" in gate_names
    assert "readback_exact" not in gate_names, (
        "verify mode never runs the assembled-bytes comparison readback_exact "
        "checks; recording that gate name as GATE PASS would claim a "
        "comparison that never happened"
    )
