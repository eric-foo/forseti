from __future__ import annotations

import json
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
    OutboundUrlCandidateRow,
    PromotionReceipt,
    RedditCandidateIntakeError,
    RunEnvelope,
    RunProvenanceReceipt,
    StopReason,
    assert_no_forbidden_output_fields,
    build_candidate_intake_output,
    project_old_reddit_html_listing,
    project_old_reddit_html_candidate_subreddits,
    validate_old_reddit_html_listing_input_url,
    validate_old_reddit_thread_url,
    validate_promotion_receipt,
    validate_run_envelope,
    write_candidate_intake_output,
)


@pytest.fixture
def scratch_dir() -> Path:
    root = Path(__file__).resolve().parents[2] / "_test_runs"
    path = root / f"reddit_candidate_intake_{uuid.uuid4().hex}"
    path.mkdir(parents=True)
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


def test_old_reddit_thread_url_is_default_valid_shape() -> None:
    subreddit, thread_id = validate_old_reddit_thread_url(
        "https://old.reddit.com/r/orca_test/comments/abc123/durable_reddit_packet_spine/"
    )

    assert subreddit == "orca_test"
    assert thread_id == "abc123"


def test_new_reddit_thread_url_is_non_default() -> None:
    with pytest.raises(RedditCandidateIntakeError) as exc_info:
        validate_old_reddit_thread_url(
            "https://www.reddit.com/r/orca_test/comments/abc123/durable_reddit_packet_spine/"
        )

    assert exc_info.value.code == "new_reddit_non_default"


def test_json_urls_are_blocked_for_intake_inputs() -> None:
    for url in (
        "https://old.reddit.com/r/orca_test/.json",
        "https://old.reddit.com/r/orca_test/search.json?q=orca",
        "https://old.reddit.com/r/orca_test/comments/abc123/x/.json",
    ):
        with pytest.raises(RedditCandidateIntakeError) as exc_info:
            validate_old_reddit_html_listing_input_url(url)
        assert exc_info.value.code == "reddit_json_input_forbidden"


def test_thread_pages_are_not_intake_input_surfaces() -> None:
    with pytest.raises(RedditCandidateIntakeError) as exc_info:
        validate_old_reddit_html_listing_input_url(
            "https://old.reddit.com/r/orca_test/comments/abc123/durable_reddit_packet_spine/"
        )

    assert exc_info.value.code == "reddit_thread_input_forbidden"


def test_projection_rejects_undeclared_candidate_surface() -> None:
    with pytest.raises(RedditCandidateIntakeError) as exc_info:
        project_old_reddit_html_listing(
            html_text="<html></html>",
            envelope=_envelope(
                candidate_surface_allowlist=(CandidateSurface.SUBREDDIT_LISTING,)
            ),
            source_url="https://old.reddit.com/r/orca_test/top/",
            timestamp="2026-06-06T00:00:00Z",
            source_surface=CandidateSurface.REDDIT_SEARCH_LISTING,
        )

    assert exc_info.value.code == "undeclared_candidate_surface"


def test_run_envelope_requires_declared_scope() -> None:
    envelope = _envelope(declared_topic_theme_query=None, seed_subreddits=())

    with pytest.raises(RedditCandidateIntakeError) as exc_info:
        validate_run_envelope(envelope)

    assert exc_info.value.code == "missing_declared_scope"


