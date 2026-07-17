#!/usr/bin/env python3
"""Placement boundary check (EP-04): dormant advisory mode plus CI diff gate.

The machine classification source is ``repo-structure.yaml``; placement
policy remains owned by ``.agents/workflow-overlay/artifact-folders.md`` and
``docs/decisions/forseti_repo_structure_binding_v0.md``. A pass proves only
that changed path shapes are declared, never authority, readiness, or quality.

Active enforcement is non-interactive:

    check_placement.py --changed --strict [--base REF]

The strict changed-path gate checks added, modified, copied, and rename-
destination paths against the CI event base, ignores deletions, and then runs
the lightweight map-to-top-level-tree freshness check. Its Git diff has a
20-second internal timeout and any unavailable diff or invalid map fails
visibly. ``--hook`` and full-tree ``--check``/``--strict`` remain compatible
manual modes but are not registered on an interactive tool boundary.
"""
from __future__ import annotations

import fnmatch
import json
import os
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _hooklib import repo_root  # noqa: E402  (sys.path pin must precede the import)

MAP_PATH = "repo-structure.yaml"
AUTHORITY = ".agents/workflow-overlay/artifact-folders.md"
BINDING = "docs/decisions/forseti_repo_structure_binding_v0.md"
DIFF_TIMEOUT_SECONDS = 20

# Frozen map schema (forseti_repo_structure_binding_v0): top-level keys.
REQUIRED_KEYS = ("version", "known_top_level", "docs_roles", "scratch_rules",
                 "legacy_tolerated", "inbox", "excluded")

OK = "ok"
SCRATCH = "scratch_excluded"
EXCLUDED = "excluded_tree"
LEGACY = "legacy_tolerated"
VIOLATION = "unplaced"


def load_map(root: Path):
    """Return (mapdata, error). mapdata None on any failure."""
    p = root / MAP_PATH
    if not p.is_file():
        return None, f"map missing: {MAP_PATH}"
    try:
        import yaml  # PyYAML; absence is an environment defect, reported not hidden
    except ImportError:
        return None, "PyYAML unavailable to hook python"
    try:
        data = yaml.safe_load(p.read_text(encoding="utf-8"))
    except Exception as exc:
        return None, f"map unparseable: {exc}"
    if not isinstance(data, dict):
        return None, "map root is not a mapping"
    missing = [k for k in REQUIRED_KEYS if k not in data]
    if missing:
        return None, "map missing frozen keys: " + ", ".join(missing)
    err = tolerance_sanity_error(data)
    if err:
        return None, err
    return data, ""


def tolerance_sanity_error(mapdata) -> str:
    """Fake-pass guard: legacy_tolerated must stay enumerated debt, not a blanket."""
    for g in mapdata.get("legacy_tolerated") or []:
        s = str(g).strip()
        if s in ("*", "**", "**/*") or "/" not in s:
            return f"legacy_tolerated entry too broad: '{s}'"
    return ""


def _known_files(mapdata) -> set:
    files = set((mapdata.get("known_top_level") or {}).get("files") or [])
    for v in (mapdata.get("entry_points") or {}).values():
        files.add(str(v))
    for role in mapdata.get("docs_roles") or []:
        if isinstance(role, dict) and role.get("entry"):
            files.add(str(role["entry"]))
    return files


def _generated_match(seg: str, patterns) -> bool:
    return any(fnmatch.fnmatch(seg, pat) for pat in patterns)


def _path_glob_match(rel: str, pattern: str) -> bool:
    """Path-aware glob: '*' never crosses '/'; a trailing '**' segment matches
    any remaining depth (>=1). fnmatch alone would let 'docs/product/*.md'
    swallow lane subfolders."""
    rparts, pparts = rel.split("/"), str(pattern).split("/")
    if pparts and pparts[-1] == "**":
        head = pparts[:-1]
        if len(rparts) <= len(head):
            return False
        return all(fnmatch.fnmatch(r, p) for r, p in zip(rparts[:len(head)], head))
    if len(rparts) != len(pparts):
        return False
    return all(fnmatch.fnmatch(r, p) for r, p in zip(rparts, pparts))


