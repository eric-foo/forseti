"""V3 reader gate: every silver/derived reader declares its sibling-selection posture.

The write-once lake multiplies derived siblings by design, and F-IGRC-001 proved a
reader can silently pick a STALE sibling when its selection is improvised. This gate
mechanizes the silver census (unit (b), 2026-07-04): every production file that walks
derived lanes must carry a declared selection posture in
``data_lake.inventory.SILVER_READER_SELECTION_POSTURES``, so a NEW reader cannot
appear without stating how it picks among siblings.

Detection honesty: ``lane_dir``-calling readers are enforced mechanically against the
same tracked-source discovery that feeds the touchpoint counter gate. Readers whose
walks are path-based or indirect (getattr) are hand-declared with
``detection: declared_free_walk`` -- mechanical free-walk detection is a NAMED
residual of this gate, not a silent claim.
"""
from __future__ import annotations

from data_lake.inventory import (
    SILVER_READER_SELECTION_POSTURES,
    lane_dir_reader_files,
    silver_reader_posture_problems,
)


def _declared(detection: str) -> set[str]:
    return {
        file_path
        for file_path, entry in SILVER_READER_SELECTION_POSTURES.items()
        if entry.get("detection") == detection
    }


def test_every_lane_dir_reader_declares_a_selection_posture() -> None:
    actual = lane_dir_reader_files()
    declared = _declared("lane_dir")

    undeclared = sorted(actual - declared)
    assert not undeclared, (
        "Production file(s) walk derived lanes via lane_dir without a declared "
        "sibling-selection posture. Every silver/derived reader must state how it "
        "selects among sibling records (V3: consumer-enumerated; the F-IGRC-001 "
        "class): add an entry to SILVER_READER_SELECTION_POSTURES in "
        "data_lake/inventory.py -- prefer binding data_lake.sibling_selection "
        "(posture selection_rule) over inventing a new walk.\n"
        f"  {undeclared}"
    )

    stale = sorted(declared - actual)
    assert not stale, (
        "SILVER_READER_SELECTION_POSTURES declares lane_dir reader(s) that no longer "
        "carry a lane_dir touchpoint. Remove or re-classify the stale declarations:\n"
        f"  {stale}"
    )


def test_declared_free_walk_readers_exist_as_tracked_files() -> None:
    from data_lake.inventory import HARNESS_ROOT

    missing = sorted(
        file_path
        for file_path in _declared("declared_free_walk")
        if not (HARNESS_ROOT / file_path).is_file()
    )
    assert not missing, (
        "declared_free_walk reader(s) do not exist on disk -- remove the stale "
        f"declarations: {missing}"
    )


def test_reader_posture_declarations_are_shape_valid() -> None:
    problems = {
        file_path: issues
        for file_path, entry in sorted(SILVER_READER_SELECTION_POSTURES.items())
        for issues in [silver_reader_posture_problems(entry)]
        if issues
    }
    assert not problems, (
        "reader posture declaration(s) with shape problems (detection must be "
        "lane_dir or declared_free_walk; posture from the closed vocabulary; "
        f"non-empty reason): {problems}"
    )
