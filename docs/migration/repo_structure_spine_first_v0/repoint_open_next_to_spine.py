#!/usr/bin/env python3
"""Repoint open_next retrieval metadata from docs/product/... to orca/product/...

A-prime scope (owner-authorized 2026-06-18): live navigation must resolve
directly; historical body prose / provenance text may stay point-in-time. This
script rewrites ONLY the open_next entries inside the FIRST fenced-yaml
retrieval header of each .md file under docs/ and .agents/ -- the exact surface
check_map_links C2 gates. It does not touch body prose, inline links, or any
path token outside an open_next list item.

Mapping comes from the generated moved_paths_index.md (sibling file). The one
RETIRED entry (docs/product/search/README.md -> RETIRED_NO_SUCCESSOR) has no
successor: its open_next occurrences are annotated with the check_map_links
"# nonresolving:" convention (pointing at the moved-paths index) rather than
repointed to an invented target.

Idempotent: a repointed (orca/product) entry is no longer an index old-path, so
re-running is a no-op; an already-annotated nonresolving line is left as-is.

Boundary mirrors .agents/hooks/check_map_links.py parse_open_next: fenced-yaml
block only, open_next list, a new top-level key ends the block, only the first
yaml header is treated as the retrieval header.

Modes:
  --dry-run   (default) report planned changes; write nothing
  --apply     write changes in place
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

# moved_paths_index lives beside this file; repo root is parents[3]
# (docs/migration/repo_structure_spine_first_v0/<this>.py).
_HERE = Path(__file__).resolve()


def repo_root() -> Path:
    return _HERE.parents[3]


def index_path() -> Path:
    return _HERE.parent / "moved_paths_index.md"


_ROW_RE = re.compile(r"^\|\s*`([^`]+)`\s*\|\s*`([^`]+)`\s*\|\s*$")
_RETIRED_RE = re.compile(r"^(\S+)\s*->\s*RETIRED_NO_SUCCESSOR\s*$")

NONRESOLVING_NOTE = (
    "nonresolving: retired without successor; resolve via "
    "docs/migration/repo_structure_spine_first_v0/moved_paths_index.md"
)

SKIP_DIRS = {"_scratch", "_inbox", "node_modules"}


def load_index(path: Path) -> tuple[dict[str, str], set[str]]:
    """Return (old->new mapping, retired old-path set) from moved_paths_index.md."""
    mapping: dict[str, str] = {}
    retired: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        m = _ROW_RE.match(s)
        if m:
            mapping[m.group(1).strip()] = m.group(2).strip()
            continue
        r = _RETIRED_RE.match(s)
        if r:
            retired.add(r.group(1).strip())
    return mapping, retired


def iter_md_files(root: Path):
    for base in ("docs", ".agents"):
        search_root = root / base
        if not search_root.is_dir():
            continue
        for dirpath, dirnames, filenames in os.walk(search_root):
            dirnames[:] = [
                d for d in dirnames if d not in SKIP_DIRS and "_scratch" not in d
            ]
            for fname in filenames:
                if fname.endswith(".md"):
                    yield Path(dirpath) / fname


def parse_entry(item: str) -> tuple[str, str]:
    """item = open_next list text after the leading '- '. Return (path, comment).

    path: surrounding quotes stripped. comment: text after the first ' # '.
    """
    raw = item
    comment = ""
    pos = raw.find(" # ")
    if pos != -1:
        comment = raw[pos + 3:].strip()
        raw = raw[:pos].strip()
    return raw.strip("\"'").strip(), comment


def _split_eol(line: str) -> tuple[str, str]:
    if line.endswith("\r\n"):
        return line[:-2], "\r\n"
    if line.endswith("\n"):
        return line[:-1], "\n"
    return line, ""


def process_file(fpath: Path, mapping: dict[str, str], retired: set[str]):
    """Return (changed, repointed, annotated, unmapped_paths, new_lines)."""
    try:
        lines = fpath.read_text(encoding="utf-8", errors="replace").splitlines(keepends=True)
    except OSError:
        return False, 0, 0, [], None

    in_yaml = False
    in_open_next = False
    repointed = 0
    annotated = 0
    unmapped: list[str] = []
    changed = False

    # Bound to the first 40 lines = exact parity with check_map_links C2 scope.
    # The checker reads only the header region across ALL yaml blocks in it
    # (e.g. a review_summary block followed by the retrieval_header block), so
    # this must not stop at the first block; the 40-line cap keeps body example
    # yaml blocks out of scope.
    for i, raw_line in enumerate(lines):
        if i >= 40:
            break
        body, _eol = _split_eol(raw_line)
        stripped = body.strip()

        if stripped.startswith("```"):
            if not in_yaml and ("yaml" in stripped.lower() or stripped == "```"):
                in_yaml = True
            elif in_yaml:
                in_yaml = False
                in_open_next = False
            continue

        if not in_yaml:
            continue

        if stripped.startswith("open_next:"):
            in_open_next = True
            continue

        if not in_open_next:
            continue

        # a new top-level key ends the open_next block
        if stripped and not stripped.startswith("-") and ":" in stripped and not stripped.startswith("#"):
            if not stripped.split(":")[0].strip().startswith("-"):
                in_open_next = False
                continue

        if not stripped.startswith("- "):
            continue

        path, _comment = parse_entry(stripped[2:].strip())
        if not ("/" in path or path.endswith(".md")):
            continue

        if path in mapping:
            new_line = raw_line.replace(path, mapping[path])
            if new_line != raw_line:
                lines[i] = new_line
                repointed += 1
                changed = True
        elif path in retired:
            if "nonresolving:" not in body:
                b, eol = _split_eol(raw_line)
                lines[i] = b + " # " + NONRESOLVING_NOTE + eol
                annotated += 1
                changed = True
        elif path.startswith("docs/product/") and "nonresolving:" not in body:
            # docs/product target not in the index and not already annotated:
            # a genuine residual to surface (already-annotated debt is skipped).
            unmapped.append(path)

    return changed, repointed, annotated, unmapped, lines


def main(argv: list[str]) -> int:
    apply = "--apply" in argv
    root = repo_root()
    mapping, retired = load_index(index_path())

    total_files = 0
    total_repointed = 0
    total_annotated = 0
    all_unmapped: list[tuple[str, str]] = []

    for fpath in iter_md_files(root):
        changed, repointed, annotated, unmapped, new_lines = process_file(
            fpath, mapping, retired
        )
        rel = fpath.relative_to(root).as_posix()
        for p in unmapped:
            all_unmapped.append((rel, p))
        if changed:
            total_files += 1
            total_repointed += repointed
            total_annotated += annotated
            print("%-90s  repoint=%d annotate=%d" % (rel, repointed, annotated))
            if apply and new_lines is not None:
                fpath.write_text("".join(new_lines), encoding="utf-8")

    print("")
    print("mode: %s" % ("APPLY" if apply else "DRY-RUN"))
    print("index rows: %d  retired: %d" % (len(mapping), len(retired)))
    print("files changed: %d" % total_files)
    print("open_next entries repointed: %d" % total_repointed)
    print("retired entries annotated nonresolving: %d" % total_annotated)
    if all_unmapped:
        print("UNMAPPED docs/product open_next paths (NOT rewritten, residual):")
        for rel, p in all_unmapped:
            print("  %s :: %s" % (rel, p))
    else:
        print("unmapped docs/product open_next paths: 0")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
