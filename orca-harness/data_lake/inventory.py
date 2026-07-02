"""Deterministic Data Lake touchpoint inventory (the A1 inventory gate core).

Single source for the AST discovery the seam-coverage contract test seeds and
for the durable, checked-in touchpoint inventory record
(``lake_touchpoint_inventory_v0.json``). The record enumerates, from tracked
source only:

1. raw-packet writers (runner seams, declared orchestrators, and the recursive
   ``source_capture`` writer-function closure);
2. non-raw lake touchpoints (derived/ack/silver/catalog call sites);
3. explicit exclusions, each carrying a reason;
4. unknowns, each carrying an owner disposition (a pending unknown fails the
   gate; dispositions are owner-attributable via the human-gated PR merge,
   never self-certified);
5. the A2 serialization-fork impact tag per entry.

The fork-impact tag is deterministic routing metadata for the deferred A2
decision (Manifest v2 vs manifest-equivalent packet index), assigned by
surface class, never per-entry judgment:

- raw-packet writers produce packet manifests -> ``manifest_shape``;
- generated catalog / Attachment Record read surfaces consume or rebuild the
  manifest-equivalent generated index -> ``packet_index``;
- derived/ack append and record-set/lane-path surfaces touch neither shape ->
  ``none``.

The checked-in record is a generated inventory of code surfaces. It is never
lake authority, never lives under the data root, and is regenerated and
diffed by ``tests/contract/test_data_lake_inventory_gate.py``; updating it is
a deliberate, reviewed edit. It does not select A2, a backend, or claim
coverage beyond source-visible discovery.
"""
from __future__ import annotations

import ast
import json
import re
import subprocess
from collections import Counter
from dataclasses import dataclass
from functools import cache
from pathlib import Path

HARNESS_ROOT = Path(__file__).resolve().parents[1]
RUNNERS_DIR = HARNESS_ROOT / "runners"
SOURCE_CAPTURE_DIR = HARNESS_ROOT / "source_capture"

INVENTORY_VERSION = 1
INVENTORY_PATH = HARNESS_ROOT / "data_lake" / "lake_touchpoint_inventory_v0.json"

DIRECT_PACKET_WRITER_TOKENS = {"write_local_source_capture_packet", "stage_and_write_packet"}
PACKET_WRITER_NAME_RE = re.compile(r"write_.*_packet$")
ENV_OUTPUT_OMITTED_TOKENS = (
    'args.output is None and os.environ.get("ORCA_DATA_ROOT")',
    'output_directory is None and os.environ.get("ORCA_DATA_ROOT")',
)
EXPLICIT_PAIR_REJECT_TOKENS = (
    "args.output is not None and args.data_root is not None",
    "output_directory is not None and args.data_root is not None",
    "add_mutually_exclusive_group",
)

# Packet-producing runners that intentionally do NOT route into the lake yet.
# Each MUST carry a reason; entries surface in the inventory record as
# exclusions and in the seam test as acknowledged-unsynced runners.
KNOWN_UNSYNCED: dict[str, str] = {}

# Orchestrator runners that forward data_root into raw-packet sub-runners
# instead of calling a packet writer directly. Declared, not auto-discovered.
BRONZE_PACKET_ORCHESTRATORS: dict[str, tuple[str, ...]] = {
    "run_fragrantica_mgt_capture.py": ("http_runner", "cloakbrowser_runner"),
    "run_ig_reels_lane_orchestrator.py": ("grid_runner",),
}

NON_RAW_LAKE_TOUCHPOINT_CALLS = {
    "append_record",
    "append_record_set",
    "append_silver_record",
    "catalog_coverage_census",
    "inspect_catalog",
    "is_record_set_complete",
    "lane_dir",
    "load_attachment_record_body",
    "rebuild_catalog",
    "record_path",
    "source_surface_catalog_rows",
}

# Surfaces that consume or rebuild the manifest-equivalent generated
# catalog/AR index; the A2 fork's packet-index branch would reshape these.
PACKET_INDEX_CALLS = {
    "catalog_coverage_census",
    "inspect_catalog",
    "load_attachment_record_body",
    "rebuild_catalog",
    "source_surface_catalog_rows",
}

A2_FORK_IMPACT_VALUES = ("manifest_shape", "packet_index", "none")

STRUCTURAL_EXCLUSIONS: tuple[dict[str, str], ...] = (
    {
        "target": "orca-harness/tests/**",
        "reason": "test code is not a production lake touchpoint; discovery scans tracked non-test harness source only",
    },
    {
        "target": "non-git-tracked files",
        "reason": "discovery reads `git ls-files` output only, so untracked scratch cannot become a silent lake touchpoint",
    },
)


