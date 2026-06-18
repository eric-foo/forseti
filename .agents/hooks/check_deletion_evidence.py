#!/usr/bin/env python3
"""Deletion-evidence gate (Phase-2 deletion safety) -- STRICT CI gate.

WHAT THIS DOES
  Fails (exit 1, --strict) when a GOVERNED artifact (one under GOVERNED_ROOTS)
  is deleted in this PR's diff without a complete evidence record in the
  deletion-evidence register. "Deleted" includes a rename that moves a governed
  artifact OUT of every governed root (it left its governed home); a rename that
  keeps it under a governed root is a move, not a deletion, and needs no record.

  The frozen Orca rule: a governed-artifact deletion is central-adjudicated and
  carries evidence -- reverse-reference check + successor + semantic delta +
  rollback. Adjudication is the existing router->human-merge flow (a deleting PR
  is routed `risk/manual-review-required`); this gate makes the EVIDENCE
  mechanically mandatory, so an unevidenced governed deletion cannot land green
  on either merge path (the bot honors the router label; the in-session
  self-merge guard requires a green CI rollup, which a finding here turns red).

WHY STRICT (not report-mode)
  Report-mode (exit 0) gives no safety here: a green CI lets the self-merge
  guard land an unevidenced deletion. Only a red check closes that path. The
  gate is born GREEN -- with no governed deletions in a diff it exits 0 -- so
  adopting strict now matches the clean state without a red-main event (the
  strict predicate equals the report predicate on the current corpus).

WHY THE GOVERNED SCOPE IS CODE-OWNED
  GOVERNED_ROOTS lives here, not in the register, so the register (mutable data)
  cannot narrow or remove its own governance by being edited or deleted. The
  register holds deletion RECORDS only; this checker owns what is governed.

WHY PROVENANCE IS NOT IN THE RECORD
  Who deleted what, when, and in which commit is authoritatively recorded by
  git. The register holds only what git cannot derive: the human judgment
  evidence (reverse_ref_check, semantic_delta) and the declared successor /
  rollback. Single authoritative home per fact; smallest forgeable surface.

DETECTION CONTRACT (mirrors header_index.py --strict)
  base ref priority: $GITHUB_BASE_REF -> origin/<ref>; else --base <ref>; else
  origin/main. Diff is three-dot `base...HEAD` (merge-base diff = the PR's net
  change). Rename-aware via --find-renames. NO HEAD~1 fallback (which would see
  only the last commit of a multi-commit lane). If the base cannot be resolved
  or git fails, fail OPEN (exit 0, loud warning) -- the universal Orca infra-gap
  stance; in CI the base is always present (fetch-depth: 0).

HARD BOUNDARY
  Read-only. Fail-open ONLY for infrastructure gaps (no git, no PyYAML, base
  unresolvable). A PRESENT register that is unparseable, or a governed deletion
  with a missing/incomplete record, or a declared successor that does not
  resolve, is a real finding -- never fail-open. A MISSING register is treated
  as an empty register (so governed deletions become findings), not a skip.

MODES
  check_deletion_evidence.py --strict     fail (exit 1) on findings; CI gate
  check_deletion_evidence.py --report     same findings, advisory (exit 0)
  check_deletion_evidence.py --check      alias for --report
  check_deletion_evidence.py --selftest   pure-function cases; exit 0/1

Doctrine + register:
  docs/decisions/deletion_evidence_doctrine_v0.md
  docs/decisions/deletion_evidence_register_v0.yaml
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

# Governed scope -- code-owned SSOT (see "WHY THE GOVERNED SCOPE IS CODE-OWNED").
# A trailing slash means "this directory and everything under it".
GOVERNED_ROOTS = ("orca/product/",)

REGISTER_REL = "docs/decisions/deletion_evidence_register_v0.yaml"
EVIDENCE_FIELDS = ("reverse_ref_check", "successor", "semantic_delta", "rollback")
# Explicit literal that declares "there is no replacement -- this is pure bloat".
# Any other successor value must resolve to a real path in the tree.
NO_SUCCESSOR = "none -- pure bloat"


def repo_root() -> Path:
    """Repo root, derived from this file's location (.agents/hooks/<this>)."""
    return Path(__file__).resolve().parents[2]


