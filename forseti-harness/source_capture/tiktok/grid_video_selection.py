"""Deterministic reach-first selection for TikTok creator-grid onboarding.

Fractional selection supports the existing bounded like-rate override. Fixed-count
onboarding selection is strict reach rank: pinned state is recorded but never changes
membership or order.
"""
from __future__ import annotations

import math
from collections.abc import Sequence
from fractions import Fraction
from typing import Any

TIKTOK_GRID_VIDEO_SELECTION_SCHEMA_VERSION = "tiktok_grid_video_selection_v1"
TIKTOK_GRID_VIDEO_SELECTION_FIXED_COUNT_POLICY_VERSION = "tiktok_reach_ranked_fixed_count_v3"
TIKTOK_GRID_VIDEO_SELECTION_POLICY_VERSION = "tiktok_reach_first_top_fraction_v3"
_DEFAULT_SELECTION_FRACTION = Fraction(1, 4)
_MINIMUM_VIEW_RETENTION_PERCENT = 80
_MINIMUM_LIKE_RATE_LIFT_PERCENT = 20


class TikTokGridVideoSelectionError(ValueError):
    """Raised when a complete, trustworthy selection cannot be produced."""


def build_tiktok_grid_video_selection(
    items: Sequence[dict[str, Any]],
    *,
    expected_item_count: int,
    selection_fraction: float = 0.25,
    selection_count: int | None = None,
) -> dict[str, Any]:
    """Select a reach-proven fraction or fixed count from one complete grid."""

    if isinstance(expected_item_count, bool) or not isinstance(expected_item_count, int):
        raise TikTokGridVideoSelectionError("expected_item_count must be an integer")
    if expected_item_count <= 0:
        raise TikTokGridVideoSelectionError("expected_item_count must be positive")
    normalized_selection_fraction = _normalize_selection_fraction(selection_fraction)
    if selection_count is not None:
        if isinstance(selection_count, bool) or not isinstance(selection_count, int):
            raise TikTokGridVideoSelectionError("selection_count must be an integer")
        if selection_count <= 0 or selection_count > expected_item_count:
            raise TikTokGridVideoSelectionError(
                "selection_count must be positive and no greater than expected_item_count"
            )
    if len(items) != expected_item_count:
        raise TikTokGridVideoSelectionError(
            "complete-grid coverage required: "
            f"expected {expected_item_count} items, received {len(items)}"
        )

    fixed_count_mode = selection_count is not None
    normalized = [
        _normalize_item(
            item,
            index=index,
            require_like_count=not fixed_count_mode,
        )
        for index, item in enumerate(items)
    ]
    video_ids = [item["video_id"] for item in normalized]
    if len(set(video_ids)) != len(video_ids):
        raise TikTokGridVideoSelectionError("duplicate video_id values are not allowed")

    resolved_selection_count = selection_count or max(
        1, math.ceil(expected_item_count * normalized_selection_fraction)
    )
    eligible = [item for item in normalized if item["selection_eligible"]]
    if len(eligible) < resolved_selection_count:
        raise TikTokGridVideoSelectionError(
            "insufficient selection-eligible rows: "
            f"required {resolved_selection_count}, found {len(eligible)}"
        )
    reach_order = sorted(
        eligible,
        key=lambda item: (
            (-item["view_count"], item["video_id"])
            if fixed_count_mode
            else (
                -item["view_count"],
                -_like_rate_fraction(item),
                -item["like_count"],
                item["video_id"],
            )
        ),
    )
    baseline_selected = reach_order[:resolved_selection_count]
    baseline_cutoff_view_count = baseline_selected[-1]["view_count"]
    if selection_count is not None:
        selected = list(baseline_selected)
        range_overrides: list[dict[str, Any]] = []
    else:
        selected, range_overrides = _apply_boundary_range_overrides(
            baseline_selected=baseline_selected,
            challengers=reach_order[resolved_selection_count:],
        )
    selected_ids = {item["video_id"] for item in selected}
    replaced_ids = {receipt["replaced_video_id"] for receipt in range_overrides}
    review_order = (
        list(selected)
        if selection_count is not None
        else sorted(
            selected,
            key=lambda item: (
                -_like_rate_fraction(item),
                -item["view_count"],
                -item["like_count"],
                item["video_id"],
            ),
        )
    )
    review_ranks = {
        item["video_id"]: index for index, item in enumerate(review_order, start=1)
    }

    ranked_items: list[dict[str, Any]] = []
    for reach_rank, item in enumerate(reach_order, start=1):
        is_selected = item["video_id"] in selected_ids
        ranked_items.append(
            {
                **{key: value for key, value in item.items() if key != "_source_index"},
                "reach_rank": reach_rank,
                "selected": is_selected,
                "review_priority_rank_or_none": (
                    review_ranks[item["video_id"]] if is_selected else None
                ),
                "exclusion_reason_or_none": (
                    None
                    if is_selected
                    else (
                        "replaced_by_within_range_higher_like_rate"
                        if item["video_id"] in replaced_ids
                        else "not_selected_after_boundary_comparison"
                    )
                ),
            }
        )
    for item in sorted(
        (row for row in normalized if not row["selection_eligible"]),
        key=lambda row: row["_source_index"],
    ):
        ranked_items.append(
            {
                **{key: value for key, value in item.items() if key != "_source_index"},
                "reach_rank": None,
                "selected": False,
                "review_priority_rank_or_none": None,
                "exclusion_reason_or_none": (
                    "selection_ineligible:"
                    f"{item['selection_ineligibility_reason_or_none']}"
                ),
            }
        )

    return {
        "schema_version": TIKTOK_GRID_VIDEO_SELECTION_SCHEMA_VERSION,
        "selection_policy": {
            "policy_version": (
                TIKTOK_GRID_VIDEO_SELECTION_FIXED_COUNT_POLICY_VERSION
                if selection_count is not None
                else TIKTOK_GRID_VIDEO_SELECTION_POLICY_VERSION
            ),
            "selection_mode": "fixed_count" if selection_count is not None else "fraction",
            "selection_fraction": (
                None if selection_count is not None else float(normalized_selection_fraction)
            ),
            "configured_selection_count_or_none": selection_count,
            "selection_count_rounding": (
                None if selection_count is not None else "ceil_with_minimum_one"
            ),
            "required_metrics": (
                ["playCount"] if fixed_count_mode else ["playCount", "diggCount"]
            ),
            "ineligible_row_rule": (
                "Preserve source-owned grid rows in the grid artifact and selection receipt, "
                "but exclude rows whose playCount cannot support fixed-count reach ranking. "
                "Naturally available diggCount remains useful context but is not required."
                if fixed_count_mode
                else "Preserve source-owned grid rows in the grid artifact and selection receipt, "
                "but exclude rows whose playCount/diggCount cannot support the ranking recipe."
            ),
            "membership_rule": (
                "Select the fixed count strictly by eligible view_count reach rank; pinned "
                "state is recorded but never changes membership."
                if selection_count is not None
                else "Start with the configured fraction by view_count. An outside video "
                "may replace an original view-selected incumbent only when it retains at "
                "least 80% of that incumbent's views and has at least 20% higher like_rate."
            ),
            "review_priority_rule": (
                "Use the same eligible reach order as membership."
                if selection_count is not None
                else "Within the selected set only, order like_rate descending, then "
                "view_count descending."
            ),
            "pinned_video_rule": (
                "Pinned videos remain eligible and pinned state is recorded, but pinning "
                "does not displace reach ranking."
            ),
            "negligible_reach_guard": (
                "Range overrides compare only against original view-selected incumbents; "
                "an override video cannot become a new lower-reach comparison anchor."
            ),
            "competing_challenger_order_rule": (
                "When more than one challenger qualifies, challengers are matched "
                "in like_rate-descending order; each qualifying challenger claims "
                "the lowest-like_rate remaining incumbent it qualifies against. "
                "A later qualifying challenger can remain outside the selection if an "
                "earlier challenger already claimed its only eligible incumbent."
            ),
            "minimum_view_retention_percent": _MINIMUM_VIEW_RETENTION_PERCENT,
            "minimum_like_rate_lift_percent": _MINIMUM_LIKE_RATE_LIFT_PERCENT,
            "like_rate_recipe": (
                "diggCount / playCount when naturally available; not required for fixed-count membership"
                if fixed_count_mode
                else "diggCount / playCount"
            ),
        },
        "coverage": {
            "expected_item_count": expected_item_count,
            "observed_item_count": len(normalized),
            "selection_eligible_item_count": len(eligible),
            "selection_ineligible_item_count": len(normalized) - len(eligible),
            "complete": True,
        },
        "selection_summary": {
            "selection_count": resolved_selection_count,
            "baseline_cutoff_view_count": baseline_cutoff_view_count,
            "final_minimum_view_count": min(item["view_count"] for item in selected),
            "range_override_count": len(range_overrides),
            "range_overrides": range_overrides,
            "selected_video_ids_in_reach_order": [
                item["video_id"] for item in selected
            ],
            "selected_video_ids_in_review_priority_order": [
                item["video_id"] for item in review_order
            ],
        },
        "ranked_items": ranked_items,
        "non_claims": [
            "not a prediction of future virality",
            "not proof of creative causality",
            "not Creator Registry truth",
        ],
    }



