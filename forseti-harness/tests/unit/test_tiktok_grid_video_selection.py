from __future__ import annotations

import json
from pathlib import Path

import pytest

from runners.run_source_capture_tiktok_grid_video_selection import (
    run_tiktok_grid_video_selection,
)
from source_capture.tiktok.grid_video_selection import (
    TIKTOK_GRID_VIDEO_SELECTION_POLICY_VERSION,
    TikTokGridVideoSelectionError,
    build_tiktok_grid_video_selection,
)


def _item(video_id: str, views: int, likes: int) -> dict[str, object]:
    return {"id": video_id, "stats": {"playCount": views, "diggCount": likes}}


def test_selects_top_view_quartile_and_excludes_negligible_reach() -> None:
    items = [
        _item("high", 1_000, 10),
        _item("second", 900, 90),
        _item("third", 800, 8),
        _item("fourth", 700, 7),
        _item("fifth", 600, 6),
        _item("sixth", 500, 5),
        _item("seventh", 400, 4),
        _item("negligible", 10, 10),
    ]

    selection = build_tiktok_grid_video_selection(items, expected_item_count=8)

    assert selection["selection_policy"]["policy_version"] == TIKTOK_GRID_VIDEO_SELECTION_POLICY_VERSION
    assert selection["selection_summary"]["selected_video_ids_in_reach_order"] == [
        "high",
        "second",
    ]
    negligible = next(
        item for item in selection["ranked_items"] if item["video_id"] == "negligible"
    )
    assert negligible["like_rate"] == 1.0
    assert negligible["selected"] is False
    assert negligible["exclusion_reason_or_none"] == "not_selected_after_boundary_comparison"


def test_like_rate_orders_review_priority_inside_selected_set() -> None:
    items = [
        _item("more_reach", 1_000, 10),
        _item("more_resonance", 900, 90),
        _item("three", 800, 8),
        _item("four", 700, 7),
        _item("five", 600, 6),
        _item("six", 500, 5),
        _item("seven", 400, 4),
        _item("eight", 300, 3),
    ]

    selection = build_tiktok_grid_video_selection(items, expected_item_count=8)

    assert selection["selection_summary"]["selected_video_ids_in_reach_order"] == [
        "more_reach",
        "more_resonance",
    ]
    assert selection["selection_summary"]["selected_video_ids_in_review_priority_order"] == [
        "more_resonance",
        "more_reach",
    ]


def test_like_rate_breaks_equal_view_boundary_tie() -> None:
    items = [
        _item("first", 1_000, 10),
        _item("tie_low_rate", 900, 9),
        _item("tie_high_rate", 900, 90),
        _item("four", 800, 8),
        _item("five", 700, 7),
        _item("six", 600, 6),
        _item("seven", 500, 5),
        _item("eight", 400, 4),
    ]

    selection = build_tiktok_grid_video_selection(items, expected_item_count=8)

    assert selection["selection_summary"]["selected_video_ids_in_reach_order"] == [
        "first",
        "tie_high_rate",
    ]


def test_boundary_challenger_can_replace_at_exact_thresholds() -> None:
    items = [
        _item("locked", 1_200, 120),
        _item("incumbent", 1_000, 100),
        _item("challenger", 800, 96),
        _item("four", 700, 7),
        _item("five", 600, 6),
        _item("six", 500, 5),
        _item("seven", 400, 4),
        _item("eight", 300, 3),
    ]

    selection = build_tiktok_grid_video_selection(items, expected_item_count=8)

    assert selection["selection_summary"]["selected_video_ids_in_reach_order"] == [
        "locked",
        "challenger",
    ]
    assert selection["selection_summary"]["promotion_count"] == 1
    incumbent = next(
        item for item in selection["ranked_items"] if item["video_id"] == "incumbent"
    )
    assert incumbent["exclusion_reason_or_none"] == (
        "replaced_by_within_range_higher_like_rate"
    )
    assert selection["selection_summary"]["promotions"] == [
        {
            "promoted_video_id": "challenger",
            "replaced_video_id": "incumbent",
            "view_retention_ratio": 0.8,
            "like_rate_lift_ratio": 1.2,
            "incumbent_like_rate_was_zero": False,
        }
    ]


