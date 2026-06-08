from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Literal


CadenceMode = Literal["fixed", "bounded_jitter"]


@dataclass(frozen=True)
class CadencePlan:
    mode: CadenceMode
    slot_count: int
    planned_offsets_seconds: tuple[float, ...]
    planned_waits_seconds: tuple[float, ...]
    delay_seconds: float | None = None
    window_seconds: float | None = None
    min_gap_seconds: float | None = None
    max_gap_seconds: float | None = None
    random_seed: int | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "mode": self.mode,
            "slot_count": self.slot_count,
            "planned_offsets_seconds": list(self.planned_offsets_seconds),
            "planned_waits_seconds": list(self.planned_waits_seconds),
            "delay_seconds": self.delay_seconds,
            "window_seconds": self.window_seconds,
            "min_gap_seconds": self.min_gap_seconds,
            "max_gap_seconds": self.max_gap_seconds,
            "random_seed": self.random_seed,
        }


def build_cadence_plan(
    *,
    slot_count: int,
    mode: CadenceMode,
    delay_seconds: float,
    window_seconds: float | None = None,
    min_gap_seconds: float | None = None,
    max_gap_seconds: float | None = None,
    random_seed: int | None = None,
) -> CadencePlan:
    if slot_count <= 0:
        raise ValueError("cadence requires at least one slot")
    if mode == "fixed":
        return _build_fixed_plan(slot_count=slot_count, delay_seconds=delay_seconds)
    if mode == "bounded_jitter":
        return _build_bounded_jitter_plan(
            slot_count=slot_count,
            window_seconds=window_seconds,
            min_gap_seconds=min_gap_seconds,
            max_gap_seconds=max_gap_seconds,
            random_seed=random_seed,
        )
    raise ValueError("cadence_mode must be fixed or bounded_jitter")


def _build_fixed_plan(*, slot_count: int, delay_seconds: float) -> CadencePlan:
    if delay_seconds < 0:
        raise ValueError("delay_seconds must be zero or greater")
    waits = tuple(round(delay_seconds, 3) for _ in range(max(0, slot_count - 1)))
    return CadencePlan(
        mode="fixed",
        slot_count=slot_count,
        planned_offsets_seconds=_offsets_from_waits(waits),
        planned_waits_seconds=waits,
        delay_seconds=delay_seconds,
    )


def _build_bounded_jitter_plan(
    *,
    slot_count: int,
    window_seconds: float | None,
    min_gap_seconds: float | None,
    max_gap_seconds: float | None,
    random_seed: int | None,
) -> CadencePlan:
    if window_seconds is None:
        raise ValueError("cadence_window_seconds is required for bounded_jitter")
    if min_gap_seconds is None:
        raise ValueError("cadence_min_gap_seconds is required for bounded_jitter")
    if max_gap_seconds is None:
        raise ValueError("cadence_max_gap_seconds is required for bounded_jitter")
    if window_seconds < 0:
        raise ValueError("cadence_window_seconds must be zero or greater")
    if min_gap_seconds < 0:
        raise ValueError("cadence_min_gap_seconds must be zero or greater")
    if max_gap_seconds < min_gap_seconds:
        raise ValueError("cadence_max_gap_seconds must be greater than or equal to cadence_min_gap_seconds")

    wait_count = max(0, slot_count - 1)
    minimum_span = min_gap_seconds * wait_count
    if minimum_span > window_seconds:
        raise ValueError(
            "cadence window cannot fit the URL count at the requested minimum gap"
        )

    seed = random_seed
    if seed is None:
        seed = random.SystemRandom().randrange(1, 2**31)
    rng = random.Random(seed)

    waits: list[float] = []
    elapsed = 0.0
    for wait_index in range(wait_count):
        waits_remaining_after_current = wait_count - wait_index - 1
        max_allowed_now = window_seconds - elapsed - (min_gap_seconds * waits_remaining_after_current)
        upper = min(max_gap_seconds, max_allowed_now)
        if upper < min_gap_seconds:
            raise ValueError(
                "cadence window cannot fit the URL count at the requested minimum gap"
            )
        wait = rng.uniform(min_gap_seconds, upper)
        wait = round(wait, 3)
        waits.append(wait)
        elapsed += wait

    waits_tuple = tuple(waits)
    return CadencePlan(
        mode="bounded_jitter",
        slot_count=slot_count,
        planned_offsets_seconds=_offsets_from_waits(waits_tuple),
        planned_waits_seconds=waits_tuple,
        window_seconds=window_seconds,
        min_gap_seconds=min_gap_seconds,
        max_gap_seconds=max_gap_seconds,
        random_seed=seed,
    )


def _offsets_from_waits(waits: tuple[float, ...]) -> tuple[float, ...]:
    offsets = [0.0]
    elapsed = 0.0
    for wait in waits:
        elapsed = round(elapsed + wait, 3)
        offsets.append(elapsed)
    return tuple(offsets)
