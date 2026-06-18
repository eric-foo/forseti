#!/usr/bin/env python3
"""R2 Data Lake convergence: harvest lake content from the in-flight lanes into
the bound orca/product/spines/data_lake/ spine, rewriting old docs/product refs.

Sources (verified canonical 2026-06-18):
  - 3 contracts + the canonical mechanics map  -> from codex/data-lake-core-contract (#232)
  - 2 migration planning docs                  -> from codex/commission-spine-structure (#239)

For each source: read content from its lane via `git show <lane>:<old>`, rewrite
every old->new path reference (R2 moves + shared/->workflows mechanics + the
spine-first moved_paths_index for other docs/product refs), and write to the new
spine path. Idempotent on content. Dry-run by default.

This does NOT git rm shared/data_lake_mechanics, edit the repo map, or write the
R2 moved-index -- those are done in the same R2 commit but outside this harvester.

Modes: --dry-run (default, reports) | --apply (writes the spine files)
"""
from __future__ import annotations
import re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]   # docs/migration/repo_structure_data_lake_r2_v0/<this> -> repo root
SPINE_INDEX = ROOT / "docs/migration/repo_structure_spine_first_v0/moved_paths_index.md"

LANE_232 = "codex/data-lake-core-contract"
LANE_239 = "codex/commission-spine-structure"

AUTH = "orca/product/spines/data_lake/authority/"
WORK = "orca/product/spines/data_lake/workflows/"
MIGR = "orca/product/spines/data_lake/migrations/"
OLD_CS = "docs/product/core_spine/"
OLD_MIG = "docs/migration/"

# (lane, old_path, new_path)
MOVES = [
    (LANE_232, OLD_CS + "core_spine_v0_data_lake_core_contract_v0.md", AUTH + "core_spine_v0_data_lake_core_contract_v0.md"),
    (LANE_232, OLD_CS + "core_spine_v0_data_lake_storage_contract_v0.md", AUTH + "core_spine_v0_data_lake_storage_contract_v0.md"),
    (LANE_232, OLD_CS + "core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md", AUTH + "core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md"),
    (LANE_232, OLD_CS + "core_spine_v0_data_lake_mechanics_map_v0.md", WORK + "core_spine_v0_data_lake_mechanics_map_v0.md"),
    # NOTE: the 2 #239 planning docs (data_lake_spine_first_migration_{plan,inventory}_v0.md)
    # are DEFERRED from this pass pending the owner's data-lake placement check-in
    # (docs/migration/ vs data_lake/migrations/). When they land they harvest VERBATIM
    # (migration-record bodies are not path-rewritten; only open_next repoints).
]


def git_show(ref: str, path: str) -> str | None:
    r = subprocess.run(["git", "-C", str(ROOT), "show", f"{ref}:{path}"],
                       capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def load_rewrite_map() -> dict[str, str]:
    m: dict[str, str] = {}
    # spine-first index rows: | `old` | `new` |
    row = re.compile(r"^\|\s*`([^`]+)`\s*\|\s*`([^`]+)`\s*\|\s*$")
    for line in SPINE_INDEX.read_text(encoding="utf-8").splitlines():
        mm = row.match(line.strip())
        if mm:
            m[mm.group(1).strip()] = mm.group(2).strip()
    # the spine-first index maps the mechanics map -> shared/; OVERRIDE to workflows/ (R2 re-home)
    m["docs/product/core_spine/core_spine_v0_data_lake_mechanics_map_v0.md"] = WORK + "core_spine_v0_data_lake_mechanics_map_v0.md"
    # refs to the (now-retired) shared/ mechanics map -> workflows/
    m["orca/product/shared/data_lake_mechanics/core_spine_v0_data_lake_mechanics_map_v0.md"] = WORK + "core_spine_v0_data_lake_mechanics_map_v0.md"
    # R2 moves (contracts + planning docs) -> their new spine homes
    for _lane, old, new in MOVES:
        m[old] = new
    return m


def rewrite(content: str, mapping: dict[str, str]) -> tuple[str, int]:
    n = 0
    # longest keys first so specific file paths win over any shorter prefix
    for old in sorted(mapping, key=len, reverse=True):
        if old in content:
            n += content.count(old)
            content = content.replace(old, mapping[old])
    return content, n


def main(argv: list[str]) -> int:
    apply = "--apply" in argv
    mapping = load_rewrite_map()
    print(f"rewrite-map entries: {len(mapping)}  mode: {'APPLY' if apply else 'DRY-RUN'}\n")
    total_resid = 0
    for lane, old, new in MOVES:
        src = git_show(lane, old)
        if src is None:
            print(f"  MISSING {lane}:{old}")
            return 1
        out, n = rewrite(src, mapping)
        resid = len(re.findall(r"docs/product/", out))
        total_resid += resid
        print(f"  {old}\n    -> {new}  (refs rewritten: {n}; residual 'docs/product/' refs: {resid})")
        if apply:
            dst = ROOT / new
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_text(out, encoding="utf-8")
    print(f"\nfiles: {len(MOVES)}  total residual docs/product refs after rewrite: {total_resid}")
    if total_resid:
        print("  (residual = dir-level or unmapped refs; inspect before commit — files live under orca/ so they are not check_map_links-scanned, but should read correctly)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
