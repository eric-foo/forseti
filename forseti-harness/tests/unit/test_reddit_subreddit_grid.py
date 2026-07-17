from __future__ import annotations

import hashlib
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
from capture_spine.reddit_subreddit_grid.grid_projection import (
    GRID_PROJECTION_PARSER_VERSION,
    build_grid_content_record,
    grid_view_from_record,
)
from runners import run_reddit_grid_capture as grid_runner
from runners import run_reddit_old_http_batch as batch_runner
from runners import run_source_capture_http_packet as http_packet_runner
from runners.run_reddit_grid_capture import build_grid_listing_url, run_reddit_grid_capture
from runners.run_reddit_old_http_batch import BatchSlot, run_reddit_old_http_batch
from runners.run_reddit_parser_fit_check import run_reddit_parser_fit_check
from source_capture.adapters.direct_http import DirectHttpCaptureSuccess
from source_capture.content_capture import ContentCaptureSpec


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


def _grid_content_spec(
    *,
    mode: str = "content",
    subreddit: str = "makeupaddiction",
    projector=None,
) -> ContentCaptureSpec:
    url = f"https://old.reddit.com/r/{subreddit}/top/?t=day"
    return ContentCaptureSpec(
        capture_artifact_mode=mode,
        parser_version=GRID_PROJECTION_PARSER_VERSION,
        projector=projector
        or (
            lambda html_text, final_url: build_grid_content_record(
                html_text=html_text, subreddit=subreddit, listing_url=url
            )
        ),
    )


def _write_grid_packet(
    scratch_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
    *,
    subreddit: str = "makeupaddiction",
    status: int = 200,
    content_capture: ContentCaptureSpec | None = None,
    expected_exit: int = 0,
) -> Path:
    url = f"https://old.reddit.com/r/{subreddit}/top/?t=day"

    def fake_fetch(**kwargs: object) -> DirectHttpCaptureSuccess:
        return DirectHttpCaptureSuccess(
            requested_url=url,
            final_url=url,
            status=status,
            reason="OK" if 200 <= status < 300 else "Not Found",
            metadata={
                "capture_timestamp": "2026-07-17T05:00:00Z",
                "requested_url": url,
                "final_url": url,
                "status": status,
            },
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
        content_capture=content_capture,
    )
    assert exit_code == expected_exit, message
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
        capture_artifact_mode="raw",
    )
    assert exit_code == 0
    capture_kwargs = calls[0][1]
    assert capture_kwargs["data_root"] is sentinel
    assert capture_kwargs["output_directory"] is None
    assert capture_kwargs["content_capture"] is None
    consolidate_kwargs = calls[1][1]
    assert consolidate_kwargs["packet_or_manifest_path"] == lake_packet_dir
    summary = json.loads(Path(message).read_text(encoding="utf-8"))
    assert summary["lake_committed"] is True
    assert summary["capture_artifact_mode"] == "raw"
    assert summary["results"][0]["packet_dir"] == str(lake_packet_dir)


