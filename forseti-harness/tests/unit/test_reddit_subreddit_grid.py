from __future__ import annotations

import json
import shutil
import uuid
from pathlib import Path

import pytest

from capture_spine.reddit_subreddit_grid import (
    RegistryRefreshError,
    project_old_reddit_grid_html,
    refresh_registry_from_grid_packets,
)
from runners import run_reddit_grid_capture as grid_runner
from runners import run_reddit_old_http_batch as batch_runner
from runners import run_source_capture_http_packet as http_packet_runner
from runners.run_reddit_grid_capture import build_grid_listing_url, run_reddit_grid_capture
from runners.run_reddit_old_http_batch import BatchSlot, run_reddit_old_http_batch
from source_capture.adapters.direct_http import DirectHttpCaptureSuccess


GRID_HTML = """
<html><body>
<div class="side">
  <div class="titlebox">
    <span class="subscribers"><span class="number">7,491,826</span> members</span>
    <p class="users-online"><span class="number">12,345</span> online</p>
  </div>
</div>
<div id="siteTable">
  <div class="thing link" data-permalink="/r/makeupaddiction/comments/aaa111/first_post/"
       data-subreddit="MakeupAddiction" data-score="4821" data-comments-count="382">
    <a class="title" href="/r/makeupaddiction/comments/aaa111/first_post/">First look post</a>
  </div>
  <div class="thing link" data-subreddit="MakeupAddiction">
    <a class="title" href="https://old.reddit.com/r/makeupaddiction/comments/bbb222/second_post/">Second post</a>
    <div class="score unvoted">1,204</div>
    <a class="comments" href="https://old.reddit.com/r/makeupaddiction/comments/bbb222/second_post/">97 comments</a>
  </div>
  <div class="thing link promoted" data-permalink="/r/makeupaddiction/comments/ccc333/promo/"
       data-score="12" data-comments-count="1">
    <a class="title" href="/r/makeupaddiction/comments/ccc333/promo/">Sponsored thing</a>
  </div>
  <div class="thing link" data-permalink="/r/makeupaddiction/comments/aaa111/first_post/"
       data-score="4821" data-comments-count="382">
    <a class="title" href="/r/makeupaddiction/comments/aaa111/first_post/">Duplicate of first</a>
  </div>
</div>
</body></html>
"""


@pytest.fixture
def scratch_dir() -> Path:
    root = Path(__file__).resolve().parents[2] / "_test_runs"
    path = root / f"reddit_subreddit_grid_{uuid.uuid4().hex}"
    path.mkdir(parents=True)
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


def _mini_registry(path: Path) -> Path:
    document = {
        "reddit_subreddit_registry": {
            "schema_version": "reddit_subreddit_registry_v0",
            "counts": {"subreddits_total": 2, "by_status": {"active": 1, "unverified": 1}},
            "subreddits": [
                {
                    "subreddit": "makeupaddiction",
                    "url": "https://www.reddit.com/r/makeupaddiction/",
                    "status": "unverified",
                    "status_observed_at": "2026-07-16",
                    "capture_state": "no_packet_recorded",
                    "observations": [],
                    "register_pointers": [],
                },
                {
                    "subreddit": "fragrance",
                    "url": "https://www.reddit.com/r/fragrance/",
                    "status": "active",
                    "status_observed_at": "2026-07-16",
                    "capture_state": "thread_packets_recorded",
                    "observations": [],
                    "register_pointers": [],
                },
            ],
        }
    }
    registry_path = path / "registry.json"
    registry_path.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8", newline="\n")
    return registry_path


