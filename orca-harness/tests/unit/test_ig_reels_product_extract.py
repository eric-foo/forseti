"""Offline integration tests for the IG Reels product-extraction runner (IG transcript spine v0).

No network, no credentials. Commits real IG-Reel ASR transcripts into a temp lake, runs the
extractor through a fake transport, and asserts mentions land in the silver lane, that the runner
is idempotent (skip-if-done), that grid-metadata packets in the SAME instagram_creator family are
skipped (surface filter), and that failure is isolated at both grains.
"""
from __future__ import annotations

import json
from typing import Any

from cleaning.audience_extractor import RawApiProvider
from cleaning.transcript_product_lake import PRODUCT_MENTIONS_LANE, PRODUCT_MENTIONS_SET_LANE
from data_lake.root import DataLakeRoot
from schemas.audience_comment_models import AudienceComment
from runners.run_ig_reels_product_extract import (
    count_partial_extractions,
    count_pending_extractions,
    main,
    run_extraction,
)
from source_capture import (
    CaptureModeCategory,
    PacketTiming,
    SourceCaptureSlice,
    known_fact,
    not_applicable,
    not_attempted,
)
from source_capture.ig_reels_deep_capture import ReelDeepCaptureResult
from source_capture.ig_reels_deep_capture_lake import (
    deep_capture_record_id,
    write_reel_deep_capture_into_lake,
)
from source_capture.packet_assembly import staged_file_id_map, stage_and_write_packet
from source_capture.transcript.ig_reels_audio_packet import write_ig_reels_asr_transcript

_PROVIDER = RawApiProvider.ANTHROPIC_MESSAGES


def _cues() -> list[dict]:
    return [
        {"start_ms": 1000, "end_ms": 3000, "text": "Today I'm testing Dior Sauvage Elixir"},
        {"start_ms": 3000, "end_ms": 6000, "text": "and it is an absolute beast in the heat"},
    ]


def _item(**over: Any) -> dict[str, Any]:
    base = dict(
        brand="Dior", line="Sauvage Elixir", concentration="elixir", stance_vote=0.8,
        creator_authored=True, possible_negation_or_irony=False, extractor_confidence=0.9,
        source_pointer="absolute beast in the heat",
    )
    base.update(over)
    return base


def _anthropic(items: list[dict[str, Any]]) -> str:
    return json.dumps({"content": [{"type": "text", "text": json.dumps(items)}]})


class FakeTransport:
    def __init__(self, canned: str) -> None:
        self.canned = canned

    def post_json(self, url, headers, body, timeout_seconds):  # noqa: ANN001
        return self.canned


class RaiseThenValidTransport:
    def __init__(self, valid: str) -> None:
        self.valid = valid
        self.calls = 0

    def post_json(self, url, headers, body, timeout_seconds):  # noqa: ANN001
        self.calls += 1
        if self.calls == 1:
            raise RuntimeError("simulated provider error")
        return self.valid


def _commit_ig_audio_transcript(data_root, shortcode: str = "DZ69knlsDb1", posture: str = "transcribed") -> None:
    cues = _cues() if posture == "transcribed" else []
    write_ig_reels_asr_transcript(
        shortcode=shortcode, audio_bytes=f"fake-audio-{shortcode}".encode(), audio_ext="m4a",
        transcribe_fn=lambda _path: (posture, cues, {"tool": "faster-whisper", "model": "test"}),
        data_root=data_root,
    )


def _commit_ig_deep_capture(data_root, shortcode: str = "DZ69knlsDb1", posture: str = "transcribed") -> str:
    cues = tuple(_cues() if posture in {"ok", "transcribed"} else [])
    result = ReelDeepCaptureResult(
        reel_shortcode=shortcode,
        comments=(
            AudienceComment(
                comment_id=f"comment-{shortcode}",
                reel_shortcode=shortcode,
                author_username="zoe",
                text="works",
                like_count=1,
                created_at_unix=1782400000,
            ),
        ),
        transcript_posture=posture,
        transcript_cues=cues,
        media_url_used="https://x.fbcdn.net/o1/v/clip.mp4",
    )
    write_reel_deep_capture_into_lake(
        data_root=data_root,
        result=result,
        generated_at="2026-06-29T00:01:00Z",
    )
    return deep_capture_record_id(result)