def test_builds_candidate_rows_and_provenance_only(scratch_dir: Path) -> None:
    output = build_candidate_intake_output(
        envelope=_envelope(),
        provenance=_provenance(),
        candidate_subreddits=[
            CandidateSubredditRow(
                run_id="run_001",
                candidate_subreddit="orca_related",
                source_surface=CandidateSurface.RELATED_SUBREDDIT,
                source_url="https://old.reddit.com/r/orca_related/",
                query_or_seed="orca",
                timestamp="2026-06-06T00:00:00Z",
                method_category="static_fixture",
            )
        ],
        candidate_threads=[
            CandidateThreadUrlRow(
                run_id="run_001",
                candidate_thread_url="https://old.reddit.com/r/orca_test/comments/abc123/durable_reddit_packet_spine/",
                subreddit="orca_test",
                source_surface=CandidateSurface.SUBREDDIT_LISTING,
                query_or_seed="orca",
                timestamp="2026-06-06T00:00:00Z",
                method_category="static_fixture",
                visible_listing_title="Durable Reddit packet spine",
            )
        ],
        outbound_urls=[
            OutboundUrlCandidateRow(
                run_id="run_001",
                outbound_url="https://example.com/source",
                originating_reddit_url="https://old.reddit.com/r/orca_test/comments/abc123/durable_reddit_packet_spine/",
                source_surface=CandidateSurface.OUTBOUND_LINKS,
                timestamp="2026-06-06T00:00:00Z",
                method_category="static_fixture",
            )
        ],
    )

    write_result = write_candidate_intake_output(output=output, output_directory=scratch_dir)
    artifact = json.loads(Path(write_result["json_path"]).read_text(encoding="utf-8"))
    intake = artifact["reddit_candidate_url_intake"]

    assert intake["candidate_threads"][0]["capture_unit_intake_status"] == "candidate_or_scouting"
    assert intake["candidate_threads"][0]["allowed_downstream_use"] == "planning_only"
    assert intake["outbound_urls"][0]["requires_separate_source_family_intake"] is True
    assert "not Source Capture Packet output" in intake["non_claims"]
    assert "Source Capture Packet" in Path(write_result["receipt_path"]).read_text(encoding="utf-8")


def test_projects_static_old_reddit_html_listing_to_candidate_rows_only(scratch_dir: Path) -> None:
    html = """
    <html>
      <body>
        <div class="thing" data-author="ordinary_person" data-selftext="body text not allowed">
          <a class="title may-blank" href="/r/orca_test/comments/abc123/durable_reddit_packet_spine/">
            Durable Reddit packet spine
          </a>
          <a class="author" href="/user/ordinary_person">ordinary_person</a>
          <a class="comments" href="/r/orca_test/comments/abc123/durable_reddit_packet_spine/">42 comments</a>
        </div>
        <div class="thing">
          <a class="title" href="https://old.reddit.com/r/orca_test/comments/def456/another_candidate">
            Another candidate
          </a>
        </div>
        <a class="title" href="https://example.com/not_reddit">Outbound ignored in this slice</a>
        <a class="title" href="https://old.reddit.com/r/orca_test/.json">JSON ignored in this slice</a>
      </body>
    </html>
    """
    rows = project_old_reddit_html_listing(
        html_text=html,
        envelope=_envelope(max_threads_per_subreddit=1),
        source_url="https://old.reddit.com/r/orca_test/top/?t=month",
        timestamp="2026-06-06T00:00:00Z",
    )

    assert len(rows) == 1
    assert rows[0].candidate_thread_url == (
        "https://old.reddit.com/r/orca_test/comments/abc123/durable_reddit_packet_spine/"
    )
    assert rows[0].visible_listing_title == "Durable Reddit packet spine"

    output = build_candidate_intake_output(
        envelope=_envelope(max_threads_per_subreddit=1),
        provenance=_provenance(row_counts={"candidate_subreddits": 0, "candidate_threads": 1, "outbound_urls": 0}),
        candidate_threads=rows,
    )
    write_result = write_candidate_intake_output(output=output, output_directory=scratch_dir)
    artifact_text = Path(write_result["json_path"]).read_text(encoding="utf-8")

    assert "ordinary_person" not in artifact_text
    assert "body text not allowed" not in artifact_text
    assert "<html>" not in artifact_text
    assert "Durable Reddit packet spine" in artifact_text


