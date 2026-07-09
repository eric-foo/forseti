#!/usr/bin/env python3
"""Repo-map freshness boundary check (forward-only, with repo-map commit interrupt).

WHAT THIS ENFORCES
  The *structural* subset of the repo map's own ``stale_if:`` block - the
  conditions that are mechanically detectable at a tool boundary. The rule (what
  makes the map stale, and what the map covers) is owned by:

      docs/workflows/orca_repo_map_v0.md   (its ``stale_if:`` header + tables)

  This script does NOT restate that rule. It reads the map AS ITS OWN SPEC: the
  set of paths the map already names is "what is covered," and a touched path
  that introduces new navigable structure NOT present in the map trips the
  tripwire. If the map and this checker ever disagree, the map wins and this
  checker is the stale party.

WHY THIS EXISTS (enforcement placement)
  "Update the repo map" was carried only by instruction, so a capable agent
  could add a new top-level folder or a new harness runner and nothing would
  notice at the moment the map went stale - the omission surfaced only later, as
  a wrong route. Per the Enforcement Placement principle in
      .agents/workflow-overlay/validation-gates.md  (-> "Enforcement Placement")
  a load-bearing, mechanically-checkable rule is enforced at the boundary (a
  write-time hook + this portable checker), not left to end-of-thread memory.

  Honest boundary: this catches STRUCTURAL omission (new top-level folder, new
  harness runner/adapter) - ``stale_if`` #1 and #2 - with a hard commit gate, and
  nudges (advisory only) on source-of-truth edits (#5). It does NOT judge whether
  an ordinary content file "deserves" a route, and it cannot detect "a spine was
  materially reorganized" (#3) or "routing doctrine changed" (#4): those stay
  judgment, backstopped by the Doctrine Change Propagation contract in
  .agents/workflow-overlay/source-of-truth.md, which already lists the repo map
  as a downstream surface to check. A clean run is not proof the map is complete.

ACKNOWLEDGING A LEGITIMATE NON-MAP CHANGE (so --strict passes)
  - One-off ("this specific new thing is not a navigation target"): put a
    ``repo-map-ack: <reason>`` line in the commit message. Ephemeral by design;
    the reason lives in that commit's history. Read via --commit-msg / --message.
  - Recurring class ("this whole kind of thing is never mapped, e.g. generated
    scratch"): add a backtick'd token to the map's
    "Generated/gitignored scratch - do not enumerate" list. This checker reads
    that list as its exclusion source, so the map stays the single source of
    truth for its own boundaries - no separate ledger that can itself rot.

MODES
  check_repo_map_freshness.py <path> ...        advisory; warns, exit 0
  check_repo_map_freshness.py --strict <path>   exit 1 if a structural trigger
                                                fires and no map/submap touched
                                                and no ack
  check_repo_map_freshness.py --staged [--strict]   check git-staged files
  check_repo_map_freshness.py --changed [--strict]  changed + untracked
  check_repo_map_freshness.py --commit-msg FILE     commit-msg hook (staged +
                                                    strict + ack from FILE)
  check_repo_map_freshness.py --message "TEXT"      ack source for CI
  check_repo_map_freshness.py --diff BASE [--strict] compare BASE...HEAD (PR diff)
  check_repo_map_freshness.py --hook                PostToolUse hook (stdin JSON):
                                                    exits 2 when the repo map
                                                    itself is dirty after edit;
                                                    other notices exit 0
  check_repo_map_freshness.py --selftest            run the pure-decision cases

  Commit gate (local, commit-msg hook):
      python .agents/hooks/check_repo_map_freshness.py --commit-msg "$1"
  CI gate (POSIX), against the PR base (fetch the base ref first):
      python3 .agents/hooks/check_repo_map_freshness.py --diff origin/main --strict --message "$PR_BODY"

This checker is boundary tooling, not validation, readiness, approval, or
source-of-truth promotion. It enforces map *shape* and the repo-map immediate
commit interrupt, never the truth of any route. On any internal error it fails
OPEN, so a bug here can never block a commit.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import subprocess
import sys
from pathlib import Path

# Authority this checker references (it does not restate the rule).
MAP = "docs/workflows/orca_repo_map_v0.md"
PRINCIPLE = ".agents/workflow-overlay/validation-gates.md (Enforcement Placement)"
DCP = ".agents/workflow-overlay/source-of-truth.md (Doctrine Change Propagation)"

# Updating any of these in the same change satisfies the gate: the main map, or a
# consolidation submap the main map delegates structural detail to.
SUBMAPS = (
    "docs/workflows/data_capture_spine_consolidation_map_v0.md",
    "docs/research/judgment-spine/judgment_spine_consolidation_map_v0.md",
)
MAP_SURFACES = (MAP,) + SUBMAPS

# Source-of-truth structural edits are an ADVISORY nudge only (stale_if #5), never
# a hard block: the file is edited often and "did the hierarchy change?" is a
# judgment question. High-precision-only in the strict gate keeps false blocks ~0.
SOURCE_OF_TRUTH = ".agents/workflow-overlay/source-of-truth.md"

# Harness subtrees whose new units (runners/adapters) the map names explicitly, so
# a new basename absent from the map text is a high-precision staleness signal.
HARNESS_UNIT_GLOBS = (
    "forseti-harness/runners/*.py",
    "forseti-harness/adapters/*.py",
)

# Always-excluded noise (scratch, skill copies, project config, VCS). The map's
# own "do not enumerate" list is merged on top of this at runtime.
DEFAULT_EXCLUDES = (
    ".git/",
    ".claude/",
    ".agents/skills/",
    "docs/_inbox/",
    "forseti-harness/_test_runs/",
    "forseti-harness/_auth_state/",
    "memory/logs/",
)
# Substrings that mark a path as generated/scratch regardless of where they sit.
DEFAULT_EXCLUDE_SUBSTR = ("_dry_run", "/scores/", "/__pycache__/", "pytest_")

# Repo-root areas that are never map navigation targets (so a write under them is
# not a "new top-level folder").
IGNORED_ROOT_AREAS = {".git", ".claude", "node_modules"}

_ACK_RE = re.compile(r"repo-map-ack\s*:\s*(.+)", re.I)
_PATCH_PATH_RE = re.compile(r"^\*\*\* (?:Add|Update|Delete) File: (.+)$")
_PATCH_MOVE_RE = re.compile(r"^\*\*\* Move to: (.+)$")
HEAD_LINES_FOR_HOOK = None  # the map is read in full; it is the spec, not the target


def repo_root() -> Path:
    """Repo root, derived from this file's location (.agents/hooks/<this>)."""
    return Path(__file__).resolve().parents[2]


