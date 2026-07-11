#!/usr/bin/env python3
"""Direction-change-propagation receipt SHAPE gate -- STRICT CI gate.

WHAT THIS DOES
  Validates the SHAPE of `direction_change_propagation` receipts (and
  `direction_change_propagation_blocker` blockers) that appear in CHANGED .md
  files in this PR's diff. For each REAL receipt block it checks the
  deterministic shape the contract fixes:
    - required keys present and non-empty;
    - `trigger` is one of the seven controlled trigger values;
    - `related_triggers`, when present, draws only from that same vocabulary;
    - `non_claims` is a non-empty list.
  The rule is owned by:

      .agents/workflow-overlay/source-of-truth.md  (Doctrine Change Propagation Contract)

  This script does NOT restate that rule. It is a thin structural tripwire that
  references the authority above. If the contract and this checker ever
  disagree, the contract wins and this checker is the stale party.

WHAT THIS GATE DOES *NOT* DO (the over-edge boundary -- PLACEMENT IS NOT AUTHORITY)
  - It does NOT decide whether an edit is doctrine-changing. "Is this edit
    doctrine-changing?" is genuine judgment; a hook that demanded a receipt on
    every changed overlay file would false-block a typo fix. So this gate never
    requires a receipt to be PRESENT -- it only validates receipts that ARE
    present. The "you forgot the receipt entirely" case stays resident judgment
    (the EP-09 over-edge in the enforcement-placement classification).
  - It does NOT verify the TRUTH of any field: that the listed
    `controlling_sources_updated` were really updated, or that
    `downstream_surfaces_checked` were really checked, is the human/author's
    job. A substrate checks a receipt's SHAPE, never its truth
    (cf. the receipt-field provenance gate in validation-gates.md).
  - It does NOT enforce the inline-receipt cap, the archive pointer, or the
    "no standalone receipt files" rule. Those are receipt-storage hygiene, are
    not born-green on the current corpus (several controlling files already hold
    >2 inline receipts), and would red-line nearly every doctrine edit if made
    strict. They stay resident / advisory, out of this gate's scope.

TEMPLATE BLOCKS ARE SKIPPED
  The contract file itself defines a receipt TEMPLATE (`trigger: a | b | c ...`,
  `doctrine_changed: "<one sentence>"`). Those are examples, not receipts. A
  block is treated as a template -- and skipped -- when its `trigger` value
  contains a pipe, or a required scalar is a `<...>` placeholder. Real receipts
  never look like that.

WHY STRICT (not report-mode)
  The receipt contract is one of the highest-frequency overlay rules (almost
  every doctrine/overlay edit owes a receipt) and was 100% actor-carried -- a
  malformed receipt (e.g. an invalid `trigger`) would sail through. Only a red
  check closes that. The gate is BORN GREEN: every real receipt in the current
  corpus passes the shape predicate (verify with --audit), so adopting strict
  now matches the clean state without a red-main event.

DETECTION CONTRACT (mirrors header_index.py / check_deletion_evidence.py --strict)
  base ref priority: $FORSETI_DIFF_BASE (exact CI event SHA); else
  $GITHUB_BASE_REF -> origin/<ref>; else --base <ref>; else origin/main.
  Diff is three-dot `base...HEAD` (the PR's net change), name-only,
  .md files only, added/modified (ACMR). NO HEAD~1 fallback. If the base cannot
  be resolved or git fails, fail OPEN (exit 0, loud warning) -- the universal
  Forseti infra-gap stance; in CI the base is always present (fetch-depth: 0).

  For each changed .md file, ALL real receipt blocks in that file are validated
  (not only diff-added lines): touching a doctrine file re-checks its receipts.
  This requires those receipts to be born-green (they are; see --audit).

HARD BOUNDARY
  Read-only. Fail-open ONLY for infrastructure gaps (no git, no PyYAML, base
  unresolvable). A PRESENT receipt whose shape is invalid, or a receipt block
  that cannot be parsed as YAML, is a real finding -- never fail-open.

MODES
  check_dcp_receipt.py --strict     fail (exit 1) on findings; CI gate
  check_dcp_receipt.py --report     same findings, advisory (exit 0)
  check_dcp_receipt.py --check      alias for --report
  check_dcp_receipt.py --audit      whole-repo advisory scan (born-green check); exit 0
  check_dcp_receipt.py --selftest   pure-function cases; exit 0/1

Contract + archive:
  .agents/workflow-overlay/source-of-truth.md  (Doctrine Change Propagation Contract)
  docs/decisions/dcp_receipts_archive_v0.md
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

# Authority this checker references (it does not restate the rule).
RULE_AUTHORITY = ".agents/workflow-overlay/source-of-truth.md (Doctrine Change Propagation Contract)"
PRINCIPLE = ".agents/workflow-overlay/validation-gates.md (Enforcement Placement)"

RECEIPT_KEY = "direction_change_propagation"
BLOCKER_KEY = "direction_change_propagation_blocker"

# The seven controlled trigger values (source-of-truth.md). Single-sourced from
# the contract; if the contract's vocabulary changes, update this set.
TRIGGER_ENUM = frozenset({
    "product_doctrine",
    "architecture_doctrine",
    "workflow_authority",
    "validation_philosophy",
    "review_authority",
    "output_authority",
    "lifecycle_boundary",
})

# Required keys (presence + non-empty). related_triggers is optional. The
# storage-hygiene fields (intentionally_not_updated, stale_language_search) are
# NOT required here -- real receipts omit them legitimately (e.g. a purely
# additive change), so requiring them would not be born-green.
REQUIRED_RECEIPT_KEYS = ("doctrine_changed", "trigger", "controlling_sources_updated", "non_claims")
REQUIRED_BLOCKER_KEYS = ("doctrine_changed", "trigger", "blocking_surface", "attempted_check", "allowed_next_step", "non_claims")

# Walk-prune dirs for --audit.
_PRUNE_DIRS = {".git", "node_modules", "__pycache__"}


def repo_root() -> Path:
    """Repo root, derived from this file's location (.agents/hooks/<this>)."""
    return Path(__file__).resolve().parents[2]


