"""Build TikTok Creator Discovery Frontier registers from bounded scan receipts."""
from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from typing import Any

from capture_spine.tiktok_creator_discovery_frontier.models import (
    DEFAULT_TIKTOK_CREATOR_DISCOVERY_FRONTIER_NON_CLAIMS,
    TIKTOK_CREATOR_DISCOVERY_FRONTIER_REGISTER_SCHEMA_VERSION,
    FrontierEdge,
    FrontierEdgeType,
    FrontierNode,
    FrontierNodeType,
    NextRunEnvelope,
    SuggestedAccountObservation,
)
from capture_spine.tiktok_creator_discovery_frontier.validation import (
    validate_tiktok_creator_discovery_frontier_register,
    validate_tiktok_creator_discovery_scan_receipt,
)


def build_tiktok_creator_discovery_frontier_register(
    *,
    scan_receipt: Mapping[str, Any],
    suggested_accounts: Sequence[Mapping[str, Any] | SuggestedAccountObservation],
    prior_register_pointer: str,
    accepted_residuals: Sequence[str] = (),
) -> dict[str, Any]:
    """Return a validated frontier register from receipt-backed suggested rows.

    The builder is intentionally network-free. It turns already-observed public
    rows into weak TikTok discovery nodes/edges and unauthorized next-run
    envelopes. It does not inspect TikTok, mutate Creator Registry, infer
    country, or produce metrics.
    """
    validate_tiktok_creator_discovery_scan_receipt(scan_receipt)
    root_seed = _root_seed(scan_receipt)
    timestamp = _required_str(scan_receipt, "captured_at_utc")
    run_id = _required_str(scan_receipt, "run_id")
    source_surface = _required_str(scan_receipt, "source_surface")
    method_mode = _required_str(scan_receipt, "method_mode")
    access_mode = _required_str(scan_receipt, "access_mode")
    stop_reason = _required_str(scan_receipt, "stop_reason")
    caps_applied = dict(_required_mapping(scan_receipt, "caps_applied"))
    exclusions = tuple(str(item) for item in _required_sequence(scan_receipt, "exclusions"))
    seed_handle = _required_str(root_seed, "handle")
    seed_url = _required_str(root_seed, "url")
    run_node_id = _node_id("run", run_id)
    seed_node_id = _node_id("seed_tiktok", seed_handle)

    nodes: list[dict[str, Any]] = [
        FrontierNode(
            node_id=run_node_id,
            node_type=FrontierNodeType.RUN,
            platform="tiktok",
            handle_or_none=None,
            display_name_or_none=None,
            source_url_or_locator=seed_url,
            run_id=run_id,
            source_surface=source_surface,
            timestamp=timestamp,
            method_mode=method_mode,
            access_mode=access_mode,
            caps_applied=caps_applied,
            exclusions=exclusions,
            stop_reason=stop_reason,
            registry_preflight_status_or_none=None,
            platform_capture_status=str(scan_receipt["parent_profile_capture_status"]),
            cross_platform_graph_status="not_started",
        ).to_dict(),
        FrontierNode(
            node_id=seed_node_id,
            node_type=FrontierNodeType.TIKTOK_CREATOR_SEED,
            platform="tiktok",
            handle_or_none=seed_handle,
            display_name_or_none=None,
            source_url_or_locator=seed_url,
            run_id=run_id,
            source_surface=source_surface,
            timestamp=timestamp,
            method_mode=method_mode,
            access_mode=access_mode,
            caps_applied=caps_applied,
            exclusions=exclusions,
            stop_reason="seed_profile_observed_and_suggested_accounts_extracted",
            registry_preflight_status_or_none=None,
            platform_capture_status=str(scan_receipt["parent_profile_capture_status"]),
            cross_platform_graph_status="not_started",
        ).to_dict(),
    ]
    edges: list[dict[str, Any]] = [
        FrontierEdge(
            edge_id=_edge_id("run_to_seed", run_node_id, seed_node_id),
            edge_type=FrontierEdgeType.DISCOVERED_FROM_RUN,
            from_node_id=run_node_id,
            to_node_id=seed_node_id,
            run_id=run_id,
            source_surface=source_surface,
            source_packet_id_or_none=_optional_str(scan_receipt, "parent_grid_packet_id_or_none"),
            observed_sections=("seed_profile",),
            timestamp=timestamp,
            method_mode=method_mode,
            stop_reason="seed_profile_observed",
            confidence="seed_surface_observed",
        ).to_dict()
    ]
    next_run_envelopes: list[dict[str, Any]] = []
    seen_candidate_ids: set[str] = set()

    for account in suggested_accounts:
        observation = _observation_dict(account)
        handle = _required_str(observation, "handle")
        candidate_node_id = _node_id("candidate_tiktok", handle)
        if candidate_node_id in seen_candidate_ids:
            continue
        seen_candidate_ids.add(candidate_node_id)
        source_url = observation.get("source_url_or_locator") or f"https://www.tiktok.com/@{handle}"
        nodes.append(
            FrontierNode(
                node_id=candidate_node_id,
                node_type=FrontierNodeType.TIKTOK_CREATOR_CANDIDATE,
                platform="tiktok",
                handle_or_none=handle,
                display_name_or_none=_optional_str(observation, "display_name_or_none"),
                source_url_or_locator=str(source_url),
                run_id=run_id,
                source_surface=source_surface,
                timestamp=timestamp,
                method_mode=method_mode,
                access_mode=access_mode,
                caps_applied=caps_applied,
                exclusions=exclusions,
                stop_reason="candidate_profile_not_opened_target_only",
                registry_preflight_status_or_none=_optional_str(
                    observation, "registry_preflight_status_or_none"
                ),
                platform_capture_status=str(
                    observation.get(
                        "platform_capture_status",
                        "tiktok_suggested_account_target_only_not_profile_captured",
                    )
                ),
                cross_platform_graph_status=str(observation.get("cross_platform_graph_status", "not_started")),
            ).to_dict()
        )
        observed_sections = tuple(
            str(item) for item in observation.get("observed_sections", ("suggested_accounts",))
        )
        edges.append(
            FrontierEdge(
                edge_id=_edge_id("seed_to_candidate", seed_node_id, candidate_node_id),
                edge_type=FrontierEdgeType.PLATFORM_SUGGESTED_ACCOUNT_RELATION,
                from_node_id=seed_node_id,
                to_node_id=candidate_node_id,
                run_id=run_id,
                source_surface=source_surface,
                source_packet_id_or_none=_optional_str(scan_receipt, "source_packet_id_or_none"),
                observed_sections=observed_sections,
                timestamp=timestamp,
                method_mode=method_mode,
                stop_reason=stop_reason,
                confidence=str(observation.get("confidence", "weak_platform_suggestion_only")),
            ).to_dict()
        )
        next_run_envelopes.append(
            NextRunEnvelope(
                next_run_id=f"tiktok_creator_scan_{_slug(handle)}_next_01",
                selected_node_id=candidate_node_id,
                prior_register_pointer=prior_register_pointer,
                declared_seed_or_surface=str(source_url),
                candidate_surface_allowlist=(
                    "tiktok_creator_profile",
                    "tiktok_creator_profile_grid",
                    "source_visible_bio_link_hub",
                ),
                caps={
                    "profiles": 1,
                    "profile_grid_observations": 1,
                    "link_hubs": 1,
                    "suggested_accounts_expansion_depth": 0,
                    "screenshots_emitted_to_chat": 0,
                },
                exclusions=(
                    "no_same_run_snowball",
                    "no_follow_unfollow",
                    "no_contact_enrichment",
                    "no_private_identity_inference",
                    "no_metric_rollup",
                    "no_registry_mutation_without_preflight",
                ),
                method_mode="owner_launched_existing_session_or_capture_lane_route_required",
                access_mode="not_started",
                source_policy_posture="requires_current_tiktok_capture_lane_posture_check_before_execution",
                stop_condition="stop_after_parent_profile_grid_and_source_visible_link_hub_or_on_access_friction",
            ).to_dict()
        )

    register = {
        "tiktok_creator_discovery_frontier_register": {
            "schema_version": TIKTOK_CREATOR_DISCOVERY_FRONTIER_REGISTER_SCHEMA_VERSION,
            "register_id": _required_str(scan_receipt, "register_id"),
            "source_run_id": run_id,
            "root_seed": root_seed,
            "provenance": {
                "source_surface": source_surface,
                "source_packet_id_or_none": _optional_str(scan_receipt, "source_packet_id_or_none"),
                "source_packet_path_or_none": _optional_str(scan_receipt, "source_packet_path_or_none"),
                "parent_grid_packet_id_or_none": _optional_str(scan_receipt, "parent_grid_packet_id_or_none"),
                "parent_grid_packet_path_or_none": _optional_str(scan_receipt, "parent_grid_packet_path_or_none"),
                "captured_at_utc": timestamp,
                "method_mode": method_mode,
                "access_mode": access_mode,
                "caps_applied": caps_applied,
                "stop_reason": stop_reason,
            },
            "nodes": nodes,
            "edges": edges,
            "frontier_decisions": [],
            "next_run_envelopes": next_run_envelopes,
            "accepted_residuals": list(accepted_residuals),
            "non_claims": list(DEFAULT_TIKTOK_CREATOR_DISCOVERY_FRONTIER_NON_CLAIMS),
        }
    }
    validate_tiktok_creator_discovery_frontier_register(register)
    return register