def to_relposix(target: str, root: Path) -> str | None:
    """Repo-relative POSIX path for a target, or None if outside the repo."""
    p = Path(target)
    if p.is_absolute():
        try:
            rel = p.resolve().relative_to(root)
        except (ValueError, OSError):
            return None
        return rel.as_posix()
    s = Path(target).as_posix()
    return s[2:] if s.startswith("./") else s


def event_candidate_paths(data: dict) -> list[str]:
    """Write-target paths from a Claude/Codex-like tool event.

    Claude-style Write/Edit/MultiEdit payloads carry ``tool_input.file_path``.
    Codex ``apply_patch`` payloads carry the patch text in ``tool_input.command``;
    parse patch headers so the same checker can run as a Codex PostToolUse hook.
    """
    try:
        tool_input = data.get("tool_input") or {}
    except AttributeError:
        return []

    out: list[str] = []
    file_path = tool_input.get("file_path")
    if isinstance(file_path, str) and file_path:
        out.append(file_path)

    patch_text = tool_input.get("command") or tool_input.get("patch") or ""
    if isinstance(patch_text, str) and patch_text:
        for line in patch_text.splitlines():
            match = _PATCH_PATH_RE.match(line) or _PATCH_MOVE_RE.match(line)
            if match:
                out.append(match.group(1).strip())

    deduped: list[str] = []
    for path in out:
        if path not in deduped:
            deduped.append(path)
    return deduped


# --- the map is the spec ----------------------------------------------------

