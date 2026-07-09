"""Tests for the LinkedIn Graph Frontier Register (slice 2).

Fake-success guard: every negative asserts the validator RAISES
``LinkedInLaneError`` on the bad case -- a forbidden field, an out-of-vocab
node/edge type, an edge to a missing node, a person-candidate node missing its
public-actor basis or a privacy/minimization flag, a public_role_context edge
with no theme linkage, an invalid projection decision, a decision to a missing
node, a duplicate node id, hollow non_claims, an execution-authorized next-run
envelope, and a capless next run. Plus a precision test that the allowed visible
influence count/band fields on a person node do NOT trip the forbidden-field walk.
"""
from __future__ import annotations

import pytest

from capture_spine.linkedin_graph_frontier import (
    DEFAULT_LINKEDIN_GRAPH_FRONTIER_NON_CLAIMS,
    LINKEDIN_GRAPH_FRONTIER_REGISTER_SCHEMA_VERSION,
    FrontierDecision,
    FrontierEdge,
    FrontierEdgeType,
    FrontierNode,
    FrontierNodeType,
    LinkedInLaneError,
    NextRunEnvelope,
    ProjectionDecision,
    validate_graph_frontier_register,
    validate_next_run_envelope,
)

_RUN_ID = "lk_frontier_run_001"
_BUSINESS_ID = "business:r1:competitorx"
_PERSON_ID = "person:r1:janepublic"
_RUN_NODE_ID = "run:lk_frontier_run_001"


def _run_node(**overrides) -> FrontierNode:
    fields = dict(
        node_id=_RUN_NODE_ID,
        node_type=FrontierNodeType.RUN,
        run_id=_RUN_ID,
        source_surface="operator_supplied_seed_list",
        source_url_or_locator="operator-supplied seed list",
        query_or_seed="competitor X pricing-sensitivity decision",
        timestamp="2026-06-10T00:00:00Z",
        method_mode="agent_assisted_rowing_only",
        access_mode="no_live",
        source_policy_posture="discoverable_or_entitled_disclosable",
        caps_applied={"max_businesses": 25, "max_people": 15},
        exclusions=(),
        stop_reason="caps_reached",
    )
    fields.update(overrides)
    return FrontierNode(**fields)


def _business_node(**overrides) -> FrontierNode:
    fields = dict(
        node_id=_BUSINESS_ID,
        node_type=FrontierNodeType.BUSINESS_CANDIDATE,
        run_id=_RUN_ID,
        source_surface="company_website_blog_press_pricing",
        source_url_or_locator="https://competitorx.example/pricing",
        query_or_seed="competitor X pricing-sensitivity decision",
        timestamp="2026-06-10T00:00:00Z",
        method_mode="agent_assisted_rowing_only",
        access_mode="no_live",
        source_policy_posture="discoverable_or_entitled_disclosable",
        caps_applied={"max_businesses": 25},
        exclusions=(),
        stop_reason="caps_reached",
        candidate_value_or_none="Competitor X",
    )
    fields.update(overrides)
    return FrontierNode(**fields)


def _person_node(**overrides) -> FrontierNode:
    fields = dict(
        node_id=_PERSON_ID,
        node_type=FrontierNodeType.SENIOR_DECISION_MAKER_CANDIDATE,
        run_id=_RUN_ID,
        source_surface="conference_podcast_newsletter_publication",
        source_url_or_locator="https://conf.example/speakers/jane-public",
        query_or_seed="competitor X pricing-sensitivity decision",
        timestamp="2026-06-10T00:00:00Z",
        method_mode="agent_assisted_rowing_only",
        access_mode="no_live",
        source_policy_posture="discoverable_or_entitled_disclosable",
        caps_applied={"max_people": 15},
        exclusions=(),
        stop_reason="caps_reached",
        privacy_sensitivity_or_none="public_actor_strict",
        minimization_rule_or_none="name_role_locator_only",
        person_data_minimized_or_none="yes",
        senior_role_or_public_actor_basis_or_none="keynote speaker at a named public conference under her own name",
    )
    fields.update(overrides)
    return FrontierNode(**fields)


