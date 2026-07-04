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

import ast

from data_lake.inventory import (
    HARNESS_ROOT,
    SILVER_READER_SELECTION_POSTURES,
    lane_dir_reader_files,
    non_raw_lake_touchpoints,
    silver_reader_posture_problems,
)

_PATH_BASED_TOUCHPOINT_CALLS = {"is_record_set_complete", "record_path"}
_DECLARED_FREE_WALK_WITHOUT_TOUCHPOINT = {
    # Direct filesystem discovery of derived projection files; no DataLakeRoot
    # touchpoint appears in the unit (b) AST census.
    "capture_spine/creator_profile_current/instagram_metric_seed.py",
}
_PATH_BASED_TOUCHPOINT_EXCLUSIONS = {
    "runners/run_asr_transcript_catchup.py": (
        "catch-up writer checks one deterministic current-policy transcript id "
        "before acking; it does not select among sibling records"
    ),
    "runners/run_cleaning_spine_periodic_audit.py": (
        "audit resolves explicitly named derived_record anchors; it is not pickup "
        "authority over a sibling set"
    ),
    "runners/run_ig_reels_lane_orchestrator.py": (
        "orchestrator checks completion markers for exact downstream outputs"
    ),
    "runners/run_source_capture_ig_reels_deep_capture.py": (
        "deep-capture writer checks completion markers for exact record sets"
    ),
    "source_capture/ig_reels_grid_projection.py": (
        "projection writer checks exact bronze-catalog proof paths while appending "
        "stable derived records"
    ),
}

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


def test_path_based_reader_census_is_declared_or_explicitly_excluded() -> None:
    """Unit (b)'s path-based lake touchpoint census must not become an invisible
    reader registry bypass.

    ``lane_dir`` callers are exact-matched mechanically above. Path-based walkers
    cannot be classified by the lane_dir detector, so every such touchpoint is
    either hand-declared as a reader posture or explicitly excluded with a reason.
    """
    path_based = {
        file_path
        for (file_path, call_name) in non_raw_lake_touchpoints()
        if call_name in _PATH_BASED_TOUCHPOINT_CALLS
        and file_path not in lane_dir_reader_files()
    }
    expected_declared = (
        path_based - set(_PATH_BASED_TOUCHPOINT_EXCLUSIONS)
    ) | _DECLARED_FREE_WALK_WITHOUT_TOUCHPOINT

    undeclared = sorted(expected_declared - _declared("declared_free_walk"))
    assert not undeclared, (
        "Path-based derived-lane reader(s) are not declared in "
        "SILVER_READER_SELECTION_POSTURES as declared_free_walk. Either declare "
        "their selection posture or add a reasoned exclusion in this gate:\n"
        f"  {undeclared}"
    )

    stale = sorted(_declared("declared_free_walk") - expected_declared)
    assert not stale, (
        "declared_free_walk posture(s) are no longer backed by the unit (b) "
        "path-based reader census or the explicit filesystem-walk list:\n"
        f"  {stale}"
    )

    stale_exclusions = sorted(set(_PATH_BASED_TOUCHPOINT_EXCLUSIONS) - path_based)
    assert not stale_exclusions, (
        "Path-based reader exclusion(s) no longer appear in the unit (b) census; "
        "remove or reclassify them:\n"
        f"  {stale_exclusions}"
    )

def _call_names(tree: ast.AST) -> set[str]:
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name):
                names.add(func.id)
            elif isinstance(func, ast.Attribute):
                names.add(func.attr)
    return names


def test_selection_rule_postures_visibly_use_their_named_mechanism() -> None:
    """V2's core claim cannot rot: a file declared ``selection_rule`` must visibly
    CALL its named mechanism (``shared:`` -- it consumes the data_lake rule) or
    DEFINE it (``local:`` -- it is the declared home of an adjudicated rule its
    consumers call). Import presence alone never satisfies this (F-SH-001)."""
    problems: dict[str, str] = {}
    for file_path, entry in sorted(SILVER_READER_SELECTION_POSTURES.items()):
        if entry.get("posture") != "selection_rule":
            continue
        kind, _, callable_name = str(entry.get("mechanism", "")).partition(":")
        tree = ast.parse((HARNESS_ROOT / file_path).read_text(encoding="utf-8"))
        if kind == "shared" and callable_name not in _call_names(tree):
            problems[file_path] = (
                f"declares selection_rule via {entry.get('mechanism')!r} but never calls "
                f"{callable_name!r} -- the declared posture has rotted or the rule was dropped"
            )
        if kind == "local":
            defined = {
                node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)
            }
            if callable_name not in defined:
                problems[file_path] = (
                    f"declares selection_rule via {entry.get('mechanism')!r} but no longer "
                    f"defines {callable_name!r} -- the rule's declared home has rotted"
                )
    assert not problems, (
        "selection_rule posture(s) not backed by visible use of the named rule:\n"
        + "\n".join(f"  {path}: {why}" for path, why in problems.items())
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