def classify(rel: str, mapdata) -> tuple[str, str]:
    """Pure placement decision for one repo-relative POSIX path.

    Returns (status, detail). Never raises on string input."""
    rel = rel.strip().lstrip("/")
    if not rel:
        return OK, ""
    parts = rel.split("/")
    ktl = mapdata.get("known_top_level") or {}
    scratch = mapdata.get("scratch_rules") or {}
    patterns = scratch.get("generated_patterns") or []

    for seg in parts:
        if scratch.get("underscore_prefix_dirs") and seg.startswith("_") and seg != "_":
            return SCRATCH, seg
        if _generated_match(seg, patterns):
            return SCRATCH, seg
    if parts[0] in (mapdata.get("excluded") or []):
        return EXCLUDED, parts[0]

    for glob in mapdata.get("legacy_tolerated") or []:
        if _path_glob_match(rel, str(glob)):
            return LEGACY, str(glob)

    if rel in _known_files(mapdata):
        return OK, "known file"

    if len(parts) == 1:
        return VIOLATION, "file at repo root is not in known_top_level.files"

    if parts[0] not in (ktl.get("dirs") or []):
        return VIOLATION, f"unknown top-level area '{parts[0]}'"

    if parts[0] == "docs":
        if len(parts) == 2:
            return VIOLATION, "file directly under docs/ is not a declared entry point"
        homes = {str(r.get("home", "")).split("/")[-1]
                 for r in (mapdata.get("docs_roles") or []) if isinstance(r, dict)}
        if parts[1] not in homes:
            return VIOLATION, f"'docs/{parts[1]}/' is not a declared docs role"
        if parts[1] == "product" and len(parts) >= 4:
            lanes = {str(l.get("name")) for l in (mapdata.get("product_lanes") or [])
                     if isinstance(l, dict)}
            if lanes and parts[2] not in lanes:
                return VIOLATION, f"'docs/product/{parts[2]}/' is not a bound product lane"
        return OK, f"docs role '{parts[1]}'"

    return OK, f"declared top-level area '{parts[0]}'"


def product_lane_hint(rel: str, mapdata) -> str:
    """Forward-only nudge for a flat docs/product write (advisory copy only)."""
    parts = rel.split("/")
    if len(parts) == 3 and parts[0] == "docs" and parts[1] == "product" and parts[2] != "README.md":
        lanes = [str(l.get("name")) for l in (mapdata.get("product_lanes") or [])
                 if isinstance(l, dict)]
        if lanes:
            return ("new product artifacts belong in a lane subfolder ("
                    + ", ".join(lanes) + "); flat placement at docs/product/ root is for "
                    "bounded residuals only, per the binding")
    return ""


def freshness_findings(root: Path, mapdata) -> list[str]:
    """Map<->tree consistency, both directions. Returns strict-failing findings."""
    out = []
    ktl = mapdata.get("known_top_level") or {}
    for d in ktl.get("dirs") or []:
        if not (root / d).is_dir():
            out.append(f"map-stale: declared top-level dir missing from tree: {d}")
    for f in ktl.get("files") or []:
        if not (root / f).is_file():
            out.append(f"map-stale: declared top-level file missing from tree: {f}")
    for role in mapdata.get("docs_roles") or []:
        home = str(role.get("home", "")) if isinstance(role, dict) else ""
        if home and not (root / home).is_dir():
            out.append(f"map-stale: declared docs role home missing: {home}")
    scratch = mapdata.get("scratch_rules") or {}
    patterns = scratch.get("generated_patterns") or []
    known = set(ktl.get("dirs") or []) | set(ktl.get("files") or [])
    excluded = set(mapdata.get("excluded") or [])
    try:
        entries = sorted(p.name for p in root.iterdir())
    except OSError:
        return out
    for name in entries:
        if name in known or name in excluded:
            continue
        if scratch.get("underscore_prefix_dirs") and name.startswith("_"):
            continue
        if _generated_match(name, patterns):
            continue
        out.append(f"unknown top-level entry (not in map): {name}")
    return out


