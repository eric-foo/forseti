"""Coverage gate: the seam cadence drives every seam consumer or names why not.

The cadence runner (``runners/run_seam_cadence.py``) is the executable
completion signal for bronze consumption — so its coverage must be pinned, not
assumed. This gate ties its declared surface to the DISCOVERED seam-consumer
surface (the same import-scan predicate as
``test_catchup_runner_seam_coverage.py``): a new runner that starts consuming
``data_lake.consumption`` fails here until it is classified INTO the cadence
(``CADENCE_ENTRYPOINTS``) or OUT of it with a recorded reason
(``CLASSIFIED_OUT_SEAM_CONSUMERS``, census authority:
``docs/decisions/bronze_consumer_census_closure_record_v0.md``). A silent
coverage gap in the completion signal is exactly the class of fake success the
census closure exists to prevent.
"""
from __future__ import annotations

import ast

from data_lake.inventory import RUNNERS_DIR as _RUNNERS_DIR
from runners.run_seam_cadence import CADENCE_ENTRYPOINTS, CLASSIFIED_OUT_SEAM_CONSUMERS

_CADENCE_RUNNERS = frozenset(entrypoint.runner for entrypoint in CADENCE_ENTRYPOINTS)


def _discovered_seam_consumers() -> set[str]:
    """Runner files importing data_lake.consumption — the same discovery
    predicate the consumer seam-coverage gate uses."""
    discovered: set[str] = set()
    for path in sorted(_RUNNERS_DIR.glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module == "data_lake.consumption":
                discovered.add(path.name)
                break
            if isinstance(node, ast.Import) and any(
                alias.name == "data_lake.consumption" for alias in node.names
            ):
                discovered.add(path.name)
                break
            if isinstance(node, ast.ImportFrom) and node.module == "data_lake":
                if any(alias.name == "consumption" for alias in node.names):
                    discovered.add(path.name)
                    break
    return discovered


def test_cadence_registry_and_classify_outs_are_disjoint() -> None:
    overlap = _CADENCE_RUNNERS & set(CLASSIFIED_OUT_SEAM_CONSUMERS)
    assert not overlap, (
        "A runner cannot be both a cadence entrypoint and classified out of the "
        f"cadence: {sorted(overlap)}"
    )


def test_cadence_plus_classify_outs_exactly_cover_seam_consumers() -> None:
    discovered = _discovered_seam_consumers()
    covered = _CADENCE_RUNNERS | set(CLASSIFIED_OUT_SEAM_CONSUMERS)

    unclassified = discovered - covered
    assert not unclassified, (
        "Seam-consumer runner(s) are neither cadence entrypoints nor classified "
        "out. The cadence is the executable bronze completion signal — classify "
        "each into CADENCE_ENTRYPOINTS or CLASSIFIED_OUT_SEAM_CONSUMERS (with the "
        f"census reason) in runners/run_seam_cadence.py: {sorted(unclassified)}"
    )

    stale = covered - discovered
    assert not stale, (
        "run_seam_cadence.py declares runner(s) that no longer consume the seam; "
        f"remove the stale declarations: {sorted(stale)}"
    )


def test_classify_out_reasons_are_recorded() -> None:
    missing = {
        name
        for name, reason in CLASSIFIED_OUT_SEAM_CONSUMERS.items()
        if not str(reason or "").strip()
    }
    assert not missing, (
        "Classified-out seam consumers must carry a non-empty census reason: "
        f"{sorted(missing)}"
    )


def test_cadence_runner_is_not_itself_a_seam_consumer() -> None:
    # The orchestrator composes runner entrypoints; consuming the seam directly
    # would put it inside the surface it is supposed to audit.
    assert "run_seam_cadence.py" not in _discovered_seam_consumers()
