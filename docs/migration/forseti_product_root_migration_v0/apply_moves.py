#!/usr/bin/env python3
"""Forseti product-root migration helper.

Dry-run/apply/reverse helper for docs/migration/forseti_product_root_migration_v0.
The lane commit remains the durable record; this helper is intentionally small
and manifest-driven.
"""
from __future__ import annotations

import argparse
import csv
import subprocess
from pathlib import Path

PKG = Path(__file__).resolve().parent
ROOT = PKG.parents[2]
MANIFEST = PKG / "moves_manifest.csv"


def git(args: list[str]) -> tuple[int, str]:
    res = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True)
    return res.returncode, (res.stdout or "") + (res.stderr or "")


def rows() -> list[dict[str, str]]:
    with MANIFEST.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def partition(data: list[dict[str, str]]):
    pending, applied, problem = [], [], []
    for row in data:
        old = ROOT / row["old_path"]
        new = ROOT / row["new_path"]
        if old.exists() and not new.exists():
            pending.append(row)
        elif not old.exists() and new.exists():
            applied.append(row)
        else:
            problem.append(row)
    return pending, applied, problem


def dry_run() -> int:
    data = rows()
    pending, applied, problem = partition(data)
    print(f"DRY RUN: {len(pending)} pending, {len(applied)} already applied, {len(problem)} problem row(s)")
    for row in problem[:20]:
        print(f"  problem: old={row['old_path']} new={row['new_path']}")
    if len(problem) > 20:
        print(f"  ... {len(problem) - 20} more problem rows")
    return 1 if problem else 0


def apply() -> int:
    if dry_run() != 0:
        return 1
    pending, _, _ = partition(rows())
    for row in pending:
        (ROOT / row["new_path"]).parent.mkdir(parents=True, exist_ok=True)
        rc, out = git(["mv", row["old_path"], row["new_path"]])
        if rc != 0:
            print(out.strip())
            return rc
    return 0


def reverse() -> int:
    data = rows()
    moved = 0
    for row in reversed(data):
        old = ROOT / row["old_path"]
        new = ROOT / row["new_path"]
        if new.exists() and not old.exists():
            old.parent.mkdir(parents=True, exist_ok=True)
            rc, out = git(["mv", row["new_path"], row["old_path"]])
            if rc != 0:
                print(out.strip())
                return rc
            moved += 1
    print(f"reversed {moved} path(s)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--reverse", action="store_true")
    args = parser.parse_args()
    if args.apply:
        return apply()
    if args.reverse:
        return reverse()
    return dry_run()


if __name__ == "__main__":
    raise SystemExit(main())