def read_map_text(root: Path) -> str:
    """Full text of the repo map (its tables + stale_if are the spec). '' if absent."""
    try:
        return (root / MAP).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def map_excludes(map_text: str) -> tuple[str, ...]:
    """Backtick'd tokens from the map's "do not enumerate" scratch list.

    These are treated as substring exclusions (over-excluding scratch is safe;
    we would rather skip a generated file than block on it). Editing that list in
    the map is the supported way to register a recurring, durable exclusion.
    """
    if not map_text:
        return ()
    m = re.search(r"do not enumerate[^\n]*\n(.*?)(?:\n\n|\n#)", map_text,
                  re.I | re.S)
    if not m:
        return ()
    return tuple(t.strip().strip("/").lower()
                 for t in re.findall(r"`([^`]+)`", m.group(1)) if t.strip())


def is_excluded(relposix: str, extra: tuple[str, ...]) -> bool:
    low = relposix.lower()
    if any(low.startswith(p) for p in DEFAULT_EXCLUDES):
        return True
    if any(s in low for s in DEFAULT_EXCLUDE_SUBSTR):
        return True
    # Map-derived scratch tokens: glob if it looks globby, else substring.
    for tok in extra:
        if any(ch in tok for ch in "*?[") and fnmatch.fnmatch(low, "*" + tok + "*"):
            return True
        if tok and tok in low:
            return True
    return False


def _area_of(relposix: str) -> str | None:
    """The map "area" a path belongs to (docs/<x>, .agents/<x>, or <root-dir>)."""
    segs = relposix.split("/")
    if len(segs) < 2:  # a bare repo-root file is not a new *folder*
        return None
    head = segs[0]
    if head in ("docs", ".agents") and len(segs) >= 2:
        return head + "/" + segs[1]
    if head in IGNORED_ROOT_AREAS:
        return None
    return head


def new_top_level_area(relposix: str, map_text: str) -> str | None:
    """Return the area if `relposix` lives in structure absent from the map."""
    area = _area_of(relposix)
    if area is None:
        return None
    # High precision: a genuinely new top-level area name is not a substring of
    # the map text. (Documented areas like `.agents/hooks` already appear there.)
    return None if area.lower() in map_text.lower() else area


def new_harness_unit(relposix: str, map_text: str) -> str | None:
    """Return the path if it is a harness runner/adapter the map does not name."""
    name = Path(relposix).name
    if name == "__init__.py":
        return None
    if not any(fnmatch.fnmatch(relposix, g) for g in HARNESS_UNIT_GLOBS):
        return None
    return None if name.lower() in map_text.lower() else relposix


def structural_trigger(relposix: str, map_text: str,
                       extra: tuple[str, ...]) -> str | None:
    """High-precision staleness signal for a path, or None. Used by the gate."""
    if relposix in MAP_SURFACES:
        return None  # a map/submap is the resolution surface, never a trigger
    if is_excluded(relposix, extra):
        return None
    area = new_top_level_area(relposix, map_text)
    if area is not None:
        return ("new top-level area `%s/` is not in the repo map "
                "(stale_if #1)" % area)
    unit = new_harness_unit(relposix, map_text)
    if unit is not None:
        return ("new harness unit `%s` is not named in the repo map's "
                "Forseti Harness section (stale_if #2)" % unit)
    return None


def advisory_only(relposix: str) -> str | None:
    """Coarse, never-blocking nudge for a touched path, or None."""
    if relposix == SOURCE_OF_TRUTH:
        return ("`%s` changed - if the source hierarchy or the doctrine-change "
                "propagation contract changed, the repo map's stale_if #5 may "
                "have tripped; confirm the map still routes correctly." % relposix)
    return None


def commit_nudge(relposix: str) -> str | None:
    """Per-edit reminder for the repo map itself: it is a high-contention
    commit-once-whole shared file, so an edit should be committed immediately,
    explicit-path, before other lanes' interleaving edits get swept into an
    unrelated commit. Fires on ANY edit to the map (distinct from the
    structural/freshness check, which fires on OTHER files adding structure)."""
    if relposix != MAP:
        return None
    return ("you edited the repo map (a high-contention commit-once-whole shared "
            "file). Commit it now, explicit-path, before other lanes' edits "
            "interleave: `git commit --only -- " + MAP + "`.")


