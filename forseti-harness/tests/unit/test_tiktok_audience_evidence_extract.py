from __future__ import annotations
import hashlib, json
from pathlib import Path

from cleaning.audience_extractor import RawApiProvider
from cleaning.tiktok_audience_evidence_extractor import AudienceTranscript, pack_transcripts, parse_response, synthesize_profiles
from cleaning.transcript_product_extractor import TranscriptInput
from cleaning.tiktok_audience_evidence_lake import (
    AUDIENCE_EVIDENCE_LANE, AUDIENCE_EVIDENCE_SET_LANE, audience_record_id, write_result,
)
from data_lake.root import DataLakeRoot
from runners.run_tiktok_audience_evidence_extract import run_extraction
from source_capture.models import (
    CaptureModeCategory, PacketTiming, SourceCaptureSlice, known_fact, not_applicable, not_attempted,
)
from source_capture.packet_assembly import stage_and_write_packet, staged_file_id_map
from test_tiktok_creator_metric_seed import _commit_batch_packet, _stats, _video


def _transcript(creator: str, video: str, text: str) -> AudienceTranscript:
    return AudienceTranscript(creator, TranscriptInput(video, "packet", "asr", [{"start_ms": 0, "end_ms": 1000, "text": text}], transcript_source_key=f"key:{video}"))


def _caption_video(video_id: str, text: str, handle: str) -> dict:
    video = _video(video_id, stats=_stats(1000, 100, 10), handle=handle)
    video["subtitles"] = {
        "posture": "source_native_webvtt_captured",
        "cues": [{"start": "00:00:00.000", "end": "00:00:01.000", "text": text}],
        "transcript_text": text,
        "transcript_text_sha256": hashlib.sha256(text.encode()).hexdigest(),
    }
    return video


def test_packer_never_mixes_creators() -> None:
    items = [_transcript("a", "v1", "one"), _transcript("b", "v2", "two")]
    batches = pack_transcripts(items, max_input_chars=1000)
    assert [[item.creator_id for item in batch] for batch in batches] == [["a"], ["b"]]


def test_parser_partitions_by_creator_and_rejects_demographics() -> None:
    items = [_transcript("a", "v1", "compare affordable alternatives"), _transcript("b", "v2", "advanced collectors debate")]
    rows = [
        {"creator_id": "a", "video_id": "v1", "audience_layer": "beneficiary_content_fit", "dimension": "value_sought", "label": "comparison-led alternative evaluation", "content_pillar": "comparisons", "vote": 1, "source_pointer": "compare affordable alternatives", "possible_negation_or_irony": False},
        {"creator_id": "b", "video_id": "v2", "audience_layer": "addressed_audience", "dimension": "category_relationship", "label": "wealthy men", "content_pillar": "collector debate", "vote": 1, "source_pointer": "advanced collectors debate", "possible_negation_or_irony": False},
    ]
    result = parse_response(json.dumps(rows), items, model="m")
    assert len(result[("a", "v1")].evidence) == 1
    assert result[("b", "v2")].rejected[0]["reason"] == "demographic_inference_forbidden"


def test_parser_rejects_demographic_inference_in_content_pillar() -> None:
    item = AudienceTranscript("a", TranscriptInput("v1", "anchor", "source", [{"start": 0.0, "text": "compare affordable alternatives"}]))
    rows = [{"creator_id": "a", "video_id": "v1", "audience_layer": "beneficiary_content_fit",
             "dimension": "value_sought", "label": "comparison shoppers", "content_pillar": "wealthy collectors",
             "vote": 1, "source_pointer": "compare affordable alternatives", "possible_negation_or_irony": False}]
    result = parse_response(json.dumps(rows), [item], model="model")[("a", "v1")]
    assert not result.evidence
    assert result.rejected[0]["reason"] == "demographic_inference_forbidden"


def test_profile_synthesis_rejects_demographic_inference_outside_primary_hypothesis() -> None:
    item = AudienceTranscript("a", TranscriptInput("v1", "anchor", "source", [{"start": 0.0, "text": "compare affordable alternatives"}]))
    evidence_rows = [{"creator_id": "a", "video_id": "v1", "audience_layer": "beneficiary_content_fit",
                      "dimension": "value_sought", "label": "comparison shoppers", "content_pillar": "comparisons",
                      "vote": 1, "source_pointer": "compare affordable alternatives", "possible_negation_or_irony": False}]
    evidence = parse_response(json.dumps(evidence_rows), [item], model="model")[("a", "v1")].evidence

    class Transport:
        def post_json(self, url, headers, body, timeout_seconds):
            return json.dumps({"output_text": json.dumps([{
                "creator_id": "a", "primary_hypothesis": "Comparison-led fragrance shoppers.",
                "knowledge_level": "category-aware", "shopping_stage": "comparison",
                "product_range": ["affordable alternatives"], "recurring_decision_jobs": ["judge replacement fit"],
                "engagement_style": "direct comparison", "price_posture": "value-aware",
                "likely_exclusions": ["wealthy collectors"], "evidence_ids": [evidence[0].evidence_id],
                "counterevidence_ids": [], "support_band": "medium", "actual_audience": "not_estimated",
            }])})

    import pytest
    with pytest.raises(ValueError, match="forbidden demographic inference"):
        synthesize_profiles(evidence_by_creator={"a": evidence}, transport=Transport(),
                            provider=RawApiProvider.OPENAI_RESPONSES, model="model", api_key="secret")


