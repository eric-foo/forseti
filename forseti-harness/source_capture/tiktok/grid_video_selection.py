"""Deterministic reach-first selection for TikTok creator-grid onboarding.

Selection membership is the top quarter by observed view count. Like rate can
break an equal-view boundary tie and orders review priority only after the
reach-qualified set is fixed. This prevents a high rate on negligible reach
from displacing a materially proven high-reach video.
"""
from __future__ import annotations

import math
from collections.abc import Sequence
from typing import Any

TIKTOK_GRID_VIDEO_SELECTION_SCHEMA_VERSION = "tiktok_grid_video_selection_v0"
TIKTOK_GRID_VIDEO_SELECTION_POLICY_VERSION = "tiktok_reach_first_top_quartile_v0"
_SELECTION_FRACTION = 0.25


class TikTokGridVideoSelectionError(ValueError):
    """Raised when a complete, trustworthy selection cannot be produced."""


def build_tiktok_grid_video_selection(
    items: Sequence[dict[str, Any]],
    *,
    expected_item_count: int,
) -> dict[str, Any]:
    """Select the reach-proven top quarter from one complete creator grid."""

    if isinstance(expected_item_count, bool) or not isinstance(expected_item_count, int):
        raise TikTokGridVideoSelectionError("expected_item_count must be an integer")
    if expected_item_count <= 0:
        raise TikTokGridVideoSelectionError("expected_item_count must be positive")
    if len(items) != expected_item_count:
        raise TikTokGridVideoSelectionError(
            "complete-grid coverage required: "
            f"expected {expected_item_count} items, received {len(items)}"
        )

    normalized = [_normalize_item(item, index=index) for index, item in enumerate(items)]
    video_ids = [item["video_id"] for item in normalized]
    if len(set(video_ids)) != len(video_ids):
        raise TikTokGridVideoSelectionError("duplicate video_id values are not allowed")

    selection_count = max(1, math.ceil(expected_item_count * _SELECTION_FRACTION))
    reach_order = sorted(
        normalized,
        key=lambda item: (
            -item["view_count"],
            -item["like_rate"],
            -item["like_count"],
            item["video_id"],
        ),
    )
    selected = reach_order[:selection_count]
    selected_ids = {item["video_id"] for item in selected}
    review_order = sorted(
        selected,
        key=lambda item: (
            -item["like_rate"],
            -item["view_count"],
            -item["like_count"],
            item["video_id"],
        ),
    )
    review_ranks = {
        item["video_id"]: index for index, item in enumerate(review_order, start=1)
    }

    ranked_items: list[dict[str, Any]] = []
    for reach_rank, item in enumerate(reach_order, start=1):
        is_selected = item["video_id"] in selected_ids
        ranked_items.append(
            {
                **item,
                "reach_rank": reach_rank,
                "selected": is_selected,
                "review_priority_rank_or_none": (
                    review_ranks[item["video_id"]] if is_selected else None
                ),
                "exclusion_reason_or_none": (
                    None if is_selected else "outside_top_view_quartile"
                ),
            }
        )

    cutoff_view_count = selected[-1]["view_count"]
    return {
        "schema_version": TIKTOK_GRID_VIDEO_SELECTION_SCHEMA_VERSION,
        "selection_policy": {
            "policy_version": TIKTOK_GRID_VIDEO_SELECTION_POLICY_VERSION,
            "selection_fraction": _SELECTION_FRACTION,
            "selection_count_rounding": "ceil_with_minimum_one",
            "required_metrics": ["playCount", "diggCount"],
            "membership_rule": (
                "Select the top ceil(25%) by view_count; like_rate breaks only "
                "equal-view ties, including at the cutoff."
            ),
            "review_priority_rule": (
                "Within the selected set only, order like_rate descending, then "
                "view_count descending."
            ),
            "negligible_reach_guard": (
                "A video outside the top view-count quartile cannot enter the "
                "selected set regardless of like_rate."
            ),
            "like_rate_recipe": "diggCount / playCount",
        },
        "coverage": {
            "expected_item_count": expected_item_count,
            "observed_item_count": len(normalized),
            "complete": True,
        },
        "selection_summary": {
            "selection_count": selection_count,
            "cutoff_view_count": cutoff_view_count,
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


def _normalize_item(item: dict[str, Any], *, index: int) -> dict[str, Any]:
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

    view_count = _required_count(
        metric_source,
        index=index,
        metric_name="playCount",
        keys=("playCount", "play_count", "view_count"),
    )
    like_count = _required_count(
        metric_source,
        index=index,
        metric_name="diggCount",
        keys=("diggCount", "digg_count", "like_count"),
    )
    if view_count == 0:
        raise TikTokGridVideoSelectionError(
            f"item {index} playCount must be positive to compute like_rate"
        )
    if like_count > view_count:
        raise TikTokGridVideoSelectionError(
            f"item {index} diggCount exceeds playCount"
        )

    return {
        "video_id": video_id,
        "view_count": view_count,
        "like_count": like_count,
        "like_rate": round(like_count / view_count, 6),
    }


def _required_count(
    payload: dict[str, Any],
    *,
    index: int,
    metric_name: str,
    keys: tuple[str, ...],
) -> int:
    value = _first_present(payload, *keys)
    if isinstance(value, bool) or not isinstance(value, int):
        raise TikTokGridVideoSelectionError(
            f"item {index} {metric_name} is missing or not an integer"
        )
    if value < 0:
        raise TikTokGridVideoSelectionError(f"item {index} {metric_name} is negative")
    return value


def _first_present(payload: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        if key in payload:
            return payload[key]
    return None


__all__ = [
    "TIKTOK_GRID_VIDEO_SELECTION_POLICY_VERSION",
    "TIKTOK_GRID_VIDEO_SELECTION_SCHEMA_VERSION",
    "TikTokGridVideoSelectionError",
    "build_tiktok_grid_video_selection",
]