def test_projects_old_reddit_search_title_anchors_without_comment_links() -> None:
    html = """
    <html>
      <body>
        <a class="search-title may-blank" href="https://old.reddit.com/r/b2bmarketing/comments/1mk4ivy/a_friend_of_mine_closed_a_72k_deal_from_a/">
          A friend of mine closed a 72k deal from a meeting funnel
        </a>
        <a class="search-comments may-blank" href="https://old.reddit.com/r/b2bmarketing/comments/1mk4ivy/a_friend_of_mine_closed_a_72k_deal_from_a/">
          19 comments
        </a>
        <a class="may-blank thumbnail self" href="/r/b2bmarketing/comments/1szt837/marketing_is_slowly_turning_into_engineering_and/">
          thumbnail only
        </a>
      </body>
    </html>
    """

    rows = project_old_reddit_html_listing(
        html_text=html,
        envelope=_envelope(candidate_surface_allowlist=(CandidateSurface.REDDIT_SEARCH_LISTING,)),
        source_url="https://old.reddit.com/r/b2bmarketing/search/?q=meetings&restrict_sr=on&sort=top&t=year",
        timestamp="2026-06-07T00:00:00Z",
        source_surface=CandidateSurface.REDDIT_SEARCH_LISTING,
    )

    assert len(rows) == 1
    assert rows[0].candidate_thread_url == (
        "https://old.reddit.com/r/b2bmarketing/comments/1mk4ivy/a_friend_of_mine_closed_a_72k_deal_from_a/"
    )
    assert rows[0].visible_listing_title == "A friend of mine closed a 72k deal from a meeting funnel"


def test_listing_projection_records_link_post_target_thread_with_its_true_subreddit() -> None:
    # Pins the link-post semantics surfaced by a real live run: when a listing
    # entry is a LINK to a thread in another subreddit, the projection captures
    # the title anchor's target thread and records its TRUE home subreddit, not
    # the declared listing subreddit. This is honest provenance, not a
    # no_subreddit_crawl breach — only the one declared page is read.
    html = """
    <html>
      <body>
        <div class="thing">
          <a class="title may-blank" href="/r/orca_test/comments/aaa111/native_self_post/">
            Native self post in the declared subreddit
          </a>
        </div>
        <div class="thing">
          <a class="title may-blank" href="/r/marketing/comments/bbb222/2025_state_of_marketing_survey/">
            2025 State of Marketing Survey
          </a>
        </div>
      </body>
    </html>
    """
    rows = project_old_reddit_html_listing(
        html_text=html,
        envelope=_envelope(),
        source_url="https://old.reddit.com/r/orca_test/",
        timestamp="2026-06-08T00:00:00Z",
    )

    assert len(rows) == 2
    by_subreddit = {row.subreddit: row for row in rows}
    # The off-subreddit link target is captured and honestly tagged with its
    # real home subreddit, which differs from the declared listing (orca_test).
    assert set(by_subreddit) == {"orca_test", "marketing"}
    assert by_subreddit["marketing"].candidate_thread_url == (
        "https://old.reddit.com/r/marketing/comments/bbb222/2025_state_of_marketing_survey/"
    )
    assert by_subreddit["marketing"].subreddit != "orca_test"


def test_projects_seed_subreddit_with_visible_counts_to_candidate_row() -> None:
    html = """
    <html>
      <body>
        <div class="titlebox">
          <h1 class="redditname"><a href="https://old.reddit.com/r/b2bmarketing/">b2bmarketing</a></h1>
          <span class="number">108,000</span><span class="word">readers</span>
          <p class="users-online"><span class="number">42</span><span class="word">users here now</span></p>
        </div>
      </body>
    </html>
    """

    rows = project_old_reddit_html_candidate_subreddits(
        html_text=html,
        envelope=_envelope(
            seed_subreddits=("b2bmarketing",),
            candidate_surface_allowlist=(CandidateSurface.SEED_SUBREDDITS,),
        ),
        source_url="https://old.reddit.com/r/b2bmarketing/search/?q=meetings&restrict_sr=on&sort=top&t=year",
        timestamp="2026-06-08T00:00:00Z",
        source_surface=CandidateSurface.SEED_SUBREDDITS,
    )

    assert len(rows) == 1
    assert rows[0].candidate_subreddit == "b2bmarketing"
    assert rows[0].source_url == "https://old.reddit.com/r/b2bmarketing/"
    assert rows[0].visible_subscriber_count_or_none == "108,000"
    assert rows[0].visible_active_user_count_or_none == "42"
    assert rows[0].same_run_traversal_authorized is False


