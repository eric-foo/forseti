from __future__ import annotations

import json
import shutil
import uuid
from pathlib import Path

import pytest

from capture_spine.reddit_candidate_intake import (
    CandidateSubredditRow,
    CandidateSurface,
    CapType,
    CoverageClaim,
    RunEnvelope,
    RunProvenanceReceipt,
    StopReason,
    build_candidate_intake_output,
    write_candidate_intake_output,
)
from runners.run_reddit_graph_frontier_register import run_reddit_graph_frontier_register


@pytest.fixture
def scratch_dir() -> Path:
    root = Path(__file__).resolve().parents[2] / "_test_runs"
    path = root / f"reddit_graph_frontier_runner_{uuid.uuid4().hex}"
    path.mkdir(parents=True)
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


def test_graph_frontier_runner_writes_register_from_candidate_output(scratch_dir: Path) -> None:
    candidate_path = _write_candidate_output(scratch_dir)

    result = run_reddit_graph_frontier_register(
        candidate_intake_output_path=candidate_path,
        output_directory=scratch_dir / "graph",
        register_id="reddit_graph_frontier_live_smoke_001",
        access_mode="live_old_reddit_direct_http_candidate_intake",
        source_policy_posture="bounded_run_envelope_candidate_only_projection",
    )

    register = json.loads(Path(result["register_json_path"]).read_text(encoding="utf-8"))
    graph = register["reddit_graph_frontier_register"]

    assert result["next_run_envelope_path"] is None
    assert graph["register_id"] == "reddit_graph_frontier_live_smoke_001"
    assert graph["source_intake_run_id"] == "intake_live_001"
    assert {node["candidate_value_or_none"] for node in graph["nodes"]} >= {"webmarketing", "PPC"}
    assert "not Source Capture Packet output" in graph["non_claims"]


def test_graph_frontier_runner_writes_non_executing_next_run_envelope(scratch_dir: Path) -> None:
    candidate_path = _write_candidate_output(scratch_dir)

    result = run_reddit_graph_frontier_register(
        candidate_intake_output_path=candidate_path,
        output_directory=scratch_dir / "graph",
        register_id="reddit_graph_frontier_live_smoke_001",
        access_mode="live_old_reddit_direct_http_candidate_intake",
        source_policy_posture="bounded_run_envelope_candidate_only_projection",
        selected_candidate_value="webmarketing",
        frontier_selection_reason="closest declared B2B marketing planning seed from related subreddit rows",
        frontier_selection_actor="operator_frontier_selection",
        next_run_id="reddit_live_candidate_intake_webmarketing_001",
        declared_topic_theme_or_query="b2b marketing adjacent subreddit scouting",
        candidate_surface_allowlist=("related_subreddit", "subreddit_listing"),
        caps={
            "max_subreddits": 7,
            "max_threads_per_subreddit": 25,
            "max_pages_or_result_surfaces": 1,
            "max_frontier_hops": 1,
        },
        exclusions=("no_same_run_traversal", "no_body_comment_profile_capture"),
        next_access_mode="live_old_reddit_direct_http_candidate_intake",
        next_source_policy_posture="bounded_run_envelope_candidate_only_projection",
        stop_condition="caps_reached",
    )

    register = json.loads(Path(result["register_json_path"]).read_text(encoding="utf-8"))
    envelope = json.loads(Path(result["next_run_envelope_path"]).read_text(encoding="utf-8"))

    assert register["reddit_graph_frontier_register"]["frontier_decisions"][0]["selected_node_id"] == (
        "subreddit:intake_live_001:webmarketing"
    )
    assert envelope["next_run_id"] == "reddit_live_candidate_intake_webmarketing_001"
    assert envelope["declared_seed_or_surface"] == "webmarketing"
    assert envelope["execution_authorized"] is False
    assert envelope["prior_register_pointer"] == (
        "reddit_graph_frontier_live_smoke_001#subreddit:intake_live_001:webmarketing"
    )


def _write_candidate_output(scratch_dir: Path) -> Path:
    envelope = RunEnvelope(
        run_id="intake_live_001",
        run_purpose="bounded live first-contact intake test",
        cap_type=CapType.PROBE,
        coverage_claim=CoverageClaim.BOUNDED_PROBE_ONLY,
        max_subreddits=7,
        max_threads_per_subreddit=1,
        max_pages_or_result_surfaces=1,
        time_window_days=30,
        sort_order="hot",
        method_category="live_old_reddit_direct_http_candidate_intake",
        stop_condition=StopReason.SCOPE_EXHAUSTED,
        declared_topic_theme_query="b2b marketing adjacent subreddit scouting",
        seed_subreddits=("SEO",),
        candidate_surface_allowlist=(CandidateSurface.RELATED_SUBREDDIT,),
    )
    output = build_candidate_intake_output(
        envelope=envelope,
        provenance=RunProvenanceReceipt(
            run_id="intake_live_001",
            caps_applied={
                "max_subreddits": 7,
                "max_threads_per_subreddit": 1,
                "max_pages_or_result_surfaces": 1,
                "time_window_days": 30,
            },
            source_surface="related_subreddit",
            query_or_listing_path="/r/SEO/",
            sort_order="hot",
            time_window_days=30,
            method_category="live_old_reddit_direct_http_candidate_intake",
            timestamp="2026-06-08T00:00:00Z",
            row_counts={"candidate_subreddits": 2, "candidate_threads": 0, "outbound_urls": 0},
            stop_reason=StopReason.SCOPE_EXHAUSTED,
            exclusions_applied=("no_same_run_traversal", "no_body_comment_profile_capture"),
        ),
        candidate_subreddits=[
            CandidateSubredditRow(
                run_id="intake_live_001",
                candidate_subreddit="webmarketing",
                source_surface=CandidateSurface.RELATED_SUBREDDIT,
                source_url="https://old.reddit.com/r/webmarketing/",
                query_or_seed="b2b marketing adjacent subreddit scouting",
                timestamp="2026-06-08T00:00:00Z",
                method_category="live_old_reddit_direct_http_candidate_intake",
                exclusion_receipt=("no_same_run_traversal", "no_body_comment_profile_capture"),
                visible_volume_signal_absent_reason_or_none="visible_volume_not_present_on_declared_surface",
            ),
            CandidateSubredditRow(
                run_id="intake_live_001",
                candidate_subreddit="PPC",
                source_surface=CandidateSurface.RELATED_SUBREDDIT,
                source_url="https://old.reddit.com/r/PPC/",
                query_or_seed="b2b marketing adjacent subreddit scouting",
                timestamp="2026-06-08T00:00:00Z",
                method_category="live_old_reddit_direct_http_candidate_intake",
                exclusion_receipt=("no_same_run_traversal", "no_body_comment_profile_capture"),
                visible_volume_signal_absent_reason_or_none="visible_volume_not_present_on_declared_surface",
            ),
        ],
    )
    write_result = write_candidate_intake_output(
        output=output,
        output_directory=scratch_dir / "candidate",
    )
    return Path(write_result["json_path"])