# ---------------------------------------------------------------------------
# Pure block extraction + classification (testable)
# ---------------------------------------------------------------------------

def iter_yaml_blocks(text: str) -> list[str]:
    """Return the inner text of every fenced ```yaml block in `text`.

    A block opens on a fence line whose info string contains 'yaml' and closes
    on the next fence line. Pure function (testable)."""
    blocks: list[str] = []
    in_block = False
    buf: list[str] = []
    for line in text.splitlines():
        s = line.strip()
        if not in_block:
            if s.startswith("```") and "yaml" in s.lower():
                in_block = True
                buf = []
        else:
            if s.startswith("```"):
                blocks.append("\n".join(buf))
                in_block = False
            else:
                buf.append(line)
    # An unterminated final fence: keep what we have (defensive).
    if in_block and buf:
        blocks.append("\n".join(buf))
    return blocks


_RECEIPT_KEY_LINE_RE = re.compile(
    r"^(?:%s|%s)\s*:" % (RECEIPT_KEY, BLOCKER_KEY), re.MULTILINE
)


def has_receipt_key_line(block: str) -> bool:
    """True if the block has a TOP-LEVEL (column-0) receipt/blocker key line.

    This is the receipt-block signal. It deliberately ignores prose or nested
    values that merely mention `direction_change_propagation` (e.g. a review
    finding ABOUT a receipt, or a `line_or_section: direction_change_propagation.x`
    value) -- those are not receipt blocks. Pure function (testable)."""
    return bool(_RECEIPT_KEY_LINE_RE.search(block))


def _is_placeholder(value: object) -> bool:
    """True if a scalar looks like a contract template placeholder (`<...>`)."""
    if not isinstance(value, str):
        return False
    v = value.strip().strip("`'\"").strip()
    return v.startswith("<") and v.endswith(">")


def is_template_receipt(inner: dict) -> bool:
    """True if a parsed receipt/blocker dict is a contract TEMPLATE/example, not
    a real receipt. Templates enumerate the trigger options with pipes
    (`a | b | c`) and use `<...>` placeholders for scalars. Pure function."""
    if not isinstance(inner, dict):
        return False
    trig = inner.get("trigger")
    if isinstance(trig, str) and "|" in trig:
        return True
    for k in ("doctrine_changed", "blocking_surface", "attempted_check", "allowed_next_step"):
        if _is_placeholder(inner.get(k)):
            return True
    return False


def _nonempty_str(v: object) -> bool:
    return isinstance(v, str) and v.strip() != ""


def _nonempty_list(v: object) -> bool:
    return isinstance(v, list) and len(v) > 0


