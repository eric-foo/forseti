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
    LinkHubOutcome,
    RefreshOutcome,
    SUGGESTED_ACCOUNT_FRONTIER_SCOPE_LIMIT_RESIDUAL,
    ScanReceipt,
    SuggestedAccountObservation,
    NextRunEnvelope,
    TikTokCreatorDiscoveryFrontierError,
    build_tiktok_creator_discovery_frontier_register,
    validate_tiktok_creator_discovery_frontier_register,
    validate_tiktok_creator_discovery_next_run_envelope,
    validate_tiktok_creator_discovery_scan_receipt,
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


def _scan_receipt(**overrides) -> dict:
    fields = dict(
        receipt_id="receipt_tiktok_creator_discovery_seed_001",
        run_id=_RUN_ID,
        register_id="tiktok_creator_discovery_frontier_example",
        root_seed={
            "platform": "tiktok",
            "handle": "fragranceknowledge",
            "url": "https://www.tiktok.com/@fragranceknowledge",
        },
        source_surface="tiktok_profile_suggested_accounts_existing_cloakbrowser_cdp",
        captured_at_utc="2026-07-07T18:06:35.790Z",
        method_mode="existing_cloakbrowser_cdp_dom_extraction",
        access_mode="owner_authorized_existing_session_screen_light_dom_read",
        extraction_method="dom_visible_suggested_account_cards",
        browser_session_label_or_none="cloakbrowser_existing_chowdakr",
        parent_grid_packet_id_or_none="01KWYMDCZMSB4S5HBERVBYJQNG",
        parent_grid_packet_path_or_none="F:/orca-data-lake/raw/4e6/01KWYMDCZMSB4S5HBERVBYJQNG",
        source_packet_id_or_none="01KWYW8Q2SB612TWPA46NKVMKQ",
        source_packet_path_or_none="F:/orca-data-lake/raw/841/01KWYW8Q2SB612TWPA46NKVMKQ",
        parent_profile_capture_status="tiktok_parent_profile_grid_packet_available",
        suggested_accounts_capture_status="tiktok_suggested_accounts_packet_available",
        link_hub_capture_status=LinkHubOutcome.CAPTURED,
        link_hub_url_or_none="https://linktr.ee/fragranceknowledge",
        browser_closed_by_runner=False,
        refresh_attempt_count=0,
        refresh_outcome=RefreshOutcome.NOT_NEEDED,
        pagination_bound=0,
        suggested_accounts_observed=1,
        candidate_profiles_opened=0,
        follow_unfollow_actions_taken=0,
        screenshots_emitted_to_chat=0,
        caps_applied={
            "root_profiles": 1,
            "suggested_accounts_observed": 1,
            "candidate_profiles_opened": 0,
            "screenshots_emitted_to_chat": 0,
        },
        stop_reason="bounded_suggested_accounts_observation_complete",
        exclusions=(
            "no_candidate_profile_open",
            "no_follow_unfollow_action",
            "no_metric_rollup",
            "no_registry_mutation",
            "no_screenshot_chat_output",
        ),
    )
    fields.update(overrides)
    return ScanReceipt(**fields).to_dict()


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


def test_invalid_node_type_raises() -> None:
    register = _register()
    register["tiktok_creator_discovery_frontier_register"]["nodes"][2]["node_type"] = "creator_identity"
    _raises_code(register, "invalid_node_type")


def test_frontier_decision_to_missing_node_raises() -> None:
    register = _register()
    register["tiktok_creator_discovery_frontier_register"]["frontier_decisions"] = [
        {
            "decision_id": "decision_001",
            "selected_node_id": "missing",
            "projection_decision": "hold",
            "frontier_selection_reason": "exercise decision validation",
            "frontier_selection_actor": "test",
            "frontier_selection_timestamp": "2026-07-07T18:06:35.790Z",
            "next_run_id_or_none": None,
            "non_claims": list(DEFAULT_TIKTOK_CREATOR_DISCOVERY_FRONTIER_NON_CLAIMS),
        }
    ]
    _raises_code(register, "frontier_decision_points_to_missing_node")