# ---------------------------------------------------------------------------
# Pure predicates (testable)
# ---------------------------------------------------------------------------

def is_governed(path: str, roots: tuple[str, ...] = GOVERNED_ROOTS) -> bool:
    """True if `path` is at or under a governed root."""
    return any(path == r.rstrip("/") or path.startswith(r) for r in roots)


def record_is_complete(rec: object) -> bool:
    """True iff `rec` is a well-formed deletion record under the minimal schema:
    `targets` a non-empty list of non-empty path strings, and all four evidence
    fields present and non-empty. No phase, no provenance -- those are not part
    of the schema (provenance lives in git; there is no lifecycle to transition)."""
    if not isinstance(rec, dict):
        return False
    targets = rec.get("targets")
    if not isinstance(targets, list) or not targets:
        return False
    if not all(isinstance(t, str) and t.strip() for t in targets):
        return False
    ev = rec.get("evidence")
    if not isinstance(ev, dict):
        return False
    return all(isinstance(ev.get(f), str) and ev.get(f, "").strip() for f in EVIDENCE_FIELDS)


def complete_records(register: object) -> list[dict]:
    """All complete records in the register (order preserved)."""
    if not isinstance(register, dict):
        return []
    return [r for r in (register.get("deletions") or []) if record_is_complete(r)]


def covered_targets(register: object) -> set[str]:
    """Repo-relative paths covered by a complete record."""
    out: set[str] = set()
    for rec in complete_records(register):
        out.update(t.strip() for t in rec["targets"])
    return out


def record_for_target(register: object, path: str) -> dict | None:
    """The latest complete record whose targets include `path` (latest wins, so a
    correction can supersede an earlier record without rewriting history)."""
    found: dict | None = None
    for rec in complete_records(register):
        if path in (t.strip() for t in rec["targets"]):
            found = rec
    return found


def successor_resolves(rec: dict, root: Path) -> bool:
    """True if the record's declared successor is the no-successor sentinel or a
    path that exists in the working tree. A successor that names a non-existent
    path is a machine-detectable false evidence claim."""
    successor = (rec.get("evidence") or {}).get("successor", "")
    successor = successor.strip()
    if successor == NO_SUCCESSOR:
        return True
    # Tolerate a successor written as a quoted/backticked path or with a trailing
    # note; resolve the first whitespace-delimited token as the candidate path.
    candidate = successor.strip("`'\" ").split()[0] if successor else ""
    return bool(candidate) and (root / candidate).exists()


# ---------------------------------------------------------------------------
# Git deletion detection (rename-aware, merge-base scoped)
# ---------------------------------------------------------------------------

def _git(root: Path, args: list[str], timeout: int = 15) -> tuple[int, str]:
    """Run a git command; return (returncode, stdout). Never raises; returns
    (-1, "") on any git failure (an infra gap -> fail-open upstream)."""
    try:
        res = subprocess.run(
            ["git", "-C", str(root), *args],
            capture_output=True, text=True, timeout=timeout,
        )
        return res.returncode, res.stdout
    except (FileNotFoundError, OSError, subprocess.TimeoutExpired):
        return -1, ""


def resolve_base_ref(cli_base: str | None) -> str:
    """Base ref for diff-scoping (mirrors header_index.py):
    1. $GITHUB_BASE_REF -> "origin/<value>"
    2. --base <ref> CLI arg
    3. default "origin/main"
    No HEAD~1 fallback -- that would see only the last commit of a multi-commit lane."""
    gh_base = os.environ.get("GITHUB_BASE_REF", "").strip()
    if gh_base:
        return "origin/%s" % gh_base
    if cli_base:
        return cli_base
    return "origin/main"


