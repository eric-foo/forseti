from __future__ import annotations

import pytest

from source_capture.cadence import build_cadence_plan


def test_weighted_long_tail_plan_is_seeded_and_bounded() -> None:
    kwargs = {
        "slot_count": 25,
        "mode": "weighted_long_tail",
        "delay_seconds": 0.0,
        "typical_min_gap_seconds": 5.0,
        "typical_max_gap_seconds": 20.0,
        "tail_min_gap_seconds": 20.0,
        "tail_max_gap_seconds": 60.0,
        "tail_probability": 0.05,
        "random_seed": 17,
    }

    first = build_cadence_plan(**kwargs)
    second = build_cadence_plan(**kwargs)

    assert first == second
    assert first.mode == "weighted_long_tail"
    assert len(first.planned_waits_seconds) == 24
    assert all(5.0 <= wait <= 60.0 for wait in first.planned_waits_seconds)
    assert first.tail_probability == 0.05


def test_weighted_long_tail_can_select_each_band_without_statistics() -> None:
    typical = build_cadence_plan(
        slot_count=4,
        mode="weighted_long_tail",
        delay_seconds=0.0,
        typical_min_gap_seconds=5.0,
        typical_max_gap_seconds=20.0,
        tail_min_gap_seconds=20.0,
        tail_max_gap_seconds=60.0,
        tail_probability=0.0,
        random_seed=3,
    )
    tail = build_cadence_plan(
        slot_count=4,
        mode="weighted_long_tail",
        delay_seconds=0.0,
        typical_min_gap_seconds=5.0,
        typical_max_gap_seconds=20.0,
        tail_min_gap_seconds=20.0,
        tail_max_gap_seconds=60.0,
        tail_probability=1.0,
        random_seed=3,
    )

    assert all(5.0 <= wait <= 20.0 for wait in typical.planned_waits_seconds)
    assert all(20.0 <= wait <= 60.0 for wait in tail.planned_waits_seconds)


@pytest.mark.parametrize(
    "overrides",
    [
        {"typical_min_gap_seconds": -1.0},
        {"typical_max_gap_seconds": 4.0},
        {"tail_min_gap_seconds": 19.0},
        {"tail_max_gap_seconds": 19.0},
        {"tail_probability": 1.1},
    ],
)
def test_weighted_long_tail_rejects_invalid_configuration(
    overrides: dict[str, float],
) -> None:
    kwargs = {
        "slot_count": 2,
        "mode": "weighted_long_tail",
        "delay_seconds": 0.0,
        "typical_min_gap_seconds": 5.0,
        "typical_max_gap_seconds": 20.0,
        "tail_min_gap_seconds": 20.0,
        "tail_max_gap_seconds": 60.0,
        "tail_probability": 0.05,
        "random_seed": 3,
        **overrides,
    }

    with pytest.raises(ValueError):
        build_cadence_plan(**kwargs)
