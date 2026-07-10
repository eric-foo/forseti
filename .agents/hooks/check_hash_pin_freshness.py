#!/usr/bin/env python3
"""Hash-pin freshness gate (EP-15, narrowed to markdown freshness-pin grammars).

Validates two repo-local markdown freshness-pin grammars against current file
bytes:

  Grammar #1 (labeled adjacent-bullet pair) -- valid in any tracked ``.md``:
  a ``<Label> path: `<path>`` bullet paired, by exact label text within the
  same file, with a ``<Label> sha256: `<hex>`` bullet. Unpaired path-only or
  hash-only labels are not pins. A label with conflicting values across its
  own bullets is not a pin (INFO only).

  Grammar #2 (preserved-files inline bullet) -- valid only in files whose
  posix-relative path contains ``/source_captures/`` and whose basename is
  ``receipt.md``: `` - `file_NN` -> `<path>` (sha256 `<hex>`, <n> bytes)``
  lines, with ``<path>`` resolved relative to the receipt.md's own directory.

NON-OVERLAP with EP-37 (``.agents/hooks/check_source_input_hashes.py``):
EP-37 covers list-style JSON ``source_inputs[]`` records; this checker covers
markdown pin grammars only. The two checkers partition by file extension
(``*.json`` vs ``*.md``) and by grammar; there is zero overlap in scanned
files or in what counts as a pin.

Rule authority:
  The "Hash-pin freshness gate" bullet in
  .agents/workflow-overlay/validation-gates.md (Current Gates).

Placement boundary:
  This is pin-shape/freshness only. A green run never proves semantic
  validity, source quality, skill correctness, validation, or readiness --
  only that a discovered pin's target file exists and its CRLF-normalized
  sha256 matches the pinned value.
"""
from __future__ import annotations

import hashlib
import os
import posixpath
import re
import subprocess
import sys
import tempfile
from pathlib import Path, PureWindowsPath
from typing import NamedTuple


def _configure_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, OSError, ValueError):
            pass


_configure_stdio()

_URL_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*://")

# Grammar #1: labeled adjacent-bullet pair (path bullet + sha256 bullet,
# paired by exact label text within the same file).
_G1_LABEL = r"[A-Z][A-Za-z0-9 _-]{0,40}?"
_G1_PATH_RE = re.compile(
    rf"^\s*-\s*(?P<label>{_G1_LABEL})\s+path:\s*`(?P<path>[^`]+)`",
    re.MULTILINE,
)
_G1_HASH_RE = re.compile(
    rf"^\s*-\s*(?P<label>{_G1_LABEL})\s+sha256:\s*`?(?P<hex>[0-9A-Fa-f]{{64}})`?",
    re.MULTILINE,
)

# Grammar #2: preserved-files inline bullet (source_captures/**/receipt.md only).
_G2_RE = re.compile(
    r"^\s*-\s*`(?P<token>file_\d+)`\s*->\s*`(?P<path>[^`]+)`"
    r"\s*\(sha256\s*`(?P<hex>[0-9a-fA-F]{64})`,\s*\d+\s+bytes\)",
    re.MULTILINE,
)


class Pin(NamedTuple):
    grammar: str  # "grammar1" | "grammar2"
    source_md: str  # repo-root-relative posix path of the .md carrying the pin
    label: str  # grammar1: paired label text; grammar2: the file_NN token
    pointer: str  # raw captured path (as written in the pin)
    resolved_rel: str  # repo-root-relative posix path to the pin target
    expected_hex: str  # lowercase


class Finding(NamedTuple):
    grammar: str
    source_md: str
    label: str
    resolved_rel: str
    problem: str  # "pin_target_missing" | "pin_hash_mismatch"
    expected_hex: str | None = None
    actual_hex: str | None = None


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def normalize_relpath(value: str) -> str:
    normalized = value.replace("\\", "/")
    while normalized.startswith("./"):
        normalized = normalized[2:]
    return normalized


def is_repo_local_pointer(pointer: str) -> bool:
    if not pointer or _URL_RE.search(pointer):
        return False
    if pointer.startswith("#"):
        return False
    if pointer.startswith(("/", "\\")):
        return False
    if Path(pointer).is_absolute():
        return False
    if PureWindowsPath(pointer).drive:
        return False
    if ".." in Path(pointer).parts:
        return False
    return True


