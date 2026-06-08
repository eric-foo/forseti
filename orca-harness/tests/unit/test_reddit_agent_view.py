from __future__ import annotations

import json
import shutil
import uuid
from pathlib import Path

import pytest

from source_capture.reddit_agent_view import RedditAgentViewFailure, build_reddit_agent_views


@pytest.fixture
def scratch_dir() -> Path:
    root = Path(__file__).resolve().parents[2] / "_test_runs"
    path = root / f"reddit_agent_view_{uuid.uuid4().hex}"
    path.mkdir(parents=True)
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


def test_thread_view_writes_full_copy_and_stripped_agent_context(scratch_dir: Path) -> None:
    source_path = scratch_dir / "reddit_thread_consolidation.json"
    source = {
        "reddit_thread_consolidation": {
            "schema_version": "reddit_thread_consolidation_v0",
            "source_packet": {"packet_id": "packet_1", "raw_html_sha256": "abc"},
            "thread": {
                "thread_id": "1abc",
                "subreddit": "SEO",
                "title": "React SEO issue",
                "permalink": "/r/SEO/comments/1abc/react_seo_issue/",
            },
            "post": {
                "author_state": "poster",
                "timestamp_state": "yesterday",
                "score_state": "12 points",
                "body_text": "Google sees <div id=\"root\"></div>",
                "provenance": {"packet_path": "packet"},
            },
            "comments": [
                {
                    "row_id": "comment_0001",
                    "comment_id": "c1",
                    "parent_id": None,
                    "depth": 0,
                    "author_state": "helper",
                    "timestamp_state": "today",
                    "score_state": "1 point",
                    "body_text": "Use SSR or prerendering.",
                    "comment_posture": "present",
                    "provenance": {"packet_path": "packet"},
                    "parser_warnings": [],
                },
                {
                    "row_id": "comment_0002",
                    "comment_id": None,
                    "parent_id": "c1",
                    "depth": 1,
                    "author_state": "helper",
                    "timestamp_state": "today",
                    "score_state": "0 points",
                    "body_text": "[removed]",
                    "comment_posture": "collapsed",
                    "provenance": {"packet_path": "packet"},
                    "parser_warnings": ["comment body carried as collapsed"],
                },
            ],
            "counts": {
                "observable_comment_nodes": 2,
                "comments_parsed": 2,
                "comment_postures": {"collapsed": 1, "present": 1},
            },
            "warnings": [],
            "limitations": [],
            "non_claims": ["not live Reddit capture"],
        }
    }
    source_path.write_text(json.dumps(source), encoding="utf-8")

    result = build_reddit_agent_views(input_json_path=source_path, output_directory=scratch_dir / "views")

    full = json.loads(Path(result["full_json_path"]).read_text(encoding="utf-8"))
    stripped = json.loads(Path(result["stripped_json_path"]).read_text(encoding="utf-8"))[
        "reddit_agent_view"
    ]
    assert full == source
    assert stripped["source_artifact_type"] == "reddit_thread_consolidation"
    thread_view = stripped["stripped"]
    assert thread_view["post"]["body_text"] == "Google sees <div id=\"root\"></div>"
    assert thread_view["comments"][0]["body_text"] == "Use SSR or prerendering."
    assert thread_view["comments"][0]["author_slot"] == "author_002"
    assert thread_view["comments"][1]["author_slot"] == "author_002"
    assert "author_state" not in thread_view["comments"][0]
    assert "provenance" not in thread_view["comments"][0]
    assert thread_view["parser_warning_count"] == 1
    assert "not canonical artifact replacement" in stripped["non_claims"]

    receipt = Path(result["receipt_path"]).read_text(encoding="utf-8")
    assert "Source artifact type: `reddit_thread_consolidation`" in receipt


