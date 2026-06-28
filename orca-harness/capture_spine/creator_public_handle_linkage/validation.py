from __future__ import annotations

import json
import re
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from capture_spine.creator_public_handle_linkage.models import (
    CREATOR_PUBLIC_HANDLE_LINKAGE_LEDGER_SCHEMA_VERSION,
    DEFAULT_LINKAGE_NON_CLAIMS,
    PUBLIC_HANDLE_LEDGER_MODE,
    SYNTHETIC_FIXTURE_MODE,
    CreatorPublicHandleLinkageError,
    EvidenceStrength,
    EvidenceType,
    LinkState,
    Platform,
    ReviewState,
)


_WRAPPER_KEY = "creator_public_handle_linkage_ledger"

_ALLOWED_TOP_LEVEL_KEYS = frozenset({_WRAPPER_KEY})
_ALLOWED_WRAPPER_KEYS = frozenset(
    {
        "schema_version",
        "ledger_id",
        "ledger_mode",
        "authority_pointers",
        "source_policy_posture",
        "creator_records",
        "platform_accounts",
        "account_link_evidence",
        "non_claims",
    }
)
_ALLOWED_CREATOR_RECORD_KEYS = frozenset(
    {
        "creator_record_id",
        "link_state",
        "platform_account_ids",
        "evidence_ids",
        "review_state",
        "link_rationale",
        "limitations",
        "created_at",
        "updated_at",
        "non_claims",
    }
)
_ALLOWED_ACCOUNT_KEYS = frozenset(
    {
        "platform_account_id",
        "platform",
        "platform_public_account_id_or_none",
        "public_handle",
        "public_profile_url",
        "handle_source_pointer",
        "handle_observed_at",
        "public_display_name_or_none",
        "display_name_source_pointer_or_none",
        "display_name_source_field_or_none",
        "synthetic_fixture",
    }
)
_ALLOWED_EVIDENCE_KEYS = frozenset(
    {
        "evidence_id",
        "evidence_type",
        "evidence_strength",
        "account_ids",
        "source_pointer",
        "source_field",
        "observed_at",
        "review_actor",
        "llm_assisted",
        "independence_key",
        "notes",
    }
)

_ALLOWED_LEDGER_MODES = frozenset({SYNTHETIC_FIXTURE_MODE, PUBLIC_HANDLE_LEDGER_MODE})
_ALLOWED_PLATFORMS = frozenset(platform.value for platform in Platform)
_ALLOWED_LINK_STATES = frozenset(state.value for state in LinkState)
_ALLOWED_REVIEW_STATES = frozenset(state.value for state in ReviewState)
_ALLOWED_EVIDENCE_TYPES = frozenset(evidence_type.value for evidence_type in EvidenceType)
_ALLOWED_EVIDENCE_STRENGTHS = frozenset(strength.value for strength in EvidenceStrength)

_STRONG_EVIDENCE_TYPES = frozenset(
    {
        EvidenceType.SELF_DECLARED_CROSS_LINK.value,
        EvidenceType.MUTUAL_PROFILE_LINK.value,
        EvidenceType.OFFICIAL_LINK_HUB.value,
    }
)
_WEAK_EVIDENCE_TYPES = frozenset(
    {
        EvidenceType.HANDLE_SIMILARITY.value,
        EvidenceType.PUBLIC_DISPLAY_NAME_SIMILARITY.value,
        EvidenceType.BIO_TEXT_OVERLAP.value,
        EvidenceType.SHARED_PUBLIC_LINK_DESTINATION.value,
        EvidenceType.CONTENT_TOPIC_OVERLAP.value,
    }
)
_DISCONFIRMING_EVIDENCE_TYPES = frozenset(
    {
        EvidenceType.CONFLICTING_SELF_DECLARATION.value,
        EvidenceType.CONFLICTING_PUBLIC_LINK_HUB.value,
        EvidenceType.DIFFERENT_PUBLIC_ENTITY_SIGNAL.value,
        EvidenceType.OPERATOR_REJECTED_MATCH.value,
    }
)