def sha256_normalized(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def _normpath(rel: str) -> str:
    return posixpath.normpath(normalize_relpath(rel))


def is_receipt_capture(source_md: str) -> bool:
    parts = normalize_relpath(source_md).split("/")
    return len(parts) >= 2 and parts[-1] == "receipt.md" and "source_captures" in parts[:-1]


def parse_grammar1_pins(text: str, source_md: str) -> tuple[list[Pin], list[str], int]:
    """Parse grammar #1 pins from ``text`` (the contents of ``source_md``).

    Returns (pins, info_messages, skipped_non_local_count).
    """
    paths: dict[str, set[str]] = {}
    hashes: dict[str, set[str]] = {}
    order: list[str] = []
    skipped_non_local = 0

    for match in _G1_PATH_RE.finditer(text):
        label = match.group("label").strip()
        pointer = normalize_relpath(match.group("path").strip())
        if label not in order:
            order.append(label)
        if not is_repo_local_pointer(pointer):
            skipped_non_local += 1
            continue
        paths.setdefault(label, set()).add(pointer)

    for match in _G1_HASH_RE.finditer(text):
        label = match.group("label").strip()
        hex_value = match.group("hex").strip().lower()
        if label not in order:
            order.append(label)
        hashes.setdefault(label, set()).add(hex_value)

    pins: list[Pin] = []
    info: list[str] = []
    for label in order:
        path_values = paths.get(label)
        hash_values = hashes.get(label)
        if not path_values or not hash_values:
            continue  # unpaired label -> not a pin
        if len(path_values) > 1 or len(hash_values) > 1:
            info.append(f"{source_md}: label {label!r} has conflicting path/sha256 values; no pin")
            continue
        pointer = next(iter(path_values))
        hex_value = next(iter(hash_values))
        pins.append(Pin("grammar1", source_md, label, pointer, _normpath(pointer), hex_value))
    return pins, info, skipped_non_local


def parse_grammar2_pins(text: str, source_md: str) -> tuple[list[Pin], int]:
    """Parse grammar #2 pins from ``text`` (the contents of ``source_md``).

    Returns (pins, skipped_non_local_count). Only fires when ``source_md`` is
    a ``.../source_captures/.../receipt.md`` file.
    """
    if not is_receipt_capture(source_md):
        return [], 0
    receipt_dir = posixpath.dirname(normalize_relpath(source_md))
    pins: list[Pin] = []
    skipped_non_local = 0
    for match in _G2_RE.finditer(text):
        pointer = normalize_relpath(match.group("path").strip())
        if not is_repo_local_pointer(pointer):
            skipped_non_local += 1
            continue
        hex_value = match.group("hex").strip().lower()
        resolved_rel = _normpath(posixpath.join(receipt_dir, pointer))
        pins.append(Pin("grammar2", source_md, match.group("token"), pointer, resolved_rel, hex_value))
    return pins, skipped_non_local


def findings_for_pins(root: Path, pins: list[Pin]) -> list[Finding]:
    findings: list[Finding] = []
    for pin in pins:
        target = root / Path(pin.resolved_rel)
        if not target.is_file():
            findings.append(
                Finding(pin.grammar, pin.source_md, pin.label, pin.resolved_rel, "pin_target_missing", pin.expected_hex, None)
            )
            continue
        actual = sha256_normalized(target)
        if actual != pin.expected_hex:
            findings.append(
                Finding(pin.grammar, pin.source_md, pin.label, pin.resolved_rel, "pin_hash_mismatch", pin.expected_hex, actual)
            )
    return findings


def relevant_pins(pins: list[Pin], changed_paths: set[str]) -> list[Pin]:
    return [
        pin
        for pin in pins
        if normalize_relpath(pin.source_md) in changed_paths
        or normalize_relpath(pin.resolved_rel) in changed_paths
    ]


def parse_name_status(lines: list[str]) -> set[str]:
    changed: set[str] = set()
    for line in lines:
        parts = [part.strip() for part in line.split("\t")]
        if len(parts) < 2:
            continue
        status = parts[0]
        if status.startswith(("R", "C")) and len(parts) >= 3:
            changed.add(normalize_relpath(parts[1]))
            changed.add(normalize_relpath(parts[2]))
        else:
            changed.add(normalize_relpath(parts[1]))
    return changed


def _git(root: Path, args: list[str], timeout: int = 20) -> tuple[int, str]:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *args],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return result.returncode, result.stdout
    except (FileNotFoundError, OSError, subprocess.TimeoutExpired):
        return -1, ""


def resolve_base_ref(cli_base: str | None) -> str:
    gh_base = os.environ.get("GITHUB_BASE_REF", "").strip()
    if gh_base:
        return f"origin/{gh_base}"
    if cli_base:
        return cli_base
    return "origin/main"