def test_candidate_intake_view_keeps_candidate_rows_without_repeated_receipts(
    scratch_dir: Path,
) -> None:
    source_path = scratch_dir / "reddit_candidate_url_intake.json"
    source_path.write_text(
        json.dumps(
            {
                "reddit_candidate_url_intake": {
                    "envelope": {
                        "run_id": "run_1",
                        "declared_topic_theme_query": "b2b",
                        "coverage_claim": "bounded_probe_only",
                    },
                    "candidate_subreddits": [
                        {
                            "candidate_subreddit": "analytics",
                            "source_url": "https://old.reddit.com/r/analytics/",
                            "source_surface": "related_subreddit",
                            "allowed_downstream_use": "planning_only",
                            "capture_unit_intake_status": "candidate_or_scouting",
                            "same_run_traversal_authorized": False,
                            "visible_subscriber_count_or_none": None,
                            "visible_active_user_count_or_none": None,
                            "exclusion_receipt": ["no_link_following"],
                        }
                    ],
                    "candidate_threads": [],
                    "outbound_urls": [],
                    "provenance": {
                        "run_id": "run_1",
                        "source_surface": "related_subreddit",
                        "stop_reason": "scope_exhausted",
                        "caps_applied": {"max_subreddits": 1},
                        "row_counts": {"candidate_subreddits": 1},
                        "non_claims": ["not Source Capture Packet output"],
                    },
                    "live_run_receipt": {"status_note": "HTTP 200"},
                    "non_claims": ["not Source Capture Packet output"],
                }
            }
        ),
        encoding="utf-8",
    )

    result = build_reddit_agent_views(input_json_path=source_path, output_directory=scratch_dir / "views")

    stripped = json.loads(Path(result["stripped_json_path"]).read_text(encoding="utf-8"))[
        "reddit_agent_view"
    ]["stripped"]
    assert stripped["run"]["run_id"] == "run_1"
    assert stripped["candidates"] == [
        {
            "candidate_type": "subreddit",
            "candidate_value": "analytics",
            "candidate_url_or_locator": "https://old.reddit.com/r/analytics/",
            "source_surface": "related_subreddit",
            "allowed_downstream_use": "planning_only",
            "intake_status": "candidate_or_scouting",
            "same_run_traversal_authorized": False,
            "visible_subscriber_count_or_none": None,
            "visible_active_user_count_or_none": None,
        }
    ]
    assert "per-row exclusion receipts" in stripped["omitted_field_groups"]


def test_graph_frontier_view_keeps_graph_shape_and_drops_repeated_non_claims(
    scratch_dir: Path,
) -> None:
    source_path = scratch_dir / "reddit_graph_frontier_register.json"
    source_path.write_text(
        json.dumps(
            {
                "reddit_graph_frontier_register": {
                    "register_id": "register_1",
                    "source_intake_run_id": "run_1",
                    "source_policy_posture": "candidate-only",
                    "nodes": [
                        {
                            "node_id": "run:run_1",
                            "node_type": "intake_run",
                            "candidate_value_or_none": None,
                            "source_surface": "related_subreddit",
                            "source_url_or_locator": "https://old.reddit.com/r/SEO/",
                            "stop_reason": "scope_exhausted",
                            "run_id": "run_1",
                            "visible_subscriber_count_or_none": None,
                            "visible_active_user_count_or_none": None,
                            "non_claims": ["not Graph Frontier-owned live Reddit fetch"],
                        },
                        {
                            "node_id": "subreddit:analytics",
                            "node_type": "subreddit_candidate",
                            "candidate_value_or_none": "analytics",
                            "source_surface": "related_subreddit",
                            "source_url_or_locator": "https://old.reddit.com/r/analytics/",
                            "stop_reason": "scope_exhausted",
                            "run_id": "run_1",
                            "visible_subscriber_count_or_none": None,
                            "visible_active_user_count_or_none": None,
                            "non_claims": ["not Graph Frontier-owned live Reddit fetch"],
                        },
                    ],
                    "edges": [
                        {
                            "edge_id": "edge_1",
                            "edge_type": "discovered_from_run",
                            "from_node_id": "run:run_1",
                            "to_node_id": "subreddit:analytics",
                            "source_surface": "related_subreddit",
                            "stop_reason": "scope_exhausted",
                            "non_claims": ["not Graph Frontier-owned live Reddit fetch"],
                        }
                    ],
                    "frontier_decisions": [
                        {
                            "decision_id": "decision_1",
                            "decision": "selected_as_next_frontier",
                            "selected_node_id": "subreddit:analytics",
                            "frontier_selection_reason": "overlap",
                            "next_run_id_or_none": "run_2",
                            "non_claims": ["not automatic capture"],
                        }
                    ],
                    "non_claims": ["not Graph Frontier-owned live Reddit fetch"],
                    "provenance": {},
                }
            }
        ),
        encoding="utf-8",
    )

    result = build_reddit_agent_views(input_json_path=source_path, output_directory=scratch_dir / "views")

    stripped = json.loads(Path(result["stripped_json_path"]).read_text(encoding="utf-8"))[
        "reddit_agent_view"
    ]["stripped"]
    assert stripped["counts"] == {"nodes": 2, "edges": 1, "frontier_decisions": 1}
    assert stripped["nodes"][1]["candidate_value_or_none"] == "analytics"
    assert "non_claims" not in stripped["nodes"][1]
    assert stripped["frontier_decisions"][0]["next_run_id_or_none"] == "run_2"