def test_candidate_subreddit_projection_drops_nav_and_keeps_declared_related_surface() -> None:
    html = """
    <html>
      <body>
        <div id="sr-header-area">
          <a class="choice" href="https://old.reddit.com/r/funny/">funny</a>
          <a class="choice" href="https://old.reddit.com/r/AskReddit/">AskReddit</a>
        </div>
        <div class="related-subreddits">
          <a href="https://old.reddit.com/r/sales/">sales</a>
          <a href="/r/marketingautomation/">marketingautomation</a>
        </div>
        <div class="footer">
          <a href="https://old.reddit.com/r/pics/">pics</a>
        </div>
      </body>
    </html>
    """

    rows = project_old_reddit_html_candidate_subreddits(
        html_text=html,
        envelope=_envelope(
            max_subreddits=5,
            seed_subreddits=("b2bmarketing",),
            candidate_surface_allowlist=(CandidateSurface.RELATED_SUBREDDIT,),
        ),
        source_url="https://old.reddit.com/r/b2bmarketing/search/?q=meetings&restrict_sr=on&sort=top&t=year",
        timestamp="2026-06-08T00:00:00Z",
        source_surface=CandidateSurface.RELATED_SUBREDDIT,
    )

    assert [row.candidate_subreddit for row in rows] == ["sales", "marketingautomation"]
    assert all(row.same_run_traversal_authorized is False for row in rows)
    assert all(row.visible_volume_signal_absent_reason_or_none for row in rows)


def test_candidate_subreddit_projection_keeps_nested_related_surface_links_only() -> None:
    html = """
    <html>
      <body>
        <div class="related-subreddits">
          <div class="nested">
            <a href="https://old.reddit.com/r/webmarketing/">webmarketing</a>
          </div>
          <section>
            <a href="/r/PPC/">PPC</a>
          </section>
        </div>
        <a href="https://old.reddit.com/r/pics/">pics</a>
      </body>
    </html>
    """

    rows = project_old_reddit_html_candidate_subreddits(
        html_text=html,
        envelope=_envelope(
            seed_subreddits=("SEO",),
            candidate_surface_allowlist=(CandidateSurface.RELATED_SUBREDDIT,),
        ),
        source_url="https://old.reddit.com/r/SEO/",
        timestamp="2026-06-08T00:00:00Z",
        source_surface=CandidateSurface.RELATED_SUBREDDIT,
    )

    assert [row.candidate_subreddit for row in rows] == ["webmarketing", "PPC"]


def test_candidate_subreddit_projection_keeps_sidebar_markdown_related_links_only() -> None:
    html = """
    <html>
      <body>
        <div id="sr-header-area">
          <a class="choice" href="https://old.reddit.com/r/AskReddit/">AskReddit</a>
        </div>
        <div class="side">
          <form id="search"><a href="https://www.reddit.com/wiki/search">search faq</a></form>
          <div class="titlebox">
            <h1 class="redditname"><a href="https://old.reddit.com/r/SEO/">SEO</a></h1>
            <div class="usertext-body may-blank-within md-container">
              <div class="md">
                <p><a href="http://www.reddit.com/r/webmarketing">/r/webmarketing</a></p>
                <p><a href="http://www.reddit.com/r/socialmedia">/r/socialmedia</a></p>
                <p><a href="http://www.reddit.com/r/PPC">/r/PPC</a></p>
                <p><a href="http://www.reddit.com/r/analytics">/r/analytics</a></p>
              </div>
            </div>
          </div>
          <a href="/message/compose/?to=/r/SEO">message the mods</a>
        </div>
        <div class="footer"><a href="https://old.reddit.com/r/pics/">pics</a></div>
      </body>
    </html>
    """

    rows = project_old_reddit_html_candidate_subreddits(
        html_text=html,
        envelope=_envelope(
            max_subreddits=10,
            seed_subreddits=("SEO",),
            candidate_surface_allowlist=(CandidateSurface.RELATED_SUBREDDIT,),
        ),
        source_url="https://old.reddit.com/r/SEO/",
        timestamp="2026-06-08T00:00:00Z",
        source_surface=CandidateSurface.RELATED_SUBREDDIT,
    )

    assert [row.candidate_subreddit for row in rows] == [
        "webmarketing",
        "socialmedia",
        "PPC",
        "analytics",
    ]
    assert all(row.same_run_traversal_authorized is False for row in rows)


