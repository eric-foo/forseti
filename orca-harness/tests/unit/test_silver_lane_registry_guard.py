"""The silver-lane write-path guard enforces the no-blur binding.

Runs the guard's own selftest (its pass/fail fixtures), proves the live repo has
no silver-lane write violations, and pins the registry's load-bearing facts (the
envelope lanes and the named FRONT_DOOR_PENDING baseline).
"""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
HOOK = REPO_ROOT / ".agents" / "hooks" / "check_silver_lane_registry.py"
REGISTRY_PATH = REPO_ROOT / "orca-harness" / "data_lake" / "lane_registry.py"


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(HOOK), *args],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )


def _load_registry():
    spec = importlib.util.spec_from_file_location("lane_registry_under_test", REGISTRY_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_guard_selftest_passes() -> None:
    result = _run("--selftest", "--strict")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "SELFTEST OK" in result.stdout


def test_live_repo_has_no_silver_lane_write_violations() -> None:
    result = _run("--strict")
    assert result.returncode == 0, result.stdout + result.stderr


def test_registry_pins_envelope_lanes_and_pending_baseline() -> None:
    registry = _load_registry()
    assert "cleaning_fragrantica_silver" in registry.SILVER_ENVELOPE_LANES
    assert {"creator_metric_silver", "creator_metric_rollup_silver"} <= set(registry.FRONT_DOOR_PENDING)
    # The Fragrantica silver lane is already on the front-door -- it must NOT be pending.
    assert "cleaning_fragrantica_silver" not in registry.FRONT_DOOR_PENDING
    # Every pending lane is a real envelope lane (no stale baseline entries).
    assert set(registry.FRONT_DOOR_PENDING) <= set(registry.SILVER_ENVELOPE_LANES)