def parse_governed_deletions(name_status: str, roots: tuple[str, ...]) -> list[str]:
    """Parse `git diff --diff-filter=DR --find-renames --name-status` output into
    the list of governed paths that were DELETED (left their governed home).

    - `D\tpath`            -> deletion of `path`.
    - `R<score>\told\tnew` -> rename; a deletion only if `old` is governed and
                              `new` is NOT governed (the artifact left governance).
                              A governed->governed rename is a move (exempt).

    Pure function (testable)."""
    out: list[str] = []
    for line in name_status.splitlines():
        line = line.rstrip("\n")
        if not line.strip():
            continue
        parts = line.split("\t")
        status = parts[0].strip()
        if status.startswith("D") and len(parts) >= 2:
            path = parts[1].strip()
            if is_governed(path, roots):
                out.append(path)
        elif status.startswith("R") and len(parts) >= 3:
            old, new = parts[1].strip(), parts[2].strip()
            if is_governed(old, roots) and not is_governed(new, roots):
                out.append(old)
    # De-dup, preserve order.
    seen: set[str] = set()
    deduped: list[str] = []
    for p in out:
        if p not in seen:
            seen.add(p)
            deduped.append(p)
    return deduped


def deleted_governed_paths(root: Path, base_ref: str, roots: tuple[str, ...]) -> list[str] | None:
    """Governed paths deleted in `base_ref...HEAD` (rename-aware). None on a git
    infra gap (fail-open): no HEAD, or the diff cannot be computed against base."""
    if _git(root, ["rev-parse", "--verify", "--quiet", "HEAD"])[0] != 0:
        return None  # not a git repo / no HEAD -> infra gap
    if _git(root, ["rev-parse", "--verify", "--quiet", base_ref])[0] != 0:
        return None  # base ref unresolvable -> infra gap (fail-open, like header_index)
    rc, out = _git(
        root,
        ["diff", "--diff-filter=DR", "--find-renames", "--name-status", "%s...HEAD" % base_ref],
    )
    if rc != 0:
        return None
    return parse_governed_deletions(out, roots)


# ---------------------------------------------------------------------------
# Gate
# ---------------------------------------------------------------------------

def check_deletions(root: Path, cli_base: str | None = None) -> tuple[list[str], str | None]:
    """Return (findings, skip_reason). Fail-open: a non-None skip_reason marks an
    infra gap and findings is []. A missing register is NOT a skip -- it is an
    empty register, so governed deletions become findings (a deleted register
    cannot un-govern the corpus)."""
    try:
        import yaml
    except Exception:
        return [], "PyYAML unavailable"

    base_ref = resolve_base_ref(cli_base)
    deleted = deleted_governed_paths(root, base_ref, GOVERNED_ROOTS)
    if deleted is None:
        return [], "git/diff unavailable (base '%s')" % base_ref
    if not deleted:
        return [], None  # born green: nothing governed deleted in this diff

    reg_path = root / REGISTER_REL
    if not reg_path.is_file():
        register: object = {"deletions": []}  # absent -> empty (DLR-05): findings follow
    else:
        try:
            register = yaml.safe_load(reg_path.read_text(encoding="utf-8")) or {"deletions": []}
        except Exception as exc:
            return ["register: cannot parse %s (%s)" % (REGISTER_REL, exc)], None

    covered = covered_targets(register)
    findings: list[str] = []
    for path in deleted:
        if path not in covered:
            findings.append(
                "governed deletion without a complete evidence record: %s" % path
            )
            continue
        rec = record_for_target(register, path)
        if rec is not None and not successor_resolves(rec, root):
            findings.append(
                "evidence successor does not resolve for %s: successor=%r "
                "(use a real path or the literal %r)"
                % (path, (rec.get("evidence") or {}).get("successor", ""), NO_SUCCESSOR)
            )
    return findings, None


def run(root: Path, strict: bool, cli_base: str | None) -> int:
    findings, skip = check_deletions(root, cli_base)
    mode = "--strict" if strict else "--report"
    if skip:
        print("check_deletion_evidence %s: fail-open (infra gap): %s -- nothing to gate"
              % (mode, skip))
        return 0
    if findings:
        print("check_deletion_evidence %s: %d governed deletion finding(s):"
              % (mode, len(findings)))
        for f in findings:
            print("  " + f)
        return 1 if strict else 0
    print("check_deletion_evidence %s: OK -- every governed deletion in this diff "
          "carries a complete evidence record" % mode)
    return 0


