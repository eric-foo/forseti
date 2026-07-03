"""Unit tests for the ledger-driven YouTube RSS daily-monitor runner.

Everything runs lake-free-testable: fetch is an injected callable serving
fixture feed XML (packets are REAL commits into a ``DataLakeRoot.for_test``
lake), pacing is an injected ``sleep_fn``, the clock an injected ``now_fn``.
The load-bearing paths: baseline vs first-seen semantics across two runs
(lake-derived state, no sidecar store), per-channel failure visibility with a
nonzero exit, null-channel-id rows surfaced rather than dropped, the
consecutive-failure circuit break plus cooldown refusal, and committed-packet
readback (byte-identical raw XML, the new consumer-filterable surface name,
and honest metric postures).
"""
from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import pytest

from data_lake.root import DataLakeRoot
from runners.run_source_capture_youtube_rss_monitor import (
    ENTRIES_ARTIFACT_FILENAME,
    FEED_URL_TEMPLATE,
    SOURCE_SURFACE,
    YOUTUBE_RSS_MONITOR_EXIT_CODE_BREAK,
    ledger_youtube_channels,
    run_youtube_rss_monitor,
)

ALPHA = "UCalphaAlphaAlphaAlpha01"
BETA = "UCbetaBetaBetaBetaBeta02"


def _ledger(*rows: dict[str, Any]) -> dict[str, Any]:
    accounts = list(rows) + [
        {
            "platform_account_id": "acct_ig_001",
            "platform": "instagram",
            "platform_public_account_id_or_none": None,
            "public_handle": "someig",
        }
    ]
    return {"creator_public_handle_linkage_ledger": {"platform_accounts": accounts}}


def _yt_row(channel_id: str | None, *, account: str, handle: str = "somehandle") -> dict[str, Any]:
    return {
        "platform_account_id": account,
        "platform": "youtube",
        "platform_public_account_id_or_none": channel_id,
        "public_handle": handle,
    }


def _entry_xml(
    video_id: str,
    *,
    channel_id: str = ALPHA,
    views: str | None = "100",
    stars: str | None = "5",
) -> str:
    statistics = f'<media:statistics views="{views}"/>' if views is not None else ""
    star = f'<media:starRating count="{stars}" average="5.00" min="1" max="5"/>' if stars is not None else ""
    return (
        "<entry>"
        f"<yt:videoId>{video_id}</yt:videoId>"
        f"<yt:channelId>{channel_id}</yt:channelId>"
        f"<title>{video_id} title</title>"
        "<published>2026-07-02T09:00:05+00:00</published>"
        "<updated>2026-07-02T16:06:10+00:00</updated>"
        f"<media:group><media:community>{star}{statistics}</media:community></media:group>"
        "</entry>"
    )


def _feed_channel_id_as_served(channel_id: str) -> str:
    return channel_id[2:] if channel_id.startswith("UC") else channel_id


def _feed_xml(*entries: str, channel_id: str = ALPHA) -> bytes:
    return (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<feed xmlns:yt="http://www.youtube.com/xml/schemas/2015" '
        'xmlns:media="http://search.yahoo.com/mrss/" '
        'xmlns="http://www.w3.org/2005/Atom">'
        f"<yt:channelId>{_feed_channel_id_as_served(channel_id)}</yt:channelId>"
        "<title>Fixture Channel</title>"
        f"{''.join(entries)}"
        "</feed>"
    ).encode("utf-8")


class _FakeFetch:
    def __init__(self, responses: dict[str, Any]) -> None:
        self.responses = responses
        self.calls: list[str] = []

    def __call__(self, url: str) -> tuple[int, str, bytes]:
        self.calls.append(url)
        response = self.responses[url]
        if isinstance(response, Exception):
            raise response
        return response


def _url(channel_id: str) -> str:
    return FEED_URL_TEMPLATE.format(channel_id=channel_id)


def _now_fn():
    tick = {"count": 0}

    def now() -> datetime:
        tick["count"] += 1
        return datetime(2026, 7, 3, 8, 0, 0, tzinfo=UTC) + timedelta(seconds=tick["count"])

    return now


