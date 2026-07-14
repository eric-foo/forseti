"""Offline tests for operator-assisted IG Reels product extraction."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from cleaning.transcript_product_lake import PRODUCT_MENTIONS_SET_LANE
from data_lake.root import DataLakeRoot
from runners import run_ig_reels_operator_product_extract as operator_runner
from runners.run_ig_reels_operator_product_extract import (
    OPERATOR_BACKEND,
    build_operator_packet,
    export_operator_packet,
    import_operator_response,
)
from runners.run_ig_reels_product_extract import discover_transcript_candidates
from source_capture.transcript.ig_reels_audio_packet import write_ig_reels_asr_transcript

_SHORTCODE = "DZ69knlsDb1"


def _cues() -> list[dict[str, Any]]:
    return [
        {"start_ms": 1000, "end_ms": 3000, "text": "Today I'm testing Dior Sauvage Elixir"},
        {"start_ms": 3000, "end_ms": 6000, "text": "and it is an absolute beast in the heat"},
    ]


def _item(**over: Any) -> dict[str, Any]:
    base = dict(
        brand="Dior",
        line="Sauvage Elixir",
        concentration="elixir",
        stance_vote=0.8,
        creator_authored=True,
        possible_negation_or_irony=False,
        extractor_confidence=0.9,
        source_pointer="absolute beast in the heat",
    )
    base.update(over)
    return base


def _commit_ig_audio_transcript(data_root: DataLakeRoot) -> tuple[str, str]:
    code, message = write_ig_reels_asr_transcript(
        shortcode=_SHORTCODE,
        audio_bytes=b"operator-product-fixture",
        audio_ext="m4a",
        transcribe_fn=lambda _path: (
            "transcribed",
            _cues(),
            {"tool": "faster-whisper", "model": "test"},
        ),
        data_root=data_root,
    )
    assert code == 0
    record_path = Path(message.split(" ")[0])
    return record_path.parts[-3], record_path.name


def test_operator_packet_export_and_import_writes_product_mentions(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    packet_id, asr_record_id = _commit_ig_audio_transcript(data_root)
    source_key = f"{packet_id}:asr:{asr_record_id}"
    packet_path = tmp_path / "operator_packet.json"

    exported = export_operator_packet(
        data_root=data_root,
        transcript_source_key=source_key,
        output_path=packet_path,
    )

    assert exported["status"] == "operator_packet_exported"
    assert exported["transcript_source_key"] == source_key
    assert packet_path.is_file()
    packet = json.loads(packet_path.read_text(encoding="utf-8"))
    assert packet["transcript_identity"]["source_route"] == "standalone_audio_packet"
    assert "Return ONLY the JSON array" in packet["prompt"]

    imported = import_operator_response(
        data_root=data_root,
        packet=packet,
        response_text=json.dumps([_item()]),
    )

    assert imported["status"] == "extracted"
    assert imported["mention_count"] == 1
    record = json.loads(Path(imported["path"]).read_text(encoding="utf-8"))
    assert record["provenance"]["extraction_backend"] == OPERATOR_BACKEND
    assert record["provenance"]["extraction_provenance"]["operator_medium"] == "codex_subscription_or_manual_json"
    assert record["provenance"]["transcript_source_key"] == source_key
    assert record["provenance"]["source_route"] == "standalone_audio_packet"
    assert record["derived_refs"][0]["lane"] == "transcript_asr"
    assert record["derived_refs"][0]["record_set_completion_lane"] is None

    second = import_operator_response(
        data_root=data_root,
        packet=packet,
        response_text=json.dumps([_item()]),
    )
    assert second["status"] == "skipped_done"


def test_operator_import_rejects_stale_packet_digest(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    packet_id, asr_record_id = _commit_ig_audio_transcript(data_root)
    source_key = f"{packet_id}:asr:{asr_record_id}"
    exported = export_operator_packet(data_root=data_root, transcript_source_key=source_key)
    packet = exported["packet"]
    packet["transcript_content_sha256"] = "0" * 64

    with pytest.raises(ValueError, match="no longer matches"):
        import_operator_response(
            data_root=data_root,
            packet=packet,
            response_text=json.dumps([_item()]),
        )


def test_build_operator_packet_carries_full_cues_without_writing(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    packet_id, asr_record_id = _commit_ig_audio_transcript(data_root)
    source_key = f"{packet_id}:asr:{asr_record_id}"
    exported = export_operator_packet(data_root=data_root, transcript_source_key=source_key)
    packet = exported["packet"]

    assert packet == build_operator_packet(
        transcript=next(
            transcript
            for transcript, failure in discover_transcript_candidates(data_root)
            if failure is None and transcript is not None and transcript.transcript_source_key == source_key
        )
    )
    assert packet["transcript"]["cue_count"] == 2
    assert packet["transcript"]["cues"][1]["text"] == "and it is an absolute beast in the heat"


def test_operator_cli_returns_nonzero_for_partial_cleanup(tmp_path, monkeypatch, capsys) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    packet_id, asr_record_id = _commit_ig_audio_transcript(data_root)
    source_key = f"{packet_id}:asr:{asr_record_id}"
    packet = export_operator_packet(data_root=data_root, transcript_source_key=source_key)["packet"]
    imported = import_operator_response(
        data_root=data_root,
        packet=packet,
        response_text=json.dumps([_item()]),
    )
    assert imported["status"] == "extracted"
    marker = next((data_root.path / "derived").glob(f"**/{PRODUCT_MENTIONS_SET_LANE}/*"))
    marker.unlink()

    packet_path = tmp_path / "operator_packet.json"
    response_path = tmp_path / "operator_response.json"
    packet_path.write_text(json.dumps(packet), encoding="utf-8")
    response_path.write_text(json.dumps([_item()]), encoding="utf-8")

    def fake_resolve(cls, *, explicit=None, **_kwargs):  # noqa: ANN001
        assert explicit is None
        return data_root

    monkeypatch.setattr(DataLakeRoot, "resolve", classmethod(fake_resolve))
    assert operator_runner.main(["import", "--packet", str(packet_path), "--response", str(response_path)]) == 4
    captured = capsys.readouterr()
    assert '"status": "partial_needs_cleanup"' in captured.out
