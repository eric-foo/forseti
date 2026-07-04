from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from capture_spine.reddit_graph_frontier.models import (
    DEFAULT_GRAPH_FRONTIER_NON_CLAIMS,
    GRAPH_FRONTIER_REGISTER_SCHEMA_VERSION,
    FrontierDecision,
    FrontierEdge,
    FrontierEdgeType,
    FrontierNode,
    FrontierNodeType,
    NextRunEnvelope,
)
from capture_spine.reddit_graph_frontier.validation import (
    validate_graph_frontier_register,
    validate_next_run_envelope,
)


def build_graph_frontier_register(
    *,
    register_id: str,
    candidate_intake_output: Mapping[str, Any],
    access_mode: str,
    source_policy_posture: str,
    prior_register_pointer: str | None = None,
    frontier_decisions: list[FrontierDecision] | None = None,
) -> dict[str, Any]:
    intake = candidate_intake_output["reddit_candidate_url_intake"]
    envelope = intake["envelope"]
    provenance = intake["provenance"]
    run_id = envelope["run_id"]
    caps = dict(provenance["caps_applied"])
    exclusions = tuple(provenance.get("exclusions_applied", ()))
    stop_reason = provenance["stop_reason"]
    timestamp = provenance["timestamp"]
    method_category = provenance["method_category"]
    sort_order = provenance.get("sort_order")
    time_window = provenance.get("time_window_days")
    query_or_seed = envelope.get("declared_topic_theme_query") or ",".join(envelope.get("seed_subreddits", ()))

    run_node = FrontierNode(
        node_id=f"run:{run_id}",
        node_type=FrontierNodeType.RUN,
        run_id=run_id,
        source_surface=provenance["source_surface"],
        source_url_or_locator=provenance["query_or_listing_path"],
        query_or_seed=query_or_seed,
        timestamp=timestamp,
        method_category=method_category,
        access_mode=access_mode,
        caps_applied=caps,
        exclusions=exclusions,
        stop_reason=stop_reason,
        prior_pointer_or_none=prior_register_pointer,
        sort_order_or_none=sort_order,
        time_window_or_none=time_window,
    )
    nodes = [run_node]
    edges: list[FrontierEdge] = []

    for row in intake.get("candidate_subreddits", []):
        node = _subreddit_node(row, run_node, access_mode, caps, exclusions, stop_reason)
        nodes.append(node)
        edges.append(_edge_from_run(run_node, node, FrontierEdgeType.DISCOVERED_FROM_RUN))
        edges.append(_edge_from_run(run_node, node, _surface_edge_type(row.get("source_surface"))))

    for row in intake.get("candidate_threads", []):
        node = _thread_node(row, run_node, access_mode, caps, exclusions, stop_reason)
        nodes.append(node)
        edges.append(_edge_from_run(run_node, node, FrontierEdgeType.DISCOVERED_FROM_RUN))
        edges.append(_edge_from_run(run_node, node, _surface_edge_type(row.get("source_surface"))))

    for row in intake.get("outbound_urls", []):
        node = _outbound_node(row, run_node, access_mode, caps, exclusions, stop_reason)
        nodes.append(node)
        edges.append(_edge_from_run(run_node, node, FrontierEdgeType.DISCOVERED_FROM_RUN))
        edges.append(_edge_from_run(run_node, node, FrontierEdgeType.OUTBOUND_LINK_RELATION))

    register = {
        "reddit_graph_frontier_register": {
            "schema_version": GRAPH_FRONTIER_REGISTER_SCHEMA_VERSION,
            "register_id": register_id,
            "source_intake_run_id": run_id,
            "source_policy_posture": source_policy_posture,
            "nodes": [node.to_dict() for node in nodes],
            "edges": [edge.to_dict() for edge in edges],
            "frontier_decisions": [
                decision.to_dict() for decision in (frontier_decisions or [])
            ],
            "provenance": {
                "source_surface": provenance["source_surface"],
                "query_or_seed": query_or_seed,
                "timestamp": timestamp,
                "method_category": method_category,
                "access_mode": access_mode,
                "caps_applied": caps,
                "exclusions": list(exclusions),
                "stop_reason": stop_reason,
                "prior_register_pointer_or_none": prior_register_pointer,
            },
            "non_claims": list(DEFAULT_GRAPH_FRONTIER_NON_CLAIMS),
        }
    }
    validate_graph_frontier_register(register)
    return register


def prepare_next_bounded_run_envelope(
    *,
    register: Mapping[str, Any],
    selected_node_id: str,
    next_run_id: str,
    declared_topic_theme_or_query: str,
    candidate_surface_allowlist: tuple[str, ...],
    caps: dict[str, int],
    exclusions: tuple[str, ...],
    access_mode: str,
    source_policy_posture: str,
    stop_condition: str,
    non_commercial_posture: str = "pre_commercial",
) -> dict[str, Any]:
    wrapper = register["reddit_graph_frontier_register"]
    nodes = {node["node_id"]: node for node in wrapper["nodes"]}
    selected_node = nodes[selected_node_id]
    envelope = NextRunEnvelope(
        next_run_id=next_run_id,
        selected_node_id=selected_node_id,
        prior_register_pointer=f"{wrapper['register_id']}#{selected_node_id}",
        declared_topic_theme_or_query=declared_topic_theme_or_query,
        declared_seed_or_surface=str(selected_node.get("candidate_value_or_none") or selected_node["source_url_or_locator"]),
        candidate_surface_allowlist=candidate_surface_allowlist,
        caps=caps,
        exclusions=exclusions,
        access_mode=access_mode,
        source_policy_posture=source_policy_posture,
        stop_condition=stop_condition,
        non_commercial_posture=non_commercial_posture,
    ).to_dict()
    validate_next_run_envelope(envelope)
    return envelope