def _run(
    lake: DataLakeRoot,
    ledger: dict[str, Any],
    fetch: _FakeFetch,
    tmp_path: Path,
    **kwargs: Any,
) -> tuple[int, dict[str, Any]]:
    sleeps: list[float] = []
    exit_code, summary_path = run_youtube_rss_monitor(
        lake,
        ledger=ledger,
        fetch_fn=fetch,
        sleep_fn=sleeps.append,
        now_fn=kwargs.pop("now_fn", _now_fn()),
        output_root=tmp_path / "runs",
        cooldown_ledger_path=kwargs.pop("cooldown_ledger_path", tmp_path / "cooldown.json"),
        **kwargs,
    )
    summary = json.loads(Path(summary_path).read_text(encoding="utf-8"))
    summary["_sleep_calls"] = sleeps
    return exit_code, summary


def _entries_payload(lake: DataLakeRoot, packet_id: str) -> dict[str, Any]:
    loaded = lake.load_raw_packet(packet_id)
    for entry in loaded.manifest.get("preserved_files", []):
        basename = str(entry.get("relative_packet_path", "")).rsplit("/", 1)[-1]
        original = basename.split("_", 1)[1] if "_" in basename else basename
        if original == ENTRIES_ARTIFACT_FILENAME:
            return json.loads(loaded.bodies[entry["file_id"]].decode("utf-8"))
    raise AssertionError(f"packet {packet_id} carries no {ENTRIES_ARTIFACT_FILENAME}")


def _raw_feed_bytes(lake: DataLakeRoot, packet_id: str, channel_id: str) -> bytes:
    loaded = lake.load_raw_packet(packet_id)
    for entry in loaded.manifest.get("preserved_files", []):
        basename = str(entry.get("relative_packet_path", "")).rsplit("/", 1)[-1]
        original = basename.split("_", 1)[1] if "_" in basename else basename
        if original == f"feed_{channel_id}.xml":
            return loaded.bodies[entry["file_id"]]
    raise AssertionError(f"packet {packet_id} carries no raw feed for {channel_id}")


def _surface_packets(lake: DataLakeRoot) -> list[str]:
    return [
        packet_id
        for packet_id in lake.list_available(source_family="youtube")
        if (lake.read_availability(packet_id) or {}).get("source_surface") == SOURCE_SURFACE
    ]


def _iter_dicts(node: Any):
    if isinstance(node, dict):
        yield node
        for value in node.values():
            yield from _iter_dicts(value)
    elif isinstance(node, list):
        for item in node:
            yield from _iter_dicts(item)


def test_first_run_baseline_and_committed_readback(tmp_path: Path) -> None:
    lake = DataLakeRoot.for_test(tmp_path / "lake")
    alpha_feed = _feed_xml(_entry_xml("vidAlpha0001", views="1718", stars="42"))
    beta_feed = _feed_xml(
        _entry_xml("vidBeta00001", channel_id=BETA),
        _entry_xml("vidBeta00002", channel_id=BETA),
        channel_id=BETA,
    )
    fetch = _FakeFetch({_url(ALPHA): (200, _url(ALPHA), alpha_feed), _url(BETA): (200, _url(BETA), beta_feed)})
    ledger = _ledger(_yt_row(ALPHA, account="acct_a"), _yt_row(BETA, account="acct_b"))

    exit_code, summary = _run(lake, ledger, fetch, tmp_path)

    assert exit_code == 0
    assert summary["status"] == "completed"
    assert summary["counts"] == {
        "roster_total": 2,
        "attempted": 2,
        "captured": 2,
        "skipped_no_channel_id": 0,
        "capture_failed": 0,
        "not_attempted": 0,
    }
    # Pacing fires between channels only.
    assert len(summary["_sleep_calls"]) == 1

    packets = _surface_packets(lake)
    assert len(packets) == 2
    by_channel = {_entries_payload(lake, pid)["channel_id"]: pid for pid in packets}
    assert set(by_channel) == {ALPHA, BETA}

    alpha_payload = _entries_payload(lake, by_channel[ALPHA])
    assert alpha_payload["compared_prior_packet_id_or_none"] is None
    assert [e["first_seen"] for e in alpha_payload["entries"]] == ["baseline"]
    assert alpha_payload["entries"][0]["view_count_exact"] == 1718
    assert alpha_payload["entries"][0]["star_rating_count"] == 42
    assert alpha_payload["known_video_ids_cumulative"] == ["vidAlpha0001"]
    # Raw XML committed byte-for-byte (load_raw_packet re-hashes against the manifest).
    assert _raw_feed_bytes(lake, by_channel[ALPHA], ALPHA) == alpha_feed


