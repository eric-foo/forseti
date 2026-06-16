from __future__ import annotations

from dataclasses import replace

import pytest

from source_capture import historical_capture
from source_capture.adapters.archive_org import (
    ArchiveBodyVerification,
    ArchiveOrgCaptureFailure,
    ArchiveOrgCaptureSuccess,
    ArchiveOrgSnapshot,
)
from source_capture.adapters.archive_today import (
    ArchiveTodayBodyVerification,
    ArchiveTodayCaptureFailure,
    ArchiveTodayCaptureSuccess,
    ArchiveTodayMemento,
)
from source_capture.adapters.direct_http import (
    DirectHttpCaptureFailure,
    DirectHttpCaptureFailureKind,
    DirectHttpCaptureSuccess,
)
from source_capture.adapters.publisher_history import (
    PublisherHistoryCaptureFailure,
    PublisherHistoryCaptureSuccess,
    PublisherRevision,
)
from source_capture.historical_capture import (
    GitHubRung,
    MediaWikiRung,
    fetch_historical_capture,
)


def _ok_http(url: str, body: bytes = b"<html>body</html>") -> DirectHttpCaptureSuccess:
    return DirectHttpCaptureSuccess(
        requested_url=url,
        final_url=url,
        status=200,
        reason="OK",
        metadata={"capture_timestamp": "2024-01-01T00:00:00Z"},
        body=body,
        warning_notes=[],
        limitation_notes=[],
    )


def _fail_http(url: str) -> DirectHttpCaptureFailure:
    return DirectHttpCaptureFailure(
        requested_url=url,
        failure_kind=DirectHttpCaptureFailureKind.NO_BODY,
        message="empty body",
        status=404,
    )


# ----- canned adapter results -----------------------------------------------------------------


def _wayback(*, selected_ts: str | None, body_ok: bool | None = True) -> ArchiveOrgCaptureSuccess:
    snapshot = None
    body_result = None
    verification = None
    snapshots: list[ArchiveOrgSnapshot] = []
    if selected_ts is not None:
        snapshot = ArchiveOrgSnapshot(
            timestamp=selected_ts,
            original_url="https://example.com/page",
            snapshot_url=f"https://web.archive.org/web/{selected_ts}/https://example.com/page",
            status_code="200",
            mime_type="text/html",
            digest="D",
        )
        snapshots = [snapshot]
        if body_ok is None:
            body_result = _fail_http(snapshot.snapshot_url)
        else:
            body_result = _ok_http(snapshot.snapshot_url)
            verification = ArchiveBodyVerification(
                ok=body_ok,
                served_timestamp=selected_ts if body_ok else "20250101000000",
                reason=None if body_ok else "served_time_leak: ...",
            )
    return ArchiveOrgCaptureSuccess(
        original_url="https://example.com/page",
        availability_url="https://web.archive.org/cdx",
        availability_result=_ok_http("https://web.archive.org/cdx", body=b"[]"),
        snapshots=snapshots,
        selected_snapshot=snapshot,
        body_result=body_result,
        body_verification=verification,
    )


def _archive_today(*, selected_ts: str | None, body_ok: bool | None = True) -> ArchiveTodayCaptureSuccess:
    memento = None
    body_result = None
    verification = None
    mementos: list[ArchiveTodayMemento] = []
    if selected_ts is not None:
        memento = ArchiveTodayMemento(
            timestamp=selected_ts,
            original_url="https://example.com/page",
            memento_url=f"https://archive.md/{selected_ts}/https://example.com/page",
        )
        mementos = [memento]
        if body_ok is None:
            body_result = _fail_http(memento.memento_url)
        else:
            body_result = _ok_http(memento.memento_url)
            verification = ArchiveTodayBodyVerification(
                ok=body_ok,
                served_timestamp=selected_ts if body_ok else "20250101000000",
                reason=None if body_ok else "served_time_leak: ...",
            )
    return ArchiveTodayCaptureSuccess(
        original_url="https://example.com/page",
        timemap_url="https://archive.ph/timemap/https://example.com/page",
        timemap_result=_ok_http("https://archive.ph/timemap/https://example.com/page", body=b"<...>"),
        mementos=mementos,
        selected_memento=memento,
        body_result=body_result,
        body_verification=verification,
    )


