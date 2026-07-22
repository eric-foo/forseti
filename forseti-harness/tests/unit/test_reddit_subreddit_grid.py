from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from capture_spine.reddit_subreddit_grid import (
    RegistryRefreshError,
    project_old_reddit_grid_html,
    read_grid_packet,
    refresh_lake_registry_from_grid_packets,
    refresh_registry_from_grid_packets,
)
from capture_spine.reddit_subreddit_grid.grid_projection import (
    GRID_PROJECTION_PARSER_VERSION,
    build_grid_content_record,
    grid_view_from_record,
)
from runners import run_reddit_grid_capture as grid_runner
from runners import run_source_capture_http_packet as http_packet_runner
from runners.run_reddit_grid_capture import (
    build_grid_listing_url,
    run_reddit_grid_capture,
)
from data_lake.reddit_subreddit_registry import (
    fold_subreddit,
    known_subreddits,
    migrate_legacy_registry,
)
from data_lake.root import DataLakeRoot
from source_capture.adapters.direct_http import DirectHttpCaptureSuccess
from source_capture.content_extraction import ContentExtractionSpec


GRID_HTML = """
<html><body>
<div class="titlebox">
  <span class="subscribers"><span class="number">7,491,826</span> members</span>
  <p class="users-online"><span class="number">12,345</span> online</p>
</div>
<div id="siteTable">
  <div class="thing link" data-permalink="/r/makeupaddiction/comments/aaa111/first_post/"
       data-subreddit="MakeupAddiction" data-score="4821" data-comments-count="382">
    <a class="title" href="/r/makeupaddiction/comments/aaa111/first_post/">First look post</a>
  </div>
  <div class="thing link" data-subreddit="MakeupAddiction">
    <a class="title" href="https://old.reddit.com/r/makeupaddiction/comments/bbb222/second_post/">Second post</a>
    <div class="score unvoted">1,204</div>
    <a class="comments" href="/r/makeupaddiction/comments/bbb222/second_post/">97 comments</a>
  </div>
  <div class="thing link promoted" data-permalink="/r/makeupaddiction/comments/ccc333/promo/"
       data-score="12" data-comments-count="1">
    <a class="title" href="/r/makeupaddiction/comments/ccc333/promo/">Sponsored thing</a>
  </div>
  <div class="thing link" data-permalink="/r/makeupaddiction/comments/aaa111/first_post/"
       data-score="4821" data-comments-count="382">
    <a class="title" href="/r/makeupaddiction/comments/aaa111/first_post/">Duplicate</a>
  </div>
</div>
</body></html>
"""


