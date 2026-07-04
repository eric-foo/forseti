from __future__ import annotations

import shutil
import uuid
from pathlib import Path

import pytest

from capture_spine.reddit_candidate_intake import (
    CandidateSubredditRow,
    CandidateSurface,
    CandidateThreadUrlRow,
    CapType,
    CoverageClaim,
    RunEnvelope,
    RunProvenanceReceipt,
    RedditCandidateIntakeError,
    StopReason,
    build_candidate_intake_output,
)
from capture_spine.reddit_graph_frontier import (
    FrontierDecision,
    GraphFrontierError,
    build_graph_frontier_register,
    prepare_next_bounded_run_envelope,
    validate_graph_frontier_register,
    validate_next_run_envelope,
    write_graph_frontier_register,
)


@pytest.fixture
def scratch_dir() -> Path:
    root = Path(__file__).resolve().parents[2] / "_test_runs"
    path = root / f"reddit_graph_frontier_{uuid.uuid4().hex}"
    path.mkdir(parents=True)
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


def test_builds_graph_frontier_register_from_candidate_rows_only(scratch_dir: Path) -> None:
    register = build_graph_frontier_register(
        register_id="reddit_graph_frontier_b2b_001",
        candidate_intake_output=_candidate_output(),
        access_mode="no_live_fixture",
        source_policy_posture="robots_policy_recorded_no_live_fixture",
    )

    graph = register["reddit_graph_frontier_register"]
    node_types = {node["node_type"] for node in graph["nodes"]}
    edge_types = {edge["edge_type"] for edge in graph["edges"]}

    assert graph["source_intake_run_id"] == "intake_run_001"
    assert "run" in node_types
    assert "subreddit_candidate" in node_types
    assert "thread_url_candidate" in node_types
    assert "discovered_from_run" in edge_types
    assert "related_subreddit_relation" in edge_types
    assert "not Graph Frontier-owned live Reddit fetch" in graph["non_claims"]
    assert "not Source Capture Packet output" in graph["non_claims"]
    assert "not Data Capture handoff" in graph["non_claims"]

    write_result = write_graph_frontier_register(register=register, output_directory=scratch_dir)
    artifact_text = Path(write_result["json_path"]).read_text(encoding="utf-8")
    receipt_text = Path(write_result["receipt_path"]).read_text(encoding="utf-8")

    assert "ordinary_person" not in artifact_text
    assert "body text not allowed" not in artifact_text
    assert "Source Capture Packet output\":" not in artifact_text
    assert "Register ID: reddit_graph_frontier_b2b_001" in receipt_text
    assert "Nodes: 3" in receipt_text


def test_frontier_decision_is_recorded_outside_candidate_intake() -> None:
    decision = FrontierDecision(
        decision_id="frontier_decision_001",
        selected_node_id="subreddit:intake_run_001:webmarketing",
        frontier_selection_reason="closest planning match to B2B marketing among related subreddit rows",
        frontier_selection_actor="semantic_frontier_agent",
        frontier_selection_timestamp="2026-06-08T00:10:00Z",
        next_run_id_or_none="intake_run_002",
    )
    candidate_output = _candidate_output()
    register = build_graph_frontier_register(
        register_id="reddit_graph_frontier_b2b_001",
        candidate_intake_output=candidate_output,
        access_mode="no_live_fixture",
        source_policy_posture="robots_policy_recorded_no_live_fixture",
        frontier_decisions=[decision],
    )

    validate_graph_frontier_register(register)

    assert "frontier_decisions" not in candidate_output["reddit_candidate_url_intake"]
    assert register["reddit_graph_frontier_register"]["frontier_decisions"][0]["selected_node_id"] == (
        "subreddit:intake_run_001:webmarketing"
    )


def test_prepare_next_run_envelope_is_not_execution_authorization() -> None:
    register = build_graph_frontier_register(
        register_id="reddit_graph_frontier_b2b_001",
        candidate_intake_output=_candidate_output(),
        access_mode="no_live_fixture",
        source_policy_posture="robots_policy_recorded_no_live_fixture",
    )

    envelope = prepare_next_bounded_run_envelope(
        register=register,
        selected_node_id="subreddit:intake_run_001:webmarketing",
        next_run_id="intake_run_002",
        declared_topic_theme_or_query="b2b marketing demand generation",
        candidate_surface_allowlist=("subreddit_listing", "related_subreddit"),
        caps={
            "max_subreddits": 5,
            "max_threads_per_subreddit": 25,
            "max_pages_or_result_surfaces": 2,
            "max_frontier_hops": 1,
        },
        exclusions=("no_user_profiles", "no_thread_bodies"),
        access_mode="no_live_fixture",
        source_policy_posture="robots_policy_recorded_before_any_live_access",
        stop_condition="caps_reached",
    )

    validate_next_run_envelope(envelope)

    assert envelope["next_run_id"] == "intake_run_002"
    assert envelope["declared_seed_or_surface"] == "webmarketing"
    assert envelope["prior_register_pointer"] == "reddit_graph_frontier_b2b_001#subreddit:intake_run_001:webmarketing"
    assert envelope["execution_authorized"] is False
    assert "not Graph Frontier-owned live Reddit fetch" in envelope["non_claims"]


def test_next_run_envelope_requires_source_policy_posture() -> None:
    register = build_graph_frontier_register(
        register_id="reddit_graph_frontier_b2b_001",
        candidate_intake_output=_candidate_output(),
        access_mode="no_live_fixture",
        source_policy_posture="robots_policy_recorded_no_live_fixture",
    )

    with pytest.raises(GraphFrontierError) as exc_info:
        prepare_next_bounded_run_envelope(
            register=register,
            selected_node_id="subreddit:intake_run_001:webmarketing",
            next_run_id="intake_run_002",
            declared_topic_theme_or_query="b2b marketing demand generation",
            candidate_surface_allowlist=("subreddit_listing",),
            caps={"max_subreddits": 5, "max_frontier_hops": 1},
            exclusions=(),
            access_mode="no_live_fixture",
            source_policy_posture="",
            stop_condition="caps_reached",
        )

    assert exc_info.value.code == "missing_source_policy_posture"


