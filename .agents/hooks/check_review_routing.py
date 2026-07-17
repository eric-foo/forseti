#!/usr/bin/env python3
"""Review-routing disposition gate -- STRICT CI gate + commit-msg advisory.

WHAT THIS DOES
  A change that touches code roots must carry its review disposition. For the
  diff base...HEAD (or the staged change in --commit-msg mode) it checks:
    - if no touched path is under a code root: out of scope, silent pass;
    - if the change ADDS a review artifact under a review root: satisfied
      (the lane filed its review prompt/report in the same change);
    - otherwise at least one commit message in the range must carry a
      shape-valid `review_routing_status:` line:
        review_routing_status: routed <existing review-root path>
        review_routing_status: routed -- chat_only_adjudicated: <durable disposition>
        review_routing_status: blocked -- <reason>
        review_routing_status: not_needed -- <reason>
      For path-routed review, the named path must exist in the HEAD tree. For
      chat-only adjudication, blocked, and not-needed forms, the required text
      must be non-empty.
  The rule is owned by:

      .agents/workflow-overlay/validation-gates.md  (Review-routing disposition gate)

  This script does NOT restate that rule. It is a thin structural tripwire
  that references the authority above. If the gate bullet and this checker
  ever disagree, the bullet wins and this checker is the stale party.

WHY THIS GATE EXISTS (provenance)
  The 2026-07-02 fused-lane audit found that most fused implementation lanes
  closed without filing the delegated-review handoff their contract carried,
  and several claimed the review in commit prose without ever filing it. The
  disposition lived only in chat, so nothing durable could be checked. This
  gate moves the disposition to a commit-visible, mechanically checkable
  surface (EP-35 in the enforcement-placement classification).

WHAT THIS GATE DOES *NOT* DO (the over-edge boundary -- PLACEMENT IS NOT AUTHORITY)
  - It does NOT decide whether a review SHOULD have been recommended or
    required. That is resident scoping judgment (the fused/review contracts).
  - It does NOT verify the TRUTH of a `not_needed`/`blocked` reason, the
    quality or severity authority of any filed review, or that a `routed`
    prompt was ever executed. A substrate checks disposition PRESENCE and
    SHAPE, never truth (cf. the receipt-field provenance gate).
  - A green run is disposition shape only -- never proof a review happened,
    was sufficient, or that the code is validated or ready.
  - Multiple token lines across a lane's commits are tolerated; at least one
    shape-valid line satisfies the gate (per-closeout multiplicity stays with
    the fused contract, not here).

DETECTION CONTRACT (mirrors check_dcp_receipt.py / header_index.py --strict)
  base ref priority: $FORSETI_DIFF_BASE (exact CI event SHA); else
  $GITHUB_BASE_REF -> origin/<ref>; else --base <ref>; else origin/main.
  Diff is three-dot `base...HEAD` (the PR's net change),
  name-status. Rename/copy rows touch BOTH paths -- a rename out of a code
  root is a code-root change (FIND-01, EP-35 delegated review). Commit
  messages come from `git log base..HEAD`. NO HEAD~1 fallback. If the base
  cannot be resolved or git fails, fail OPEN (exit 0, loud warning) -- the
  universal Forseti infra-gap stance; in CI the base is always present
  (fetch-depth: 0). Fail-open is for INFRASTRUCTURE GAPS ONLY: in --strict and
  --selftest an unexpected internal exception exits nonzero (the GATE FAIL
  bucket, validation-gates.md; FIND-02, EP-35 delegated review); advisory
  modes fail open on internal error. Forward-only by construction: only the
  current diff is gated, never historical backlog (see --audit for that view).

MODES
  check_review_routing.py --strict [--base <ref>]   fail (exit 1) on findings; CI gate
  check_review_routing.py --report | --check        same findings, advisory (exit 0)
  check_review_routing.py --commit-msg <file>       staged change + message file; ADVISORY (always exit 0)
  check_review_routing.py --audit [--limit N]       per-commit advisory history view; exit 0
  check_review_routing.py --selftest                pure-function cases; exit 0/1
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _hooklib import (  # noqa: E402  (sys.path pin must precede the import)
    git_out,
    repo_root,
    resolve_base_ref,
)

# Authority this checker references (it does not restate the rule).
RULE_AUTHORITY = ".agents/workflow-overlay/validation-gates.md (Review-routing disposition gate)"
PRINCIPLE = ".agents/workflow-overlay/validation-gates.md (Enforcement Placement)"

# Code roots whose changes owe a review disposition. forseti-harness/ is the
# implementation tree; .agents/hooks/ is governance code (the 2026-06-13
# header_index lane was exactly a hook lane that filed no disposition).
CODE_ROOTS = ("forseti-harness/", ".agents/hooks/")

# Review roots: an artifact added here in the same change IS the disposition.
REVIEW_ROOTS = ("docs/prompts/reviews/", "docs/review-outputs/")

TOKEN_RE = re.compile(
    r"(?m)^[ \t]*review_routing_status[ \t]*:[ \t]*(routed|blocked|not_needed)\b[ \t]*(.*)$"
)
REVIEW_PATH_RE = re.compile(
    r"(docs/(?:prompts/reviews|review-outputs)/[^\s`'\"\)\]]+)"
)
CHAT_ONLY_ADJUDICATED_RE = re.compile(
    r"(?i)\bchat_only_adjudicated\b[ \t]*:[ \t]*(\S(?:.*\S)?)"
)


# ---------------------------------------------------------------------------
# Pure decision core (testable)
# ---------------------------------------------------------------------------

def touches_code_root(paths: list[str]) -> bool:
    return any(p.startswith(CODE_ROOTS) for p in paths)


def adds_review_artifact(added_paths: list[str]) -> bool:
    return any(p.startswith(REVIEW_ROOTS) for p in added_paths)


def parse_name_status(lines: list[str]) -> tuple[list[str], list[str]]:
    """(touched, added) from `git diff --name-status` output lines.

    Rename/copy rows (`Rnnn<TAB>old<TAB>new`, `Cnnn<TAB>old<TAB>new`) touch
    BOTH paths -- keeping only the destination let a rename out of a code root
    bypass the gate (FIND-01, EP-35 delegated review). `added` carries the
    destination path only. Pure function (testable)."""
    touched: list[str] = []
    added: list[str] = []
    for ln in lines:
        parts = [p.strip() for p in ln.split("\t")]
        if len(parts) < 2:
            continue
        status = parts[0]
        touched.extend(p for p in parts[1:] if p)
        if status.startswith(("A", "R", "C")):
            added.append(parts[-1])
    return touched, added


def _reason_of(remainder: str) -> str:
    """Strip leading separators from a token remainder to get the reason text."""
    return remainder.strip().lstrip(":-–—").strip()


def token_findings(messages: str, path_exists) -> tuple[bool, list[str]]:
    """(satisfied, findings) for the token lines found in `messages`.

    Satisfied when at least one token line is shape-valid. Findings list the
    problems of the invalid lines (only reported when nothing satisfies).
    `path_exists` is injected: rel-posix path -> bool. Pure function."""
    problems: list[str] = []
    matches = TOKEN_RE.findall(messages)
    if not matches:
        return False, ["no `review_routing_status:` line found in the change's commit messages"]
    for value, remainder in matches:
        if value == "routed":
            m = REVIEW_PATH_RE.search(remainder)
            if m:
                rel = m.group(1).rstrip(".,;")
                if path_exists(rel):
                    return True, []
                problems.append("`routed` names a path that does not exist: %s" % rel)
            if CHAT_ONLY_ADJUDICATED_RE.search(remainder):
                return True, []
            if not m:
                problems.append(
                    "`routed` names neither an existing review path nor a non-empty "
                    "`chat_only_adjudicated:` disposition"
                )
            continue
        else:  # blocked | not_needed
            if not _reason_of(remainder):
                problems.append("`%s` carries no reason text" % value)
                continue
            return True, []
    return False, problems


def evaluate(touched: list[str], added: list[str], messages: str, path_exists) -> list[str]:
    """All findings for one change (empty == ok / out of scope). Pure function."""
    if not touches_code_root(touched):
        return []
    if adds_review_artifact(added):
        return []
    satisfied, problems = token_findings(messages, path_exists)
    if satisfied:
        return []
    findings = [
        "code-root change (%s) with no review artifact added under %s"
        % (", ".join(sorted({r for r in CODE_ROOTS for p in touched if p.startswith(r)})),
           " or ".join(REVIEW_ROOTS))
    ]
    findings.extend(problems)
    return findings


# ---------------------------------------------------------------------------
# Git plumbing (mirrors check_dcp_receipt.py)
# ---------------------------------------------------------------------------

def _git(root: Path, args: list[str], timeout: int = 15) -> tuple[int, str]:
    """Run a git command; return (returncode, stdout). Never raises.

    Thin adapter over the shared _hooklib.git_out (keeps this file's 15s
    default). git_out returns (1, "") on launch failure/timeout instead of
    (-1, ""); callers here only test rc != 0, so the distinction is inert."""
    return git_out(root, args, timeout=timeout)


def diff_paths(root: Path, base_ref: str) -> tuple[list[str], list[str]] | None:
    """(touched, added) relpaths in base...HEAD. None on a git infra gap."""
    if _git(root, ["rev-parse", "--verify", "--quiet", "HEAD"])[0] != 0:
        return None
    if _git(root, ["rev-parse", "--verify", "--quiet", base_ref])[0] != 0:
        return None
    rc, out = _git(
        root,
        ["diff", "--find-renames", "--name-status", "%s...HEAD" % base_ref],
    )
    if rc != 0:
        return None
    return parse_name_status(out.splitlines())


def range_messages(root: Path, base_ref: str) -> str:
    rc, out = _git(root, ["log", "--format=%B", "%s..HEAD" % base_ref])
    return out if rc == 0 else ""


def head_path_exists(root: Path):
    def _exists(rel: str) -> bool:
        return _git(root, ["cat-file", "-e", "HEAD:%s" % rel])[0] == 0
    return _exists


def worktree_path_exists(root: Path):
    def _exists(rel: str) -> bool:
        return (root / rel).is_file()
    return _exists


# ---------------------------------------------------------------------------
# Runs
# ---------------------------------------------------------------------------

def run_diff_mode(root: Path, mode: str, cli_base: str | None) -> int:
    base_ref = resolve_base_ref(cli_base)
    scoped = diff_paths(root, base_ref)
    if scoped is None:
        print("check_review_routing --%s: fail-open (infra gap): git/diff unavailable "
              "(base '%s') -- nothing to gate" % (mode, base_ref))
        return 0
    touched, added = scoped
    findings = evaluate(touched, added, range_messages(root, base_ref), head_path_exists(root))
    if findings:
        print("check_review_routing --%s: %d finding(s) (base: %s):" % (mode, len(findings), base_ref))
        for f in findings:
            print("  " + f)
        print("  Satisfy by adding the lane's review prompt/report under "
              "%s, or a shape-valid `review_routing_status:` commit-message line."
              % " or ".join(REVIEW_ROOTS))
        print("  Rule authority: %s" % RULE_AUTHORITY)
        return 1 if mode == "strict" else 0
    print("check_review_routing --%s: OK (base: %s)" % (mode, base_ref))
    return 0


def run_commit_msg(root: Path, msg_file: str) -> int:
    """Local commit-msg ADVISORY: staged paths + the message being written.
    Always exit 0 -- the strict boundary is CI, not the local commit."""
    try:
        message = Path(msg_file).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return 0
    rc, out = _git(root, ["diff", "--cached", "--name-status"])
    if rc != 0:
        return 0
    touched, added = parse_name_status(out.splitlines())
    findings = evaluate(touched, added, message, worktree_path_exists(root))
    if findings:
        print("check_review_routing (advisory): this commit touches a code root with "
              "no review disposition:")
        for f in findings:
            print("  " + f)
        print("  CI will require it PR-wide (any commit in the PR range can carry the "
              "line, or the PR can add the review artifact).")
        print("  Rule authority: %s" % RULE_AUTHORITY)
    return 0


def run_audit(root: Path, limit: int) -> int:
    """Per-commit advisory history view (first-parent). Exit 0 always."""
    rc, out = _git(root, ["rev-list", "--first-parent", "-n", str(limit), "HEAD"])
    if rc != 0:
        print("check_review_routing --audit: fail-open (infra gap): git unavailable")
        return 0
    shas = [s.strip() for s in out.splitlines() if s.strip()]
    flagged = 0
    scoped = 0
    for sha in shas:
        rc, out = _git(root, ["diff", "--name-status", "%s^" % sha, sha])
        if rc != 0:
            continue  # root commit or unreadable parent
        touched, added = parse_name_status(out.splitlines())
        if not touches_code_root(touched):
            continue
        scoped += 1
        _, msg = _git(root, ["log", "-1", "--format=%B", sha])
        findings = evaluate(touched, added, msg, head_path_exists(root))
        if findings:
            flagged += 1
            _, subj = _git(root, ["log", "-1", "--format=%h %ad %s", "--date=short", sha])
            print("  MISSING  %s" % subj.strip())
    print("check_review_routing --audit: %d of %d code-root commit(s) in the last %d "
          "first-parent commit(s) carry no review disposition (advisory, exit 0; "
          "forward-only backlog, never gated)." % (flagged, scoped, len(shas)))
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
        print("%s  %-58s got=%r" % (status, label, got))

    exists_all = lambda _p: True
    exists_none = lambda _p: False

    # --- scope classification ---
    check("docs-only change out of scope",
          evaluate(["docs/decisions/x.md"], [], "", exists_none), [])
    check("harness touch is in scope",
          touches_code_root(["forseti-harness/src/foo.py"]), True)
    check("hook touch is in scope",
          touches_code_root([".agents/hooks/new_hook.py"]), True)

    # --- satisfied by filed review artifact ---
    check("added review prompt satisfies",
          evaluate(["forseti-harness/a.py", "docs/prompts/reviews/a_prompt_v0.md"],
                   ["docs/prompts/reviews/a_prompt_v0.md"], "", exists_none), [])
    check("added review report satisfies",
          evaluate(["forseti-harness/a.py"], ["docs/review-outputs/a_review_v0.md"],
                   "", exists_none), [])
    check("MODIFIED (not added) review file does not satisfy alone",
          evaluate(["forseti-harness/a.py", "docs/prompts/reviews/old.md"], [], "",
                   exists_none) != [], True)

    # --- token grammar ---
    check("no token -> finding (the #577 shape)",
          evaluate(["forseti-harness/a.py"], [], "feat: impl only\n", exists_none) != [], True)
    check("not_needed with reason passes",
          evaluate(["forseti-harness/a.py"], [],
                   "review_routing_status: not_needed -- mechanical rename, no advisory carried\n",
                   exists_none), [])
    check("not_needed bare fails",
          evaluate(["forseti-harness/a.py"], [], "review_routing_status: not_needed\n",
                   exists_none) != [], True)
    check("blocked with reason passes",
          evaluate([".agents/hooks/h.py"], [],
                   "review_routing_status: blocked -- orchestrator unavailable\n",
                   exists_none), [])
    check("routed with existing path passes",
          evaluate(["forseti-harness/a.py"], [],
                   "review_routing_status: routed docs/prompts/reviews/a_prompt_v0.md\n",
                   exists_all), [])
    check("routed with dangling path fails",
          evaluate(["forseti-harness/a.py"], [],
                   "review_routing_status: routed docs/prompts/reviews/ghost.md\n",
                   exists_none) != [], True)
    check("routed chat-only adjudicated passes",
          evaluate(["forseti-harness/a.py"], [],
                   "review_routing_status: routed -- chat_only_adjudicated: "
                   "Anthropic review returned; findings adjudicated\n",
                   exists_none), [])
    check("routed chat-only bare fails",
          evaluate(["forseti-harness/a.py"], [],
                   "review_routing_status: routed -- chat_only_adjudicated:\n",
                   exists_none) != [], True)
    check("routed with no path fails",
          evaluate(["forseti-harness/a.py"], [], "review_routing_status: routed\n",
                   exists_none) != [], True)
    check("one valid among invalid tokens satisfies",
          evaluate(["forseti-harness/a.py"], [],
                   "review_routing_status: routed\nreview_routing_status: not_needed -- covered by X\n",
                   exists_none), [])
    check("token in body prose position still matches (indented)",
          evaluate(["forseti-harness/a.py"], [],
                   "  review_routing_status: not_needed -- lane adjudicated in-chat\n",
                   exists_none), [])
    check("mention WITHOUT key:value shape does not satisfy",
          evaluate(["forseti-harness/a.py"], [],
                   "we should add review_routing_status later\n", exists_none) != [], True)

    # --- parse_name_status (FIND-01: rename out of a code root stays in scope) ---
    t, a = parse_name_status(["R100\tforseti-harness/a.py\tdocs/moved/a.py"])
    check("rename OUT of code root keeps old path touched",
          "forseti-harness/a.py" in t, True)
    check("rename destination is the added path", a, ["docs/moved/a.py"])
    check("rename-out triggers scope (missing disposition found)",
          evaluate(t, a, "", exists_none) != [], True)
    t2, a2 = parse_name_status(
        ["M\tforseti-harness/b.py", "A\tdocs/review-outputs/r.md", "short-noise-line"])
    check("plain rows parse; noise skipped", (t2, a2),
          (["forseti-harness/b.py", "docs/review-outputs/r.md"],
           ["docs/review-outputs/r.md"]))

    # --- reason stripping ---
    check("reason separator variants", _reason_of("-- because reasons"), "because reasons")
    check("empty reason", _reason_of("  --  "), "")

    # --- resolve_base_ref ---
    saved_ci_base = os.environ.pop("FORSETI_DIFF_BASE", None)
    saved = os.environ.pop("GITHUB_BASE_REF", None)
    try:
        check("base default", resolve_base_ref(None), "origin/main")
        check("base cli", resolve_base_ref("some-branch"), "some-branch")
        os.environ["GITHUB_BASE_REF"] = "develop"
        check("base env wins", resolve_base_ref("ignored"), "origin/develop")
    finally:
        if saved is not None:
            os.environ["GITHUB_BASE_REF"] = saved
        else:
            os.environ.pop("GITHUB_BASE_REF", None)
        if saved_ci_base is not None:
            os.environ["FORSETI_DIFF_BASE"] = saved_ci_base
        else:
            os.environ.pop("FORSETI_DIFF_BASE", None)

    print()
    print("SELFTEST", "OK" if ok else "FAILED")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()
    try:
        root = repo_root()
    except Exception as exc:
        sys.stderr.write("check_review_routing: cannot determine repo root: %s\n" % exc)
        return 0
    cli_base: str | None = None
    if "--base" in argv:
        idx = argv.index("--base")
        if idx + 1 < len(argv):
            cli_base = argv[idx + 1]
    if "--commit-msg" in argv:
        idx = argv.index("--commit-msg")
        if idx + 1 < len(argv):
            return run_commit_msg(root, argv[idx + 1])
        return 0
    if "--audit" in argv:
        limit = 100
        if "--limit" in argv:
            idx = argv.index("--limit")
            if idx + 1 < len(argv):
                try:
                    limit = int(argv[idx + 1])
                except ValueError:
                    pass
        return run_audit(root, limit)
    if "--strict" in argv:
        return run_diff_mode(root, "strict", cli_base)
    if "--report" in argv or "--check" in argv:
        return run_diff_mode(root, "report", cli_base)
    print("Usage: check_review_routing.py --strict | --report | --check | "
          "--audit [--limit N] | --commit-msg <file> | --selftest [--base <ref>]")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as exc:
        # GATE FAIL bucket in gating modes (validation-gates.md; FIND-02,
        # EP-35 delegated review): an internal checker bug must not read as a
        # green gate. Advisory modes fail open so a bug never bricks the agent.
        sys.stderr.write("check_review_routing: internal error: %s\n" % exc)
        gating = "--strict" in sys.argv[1:] or "--selftest" in sys.argv[1:]
        sys.exit(1 if gating else 0)
