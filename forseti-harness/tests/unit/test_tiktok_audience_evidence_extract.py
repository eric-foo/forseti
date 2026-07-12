from __future__ import annotations
import hashlib, json

from cleaning.audience_extractor import RawApiProvider
from cleaning.tiktok_audience_evidence_extractor import AudienceTranscript, pack_transcripts, parse_response
from cleaning.transcript_product_extractor import TranscriptInput
from cleaning.tiktok_audience_evidence_lake import AUDIENCE_EVIDENCE_SET_LANE, audience_record_id
from data_lake.root import DataLakeRoot
from runners.run_tiktok_audience_evidence_extract import run_extraction
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


def test_packer_can_mix_creators_but_keeps_transcript_units() -> None:
    items = [_transcript("a", "v1", "one"), _transcript("b", "v2", "two")]
    batches = pack_transcripts(items, max_input_chars=1000)
    assert [[item.creator_id for item in batch] for batch in batches] == [["a", "b"]]


def test_parser_partitions_by_creator_and_rejects_demographics() -> None:
    items = [_transcript("a", "v1", "compare affordable alternatives"), _transcript("b", "v2", "advanced collectors debate")]
    rows = [
        {"creator_id": "a", "video_id": "v1", "audience_layer": "beneficiary_content_fit", "dimension": "value_sought", "label": "comparison-led alternative evaluation", "content_pillar": "comparisons", "vote": 1, "source_pointer": "compare affordable alternatives", "possible_negation_or_irony": False},
        {"creator_id": "b", "video_id": "v2", "audience_layer": "addressed_audience", "dimension": "category_relationship", "label": "wealthy men", "content_pillar": "collector debate", "vote": 1, "source_pointer": "advanced collectors debate", "possible_negation_or_irony": False},
    ]
    result = parse_response(json.dumps(rows), items, model="m")
    assert len(result[("a", "v1")].evidence) == 1
    assert result[("b", "v2")].rejected[0]["reason"] == "demographic_inference_forbidden"


def test_runner_batches_two_creators_in_one_call_and_second_cycle_zero(tmp_path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    p1 = _commit_batch_packet(root, handle="alpha", videos=[_caption_video("v1", "compare affordable alternatives", "alpha")])
    p2 = _commit_batch_packet(root, handle="beta", videos=[_caption_video("v2", "advanced collectors debate", "beta")])

    class Transport:
        calls = 0
        def post_json(self, url, headers, body, timeout_seconds):
            self.calls += 1
            prompt = body["input"]
            if "primary_hypothesis" in prompt:
                profiles = []
                if "tiktok:@alpha" in prompt:
                    evidence_id = json.loads(prompt.split("\n\n", 1)[1])["tiktok:@alpha"][0]["evidence_id"]
                    profiles.append({"creator_id": "tiktok:@alpha", "primary_hypothesis": "Comparison-led fragrance shoppers evaluating affordable alternatives.", "knowledge_level": "category-aware", "shopping_stage": "comparison", "product_range": ["affordable alternatives"], "recurring_decision_jobs": ["judge replacement fit"], "engagement_style": "direct comparison", "price_posture": "value-aware", "likely_exclusions": ["non-shoppers"], "evidence_ids": [evidence_id], "counterevidence_ids": [], "support_band": "medium", "actual_audience": "not_estimated"})
                if "tiktok:@beta" in prompt:
                    evidence_id = json.loads(prompt.split("\n\n", 1)[1])["tiktok:@beta"][0]["evidence_id"]
                    profiles.append({"creator_id": "tiktok:@beta", "primary_hypothesis": "Category-fluent collectors who enjoy technical debate.", "knowledge_level": "advanced", "shopping_stage": "category participation", "product_range": ["collector fragrances"], "recurring_decision_jobs": ["debate category choices"], "engagement_style": "collector debate", "price_posture": "unknown", "likely_exclusions": ["complete beginners"], "evidence_ids": [evidence_id], "counterevidence_ids": [], "support_band": "medium", "actual_audience": "not_estimated"})
                return json.dumps({"output_text": json.dumps(profiles)})
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
    assert sorted(row["status"] for row in first) == ["extracted", "extracted", "profile_extracted", "profile_extracted"]
    for packet_id, creator, video in [(p1, "tiktok:@alpha", "v1"), (p2, "tiktok:@beta", "v2")]:
        transcripts, _ = __import__("runners.run_tiktok_product_extract", fromlist=["_transcripts_for_packet"])._transcripts_for_packet(root, packet_id)
        item = AudienceTranscript(creator, transcripts[0])
        rid = audience_record_id(item, "model")
        assert root.is_record_set_complete(subtree="derived", raw_anchor=packet_id, record_id=rid, completion_lane=AUDIENCE_EVIDENCE_SET_LANE)
    assert run_extraction(data_root=root, transport=transport, provider=RawApiProvider.OPENAI_RESPONSES,
                          model="model", api_key="secret") == []
    assert transport.calls == 2
