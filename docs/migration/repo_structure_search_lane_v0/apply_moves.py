#!/usr/bin/env python3
"""Search-lane migration: search-primary + demand-signal-method docs -> docs/product/search/.

Scoped, manifest-driven, reversible, dry-run-first, IDEMPOTENT. Owned by
docs/decisions/orca_search_product_lane_binding_v0.md (lane binding) and
docs/migration/repo_structure_search_lane_v0/runbook.md (procedure). Cloned and
scoped down from the Phase-2 engine
(docs/migration/repo_structure_phase2_consolidation_v0/apply_moves.py).

DESIGN INVARIANTS
  - moves_manifest.csv is the single source for apply/reverse (the full lane set).
  - IDEMPOTENT: a row whose source is already gone AND target already exists is
    treated as already-applied and skipped (so the manifest can grow across
    waves and --apply re-run safely).
  - Reference rewrites replace the FULL old-path string -> new-path string only.
    Bare-filename mentions are never rewritten.
  - Rewrites apply in CURRENT/LIVE files only. HISTORICAL records (decisions,
    reviews, prompts, research, hygiene, _inbox) and scratch keep their old-path
    text and resolve via moved_paths_index.md (written by --apply).
  - --apply refuses on a dirty tree unless --waive-dirty-tree (runbook
    precondition: clean commit checkpoint).
  - --apply flips repo-structure.yaml product_lanes `search` planned -> current
    (idempotent: a no-op once already current).

MODES
  apply_moves.py --dry-run   validate manifest, scan refs, print plan (default)
  apply_moves.py --apply     git mv pending + live rewrites + moved_paths_index + status flip
  apply_moves.py --reverse   undo the moves (content rewrites + status flip revert via git)

Not validation, readiness, or authority. After --apply, run
  python .agents/hooks/check_placement.py --strict
and follow the runbook's post-apply checklist.
"""
from __future__ import annotations

import argparse
import csv
import subprocess
import sys
from pathlib import Path

PKG = Path(__file__).resolve().parent
ROOT = PKG.parents[2]
MANIFEST = PKG / "moves_manifest.csv"
INDEX = PKG / "moved_paths_index.md"
MAP_FILE = ROOT / "repo-structure.yaml"

# Current/live trees get path rewrites; historical trees keep old text (index covers them).
HISTORICAL_PREFIXES = (
    "docs/decisions/", "docs/review-inputs/", "docs/review-outputs/",
    "docs/prompts/", "docs/research/", "docs/hygiene/", "docs/_inbox/",
)
SCAN_EXCLUDE = (
    ".git/", ".codex/", ".claude/",
    "docs/migration/repo_structure_search_lane_v0/",
    "docs/migration/repo_structure_phase2_consolidation_v0/",
)
TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".py", ".json", ".txt", ".toml"}


def git(args):
    res = subprocess.run(["git", "-C", str(ROOT)] + args, capture_output=True, text=True)
    return res.returncode, (res.stdout or "") + (res.stderr or "")


def load_manifest():
    with MANIFEST.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def partition(rows):
    """pending = source exists; done = already moved (src gone, dst exists); problem = both gone."""
    pending, done, problem = [], [], []
    for r in rows:
        if (ROOT / r["old_path"]).is_file():
            pending.append(r)
        elif (ROOT / r["new_path"]).exists():
            done.append(r)
        else:
            problem.append(r)
    return pending, done, problem


def iter_scan_files():
    for p in ROOT.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in TEXT_SUFFIXES:
            continue
        rel = p.relative_to(ROOT).as_posix()
        if any(rel.startswith(x) for x in SCAN_EXCLUDE):
            continue
        if "/_" in ("/" + rel):          # underscore-prefixed (scratch) path segment anywhere
            continue
        yield rel, p


def is_historical(rel):
    return any(rel.startswith(h) for h in HISTORICAL_PREFIXES)


def scan_refs(rows):
    olds = [r["old_path"] for r in rows]
    moved = {r["old_path"] for r in rows}
    out = {}
    for rel, p in iter_scan_files():
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        hits = sum(text.count(o) for o in olds)
        if not hits:
            continue
        cls = "moved_set" if rel in moved else ("historical" if is_historical(rel) else "live")
        out[rel] = {"class": cls, "hits": hits}
    return out


def dirty_lines():
    code, out = git(["status", "--porcelain"])
    return [] if code != 0 else [l for l in out.splitlines() if l.strip()]