def test_seed_subreddit_volume_does_not_use_listing_score_spans() -> None:
    html = """
    <html>
      <body>
        <div class="titlebox">
          <h1 class="redditname"><a href="https://old.reddit.com/r/SEO/">SEO</a></h1>
        </div>
        <div class="score unvoted"><span class="number">999</span></div>
      </body>
    </html>
    """

    rows = project_old_reddit_html_candidate_subreddits(
        html_text=html,
        envelope=_envelope(
            seed_subreddits=("SEO",),
            candidate_surface_allowlist=(CandidateSurface.SEED_SUBREDDITS,),
        ),
        source_url="https://old.reddit.com/r/SEO/",
        timestamp="2026-06-08T00:00:00Z",
        source_surface=CandidateSurface.SEED_SUBREDDITS,
    )

    assert rows[0].visible_subscriber_count_or_none is None
    assert rows[0].visible_active_user_count_or_none is None
    assert rows[0].visible_volume_signal_absent_reason_or_none == "visible_volume_not_present_on_declared_surface"


def test_no_live_dry_use_projects_fixture_through_writer_with_candidate_only_output(scratch_dir: Path) -> None:
    fixture_path = (
        Path(__file__).resolve().parents[1]
        / "fixtures"
        / "reddit_candidate_intake"
        / "old_reddit_listing_noisy.html"
    )
    envelope = _envelope(
        run_id="dry_use_old_reddit_html_001",
        run_purpose="no-live dry-use acceptance slice",
        max_threads_per_subreddit=2,
        candidate_surface_allowlist=(CandidateSurface.REDDIT_SEARCH_LISTING,),
        sort_order="top",
        declared_topic_theme_query="orca durable capture",
        seed_subreddits=("orca_test",),
    )

    rows = project_old_reddit_html_listing(
        html_text=fixture_path.read_text(encoding="utf-8"),
        envelope=envelope,
        source_url="https://old.reddit.com/r/orca_test/search/?q=orca+durable+capture&sort=top&t=month",
        timestamp="2026-06-07T00:00:00Z",
        source_surface=CandidateSurface.REDDIT_SEARCH_LISTING,
        method_category="static_old_reddit_html_fixture",
    )
    output = build_candidate_intake_output(
        envelope=envelope,
        provenance=_provenance(
            run_id="dry_use_old_reddit_html_001",
            caps_applied={
                "max_subreddits": 5,
                "max_threads_per_subreddit": 2,
                "max_pages_or_result_surfaces": 2,
                "time_window_days": 30,
            },
            source_surface="reddit_search_listing",
            query_or_listing_path="/r/orca_test/search/?q=orca+durable+capture&sort=top&t=month",
            method_category="static_old_reddit_html_fixture",
            timestamp="2026-06-07T00:00:00Z",
            row_counts={"candidate_subreddits": 0, "candidate_threads": 2, "outbound_urls": 0},
            stop_reason=StopReason.CAPS_REACHED,
        ),
        candidate_threads=rows,
    )
    write_result = write_candidate_intake_output(output=output, output_directory=scratch_dir)

    artifact_text = Path(write_result["json_path"]).read_text(encoding="utf-8")
    artifact = json.loads(artifact_text)
    intake = artifact["reddit_candidate_url_intake"]
    receipt_text = Path(write_result["receipt_path"]).read_text(encoding="utf-8")

    assert [row["candidate_thread_url"] for row in intake["candidate_threads"]] == [
        "https://old.reddit.com/r/orca_test/comments/abc123/durable_reddit_packet_spine/",
        "https://old.reddit.com/r/orca_test/comments/def456/another_candidate/",
    ]
    assert intake["candidate_threads"][0]["source_surface"] == "reddit_search_listing"
    assert intake["candidate_threads"][0]["allowed_downstream_use"] == "planning_only"
    assert intake["candidate_threads"][0]["same_run_traversal_authorized"] is False
    assert intake["provenance"]["stop_reason"] == "caps_reached"
    assert intake["provenance"]["row_counts"] == {
        "candidate_subreddits": 0,
        "candidate_threads": 2,
        "outbound_urls": 0,
    }
    assert "not Source Capture Packet output" in intake["non_claims"]
    assert "not Data Capture handoff" in intake["non_claims"]
    assert "Candidate threads: 2" in receipt_text
    assert "Stop reason: caps_reached" in receipt_text
    for forbidden in (
        "ordinary_person",
        "body text not allowed",
        "Comment body text",
        '"author":',
        '"author_fullname":',
        "<html>",
        ".json",
        "example.com/outbound-source",
        "beyond_cap_candidate",
        "Source Capture Packet output\":",
    ):
        assert forbidden not in artifact_text


