#!/usr/bin/env python3
"""`review_summary` YAML shape gate (EP-10, narrowed to the born-green subset).

WHAT THIS ENFORCES (shape only)
  For every fenced ```yaml block in an in-scope review-output file that
  carries a top-level `review_summary:` key, validate the courier shape fixed
  by the Adversarial Review Summary Pattern:

    - none of the six forbidden keys are present;
    - `report_path`, when present, points at a file that exists on disk
      (repo-root-relative);
    - a `status: failed` block matches the failed-write shape exactly
      (no `report_path`; `recommendation: blocked`;
      `review_location: chat_only_current_thread`);
    - `recommendation`, when present, is not blank.

  RULE AUTHORITY (never restated here)
    .agents/workflow-overlay/communication-style.md, "Adversarial Review
    Summary Pattern" (~lines 185-255): canonical `review_summary` shape,
    the `recommendation` enum, `report_path` validity, the failed-write
    shape, and the forbidden-key list. If this checker and that section ever
    disagree, the section wins and this checker is the stale party.
    EP handle: EP-10 in
    docs/decisions/overlay_enforcement_placement_classification_v0.md.

NARROWED TO THE BORN-GREEN SUBSET
  EP-10 also lists the `recommendation` enum
  (accept | accept_with_friction | patch_before_acceptance | reject |
  blocked) as substrate-enforceable. That vocabulary is NOT strict here: the
  current corpus already carries an extended, undocumented `recommendation`
  vocabulary from delegated-review-patch lanes (dozens of instances), so
  gating it would not be born green. The owner accepted this narrowing as
  the standing shape (decision 2026-07-10, recorded in validation-gates.md
  and the EP-10 classification row). Out-of-enum `recommendation` values are
  tracked as an ADVISORY enum-drift signal (--audit count/list, --check
  INFO) and NEVER a strict finding.

WHAT THIS DOES NOT DO (PLACEMENT IS NOT AUTHORITY)
  - It never judges review QUALITY or TRUTH: whether the recommendation was
    the right call, whether findings are accurate, or whether the report
    content is good. Shape only (cf. EP-29, receipt-field provenance).
  - It is not a validation or readiness claim. A clean run means the
    `review_summary` block's shape matches the courier pattern -- nothing
    about the review itself.
  - It never requires a `review_summary` block to be present. Whether an
    artifact owed a courier summary at all stays resident judgment; this
    gate only validates blocks that ARE present.

NON-OVERLAP WITH check_review_output_provenance.py
  check_review_output_provenance.py already owns, for the same
  docs/review-outputs/ file family: retrieval-header shape, `reviewed_by` /
  `authored_by` provenance-field presence, the review-use-boundary prose
  requirement, and Markdown fence/diff integrity. This checker does NOT
  duplicate any of those checks. It owns a disjoint surface: the courier
  `review_summary:` YAML block's own field shape (forbidden keys,
  `report_path` existence, the failed-write shape, blank `recommendation`,
  and the `recommendation` enum-drift advisory signal).

HELPER REUSE
  check_dcp_receipt.py's fenced-```yaml-block iteration and top-level
  receipt-key-line detection are the structural model for the block/key
  extraction below, implemented here as a LOCAL EQUIVALENT rather than a
  dynamic import: (1) this checker is deliberately stdlib-only (no PyYAML
  dependency, mirroring check_handoff_pointers.py), so it cannot reuse
  check_dcp_receipt.py's `yaml.safe_load`-based parse; (2) the spec here
  calls for a simpler line-based immediate-child-key parse (2-space indent
  `key: value`, no nested-list parsing) rather than a full YAML document
  parse, so the extraction logic differs in shape from check_dcp_receipt.py
  even where the block-iteration skeleton is the same.

DETECTION CONTRACT (mirrors check_handoff_pointers.py / check_dcp_receipt.py)
  base ref priority: $FORSETI_DIFF_BASE (exact CI event SHA); else
  $GITHUB_BASE_REF -> origin/<ref>; else --base <ref>; else origin/main.
  Diff is three-dot `base...HEAD`, name-status, in-scope
  .md paths only (added/modified/rename-or-copy destinations still present
  in the tree). NO HEAD~1 fallback. If the base cannot be resolved or git
  fails, fail OPEN (exit 0, loud warning) -- the universal Forseti infra-gap
  stance; in CI the base is always present (fetch-depth: 0). Fail-open is
  for INFRASTRUCTURE GAPS ONLY: in --strict and --selftest an unexpected
  internal exception exits 1 (the GATE FAIL bucket, validation-gates.md);
  advisory modes (--check, --audit) fail open on internal error. Forward-only
  by construction: only the current diff is gated in --strict, never
  historical backlog (--audit is the whole-corpus advisory view).

SCOPE
  In-scope file: posix relpath starts `docs/review-outputs/`, ends `.md`,
  basename != `README.md` (same scope rule check_review_output_provenance.py
  uses; not imported, restated here as a two-line predicate).

MODES
  check_review_summary.py --strict [--base <ref>]   CI gate; exit 1 on findings
  check_review_summary.py --check [--base <ref>] [paths...]
                                                      advisory, human-readable, exit 0
  check_review_summary.py --audit                    whole-corpus backlog view, exit 0 (never a gate)
  check_review_summary.py --selftest                 pure-function cases; exit per pass/fail

REGISTRATION
  Registered in .github/workflows/ci.yml (--strict step, single-line run
  format) in the same gate-wave change that added this checker.
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from typing import Callable, NamedTuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _hooklib import (  # noqa: E402  (sys.path pin must precede the import)
    git_out,
    parse_name_status,
    repo_root,
    resolve_base_ref,
)


# ---------------------------------------------------------------------------
# Scope predicate
# ---------------------------------------------------------------------------

REVIEW_OUTPUT_PREFIX = "docs/review-outputs/"


def is_in_scope(relpath: str) -> bool:
    """True if a repo-relative path is a review-output courier candidate.

    Pure function (testable)."""
    p = relpath.replace("\\", "/")
    if not p.startswith(REVIEW_OUTPUT_PREFIX):
        return False
    if not p.endswith(".md"):
        return False
    return Path(p).name != "README.md"


# ---------------------------------------------------------------------------
# Forbidden keys / recommendation enum (communication-style.md)
# ---------------------------------------------------------------------------

FORBIDDEN_KEYS = frozenset({
    "report_written",
    "protected_path_check",
    "hidden_ledger_read",
    "runtime_code_changed",
    "fixture_expansion_performed",
    "harness_or_compiler_or_path_b_run",
})

RECOMMENDATION_ENUM = frozenset({
    "accept",
    "accept_with_friction",
    "patch_before_acceptance",
    "reject",
    "blocked",
})

RULE_AUTHORITY = (
    ".agents/workflow-overlay/communication-style.md "
    "(Adversarial Review Summary Pattern)"
)


# ---------------------------------------------------------------------------
# Pure block extraction (testable) -- local equivalent of
# check_dcp_receipt.py's iter_yaml_blocks / has_receipt_key_line, adapted to
# track line numbers and to target `review_summary:` instead of the DCP
# receipt keys.
# ---------------------------------------------------------------------------

def iter_fenced_yaml_blocks(text: str) -> list[tuple[list[str], int]]:
    """Return (block_lines, first_line_lineno) for every fenced ```yaml block.

    `first_line_lineno` is the 1-indexed source line number of the block's
    first inner line (the line right after the opening fence). A block opens
    on a fence line whose info string contains 'yaml' and closes on the next
    fence line. Pure function (testable)."""
    blocks: list[tuple[list[str], int]] = []
    in_block = False
    buf: list[str] = []
    start_lineno = 0
    for i, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        if not in_block:
            if s.startswith("```") and "yaml" in s.lower():
                in_block = True
                buf = []
                start_lineno = i + 1
        else:
            if s.startswith("```"):
                blocks.append((buf, start_lineno))
                in_block = False
            else:
                buf.append(line)
    # An unterminated final fence: keep what we have (defensive).
    if in_block and buf:
        blocks.append((buf, start_lineno))
    return blocks


