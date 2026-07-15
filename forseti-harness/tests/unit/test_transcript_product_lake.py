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

from cleaning.raw_model_transport import RawApiProvider
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
    product_mentions_policy_fingerprint,
)
from data_lake.root import DataLakeRoot, DataLakeRootError
from data_lake.silver_lineage import SilverDerivedRef
from runners import run_transcript_product_extract as yt_runner
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

        self.calls = 0
    def post_json(self, url, headers, body, timeout_seconds):  # noqa: ANN001
        self.calls += 1
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


def _source_ref(
    data_root: DataLakeRoot | None = None, *, record_id: str = "asr_fixture.json"
) -> SilverDerivedRef:
    body = b'{"kind":"transcript_fixture"}'
    digest = hashlib.sha256(body).hexdigest()
    if data_root is not None:
        data_root.append_record(
            subtree="derived",
            raw_anchor=_ANCHOR,
            lane="transcript_asr",
            record_id=record_id,
            data=body,
        )
    return SilverDerivedRef(
        raw_anchor=_ANCHOR,
        lane="transcript_asr",
        record_id=record_id,
        sha256=digest,
        hash_basis="derived_record_bytes",
    )


def _transcript(data_root: DataLakeRoot | None = None) -> TranscriptInput:
    lineage = build_transcript_source_lineage(
        namespace="youtube",
        source_surface="youtube_audio",
        video_id="vid12345678",
        derived_ref=_source_ref(data_root),
    )
    return TranscriptInput("vid12345678", _ANCHOR, "asr", _cues(), source_lineage=lineage)


def _stored_mentions(record: dict) -> list[dict]:
    return [row["mention"] for row in record["payload"]["observation"]["rows"]]


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
    transcript = _transcript(data_root)
    paths = extract_products_into_lake(
        data_root=data_root, transcript=transcript, transport=FakeTransport(_anthropic([_item()])),
        provider=_PROVIDER, model="test-model", api_key="k",
    )
    assert PRODUCT_MENTIONS_LANE in paths
    rid = mentions_record_id(transcript, "test-model")
    assert data_root.is_record_set_complete(
        subtree="derived", raw_anchor=_ANCHOR, record_id=rid, completion_lane=PRODUCT_MENTIONS_SET_LANE,
    )
    written = json.loads(paths[PRODUCT_MENTIONS_LANE].read_text(encoding="utf-8"))
    assert written["payload"]["observation"]["row_count"] == 1
    assert _stored_mentions(written)[0]["start_ms"] == 3000  # CE5 timestamp from the cue


