from __future__ import annotations

import json
from collections.abc import Callable

import pytest

from evidence_binding.instagram_audience_triangulation import (
    build_instagram_creator_audience_evidence_bundle,
)
from judgment.creator_audience import (
    METHOD_DECK_RELATIVE_PATH,
    build_capability_manifest,
    build_compact_judgment_view,
    build_creator_audience_prompt,
    load_method_deck,
)
from packing import (
    COLUMNAR_PACKING_VERSION,
    ColumnarPackingError,
    pack_creator_audience_view,
    unpack_creator_audience_view,
)


def _compact_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def _tiktok_bundle() -> dict:
    _, method_hash = load_method_deck()
    return {
        "schema_version": "creator_audience_evidence_bundle_v0",
        "creator_id": "tiktok:@alpha",
        "profile_subject_kind": "platform_account",
        "profile_subject_id": "platform_account:tiktok:alpha",
        "platform_scope": "tiktok",
        "raw_anchor": "01PACKINGV0TEST",
        "question": "Who should hire this creator and why?",
        "evidence_cutoff": "2026-07-16T00:00:00Z",
        "method_deck_path": METHOD_DECK_RELATIVE_PATH,
        "method_deck_sha256": method_hash,
        "capture_scope": {"selected_video_ids": ["v1", "v2"]},
        "transcript_evidence": [
            {
                "evidence_id": "content-1",
                "video_id": "v1",
                "text": "I compare the product side by side.",
                "start_ms": 0,
                "end_ms": 1200,
                "source_pointer": "/private/audit/path/1",
            },
            {
                "evidence_id": "content-2",
                "video_id": "v2",
                "text": "  I compare the product SIDE by side. ",
                "start_ms": 200,
                "end_ms": 1400,
                "source_pointer": "/private/audit/path/2",
            },
            {
                "evidence_id": "content-3",
                "video_id": "v2",
                "text": "The finish lasts through a full day.",
                "start_ms": 3000,
                "end_ms": 4100,
                "source_pointer": "/private/audit/path/3",
            },
        ],
        "comment_evidence": [
            {
                "evidence_id": "comment-1",
                "video_id": "v1",
                "comment_id": "c1",
                "text": "Please compare the next release too.",
                "comment_likes": 25,
                "comment_like_rank_within_captured": 1,
                "temporal_alignment": "same_capture_observation",
                "comment_attention_record_id": "attention-1",
                "source_pointer": "/private/audit/path/4",
            },
            {
                "evidence_id": "comment-2",
                "video_id": "v2",
                "comment_id": "c2",
                "text": "This made the trade-off easy to understand.",
                "comment_likes": 10,
                "comment_like_rank_within_captured": 2,
                "temporal_alignment": "same_capture_observation",
                "comment_attention_record_id": "attention-2",
                "source_pointer": "/private/audit/path/5",
            },
            {
                "evidence_id": "comment-3",
                "video_id": "v2",
                "comment_id": "c3",
                "text": "please   compare the next release TOO.",
                "comment_likes": 5,
                "comment_like_rank_within_captured": 3,
                "temporal_alignment": "same_capture_observation",
                "comment_attention_record_id": "attention-3",
                "source_pointer": "/private/audit/path/6",
            },
        ],
        "bundle_id": "bundle-packing-v0",
        "bundle_hash": "sha256:" + "b" * 64,
    }


def _scaled_tiktok_bundle() -> dict:
    # The multi-row regime the packer targets: several rows per table. At the
    # tiny one-row-per-table scale of _tiktok_bundle, the declared-columns
    # header plus envelope overhead outweighs the per-row key savings and the
    # packed form is larger; the size measurement belongs to this fixture.
    bundle = _tiktok_bundle()
    for index in range(4, 10):
        bundle["transcript_evidence"].append(
            {
                "evidence_id": f"content-{index}",
                "video_id": f"v{index}",
                "text": f"Segment {index} walks through application step {index}.",
                "start_ms": index * 1000,
                "end_ms": index * 1000 + 900,
                "source_pointer": f"/private/audit/path/t{index}",
            }
        )
        bundle["comment_evidence"].append(
            {
                "evidence_id": f"comment-{index}",
                "video_id": f"v{index}",
                "comment_id": f"c{index}",
                "text": f"Question {index} about shade matching.",
                "comment_likes": index,
                "comment_like_rank_within_captured": index,
                "temporal_alignment": "same_capture_observation",
                "comment_attention_record_id": f"attention-{index}",
                "source_pointer": f"/private/audit/path/c{index}",
            }
        )
    bundle["capture_scope"] = {
        "selected_video_ids": [f"v{index}" for index in range(1, 10)]
    }
    return bundle


