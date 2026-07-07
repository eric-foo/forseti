"""Validators for TikTok Creator Discovery Frontier register artifacts."""
from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from dataclasses import fields
from typing import Any

from capture_spine.tiktok_creator_discovery_frontier.models import (
    TIKTOK_CREATOR_DISCOVERY_FRONTIER_REGISTER_SCHEMA_VERSION,
    TIKTOK_CREATOR_DISCOVERY_NEXT_RUN_ENVELOPE_SCHEMA_VERSION,
    FrontierDecision,
    FrontierEdge,
    FrontierEdgeType,
    FrontierNode,
    FrontierNodeType,
    NextRunEnvelope,
    ProjectionDecision,
    TikTokCreatorDiscoveryFrontierError,
)

_WRAPPER_KEY = "tiktok_creator_discovery_frontier_register"

_ALLOWED_TOP_LEVEL_KEYS = frozenset({_WRAPPER_KEY})
_ALLOWED_WRAPPER_KEYS = frozenset(
    {
        "schema_version",
        "register_id",
        "source_run_id",
        "root_seed",
        "provenance",
        "nodes",
        "edges",
        "frontier_decisions",
        "next_run_envelopes",
        "accepted_residuals",
        "non_claims",
    }
)
_ALLOWED_ROOT_SEED_KEYS = frozenset({"platform", "handle", "url"})
_ALLOWED_PROVENANCE_KEYS = frozenset(
    {
        "source_surface",
        "source_packet_id_or_none",
        "source_packet_path_or_none",
        "parent_grid_packet_id_or_none",
        "parent_grid_packet_path_or_none",
        "captured_at_utc",
        "method_mode",
        "access_mode",
        "caps_applied",
        "stop_reason",
    }
)
_ALLOWED_NODE_KEYS = frozenset(f.name for f in fields(FrontierNode))
_ALLOWED_EDGE_KEYS = frozenset(f.name for f in fields(FrontierEdge))
_ALLOWED_DECISION_KEYS = frozenset(f.name for f in fields(FrontierDecision))
_ALLOWED_NEXT_RUN_ENVELOPE_KEYS = frozenset(f.name for f in fields(NextRunEnvelope))

_ALLOWED_NODE_TYPES = frozenset(item.value for item in FrontierNodeType)
_ALLOWED_EDGE_TYPES = frozenset(item.value for item in FrontierEdgeType)
_ALLOWED_PROJECTION_DECISIONS = frozenset(item.value for item in ProjectionDecision)

_REQUIRED_NON_CLAIM_CATEGORIES = (
    "creator registry identity proof",
    "follower graph",
    "following graph",
    "endorsement proof",
    "country/region evidence",
    "metric rollup",
    "capture execution authorization",
    "source-access authorization",
    "standing crawler or monitor",
    "account completeness proof",
)