def _commit_ig_grid_packet(data_root) -> None:
    """A non-audio instagram_creator packet (grid metadata surface) — must be skipped by the runner."""
    artifacts = [("grid.json", b'{"ok": true}')]
    file_ids = staged_file_id_map(artifacts)
    loc = known_fact("https://www.instagram.com/creatorhandle/")
    timing = PacketTiming(
        source_publication_or_event=not_attempted("n/a"),
        source_edit_or_version=not_applicable("n/a"),
        capture_time=known_fact("2026-06-25T00:00:00Z"),
        recapture_time=not_applicable("n/a"),
        cutoff_posture=not_applicable("n/a"),
    )
    access = known_fact("grid dom captured")
    media = not_applicable("grid metadata: no media bytes preserved")
    archive = not_attempted("n/a")
    recap = not_applicable("n/a")
    stage_and_write_packet(
        data_root=data_root,
        staged_artifacts=artifacts,
        source_slices=[
            SourceCaptureSlice(
                slice_id="slice_01", locator=loc, timing=timing,
                access_posture=access, archive_history_posture=archive,
                media_modality_posture=media, re_capture_relationship=recap,
                preserved_file_ids=[file_ids["grid.json"]],
            )
        ],
        source_family="instagram_creator",
        source_surface="ig_reels_grid_dom_passive_json",
        source_locator=loc,
        decision_question="Q",
        capture_context="ctx",
        actor_audience_context=not_applicable("n/a"),
        capture_mode=CaptureModeCategory.AUTOMATED_EXTRACTION,
        operator_category="ig_test",
        session_identity=None,
        visible_mode_changes=[],
        source_publication_or_event=timing.source_publication_or_event,
        source_edit_or_version=timing.source_edit_or_version,
        cutoff_posture=timing.cutoff_posture,
        recapture_time=timing.recapture_time,
        access_posture=access,
        archive_history_posture=archive,
        media_modality_posture=media,
        re_capture_relationship=recap,
        warnings=[],
        limitations=[],
        receipt_summary="ig grid metadata",
        receipt_non_claims=["test fixture"],
    )