def _commit_non_batch_tiktok_packet(data_root: DataLakeRoot, *, handle: str = "gamma") -> str:
    """A committed TikTok packet sharing source_family="tiktok" but NOT the
    batch-admission surface (mirrors a single-video SCI packet) -- it has no
    preserved batch capture JSON, so it is not this consumer's work."""
    staged = [("fixture_video_admission.json", json.dumps({"video_id": "v9"}).encode("utf-8"))]
    file_ids = staged_file_id_map(staged)
    locator = f"https://www.tiktok.com/@{handle}/video/v9"
    timing = PacketTiming(
        source_publication_or_event=known_fact("fixture single-video window"),
        source_edit_or_version=not_applicable("fixture single-video packet"),
        capture_time=known_fact("2026-06-30T17:48:37Z"),
        recapture_time=not_applicable("fixture single-video packet"),
        cutoff_posture=not_applicable("fixture single-video packet"),
    )
    access = known_fact("sanitized parsed TikTok staging admission (fixture)")
    archive = not_attempted("fixture single-video packet does not query archive services")
    media = known_fact("parsed fields preserved; no raw media bytes (fixture)")
    recapture = not_applicable("fixture single-video packet")
    limitations = ["fixture only"]
    result = stage_and_write_packet(
        data_root=data_root,
        staged_artifacts=staged,
        source_slices=[
            SourceCaptureSlice(
                slice_id="tiktok_video_admission_01",
                locator=known_fact(locator),
                timing=timing,
                access_posture=access,
                archive_history_posture=archive,
                media_modality_posture=media,
                re_capture_relationship=recapture,
                limitations=limitations,
                warning_notes=[],
                preserved_file_ids=[file_ids["fixture_video_admission.json"]],
            )
        ],
        source_family="tiktok",
        source_surface="tiktok_video_comment_subtitle_admission",
        source_locator=known_fact(locator),
        decision_question="fixture: TikTok single-video admission",
        capture_context="fixture TikTok single-video admission (not a batch packet)",
        actor_audience_context=not_applicable("fixture single-video packet"),
        capture_mode=CaptureModeCategory.AUTOMATED_EXTRACTION,
        operator_category="tiktok_video_admission_cli_operator",
        session_identity=None,
        visible_mode_changes=["tiktok_sci_admission:single_video"],
        source_publication_or_event=timing.source_publication_or_event,
        source_edit_or_version=timing.source_edit_or_version,
        cutoff_posture=timing.cutoff_posture,
        recapture_time=timing.recapture_time,
        access_posture=access,
        archive_history_posture=archive,
        media_modality_posture=media,
        re_capture_relationship=recapture,
        warnings=[],
        limitations=limitations,
        receipt_summary=f"fixture TikTok single-video admission for @{handle}",
        receipt_non_claims=["fixture only"],
    )
    data_root.rebuild_availability()
    return Path(result.output_directory).name


