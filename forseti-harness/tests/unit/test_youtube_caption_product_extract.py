"""Offline integration test for the YouTube caption product-extraction runner (Pass-1).

No network, no credentials. Commits a real YouTube caption packet (json3) into a temp lake,
runs the transcript product extractor through a CONTRACT-SENSITIVE fake transport, and asserts
the mention lands in the silver lane with a cue-derived timestamp (CE5) and that the runner is
idempotent (skip-if-done). The contract-sensitive transport proves the runner actually assembled
and SENT the caption cues -- a payload-blind stub could otherwise manufacture a silver row
without the runner ever reading the transcript.
"""
from __future__ import annotations

import json
from typing import Any

from cleaning.raw_model_transport import RawApiProvider
from cleaning.transcript_product_lake import PRODUCT_MENTIONS_LANE
from data_lake.root import DataLakeRoot
from runners.run_transcript_product_extract import run_extraction
from source_capture.transcript.caption_packet import write_caption_packet
from source_capture.transcript.youtube_captions import CaptionFetch

_PROVIDER = RawApiProvider.ANTHROPIC_MESSAGES
_VIDEO_ID = "dQw4w9WgXcQ"
_CUE_PHRASE = "absolute beast in the heat"


def _json3_bytes() -> bytes:
    events = [
        {"tStartMs": 1000, "dDurationMs": 2000, "segs": [{"utf8": "Today I'm testing Dior Sauvage Elixir"}]},
        {"tStartMs": 3000, "dDurationMs": 3000, "segs": [{"utf8": f"and it is an {_CUE_PHRASE}"}]},
    ]
    return (json.dumps({"events": events}, sort_keys=True) + "\n").encode("utf-8")


def _item(**over: Any) -> dict[str, Any]:
    base = dict(
        brand="Dior", line="Sauvage Elixir", concentration="elixir", stance_vote=0.8,
        creator_authored=True, possible_negation_or_irony=False, extractor_confidence=0.9,
        source_pointer=_CUE_PHRASE,
    )
    base.update(over)
    return base


def _anthropic(items: list[dict[str, Any]]) -> str:
    return json.dumps({"content": [{"type": "text", "text": json.dumps(items)}]})


class ContractSensitiveTransport:
    """Proves the runner actually assembled and sent the caption cues -- not a payload-blind
    stub. Asserts the request body carries the cue text before returning the canned mention.
    """

    def __init__(self, canned: str, *, expected_in_body: str) -> None:
        self.canned = canned
        self.expected_in_body = expected_in_body
        self.calls = 0

    def post_json(self, url, headers, body, timeout_seconds):  # noqa: ANN001
        self.calls += 1
        if isinstance(body, bytes):
            body_text = body.decode("utf-8", "replace")
        elif isinstance(body, str):
            body_text = body
        else:
            body_text = json.dumps(body)
        assert self.expected_in_body in body_text, (
            "runner did not send the YouTube caption cues to the transport"
        )
        return self.canned


def _commit_youtube_caption(data_root) -> None:
    cap = CaptionFetch(
        video_id=_VIDEO_ID, found=True, note="ok", lang="en", caption_kind="manual",
        original_language_assumed=False, json3_bytes=_json3_bytes(), flat_text=None,
        cue_count=2, title="Fragrance review", channel_id="UCfixturechan",
        publish_date_iso="2024-08-01", duration_s=120, tooling={"fixture": "youtube_extract"},
    )
    code, _ = write_caption_packet(
        cap,
        data_root=data_root,
        decision_question="What products are mentioned?",
        now_iso="2026-06-16T20:32:17Z",
    )
    assert code == 0


def test_runner_extracts_youtube_caption_then_skips_on_rerun(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _commit_youtube_caption(data_root)

    transport = ContractSensitiveTransport(_anthropic([_item()]), expected_in_body=_CUE_PHRASE)
    first = run_extraction(
        data_root=data_root, transport=transport, provider=_PROVIDER, model="m", api_key="k"
    )
    assert len(first) == 1
    assert first[0]["status"] == "extracted"
    assert first[0]["video_id"] == _VIDEO_ID
    assert transport.calls == 1  # the runner actually called the cue-bearing transport

    assert PRODUCT_MENTIONS_LANE in first[0]["path"]
    written = json.loads((data_root.path / first[0]["path"]).read_text(encoding="utf-8"))
    assert written["payload"]["observation"]["row_count"] == 1
    mention = written["payload"]["observation"]["rows"][0]["mention"]
    assert mention["brand"] == "Dior"
    assert mention["line"] == "Sauvage Elixir"
    assert mention["video_id"] == _VIDEO_ID
    assert mention["start_ms"] == 3000  # CE5: timestamp from the cue containing the source_pointer

    # rerun is a no-op: the acked packet is skipped at the consumption seam without
    # loading raw bodies — no status entries, and the transport is never called again.
    second = run_extraction(
        data_root=data_root, transport=transport, provider=_PROVIDER, model="m", api_key="k"
    )
    assert second == []
    assert transport.calls == 1