def a2_fork_impact_for_call(call_name: str) -> str:
    """Deterministic fork-impact class for a non-raw touchpoint call name."""
    return "packet_index" if call_name in PACKET_INDEX_CALLS else "none"


@dataclass(frozen=True)
class ProducerCall:
    name: str
    line: int
    forwards_data_root: bool


@dataclass(frozen=True)
class RunnerSeam:
    exposes_output_arg: bool
    exposes_data_root_arg: bool
    exposes_env_fallback: bool
    resolves_data_root: bool
    rejects_output_and_data_root: bool
    env_fallback_uses_output_omitted: bool
    producer_calls: tuple[ProducerCall, ...]

    @property
    def forwards_data_root(self) -> bool:
        return any(call.forwards_data_root for call in self.producer_calls)

    @property
    def has_seam(self) -> bool:
        return (
            self.exposes_data_root_arg
            and self.exposes_env_fallback
            and self.resolves_data_root
            and self.forwards_data_root
        )

    @property
    def has_exclusive_output_mode(self) -> bool:
        if not self.exposes_output_arg:
            return True
        return self.rejects_output_and_data_root and self.env_fallback_uses_output_omitted

    def missing_seam_parts(self) -> list[str]:
        missing: list[str] = []
        if not self.exposes_data_root_arg:
            missing.append("--data-root argument")
        if not self.exposes_env_fallback:
            missing.append("ORCA_DATA_ROOT fallback")
        if not self.resolves_data_root:
            missing.append("DataLakeRoot.resolve")
        if not self.forwards_data_root:
            missing.append("data_root= forwarded into packet writer")
        return missing

    def missing_output_mode_parts(self) -> list[str]:
        if not self.exposes_output_arg:
            return []
        missing: list[str] = []
        if not self.rejects_output_and_data_root:
            missing.append("explicit --output + --data-root rejection")
        if not self.env_fallback_uses_output_omitted:
            missing.append("ORCA_DATA_ROOT gated on --output being omitted")
        return missing


def has_any_token(src: str, tokens: tuple[str, ...]) -> bool:
    return any(token in src for token in tokens)


def call_name(node: ast.Call) -> str | None:
    if isinstance(node.func, ast.Name):
        return node.func.id
    if isinstance(node.func, ast.Attribute):
        return node.func.attr
    return None


def dotted_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parent = dotted_name(node.value)
        if parent is None:
            return None
        return f"{parent}.{node.attr}"
    return None


def called_names(node: ast.AST) -> set[str]:
    return {
        name
        for child in ast.walk(node)
        if isinstance(child, ast.Call)
        for name in [call_name(child)]
        if name is not None
    }


def calls_named(tree: ast.AST, names: tuple[str, ...]) -> list[ast.Call]:
    return [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and call_name(node) in names
    ]


@cache
def _packet_writer_function_index() -> tuple[frozenset[str], tuple[tuple[str, tuple[str, ...]], ...]]:
    """Recursive writer-function closure plus the files each writer is defined in."""
    function_calls: dict[str, set[str]] = {}
    definition_sites: dict[str, set[str]] = {}
    for path in sorted(SOURCE_CAPTURE_DIR.rglob("*.py")):
        relative = path.relative_to(HARNESS_ROOT).as_posix()
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                function_calls[node.name] = called_names(node)
                definition_sites.setdefault(node.name, set()).add(relative)

    writers = set(DIRECT_PACKET_WRITER_TOKENS)
    changed = True
    while changed:
        changed = False
        for name, calls in function_calls.items():
            if name not in writers and calls.intersection(writers):
                writers.add(name)
                changed = True
    sites = tuple(
        (name, tuple(sorted(definition_sites.get(name, set()))))
        for name in sorted(writers)
    )
    return frozenset(writers), sites


def source_capture_packet_writer_names() -> frozenset[str]:
    """Function names in source_capture that eventually stage/write a raw packet."""
    names, _sites = _packet_writer_function_index()
    return names


def packet_writer_function_sites() -> dict[str, tuple[str, ...]]:
    """Writer-function name -> sorted defining files (empty for the seed tokens
    when they are defined outside source_capture rglob, which does not happen
    today)."""
    _names, sites = _packet_writer_function_index()
    return dict(sites)