def test_second_run_marks_only_new_video_first_seen(tmp_path: Path) -> None:
    lake = DataLakeRoot.for_test(tmp_path / "lake")
    ledger = _ledger(_yt_row(ALPHA, account="acct_a"))
    run1_feed = _feed_xml(_entry_xml("vidAlpha0001"), _entry_xml("vidAlpha0002"))
    fetch1 = _FakeFetch({_url(ALPHA): (200, _url(ALPHA), run1_feed)})
    exit1, _ = _run(lake, ledger, fetch1, tmp_path)
    assert exit1 == 0
    (run1_packet,) = _surface_packets(lake)

    # Run 2: one NEW video; vidAlpha0002 dropped out of the feed window.
    run2_feed = _feed_xml(_entry_xml("vidAlphaNEW1"), _entry_xml("vidAlpha0001"))
    fetch2 = _FakeFetch({_url(ALPHA): (200, _url(ALPHA), run2_feed)})
    exit2, _ = _run(lake, ledger, fetch2, tmp_path)
    assert exit2 == 0

    packets = _surface_packets(lake)
    assert len(packets) == 2
    run2_packet = next(pid for pid in packets if pid != run1_packet)
    payload = _entries_payload(lake, run2_packet)
    assert payload["compared_prior_packet_id_or_none"] == run1_packet
    flags = {e["video_id"]: e["first_seen"] for e in payload["entries"]}
    assert flags == {"vidAlphaNEW1": "true", "vidAlpha0001": "false"}
    # The dropped-out-of-window video stays known (first-seen is first-EVER-seen).
    assert payload["known_video_ids_cumulative"] == sorted(
        ["vidAlpha0001", "vidAlpha0002", "vidAlphaNEW1"]
    )


