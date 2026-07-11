#!/usr/bin/env python3
"""Output-mode declaration SHAPE gate (EP-11): every in-scope prompt artifact
must carry a recognized output-mode declaration.

RULE AUTHORITY
  .agents/workflow-overlay/prompt-orchestration.md -> "Output Modes" (the
  closed-set token list and per-token meaning) and .agents/workflow-overlay/
  validation-gates.md -> "Output-mode gate" bullet ("prompts must name exactly
  one output mode from ..."). This checker references those rules and never
  restates them. EP handle: EP-11 in
  docs/decisions/overlay_enforcement_placement_classification_v0.md, which
  scopes this checker to SHAPE only: `schema: token-in-set`.

WHAT THIS ENFORCES (shape only, narrowed from the EP-11 full rule)
  A prompt artifact under docs/prompts/ must contain at least one recognized
  output-mode declaration line -- a line naming one of the five closed-set
  tokens (`chat-only`, `file-write`, `review-report`, `paste-ready-chat`,
  `patch-queue`) in either YAML-key or prose-bullet form. This is the
  mechanically checkable shell of EP-11:
    - zero declaration lines at all           -> FINDING (never declared)
    - declaration line(s) present, but every one carries zero closed-set
      tokens (empty value, legacy/typo'd token, wrong separator)
                                               -> FINDING (declared but invalid)
    - otherwise                               -> PASS

WHAT THIS DOES *NOT* DO (the over-edge boundary -- PLACEMENT IS NOT AUTHORITY)
  - It does NOT verify "exactly one" output mode is declared for the artifact
    as a whole. Multiple declaration lines are common and legitimate (a
    dispatch block plus a preflight recap; a receiver-output aside), and
    deciding which one is *the* artifact's output mode -- versus a compound
    per-audience or per-phase declaration -- stays resident judgment (the
    EP-11 "exactly one" clause is COUNT judgment, not TOKEN-IN-SET shape).
    Multiple declaration lines, and a single line carrying 2+ tokens (a
    legitimate compound declaration, e.g. `file-write` for this artifact plus
    `paste-ready-chat` for a courier copy), are printed as INFO notes only in
    --check/--audit output -- never findings.
  - It does NOT decide whether the chosen token is the RIGHT one for the
    artifact's actual delivery shape, whether a `review-report` prompt really
    wrote its report, or whether output-mode exceptions in
    prompt-orchestration.md were honored. Truth of the declared mode stays
    resident judgment.
  - It does NOT parse `receiver_output_mode:` / `reviewer_output_mode:` /
    `downstream_review_output_mode:` / `terminal_output_mode:` (or any other
    qualified key) as *this* artifact's declaration, and it does NOT treat an
    "output mode for the receiving/downstream/future/reviewer/delegate/
    adjudicator" prose aside as a declaration -- those describe a DIFFERENT
    actor's output mode, not this artifact's own.

DETECTION CONTRACT (mirrors check_handoff_pointers.py / check_dcp_receipt.py)
  base ref priority: $FORSETI_DIFF_BASE (exact CI event SHA); else
  $GITHUB_BASE_REF -> origin/<ref>; else --base <ref>; else origin/main.
  Diff is three-dot `base...HEAD`, name-status; scanned files are
  the added/modified/rename-or-copy-destination `.md` paths still present in
  the tree, filtered to the in-scope set (below). NO HEAD~1 fallback. If the
  base cannot be resolved or git fails, fail OPEN (exit 0, loud warning) --
  the universal Forseti infra-gap stance; in CI the base is always present
  (fetch-depth: 0). Fail-open is for INFRASTRUCTURE GAPS ONLY: in --strict and
  --selftest an unexpected internal exception exits 1 (the GATE FAIL bucket,
  validation-gates.md); advisory modes fail open on internal error.
  Forward-only by construction: only the current diff is gated, never
  historical backlog (see --audit for that view).

IN-SCOPE FILES
  posix relpath starts with `docs/prompts/`, ends `.md`, is NOT under
  `docs/prompts/templates/` (those are examples, not filed prompt artifacts),
  basename is not `README.md`, and is not under a globally excluded dir
  (`_scratch`, `node_modules`, `docs/_inbox/` / any `_inbox/` segment --
  mirrors check_handoff_pointers.py's exclusion list).

MODES
  check_prompt_output_mode.py --strict [--base <ref>]        CI gate; exit 1 on findings
  check_prompt_output_mode.py --check  [--base <ref>] [paths] same scan, human-readable, exit 0;
                                                               explicit paths scan those files
                                                               directly instead of the base diff
  check_prompt_output_mode.py --audit                         whole-corpus backlog view
                                                               (git ls-files -- docs/prompts), exit 0
  check_prompt_output_mode.py --selftest                      pure-function cases; exit per pass/fail

NON-CLAIMS
  Shape only, never truth. Not validation, not readiness. A PASS means a
  recognized token appears on a declaration line -- it is not a claim that
  the token is the correct one, that only one was intended, or that the
  artifact honors the mode it names.

REGISTRATION (.github/workflows/ci.yml, after the output-mode-adjacent step)
  - name: prompt output-mode declaration (EP-11 shape gate)
    run: python .agents/hooks/check_prompt_output_mode.py --strict
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path
from typing import NamedTuple

# ---------------------------------------------------------------------------
# Repo root (this file lives at .agents/hooks/check_prompt_output_mode.py)
# ---------------------------------------------------------------------------

def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


# ---------------------------------------------------------------------------
# Closed-set vocabulary (frozenset-constant style, mirrors check_dcp_receipt.py)
# ---------------------------------------------------------------------------

# Single-sourced from .agents/workflow-overlay/prompt-orchestration.md
# § "Output Modes". Additions or removals there are doctrine changes and must
# update this constant (see selftest case "token-drift insurance", which
# parses that section and asserts set equality against this constant).
TOKENS = frozenset({
    "chat-only",
    "file-write",
    "review-report",
    "paste-ready-chat",
    "patch-queue",
})

RULE_AUTHORITY = (
    ".agents/workflow-overlay/prompt-orchestration.md (Output Modes) / "
    ".agents/workflow-overlay/validation-gates.md (Output-mode gate)"
)

# ---------------------------------------------------------------------------
# Pure decision core (testable)
# ---------------------------------------------------------------------------

# Key form: `output_mode:` (optionally indented/bulleted), never a qualified
# key like `receiver_output_mode:` or `terminal_output_mode:` -- the negative
# lookbehind refuses a match when the character immediately before
# "output_mode" is a word character or hyphen.
_KEY_RE = re.compile(r"(?<![\w-])output_mode\s*:")

# Prose form: "Output mode:" (optionally bulleted/bolded), case-insensitive.
_PROSE_RE = re.compile(
    r"^\s*(?:[-*]\s*)?\*{0,2}output mode\*{0,2}\s*:", re.IGNORECASE
)

# Denylist: a line otherwise matching the key or prose form is NOT this
# artifact's own declaration when it is actually describing a DIFFERENT
# actor's output mode ("output mode for the receiving CA: ...").
_DENY_RE = re.compile(
    r"output[_ ]mode\s*:?\s*for\s+(the\s+)?"
    r"(receiving|downstream|future|reviewer|receiver|delegate|adjudicator)",
    re.IGNORECASE,
)

# Closed-set token match on a declaration line.
_TOKEN_RE = re.compile(
    r"\b(chat-only|file-write|review-report|paste-ready-chat|patch-queue)\b"
)


def is_declaration_line(line: str) -> bool:
    """True if `line` is this artifact's own output-mode declaration line.

    Pure function (testable)."""
    if not (_KEY_RE.search(line) or _PROSE_RE.search(line)):
        return False
    if _DENY_RE.search(line):
        return False
    return True


def tokens_in_line(line: str) -> list[str]:
    """Closed-set output-mode tokens present on `line`, in order.

    Pure function (testable)."""
    return _TOKEN_RE.findall(line)


class Finding(NamedTuple):
    source: str              # scanned file (repo-relative, forward slashes)
    kind: str                # "no_output_mode_declaration" | "no_recognized_output_mode_token"
    lineno: int | None       # offending line number, or None for no-declaration
    detail: str              # offending line text (stripped), or "" for no-declaration


def evaluate_file_lines(rel_source: str, lines: list[str]) -> tuple[Finding | None, list[str]]:
    """Scan one file's lines for the output-mode declaration shell.

    Returns (finding_or_none, info_notes). Multiple declaration lines and a
    declaration line with 2+ tokens are INFO notes only, never findings --
    that count/compound judgment stays resident (see module docstring).
    Pure function (testable)."""
    decl_lines = [
        (i, line, tokens_in_line(line))
        for i, line in enumerate(lines, 1)
        if is_declaration_line(line)
    ]

    info: list[str] = []
    if len(decl_lines) > 1:
        info.append(
            "multiple output-mode declaration lines (%d), first at line %d"
            % (len(decl_lines), decl_lines[0][0])
        )
    for lineno, _line, toks in decl_lines:
        if len(toks) >= 2:
            info.append(
                "line %d carries %d output-mode tokens: %s"
                % (lineno, len(toks), ", ".join(toks))
            )

    if not decl_lines:
        return Finding(rel_source, "no_output_mode_declaration", None, ""), info

    if all(len(toks) == 0 for _lineno, _line, toks in decl_lines):
        first_lineno, first_line, _toks = decl_lines[0]
        return (
            Finding(rel_source, "no_recognized_output_mode_token", first_lineno, first_line.strip()),
            info,
        )

    return None, info


def is_in_scope_file(rel_path: str) -> bool:
    """True if a path is in this gate's scanned set.

    Pure function (testable)."""
    p = rel_path.replace("\\", "/")
    if not p.endswith(".md"):
        return False
    if not p.startswith("docs/prompts/"):
        return False
    if p.startswith("docs/prompts/templates/"):
        return False
    if p.rsplit("/", 1)[-1] == "README.md":
        return False
    if "_scratch" in p or "node_modules" in p:
        return False
    if p.startswith("docs/_inbox/") or "/_inbox/" in p:
        return False
    return True


def extract_authority_tokens(text: str) -> frozenset[str] | None:
    """Closed-set tokens declared in the "## Output Modes" section of
    prompt-orchestration.md (the leading backticked token of each
    `- \\`token\\`: ...` bullet, up to the next `## ` heading).

    Returns None if the section cannot be found. Pure function (testable)."""
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip() == "## Output Modes":
            start = i + 1
            break
    if start is None:
        return None
    bullet_re = re.compile(r"^-\s*`([a-z0-9\-]+)`\s*:")
    tokens: list[str] = []
    for line in lines[start:]:
        if line.startswith("## "):
            break
        m = bullet_re.match(line)
        if m:
            tokens.append(m.group(1))
    return frozenset(tokens)


def parse_name_status(lines: list[str]) -> list[str]:
    """Present-in-tree changed paths from `git diff --name-status` output:
    added, modified, and rename/copy DESTINATIONS (sources may be gone).

    Pure function (testable)."""
    present: list[str] = []
    for ln in lines:
        parts = [p.strip() for p in ln.split("\t")]
        if len(parts) < 2:
            continue
        status = parts[0]
        if status.startswith(("R", "C")) and len(parts) >= 3:
            present.append(parts[2])
        elif status.startswith(("A", "M")):
            present.append(parts[1])
        # D rows: skip -- nothing left in the tree to scan
    return present


# ---------------------------------------------------------------------------
# Git plumbing (infra-gap fail-open)
# ---------------------------------------------------------------------------

def _git(root: Path, args: list[str], timeout: int = 15) -> tuple[int, str]:
    """Run a git command; return (returncode, stdout). Never raises."""
    try:
        res = subprocess.run(
            ["git", "-C", str(root), *args],
            capture_output=True, text=True, timeout=timeout,
        )
        return res.returncode, res.stdout
    except (FileNotFoundError, OSError, subprocess.TimeoutExpired):
        return -1, ""


def resolve_base_ref(cli_base: str | None) -> str:
    ci_base = os.environ.get("FORSETI_DIFF_BASE", "").strip()
    if ci_base:
        return ci_base
    gh_base = os.environ.get("GITHUB_BASE_REF", "").strip()
    if gh_base:
        return "origin/%s" % gh_base
    if cli_base:
        return cli_base
    return "origin/main"


def changed_scanned_files(root: Path, base_ref: str) -> list[str] | None:
    """Repo-relative in-scope .md paths changed in base...HEAD. None = infra gap."""
    if _git(root, ["rev-parse", "--verify", "--quiet", "HEAD"])[0] != 0:
        return None
    if _git(root, ["rev-parse", "--verify", "--quiet", base_ref])[0] != 0:
        return None
    code, out = _git(root, ["diff", "--name-status", "%s...HEAD" % base_ref])
    if code != 0:
        return None
    return [p for p in parse_name_status(out.splitlines()) if is_in_scope_file(p)]


def tracked_prompt_files(root: Path) -> list[str] | None:
    """All git-tracked paths under docs/prompts (for --audit). None = infra gap."""
    code, out = _git(root, ["ls-files", "--", "docs/prompts"])
    if code != 0:
        return None
    return [ln.strip() for ln in out.splitlines() if ln.strip()]


# ---------------------------------------------------------------------------
# Scanning
# ---------------------------------------------------------------------------

def scan_files(root: Path, rel_paths: list[str]) -> tuple[list[Finding], list[str]]:
    findings: list[Finding] = []
    infos: list[str] = []
    for rel in rel_paths:
        norm = rel.replace("\\", "/")
        fpath = root / Path(norm)
        try:
            lines = fpath.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        finding, file_infos = evaluate_file_lines(norm, lines)
        if finding is not None:
            findings.append(finding)
        for note in file_infos:
            infos.append("%s: %s" % (norm, note))
    return findings, infos


# ---------------------------------------------------------------------------
# Mode runners
# ---------------------------------------------------------------------------

def _print_findings(findings: list[Finding]) -> None:
    for f in findings:
        if f.kind == "no_output_mode_declaration":
            print("  %s  ->  no output-mode declaration found" % f.source)
        else:
            print(
                "  %s:%d  ->  declaration line carries no recognized output-mode token: %r"
                % (f.source, f.lineno, f.detail)
            )


def _print_infos(infos: list[str]) -> None:
    for note in infos:
        print("  INFO  %s" % note)


def _print_rule() -> None:
    print(
        "rule: an in-scope prompt artifact must carry at least one output-mode\n"
        "      declaration line naming a closed-set token. Authority: %s.\n"
        "      Shape only, never truth: not validation, not readiness."
        % RULE_AUTHORITY
    )


def run_strict(root: Path, cli_base: str | None) -> int:
    base_ref = resolve_base_ref(cli_base)
    rel_paths = changed_scanned_files(root, base_ref)
    if rel_paths is None:
        sys.stderr.write(
            "check_prompt_output_mode --strict: WARNING git diff vs %s unavailable; "
            "failing OPEN (infra gap, not a pass)\n" % base_ref
        )
        return 0
    findings, infos = scan_files(root, rel_paths)
    if findings:
        print(
            "check_prompt_output_mode --strict: %d finding(s) vs %s"
            % (len(findings), base_ref)
        )
        _print_findings(findings)
        _print_infos(infos)
        _print_rule()
        return 1
    print(
        "check_prompt_output_mode --strict: OK (0 findings in %d changed in-scope file(s) vs %s)"
        % (len(rel_paths), base_ref)
    )
    _print_infos(infos)
    return 0


def run_check(root: Path, cli_base: str | None, explicit_paths: list[str]) -> int:
    if explicit_paths:
        rel_paths = [p.replace("\\", "/") for p in explicit_paths]
        rel_paths = [p for p in rel_paths if is_in_scope_file(p)]
        scope_desc = "%d explicit path(s)" % len(rel_paths)
    else:
        base_ref = resolve_base_ref(cli_base)
        changed = changed_scanned_files(root, base_ref)
        if changed is None:
            print(
                "check_prompt_output_mode --check: git diff vs %s unavailable; nothing scanned"
                % base_ref
            )
            return 0
        rel_paths = changed
        scope_desc = "%d changed file(s) vs %s" % (len(rel_paths), base_ref)
    findings, infos = scan_files(root, rel_paths)
    print(
        "check_prompt_output_mode --check (advisory, exit 0): %d finding(s) in %s"
        % (len(findings), scope_desc)
    )
    _print_findings(findings)
    _print_infos(infos)
    return 0


def run_audit(root: Path) -> int:
    tracked = tracked_prompt_files(root)
    if tracked is None:
        print(
            "check_prompt_output_mode --audit: WARNING git ls-files unavailable; "
            "nothing scanned (infra gap, exit 0)"
        )
        return 0
    rel_paths = [p for p in tracked if is_in_scope_file(p)]
    findings, infos = scan_files(root, rel_paths)
    no_decl = sum(1 for f in findings if f.kind == "no_output_mode_declaration")
    no_token = sum(1 for f in findings if f.kind == "no_recognized_output_mode_token")
    passed = len(rel_paths) - len(findings)
    print(
        "check_prompt_output_mode --audit (whole-corpus backlog view, exit 0; "
        "never a gate):"
    )
    print("  scanned in-scope files: %d" % len(rel_paths))
    print("  pass: %d" % passed)
    print("  no_output_mode_declaration: %d" % no_decl)
    print("  no_recognized_output_mode_token: %d" % no_token)
    _print_findings(findings)
    _print_infos(infos)
    print(
        "  Shape only, never truth: not validation, not readiness. "
        "Authority: %s." % RULE_AUTHORITY
    )
    return 0


# ---------------------------------------------------------------------------
# Selftest
# ---------------------------------------------------------------------------

def selftest() -> int:
    ok = True

    def check(label: str, got: object, expected: object) -> None:
        nonlocal ok
        status = "PASS" if got == expected else "FAIL"
        if got != expected:
            ok = False
        print("%s  %-58s  expect=%r got=%r" % (status, label, expected, got))

    # --- 1: YAML key + valid token -> declared, no finding ---
    print("--- declaration + token detection ---")
    f, info = evaluate_file_lines("f.md", ["output_mode: file-write"])
    check("1 key form + valid token -> no finding", f, None)

    # --- 2: indented/bulleted key form -> declared ---
    f, info = evaluate_file_lines("f.md", ["  - output_mode: chat-only"])
    check("2 indented/bulleted key form -> no finding", f, None)

    # --- 3: prose bullet -> declared ---
    f, info = evaluate_file_lines("f.md", ["- Output mode: `review-report`"])
    check("3 prose bullet -> no finding", f, None)

    # --- 4: prose plain -> declared ---
    f, info = evaluate_file_lines("f.md", ["Output mode: `chat-only`"])
    check("4 prose plain -> no finding", f, None)

    # --- 5: "output mode for the receiving CA:" -> NOT a declaration ---
    check(
        "5 'output mode for the receiving CA:' -> not a declaration",
        is_declaration_line("Output mode for the receiving CA: `chat-only`"),
        False,
    )
    f, info = evaluate_file_lines(
        "f.md", ["Output mode for the receiving CA: `chat-only`"]
    )
    check("5 file with only that line -> no_output_mode_declaration",
          f.kind if f else None, "no_output_mode_declaration")

    # --- 6: qualified keys -> NOT declarations ---
    check("6a receiver_output_mode: not a declaration",
          is_declaration_line("receiver_output_mode: file-write"), False)
    check("6b reviewer_output_mode: not a declaration",
          is_declaration_line("reviewer_output_mode: review-report"), False)
    check("6c downstream_review_output_mode: not a declaration",
          is_declaration_line("downstream_review_output_mode: review-report"), False)
    check("6d terminal_output_mode: not a declaration",
          is_declaration_line("terminal_output_mode: filed_prompt_plus_paste_ready_copy"),
          False)

    # --- 7: legacy token -> declaration with 0 valid tokens -> finding ---
    f, info = evaluate_file_lines("f.md", ["output_mode: filesystem-output"])
    check("7 legacy token -> no_recognized_output_mode_token",
          f.kind if f else None, "no_recognized_output_mode_token")

    # --- 8: empty value -> declaration, 0 tokens ---
    check("8 tokens_in_line empty value", tokens_in_line("output_mode:"), [])
    f, info = evaluate_file_lines("f.md", ["output_mode:"])
    check("8 file with only empty-value line -> finding",
          f.kind if f else None, "no_recognized_output_mode_token")

    # --- 9: compound tokens -> PASS + INFO ---
    f, info = evaluate_file_lines(
        "f.md",
        ["output_mode: file-write (this artifact) + paste-ready-chat (courier prompt)"],
    )
    check("9 compound tokens -> no finding", f, None)
    check("9 compound tokens -> INFO note present",
          any("2 output-mode tokens" in n for n in info), True)

    # --- 10: "paste-ready chat" (space, no hyphen) -> 0 tokens ---
    check("10 space-separated token variant -> 0 tokens",
          tokens_in_line("output_mode: paste-ready chat"), [])

    # --- 11: two valid declaration lines -> PASS + INFO, no finding ---
    f, info = evaluate_file_lines(
        "f.md",
        [
            "output_mode: file-write",
            "some body text",
            "- Output mode: `file-write`",
        ],
    )
    check("11 two valid declarations -> no finding", f, None)
    check("11 two valid declarations -> multiple-lines INFO note",
          any("multiple output-mode declaration lines" in n for n in info), True)

    # --- 12: no declaration at all -> finding ---
    f, info = evaluate_file_lines("f.md", ["nothing here about modes"])
    check("12 no declaration -> no_output_mode_declaration",
          f.kind if f else None, "no_output_mode_declaration")

    # --- 13: scope function ---
    print()
    print("--- is_in_scope_file ---")
    check("13a review prompt in scope",
          is_in_scope_file("docs/prompts/reviews/x_v0.md"), True)
    check("13b templates excluded",
          is_in_scope_file("docs/prompts/templates/shared/y.md"), False)
    check("13c docs/prompts/README.md excluded",
          is_in_scope_file("docs/prompts/README.md"), False)
    check("13d architecture prompt in scope",
          is_in_scope_file("docs/prompts/architecture/z.md"), True)
    check("13e docs/other excluded (wrong root)",
          is_in_scope_file("docs/other/a.md"), False)
    check("13f non-md excluded",
          is_in_scope_file("docs/prompts/reviews/x_v0.py"), False)

    # --- 14: token-drift insurance (real repo dependence) ---
    print()
    print("--- token-drift insurance (reads real authority file) ---")
    authority_path = repo_root() / ".agents" / "workflow-overlay" / "prompt-orchestration.md"
    if not authority_path.is_file():
        print("FAIL  authority file missing: %s" % authority_path)
        ok = False
    else:
        text = authority_path.read_text(encoding="utf-8")
        extracted = extract_authority_tokens(text)
        check("14 authority tokens == TOKENS constant (no drift)", extracted, TOKENS)

    # --- resolve_base_ref ---
    print()
    print("--- resolve_base_ref ---")
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

    # --- parse_name_status ---
    print()
    print("--- parse_name_status ---")
    check(
        "A/M kept, D dropped, R keeps destination",
        parse_name_status([
            "A\tdocs/prompts/reviews/new_v0.md",
            "M\tdocs/prompts/architecture/a_v0.md",
            "D\tdocs/prompts/reviews/old_v0.md",
            "R100\tdocs/prompts/from_v0.md\tdocs/prompts/to_v0.md",
            "noise",
        ]),
        ["docs/prompts/reviews/new_v0.md", "docs/prompts/architecture/a_v0.md",
         "docs/prompts/to_v0.md"],
    )

    print()
    print("SELFTEST", "OK" if ok else "FAILED")
    return 0 if ok else 1


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def _arg_value(argv: list[str], flag: str) -> str | None:
    if flag in argv:
        idx = argv.index(flag)
        if idx + 1 < len(argv):
            return argv[idx + 1]
    return None


def _collect_check_paths(argv: list[str]) -> list[str]:
    """Positional path arguments given alongside --check (excludes recognized
    flags and the --base value). Empty when --check is used without paths."""
    known_flags = {"--strict", "--check", "--audit", "--selftest", "--force-internal-error"}
    paths: list[str] = []
    skip_next = False
    for tok in argv:
        if skip_next:
            skip_next = False
            continue
        if tok == "--base":
            skip_next = True
            continue
        if tok in known_flags:
            continue
        paths.append(tok)
    return paths


def main(argv: list[str]) -> int:
    # Forced-exception probe: proves the __main__ gating handler
    # (forseti-harness/tests/unit/test_hook_internal_error_gating.py).
    if "--force-internal-error" in argv:
        raise RuntimeError("forced internal error (probe)")
    if "--selftest" in argv:
        return selftest()
    root = repo_root()
    cli_base = _arg_value(argv, "--base")
    if "--strict" in argv:
        return run_strict(root, cli_base)
    if "--check" in argv:
        return run_check(root, cli_base, _collect_check_paths(argv))
    if "--audit" in argv:
        return run_audit(root)
    print(
        "Usage: check_prompt_output_mode.py --strict [--base <ref>] | "
        "--check [--base <ref>] [paths...] | --audit | --selftest"
    )
    print("  --strict    CI gate: exit 1 if a changed in-scope prompt lacks a")
    print("              recognized output-mode declaration")
    print("  --check     same scan, human-readable, always exit 0; explicit")
    print("              paths scan those files directly instead of the diff")
    print("  --audit     whole-corpus backlog view, always exit 0 (never a gate)")
    print("  --selftest  pure-function self-check")
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as exc:
        # GATE FAIL bucket in gating modes (validation-gates.md): an internal
        # checker bug must not read as a green gate. Advisory modes fail open
        # so a bug never bricks the agent.
        sys.stderr.write("check_prompt_output_mode: internal error: %s\n" % exc)
        gating = "--strict" in sys.argv[1:] or "--selftest" in sys.argv[1:]
        sys.exit(1 if gating else 0)
