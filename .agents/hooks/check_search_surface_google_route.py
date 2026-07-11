#!/usr/bin/env python3
"""Google search-surface route guard.

WHAT THIS DOES
  Enforces the mechanically-checkable shell of Forseti's current Google
  search-surface route:

  - Google Search URLs preserved in durable Forseti docs must carry
    hl=en, gl=us, and pws=0 when they are used as capture URLs.
  - A durable artifact that uses a US-parameterized Google search route must
    carry the physical-locality non-claim.
  - Google "unusual traffic" / sorry pages that expose an IP address must not be
    preserved in durable docs.

WHY
  The route decision is owned by
  docs/decisions/search_surface_google_parameterized_us_capture_route_v0.md.
  This checker enforces shape only. It cannot prove what Google showed, whether
  a source is adequate, whether a market claim is valid, or whether an exit was
  physically US-local.

MODES
  check_search_surface_google_route.py --hook
  check_search_surface_google_route.py --check [PATH ...]
  check_search_surface_google_route.py --changed [--strict]
  check_search_surface_google_route.py --strict [--base REF]
  check_search_surface_google_route.py --selftest
"""
from __future__ import annotations

import html
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _hooklib  # noqa: E402  (sys.path pin must precede the import)
from _hooklib import repo_root, to_relposix  # noqa: E402


# Deliberately NOT _hooklib.DURABLE_DOC_PREFIXES: this checker's scope follows
# where Google capture URLs legitimately land -- it adds docs/research/ and
# forseti/product/ (capture/evidence surfaces) and omits doc-role folders that
# never carry capture URLs (docs/product/, docs/migration/, docs/hygiene/, the
# overlay). Keep the delta explicit here instead of silently drifting the base.
IN_SCOPE_PREFIXES = (
    "docs/decisions/",
    "docs/prompts/",
    "docs/research/",
    "docs/review-inputs/",
    "docs/review-outputs/",
    "docs/workflows/",
    "forseti/product/",
)
EXCLUDED_PARTS = ("/_inbox/", "/_scratch/", "/snapshots/")
REQUIRED_SEARCH_PARAMS = {"hl": "en", "gl": "us", "pws": "0"}

