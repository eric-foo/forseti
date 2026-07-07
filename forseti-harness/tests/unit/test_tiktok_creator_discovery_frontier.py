from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from capture_spine.tiktok_creator_discovery_frontier import (
    DEFAULT_TIKTOK_CREATOR_DISCOVERY_FRONTIER_NON_CLAIMS,
    FrontierEdge,
    FrontierEdgeType,
    FrontierNode,
    FrontierNodeType,
    NextRunEnvelope,
    TikTokCreatorDiscoveryFrontierError,
    validate_tiktok_creator_discovery_frontier_register,
    validate_tiktok_creator_discovery_next_run_envelope,
)

_RUN_ID = "tiktok_creator_discovery_seed_001"
_RUN_NODE_ID = "run_tiktok_creator_discovery_seed_001"
_SEED_NODE_ID = "seed_tiktok_fragranceknowledge"
_CANDIDATE_NODE_ID = "candidate_tiktok_3whiffs"


def _node(node_id: str, node_type: FrontierNodeType, handle: str | None, **overrides) -> FrontierNode:
    fields = dict(
        node_id=node_id,
        node_type=node_type,
        platform="tiktok",
        handle_or_none=handle,
        display_name_or_none="Fragrance creator" if handle else None,
        source_url_or_locator=f"https://www.tiktok.com/@{handle}" if handle else "seed-profile",
        run_id=_RUN_ID,
        source_surface="tiktok_profile_suggested_accounts_existing_cloakbrowser_cdp",
        timestamp="2026-07-07T18:06:35.790Z",
        method_mode="existing_cloakbrowser_cdp_dom_extraction",
        access_mode="owner_authorized_existing_session_screen_light_dom_read",
        caps_applied={"root_profiles": 1, "suggested_accounts_observed": 1},
        exclusions=("no_candidate_profile_open", "no_metric_rollup", "no_registry_mutation"),
        stop_reason="bounded_suggested_accounts_observation_complete",
        registry_preflight_status_or_none=None,
        platform_capture_status="tiktok_suggested_account_target_only_not_profile_captured",
        cross_platform_graph_status="not_started",
    )
    fields.update(overrides)
    return FrontierNode(**fields)


def _edge(**overrides) -> FrontierEdge:
    fields = dict(
        edge_id="edge_seed_to_candidate_3whiffs",
        edge_type=FrontierEdgeType.PLATFORM_SUGGESTED_ACCOUNT_RELATION,
        from_node_id=_SEED_NODE_ID,
        to_node_id=_CANDIDATE_NODE_ID,
        run_id=_RUN_ID,
        source_surface="tiktok_profile_suggested_accounts_existing_cloakbrowser_cdp",
        source_packet_id_or_none="01KWYW8Q2SB612TWPA46NKVMKQ",
        observed_sections=("suggested_accounts",),
        timestamp="2026-07-07T18:06:35.790Z",
        method_mode="existing_cloakbrowser_cdp_dom_extraction",
        stop_reason="bounded_suggested_accounts_observation_complete",
        confidence="weak_platform_suggestion_only",
    )
    fields.update(overrides)
    return FrontierEdge(**fields)


def _next_run(**overrides) -> NextRunEnvelope:
    fields = dict(
        next_run_id="tiktok_creator_scan_3whiffs_next_01",
        selected_node_id=_CANDIDATE_NODE_ID,
        prior_register_pointer="docs/review-inputs/example.json#/tiktok_creator_discovery_frontier_register",
        declared_seed_or_surface="https://www.tiktok.com/@3whiffs",
        candidate_surface_allowlist=("tiktok_creator_profile", "source_visible_bio_link_hub"),
        caps={"profiles": 1, "suggested_accounts_expansion_depth": 0},
        exclusions=("no_same_run_snowball", "no_metric_rollup", "no_registry_mutation_without_preflight"),
        method_mode="owner_launched_existing_session_or_capture_lane_route_required",
        access_mode="not_started",
        source_policy_posture="requires_current_tiktok_capture_lane_posture_check_before_execution",
        stop_condition="stop_after_parent_profile_grid_and_source_visible_link_hub_or_on_access_friction",
    )
    fields.update(overrides)
    return NextRunEnvelope(**fields)