def test_forbidden_body_comment_profile_packet_fields_are_rejected() -> None:
    with pytest.raises(RedditCandidateIntakeError) as exc_info:
        assert_no_forbidden_output_fields(
            {
                "candidate_thread_url": "https://old.reddit.com/r/orca_test/comments/abc123/x/",
                "comments": ["not allowed"],
            }
        )

    assert exc_info.value.code == "forbidden_output_field"


def test_reddit_post_body_field_selftext_is_rejected() -> None:
    # selftext / selftext_html / body_html are Reddit's canonical body field names.
    for field in ("selftext", "selftext_html", "body_html"):
        with pytest.raises(RedditCandidateIntakeError) as exc_info:
            assert_no_forbidden_output_fields({field: "not allowed"})
        assert exc_info.value.code == "forbidden_output_field"


def test_secret_like_output_values_are_rejected() -> None:
    # Defense-in-depth beyond the field-NAME blocklist: a credential that lands
    # in a non-secret-named field (a leaked header pasted into a free-text
    # reason, or proxy creds embedded in a source URL) must still be rejected by
    # a VALUE scan. The keys here are deliberately legitimate, so only the value
    # scan can trip.
    secret_values = (
        "-----BEGIN RSA PRIVATE KEY-----",                          # PEM private key
        "Authorization: Bearer abcdef0123456789ABCDEF",             # bearer token
        "https://proxyuser:proxypass@proxy.internal:8080",          # url userinfo creds
        "Set-Cookie: reddit_session=eyJhbGciOiJIUzI1NiJ9; Path=/",  # cookie header
    )
    for secret in secret_values:
        with pytest.raises(RedditCandidateIntakeError) as exc_info:
            assert_no_forbidden_output_fields({"frontier_decision_reason": secret})
        assert exc_info.value.code == "forbidden_output_value"


def test_legit_token_like_values_are_not_rejected() -> None:
    # The secret-value scan must NOT false-positive on the candidate/frontier
    # value vocabulary. Each anchors on a credential marker, never on entropy,
    # so hash-like node ids and colon/`:`-bearing ids pass.
    legit_values = (
        "abc123",                                                   # base36 thread id
        "a3f8c9e2b1d4f6a87c0e",                                     # hash-like node id (no marker)
        "orca_test:abc123:0",                                       # colon-bearing node id
        "https://old.reddit.com/r/orca_test/comments/abc123/x/",    # permalink
        "orca_test",                                                # subreddit name
        "run_001",                                                  # run id
        "bounded_probe_only",                                       # coverage claim
        "stopped: max_threads_per_subreddit reached",               # free-text stop reason
    )
    for value in legit_values:
        # Must not raise.
        assert_no_forbidden_output_fields({"node_id": value, "reason": value})


