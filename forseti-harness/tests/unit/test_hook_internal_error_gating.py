"""Internal checker bugs must not read as green gates (EP-35 FIND-02 class sweep).

Every hook wired as a CI --strict gate carries a __main__ handler that maps an
unexpected internal exception to exit 1 in gating modes (--strict / --selftest,
the GATE FAIL bucket in validation-gates.md) and to exit 0 in advisory/hook
modes so a checker bug never bricks the agent. Each hook exposes a
--force-internal-error probe flag that raises at main() entry; these tests
prove the handler's mapping in both directions, in-process-independent (real
subprocess, real exit codes). Documented infra-gap fail-opens (git/PyYAML
unavailable, base ref unresolvable) are a different contract and are not
probed here.

check_placement.py is not CI-wired but shares the same handler shape and is
covered for the same property. Hooks without a __main__ handler
(check_csb_scanning_artifact, check_ontology_tag_validity, check_ontology_drift,
check_silver_lane_registry) already propagate exceptions as nonzero exits and
need no probe.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
HOOKS_DIR = REPO_ROOT / ".agents" / "hooks"

# (hook filename, gating-mode argv lists, advisory-mode argv lists)
CASES = [
    ("check_map_links.py",
     [["--strict"], ["--strict-inline"], ["--selftest"]], [["--check"]]),
    ("header_index.py",
     [["--strict"], ["--selftest"]], [["--health"]]),
    ("check_search_surface_google_route.py",
     [["--strict"], ["--selftest"]], [["--hook"]]),
    ("check_ontology_ssot.py",
     [["--strict"], ["--selftest"]], [["--check"]]),
    ("check_fragrance_reference.py",
     [["--strict"], ["--selftest"]], [["--check"]]),
    ("check_deletion_evidence.py",
     [["--strict"], ["--selftest"]], [["--report"]]),
    ("check_dcp_receipt.py",
     [["--strict"], ["--selftest"]], [["--report"]]),
    ("check_placement.py",
     [["--strict"], ["--selftest"]], [["--hook"]]),
    ("check_handoff_pointers.py",
     [["--strict"], ["--selftest"]], [["--check"], ["--audit"]]),
    ("check_source_input_hashes.py",
     [["--strict"], ["--selftest"]], [["--check"], ["--audit"]]),
]

GATING = [(hook, mode) for hook, gating, _ in CASES for mode in gating]
ADVISORY = [(hook, mode) for hook, _, advisory in CASES for mode in advisory]


def _ids(params: list[tuple[str, list[str]]]) -> list[str]:
    return ["%s %s" % (hook, " ".join(mode)) for hook, mode in params]


def _run_probe(hook: str, mode: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(HOOKS_DIR / hook), *mode, "--force-internal-error"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )


@pytest.mark.parametrize(("hook", "mode"), GATING, ids=_ids(GATING))
def test_forced_internal_error_is_gate_fail_in_gating_mode(
    hook: str, mode: list[str]
) -> None:
    result = _run_probe(hook, mode)
    assert result.returncode == 1, result.stdout + result.stderr
    # The nonzero exit must come from the internal-error handler, not from
    # ordinary findings.
    assert "internal error" in result.stderr, result.stdout + result.stderr


@pytest.mark.parametrize(("hook", "mode"), ADVISORY, ids=_ids(ADVISORY))
def test_forced_internal_error_fails_open_in_advisory_mode(
    hook: str, mode: list[str]
) -> None:
    result = _run_probe(hook, mode)
    assert result.returncode == 0, result.stdout + result.stderr
    # The green exit must be the loud fail-open path, not a silent success.
    assert "internal error" in result.stderr, result.stdout + result.stderr