def test_runner_extracts_ig_transcript_then_skips_on_rerun(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _commit_ig_audio_transcript(data_root)

    transport = FakeTransport(_anthropic([_item()]))
    first = run_extraction(data_root=data_root, transport=transport, provider=_PROVIDER, model="m", api_key="k")
    assert len(first) == 1
    assert first[0]["status"] == "extracted"
    assert first[0]["video_id"] == "DZ69knlsDb1"

    written = json.loads((data_root.path / first[0]["path"]).read_text(encoding="utf-8"))
    assert written["mention_count"] == 1
    assert written["mentions"][0]["start_ms"] == 3000  # CE5 timestamp from the cue
    assert written["mentions"][0]["video_id"] == "DZ69knlsDb1"

    second = run_extraction(data_root=data_root, transport=transport, provider=_PROVIDER, model="m", api_key="k")
    assert len(second) == 1
    assert second[0]["status"] == "skipped_done"


def test_runner_extracts_deep_capture_transcript_records(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    deep_record_id = _commit_ig_deep_capture(data_root)
    deep_key = f"DZ69knlsDb1:asr:{deep_record_id}"
    assert count_pending_extractions(data_root=data_root, model="m") == 1

    transport = FakeTransport(_anthropic([_item()]))
    first = run_extraction(data_root=data_root, transport=transport, provider=_PROVIDER, model="m", api_key="k")
    assert first == [
        {
            "anchor": "DZ69knlsDb1",
            "video_id": "DZ69knlsDb1",
            "transcript_source_key": deep_key,
            "source_route": "deep_capture_render_audio",
            "asr_record_id": deep_record_id,
            "status": "extracted",
            "path": first[0]["path"],
        }
    ]

    written = json.loads((data_root.path / first[0]["path"]).read_text(encoding="utf-8"))
    assert written["transcript_anchor"] == "DZ69knlsDb1"
    assert written["transcript_source"] == "asr"
    assert written["transcript_source_key"] == deep_key
    assert written["source_route"] == "deep_capture_render_audio"
    assert written["asr_record_id"] == deep_record_id

    second = run_extraction(data_root=data_root, transport=transport, provider=_PROVIDER, model="m", api_key="k")
    assert len(second) == 1
    assert second[0]["status"] == "skipped_done"
    assert second[0]["transcript_source_key"] == deep_key


def test_runner_extracts_legacy_ok_deep_capture_transcript_records(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    deep_record_id = _commit_ig_deep_capture(data_root, posture="ok")
    deep_key = f"DZ69knlsDb1:asr:{deep_record_id}"
    assert count_pending_extractions(data_root=data_root, model="m") == 1

    transport = FakeTransport(_anthropic([_item()]))
    first = run_extraction(data_root=data_root, transport=transport, provider=_PROVIDER, model="m", api_key="k")
    assert len(first) == 1
    assert first[0]["status"] == "extracted"
    assert first[0]["transcript_source_key"] == deep_key


def test_check_count_tracks_completed_mentions_for_model(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _commit_ig_audio_transcript(data_root)
    assert count_pending_extractions(data_root=data_root, model="m") == 1

    run_extraction(
        data_root=data_root, transport=FakeTransport(_anthropic([_item()])),
        provider=_PROVIDER, model="m", api_key="k",
    )
    assert count_pending_extractions(data_root=data_root, model="m") == 0
    assert count_partial_extractions(data_root=data_root, model="m") == 0
    assert count_pending_extractions(data_root=data_root, model="other-model") == 1


def test_check_cli_prints_pending_count(tmp_path, monkeypatch, capsys) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _commit_ig_audio_transcript(data_root)

    def fake_resolve(cls, *, explicit=None, **_kwargs):  # noqa: ANN001
        assert explicit is None
        return data_root

    monkeypatch.setattr(DataLakeRoot, "resolve", classmethod(fake_resolve))
    assert main(["--check", "--model", "m"]) == 0
    captured = capsys.readouterr()
    assert captured.out == "1\n"
    assert captured.err == ""

    assert main(["--check-partials", "--model", "m"]) == 0
    captured = capsys.readouterr()
    assert captured.out == "0\n"
    assert captured.err == ""


def test_runner_skips_grid_metadata_packet_in_same_family(tmp_path) -> None:
    # instagram_creator holds BOTH audio (ig_reels_audio) and grid packets; only audio is a transcript source.
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _commit_ig_grid_packet(data_root)
    _commit_ig_audio_transcript(data_root)
    results = run_extraction(
        data_root=data_root, transport=FakeTransport(_anthropic([_item()])),
        provider=_PROVIDER, model="m", api_key="k",
    )
    assert [r["status"] for r in results] == ["extracted"]  # the grid packet produced no transcript


def test_runner_empty_lake_yields_no_results(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    results = run_extraction(
        data_root=data_root, transport=FakeTransport(_anthropic([_item()])),
        provider=_PROVIDER, model="m", api_key="k",
    )
    assert results == []


def test_runner_skips_non_transcribed_asr(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _commit_ig_audio_transcript(data_root, "DaALKgOsWn0", posture="no_speech")
    results = run_extraction(
        data_root=data_root, transport=FakeTransport(_anthropic([_item()])),
        provider=_PROVIDER, model="m", api_key="k",
    )
    assert results == []


def test_runner_marks_zero_mention_transcript_done(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _commit_ig_audio_transcript(data_root)
    empty = FakeTransport(_anthropic([]))
    first = run_extraction(data_root=data_root, transport=empty, provider=_PROVIDER, model="m", api_key="k")
    assert len(first) == 1 and first[0]["status"] == "extracted"
    second = run_extraction(data_root=data_root, transport=empty, provider=_PROVIDER, model="m", api_key="k")
    assert second[0]["status"] == "skipped_done"


def test_runner_reports_partial_needs_cleanup(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _commit_ig_audio_transcript(data_root)
    transport = FakeTransport(_anthropic([_item()]))
    first = run_extraction(data_root=data_root, transport=transport, provider=_PROVIDER, model="m", api_key="k")
    assert first[0]["status"] == "extracted"
    marker = next((data_root.path / "derived").glob(f"**/{PRODUCT_MENTIONS_SET_LANE}/*"))
    marker.unlink()
    assert count_pending_extractions(data_root=data_root, model="m") == 0
    assert count_partial_extractions(data_root=data_root, model="m") == 1
    second = run_extraction(data_root=data_root, transport=transport, provider=_PROVIDER, model="m", api_key="k")
    assert second[0]["status"] == "partial_needs_cleanup"


def test_runner_isolates_per_item_extraction_failure(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _commit_ig_audio_transcript(data_root, "DZ69knlsDb1")
    _commit_ig_audio_transcript(data_root, "DaALKgOsWn0")
    transport = RaiseThenValidTransport(_anthropic([_item()]))
    results = run_extraction(data_root=data_root, transport=transport, provider=_PROVIDER, model="m", api_key="k")
    assert sorted(r["status"] for r in results) == ["extracted", "failed"]