def test_invalid_projection_decision_raises() -> None:
    register = _register()
    register["tiktok_creator_discovery_frontier_register"]["frontier_decisions"] = [
        {
            "decision_id": "decision_001",
            "selected_node_id": _CANDIDATE_NODE_ID,
            "projection_decision": "capture_now",
            "frontier_selection_reason": "exercise decision validation",
            "frontier_selection_actor": "test",
            "frontier_selection_timestamp": "2026-07-07T18:06:35.790Z",
            "next_run_id_or_none": None,
            "non_claims": list(DEFAULT_TIKTOK_CREATOR_DISCOVERY_FRONTIER_NON_CLAIMS),
        }
    ]
    _raises_code(register, "invalid_projection_decision")


def test_next_run_to_missing_node_raises() -> None:
    register = _register()
    register["tiktok_creator_discovery_frontier_register"]["next_run_envelopes"][0][
        "selected_node_id"
    ] = "missing"
    _raises_code(register, "next_run_points_to_missing_node")


def test_source_packet_id_requires_path() -> None:
    register = _register()
    register["tiktok_creator_discovery_frontier_register"]["provenance"][
        "source_packet_path_or_none"
    ] = None
    _raises_code(register, "missing_packet_path")


def test_source_packet_path_requires_id() -> None:
    register = _register()
    register["tiktok_creator_discovery_frontier_register"]["provenance"][
        "source_packet_id_or_none"
    ] = None
    _raises_code(register, "missing_packet_id")


def test_invalid_root_seed_platform_raises() -> None:
    register = _register()
    register["tiktok_creator_discovery_frontier_register"]["root_seed"]["platform"] = "instagram"
    _raises_code(register, "invalid_root_seed_platform")


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


def test_multi_category_smuggle_non_claims_raise() -> None:
    # A single claim that negates one category but then positively asserts the
    # rest ("not <A> but it IS <B>, <C> ...") must NOT satisfy the smuggled
    # categories: each required category needs its own genuine disclaimer. Under
    # the head-only negation check this one string would otherwise satisfy every
    # category at once while asserting nine of them positively.
    smuggle = (
        "not follower graph but it IS following graph, endorsement proof, "
        "metric rollup, country/region evidence, capture execution authorization, "
        "source-access authorization, standing crawler or monitor, "
        "account completeness proof, creator registry identity proof"
    )
    register = _register(non_claims=[smuggle])
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


def test_valid_scan_receipt_passes() -> None:
    validate_tiktok_creator_discovery_scan_receipt(_scan_receipt())


def test_scan_receipt_parent_packet_available_requires_parent_pointer() -> None:
    receipt = _scan_receipt(
        parent_grid_packet_id_or_none=None,
        parent_grid_packet_path_or_none=None,
    )
    with pytest.raises(TikTokCreatorDiscoveryFrontierError) as exc_info:
        validate_tiktok_creator_discovery_scan_receipt(receipt)
    assert exc_info.value.code == "missing_parent_grid_packet_pointer"


def test_scan_receipt_suggested_packet_available_requires_source_pointer() -> None:
    receipt = _scan_receipt(
        source_packet_id_or_none=None,
        source_packet_path_or_none=None,
    )
    with pytest.raises(TikTokCreatorDiscoveryFrontierError) as exc_info:
        validate_tiktok_creator_discovery_scan_receipt(receipt)
    assert exc_info.value.code == "missing_source_packet_pointer"


def test_cloakbrowser_parent_packet_requires_suggested_attempt_status() -> None:
    receipt = _scan_receipt(
        suggested_accounts_capture_status="tiktok_suggested_accounts_not_started",
        source_packet_id_or_none=None,
        source_packet_path_or_none=None,
    )
    with pytest.raises(TikTokCreatorDiscoveryFrontierError) as exc_info:
        validate_tiktok_creator_discovery_scan_receipt(receipt)
    assert exc_info.value.code == "suggested_accounts_required_after_cloakbrowser_parent_grid"


def test_cloakbrowser_parent_packet_allows_suggested_blocked_or_empty_status() -> None:
    receipt = _scan_receipt(
        suggested_accounts_capture_status="tiktok_suggested_accounts_blocked_or_empty_visible_outcome",
        source_packet_id_or_none=None,
        source_packet_path_or_none=None,
        suggested_accounts_observed=0,
        caps_applied={
            "root_profiles": 1,
            "suggested_accounts_observed": 0,
            "candidate_profiles_opened": 0,
            "screenshots_emitted_to_chat": 0,
        },
    )
    validate_tiktok_creator_discovery_scan_receipt(receipt)