def test_runner_acks_non_batch_tiktok_packet_without_infinite_retry(tmp_path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    _commit_non_batch_tiktok_packet(root)

    class Transport:
        def post_json(self, *args, **kwargs):
            raise AssertionError("no provider call expected for a non-batch TikTok packet")

    transport = Transport()
    first = run_extraction(data_root=root, transport=transport, provider=RawApiProvider.OPENAI_RESPONSES,
                           model="model", api_key="secret")
    assert first == []
    second = run_extraction(data_root=root, transport=transport, provider=RawApiProvider.OPENAI_RESPONSES,
                            model="model", api_key="secret")
    assert second == []


def test_runner_skips_already_written_evidence_after_crash_before_ack(tmp_path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    packet_id = _commit_batch_packet(root, handle="alpha", videos=[_caption_video("v1", "compare affordable alternatives", "alpha")])
    creator = "tiktok:@alpha"

    transcripts, _ = __import__("runners.run_tiktok_product_extract", fromlist=["_transcripts_for_packet"])._transcripts_for_packet(root, packet_id)
    item = AudienceTranscript(creator, transcripts[0])
    rows = [{"creator_id": creator, "video_id": "v1", "audience_layer": "beneficiary_content_fit", "dimension": "value_sought", "label": "comparison-led alternative evaluation", "content_pillar": "comparisons", "vote": 1, "source_pointer": "compare affordable alternatives", "possible_negation_or_irony": False}]
    extraction = parse_response(json.dumps(rows), [item], model="model")[(creator, "v1")]
    assert extraction.evidence and not extraction.rejected
    write_result(data_root=root, item=item, result=extraction, model="model")
    rid = audience_record_id(item, "model")

    # Simulate a crash that landed the evidence record durably, but before the
    # runner reached its final append_ack loop.

    class Transport:
        calls = 0
        def post_json(self, url, headers, body, timeout_seconds):
            self.calls += 1
            return json.dumps({"output_text": "[]"})

    transport = Transport()
    first = run_extraction(data_root=root, transport=transport, provider=RawApiProvider.OPENAI_RESPONSES,
                           model="model", api_key="secret")
    assert transport.calls == 0
    assert [row.get("status") for row in first] == ["skipped_done"]
    second = run_extraction(data_root=root, transport=transport, provider=RawApiProvider.OPENAI_RESPONSES,
                            model="model", api_key="secret")
    assert second == []
    assert transport.calls == 0


def test_runner_rejects_tampered_completed_evidence_before_skip(tmp_path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    packet_id = _commit_batch_packet(
        root,
        handle="alpha",
        videos=[_caption_video("v1", "compare affordable alternatives", "alpha")],
    )
    creator = "tiktok:@alpha"
    transcripts, _ = __import__(
        "runners.run_tiktok_product_extract", fromlist=["_transcripts_for_packet"]
    )._transcripts_for_packet(root, packet_id)
    item = AudienceTranscript(creator, transcripts[0])
    rows = [{
        "creator_id": creator,
        "video_id": "v1",
        "audience_layer": "beneficiary_content_fit",
        "dimension": "value_sought",
        "label": "comparison-led alternative evaluation",
        "content_pillar": "comparisons",
        "vote": 1,
        "source_pointer": "compare affordable alternatives",
        "possible_negation_or_irony": False,
    }]
    extraction = parse_response(json.dumps(rows), [item], model="model")[(creator, "v1")]
    paths = write_result(data_root=root, item=item, result=extraction, model="model")
    record_path = paths[AUDIENCE_EVIDENCE_LANE]
    stored = json.loads(record_path.read_text(encoding="utf-8"))
    stored["content_hash"] = "sha256:" + "0" * 64
    record_path.write_text(json.dumps(stored, sort_keys=True) + "\n", encoding="utf-8")

    class Transport:
        calls = 0

        def post_json(self, *args, **kwargs):
            self.calls += 1
            raise AssertionError("tampered evidence must not reach provider extraction")

    transport = Transport()
    result = run_extraction(
        data_root=root,
        transport=transport,
        provider=RawApiProvider.OPENAI_RESPONSES,
        model="model",
        api_key="secret",
    )

    assert transport.calls == 0
    assert [row["status"] for row in result] == ["discovery_failed"]
    assert "SilverRecordError: Silver content hash mismatch" in result[0]["error"]


def test_runner_isolates_two_creators_and_second_cycle_zero(tmp_path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    p1 = _commit_batch_packet(root, handle="alpha", videos=[_caption_video("v1", "compare affordable alternatives", "alpha")])
    p2 = _commit_batch_packet(root, handle="beta", videos=[_caption_video("v2", "advanced collectors debate", "beta")])

    class Transport:
        calls = 0
        def post_json(self, url, headers, body, timeout_seconds):
            self.calls += 1
            prompt = body["input"]
            rows = []
            if "v1" in prompt:
                rows.append({"creator_id": "tiktok:@alpha", "video_id": "v1", "audience_layer": "beneficiary_content_fit", "dimension": "value_sought", "label": "comparison-led alternative evaluation", "content_pillar": "comparisons", "vote": 1, "source_pointer": "compare affordable alternatives", "possible_negation_or_irony": False})
            if "v2" in prompt:
                rows.append({"creator_id": "tiktok:@beta", "video_id": "v2", "audience_layer": "addressed_audience", "dimension": "assumed_knowledge", "label": "category-fluent collectors", "content_pillar": "collector debate", "vote": 1, "source_pointer": "advanced collectors debate", "possible_negation_or_irony": False})
            return json.dumps({"output_text": json.dumps(rows)})

    transport = Transport()
    first = run_extraction(data_root=root, transport=transport, provider=RawApiProvider.OPENAI_RESPONSES,
                           model="model", api_key="secret", max_input_chars=10000)
    assert transport.calls == 2
    assert sorted(row["status"] for row in first) == ["extracted", "extracted"]
    for packet_id, creator, video in [(p1, "tiktok:@alpha", "v1"), (p2, "tiktok:@beta", "v2")]:
        transcripts, _ = __import__("runners.run_tiktok_product_extract", fromlist=["_transcripts_for_packet"])._transcripts_for_packet(root, packet_id)
        item = AudienceTranscript(creator, transcripts[0])
        rid = audience_record_id(item, "model")
        assert root.is_record_set_complete(subtree="derived", raw_anchor=packet_id, record_id=rid, completion_lane=AUDIENCE_EVIDENCE_SET_LANE)
    assert run_extraction(data_root=root, transport=transport, provider=RawApiProvider.OPENAI_RESPONSES,
                          model="model", api_key="secret") == []
    assert transport.calls == 2