def _instagram_bundle() -> dict:
    _, method_hash = load_method_deck()
    comments = [
        {
            "record_id": "comments-r1",
            "reel_shortcode": "R1",
            "comments": [
                {
                    "comment_id": "c1",
                    "text": "Compare this with the original.",
                    "like_count": 7,
                },
                {
                    "comment_id": "c2",
                    "text": "The routine is easy to follow.",
                    "like_count": 4,
                },
            ],
        },
        {
            "record_id": "comments-r2",
            "reel_shortcode": "R2",
            "comments": [
                {
                    "comment_id": "c3",
                    "text": "compare THIS with the original.",
                    "like_count": 2,
                },
                {
                    "comment_id": "c4",
                    "text": "the ROUTINE is easy to follow.",
                    "like_count": 1,
                },
            ],
        },
        {
            "record_id": "comments-r3",
            "reel_shortcode": "R3",
            "comments": [
                {
                    "comment_id": "c5",
                    "text": "I understand the difference now.",
                    "like_count": 3,
                }
            ],
        },
    ]
    transcripts = [
        {
            "record_id": "transcript-r1",
            "reel_shortcode": "R1",
            "cues": [{"start_ms": 0, "end_ms": 900, "text": "First comparison"}],
        },
        {
            "record_id": "transcript-r2",
            "reel_shortcode": "R2",
            "cues": [{"start_ms": 0, "end_ms": 900, "text": "Second comparison"}],
        },
        {
            "record_id": "transcript-r3",
            "reel_shortcode": "R3",
            "cues": [{"start_ms": 0, "end_ms": 900, "text": "Third comparison"}],
        },
    ]
    return build_instagram_creator_audience_evidence_bundle(
        creator_id="@alpha",
        profile_subject_id="platform_account:instagram:alpha",
        primary_raw_anchor="01INSTAGRAMPACKING",
        comment_records=comments,
        transcript_records=transcripts,
        question="Who should hire Alpha?",
        evidence_cutoff="2026-07-16T00:00:00Z",
        method_deck_path=METHOD_DECK_RELATIVE_PATH,
        method_deck_sha256=method_hash,
    )


@pytest.mark.parametrize(
    "bundle_builder",
    [_tiktok_bundle, _scaled_tiktok_bundle, _instagram_bundle],
    ids=["tiktok", "tiktok_scaled", "instagram"],
)
def test_pack_unpack_rehydrates_deep_equal(
    bundle_builder: Callable[[], dict],
) -> None:
    view = build_compact_judgment_view(bundle_builder())
    packed = pack_creator_audience_view(view)
    assert packed["packing_version"] == COLUMNAR_PACKING_VERSION
    assert unpack_creator_audience_view(packed) == view
    # Packer determinism: the same view packs to the same bytes.
    assert _compact_json(pack_creator_audience_view(view)) == _compact_json(packed)


def test_tiktok_fixture_exercises_all_four_tables() -> None:
    packed = pack_creator_audience_view(build_compact_judgment_view(_tiktok_bundle()))
    assert set(packed["evidence_tables"]) == {
        "creator_content",
        "creator_content_duplicates",
        "observed_comment",
        "observed_comment_duplicates",
    }


def test_packed_view_preserves_alias_set_and_hides_durable_ids() -> None:
    bundle = _tiktok_bundle()
    manifest = build_capability_manifest(bundle)
    packed = pack_creator_audience_view(build_compact_judgment_view(bundle))
    packed_aliases = {
        row[table["columns"].index("alias")]
        for table in packed["evidence_tables"].values()
        for row in table["rows"]
    }
    assert packed_aliases == set(manifest["evidence"])
    serialized = _compact_json(packed)
    for evidence_id in (
        "content-1",
        "content-2",
        "content-3",
        "comment-1",
        "comment-2",
        "comment-3",
    ):
        assert evidence_id not in serialized
    assert "/private/audit/path" not in serialized


