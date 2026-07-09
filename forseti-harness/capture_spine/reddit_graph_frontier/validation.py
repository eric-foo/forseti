from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from capture_spine.reddit_candidate_intake.validation import assert_no_forbidden_output_fields
from capture_spine.reddit_graph_frontier.models import (
    GRAPH_FRONTIER_NEXT_RUN_ENVELOPE_SCHEMA_VERSION,
    GRAPH_FRONTIER_REGISTER_SCHEMA_VERSION,
    GraphFrontierError,
)


REQUIRED_NON_CLAIMS = {
    "not Graph Frontier-owned live Reddit fetch",
    "not Source Capture Packet output",
    "not Data Capture handoff",
}


def validate_graph_frontier_register(register: Mapping[str, Any]) -> None:
    assert_no_forbidden_output_fields(register)
    wrapper = register.get("reddit_graph_frontier_register")
    if not isinstance(wrapper, Mapping):
        _fail("missing_graph_frontier_register", "reddit_graph_frontier_register wrapper is required")
    if wrapper.get("schema_version") != GRAPH_FRONTIER_REGISTER_SCHEMA_VERSION:
        _fail(
            "missing_or_unexpected_schema_version",
            f"register schema_version must be {GRAPH_FRONTIER_REGISTER_SCHEMA_VERSION}",
        )

    nodes = wrapper.get("nodes")
    edges = wrapper.get("edges")
    if not isinstance(nodes, Sequence) or isinstance(nodes, (str, bytes, bytearray)):
        _fail("invalid_nodes", "nodes must be a list")
    if not isinstance(edges, Sequence) or isinstance(edges, (str, bytes, bytearray)):
        _fail("invalid_edges", "edges must be a list")

    node_ids = {node.get("node_id") for node in nodes if isinstance(node, Mapping)}
    if len(node_ids) != len(nodes):
        _fail("duplicate_or_invalid_node_id", "every node must have a unique node_id")

    for node in nodes:
        if not isinstance(node, Mapping):
            _fail("invalid_node", "node entries must be mappings")
        _validate_required_mapping_fields(
            node,
            (
                "node_id",
                "node_type",
                "run_id",
                "source_surface",
                "source_url_or_locator",
                "query_or_seed",
                "sort_order_or_none",
                "time_window_or_none",
                "timestamp",
                "method_category",
                "access_mode",
                "caps_applied",
                "exclusions",
                "stop_reason",
                "non_claims",
            ),
            "node",
        )
        _validate_non_claims(node["non_claims"], "node")

    for edge in edges:
        if not isinstance(edge, Mapping):
            _fail("invalid_edge", "edge entries must be mappings")
        _validate_required_mapping_fields(
            edge,
            (
                "edge_id",
                "edge_type",
                "from_node_id",
                "to_node_id",
                "run_id",
                "source_surface",
                "timestamp",
                "method_category",
                "stop_reason",
                "non_claims",
            ),
            "edge",
        )
        if edge["from_node_id"] not in node_ids or edge["to_node_id"] not in node_ids:
            _fail("edge_points_to_missing_node", "frontier edges must point to known nodes")
        _validate_non_claims(edge["non_claims"], "edge")

    for decision in wrapper.get("frontier_decisions", []):
        if not isinstance(decision, Mapping):
            _fail("invalid_frontier_decision", "frontier decisions must be mappings")
        if decision.get("selected_node_id") not in node_ids:
            _fail("frontier_decision_points_to_missing_node", "frontier decision must point to a known node")
        if not str(decision.get("frontier_selection_reason", "")).strip():
            _fail("missing_frontier_selection_reason", "frontier decision requires a selection reason")
        _validate_non_claims(decision.get("non_claims"), "frontier_decision")

    _validate_non_claims(wrapper.get("non_claims"), "register")


def validate_next_run_envelope(envelope: Mapping[str, Any]) -> None:
    assert_no_forbidden_output_fields(envelope)
    _validate_required_mapping_fields(
        envelope,
        (
            "schema_version",
            "next_run_id",
            "selected_node_id",
            "prior_register_pointer",
            "declared_topic_theme_or_query",
            "declared_seed_or_surface",
            "candidate_surface_allowlist",
            "caps",
            "exclusions",
            "access_mode",
            "source_policy_posture",
            "stop_condition",
            "non_commercial_posture",
            "execution_authorized",
            "non_claims",
        ),
        "next_run_envelope",
    )
    if envelope["schema_version"] != GRAPH_FRONTIER_NEXT_RUN_ENVELOPE_SCHEMA_VERSION:
        _fail(
            "missing_or_unexpected_schema_version",
            f"next run envelope schema_version must be {GRAPH_FRONTIER_NEXT_RUN_ENVELOPE_SCHEMA_VERSION}",
        )
    if envelope["execution_authorized"] is not False:
        _fail("execution_authorization_forbidden", "next run envelopes must not authorize execution")
    if not str(envelope["source_policy_posture"]).strip():
        _fail("missing_source_policy_posture", "source_policy_posture is required")
    if not isinstance(envelope["caps"], Mapping) or not envelope["caps"]:
        _fail("missing_caps", "caps are required")
    _validate_non_claims(envelope["non_claims"], "next_run_envelope")


def _validate_required_mapping_fields(value: Mapping[str, Any], fields: tuple[str, ...], label: str) -> None:
    for field in fields:
        if field not in value:
            _fail(f"missing_{field}", f"{label} missing required field: {field}")


def _validate_non_claims(value: Any, label: str) -> None:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        _fail("missing_non_claims", f"{label} requires non_claims")
    missing = REQUIRED_NON_CLAIMS.difference(set(value))
    if missing:
        _fail("missing_required_non_claim", f"{label} missing non-claims: {sorted(missing)}")


def _fail(code: str, message: str) -> None:
    raise GraphFrontierError(code, message)