def inbox_age_warnings(root: Path, mapdata) -> list[str]:
    """WARN-only hygiene signal; never affects exit codes."""
    inbox = mapdata.get("inbox") or {}
    home, days = inbox.get("home"), inbox.get("max_age_days")
    if not home or not days:
        return []
    base = root / str(home)
    if not base.is_dir():
        return []
    cutoff = time.time() - float(days) * 86400.0
    old = []
    try:
        for p in sorted(base.iterdir()):
            if p.name.lower() == "readme.md":
                continue
            try:
                if p.stat().st_mtime < cutoff:
                    old.append(p.name)
            except OSError:
                continue
    except OSError:
        return []
    if not old:
        return []
    head = ", ".join(old[:5]) + (f" (+{len(old) - 5} more)" if len(old) > 5 else "")
    return [f"_inbox items older than {days} days: {head} - promote, archive, or queue "
            f"(docs/hygiene/queue.md); advisory only"]


def _authority_line() -> str:
    return (f"Authority: {AUTHORITY} (rules) + {BINDING} (binding) + {MAP_PATH} (router). "
            "Placement-shape only - not authority, validation, or readiness.")


def evaluate_tree(root: Path, mapdata):
    """Return (violations, legacy, scratch_count, freshness, inbox_warns)."""
    violations, legacy = [], []
    scratch_count = 0
    skip_dirs = set(mapdata.get("excluded") or []) | {".git"}
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(root).as_posix()
        if rel.split("/")[0] in skip_dirs:
            continue
        status, detail = classify(rel, mapdata)
        if status == VIOLATION:
            violations.append((rel, detail))
        elif status == LEGACY:
            legacy.append(rel)
        elif status == SCRATCH:
            scratch_count += 1
    return violations, legacy, scratch_count, freshness_findings(root, mapdata), \
        inbox_age_warnings(root, mapdata)


def resolve_base_ref(requested: str | None = None) -> str:
    """Resolve the exact CI event base before branch or CLI fallbacks."""
    event_base = os.environ.get("FORSETI_DIFF_BASE", "").strip()
    if event_base:
        return event_base
    github_base = os.environ.get("GITHUB_BASE_REF", "").strip()
    if github_base:
        return f"origin/{github_base}"
    if requested and requested.strip():
        return requested.strip()
    return "origin/main"


def parse_name_status(output: str) -> tuple[list[str], str]:
    """Return changed destinations from ``git diff --name-status -z`` output."""
    tokens = output.split("\0")
    if tokens and tokens[-1] == "":
        tokens.pop()
    paths: list[str] = []
    index = 0
    while index < len(tokens):
        status = tokens[index]
        index += 1
        kind = status[:1]
        if kind in {"A", "M", "D"}:
            if index >= len(tokens):
                return [], f"malformed diff: {status} has no path"
            path = tokens[index]
            index += 1
            if kind != "D":
                paths.append(path)
        elif kind in {"C", "R"}:
            if index + 1 >= len(tokens):
                return [], f"malformed diff: {status} has no source/destination pair"
            index += 1  # source path is not the placement target
            paths.append(tokens[index])
            index += 1
        else:
            return [], f"malformed diff: unsupported status {status!r}"
    return paths, ""


def changed_paths(root: Path, base: str) -> tuple[list[str] | None, str]:
    command = [
        "git", "--no-optional-locks", "-C", str(root), "diff",
        "--name-status", "-z", "--diff-filter=ACMR", "--find-renames",
        f"{base}...HEAD",
    ]
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=DIFF_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        return None, f"git diff timed out after {DIFF_TIMEOUT_SECONDS}s against {base}"
    except (FileNotFoundError, OSError) as exc:
        return None, f"git diff unavailable against {base}: {exc}"
    if result.returncode != 0:
        detail = result.stderr.strip() or f"exit {result.returncode}"
        return None, f"git diff failed against {base}: {detail}"
    paths, error = parse_name_status(result.stdout)
    return (None, error) if error else (paths, "")


