"""V3 reader gate: every silver/derived reader declares its sibling-selection posture.

The write-once lake multiplies derived siblings by design, and F-IGRC-001 proved a
reader can silently pick a STALE sibling when its selection is improvised. This gate
mechanizes the silver census (unit (b), 2026-07-04): every production file that walks
derived lanes must carry a declared selection posture in
``data_lake.inventory.SILVER_READER_SELECTION_POSTURES``, so a NEW reader cannot
appear without stating how it picks among siblings.

Detection honesty: ``lane_dir``-calling readers and direct derived-root traversal are
enforced mechanically against tracked production source. Narrow indirect (getattr)
and record-path readers remain classified by the explicit path-based census below.
"""
from __future__ import annotations

import ast
from functools import cache

from data_lake.inventory import (
    HARNESS_ROOT,
    SILVER_READER_SELECTION_POSTURES,
    derived_root_traversal_files,
    lane_dir_reader_files,
    non_raw_lake_touchpoints,
    silver_reader_posture_problems,
    tracked_harness_python_files,
)

# Session-scoped memo: the full-repo AST census is deterministic for the tests in
# this file (none mutate tracked source mid-run), so repeated calls may share one
# scan. A future test that edits tracked files must call .cache_clear() first.
_derived_root_traversal_files = cache(derived_root_traversal_files)

_PATH_BASED_TOUCHPOINT_CALLS = {"is_record_set_complete", "record_path"}
_PATH_BASED_TOUCHPOINT_EXCLUSIONS = {
    "capture_spine/creator_profile_current/tiktok_comment_attention_producer.py": (
        "producer checks its own deterministic current-policy record id for "
        "idempotency/collision; it does not select among sibling records"
    ),
    "capture_spine/creator_profile_current/tiktok_grid_observation_producer.py": (
        "producer checks its own deterministic exact-policy observation-set record id "
        "for idempotency/collision; it does not select among sibling records"
    ),
    "runners/run_asr_transcript_catchup.py": (
        "catch-up writer checks one deterministic current-policy transcript id "
        "before acking; it does not select among sibling records"
    ),
    "runners/run_ig_reels_lane_orchestrator.py": (
        "orchestrator checks completion markers for exact downstream outputs"
    ),
    "runners/run_tiktok_product_extract.py": (
        "product-extraction writer checks one deterministic mention record id "
        "for completion or a crash-partial collision; it does not select among siblings"
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


def test_direct_derived_root_walks_are_mechanically_censused() -> None:
    detected = _derived_root_traversal_files()
    assert "capture_spine/creator_profile_current/rollup_formula_revalidation.py" in detected
    assert detected <= _declared("declared_free_walk")


def test_path_based_reader_census_is_declared_or_explicitly_excluded() -> None:
    """Unit (b)'s path-based lake touchpoint census must not become an invisible
    reader registry bypass.

    ``lane_dir`` callers are exact-matched mechanically above. Path-based walkers
    cannot be classified by the lane_dir detector, so every such touchpoint is
    either hand-declared as a reader posture or explicitly excluded with a reason.
    """
    touchpoints = non_raw_lake_touchpoints()
    lane_dir_readers = {
        file_path
        for (file_path, call_name) in touchpoints
        if call_name == "lane_dir"
    }
    path_based = {
        file_path
        for (file_path, call_name) in touchpoints
        if call_name in _PATH_BASED_TOUCHPOINT_CALLS and file_path not in lane_dir_readers
    }
    expected_declared = (
        path_based - set(_PATH_BASED_TOUCHPOINT_EXCLUSIONS)
    ) | _derived_root_traversal_files()

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
        "path-based reader census or the derived-root traversal detector:\n"
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


def test_structural_lineage_helpers_cannot_be_used_as_reader_authority() -> None:
    """Shape checks may support a writer, but may never admit read-side evidence."""
    structural_calls = {
        "has_complete_silver_lineage_structure",
        "silver_record_lineage_structure_status",
    }
    retired_misleading_calls = {
        "is_silver_record_source_backed_complete",
        "silver_record_source_backed_status",
    }
    write_front_doors = {"append_silver_record", "append_silver_record_set"}
    problems: dict[str, str] = {}
    for path in tracked_harness_python_files():
        relative = path.relative_to(HARNESS_ROOT)
        if "tests" in relative.parts or relative.as_posix() == "data_lake/silver_lineage.py":
            continue
        calls = _call_names(ast.parse(path.read_text(encoding="utf-8")))
        retired = sorted(calls & retired_misleading_calls)
        if retired:
            problems[relative.as_posix()] = f"calls retired shape-only authority API: {retired}"
            continue
        structural = sorted(calls & structural_calls)
        if structural and not calls & write_front_doors:
            problems[relative.as_posix()] = (
                f"calls structural-only lineage helper {structural} without a strict "
                "Silver write front door; authority readers must use root-aware "
                "physical verification"
            )
    assert not problems, (
        "Structural Silver lineage status escaped into read-side authority:\n"
        + "\n".join(f"  {path}: {why}" for path, why in sorted(problems.items()))
    )

def test_declared_envelope_readers_visibly_use_physical_authority() -> None:
    """Envelope validity alone must never admit evidence from a declared reader."""
    physical_calls = {
        "build_creator_metric_lineage_index",
        "classify_silver_vault_record_sources",
        "select_product_mention_records",
        "verify_silver_vault_record_sources",
    }
    problems: dict[str, str] = {}
    for file_path in sorted(SILVER_READER_SELECTION_POSTURES):
        tree = ast.parse((HARNESS_ROOT / file_path).read_text(encoding="utf-8"))
        calls = _call_names(tree)
        if "validate_silver_vault_record" in calls and not calls & physical_calls:
            problems[file_path] = (
                "validates a Silver envelope but exposes no root-aware physical "
                "classifier/verifier or a shared physically gated selector"
            )
    assert not problems, (
        "Declared Silver reader(s) can treat envelope shape as authority:\n"
        + "\n".join(f"  {path}: {why}" for path, why in problems.items())
    )

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