def _subreddit_node(
    row: Mapping[str, Any],
    run_node: FrontierNode,
    access_mode: str,
    caps: dict[str, int],
    exclusions: tuple[str, ...],
    stop_reason: str,
) -> FrontierNode:
    subreddit = str(row["candidate_subreddit"])
    return FrontierNode(
        node_id=f"subreddit:{row['run_id']}:{subreddit.lower()}",
        node_type=FrontierNodeType.SUBREDDIT_CANDIDATE,
        run_id=row["run_id"],
        source_surface=row["source_surface"],
        source_url_or_locator=row["source_url"],
        query_or_seed=row["query_or_seed"],
        timestamp=row["timestamp"],
        method_category=row["method_category"],
        access_mode=access_mode,
        caps_applied=caps,
        exclusions=tuple(row.get("exclusion_receipt") or exclusions),
        stop_reason=stop_reason,
        prior_pointer_or_none=run_node.node_id,
        sort_order_or_none=run_node.sort_order_or_none,
        time_window_or_none=run_node.time_window_or_none,
        candidate_value_or_none=subreddit,
        visible_subscriber_count_or_none=row.get("visible_subscriber_count_or_none"),
        visible_active_user_count_or_none=row.get("visible_active_user_count_or_none"),
        visible_volume_signal_absent_reason_or_none=row.get("visible_volume_signal_absent_reason_or_none"),
    )


def _thread_node(
    row: Mapping[str, Any],
    run_node: FrontierNode,
    access_mode: str,
    caps: dict[str, int],
    exclusions: tuple[str, ...],
    stop_reason: str,
) -> FrontierNode:
    url = str(row["candidate_thread_url"])
    return FrontierNode(
        node_id=f"thread:{row['run_id']}:{_stable_value(url)}",
        node_type=FrontierNodeType.THREAD_URL_CANDIDATE,
        run_id=row["run_id"],
        source_surface=row["source_surface"],
        source_url_or_locator=url,
        query_or_seed=row["query_or_seed"],
        timestamp=row["timestamp"],
        method_category=row["method_category"],
        access_mode=access_mode,
        caps_applied=caps,
        exclusions=tuple(row.get("exclusion_receipt") or exclusions),
        stop_reason=stop_reason,
        prior_pointer_or_none=run_node.node_id,
        sort_order_or_none=run_node.sort_order_or_none,
        time_window_or_none=run_node.time_window_or_none,
        candidate_value_or_none=url,
    )


def _outbound_node(
    row: Mapping[str, Any],
    run_node: FrontierNode,
    access_mode: str,
    caps: dict[str, int],
    exclusions: tuple[str, ...],
    stop_reason: str,
) -> FrontierNode:
    url = str(row["outbound_url"])
    return FrontierNode(
        node_id=f"outbound:{row['run_id']}:{_stable_value(url)}",
        node_type=FrontierNodeType.OUTBOUND_URL_CANDIDATE,
        run_id=row["run_id"],
        source_surface=row["source_surface"],
        source_url_or_locator=url,
        query_or_seed=row.get("originating_reddit_url", ""),
        timestamp=row["timestamp"],
        method_category=row["method_category"],
        access_mode=access_mode,
        caps_applied=caps,
        exclusions=tuple(row.get("exclusion_receipt") or exclusions),
        stop_reason=stop_reason,
        prior_pointer_or_none=run_node.node_id,
        sort_order_or_none=run_node.sort_order_or_none,
        time_window_or_none=run_node.time_window_or_none,
        candidate_value_or_none=url,
    )


def _edge_from_run(run_node: FrontierNode, node: FrontierNode, edge_type: FrontierEdgeType) -> FrontierEdge:
    return FrontierEdge(
        edge_id=f"{edge_type.value}:{run_node.node_id}->{node.node_id}",
        edge_type=edge_type,
        from_node_id=run_node.node_id,
        to_node_id=node.node_id,
        run_id=run_node.run_id,
        source_surface=node.source_surface,
        timestamp=node.timestamp,
        method_category=node.method_category,
        stop_reason=node.stop_reason,
        prior_pointer_or_none=run_node.prior_pointer_or_none,
    )


def _surface_edge_type(source_surface: object) -> FrontierEdgeType:
    match str(source_surface):
        case "cross_post":
            return FrontierEdgeType.CROSSPOST_RELATION
        case "related_subreddit":
            return FrontierEdgeType.RELATED_SUBREDDIT_RELATION
        case "recommendation":
            return FrontierEdgeType.RECOMMENDATION_RELATION
        case "more_like_this":
            return FrontierEdgeType.MORE_LIKE_THIS_RELATION
        case _:
            return FrontierEdgeType.FOUND_ON_SURFACE


def _stable_value(value: str) -> str:
    return (
        value.lower()
        .replace("https://", "")
        .replace("http://", "")
        .replace("/", "_")
        .replace("?", "_")
        .replace("&", "_")
        .replace("=", "_")
        .strip("_")
    )