_FORBIDDEN_OUTPUT_FIELDS = {
    "registry_insert",
    "registry_insertion",
    "registry_update",
    "registry_mutation",
    "creator_registry_write",
    "inserted_creator_id",
    "metric",
    "metrics",
    "metric_rollup",
    "metric_rollups",
    "current_metric_rollups",
    "computed_metric_rollup",
    "view_count",
    "like_count",
    "comment_count",
    "share_count",
    "engagement_rate",
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
    "private_contact_route",
    "enrichment",
    "private_identity",
    "legal_name",
    "real_name",
    "inferred_real_name",
    "home_city",
    "address",
    "follower_list",
    "followers",
    "follower_graph",
    "following_list",
    "following",
    "following_graph",
    "audience_graph",
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
}
_FORBIDDEN_OUTPUT_VALUE_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("pem_private_key", re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----")),
    ("bearer_token", re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=\-]{16,}")),
    ("credentialed_url_userinfo", re.compile(r"://[^/\s:@]+:[^/\s:@]+@")),
    ("email_address", re.compile(r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b")),
    ("phone_url", re.compile(r"(?i)\btel:\+?[0-9][0-9 .()\-]{6,}")),
)
_REVERSAL_PREFIXES = ("not only ", "not merely ", "not just ", "no mere ")


def validate_tiktok_creator_discovery_frontier_register(register: Mapping[str, Any]) -> None:
    """Validate the frontier register shape without proving source truth."""
    _assert_no_forbidden_output_fields(register)
    _reject_unknown_keys(register, _ALLOWED_TOP_LEVEL_KEYS, "register top-level")
    wrapper = register.get(_WRAPPER_KEY)
    if not isinstance(wrapper, Mapping):
        _fail("missing_register_wrapper", f"{_WRAPPER_KEY} wrapper is required")
    _reject_unknown_keys(wrapper, _ALLOWED_WRAPPER_KEYS, "register")
    _require(
        wrapper,
        (
            "schema_version",
            "register_id",
            "source_run_id",
            "root_seed",
            "provenance",
            "nodes",
            "edges",
            "next_run_envelopes",
            "non_claims",
        ),
        "register",
    )
    if wrapper.get("schema_version") != TIKTOK_CREATOR_DISCOVERY_FRONTIER_REGISTER_SCHEMA_VERSION:
        _fail(
            "invalid_schema_version",
            "schema_version must be "
            f"{TIKTOK_CREATOR_DISCOVERY_FRONTIER_REGISTER_SCHEMA_VERSION}",
        )
    _validate_root_seed(wrapper["root_seed"])
    _validate_provenance(wrapper["provenance"])
    _validate_non_claims(wrapper.get("non_claims"), "register")
    _validate_accepted_residuals(wrapper.get("accepted_residuals"))

    nodes = wrapper.get("nodes")
    edges = wrapper.get("edges")
    if not _is_list(nodes):
        _fail("invalid_nodes", "nodes must be a list")
    if not _is_list(edges):
        _fail("invalid_edges", "edges must be a list")

    node_by_id: dict[str, Mapping[str, Any]] = {}
    for node in nodes:
        if not isinstance(node, Mapping):
            _fail("invalid_node", "node entries must be mappings")
        _validate_node(node, wrapper["provenance"])
        node_id = node.get("node_id")
        if node_id in node_by_id:
            _fail("duplicate_node_id", "every node must have a unique node_id")
        node_by_id[str(node_id)] = node

    edge_ids: set[str] = set()
    for edge in edges:
        if not isinstance(edge, Mapping):
            _fail("invalid_edge", "edge entries must be mappings")
        _validate_edge(edge, set(node_by_id))
        edge_id = str(edge.get("edge_id"))
        if edge_id in edge_ids:
            _fail("duplicate_edge_id", "every edge must have a unique edge_id")
        edge_ids.add(edge_id)

    for decision in wrapper.get("frontier_decisions", []):
        if not isinstance(decision, Mapping):
            _fail("invalid_frontier_decision", "frontier decisions must be mappings")
        _validate_decision(decision, set(node_by_id))

    for envelope in wrapper.get("next_run_envelopes"):
        if not isinstance(envelope, Mapping):
            _fail("invalid_next_run_envelope", "next run envelopes must be mappings")
        validate_tiktok_creator_discovery_next_run_envelope(envelope)
        selected_node_id = envelope.get("selected_node_id")
        selected_node = node_by_id.get(str(selected_node_id))
        if selected_node is None:
            _fail("next_run_points_to_missing_node", "next run envelope selected_node_id must point to a known node")
        if selected_node.get("node_type") != FrontierNodeType.TIKTOK_CREATOR_CANDIDATE.value:
            _fail("next_run_not_candidate", "next run envelopes must target candidate nodes")


def validate_tiktok_creator_discovery_next_run_envelope(envelope: Mapping[str, Any]) -> None:
    """Validate a next-run envelope and keep it execution-unauthorized."""
    _assert_no_forbidden_output_fields(envelope)
    _reject_unknown_keys(envelope, _ALLOWED_NEXT_RUN_ENVELOPE_KEYS, "next_run_envelope")
    _require(
        envelope,
        (
            "schema_version",
            "next_run_id",
            "selected_node_id",
            "prior_register_pointer",
            "declared_seed_or_surface",
            "candidate_surface_allowlist",
            "caps",
            "exclusions",
            "method_mode",
            "access_mode",
            "source_policy_posture",
            "stop_condition",
            "execution_authorized",
            "non_claims",
        ),
        "next_run_envelope",
    )
    if envelope.get("schema_version") != TIKTOK_CREATOR_DISCOVERY_NEXT_RUN_ENVELOPE_SCHEMA_VERSION:
        _fail(
            "invalid_next_run_schema_version",
            "next run envelope schema_version must be "
            f"{TIKTOK_CREATOR_DISCOVERY_NEXT_RUN_ENVELOPE_SCHEMA_VERSION}",
        )
    if envelope.get("execution_authorized") is not False:
        _fail("execution_authorization_forbidden", "next run envelopes must not authorize execution")
    if not isinstance(envelope.get("caps"), Mapping) or not envelope.get("caps"):
        _fail("missing_caps", "next run envelope caps must be a non-empty mapping")
    if not _is_list(envelope.get("candidate_surface_allowlist")) or not envelope.get(
        "candidate_surface_allowlist"
    ):
        _fail("missing_candidate_surface_allowlist", "candidate_surface_allowlist must be a non-empty list")
    if not _is_list(envelope.get("exclusions")):
        _fail("missing_exclusions", "next run envelope exclusions must be a list")
    _validate_non_claims(envelope.get("non_claims"), "next_run_envelope")


def _validate_root_seed(value: Any) -> None:
    if not isinstance(value, Mapping):
        _fail("invalid_root_seed", "root_seed must be a mapping")
    _reject_unknown_keys(value, _ALLOWED_ROOT_SEED_KEYS, "root_seed")
    _require(value, ("platform", "handle", "url"), "root_seed")
    if value.get("platform") != "tiktok":
        _fail("invalid_root_seed_platform", "root_seed platform must be tiktok")


def _validate_provenance(value: Any) -> None:
    if not isinstance(value, Mapping):
        _fail("invalid_provenance", "provenance must be a mapping")
    _reject_unknown_keys(value, _ALLOWED_PROVENANCE_KEYS, "provenance")
    _require(
        value,
        (
            "source_surface",
            "source_packet_id_or_none",
            "source_packet_path_or_none",
            "captured_at_utc",
            "method_mode",
            "access_mode",
            "caps_applied",
            "stop_reason",
        ),
        "provenance",
    )
    if not isinstance(value.get("caps_applied"), Mapping) or not value.get("caps_applied"):
        _fail("missing_caps_applied", "provenance caps_applied must be a non-empty mapping")
    _validate_packet_pair(value, "source_packet")
    _validate_packet_pair(value, "parent_grid_packet")


def _validate_packet_pair(value: Mapping[str, Any], prefix: str) -> None:
    id_key = f"{prefix}_id_or_none"
    path_key = f"{prefix}_path_or_none"
    packet_id = value.get(id_key)
    packet_path = value.get(path_key)
    if packet_id is not None and (not isinstance(packet_id, str) or not packet_id.strip()):
        _fail("invalid_packet_id", f"{id_key} must be a non-empty string or null")
    if packet_path is not None and (not isinstance(packet_path, str) or not packet_path.strip()):
        _fail("invalid_packet_path", f"{path_key} must be a non-empty string or null")
    if packet_id and not packet_path:
        _fail("missing_packet_path", f"{path_key} is required when {id_key} is present")
    if packet_path and not packet_id:
        _fail("missing_packet_id", f"{id_key} is required when {path_key} is present")


def _validate_node(node: Mapping[str, Any], provenance: Mapping[str, Any]) -> None:
    _reject_unknown_keys(node, _ALLOWED_NODE_KEYS, "node")
    _require(
        node,
        (
            "node_id",
            "node_type",
            "platform",
            "source_url_or_locator",
            "run_id",
            "source_surface",
            "timestamp",
            "method_mode",
            "access_mode",
            "caps_applied",
            "exclusions",
            "stop_reason",
            "platform_capture_status",
            "cross_platform_graph_status",
            "non_claims",
        ),
        "node",
    )
    if node.get("node_type") not in _ALLOWED_NODE_TYPES:
        _fail("invalid_node_type", "node_type must be an allowed TikTok frontier node type")
    if node.get("platform") != "tiktok":
        _fail("invalid_node_platform", "frontier nodes must use platform tiktok")
    if not isinstance(node.get("caps_applied"), Mapping) or not node.get("caps_applied"):
        _fail("missing_node_caps_applied", "node caps_applied must be a non-empty mapping")
    if not _is_list(node.get("exclusions")):
        _fail("missing_node_exclusions", "node exclusions must be a list")
    if "packet_available" in str(node.get("platform_capture_status", "")):
        if not (
            provenance.get("source_packet_id_or_none")
            or provenance.get("parent_grid_packet_id_or_none")
        ):
            _fail("missing_packet_pointer", "packet-available node status requires provenance packet pointer")
    _validate_non_claims(node.get("non_claims"), "node")


def _validate_edge(edge: Mapping[str, Any], node_ids: set[str]) -> None:
    _reject_unknown_keys(edge, _ALLOWED_EDGE_KEYS, "edge")
    _require(
        edge,
        (
            "edge_id",
            "edge_type",
            "from_node_id",
            "to_node_id",
            "run_id",
            "source_surface",
            "observed_sections",
            "timestamp",
            "method_mode",
            "stop_reason",
            "confidence",
            "non_claims",
        ),
        "edge",
    )
    if edge.get("edge_type") not in _ALLOWED_EDGE_TYPES:
        _fail("invalid_edge_type", "edge_type must be an allowed TikTok frontier edge type")
    if edge.get("from_node_id") not in node_ids or edge.get("to_node_id") not in node_ids:
        _fail("edge_points_to_missing_node", "frontier edges must point to known nodes")
    if not _is_list(edge.get("observed_sections")) or not edge.get("observed_sections"):
        _fail("missing_observed_sections", "edge observed_sections must be a non-empty list")
    _validate_non_claims(edge.get("non_claims"), "edge")


def _validate_decision(decision: Mapping[str, Any], node_ids: set[str]) -> None:
    _reject_unknown_keys(decision, _ALLOWED_DECISION_KEYS, "frontier_decision")
    _require(
        decision,
        (
            "decision_id",
            "selected_node_id",
            "projection_decision",
            "frontier_selection_reason",
            "frontier_selection_actor",
            "frontier_selection_timestamp",
            "non_claims",
        ),
        "frontier_decision",
    )
    if decision.get("selected_node_id") not in node_ids:
        _fail("frontier_decision_points_to_missing_node", "frontier decision must point to a known node")
    if decision.get("projection_decision") not in _ALLOWED_PROJECTION_DECISIONS:
        _fail("invalid_projection_decision", "frontier decision projection_decision is invalid")
    _validate_non_claims(decision.get("non_claims"), "frontier_decision")


def _validate_accepted_residuals(value: Any) -> None:
    if value is None:
        return
    if not _is_list(value):
        _fail("invalid_accepted_residuals", "accepted_residuals must be a list when present")
    for item in value:
        if not isinstance(item, str) or not item.strip():
            _fail("invalid_accepted_residual", "accepted_residual entries must be non-empty strings")


def _validate_non_claims(value: Any, label: str) -> None:
    if not _is_list(value):
        _fail("missing_non_claims", f"{label} requires non_claims")
    claims = [str(item).strip().lower() for item in value]
    missing = [
        category
        for category in _REQUIRED_NON_CLAIM_CATEGORIES
        if not any(_claim_disclaims_category(claim, category) for claim in claims)
    ]
    if missing:
        _fail("incomplete_non_claims", f"{label} non_claims missing negated categories: {missing}")


def _claim_disclaims_category(claim: str, category: str) -> bool:
    """Return True only when ``claim`` genuinely negates this one category.

    The category substring must appear in a negated claim (``_is_negated``) AND
    the claim must not also name another required category. Without the
    single-category constraint, one string that starts with ``not <A>`` but then
    positively asserts ``<B>``/``<C>`` ("not follower graph but it IS following
    graph, endorsement proof, ...") would satisfy every named category at once,
    because ``_is_negated`` only inspects the head of the string while the
    category match is substring-anywhere. Requiring exactly one required category
    per disclaimer closes that positive-smuggle path. No required category is a
    substring of another, so a real single-category disclaimer such as
    "not follower graph" still matches.
    """
    if not (_is_negated(claim) and category in claim):
        return False
    return not any(
        other != category and other in claim
        for other in _REQUIRED_NON_CLAIM_CATEGORIES
    )


def _is_negated(claim: str) -> bool:
    if not (claim.startswith("not ") or claim.startswith("no ")):
        return False
    return not any(claim.startswith(prefix) for prefix in _REVERSAL_PREFIXES)


def _assert_no_forbidden_output_fields(value: Any, *, path: str = "$") -> None:
    if isinstance(value, Mapping):
        for key, child in value.items():
            key_name = str(key)
            if key_name.lower() in _FORBIDDEN_OUTPUT_FIELDS:
                _fail("forbidden_output_field", f"forbidden output field at {path}.{key_name}")
            _assert_no_forbidden_output_fields(child, path=f"{path}.{key_name}")
        return
    if _is_list(value):
        for index, child in enumerate(value):
            _assert_no_forbidden_output_fields(child, path=f"{path}[{index}]")
        return
    if isinstance(value, str):
        for marker, pattern in _FORBIDDEN_OUTPUT_VALUE_PATTERNS:
            if pattern.search(value):
                _fail("forbidden_output_value", f"forbidden value ({marker}) at {path}")


def _reject_unknown_keys(value_map: Mapping[str, Any], allowed_keys: frozenset[str], label: str) -> None:
    unknown = sorted(str(key) for key in value_map if str(key) not in allowed_keys)
    if unknown:
        _fail("unknown_field", f"{label} contains unknown field(s): {unknown}")


def _require(value_map: Mapping[str, Any], field_names: Sequence[str], label: str) -> None:
    for field_name in field_names:
        if field_name not in value_map:
            _fail(f"missing_{field_name}", f"{label} missing required field: {field_name}")
        value = value_map.get(field_name)
        if isinstance(value, str) and not value.strip():
            _fail(f"missing_{field_name}", f"{label} missing required field: {field_name}")


def _is_list(value: Any) -> bool:
    return isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray))


def _fail(code: str, message: str) -> None:
    raise TikTokCreatorDiscoveryFrontierError(code, message)