_TOPLEVEL_KEY_RE = re.compile(r"^review_summary\s*:")
_CHILD_KEY_RE = re.compile(r"^  ([A-Za-z_][A-Za-z0-9_]*):[ \t]*(.*)$")


def has_review_summary_key_line(block_lines: list[str]) -> bool:
    """True if the block has a TOP-LEVEL (column-0) `review_summary:` key line.

    Deliberately ignores prose or table-cell mentions of `review_summary`
    outside a fenced yaml block, and deeper-nested/value mentions inside one.
    Pure function (testable)."""
    return any(_TOPLEVEL_KEY_RE.match(line) for line in block_lines)


def extract_review_summary_children(
    block_lines: list[str], block_start_lineno: int
) -> tuple[dict[str, str], dict[str, int], int] | None:
    """Immediate child keys of the block's top-level `review_summary:` key.

    Parses 2-space-indent `key: value` lines following the `review_summary:`
    line until indentation drops back to column 0 (a line that does not
    start with two spaces). Deeper nesting (list items under a key, e.g.
    `  advisory_findings:` followed by `    - FF-01: ...`) is walked over,
    not parsed, per spec. Returns (children, lineno_map, key_lineno) or None
    if no top-level `review_summary:` line exists. Pure function (testable).
    """
    idx = None
    for i, line in enumerate(block_lines):
        if _TOPLEVEL_KEY_RE.match(line):
            idx = i
            break
    if idx is None:
        return None
    children: dict[str, str] = {}
    lineno_map: dict[str, int] = {}
    for j in range(idx + 1, len(block_lines)):
        line = block_lines[j]
        if not line.strip():
            continue
        m = _CHILD_KEY_RE.match(line)
        if m is not None:
            key, val = m.group(1), m.group(2).strip()
            if key not in children:  # first occurrence wins
                children[key] = val
                lineno_map[key] = block_start_lineno + j
            continue
        if not line.startswith("  "):
            break  # indentation dropped to column 0: left the mapping
        # deeper-nested line (list item, etc.) -- walked over, not parsed
    return children, lineno_map, block_start_lineno + idx


