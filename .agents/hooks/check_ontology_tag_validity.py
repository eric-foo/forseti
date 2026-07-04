#!/usr/bin/env python3
"""Validate ontology tag annotations against the ontology SSOT roster.

This is a tag-mode gate only. It validates additive annotations such as
``term (CanonicalType)`` and does not ban CamelCase coinages or ordinary prose
parentheses.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[2]
ONTOLOGY_PATH = REPO_ROOT / "forseti/product/spines/foundation/ontology/ontology.yaml"

PAREN_RE = re.compile(r"\(([^()\n]{1,80})\)")
TYPE_TOKEN_RE = re.compile(r"^[A-Z][A-Za-z0-9]*$")

ONTOLOGY_PARTS = {
    "Vertical",
    "Brand",
    "Product",
    "Venue",
    "Wind",
    "Caller",
    "Call",
    "Observation",
    "Trend",
    "Vector",
    "Decision",
    "Event",
    "Reading",
    "Memo",
    "Case",
    "Outcome",
    "Capture",
    "Packet",
    "Evidence",
    "Unit",
    "Buyer",
    "Org",
    "Signal",
}

COMMON_PROPER_PARENS = {
    "Codex",
    "Claude",
    "Gemini",
    "GitHub",
    "Google",
    "Grok",
    "Haiku",
    "LinkedIn",
    "OpenAI",
    "Opus",
    "PyYAML",
    "Python",
    "Reddit",
    "Sonnet",
    "TikTok",
    "YouTube",
    "Windows",
}

# Pre-existing prose/code parentheticals that look type-like but are not
# ontology tag annotations. Keep this list narrow so new invalid tags still fail.
ALLOWLISTED_NON_TAG_PARENS = {
    (
        "forseti/product/spines/ecr/signal_content/core_spine_v0_signal_content_record_architecture_v0.md",
        "SourceCapturePacket",
        "provenance (SourceCapturePacket) and integrity",
    ),
    (
        "docs/review-outputs/adversarial-artifact-reviews/linkedin_live_observation_slice3b_code_review_v0.md",
        "LiveObservation",
        "reviewed_artifact: capture_spine/linkedin_live_adapter/{models,validation,__init__}.py (LiveObservation)",
    ),
    (
        "docs/prompts/reviews/source_capture_anti_blocking_http_ladder_delegated_adversarial_code_review_and_patch_prompt_v0.md",
        "CaptureBodyClass",
        "assert set(CaptureBodyClass) ==",
    ),
    (
        "docs/migration/capture_spine_source_capture_migration_inventory_v0.md",
        "Capture",
        "current_owner: Source Capture Armory (Capture)",
    ),
    (
        "docs/migration/search_demand_signal_migration_inventory_v0.md",
        "Capture",
        "wind-caller **capture** (Capture)",
    ),
}

SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".codex",
    ".claude",
    ".pytest_tmp",
    "__pycache__",
    "node_modules",
}


@dataclass(frozen=True)
class Finding:
    path: Path
    line_no: int
    col_no: int
    tag: str
    line: str


def load_roster(path: Path = ONTOLOGY_PATH) -> set[str]:
    import yaml

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    types = data.get("types", {})
    if not isinstance(types, dict) or not types:
        raise RuntimeError(f"ontology roster not found at {path}")
    return set(types)


def writable_temp_parent() -> Path:
    candidates: list[Path] = []
    for var in ("ORCA_HOOK_TMPDIR", "RUNNER_TEMP", "TMPDIR", "TEMP", "TMP"):
        value = os.environ.get(var)
        if value:
            candidates.append(Path(value))
    candidates.append(REPO_ROOT)

    for candidate in candidates:
        probe_dir = candidate / f".ontology_tag_validity_probe_{os.getpid()}"
        try:
            candidate.mkdir(parents=True, exist_ok=True)
            probe_dir.mkdir(exist_ok=False)
            probe = probe_dir / "probe.txt"
            probe.write_text("ok", encoding="utf-8")
            probe.unlink()
            probe_dir.rmdir()
            return candidate
        except OSError:
            try:
                probe = probe_dir / "probe.txt"
                if probe.exists():
                    probe.unlink()
                if probe_dir.exists():
                    probe_dir.rmdir()
            except OSError:
                pass
            continue
    raise RuntimeError("no writable temporary directory for ontology tag validity selftest")


def markdown_files(root: Path) -> Iterable[Path]:
    stack = [root]
    while stack:
        current = stack.pop()
        try:
            with os.scandir(current) as entries:
                for entry in entries:
                    if entry.name in SKIP_DIRS:
                        continue
                    path = Path(entry.path)
                    if entry.is_dir(follow_symlinks=False):
                        stack.append(path)
                    elif entry.is_file(follow_symlinks=False) and path.suffix.lower() == ".md":
                        yield path
        except OSError:
            continue


def split_type_parts(token: str) -> set[str]:
    return set(re.findall(r"[A-Z][a-z0-9]*", token))


def left_phrase(line: str, paren_start: int) -> str:
    left = line[:paren_start].rstrip()
    if not left:
        return ""
    pieces = re.split(r"[`|:[\]{}]", left)
    phrase = pieces[-1].strip()
    phrase = re.sub(r"^[>*#\-\d.\s]+", "", phrase).strip()
    return phrase[-96:]


def looks_like_type_token(token: str) -> bool:
    return bool(TYPE_TOKEN_RE.fullmatch(token)) and any(ch.islower() for ch in token)


def looks_like_tag_annotation(line: str, match: re.Match[str], roster: set[str]) -> bool:
    token = match.group(1).strip()
    if not looks_like_type_token(token):
        return False
    if token in roster:
        return True
    if token in COMMON_PROPER_PARENS:
        return False

    phrase = left_phrase(line, match.start())
    if not phrase:
        return False
    last_word = re.search(r"([A-Za-z][A-Za-z0-9_-]*)\s*$", phrase)
    if last_word and last_word.group(1) == token:
        return False

    token_parts = split_type_parts(token)
    return bool(token_parts & ONTOLOGY_PARTS)


def is_allowlisted_non_tag(path: Path, token: str, line: str) -> bool:
    try:
        rel = path.resolve().relative_to(REPO_ROOT.resolve()).as_posix()
    except ValueError:
        return False
    return any(
        rel == allowed_path and token == allowed_token and snippet in line
        for allowed_path, allowed_token, snippet in ALLOWLISTED_NON_TAG_PARENS
    )


def scan_file(path: Path, roster: set[str]) -> list[Finding]:
    findings: list[Finding] = []
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = path.read_text(encoding="utf-8", errors="replace")
    for line_no, line in enumerate(text.splitlines(), start=1):
        for match in PAREN_RE.finditer(line):
            token = match.group(1).strip()
            if not looks_like_tag_annotation(line, match, roster):
                continue
            if token not in roster and is_allowlisted_non_tag(path, token, line):
                continue
            if token not in roster:
                findings.append(
                    Finding(
                        path=path,
                        line_no=line_no,
                        col_no=match.start(1) + 1,
                        tag=token,
                        line=line.rstrip(),
                    )
                )
    return findings


def scan(root: Path, roster: set[str]) -> list[Finding]:
    findings: list[Finding] = []
    for path in markdown_files(root):
        findings.extend(scan_file(path, roster))
    return findings


def print_findings(findings: list[Finding], root: Path) -> None:
    if not findings:
        print("ontology tag validity: OK")
        return
    print("ontology tag validity: INVALID TAGS")
    for finding in findings:
        rel = finding.path.relative_to(root)
        print(
            f"{rel}:{finding.line_no}:{finding.col_no}: "
            f"unknown ontology tag type ({finding.tag})"
        )
        safe_line = finding.line.encode("ascii", "backslashreplace").decode("ascii")
        print(f"  {safe_line}")


def run_selftest() -> int:
    roster = {
        "Vertical",
        "Brand",
        "Product",
        "Venue",
        "WindCaller",
        "Call",
        "Observation",
        "TrendVector",
        "DecisionEvent",
        "Reading",
        "Memo",
        "Case",
        "Outcome",
        "CapturePacket",
        "EvidenceUnit",
        "Buyer",
        "Org",
    }
    root = writable_temp_parent() / f".ontology_tag_validity_selftest_{os.getpid()}"
    root.mkdir(exist_ok=False)
    try:
        (root / "valid.md").write_text(
            "\n".join(
                [
                    "purchase (DecisionEvent)",
                    "Source Capture Packet (CapturePacket)",
                    "target buyer (Buyer)",
                    "OpenAI (OpenAI) is ordinary prose here.",
                    "Section 2 (Examples) is ordinary prose here.",
                    "EvidenceUnit (EvidenceUnit) is redundant but not invalid.",
                ]
            ),
            encoding="utf-8",
        )
        (root / "invalid.md").write_text(
            "\n".join(
                [
                    "purchase decision (Decision)",
                    "buying signal (Signal)",
                    "candidate packet (PacketThing)",
                ]
            ),
            encoding="utf-8",
        )
        findings = scan(root, roster)
        found = {(f.path.name, f.tag) for f in findings}
    finally:
        for child in root.iterdir():
            child.unlink()
        root.rmdir()

    expected = {
        ("invalid.md", "Decision"),
        ("invalid.md", "Signal"),
        ("invalid.md", "PacketThing"),
    }
    if found != expected:
        print("ontology tag validity selftest: FAILED")
        print(f"expected: {sorted(expected)}")
        print(f"found:    {sorted(found)}")
        return 1
    print("ontology tag validity selftest: OK")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--strict", action="store_true", help="fail on invalid tags")
    mode.add_argument("--check", action="store_true", help="report invalid tags, exit 0")
    mode.add_argument("--selftest", action="store_true", help="run built-in tests")
    parser.add_argument("--root", type=Path, default=REPO_ROOT)
    args = parser.parse_args()

    if args.selftest:
        return run_selftest()

    roster = load_roster()
    findings = scan(args.root.resolve(), roster)
    print_findings(findings, args.root.resolve())
    if args.strict and findings:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())