def receipt_problems(inner: dict, kind: str) -> list[str]:
    """Shape problems for a real receipt/blocker inner dict (empty == ok).

    `kind` is RECEIPT_KEY or BLOCKER_KEY. Pure function (testable)."""
    problems: list[str] = []
    if not isinstance(inner, dict):
        return ["%s: block is not a mapping" % kind]

    required = REQUIRED_BLOCKER_KEYS if kind == BLOCKER_KEY else REQUIRED_RECEIPT_KEYS
    for key in required:
        val = inner.get(key)
        if key in ("non_claims", "controlling_sources_updated"):
            if not _nonempty_list(val):
                problems.append("`%s` missing or not a non-empty list" % key)
        else:
            if not _nonempty_str(val):
                problems.append("`%s` missing or empty" % key)

    trig = inner.get("trigger")
    if isinstance(trig, str) and trig.strip() and trig.strip() not in TRIGGER_ENUM:
        problems.append(
            "`trigger` is %r, must be one of %s"
            % (trig.strip(), ", ".join(sorted(TRIGGER_ENUM)))
        )

    rel = inner.get("related_triggers")
    if rel is not None:
        if not isinstance(rel, list):
            problems.append("`related_triggers` must be a list when present")
        else:
            bad = [t for t in rel if not (isinstance(t, str) and t.strip() in TRIGGER_ENUM)]
            if bad:
                problems.append(
                    "`related_triggers` has out-of-vocabulary value(s): %r" % bad
                )
    return problems


def file_findings(text: str, relposix: str, yaml_mod) -> list[str]:
    """All receipt-shape findings for one file's text (empty == ok).

    A yaml block is validated only when it has a TOP-LEVEL receipt/blocker key
    (has_receipt_key_line) -- prose mentions and review findings ABOUT receipts
    are ignored. Within such a block:
      - template/example blocks (pipe trigger, `<...>` placeholders) are skipped;
      - note-marker blocks that reuse the receipt key without a `trigger`
        (e.g. `direction_change_propagation: {note:, authority:, date:}`,
        a pre-existing downstream-surface marker convention) are NOT receipts
        and are skipped;
      - a real receipt (has `trigger`) is shape-validated.
    A block WITH a top-level receipt key that fails YAML parse is a finding (a
    malformed real receipt), not a skip. Pure given an injected yaml module."""
    findings: list[str] = []
    for block in iter_yaml_blocks(text):
        if not has_receipt_key_line(block):
            continue
        try:
            doc = yaml_mod.safe_load(block)
        except Exception as exc:  # malformed receipt-bearing yaml -> real finding
            findings.append("%s: unparseable receipt block (%s)" % (relposix, exc))
            continue
        if not isinstance(doc, dict):
            continue
        for kind in (RECEIPT_KEY, BLOCKER_KEY):
            if kind not in doc:
                continue
            inner = doc.get(kind)
            if not isinstance(inner, dict):
                continue
            if is_template_receipt(inner):
                continue  # contract template / example, not a real receipt
            if "trigger" not in inner:
                continue  # note-marker / non-receipt reuse of the key; not a receipt
            for p in receipt_problems(inner, kind):
                findings.append("%s: %s" % (relposix, p))
    return findings


# ---------------------------------------------------------------------------
# Git diff-scoping (mirrors check_deletion_evidence.py / header_index.py)
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
    """Base ref for diff-scoping (mirrors header_index.py / deletion-evidence)."""
    ci_base = os.environ.get("FORSETI_DIFF_BASE", "").strip()
    if ci_base:
        return ci_base
    gh_base = os.environ.get("GITHUB_BASE_REF", "").strip()
    if gh_base:
        return "origin/%s" % gh_base
    if cli_base:
        return cli_base
    return "origin/main"


def changed_md_files(root: Path, base_ref: str) -> list[str] | None:
    """Added/modified .md relpaths in `base_ref...HEAD`. None on a git infra gap."""
    if _git(root, ["rev-parse", "--verify", "--quiet", "HEAD"])[0] != 0:
        return None
    if _git(root, ["rev-parse", "--verify", "--quiet", base_ref])[0] != 0:
        return None
    rc, out = _git(
        root,
        ["diff", "--diff-filter=ACMR", "--find-renames", "--name-only",
         "%s...HEAD" % base_ref],
    )
    if rc != 0:
        return None
    return [ln.strip() for ln in out.splitlines() if ln.strip().endswith(".md")]


# ---------------------------------------------------------------------------
# Scans
# ---------------------------------------------------------------------------

def scan_paths(root: Path, relpaths: list[str], yaml_mod) -> list[str]:
    """Validate receipts in the given repo-relative .md paths."""
    findings: list[str] = []
    for rel in relpaths:
        p = root / rel
        if not p.is_file():
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        findings.extend(file_findings(text, rel, yaml_mod))
    return findings