def test_batch_runner_content_mode_parses_in_flight_and_skips_post_hoc(
    scratch_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    lake_packet_dir = scratch_dir / "lake" / "raw" / "abc" / "packet_z"
    captured_specs: list[object] = []

    def fake_capture(**kwargs: object) -> tuple[int, str]:
        captured_specs.append(kwargs["content_capture"])
        lake_packet_dir.mkdir(parents=True)
        (lake_packet_dir / "content_record.json").write_text("{}\n", encoding="utf-8")
        return 0, str(lake_packet_dir)

    def fail_consolidate(**kwargs: object) -> dict[str, str]:
        raise AssertionError("post-hoc consolidation must not run in content mode")

    monkeypatch.setattr(batch_runner, "run_source_capture_http_packet", fake_capture)
    monkeypatch.setattr(batch_runner, "consolidate_reddit_packet", fail_consolidate)
    monkeypatch.setattr(batch_runner.time, "sleep", lambda seconds: None)

    exit_code, message = run_reddit_old_http_batch(
        slots=[BatchSlot("slot_a", "https://old.reddit.com/r/SaaS/comments/abc/example/")],
        output_root=scratch_dir / "batch_content",
        decision_question="content batch?",
        data_root=object(),  # type: ignore[arg-type]
        delay_seconds=0.0,
    )
    assert exit_code == 0
    spec = captured_specs[0]
    assert isinstance(spec, ContentCaptureSpec)
    assert spec.capture_artifact_mode == "content"
    summary = json.loads(Path(message).read_text(encoding="utf-8"))
    assert summary["capture_artifact_mode"] == "content"
    row = summary["results"][0]
    assert row["consolidation_exit"] == 0
    assert row["consolidation_message"]["mode"] == "parse_in_flight"
    assert row["content_projection_failed"] is False


def test_batch_runner_content_mode_raw_fallback_runs_post_hoc_consolidation(
    scratch_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    calls: list[str] = []
    packet_dirs: list[Path] = []

    def fake_capture(**kwargs: object) -> tuple[int, str]:
        calls.append("capture")
        packet_dir = Path(kwargs["output_directory"])
        packet_dirs.append(packet_dir)
        packet_dir.mkdir(parents=True)
        (packet_dir / "http_response_body.bin").write_bytes(b"non-2xx response")
        return 0, str(packet_dir)

    def fake_consolidate(**kwargs: object) -> dict[str, str]:
        calls.append("consolidate")
        assert kwargs["packet_or_manifest_path"] == packet_dirs[0]
        return {
            "json_path": "x",
            "receipt_path": "y",
            "comment_count": "0",
            "observable_comment_node_count": "0",
        }

    monkeypatch.setattr(batch_runner, "run_source_capture_http_packet", fake_capture)
    monkeypatch.setattr(batch_runner, "consolidate_reddit_packet", fake_consolidate)

    _, message = run_reddit_old_http_batch(
        slots=[BatchSlot("slot_a", "https://old.reddit.com/r/SaaS/comments/abc/example/")],
        output_root=scratch_dir / "batch_raw_fallback",
        decision_question="Does raw fallback stay consumable?",
        delay_seconds=0.0,
    )

    summary = json.loads(Path(message).read_text(encoding="utf-8"))
    assert calls == ["capture", "consolidate"]
    row = summary["results"][0]
    assert row["content_projection_failed"] is False
    assert row["consolidation_exit"] == 0
    assert row["consolidation_message"]["json_path"] == "x"


def _single_file(packet_dir: Path, name_suffix: str) -> Path:
    matches = [path for path in packet_dir.rglob("*") if path.name.endswith(name_suffix)]
    assert len(matches) == 1, f"expected exactly one {name_suffix} in {packet_dir}, found {len(matches)}"
    return matches[0]


def _no_file(packet_dir: Path, name_suffix: str) -> None:
    matches = [path for path in packet_dir.rglob("*") if path.name.endswith(name_suffix)]
    assert not matches, f"expected no {name_suffix} in {packet_dir}, found {matches}"


def test_grid_content_record_round_trip() -> None:
    url = "https://old.reddit.com/r/makeupaddiction/top/?t=day"
    record = build_grid_content_record(
        html_text=GRID_HTML, subreddit="makeupaddiction", listing_url=url
    )
    assert record["record_kind"] == "reddit_subreddit_grid_view_v0"
    assert record["parser_version"] == GRID_PROJECTION_PARSER_VERSION
    rebuilt = grid_view_from_record(record)
    direct = project_old_reddit_grid_html(
        html_text=GRID_HTML, subreddit="makeupaddiction", listing_url=url
    )
    assert rebuilt == direct


def test_content_mode_packet_discards_raw_and_records_provenance(
    scratch_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import hashlib

    packet_dir = _write_grid_packet(
        scratch_dir, monkeypatch, content_capture=_grid_content_spec(mode="content")
    )
    _no_file(packet_dir, "http_response_body.bin")
    content_path = _single_file(packet_dir, "content_record.json")
    record = json.loads(content_path.read_text(encoding="utf-8"))
    assert record["record_kind"] == "reddit_subreddit_grid_view_v0"

    metadata_path = _single_file(packet_dir, "http_response_metadata.json")
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    block = metadata["content_capture"]
    assert block["capture_artifact_mode"] == "content"
    assert block["parser_version"] == GRID_PROJECTION_PARSER_VERSION
    assert block["raw_sha256"] == hashlib.sha256(GRID_HTML.encode("utf-8")).hexdigest()
    assert block["raw_byte_count"] == len(GRID_HTML.encode("utf-8"))
    assert block["raw_preserved"] is False
    assert block["projection_status"] == "succeeded"


def test_sample_mode_packet_preserves_raw_and_derived(
    scratch_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    packet_dir = _write_grid_packet(
        scratch_dir, monkeypatch, content_capture=_grid_content_spec(mode="sample")
    )
    _single_file(packet_dir, "http_response_body.bin")
    _single_file(packet_dir, "content_record.json")
    metadata = json.loads(
        _single_file(packet_dir, "http_response_metadata.json").read_text(encoding="utf-8")
    )
    assert metadata["content_capture"]["raw_preserved"] is True
    assert metadata["content_capture"]["projection_status"] == "succeeded"


def test_content_projection_failure_falls_back_to_raw(
    scratch_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def broken_projector(html_text: str, final_url: str) -> dict:
        raise ValueError("boom: markup changed")

    packet_dir = _write_grid_packet(
        scratch_dir,
        monkeypatch,
        content_capture=_grid_content_spec(mode="content", projector=broken_projector),
        expected_exit=4,
    )
    _single_file(packet_dir, "http_response_body.bin")
    _no_file(packet_dir, "content_record.json")
    metadata = json.loads(
        _single_file(packet_dir, "http_response_metadata.json").read_text(encoding="utf-8")
    )
    block = metadata["content_capture"]
    assert block["raw_preserved"] is True
    assert block["projection_status"].startswith("failed: ValueError: boom")


def test_non_object_content_projection_falls_back_to_raw(
    scratch_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def invalid_projector(html_text: str, final_url: str) -> dict:
        return []  # type: ignore[return-value]

    packet_dir = _write_grid_packet(
        scratch_dir,
        monkeypatch,
        content_capture=_grid_content_spec(mode="content", projector=invalid_projector),
        expected_exit=4,
    )
    _single_file(packet_dir, "http_response_body.bin")
    _no_file(packet_dir, "content_record.json")
    metadata = json.loads(
        _single_file(packet_dir, "http_response_metadata.json").read_text(encoding="utf-8")
    )
    assert metadata["content_capture"]["raw_preserved"] is True
    assert metadata["content_capture"]["projection_status"].startswith("failed: TypeError:")


def test_materializer_accepts_content_mode_packet(
    scratch_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    packet_dir = _write_grid_packet(
        scratch_dir, monkeypatch, content_capture=_grid_content_spec(mode="content")
    )
    registry_path = _mini_registry(scratch_dir)

    outcome = refresh_registry_from_grid_packets(
        registry_path=registry_path, packet_paths=[packet_dir]
    )
    assert outcome.refreshed_subreddits == ["makeupaddiction"]
    assert outcome.unknown_subreddits == []
    document = json.loads(registry_path.read_text(encoding="utf-8"))
    row = document["reddit_subreddit_registry"]["subreddits"][0]
    assert row["capture_state"] == "grid_packets_recorded"
    assert row["observations"][0]["subscriber_count_or_none"] == "7491826"


def test_parser_fit_check_match_drift_and_content_only_rejection(
    scratch_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    url = "https://old.reddit.com/r/makeupaddiction/top/?t=day"
    honest_dir = _write_grid_packet(
        scratch_dir, monkeypatch, content_capture=_grid_content_spec(mode="sample")
    )

    def tampering_projector(html_text: str, final_url: str) -> dict:
        record = build_grid_content_record(
            html_text=html_text, subreddit="makeupaddiction", listing_url=url
        )
        record["grid_view"]["visible_subscriber_count_or_none"] = "1"
        return record

    drifted_dir = _write_grid_packet(
        scratch_dir / "drifted",
        monkeypatch,
        content_capture=_grid_content_spec(mode="sample", projector=tampering_projector),
    )
    content_only_dir = _write_grid_packet(
        scratch_dir / "content_only",
        monkeypatch,
        content_capture=_grid_content_spec(mode="content"),
    )

    exit_code, report = run_reddit_parser_fit_check(
        packet_paths=[honest_dir, drifted_dir, content_only_dir],
        report_path=scratch_dir / "fit_report.json",
    )
    assert exit_code == 1
    by_status = {row["status"] for row in report["results"]}
    assert by_status == {"match", "drift", "check_failed"}
    assert report["match_count"] == 1
    assert report["drift_count"] == 1
    assert report["check_failure_count"] == 1
    drift_row = next(row for row in report["results"] if row["status"] == "drift")
    assert drift_row["diff_summary"]["differing_top_level_keys"] == ["grid_view"]

    honest_only_exit, honest_report = run_reddit_parser_fit_check(packet_paths=[honest_dir])
    assert honest_only_exit == 0
    assert honest_report["results"][0]["status"] == "match"


def test_parser_fit_check_rejects_record_subreddit_not_bound_to_packet(
    scratch_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    packet_dir = _write_grid_packet(
        scratch_dir, monkeypatch, content_capture=_grid_content_spec(mode="sample")
    )
    content_path = _single_file(packet_dir, "content_record.json")
    record = json.loads(content_path.read_text(encoding="utf-8"))
    record["grid_view"]["subreddit"] = "fragrance"
    content_path.write_text(
        json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    manifest_path = packet_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    content_entry = next(
        item
        for item in manifest["preserved_files"]
        if item["relative_packet_path"].endswith("content_record.json")
    )
    content_entry["sha256"] = hashlib.sha256(content_path.read_bytes()).hexdigest()
    manifest_path.write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    exit_code, report = run_reddit_parser_fit_check(packet_paths=[packet_dir])

    assert exit_code == 1
    row = report["results"][0]
    assert row["status"] == "check_failed"
    assert row["failure_code"] == "grid_subreddit_mismatch"
