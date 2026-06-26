#!/usr/bin/env python3
"""Validate Commission Signal Board classifier handoff rows.

This is a local/manual checker. It does not run retrieval, classify demand,
construct graphs, or prove a board is correct. It only checks that rows listed
in the classifier handoff are evidence-backed and cutoff-safe according to the
board's own row table, that the row table carries the mechanically required
recency/current-state attention fields, and that the output does not turn
engagement/resonance language into a mechanical proof or authority shortcut.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import sys
from typing import Any

import yaml

ROW_SECTION_RE = re.compile(
    r"^###\s+4\.\s+Signal Board Rows\s*$"
    r"(?P<body>.*?)"
    r"(?=^###\s+\d+\.|\Z)",
    re.IGNORECASE | re.MULTILINE | re.DOTALL,
)
HANDOFF_SECTION_RE = re.compile(
    r"^###\s+8\.\s+Demand-Classifier Handoff Packet\s*$"
    r"(?P<body>.*?)"
    r"(?=^###\s+\d+\.|\Z)",
    re.IGNORECASE | re.MULTILINE | re.DOTALL,
)
YAML_FENCE_RE = re.compile(r"```yaml\s*(?P<body>.*?)\s*```", re.IGNORECASE | re.DOTALL)

REQUIRED_ROW_COLUMNS = {
    "row_id",
    "source_family",
    "signal_role",
    "row_purpose",
    "recency_status",
    "recency_attention",
    "graph_role",
    "graph_weight_hint",
    "evidence_status",
    "surface_cutoff_status",
    "cutoff_status",
}
VALID_HANDOFF_MODES = {"backtest", "forward", "unknown"}
VALID_ROW_PURPOSES = {
    "chronology",
    "source_route",
    "signal_unit",
    "contradiction",
    "gap",
    "classifier_handoff",
    "recency_priority",
}
VALID_RECENCY_STATUSES = {
    "current_state",
    "recent",
    "older_context",
    "stale_or_unknown",
    "not_applicable",
}
VALID_RECENCY_ATTENTIONS = {"high", "normal", "low", "unknown"}
VALID_GRAPH_ROLES = {
    "seed",
    "node_candidate",
    "edge_candidate",
    "propagation_path",
    "campaign_overlap_check",
    "counterevidence_path",
    "none",
}
VALID_GRAPH_WEIGHT_HINTS = {"high", "medium", "low", "none"}
ENGAGEMENT_RULE_AUTHORITY = (
    "orca/product/spines/commission_signal_board/authority/"
    "orca_commission_signal_board_prompt_structure_rules_v0.md"
)
ENGAGEMENT_SIGNAL_RE = (
    r"(?:engagement(?:\s+counts?)?|public[- ]reaction|reaction\s+volume|"
    r"high[- ]engagement|low[- ]engagement|upvotes?|helpful\s+votes?|likes?|"
    r"views?|shares?|comments?|reply\s+counts?|source[- ]native\s+scores?|"
    r"source\s+rank|source\s+order|resonance)"
)
ENGAGEMENT_CLAIM_GAP = r"[^.\n;]{0,80}"
NEGATED_OVERCLAIM_RE = re.compile(
    r"\b(?:no|not|never|without|cannot|can't|must\s+not|does\s+not|do\s+not|"
    r"don't|is\s+not|are\s+not|not\s+enough\s+to)\b",
    re.IGNORECASE,
)
FORBIDDEN_ENGAGEMENT_OVERCLAIMS = {
    "engagement_as_proof": re.compile(
        rf"(?:\b{ENGAGEMENT_SIGNAL_RE}\b{ENGAGEMENT_CLAIM_GAP}\b(?:proves?|proof|validates?|confirms?|"
        rf"establishes|demonstrates|clears?|means|counts\s+as)\b{ENGAGEMENT_CLAIM_GAP}\b(?:demand|buyer\s+pull|"
        rf"willingness\s+to\s+pay|market\s+pull|purchase\s+intent)\b|"
        rf"\b(?:demand|buyer\s+pull|willingness\s+to\s+pay|market\s+pull|purchase\s+intent)\b"
        rf"{ENGAGEMENT_CLAIM_GAP}\b(?:is\s+)?(?:proven|proved|validated|confirmed|established|demonstrated|cleared|"
        rf"proof)\b{ENGAGEMENT_CLAIM_GAP}\b(?:by|from|because\s+of|due\s+to|through|via)\b{ENGAGEMENT_CLAIM_GAP}\b"
        rf"{ENGAGEMENT_SIGNAL_RE}\b)",
        re.IGNORECASE,
    ),
    "engagement_graph_weight_shortcut": re.compile(
        rf"(?:\b{ENGAGEMENT_SIGNAL_RE}\b{ENGAGEMENT_CLAIM_GAP}\b(?:sets?|determines|drives|raises|"
        rf"increases|justifies|supports?|becomes|is|means|counts\s+as)\b{ENGAGEMENT_CLAIM_GAP}\b(?:graph[_ -]?weight"
        rf"(?:[_ -]?hint)?|graph\s+score|graph\s+strength)\b|"
        rf"\b(?:graph[_ -]?weight(?:[_ -]?hint)?|graph\s+score|graph\s+strength)\b"
        rf"{ENGAGEMENT_CLAIM_GAP}\b(?:is|was|becomes|sets?|determined|driven|raised|increased|justified|supported|"
        rf"because\s+of|due\s+to|from|by|based\s+on)\b{ENGAGEMENT_CLAIM_GAP}\b{ENGAGEMENT_SIGNAL_RE}\b)",
        re.IGNORECASE,
    ),
    "engagement_commit_scale_shortcut": re.compile(
        rf"(?:\b{ENGAGEMENT_SIGNAL_RE}\b{ENGAGEMENT_CLAIM_GAP}\b(?:clears?|supports?|justifies?|passes?|"
        rf"unlocks?|establishes|means|counts\s+as)\b{ENGAGEMENT_CLAIM_GAP}\b(?:Commit/Scale|Commit|Scale|buyer\s+proof|"
        rf"demand\s+gate)\b|"
        rf"\b(?:Commit/Scale|Commit|Scale|buyer\s+proof|demand\s+gate)\b"
        rf"{ENGAGEMENT_CLAIM_GAP}\b(?:is|was|cleared|supported|justified|passed|unlocked|established|"
        rf"because\s+of|due\s+to|from|by|based\s+on)\b{ENGAGEMENT_CLAIM_GAP}\b{ENGAGEMENT_SIGNAL_RE}\b)",
        re.IGNORECASE,
    ),
    "engagement_credibility_shortcut": re.compile(
        rf"(?:\b{ENGAGEMENT_SIGNAL_RE}\b{ENGAGEMENT_CLAIM_GAP}\b(?:proves?|confirms?|establishes|"
        rf"supports?|justifies?|sets?|labels?|means|counts\s+as)\b{ENGAGEMENT_CLAIM_GAP}\b(?:credibility|credible|"
        rf"independence|trustworthy|trust)\b|"
        rf"\b(?:credibility|credible|independence|trustworthy|trust)\b"
        rf"{ENGAGEMENT_CLAIM_GAP}\b(?:is|was|proven|confirmed|established|supported|justified|set|labeled|"
        rf"because\s+of|due\s+to|from|by|based\s+on)\b{ENGAGEMENT_CLAIM_GAP}\b{ENGAGEMENT_SIGNAL_RE}\b)",
        re.IGNORECASE,
    ),
    "engagement_action_ceiling_shortcut": re.compile(
        rf"(?:\b{ENGAGEMENT_SIGNAL_RE}\b{ENGAGEMENT_CLAIM_GAP}\b(?:clears?|sets?|raises|supports?|"
        rf"justifies?|establishes|means|counts\s+as)\b{ENGAGEMENT_CLAIM_GAP}\bAction\s+Ceiling\b|"
        rf"\bAction\s+Ceiling\b{ENGAGEMENT_CLAIM_GAP}\b(?:is|was|cleared|set|raised|supported|justified|"
        rf"established|because\s+of|due\s+to|from|by|based\s+on)\b{ENGAGEMENT_CLAIM_GAP}\b"
        rf"{ENGAGEMENT_SIGNAL_RE}\b)",
        re.IGNORECASE,
    ),
    "engagement_final_resonance_weight": re.compile(r"\bfinal\s+resonance\s+weight\b", re.IGNORECASE),
}



@dataclass(frozen=True)
class Finding:
    code: str
    message: str
    row_id: str = ""


def _normalize_header(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.strip().lower()).strip("_")


def _normalize_vocab(value: Any) -> str:
    if value is None:
        return ""
    return re.sub(r"[^a-z0-9]+", "_", str(value).strip().lower()).strip("_")


def _line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _excerpt(value: str, limit: int = 120) -> str:
    compact = " ".join(value.split())
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3] + "..."


def _is_nonclaim_context(text: str, start: int, end: int) -> bool:
    left_bounds = [text.rfind(boundary, 0, start) for boundary in (".", "\n", ";")]
    right_bounds = [idx for idx in (text.find(boundary, end) for boundary in (".", "\n", ";")) if idx != -1]
    left = max(left_bounds) + 1
    right = min(right_bounds) if right_bounds else min(len(text), end + 80)
    window = text[left:right]
    return NEGATED_OVERCLAIM_RE.search(window) is not None


def _validate_engagement_overclaims(text: str) -> list[Finding]:
    findings: list[Finding] = []
    seen: set[tuple[str, int, str]] = set()
    for code, pattern in FORBIDDEN_ENGAGEMENT_OVERCLAIMS.items():
        for match in pattern.finditer(text):
            if _is_nonclaim_context(text, match.start(), match.end()):
                continue
            line = _line_number(text, match.start())
            excerpt = _excerpt(match.group(0))
            key = (code, line, excerpt)
            if key in seen:
                continue
            seen.add(key)
            findings.append(
                Finding(
                    code,
                    "Forbidden engagement/resonance overclaim language "
                    f"near line {line}: {excerpt!r}. See {ENGAGEMENT_RULE_AUTHORITY}.",
                )
            )
    return findings


def _split_table_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def _is_separator_row(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell.strip()) for cell in cells)


def _extract_section(pattern: re.Pattern[str], text: str, missing_code: str, missing_message: str) -> tuple[str, list[Finding]]:
    match = pattern.search(text)
    if not match:
        return "", [Finding(missing_code, missing_message)]
    return match.group("body"), []



def _validate_vocab_field(
    row_id: str,
    row: dict[str, str],
    field_name: str,
    valid_values: set[str],
    finding_code: str,
) -> list[Finding]:
    raw_value = row.get(field_name, "")
    normalized = _normalize_vocab(raw_value)
    if normalized in valid_values:
        return []
    valid_display = ", ".join(sorted(valid_values))
    return [
        Finding(
            finding_code,
            f"{field_name} must be one of {valid_display}, got {raw_value or '<blank>'}.",
            row_id,
        )
    ]


def _validate_signal_row_vocab(row_id: str, row: dict[str, str]) -> list[Finding]:
    findings: list[Finding] = []
    findings.extend(
        _validate_vocab_field(row_id, row, "row_purpose", VALID_ROW_PURPOSES, "invalid_row_purpose")
    )
    findings.extend(
        _validate_vocab_field(
            row_id,
            row,
            "recency_status",
            VALID_RECENCY_STATUSES,
            "invalid_recency_status",
        )
    )
    findings.extend(
        _validate_vocab_field(
            row_id,
            row,
            "recency_attention",
            VALID_RECENCY_ATTENTIONS,
            "invalid_recency_attention",
        )
    )
    findings.extend(
        _validate_vocab_field(
            row_id,
            row,
            "graph_role",
            VALID_GRAPH_ROLES,
            "invalid_graph_role",
        )
    )
    findings.extend(
        _validate_vocab_field(
            row_id,
            row,
            "graph_weight_hint",
            VALID_GRAPH_WEIGHT_HINTS,
            "invalid_graph_weight_hint",
        )
    )
    return findings


def parse_signal_rows(text: str) -> tuple[dict[str, dict[str, str]], list[Finding]]:
    section, findings = _extract_section(
        ROW_SECTION_RE,
        text,
        "missing_signal_board_rows",
        "Missing Section 4 Signal Board Rows.",
    )
    if findings:
        return {}, findings

    table_lines = [line for line in section.splitlines() if line.strip().startswith("|")]
    if len(table_lines) < 2:
        return {}, [Finding("missing_signal_board_rows_table", "Section 4 has no Markdown table.")]

    headers = [_normalize_header(cell) for cell in _split_table_row(table_lines[0])]
    missing = sorted(REQUIRED_ROW_COLUMNS - set(headers))
    if missing:
        return {}, [
            Finding(
                "missing_required_row_columns",
                "Section 4 table is missing required columns: " + ", ".join(missing),
            )
        ]

    rows: dict[str, dict[str, str]] = {}
    out_findings: list[Finding] = []
    for table_index, line in enumerate(table_lines[1:], start=2):
        cells = _split_table_row(line)
        if _is_separator_row(cells):
            continue
        if len(cells) != len(headers):
            first_cell = cells[0] if cells else ""
            out_findings.append(
                Finding(
                    "malformed_signal_board_row",
                    "Row has a different cell count than the header "
                    f"(table row {table_index}, first cell {first_cell or '<blank>'}).",
                )
            )
            continue
        row = dict(zip(headers, cells, strict=True))
        row_id = row.get("row_id", "")
        if not row_id:
            out_findings.append(Finding("missing_row_id", "Signal board row is missing Row ID."))
            continue
        if row_id in rows:
            out_findings.append(Finding("duplicate_row_id", f"Duplicate signal board row ID {row_id}.", row_id))
            continue
        out_findings.extend(_validate_signal_row_vocab(row_id, row))
        rows[row_id] = row
    return rows, out_findings


def parse_classifier_handoff(text: str) -> tuple[dict[str, Any], list[Finding]]:
    section, findings = _extract_section(
        HANDOFF_SECTION_RE,
        text,
        "missing_classifier_handoff_section",
        "Missing Section 8 Demand-Classifier Handoff Packet.",
    )
    if findings:
        return {}, findings

    fence = YAML_FENCE_RE.search(section)
    if not fence:
        return {}, [Finding("missing_classifier_handoff_yaml", "Section 8 has no yaml fence.")]

    try:
        data = yaml.safe_load(fence.group("body")) or {}
    except yaml.YAMLError as exc:
        return {}, [Finding("invalid_classifier_handoff_yaml", f"Section 8 YAML is invalid: {exc}")]

    packet = data.get("classifier_handoff_packet") if isinstance(data, dict) else None
    if not isinstance(packet, dict):
        return {}, [Finding("missing_classifier_handoff_packet", "Section 8 YAML lacks classifier_handoff_packet.")]
    return packet, []


def _handoff_ids(packet: dict[str, Any], key: str) -> tuple[list[str], list[Finding]]:
    value = packet.get(key)
    if value is None:
        return [], []
    if not isinstance(value, list):
        return [], [Finding("handoff_rows_not_list", f"{key} must be a list.")]
    ids: list[str] = []
    findings: list[Finding] = []
    for item in value:
        if not isinstance(item, str):
            findings.append(Finding("handoff_row_id_not_string", f"{key} contains a non-string row ID."))
            continue
        ids.append(item)
    return ids, findings


def _validate_handoff_row(row_id: str, row: dict[str, str], mode: str) -> list[Finding]:
    findings: list[Finding] = []
    evidence_status_raw = row.get("evidence_status", "")
    evidence_status = _normalize_vocab(evidence_status_raw)
    cutoff_status = _normalize_vocab(row.get("cutoff_status", ""))
    surface_cutoff_status = _normalize_vocab(row.get("surface_cutoff_status", ""))
    source_family = _normalize_vocab(row.get("source_family", ""))
    signal_role = _normalize_vocab(row.get("signal_role", ""))

    if source_family == "aeo_answer_engines" or signal_role == "aeo_visibility":
        findings.append(
            Finding(
                "handoff_row_aeo_visibility",
                "AEO / answer-engine rows are visibility annotations and must not enter classifier handoff.",
                row_id,
            )
        )

    if evidence_status == "excluded_future_info":
        findings.append(
            Finding("handoff_row_future_info", "excluded_future_info rows must not enter classifier handoff.", row_id)
        )
    elif evidence_status != "source_backed":
        findings.append(
            Finding(
                "handoff_row_not_source_backed",
                f"Classifier handoff row must be source_backed, got {evidence_status_raw or '<blank>'}.",
                row_id,
            )
        )

    if mode == "backtest":
        if surface_cutoff_status != "existed_by_cutoff":
            findings.append(
                Finding(
                    "handoff_row_surface_cutoff_invalid",
                    "Backtest handoff row must have surface_cutoff_status: existed_by_cutoff.",
                    row_id,
                )
            )
        if cutoff_status != "in_window":
            findings.append(
                Finding(
                    "handoff_row_cutoff_invalid",
                    "Backtest handoff row must have cutoff_status: in_window.",
                    row_id,
                )
            )

    return findings


def validate_text(text: str) -> list[Finding]:
    rows, row_findings = parse_signal_rows(text)
    packet, packet_findings = parse_classifier_handoff(text)
    findings = [*row_findings, *packet_findings]
    findings.extend(_validate_engagement_overclaims(text))
    if packet_findings or not rows:
        return findings

    mode = _normalize_vocab(packet.get("mode"))
    if not mode:
        findings.append(Finding("missing_handoff_mode", "classifier_handoff_packet.mode is required."))
    elif mode not in VALID_HANDOFF_MODES:
        findings.append(
            Finding(
                "invalid_handoff_mode",
                f"classifier_handoff_packet.mode must be one of {', '.join(sorted(VALID_HANDOFF_MODES))}.",
            )
        )

    signal_ids, signal_findings = _handoff_ids(packet, "signal_rows_for_handoff")
    counter_ids, counter_findings = _handoff_ids(packet, "counterevidence_rows_for_handoff")
    findings.extend(signal_findings)
    findings.extend(counter_findings)

    all_ids = [*signal_ids, *counter_ids]
    seen: set[str] = set()
    for row_id in all_ids:
        if row_id in seen:
            findings.append(Finding("duplicate_handoff_row", f"Row {row_id} appears more than once.", row_id))
            continue
        seen.add(row_id)

        row = rows.get(row_id)
        if row is None:
            findings.append(Finding("handoff_row_unknown", f"Row {row_id} is not present in Section 4.", row_id))
            continue
        findings.extend(_validate_handoff_row(row_id, row, mode))

    return findings


def _expected_from_fixture(path: Path) -> str:
    first_line = path.read_text(encoding="utf-8").splitlines()[0]
    match = re.search(r"fixture_expected:\s*(pass|fail)", first_line)
    if not match:
        return ""
    return match.group(1)


def selftest() -> int:
    root = Path(__file__).resolve().parents[2]
    fixture_dir = root / "orca-harness" / "tests" / "fixtures" / "commission_signal_board_outputs"
    fixture_paths = sorted(fixture_dir.glob("*.txt"))
    if not fixture_paths:
        print(f"SELFTEST FAILED: no fixtures found at {fixture_dir}")
        return 1

    ok = True
    for path in fixture_paths:
        expected = _expected_from_fixture(path)
        findings = validate_text(path.read_text(encoding="utf-8"))
        passed = not findings
        if expected == "pass" and passed:
            print(f"PASS {path.name}")
        elif expected == "fail" and not passed:
            print(f"PASS {path.name} expected fail: {', '.join(sorted({f.code for f in findings}))}")
        else:
            ok = False
            print(f"FAIL {path.name} expected={expected or '<missing>'} findings={findings}")
    print("SELFTEST", "OK" if ok else "FAILED")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()
    paths = [Path(arg) for arg in argv if not arg.startswith("-")]
    if not paths:
        print("usage: check_commission_signal_board_output.py [--selftest] <output-file> [...]", file=sys.stderr)
        return 2

    exit_code = 0
    for path in paths:
        findings = validate_text(path.read_text(encoding="utf-8"))
        if findings:
            exit_code = 1
            print(f"FAIL {path}")
            for finding in findings:
                suffix = f" row={finding.row_id}" if finding.row_id else ""
                print(f"  {finding.code}{suffix}: {finding.message}")
        else:
            print(f"PASS {path}")
    return exit_code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