def is_packet_writer_name(
    name: str | None, packet_writer_names: set[str] | frozenset[str]
) -> bool:
    return bool(name) and (
        name in packet_writer_names or bool(PACKET_WRITER_NAME_RE.fullmatch(name))
    )


def cli_flags(tree: ast.AST) -> set[str]:
    flags: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or call_name(node) != "add_argument":
            continue
        for arg in node.args:
            if (
                isinstance(arg, ast.Constant)
                and isinstance(arg.value, str)
                and arg.value.startswith("--")
            ):
                flags.add(arg.value)
    return flags


def source_capture_imports(tree: ast.AST) -> tuple[set[str], set[str]]:
    packet_writer_names = source_capture_packet_writer_names()
    writer_names = set(DIRECT_PACKET_WRITER_TOKENS)
    module_aliases: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if not (node.module or "").startswith("source_capture"):
                continue
            for alias in node.names:
                if is_packet_writer_name(alias.name, packet_writer_names):
                    writer_names.add(alias.asname or alias.name)
                else:
                    module_aliases.add(alias.asname or alias.name)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.startswith("source_capture."):
                    module_aliases.add(alias.asname or alias.name)
    return writer_names, module_aliases


def is_imported_module_writer_call(node: ast.Call, module_aliases: set[str]) -> bool:
    if not isinstance(node.func, ast.Attribute):
        return False
    if not is_packet_writer_name(node.func.attr, source_capture_packet_writer_names()):
        return False
    base_name = dotted_name(node.func.value)
    return base_name in module_aliases


def producer_calls(
    tree: ast.AST, writer_names: set[str], module_aliases: set[str]
) -> tuple[ProducerCall, ...]:
    calls: list[ProducerCall] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = call_name(node)
        if name not in writer_names and not is_imported_module_writer_call(node, module_aliases):
            continue
        calls.append(
            ProducerCall(
                name=name or "<unknown>",
                line=node.lineno,
                forwards_data_root=any(keyword.arg == "data_root" for keyword in node.keywords),
            )
        )
    return tuple(calls)


def packet_producers() -> dict[str, RunnerSeam]:
    """Map each packet-producing runner filename to its lake seam shape."""
    producers: dict[str, RunnerSeam] = {}
    for path in sorted(RUNNERS_DIR.glob("run_*.py")):
        src = path.read_text(encoding="utf-8")
        tree = ast.parse(src, filename=str(path))
        flags = cli_flags(tree)
        writer_names, module_aliases = source_capture_imports(tree)
        calls = producer_calls(tree, writer_names, module_aliases)
        if calls:
            producers[path.name] = RunnerSeam(
                exposes_output_arg="--output" in flags,
                exposes_data_root_arg="--data-root" in flags,
                exposes_env_fallback="ORCA_DATA_ROOT" in src,
                resolves_data_root="DataLakeRoot.resolve" in src,
                rejects_output_and_data_root=has_any_token(src, EXPLICIT_PAIR_REJECT_TOKENS),
                env_fallback_uses_output_omitted=has_any_token(src, ENV_OUTPUT_OMITTED_TOKENS),
                producer_calls=calls,
            )
    return producers


def bronze_writer_runners() -> frozenset[str]:
    return frozenset(packet_producers()).union(BRONZE_PACKET_ORCHESTRATORS)


@cache
def tracked_harness_python_files() -> tuple[Path, ...]:
    result = subprocess.run(
        ["git", "-C", str(HARNESS_ROOT.parent), "ls-files", "--", "orca-harness"],
        check=True,
        stdout=subprocess.PIPE,
        text=True,
    )
    paths: list[Path] = []
    for line in result.stdout.splitlines():
        path = HARNESS_ROOT.parent / line
        if path.suffix != ".py":
            continue
        relative_path = path.relative_to(HARNESS_ROOT).as_posix()
        if relative_path.startswith("tests/"):
            continue
        paths.append(path)
    return tuple(sorted(paths))


def non_raw_lake_touchpoints() -> Counter[tuple[str, str]]:
    """Current non-raw lake write/read touchpoints that must be classified before GT forks."""
    touchpoints: Counter[tuple[str, str]] = Counter()
    for path in tracked_harness_python_files():
        relative_path = path.relative_to(HARNESS_ROOT).as_posix()
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            name = call_name(node)
            if name in NON_RAW_LAKE_TOUCHPOINT_CALLS:
                touchpoints[(relative_path, name)] += 1
    return touchpoints