def _edge(**overrides) -> FrontierEdge:
    fields = dict(
        edge_id="discovered_from_run:run->business",
        edge_type=FrontierEdgeType.DISCOVERED_FROM_RUN,
        from_node_id=_RUN_NODE_ID,
        to_node_id=_BUSINESS_ID,
        run_id=_RUN_ID,
        source_surface="company_website_blog_press_pricing",
        timestamp="2026-06-10T00:00:00Z",
        method_mode="agent_assisted_rowing_only",
        stop_reason="caps_reached",
    )
    fields.update(overrides)
    return FrontierEdge(**fields)


def _public_role_edge(**overrides) -> FrontierEdge:
    fields = dict(
        edge_id="public_role_context:run->person",
        edge_type=FrontierEdgeType.PUBLIC_ROLE_CONTEXT,
        from_node_id=_RUN_NODE_ID,
        to_node_id=_PERSON_ID,
        run_id=_RUN_ID,
        source_surface="conference_podcast_newsletter_publication",
        timestamp="2026-06-10T00:00:00Z",
        method_mode="agent_assisted_rowing_only",
        stop_reason="caps_reached",
        theme_linkage_or_none="public keynote on competitor X pricing strategy -- material to the declared theme",
    )
    fields.update(overrides)
    return FrontierEdge(**fields)


def _decision(**overrides) -> FrontierDecision:
    fields = dict(
        decision_id="decision:0001",
        selected_node_id=_BUSINESS_ID,
        projection_decision=ProjectionDecision.PROMOTE,
        frontier_selection_reason="direct competitor in the declared theme; strong public pricing signal",
        frontier_selection_actor="operator",
        frontier_selection_timestamp="2026-06-10T00:00:00Z",
    )
    fields.update(overrides)
    return FrontierDecision(**fields)


def _register(*, nodes=None, edges=None, decisions=None, **wrapper_overrides) -> dict:
    if nodes is None:
        nodes = [_run_node(), _business_node(), _person_node()]
    if edges is None:
        edges = [_edge(), _public_role_edge()]
    if decisions is None:
        decisions = [_decision()]
    wrapper = dict(
        schema_version=LINKEDIN_GRAPH_FRONTIER_REGISTER_SCHEMA_VERSION,
        register_id="lk_frontier_register_001",
        source_run_id=_RUN_ID,
        nodes=[n.to_dict() for n in nodes],
        edges=[e.to_dict() for e in edges],
        frontier_decisions=[d.to_dict() for d in decisions],
        non_claims=list(DEFAULT_LINKEDIN_GRAPH_FRONTIER_NON_CLAIMS),
    )
    wrapper.update(wrapper_overrides)
    return {"linkedin_graph_frontier_register": wrapper}


def _next_run_envelope(**overrides) -> NextRunEnvelope:
    fields = dict(
        next_run_id="lk_frontier_run_002",
        originating_run_id=_RUN_ID,
        selected_node_id=_BUSINESS_ID,
        prior_register_pointer="lk_frontier_register_001#business:r1:competitorx",
        declared_theme_or_decision_context="competitor X pricing-sensitivity decision",
        declared_seed_or_surface="competitorx.example",
        candidate_surface_allowlist=("company_website_blog_press_pricing",),
        caps={"max_businesses": 25},
        exclusions=(),
        method_mode="agent_assisted_rowing_only",
        access_mode="no_live",
        source_policy_posture="discoverable_or_entitled_disclosable",
        stop_condition="caps_reached",
    )
    fields.update(overrides)
    return NextRunEnvelope(**fields)


# --- positive / round-trip ---

def test_valid_register_passes() -> None:
    validate_graph_frontier_register(_register())


def test_valid_next_run_envelope_passes() -> None:
    validate_next_run_envelope(_next_run_envelope().to_dict())