def _clean(value: str) -> str:
    """Strip surrounding whitespace/quotes/backticks from a scalar value."""
    return value.strip().strip("`'\"").strip()


# ---------------------------------------------------------------------------
# Template/placeholder skip (INFO, never findings)
# ---------------------------------------------------------------------------

def is_template_block(children: dict[str, str]) -> bool:
    """True if a parsed `review_summary` child-key dict is a template/
    placeholder block rather than a real courier summary. Pure function
    (testable)."""
    for v in children.values():
        if " | " in v:
            return True
        cv = _clean(v)
        if cv.startswith("<") and cv.endswith(">"):
            return True

    summary_empty = _clean(children.get("summary", "")) == ""
    next_action_raw = children.get("next_action")
    next_action_empty = next_action_raw is None or _clean(next_action_raw) == ""
    if summary_empty and next_action_empty:
        return True

    reviewed_by = _clean(children.get("reviewed_by", "")).lower()
    if reviewed_by == "operator_to_fill" or reviewed_by.endswith("_to_fill"):
        return True

    return False


# ---------------------------------------------------------------------------
# Findings (testable, pure given an injected path_exists)
# ---------------------------------------------------------------------------

class Finding(NamedTuple):
    source: str
    lineno: int
    code: str
    message: str


class EnumDrift(NamedTuple):
    source: str
    lineno: int
    value: str