_GOOGLE_SEARCH_URL_RE = re.compile(
    r"https?://(?:www\.)?google\.com/search[^\s<>)\"'`\]\*|]*",
    re.IGNORECASE,
)
_US_PARAMETERIZED_RE = re.compile(
    r"\b(?:US[- ]parameteri[sz]ed|U\.S\.[- ]parameteri[sz]ed|gl=us)\b",
    re.IGNORECASE,
)
_GOOGLE_SURFACE_RE = re.compile(
    r"\b(?:Google Search|Google SERP|Google search-surface|search-surface|SERP)\b",
    re.IGNORECASE,
)
_PHYSICAL_LOCALITY_NONCLAIM_RE = re.compile(
    r"(?:not\s+physically\s+US(?:[- ](?:local|located))?|"
    r"not\s+physical(?:ly)?\s+US\s+locality|"
    r"physical\s+locality\s+(?:is\s+)?not\s+asserted|"
    r"physically\s+US(?:[- ](?:local|located))?\s+is\s+not\s+asserted|"
    r"not\s+physically\s+located\s+in\s+the\s+US)",
    re.IGNORECASE,
)
_GOOGLE_BLOCK_CONTEXT_RE = re.compile(
    r"(?:our\s+systems\s+have\s+detected\s+unusual\s+traffic|"
    r"https?://(?:www\.)?google\.com/sorry(?:/|\b)|"
    r"\bgoogle\.com/sorry(?:/|\b))",
    re.IGNORECASE,
)
_IP_LITERAL_PATTERN = (
    r"(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}"
    r"(?:25[0-5]|2[0-4]\d|1?\d?\d)|"
    r"(?:[0-9a-f]{1,4}:){2,}[0-9a-f]{1,4}"
)
_IP_WITH_LABEL_RE = re.compile(
    r"\b(?:your\s+)?ip\s+address(?:\s+is|:)?\s+(?:" + _IP_LITERAL_PATTERN + r")\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class Finding:
    path: str
    code: str
    detail: str


def _to_posix(path: str) -> str:
    # Strip only a LITERAL leading "./" prefix. NOT lstrip("./"), which is a
    # character-set strip that would also eat the leading dot of ".agents/..."
    # paths (silently dropping overlay files out of scope).
    s = path.replace("\\", "/")
    return s[2:] if s.startswith("./") else s


# to_relposix comes from _hooklib: it handles the ABSOLUTE file_path Claude Code
# passes in the PostToolUse payload (without which the --hook advisory silently
# no-opped on every edit) and returns None for rooted-but-not-absolute paths
# ("/docs/..." on Windows -- the FIND-01 class), which analyze_paths drops.


def in_scope(relpath: str) -> bool:
    rel = _to_posix(relpath)
    if not rel.endswith(".md"):
        return False
    wrapped = f"/{rel}"
    if any(part in wrapped for part in EXCLUDED_PARTS):
        return False
    return any(rel.startswith(prefix) for prefix in IN_SCOPE_PREFIXES)


def google_search_urls(text: str) -> list[str]:
    urls: list[str] = []
    for match in _GOOGLE_SEARCH_URL_RE.finditer(text):
        raw = html.unescape(match.group(0)).rstrip(".,;`)]*|")
        urls.append(raw)
    return urls


def missing_required_params(url: str) -> list[str]:
    parsed = urlparse(url)
    params = parse_qs(parsed.query, keep_blank_values=True)
    missing: list[str] = []
    for key, expected in REQUIRED_SEARCH_PARAMS.items():
        values = [value.lower() for value in params.get(key, [])]
        if expected not in values:
            missing.append(f"{key}={expected}")
    return missing


def has_us_parameterized_google_surface(text: str, urls: list[str]) -> bool:
    for url in urls:
        parsed = urlparse(url)
        params = parse_qs(parsed.query, keep_blank_values=True)
        if "us" in [value.lower() for value in params.get("gl", [])]:
            return True
    return bool(_US_PARAMETERIZED_RE.search(text) and _GOOGLE_SURFACE_RE.search(text))


def has_physical_locality_nonclaim(text: str) -> bool:
    return bool(_PHYSICAL_LOCALITY_NONCLAIM_RE.search(text))


def has_google_sorry_ip_leak(text: str) -> bool:
    for match in _GOOGLE_BLOCK_CONTEXT_RE.finditer(text):
        start = max(match.start() - 500, 0)
        end = min(match.end() + 500, len(text))
        if _IP_WITH_LABEL_RE.search(text[start:end]):
            return True
    return False


def analyze_text(path: str, text: str) -> list[Finding]:
    findings: list[Finding] = []
    urls = google_search_urls(text)
    for url in urls:
        missing = missing_required_params(url)
        if missing:
            findings.append(
                Finding(
                    path=path,
                    code="GOOGLE_SEARCH_ROUTE_PARAMS",
                    detail=(
                        "Google Search capture URL is missing required "
                        "US-parameterized route param(s): "
                        + ", ".join(missing)
                    ),
                )
            )

    if has_us_parameterized_google_surface(text, urls) and not has_physical_locality_nonclaim(text):
        findings.append(
            Finding(
                path=path,
                code="GOOGLE_SEARCH_PHYSICAL_LOCALITY_NONCLAIM",
                detail=(
                    "US-parameterized Google search-surface artifact must state "
                    "the non-claim: parameterized US is not physically US-local."
                ),
            )
        )

    if has_google_sorry_ip_leak(text):
        findings.append(
            Finding(
                path=path,
                code="GOOGLE_SORRY_IP_LEAK",
                detail=(
                    "Google unusual-traffic/sorry page with exposed IP address "
                    "must not be preserved in durable docs."
                ),
            )
        )

    return findings


def analyze_file(root: Path, relpath: str) -> list[Finding]:
    rel = _to_posix(relpath)
    if not in_scope(rel):
        return []
    path = root / rel
    if not path.is_file():
        return []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return [Finding(path=rel, code="READ_ERROR", detail=str(exc))]
    return analyze_text(rel, text)


def _git(root: Path, *args: str, timeout: int = 15) -> tuple[int, str]:
    """Thin varargs adapter over the shared git wrapper (keeps call sites flat).
    _hooklib.git_out returns (1, "") on launch failure/timeout; callers here only
    test rc != 0, so the -1/1 distinction does not matter."""
    return _hooklib.git_out(root, list(args), timeout=timeout)


def changed_paths(root: Path) -> list[str] | None:
    rc, out = _git(root, "diff", "--name-only", "--diff-filter=ACMRT", "HEAD")
    if rc != 0:
        return None
    paths = [line.strip() for line in out.splitlines() if line.strip()]
    rc_u, out_u = _git(root, "ls-files", "--others", "--exclude-standard")
    if rc_u == 0:
        paths.extend(line.strip() for line in out_u.splitlines() if line.strip())
    return sorted(set(paths))


def changed_paths_vs_base(root: Path, base_ref: str) -> list[str] | None:
    rc, out = _git(root, "diff", "--name-only", f"{base_ref}...HEAD")
    if rc != 0:
        rc2, out2 = _git(root, "diff", "--name-only", base_ref, "HEAD")
        if rc2 != 0:
            return None
        out = out2
    return sorted(set(line.strip() for line in out.splitlines() if line.strip()))


def resolve_base(cli_base: str | None) -> str:
    ci_base = os.environ.get("FORSETI_DIFF_BASE", "").strip()
    if ci_base:
        return ci_base
    gh_base = os.environ.get("GITHUB_BASE_REF", "").strip()
    if gh_base:
        return f"origin/{gh_base}"
    return cli_base or "origin/main"


def analyze_paths(root: Path, paths: list[str]) -> list[Finding]:
    findings: list[Finding] = []
    relpaths = {rel for path in paths if (rel := to_relposix(path, root)) is not None}
    for relpath in sorted(relpaths):
        findings.extend(analyze_file(root, relpath))
    return findings


def print_findings(findings: list[Finding], *, strict: bool) -> int:
    mode = "--strict" if strict else "--check"
    if not findings:
        print(f"check_search_surface_google_route {mode}: OK (0 findings)")
        return 0
    print(f"check_search_surface_google_route {mode}: {len(findings)} finding(s)")
    for finding in findings:
        print(f"  [{finding.code}] {finding.path} :: {finding.detail}")
    return 1 if strict else 0


def run_hook(root: Path) -> int:
    # Event parsing is shared: _hooklib.candidate_paths covers file_path/path/
    # notebook_path plus Codex apply_patch headers in command/patch/input.
    paths = _hooklib.candidate_paths(_hooklib.read_event())
    findings = analyze_paths(root, paths)
    if findings:
        msg = (
            "Google search-surface route guard (advisory):\n"
            + "\n".join(f"  [{f.code}] {f.path}: {f.detail}" for f in findings)
            + "\nRule owner: docs/decisions/"
            "search_surface_google_parameterized_us_capture_route_v0.md. "
            "Shape check only; not validation, readiness, demand proof, or "
            "physical-locality proof."
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


def run_check(root: Path, paths: list[str], *, strict: bool) -> int:
    findings = analyze_paths(root, paths)
    return print_findings(findings, strict=strict)


def run_changed(root: Path, *, strict: bool) -> int:
    paths = changed_paths(root)
    if paths is None:
        print(
            "check_search_surface_google_route --changed: WARNING: git changed-file "
            "scope unavailable; failing open",
            file=sys.stderr,
        )
        return 0
    findings = analyze_paths(root, paths)
    return print_findings(findings, strict=strict)


def run_strict(root: Path, cli_base: str | None) -> int:
    base = resolve_base(cli_base)
    paths = changed_paths_vs_base(root, base)
    if paths is None:
        print(
            "check_search_surface_google_route --strict: WARNING: diff scope "
            f"unavailable for base {base!r}; failing open",
            file=sys.stderr,
        )
        return 0
    findings = analyze_paths(root, paths)
    return print_findings(findings, strict=True)


def selftest() -> int:
    ok = True

    def check(label: str, got, expected) -> None:
        nonlocal ok
        passed = got == expected
        if not passed:
            ok = False
        print(f"{'PASS' if passed else 'FAIL'}  {label}  expect={expected!r} got={got!r}")

    _root = repo_root()
    check("absolute payload path -> repo-relative (was the --hook no-op bug)",
          to_relposix(str(_root / "docs" / "decisions" / "x.md"), _root),
          "docs/decisions/x.md")
    check("to_posix keeps a leading dot (no lstrip corruption)",
          _to_posix(".agents/workflow-overlay/x.md"),
          ".agents/workflow-overlay/x.md")
    check("outside-repo absolute path -> None",
          to_relposix(str(_root.parent / "definitely_outside_x.md"), _root),
          None)

    good = (
        "Google Search capture URL: "
        "https://www.google.com/search?q=niche+perfume&hl=en&gl=us&pws=0\n"
        "This is US-parameterized, not physically US-local."
    )
    bad_params = "https://www.google.com/search?q=niche+perfume&gl=us"
    bad_nonclaim = (
        "Google SERP capture: "
        "https://www.google.com/search?q=niche+perfume&hl=en&gl=us&pws=0"
    )
    sorry = (
        "Google sorry page. Our systems have detected unusual traffic.\n"
        "IP address: 100.38.68.100\n"
        "URL: https://www.google.com/search?q=niche+perfume&hl=en&gl=us&pws=0\n"
        "This is US-parameterized, not physically US-local."
    )
    sorry_path = (
        "Google block page. Our systems have detected unusual traffic.\n"
        "Your IP address is 100.38.68.100\n"
        "URL: https://www.google.com/sorry/index?continue=/search\n"
        "This is US-parameterized, not physically US-local."
    )
    inline_code = (
        "Google Search capture URL: "
        "`https://www.google.com/search?q=niche+perfume&hl=en&gl=us&pws=0`\n"
        "This is US-parameterized, not physically US-local."
    )
    uppercase_gl = (
        "Google Search capture URL: "
        "https://www.google.com/search?q=niche+perfume&hl=en&gl=US&pws=0\n"
        "This is US-parameterized, not physically US-local."
    )
    ip_without_block = (
        "Network note: 100.38.68.100.\n"
        "This is US-parameterized, not physically US-local."
    )

    check("good has no findings", [f.code for f in analyze_text("x.md", good)], [])
    check(
        "missing params",
        [f.code for f in analyze_text("x.md", bad_params)],
        ["GOOGLE_SEARCH_ROUTE_PARAMS", "GOOGLE_SEARCH_PHYSICAL_LOCALITY_NONCLAIM"],
    )
    check(
        "missing nonclaim",
        [f.code for f in analyze_text("x.md", bad_nonclaim)],
        ["GOOGLE_SEARCH_PHYSICAL_LOCALITY_NONCLAIM"],
    )
    check(
        "sorry page IP leak",
        [f.code for f in analyze_text("x.md", sorry)],
        ["GOOGLE_SORRY_IP_LEAK"],
    )
    check(
        "sorry path IP leak",
        [f.code for f in analyze_text("x.md", sorry_path)],
        ["GOOGLE_SORRY_IP_LEAK"],
    )
    check("inline code URL has no findings", [f.code for f in analyze_text("x.md", inline_code)], [])
    check("uppercase gl accepted", [f.code for f in analyze_text("x.md", uppercase_gl)], [])
    check("IP without block context has no findings", [f.code for f in analyze_text("x.md", ip_without_block)], [])
    check(
        "html escaped url",
        missing_required_params(
            google_search_urls(
                "https://www.google.com/search?q=a&amp;hl=en&amp;gl=us&amp;pws=0"
            )[0]
        ),
        [],
    )
    check("scope docs decisions", in_scope("docs/decisions/x.md"), True)
    check("scope excludes inbox", in_scope("docs/_inbox/x.md"), False)
    check("scope excludes code", in_scope(".agents/hooks/x.md"), False)
    root = repo_root()
    rel_win = to_relposix("C:/elsewhere/docs/decisions/x.md", root)
    check(
        "windows-drive path outside the repo never lands in scope",
        rel_win is None or not in_scope(rel_win),
        True,
    )
    rel_rooted = to_relposix("/docs/decisions/x.md", root)
    check(
        "posix-rooted path outside the repo never lands in scope",
        rel_rooted is None or not in_scope(rel_rooted),
        True,
    )
    rel_unc = to_relposix("//server/share/docs/decisions/x.md", root)
    check(
        "unc path outside the repo never lands in scope",
        rel_unc is None or not in_scope(rel_unc),
        True,
    )
    check(
        "production path: analyze_paths on rooted out-of-repo path yields nothing",
        analyze_paths(root, ["/docs/decisions/x.md"]),
        [],
    )
    if os.name == "nt":
        check(
            "production path: backslash windows payload under root is in scope",
            in_scope(to_relposix(str(root) + "\\docs\\decisions\\x.md", root) or ""),
            True,
        )

    print("SELFTEST", "OK" if ok else "FAILED")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    # Forced-exception probe: proves the __main__ gating handler
    # (forseti-harness/tests/unit/test_hook_internal_error_gating.py).
    if "--force-internal-error" in argv:
        raise RuntimeError("forced internal error (probe)")
    try:
        root = repo_root()
    except Exception as exc:
        sys.stderr.write(f"check_search_surface_google_route: no repo root: {exc}\n")
        return 0

    if "--selftest" in argv:
        return selftest()
    if "--hook" in argv:
        return run_hook(root)
    strict = "--strict" in argv
    if "--changed" in argv:
        return run_changed(root, strict=strict)
    if "--check" in argv:
        paths = [arg for arg in argv if not arg.startswith("--")]
        if not paths:
            print("check_search_surface_google_route --check: no paths supplied")
            return 0
        return run_check(root, paths, strict=strict)
    if strict:
        cli_base: str | None = None
        if "--base" in argv:
            idx = argv.index("--base")
            if idx + 1 < len(argv):
                cli_base = argv[idx + 1]
        return run_strict(root, cli_base)

    print(
        "Usage: check_search_surface_google_route.py --hook | --check [PATH ...] "
        "| --changed [--strict] | --strict [--base REF] | --selftest"
    )
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as exc:
        # GATE FAIL bucket in gating modes (validation-gates.md; EP-35
        # delegated review FIND-02 class sweep): an internal checker bug must
        # not read as a green gate. Advisory/--hook modes fail open so a bug
        # never bricks the agent.
        sys.stderr.write(f"check_search_surface_google_route: internal error: {exc}\n")
        gating = "--strict" in sys.argv[1:] or "--selftest" in sys.argv[1:]
        sys.exit(1 if gating else 0)