# --- git plumbing -----------------------------------------------------------

def git_lines(root: Path, args: list[str]) -> list[str]:
    try:
        out = subprocess.run(["git", "-C", str(root), *args],
                             capture_output=True, text=True)
    except (FileNotFoundError, OSError):
        return []
    if out.returncode != 0:
        return []
    return [ln.strip() for ln in out.stdout.splitlines() if ln.strip()]


def map_is_dirty(root: Path) -> bool:
    """True when the repo map is staged or unstaged dirty."""
    return bool(git_lines(root, ["status", "--porcelain", "--", MAP]))


def _dedup(*groups: list[str]) -> list[str]:
    seen: list[str] = []
    for g in groups:
        for p in g:
            if p not in seen:
                seen.append(p)
    return seen


def added_paths(root: Path, staged: bool, changed: bool) -> list[str]:
    """New/renamed files (the 'new structure' signal)."""
    groups: list[list[str]] = []
    if staged or changed:
        groups.append(git_lines(root, ["diff", "--cached", "--name-only",
                                        "--diff-filter=AR"]))
    if changed:
        groups.append(git_lines(root, ["diff", "--name-only", "--diff-filter=AR"]))
        groups.append(git_lines(root, ["ls-files", "--others", "--exclude-standard"]))
    return _dedup(*groups)


def touched_paths(root: Path, staged: bool, changed: bool) -> list[str]:
    """Any add/modify/rename (for the map-touched check + source-of-truth nudge)."""
    groups: list[list[str]] = []
    if staged or changed:
        groups.append(git_lines(root, ["diff", "--cached", "--name-only",
                                        "--diff-filter=ACMR"]))
    if changed:
        groups.append(git_lines(root, ["diff", "--name-only", "--diff-filter=ACMR"]))
        groups.append(git_lines(root, ["ls-files", "--others", "--exclude-standard"]))
    return _dedup(*groups)


def diff_paths(root: Path, base: str, difffilter: str) -> list[str]:
    """Files changed in BASE...HEAD (the PR diff vs the merge base). `difffilter`
    picks the git --diff-filter: AR = added/renamed (the 'new structure' signal
    feeding `added`); ACMR = any change (feeding the map-touched check via
    `touched`). This is the CI/PR entrypoint; the base ref must be fetched first."""
    return git_lines(root, ["diff", "--name-only", "--diff-filter=" + difffilter,
                            base + "...HEAD"])


def read_ack(commit_msg_file: str | None, message: str | None) -> str | None:
    """Return the ack reason from a commit-msg file or explicit message, or None."""
    text = message or ""
    if commit_msg_file:
        try:
            text += "\n" + Path(commit_msg_file).read_text(encoding="utf-8",
                                                           errors="replace")
        except OSError:
            pass
    m = _ACK_RE.search(text)
    return m.group(1).strip() if m else None


# --- run modes --------------------------------------------------------------

def run_hook(root: Path) -> int:
    """PostToolUse hook: block dirty repo-map edits; otherwise advise."""
    try:
        data = json.loads(sys.stdin.read() or "{}")
    except ValueError:
        return 0

    paths = event_candidate_paths(data)
    if not paths:
        return 0

    map_text = read_map_text(root)
    extra = map_excludes(map_text)

    notes: list[str] = []
    block = False
    for path in paths:
        rel = to_relposix(path, root)
        if rel is None:
            continue
        # Editing the map itself -> an immediate commit interrupt (its own,
        # simpler note); structural/freshness triggers only fire on OTHER files.
        nudge = commit_nudge(rel)
        if nudge:
            if map_is_dirty(root):
                block = True
                notes.append("Repo-map commit interrupt (blocking): " + nudge)
            continue

        msg = structural_trigger(rel, map_text, extra) or advisory_only(rel)
        if msg:
            notes.append(
            "Repo-map freshness (advisory, not blocking): " + msg
            + " Update " + MAP + " (or the relevant consolidation submap), or record "
            "a `repo-map-ack: <reason>` in your commit message if it is deliberately "
            "not a navigation target. Enforced at the write boundary per " + PRINCIPLE
            + "; judgment-shaped staleness stays with " + DCP + "."
            )

    if not notes:
        return 0
    deduped: list[str] = []
    for note in notes:
        if note not in deduped:
            deduped.append(note)
    note = "\n".join(deduped)
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PostToolUse", "additionalContext": note}}))
    if block:
        print(note, file=sys.stderr)
        return 2
    return 0