# ---------------------------------------------------------------------------
# Selftest
# ---------------------------------------------------------------------------

def selftest() -> int:
    ok = True

    def check(label: str, got, exp):
        nonlocal ok
        status = "PASS" if got == exp else "FAIL"
        if got != exp:
            ok = False
        print("%s  %-52s got=%s" % (status, label, got))

    # --- record_is_complete (minimal schema: targets + 4 evidence) ---
    complete = {
        "targets": ["orca/product/x_v0.md"],
        "evidence": {f: "a non-empty narrative" for f in EVIDENCE_FIELDS},
    }
    check("complete record", record_is_complete(complete), True)
    check("missing evidence field",
          record_is_complete({**complete, "evidence": {"reverse_ref_check": "x"}}), False)
    check("empty targets", record_is_complete({**complete, "targets": []}), False)
    check("blank evidence value",
          record_is_complete({**complete, "evidence": {**complete["evidence"], "rollback": "  "}}), False)
    check("non-dict record", record_is_complete(["not", "a", "dict"]), False)
    # Provenance is NOT part of the schema -- a record with extra provenance still
    # passes (extra keys are ignored), and one WITHOUT it still passes (not required).
    check("provenance not required",
          record_is_complete({**complete, "proposed_by": "lane"}), True)

    reg = {"deletions": [complete, {"targets": ["orca/product/y.md"]}]}  # 2nd is incomplete
    check("covered_targets (complete only)", covered_targets(reg), {"orca/product/x_v0.md"})

    # --- is_governed ---
    check("governed inside root", is_governed("orca/product/a/b.md"), True)
    check("governed root exact", is_governed("orca/product"), True)
    check("not governed", is_governed("docs/decisions/z.md"), False)

    # --- parse_governed_deletions (rename-aware) ---
    roots = ("orca/product/",)
    ns = "\n".join([
        "D\torca/product/deleted.md",                              # governed delete
        "D\tdocs/decisions/ungoverned.md",                         # not governed -> ignored
        "R100\torca/product/old.md\torca/product/sub/new.md",      # governed->governed move -> exempt
        "R090\torca/product/leaving.md\tdocs/archive/leaving.md",  # governed->outside -> deletion
        "R095\tdocs/x.md\torca/product/incoming.md",               # outside->governed -> not a deletion
    ])
    check("rename-aware governed deletions",
          parse_governed_deletions(ns, roots),
          ["orca/product/deleted.md", "orca/product/leaving.md"])
    check("empty diff -> no deletions", parse_governed_deletions("", roots), [])

    # --- successor_resolves (sentinel + path resolution) ---
    root = repo_root()
    check("successor sentinel resolves",
          successor_resolves({"evidence": {"successor": NO_SUCCESSOR}}, root), True)
    check("successor real path resolves",
          successor_resolves({"evidence": {"successor": "AGENTS.md"}}, root), True)
    check("successor bogus path fails",
          successor_resolves({"evidence": {"successor": "orca/product/does_not_exist_zzz.md"}}, root), False)

    print()
    print("SELFTEST", "OK" if ok else "FAILED")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()
    try:
        root = repo_root()
    except Exception as exc:
        sys.stderr.write("check_deletion_evidence: cannot determine repo root: %s\n" % exc)
        return 0
    cli_base: str | None = None
    if "--base" in argv:
        idx = argv.index("--base")
        if idx + 1 < len(argv):
            cli_base = argv[idx + 1]
    if "--strict" in argv:
        return run(root, strict=True, cli_base=cli_base)
    if "--report" in argv or "--check" in argv:
        return run(root, strict=False, cli_base=cli_base)
    print("Usage: check_deletion_evidence.py --strict | --report | --check | --selftest [--base <ref>]")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as exc:  # never ghost-fail; print and fail open
        sys.stderr.write("check_deletion_evidence: internal error, allowing: %s\n" % exc)
        sys.exit(0)