def run_changed(root: Path, base: str) -> int:
    mapdata, error = load_map(root)
    if mapdata is None:
        print(f"MAP ERROR: {error}")
        print(_authority_line())
        return 1
    paths, error = changed_paths(root, base)
    if paths is None:
        print(f"DIFF ERROR: {error}")
        print(_authority_line())
        return 1

    violations: list[tuple[str, str]] = []
    legacy: list[str] = []
    for rel in paths:
        status, detail = classify(rel, mapdata)
        if status == VIOLATION:
            violations.append((rel, detail))
        elif status == LEGACY:
            legacy.append(rel)
    freshness = freshness_findings(root, mapdata)
    for rel, detail in violations:
        print(f"VIOLATION  {rel}  ({detail})")
    for finding in freshness:
        print(f"FRESHNESS  {finding}")
    for rel in legacy:
        print(f"LEGACY     {rel}")
    print(
        f"summary: {len(paths)} changed path(s), {len(violations)} violation(s), "
        f"{len(freshness)} freshness, {len(legacy)} legacy-tolerated (warn-only); "
        f"base={base}"
    )
    print(_authority_line())
    return 1 if violations or freshness else 0


def _base_arg(argv: list[str]) -> str | None:
    if "--base" not in argv:
        return None
    index = argv.index("--base")
    if index + 1 >= len(argv) or argv[index + 1].startswith("--"):
        raise ValueError("--base requires a ref")
    return argv[index + 1]


def run_hook(root: Path) -> int:
    try:
        ev = json.loads(sys.stdin.read() or "{}")
    except ValueError:
        return 0
    ti = ev.get("tool_input") or {}
    target = ti.get("file_path") or ti.get("notebook_path") or ti.get("path") or ""
    if not target:
        return 0
    p = Path(target)
    try:
        rel = (p if p.is_absolute() else root / p).resolve().relative_to(root).as_posix()
    except (ValueError, OSError):
        return 0  # outside repo - not this checker's boundary
    mapdata, err = load_map(root)
    if mapdata is None:
        sys.stderr.write(f"check_placement: {err}; allowing (advisory hook fails open)\n")
        return 0
    status, detail = classify(rel, mapdata)
    msg = ""
    if status == VIOLATION:
        msg = (f"PLACEMENT WARN: '{rel}' has no declared home ({detail}). Place it in a "
               f"declared role folder, or quarantine in docs/_inbox/ and add a "
               f"docs/hygiene/queue.md entry. A new lane/role needs a recorded decision. "
               + _authority_line())
    elif status in (OK, LEGACY):
        # forward-only lane nudge for flat docs/product writes (fires whether the
        # flat file is tolerated legacy debt or a post-apply residual)
        hint = product_lane_hint(rel, mapdata)
        if hint:
            msg = f"PLACEMENT NOTE: '{rel}' - {hint}. " + _authority_line()
    if msg:
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PostToolUse", "additionalContext": msg}}))
    return 0


def run_tree(root: Path, strict: bool) -> int:
    mapdata, err = load_map(root)
    if mapdata is None:
        print(f"MAP ERROR: {err}")
        print(_authority_line())
        return 1 if strict else 0
    violations, legacy, scratch_count, freshness, inbox_warns = evaluate_tree(root, mapdata)
    for rel, detail in violations:
        print(f"VIOLATION  {rel}  ({detail})")
    for f in freshness:
        print(f"FRESHNESS  {f}")
    for rel in legacy:
        print(f"LEGACY     {rel}")
    for w in inbox_warns:
        print(f"INBOX      {w}")
    print(f"summary: {len(violations)} violation(s), {len(freshness)} freshness, "
          f"{len(legacy)} legacy-tolerated (warn-only), {scratch_count} scratch-excluded file(s)")
    print(_authority_line())
    if strict and (violations or freshness):
        return 1
    return 0