def test_scan_receipt_rejects_browser_close() -> None:
    receipt = _scan_receipt(browser_closed_by_runner=True)
    with pytest.raises(TikTokCreatorDiscoveryFrontierError) as exc_info:
        validate_tiktok_creator_discovery_scan_receipt(receipt)
    assert exc_info.value.code == "browser_close_forbidden"


def test_scan_receipt_rejects_second_refresh() -> None:
    receipt = _scan_receipt(
        refresh_attempt_count=2,
        refresh_outcome=RefreshOutcome.CLICKED_ONCE_NO_RECOVERY,
    )
    with pytest.raises(TikTokCreatorDiscoveryFrontierError) as exc_info:
        validate_tiktok_creator_discovery_scan_receipt(receipt)
    assert exc_info.value.code == "refresh_attempt_limit_exceeded"


def test_scan_receipt_rejects_candidate_open_and_screenshot() -> None:
    for field_name, code in (
        ("candidate_profiles_opened", "candidate_profile_open_forbidden"),
        ("screenshots_emitted_to_chat", "screenshot_chat_output_forbidden"),
    ):
        receipt = _scan_receipt(**{field_name: 1})
        with pytest.raises(TikTokCreatorDiscoveryFrontierError) as exc_info:
            validate_tiktok_creator_discovery_scan_receipt(receipt)
        assert exc_info.value.code == code


def test_scan_receipt_allows_one_root_follow_but_rejects_more() -> None:
    validate_tiktok_creator_discovery_scan_receipt(_scan_receipt(follow_unfollow_actions_taken=1))
    receipt = _scan_receipt(follow_unfollow_actions_taken=2)
    with pytest.raises(TikTokCreatorDiscoveryFrontierError) as exc_info:
        validate_tiktok_creator_discovery_scan_receipt(receipt)
    assert exc_info.value.code == "follow_unfollow_limit_exceeded"


def test_scan_receipt_rejects_wrong_schema_version() -> None:
    receipt = _scan_receipt(schema_version="wrong")
    with pytest.raises(TikTokCreatorDiscoveryFrontierError) as exc_info:
        validate_tiktok_creator_discovery_scan_receipt(receipt)
    assert exc_info.value.code == "invalid_scan_receipt_schema_version"


def test_scan_receipt_rejects_unknown_refresh_outcome() -> None:
    receipt = _scan_receipt(refresh_outcome="totally_unknown_outcome")
    with pytest.raises(TikTokCreatorDiscoveryFrontierError) as exc_info:
        validate_tiktok_creator_discovery_scan_receipt(receipt)
    assert exc_info.value.code == "invalid_refresh_outcome"


def test_scan_receipt_rejects_refresh_outcome_attempt_mismatch() -> None:
    # One recorded attempt must carry a clicked-once outcome...
    one_attempt_wrong = _scan_receipt(
        refresh_attempt_count=1,
        refresh_outcome=RefreshOutcome.NOT_NEEDED,
    )
    with pytest.raises(TikTokCreatorDiscoveryFrontierError) as exc_info:
        validate_tiktok_creator_discovery_scan_receipt(one_attempt_wrong)
    assert exc_info.value.code == "refresh_outcome_attempt_mismatch"

    # ...and a clicked-once outcome must not appear with zero recorded attempts.
    zero_attempt_wrong = _scan_receipt(
        refresh_attempt_count=0,
        refresh_outcome=RefreshOutcome.CLICKED_ONCE_RECOVERED,
    )
    with pytest.raises(TikTokCreatorDiscoveryFrontierError) as exc_info:
        validate_tiktok_creator_discovery_scan_receipt(zero_attempt_wrong)
    assert exc_info.value.code == "refresh_outcome_attempt_mismatch"


def test_scan_receipt_rejects_negative_pagination_bound() -> None:
    receipt = _scan_receipt(pagination_bound=-1)
    with pytest.raises(TikTokCreatorDiscoveryFrontierError) as exc_info:
        validate_tiktok_creator_discovery_scan_receipt(receipt)
    assert exc_info.value.code == "invalid_non_negative_int"


