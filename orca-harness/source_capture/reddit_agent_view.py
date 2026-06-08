from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
from typing import Any

from harness_utils import utc_now_z


REDDIT_AGENT_VIEW_SCHEMA_VERSION = "reddit_agent_view_v0"

NON_CLAIMS = [
    "not source capture",
    "not live Reddit access",
    "not canonical artifact replacement",
    "not raw HTML persistence",
    "not Data Capture handoff",
    "not source completeness proof",
    "not ECR, Cleaning, Judgment, fixture admission, or commercial readiness",
]


class RedditAgentViewFailure(ValueError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


def build_reddit_agent_views(
    *,
    input_json_path: Path,
    output_directory: Path,
    full_name: str = "reddit_agent_view_full.json",
    stripped_name: str = "reddit_agent_view_stripped.json",
    receipt_name: str = "reddit_agent_view_receipt.md",
) -> dict[str, str]:
    input_json_path = input_json_path.resolve()
    source = _read_json(input_json_path)
    artifact_type = _detect_artifact_type(source)

    output_directory.mkdir(parents=True, exist_ok=True)
    full_path = output_directory / full_name
    stripped_path = output_directory / stripped_name
    receipt_path = output_directory / receipt_name
    for path in (full_path, stripped_path, receipt_path):
        if path.exists():
            raise RedditAgentViewFailure("output_exists", f"output already exists: {path}")

    stripped_payload = _build_stripped_payload(
        source=source,
        artifact_type=artifact_type,
        input_json_path=input_json_path,
    )
    full_path.write_text(json.dumps(source, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    stripped_path.write_text(
        json.dumps(stripped_payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    receipt_path.write_text(
        _render_receipt(
            artifact=stripped_payload,
            input_json_path=input_json_path,
            full_path=full_path,
            stripped_path=stripped_path,
        ),
        encoding="utf-8",
    )
    return {
        "full_json_path": str(full_path),
        "stripped_json_path": str(stripped_path),
        "receipt_path": str(receipt_path),
        "artifact_type": artifact_type,
    }


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise RedditAgentViewFailure("input_missing", f"input JSON does not exist: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RedditAgentViewFailure("input_not_json", f"input is not valid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise RedditAgentViewFailure("input_not_object", "input JSON must be an object")
    return data


def _detect_artifact_type(source: dict[str, Any]) -> str:
    if isinstance(source.get("reddit_thread_consolidation"), dict):
        return "reddit_thread_consolidation"
    if isinstance(source.get("reddit_candidate_url_intake"), dict):
        return "reddit_candidate_url_intake"
    if isinstance(source.get("reddit_graph_frontier_register"), dict):
        return "reddit_graph_frontier_register"
    raise RedditAgentViewFailure(
        "unsupported_artifact",
        "expected reddit_thread_consolidation, reddit_candidate_url_intake, or reddit_graph_frontier_register",
    )


def _build_stripped_payload(
    *,
    source: dict[str, Any],
    artifact_type: str,
    input_json_path: Path,
) -> dict[str, Any]:
    if artifact_type == "reddit_thread_consolidation":
        stripped = _strip_thread(source["reddit_thread_consolidation"])
    elif artifact_type == "reddit_candidate_url_intake":
        stripped = _strip_candidate_intake(source["reddit_candidate_url_intake"])
    elif artifact_type == "reddit_graph_frontier_register":
        stripped = _strip_graph_frontier(source["reddit_graph_frontier_register"])
    else:
        raise AssertionError(f"unhandled artifact type: {artifact_type}")

    return {
        "reddit_agent_view": {
            "schema_version": REDDIT_AGENT_VIEW_SCHEMA_VERSION,
            "generated_at": utc_now_z(),
            "source_artifact_path": str(input_json_path),
            "source_artifact_type": artifact_type,
            "view_mode": "stripped_agent_context",
            "stripped_profile": "agent_context_v0",
            "stripped": stripped,
            "non_claims": NON_CLAIMS,
        }
    }


def _strip_thread(data: dict[str, Any]) -> dict[str, Any]:
    comments = _list_of_dicts(data.get("comments"))
    author_slots: dict[str, str] = {}
    post = data.get("post", {}) if isinstance(data.get("post"), dict) else {}
    post_author_slot = _author_slot(post.get("author_state"), author_slots)
    stripped_comments = []
    for comment in comments:
        author_slot = _author_slot(comment.get("author_state"), author_slots)
        stripped_comment = {
            "row_id": comment.get("row_id"),
            "comment_id": comment.get("comment_id"),
            "parent_id": comment.get("parent_id"),
            "depth": comment.get("depth"),
            "comment_posture": comment.get("comment_posture"),
            "body_text": comment.get("body_text"),
            "author_slot": author_slot,
        }
        parser_warnings = comment.get("parser_warnings")
        if parser_warnings:
            stripped_comment["parser_warnings"] = parser_warnings
        stripped_comments.append(stripped_comment)

    parser_warning_count = sum(
        len(comment.get("parser_warnings", []))
        for comment in comments
        if isinstance(comment.get("parser_warnings"), list)
    )
    return {
        "thread": data.get("thread", {}),
        "post": {
            "body_text": post.get("body_text"),
            "author_slot": post_author_slot,
        },
        "comments": stripped_comments,
        "counts": data.get("counts", {}),
        "warnings_count": len(_list(data.get("warnings"))),
        "limitations_count": len(_list(data.get("limitations"))),
        "parser_warning_count": parser_warning_count,
        "author_slot_count": len(author_slots),
        "omitted_field_groups": [
            "packet-level provenance and hashes",
            "post score and timestamp state",
            "per-comment provenance",
            "per-comment direct author handles",
            "per-comment score and timestamp state",
            "repeated non-claims payload",
        ],
    }


def _strip_candidate_intake(data: dict[str, Any]) -> dict[str, Any]:
    envelope = data.get("envelope", {}) if isinstance(data.get("envelope"), dict) else {}
    provenance = data.get("provenance", {}) if isinstance(data.get("provenance"), dict) else {}
    rows: list[dict[str, Any]] = []
    for row in _list_of_dicts(data.get("candidate_subreddits")):
        rows.append(
            {
                "candidate_type": "subreddit",
                "candidate_value": row.get("candidate_subreddit"),
                "candidate_url_or_locator": row.get("source_url"),
                "source_surface": row.get("source_surface"),
                "allowed_downstream_use": row.get("allowed_downstream_use"),
                "intake_status": row.get("capture_unit_intake_status"),
                "same_run_traversal_authorized": row.get("same_run_traversal_authorized"),
                "visible_subscriber_count_or_none": row.get("visible_subscriber_count_or_none"),
                "visible_active_user_count_or_none": row.get("visible_active_user_count_or_none"),
            }
        )
    for row in _list_of_dicts(data.get("candidate_threads")):
        rows.append(
            {
                "candidate_type": "thread_url",
                "candidate_value": row.get("candidate_thread_url"),
                "candidate_url_or_locator": row.get("candidate_thread_url"),
                "source_surface": row.get("source_surface"),
                "allowed_downstream_use": row.get("allowed_downstream_use"),
                "intake_status": row.get("capture_unit_intake_status"),
                "same_run_traversal_authorized": row.get("same_run_traversal_authorized"),
            }
        )
    for row in _list_of_dicts(data.get("outbound_urls")):
        rows.append(
            {
                "candidate_type": "outbound_url",
                "candidate_value": row.get("outbound_url"),
                "candidate_url_or_locator": row.get("outbound_url"),
                "source_surface": row.get("source_surface"),
                "allowed_downstream_use": row.get("allowed_downstream_use"),
                "requires_separate_source_family_intake": row.get(
                    "requires_separate_source_family_intake"
                ),
            }
        )
    return {
        "run": {
            "run_id": envelope.get("run_id") or provenance.get("run_id"),
            "declared_topic_theme_query": envelope.get("declared_topic_theme_query"),
            "source_surface": provenance.get("source_surface"),
            "stop_reason": provenance.get("stop_reason"),
            "coverage_claim": envelope.get("coverage_claim"),
            "caps_applied": provenance.get("caps_applied"),
            "exclusions": provenance.get("exclusions_applied"),
        },
        "candidates": rows,
        "counts": provenance.get("row_counts", {}),
        "omitted_field_groups": [
            "per-row exclusion receipts",
            "per-row method category repeats",
            "per-row timestamps",
            "live-run receipt details",
            "repeated non-claims payload",
        ],
    }


def _strip_graph_frontier(data: dict[str, Any]) -> dict[str, Any]:
    nodes = [
        {
            "node_id": node.get("node_id"),
            "node_type": node.get("node_type"),
            "candidate_value_or_none": node.get("candidate_value_or_none"),
            "source_surface": node.get("source_surface"),
            "source_url_or_locator": node.get("source_url_or_locator"),
            "stop_reason": node.get("stop_reason"),
            "run_id": node.get("run_id"),
            "visible_subscriber_count_or_none": node.get("visible_subscriber_count_or_none"),
            "visible_active_user_count_or_none": node.get("visible_active_user_count_or_none"),
        }
        for node in _list_of_dicts(data.get("nodes"))
    ]
    edges = [
        {
            "edge_type": edge.get("edge_type"),
            "from_node_id": edge.get("from_node_id"),
            "to_node_id": edge.get("to_node_id"),
            "source_surface": edge.get("source_surface"),
            "stop_reason": edge.get("stop_reason"),
        }
        for edge in _list_of_dicts(data.get("edges"))
    ]
    decisions = [
        {
            "decision": decision.get("decision"),
            "selected_node_id": decision.get("selected_node_id"),
            "frontier_selection_reason": decision.get("frontier_selection_reason"),
            "next_run_id_or_none": decision.get("next_run_id_or_none"),
        }
        for decision in _list_of_dicts(data.get("frontier_decisions"))
    ]
    node_values = [
        node["candidate_value_or_none"]
        for node in nodes
        if isinstance(node.get("candidate_value_or_none"), str)
    ]
    repeated = {
        value: count
        for value, count in sorted(Counter(value.lower() for value in node_values).items())
        if count > 1
    }
    provenance = data.get("provenance")
    if not isinstance(provenance, dict):
        provenance = {}
    return {
        "register_id": data.get("register_id"),
        "source_intake_run_id": data.get("source_intake_run_id"),
        "source_policy_posture": data.get("source_policy_posture"),
        "caps_applied": provenance.get("caps_applied"),
        "exclusions": provenance.get("exclusions"),
        "nodes": nodes,
        "edges": edges,
        "frontier_decisions": decisions,
        "counts": {
            "nodes": len(nodes),
            "edges": len(edges),
            "frontier_decisions": len(decisions),
        },
        "repeated_candidate_values": repeated,
        "omitted_field_groups": [
            "per-node cap and exclusion repeats",
            "per-node method and timestamp repeats",
            "per-node repeated non-claims payload",
            "per-edge generated identifiers",
            "per-edge method and timestamp repeats",
            "per-edge repeated non-claims payload",
            "frontier-decision generated identifiers and timestamps",
            "frontier-decision repeated non-claims payload",
            "register provenance detail beyond run-level caps and exclusions",
            "top-level repeated non-claims payload",
        ],
    }


def _author_slot(author: object, slots: dict[str, str]) -> str | None:
    if not isinstance(author, str) or not author.strip():
        return None
    if author not in slots:
        slots[author] = f"author_{len(slots) + 1:03d}"
    return slots[author]


def _list(value: object) -> list[Any]:
    return value if isinstance(value, list) else []


def _list_of_dicts(value: object) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _render_receipt(
    *,
    artifact: dict[str, Any],
    input_json_path: Path,
    full_path: Path,
    stripped_path: Path,
) -> str:
    view = artifact["reddit_agent_view"]
    stripped = view["stripped"]
    counts = stripped.get("counts", {}) if isinstance(stripped, dict) else {}
    lines = [
        "# Reddit Agent View Receipt",
        "",
        f"Input JSON: `{input_json_path}`",
        f"Source artifact type: `{view['source_artifact_type']}`",
        f"Full state: `{full_path}`",
        f"Stripped state: `{stripped_path}`",
        f"Stripped profile: `{view['stripped_profile']}`",
        "",
        "Counts:",
    ]
    if isinstance(counts, dict) and counts:
        lines.extend(f"- {key}: {value}" for key, value in counts.items())
    else:
        lines.append("- none")
    lines.extend(["", "Non-claims:"])
    lines.extend(f"- {non_claim}" for non_claim in view["non_claims"])
    return "\n".join(lines) + "\n"
