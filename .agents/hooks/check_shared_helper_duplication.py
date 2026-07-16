#!/usr/bin/env python3
"""Shared-helper duplication guard (adoption-rule mechanical backstop).

WHAT THIS DOES
  Diff-scoped, forward-only: flags an ADDED line that privately re-defines a
  shared helper the owning home already provides --

  - anywhere in scope: ``def _utc_now`` / ``def _now_utc`` / ``def _utc_now_z``
    / ``def _utc_now_iso`` / ``def _sha256*`` / ``def _as_dict`` /
    ``def _hash_file`` / ``def _string_or_none`` /
    ``def _non_empty_string_or_none`` / ``def _int_or_none`` /
    ``def _bool_or_none``;
  - in ``forseti-harness/`` only (projection-surface helpers; home
    ``source_capture/projection_shared.py``): ``def _is_forbidden_field_name``
    / ``def _first_match`` / ``def _dedupe_preserve_order`` /
    ``def _read_packet_directory``;
  - in ``.agents/hooks/`` only: ``def repo_root`` / ``def _git(`` /
    ``def _git_lines`` / ``def porcelain_paths``.

  Scope: added lines in ``forseti-harness/**/*.py`` (excluding
  ``forseti-harness/tests/**`` and ``harness_utils.py`` itself) and
  ``.agents/hooks/*.py`` (excluding ``_hooklib.py`` and
  ``guard_protected_actions.py`` -- the guard's duplication is a documented
  deliberate exception; see the ``_hooklib.py`` docstring).

  ESCAPE HATCH (deliberate divergence is legitimate): the flag is suppressed
  when the def line, the line immediately above, or the first body line below
  carries a comment naming the delta vs the shared home (any comment containing
  ``harness_utils``, ``_hooklib``, ``projection_shared``, or ``helper-delta``).
  The body-line form is
  the placement the 2026-07-16 adoption sweeps actually used, so re-added
  compliant defs (signature edits, file copies) stay suppressed.

Rule authority:
  The shared-helper adoption-rule paragraphs in ``.agents/hooks/README.md``
  ("Shared helpers" / Adoption rule) and ``forseti-harness/README.md``
  ("Shared Helpers"). This checker references that rule; it never restates or
  owns it.

Placement boundary:
  Shape only. A finding never claims the shared helper is wrong or that the
  private copy misbehaves; a green run is never validation, readiness, or
  proof that imports are correct or that a kept divergence is justified.

MODES
  check_shared_helper_duplication.py --hook               PostToolUse advisory (exit 0)
  check_shared_helper_duplication.py --strict [--base R]  CI gate: exit 1 on findings
  check_shared_helper_duplication.py --selftest           synthetic-fixture self-check
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import NamedTuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _hooklib  # noqa: E402  (sys.path pin must precede the import)
from _hooklib import repo_root, to_relposix  # noqa: E402

HARNESS_HOME = "forseti-harness/harness_utils.py"
HOOKLIB_HOME = ".agents/hooks/_hooklib.py"
PROJECTION_HOME = "forseti-harness/source_capture/projection_shared.py"
DELTA_TOKENS = ("harness_utils", "_hooklib", "projection_shared", "helper-delta")

_GENERAL_HELPER_RE = re.compile(
    r"^\s*def\s+(?P<name>_utc_now_z|_utc_now_iso|_utc_now|_now_utc"
    r"|_sha256\w*|_as_dict|_hash_file"
    r"|_string_or_none|_non_empty_string_or_none|_int_or_none|_bool_or_none)\s*\("
)
_PROJECTION_HELPER_RE = re.compile(
    r"^\s*def\s+(?P<name>_is_forbidden_field_name|_first_match"
    r"|_dedupe_preserve_order|_read_packet_directory)\s*\("
)
_HOOKS_ONLY_HELPER_RE = re.compile(
    r"^\s*def\s+(?P<name>repo_root|_git_lines|_git|porcelain_paths)\s*\("
)
_HUNK_RE = re.compile(r"^@@ -\d+(?:,\d+)? \+(?P<start>\d+)(?:,\d+)? @@")


class Finding(NamedTuple):
    path: str
    lineno: int
    name: str
    home: str


def scope_of(rel: str) -> str | None:
    """"harness" | "hooks" | None for a repo-relative posix path."""
    if not rel.endswith(".py"):
        return None
    if rel.startswith("forseti-harness/"):
        if rel.startswith("forseti-harness/tests/"):
            return None
        if rel == "forseti-harness/harness_utils.py":
            return None
        return "harness"
    if rel.startswith(".agents/hooks/") and "/" not in rel[len(".agents/hooks/"):]:
        if rel.rsplit("/", 1)[1] in ("_hooklib.py", "guard_protected_actions.py"):
            return None
        return "hooks"
    return None


def helper_match(line: str, scope: str) -> tuple[str, str] | None:
    """(helper name, owning home) when `line` re-defines a shared helper."""
    match = _GENERAL_HELPER_RE.match(line)
    if match:
        home = HARNESS_HOME if scope == "harness" else HOOKLIB_HOME
        return match.group("name"), home
    if scope == "harness":
        match = _PROJECTION_HELPER_RE.match(line)
        if match:
            return match.group("name"), PROJECTION_HOME
    if scope == "hooks":
        match = _HOOKS_ONLY_HELPER_RE.match(line)
        if match:
            return match.group("name"), HOOKLIB_HOME
    return None


def comment_names_delta(line: str) -> bool:
    if "#" not in line:
        return False
    comment = line.split("#", 1)[1]
    return any(token in comment for token in DELTA_TOKENS)


def added_lines_by_file(diff_text: str) -> dict[str, list[tuple[int, str]]]:
    """{new-side path: [(new-file lineno, added line text)]} from a unified diff.

    Removed lines never advance the new-side counter (a pure deletion of a
    helper is not an addition); '+++ /dev/null' (deleted file) is skipped."""
    out: dict[str, list[tuple[int, str]]] = {}
    current: str | None = None
    new_ln = 0
    for line in diff_text.splitlines():
        if line.startswith("+++ "):
            target = line[4:].strip()
            current = None if target == "/dev/null" else target.removeprefix("b/")
            continue
        if line.startswith("@@"):
            match = _HUNK_RE.match(line)
            new_ln = int(match.group("start")) if match else 0
            continue
        if current is None:
            continue
        if line.startswith("+") and not line.startswith("+++"):
            out.setdefault(current, []).append((new_ln, line[1:]))
            new_ln += 1
        elif line.startswith(("-", "\\")):
            continue  # removed line / no-newline marker: new side unmoved
        else:
            new_ln += 1  # context line
    return out


def analyze_added(
    rel: str,
    scope: str,
    added: list[tuple[int, str]],
    file_lines: list[str] | None,
) -> list[Finding]:
    findings: list[Finding] = []
    for lineno, text in added:
        matched = helper_match(text, scope)
        if matched is None:
            continue
        name, home = matched
        above = below = ""
        if file_lines and 2 <= lineno <= len(file_lines):
            above = file_lines[lineno - 2]
        if file_lines and 1 <= lineno < len(file_lines):
            below = file_lines[lineno]  # first body line: the sweeps' practiced placement
        if comment_names_delta(text) or comment_names_delta(above) or comment_names_delta(below):
            continue
        findings.append(Finding(rel, lineno, name, home))
    return findings


def resolve_base_ref(cli_base: str | None) -> str:
    ci_base = os.environ.get("FORSETI_DIFF_BASE", "").strip()
    if ci_base:
        return ci_base
    gh_base = os.environ.get("GITHUB_BASE_REF", "").strip()
    if gh_base:
        return f"origin/{gh_base}"
    return cli_base or "origin/main"


def _file_lines(root: Path, rel: str, *, head: bool) -> list[str] | None:
    """New-side content: HEAD blob for --strict, working tree for --hook."""
    if head:
        rc, out = _hooklib.git_out(root, ["show", f"HEAD:{rel}"], timeout=20)
        if rc == 0:
            return out.splitlines()
    try:
        return (root / rel).read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return None


def findings_for_diff(root: Path, diff_text: str, *, head: bool) -> list[Finding]:
    findings: list[Finding] = []
    for path, added in sorted(added_lines_by_file(diff_text).items()):
        rel = to_relposix(path, root)
        if rel is None:
            continue
        scope = scope_of(rel)
        if scope is None:
            continue
        findings.extend(analyze_added(rel, scope, added, _file_lines(root, rel, head=head)))
    return findings


def format_findings(findings: list[Finding]) -> str:
    lines = []
    for finding in findings:
        lines.append(
            f"  [SHARED_HELPER_DUPLICATION] {finding.path}:{finding.lineno}: added "
            f"private re-definition of `{finding.name}`; the shared home is "
            f"`{finding.home}` -- import the shared helper (or add it there), or "
            "keep a deliberately divergent copy with a one-line comment naming "
            "the delta (e.g. `# helper-delta: ...`)."
        )
    return "\n".join(lines)


def run_strict(root: Path, cli_base: str | None) -> int:
    base = resolve_base_ref(cli_base)
    rc, out = _hooklib.git_out(
        root, ["diff", "--unified=0", f"{base}...HEAD"], timeout=60
    )
    if rc != 0:
        rc, out = _hooklib.git_out(root, ["diff", "--unified=0", base, "HEAD"], timeout=60)
    if rc != 0:
        print(
            "check_shared_helper_duplication --strict: WARNING: diff scope "
            f"unavailable for base {base!r}; fail-open",
            file=sys.stderr,
        )
        return 0
    findings = findings_for_diff(root, out, head=True)
    if findings:
        print(
            f"check_shared_helper_duplication --strict: {len(findings)} finding(s) "
            f"(base: {base}):"
        )
        print(format_findings(findings))
        print(
            "  Rule owner: the adoption-rule paragraphs in .agents/hooks/README.md "
            "and forseti-harness/README.md. Shape only; never helper correctness, "
            "validation, or readiness."
        )
        return 1
    print(f"check_shared_helper_duplication --strict: OK (base: {base})")
    return 0


def _added_for_live_file(root: Path, rel: str) -> list[tuple[int, str]]:
    if _hooklib.git_lines(root, ["ls-files", "--", rel], timeout=20):
        rc, out = _hooklib.git_out(
            root, ["diff", "--unified=0", "HEAD", "--", rel], timeout=20
        )
        if rc != 0:
            return []  # advisory: fail open
        return added_lines_by_file(out).get(rel, [])
    lines = _file_lines(root, rel, head=False)  # untracked: every line is added
    return [(index + 1, line) for index, line in enumerate(lines or [])]


def run_hook(root: Path) -> int:
    findings: list[Finding] = []
    for path in _hooklib.candidate_paths(_hooklib.read_event()):
        rel = to_relposix(path, root)
        if rel is None:
            continue
        scope = scope_of(rel)
        if scope is None:
            continue
        added = _added_for_live_file(root, rel)
        findings.extend(analyze_added(rel, scope, added, _file_lines(root, rel, head=False)))
    if findings:
        msg = (
            "Shared-helper duplication guard (advisory):\n"
            + format_findings(findings)
            + "\nRule owner: the adoption-rule paragraphs in .agents/hooks/README.md"
            " and forseti-harness/README.md. Shape only; not validation,"
            " readiness, or proof the divergence is unjustified."
        )
        print(
            json.dumps(
                {
                    "hookSpecificOutput": {
                        "hookEventName": "PostToolUse",
                        "additionalContext": msg,
                    }
                }
            )
        )
    return 0


def selftest() -> int:
    ok = True

    def check(label: str, got, expected) -> None:
        nonlocal ok
        passed = got == expected
        if not passed:
            ok = False
        print(f"{'PASS' if passed else 'FAIL'}  {label}  expect={expected!r} got={got!r}")

    def diff(path: str, added: list[str], removed: list[str] | None = None) -> str:
        body = [f"--- a/{path}", f"+++ b/{path}", "@@ -1,0 +1,%d @@" % len(added)]
        body += ["+" + line for line in added]
        body += ["-" + line for line in (removed or [])]
        return "\n".join(body) + "\n"

    def run(path: str, added: list[str], file_lines: list[str] | None = None) -> list[Finding]:
        records = added_lines_by_file(diff(path, added)).get(path, [])
        scope = scope_of(path)
        if scope is None:
            return []
        return analyze_added(path, scope, records, file_lines)

    # 1. flagged add in harness scope -> finding names harness_utils home.
    got = run("forseti-harness/runners/x.py", ["def _utc_now():", "    pass"])
    check("case1 flagged add count", len(got), 1)
    check("case1 helper name", got[0].name if got else None, "_utc_now")
    check("case1 owning home", got[0].home if got else None, HARNESS_HOME)
    check("case1 lineno", got[0].lineno if got else None, 1)

    # 2. suppressed by delta comment on the def line and on the line above.
    check("case2 same-line delta comment suppresses",
          run("forseti-harness/runners/x.py",
              ["def _utc_now():  # helper-delta: naive datetime, no Z suffix"]), [])
    above = ["# helper-delta: sha over normalized text, unlike harness_utils",
             "def _sha256_text(x):"]
    check("case2 line-above delta comment suppresses",
          run("forseti-harness/runners/x.py", above, file_lines=above), [])
    check("case2 line-above harness_utils comment suppresses",
          run("forseti-harness/runners/x.py",
              ["# differs from harness_utils.hash_file: streams in chunks",
               "def _hash_file(p):"],
              file_lines=["# differs from harness_utils.hash_file: streams in chunks",
                          "def _hash_file(p):"]), [])
    # A non-comment mention does not suppress.
    got = run("forseti-harness/runners/x.py", ["def _as_dict(harness_utils):"])
    check("case2 non-comment token does not suppress", len(got), 1)
    # First-body-line comment suppresses (the sweeps' practiced placement):
    # a re-added compliant def (signature edit / file copy) must stay green.
    body_form = ["def _utc_now_z() -> str:",
                 "    # Diverges from harness_utils.utc_now_z: naive utcnow(), keeps microseconds."]
    check("case2 first-body-line delta comment suppresses",
          run("forseti-harness/source_capture/x.py", body_form[:1], file_lines=body_form), [])

    # 2b. coercion-helper names (2026-07-16 sweep): flagged add + delta suppression.
    for helper_name in (
        "_string_or_none",
        "_non_empty_string_or_none",
        "_int_or_none",
        "_bool_or_none",
    ):
        got = run(
            "forseti-harness/source_capture/x.py",
            [f"def {helper_name}(value):", "    pass"],
        )
        check(
            f"case2b {helper_name} flagged",
            [f.name for f in got],
            [helper_name],
        )
        check(
            f"case2b {helper_name} owning home",
            got[0].home if got else None,
            HARNESS_HOME,
        )
    coercion_body = ["def _string_or_none(value):",
                     "    # helper-delta: does not strip, unlike harness_utils.string_or_none"]
    check("case2b coercion first-body-line delta comment suppresses",
          run("forseti-harness/source_capture/x.py", coercion_body[:1],
              file_lines=coercion_body), [])

    # 2c. projection-surface helper names (2026-07-16 sweep): flagged add toward
    # the projection_shared home + delta suppression; harness scope only.
    for helper_name in (
        "_is_forbidden_field_name",
        "_first_match",
        "_dedupe_preserve_order",
        "_read_packet_directory",
    ):
        got = run(
            "forseti-harness/source_capture/x.py",
            [f"def {helper_name}(value):", "    pass"],
        )
        check(
            f"case2c {helper_name} flagged",
            [f.name for f in got],
            [helper_name],
        )
        check(
            f"case2c {helper_name} owning home",
            got[0].home if got else None,
            PROJECTION_HOME,
        )
    projection_body = [
        "def _read_packet_directory(path):",
        "    # helper-delta: returns a (packet, bytes, packet_dir) 3-tuple, unlike projection_shared",
    ]
    check("case2c projection first-body-line delta comment suppresses",
          run("forseti-harness/source_capture/x.py", projection_body[:1],
              file_lines=projection_body), [])
    check("case2c projection name not flagged in hooks scope",
          run(".agents/hooks/check_example.py", ["def _first_match(t):"]), [])
    check("case2c longer-name def not prefix-flagged",
          run("forseti-harness/source_capture/x.py",
              ["def _first_matching_class(tokens):"]), [])

    # 3. excluded paths -> no findings.
    check("case3 harness tests excluded",
          run("forseti-harness/tests/unit/test_x.py", ["def _utc_now():"]), [])
    check("case3 harness_utils itself excluded",
          run("forseti-harness/harness_utils.py", ["def _utc_now():"]), [])
    check("case3 _hooklib excluded",
          run(".agents/hooks/_hooklib.py", ["def repo_root():"]), [])
    check("case3 non-python excluded",
          run("forseti-harness/notes.md", ["def _utc_now():"]), [])
    check("case3 out-of-scope root excluded",
          run("docs/tools/x.py", ["def _utc_now():"]), [])

    # 4. guard exclusion (documented deliberate duplication).
    check("case4 guard exclusion",
          run(".agents/hooks/guard_protected_actions.py",
              ["def repo_root():", "def _git(args):"]), [])
    got = run(".agents/hooks/check_example.py", ["def _git(args):"])
    check("case4 hooks-scope _git flagged elsewhere", len(got), 1)
    check("case4 hooks owning home", got[0].home if got else None, HOOKLIB_HOME)
    check("case4 hooks-only name outside hooks not flagged",
          run("forseti-harness/runners/x.py", ["def porcelain_paths(s):"]), [])

    # 5. removed-line ignored.
    removed_only = diff("forseti-harness/runners/x.py", ["x = 1"], ["def _utc_now():"])
    records = added_lines_by_file(removed_only).get("forseti-harness/runners/x.py", [])
    check("case5 removed line ignored",
          analyze_added("forseti-harness/runners/x.py", "harness", records, None), [])

    # 6. name/pattern edges.
    check("case6 sha256 suffix matched",
          [f.name for f in run("forseti-harness/runners/x.py", ["def _sha256_file(p):"])],
          ["_sha256_file"])
    check("case6 longest utc name wins",
          [f.name for f in run("forseti-harness/runners/x.py", ["def _utc_now_z():"])],
          ["_utc_now_z"])
    check("case6 unlisted helper not flagged",
          run("forseti-harness/runners/x.py", ["def _utc_offset():"]), [])
    check("case6 indented (method) def flagged",
          [f.lineno for f in run("forseti-harness/runners/x.py",
                                 ["class C:", "    def _as_dict(self):"])],
          [2])

    # 7. hunk lineno mapping across context and removals.
    mapped = added_lines_by_file(
        "--- a/f.py\n+++ b/f.py\n@@ -10,3 +20,3 @@\n ctx\n-old\n+new\n ctx2\n"
    )
    check("case7 lineno mapping", mapped.get("f.py"), [(21, "new")])
    check("case7 deleted file skipped",
          added_lines_by_file("--- a/f.py\n+++ /dev/null\n@@ -1,2 +0,0 @@\n-def _utc_now():\n-    pass\n"),
          {})

    # 8. resolve_base_ref precedence: env wins, then --base, then default.
    saved_ci = os.environ.pop("FORSETI_DIFF_BASE", None)
    saved_gh = os.environ.pop("GITHUB_BASE_REF", None)
    try:
        check("case8 default base", resolve_base_ref(None), "origin/main")
        check("case8 cli base", resolve_base_ref("main"), "main")
        os.environ["GITHUB_BASE_REF"] = "develop"
        check("case8 branch base wins over cli", resolve_base_ref("main"), "origin/develop")
        os.environ["FORSETI_DIFF_BASE"] = "a" * 40
        check("case8 event base wins", resolve_base_ref("main"), "a" * 40)
    finally:
        for key, saved in (("FORSETI_DIFF_BASE", saved_ci), ("GITHUB_BASE_REF", saved_gh)):
            if saved is not None:
                os.environ[key] = saved
            else:
                os.environ.pop(key, None)

    print("SELFTEST", "OK" if ok else "FAILED")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    # Forced-exception probe: proves the __main__ gating handler
    # (forseti-harness/tests/unit/test_hook_internal_error_gating.py).
    if "--force-internal-error" in argv:
        raise RuntimeError("forced internal error (probe)")
    if "--selftest" in argv:
        return selftest()
    root = repo_root()
    if "--hook" in argv:
        return run_hook(root)
    if "--strict" in argv:
        cli_base: str | None = None
        if "--base" in argv:
            index = argv.index("--base")
            if index + 1 < len(argv):
                cli_base = argv[index + 1]
        return run_strict(root, cli_base)
    print(
        "Usage: check_shared_helper_duplication.py --hook | --strict [--base REF] | --selftest"
    )
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as exc:
        # GATE FAIL bucket in gating modes (validation-gates.md): an internal
        # checker bug must not read as a green gate. Advisory --hook fails open
        # so a bug never bricks the agent.
        sys.stderr.write(f"check_shared_helper_duplication: internal error: {exc}\n")
        gating = "--strict" in sys.argv[1:] or "--selftest" in sys.argv[1:]
        sys.exit(1 if gating else 0)