def changed_paths_for_base(root: Path, base_ref: str) -> set[str] | None:
    if _git(root, ["rev-parse", "--verify", "--quiet", "HEAD"])[0] != 0:
        return None
    if _git(root, ["rev-parse", "--verify", "--quiet", base_ref])[0] != 0:
        return None
    code, output = _git(root, ["diff", "--name-status", f"{base_ref}...HEAD"])
    if code != 0:
        return None
    return parse_name_status(output.splitlines())


def tracked_md_files(root: Path) -> list[str] | None:
    code, output = _git(root, ["ls-files", "*.md"])
    if code != 0:
        return None
    return [normalize_relpath(line) for line in output.splitlines() if line.strip()]


def discover_pins(root: Path) -> tuple[list[Pin], list[str], int, int] | None:
    """Read every tracked ``.md`` once and scan both grammars.

    Returns (all_pins, info_messages, skipped_non_local_total, md_file_count),
    or None if ``git ls-files`` is unavailable.
    """
    md_files = tracked_md_files(root)
    if md_files is None:
        return None
    all_pins: list[Pin] = []
    info: list[str] = []
    skipped = 0
    for rel in md_files:
        path = root / Path(rel)
        try:
            text = path.read_text(encoding="utf-8-sig", errors="replace")
        except OSError:
            continue
        g1_pins, g1_info, g1_skipped = parse_grammar1_pins(text, rel)
        g2_pins, g2_skipped = parse_grammar2_pins(text, rel)
        all_pins.extend(g1_pins)
        all_pins.extend(g2_pins)
        info.extend(g1_info)
        skipped += g1_skipped + g2_skipped
    return all_pins, info, skipped, len(md_files)


def format_findings(findings: list[Finding]) -> str:
    lines: list[str] = []
    for finding in findings:
        lines.append(
            f"[{finding.grammar}] {finding.source_md} ({finding.label}): "
            f"{finding.problem}: {finding.resolved_rel}"
        )
        if finding.expected_hex is not None:
            lines.append(f"  pinned: {finding.expected_hex}")
        if finding.actual_hex is not None:
            lines.append(f"  actual: {finding.actual_hex}")
    return "\n".join(lines)


def run_scan(root: Path, *, base_ref: str | None, strict: bool, audit: bool) -> int:
    discovered = discover_pins(root)
    if discovered is None:
        print("check_hash_pin_freshness: WARNING: git ls-files unavailable; fail-open")
        return 0
    all_pins, info, skipped_non_local, md_count = discovered

    if audit:
        scoped = all_pins
        base_note = "audit"
    else:
        assert base_ref is not None
        changed = changed_paths_for_base(root, base_ref)
        if changed is None:
            mode = "--strict" if strict else "--check"
            print(f"check_hash_pin_freshness {mode}: WARNING: diff scope unavailable for {base_ref}; fail-open")
            return 0
        scoped = relevant_pins(all_pins, changed)
        base_note = f"base: {base_ref}"

    findings = findings_for_pins(root, scoped)

    if audit:
        g1_count = sum(1 for pin in all_pins if pin.grammar == "grammar1")
        g2_count = sum(1 for pin in all_pins if pin.grammar == "grammar2")
        missing = sum(1 for finding in findings if finding.problem == "pin_target_missing")
        mismatch = sum(1 for finding in findings if finding.problem == "pin_hash_mismatch")
        passed = len(all_pins) - len(findings)
        print("check_hash_pin_freshness --audit:")
        print(f"  md files scanned: {md_count}")
        print(f"  pins found: grammar1={g1_count} grammar2={g2_count} total={len(all_pins)}")
        print(f"  skipped (non-repo-local pointer): {skipped_non_local}")
        for message in info:
            print(f"  INFO: {message}")
        print(f"  pass: {passed}")
        print(f"  pin_target_missing: {missing}")
        print(f"  pin_hash_mismatch: {mismatch}")
        if findings:
            print(format_findings(findings))
        return 0

    mode = "--strict" if strict else "--check"
    if findings:
        print(f"check_hash_pin_freshness {mode}: {len(findings)} finding(s) ({base_note}):")
        print(format_findings(findings))
        return 1 if strict else 0
    print(f"check_hash_pin_freshness: OK ({base_note}; checked {len(scoped)} of {len(all_pins)} pin(s))")
    return 0