def test_to_dict_serializes_enums() -> None:
    node = _person_node().to_dict()
    assert node["node_type"] == "senior_decision_maker_candidate"
    assert isinstance(node["non_claims"], list)  # tuple -> list via _enum_values
    decision = _decision().to_dict()
    assert decision["projection_decision"] == "promote"


def test_visible_influence_counts_on_person_node_do_not_trip_walk() -> None:
    # precision: *_count_or_none / *_band_or_none are allowed; only graphs/lists are banned
    reg = _register(
        nodes=[
            _run_node(),
            _business_node(),
            _person_node(
                visible_follower_count_or_none="12k",
                visible_connection_count_band_or_none="500+",
            ),
        ]
    )
    validate_graph_frontier_register(reg)


# --- negatives: every one must raise ---

def test_forbidden_field_in_register_raises() -> None:
    reg = _register()
    reg["linkedin_graph_frontier_register"]["followers"] = ["a", "b", "c"]
    with pytest.raises(LinkedInLaneError):
        validate_graph_frontier_register(reg)


def test_invalid_node_type_raises() -> None:
    # frontier_decision is NOT a node type here (it is a separate structure)
    reg = _register()
    reg["linkedin_graph_frontier_register"]["nodes"][1]["node_type"] = "frontier_decision"
    with pytest.raises(LinkedInLaneError):
        validate_graph_frontier_register(reg)


def test_invalid_edge_type_raises() -> None:
    reg = _register()
    reg["linkedin_graph_frontier_register"]["edges"][0]["edge_type"] = "follower_graph"
    with pytest.raises(LinkedInLaneError):
        validate_graph_frontier_register(reg)


def test_edge_to_missing_node_raises() -> None:
    reg = _register(edges=[_edge(to_node_id="nonexistent-node")])
    with pytest.raises(LinkedInLaneError):
        validate_graph_frontier_register(reg)


def test_person_node_missing_basis_raises() -> None:
    reg = _register(
        nodes=[_run_node(), _business_node(), _person_node(senior_role_or_public_actor_basis_or_none=None)]
    )
    with pytest.raises(LinkedInLaneError):
        validate_graph_frontier_register(reg)


def test_person_node_wrong_privacy_sensitivity_raises() -> None:
    reg = _register(
        nodes=[_run_node(), _business_node(), _person_node(privacy_sensitivity_or_none="business_low")]
    )
    with pytest.raises(LinkedInLaneError):
        validate_graph_frontier_register(reg)


def test_person_node_not_minimized_raises() -> None:
    reg = _register(
        nodes=[_run_node(), _business_node(), _person_node(person_data_minimized_or_none="not_applicable")]
    )
    with pytest.raises(LinkedInLaneError):
        validate_graph_frontier_register(reg)


def test_person_node_missing_minimization_rule_raises() -> None:
    reg = _register(
        nodes=[_run_node(), _business_node(), _person_node(minimization_rule_or_none=None)]
    )
    with pytest.raises(LinkedInLaneError):
        validate_graph_frontier_register(reg)


def test_public_role_context_edge_missing_theme_linkage_raises() -> None:
    reg = _register(edges=[_edge(), _public_role_edge(theme_linkage_or_none=None)])
    with pytest.raises(LinkedInLaneError):
        validate_graph_frontier_register(reg)


def test_invalid_projection_decision_raises() -> None:
    reg = _register()
    reg["linkedin_graph_frontier_register"]["frontier_decisions"][0]["projection_decision"] = "totally_bogus"
    with pytest.raises(LinkedInLaneError):
        validate_graph_frontier_register(reg)


def test_decision_to_missing_node_raises() -> None:
    reg = _register(decisions=[_decision(selected_node_id="nonexistent-node")])
    with pytest.raises(LinkedInLaneError):
        validate_graph_frontier_register(reg)


def test_duplicate_node_id_raises() -> None:
    reg = _register(nodes=[_run_node(), _business_node(), _business_node()])
    with pytest.raises(LinkedInLaneError):
        validate_graph_frontier_register(reg)