def test_scan_receipt_requires_every_named_cap() -> None:
    receipt = _scan_receipt(
        caps_applied={
            "root_profiles": 1,
            "suggested_accounts_observed": 1,
            "candidate_profiles_opened": 0,
            # screenshots_emitted_to_chat intentionally omitted
        }
    )
    with pytest.raises(TikTokCreatorDiscoveryFrontierError) as exc_info:
        validate_tiktok_creator_discovery_scan_receipt(receipt)
    assert exc_info.value.code == "missing_scan_receipt_cap"


def test_scan_receipt_requires_every_exclusion_marker() -> None:
    receipt = _scan_receipt(
        exclusions=(
            "no_candidate_profile_open",
            "no_follow_unfollow_action",
            "no_metric_rollup",
            "no_registry_mutation",
            # no_screenshot marker intentionally omitted
        )
    )
    with pytest.raises(TikTokCreatorDiscoveryFrontierError) as exc_info:
        validate_tiktok_creator_discovery_scan_receipt(receipt)
    assert exc_info.value.code == "missing_scan_receipt_exclusion"


def test_register_builder_adds_scope_limit_residual_without_dropping_user_residuals() -> None:
    register = build_tiktok_creator_discovery_frontier_register(
        scan_receipt=_scan_receipt(),
        suggested_accounts=({"handle": "3whiffs"},),
        prior_register_pointer="docs/review-inputs/example.json#/tiktok_creator_discovery_frontier_register",
        accepted_residuals=("No graph database; JSON registers remain sufficient.",),
    )

    residuals = register["tiktok_creator_discovery_frontier_register"]["accepted_residuals"]
    assert residuals[0] == SUGGESTED_ACCOUNT_FRONTIER_SCOPE_LIMIT_RESIDUAL
    assert "No graph database; JSON registers remain sufficient." in residuals

def test_register_builder_from_receipt_passes_and_keeps_next_runs_unauthorized() -> None:
    register = build_tiktok_creator_discovery_frontier_register(
        scan_receipt=_scan_receipt(),
        suggested_accounts=(
            {"handle": "3whiffs", "display_name_or_none": "Jonah | 3Whiffs Fragrance"},
            SuggestedAccountObservation(handle="calcologne", display_name_or_none="Cal Cologne"),
        ),
        prior_register_pointer="docs/review-inputs/example.json#/tiktok_creator_discovery_frontier_register",
        accepted_residuals=("No graph database; JSON registers remain sufficient.",),
    )
    validate_tiktok_creator_discovery_frontier_register(register)
    wrapper = register["tiktok_creator_discovery_frontier_register"]
    candidate_handles = {node["handle_or_none"] for node in wrapper["nodes"]}
    assert {"3whiffs", "calcologne"}.issubset(candidate_handles)
    assert all(envelope["execution_authorized"] is False for envelope in wrapper["next_run_envelopes"])
    assert all(
        edge["edge_type"] in {"discovered_from_run", "platform_suggested_account_relation"}
        for edge in wrapper["edges"]
    )


def _decision(**overrides) -> dict:
    fields = dict(
        decision_id="decision_promote_3whiffs",
        selected_node_id=_CANDIDATE_NODE_ID,
        projection_decision="promote",
        frontier_selection_reason="ranked_first_by_suggested_overlap",
        frontier_selection_actor="operator",
        frontier_selection_timestamp="2026-07-10T04:00:00Z",
        next_run_id_or_none=None,
        non_claims=list(DEFAULT_TIKTOK_CREATOR_DISCOVERY_FRONTIER_NON_CLAIMS),
    )
    fields.update(overrides)
    return fields


def _receipt_raises_code(receipt: dict, code: str) -> None:
    with pytest.raises(TikTokCreatorDiscoveryFrontierError) as exc_info:
        validate_tiktok_creator_discovery_scan_receipt(receipt)
    assert exc_info.value.code == code


def test_scan_receipt_missing_link_hub_status_raises() -> None:
    receipt = _scan_receipt()
    del receipt["link_hub_capture_status"]
    _receipt_raises_code(receipt, "missing_link_hub_capture_status")


def test_scan_receipt_missing_link_hub_url_key_raises() -> None:
    receipt = _scan_receipt()
    del receipt["link_hub_url_or_none"]
    _receipt_raises_code(receipt, "missing_link_hub_url_or_none")


