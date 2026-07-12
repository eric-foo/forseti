from __future__ import annotations

import json

import pytest

from cleaning.audience_extractor import RawApiProvider
from cleaning.tiktok_silver_analytics import (
    build_comment_classification_prompt,
    classify_comments,
    comment_engagement_context,
    parse_comment_classification,
    product_readout,
    resolve_product_mentions,
    temporal_signal,
)
from runners.run_tiktok_silver_analytics import build_readout


def _video() -> dict:
    return {
        "video_id": "v1",
        "stats": {"diggCount": 1000, "commentCount": 100},
        "comments": {
            "comments": [
                {"cid": "c1", "text": "Love YSL Y", "digg_count": 100, "reply_comment_total": 2},
                {"cid": "c2", "text": "No way", "digg_count": 10, "reply_comment_total": 7},
            ]
        },
    }


def _catalog() -> dict:
    return {
        "version": "fragrance-catalog-test-v1",
        "entities": [
            {"entity_id": "ysl-y-edp", "brand": "Yves Saint Laurent", "line": "Y Eau de Parfum", "aliases": ["YSL Y EDP"]},
            {"entity_id": "lv-city-stars", "brand": "Louis Vuitton", "line": "City of Stars", "aliases": ["city stars"]},
        ],
    }


def test_comment_context_uses_comment_like_to_video_like_ratio() -> None:
    view = comment_engagement_context(_video(), {"v1:c1": ["product_relevant"], "v1:c2": ["disagreement"]})
    assert view["comments"][0]["comment_id"] == "c1"
    assert view["comments"][0]["comment_like_to_video_like_ratio"] == pytest.approx(0.1)
    assert "captured_comment_coverage_ratio" not in view
    assert "like_percentile_within_captured" not in view["comments"][0]
    assert "not_decision_impact" in view["non_claims"]


def test_entity_resolution_preserves_unresolved_and_sov_uses_resolved_only() -> None:
    rows = resolve_product_mentions(
        [
            {"mention_id": "m1", "video_id": "v1", "brand": "YSL", "line": "YSL Y EDP", "source_pointer": "YSL Y EDP"},
            {"mention_id": "m2", "video_id": "v1", "brand": "mangled", "line": "mystery", "source_pointer": "mystery"},
        ],
        _catalog(),
    )
    assert [row["resolution_posture"] for row in rows] == ["resolved", "unresolved"]
    readout = product_readout(rows)
    assert readout["resolution_counts"] == {"resolved": 1, "ambiguous": 0, "unresolved": 1}
    assert readout["sov_denominator"] == 1
    assert readout["products"][0]["share_of_resolved_mentions"] == 1.0


def test_temporal_signal_requires_real_history() -> None:
    empty = temporal_signal([])
    assert empty["velocity_reason"] == "requires_two_genuine_observations"
    two = temporal_signal(
        [{"observed_at": "2026-01-01T00:00:00Z", "value": 100}, {"observed_at": "2026-01-01T02:00:00Z", "value": 140}]
    )
    assert two["latest_velocity_per_hour"] == 20
    assert two["acceleration_reason"] == "requires_three_genuine_observations"
    three = temporal_signal(
        [
            {"observed_at": "2026-01-01T00:00:00Z", "value": 100},
            {"observed_at": "2026-01-01T02:00:00Z", "value": 140},
            {"observed_at": "2026-01-01T04:00:00Z", "value": 200},
        ]
    )
    assert three["latest_acceleration_delta_per_hour"] == 10


def test_comment_classifier_is_one_strict_batch_call() -> None:
    class FakeTransport:
        calls = []

        def post_json(self, url, headers, body, timeout_seconds):
            self.calls.append((url, headers, body, timeout_seconds))
            labels = [
                {"video_id": "v1", "comment_id": "c1", "labels": ["product_relevant"]},
                {"video_id": "v1", "comment_id": "c2", "labels": ["disagreement"]},
            ]
            return json.dumps({"output_text": json.dumps(labels)})

    transport = FakeTransport()
    result = classify_comments(
        videos=[_video()],
        transport=transport,
        provider=RawApiProvider.OPENAI_RESPONSES,
        model="model",
        api_key="secret",
    )
    assert result == {"v1:c1": ["product_relevant"], "v1:c2": ["disagreement"]}
    assert len(transport.calls) == 1
    assert "Love YSL Y" in build_comment_classification_prompt([_video()])


def test_classifier_rejects_missing_comment_and_fused_readout_has_loud_gaps() -> None:
    with pytest.raises(ValueError, match="omitted ids"):
        parse_comment_classification(
            json.dumps([{"video_id": "v1", "comment_id": "c1", "labels": ["other"]}]),
            [_video()],
        )
    readout = build_readout(
        batch_payloads=[{"videos": [_video()]}],
        mention_records=[{"mentions": []}],
        entity_catalog=_catalog(),
    )
    assert readout["products"]["sov_posture"] == "unavailable_with_reason"
    assert readout["comments"]["semantic_posture"] == "not_attempted"
    assert readout["temporal"]["creator_metrics"]["velocity_posture"] == "unavailable_with_reason"