def all_md_files(root: Path) -> list[str]:
    """Every .md relpath under the repo (pruned of .git/node_modules/__pycache__)."""
    out: list[str] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in _PRUNE_DIRS and not d.startswith(".git")]
        for fname in filenames:
            if fname.endswith(".md"):
                out.append((Path(dirpath) / fname).relative_to(root).as_posix())
    return sorted(out)


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

def run(root: Path, mode: str, cli_base: str | None) -> int:
    try:
        import yaml
    except Exception:
        print("check_dcp_receipt --%s: fail-open (infra gap): PyYAML unavailable -- nothing to gate" % mode)
        return 0

    if mode == "audit":
        relpaths = all_md_files(root)
        findings = scan_paths(root, relpaths, yaml)
        if findings:
            print("check_dcp_receipt --audit: %d receipt-shape finding(s) across the repo "
                  "(advisory, exit 0):" % len(findings))
            for f in findings:
                print("  " + f)
        else:
            print("check_dcp_receipt --audit: OK -- every real receipt in the repo is shape-valid "
                  "(%d .md scanned)" % len(relpaths))
        return 0

    base_ref = resolve_base_ref(cli_base)
    changed = changed_md_files(root, base_ref)
    if changed is None:
        print("check_dcp_receipt --%s: fail-open (infra gap): git/diff unavailable "
              "(base '%s') -- nothing to gate" % (mode, base_ref))
        return 0
    if not changed:
        print("check_dcp_receipt --%s: no changed .md files in this diff -- OK" % mode)
        return 0

    findings = scan_paths(root, changed, yaml)
    if findings:
        print("check_dcp_receipt --%s: %d receipt-shape finding(s) on changed .md files "
              "(base: %s):" % (mode, len(findings), base_ref))
        for f in findings:
            print("  " + f)
        print("  Rule authority: %s" % RULE_AUTHORITY)
        return 1 if mode == "strict" else 0
    print("check_dcp_receipt --%s: OK -- every real receipt in the changed .md files is "
          "shape-valid (base: %s)" % (mode, base_ref))
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
        print("%s  %-54s got=%r" % (status, label, got))

    # --- iter_yaml_blocks ---
    md = "intro\n```yaml\na: 1\n```\nmid\n```yaml\nb: 2\n```\nend\n"
    check("iter_yaml_blocks count", len(iter_yaml_blocks(md)), 2)
    check("iter_yaml_blocks no fence", iter_yaml_blocks("no fence here"), [])

    # --- has_receipt_key_line (column-0 key vs prose/value mention) ---
    check("key line at column 0",
          has_receipt_key_line("direction_change_propagation:\n  trigger: x"), True)
    check("blocker key line at column 0",
          has_receipt_key_line("direction_change_propagation_blocker:\n  trigger: x"), True)
    check("key only in a value is NOT a receipt block",
          has_receipt_key_line("line_or_section: direction_change_propagation.downstream\nfinding: F-05"), False)
    check("key only in prose is NOT a receipt block",
          has_receipt_key_line("the direction_change_propagation receipt is absent"), False)

    # --- is_template_receipt ---
    check("template via pipe trigger",
          is_template_receipt({"trigger": "product_doctrine | architecture_doctrine"}), True)
    check("template via placeholder",
          is_template_receipt({"trigger": "workflow_authority", "doctrine_changed": "<one sentence>"}), True)
    check("real receipt not template",
          is_template_receipt({"trigger": "workflow_authority", "doctrine_changed": "real change"}), False)

    # --- receipt_problems (RECEIPT) ---
    good = {
        "doctrine_changed": "a real one-sentence change",
        "trigger": "workflow_authority",
        "controlling_sources_updated": ["x.md"],
        "non_claims": ["not validation", "not readiness"],
    }
    check("good receipt", receipt_problems(good, RECEIPT_KEY), [])
    check("good receipt + valid related_triggers",
          receipt_problems({**good, "related_triggers": ["output_authority"]}, RECEIPT_KEY), [])
    check("bad trigger flagged",
          any("`trigger`" in p for p in receipt_problems({**good, "trigger": "made_up"}, RECEIPT_KEY)), True)
    check("missing non_claims flagged",
          any("`non_claims`" in p for p in receipt_problems({**good, "non_claims": []}, RECEIPT_KEY)), True)
    check("empty doctrine_changed flagged",
          any("doctrine_changed" in p for p in receipt_problems({**good, "doctrine_changed": "  "}, RECEIPT_KEY)), True)
    check("controlling_sources_updated as scalar flagged",
          any("controlling_sources_updated" in p for p in receipt_problems({**good, "controlling_sources_updated": "x.md"}, RECEIPT_KEY)), True)
    check("bad related_triggers flagged",
          any("related_triggers" in p for p in receipt_problems({**good, "related_triggers": ["nope"]}, RECEIPT_KEY)), True)

    # --- receipt_problems (BLOCKER) ---
    good_blocker = {
        "doctrine_changed": "a blocked change",
        "trigger": "review_authority",
        "blocking_surface": "missing X",
        "attempted_check": "tried Y",
        "allowed_next_step": "do Z",
        "non_claims": ["not validation"],
    }
    check("good blocker", receipt_problems(good_blocker, BLOCKER_KEY), [])
    check("blocker missing allowed_next_step flagged",
          any("allowed_next_step" in p for p in receipt_problems({k: v for k, v in good_blocker.items() if k != "allowed_next_step"}, BLOCKER_KEY)), True)

    # --- file_findings (needs a real YAML parser; skip gracefully if absent) ---
    try:
        import yaml as _yaml
    except Exception:
        print("SKIP  file_findings cases (PyYAML unavailable)")
        _yaml = None
    if _yaml is not None:
        def fence(body: str) -> str:
            return "```yaml\n%s\n```" % body
        bad_real = ("direction_change_propagation:\n"
                    "  doctrine_changed: a real change\n"
                    "  trigger: made_up\n"
                    "  controlling_sources_updated:\n    - x.md\n"
                    "  non_claims:\n    - not validation\n")
        tmpl = ("direction_change_propagation:\n"
                "  trigger: product_doctrine | architecture_doctrine\n"
                "  doctrine_changed: \"<one sentence>\"\n")
        note_marker = ("direction_change_propagation:\n"
                       "  note: this file is a downstream surface of propagation X\n"
                       "  authority: docs/decisions/foo_v0.md\n")
        good_real = ("direction_change_propagation:\n"
                     "  doctrine_changed: a real change\n"
                     "  trigger: workflow_authority\n"
                     "  controlling_sources_updated:\n    - x.md\n"
                     "  non_claims:\n    - not validation\n")
        check("file_findings flags bad real receipt",
              len(file_findings(fence(bad_real), "f.md", _yaml)), 1)
        check("file_findings passes good real receipt",
              file_findings(fence(good_real), "f.md", _yaml), [])
        check("file_findings skips template",
              file_findings(fence(tmpl), "f.md", _yaml), [])
        check("file_findings skips note-marker (no trigger)",
              file_findings(fence(note_marker), "f.md", _yaml), [])
        check("file_findings ignores non-receipt yaml",
              file_findings("```yaml\na: 1\n```", "f.md", _yaml), [])
        check("file_findings ignores prose mention of the key",
              file_findings("```yaml\nfinding: the direction_change_propagation receipt is absent\n```", "f.md", _yaml), [])

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
    # Forced-exception probe: proves the __main__ gating handler
    # (forseti-harness/tests/unit/test_hook_internal_error_gating.py).
    if "--force-internal-error" in argv:
        raise RuntimeError("forced internal error (probe)")
    if "--selftest" in argv:
        return selftest()
    try:
        root = repo_root()
    except Exception as exc:
        sys.stderr.write("check_dcp_receipt: cannot determine repo root: %s\n" % exc)
        return 0
    cli_base: str | None = None
    if "--base" in argv:
        idx = argv.index("--base")
        if idx + 1 < len(argv):
            cli_base = argv[idx + 1]
    if "--audit" in argv:
        return run(root, "audit", cli_base)
    if "--strict" in argv:
        return run(root, "strict", cli_base)
    if "--report" in argv or "--check" in argv:
        return run(root, "report", cli_base)
    print("Usage: check_dcp_receipt.py --strict | --report | --check | --audit | --selftest [--base <ref>]")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as exc:
        # GATE FAIL bucket in gating modes (validation-gates.md; EP-35
        # delegated review FIND-02 class sweep): an internal checker bug must
        # not read as a green gate -- fail-open here is for infra gaps only
        # (see HARD BOUNDARY). Advisory modes fail open so a bug never bricks
        # the agent.
        sys.stderr.write("check_dcp_receipt: internal error: %s\n" % exc)
        gating = "--strict" in sys.argv[1:] or "--selftest" in sys.argv[1:]
        sys.exit(1 if gating else 0)
