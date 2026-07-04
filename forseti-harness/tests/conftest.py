from __future__ import annotations

from collections.abc import Iterator
import shutil
import sys
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


@pytest.fixture
def tmp_path() -> Iterator[Path]:
    path = PROJECT_ROOT.parent / "_scratch" / f"forseti_harness_tmp_path_{uuid.uuid4().hex}"
    path.mkdir(parents=True)
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


def _copy_ignore(_directory: str, names: list[str]) -> set[str]:
    ignored: set[str] = set()
    for name in names:
        if name in {"_test_runs", ".pytest_cache", ".pytest_tmp", "pytest_tmp", "_scratch"}:
            ignored.add(name)
        if (
            name.startswith(".pytest_")
            or name.startswith("pytest_run_")
            or name.startswith("pytest-cache-files-")
            or name.startswith("pytest_tmp")
            or (name.startswith("pytest_") and name.endswith("_tmp"))
        ):
            ignored.add(name)
    return ignored


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
def copied_project() -> Path:
    scratch_root = PROJECT_ROOT / "_test_runs"
    scratch_root.mkdir(exist_ok=True)
    destination = scratch_root / f"run_{uuid.uuid4().hex}"
    shutil.copytree(PROJECT_ROOT, destination, ignore=_copy_ignore)
    _reset_copied_outputs(destination)
    try:
        yield destination
    finally:
        shutil.rmtree(destination)


@pytest.fixture
def copied_case_dir(copied_project: Path) -> Path:
    return copied_project / "cases" / "plumbing" / CASE_ID
