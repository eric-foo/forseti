"""Offline tests for TikTok batch transcript product extraction."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from cleaning.audience_extractor import RawApiProvider
from cleaning.transcript_product_lake import PRODUCT_MENTIONS_LANE
from data_lake.root import DataLakeRoot
from runners.run_tiktok_product_extract import _transcripts_for_packet, run_extraction
from tiktok_batch_test_support import _commit_batch_packet, _stats, _video

_PROVIDER = RawApiProvider.ANTHROPIC_MESSAGES


def _subtitles(*, text: str, start: str = "00:00:01.000", end: str = "00:00:03.000") -> dict:
    return {
        "posture": "source_native_webvtt_captured",
        "cue_count": 1,
        "transcript_text": text,
        "transcript_text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "cues": [{"source_order": 0, "start": start, "end": end, "text": text}],
    }


def _video_with_transcript(video_id: str, text: str) -> dict:
    video = _video(video_id, stats=_stats(10_000, 1_000, 100))
    video["subtitles"] = _subtitles(text=text)
    return video


def _anthropic(items: list[dict]) -> str:
    return json.dumps({"content": [{"type": "text", "text": json.dumps(items)}]})


class FakeTransport:
    def __init__(self, responses: list[str]) -> None:
        self.responses = list(responses)
        self.calls = 0

    def post_json(self, url, headers, body, timeout_seconds):  # noqa: ANN001
        response = self.responses[self.calls]
        self.calls += 1
        return response


class FailFirstTransport(FakeTransport):
    def post_json(self, url, headers, body, timeout_seconds):  # noqa: ANN001
        self.calls += 1
        if self.calls == 1:
            raise RuntimeError("simulated provider failure")
        return self.responses[0]


def _mention(line: str, pointer: str) -> dict:
    return {
        "brand": "unknown",
        "line": line,
        "concentration": "unknown",
        "stance_vote": 0.5,
        "creator_authored": True,
        "possible_negation_or_irony": False,
        "extractor_confidence": 0.8,
        "source_pointer": pointer,
    }


def test_discovers_one_timed_lineage_closed_transcript_per_video(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    packet_id = _commit_batch_packet(
        root,
        videos=[
            _video_with_transcript("7650000000000000001", "City of Stars is excellent"),
            _video_with_transcript("7650000000000000002", "Nautica Voyage is great value"),
        ],
    )

    transcripts, discovery_failures = _transcripts_for_packet(root, packet_id)

    assert discovery_failures == []
    assert [item.video_id for item in transcripts] == [
        "7650000000000000001",
        "7650000000000000002",
    ]
    assert transcripts[0].cues == [
        {"start_ms": 1000, "end_ms": 3000, "text": "City of Stars is excellent"}
    ]
    assert transcripts[0].transcript_source_key.startswith(
        f"{packet_id}:tiktok:7650000000000000001:"
    )
    fields = transcripts[0].source_lineage.to_record_fields()
    assert fields["source_object"] == {
        "namespace": "tiktok",
        "kind": "transcript",
        "native_id": "7650000000000000001",
        "source_url": None,
    }
    assert fields["raw_refs"][0]["anchor"] == {
        "kind": "json_pointer",
        "value": "/videos/0/subtitles",
    }
    assert fields["raw_refs"][0]["sha256"]


def test_runner_extracts_all_videos_then_acknowledged_rerun_is_empty(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    packet_id = _commit_batch_packet(
        root,
        videos=[
            _video_with_transcript("7650000000000000001", "City of Stars is excellent"),
            _video_with_transcript("7650000000000000002", "Nautica Voyage is great value"),
        ],
    )
    transport = FakeTransport(
        [
            _anthropic([_mention("City of Stars", "City of Stars is excellent")]),
            _anthropic([_mention("Nautica Voyage", "Nautica Voyage is great value")]),
        ]
    )

    first = run_extraction(
        data_root=root,
        transport=transport,
        provider=_PROVIDER,
        model="test-model",
        api_key="k",
    )
    second = run_extraction(
        data_root=root,
        transport=transport,
        provider=_PROVIDER,
        model="test-model",
        api_key="k",
    )

    assert [row["status"] for row in first] == ["extracted", "extracted"]
    assert second == []
    assert transport.calls == 2
    records = sorted(
        root.lane_dir(subtree="derived", raw_anchor=packet_id, lane=PRODUCT_MENTIONS_LANE).iterdir()
    )
    assert len(records) == 2
    payloads = [json.loads(path.read_text(encoding="utf-8")) for path in records]
    assert {
        payload["payload"]["observation"]["subject"]["ref"]["native_id"]
        for payload in payloads
    } == {
        "7650000000000000001",
        "7650000000000000002",
    }
    assert all(payload["source_surface"].startswith("tiktok_") for payload in payloads)


def test_failed_sibling_is_retried_without_duplicate_success(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    _commit_batch_packet(
        root,
        videos=[
            _video_with_transcript("7650000000000000001", "City of Stars is excellent"),
            _video_with_transcript("7650000000000000002", "Nautica Voyage is great value"),
        ],
    )
    valid = _anthropic([_mention("Nautica Voyage", "Nautica Voyage is great value")])
    first_transport = FailFirstTransport([valid])

    first = run_extraction(
        data_root=root,
        transport=first_transport,
        provider=_PROVIDER,
        model="test-model",
        api_key="k",
    )
    second_transport = FakeTransport(
        [_anthropic([_mention("City of Stars", "City of Stars is excellent")])]
    )
    second = run_extraction(
        data_root=root,
        transport=second_transport,
        provider=_PROVIDER,
        model="test-model",
        api_key="k",
    )

    assert [row["status"] for row in first] == ["failed", "extracted"]
    assert [row["status"] for row in second] == ["extracted", "skipped_done"]
    assert second_transport.calls == 1


def test_malformed_timing_fails_discovery_without_provider_call(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    video = _video_with_transcript("7650000000000000001", "City of Stars")
    video["subtitles"] = _subtitles(text="City of Stars", start="not-a-time")
    _commit_batch_packet(root, videos=[video])
    transport = FakeTransport([])

    result = run_extraction(
        data_root=root,
        transport=transport,
        provider=_PROVIDER,
        model="test-model",
        api_key="k",
    )

    assert len(result) == 1
    assert result[0]["status"] == "discovery_failed"
    assert "invalid TikTok WebVTT timestamp" in result[0]["error"]
    assert transport.calls == 0


def test_one_malformed_sibling_does_not_block_or_drop_valid_sibling(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    good_video = _video_with_transcript("7650000000000000001", "City of Stars is excellent")
    bad_video = _video_with_transcript("7650000000000000002", "Nautica Voyage is great value")
    bad_video["subtitles"]["cues"][0]["start"] = "not-a-time"
    packet_id = _commit_batch_packet(root, videos=[good_video, bad_video])
    transport = FakeTransport(
        [_anthropic([_mention("City of Stars", "City of Stars is excellent")])]
    )

    first = run_extraction(
        data_root=root,
        transport=transport,
        provider=_PROVIDER,
        model="test-model",
        api_key="k",
    )

    by_video = {row.get("video_id"): row for row in first}
    assert by_video["7650000000000000001"]["status"] == "extracted"
    assert by_video["7650000000000000002"]["status"] == "discovery_failed"
    assert "invalid TikTok WebVTT timestamp" in by_video["7650000000000000002"]["error"]
    assert transport.calls == 1

    records = sorted(
        root.lane_dir(subtree="derived", raw_anchor=packet_id, lane=PRODUCT_MENTIONS_LANE).iterdir()
    )
    assert len(records) == 1

    # A packet with a still-unresolved malformed sibling is never acknowledged: it
    # re-surfaces every run, but the already-extracted good sibling is not redone.
    second = run_extraction(
        data_root=root,
        transport=FakeTransport([]),
        provider=_PROVIDER,
        model="test-model",
        api_key="k",
    )
    by_video_second = {row.get("video_id"): row for row in second}
    assert by_video_second["7650000000000000001"]["status"] == "skipped_done"
    assert by_video_second["7650000000000000002"]["status"] == "discovery_failed"