def selftest() -> int:
    ok = True

    def check(label: str, got: object, expected: object) -> None:
        nonlocal ok
        passed = got == expected
        if not passed:
            ok = False
        print(f"{'PASS' if passed else 'FAIL'}  {label}  expect={expected!r} got={got!r}")

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)

        # 1. grammar-1 pair parses; hash match passes.
        target = root / "foo.txt"
        target.write_bytes(b"hello world\n")
        expected_hex = sha256_normalized(target)
        text1 = f"- Source path: `foo.txt`\n- Source sha256: `{expected_hex}`\n"
        pins1, _, _ = parse_grammar1_pins(text1, "doc.md")
        check("case1 grammar1 pin count", len(pins1), 1)
        check("case1 grammar1 hash match passes", findings_for_pins(root, pins1), [])

        # 2. label mismatch (Source path + Wrapper sha256) -> no pin.
        text2 = f"- Source path: `foo.txt`\n- Wrapper sha256: `{expected_hex}`\n"
        pins2, _, _ = parse_grammar1_pins(text2, "doc.md")
        check("case2 label mismatch -> no pin", len(pins2), 0)

        # 3. uppercase pinned hex vs lowercase actual -> passes (case-insensitive).
        text3 = f"- Source path: `foo.txt`\n- Source sha256: `{expected_hex.upper()}`\n"
        pins3, _, _ = parse_grammar1_pins(text3, "doc.md")
        check("case3 uppercase pin parses", len(pins3), 1)
        check("case3 case-insensitive match passes", findings_for_pins(root, pins3), [])

        # 4. grammar-2 line parses; path resolves relative to receipt dir; passes.
        receipt_dir = root / "case" / "source_captures" / "e1"
        raw_dir = receipt_dir / "raw"
        raw_dir.mkdir(parents=True)
        raw_file = raw_dir / "blob.bin"
        raw_file.write_bytes(b"binary-content")
        g2_hex = sha256_normalized(raw_file)
        g2_text = f"- `file_01` -> `raw/blob.bin` (sha256 `{g2_hex}`, 14 bytes)\n"
        receipt_rel = "case/source_captures/e1/receipt.md"
        g2_pins, g2_skipped = parse_grammar2_pins(g2_text, receipt_rel)
        check("case4 grammar2 pin count", len(g2_pins), 1)
        check(
            "case4 resolved relative to receipt dir",
            g2_pins[0].resolved_rel if g2_pins else None,
            "case/source_captures/e1/raw/blob.bin",
        )
        check("case4 grammar2 hash match passes", findings_for_pins(root, g2_pins), [])

        # 5. CRLF fixture vs LF fixture -> identical normalized hash.
        crlf_file = root / "crlf.txt"
        lf_file = root / "lf.txt"
        crlf_file.write_bytes(b"line one\r\nline two\r\n")
        lf_file.write_bytes(b"line one\nline two\n")
        check("case5 CRLF/LF normalized hash match", sha256_normalized(crlf_file), sha256_normalized(lf_file))

        # 6. mismatch -> pin_hash_mismatch finding with both hex values.
        bad_pin = Pin("grammar1", "doc.md", "Source", "foo.txt", "foo.txt", "0" * 64)
        bad_findings = findings_for_pins(root, [bad_pin])
        check("case6 mismatch problem", bad_findings[0].problem if bad_findings else None, "pin_hash_mismatch")
        check("case6 mismatch expected hex", bad_findings[0].expected_hex if bad_findings else None, "0" * 64)
        check("case6 mismatch actual hex", bad_findings[0].actual_hex if bad_findings else None, expected_hex)

        # 7. missing target -> pin_target_missing.
        missing_pin = Pin("grammar1", "doc.md", "Source", "nope.txt", "nope.txt", expected_hex)
        missing_findings = findings_for_pins(root, [missing_pin])
        check(
            "case7 missing target problem",
            missing_findings[0].problem if missing_findings else None,
            "pin_target_missing",
        )

    # 8. table row -> not a pin.
    table_text = f"| Source | `{'a' * 64}` |\n"
    table_pins, _, _ = parse_grammar1_pins(table_text, "doc.md")
    check("case8 table row not a pin", len(table_pins), 0)

    # 9. source-read-ledger "Compare target: sha256 `<hex>`" -> not a pin.
    ledger_text = f"- Compare target: sha256 `{'b' * 64}`, size 100, checked 2026-01-01.\n"
    ledger_pins, _, _ = parse_grammar1_pins(ledger_text, "doc.md")
    check("case9 ledger line not a pin", len(ledger_pins), 0)

    # 10. URL/absolute/../drive path -> skipped non-repo-local, not a finding.
    skip_text = f"- Source path: `https://example.com/x`\n- Source sha256: `{'c' * 64}`\n"
    skip_pins, _, skip_count = parse_grammar1_pins(skip_text, "doc.md")
    check("case10 non-repo-local path -> no pin", len(skip_pins), 0)
    check("case10 non-repo-local path counted as skip", skip_count, 1)

    # 11. grammar-2 line outside a source_captures receipt.md -> not a pin.
    outside_text = f"- `file_01` -> `raw/blob.bin` (sha256 `{'d' * 64}`, 14 bytes)\n"
    outside_pins, _ = parse_grammar2_pins(outside_text, "docs/notes.md")
    check("case11 grammar2 outside receipt.md -> no pin", len(outside_pins), 0)

    # 12/13. relevance: pin-file changed, target-only changed, unrelated change.
    rel_pin = Pin("grammar1", "a.md", "Source", "b/file.bin", "b/file.bin", "e" * 64)
    check("case12 relevant when pin-file changed", [pin.label for pin in relevant_pins([rel_pin], {"a.md"})], ["Source"])
    check(
        "case13 relevant when only target changed",
        [pin.label for pin in relevant_pins([rel_pin], {"b/file.bin"})],
        ["Source"],
    )
    check("case13b not relevant on unrelated change", relevant_pins([rel_pin], {"unrelated.md"}), [])

    # 14. resolve_base_ref precedence: env wins, then --base, then default.
    saved = os.environ.pop("GITHUB_BASE_REF", None)
    try:
        check("case14 default base", resolve_base_ref(None), "origin/main")
        check("case14 cli base", resolve_base_ref("main"), "main")
        os.environ["GITHUB_BASE_REF"] = "develop"
        check("case14 env base wins", resolve_base_ref("main"), "origin/develop")
    finally:
        if saved is not None:
            os.environ["GITHUB_BASE_REF"] = saved
        else:
            os.environ.pop("GITHUB_BASE_REF", None)

    # Regression: repo-local pointer filter (mirror EP-37).
    check("repo-local pointer", is_repo_local_pointer("docs/a.md"), True)
    check("url pointer skipped", is_repo_local_pointer("https://example.com/x"), False)
    check("windows absolute skipped", is_repo_local_pointer("F:/outside/file.md"), False)
    check("parent traversal skipped", is_repo_local_pointer("../outside.md"), False)
    check("posix-rooted pointer skipped", is_repo_local_pointer("/etc/passwd"), False)
    check("unc-rooted pointer skipped", is_repo_local_pointer("\\\\server\\share\\file.md"), False)

    # Regression: rename-aware name-status parsing (mirror EP-37).
    check(
        "name-status includes rename source and destination",
        parse_name_status(["M\tdocs/a.md", "D\tdocs/b.md", "R100\tdocs/c.md\tdocs/d.md"]),
        {"docs/a.md", "docs/b.md", "docs/c.md", "docs/d.md"},
    )

    print("SELFTEST", "OK" if ok else "FAILED")
    return 0 if ok else 1