def test_register_hollow_non_claims_raises() -> None:
    reg = _register(non_claims=("not ready",))
    with pytest.raises(LinkedInLaneError):
        validate_graph_frontier_register(reg)


def test_next_run_execution_authorized_true_raises() -> None:
    with pytest.raises(LinkedInLaneError):
        validate_next_run_envelope(_next_run_envelope(execution_authorized=True).to_dict())


def test_next_run_missing_caps_raises() -> None:
    with pytest.raises(LinkedInLaneError):
        validate_next_run_envelope(_next_run_envelope(caps={}).to_dict())


# --- negatives added after the cross-vendor delegated review (F1-F4) ---

def test_aliased_forbidden_payload_under_unknown_wrapper_key_raises() -> None:
    # F1: a forbidden graph smuggled under a non-denied key is rejected by the allowlist.
    reg = _register()
    reg["linkedin_graph_frontier_register"]["graph_payload"] = "follower graph: A follows B"
    with pytest.raises(LinkedInLaneError):
        validate_graph_frontier_register(reg)


def test_unknown_field_on_node_raises() -> None:
    # F1: an unknown (aliased) node key is rejected by the node allowlist.
    reg = _register()
    reg["linkedin_graph_frontier_register"]["nodes"][1]["connection_graph_blob"] = "A-B-C"
    with pytest.raises(LinkedInLaneError):
        validate_graph_frontier_register(reg)


def test_person_node_excluded_basis_raises() -> None:
    # F2: an explicitly excluded basis (org chart) is rejected, not just empty text.
    reg = _register(
        nodes=[
            _run_node(),
            _business_node(),
            _person_node(senior_role_or_public_actor_basis_or_none="org chart says VP"),
        ]
    )
    with pytest.raises(LinkedInLaneError):
        validate_graph_frontier_register(reg)


def test_same_run_envelope_raises() -> None:
    # F3: next_run_id == originating_run_id is same-run traversal -- fail-closed.
    with pytest.raises(LinkedInLaneError):
        validate_next_run_envelope(
            _next_run_envelope(next_run_id=_RUN_ID, originating_run_id=_RUN_ID).to_dict()
        )


def test_next_run_missing_seed_or_surface_raises() -> None:
    env = _next_run_envelope().to_dict()
    del env["declared_seed_or_surface"]
    with pytest.raises(LinkedInLaneError):
        validate_next_run_envelope(env)


def test_next_run_missing_exclusions_raises() -> None:
    env = _next_run_envelope().to_dict()
    del env["exclusions"]
    with pytest.raises(LinkedInLaneError):
        validate_next_run_envelope(env)


def test_positive_non_claims_raises() -> None:
    # F4: non_claims stating the POSITIVE inverse must not satisfy the category check.
    reg = _register(
        non_claims=(
            "live LinkedIn access",
            "automatic promotion",
            "Source Capture Packet output",
            "Data Capture handoff",
            "Outreach Lane execution",
        )
    )
    with pytest.raises(LinkedInLaneError):
        validate_graph_frontier_register(reg)


def test_reversal_negation_in_non_claims_raises() -> None:
    # Cross-vendor (GPT-5.5) reversal-bypass, shared with slice 3a: a syntactically
    # negated but semantically POSITIVE claim ("not only live access; it also
    # authorizes it") must NOT satisfy the "live" category.
    reg = _register(
        non_claims=(
            "not only live access; it also authorizes it",
            "not promotion",
            "not source capture packet",
            "not data capture",
            "not outreach",
        )
    )
    with pytest.raises(LinkedInLaneError):
        validate_graph_frontier_register(reg)


def test_register_unknown_top_level_sibling_key_raises() -> None:
    # Cross-vendor F2: a non-forbidden key ADJACENT to the wrapper at the top level
    # must be rejected, not silently ignored.
    reg = _register()
    reg["extra_top_level"] = "ignored"
    with pytest.raises(LinkedInLaneError):
        validate_graph_frontier_register(reg)