def build_inventory() -> dict:
    """Fresh deterministic inventory from tracked source. Pure discovery plus
    module-declared exclusions; no filesystem writes."""
    runner_entries = [
        {"runner": name, "kind": "direct_packet_writer", "a2_fork_impact": "manifest_shape"}
        for name in sorted(packet_producers())
    ] + [
        {"runner": name, "kind": "orchestrator", "a2_fork_impact": "manifest_shape"}
        for name in sorted(BRONZE_PACKET_ORCHESTRATORS)
    ]
    writer_entries = [
        {
            "function": name,
            "defined_in": list(sites),
            "a2_fork_impact": "manifest_shape",
        }
        for name, sites in sorted(packet_writer_function_sites().items())
    ]
    touchpoint_entries = [
        {
            "module": module,
            "call": call,
            "count": count,
            "a2_fork_impact": a2_fork_impact_for_call(call),
        }
        for (module, call), count in sorted(non_raw_lake_touchpoints().items())
    ]
    exclusions = [dict(entry) for entry in STRUCTURAL_EXCLUSIONS] + [
        {
            "target": runner,
            "reason": reason,
            "kind": "acknowledged_unsynced_packet_runner",
        }
        for runner, reason in sorted(KNOWN_UNSYNCED.items())
    ]
    return {
        "inventory_version": INVENTORY_VERSION,
        "authority_note": (
            "Generated inventory of code surfaces; never lake authority; "
            "regenerated and diffed by tests/contract/test_data_lake_inventory_gate.py; "
            "a2_fork_impact is routing metadata for the deferred A2 decision, not a selection."
        ),
        "raw_packet_writers": {
            "runner_seams": sorted(runner_entries, key=lambda e: e["runner"]),
            "writer_functions": writer_entries,
        },
        "non_raw_touchpoints": touchpoint_entries,
        "exclusions": exclusions,
        "unknowns": [],
    }


def serialize_inventory(inventory: dict) -> str:
    """Canonical serialization: sorted keys, two-space indent, trailing newline."""
    return json.dumps(inventory, indent=2, sort_keys=True) + "\n"


def load_declared_inventory(path: Path = INVENTORY_PATH) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def inventory_violations(declared: dict, discovered: dict) -> list[str]:
    """Gate checks: drift between declared and discovered, unreasoned
    exclusions, and unknowns without a resolved owner disposition."""
    violations: list[str] = []

    if declared.get("inventory_version") != discovered.get("inventory_version"):
        violations.append(
            "inventory_version mismatch: declared="
            f"{declared.get('inventory_version')!r} discovered={discovered.get('inventory_version')!r}"
        )

    def _entry_set(inventory: dict, family: str, subfamily: str | None = None) -> set[str]:
        node = inventory.get(family, {})
        entries = node.get(subfamily, []) if subfamily else node
        if not isinstance(entries, list):
            return set()
        return {json.dumps(entry, sort_keys=True) for entry in entries}

    for family, subfamily in (
        ("raw_packet_writers", "runner_seams"),
        ("raw_packet_writers", "writer_functions"),
        ("non_raw_touchpoints", None),
        ("exclusions", None),
    ):
        label = f"{family}.{subfamily}" if subfamily else family
        declared_set = _entry_set(declared, family, subfamily)
        discovered_set = _entry_set(discovered, family, subfamily)
        for entry in sorted(discovered_set - declared_set):
            violations.append(f"undeclared {label} entry (discovered, not in record): {entry}")
        for entry in sorted(declared_set - discovered_set):
            violations.append(f"stale {label} entry (declared, no longer discovered): {entry}")

    for exclusion in declared.get("exclusions", []):
        if not str(exclusion.get("reason", "")).strip():
            violations.append(f"exclusion without a reason: {exclusion.get('target')!r}")

    for unknown in declared.get("unknowns", []):
        disposition = unknown.get("owner_disposition") or {}
        if disposition.get("status") != "resolved":
            violations.append(
                "unknown without a resolved owner disposition (owner-attributable via the "
                f"human-gated PR merge; pending fails the gate): {unknown.get('target')!r}"
            )
            continue
        if not str(unknown.get("target", "")).strip():
            violations.append("resolved unknown without a target")
        if not str(unknown.get("question", "")).strip():
            violations.append(f"resolved unknown without a question: {unknown.get('target')!r}")
        if not str(disposition.get("disposition", "")).strip():
            violations.append(
                f"resolved unknown without a concrete disposition: {unknown.get('target')!r}"
            )
        if not str(disposition.get("recorded_by", "")).strip():
            violations.append(
                f"resolved unknown without owner-attribution evidence: {unknown.get('target')!r}"
            )

    return violations