def _register(**wrapper_overrides) -> dict:
    wrapper = {
        "schema_version": "tiktok_creator_discovery_frontier_register_v0",
        "register_id": "tiktok_creator_discovery_frontier_example",
        "source_run_id": _RUN_ID,
        "root_seed": {
            "platform": "tiktok",
            "handle": "fragranceknowledge",
            "url": "https://www.tiktok.com/@fragranceknowledge",
        },
        "provenance": {
            "source_surface": "tiktok_profile_suggested_accounts_existing_cloakbrowser_cdp",
            "source_packet_id_or_none": "01KWYW8Q2SB612TWPA46NKVMKQ",
            "source_packet_path_or_none": "F:/orca-data-lake/raw/841/01KWYW8Q2SB612TWPA46NKVMKQ",
            "parent_grid_packet_id_or_none": "01KWYMDCZMSB4S5HBERVBYJQNG",
            "parent_grid_packet_path_or_none": "F:/orca-data-lake/raw/4e6/01KWYMDCZMSB4S5HBERVBYJQNG",
            "captured_at_utc": "2026-07-07T18:06:35.790Z",
            "method_mode": "existing_cloakbrowser_cdp_dom_extraction",
            "access_mode": "owner_authorized_existing_session_screen_light_dom_read",
            "caps_applied": {"root_profiles": 1, "candidate_profiles_opened": 0},
            "stop_reason": "bounded_suggested_accounts_observation_complete",
        },
        "nodes": [
            _node(_RUN_NODE_ID, FrontierNodeType.RUN, None).to_dict(),
            _node(_SEED_NODE_ID, FrontierNodeType.TIKTOK_CREATOR_SEED, "fragranceknowledge").to_dict(),
            _node(_CANDIDATE_NODE_ID, FrontierNodeType.TIKTOK_CREATOR_CANDIDATE, "3whiffs").to_dict(),
        ],
        "edges": [_edge().to_dict()],
        "frontier_decisions": [],
        "next_run_envelopes": [_next_run().to_dict()],
        "non_claims": list(DEFAULT_TIKTOK_CREATOR_DISCOVERY_FRONTIER_NON_CLAIMS),
    }
    wrapper.update(wrapper_overrides)
    return {"tiktok_creator_discovery_frontier_register": wrapper}


def _raises_code(register: dict, code: str) -> None:
    with pytest.raises(TikTokCreatorDiscoveryFrontierError) as exc_info:
        validate_tiktok_creator_discovery_frontier_register(register)
    assert exc_info.value.code == code


def test_valid_register_passes() -> None:
    validate_tiktok_creator_discovery_frontier_register(_register())


def test_valid_next_run_envelope_passes() -> None:
    validate_tiktok_creator_discovery_next_run_envelope(_next_run().to_dict())


def test_to_dict_serializes_enums() -> None:
    node = _node(_CANDIDATE_NODE_ID, FrontierNodeType.TIKTOK_CREATOR_CANDIDATE, "3whiffs").to_dict()
    assert node["node_type"] == "tiktok_creator_candidate"
    edge = _edge().to_dict()
    assert edge["edge_type"] == "platform_suggested_account_relation"


def test_committed_fragranceknowledge_register_passes() -> None:
    path = (
        Path(__file__).resolve().parents[3]
        / "docs"
        / "review-inputs"
        / "fragranceknowledge_tiktok_creator_discovery_frontier_register_20260708.json"
    )
    data = json.loads(path.read_text(encoding="utf-8"))
    validate_tiktok_creator_discovery_frontier_register(data)


def test_missing_wrapper_raises() -> None:
    _raises_code({"wrong": {}}, "unknown_field")


def test_wrong_schema_version_raises() -> None:
    register = _register()
    register["tiktok_creator_discovery_frontier_register"]["schema_version"] = "wrong"
    _raises_code(register, "invalid_schema_version")


