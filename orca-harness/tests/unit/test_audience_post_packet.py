"""Audience-input post-text capture packet (A4): offline tests, no network.

Round-trips a creator post (written caption + bio) through a `for_test` data lake:
build -> SourceCapturePacket -> load_raw_packet -> PostInput, plus the input guards
and the adapter's packet-shape check. Deterministic; no LLM, no transcription.
"""

from __future__ import annotations

import json
from typing import Any

import pytest

from cleaning.audience_post_input import post_input_from_packet
from data_lake.root import DataLakeRoot
from source_capture.audience_post_packet import AudiencePostFetch, write_audience_post_packet

_DQ = "who is this creator's content for?"


def _root(tmp_path) -> DataLakeRoot:
    return DataLakeRoot.for_test(tmp_path / "lake")


def _write(root: DataLakeRoot, **over: Any) -> tuple[int, str]:
    base = dict(
        platform="youtube",
        post_id="vid123",
        creator_handle="jeremyfragrance",
        caption="Best fragrances for every occasion. #fragrance #cologne",
        bio="fragrance reviews + recommendations",
        canonical_url="https://www.youtube.com/watch?v=vid123",
        publish_date_iso="2026-06-01",
        tooling="test",
    )
    base.update(over)
    return write_audience_post_packet(AudiencePostFetch(**base), data_root=root, decision_question=_DQ)


def _load_one(root: DataLakeRoot):
    root.rebuild_availability()
    ids = root.list_available()
    assert len(ids) == 1, ids
    return root.load_raw_packet(ids[0])


def _only_post_input(root: DataLakeRoot, **adapter_kwargs: Any):
    return post_input_from_packet(_load_one(root), **adapter_kwargs)


# --- round trips ----------------------------------------------------------


def test_round_trip_youtube_with_bio(tmp_path) -> None:
    root = _root(tmp_path)
    assert _write(root)[0] == 0
    loaded = _load_one(root)
    # bio present -> no bio-gap limitation recorded in the manifest
    assert "profile bio not captured" not in json.dumps(loaded.manifest)
    pi = post_input_from_packet(loaded)
    assert (pi.creator_id, pi.platform, pi.post_id) == ("jeremyfragrance", "youtube", "vid123")
    assert "Best fragrances" in pi.caption
    assert pi.bio == "fragrance reviews + recommendations"


def test_round_trip_instagram_no_bio(tmp_path) -> None:
    # IG caption-only (bio is the queued capture-add): still a valid packet.
    root = _root(tmp_path)
    code, _ = _write(
        root,
        platform="instagram",
        post_id="DZ5bqNdM2fq",
        caption="SUPERZ Fragrances Budapest. #jeremyfragrance #fragrance #cologne",
        bio=None,
        canonical_url="https://www.instagram.com/p/DZ5bqNdM2fq/",
        publish_date_iso=None,
    )
    assert code == 0
    loaded = _load_one(root)
    # bio absent -> the gap is recorded as a capture-level limitation in the manifest
    assert "profile bio not captured" in json.dumps(loaded.manifest)
    pi = post_input_from_packet(loaded)
    assert pi.platform == "instagram"
    assert pi.bio is None
    assert "SUPERZ" in pi.caption


def test_identity_comes_from_packet(tmp_path) -> None:
    root = _root(tmp_path)
    assert _write(root, creator_handle="realhandle", post_id="v9")[0] == 0
    pi = _only_post_input(root, pillar_label="reviews")
    assert pi.creator_id == "realhandle"
    assert pi.post_id == "v9"
    assert pi.pillar_label == "reviews"


# --- input guards ---------------------------------------------------------


def test_empty_caption_rejected(tmp_path) -> None:
    root = _root(tmp_path)
    code, _ = _write(root, caption="   ")
    assert code == 4
    root.rebuild_availability()
    assert root.list_available() == []  # nothing committed


def test_unsupported_platform_rejected(tmp_path) -> None:
    assert _write(_root(tmp_path), platform="tiktok")[0] == 5


def test_empty_post_id_rejected(tmp_path) -> None:
    assert _write(_root(tmp_path), post_id="  ")[0] == 5


def test_empty_creator_handle_rejected(tmp_path) -> None:
    assert _write(_root(tmp_path), creator_handle="")[0] == 5


# --- adapter fail-closed guards (fake packets) ----------------------------


class _FakePacket:
    """Minimal LoadedRawPacket stand-in: manifest + bodies; file_ids assigned in order."""

    def __init__(self, surface: str, files: list[tuple[str, bytes]]) -> None:
        self.manifest = {
            "source_surface": surface,
            "preserved_files": [
                {"file_id": f"file_{i:02d}", "relative_packet_path": rel}
                for i, (rel, _b) in enumerate(files, start=1)
            ],
        }
        self.bodies = {f"file_{i:02d}": b for i, (_rel, b) in enumerate(files, start=1)}


def _meta(**over: Any) -> bytes:
    base: dict[str, Any] = {"creator_handle": "c", "platform": "youtube", "post_id": "p", "bio": None}
    base.update(over)
    return json.dumps(base).encode("utf-8")


_CAP = ("a.post_caption.txt", b"hello fragrance world")
_META = ("capture_metadata.json", _meta())


def test_adapter_rejects_non_audience_surface() -> None:
    with pytest.raises(ValueError):
        post_input_from_packet(_FakePacket("youtube_captions", [_CAP, _META]))


def test_adapter_rejects_foreign_post_text_surface() -> None:
    # a foreign `<other>_post_text` packet must NOT be adapted (exact-surface gate, not suffix).
    with pytest.raises(ValueError):
        post_input_from_packet(
            _FakePacket("reddit_post_text", [_CAP, ("capture_metadata.json", _meta(platform="reddit"))])
        )


def test_adapter_rejects_platform_surface_mismatch() -> None:
    with pytest.raises(ValueError):
        post_input_from_packet(
            _FakePacket("youtube_post_text", [_CAP, ("capture_metadata.json", _meta(platform="instagram"))])
        )


def test_adapter_rejects_duplicate_caption() -> None:
    with pytest.raises(ValueError):
        post_input_from_packet(
            _FakePacket("youtube_post_text", [_CAP, ("b.post_caption.txt", b"second"), _META])
        )


def test_adapter_rejects_missing_caption() -> None:
    with pytest.raises(ValueError):
        post_input_from_packet(_FakePacket("youtube_post_text", [_META]))


def test_adapter_rejects_non_dict_metadata() -> None:
    with pytest.raises(ValueError):
        post_input_from_packet(_FakePacket("youtube_post_text", [_CAP, ("capture_metadata.json", b"[]")]))


def test_adapter_rejects_non_string_identity() -> None:
    bad = json.dumps({"creator_handle": 123, "platform": "youtube", "post_id": "p"}).encode("utf-8")
    with pytest.raises(ValueError):
        post_input_from_packet(_FakePacket("youtube_post_text", [_CAP, ("capture_metadata.json", bad)]))