def _publisher(*, selected: bool, body_ok: bool = True) -> PublisherHistoryCaptureSuccess:
    revision = None
    body_result = None
    if selected:
        revision = PublisherRevision(
            identity="rev123",
            served_timestamp="2024-01-01T00:00:00Z",
            content_url="https://en.wikipedia.org/w/api.php?revid=rev123",
        )
        body_result = _ok_http(revision.content_url) if body_ok else _fail_http(revision.content_url)
    return PublisherHistoryCaptureSuccess(
        rung="mediawiki_page_history",
        source_identity="https://en.wikipedia.org :: Example",
        listing_url="https://en.wikipedia.org/w/api.php",
        listing_result=_ok_http("https://en.wikipedia.org/w/api.php", body=b"{}"),
        revisions=[revision] if revision else [],
        selected_revision=revision,
        cutoff_timestamp="2024-06-01T00:00:00Z",
        body_result=body_result,
    )


def _patch(monkeypatch, *, wayback=None, archive_today=None, mediawiki=None, github=None, calls=None):
    if calls is None:
        calls = {}

    def make(name, value):
        def fake(**kwargs):
            calls.setdefault(name, []).append(kwargs)
            if isinstance(value, Exception):
                raise value
            return value
        return fake

    if wayback is not None:
        monkeypatch.setattr(historical_capture, "fetch_archive_org_capture", make("wayback", wayback))
    if archive_today is not None:
        monkeypatch.setattr(historical_capture, "fetch_archive_today_capture", make("archive_today", archive_today))
    if mediawiki is not None:
        monkeypatch.setattr(historical_capture, "fetch_mediawiki_history_capture", make("mediawiki", mediawiki))
    if github is not None:
        monkeypatch.setattr(historical_capture, "fetch_github_history_capture", make("github", github))
    return calls


# ----- tests ----------------------------------------------------------------------------------


def test_wayback_verified_body_stops_ladder_and_archive_today_not_tried(monkeypatch) -> None:
    calls = _patch(
        monkeypatch,
        wayback=_wayback(selected_ts="20240101000000", body_ok=True),
        archive_today=_archive_today(selected_ts="20240101000000", body_ok=True),
    )
    result = fetch_historical_capture(
        original_url="https://example.com/page", cutoff_timestamp_iso="2024-06-01T00:00:00Z"
    )
    assert result.archive_selected == "wayback"
    assert [outcome.rung for outcome in result.archives_tried] == ["wayback"]
    assert "archive_today" not in calls  # ladder stopped; second archive never queried
    assert result.selected_outcome is not None and result.selected_outcome.verified_body


def test_wayback_miss_escalates_to_archive_today(monkeypatch) -> None:
    _patch(
        monkeypatch,
        wayback=_wayback(selected_ts=None),
        archive_today=_archive_today(selected_ts="20240101000000", body_ok=True),
    )
    result = fetch_historical_capture(
        original_url="https://example.com/page", cutoff_timestamp_iso="2024-06-01T00:00:00Z"
    )
    assert result.archive_selected == "archive_today"
    assert [outcome.rung for outcome in result.archives_tried] == ["wayback", "archive_today"]
    assert result.archives_tried[0].located is False
    assert result.archives_tried[1].verified_body is True


def test_wayback_located_but_body_verification_fail_is_partial_and_escalates(monkeypatch) -> None:
    _patch(
        monkeypatch,
        wayback=_wayback(selected_ts="20240101000000", body_ok=False),  # served-time leak
        archive_today=_archive_today(selected_ts="20240101000000", body_ok=True),
    )
    result = fetch_historical_capture(
        original_url="https://example.com/page", cutoff_timestamp_iso="2024-06-01T00:00:00Z"
    )
    assert result.archive_selected == "archive_today"
    wayback_outcome = result.archives_tried[0]
    assert wayback_outcome.located is True and wayback_outcome.verified_body is False
    assert "verification failed" in wayback_outcome.body_detail