def _write_grid_packet(
    scratch_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
    *,
    subreddit: str = "makeupaddiction",
    status: int = 200,
) -> Path:
    url = f"https://old.reddit.com/r/{subreddit}/top/?t=day"

    def fake_fetch(**kwargs: object) -> DirectHttpCaptureSuccess:
        return DirectHttpCaptureSuccess(
            requested_url=url,
            final_url=url,
            status=status,
            reason="OK" if 200 <= status < 300 else "Not Found",
            metadata={"capture_timestamp": "2026-07-17T05:00:00Z"},
            body=GRID_HTML.encode("utf-8"),
            warning_notes=[],
            limitation_notes=[],
        )

    monkeypatch.setattr(http_packet_runner, "fetch_direct_http_capture", fake_fetch)
    packet_dir = scratch_dir / f"{subreddit}_grid_packet"
    exit_code, message = http_packet_runner.run_source_capture_http_packet(
        url=url,
        source_family="reddit_subreddit_grid",
        source_surface="old_reddit_direct_http",
        decision_question="test grid packet",
        output_directory=packet_dir,
        capture_context="test",
        operator_category="test_operator",
        capture_mode=http_packet_runner.CaptureModeCategory.STRUCTURED_ACCESS,
        session_id=None,
        actor_audience_context=None,
        visible_mode_changes=[],
        source_publication_or_event=None,
        source_edit_or_version=None,
        cutoff_posture=None,
        recapture_time=None,
        re_capture_relationship=None,
        warnings=[],
        limitations=[],
        timeout_seconds=5.0,
        max_bytes=1_000_000,
    )
    assert exit_code == 0, message
    return packet_dir


def test_grid_projection_reads_titlebox_and_thread_rows() -> None:
    view = project_old_reddit_grid_html(
        html_text=GRID_HTML,
        subreddit="makeupaddiction",
        listing_url="https://old.reddit.com/r/makeupaddiction/top/?t=day",
    )

    assert view.visible_subscriber_count_or_none == "7,491,826"
    assert view.visible_active_user_count_or_none == "12,345"
    assert view.visible_volume_signal_absent_reason_or_none is None

    assert [row.thread_url for row in view.thread_rows] == [
        "https://old.reddit.com/r/makeupaddiction/comments/aaa111/first_post/",
        "https://old.reddit.com/r/makeupaddiction/comments/bbb222/second_post/",
        "https://old.reddit.com/r/makeupaddiction/comments/ccc333/promo/",
    ]
    first, second, promo = view.thread_rows
    assert first.visible_score_or_none == "4821"
    assert first.visible_comment_count_or_none == "382"
    assert first.subreddit == "MakeupAddiction"
    assert not first.promoted
    assert second.visible_score_or_none == "1,204"
    assert second.visible_comment_count_or_none == "97"
    assert second.visible_title_or_none == "Second post"
    assert promo.promoted


def test_grid_projection_reports_absent_volume_signal() -> None:
    view = project_old_reddit_grid_html(
        html_text="<html><body><div id='siteTable'></div></body></html>",
        subreddit="makeupaddiction",
        listing_url="https://old.reddit.com/r/makeupaddiction/top/?t=day",
    )
    assert view.visible_subscriber_count_or_none is None
    assert view.visible_volume_signal_absent_reason_or_none == "visible_volume_not_present_on_declared_surface"
    assert view.thread_rows == ()


def test_grid_projection_preserves_nested_visible_text() -> None:
    html = """
    <html><body>
      <div class="titlebox">
        <span class="subscribers">
          <span class="number"><b>7,491</b>,826</span> members
        </span>
      </div>
      <div class="thing link" data-permalink="/r/makeupaddiction/comments/abc123/nested/">
        <a class="title" href="/r/makeupaddiction/comments/abc123/nested/">
          First <em>look</em> post
        </a>
        <div class="score unvoted"><span>1,</span>204</div>
        <a class="comments" href="/r/makeupaddiction/comments/abc123/nested/">
          <span>97</span> comments
        </a>
      </div>
    </body></html>
    """

    view = project_old_reddit_grid_html(
        html_text=html,
        subreddit="makeupaddiction",
        listing_url="https://old.reddit.com/r/makeupaddiction/top/?t=day",
    )

    assert view.visible_subscriber_count_or_none == "7,491,826"
    assert len(view.thread_rows) == 1
    row = view.thread_rows[0]
    assert row.visible_title_or_none == "First look post"
    assert row.visible_score_or_none == "1,204"
    assert row.visible_comment_count_or_none == "97"