def test_forbidden_registry_mutation_key_raises() -> None:
    register = _register()
    register["tiktok_creator_discovery_frontier_register"]["registry_mutation"] = {"insert": True}
    _raises_code(register, "forbidden_output_field")


def test_unknown_node_key_raises() -> None:
    register = _register()
    register["tiktok_creator_discovery_frontier_register"]["nodes"][2]["graph_payload"] = "A follows B"
    _raises_code(register, "unknown_field")


def test_duplicate_node_id_raises() -> None:
    register = _register()
    wrapper = register["tiktok_creator_discovery_frontier_register"]
    wrapper["nodes"].append(deepcopy(wrapper["nodes"][2]))
    _raises_code(register, "duplicate_node_id")


def test_duplicate_edge_id_raises() -> None:
    register = _register()
    wrapper = register["tiktok_creator_discovery_frontier_register"]
    wrapper["edges"].append(deepcopy(wrapper["edges"][0]))
    _raises_code(register, "duplicate_edge_id")


def test_invalid_edge_type_raises() -> None:
    register = _register()
    register["tiktok_creator_discovery_frontier_register"]["edges"][0]["edge_type"] = "follower_graph"
    _raises_code(register, "invalid_edge_type")


def test_edge_to_missing_node_raises() -> None:
    register = _register()
    register["tiktok_creator_discovery_frontier_register"]["edges"][0]["to_node_id"] = "missing"
    _raises_code(register, "edge_points_to_missing_node")


def test_next_run_execution_authorized_true_raises() -> None:
    with pytest.raises(TikTokCreatorDiscoveryFrontierError) as exc_info:
        validate_tiktok_creator_discovery_next_run_envelope(
            _next_run(execution_authorized=True).to_dict()
        )
    assert exc_info.value.code == "execution_authorization_forbidden"


def test_next_run_missing_caps_raises() -> None:
    with pytest.raises(TikTokCreatorDiscoveryFrontierError) as exc_info:
        validate_tiktok_creator_discovery_next_run_envelope(_next_run(caps={}).to_dict())
    assert exc_info.value.code == "missing_caps"


def test_next_run_must_target_candidate_node() -> None:
    register = _register()
    register["tiktok_creator_discovery_frontier_register"]["next_run_envelopes"][0][
        "selected_node_id"
    ] = _SEED_NODE_ID
    _raises_code(register, "next_run_not_candidate")


def test_positive_non_claims_raise() -> None:
    register = _register(non_claims=["Creator Registry identity proof"])
    _raises_code(register, "incomplete_non_claims")


def test_reversal_non_claims_raise() -> None:
    claims = list(DEFAULT_TIKTOK_CREATOR_DISCOVERY_FRONTIER_NON_CLAIMS)
    claims[0] = "not only Creator Registry identity proof; it authorizes registry use"
    register = _register(non_claims=claims)
    _raises_code(register, "incomplete_non_claims")


def test_forbidden_metric_field_raises() -> None:
    register = _register()
    register["tiktok_creator_discovery_frontier_register"]["nodes"][2]["metric_rollups"] = []
    _raises_code(register, "forbidden_output_field")


def test_forbidden_contact_value_raises() -> None:
    register = _register()
    register["tiktok_creator_discovery_frontier_register"]["nodes"][2][
        "display_name_or_none"
    ] = "email me at creator@example.com"
    _raises_code(register, "forbidden_output_value")


def test_packet_available_status_requires_packet_pointer() -> None:
    register = _register()
    wrapper = register["tiktok_creator_discovery_frontier_register"]
    wrapper["provenance"]["source_packet_id_or_none"] = None
    wrapper["provenance"]["source_packet_path_or_none"] = None
    wrapper["provenance"]["parent_grid_packet_id_or_none"] = None
    wrapper["provenance"]["parent_grid_packet_path_or_none"] = None
    wrapper["nodes"][2]["platform_capture_status"] = "tiktok_parent_profile_grid_packet_available"
    _raises_code(register, "missing_packet_pointer")
