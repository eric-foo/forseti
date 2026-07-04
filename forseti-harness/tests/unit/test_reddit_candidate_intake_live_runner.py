from __future__ import annotations

import json
import shutil
import uuid
from pathlib import Path

import pytest

from capture_spine.reddit_candidate_intake import CandidateSurface
from runners.run_reddit_candidate_intake_live import run_reddit_candidate_intake_live


@pytest.fixture
def scratch_dir() -> Path:
    root = Path(__file__).resolve().parents[2] / "_test_runs"
    path = root / f"reddit_candidate_intake_live_{uuid.uuid4().hex}"
    path.mkdir(parents=True)
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


def test_live_runner_projects_related_subreddits_without_raw_source(scratch_dir: Path) -> None:
    exit_code, json_path = run_reddit_candidate_intake_live(
        output_directory=scratch_dir,
        run_id="live_related_seo_001",
        run_purpose="bounded live old Reddit related-subreddit intake",
        declared_topic_theme_query="b2b marketing adjacent subreddit scouting",
        source_url="https://old.reddit.com/r/SEO/",
        source_surface=CandidateSurface.RELATED_SUBREDDIT,
        seed_subreddits=("SEO",),
        max_subreddits=3,
        max_threads_per_subreddit=1,
        max_pages_or_result_surfaces=1,
        fetch_html=_related_subreddit_fetch,
    )

    artifact_text = Path(json_path).read_text(encoding="utf-8")
    artifact = json.loads(artifact_text)
    intake = artifact["reddit_candidate_url_intake"]

    assert exit_code == 0
    assert [row["candidate_subreddit"] for row in intake["candidate_subreddits"]] == [
        "webmarketing",
        "socialmedia",
        "PPC",
    ]
    assert intake["candidate_threads"] == []
    assert intake["provenance"]["stop_reason"] == "caps_reached"
    assert intake["live_run_receipt"]["access_mode"] == "old_reddit_direct_http_single_surface"
    assert intake["live_run_receipt"]["live_access_authorized_for_this_run"] is True
    assert intake["live_run_receipt"]["raw_source_persisted"] is False
    assert intake["live_run_receipt"]["armory_invoked"] is False
    assert intake["live_run_receipt"]["capture_packet_emitted"] is False
    assert "not Source Capture Packet output" in intake["non_claims"]
    assert "not Armory execution" in intake["non_claims"]
    assert "<html>" not in artifact_text
    assert "ordinary_person" not in artifact_text


def test_live_runner_projects_listing_threads_as_candidates_only(scratch_dir: Path) -> None:
    exit_code, json_path = run_reddit_candidate_intake_live(
        output_directory=scratch_dir,
        run_id="live_listing_b2b_001",
        run_purpose="bounded live old Reddit listing intake",
        declared_topic_theme_query="b2b meetings funnel",
        source_url="https://old.reddit.com/r/b2bmarketing/search/?q=meetings&restrict_sr=on&sort=top&t=year",
        source_surface=CandidateSurface.SUBREDDIT_LISTING,
        seed_subreddits=("b2bmarketing",),
        max_subreddits=1,
        max_threads_per_subreddit=1,
        max_pages_or_result_surfaces=1,
        sort_order="top",
        fetch_html=_listing_fetch,
    )

    artifact = json.loads(Path(json_path).read_text(encoding="utf-8"))
    intake = artifact["reddit_candidate_url_intake"]

    assert exit_code == 0
    assert intake["candidate_subreddits"] == []
    assert [row["candidate_thread_url"] for row in intake["candidate_threads"]] == [
        "https://old.reddit.com/r/b2bmarketing/comments/abc123/meetings_from_a_small_funnel/"
    ]
    assert intake["candidate_threads"][0]["allowed_downstream_use"] == "planning_only"
    assert intake["candidate_threads"][0]["same_run_traversal_authorized"] is False
    assert intake["provenance"]["stop_reason"] == "caps_reached"


def test_live_runner_writes_blocked_result_for_fetch_block(scratch_dir: Path) -> None:
    exit_code, json_path = run_reddit_candidate_intake_live(
        output_directory=scratch_dir,
        run_id="live_blocked_001",
        run_purpose="bounded live old Reddit blocked-result intake",
        declared_topic_theme_query="b2b marketing adjacent subreddit scouting",
        source_url="https://old.reddit.com/r/SEO/",
        source_surface=CandidateSurface.RELATED_SUBREDDIT,
        seed_subreddits=("SEO",),
        fetch_html=_blocked_fetch,
    )

    artifact = json.loads(Path(json_path).read_text(encoding="utf-8"))
    intake = artifact["reddit_candidate_url_intake"]

    assert exit_code == 0
    assert intake["candidate_subreddits"] == []
    assert intake["candidate_threads"] == []
    assert intake["provenance"]["stop_reason"] == "blocked_result"
    assert "ValueError: visible Reddit block page" in intake["live_run_receipt"]["status_note"]


def _related_subreddit_fetch(_url: str, _timeout_seconds: float, _max_bytes: int) -> tuple[int, str]:
    return 200, """
    <html>
      <body>
        <div class="side">
          <div class="titlebox">
            <h1 class="redditname"><a href="https://old.reddit.com/r/SEO/">SEO</a></h1>
            <div class="usertext-body may-blank-within md-container">
              <div class="md">
                <a href="https://old.reddit.com/r/webmarketing/">/r/webmarketing</a>
                <a href="https://old.reddit.com/r/socialmedia/">/r/socialmedia</a>
                <a href="https://old.reddit.com/r/PPC/">/r/PPC</a>
                <a href="https://old.reddit.com/r/analytics/">/r/analytics</a>
              </div>
            </div>
          </div>
        </div>
        <a class="author" href="/user/ordinary_person">ordinary_person</a>
      </body>
    </html>
    """


def _listing_fetch(_url: str, _timeout_seconds: float, _max_bytes: int) -> tuple[int, str]:
    return 200, """
    <html>
      <body>
        <a class="title may-blank" href="/r/b2bmarketing/comments/abc123/meetings_from_a_small_funnel/">
          Meetings from a small funnel
        </a>
        <a class="comments" href="/r/b2bmarketing/comments/abc123/meetings_from_a_small_funnel/">
          17 comments
        </a>
      </body>
    </html>
    """


def _blocked_fetch(_url: str, _timeout_seconds: float, _max_bytes: int) -> tuple[int, str]:
    raise ValueError("visible Reddit block page")