def _arg_value(argv: list[str], flag: str) -> str | None:
    if flag in argv:
        index = argv.index(flag)
        if index + 1 < len(argv):
            return argv[index + 1]
    return None


def main(argv: list[str]) -> int:
    if "--force-internal-error" in argv:
        raise RuntimeError("forced internal error (probe)")
    if "--selftest" in argv:
        return selftest()
    root = repo_root()
    if "--strict" in argv:
        return run_scan(
            root,
            base_ref=resolve_base_ref(_arg_value(argv, "--base")),
            strict=True,
            audit=False,
        )
    if "--check" in argv:
        return run_scan(
            root,
            base_ref=resolve_base_ref(_arg_value(argv, "--base")),
            strict=False,
            audit=False,
        )
    if "--audit" in argv:
        return run_scan(root, base_ref=None, strict=False, audit=True)
    print(
        "Usage: check_hash_pin_freshness.py --strict [--base <ref>] | --check [--base <ref>] | --audit | --selftest"
    )
    print("  --strict    CI/pre-push gate: fail on changed markdown hash-pin drift")
    print("  --check     same diff-scoped scan, always exit 0 except internal errors")
    print("  --audit     whole-repo markdown hash-pin scan, advisory")
    print("  --selftest  pure-function self-check")
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as exc:
        sys.stderr.write(f"check_hash_pin_freshness: internal error: {exc}\n")
        gating = "--strict" in sys.argv[1:] or "--selftest" in sys.argv[1:]
        sys.exit(1 if gating else 0)