def test_wayback_non_2xx_body_is_partial_and_escalates(monkeypatch) -> None:
    wayback = _wayback(selected_ts="20240101000000", body_ok=True)
    assert wayback.selected_snapshot is not None
    rate_limited_body = DirectHttpCaptureSuccess(
        requested_url=wayback.selected_snapshot.snapshot_url,
        final_url=wayback.selected_snapshot.snapshot_url,
        status=429,
        reason="Too Many Requests",
        metadata={"capture_timestamp": "2024-01-01T00:00:00Z"},
        body=b"<html>rate limited</html>",
        warning_notes=[],
        limitation_notes=["access_failed: direct HTTP returned HTTP 429 Too Many Requests"],
    )
    _patch(
        monkeypatch,
        wayback=replace(wayback, body_result=rate_limited_body),
        archive_today=_archive_today(selected_ts="20240101000000", body_ok=True),
    )
    result = fetch_historical_capture(
        original_url="https://example.com/page", cutoff_timestamp_iso="2024-06-01T00:00:00Z"
    )
    assert result.archive_selected == "archive_today"
    wayback_outcome = result.archives_tried[0]
    assert wayback_outcome.located is True and wayback_outcome.verified_body is False
    assert "HTTP 429" in wayback_outcome.body_detail


def test_all_miss_is_honest_no_go(monkeypatch) -> None:
    _patch(
        monkeypatch,
        wayback=_wayback(selected_ts=None),
        archive_today=_archive_today(selected_ts=None),
    )
    result = fetch_historical_capture(
        original_url="https://example.com/page", cutoff_timestamp_iso="2024-06-01T00:00:00Z"
    )
    assert result.archive_selected is None
    assert result.selected_outcome is None
    assert [outcome.rung for outcome in result.archives_tried] == ["wayback", "archive_today"]
    assert all(outcome.verified_body is False for outcome in result.archives_tried)


def test_publisher_history_rung_runs_when_provided_and_general_archives_miss(monkeypatch) -> None:
    _patch(
        monkeypatch,
        wayback=_wayback(selected_ts=None),
        archive_today=_archive_today(selected_ts=None),
        mediawiki=_publisher(selected=True, body_ok=True),
    )
    result = fetch_historical_capture(
        original_url="https://en.wikipedia.org/wiki/Example",
        cutoff_timestamp_iso="2024-06-01T00:00:00Z",
        publisher_history_rung=MediaWikiRung(wiki_api_base="https://en.wikipedia.org", title="Example"),
    )
    assert result.archive_selected == "publisher_history:mediawiki"
    assert [outcome.rung for outcome in result.archives_tried] == [
        "wayback",
        "archive_today",
        "publisher_history:mediawiki",
    ]
    assert result.selected_outcome.verified_body is True


def test_publisher_history_skipped_without_cutoff(monkeypatch) -> None:
    _patch(
        monkeypatch,
        wayback=_wayback(selected_ts=None),
        archive_today=_archive_today(selected_ts=None),
        mediawiki=_publisher(selected=True),
    )
    result = fetch_historical_capture(
        original_url="https://en.wikipedia.org/wiki/Example",
        cutoff_timestamp_iso=None,
        publisher_history_rung=MediaWikiRung(wiki_api_base="https://en.wikipedia.org", title="Example"),
    )
    assert result.archive_selected is None
    publisher_outcome = result.archives_tried[-1]
    assert publisher_outcome.located is False
    assert "requires a cutoff" in publisher_outcome.locate_detail


def test_iso_cutoff_converted_to_14digit_for_general_archives_iso_for_publisher(monkeypatch) -> None:
    calls = _patch(
        monkeypatch,
        wayback=_wayback(selected_ts=None),
        archive_today=_archive_today(selected_ts=None),
        github=_publisher(selected=False),
    )
    fetch_historical_capture(
        original_url="https://github.com/o/r/blob/main/README.md",
        cutoff_timestamp_iso="2024-06-01T12:30:45Z",
        publisher_history_rung=GitHubRung(owner="o", repo="r", path="README.md"),
    )
    assert calls["wayback"][0]["cutoff_timestamp"] == "20240601123045"
    assert calls["archive_today"][0]["cutoff_timestamp"] == "20240601123045"
    assert calls["github"][0]["cutoff_timestamp"] == "2024-06-01T12:30:45Z"


