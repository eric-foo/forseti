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
        _item("third", 800, 80),
        _item("fourth", 700, 70),
        _item("fifth", 600, 60),
        _item("sixth", 500, 50),
        _item("seventh", 400, 40),
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
    assert negligible["exclusion_reason_or_none"] == "outside_top_view_quartile"


def test_like_rate_orders_review_only_inside_proven_reach_set() -> None:
    items = [
        _item("more_reach", 1_000, 10),
        _item("more_resonance", 900, 90),
        _item("three", 800, 80),
        _item("four", 700, 70),
        _item("five", 600, 60),
        _item("six", 500, 50),
        _item("seven", 400, 40),
        _item("eight", 300, 30),
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
        _item("four", 800, 80),
        _item("five", 700, 70),
        _item("six", 600, 60),
        _item("seven", 500, 50),
        _item("eight", 400, 40),
    ]

    selection = build_tiktok_grid_video_selection(items, expected_item_count=8)

    assert selection["selection_summary"]["selected_video_ids_in_reach_order"] == [
        "first",
        "tie_high_rate",
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