def _normalize_selection_fraction(value: float) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TikTokGridVideoSelectionError("selection_fraction must be numeric")
    normalized = Fraction(str(value))
    if normalized <= 0 or normalized > 1:
        raise TikTokGridVideoSelectionError("selection_fraction must be greater than 0 and at most 1")
    return normalized


def _apply_boundary_range_overrides(
    *,
    baseline_selected: Sequence[dict[str, Any]],
    challengers: Sequence[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    remaining_incumbents = list(baseline_selected)
    override_items: list[dict[str, Any]] = []
    range_override_receipts: list[dict[str, Any]] = []
    challenger_order = sorted(
        challengers,
        key=lambda item: (
            -_like_rate_fraction(item),
            -item["view_count"],
            -item["like_count"],
            item["video_id"],
        ),
    )

    for challenger in challenger_order:
        replaceable = [
            incumbent
            for incumbent in remaining_incumbents
            if _within_view_range(challenger, incumbent)
            and _has_required_like_rate_lift(challenger, incumbent)
        ]
        if not replaceable:
            continue
        incumbent = min(
            replaceable,
            key=lambda item: (
                _like_rate_fraction(item),
                item["view_count"],
                item["video_id"],
            ),
        )
        remaining_incumbents.remove(incumbent)
        override_items.append(challenger)
        range_override_receipts.append(
            {
                "range_override_video_id": challenger["video_id"],
                "replaced_video_id": incumbent["video_id"],
                "view_retention_ratio": round(
                    challenger["view_count"] / incumbent["view_count"], 6
                ),
                "like_rate_lift_ratio": (
                    round(
                        float(
                            _like_rate_fraction(challenger)
                            / _like_rate_fraction(incumbent)
                        ),
                        6,
                    )
                    if incumbent["like_count"] > 0
                    else None
                ),
                "incumbent_like_rate_was_zero": incumbent["like_count"] == 0,
            }
        )

    final_selected = sorted(
        [*remaining_incumbents, *override_items],
        key=lambda item: (
            -item["view_count"],
            -_like_rate_fraction(item),
            -item["like_count"],
            item["video_id"],
        ),
    )
    return final_selected, range_override_receipts


def _within_view_range(
    challenger: dict[str, Any], incumbent: dict[str, Any]
) -> bool:
    return (
        challenger["view_count"] * 100
        >= incumbent["view_count"] * _MINIMUM_VIEW_RETENTION_PERCENT
    )


def _has_required_like_rate_lift(
    challenger: dict[str, Any], incumbent: dict[str, Any]
) -> bool:
    if challenger["like_count"] == 0:
        return False
    if incumbent["like_count"] == 0:
        return True
    return (
        challenger["like_count"]
        * incumbent["view_count"]
        * 100
        >= incumbent["like_count"]
        * challenger["view_count"]
        * (100 + _MINIMUM_LIKE_RATE_LIFT_PERCENT)
    )


def _like_rate_fraction(item: dict[str, Any]) -> Fraction:
    return Fraction(item["like_count"], item["view_count"])


def _normalize_item(
    item: dict[str, Any],
    *,
    index: int,
    require_like_count: bool,
) -> dict[str, Any]:
    if not isinstance(item, dict):
        raise TikTokGridVideoSelectionError(f"item {index} must be an object")
    stats = item.get("stats")
    metric_source = stats if isinstance(stats, dict) else item

    raw_video_id = _first_present(item, "video_id", "id", "item_id")
    if isinstance(raw_video_id, bool) or not isinstance(raw_video_id, (str, int)):
        raise TikTokGridVideoSelectionError(f"item {index} video_id is missing or invalid")
    video_id = str(raw_video_id).strip()
    if not video_id:
        raise TikTokGridVideoSelectionError(f"item {index} video_id is blank")

    view_count, view_reason = _optional_selection_count(
        metric_source,
        metric_name="playCount",
        keys=("playCount", "play_count", "view_count"),
    )
    like_count, like_reason = _optional_selection_count(
        metric_source,
        metric_name="diggCount",
        keys=("diggCount", "digg_count", "like_count"),
    )
    ineligibility_reason = view_reason or (like_reason if require_like_count else None)
    if ineligibility_reason is None and view_count == 0:
        ineligibility_reason = "playCount_zero"
    if (
        ineligibility_reason is None
        and view_count is not None
        and like_count is not None
        and require_like_count
        and like_count > view_count
    ):
        ineligibility_reason = "diggCount_exceeds_playCount"
    eligible = ineligibility_reason is None

    return {
        "video_id": video_id,
        "view_count": view_count,
        "like_count": like_count,
        "like_rate": (
            round(like_count / view_count, 6)
            if view_count not in (None, 0) and like_count is not None
            else None
        ),
        "selection_eligible": eligible,
        "selection_ineligibility_reason_or_none": ineligibility_reason,
        "pinned_visible": item.get("pinned_visible") is True,
        "_source_index": index,
    }


def _optional_selection_count(
    payload: dict[str, Any],
    *,
    metric_name: str,
    keys: tuple[str, ...],
) -> tuple[int | None, str | None]:
    value = _first_present(payload, *keys)
    if value is None:
        return None, f"{metric_name}_missing"
    if isinstance(value, bool) or not isinstance(value, int):
        return None, f"{metric_name}_not_integer"
    if value < 0:
        return None, f"{metric_name}_negative"
    return value, None


def _first_present(payload: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        if key in payload:
            return payload[key]
    return None


__all__ = [
    "TIKTOK_GRID_VIDEO_SELECTION_POLICY_VERSION",
    "TIKTOK_GRID_VIDEO_SELECTION_FIXED_COUNT_POLICY_VERSION",
    "TIKTOK_GRID_VIDEO_SELECTION_SCHEMA_VERSION",
    "TikTokGridVideoSelectionError",
    "build_tiktok_grid_video_selection",
]
