"""LinkedIn Lane Graph Frontier Register -- slice 2 validators.

Translate the architecture's Graph Frontier Register Additions + the pilot's
frontier stage into raising validators (``LinkedInLaneError``). Every negative is
a raise, so a test can prove the gate fails bad input rather than passing hollow.

Hardened to the slice-1 candidate-row standard (a cross-vendor delegated review
caught that this module had not carried those lessons): a fail-closed top-level
KEY allowlist on every mapping (derived from the dataclasses, so a forbidden
graph cannot be smuggled under an innocuous key the exact-match walk misses);
closed-enum allowlists on node_type/edge_type; a person-node excluded-basis
gate; the public_role_context theme-linkage rule; an originating-run guard so a
same-run frontier hop is fail-closed (not only execution_authorized=False); and
a NEGATED non_claims check (a positive inverse claim must not satisfy a category).
The forbidden-output-field walk is IMPORTED from linkedin_lane (slice 1).
"""
from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import fields
from typing import Any

from capture_spine.linkedin_lane.models import LinkedInLaneError
from capture_spine.linkedin_lane.validation import assert_no_forbidden_output_fields
from capture_spine.linkedin_graph_frontier.models import (
    LINKEDIN_GRAPH_FRONTIER_NEXT_RUN_ENVELOPE_SCHEMA_VERSION,
    LINKEDIN_GRAPH_FRONTIER_REGISTER_SCHEMA_VERSION,
    PERSON_CANDIDATE_NODE_TYPES,
    FrontierDecision,
    FrontierEdge,
    FrontierEdgeType,
    FrontierNode,
    FrontierNodeType,
    NextRunEnvelope,
    ProjectionDecision,
)


_ALLOWED_NODE_TYPES = frozenset(v.value for v in FrontierNodeType)
_ALLOWED_EDGE_TYPES = frozenset(v.value for v in FrontierEdgeType)
_PERSON_NODE_TYPE_VALUES = frozenset(v.value for v in PERSON_CANDIDATE_NODE_TYPES)
_ALLOWED_PROJECTION_DECISIONS = frozenset(v.value for v in ProjectionDecision)
_PERSON_PRIVACY_SENSITIVITIES = frozenset(
    {"person_strict", "public_actor_strict", "quarantine"}
)
_PERSON_DATA_MINIMIZED_SET = frozenset({"yes", "no"})

# Fail-closed top-level KEY allowlists, derived from the dataclasses so they track
# the schema with zero drift (mirrors slice-1 candidate-row hardening). This closes
# the alias path the exact-key forbidden walk cannot: a forbidden graph under an
# innocuous key, e.g. {"graph_payload": "follower graph: A->B"}.
_ALLOWED_REGISTER_WRAPPER_KEYS = frozenset(
    {"schema_version", "register_id", "source_run_id", "nodes", "edges", "frontier_decisions", "non_claims"}
)
_ALLOWED_NODE_KEYS = frozenset(f.name for f in fields(FrontierNode))
_ALLOWED_EDGE_KEYS = frozenset(f.name for f in fields(FrontierEdge))
_ALLOWED_DECISION_KEYS = frozenset(f.name for f in fields(FrontierDecision))
_ALLOWED_NEXT_RUN_ENVELOPE_KEYS = frozenset(f.name for f in fields(NextRunEnvelope))

# A person qualifies only on a concrete public-actor basis that stands OUTSIDE the
# org chart. These markers name bases the architecture/pilot disqualify outright;
# conservative fail-closed lexical exclusion (mirrors slice-1 candidate-row).
_EXCLUDED_PERSON_BASIS_MARKERS: tuple[str, ...] = (
    "org chart",
    "org-chart",
    "orgchart",
    "organization chart",
    "organisation chart",
    "reporting line",
    "reports to",
    "mentioned by",
    "tagged by",
    "mention/tag",
    "routine post",
    "routine employer",
    "routine work update",
    "routine update",
    "commenter",
    "follower",
    "connection",
)

# non_claims must DISCLAIM each hard-stop category (negative posture), not merely
# mention the category word -- a positive claim like "live LinkedIn access" must
# NOT satisfy "live". Each category must appear in a NEGATED claim.
_REQUIRED_NON_CLAIM_CATEGORIES: tuple[str, ...] = (
    "live",
    "promotion",
    "source capture packet",
    "data capture",
    "outreach",
)