def test_operator_result_writer_reuses_silver_lane_shape(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    transcript = _transcript(data_root)
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
    assert rec["provenance"]["extraction_backend"] == "operator_codex_assisted"
    assert rec["provenance"]["extraction_provenance"]["packet_kind"] == "ig_reels_operator_product_extract_v0"
    assert rec["payload"]["observation"]["row_count"] == 1
    assert _stored_mentions(rec)[0]["video_id"] == "vid12345678"


def test_driver_refuses_duplicate_write(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    kw = dict(data_root=data_root, transcript=_transcript(data_root), transport=FakeTransport(_anthropic([_item()])),
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
        data_root=data_root, transcript=_transcript(data_root), transport=FakeTransport(_anthropic(items)),
        provider=_PROVIDER, model="m", api_key="k",
    )
    record = json.loads(paths[PRODUCT_MENTIONS_LANE].read_text(encoding="utf-8"))
    assert record["payload"]["observation"]["row_count"] == 1
    assert record["provenance"]["rejected_count"] == 1
    assert "rejected" not in record  # processing rejects do not blur into Silver facts


# --- runner: ASR path, end-to-end + idempotent --------------------------------


def _commit_asr_transcript(data_root, video_id: str = "vid12345678", posture: str = "transcribed") -> None:
    cues = _cues() if posture == "transcribed" else []
    write_asr_transcript(
        video_id=video_id, audio_bytes=f"fake-audio-{video_id}".encode(), audio_ext="m4a",
        transcribe_fn=lambda _path: (posture, cues, {"tool": "faster-whisper", "model": "test"}),
        data_root=data_root,
    )


def _lake_tree_state(data_root) -> dict[str, str]:
    """Every file under the lake root -> sha256, for byte-unchanged idempotence asserts."""
    return {
        str(p.relative_to(data_root.path)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(data_root.path.rglob("*"))
        if p.is_file()
    }


def test_runner_extracts_asr_transcript_then_skips_on_rerun(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _commit_asr_transcript(data_root)

    transport = FakeTransport(_anthropic([_item()]))
    first = run_extraction(data_root=data_root, transport=transport, provider=_PROVIDER, model="m", api_key="k")
    assert len(first) == 1
    assert first[0]["status"] == "extracted"
    assert first[0]["video_id"] == "vid12345678"

    # the completed packet is acknowledged: the ack record is the durable completion fact.
    acks = list((data_root.path / "acknowledgements").glob(f"**/{PRODUCT_MENTIONS_LANE}/*"))
    assert len(acks) == 1
    ack = json.loads(acks[0].read_text(encoding="utf-8"))
    assert ack["record_kind"] == "acknowledgement"
    assert ack["obligation"]["model"] == "m"
    assert ack["evidence"][0]["kind"] == "record_set_complete"

    # idempotent: a second pass skips the acked packet at the seam WITHOUT loading
    # raw bodies — no per-run status entries, no re-extraction, and the lake tree
    # is byte-unchanged (zero writes, not merely zero failures).
    before = _lake_tree_state(data_root)
    second = run_extraction(data_root=data_root, transport=transport, provider=_PROVIDER, model="m", api_key="k")
    assert second == []
    assert _lake_tree_state(data_root) == before


def test_runner_late_asr_record_resurfaces_acked_packet(tmp_path) -> None:
    # obligation growth: a new transcript_asr record lands AFTER the packet was
    # acknowledged -> the fingerprint changes, the packet is re-picked, the still-done
    # transcript is re-verified (skipped_done), and a SECOND ack records the new inputs.
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _commit_asr_transcript(data_root)
    transport = FakeTransport(_anthropic([_item()]))
    first = run_extraction(data_root=data_root, transport=transport, provider=_PROVIDER, model="m", api_key="k")
    assert first[0]["status"] == "extracted"

    packet_dir = next((data_root.path / "raw").glob("*/*"))
    packet_id = packet_dir.name
    data_root.append_record(
        subtree="derived", raw_anchor=packet_id, lane="transcript_asr",
        record_id="late_asr_record",
        data=json.dumps({"posture": "no_speech", "video_id": "vid99999999"}).encode("utf-8"),
    )

    second = run_extraction(data_root=data_root, transport=transport, provider=_PROVIDER, model="m", api_key="k")
    assert [r["status"] for r in second] == ["skipped_done"]
    acks = list((data_root.path / "acknowledgements").glob(f"**/{PRODUCT_MENTIONS_LANE}/*"))
    assert len(acks) == 2  # append-only completion history

    third = run_extraction(data_root=data_root, transport=transport, provider=_PROVIDER, model="m", api_key="k")
    assert third == []


def test_runner_surfaces_malformed_packet_asr_record_without_ack(tmp_path) -> None:
    # F1 class (YouTube mirror of the IG adjudicated fix): a damaged transcript_asr
    # record must be a LOUD packet discovery failure that blocks the ack and
    # re-surfaces every run — never a silent skip that lets the packet ack as
    # transcript-less over damaged input.
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _commit_asr_transcript(data_root)
    asr_record = next((data_root.path / "derived").glob("**/transcript_asr/*"))
    asr_record.write_text("{not-json\n", encoding="utf-8")

    results = run_extraction(
        data_root=data_root, transport=FakeTransport(_anthropic([_item()])),
        provider=_PROVIDER, model="m", api_key="k",
    )
    assert len(results) == 1
    assert results[0]["status"] == "discovery_failed"
    assert "transcript_asr record" in results[0]["error"]
    assert list((data_root.path / "acknowledgements").glob(f"**/{PRODUCT_MENTIONS_LANE}/*")) == []

    second = run_extraction(
        data_root=data_root, transport=FakeTransport(_anthropic([_item()])),
        provider=_PROVIDER, model="m", api_key="k",
    )
    assert [r["status"] for r in second] == ["discovery_failed"]
    assert list((data_root.path / "acknowledgements").glob(f"**/{PRODUCT_MENTIONS_LANE}/*")) == []


def test_runner_surfaces_unreadable_packet_asr_record_without_ack(tmp_path, monkeypatch) -> None:
    # F1 also covers OSError: the obligation snapshot must stay non-raising by
    # fingerprinting the damage, while the actual transcript scan fails loud.
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _commit_asr_transcript(data_root)
    asr_record = next((data_root.path / "derived").glob("**/transcript_asr/*"))
    packet_id = next((data_root.path / "raw").glob("*/*")).name
    real_read_bytes = Path.read_bytes

    def maybe_raise_unreadable(path: Path) -> bytes:
        if path == asr_record:
            raise OSError("simulated unreadable ASR record")
        return real_read_bytes(path)

    monkeypatch.setattr(Path, "read_bytes", maybe_raise_unreadable)

    obligation = yt_runner._packet_obligation(data_root, packet_id, "m")
    assert obligation["asr_records"] == [[asr_record.name, "unreadable:OSError"]]

    results = run_extraction(
        data_root=data_root, transport=FakeTransport(_anthropic([_item()])),
        provider=_PROVIDER, model="m", api_key="k",
    )
    assert len(results) == 1
    assert results[0]["status"] == "discovery_failed"
    assert "unreadable" in results[0]["error"]
    assert list((data_root.path / "acknowledgements").glob(f"**/{PRODUCT_MENTIONS_LANE}/*")) == []

    second = run_extraction(
        data_root=data_root, transport=FakeTransport(_anthropic([_item()])),
        provider=_PROVIDER, model="m", api_key="k",
    )
    assert [r["status"] for r in second] == ["discovery_failed"]
    assert list((data_root.path / "acknowledgements").glob(f"**/{PRODUCT_MENTIONS_LANE}/*")) == []


def test_rubric_version_reextracts_to_distinct_policy_identity(tmp_path, monkeypatch) -> None:
    # A policy change must not reuse the old completion identity: it re-extracts,
    # writes a distinct record/set marker, and acks the new exact policy.
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _commit_asr_transcript(data_root)
    original_rubric = yt_runner.EXTRACTOR_RUBRIC_VERSION
    transport = FakeTransport(_anthropic([_item()]))

    first = run_extraction(data_root=data_root, transport=transport, provider=_PROVIDER, model="m", api_key="k")
    assert [r["status"] for r in first] == ["extracted"]
    assert run_extraction(data_root=data_root, transport=transport, provider=_PROVIDER, model="m", api_key="k") == []

    monkeypatch.setattr(yt_runner, "EXTRACTOR_RUBRIC_VERSION", "test-rubric-vnext")
    third = run_extraction(data_root=data_root, transport=transport, provider=_PROVIDER, model="m", api_key="k")
    assert [r["status"] for r in third] == ["extracted"]
    acks = [
        json.loads(p.read_text(encoding="utf-8"))
        for p in (data_root.path / "acknowledgements").glob(f"**/{PRODUCT_MENTIONS_LANE}/*")
    ]
    assert len(acks) == 2
    assert {ack["obligation"]["rubric_version"] for ack in acks} == {original_rubric, "test-rubric-vnext"}
    assert transport.calls == 2
    records = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in data_root.lane_dir(
            subtree="derived", raw_anchor=first[0]["anchor"], lane=PRODUCT_MENTIONS_LANE
        ).glob("*.json")
    ]
    assert len(records) == 2
    assert {r["payload"]["observation"]["policy_version"] for r in records} == {original_rubric, "test-rubric-vnext"}


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
    assert record["payload"]["observation"]["row_count"] == 1
    mention = _stored_mentions(record)[0]
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


def test_mentions_record_id_keys_on_content_model_source_and_policy() -> None:
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
    policy_fingerprint = product_mentions_policy_fingerprint("rubric_v0")
    expected_digest = hashlib.sha256(f"{policy_fingerprint}\x00{t1.joined_text}".encode("utf-8")).hexdigest()
    expected_no_key_id = f"mentions_m__{expected_digest[:16]}__p{policy_fingerprint[:12]}.json"
    assert mentions_record_id(t1, "m", policy_fingerprint_sha256=policy_fingerprint) == expected_no_key_id
    assert mentions_record_id(t1, "m") == mentions_record_id(t1, "m")  # stable across calls
    assert mentions_record_id(t1, "m") != mentions_record_id(t2, "m")  # content-keyed
    assert mentions_record_id(t1, "m1") != mentions_record_id(t1, "m2")  # model-keyed (R1 backfill)
    assert mentions_record_id(t3, "m") != mentions_record_id(t4, "m")  # exact source-keyed when present


    assert mentions_record_id(t1, "m", policy_fingerprint_sha256="1" * 64) != mentions_record_id(t1, "m", policy_fingerprint_sha256="2" * 64)
def test_runner_marks_zero_mention_transcript_done(tmp_path) -> None:
    # D5 filler-drop: the model finds no products -> still persisted + marked complete (idempotent).
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _commit_asr_transcript(data_root, "vid12345678")
    empty = FakeTransport(_anthropic([]))
    first = run_extraction(data_root=data_root, transport=empty, provider=_PROVIDER, model="m", api_key="k")
    assert len(first) == 1 and first[0]["status"] == "extracted"
    # completed + acked: the second pass skips at the seam with no status entries.
    second = run_extraction(data_root=data_root, transport=empty, provider=_PROVIDER, model="m", api_key="k")
    assert second == []


def test_runner_reports_partial_needs_cleanup(tmp_path) -> None:
    # crash between the member write and the completion marker: neither the marker
    # nor the packet ack exists (the ack is written only after ALL transcripts
    # complete, so a crash mid-packet leaves the packet unacknowledged and it
    # re-surfaces every run until the operator remediates).
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _commit_asr_transcript(data_root, "vid12345678")
    transport = FakeTransport(_anthropic([_item()]))
    first = run_extraction(data_root=data_root, transport=transport, provider=_PROVIDER, model="m", api_key="k")
    assert first[0]["status"] == "extracted"
    marker = next((data_root.path / "derived").glob(f"**/{PRODUCT_MENTIONS_SET_LANE}/*"))
    marker.unlink()
    ack = next((data_root.path / "acknowledgements").glob(f"**/{PRODUCT_MENTIONS_LANE}/*"))
    ack.unlink()
    second = run_extraction(data_root=data_root, transport=transport, provider=_PROVIDER, model="m", api_key="k")
    assert second[0]["status"] == "partial_needs_cleanup"
    # a partial packet is never acknowledged: it must keep surfacing for cleanup.
    assert list((data_root.path / "acknowledgements").glob(f"**/{PRODUCT_MENTIONS_LANE}/*")) == []


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


def _derived_ref(data_root: DataLakeRoot | None = None) -> SilverDerivedRef:
    return _source_ref(data_root, record_id="asr_test__deadbeefdeadbeef")


def test_driver_persists_silver_lineage_in_place(tmp_path) -> None:
    # AR-01: lineage lands in TOP-LEVEL header-shaped fields, never a nested silver_lineage block.
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    lineage = build_transcript_source_lineage(
        namespace="youtube", source_surface="youtube_audio", video_id="vid12345678",
        derived_ref=_derived_ref(data_root),
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


def test_driver_without_lineage_fails_closed(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    transcript = TranscriptInput("vid12345678", _ANCHOR, "asr", _cues())
    with pytest.raises(ValueError, match="requires exact transcript lineage"):
        extract_products_into_lake(
            data_root=data_root, transcript=transcript, transport=FakeTransport(_anthropic([_item()])),
            provider=_PROVIDER, model="m", api_key="k",
        )


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