def test_same_run_traversal_is_rejected() -> None:
    with pytest.raises(RedditCandidateIntakeError) as exc_info:
        build_candidate_intake_output(
            envelope=_envelope(),
            provenance=_provenance(),
            candidate_threads=[
                CandidateThreadUrlRow(
                    run_id="run_001",
                    candidate_thread_url="https://old.reddit.com/r/orca_test/comments/abc123/durable_reddit_packet_spine/",
                    subreddit="orca_test",
                    source_surface=CandidateSurface.CROSS_POST,
                    query_or_seed="orca",
                    timestamp="2026-06-06T00:00:00Z",
                    method_category="static_fixture",
                    same_run_traversal_authorized=True,
                )
            ],
        )

    assert exc_info.value.code == "same_run_traversal_forbidden"


def test_promotion_receipt_requires_non_authorization_and_limitations() -> None:
    receipt = PromotionReceipt(
        promoted_url="https://old.reddit.com/r/orca_test/comments/abc123/durable_reddit_packet_spine/",
        originating_run_id="run_001",
        candidate_row_pointer="candidate_threads[0]",
        reason_for_promotion="operator selected for later capture",
        known_limitations=("bounded_probe_only", "caps_reached"),
        selected_downstream_capture_method="cloakbrowser_primary_anti_blocking",
        approved_downstream_access_route="cloakbrowser_primary_anti_blocking",
        decision_frame_or_capture_unit_authority=None,
        non_promoted_candidate_rows=("candidate_threads[1]",),
        capture_not_yet_authorized=True,
    )

    validate_promotion_receipt(receipt)

    bad_receipt = PromotionReceipt(
        promoted_url=receipt.promoted_url,
        originating_run_id=receipt.originating_run_id,
        candidate_row_pointer=receipt.candidate_row_pointer,
        reason_for_promotion=receipt.reason_for_promotion,
        known_limitations=receipt.known_limitations,
        selected_downstream_capture_method=receipt.selected_downstream_capture_method,
        approved_downstream_access_route=receipt.approved_downstream_access_route,
        decision_frame_or_capture_unit_authority=None,
        non_promoted_candidate_rows=receipt.non_promoted_candidate_rows,
        capture_not_yet_authorized=False,
    )
    with pytest.raises(RedditCandidateIntakeError) as exc_info:
        validate_promotion_receipt(bad_receipt)

    assert exc_info.value.code == "capture_authorization_leak"


def _envelope(**overrides: object) -> RunEnvelope:
    values = {
        "run_id": "run_001",
        "run_purpose": "static no-live-access test",
        "cap_type": CapType.PROBE,
        "coverage_claim": CoverageClaim.BOUNDED_PROBE_ONLY,
        "max_subreddits": 5,
        "max_threads_per_subreddit": 25,
        "max_pages_or_result_surfaces": 2,
        "time_window_days": 30,
        "sort_order": "top",
        "method_category": "static_fixture",
        "stop_condition": StopReason.CAPS_REACHED,
        "declared_topic_theme_query": "orca",
        "seed_subreddits": ("orca_test",),
    }
    values.update(overrides)
    return RunEnvelope(**values)


def _provenance(**overrides: object) -> RunProvenanceReceipt:
    values = {
        "run_id": "run_001",
        "caps_applied": {
            "max_subreddits": 5,
            "max_threads_per_subreddit": 25,
            "max_pages_or_result_surfaces": 2,
            "time_window_days": 30,
        },
        "source_surface": "subreddit_listing",
        "query_or_listing_path": "/r/orca_test/top",
        "sort_order": "top",
        "time_window_days": 30,
        "method_category": "static_fixture",
        "timestamp": "2026-06-06T00:00:00Z",
        "row_counts": {"candidate_subreddits": 1, "candidate_threads": 1, "outbound_urls": 1},
        "stop_reason": StopReason.CAPS_REACHED,
    }
    values.update(overrides)
    return RunProvenanceReceipt(
        **values,
    )
