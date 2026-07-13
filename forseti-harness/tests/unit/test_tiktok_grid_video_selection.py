from __future__ import annotations

import json
from pathlib import Path

import pytest

from runners.run_source_capture_tiktok_grid_video_selection import (
    run_tiktok_grid_video_selection,
)
from source_capture.tiktok.grid_video_selection import (
    TIKTOK_GRID_VIDEO_SELECTION_POLICY_VERSION,
    TIKTOK_GRID_VIDEO_SELECTION_FIXED_COUNT_POLICY_VERSION,
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
    assert selection["selection_summary"]["range_override_count"] == 1
    incumbent = next(
        item for item in selection["ranked_items"] if item["video_id"] == "incumbent"
    )
    assert incumbent["exclusion_reason_or_none"] == (
        "replaced_by_within_range_higher_like_rate"
    )
    assert selection["selection_summary"]["range_overrides"] == [
        {
            "range_override_video_id": "challenger",
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
    assert selection["selection_summary"]["range_override_count"] == 0


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
    assert selection["selection_summary"]["range_override_count"] == 0


def test_range_overrides_cannot_chain_the_reach_floor_downward() -> None:
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


def test_incumbent_with_zero_like_rate_is_replaced_with_no_lift_ratio() -> None:
    items = [
        _item("locked", 1_200, 120),
        _item("incumbent", 1_000, 0),
        _item("challenger", 900, 5),
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
    assert selection["selection_summary"]["range_overrides"] == [
        {
            "range_override_video_id": "challenger",
            "replaced_video_id": "incumbent",
            "view_retention_ratio": 0.9,
            "like_rate_lift_ratio": None,
            "incumbent_like_rate_was_zero": True,
        }
    ]


def test_challenger_processing_order_can_leave_a_qualifying_challenger_outside_selection() -> None:
    # Documents (does not endorse) the greedy assignment order recorded in
    # selection_policy.competing_challenger_order_rule: challengers are matched
    # in like_rate-descending order, and each claims the lowest-like_rate
    # remaining eligible incumbent. Here "c1" (higher like_rate) is processed
    # first and claims "b" -- the only incumbent shared with "c2" -- even
    # though a different pairing (c1<->a, c2<->b) would have selected both through range overrides
    # challengers. "c2" individually satisfies the 80%/20% thresholds against
    # "b" but is left outside the selection solely because of processing order.
    items = [
        _item("a", 1_000, 10),
        _item("b", 1_000, 5),
        _item("c1", 900, 15),
        _item("c2", 850, 7),
        _item("d", 700, 0),
        _item("e", 600, 0),
        _item("f", 500, 0),
        _item("g", 400, 0),
    ]

    selection = build_tiktok_grid_video_selection(items, expected_item_count=8)

    assert selection["selection_summary"]["selected_video_ids_in_reach_order"] == [
        "a",
        "c1",
    ]
    assert selection["selection_summary"]["range_override_count"] == 1
    c2 = next(
        item for item in selection["ranked_items"] if item["video_id"] == "c2"
    )
    assert c2["selected"] is False
    assert c2["exclusion_reason_or_none"] == "not_selected_after_boundary_comparison"


def test_runner_reads_bare_list_input(tmp_path: Path) -> None:
    input_path = tmp_path / "bare_list.json"
    output_path = tmp_path / "selection.json"
    input_path.write_text(
        json.dumps(
            [
                {"id": "one", "playCount": 400, "diggCount": 20},
                {"id": "two", "playCount": 300, "diggCount": 30},
                {"id": "three", "playCount": 200, "diggCount": 20},
                {"id": "four", "playCount": 100, "diggCount": 10},
            ]
        ),
        encoding="utf-8",
    )

    selection = run_tiktok_grid_video_selection(
        input_path=input_path,
        expected_item_count=4,
        output_path=output_path,
    )

    assert selection["selection_summary"]["selected_video_ids_in_reach_order"] == ["one"]


@pytest.mark.parametrize(
    ("items", "expected_count", "message"),
    [
        ([_item("one", 100, 10)], 2, "complete-grid coverage required"),
        ([_item("one", 100, 10), _item("one", 90, 9)], 2, "duplicate video_id"),
    ],
)
def test_selection_fails_closed_on_untrustworthy_inputs(
    items: list[dict[str, object]],
    expected_count: int,
    message: str,
) -> None:
    with pytest.raises(TikTokGridVideoSelectionError, match=message):
        build_tiktok_grid_video_selection(items, expected_item_count=expected_count)


def test_selection_preserves_ineligible_rows_when_enough_eligible_rows_remain() -> None:
    selection = build_tiktok_grid_video_selection(
        [
            _item("eligible_one", 300, 30),
            {"id": "missing_like", "stats": {"playCount": 200}},
            _item("zero_views", 0, 0),
            _item("eligible_two", 100, 10),
        ],
        expected_item_count=4,
        selection_count=1,
    )

    assert selection["coverage"] == {
        "expected_item_count": 4,
        "observed_item_count": 4,
        "selection_eligible_item_count": 2,
        "selection_ineligible_item_count": 2,
        "complete": True,
    }
    by_id = {row["video_id"]: row for row in selection["ranked_items"]}
    assert by_id["missing_like"]["reach_rank"] is None
    assert by_id["missing_like"]["exclusion_reason_or_none"] == (
        "selection_ineligible:diggCount_missing"
    )
    assert by_id["zero_views"]["reach_rank"] is None
    assert by_id["zero_views"]["exclusion_reason_or_none"] == (
        "selection_ineligible:playCount_zero"
    )


def test_selection_fails_only_when_eligible_rows_are_insufficient() -> None:
    items = [
        _item("eligible", 100, 10),
        {"id": "missing_like", "stats": {"playCount": 90}},
        _item("zero_views", 0, 0),
        _item("likes_exceed_views", 10, 11),
    ]

    with pytest.raises(
        TikTokGridVideoSelectionError,
        match="insufficient selection-eligible rows: required 2, found 1",
    ):
        build_tiktok_grid_video_selection(
            items,
            expected_item_count=4,
            selection_count=2,
        )


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


def test_selection_fraction_override_is_recorded_and_applied() -> None:
    selection = build_tiktok_grid_video_selection(
        [
            _item("one", 400, 20),
            _item("two", 300, 15),
            _item("three", 200, 10),
            _item("four", 100, 5),
        ],
        expected_item_count=4,
        selection_fraction=0.5,
    )

    assert selection["selection_policy"]["selection_fraction"] == 0.5
    assert selection["selection_summary"]["selection_count"] == 2
    assert "promot" not in json.dumps(selection).lower()


@pytest.mark.parametrize("fraction", [0, -0.25, 1.25, True, "0.25"])
def test_selection_fraction_rejects_invalid_values(fraction: object) -> None:
    with pytest.raises(TikTokGridVideoSelectionError, match="selection_fraction"):
        build_tiktok_grid_video_selection(
            [_item("one", 100, 10)],
            expected_item_count=1,
            selection_fraction=fraction,  # type: ignore[arg-type]
        )


def test_fixed_selection_count_is_recorded_and_applied() -> None:
    items = [
        _item(str(index), 1_000 - index * 10, 100 - index)
        for index in range(10)
    ]

    selection = build_tiktok_grid_video_selection(
        items, expected_item_count=10, selection_count=8
    )

    assert selection["selection_policy"]["selection_mode"] == "fixed_count"
    assert (
        selection["selection_policy"]["policy_version"]
        == TIKTOK_GRID_VIDEO_SELECTION_FIXED_COUNT_POLICY_VERSION
    )
    assert selection["selection_policy"]["selection_fraction"] is None
    assert selection["selection_policy"]["configured_selection_count_or_none"] == 8
    assert selection["selection_summary"]["selection_count"] == 8


@pytest.mark.parametrize("selection_count", [0, -1, 11, True, 1.5])
def test_fixed_selection_count_rejects_invalid_values(selection_count: object) -> None:
    with pytest.raises(TikTokGridVideoSelectionError, match="selection_count"):
        build_tiktok_grid_video_selection(
            [_item(str(index), 100 - index, 10) for index in range(10)],
            expected_item_count=10,
            selection_count=selection_count,  # type: ignore[arg-type]
        )