def validate_graph_frontier_register(register: Mapping[str, Any]) -> None:
    assert_no_forbidden_output_fields(register)
    wrapper = register.get("linkedin_graph_frontier_register")
    if not isinstance(wrapper, Mapping):
        _fail("missing_register", "linkedin_graph_frontier_register wrapper is required")
    _reject_unknown_keys(wrapper, _ALLOWED_REGISTER_WRAPPER_KEYS, "register")
    if wrapper.get("schema_version") != LINKEDIN_GRAPH_FRONTIER_REGISTER_SCHEMA_VERSION:
        _fail(
            "invalid_schema_version",
            f"register schema_version must be {LINKEDIN_GRAPH_FRONTIER_REGISTER_SCHEMA_VERSION}",
        )
    nodes = wrapper.get("nodes")
    edges = wrapper.get("edges")
    if not _is_list(nodes):
        _fail("invalid_nodes", "nodes must be a list")
    if not _is_list(edges):
        _fail("invalid_edges", "edges must be a list")

    node_ids: set[Any] = set()
    for node in nodes:
        if not isinstance(node, Mapping):
            _fail("invalid_node", "node entries must be mappings")
        _validate_node(node)
        node_ids.add(node.get("node_id"))
    if len(node_ids) != len(nodes):
        _fail("duplicate_node_id", "every node must have a unique node_id")

    for edge in edges:
        if not isinstance(edge, Mapping):
            _fail("invalid_edge", "edge entries must be mappings")
        _validate_edge(edge, node_ids)

    for decision in wrapper.get("frontier_decisions", []):
        if not isinstance(decision, Mapping):
            _fail("invalid_frontier_decision", "frontier decisions must be mappings")
        _validate_decision(decision, node_ids)

    _validate_non_claims(wrapper.get("non_claims"), "register")


def validate_next_run_envelope(envelope: Mapping[str, Any]) -> None:
    assert_no_forbidden_output_fields(envelope)
    _reject_unknown_keys(envelope, _ALLOWED_NEXT_RUN_ENVELOPE_KEYS, "next_run_envelope")
    _require(
        envelope,
        (
            "schema_version",
            "next_run_id",
            "originating_run_id",
            "selected_node_id",
            "prior_register_pointer",
            "declared_theme_or_decision_context",
            "declared_seed_or_surface",
            "candidate_surface_allowlist",
            "exclusions",
            "method_mode",
            "access_mode",
            "source_policy_posture",
            "stop_condition",
        ),
        "next_run_envelope",
    )
    if envelope.get("schema_version") != LINKEDIN_GRAPH_FRONTIER_NEXT_RUN_ENVELOPE_SCHEMA_VERSION:
        _fail(
            "invalid_schema_version",
            f"next run envelope schema_version must be {LINKEDIN_GRAPH_FRONTIER_NEXT_RUN_ENVELOPE_SCHEMA_VERSION}",
        )
    if envelope.get("execution_authorized") is not False:
        _fail(
            "execution_authorization_forbidden",
            "next run envelopes must not authorize execution (each hop = a new, separately-authorized run)",
        )
    if envelope.get("next_run_id") == envelope.get("originating_run_id"):
        _fail(
            "same_run_frontier_traversal",
            "a frontier hop requires a new run_id; next_run_id must differ from originating_run_id (no same-run traversal)",
        )
    if not isinstance(envelope.get("caps"), Mapping) or not envelope.get("caps"):
        _fail("missing_caps", "caps are required (each hop = a new run with its own caps)")
    _validate_non_claims(envelope.get("non_claims"), "next_run_envelope")


def _validate_node(node: Mapping[str, Any]) -> None:
    _reject_unknown_keys(node, _ALLOWED_NODE_KEYS, "node")
    _require(
        node,
        (
            "node_id",
            "node_type",
            "run_id",
            "source_surface",
            "source_url_or_locator",
            "timestamp",
            "method_mode",
            "access_mode",
            "source_policy_posture",
            "stop_reason",
        ),
        "node",
    )
    if node.get("node_type") not in _ALLOWED_NODE_TYPES:
        _fail("invalid_node_type", "frontier node_type must be an allowed FrontierNodeType")
    _validate_non_claims(node.get("non_claims"), "node")
    if node.get("node_type") in _PERSON_NODE_TYPE_VALUES:
        _validate_person_node(node)