def evaluate_review_summary_block(
    rel: str,
    children: dict[str, str],
    lineno_map: dict[str, int],
    key_lineno: int,
    path_exists: Callable[[str], bool],
) -> tuple[list[Finding], list[EnumDrift]]:
    """STRICT findings + audit-only enum-drift signal for one real (non-
    template) `review_summary` block. Pure function given an injected
    `path_exists` (testable)."""
    findings: list[Finding] = []
    drift: list[EnumDrift] = []

    for key in sorted(FORBIDDEN_KEYS & children.keys()):
        findings.append(Finding(
            rel, lineno_map[key], "forbidden_key",
            "`%s` is a forbidden review_summary key. Authority: %s."
            % (key, RULE_AUTHORITY),
        ))

    if "report_path" in children:
        raw = _clean(children["report_path"])
        # A literal YAML null (`null` / `~` / empty) means "no report_path",
        # not a file named "null" -- treat it the same as the key being
        # absent (never a finding), matching YAML null semantics even though
        # this checker does not run a real YAML parser.
        if raw and raw.lower() not in ("null", "~", "none") and not path_exists(raw):
            findings.append(Finding(
                rel, lineno_map["report_path"], "report_path_missing",
                "report_path %r does not exist on disk. Authority: %s."
                % (raw, RULE_AUTHORITY),
            ))

    status = _clean(children.get("status", ""))
    if status == "failed":
        report_path_present = "report_path" in children and _clean(children["report_path"]) != ""
        recommendation = _clean(children.get("recommendation", ""))
        review_location = _clean(children.get("review_location", ""))
        if (
            report_path_present
            or recommendation != "blocked"
            or review_location != "chat_only_current_thread"
        ):
            findings.append(Finding(
                rel, lineno_map.get("status", key_lineno), "failed_write_inconsistent",
                "status: failed requires no report_path, "
                "recommendation: blocked, and "
                "review_location: chat_only_current_thread. Authority: %s."
                % RULE_AUTHORITY,
            ))

    if "recommendation" in children:
        rec = _clean(children["recommendation"])
        if rec == "":
            findings.append(Finding(
                rel, lineno_map["recommendation"], "blank_recommendation",
                "`recommendation` key present with blank value. Authority: %s."
                % RULE_AUTHORITY,
            ))
        elif rec not in RECOMMENDATION_ENUM:
            drift.append(EnumDrift(rel, lineno_map["recommendation"], rec))

    return findings, drift


def file_findings(
    rel: str, text: str, path_exists: Callable[[str], bool]
) -> tuple[list[Finding], list[EnumDrift], int]:
    """All findings, enum-drift entries, and template-skip count for one
    file's text. Pure function given an injected `path_exists` (testable)."""
    findings: list[Finding] = []
    drift: list[EnumDrift] = []
    templates = 0
    for block_lines, start_lineno in iter_fenced_yaml_blocks(text):
        if not has_review_summary_key_line(block_lines):
            continue
        extracted = extract_review_summary_children(block_lines, start_lineno)
        if extracted is None:
            continue
        children, lineno_map, key_lineno = extracted
        if is_template_block(children):
            templates += 1
            continue
        f, d = evaluate_review_summary_block(rel, children, lineno_map, key_lineno, path_exists)
        findings.extend(f)
        drift.extend(d)
    return findings, drift, templates


# ---------------------------------------------------------------------------
# Git plumbing (infra-gap fail-open) -- mirrors check_handoff_pointers.py
# ---------------------------------------------------------------------------

def _git(root: Path, args: list[str], timeout: int = 15) -> tuple[int, str]:
    """Run a git command; return (returncode, stdout). Never raises.

    Thin adapter over the shared _hooklib.git_out (keeps this file's 15s
    default). git_out returns (1, "") on launch failure/timeout instead of
    (-1, ""); callers here only test rc != 0, so the distinction is inert."""
    return git_out(root, args, timeout=timeout)


def changed_in_scope_files(root: Path, base_ref: str) -> list[str] | None:
    """Repo-relative in-scope .md paths changed in base...HEAD. None = infra gap."""
    if _git(root, ["rev-parse", "--verify", "--quiet", "HEAD"])[0] != 0:
        return None
    if _git(root, ["rev-parse", "--verify", "--quiet", base_ref])[0] != 0:
        return None
    code, out = _git(root, ["diff", "--name-status", "%s...HEAD" % base_ref])
    if code != 0:
        return None
    return [p for p in parse_name_status(out.splitlines()) if is_in_scope(p)]