def dry_run(rows):
    pending, done, problem_rows = partition(rows)
    problems = [f"source AND target both missing: {r['old_path']}" for r in problem_rows]
    targets = set()
    for r in pending:
        if (ROOT / r["new_path"]).exists():
            problems.append(f"target exists for a pending move: {r['new_path']}")
        if r["new_path"] in targets:
            problems.append(f"target collision: {r['new_path']}")
        targets.add(r["new_path"])
    refs = scan_refs(rows)
    rewrite = {r: v for r, v in refs.items() if v["class"] in ("live", "moved_set")}
    hist = {r: v for r, v in refs.items() if v["class"] == "historical"}
    print(f"DRY RUN: {len(pending)} pending move(s), {len(done)} already-applied (skipped) -> docs/product/search/")
    print(f"  live/moved_set files to rewrite ({len(rewrite)}):")
    for rel in sorted(rewrite):
        print(f"    rewrite {refs[rel]['hits']} ref(s): {rel}  [{refs[rel]['class']}]")
    print(f"  historical referencing files (indexed, NOT rewritten): {len(hist)}")
    print(f"  worktree dirty lines: {len(dirty_lines())} (apply needs clean tree or --waive-dirty-tree)")
    if problems:
        print("PROBLEMS:")
        for x in problems:
            print(f"  {x}")
        return 1
    print("dry run OK: manifest is applicable")
    return 0


def rewrite_live(mapping):
    rewritten = 0
    for rel, p in iter_scan_files():
        if is_historical(rel):
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except OSError:
            continue
        new, n = text, 0
        for old, dst in mapping.items():
            if old in new:
                n += new.count(old)
                new = new.replace(old, dst)
        if n:
            p.write_text(new, encoding="utf-8")
            rewritten += n
            print(f"  rewrote {n} ref(s): {rel}")
    return rewritten


def flip_status_current():
    try:
        text = MAP_FILE.read_text(encoding="utf-8")
    except OSError:
        return "map-unreadable"
    planned = "{ name: search, status: planned }"
    current = "{ name: search, status: current }"
    if planned in text:
        MAP_FILE.write_text(text.replace(planned, current, 1), encoding="utf-8")
        return "flipped planned -> current"
    if current in text:
        return "already current"
    return "search lane not found in map"


def write_index(rows):
    lines = ["# Moved Paths Index - Search lane migration (generated)", "",
             "Historical records reference old paths by design; resolve them here.",
             "", "| Old path | New path |", "| --- | --- |"]
    lines += [f"| `{r['old_path']}` | `{r['new_path']}` |" for r in rows]
    INDEX.write_text("\n".join(lines) + "\n", encoding="utf-8")


def apply(rows, waive):
    d = dirty_lines()
    if d and not waive:
        print(f"REFUSED: {len(d)} dirty line(s); commit a checkpoint first or pass --waive-dirty-tree.")
        return 1
    if dry_run(rows) != 0:
        print("REFUSED: dry run found problems.")
        return 1
    pending, done, _ = partition(rows)
    mapping = {r["old_path"]: r["new_path"] for r in rows}
    for r in pending:
        (ROOT / r["new_path"]).parent.mkdir(parents=True, exist_ok=True)
        if r["tracked"] == "tracked":
            code, out = git(["mv", r["old_path"], r["new_path"]])
            if code != 0:
                print(f"ABORT at {r['old_path']}: git mv failed: {out.strip()}")
                return 1
        else:
            (ROOT / r["old_path"]).rename(ROOT / r["new_path"])
    print(f"moved {len(pending)} file(s); {len(done)} already-applied (skipped) -> docs/product/search/")
    print(f"live references rewritten: {rewrite_live(mapping)}")
    write_index(rows)
    print("moved_paths_index written")
    print(f"repo-structure.yaml search lane: {flip_status_current()}")
    print("\nNEXT (runbook): python .agents/hooks/check_placement.py --strict (expect exit 0); "
          "grep for stale old paths in LIVE docs; review git diff --stat; commit.")
    return 0


def reverse(rows):
    n = 0
    for r in rows:
        if not (ROOT / r["new_path"]).is_file():
            continue
        if r["tracked"] == "tracked":
            code, out = git(["mv", r["new_path"], r["old_path"]])
            if code != 0:
                print(f"reverse failed at {r['new_path']}: {out.strip()}")
                return 1
        else:
            (ROOT / r["old_path"]).parent.mkdir(parents=True, exist_ok=True)
            (ROOT / r["new_path"]).rename(ROOT / r["old_path"])
        n += 1
    print(f"reversed {n} move(s). NOTE: live-reference rewrites and the status flip are content "
          "edits - revert them via git from the checkpoint (not undone here).")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--dry-run", action="store_true")
    g.add_argument("--apply", action="store_true")
    g.add_argument("--reverse", action="store_true")
    ap.add_argument("--waive-dirty-tree", action="store_true")
    a = ap.parse_args()
    rows = load_manifest()
    if a.apply:
        return apply(rows, a.waive_dirty_tree)
    if a.reverse:
        return reverse(rows)
    return dry_run(rows)


if __name__ == "__main__":
    sys.exit(main())