def _registry(path: Path) -> Path:
    registry = path / "registry.json"
    registry.write_text(
        json.dumps(
            {
                "reddit_subreddit_registry": {
                    "schema_version": "reddit_subreddit_registry_v0",
                    "counts": {
                        "subreddits_total": 1,
                        "by_status": {"unverified": 1},
                    },
                    "subreddits": [
                        {
                            "subreddit": "makeupaddiction",
                            "url": "https://www.reddit.com/r/makeupaddiction/",
                            "status": "unverified",
                            "status_observed_at": "2026-07-16",
                            "capture_state": "no_packet_recorded",
                            "observations": [],
                            "register_pointers": [],
                        }
                    ],
                }
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return registry


def _raw_grid_packet(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    *,
    status: int = 200,
) -> Path:
    url = "https://old.reddit.com/r/makeupaddiction/top/?t=day"

    def fake_fetch(**_: object) -> DirectHttpCaptureSuccess:
        return DirectHttpCaptureSuccess(
            requested_url=url,
            final_url=url,
            status=status,
            reason="OK" if status == 200 else "Not Found",
            metadata={
                "capture_timestamp": "2026-07-17T05:00:00Z",
                "requested_url": url,
                "final_url": url,
                "status": status,
            },
            body=GRID_HTML.encode(),
            warning_notes=[],
            limitation_notes=[],
        )

    monkeypatch.setattr(http_packet_runner, "fetch_direct_http_capture", fake_fetch)
    packet_dir = tmp_path / f"packet_{status}"
    exit_code, _ = http_packet_runner.run_source_capture_http_packet(
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
        timeout_seconds=5,
        max_bytes=1_000_000,
    )
    assert exit_code == 0
    return packet_dir


def test_grid_projection_preserves_titlebox_threads_nested_text_and_dedupes() -> None:
    nested = GRID_HTML.replace("First look post", "First <em>look</em> post")
    view = project_old_reddit_grid_html(
        html_text=nested,
        subreddit="makeupaddiction",
        listing_url="https://old.reddit.com/r/makeupaddiction/top/?t=day",
    )

    assert view.visible_subscriber_count_or_none == "7,491,826"
    assert view.visible_active_user_count_or_none == "12,345"
    assert len(view.thread_rows) == 3
    first, second, promoted = view.thread_rows
    assert first.visible_title_or_none == "First look post"
    assert first.visible_score_or_none == "4821"
    assert first.visible_comment_count_or_none == "382"
    assert second.visible_score_or_none == "1,204"
    assert second.visible_comment_count_or_none == "97"
    assert promoted.promoted


def test_grid_projection_reports_absent_volume_and_round_trips_content() -> None:
    empty = project_old_reddit_grid_html(
        html_text="<html><body><div id='siteTable'></div></body></html>",
        subreddit="makeupaddiction",
        listing_url="https://old.reddit.com/r/makeupaddiction/top/?t=day",
    )
    assert empty.visible_subscriber_count_or_none is None
    assert (
        empty.visible_volume_signal_absent_reason_or_none
        == "visible_volume_not_present_on_declared_surface"
    )

    record = build_grid_content_record(
        html_text=GRID_HTML,
        subreddit="makeupaddiction",
        listing_url="https://old.reddit.com/r/makeupaddiction/top/?t=day",
    )
    assert record["parser_version"] == GRID_PROJECTION_PARSER_VERSION
    assert grid_view_from_record(record) == project_old_reddit_grid_html(
        html_text=GRID_HTML,
        subreddit="makeupaddiction",
        listing_url="https://old.reddit.com/r/makeupaddiction/top/?t=day",
    )


def test_materializer_updates_once_and_dedupes_packet(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    registry = _registry(tmp_path)
    packet = _raw_grid_packet(tmp_path, monkeypatch)

    first = refresh_registry_from_grid_packets(
        registry_path=registry, packet_paths=[packet]
    )
    assert first.refreshed_subreddits == ["makeupaddiction"]
    assert first.status_changes == ["makeupaddiction"]

    second = refresh_registry_from_grid_packets(
        registry_path=registry, packet_paths=[packet]
    )
    assert second.refreshed_subreddits == []
    assert second.duplicate_observation_skips == ["makeupaddiction"]
    row = json.loads(registry.read_text(encoding="utf-8"))[
        "reddit_subreddit_registry"
    ]["subreddits"][0]
    assert row["status"] == "active"
    assert row["observations"][0]["subscriber_count_or_none"] == "7491826"
    assert len(row["observations"]) == 1


def test_materializer_rejects_off_domain_locator(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    packet = _raw_grid_packet(tmp_path, monkeypatch)
    manifest_path = packet / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["source_locator"]["value"] = "https://example.com/r/x/top/"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    with pytest.raises(RegistryRefreshError) as exc:
        read_grid_packet(packet_or_manifest_path=packet)
    assert exc.value.code == "locator_unparseable"


def test_materializer_rejects_preserved_body_outside_packet(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    packet = _raw_grid_packet(tmp_path, monkeypatch)
    manifest_path = packet / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    body = next(
        item
        for item in manifest["preserved_files"]
        if item["relative_packet_path"].endswith("http_response_body.bin")
    )
    original = packet / body["relative_packet_path"]
    escaped = tmp_path / "escaped.bin"
    shutil.copyfile(original, escaped)
    body["relative_packet_path"] = "../escaped.bin"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    with pytest.raises(RegistryRefreshError) as exc:
        read_grid_packet(packet_or_manifest_path=packet)
    assert exc.value.code == "preserved_file_unresolved"


def test_materializer_rejects_unsuccessful_raw_response(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    packet = _raw_grid_packet(tmp_path, monkeypatch, status=404)
    with pytest.raises(RegistryRefreshError) as exc:
        read_grid_packet(packet_or_manifest_path=packet)
    assert exc.value.code == "grid_access_unsuccessful"


def test_grid_listing_url_and_runner_content_extraction_contract(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    assert build_grid_listing_url(
        subreddit="r/fragrance", listing="rising", time_window=None
    ) == "https://old.reddit.com/r/fragrance/rising/"
    assert build_grid_listing_url(
        subreddit="MakeupAddiction", listing="top", time_window="day"
    ) == "https://old.reddit.com/r/makeupaddiction/top/?t=day"
    with pytest.raises(ValueError, match="top listing"):
        build_grid_listing_url(
            subreddit="fragrance", listing="hot", time_window="day"
        )

    calls: list[dict[str, object]] = []

    def fake_capture(**kwargs: object) -> tuple[int, str]:
        calls.append(kwargs)
        return 0, str(kwargs["output_directory"])

    monkeypatch.setattr(grid_runner, "run_source_capture_http_packet", fake_capture)
    monkeypatch.setattr(grid_runner.time, "sleep", lambda _: None)
    code, summary_path = run_reddit_grid_capture(
        subreddits=["MakeupAddiction"],
        listing="top",
        time_window="day",
        output_root=tmp_path / "run",
        decision_question="test",
        delay_seconds=0,
    )
    assert code == 0
    spec = calls[0]["content_extraction"]
    assert isinstance(spec, ContentExtractionSpec)
    assert spec.requested_retention_mode == "content"
    assert spec.extractor_version == GRID_PROJECTION_PARSER_VERSION
    assert calls[0]["url"] == (
        "https://old.reddit.com/r/makeupaddiction/top/?t=day"
    )
    summary = json.loads(Path(summary_path).read_text(encoding="utf-8"))
    assert summary["capture_success_count"] == 1
    assert summary["requested_retention_mode"] == "content"


def test_lake_materializer_appends_once_and_dedupes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The repointed writer appends to lake authority and never mutates a file."""
    registry = _registry(tmp_path)
    packet = _raw_grid_packet(tmp_path, monkeypatch)
    frozen = registry.read_bytes()
    lake = DataLakeRoot.for_test(tmp_path / "lake")
    migrate_legacy_registry(lake, registry_path=registry)

    first = refresh_lake_registry_from_grid_packets(data_root=lake, packet_paths=[packet])
    assert first.refreshed_subreddits == ["makeupaddiction"]
    assert first.records_written == 1

    second = refresh_lake_registry_from_grid_packets(data_root=lake, packet_paths=[packet])
    assert second.refreshed_subreddits == []
    assert second.duplicate_observation_skips == ["makeupaddiction"]
    assert second.records_written == 0

    row = fold_subreddit(lake, "makeupaddiction")
    assert row["status"] == "active"
    assert row["capture_state"] == "grid_packets_recorded"
    assert len(row["observations"]) == 1
    assert row["observations"][0]["subscriber_count_or_none"] == "7491826"
    assert row["register_pointers"] == [row["observations"][0]["provenance_pointer"]]
    assert registry.read_bytes() == frozen


def test_lake_materializer_reports_unknown_subreddit_without_adding_it(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    packet = _raw_grid_packet(tmp_path, monkeypatch)
    lake = DataLakeRoot.for_test(tmp_path / "lake")

    outcome = refresh_lake_registry_from_grid_packets(data_root=lake, packet_paths=[packet])
    assert outcome.unknown_subreddits == ["makeupaddiction"]
    assert outcome.records_written == 0
    assert known_subreddits(lake) == []


def test_lake_materializer_dry_run_writes_nothing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    registry = _registry(tmp_path)
    packet = _raw_grid_packet(tmp_path, monkeypatch)
    lake = DataLakeRoot.for_test(tmp_path / "lake")
    migrate_legacy_registry(lake, registry_path=registry)

    outcome = refresh_lake_registry_from_grid_packets(
        data_root=lake, packet_paths=[packet], dry_run=True
    )
    assert outcome.refreshed_subreddits == ["makeupaddiction"]
    assert outcome.records_written == 0
    assert fold_subreddit(lake, "makeupaddiction")["observations"] == []