def corpus_files(root: Path) -> list[str] | None:
    """All tracked in-scope files (git ls-files -- docs/review-outputs).

    None = infra gap (git unavailable)."""
    code, out = _git(root, ["ls-files", "--", "docs/review-outputs"])
    if code != 0:
        return None
    return [p for p in (ln.strip() for ln in out.splitlines()) if p and is_in_scope(p)]


# ---------------------------------------------------------------------------
# Scanning
# ---------------------------------------------------------------------------

def _disk_exists(root: Path) -> Callable[[str], bool]:
    def exists(token: str) -> bool:
        return (root / Path(token.replace("/", os.sep))).exists()
    return exists


def scan_files(root: Path, rel_paths: list[str]) -> tuple[list[Finding], list[EnumDrift], int]:
    findings: list[Finding] = []
    drift: list[EnumDrift] = []
    templates = 0
    exists = _disk_exists(root)
    for rel in rel_paths:
        fpath = root / Path(rel.replace("/", os.sep))
        try:
            text = fpath.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        f, d, t = file_findings(rel.replace("\\", "/"), text, exists)
        findings.extend(f)
        drift.extend(d)
        templates += t
    return findings, drift, templates


# ---------------------------------------------------------------------------
# Mode runners
# ---------------------------------------------------------------------------

def _print_findings(findings: list[Finding]) -> None:
    for f in findings:
        print("  %s:%d  ->  %s: %s" % (f.source, f.lineno, f.code, f.message))


def _print_drift(drift: list[EnumDrift], label: str) -> None:
    print("  %s: %d out-of-enum `recommendation` value(s) "
          "(advisory/no-gate: owner accepted 2026-07-10 keeping enum membership "
          "audit-only; the delegated-review-patch extended vocabulary stays unbound)" % (label, len(drift)))
    for d in drift:
        print("    %s:%d  ->  recommendation: %s" % (d.source, d.lineno, d.value))


def run_strict(root: Path, cli_base: str | None) -> int:
    base_ref = resolve_base_ref(cli_base)
    rel_paths = changed_in_scope_files(root, base_ref)
    if rel_paths is None:
        sys.stderr.write(
            "check_review_summary --strict: WARNING git diff vs %s unavailable; "
            "failing OPEN (infra gap, not a pass)\n" % base_ref
        )
        return 0
    findings, _drift, _templates = scan_files(root, rel_paths)
    if findings:
        print("check_review_summary --strict: %d finding(s) vs %s"
              % (len(findings), base_ref))
        _print_findings(findings)
        print("Rule authority: %s" % RULE_AUTHORITY)
        return 1
    print("check_review_summary --strict: OK (0 findings in %d changed in-scope file(s) vs %s)"
          % (len(rel_paths), base_ref))
    return 0


def run_check(root: Path, cli_base: str | None, explicit_paths: list[str]) -> int:
    if explicit_paths:
        rel_paths = [p for p in explicit_paths if is_in_scope(p)]
        base_ref = None
    else:
        base_ref = resolve_base_ref(cli_base)
        rel_paths = changed_in_scope_files(root, base_ref)
        if rel_paths is None:
            print("check_review_summary --check: git diff vs %s unavailable; nothing scanned"
                  % base_ref)
            return 0
    findings, drift, templates = scan_files(root, rel_paths)
    scope_desc = ("%d explicit path(s)" % len(rel_paths)) if base_ref is None else (
        "%d changed in-scope file(s) vs %s" % (len(rel_paths), base_ref)
    )
    print("check_review_summary --check (advisory, exit 0): %d finding(s) in %s"
          % (len(findings), scope_desc))
    _print_findings(findings)
    print("  templates/placeholders skipped: %d" % templates)
    if drift:
        _print_drift(drift, "INFO")
    return 0