def test_archive_today_gate_defeat_does_not_abort_ladder(monkeypatch) -> None:
    _patch(
        monkeypatch,
        wayback=_wayback(selected_ts=None),
        archive_today=ArchiveTodayCaptureFailure(
            original_url="https://example.com/page",
            timemap_url="https://archive.ph/timemap/https://example.com/page",
            timemap_result=_ok_http("https://archive.ph/timemap/x", body=b"just a moment"),
            gate_defeat_stop="challenge_detected (HTTP 403); marker 'just a moment' present",
            limitation_notes=["gate_defeat_stop: archive.today TimeMap ..."],
        ),
        mediawiki=_publisher(selected=True, body_ok=True),
    )
    result = fetch_historical_capture(
        original_url="https://example.com/page",
        cutoff_timestamp_iso="2024-06-01T00:00:00Z",
        publisher_history_rung=MediaWikiRung(wiki_api_base="https://en.wikipedia.org", title="Example"),
    )
    archive_today_outcome = result.archives_tried[1]
    assert archive_today_outcome.gate_defeat_stop is not None
    assert "gate-defeat STOP" in archive_today_outcome.locate_detail
    # the challenge STOP on archive.today did not abort the ladder -- publisher-history still ran.
    assert result.archive_selected == "publisher_history:mediawiki"


def test_include_archive_today_false_skips_second_archive(monkeypatch) -> None:
    calls = _patch(
        monkeypatch,
        wayback=_wayback(selected_ts=None),
        archive_today=_archive_today(selected_ts="20240101000000", body_ok=True),
    )
    result = fetch_historical_capture(
        original_url="https://example.com/page",
        cutoff_timestamp_iso="2024-06-01T00:00:00Z",
        include_archive_today=False,
    )
    assert result.archive_selected is None
    assert [outcome.rung for outcome in result.archives_tried] == ["wayback"]
    assert "archive_today" not in calls


def test_wayback_availability_failure_is_located_false(monkeypatch) -> None:
    _patch(
        monkeypatch,
        wayback=ArchiveOrgCaptureFailure(
            original_url="https://example.com/page",
            availability_url="https://web.archive.org/cdx",
            availability_result=DirectHttpCaptureFailure(
                requested_url="https://web.archive.org/cdx",
                failure_kind=DirectHttpCaptureFailureKind.NETWORK_ERROR,
                message="boom",
            ),
        ),
        archive_today=_archive_today(selected_ts=None),
    )
    result = fetch_historical_capture(
        original_url="https://example.com/page", cutoff_timestamp_iso="2024-06-01T00:00:00Z"
    )
    assert result.archives_tried[0].located is False
    assert "availability lookup failed" in result.archives_tried[0].locate_detail
    assert result.archive_selected is None


def test_rung_outcomes_carry_only_neutral_facts(monkeypatch) -> None:
    # INV-1: a RungOutcome records mechanical facts (located/verified_body/timestamp/detail), never a
    # score, weight, rank, or quality verdict.
    _patch(monkeypatch, wayback=_wayback(selected_ts="20240101000000", body_ok=True))
    result = fetch_historical_capture(
        original_url="https://example.com/page", cutoff_timestamp_iso="2024-06-01T00:00:00Z"
    )
    outcome = result.archives_tried[0]
    fields = set(vars(outcome).keys())
    assert fields == {
        "rung",
        "located",
        "verified_body",
        "selected_timestamp",
        "locate_detail",
        "body_detail",
        "result",
        "gate_defeat_stop",
    }
    for forbidden in ("score", "weight", "rank", "rating", "quality", "verdict", "confidence"):
        assert forbidden not in fields


def test_invalid_cutoff_raises_value_error(monkeypatch) -> None:
    _patch(monkeypatch, wayback=_wayback(selected_ts=None), archive_today=_archive_today(selected_ts=None))
    with pytest.raises(ValueError):
        fetch_historical_capture(
            original_url="https://example.com/page", cutoff_timestamp_iso="not-a-date"
        )