def test_boundary_challenger_fails_when_views_are_more_than_twenty_percent_lower() -> None:
    items = [
        _item("locked", 1_000, 10),
        _item("incumbent", 900, 9),
        _item("challenger", 700, 70),
        _item("four", 600, 6),
        _item("five", 500, 5),
        _item("six", 400, 4),
        _item("seven", 300, 3),
        _item("eight", 200, 2),
    ]

    selection = build_tiktok_grid_video_selection(items, expected_item_count=8)

    assert selection["selection_summary"]["selected_video_ids_in_reach_order"] == [
        "locked",
        "incumbent",
    ]
    assert selection["selection_summary"]["promotion_count"] == 0


def test_boundary_challenger_fails_without_twenty_percent_like_rate_lift() -> None:
    items = [
        _item("locked", 1_000, 100),
        _item("incumbent", 900, 90),
        _item("challenger", 850, 95),
        _item("four", 700, 70),
        _item("five", 600, 60),
        _item("six", 500, 50),
        _item("seven", 400, 40),
        _item("eight", 300, 30),
    ]

    selection = build_tiktok_grid_video_selection(items, expected_item_count=8)

    assert selection["selection_summary"]["selected_video_ids_in_reach_order"] == [
        "locked",
        "incumbent",
    ]
    assert selection["selection_summary"]["promotion_count"] == 0


def test_promotions_cannot_chain_the_reach_floor_downward() -> None:
    items = [
        _item("locked", 1_000, 10),
        _item("incumbent", 900, 9),
        _item("qualifying", 750, 150),
        _item("would_chain", 610, 610),
        _item("five", 500, 5),
        _item("six", 400, 4),
        _item("seven", 300, 3),
        _item("eight", 200, 2),
    ]

    selection = build_tiktok_grid_video_selection(items, expected_item_count=8)

    assert selection["selection_summary"]["selected_video_ids_in_reach_order"] == [
        "locked",
        "qualifying",
    ]
    assert "would_chain" not in selection["selection_summary"][
        "selected_video_ids_in_reach_order"
    ]


@pytest.mark.parametrize(
    ("items", "expected_count", "message"),
    [
        ([_item("one", 100, 10)], 2, "complete-grid coverage required"),
        ([_item("one", 100, 10), _item("one", 90, 9)], 2, "duplicate video_id"),
        ([{"id": "one", "stats": {"playCount": 100}}], 1, "diggCount"),
        ([_item("one", 0, 0)], 1, "playCount must be positive"),
        ([_item("one", 100, 101)], 1, "diggCount exceeds playCount"),
    ],
)
def test_selection_fails_closed_on_untrustworthy_inputs(
    items: list[dict[str, object]],
    expected_count: int,
    message: str,
) -> None:
    with pytest.raises(TikTokGridVideoSelectionError, match=message):
        build_tiktok_grid_video_selection(items, expected_item_count=expected_count)


def test_runner_reads_probe_summary_shape_and_writes_receipt(tmp_path: Path) -> None:
    input_path = tmp_path / "probe_summary.json"
    output_path = tmp_path / "selection.json"
    input_path.write_text(
        json.dumps(
            {
                "public_item_stats": [
                    {"id": "one", "playCount": 400, "diggCount": 20},
                    {"id": "two", "playCount": 300, "diggCount": 30},
                    {"id": "three", "playCount": 200, "diggCount": 20},
                    {"id": "four", "playCount": 100, "diggCount": 10},
                ]
            }
        ),
        encoding="utf-8",
    )

    selection = run_tiktok_grid_video_selection(
        input_path=input_path,
        expected_item_count=4,
        output_path=output_path,
    )

    persisted = json.loads(output_path.read_text(encoding="utf-8"))
    assert selection["selection_summary"]["selected_video_ids_in_reach_order"] == ["one"]
    assert persisted["input_receipt"]["file_name"] == input_path.name
    assert len(persisted["input_receipt"]["sha256"]) == 64