def test_graph_frontier_view_retains_caps_and_exclusions_once(scratch_dir: Path) -> None:
    source_path = scratch_dir / "reddit_graph_frontier_register.json"
    source_path.write_text(
        json.dumps(
            {
                "reddit_graph_frontier_register": {
                    "register_id": "register_1",
                    "source_intake_run_id": "run_1",
                    "source_policy_posture": "candidate-only",
                    "nodes": [
                        {
                            "node_id": "run:run_1",
                            "node_type": "run",
                            "candidate_value_or_none": None,
                            "source_surface": "subreddit_listing",
                            "source_url_or_locator": "https://old.reddit.com/r/SEO/",
                            "stop_reason": "caps_reached",
                            "run_id": "run_1",
                            "caps_applied": {"max_subreddits": 5, "max_frontier_hops": 1},
                            "exclusions": ["no_same_run_traversal"],
                            "visible_subscriber_count_or_none": None,
                            "visible_active_user_count_or_none": None,
                            "non_claims": ["not Graph Frontier-owned live Reddit fetch"],
                        }
                    ],
                    "edges": [],
                    "frontier_decisions": [],
                    "provenance": {
                        "caps_applied": {"max_subreddits": 5, "max_frontier_hops": 1},
                        "exclusions": [
                            "no_same_run_traversal",
                            "no_body_comment_profile_capture",
                        ],
                        "source_surface": "subreddit_listing",
                        "stop_reason": "caps_reached",
                    },
                    "non_claims": ["not Graph Frontier-owned live Reddit fetch"],
                }
            }
        ),
        encoding="utf-8",
    )

    result = build_reddit_agent_views(input_json_path=source_path, output_directory=scratch_dir / "views")

    stripped = json.loads(Path(result["stripped_json_path"]).read_text(encoding="utf-8"))[
        "reddit_agent_view"
    ]["stripped"]
    # Caps and exclusions are the traversal bounds an agent needs to plan the next
    # hop; the runbook preserve rule names them. Retain once at run level, not
    # dropped and not repeated per node.
    assert stripped["caps_applied"] == {"max_subreddits": 5, "max_frontier_hops": 1}
    assert stripped["exclusions"] == [
        "no_same_run_traversal",
        "no_body_comment_profile_capture",
    ]
    assert "caps_applied" not in stripped["nodes"][0]
    assert "exclusions" not in stripped["nodes"][0]


def test_rejects_unsupported_json_artifact(scratch_dir: Path) -> None:
    source_path = scratch_dir / "other.json"
    source_path.write_text(json.dumps({"other": {}}), encoding="utf-8")

    with pytest.raises(RedditAgentViewFailure) as excinfo:
        build_reddit_agent_views(input_json_path=source_path, output_directory=scratch_dir / "views")

    assert excinfo.value.code == "unsupported_artifact"