def evaluate(root: Path, relpaths_added: list[str], relpaths_touched: list[str],
             ack: str | None) -> tuple[list[str], list[str], bool, str | None]:
    """Return (structural_hits, advisory_hits, map_touched, ack)."""
    map_text = read_map_text(root)
    extra = map_excludes(map_text)
    structural = []
    for rel in relpaths_added:
        if rel is None:
            continue
        hit = structural_trigger(rel, map_text, extra)
        if hit:
            structural.append(hit)
    advisory = []
    for rel in relpaths_touched:
        if rel is None:
            continue
        a = advisory_only(rel)
        if a:
            advisory.append(a)
    map_touched = any(p in MAP_SURFACES for p in relpaths_touched)
    return structural, advisory, map_touched, ack


def report(structural: list[str], advisory: list[str], map_touched: bool,
           ack: str | None, strict: bool) -> int:
    for a in advisory:
        print("repo-map-freshness (advisory): " + a, file=sys.stderr)
    if not structural:
        return 0
    for s in structural:
        print("repo-map-freshness: " + s, file=sys.stderr)
    if map_touched:
        print("repo-map-freshness: a map/submap was also updated in this change "
              "- gate satisfied (shape only; entry correctness is not checked).",
              file=sys.stderr)
        return 0
    if ack:
        print("repo-map-freshness: acknowledged not-a-route via "
              "repo-map-ack: " + ack + " - gate satisfied.", file=sys.stderr)
        return 0
    print(
        "repo-map-freshness: %d structural change(s) above add navigable "
        "structure but no map/submap was updated and no `repo-map-ack:` was "
        "found. Resolve by one of: (1) add the route to %s or the relevant "
        "consolidation submap; (2) put `repo-map-ack: <reason>` in the commit "
        "message; (3) if it is recurring scratch, add it to the map's "
        "\"do not enumerate\" list. Authority: %s." % (
            len(structural), MAP, PRINCIPLE),
        file=sys.stderr)
    return 1 if strict else 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Advisory, forward-only repo-map freshness check. "
        "Spec authority: " + MAP)
    parser.add_argument("paths", nargs="*", help="explicit file paths to check")
    parser.add_argument("--staged", action="store_true", help="check git-staged files")
    parser.add_argument("--changed", action="store_true",
                        help="check changed + untracked files")
    parser.add_argument("--strict", action="store_true",
                        help="exit 1 on an unresolved structural trigger (CI/commit)")
    parser.add_argument("--commit-msg", metavar="FILE",
                        help="commit-msg hook: staged + strict + ack read from FILE")
    parser.add_argument("--message", metavar="TEXT",
                        help="explicit ack source (e.g. PR body) for CI")
    parser.add_argument("--diff", metavar="BASE",
                        help="compare BASE...HEAD, e.g. origin/main (CI/PR mode)")
    parser.add_argument("--hook", action="store_true",
                        help="PostToolUse hook mode (stdin JSON, exit 0)")
    parser.add_argument("--selftest", action="store_true", help="run decision cases")
    args = parser.parse_args(argv)

    if args.selftest:
        return selftest()

    root = repo_root()

    if args.hook:
        return run_hook(root)

    staged = args.staged or bool(args.commit_msg)
    strict = args.strict or bool(args.commit_msg)
    ack = read_ack(args.commit_msg, args.message)

    added = added_paths(root, staged, args.changed)
    touched = touched_paths(root, staged, args.changed)
    explicit = [to_relposix(p, root) for p in args.paths]
    added = _dedup(added, [p for p in explicit if p])
    touched = _dedup(touched, [p for p in explicit if p])
    if args.diff:
        added = _dedup(added, diff_paths(root, args.diff, "AR"))
        touched = _dedup(touched, diff_paths(root, args.diff, "ACMR"))

    structural, advisory, map_touched, ack = evaluate(root, added, touched, ack)
    return report(structural, advisory, map_touched, ack, strict)