def test_grid_projection_first_number_span_wins_per_field() -> None:
    html = """
    <html><body>
      <div class="titlebox">
        <span class="subscribers"><span class="number">7,491,826</span> members</span>
        <span class="other-widget"><span class="number">42</span> widgets</span>
      </div>
    </body></html>
    """

    view = project_old_reddit_grid_html(
        html_text=html,
        subreddit="makeupaddiction",
        listing_url="https://old.reddit.com/r/makeupaddiction/top/?t=day",
    )

    assert view.visible_subscriber_count_or_none == "7,491,826"


def test_materializer_applies_two_speed_rule_and_dedupes(
    scratch_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    registry_path = _mini_registry(scratch_dir)
    packet_dir = _write_grid_packet(scratch_dir, monkeypatch)

    outcome = refresh_registry_from_grid_packets(
        registry_path=registry_path,
        packet_paths=[packet_dir],
    )
    assert outcome.refreshed_subreddits == ["makeupaddiction"]
    assert outcome.registry_written
    assert outcome.status_changes == ["makeupaddiction"]

    document = json.loads(registry_path.read_text(encoding="utf-8"))
    row = next(
        item
        for item in document["reddit_subreddit_registry"]["subreddits"]
        if item["subreddit"] == "makeupaddiction"
    )
    assert row["status"] == "active"
    assert row["status_observed_at"] == "2026-07-17"
    assert row["capture_state"] == "grid_packets_recorded"
    assert row["descriptive_changes"][-1]["previous_value"] == "unverified"
    assert len(row["observations"]) == 1
    observation = row["observations"][0]
    assert observation["subscriber_count_or_none"] == "7491826"
    assert observation["active_user_count_or_none"] == "12345"
    assert observation["source_surface"] == "old_reddit_grid_packet"
    assert observation["observed_at"] == "2026-07-17"
    assert row["register_pointers"] == [observation["provenance_pointer"]]
    assert document["reddit_subreddit_registry"]["counts"]["by_status"] == {"active": 2}

    rerun = refresh_registry_from_grid_packets(
        registry_path=registry_path,
        packet_paths=[packet_dir],
    )
    assert rerun.duplicate_observation_skips == ["makeupaddiction"]
    assert rerun.refreshed_subreddits == []
    document = json.loads(registry_path.read_text(encoding="utf-8"))
    row = next(
        item
        for item in document["reddit_subreddit_registry"]["subreddits"]
        if item["subreddit"] == "makeupaddiction"
    )
    assert len(row["observations"]) == 1


def test_materializer_dedupes_relative_and_absolute_paths(
    scratch_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    registry_path = _mini_registry(scratch_dir)
    packet_dir = _write_grid_packet(scratch_dir, monkeypatch)
    monkeypatch.chdir(scratch_dir)

    first = refresh_registry_from_grid_packets(
        registry_path=registry_path,
        packet_paths=[Path(packet_dir.name)],
    )
    assert first.refreshed_subreddits == ["makeupaddiction"]

    second = refresh_registry_from_grid_packets(
        registry_path=registry_path,
        packet_paths=[packet_dir],
    )
    assert second.duplicate_observation_skips == ["makeupaddiction"]
    assert second.refreshed_subreddits == []

    document = json.loads(registry_path.read_text(encoding="utf-8"))
    row = next(
        item
        for item in document["reddit_subreddit_registry"]["subreddits"]
        if item["subreddit"] == "makeupaddiction"
    )
    assert len(row["observations"]) == 1
    assert Path(row["observations"][0]["provenance_pointer"]).is_absolute()


def test_materializer_rejects_off_domain_grid_locator(
    scratch_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    registry_path = _mini_registry(scratch_dir)
    packet_dir = _write_grid_packet(scratch_dir, monkeypatch)
    manifest_path = packet_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["source_locator"]["value"] = "https://example.com/r/makeupaddiction/top/?t=day"
    manifest_path.write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    with pytest.raises(RegistryRefreshError) as excinfo:
        refresh_registry_from_grid_packets(
            registry_path=registry_path,
            packet_paths=[packet_dir],
        )
    assert excinfo.value.code == "locator_unparseable"


def test_materializer_rejects_preserved_body_outside_packet(
    scratch_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    registry_path = _mini_registry(scratch_dir)
    packet_dir = _write_grid_packet(scratch_dir, monkeypatch)
    manifest_path = packet_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    body_file = next(
        item
        for item in manifest["preserved_files"]
        if item["relative_packet_path"].endswith("http_response_body.bin")
    )
    original_body = packet_dir / body_file["relative_packet_path"]
    escaped_body = scratch_dir / "escaped_http_response_body.bin"
    shutil.copyfile(original_body, escaped_body)
    body_file["relative_packet_path"] = "../escaped_http_response_body.bin"
    manifest_path.write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    with pytest.raises(RegistryRefreshError) as excinfo:
        refresh_registry_from_grid_packets(
            registry_path=registry_path,
            packet_paths=[packet_dir],
        )
    assert excinfo.value.code == "raw_body_outside_packet"


def test_materializer_rejects_hash_verified_unsuccessful_response(
    scratch_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    registry_path = _mini_registry(scratch_dir)
    packet_dir = _write_grid_packet(scratch_dir, monkeypatch, status=404)

    with pytest.raises(RegistryRefreshError) as excinfo:
        refresh_registry_from_grid_packets(
            registry_path=registry_path,
            packet_paths=[packet_dir],
        )
    assert excinfo.value.code == "grid_access_unsuccessful"


def test_materializer_does_not_regress_newer_status(
    scratch_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    registry_path = _mini_registry(scratch_dir)
    document = json.loads(registry_path.read_text(encoding="utf-8"))
    row = next(
        item
        for item in document["reddit_subreddit_registry"]["subreddits"]
        if item["subreddit"] == "makeupaddiction"
    )
    row["status"] = "banned"
    row["status_observed_at"] = "2026-07-18"
    registry_path.write_text(
        json.dumps(document, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    packet_dir = _write_grid_packet(scratch_dir, monkeypatch)

    outcome = refresh_registry_from_grid_packets(
        registry_path=registry_path,
        packet_paths=[packet_dir],
    )

    assert outcome.refreshed_subreddits == ["makeupaddiction"]
    assert outcome.status_changes == []
    document = json.loads(registry_path.read_text(encoding="utf-8"))
    row = next(
        item
        for item in document["reddit_subreddit_registry"]["subreddits"]
        if item["subreddit"] == "makeupaddiction"
    )
    assert row["status"] == "banned"
    assert row["status_observed_at"] == "2026-07-18"
    assert len(row["observations"]) == 1
    assert row["capture_state"] == "grid_packets_recorded"


def test_materializer_reports_unknown_subreddit_and_never_adds_rows(
    scratch_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    registry_path = _mini_registry(scratch_dir)
    packet_dir = _write_grid_packet(scratch_dir, monkeypatch, subreddit="notinregistry")

    outcome = refresh_registry_from_grid_packets(
        registry_path=registry_path,
        packet_paths=[packet_dir],
    )
    assert outcome.unknown_subreddits == ["notinregistry"]
    assert not outcome.registry_written
    document = json.loads(registry_path.read_text(encoding="utf-8"))
    assert len(document["reddit_subreddit_registry"]["subreddits"]) == 2


def test_materializer_refuses_non_grid_packets(scratch_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    registry_path = _mini_registry(scratch_dir)
    url = "https://old.reddit.com/r/makeupaddiction/comments/aaa111/first_post/"

    def fake_fetch(**kwargs: object) -> DirectHttpCaptureSuccess:
        return DirectHttpCaptureSuccess(
            requested_url=url,
            final_url=url,
            status=200,
            reason="OK",
            metadata={"capture_timestamp": "2026-07-17T05:00:00Z"},
            body=b"<html></html>",
            warning_notes=[],
            limitation_notes=[],
        )

    monkeypatch.setattr(http_packet_runner, "fetch_direct_http_capture", fake_fetch)
    packet_dir = scratch_dir / "thread_packet"
    exit_code, _ = http_packet_runner.run_source_capture_http_packet(
        url=url,
        source_family="reddit_thread",
        source_surface="old_reddit_direct_http",
        decision_question="test thread packet",
        output_directory=packet_dir,
        capture_context="test",
        operator_category="test_operator",
        capture_mode=http_packet_runner.CaptureModeCategory.STRUCTURED_ACCESS,
        session_id=None,
        actor_audience_context=None,
        visible_mode_changes=[],
        source_publication_or_event=None,
        source_edit_or_version=None,
        cutoff_posture=None,
        recapture_time=None,
        re_capture_relationship=None,
        warnings=[],
        limitations=[],
        timeout_seconds=5.0,
        max_bytes=1_000_000,
    )
    assert exit_code == 0

    with pytest.raises(RegistryRefreshError, match="not 'reddit_subreddit_grid'") as excinfo:
        refresh_registry_from_grid_packets(registry_path=registry_path, packet_paths=[packet_dir])
    assert excinfo.value.code == "ineligible_source_family"


def test_build_grid_listing_url_shapes() -> None:
    assert (
        build_grid_listing_url(subreddit="MakeupAddiction", listing="top", time_window="day")
        == "https://old.reddit.com/r/makeupaddiction/top/?t=day"
    )
    assert (
        build_grid_listing_url(subreddit="r/fragrance", listing="rising", time_window=None)
        == "https://old.reddit.com/r/fragrance/rising/"
    )
    with pytest.raises(ValueError, match="top listing"):
        build_grid_listing_url(subreddit="fragrance", listing="hot", time_window="day")
    with pytest.raises(ValueError, match="invalid subreddit"):
        build_grid_listing_url(subreddit="bad name!", listing="hot", time_window=None)
    with pytest.raises(ValueError, match="invalid subreddit"):
        build_grid_listing_url(subreddit="café", listing="hot", time_window=None)


def test_grid_runner_builds_urls_caps_and_summary(
    scratch_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    calls: list[dict[str, object]] = []

    def fake_capture(**kwargs: object) -> tuple[int, str]:
        calls.append(kwargs)
        return 0, str(kwargs["output_directory"])

    monkeypatch.setattr(grid_runner, "run_source_capture_http_packet", fake_capture)
    monkeypatch.setattr(grid_runner.time, "sleep", lambda seconds: None)

    exit_code, message = run_reddit_grid_capture(
        subreddits=["MakeupAddiction", "fragrance"],
        listing="top",
        time_window="day",
        output_root=scratch_dir / "grid",
        decision_question="test grid batch",
        delay_seconds=0.0,
    )
    assert exit_code == 0
    assert [call["url"] for call in calls] == [
        "https://old.reddit.com/r/makeupaddiction/top/?t=day",
        "https://old.reddit.com/r/fragrance/top/?t=day",
    ]
    assert all(call["source_family"] == "reddit_subreddit_grid" for call in calls)
    assert all(call["data_root"] is None for call in calls)
    summary = json.loads(Path(message).read_text(encoding="utf-8"))
    assert summary["runner"] == "reddit_grid_capture"
    assert summary["capture_success_count"] == 2
    assert summary["lake_committed"] is False
    assert "source_policy_posture" in summary

    with pytest.raises(ValueError, match="max_subreddits"):
        run_reddit_grid_capture(
            subreddits=["a1", "b2"],
            listing="hot",
            time_window=None,
            output_root=scratch_dir / "grid2",
            decision_question="q",
            max_subreddits=1,
        )
    with pytest.raises(ValueError, match="duplicate subreddit"):
        run_reddit_grid_capture(
            subreddits=["same", "SAME"],
            listing="hot",
            time_window=None,
            output_root=scratch_dir / "grid3",
            decision_question="q",
        )

    invalid_output_root = scratch_dir / "invalid_grid"
    with pytest.raises(ValueError, match="timeout_seconds"):
        run_reddit_grid_capture(
            subreddits=["makeupaddiction"],
            listing="hot",
            time_window=None,
            output_root=invalid_output_root,
            decision_question="q",
            timeout_seconds=0,
        )
    assert not invalid_output_root.exists()


def test_grid_runner_threads_data_root_through(scratch_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    sentinel = object()
    calls: list[dict[str, object]] = []

    def fake_capture(**kwargs: object) -> tuple[int, str]:
        calls.append(kwargs)
        return 0, str(scratch_dir / "lake" / "raw" / "abc" / "packet_x")

    monkeypatch.setattr(grid_runner, "run_source_capture_http_packet", fake_capture)

    exit_code, message = run_reddit_grid_capture(
        subreddits=["makeupaddiction"],
        listing="hot",
        time_window=None,
        output_root=scratch_dir / "grid_lake",
        data_root=sentinel,  # type: ignore[arg-type]
        decision_question="test lake grid",
    )
    assert exit_code == 0
    assert calls[0]["data_root"] is sentinel
    assert calls[0]["output_directory"] is None
    summary = json.loads(Path(message).read_text(encoding="utf-8"))
    assert summary["lake_committed"] is True
    assert summary["results"][0]["packet_path"].endswith("packet_x")


def test_batch_runner_threads_data_root_and_consolidates_lake_packet(
    scratch_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    sentinel = object()
    lake_packet_dir = scratch_dir / "lake" / "raw" / "abc" / "packet_y"
    calls: list[tuple[str, dict[str, object]]] = []

    def fake_capture(**kwargs: object) -> tuple[int, str]:
        calls.append(("capture", kwargs))
        lake_packet_dir.mkdir(parents=True)
        return 0, str(lake_packet_dir)

    def fake_consolidate(**kwargs: object) -> dict[str, str]:
        calls.append(("consolidate", kwargs))
        return {"json_path": "x", "receipt_path": "y", "comment_count": "0", "observable_comment_node_count": "0"}

    monkeypatch.setattr(batch_runner, "run_source_capture_http_packet", fake_capture)
    monkeypatch.setattr(batch_runner, "consolidate_reddit_packet", fake_consolidate)
    monkeypatch.setattr(batch_runner.time, "sleep", lambda seconds: None)

    exit_code, message = run_reddit_old_http_batch(
        slots=[BatchSlot("slot_a", "https://old.reddit.com/r/SaaS/comments/abc/example/")],
        output_root=scratch_dir / "batch_lake",
        decision_question="lake batch?",
        data_root=sentinel,  # type: ignore[arg-type]
        delay_seconds=0.0,
    )
    assert exit_code == 0
    capture_kwargs = calls[0][1]
    assert capture_kwargs["data_root"] is sentinel
    assert capture_kwargs["output_directory"] is None
    consolidate_kwargs = calls[1][1]
    assert consolidate_kwargs["packet_or_manifest_path"] == lake_packet_dir
    summary = json.loads(Path(message).read_text(encoding="utf-8"))
    assert summary["lake_committed"] is True
    assert summary["results"][0]["packet_dir"] == str(lake_packet_dir)