def _observation_dict(value: Mapping[str, Any] | SuggestedAccountObservation) -> Mapping[str, Any]:
    if isinstance(value, SuggestedAccountObservation):
        return value.to_dict()
    return value


def _root_seed(scan_receipt: Mapping[str, Any]) -> dict[str, str]:
    seed = _required_mapping(scan_receipt, "root_seed")
    return {"platform": str(seed["platform"]), "handle": str(seed["handle"]), "url": str(seed["url"])}


def _node_id(prefix: str, value: str) -> str:
    return f"{prefix}_{_slug(value)}"


def _edge_id(prefix: str, from_node_id: str, to_node_id: str) -> str:
    return f"edge_{prefix}_{_slug(from_node_id)}_{_slug(to_node_id)}"


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", value.strip().lower()).strip("_")
    if not slug:
        raise ValueError("cannot build frontier id from empty value")
    return slug


def _required_str(value: Mapping[str, Any], key: str) -> str:
    item = value.get(key)
    if not isinstance(item, str) or not item.strip():
        raise ValueError(f"{key} must be a non-empty string")
    return item


def _optional_str(value: Mapping[str, Any], key: str) -> str | None:
    item = value.get(key)
    if item is None:
        return None
    if not isinstance(item, str) or not item.strip():
        raise ValueError(f"{key} must be a non-empty string or None")
    return item


def _required_mapping(value: Mapping[str, Any], key: str) -> Mapping[str, Any]:
    item = value.get(key)
    if not isinstance(item, Mapping):
        raise ValueError(f"{key} must be a mapping")
    return item


def _required_sequence(value: Mapping[str, Any], key: str) -> Sequence[Any]:
    item = value.get(key)
    if not isinstance(item, Sequence) or isinstance(item, (str, bytes, bytearray)):
        raise ValueError(f"{key} must be a sequence")
    return item