# --- selftest ---------------------------------------------------------------

def selftest() -> int:
    """Pure-decision cases against a tiny synthetic map text."""
    map_text = (
        "| `forseti-harness/runners/` | CLI entrypoints ... "
        "run_reddit_candidate_intake_live.py ... |\n"
        "| `.agents/workflow-overlay/` | overlay |\n"
        "| `docs/decisions/` | Decision records. |\n"
        "Active Hooks ... `.agents/hooks/check_retrieval_header.py` ...\n"
        "Generated/gitignored scratch - do not enumerate or treat as authoritative:\n"
        "`forseti-harness/_test_runs/`, `cases/*/*/scores/`, and `memory/logs/`.\n\n"
    )
    extra = map_excludes(map_text)
    cases = [
        # (path, expect_structural_trigger?)
        ("docs/playbooks/x.md", True),                 # new top-level area
        ("tooling/x.py", True),                        # new repo-root area
        ("forseti-harness/runners/run_new_thing.py", True),   # new runner
        ("forseti-harness/adapters/new_adapter.py", True),    # new adapter
        ("docs/decisions/new_decision_v0.md", False),  # mapped folder convention
        (".agents/hooks/sibling.py", False),           # area already in map text
        ("forseti-harness/runners/run_reddit_candidate_intake_live.py", False),  # named
        ("forseti-harness/runners/__init__.py", False),   # package init, ignored
        ("forseti-harness/_test_runs/out.json", False),   # default scratch exclude
        ("forseti-harness/cases/tr/v0/scores/s.json", False),  # map-listed scratch
        ("README.md", False),                          # bare root file, not a folder
        ("docs/workflows/orca_repo_map_v0.md", False), # editing the map itself
    ]
    ok = True
    for i, (path, expect) in enumerate(cases, 1):
        got = structural_trigger(path, map_text, extra) is not None
        status = "PASS" if got == expect else "FAIL"
        if got != expect:
            ok = False
        print("%s case %02d  expect=%-5s got=%-5s  %s" % (status, i, expect, got, path))
    # ack parsing
    ack_ok = (read_ack(None, "feat: x\n\nrepo-map-ack: internal helper") ==
              "internal helper") and read_ack(None, "no ack here") is None
    print(("PASS" if ack_ok else "FAIL") + " ack-parse")
    ok = ok and ack_ok
    # commit nudge: fires on the map itself, silent on any other path
    nudge_ok = (commit_nudge(MAP) is not None
                and commit_nudge("docs/decisions/x_v0.md") is None
                and commit_nudge(SOURCE_OF_TRUTH) is None)
    print(("PASS" if nudge_ok else "FAIL") + " commit-nudge")
    ok = ok and nudge_ok
    paths_ok = (
        event_candidate_paths({"tool_input": {"file_path": MAP}}) == [MAP]
        and event_candidate_paths({"tool_input": {"command": (
            "*** Begin Patch\n"
            "*** Update File: docs/workflows/orca_repo_map_v0.md\n"
            "@@\n"
            "-old\n"
            "+new\n"
            "*** Move to: docs/workflows/orca_repo_map_v1.md\n"
            "*** End Patch\n"
        )}}) == [MAP, "docs/workflows/orca_repo_map_v1.md"]
        and event_candidate_paths({"tool_input": {}}) == []
    )
    print(("PASS" if paths_ok else "FAIL") + " hook-paths")
    ok = ok and paths_ok
    print("SELFTEST", "OK" if ok else "FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as exc:  # fail OPEN: a checker bug must never block a commit
        sys.stderr.write("repo-map-freshness: internal error, allowing: %s\n" % exc)
        sys.exit(0)