def _validate_person_node(node: Mapping[str, Any]) -> None:
    basis = node.get("senior_role_or_public_actor_basis_or_none")
    if not isinstance(basis, str) or not basis.strip():
        _fail(
            "missing_public_actor_basis",
            "a person-candidate node requires a concrete org-chart-independent public-actor basis",
        )
    lowered_basis = basis.lower()
    for marker in _EXCLUDED_PERSON_BASIS_MARKERS:
        if marker in lowered_basis:
            _fail(
                "excluded_public_actor_basis",
                "a person-candidate node basis must stand outside the org chart and must not rely on a "
                f"mention/tag, routine post, commenter, follower, or connection status (matched: {marker!r})",
            )
    if node.get("privacy_sensitivity_or_none") not in _PERSON_PRIVACY_SENSITIVITIES:
        _fail(
            "invalid_person_privacy_sensitivity",
            "a person-candidate node requires privacy_sensitivity person_strict / public_actor_strict / quarantine",
        )
    minimization = node.get("minimization_rule_or_none")
    if not isinstance(minimization, str) or not minimization.strip():
        _fail("missing_minimization_rule", "a person-candidate node requires a minimization_rule")
    if node.get("person_data_minimized_or_none") not in _PERSON_DATA_MINIMIZED_SET:
        _fail(
            "person_data_minimized_not_set",
            "a person-candidate node requires person_data_minimized set (yes/no)",
        )


def _validate_edge(edge: Mapping[str, Any], node_ids: set[Any]) -> None:
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
            "timestamp",
            "method_mode",
            "stop_reason",
        ),
        "edge",
    )
    if edge.get("edge_type") not in _ALLOWED_EDGE_TYPES:
        _fail("invalid_edge_type", "frontier edge_type must be an allowed FrontierEdgeType")
    if edge.get("from_node_id") not in node_ids or edge.get("to_node_id") not in node_ids:
        _fail("edge_points_to_missing_node", "frontier edges must point to known nodes")
    if edge.get("edge_type") == FrontierEdgeType.PUBLIC_ROLE_CONTEXT.value:
        linkage = edge.get("theme_linkage_or_none")
        if not isinstance(linkage, str) or not linkage.strip():
            _fail(
                "missing_theme_linkage",
                "a public_role_context edge requires a theme linkage (it must not become general person tracking)",
            )
    _validate_non_claims(edge.get("non_claims"), "edge")


def _validate_decision(decision: Mapping[str, Any], node_ids: set[Any]) -> None:
    _reject_unknown_keys(decision, _ALLOWED_DECISION_KEYS, "frontier_decision")
    if decision.get("selected_node_id") not in node_ids:
        _fail("decision_points_to_missing_node", "frontier decision must point to a known node")
    if decision.get("projection_decision") not in _ALLOWED_PROJECTION_DECISIONS:
        _fail(
            "invalid_projection_decision",
            "frontier decision projection_decision must be promote / hold / quarantine / dead_end",
        )
    reason = decision.get("frontier_selection_reason")
    if not isinstance(reason, str) or not reason.strip():
        _fail("missing_selection_reason", "frontier decision requires a selection reason")
    _validate_non_claims(decision.get("non_claims"), "frontier_decision")


def _reject_unknown_keys(value_map: Mapping[str, Any], allowed_keys: frozenset[str], label: str) -> None:
    unknown = sorted(str(key) for key in value_map if str(key) not in allowed_keys)
    if unknown:
        _fail("unknown_field", f"{label} contains unknown field(s): {unknown}")


def _require(value_map: Mapping[str, Any], field_names: tuple[str, ...], label: str) -> None:
    for field_name in field_names:
        value = value_map.get(field_name)
        if value is None or (isinstance(value, str) and not value.strip()):
            _fail(f"missing_{field_name}", f"{label} missing required field: {field_name}")


def _validate_non_claims(value: Any, label: str) -> None:
    if not _is_list(value):
        _fail("missing_non_claims", f"{label} requires non_claims")
    claims = [str(item).strip().lower() for item in value]
    missing = [
        category
        for category in _REQUIRED_NON_CLAIM_CATEGORIES
        if not any(category in claim and _is_negated(claim) for claim in claims)
    ]
    if missing:
        _fail(
            "incomplete_non_claims",
            f"{label} non_claims must DISCLAIM (negate) the required hard-stop categories; missing: {missing}",
        )


def _is_negated(claim: str) -> bool:
    return claim.startswith("not ") or claim.startswith("no ") or " not " in claim


def _is_list(value: Any) -> bool:
    return isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray))


def _fail(code: str, message: str) -> None:
    raise LinkedInLaneError(code, message)
