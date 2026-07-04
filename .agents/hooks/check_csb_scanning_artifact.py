#!/usr/bin/env python3
"""Validate minimum receipt shape for CSB-first scanning artifacts.

This is a local/manual checker with a forward-only changed-file mode for CI.
It does not run retrieval, grade signal quality, validate candidates, bind
Capture routes, or prove a scan is good. It only checks that a CSB-first scan
artifact preserves the mechanical receipt shape needed for review: source
context, caps, broad-scout accounting, CSB-row accountability, exact-query
accounting, venue/hidden-venue accounting, observations, negatives/access notes,
capture-request accounting, bounded candidate closeout, and mechanical
engagement/resonance overclaim language.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import date
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any, Iterable

import yaml

YAML_FENCE_RE = re.compile(r"```yaml\s*(?P<body>.*?)\s*```", re.IGNORECASE | re.DOTALL)
HEADING_RE = re.compile(r"^##\s+", re.MULTILINE)
MOVE_ID_RE = re.compile(r"\bM\d{2,}\b")
EXACT_QUERY_ID_RE = re.compile(r"\bEQ-\d{3,}\b")
CSB_ROW_ID_RE = re.compile(r"\bSBR-\d{3,}\b")

REQUIRED_INTAKE_FIELDS = {
    "commission_id",
    "scan_date",
    "mode",
    "subject",
    "source_context_status",
    "run_caps",
    "screening_moves_used",
    "exact_queries_used",
    "closeout_state",
}
REQUIRED_RUN_CAPS = {"max_screening_moves_total", "max_exact_queries_total"}
VALID_CLOSEOUT_STATES = {
    "candidate_ready_for_next_lane",
    "capture_preservation_only",
    "no_candidate_after_discovery",
}
VALID_SOURCE_CONTEXT_STATUS = "SOURCE_CONTEXT_READY"
VALID_SIGNAL_STAGES = {
    "venue_value",
    "precursor",
    "candidate_support",
    "contradiction",
    "negative",
    "access_note",
    "unknown",
}
VALID_GATE_ROLES = {
    "none",
    "demand_origin",
    "costly_behavior",
    "divergence",
    "org_motion",
    "decision_event",
    "influence",
}
VALID_ROUTE_BINDING_STATES = {
    "cited_current",
    "unknown",
    "blocked_outside_current_binding",
    "not_applicable",
}
AUTO_SCAN_PREFIXES = ("docs/research/",)
AUTO_SCAN_REQUIRED_MARKERS = (
    "commission_id:",
    "source_context_status:",
    "closeout_state:",
)
AUTO_SCAN_ROUTE_MARKERS = (
    "csb-first",
    "csb board",
    "csb_rows_consumed",
    "rows consumed as route map",
)
REQUIRED_OBSERVATION_FIELDS = {
    "observation_id",
    "source_move_id",
    "url",
    "retrieval_date",
    "short_quote_or_summary",
    "signal_stage",
    "claim_it_might_support",
    "gate_role",
    "independence_hypothesis",
    "uncertainty_or_limits",
}
REQUIRED_CANDIDATE_OBSERVATION_FIELDS = {
    "candidate_observation_id",
    "candidate",
    "supporting_observations",
    "why_promoted",
    "decision_window",
    "competing_or_defeating_observations",
    "capture_needed",
}
REQUIRED_CAPTURE_REQUEST_FIELDS = {
    "capture_request_id",
    "source_scan",
    "candidate_or_observation_ids",
    "urls",
    "what_capture_should_verify",
    "decision_window",
    "route_binding_state",
    "creator_registry_match_preflight",
    "screening_evidence_summary",
    "uncertainty_or_access_limits",
    "not_requested",
}
REQUIRED_CREATOR_REGISTRY_PREFLIGHT_FIELDS = {
    "required_when",
    "receipt_path",
    "intended_action",
    "decision",
    "action_status",
    "can_start_new_capture",
}
VALID_CREATOR_REGISTRY_REQUIRED_WHEN = {"new_social_creator_account_capture", "not_applicable"}
NOT_APPLICABLE_ALLOWED_PREFLIGHT_VOCAB = {"", "not_applicable"}
VALID_CREATOR_REGISTRY_INTENDED_ACTIONS = {"new_capture", "classify", "update_existing", "not_applicable"}
VALID_CREATOR_REGISTRY_DECISIONS = {"existing_match", "new_candidate", "ambiguous_match", "invalid_candidate", "not_applicable"}
VALID_CREATOR_REGISTRY_ACTION_STATUSES = {"allowed", "blocked", "not_applicable"}
PLACEHOLDER_PREFLIGHT_RECEIPT_VALUES = {
    "",
    "none",
    "null",
    "null_or_path",
    "not_applicable",
    "unknown",
    "unknown_with_reason",
    "path",
    "path_to_preflight_receipt_json",
}
REQUIRED_CAPTURE_URL_FIELDS = {"url", "venue", "observation_supported", "gate_role"}
REQUIRED_NOT_REQUESTED = {
    "route_expansion",
    "packet_commitment_by_scanning",
    "ecr_cleaning_or_judgment_work",
}

SECTION_PATTERNS = {
    "broad_scout_accounting": re.compile(r"^##\s+Broad Scout\b", re.IGNORECASE | re.MULTILINE),
    "csb_row_accounting": re.compile(
        r"(csb_rows_consumed|Rows consumed as route map:)",
        re.IGNORECASE | re.MULTILINE,
    ),
    "exact_query_accounting": re.compile(
        r"^##\s+Exact Query Discovery Ledger\b",
        re.IGNORECASE | re.MULTILINE,
    ),
    "venue_evaluation": re.compile(r"^##\s+Venue Evaluation\b", re.IGNORECASE | re.MULTILINE),
    "hidden_venue_accounting": re.compile(
        r"^##\s+Hidden Venue Pointers\b",
        re.IGNORECASE | re.MULTILINE,
    ),
    "observations": re.compile(r"^##\s+(Screen-Light Observations|Observations)\b", re.IGNORECASE | re.MULTILINE),
    "negatives_access_notes": re.compile(r"^##\s+Negatives And Access Notes\b", re.IGNORECASE | re.MULTILINE),
    "capture_request_accounting": re.compile(
        r"^##\s+(Capture Requests|Capture Triage)\b",
        re.IGNORECASE | re.MULTILINE,
    ),
    "candidate_decision": re.compile(
        r"^##\s+(Candidate Decision|Candidate Observation Decision)\b",
        re.IGNORECASE | re.MULTILINE,
    ),
    "closeout": re.compile(r"^##\s+Closeout\b", re.IGNORECASE | re.MULTILINE),
}

BROAD_SCOUT_DETAIL_PATTERNS = {
    "frontier": re.compile(r"\bfrontiers?\b", re.IGNORECASE),
    "exact_query": re.compile(r"\b(exact[-_ ]?quer(y|ies)|EQ-\d{3,})\b", re.IGNORECASE),
    "venue_eval": re.compile(r"\b(venue[_ -]?eval|venue evaluation|venues?)\b", re.IGNORECASE),
    "hidden_venue_pointer": re.compile(r"\b(hidden venue|hidden_venue_pointer)\b", re.IGNORECASE),
    "negative": re.compile(r"\bnegatives?\b", re.IGNORECASE),
    "access_note": re.compile(r"\b(access notes?|access walls?)\b", re.IGNORECASE),
    "recency_current_state": re.compile(r"\b(recency|recent|currentness|current-state|current state)\b", re.IGNORECASE),
    "main_deepening": re.compile(
        r"\b(main deepening|recommended(?: main)? deepening|recommended for deepening|targeted deepening|deepening (?:phase|path|direction|recommendation)|deepen(?:ing)?)\b",
        re.IGNORECASE,
    ),
}

ENGAGEMENT_RULE_AUTHORITY = "orca/product/shared/engagement_registry/engagement_logic_registry_v0.md"
ENGAGEMENT_SIGNAL_RE = (
    r"(?:engagement(?:\s+counts?)?|public[- ]reaction|reaction\s+volume|"
    r"high[- ]engagement|low[- ]engagement|upvotes?|helpful\s+votes?|likes?|"
    r"views?|shares?|comments?|reply\s+counts?|source[- ]native\s+scores?|"
    r"source\s+rank|source\s+order|visible\s+sort|visible\s+rank|resonance)"
)
ENGAGEMENT_CLAIM_GAP = r"[^.\n;]{0,80}"
NEGATED_OVERCLAIM_RE = re.compile(
    r"\b(?:no|not|never|without|cannot|can't|must\s+not|does\s+not|do\s+not|"
    r"don't|is\s+not|are\s+not|not\s+enough\s+to)\b",
    re.IGNORECASE,
)
ENGAGEMENT_OVERCLAIM_PATTERNS = {
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
    "engagement_gate_clearance_shortcut": re.compile(
        rf"(?:\b{ENGAGEMENT_SIGNAL_RE}\b{ENGAGEMENT_CLAIM_GAP}\b(?:clears?|passes?|satisfies|unlocks?|"
        rf"establishes|justifies?|means|counts\s+as)\b{ENGAGEMENT_CLAIM_GAP}\b(?:gate(?:\s+clearance)?|"
        rf"demand\s+gate|admissibility|candidate\s+clearance)\b|"
        rf"\b(?:gate(?:\s+clearance)?|demand\s+gate|admissibility|candidate\s+clearance)\b"
        rf"{ENGAGEMENT_CLAIM_GAP}\b(?:is|was|cleared|passed|satisfied|unlocked|established|justified|"
        rf"because\s+of|due\s+to|from|by|based\s+on)\b{ENGAGEMENT_CLAIM_GAP}\b{ENGAGEMENT_SIGNAL_RE}\b)",
        re.IGNORECASE,
    ),
    "engagement_route_binding_shortcut": re.compile(
        rf"(?:\b{ENGAGEMENT_SIGNAL_RE}\b{ENGAGEMENT_CLAIM_GAP}\b(?:binds?|sets?|selects?|authorizes?|clears?|"
        rf"recommends?|establishes)\b{ENGAGEMENT_CLAIM_GAP}\b(?:Capture\s+route|capture\s+method|"
        rf"route[_ -]?binding(?:[_ -]?state)?|source[- ]access\s+route|capture[- ]owned\s+route)\b|"
        rf"\b(?:Capture\s+route|capture\s+method|route[_ -]?binding(?:[_ -]?state)?|"
        rf"source[- ]access\s+route|capture[- ]owned\s+route)\b{ENGAGEMENT_CLAIM_GAP}\b(?:is|was|bound|set|"
        rf"selected|authorized|cleared|recommended|established|because\s+of|due\s+to|from|by|"
        rf"based\s+on)\b{ENGAGEMENT_CLAIM_GAP}\b{ENGAGEMENT_SIGNAL_RE}\b)",
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
    "engagement_credibility_shortcut": re.compile(
        rf"(?:\b{ENGAGEMENT_SIGNAL_RE}\b{ENGAGEMENT_CLAIM_GAP}\b(?:proves?|confirms?|establishes|"
        rf"supports?|justifies?|sets?|labels?|means|counts\s+as)\b{ENGAGEMENT_CLAIM_GAP}\b(?:credibility|credible|"
        rf"independence|trustworthy|trust)\b|"
        rf"\b(?:credibility|credible|independence|trustworthy|trust)\b"
        rf"{ENGAGEMENT_CLAIM_GAP}\b(?:is|was|proven|confirmed|established|supported|justified|set|labeled|"
        rf"because\s+of|due\s+to|from|by|based\s+on)\b{ENGAGEMENT_CLAIM_GAP}\b{ENGAGEMENT_SIGNAL_RE}\b)",
        re.IGNORECASE,
    ),
    "engagement_amplification_shortcut": re.compile(
        rf"(?:\b{ENGAGEMENT_SIGNAL_RE}\b{ENGAGEMENT_CLAIM_GAP}\b(?:proves?|confirms?|establishes|"
        rf"decides|labels?|sets?|means|counts\s+as)\b{ENGAGEMENT_CLAIM_GAP}\b(?:artificial\s+amplification|"
        rf"amplification|manipulation|bot(?:-like)?\s+activity)\b|"
        rf"\b(?:artificial\s+amplification|amplification|manipulation|bot(?:-like)?\s+activity)\b"
        rf"{ENGAGEMENT_CLAIM_GAP}\b(?:is|was|proven|confirmed|established|decided|labeled|set|because\s+of|"
        rf"due\s+to|from|by|based\s+on)\b{ENGAGEMENT_CLAIM_GAP}\b{ENGAGEMENT_SIGNAL_RE}\b)",
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
FORBIDDEN_TEXT_PATTERNS = {
    "recency_as_proof": re.compile(
        r"\b(recency|recent|currentness|current-state|current state)\b.{0,60}\b(proves|proof|gate clearance|clears? gate|demand verdict)\b",
        re.IGNORECASE,
    ),
    "scanning_binds_capture": re.compile(
        r"\b(scan|scanning)\b.{0,60}\b(bind|binds|sets|selects)\b.{0,40}\bCapture\b.{0,40}\b(route|method)\b",
        re.IGNORECASE,
    ),
    "capture_authorized_by_scan": re.compile(
        r"\bCapture\b.{0,40}\b(authorized|route-bound|route bound)\b.{0,40}\b(scan|scanning)\b",
        re.IGNORECASE,
    ),
}


@dataclass(frozen=True)
class Finding:
    code: str
    message: str


def _normalize_vocab(value: Any) -> str:
    if value is None:
        return ""
    return re.sub(r"[^a-z0-9]+", "_", str(value).strip().lower()).strip("_")


def _yaml_blocks(text: str) -> tuple[list[Any], list[Finding]]:
    blocks: list[Any] = []
    findings: list[Finding] = []
    for index, match in enumerate(YAML_FENCE_RE.finditer(text), start=1):
        try:
            blocks.append(yaml.safe_load(match.group("body")) or {})
        except yaml.YAMLError as exc:
            findings.append(Finding("invalid_yaml_fence", f"YAML fence {index} is invalid: {exc}"))
    return blocks, findings


def _find_intake(blocks: list[Any]) -> dict[str, Any] | None:
    for block in blocks:
        if not isinstance(block, dict):
            continue
        if "commission_id" in block:
            return block
    return None


def _as_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str) and re.fullmatch(r"\d+", value.strip()):
        return int(value.strip())
    return None


def _has_text(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return value.strip() != ""
    return True


def _is_url(value: Any) -> bool:
    return isinstance(value, str) and re.match(r"https?://", value.strip(), re.IGNORECASE) is not None


def _as_bool(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized == "true":
            return True
        if normalized == "false":
            return False
    return None


def _is_iso_date(value: Any) -> bool:
    if isinstance(value, date):
        return True
    if not isinstance(value, str):
        return False
    try:
        date.fromisoformat(value.strip())
    except ValueError:
        return False
    return True


def _iter_dict_records(value: Any, required_key: str) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        if required_key in value:
            yield value
        for child in value.values():
            yield from _iter_dict_records(child, required_key)
    elif isinstance(value, list):
        for child in value:
            yield from _iter_dict_records(child, required_key)


def _records(blocks: list[Any], required_key: str) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for block in blocks:
        records.extend(_iter_dict_records(block, required_key))
    return records


def _mapping_values(value: Any, key_name: str) -> Iterable[Any]:
    if isinstance(value, dict):
        for key, child in value.items():
            if _normalize_vocab(key) == key_name:
                yield child
            yield from _mapping_values(child, key_name)
    elif isinstance(value, list):
        for child in value:
            yield from _mapping_values(child, key_name)


def _section_body(text: str, pattern: re.Pattern[str]) -> str:
    match = pattern.search(text)
    if not match:
        return ""
    start = match.end()
    next_heading = HEADING_RE.search(text, start)
    end = next_heading.start() if next_heading else len(text)
    return text[start:end]


def _required_missing(record: dict[str, Any], required: set[str]) -> list[str]:
    return sorted(field for field in required if field not in record or not _has_text(record.get(field)))


def _validate_intake(intake: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []

    missing = sorted(REQUIRED_INTAKE_FIELDS - set(intake))
    if missing:
        findings.append(
            Finding("missing_intake_fields", "Scan intake receipt is missing fields: " + ", ".join(missing))
        )

    status = intake.get("source_context_status")
    if status != VALID_SOURCE_CONTEXT_STATUS:
        findings.append(
            Finding(
                "source_context_not_ready",
                f"source_context_status must be {VALID_SOURCE_CONTEXT_STATUS}, got {status or '<blank>'}.",
            )
        )

    closeout = _normalize_vocab(intake.get("closeout_state"))
    if closeout not in VALID_CLOSEOUT_STATES:
        findings.append(
            Finding(
                "invalid_closeout_state",
                "closeout_state must be one of "
                + ", ".join(sorted(VALID_CLOSEOUT_STATES))
                + f", got {intake.get('closeout_state')}.",
            )
        )

    run_caps = intake.get("run_caps")
    if not isinstance(run_caps, dict):
        findings.append(Finding("missing_run_caps", "run_caps must be a mapping."))
        return findings

    missing_caps = sorted(REQUIRED_RUN_CAPS - set(run_caps))
    if missing_caps:
        findings.append(Finding("missing_run_cap_fields", "run_caps is missing fields: " + ", ".join(missing_caps)))

    _validate_used_within_cap(
        findings,
        intake,
        run_caps,
        "screening_moves_used",
        "max_screening_moves_total",
        "screening_moves_exceed_cap",
    )
    _validate_used_within_cap(
        findings,
        intake,
        run_caps,
        "exact_queries_used",
        "max_exact_queries_total",
        "exact_queries_exceed_cap",
    )

    return findings


def _validate_used_within_cap(
    findings: list[Finding],
    intake: dict[str, Any],
    run_caps: dict[str, Any],
    used_field: str,
    cap_field: str,
    code: str,
) -> None:
    used = _as_int(intake.get(used_field))
    cap = _as_int(run_caps.get(cap_field))
    if used is None and used_field in intake:
        findings.append(Finding("invalid_numeric_field", f"{used_field} must be a non-negative integer."))
    if cap is None and cap_field in run_caps:
        findings.append(Finding("invalid_numeric_field", f"{cap_field} must be a non-negative integer."))
    if used is None or cap is None:
        return
    if used > cap:
        findings.append(Finding(code, f"{used_field}={used} exceeds {cap_field}={cap}."))


def _validate_required_receipt_parts(text: str, intake: dict[str, Any] | None = None) -> list[Finding]:
    findings: list[Finding] = []
    for name, pattern in SECTION_PATTERNS.items():
        if pattern.search(text):
            continue
        if name == "capture_request_accounting" and isinstance(intake, dict):
            if _as_int(intake.get("capture_requests")) == 0:
                continue
        findings.append(Finding(f"missing_{name}", f"Missing required CSB-first scan receipt part: {name}."))
    return findings


def _validate_broad_scout_detail(text: str) -> list[Finding]:
    if not SECTION_PATTERNS["broad_scout_accounting"].search(text):
        return []
    body = _section_body(text, SECTION_PATTERNS["broad_scout_accounting"])
    missing = sorted(name for name, pattern in BROAD_SCOUT_DETAIL_PATTERNS.items() if not pattern.search(body))
    if missing:
        return [Finding("missing_broad_scout_detail", "Broad Scout section is missing: " + ", ".join(missing))]
    return []


def _validate_csb_row_ids(text: str) -> list[Finding]:
    if SECTION_PATTERNS["csb_row_accounting"].search(text) and not CSB_ROW_ID_RE.search(text):
        return [Finding("missing_csb_row_ids", "CSB row accounting must cite at least one SBR-NNN row id.")]
    return []


def _validate_count_consistency(text: str, blocks: list[Any], intake: dict[str, Any] | None) -> list[Finding]:
    if not isinstance(intake, dict):
        return []
    findings: list[Finding] = []
    checks = [
        ("screening_moves_used", len(set(MOVE_ID_RE.findall(text))), "screening_moves_count_mismatch"),
        ("exact_queries_used", len(set(EXACT_QUERY_ID_RE.findall(text))), "exact_queries_count_mismatch"),
        ("hidden_venue_pointers", len(_records(blocks, "hidden_venue_pointer_id")), "hidden_venue_pointer_count_mismatch"),
        ("capture_requests", len(_records(blocks, "capture_request_id")), "capture_request_count_mismatch"),
    ]
    for field, observed, code in checks:
        declared = _as_int(intake.get(field))
        if declared is None:
            continue
        if declared != observed:
            findings.append(Finding(code, f"{field}={declared} but artifact records {observed}."))
    return findings


def _validate_observations(blocks: list[Any]) -> list[Finding]:
    observations = _records(blocks, "observation_id")
    if not observations:
        return [Finding("missing_observation_records", "Observations section must include at least one observation_id YAML record.")]

    findings: list[Finding] = []
    for observation in observations:
        obs_id = observation.get("observation_id", "<unknown>")
        missing = _required_missing(observation, REQUIRED_OBSERVATION_FIELDS)
        if missing:
            findings.append(Finding("missing_observation_fields", f"Observation {obs_id} is missing: {', '.join(missing)}."))
        if "url" in observation and not _is_url(observation.get("url")):
            findings.append(Finding("invalid_observation_url", f"Observation {obs_id} url must be http(s)."))
        if "retrieval_date" in observation and not _is_iso_date(observation.get("retrieval_date")):
            findings.append(Finding("invalid_observation_retrieval_date", f"Observation {obs_id} retrieval_date must be YYYY-MM-DD."))
        if "signal_stage" in observation:
            signal_stage = _normalize_vocab(observation.get("signal_stage"))
            if signal_stage not in VALID_SIGNAL_STAGES:
                findings.append(
                    Finding("invalid_signal_stage", f"Observation {obs_id} signal_stage must be one of {', '.join(sorted(VALID_SIGNAL_STAGES))}.")
                )
        if "gate_role" in observation:
            gate_role = _normalize_vocab(observation.get("gate_role"))
            if gate_role not in VALID_GATE_ROLES:
                findings.append(
                    Finding("invalid_gate_role", f"Observation {obs_id} gate_role must be one of {', '.join(sorted(VALID_GATE_ROLES))}.")
                )
    return findings


def _validate_candidate_observations(blocks: list[Any]) -> list[Finding]:
    findings: list[Finding] = []
    for candidate_obs in _records(blocks, "candidate_observation_id"):
        candidate_obs_id = candidate_obs.get("candidate_observation_id", "<unknown>")
        missing = _required_missing(candidate_obs, REQUIRED_CANDIDATE_OBSERVATION_FIELDS)
        if missing:
            findings.append(
                Finding(
                    "missing_candidate_observation_fields",
                    f"Candidate observation {candidate_obs_id} is missing: {', '.join(missing)}.",
                )
            )
        capture_needed = _normalize_vocab(candidate_obs.get("capture_needed"))
        if capture_needed and capture_needed not in {"yes", "no", "unknown"}:
            findings.append(
                Finding("invalid_capture_needed", f"Candidate observation {candidate_obs_id} capture_needed must be yes/no/unknown.")
            )
    return findings


def _validate_creator_registry_match_preflight(request_id: Any, request: dict[str, Any]) -> list[Finding]:
    preflight = request.get("creator_registry_match_preflight")
    if not isinstance(preflight, dict):
        return [
            Finding(
                "invalid_creator_registry_match_preflight",
                f"Capture request {request_id} creator_registry_match_preflight must be a mapping with required_when.",
            )
        ]

    findings: list[Finding] = []
    required_when = _normalize_vocab(preflight.get("required_when"))
    if required_when not in VALID_CREATOR_REGISTRY_REQUIRED_WHEN:
        findings.append(
            Finding(
                "invalid_creator_registry_match_preflight_required_when",
                "creator_registry_match_preflight.required_when must be new_social_creator_account_capture or not_applicable.",
            )
        )
        return findings

    if required_when == "not_applicable":
        disallowed = [
            field
            for field in ("intended_action", "decision", "action_status")
            if _normalize_vocab(preflight.get(field)) not in NOT_APPLICABLE_ALLOWED_PREFLIGHT_VOCAB
        ]
        if "receipt_path" in preflight and _normalize_vocab(
            preflight.get("receipt_path")
        ) not in PLACEHOLDER_PREFLIGHT_RECEIPT_VALUES:
            disallowed.append("receipt_path")
        can_start = preflight.get("can_start_new_capture")
        if _as_bool(can_start) is True or _normalize_vocab(can_start) not in (
            NOT_APPLICABLE_ALLOWED_PREFLIGHT_VOCAB | {"false"}
        ):
            disallowed.append("can_start_new_capture")
        if disallowed:
            findings.append(
                Finding(
                    "contradictory_creator_registry_match_preflight_not_applicable",
                    f"Capture request {request_id} creator_registry_match_preflight is not_applicable but also carries: {', '.join(disallowed)}.",
                )
            )
        return findings

    missing = _required_missing(preflight, REQUIRED_CREATOR_REGISTRY_PREFLIGHT_FIELDS)
    if missing:
        findings.append(
            Finding(
                "missing_creator_registry_match_preflight_fields",
                f"Capture request {request_id} creator_registry_match_preflight is missing: {', '.join(missing)}.",
            )
        )
        return findings

    receipt_path = preflight.get("receipt_path")
    if not isinstance(receipt_path, str) or _normalize_vocab(receipt_path) in PLACEHOLDER_PREFLIGHT_RECEIPT_VALUES:
        findings.append(
            Finding(
                "invalid_creator_registry_match_preflight_receipt_path",
                f"Capture request {request_id} must cite a concrete Creator Registry preflight receipt path.",
            )
        )

    intended_action = _normalize_vocab(preflight.get("intended_action"))
    decision = _normalize_vocab(preflight.get("decision"))
    action_status = _normalize_vocab(preflight.get("action_status"))
    can_start = _as_bool(preflight.get("can_start_new_capture"))

    if intended_action not in VALID_CREATOR_REGISTRY_INTENDED_ACTIONS:
        findings.append(Finding("invalid_creator_registry_preflight_intended_action", f"Capture request {request_id} has invalid intended_action."))
    if decision not in VALID_CREATOR_REGISTRY_DECISIONS:
        findings.append(Finding("invalid_creator_registry_preflight_decision", f"Capture request {request_id} has invalid decision."))
    if action_status not in VALID_CREATOR_REGISTRY_ACTION_STATUSES:
        findings.append(Finding("invalid_creator_registry_preflight_action_status", f"Capture request {request_id} has invalid action_status."))
    if intended_action != "new_capture" or decision != "new_candidate" or action_status != "allowed" or can_start is not True:
        findings.append(
            Finding(
                "creator_registry_preflight_does_not_clear_new_capture",
                f"Capture request {request_id} new social creator/account capture requires intended_action=new_capture, decision=new_candidate, action_status=allowed, and can_start_new_capture=true.",
            )
        )
    return findings


def _validate_capture_requests(blocks: list[Any]) -> list[Finding]:
    findings: list[Finding] = []
    for request in _records(blocks, "capture_request_id"):
        request_id = request.get("capture_request_id", "<unknown>")
        missing = _required_missing(request, REQUIRED_CAPTURE_REQUEST_FIELDS)
        if missing:
            findings.append(Finding("missing_capture_request_fields", f"Capture request {request_id} is missing: {', '.join(missing)}."))

        if "creator_registry_match_preflight" in request:
            findings.extend(_validate_creator_registry_match_preflight(request_id, request))

        route_state = _normalize_vocab(request.get("route_binding_state"))
        if route_state not in VALID_ROUTE_BINDING_STATES:
            findings.append(
                Finding(
                    "invalid_capture_route_binding_state",
                    f"Capture request {request_id} route_binding_state must be one of {', '.join(sorted(VALID_ROUTE_BINDING_STATES))}.",
                )
            )

        urls = request.get("urls")
        if not isinstance(urls, list) or not urls:
            findings.append(Finding("invalid_capture_request_urls", f"Capture request {request_id} urls must be a non-empty list."))
        else:
            for index, entry in enumerate(urls, start=1):
                if not isinstance(entry, dict):
                    findings.append(
                        Finding("invalid_capture_request_urls", f"Capture request {request_id} url entry {index} must be a mapping.")
                    )
                    continue
                missing_url_fields = _required_missing(entry, REQUIRED_CAPTURE_URL_FIELDS)
                if missing_url_fields:
                    findings.append(
                        Finding(
                            "missing_capture_request_url_fields",
                            f"Capture request {request_id} url entry {index} is missing: {', '.join(missing_url_fields)}.",
                        )
                    )
                if "url" in entry and not _is_url(entry.get("url")):
                    findings.append(Finding("invalid_capture_request_url", f"Capture request {request_id} url entry {index} must be http(s)."))
                gate_role = _normalize_vocab(entry.get("gate_role"))
                if gate_role and gate_role not in VALID_GATE_ROLES:
                    findings.append(Finding("invalid_gate_role", f"Capture request {request_id} url entry {index} has invalid gate_role."))

        not_requested = request.get("not_requested")
        if isinstance(not_requested, list):
            normalized = {_normalize_vocab(item) for item in not_requested}
            missing_not_requested = sorted(REQUIRED_NOT_REQUESTED - normalized)
            if missing_not_requested:
                findings.append(
                    Finding(
                        "missing_capture_request_not_requested_boundaries",
                        f"Capture request {request_id} not_requested is missing: {', '.join(missing_not_requested)}.",
                    )
                )
        elif "not_requested" in request:
            findings.append(Finding("invalid_capture_request_not_requested", f"Capture request {request_id} not_requested must be a list."))
    return findings


def _validate_closeout(text: str, blocks: list[Any], intake: dict[str, Any] | None) -> list[Finding]:
    if not isinstance(intake, dict):
        return []
    findings: list[Finding] = []
    closeout = _normalize_vocab(intake.get("closeout_state"))
    candidate_observations = _records(blocks, "candidate_observation_id")
    capture_request_count = len(_records(blocks, "capture_request_id"))

    body = _section_body(text, SECTION_PATTERNS["closeout"])
    if closeout and closeout not in _normalize_vocab(body):
        findings.append(Finding("closeout_state_not_in_closeout_section", "Closeout section must repeat the intake closeout_state."))

    for decision in _mapping_values(blocks, "candidate_decision"):
        if isinstance(decision, dict) and "closeout_state" in decision:
            decision_closeout = _normalize_vocab(decision.get("closeout_state"))
            if closeout and decision_closeout != closeout:
                findings.append(Finding("candidate_decision_closeout_mismatch", "candidate_decision.closeout_state must match intake closeout_state."))

    if closeout == "candidate_ready_for_next_lane" and not candidate_observations:
        findings.append(
            Finding("candidate_ready_without_candidate_observation", "candidate_ready_for_next_lane requires a candidate_observation_id record.")
        )
    if closeout == "no_candidate_after_discovery" and candidate_observations:
        findings.append(Finding("no_candidate_with_candidate_observation", "no_candidate_after_discovery must not include candidate_observation_id records."))
    if closeout == "capture_preservation_only" and capture_request_count == 0:
        findings.append(Finding("preservation_without_capture_request", "capture_preservation_only requires at least one capture_request_id record."))
    if closeout == "capture_preservation_only" and candidate_observations:
        findings.append(Finding("preservation_with_candidate_observation", "capture_preservation_only must not include candidate_observation_id records."))
    return findings


def _iter_yaml_items(value: Any, path: str = ""):
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else str(key)
            yield child_path, key, child
            yield from _iter_yaml_items(child, child_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            child_path = f"{path}[{index}]"
            yield child_path, index, child
            yield from _iter_yaml_items(child, child_path)


def _validate_yaml_overclaims(blocks: list[Any]) -> list[Finding]:
    findings: list[Finding] = []
    for block in blocks:
        for path, key, value in _iter_yaml_items(block):
            key_norm = _normalize_vocab(key)
            value_norm = _normalize_vocab(value)
            if key_norm in {"recency_status", "recency_attention", "signal_stage"} and value_norm in {
                "proof",
                "demand_proof",
                "gate_clearance",
                "candidate_authorization",
            }:
                findings.append(Finding("invalid_signal_stage_overclaim", f"{path} must not use {value!r}."))
    return findings


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
    for code, pattern in ENGAGEMENT_OVERCLAIM_PATTERNS.items():
        position = 0
        while True:
            match = pattern.search(text, position)
            if match is None:
                break
            position = match.start() + 1
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

def _validate_forbidden_text(text: str) -> list[Finding]:
    findings: list[Finding] = []
    for code, pattern in FORBIDDEN_TEXT_PATTERNS.items():
        match = pattern.search(text)
        if match:
            excerpt = " ".join(match.group(0).split())
            findings.append(Finding(code, f"Forbidden overclaim language found: {excerpt!r}."))
    return findings


def validate_text(text: str) -> list[Finding]:
    blocks, yaml_findings = _yaml_blocks(text)
    findings = [*yaml_findings]
    intake = _find_intake(blocks)
    if intake is None:
        findings.append(
            Finding(
                "missing_scan_intake_receipt",
                "No YAML scan intake receipt with commission_id and source_context_status found.",
            )
        )
    else:
        findings.extend(_validate_intake(intake))

    findings.extend(_validate_required_receipt_parts(text, intake))
    findings.extend(_validate_broad_scout_detail(text))
    findings.extend(_validate_csb_row_ids(text))
    findings.extend(_validate_count_consistency(text, blocks, intake))
    findings.extend(_validate_observations(blocks))
    findings.extend(_validate_candidate_observations(blocks))
    findings.extend(_validate_capture_requests(blocks))
    findings.extend(_validate_closeout(text, blocks, intake))
    findings.extend(_validate_yaml_overclaims(blocks))
    findings.extend(_validate_engagement_overclaims(text))
    findings.extend(_validate_forbidden_text(text))
    return findings


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]



def _git_lines(root: Path, args: list[str]) -> list[str] | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *args],
            capture_output=True,
            text=True,
            timeout=15,
        )
    except (FileNotFoundError, OSError, subprocess.TimeoutExpired):
        return None
    if result.returncode != 0:
        return None
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def _dedupe(values: Iterable[str]) -> list[str]:
    seen: list[str] = []
    for value in values:
        if value not in seen:
            seen.append(value)
    return seen


def changed_paths(root: Path) -> list[str]:
    paths: list[str] = []
    for args in (
        ["diff", "--name-only", "--diff-filter=ACMR"],
        ["diff", "--cached", "--name-only", "--diff-filter=ACMR"],
        ["ls-files", "--others", "--exclude-standard"],
    ):
        lines = _git_lines(root, args)
        if lines:
            paths.extend(lines)
    return _dedupe(paths)


def resolve_base_ref(cli_base: str | None) -> str:
    github_base = os.environ.get("GITHUB_BASE_REF", "").strip()
    if github_base:
        return f"origin/{github_base}"
    if cli_base:
        return cli_base
    return "origin/main"


def diff_paths(root: Path, base_ref: str) -> list[str] | None:
    lines = _git_lines(root, ["diff", "--name-only", "--diff-filter=ACMR", f"{base_ref}...HEAD"])
    if lines is not None:
        return lines
    return _git_lines(root, ["diff", "--name-only", "--diff-filter=ACMR", base_ref, "HEAD"])


def looks_like_csb_first_scan_artifact(relposix: str, text: str) -> bool:
    if not relposix.endswith(".md"):
        return False
    if not any(relposix.startswith(prefix) for prefix in AUTO_SCAN_PREFIXES):
        return False
    lower = text.lower()
    return all(marker in lower for marker in AUTO_SCAN_REQUIRED_MARKERS) and any(
        marker in lower for marker in AUTO_SCAN_ROUTE_MARKERS
    )


def auto_targets(root: Path, relpaths: Iterable[str]) -> list[Path]:
    targets: list[Path] = []
    for rel in _dedupe(relpaths):
        path = root / rel
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if looks_like_csb_first_scan_artifact(rel, text):
            targets.append(path)
    return targets


def validate_paths(paths: Iterable[Path]) -> int:
    exit_code = 0
    for path in paths:
        findings = validate_text(path.read_text(encoding="utf-8"))
        if findings:
            exit_code = 1
            print(f"FAIL {path}")
            for finding in findings:
                print(f"  {finding.code}: {finding.message}")
        else:
            print(f"PASS {path}")
    return exit_code


def _expected_from_fixture(path: Path) -> str:
    first_line = path.read_text(encoding="utf-8").splitlines()[0]
    match = re.search(r"fixture_expected:\s*(pass|fail)", first_line)
    if not match:
        return ""
    return match.group(1)


def selftest() -> int:
    root = Path(__file__).resolve().parents[2]
    fixture_dir = root / "orca-harness" / "tests" / "fixtures" / "csb_scanning_artifacts"
    fixture_paths = sorted(fixture_dir.glob("*.md"))
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
    parser = argparse.ArgumentParser(
        description="Validate CSB-first scanning artifact receipt shape."
    )
    parser.add_argument("paths", nargs="*", help="explicit scan artifact paths")
    parser.add_argument("--changed", action="store_true", help="auto-check changed CSB-first docs/research scan artifacts")
    parser.add_argument("--diff", metavar="BASE", help="auto-check CSB-first docs/research scan artifacts changed in BASE...HEAD")
    parser.add_argument("--strict", action="store_true", help="accepted for CI readability; findings already exit 1")
    parser.add_argument("--selftest", action="store_true", help="run fixture selftest")
    args = parser.parse_args(argv)

    if args.selftest:
        return selftest()

    root = repo_root()
    explicit_paths = [Path(path) for path in args.paths]
    auto_relpaths: list[str] = []

    if args.changed:
        auto_relpaths.extend(changed_paths(root))
    if args.diff:
        base = resolve_base_ref(args.diff)
        diff_relpaths = diff_paths(root, base)
        if diff_relpaths is None:
            print(
                f"check_csb_scanning_artifact: diff-scoping unavailable for {base}; failing open.",
                file=sys.stderr,
            )
            diff_relpaths = []
        auto_relpaths.extend(diff_relpaths)

    paths = explicit_paths + auto_targets(root, auto_relpaths)
    paths = [Path(path) for path in _dedupe(str(path) for path in paths)]

    if not paths:
        if args.changed or args.diff:
            print("check_csb_scanning_artifact: no changed CSB-first scan artifacts detected")
            return 0
        print(
            "usage: check_csb_scanning_artifact.py [--selftest] [--changed] [--diff BASE] <scan-artifact> [...]",
            file=sys.stderr,
        )
        return 2

    return validate_paths(paths)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
