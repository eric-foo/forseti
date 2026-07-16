from __future__ import annotations

from collections.abc import Iterator
import os
import shutil
import stat
import sys
import tempfile
import time
import uuid
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CASE_ID = "tr_casetext_2023_v0_14"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture(autouse=True)
def _no_ambient_data_lake(monkeypatch: pytest.MonkeyPatch) -> None:
    # Hermetic suite: no test may resolve the operator's live lake through the
    # ambient environment (FORSETI_DATA_ROOT/ORCA_DATA_ROOT env fallbacks would otherwise publish
    # into a real lake). Tests that need a lake set FORSETI_DATA_ROOT or legacy ORCA_DATA_ROOT themselves
    # against a scratch root; live-lake reconciliation is an explicit opt-in
    # via FORSETI_LIVE_LAKE_TEST_ROOT (legacy ORCA_LIVE_LAKE_TEST_ROOT
    # also accepted; archived-lake reconciliation for retired-root-bound
    # fixtures via FORSETI_ARCHIVED_LAKE_TEST_ROOT with legacy
    # ORCA_ARCHIVED_LAKE_TEST_ROOT fallback).
    monkeypatch.delenv("FORSETI_DATA_ROOT", raising=False)
    monkeypatch.delenv("ORCA_DATA_ROOT", raising=False)


def _session_temp_root() -> Path:
    configured_root = os.environ.get("FORSETI_PYTEST_TMP_ROOT")
    candidates = (
        Path(configured_root).expanduser() if configured_root else None,
        Path(tempfile.gettempdir()) / "forseti-harness-pytest",
        PROJECT_ROOT.parent / "_scratch",
    )
    worker_id = os.environ.get("PYTEST_XDIST_WORKER", "main")
    failures: list[str] = []
    for candidate in candidates:
        if candidate is None:
            continue
        session_root = candidate / f"session_{worker_id}_{uuid.uuid4().hex}"
        try:
            session_root.mkdir(parents=True)
        except OSError as exc:
            failures.append(f"{candidate}: {exc}")
            continue
        return session_root
    raise OSError("Unable to create a pytest scratch root: " + "; ".join(failures))


def _remove_readonly(func, path: str, exc: BaseException) -> None:
    if not isinstance(exc, PermissionError):
        raise exc
    os.chmod(path, stat.S_IWRITE)
    func(path)


def _remove_tree(path: Path) -> None:
    last_error: OSError | None = None
    for delay_seconds in (0.0, 0.1, 0.5, 1.5):
        if delay_seconds:
            time.sleep(delay_seconds)
        try:
            shutil.rmtree(path, onexc=_remove_readonly)
            return
        except FileNotFoundError:
            return
        except OSError as exc:
            last_error = exc
    assert last_error is not None
    raise last_error


@pytest.fixture(scope="session")
def harness_tmp_root() -> Iterator[Path]:
    path = _session_temp_root()
    try:
        yield path
    finally:
        _remove_tree(path)


@pytest.fixture
def tmp_path(harness_tmp_root: Path) -> Iterator[Path]:
    path = harness_tmp_root / f"test_{uuid.uuid4().hex}"
    path.mkdir(parents=True)
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


def _copy_project_fixture(destination: Path) -> None:
    destination.mkdir()
    for filename in ("harness_utils.py", "pyproject.toml"):
        shutil.copy2(PROJECT_ROOT / filename, destination / filename)
    for directory in ("reports", "runners", "schemas", "scoring"):
        shutil.copytree(PROJECT_ROOT / directory, destination / directory)
    shutil.copytree(
        PROJECT_ROOT / "cases" / "plumbing" / CASE_ID,
        destination / "cases" / "plumbing" / CASE_ID,
    )
    (destination / "memory" / "logs").mkdir(parents=True)


def _reset_copied_outputs(project_root: Path) -> None:
    case_dir = project_root / "cases" / "plumbing" / CASE_ID
    scores_dir = case_dir / "scores"
    if scores_dir.exists():
        shutil.rmtree(scores_dir)

    report_dir = project_root / "reports" / "plumbing" / CASE_ID
    if report_dir.exists():
        shutil.rmtree(report_dir)

    failure_log = project_root / "memory" / "logs" / "failure_events.yaml"
    if failure_log.exists():
        failure_log.unlink()


@pytest.fixture
def copied_project(harness_tmp_root: Path) -> Path:
    destination = harness_tmp_root / f"project_{uuid.uuid4().hex}"
    _copy_project_fixture(destination)
    _reset_copied_outputs(destination)
    try:
        yield destination
    finally:
        shutil.rmtree(destination, ignore_errors=True)


@pytest.fixture
def copied_case_dir(copied_project: Path) -> Path:
    return copied_project / "cases" / "plumbing" / CASE_ID