def run_audit(root: Path) -> int:
    rel_paths = corpus_files(root)
    if rel_paths is None:
        print("check_review_summary --audit: fail-open (infra gap): git ls-files unavailable")
        return 0
    findings, drift, templates = scan_files(root, rel_paths)
    print("check_review_summary --audit (whole-corpus backlog view, exit 0; never a gate):")
    print("  in-scope files scanned: %d" % len(rel_paths))
    print("  findings by type:")
    if findings:
        by_code: dict[str, int] = {}
        for f in findings:
            by_code[f.code] = by_code.get(f.code, 0) + 1
        for code in sorted(by_code):
            print("    %s: %d" % (code, by_code[code]))
        _print_findings(findings)
    else:
        print("    (none)")
    print("  templates/placeholders skipped: %d" % templates)
    _print_drift(drift, "enum-drift advisory count")
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
        print("%s  %-60s  expect=%r got=%r" % (status, label, expected, got))

    # --- scope predicate ---
    print("--- is_in_scope ---")
    check("in-scope review output",
          is_in_scope("docs/review-outputs/adversarial-artifact-reviews/x_v0.md"), True)
    check("README excluded",
          is_in_scope("docs/review-outputs/README.md"), False)
    check("docs/prompts excluded",
          is_in_scope("docs/prompts/reviews/x_v0.md"), False)
    check("non-md excluded",
          is_in_scope("docs/review-outputs/x_v0.txt"), False)

    # --- case 1: real block extracted; prose mention not extracted ---
    print()
    print("--- block detection (case 1: real vs prose) ---")
    text1 = (
        "intro\n"
        "| col | review_summary |\n"
        "|---|---|\n"
        "| a   | mentions review_summary in a cell |\n"
        "```yaml\n"
        "review_summary:\n"
        "  status: completed\n"
        "  recommendation: accept\n"
        "```\n"
    )
    blocks1 = iter_fenced_yaml_blocks(text1)
    check("only the fenced yaml block is extracted", len(blocks1), 1)
    check("extracted block has top-level review_summary key",
          has_review_summary_key_line(blocks1[0][0]), True)

    # --- case 2: unrelated fenced yaml (direction_change_propagation) ignored ---
    print()
    print("--- block detection (case 2: unrelated fenced yaml ignored) ---")
    text2 = "```yaml\ndirection_change_propagation:\n  trigger: workflow_authority\n```\n"
    blocks2 = iter_fenced_yaml_blocks(text2)
    check("one fenced yaml block found", len(blocks2), 1)
    check("no top-level review_summary key in unrelated block",
          has_review_summary_key_line(blocks2[0][0]), False)

    # --- template skip cases ---
    print()
    print("--- is_template_block ---")
    check("case 3: piped recommendation alternatives",
          is_template_block({"recommendation": "accept | accept_with_friction | reject"}), True)
    check("case 4: angle-bracket placeholder",
          is_template_block({"recommendation": "<one recommendation from the allowed vocabulary>"}), True)
    check("case 5a: empty summary + missing next_action",
          is_template_block({"summary": '""'}), True)
    check("case 5b: empty summary + empty next_action",
          is_template_block({"summary": "", "next_action": ""}), True)
    check("case: operator_to_fill reviewed_by",
          is_template_block({"reviewed_by": "operator_to_fill", "summary": "x", "next_action": "y"}), True)
    check("real block is not a template",
          is_template_block({
              "status": "completed",
              "recommendation": "accept_with_friction",
              "reviewed_by": "claude-opus-4.8",
              "authored_by": "claude-opus-4.8",
              "summary": "One sentence describing the review result.",
              "next_action": "One concrete next step",
          }), False)

    # --- case 6: each forbidden key individually -> finding ---
    print()
    print("--- forbidden keys (case 6) ---")
    exists_all: Callable[[str], bool] = lambda _t: True  # noqa: E731
    base_children = {
        "status": "completed",
        "recommendation": "accept",
        "summary": "s",
        "next_action": "n",
    }
    for key in sorted(FORBIDDEN_KEYS):
        children = {**base_children, key: "true"}
        lineno_map = {k: i + 1 for i, k in enumerate(children)}
        findings, _drift = evaluate_review_summary_block(
            "f.md", children, lineno_map, 1, exists_all)
        codes = {f.code for f in findings}
        check("forbidden key %r flagged" % key, "forbidden_key" in codes, True)

    # --- case 7: clean canonical block -> no findings ---
    print()
    print("--- case 7: clean canonical block ---")
    canonical = {
        "status": "completed",
        "report_path": "docs/review-outputs/example_adversarial_review_v0.md",
        "recommendation": "accept_with_friction",
        "reviewed_by": "claude-opus-4.8",
        "authored_by": "claude-opus-4.8",
        "summary": "One sentence describing the review result.",
        "next_action": "One concrete next step",
    }
    lineno_map = {k: i + 1 for i, k in enumerate(canonical)}
    findings, drift = evaluate_review_summary_block(
        "f.md", canonical, lineno_map, 1, exists_all)
    check("clean canonical block -> no findings", findings, [])
    check("clean canonical block -> no enum drift", drift, [])

    # --- case 8/9: report_path existing/missing ---
    print()
    print("--- case 8/9: report_path existence ---")
    exists_none: Callable[[str], bool] = lambda _t: False  # noqa: E731
    findings, _ = evaluate_review_summary_block(
        "f.md", {"report_path": "docs/review-outputs/x.md"},
        {"report_path": 1}, 1, exists_all)
    check("case 8: existing report_path -> no finding",
          any(f.code == "report_path_missing" for f in findings), False)
    findings, _ = evaluate_review_summary_block(
        "f.md", {"report_path": "docs/review-outputs/x.md"},
        {"report_path": 1}, 1, exists_none)
    check("case 9: missing report_path file -> finding",
          any(f.code == "report_path_missing" for f in findings), True)
    findings, _ = evaluate_review_summary_block(
        "f.md", {"report_path": "null"}, {"report_path": 1}, 1, exists_none)
    check("report_path: null (YAML null) -> no finding, not a literal path",
          any(f.code == "report_path_missing" for f in findings), False)

    # --- case 10: no report_path key -> never required ---
    print()
    print("--- case 10: report_path never required ---")
    findings, _ = evaluate_review_summary_block(
        "f.md", {"status": "completed", "recommendation": "accept"},
        {"status": 1, "recommendation": 2}, 1, exists_none)
    check("no report_path key -> no report_path_missing finding",
          any(f.code == "report_path_missing" for f in findings), False)

    # --- case 11/12: failed-write shape ---
    print()
    print("--- case 11/12: failed-write inconsistency ---")
    findings, _ = evaluate_review_summary_block(
        "f.md",
        {"status": "failed", "report_path": "docs/review-outputs/x.md",
         "recommendation": "blocked", "review_location": "chat_only_current_thread"},
        {"status": 1, "report_path": 2, "recommendation": 3, "review_location": 4},
        1, exists_all)
    check("case 11: status failed + report_path present -> finding",
          any(f.code == "failed_write_inconsistent" for f in findings), True)
    findings, _ = evaluate_review_summary_block(
        "f.md",
        {"status": "failed", "recommendation": "blocked",
         "review_location": "chat_only_current_thread"},
        {"status": 1, "recommendation": 2, "review_location": 3},
        1, exists_all)
    check("case 12: status failed + correct failed shape -> clean",
          any(f.code == "failed_write_inconsistent" for f in findings), False)

    # --- case 13: blank recommendation finding; out-of-enum not a finding ---
    print()
    print("--- case 13: recommendation blank vs out-of-enum ---")
    findings, _ = evaluate_review_summary_block(
        "f.md", {"recommendation": ""}, {"recommendation": 1}, 1, exists_all)
    check("blank recommendation -> finding",
          any(f.code == "blank_recommendation" for f in findings), True)
    findings, drift = evaluate_review_summary_block(
        "f.md", {"recommendation": "keep"}, {"recommendation": 1}, 1, exists_all)
    check("out-of-enum recommendation -> NO strict finding", findings, [])
    check("out-of-enum recommendation -> counted in enum-drift", len(drift), 1)
    check("enum-drift value recorded", drift[0].value, "keep")

    # --- extract_review_summary_children: deeper nesting not parsed ---
    print()
    print("--- extract_review_summary_children ---")
    block = [
        "review_summary:",
        "  status: completed",
        "  advisory_findings:",
        "    - FF-01: Short finding title",
        "  next_action: done",
    ]
    extracted = extract_review_summary_children(block, 10)
    assert extracted is not None
    children, lineno_map, key_lineno = extracted
    check("advisory_findings key captured with empty value",
          children.get("advisory_findings"), "")
    check("nested list item not parsed as a key",
          "FF-01" in children, False)
    check("next_action still captured after nested list item",
          children.get("next_action"), "done")
    check("key_lineno points at the review_summary: line", key_lineno, 10)
    check("status lineno correct", lineno_map.get("status"), 11)

    # --- file_findings: end-to-end wiring, report_path via real disk check ---
    print()
    print("--- file_findings (end-to-end) ---")
    good_text = (
        "```yaml\n"
        "review_summary:\n"
        "  status: completed\n"
        "  recommendation: accept\n"
        "  reviewed_by: claude-opus-4.8\n"
        "  authored_by: claude-opus-4.8\n"
        "  summary: \"One sentence describing the review result.\"\n"
        "  next_action: \"One concrete next step\"\n"
        "```\n"
    )
    f, d, t = file_findings("f.md", good_text, exists_all)
    check("file_findings: clean real block -> no findings", f, [])
    check("file_findings: clean real block -> no templates skipped", t, 0)
    tmpl_text = (
        "```yaml\n"
        "review_summary:\n"
        "  status: completed\n"
        "  recommendation: accept | reject\n"
        "```\n"
    )
    f, d, t = file_findings("f.md", tmpl_text, exists_all)
    check("file_findings: template block skipped, no findings", (f, t), ([], 1))

    # --- parse_name_status / resolve_base_ref (git plumbing, mirrors siblings) ---
    print()
    print("--- parse_name_status ---")
    check("A/M kept, D dropped, R keeps destination",
          parse_name_status([
              "A\tdocs/review-outputs/new_v0.md",
              "M\tdocs/review-outputs/existing_v0.md",
              "D\tdocs/review-outputs/old_v0.md",
              "R100\tdocs/review-outputs/from_v0.md\tdocs/review-outputs/to_v0.md",
              "noise",
          ]),
          ["docs/review-outputs/new_v0.md", "docs/review-outputs/existing_v0.md",
           "docs/review-outputs/to_v0.md"])

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


def _positional_paths(argv: list[str]) -> list[str]:
    out: list[str] = []
    skip_next = False
    for a in argv:
        if skip_next:
            skip_next = False
            continue
        if a == "--base":
            skip_next = True
            continue
        if a.startswith("--"):
            continue
        out.append(a)
    return out


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
        return run_check(root, cli_base, _positional_paths(argv))
    if "--audit" in argv:
        return run_audit(root)
    print("Usage: check_review_summary.py --strict [--base <ref>] "
          "| --check [--base <ref>] [paths...] | --audit | --selftest")
    print("  --strict    CI gate: exit 1 if a changed review-output file has a")
    print("              malformed review_summary block")
    print("  --check     same scan, human-readable, always exit 0; optional")
    print("              explicit paths instead of the changed-file diff")
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
        sys.stderr.write("check_review_summary: internal error: %s\n" % exc)
        gating = "--strict" in sys.argv[1:] or "--selftest" in sys.argv[1:]
        sys.exit(1 if gating else 0)