def test_scan_receipt_invalid_link_hub_status_raises() -> None:
    receipt = _scan_receipt(link_hub_capture_status="skipped")
    _receipt_raises_code(receipt, "invalid_link_hub_capture_status")


def test_scan_receipt_captured_link_hub_requires_url() -> None:
    receipt = _scan_receipt(link_hub_url_or_none=None)
    _receipt_raises_code(receipt, "missing_link_hub_url")


def test_scan_receipt_none_visible_link_hub_rejects_url() -> None:
    receipt = _scan_receipt(link_hub_capture_status=LinkHubOutcome.NONE_VISIBLE)
    _receipt_raises_code(receipt, "link_hub_url_contradicts_none_visible")


def test_scan_receipt_explicit_link_hub_outcomes_pass() -> None:
    for status in (LinkHubOutcome.BLOCKED, LinkHubOutcome.DEFERRED_NOT_AUTHORIZED):
        validate_tiktok_creator_discovery_scan_receipt(
            _scan_receipt(link_hub_capture_status=status, link_hub_url_or_none=None)
        )
    validate_tiktok_creator_discovery_scan_receipt(
        _scan_receipt(
            link_hub_capture_status=LinkHubOutcome.NONE_VISIBLE, link_hub_url_or_none=None
        )
    )


def test_promote_decision_without_registry_preflight_raises() -> None:
    register = _register(frontier_decisions=[_decision()])
    _raises_code(register, "promote_requires_registry_preflight")


def test_promote_decision_with_registry_preflight_passes() -> None:
    nodes = [
        _node(_RUN_NODE_ID, FrontierNodeType.RUN, None).to_dict(),
        _node(_SEED_NODE_ID, FrontierNodeType.TIKTOK_CREATOR_SEED, "fragranceknowledge").to_dict(),
        _node(
            _CANDIDATE_NODE_ID,
            FrontierNodeType.TIKTOK_CREATOR_CANDIDATE,
            "3whiffs",
            registry_preflight_status_or_none="no_exact_string_seen_in_registry_json",
        ).to_dict(),
    ]
    register = _register(nodes=nodes, frontier_decisions=[_decision()])
    validate_tiktok_creator_discovery_frontier_register(register)


def test_non_promote_decision_without_preflight_passes() -> None:
    register = _register(frontier_decisions=[_decision(projection_decision="hold")])
    validate_tiktok_creator_discovery_frontier_register(register)


def test_lake_writer_appends_register_keyed_to_parent_grid_packet(tmp_path) -> None:
    from data_lake.root import DataLakeRoot
    from capture_spine.tiktok_creator_discovery_frontier.register_lake_writer import (
        write_tiktok_creator_discovery_frontier_register,
    )

    root = DataLakeRoot.for_test(tmp_path / "lake")
    register = _register()
    written = write_tiktok_creator_discovery_frontier_register(
        register, root, record_id="register_example.json"
    )
    assert written.is_file()
    assert json.loads(written.read_text(encoding="utf-8")) == register
    written_posix = written.as_posix()
    assert "/derived/" in written_posix
    assert "/01KWYMDCZMSB4S5HBERVBYJQNG/" in written_posix
    assert "/tiktok_creator_discovery_frontier/" in written_posix


def test_lake_writer_requires_parent_grid_anchor(tmp_path) -> None:
    from data_lake.root import DataLakeRoot
    from capture_spine.tiktok_creator_discovery_frontier.register_lake_writer import (
        write_tiktok_creator_discovery_frontier_register,
    )

    root = DataLakeRoot.for_test(tmp_path / "lake")
    register = _register()
    provenance = dict(register["tiktok_creator_discovery_frontier_register"]["provenance"])
    provenance["parent_grid_packet_id_or_none"] = None
    provenance["parent_grid_packet_path_or_none"] = None
    register["tiktok_creator_discovery_frontier_register"]["provenance"] = provenance
    with pytest.raises(TikTokCreatorDiscoveryFrontierError) as exc_info:
        write_tiktok_creator_discovery_frontier_register(
            register, root, record_id="register_example.json"
        )
    assert exc_info.value.code == "missing_parent_grid_packet_anchor"
