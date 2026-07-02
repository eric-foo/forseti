"""Driver + daemon-ready runner: offline integration tests over a `for_test` data lake.

No network, no credentials. Commits real caption / ASR transcripts into a temp lake, runs the
extractor through a fake transport, and asserts mentions land in the silver lane, that the
runner is idempotent (skip-if-done), and that the json3->cues parser preserves timing.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import pytest

from cleaning.audience_extractor import RawApiProvider
from cleaning.transcript_product_extractor import TranscriptInput, parse_mentions
from cleaning.transcript_product_lake import (
    PRODUCT_MENTIONS_LANE,
    PRODUCT_MENTIONS_SET_LANE,
    build_transcript_source_lineage,
    cues_from_asr_record,
    cues_from_json3,
    extract_products_into_lake,
    mentions_record_id,
    write_product_mentions_result_into_lake,
)
from data_lake.root import DataLakeRoot, DataLakeRootError
from data_lake.silver_lineage import SilverDerivedRef
from runners.run_transcript_product_extract import run_extraction
from source_capture.transcript.asr_packet import write_asr_transcript
from source_capture.transcript.youtube_captions import CaptionFetch
from source_capture.transcript.caption_packet import write_caption_packet

_ANCHOR = "ANCHORTEST0123456789ABCDEF"
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
    """Raises on the first call, returns valid JSON after — to exercise per-item isolation."""

    def __init__(self, valid: str) -> None:
        self.valid = valid
        self.calls = 0

    def post_json(self, url, headers, body, timeout_seconds):  # noqa: ANN001
        self.calls += 1
        if self.calls == 1:
            raise RuntimeError("simulated provider error")
        return self.valid


def _caption_fetch() -> CaptionFetch:
    json3 = json.dumps(
        {
            "events": [
                {"tStartMs": 1000, "dDurationMs": 2000, "segs": [{"utf8": "Today I'm testing Dior Sauvage Elixir"}]},
                {"tStartMs": 3000, "dDurationMs": 3000, "segs": [{"utf8": "and it is an absolute beast in the heat"}]},
            ]
        }
    ).encode("utf-8")
    return CaptionFetch(
        video_id="vid12345678", found=True, note="ok", lang="en", caption_kind="auto",
        json3_bytes=json3, flat_text="x", cue_count=2, title="T", channel_id="UC",
        publish_date_iso="2026-06-20", duration_s=42,
        tooling={"tool": "yt-dlp", "tool_version": "x", "client": "yt-dlp-default"},
    )


def _transcript() -> TranscriptInput:
    return TranscriptInput("vid12345678", _ANCHOR, "asr", _cues())


# --- json3 -> cues (timing preserved) ----------------------------------------


def test_cues_from_json3_preserves_timing_and_dedups() -> None:
    raw = json.dumps(
        {
            "events": [
                {"tStartMs": 1000, "dDurationMs": 2000, "segs": [{"utf8": "hello world"}]},
                {"tStartMs": 1000, "dDurationMs": 2000, "segs": [{"utf8": "hello world"}]},  # rolling dup
                {"tStartMs": 3000, "dDurationMs": 1500, "segs": [{"utf8": "second line"}]},
                {"segs": []},  # empty -> skipped
            ]
        }
    ).encode("utf-8")
    cues = cues_from_json3(raw)
    assert cues == [
        {"start_ms": 1000, "end_ms": 3000, "text": "hello world"},
        {"start_ms": 3000, "end_ms": 4500, "text": "second line"},
    ]


def test_cues_from_json3_clamps_negative_duration() -> None:
    raw = json.dumps(
        {"events": [{"tStartMs": 5000, "dDurationMs": -3000, "segs": [{"utf8": "a product line"}]}]}
    ).encode("utf-8")
    # end_ms must not fall below start_ms (else ProductMention would reject a valid mention).
    assert cues_from_json3(raw) == [{"start_ms": 5000, "end_ms": 5000, "text": "a product line"}]


def test_cues_from_json3_handles_missing_and_nonnumeric_timing() -> None:
    raw = json.dumps(
        {
            "events": [
                {"segs": [{"utf8": "no timing fields"}]},
                {"tStartMs": "bad", "dDurationMs": "bad", "segs": [{"utf8": "nonnumeric timing"}]},
            ]
        }
    ).encode("utf-8")
    assert cues_from_json3(raw) == [
        {"start_ms": 0, "end_ms": 0, "text": "no timing fields"},
        {"start_ms": 0, "end_ms": 0, "text": "nonnumeric timing"},
    ]


def test_cues_from_json3_handles_nonfinite_timing() -> None:
    # json.loads accepts bare NaN/Infinity (they ARE floats); the parser must finite-guard, not crash.
    raw = json.dumps(
        {
            "events": [
                {"tStartMs": float("nan"), "dDurationMs": 1000, "segs": [{"utf8": "nan start"}]},
                {"tStartMs": 2000, "dDurationMs": float("inf"), "segs": [{"utf8": "inf dur"}]},
            ]
        }
    ).encode("utf-8")
    assert cues_from_json3(raw) == [
        {"start_ms": 0, "end_ms": 1000, "text": "nan start"},
        {"start_ms": 2000, "end_ms": 2000, "text": "inf dur"},
    ]


def test_mentions_record_id_bounded_for_long_model_name() -> None:
    rid = mentions_record_id(_transcript(), "x" * 300)
    assert len(rid) <= 128  # stays within the lake's 128-char _SAFE_SEGMENT limit


# --- driver: persists to the silver lane + write-once -------------------------


def test_driver_persists_to_silver_lane(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    paths = extract_products_into_lake(
        data_root=data_root, transcript=_transcript(), transport=FakeTransport(_anthropic([_item()])),
        provider=_PROVIDER, model="test-model", api_key="k",
    )
    assert PRODUCT_MENTIONS_LANE in paths
    rid = mentions_record_id(_transcript(), "test-model")
    assert data_root.is_record_set_complete(
        subtree="derived", raw_anchor=_ANCHOR, record_id=rid, completion_lane=PRODUCT_MENTIONS_SET_LANE,
    )
    written = json.loads(paths[PRODUCT_MENTIONS_LANE].read_text(encoding="utf-8"))
    assert written["mention_count"] == 1
    assert written["mentions"][0]["start_ms"] == 3000  # CE5 timestamp from the cue


def test_operator_result_writer_reuses_silver_lane_shape(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    transcript = _transcript()
    parsed = parse_mentions(json.dumps([_item()]), transcript, model="operator")

    paths = write_product_mentions_result_into_lake(
        data_root=data_root,
        transcript=transcript,
        result=parsed,
        model="operator",
        extraction_backend="operator_codex_assisted",
        extraction_provenance={"packet_kind": "ig_reels_operator_product_extract_v0"},
    )

    rec = json.loads(paths[PRODUCT_MENTIONS_LANE].read_text(encoding="utf-8"))
    assert rec["extraction_backend"] == "operator_codex_assisted"
    assert rec["extraction_provenance"]["packet_kind"] == "ig_reels_operator_product_extract_v0"
    assert rec["mention_count"] == 1
    assert rec["mentions"][0]["video_id"] == "vid12345678"


def test_driver_refuses_duplicate_write(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    kw = dict(data_root=data_root, transcript=_transcript(), transport=FakeTransport(_anthropic([_item()])),
              provider=_PROVIDER, model="test-model", api_key="k")
    paths = extract_products_into_lake(**kw)
    before = paths[PRODUCT_MENTIONS_LANE].read_text(encoding="utf-8")
    with pytest.raises(DataLakeRootError):  # write-once: refuses an existing set
        extract_products_into_lake(**kw)
    assert paths[PRODUCT_MENTIONS_LANE].read_text(encoding="utf-8") == before  # first record intact


def test_driver_persists_rejected_count(tmp_path) -> None:
    # CE8 audit trail must reach disk: one valid + one rejectable (bad enum) item.
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    items = [_item(), _item(concentration="spray")]
    paths = extract_products_into_lake(
        data_root=data_root, transcript=_transcript(), transport=FakeTransport(_anthropic(items)),
        provider=_PROVIDER, model="m", api_key="k",
    )
    record = json.loads(paths[PRODUCT_MENTIONS_LANE].read_text(encoding="utf-8"))
    assert record["mention_count"] == 1
    assert record["rejected_count"] == 1
    assert record["rejected"][0]["index"] == "1"


# --- runner: ASR path, end-to-end + idempotent --------------------------------


def _commit_asr_transcript(data_root, video_id: str = "vid12345678", posture: str = "transcribed") -> None:
    cues = _cues() if posture == "transcribed" else []
    write_asr_transcript(
        video_id=video_id, audio_bytes=f"fake-audio-{video_id}".encode(), audio_ext="m4a",
        transcribe_fn=lambda _path: (posture, cues, {"tool": "faster-whisper", "model": "test"}),
        data_root=data_root,
    )


def test_runner_extracts_asr_transcript_then_skips_on_rerun(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _commit_asr_transcript(data_root)

    transport = FakeTransport(_anthropic([_item()]))
    first = run_extraction(data_root=data_root, transport=transport, provider=_PROVIDER, model="m", api_key="k")
    assert len(first) == 1
    assert first[0]["status"] == "extracted"
    assert first[0]["video_id"] == "vid12345678"

    # idempotent: a second pass finds the completed set and skips (does not re-extract).
    second = run_extraction(data_root=data_root, transport=transport, provider=_PROVIDER, model="m", api_key="k")
    assert len(second) == 1
    assert second[0]["status"] == "skipped_done"


# --- runner: caption path, end-to-end -----------------------------------------


def test_runner_extracts_caption_transcript(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    json3 = json.dumps(
        {
            "events": [
                {"tStartMs": 1000, "dDurationMs": 2000, "segs": [{"utf8": "Today I'm testing Dior Sauvage Elixir"}]},
                {"tStartMs": 3000, "dDurationMs": 3000, "segs": [{"utf8": "and it is an absolute beast in the heat"}]},
            ]
        }
    ).encode("utf-8")
    cap = CaptionFetch(
        video_id="vid12345678", found=True, note="ok", lang="en", caption_kind="auto",
        json3_bytes=json3, flat_text="x", cue_count=2, title="T", channel_id="UC",
        publish_date_iso="2026-06-20", duration_s=42,
        tooling={"tool": "yt-dlp", "tool_version": "x", "client": "yt-dlp-default"},
    )
    write_caption_packet(cap, data_root=data_root, decision_question="Q")

    results = run_extraction(
        data_root=data_root, transport=FakeTransport(_anthropic([_item()])),
        provider=_PROVIDER, model="m", api_key="k",
    )
    assert len(results) == 1
    assert results[0]["status"] == "extracted"

    record_path = next((data_root.path / "derived").glob(f"**/{PRODUCT_MENTIONS_LANE}/*"))
    record = json.loads(record_path.read_text(encoding="utf-8"))
    assert record["mention_count"] == 1
    mention = record["mentions"][0]
    assert mention["video_id"] == "vid12345678"
    assert mention["transcript_source"] == "caption"
    assert mention["source_pointer"] == "absolute beast in the heat"
    assert mention["start_ms"] == 3000
    assert mention["end_ms"] == 6000


def test_runner_empty_lake_yields_no_results(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    results = run_extraction(
        data_root=data_root, transport=FakeTransport(_anthropic([_item()])),
        provider=_PROVIDER, model="m", api_key="k",
    )
    assert results == []


def test_runner_skips_non_transcribed_asr(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _commit_asr_transcript(data_root, "vid12345678", posture="no_speech")
    results = run_extraction(
        data_root=data_root, transport=FakeTransport(_anthropic([_item()])),
        provider=_PROVIDER, model="m", api_key="k",
    )
    assert results == []


def test_cues_from_asr_record_guards_non_list() -> None:
    assert cues_from_asr_record({"cues": "not-a-list"}) == []
    assert cues_from_asr_record({}) == []
    good = [{"start_ms": 0, "end_ms": 1, "text": "x"}]
    assert cues_from_asr_record({"cues": good}) == good


def test_mentions_record_id_keys_on_content_model_and_optional_source_key() -> None:
    t1 = _transcript()
    t2 = TranscriptInput("vid12345678", _ANCHOR, "asr", [{"start_ms": 0, "end_ms": 1, "text": "totally other words"}])
    t3 = TranscriptInput(
        "vid12345678",
        _ANCHOR,
        "asr",
        _cues(),
        transcript_source_key="vid12345678:asr:deepcap-a",
    )
    t4 = TranscriptInput(
        "vid12345678",
        _ANCHOR,
        "asr",
        _cues(),
        transcript_source_key="vid12345678:asr:deepcap-b",
    )
    expected_no_key_id = f"mentions_m__{hashlib.sha256(t1.joined_text.encode('utf-8')).hexdigest()[:16]}.json"
    assert mentions_record_id(t1, "m") == expected_no_key_id  # no-key legacy formula
    assert mentions_record_id(t1, "m") == mentions_record_id(t1, "m")  # stable across calls
    assert mentions_record_id(t1, "m") != mentions_record_id(t2, "m")  # content-keyed
    assert mentions_record_id(t1, "m1") != mentions_record_id(t1, "m2")  # model-keyed (R1 backfill)
    assert mentions_record_id(t3, "m") != mentions_record_id(t4, "m")  # exact source-keyed when present


def test_runner_marks_zero_mention_transcript_done(tmp_path) -> None:
    # D5 filler-drop: the model finds no products -> still persisted + marked complete (idempotent).
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _commit_asr_transcript(data_root, "vid12345678")
    empty = FakeTransport(_anthropic([]))
    first = run_extraction(data_root=data_root, transport=empty, provider=_PROVIDER, model="m", api_key="k")
    assert len(first) == 1 and first[0]["status"] == "extracted"
    second = run_extraction(data_root=data_root, transport=empty, provider=_PROVIDER, model="m", api_key="k")
    assert second[0]["status"] == "skipped_done"


def test_runner_reports_partial_needs_cleanup(tmp_path) -> None:
    # crash between the member write and the completion marker: delete the marker, then re-run.
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _commit_asr_transcript(data_root, "vid12345678")
    transport = FakeTransport(_anthropic([_item()]))
    first = run_extraction(data_root=data_root, transport=transport, provider=_PROVIDER, model="m", api_key="k")
    assert first[0]["status"] == "extracted"
    marker = next((data_root.path / "derived").glob(f"**/{PRODUCT_MENTIONS_SET_LANE}/*"))
    marker.unlink()
    second = run_extraction(data_root=data_root, transport=transport, provider=_PROVIDER, model="m", api_key="k")
    assert second[0]["status"] == "partial_needs_cleanup"


# --- daemon-readiness: failure isolation at both grains (review major) --------


def test_runner_isolates_per_item_extraction_failure(tmp_path) -> None:
    # two transcripts; the transport raises on the first -> that one 'failed', the batch continues.
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _commit_asr_transcript(data_root, "vid12345678")
    _commit_asr_transcript(data_root, "vid87654321")
    transport = RaiseThenValidTransport(_anthropic([_item()]))
    results = run_extraction(data_root=data_root, transport=transport, provider=_PROVIDER, model="m", api_key="k")
    assert sorted(r["status"] for r in results) == ["extracted", "failed"]


def test_runner_isolates_corrupt_packet_discovery(tmp_path) -> None:
    # a corrupt packet must not abort the batch: it -> discovery_failed, the good one still extracts.
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _commit_asr_transcript(data_root, "vid12345678")
    write_caption_packet(_caption_fetch(), data_root=data_root, decision_question="Q")
    json3_file = next((data_root.path / "raw").glob("**/*.json3"))
    json3_file.write_bytes(b'{"events": "tampered"}')  # breaks the fail-closed sha/size check
    results = run_extraction(
        data_root=data_root, transport=FakeTransport(_anthropic([_item()])),
        provider=_PROVIDER, model="m", api_key="k",
    )
    statuses = {r["status"] for r in results}
    assert "extracted" in statuses
    assert "discovery_failed" in statuses


# --- silver lineage adoption: exact consumed-source reference -----------------


def _derived_ref() -> SilverDerivedRef:
    return SilverDerivedRef(
        raw_anchor=_ANCHOR, lane="transcript_asr", record_id="asr_test__deadbeefdeadbeef",
        sha256="b" * 64, hash_basis="derived_record_bytes",
    )


def test_driver_persists_silver_lineage_in_place(tmp_path) -> None:
    # AR-01: lineage lands in TOP-LEVEL header-shaped fields, never a nested silver_lineage block.
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    lineage = build_transcript_source_lineage(
        namespace="youtube", source_surface="youtube_audio", video_id="vid12345678",
        derived_ref=_derived_ref(),
    )
    transcript = TranscriptInput("vid12345678", _ANCHOR, "asr", _cues(), source_lineage=lineage)
    paths = extract_products_into_lake(
        data_root=data_root, transcript=transcript, transport=FakeTransport(_anthropic([_item()])),
        provider=_PROVIDER, model="m", api_key="k",
    )
    rec = json.loads(paths[PRODUCT_MENTIONS_LANE].read_text(encoding="utf-8"))
    assert "silver_lineage" not in rec
    assert rec["lineage_schema_version"] == "silver_lineage_v0"
    assert rec["derived_refs"][0]["lane"] == "transcript_asr"
    assert rec["derived_refs"][0]["record_id"] == "asr_test__deadbeefdeadbeef"
    assert rec["raw_refs"] == []
    assert rec["source_object"]["kind"] == "transcript"


def test_driver_without_lineage_omits_lineage_fields(tmp_path) -> None:
    # Additive: a producer that has not adopted lineage (e.g. the IG runner, Patch 3) still
    # writes, and the record simply carries no lineage fields -- no fake/empty lineage.
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    paths = extract_products_into_lake(
        data_root=data_root, transcript=_transcript(), transport=FakeTransport(_anthropic([_item()])),
        provider=_PROVIDER, model="m", api_key="k",
    )
    rec = json.loads(paths[PRODUCT_MENTIONS_LANE].read_text(encoding="utf-8"))
    for key in ("derived_refs", "raw_refs", "lineage_schema_version", "source_object"):
        assert key not in rec


def test_runner_asr_record_references_exact_transcript(tmp_path) -> None:
    # End-to-end: the product-mention record references the EXACT transcript_asr record consumed.
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _commit_asr_transcript(data_root)
    results = run_extraction(
        data_root=data_root, transport=FakeTransport(_anthropic([_item()])),
        provider=_PROVIDER, model="m", api_key="k",
    )
    assert results[0]["status"] == "extracted"
    record_path = next((data_root.path / "derived").glob(f"**/{PRODUCT_MENTIONS_LANE}/*"))
    ref = json.loads(record_path.read_text(encoding="utf-8"))["derived_refs"][0]
    assert ref["ref_type"] == "derived_record" and ref["lane"] == "transcript_asr"
    target = data_root.record_path(
        subtree="derived", raw_anchor=ref["raw_anchor"], lane=ref["lane"], record_id=ref["record_id"]
    )
    assert target.is_file()  # the ref resolves to a real committed record...
    assert ref["sha256"] == hashlib.sha256(target.read_bytes()).hexdigest()  # ...and is verifiable


def test_runner_caption_record_references_raw_json3(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    write_caption_packet(_caption_fetch(), data_root=data_root, decision_question="Q")
    results = run_extraction(
        data_root=data_root, transport=FakeTransport(_anthropic([_item()])),
        provider=_PROVIDER, model="m", api_key="k",
    )
    assert results[0]["status"] == "extracted"
    record_path = next((data_root.path / "derived").glob(f"**/{PRODUCT_MENTIONS_LANE}/*"))
    rec = json.loads(record_path.read_text(encoding="utf-8"))
    ref = rec["raw_refs"][0]
    assert ref["ref_type"] == "raw_packet" and ref["hash_basis"] == "raw_stored_bytes"
    assert ref["file_id"] and len(ref["sha256"]) == 64
    assert rec["derived_refs"] == []