def test_graph_frontier_rejects_forbidden_fields() -> None:
    register = build_graph_frontier_register(
        register_id="reddit_graph_frontier_b2b_001",
        candidate_intake_output=_candidate_output(),
        access_mode="no_live_fixture",
        source_policy_posture="robots_policy_recorded_no_live_fixture",
    )
    register["reddit_graph_frontier_register"]["nodes"][0]["raw_html"] = "<html>not allowed</html>"

    with pytest.raises(RedditCandidateIntakeError) as exc_info:
        validate_graph_frontier_register(register)

    assert getattr(exc_info.value, "code", None) == "forbidden_output_field"


def test_register_and_envelope_carry_schema_version() -> None:
    register = build_graph_frontier_register(
        register_id="reddit_graph_frontier_b2b_001",
        candidate_intake_output=_candidate_output(),
        access_mode="no_live_fixture",
        source_policy_posture="robots_policy_recorded_no_live_fixture",
    )
    assert (
        register["reddit_graph_frontier_register"]["schema_version"]
        == "reddit_graph_frontier_register_v0"
    )

    envelope = prepare_next_bounded_run_envelope(
        register=register,
        selected_node_id="subreddit:intake_run_001:webmarketing",
        next_run_id="intake_run_002",
        declared_topic_theme_or_query="b2b marketing demand generation",
        candidate_surface_allowlist=("subreddit_listing",),
        caps={"max_subreddits": 5, "max_frontier_hops": 1},
        exclusions=(),
        access_mode="no_live_fixture",
        source_policy_posture="robots_policy_recorded_before_any_live_access",
        stop_condition="caps_reached",
    )
    assert envelope["schema_version"] == "reddit_graph_frontier_next_run_envelope_v0"


def test_nodes_carry_run_listing_context() -> None:
    register = build_graph_frontier_register(
        register_id="reddit_graph_frontier_b2b_001",
        candidate_intake_output=_candidate_output(),
        access_mode="no_live_fixture",
        source_policy_posture="robots_policy_recorded_no_live_fixture",
    )
    nodes = {
        node["node_id"]: node
        for node in register["reddit_graph_frontier_register"]["nodes"]
    }
    run_node = nodes["run:intake_run_001"]
    assert run_node["sort_order_or_none"] == "top"
    assert run_node["time_window_or_none"] == 30
    # run-level listing context propagates to candidate nodes (self-describing).
    candidate = nodes["subreddit:intake_run_001:webmarketing"]
    assert candidate["sort_order_or_none"] == "top"
    assert candidate["time_window_or_none"] == 30


def _candidate_output() -> dict[str, object]:
    envelope = RunEnvelope(
        run_id="intake_run_001",
        run_purpose="static no-live graph frontier input",
        cap_type=CapType.PROBE,
        coverage_claim=CoverageClaim.BOUNDED_PROBE_ONLY,
        max_subreddits=5,
        max_threads_per_subreddit=25,
        max_pages_or_result_surfaces=2,
        time_window_days=30,
        sort_order="top",
        method_category="static_fixture",
        stop_condition=StopReason.CAPS_REACHED,
        declared_topic_theme_query="b2b marketing",
        seed_subreddits=("SEO",),
        candidate_surface_allowlist=(CandidateSurface.RELATED_SUBREDDIT, CandidateSurface.SUBREDDIT_LISTING),
    )
    return build_candidate_intake_output(
        envelope=envelope,
        provenance=RunProvenanceReceipt(
            run_id="intake_run_001",
            caps_applied={
                "max_subreddits": 5,
                "max_threads_per_subreddit": 25,
                "max_pages_or_result_surfaces": 2,
                "time_window_days": 30,
            },
            source_surface="related_subreddit",
            query_or_listing_path="/r/SEO/",
            sort_order="top",
            time_window_days=30,
            method_category="static_fixture",
            timestamp="2026-06-08T00:00:00Z",
            row_counts={"candidate_subreddits": 1, "candidate_threads": 1, "outbound_urls": 0},
            stop_reason=StopReason.CAPS_REACHED,
            exclusions_applied=("no_user_profiles", "no_thread_bodies"),
        ),
        candidate_subreddits=[
            CandidateSubredditRow(
                run_id="intake_run_001",
                candidate_subreddit="webmarketing",
                source_surface=CandidateSurface.RELATED_SUBREDDIT,
                source_url="https://old.reddit.com/r/webmarketing/",
                query_or_seed="SEO",
                timestamp="2026-06-08T00:00:00Z",
                method_category="static_fixture",
                exclusion_receipt=("no_user_profiles", "no_thread_bodies"),
                visible_volume_signal_absent_reason_or_none="visible_volume_not_present_on_declared_surface",
            )
        ],
        candidate_threads=[
            CandidateThreadUrlRow(
                run_id="intake_run_001",
                candidate_thread_url="https://old.reddit.com/r/SEO/comments/abc123/b2b_seo_candidate/",
                subreddit="SEO",
                source_surface=CandidateSurface.SUBREDDIT_LISTING,
                query_or_seed="SEO",
                timestamp="2026-06-08T00:00:00Z",
                method_category="static_fixture",
                visible_listing_title="B2B SEO candidate",
                exclusion_receipt=("no_user_profiles", "no_thread_bodies"),
            )
        ],
    )