def test_prompt_embeds_packed_columnar_view_without_durable_ids() -> None:
    bundle = _tiktok_bundle()
    method_text, _ = load_method_deck()
    prompt = build_creator_audience_prompt(bundle, method_text=method_text)
    packed = pack_creator_audience_view(build_compact_judgment_view(bundle))

    assert "COMPACT_EVIDENCE_VIEW" in prompt
    assert COLUMNAR_PACKING_VERSION in prompt
    assert _compact_json(packed) in prompt
    assert "content-1" not in prompt
    assert "comment-1" not in prompt
    assert "/private/audit/path" not in prompt


def test_unpack_fails_loud_on_version_drift() -> None:
    packed = pack_creator_audience_view(build_compact_judgment_view(_tiktok_bundle()))
    tampered = {**packed, "packing_version": "packing_columnar_view_v1"}
    with pytest.raises(ColumnarPackingError, match="packing_version"):
        unpack_creator_audience_view(tampered)


def test_unpack_fails_loud_on_column_drift() -> None:
    packed = pack_creator_audience_view(build_compact_judgment_view(_tiktok_bundle()))
    table = packed["evidence_tables"]["observed_comment"]
    tampered = {
        **packed,
        "evidence_tables": {
            **packed["evidence_tables"],
            "observed_comment": {
                **table,
                "columns": ["renamed", *table["columns"][1:]],
            },
        },
    }
    with pytest.raises(ColumnarPackingError, match="columns drifted"):
        unpack_creator_audience_view(tampered)


def test_unpack_fails_loud_on_row_shape_drift() -> None:
    packed = pack_creator_audience_view(build_compact_judgment_view(_tiktok_bundle()))
    table = packed["evidence_tables"]["creator_content"]
    tampered = {
        **packed,
        "evidence_tables": {
            **packed["evidence_tables"],
            "creator_content": {**table, "rows": [table["rows"][0][:-1]]},
        },
    }
    with pytest.raises(ColumnarPackingError, match="column count"):
        unpack_creator_audience_view(tampered)


def test_unpack_fails_loud_on_unknown_table() -> None:
    packed = pack_creator_audience_view(build_compact_judgment_view(_tiktok_bundle()))
    tampered = {
        **packed,
        "evidence_tables": {
            **packed["evidence_tables"],
            "judged_claim": {"columns": ["alias"], "rows": []},
        },
    }
    with pytest.raises(ColumnarPackingError, match="unknown evidence tables"):
        unpack_creator_audience_view(tampered)


def test_pack_fails_loud_on_evidence_field_drift() -> None:
    view = build_compact_judgment_view(_tiktok_bundle())
    view["evidence"][0]["unexpected_field"] = 1
    with pytest.raises(ColumnarPackingError, match="unexpected"):
        pack_creator_audience_view(view)


def test_pack_rejects_foreign_view_version() -> None:
    view = build_compact_judgment_view(_tiktok_bundle())
    view["view_version"] = "creator_audience_compact_judgment_view_v2"
    with pytest.raises(ColumnarPackingError, match="view_version"):
        pack_creator_audience_view(view)


@pytest.mark.parametrize(
    "bundle_builder",
    [_scaled_tiktok_bundle, _instagram_bundle],
    ids=["tiktok_scaled", "instagram"],
)
def test_columnar_packing_reduces_fixture_view_bytes(
    bundle_builder: Callable[[], dict],
) -> None:
    # The recorded byte measurement for these generated fixtures; any
    # size-savings claim must trace to these numbers, not to earlier estimates.
    # Scoped to multi-row fixtures: at one row per table the packed form is
    # measurably larger (headers dominate), which is accepted and documented.
    view = build_compact_judgment_view(bundle_builder())
    flat_bytes = len(_compact_json(view).encode("utf-8"))
    packed_bytes = len(
        _compact_json(pack_creator_audience_view(view)).encode("utf-8")
    )
    assert packed_bytes < flat_bytes, (
        f"packed={packed_bytes}B flat={flat_bytes}B"
    )