def selftest() -> int:
    m = {
        "version": 1,
        "entry_points": {"docs_readme": "docs/README.md"},
        "known_top_level": {"dirs": [".agents", "docs", "forseti-harness"],
                            "files": ["AGENTS.md", "repo-structure.yaml"]},
        "docs_roles": [{"home": "docs/decisions", "entry": "docs/decisions/README.md"},
                       {"home": "docs/product", "entry": "forseti/product/README.md"},
                       {"home": "docs/_inbox", "entry": "docs/_inbox/README.md"}],
        "product_lanes": [{"name": "core_spine", "status": "planned"}],
        "scratch_rules": {"underscore_prefix_dirs": True,
                          "generated_patterns": ["__pycache__", "pytest_run_*"]},
        "legacy_tolerated": ["docs/product/*.md", "forseti-harness/**"],
        "inbox": {"home": "docs/_inbox", "max_age_days": 30},
        "excluded": [".git", ".claude"],
    }
    cases = [
        ("docs/decisions/foo_v0.md", OK),
        ("docs/decisions/README.md", OK),
        ("docs/README.md", OK),                       # declared entry point
        ("docs/STRUCTURE.md", VIOLATION),             # not declared in this test map
        ("AGENTS.md", OK),
        ("stray_root_note.md", VIOLATION),            # root stray
        ("mystery_dir/file.md", VIOLATION),           # unknown top-level
        ("docs/notarole/file.md", VIOLATION),         # undeclared docs role
        ("docs/product/flat_note_v0.md", LEGACY),     # tolerated debt, warn-only
        ("docs/product/core_spine/x_v0.md", OK),      # lane placement
        ("docs/product/random_lane/file.md", VIOLATION),  # DRB-002: unknown lane rejected
        ("docs/product/core_spine/deep/nested_v0.md", OK),  # depth below a bound lane
        ("docs/_inbox/whatever.bin", SCRATCH),        # quarantine, excluded
        ("forseti-harness/pytest_run_3/out.json", SCRATCH),
        ("forseti-harness/__pycache__/x.pyc", SCRATCH),
        ("forseti-harness/Makefile", LEGACY),            # harness tolerance (recursive **)
        ("forseti-harness/capture_spine/runner.py", LEGACY),
        (".claude/settings.json", EXCLUDED),
    ]
    ok = True
    for i, (rel, expect) in enumerate(cases, 1):
        got, detail = classify(rel, m)
        status = "PASS" if got == expect else "FAIL"
        if got != expect:
            ok = False
        print(f"{status} case {i:02d}  {rel:45s} expect={expect:16s} got={got}  {detail}")
    # fake-pass guards
    guards = [
        (tolerance_sanity_error({"legacy_tolerated": ["**"]}) != "", "blanket '**' tolerance rejected"),
        (tolerance_sanity_error({"legacy_tolerated": ["docs"]}) != "", "no-slash tolerance rejected"),
        (tolerance_sanity_error(m) == "", "enumerated tolerance accepted"),
        (load_map(Path("/nonexistent-root-xyz"))[0] is None, "missing map loads as None (strict mode exits 1)"),
        (classify("docs/product/flat_note_v0.md", m)[0] != OK, "flat product is never a silent OK"),
        (not _path_glob_match("docs/product/core_spine/x.md", "docs/product/*.md"),
         "single-star tolerance does not cross '/' into lanes"),
    ]
    for i, (passed, name) in enumerate(guards, 1):
        status = "PASS" if passed else "FAIL"
        if not passed:
            ok = False
        print(f"{status} guard {i:02d}  {name}")
    print("SELFTEST", "OK" if ok else "FAILED")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    # Forced-exception probe: proves the __main__ gating handler
    # (forseti-harness/tests/unit/test_hook_internal_error_gating.py).
    if "--force-internal-error" in argv:
        raise RuntimeError("forced internal error (probe)")
    root = repo_root()
    if "--selftest" in argv:
        return selftest()
    if "--changed" in argv:
        if "--strict" not in argv:
            sys.stderr.write("check_placement: --changed requires --strict\n")
            return 2
        return run_changed(root, resolve_base_ref(_base_arg(argv)))
    if "--strict" in argv:
        return run_tree(root, strict=True)
    if "--check" in argv:
        return run_tree(root, strict=False)
    return run_hook(root)  # default / --hook compatibility mode


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except SystemExit:
        raise
    except Exception as exc:  # fail OPEN in the advisory paths; never brick the agent
        # --selftest joins --strict as a gating mode (GATE FAIL bucket,
        # validation-gates.md; EP-35 FIND-02 class sweep).
        if "--strict" in sys.argv or "--changed" in sys.argv or "--selftest" in sys.argv:
            sys.stderr.write(f"check_placement: internal error in gating mode: {exc}\n")
            sys.exit(1)
        sys.stderr.write(f"check_placement: internal error, allowing: {exc}\n")
        sys.exit(0)