def test_prior_state_readback_failure_is_visible_not_baseline(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    lake = DataLakeRoot.for_test(tmp_path / "lake")
    ledger = _ledger(_yt_row(ALPHA, account="acct_a"))
    run1_feed = _feed_xml(_entry_xml("vidAlpha0001"))
    fetch1 = _FakeFetch({_url(ALPHA): (200, _url(ALPHA), run1_feed)})
    exit1, _ = _run(lake, ledger, fetch1, tmp_path)
    assert exit1 == 0
    (run1_packet,) = _surface_packets(lake)

    original_load_raw_packet = lake.load_raw_packet

    def fail_prior_packet(packet_id: str):
        if packet_id == run1_packet:
            raise RuntimeError("corrupt prior entries artifact")
        return original_load_raw_packet(packet_id)

    monkeypatch.setattr(lake, "load_raw_packet", fail_prior_packet)
    fetch2 = _FakeFetch(
        {_url(ALPHA): (200, _url(ALPHA), _feed_xml(_entry_xml("vidAlphaNEW1")))}
    )
    exit2, summary = _run(lake, ledger, fetch2, tmp_path)

    assert exit2 == 2
    assert summary["status"] == "completed_with_failures"
    assert summary["failed_channel_ids"] == [ALPHA]
    (failed_row,) = summary["results"]
    assert failed_row["attempted_at"] is None
    assert "prior rss monitor state derivation failed" in failed_row["packet_ref_or_error"]
    assert "corrupt prior entries artifact" in failed_row["packet_ref_or_error"]
    assert fetch2.calls == []
    assert _surface_packets(lake) == [run1_packet]


def test_equal_prior_retrieval_times_fail_visible_not_packet_id_guess(tmp_path: Path) -> None:
    lake = DataLakeRoot.for_test(tmp_path / "lake")
    ledger = _ledger(_yt_row(ALPHA, account="acct_a"))
    fixed_now = lambda: datetime(2026, 7, 3, 8, 0, 0, tzinfo=UTC)

    fetch1 = _FakeFetch({_url(ALPHA): (200, _url(ALPHA), _feed_xml(_entry_xml("vidA")))})
    exit1, _ = _run(lake, ledger, fetch1, tmp_path, now_fn=fixed_now)
    assert exit1 == 0

    fetch2 = _FakeFetch({_url(ALPHA): (200, _url(ALPHA), _feed_xml(_entry_xml("vidB")))})
    exit2, _ = _run(lake, ledger, fetch2, tmp_path, now_fn=fixed_now)
    assert exit2 == 0
    assert len(_surface_packets(lake)) == 2

    fetch3 = _FakeFetch({_url(ALPHA): (200, _url(ALPHA), _feed_xml(_entry_xml("vidC")))})
    exit3, summary = _run(lake, ledger, fetch3, tmp_path)

    assert exit3 == 2
    assert summary["status"] == "completed_with_failures"
    (failed_row,) = summary["results"]
    assert "ambiguous prior rss state" in failed_row["packet_ref_or_error"]
    assert fetch3.calls == []
    assert len(_surface_packets(lake)) == 2


def test_feed_channel_identity_mismatch_is_visible_failure(tmp_path: Path) -> None:
    lake = DataLakeRoot.for_test(tmp_path / "lake")
    ledger = _ledger(_yt_row(ALPHA, account="acct_a"))
    wrong_feed = _feed_xml(
        _entry_xml("vidBeta00001", channel_id=BETA),
        channel_id=BETA,
    )
    fetch = _FakeFetch({_url(ALPHA): (200, _url(ALPHA), wrong_feed)})

    exit_code, summary = _run(lake, ledger, fetch, tmp_path)

    assert exit_code == 2
    assert summary["status"] == "completed_with_failures"
    assert summary["failed_channel_ids"] == [ALPHA]
    (failed_row,) = summary["results"]
    assert "feed channel identity mismatch" in failed_row["packet_ref_or_error"]
    assert _surface_packets(lake) == []


def test_channel_failure_is_visible_and_exit_2(tmp_path: Path) -> None:
    lake = DataLakeRoot.for_test(tmp_path / "lake")
    ledger = _ledger(_yt_row(ALPHA, account="acct_a"), _yt_row(BETA, account="acct_b"))
    fetch = _FakeFetch(
        {
            _url(ALPHA): ConnectionError("network down"),
            _url(BETA): (
                200,
                _url(BETA),
                _feed_xml(_entry_xml("vidBeta00001", channel_id=BETA), channel_id=BETA),
            ),
        }
    )
    exit_code, summary = _run(lake, ledger, fetch, tmp_path)
    assert exit_code == 2
    assert summary["status"] == "completed_with_failures"
    assert summary["failed_channel_ids"] == [ALPHA]
    (failed_row,) = [r for r in summary["results"] if r["status"] == "capture_failed"]
    assert "ConnectionError" in failed_row["packet_ref_or_error"]
    assert len(_surface_packets(lake)) == 1


def test_http_non_200_and_non_feed_body_are_failures(tmp_path: Path) -> None:
    lake = DataLakeRoot.for_test(tmp_path / "lake")
    ledger = _ledger(_yt_row(ALPHA, account="acct_a"), _yt_row(BETA, account="acct_b"))
    fetch = _FakeFetch(
        {
            _url(ALPHA): (404, _url(ALPHA), b""),
            _url(BETA): (200, _url(BETA), b"<html><body>consent wall</body></html>"),
        }
    )
    exit_code, summary = _run(lake, ledger, fetch, tmp_path)
    assert exit_code == 2
    errors = {r["channel_id"]: r["packet_ref_or_error"] for r in summary["results"]}
    assert "http_status=404" in errors[ALPHA]
    assert "not_an_atom_feed" in errors[BETA]
    assert _surface_packets(lake) == []


def test_null_channel_id_row_is_skipped_visibly(tmp_path: Path) -> None:
    lake = DataLakeRoot.for_test(tmp_path / "lake")
    ledger = _ledger(_yt_row(None, account="acct_nullid"), _yt_row(ALPHA, account="acct_a"))
    fetch = _FakeFetch({_url(ALPHA): (200, _url(ALPHA), _feed_xml(_entry_xml("vidAlpha0001")))})
    exit_code, summary = _run(lake, ledger, fetch, tmp_path)
    assert exit_code == 0
    assert summary["counts"]["skipped_no_channel_id"] == 1
    assert summary["counts"]["captured"] == 1
    (skipped_row,) = [r for r in summary["results"] if r["status"] == "skipped_no_channel_id"]
    assert skipped_row["platform_account_id"] == "acct_nullid"
    assert fetch.calls == [_url(ALPHA)]


def test_consecutive_failures_trip_break_then_cooldown_refuses(tmp_path: Path) -> None:
    lake = DataLakeRoot.for_test(tmp_path / "lake")
    gamma = "UCgammaGammaGammaGamma03"
    ledger = _ledger(
        _yt_row(ALPHA, account="acct_a"),
        _yt_row(BETA, account="acct_b"),
        _yt_row(gamma, account="acct_c"),
    )
    fetch = _FakeFetch(
        {
            _url(ALPHA): ConnectionError("blocked"),
            _url(BETA): ConnectionError("blocked"),
            _url(gamma): ConnectionError("blocked"),
        }
    )
    cooldown_path = tmp_path / "cooldown.json"
    exit_code, summary = _run(
        lake, ledger, fetch, tmp_path, break_after_failures=2, cooldown_ledger_path=cooldown_path
    )
    assert exit_code == YOUTUBE_RSS_MONITOR_EXIT_CODE_BREAK
    assert summary["status"] == "stopped_circuit_break"
    assert "2 consecutive channel-capture failures" in summary["break_reason_or_none"]
    assert len(summary["results"]) == 2  # gamma never attempted
    assert cooldown_path.is_file()

    calls_before = len(fetch.calls)
    exit_again, summary_again = _run(
        lake, ledger, fetch, tmp_path, break_after_failures=2, cooldown_ledger_path=cooldown_path
    )
    assert exit_again == YOUTUBE_RSS_MONITOR_EXIT_CODE_BREAK
    assert summary_again["status"] == "cooldown_active"
    assert len(fetch.calls) == calls_before  # refused before any fetch


def test_metric_postures_are_honest_in_manifest(tmp_path: Path) -> None:
    lake = DataLakeRoot.for_test(tmp_path / "lake")
    ledger = _ledger(_yt_row(ALPHA, account="acct_a"))
    # One entry with exact metrics, one served without media:statistics.
    feed = _feed_xml(
        _entry_xml("vidAlpha0001", views="1718", stars="42"),
        _entry_xml("vidAlpha0002", views=None, stars=None),
    )
    fetch = _FakeFetch({_url(ALPHA): (200, _url(ALPHA), feed)})
    exit_code, _ = _run(lake, ledger, fetch, tmp_path)
    assert exit_code == 0
    (packet_id,) = _surface_packets(lake)
    manifest = lake.load_raw_packet(packet_id).manifest
    observations = [
        d
        for d in _iter_dicts(manifest)
        if isinstance(d.get("metric"), str) and d.get("posture") is not None
    ]
    assert observations, "manifest carries no metric observations"

    def postures(metric: str) -> set[tuple[str, Any]]:
        return {
            (str(d["posture"]).lower(), d.get("value"))
            for d in observations
            if d["metric"] == metric
        }

    view_postures = postures("view_count")
    assert any(p.endswith("observed") and v == 1718 for p, v in view_postures)
    assert any("unavailable_with_reason" in p and v is None for p, v in view_postures)
    # No zero-fill anywhere: absence is never stored as a value.
    assert not any(v == 0 for _p, v in view_postures)
    assert all("unavailable_with_reason" in p for p, _v in postures("comment_count"))


def test_ledger_without_youtube_rows_raises(tmp_path: Path) -> None:
    lake = DataLakeRoot.for_test(tmp_path / "lake")
    with pytest.raises(ValueError, match="no YouTube platform_accounts rows"):
        run_youtube_rss_monitor(
            lake,
            ledger=_ledger(),
            fetch_fn=_FakeFetch({}),
            sleep_fn=lambda _s: None,
            output_root=tmp_path / "runs",
            cooldown_ledger_path=tmp_path / "cooldown.json",
        )


def test_ledger_reader_filters_platforms() -> None:
    rows = ledger_youtube_channels(
        _ledger(_yt_row(ALPHA, account="acct_a"), _yt_row(None, account="acct_n"))
    )
    assert [row["platform_account_id"] for row in rows] == ["acct_a", "acct_n"]
    assert rows[0]["channel_id_or_none"] == ALPHA
    assert rows[1]["channel_id_or_none"] is None
