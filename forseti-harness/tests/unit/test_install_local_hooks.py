"""Exercise the supported local-hook installer across linked worktrees."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[3]
INSTALLER = REPO_ROOT / ".github" / "scripts" / "install-local-hooks.ps1"


def _run(*args: str, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
    )


def _git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = _run("git", *args, cwd=repo)
    if check and result.returncode != 0:
        pytest.fail(f"git {' '.join(args)} failed:\n{result.stdout}\n{result.stderr}")
    return result


def _write_sentinel_hook(path: Path, marker: Path, value: str) -> None:
    marker_literal = repr(marker.as_posix())
    path.write_text(
        "#!/bin/sh\n"
        f'python -c "from pathlib import Path; '
        f"Path({marker_literal}).write_text('{value}', encoding='utf-8')"
        '"\n',
        encoding="utf-8",
    )


def test_installer_repairs_foreign_worktree_hook_binding(tmp_path: Path) -> None:
    pwsh = shutil.which("pwsh")
    if pwsh is None:
        pytest.fail("pwsh is required to exercise install-local-hooks.ps1")

    primary = tmp_path / "primary"
    linked = tmp_path / "linked"
    primary.mkdir()
    _git(primary, "init", "--initial-branch=main")
    _git(primary, "config", "user.name", "Forseti Test")
    _git(primary, "config", "user.email", "forseti-test@example.invalid")

    scripts = primary / ".github" / "scripts"
    hooks = primary / ".githooks"
    scripts.mkdir(parents=True)
    hooks.mkdir()
    shutil.copy2(INSTALLER, scripts / INSTALLER.name)
    (hooks / "pre-push").write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    (hooks / "commit-msg").write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    _git(primary, "add", ".")
    _git(primary, "commit", "-m", "test fixture")
    _git(primary, "config", "extensions.worktreeConfig", "true")
    _git(primary, "worktree", "add", "-b", "linked", str(linked), "HEAD")

    primary_marker = tmp_path / "primary-hook-ran"
    linked_marker = tmp_path / "linked-hook-ran"
    _write_sentinel_hook(primary / ".githooks" / "commit-msg", primary_marker, "primary")
    _write_sentinel_hook(linked / ".githooks" / "commit-msg", linked_marker, "linked")
    _git(linked, "config", "--worktree", "core.hooksPath", str(primary / ".githooks"))

    verify_mismatch = _run(
        pwsh,
        "-NoProfile",
        "-File",
        str(linked / ".github" / "scripts" / INSTALLER.name),
        "-VerifyOnly",
        cwd=linked,
    )
    mismatch_output = verify_mismatch.stdout + verify_mismatch.stderr
    assert verify_mismatch.returncode == 1
    assert str(primary / ".githooks") in mismatch_output
    assert str(linked / ".githooks") in mismatch_output
    assert not primary_marker.exists()
    assert not linked_marker.exists()

    install = _run(
        pwsh,
        "-NoProfile",
        "-File",
        str(linked / ".github" / "scripts" / INSTALLER.name),
        cwd=linked,
    )
    assert install.returncode == 0, install.stdout + install.stderr
    assert "Configuration scope: --worktree" in install.stdout
    assert not primary_marker.exists()
    assert not linked_marker.exists()

    configured = _git(linked, "config", "--worktree", "--get", "core.hooksPath")
    assert configured.stdout.strip() == ".githooks"

    verify_correct = _run(
        pwsh,
        "-NoProfile",
        "-File",
        str(linked / ".github" / "scripts" / INSTALLER.name),
        "-VerifyOnly",
        cwd=linked,
    )
    assert verify_correct.returncode == 0, verify_correct.stdout + verify_correct.stderr

    lifecycle = _git(linked, "commit", "--allow-empty", "-m", "exercise linked hook")
    assert lifecycle.returncode == 0
    assert linked_marker.read_text(encoding="utf-8") == "linked"
    assert not primary_marker.exists(), "foreign worktree adapter executed"
