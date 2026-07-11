#!/usr/bin/env python3
"""Repo-map freshness boundary check (forward-only, with repo-map commit interrupt).

WHAT THIS ENFORCES
  The *structural* subset of the repo map's own ``stale_if:`` block - the
  conditions that are mechanically detectable at a tool boundary. The rule (what
  makes the map stale, and what the map covers) is owned by:

      docs/workflows/forseti_repo_map_v0.md   (its ``stale_if:`` header + tables)

  This script does NOT restate that rule. It reads the map AS ITS OWN SPEC: the
  set of paths the map already names is "what is covered," and a touched path
  that introduces new navigable structure NOT present in the map trips the
  tripwire. If the map and this checker ever disagree, the map wins and this
  checker is the stale party.

WHY THIS EXISTS (enforcement placement)
  "Update the repo map" was carried only by instruction, so a capable agent
  could add a new top-level folder or a new direct harness area and nothing would
  notice at the moment the map went stale - the omission surfaced only later, as
  a wrong route. Per the Enforcement Placement principle in
      .agents/workflow-overlay/validation-gates.md  (-> "Enforcement Placement")
  a load-bearing, mechanically-checkable rule is enforced at the boundary (a
  write-time hook + this portable checker), not left to end-of-thread memory.

  Honest boundary: this catches STRUCTURAL omission (new top-level folder, new
  direct harness area) - ``stale_if`` #1 and #2 - with a hard commit gate,
  nudges (advisory only) on source-of-truth edits (#5), and nudges (advisory
  only) when new files land under a map-described directory without a map update,
  so a stale directory description can be caught before it silently rots
  (#3, partial). It does NOT judge whether
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
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _hooklib import (  # noqa: E402  (sys.path pin must precede the import)
    candidate_paths as event_candidate_paths,
    git_lines,
    read_event,
    repo_root,
    to_relposix,
)

# Authority this checker references (it does not restate the rule).
MAP = "docs/workflows/forseti_repo_map_v0.md"
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

# The map owns area-level harness navigation. Already mapped directories such as
# `forseti-harness/runners/` are discoverable by directory and do not require every
# new file basename to be listed in the shared map.

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
HEAD_LINES_FOR_HOOK = None  # the map is read in full; it is the spec, not the target

# Event parsing is shared: _hooklib.candidate_paths handles Claude-style
# tool_input.file_path/.path/.notebook_path AND Codex apply_patch headers in
# tool_input.command/.patch/.input (imported above as event_candidate_paths).


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


def mapped_dirs(map_text: str) -> tuple[str, ...]:
    """Repo-relative directory paths the map names (backtick'd tokens ending in
    '/'). These are the directories whose one-line description can silently go
    stale when their contents change. Over-matching is harmless: this feeds an
    advisory nudge only, never the gate. Returned longest-first so the most
    specific mapped directory wins when several are prefixes of one file."""
    if not map_text:
        return ()
    out: set[str] = set()
    for tok in re.findall(r"`([^`]+/)`", map_text):
        t = tok.strip()
        if any(ch in t for ch in "*?[]"):  # globs are scratch/exclusion tokens
            continue
        t = t[2:] if t.startswith("./") else t
        if t.startswith("/") or "/" not in t.rstrip("/"):
            continue  # absolute, or a bare top-level name with no nesting
        out.add(t)
    return tuple(sorted(out, key=len, reverse=True))


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


def new_harness_area(relposix: str, map_text: str) -> str | None:
    """Return a direct forseti-harness area absent from the map, or None.

    The map owns area-level navigation, not a complete list of every runner or
    adapter file. This keeps mapped harness folders discoverable by directory
    while avoiding repeated edits to the same high-contention map rows.
    """
    parts = relposix.split("/")
    if not parts or parts[0] != "forseti-harness":
        return None
    if len(parts) == 1:
        return None
    if len(parts) == 2:
        name = parts[1]
        if name == "__init__.py" or name.startswith("."):
            return None
        return None if name.lower() in map_text.lower() else relposix
    area = "forseti-harness/" + parts[1]
    return None if area.lower() in map_text.lower() else area + "/"


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
    harness_area = new_harness_area(relposix, map_text)
    if harness_area is not None:
        return ("new harness area `%s` is not in the repo map's "
                "Forseti Harness section (stale_if #2)" % harness_area)
    return None


def advisory_only(relposix: str) -> str | None:
    """Coarse, never-blocking nudge for a touched path, or None."""
    if relposix == SOURCE_OF_TRUTH:
        return ("`%s` changed - if the source hierarchy or the doctrine-change "
                "propagation contract changed, the repo map's stale_if #5 may "
                "have tripped; confirm the map still routes correctly." % relposix)
    return None


def description_drift(added: list[str], map_text: str, extra: tuple[str, ...],
                      map_touched: bool) -> list[str]:
    """Advisory (never blocking): one or more NEW files were added under a
    directory the map describes, but no map/submap was updated in the same change
    - so that directory's one-line description may no longer match what now lives
    there (the silent-drift class: e.g. a new ASR module under transcript/ while
    the row still says ASR 'is not present'). Stays silent when the map was
    touched (the author is presumably refreshing it), for scratch/__init__ paths,
    and for additions the structural gate already reports (new area/harness area)."""
    if map_touched or not map_text:
        return []
    dirs = mapped_dirs(map_text)
    if not dirs:
        return []
    flagged: dict[str, list[str]] = {}
    for rel in added:
        if not rel or rel in MAP_SURFACES:
            continue
        if is_excluded(rel, extra) or Path(rel).name == "__init__.py":
            continue
        if new_top_level_area(rel, map_text) or new_harness_area(rel, map_text):
            continue  # already reported by the structural gate
        for d in dirs:  # longest-first: most specific mapped dir wins
            if rel != d and rel.startswith(d):
                flagged.setdefault(d, []).append(rel)
                break
    out: list[str] = []
    for d in sorted(flagged):
        files = sorted(flagged[d])
        shown = ", ".join(files[:3]) + ("" if len(files) <= 3
                                        else " (+%d more)" % (len(files) - 3))
        out.append(
            "new file(s) under map-described `%s` (%s) but no map/submap was "
            "updated - verify that directory's description still matches what now "
            "lives there (advisory; stale_if #3)." % (d, shown))
    return out


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


# --- git plumbing (shared _hooklib.git_lines) --------------------------------

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
    data = read_event()

    paths = event_candidate_paths(data)
    if not paths:
        return 0

    notes: list[str] = []
    block = False
    checkable: list[str] = []
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
        # Cheap pre-gate: a path the DEFAULT excludes already rule out can never
        # trigger or nudge, so it must not cost a full map read. Map-derived
        # exclusions still apply below for the paths that survive.
        if not is_excluded(rel, ()):
            checkable.append(rel)

    if checkable:
        map_text = read_map_text(root)  # read once, only when a path needs the spec
        extra = map_excludes(map_text)
        for rel in checkable:
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
    advisory.extend(description_drift(relpaths_added, map_text, extra, map_touched))
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
        "| `forseti-harness/runners/` | CLI entrypoints; enumerate with git ls-files. |\n"
        "| `forseti-harness/source_capture/` | Source capture package. |\n"
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
        ("forseti-harness/runners/run_new_thing.py", False),  # mapped runner area
        ("forseti-harness/source_capture/new_module.py", False),  # mapped harness area
        ("forseti-harness/new_area/tool.py", True),       # new direct harness area
        ("forseti-harness/new_root_file.py", True),       # new direct harness file
        ("docs/decisions/new_decision_v0.md", False),  # mapped folder convention
        (".agents/hooks/sibling.py", False),           # area already in map text
        ("forseti-harness/runners/__init__.py", False),   # package init, ignored
        ("forseti-harness/_test_runs/out.json", False),   # default scratch exclude
        ("forseti-harness/cases/tr/v0/scores/s.json", False),  # map-listed scratch
        ("README.md", False),                          # bare root file, not a folder
        ("docs/workflows/forseti_repo_map_v0.md", False), # editing the map itself
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
            "*** Update File: docs/workflows/forseti_repo_map_v0.md\n"
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
    # description-drift advisory: new file under a map-described dir, map untouched
    drift_map = ("| `forseti-harness/schemas/` | models |\n"
                 "| `forseti-harness/cleaning/` | cleaning |\n")
    d_extra = map_excludes(drift_map)
    drift_ok = (
        len(description_drift(["forseti-harness/schemas/new_model.py"],
                              drift_map, d_extra, False)) == 1
        and description_drift(["forseti-harness/schemas/new_model.py"],
                              drift_map, d_extra, True) == []           # map touched
        and description_drift(["forseti-harness/schemas/__init__.py"],
                              drift_map, d_extra, False) == []          # package init
        and description_drift(["tooling/x.py"], drift_map, d_extra, False) == []  # unmapped
        and mapped_dirs(drift_map) == ("forseti-harness/cleaning/",
                                       "forseti-harness/schemas/")
    )
    print(("PASS" if drift_ok else "FAIL") + " description-drift")
    ok = ok and drift_ok
    print("SELFTEST", "OK" if ok else "FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as exc:  # fail OPEN: a checker bug must never block a commit
        sys.stderr.write("repo-map-freshness: internal error, allowing: %s\n" % exc)
        sys.exit(0)