_FORBIDDEN_OUTPUT_FIELDS = {
    "legal_name",
    "real_name",
    "inferred_real_name",
    "birth_name",
    "email",
    "emails",
    "email_address",
    "phone",
    "phone_number",
    "contact",
    "contacts",
    "contact_info",
    "contact_details",
    "contact_route",
    "dm_route",
    "outreach",
    "lead",
    "lead_list",
    "address",
    "home_city",
    "location",
    "age",
    "gender",
    "ethnicity",
    "health",
    "religion",
    "politics",
    "sexuality",
    "family_status",
    "private_handle",
    "non_public_handle",
    "follower_list",
    "followers",
    "follower_graph",
    "audience_graph",
    "commenter_graph",
    "relationship_graph",
    "raw_html",
    "html",
    "rendered_dom",
    "dom",
    "parser_output",
    "screenshot",
    "screenshot_path",
    "cookie",
    "cookies",
    "session",
    "session_state",
    "hidden_session_state",
    "authorization_header",
    "confirmed_public_account_link",
}

_FORBIDDEN_OUTPUT_VALUE_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("pem_private_key", re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----")),
    ("bearer_token", re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=\-]{16,}")),
    ("credentialed_url_userinfo", re.compile(r"://[^/\s:@]+:[^/\s:@]+@")),
    ("email_address", re.compile(r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b")),
    ("phone_url", re.compile(r"(?i)\btel:\+?[0-9][0-9 .()\-]{6,}")),
)

_PUBLIC_HANDLE_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{1,63}$")


def load_creator_public_handle_linkage_ledger(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        _fail("invalid_json_fixture", "creator public-handle linkage ledger must be a JSON object")
    validate_creator_public_handle_linkage_ledger(value)
    return value


def validate_creator_public_handle_linkage_ledger(ledger: Mapping[str, Any]) -> None:
    assert_no_forbidden_output_fields(ledger)
    _reject_unknown_keys(ledger, _ALLOWED_TOP_LEVEL_KEYS, "ledger top-level")
    wrapper = ledger.get(_WRAPPER_KEY)
    if not isinstance(wrapper, Mapping):
        _fail("missing_ledger_wrapper", f"{_WRAPPER_KEY} wrapper is required")
    _reject_unknown_keys(wrapper, _ALLOWED_WRAPPER_KEYS, "ledger")
    _require(
        wrapper,
        (
            "schema_version",
            "ledger_id",
            "ledger_mode",
            "authority_pointers",
            "source_policy_posture",
            "creator_records",
            "platform_accounts",
            "account_link_evidence",
            "non_claims",
        ),
        "ledger",
    )
    _require_str(
        wrapper,
        ("schema_version", "ledger_id", "ledger_mode", "source_policy_posture"),
        "ledger",
    )
    if wrapper.get("schema_version") != CREATOR_PUBLIC_HANDLE_LINKAGE_LEDGER_SCHEMA_VERSION:
        _fail(
            "invalid_schema_version",
            "schema_version must be "
            f"{CREATOR_PUBLIC_HANDLE_LINKAGE_LEDGER_SCHEMA_VERSION}",
        )
    ledger_mode = str(wrapper["ledger_mode"])
    if ledger_mode not in _ALLOWED_LEDGER_MODES:
        _fail("invalid_ledger_mode", f"ledger_mode must be one of {sorted(_ALLOWED_LEDGER_MODES)}")
    _validate_authority_pointers(wrapper["authority_pointers"])
    _validate_non_claims(wrapper["non_claims"], "ledger")

    accounts = _validate_platform_accounts(wrapper["platform_accounts"], ledger_mode)
    evidence = _validate_link_evidence(wrapper["account_link_evidence"], accounts, ledger_mode)
    _validate_creator_records(wrapper["creator_records"], accounts, evidence)


def assert_no_forbidden_output_fields(value: Any, *, path: str = "$") -> None:
    if isinstance(value, Mapping):
        for key, child in value.items():
            key_name = str(key)
            lowered = key_name.lower()
            if lowered in _FORBIDDEN_OUTPUT_FIELDS:
                _fail("forbidden_output_field", f"forbidden output field at {path}.{key_name}")
            assert_no_forbidden_output_fields(child, path=f"{path}.{key_name}")
        return
    if _is_list(value):
        for index, child in enumerate(value):
            assert_no_forbidden_output_fields(child, path=f"{path}[{index}]")
        return
    if isinstance(value, str):
        _assert_no_forbidden_output_value(value, path=path)


def _validate_authority_pointers(value: Any) -> None:
    if not _is_list(value) or not value:
        _fail("missing_authority_pointers", "ledger authority_pointers must be a non-empty list")
    if "docs/decisions/wind_caller_calibration_carveout_v0.md" not in set(value):
        _fail(
            "missing_wind_caller_authority_pointer",
            "ledger must point to wind_caller_calibration_carveout_v0.md",
        )
    for pointer in value:
        if not isinstance(pointer, str) or not pointer.strip():
            _fail("invalid_authority_pointer", "authority_pointers entries must be non-empty strings")


def _validate_platform_accounts(value: Any, ledger_mode: str) -> dict[str, Mapping[str, Any]]:
    if not _is_list(value):
        _fail("invalid_platform_accounts", "platform_accounts must be a list")
    accounts: dict[str, Mapping[str, Any]] = {}
    for account in value:
        if not isinstance(account, Mapping):
            _fail("invalid_platform_account", "platform account entries must be mappings")
        _reject_unknown_keys(account, _ALLOWED_ACCOUNT_KEYS, "platform_account")
        _require_str(
            account,
            (
                "platform_account_id",
                "platform",
                "public_handle",
                "public_profile_url",
                "handle_source_pointer",
                "handle_observed_at",
            ),
            "platform_account",
        )
        _validate_optional_str(
            account,
            (
                "platform_public_account_id_or_none",
                "public_display_name_or_none",
                "display_name_source_pointer_or_none",
                "display_name_source_field_or_none",
            ),
            "platform_account",
        )
        account_id = str(account["platform_account_id"])
        if account_id in accounts:
            _fail("duplicate_platform_account_id", f"duplicate platform_account_id: {account_id}")
        if account["platform"] not in _ALLOWED_PLATFORMS:
            _fail("invalid_platform", f"platform must be one of {sorted(_ALLOWED_PLATFORMS)}")
        handle = str(account["public_handle"])
        if not _PUBLIC_HANDLE_RE.fullmatch(handle):
            _fail("invalid_public_handle", "public_handle must be a normalized public handle without @")
        _validate_https_url(account["public_profile_url"], "public_profile_url")

        display_name = account.get("public_display_name_or_none")
        if display_name is not None:
            _require_str(
                account,
                (
                    "public_display_name_or_none",
                    "display_name_source_pointer_or_none",
                    "display_name_source_field_or_none",
                ),
                "platform_account public display name",
            )
        if ledger_mode == SYNTHETIC_FIXTURE_MODE:
            _validate_synthetic_account(account)
        accounts[account_id] = account
    return accounts


def _validate_link_evidence(
    value: Any,
    accounts: Mapping[str, Mapping[str, Any]],
    ledger_mode: str,
) -> dict[str, Mapping[str, Any]]:
    if not _is_list(value):
        _fail("invalid_account_link_evidence", "account_link_evidence must be a list")
    evidence: dict[str, Mapping[str, Any]] = {}
    for record in value:
        if not isinstance(record, Mapping):
            _fail("invalid_evidence_record", "account_link_evidence entries must be mappings")
        _reject_unknown_keys(record, _ALLOWED_EVIDENCE_KEYS, "account_link_evidence")
        _require(
            record,
            (
                "evidence_id",
                "evidence_type",
                "evidence_strength",
                "account_ids",
                "source_pointer",
                "source_field",
                "observed_at",
                "review_actor",
                "llm_assisted",
                "independence_key",
            ),
            "account_link_evidence",
        )
        _require_str(
            record,
            (
                "evidence_id",
                "evidence_type",
                "evidence_strength",
                "source_pointer",
                "source_field",
                "observed_at",
                "review_actor",
                "independence_key",
            ),
            "account_link_evidence",
        )
        evidence_id = str(record["evidence_id"])
        if evidence_id in evidence:
            _fail("duplicate_evidence_id", f"duplicate evidence_id: {evidence_id}")
        evidence_type = str(record["evidence_type"])
        evidence_strength = str(record["evidence_strength"])
        if evidence_type not in _ALLOWED_EVIDENCE_TYPES:
            _fail("invalid_evidence_type", f"evidence_type is not allowed: {evidence_type}")
        if evidence_strength not in _ALLOWED_EVIDENCE_STRENGTHS:
            _fail("invalid_evidence_strength", f"evidence_strength is not allowed: {evidence_strength}")
        _validate_evidence_strength_matches_type(evidence_type, evidence_strength)
        _validate_account_id_list(record["account_ids"], accounts, "account_link_evidence.account_ids")
        if not isinstance(record.get("llm_assisted"), bool):
            _fail("invalid_llm_assisted", "llm_assisted must be a boolean")
        if ledger_mode == SYNTHETIC_FIXTURE_MODE:
            _validate_synthetic_source_pointer(record["source_pointer"], "evidence source_pointer")
        evidence[evidence_id] = record
    return evidence


def _validate_creator_records(
    value: Any,
    accounts: Mapping[str, Mapping[str, Any]],
    evidence: Mapping[str, Mapping[str, Any]],
) -> None:
    if not _is_list(value):
        _fail("invalid_creator_records", "creator_records must be a list")
    creator_ids: set[str] = set()
    for record in value:
        if not isinstance(record, Mapping):
            _fail("invalid_creator_record", "creator_records entries must be mappings")
        _reject_unknown_keys(record, _ALLOWED_CREATOR_RECORD_KEYS, "creator_record")
        _require(
            record,
            (
                "creator_record_id",
                "link_state",
                "platform_account_ids",
                "evidence_ids",
                "review_state",
                "link_rationale",
                "limitations",
                "created_at",
                "updated_at",
                "non_claims",
            ),
            "creator_record",
        )
        _require_str(
            record,
            (
                "creator_record_id",
                "link_state",
                "review_state",
                "link_rationale",
                "limitations",
                "created_at",
                "updated_at",
            ),
            "creator_record",
        )
        creator_id = str(record["creator_record_id"])
        if creator_id in creator_ids:
            _fail("duplicate_creator_record_id", f"duplicate creator_record_id: {creator_id}")
        creator_ids.add(creator_id)
        if record["link_state"] == "confirmed_public_account_link":
            _fail("confirmed_link_state_forbidden", "use declared/probable/candidate/rejected, not confirmed")
        if record["link_state"] not in _ALLOWED_LINK_STATES:
            _fail("invalid_link_state", f"link_state must be one of {sorted(_ALLOWED_LINK_STATES)}")
        if record["review_state"] not in _ALLOWED_REVIEW_STATES:
            _fail("invalid_review_state", f"review_state must be one of {sorted(_ALLOWED_REVIEW_STATES)}")
        _validate_non_claims(record["non_claims"], "creator_record")
        account_ids = _validate_account_id_list(record["platform_account_ids"], accounts, "creator_record")
        platforms = {str(accounts[account_id]["platform"]) for account_id in account_ids}
        if len(platforms) < 2:
            _fail("single_platform_creator_record", "creator_record must link accounts across at least two platforms")
        evidence_rows = _evidence_rows(record["evidence_ids"], evidence)
        _validate_evidence_refs_stay_inside_creator_accounts(evidence_rows, set(account_ids))
        _validate_link_state_evidence(record, evidence_rows)


def _validate_link_state_evidence(
    record: Mapping[str, Any],
    evidence_rows: Sequence[Mapping[str, Any]],
) -> None:
    link_state = record["link_state"]
    review_state = record["review_state"]
    strengths = [str(row["evidence_strength"]) for row in evidence_rows]
    evidence_types = [str(row["evidence_type"]) for row in evidence_rows]
    disconfirming = [row for row in evidence_rows if row["evidence_strength"] == EvidenceStrength.DISCONFIRMING.value]

    if link_state in {LinkState.DECLARED.value, LinkState.PROBABLE.value}:
        if disconfirming:
            _fail("disconfirming_evidence_blocks_final_link", "final link states cannot include disconfirming evidence")
        _validate_not_llm_only_final_link(evidence_rows)
    if link_state == LinkState.DECLARED.value:
        if review_state != ReviewState.HUMAN_REVIEWED_DECLARED.value:
            _fail("declared_link_requires_human_review", "declared links require human_reviewed_declared")
        if EvidenceStrength.STRONG.value not in strengths:
            _fail("declared_link_missing_strong_evidence", "declared links require at least one strong evidence row")
    elif link_state == LinkState.PROBABLE.value:
        if review_state != ReviewState.HUMAN_REVIEWED_PROBABLE.value:
            _fail("probable_link_requires_human_review", "probable links require human_reviewed_probable")
        weak_rows = [row for row in evidence_rows if str(row["evidence_type"]) in _WEAK_EVIDENCE_TYPES]
        weak_types = {str(row["evidence_type"]) for row in weak_rows}
        if len(weak_types) < 3:
            _fail(
                "probable_link_needs_three_independent_weak_evidence_types",
                "probable links require at least three independent weak evidence types",
            )
        weak_independence_keys = {str(row["independence_key"]) for row in weak_rows}
        if len(weak_independence_keys) < 3:
            _fail(
                "probable_link_needs_three_independent_evidence_families",
                "probable links require at least three independent weak evidence families "
                "(distinct independence_key)",
            )
    elif link_state == LinkState.CANDIDATE.value:
        if review_state != ReviewState.CANDIDATE_NEEDS_REVIEW.value:
            _fail("candidate_link_review_state_mismatch", "candidate links require candidate_needs_review")
    elif link_state == LinkState.REJECTED.value:
        if review_state != ReviewState.OPERATOR_REJECTED.value:
            _fail("rejected_link_review_state_mismatch", "rejected links require operator_rejected")
        if not disconfirming:
            _fail("rejected_link_missing_disconfirming_evidence", "rejected links require disconfirming evidence")


def _validate_not_llm_only_final_link(evidence_rows: Sequence[Mapping[str, Any]]) -> None:
    if all(row.get("llm_assisted") is True for row in evidence_rows):
        _fail("llm_only_final_link", "LLM-assisted evidence alone cannot finalize a public-handle link")
    for row in evidence_rows:
        actor = str(row.get("review_actor", "")).strip().lower()
        if actor in {"llm", "llm_only", "model", "model_only"}:
            _fail("llm_only_final_link", "final public-handle links require a non-LLM review actor")


def _validate_evidence_refs_stay_inside_creator_accounts(
    evidence_rows: Sequence[Mapping[str, Any]],
    account_ids: set[str],
) -> None:
    for row in evidence_rows:
        row_account_ids = set(str(account_id) for account_id in row["account_ids"])
        if not row_account_ids.issubset(account_ids):
            _fail(
                "evidence_points_outside_creator_record",
                "creator_record evidence_ids must not point outside platform_account_ids",
            )


def _evidence_rows(
    value: Any,
    evidence: Mapping[str, Mapping[str, Any]],
) -> list[Mapping[str, Any]]:
    if not _is_list(value) or not value:
        _fail("invalid_evidence_ids", "creator_record.evidence_ids must be a non-empty list")
    evidence_ids = [str(item) for item in value]
    if len(set(evidence_ids)) != len(evidence_ids):
        _fail("duplicate_evidence_ref", "creator_record.evidence_ids must be unique")
    rows = []
    for evidence_id in evidence_ids:
        if evidence_id not in evidence:
            _fail("unknown_evidence_ref", f"unknown evidence_id reference: {evidence_id}")
        rows.append(evidence[evidence_id])
    return rows


def _validate_account_id_list(
    value: Any,
    accounts: Mapping[str, Mapping[str, Any]],
    label: str,
) -> list[str]:
    if not _is_list(value) or len(value) < 2:
        _fail("invalid_account_id_list", f"{label} must list at least two account ids")
    account_ids = [str(item) for item in value]
    if len(set(account_ids)) != len(account_ids):
        _fail("duplicate_account_ref", f"{label} account ids must be unique")
    missing = sorted(account_id for account_id in account_ids if account_id not in accounts)
    if missing:
        _fail("unknown_account_ref", f"{label} references unknown platform_account_id(s): {missing}")
    return account_ids


def _validate_evidence_strength_matches_type(evidence_type: str, evidence_strength: str) -> None:
    if evidence_type in _STRONG_EVIDENCE_TYPES and evidence_strength != EvidenceStrength.STRONG.value:
        _fail("evidence_strength_mismatch", "strong evidence_type must have evidence_strength=strong")
    if evidence_type in _WEAK_EVIDENCE_TYPES and evidence_strength != EvidenceStrength.WEAK.value:
        _fail("evidence_strength_mismatch", "weak evidence_type must have evidence_strength=weak")
    if evidence_type in _DISCONFIRMING_EVIDENCE_TYPES and evidence_strength != EvidenceStrength.DISCONFIRMING.value:
        _fail(
            "evidence_strength_mismatch",
            "disconfirming evidence_type must have evidence_strength=disconfirming",
        )


def _validate_synthetic_account(account: Mapping[str, Any]) -> None:
    if account.get("synthetic_fixture") is not True:
        _fail("synthetic_fixture_marker_required", "synthetic_fixture ledgers require synthetic_fixture=true")
    handle = str(account["public_handle"])
    if not handle.startswith(("synthetic_", "fixture_")):
        _fail("synthetic_fixture_handle_required", "synthetic fixture handles must start synthetic_ or fixture_")
    host = (urlparse(str(account["public_profile_url"])).hostname or "").lower()
    if host != "example.test" and not host.endswith(".example.test"):
        _fail("synthetic_fixture_url_required", "synthetic fixture profile URLs must use the example.test host")
    _validate_synthetic_source_pointer(account["handle_source_pointer"], "handle_source_pointer")
    display_name = account.get("public_display_name_or_none")
    if display_name:
        _validate_synthetic_source_pointer(
            account.get("display_name_source_pointer_or_none"),
            "display_name_source_pointer_or_none",
        )


def _validate_synthetic_source_pointer(value: Any, label: str) -> None:
    if not isinstance(value, str) or not value.startswith("synthetic_fixture:"):
        _fail("synthetic_fixture_source_required", f"{label} must start with synthetic_fixture:")


def _validate_non_claims(value: Any, label: str) -> None:
    if not _is_list(value):
        _fail("missing_non_claims", f"{label} requires non_claims")
    claims = {str(item) for item in value}
    missing = sorted(set(DEFAULT_LINKAGE_NON_CLAIMS).difference(claims))
    if missing:
        _fail("missing_required_non_claim", f"{label} missing non-claims: {missing}")


def _reject_unknown_keys(value_map: Mapping[str, Any], allowed_keys: frozenset[str], label: str) -> None:
    unknown = sorted(str(key) for key in value_map if str(key) not in allowed_keys)
    if unknown:
        _fail("unknown_field", f"{label} contains unknown field(s): {unknown}")


def _require(value_map: Mapping[str, Any], field_names: Sequence[str], label: str) -> None:
    for field_name in field_names:
        value = value_map.get(field_name)
        if value is None or (isinstance(value, str) and not value.strip()):
            _fail(f"missing_{field_name}", f"{label} missing required field: {field_name}")


def _require_str(value_map: Mapping[str, Any], field_names: Sequence[str], label: str) -> None:
    """Require a present, non-empty string. Rejects nested objects/lists in scalar
    fields so a metadata blob cannot bypass the allowlist envelope under a
    non-denylisted key name."""
    for field_name in field_names:
        value = value_map.get(field_name)
        if value is None or (isinstance(value, str) and not value.strip()):
            _fail(f"missing_{field_name}", f"{label} missing required field: {field_name}")
        if not isinstance(value, str):
            _fail(f"non_string_{field_name}", f"{label} field must be a string: {field_name}")


def _validate_optional_str(value_map: Mapping[str, Any], field_names: Sequence[str], label: str) -> None:
    for field_name in field_names:
        if field_name not in value_map:
            continue
        value = value_map[field_name]
        if value is None:
            continue
        if not isinstance(value, str) or not value.strip():
            _fail(f"non_string_{field_name}", f"{label} field must be null or a non-empty string: {field_name}")


def _validate_https_url(value: Any, label: str) -> None:
    if not isinstance(value, str) or not re.match(r"^https://", value.strip(), re.IGNORECASE):
        _fail("invalid_url", f"{label} must be an https URL")


def _is_list(value: Any) -> bool:
    return isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray))


def _assert_no_forbidden_output_value(value: str, *, path: str) -> None:
    for marker, pattern in _FORBIDDEN_OUTPUT_VALUE_PATTERNS:
        if pattern.search(value):
            _fail("forbidden_output_value", f"forbidden value ({marker}) at {path}")


def _fail(code: str, message: str) -> None:
    raise CreatorPublicHandleLinkageError(code, message)


