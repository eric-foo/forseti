from __future__ import annotations

import argparse

from source_capture.cadence import build_cadence_plan
from source_capture.models import (
    VisibleFact,
    known_fact,
    not_applicable,
    not_attempted,
    unknown_with_reason,
)


def build_optional_fact(
    *,
    label: str,
    value: str | None = None,
    unknown_reason: str | None = None,
    not_attempted_reason: str | None = None,
    not_applicable_reason: str | None = None,
) -> VisibleFact | None:
    supplied = [
        item
        for item in (value, unknown_reason, not_attempted_reason, not_applicable_reason)
        if item is not None
    ]
    if len(supplied) > 1:
        raise ValueError(f"{label} accepts only one value/reason flag")
    if value is not None:
        return known_fact(value)
    if unknown_reason is not None:
        return unknown_with_reason(unknown_reason)
    if not_attempted_reason is not None:
        return not_attempted(not_attempted_reason)
    if not_applicable_reason is not None:
        return not_applicable(not_applicable_reason)
    return None


# --- Shared demand-durability series CLI contract (Ob.17 Elements 1, 2 & 4) ----------------
#
# The cadence runner (run_source_capture_durability_series.py) forwards a fixed argv of
# series/cadence/pin flags to whichever per-slot writer it invokes. Every durability-series
# writer (direct_http and the rendered CloakBrowser writer) must therefore expose the SAME
# flag surface so the runner's injectable ``writer_main`` seam can call any of them
# interchangeably. These helpers are the single definition of that surface so the writers
# cannot drift apart. They record observed facts only -- never weights, scores, thresholds,
# rankings, or a durable-vs-hollow verdict (INV-1).


def add_durability_arguments(parser: argparse.ArgumentParser) -> None:
    """Add the optional demand-durability series flags (Ob.17 Elements 1, 2 & 4).

    All flags are optional; when none are supplied the packet's durability fields stay
    ``None`` (a non-durability capture, back-compat preserved). The four pins and the
    cold-start / pre-coverage postures are ``VisibleFact``s built by ``build_optional_fact``
    so an operator can record an honest gap (``unknown_with_reason`` / ``not_applicable``)
    instead of fabricating a value. ``--series-id`` is a plain identifier. The cadence flags
    build ``intended_cadence`` from ``cadence.build_cadence_plan(...).to_dict()`` -- the
    declared (not realized) sampling plan. These are observed facts, never weights or a
    durable-vs-hollow verdict (INV-1).
    """
    group = parser.add_argument_group("demand-durability series (optional)")
    group.add_argument("--series-id", default=None)
    # Element 1 pins (ride on the slice). Each pin accepts one of value / unknown / not-applicable.
    for pin in ("session-visibility-pin", "locale-pin", "currency-pin", "variant-pin"):
        group.add_argument(f"--{pin}", default=None)
        group.add_argument(f"--{pin}-unknown-reason", default=None)
        group.add_argument(f"--{pin}-not-applicable-reason", default=None)
    # Element 2 series-origin postures (ride on the packet).
    group.add_argument("--cold-start-at", default=None)
    group.add_argument("--cold-start-at-unknown-reason", default=None)
    group.add_argument("--cold-start-at-not-applicable-reason", default=None)
    group.add_argument("--pre-coverage-history-posture", default=None)
    group.add_argument("--pre-coverage-history-posture-unknown-reason", default=None)
    group.add_argument("--pre-coverage-history-posture-not-applicable-reason", default=None)
    # Element 4 declared cadence (built via cadence.build_cadence_plan).
    group.add_argument(
        "--intended-cadence-mode", choices=["fixed", "bounded_jitter"], default=None
    )
    group.add_argument("--intended-cadence-slot-count", type=int, default=None)
    group.add_argument("--intended-cadence-delay-seconds", type=float, default=None)
    group.add_argument("--intended-cadence-window-seconds", type=float, default=None)
    group.add_argument("--intended-cadence-min-gap-seconds", type=float, default=None)
    group.add_argument("--intended-cadence-max-gap-seconds", type=float, default=None)
    group.add_argument("--intended-cadence-random-seed", type=int, default=None)


CADENCE_SUBFLAG_ATTRS = (
    "intended_cadence_slot_count",
    "intended_cadence_delay_seconds",
    "intended_cadence_window_seconds",
    "intended_cadence_min_gap_seconds",
    "intended_cadence_max_gap_seconds",
    "intended_cadence_random_seed",
)


def build_intended_cadence(args: argparse.Namespace) -> dict[str, object] | None:
    """Build the declared ``intended_cadence`` dict from cadence flags, or ``None`` if absent.

    Reuses ``cadence.build_cadence_plan`` so the shape is the canonical
    ``CadencePlan.to_dict()`` (no invented shape). ``--intended-cadence-mode`` gates the build:
    without it the field stays ``None`` ONLY when no other cadence subflag is set. A cadence
    subflag supplied without ``--intended-cadence-mode`` is an incoherent partial plan and fails
    visibly (``ValueError`` -> exit 2) rather than being silently dropped. ``build_cadence_plan``
    itself validates slot count and gap/window constraints and raises ``ValueError`` for an
    incoherent plan.
    """
    if args.intended_cadence_mode is None:
        if any(getattr(args, attr) is not None for attr in CADENCE_SUBFLAG_ATTRS):
            raise ValueError(
                "cadence flags require --intended-cadence-mode"
            )
        return None
    if args.intended_cadence_slot_count is None:
        raise ValueError("--intended-cadence-slot-count is required when --intended-cadence-mode is set")
    plan = build_cadence_plan(
        slot_count=args.intended_cadence_slot_count,
        mode=args.intended_cadence_mode,
        delay_seconds=(
            args.intended_cadence_delay_seconds
            if args.intended_cadence_delay_seconds is not None
            else 0.0
        ),
        window_seconds=args.intended_cadence_window_seconds,
        min_gap_seconds=args.intended_cadence_min_gap_seconds,
        max_gap_seconds=args.intended_cadence_max_gap_seconds,
        random_seed=args.intended_cadence_random_seed,
    )
    return plan.to_dict()


# Durability fields that imply a demand-durability series. If any is provided, the capture
# must declare a --series-id so the facts have an identity to ride on (Major 2). Pins remain
# honest gaps when absent (Ob.17); --series-id alone (no pins/cadence) stays a permitted
# degenerate declared series. This gate validates input coherence only -- no weight, score,
# threshold, ranking, or verdict (INV-1).
DURABILITY_FIELD_ATTRS = (
    "session_visibility_pin",
    "session_visibility_pin_unknown_reason",
    "session_visibility_pin_not_applicable_reason",
    "locale_pin",
    "locale_pin_unknown_reason",
    "locale_pin_not_applicable_reason",
    "currency_pin",
    "currency_pin_unknown_reason",
    "currency_pin_not_applicable_reason",
    "variant_pin",
    "variant_pin_unknown_reason",
    "variant_pin_not_applicable_reason",
    "cold_start_at",
    "cold_start_at_unknown_reason",
    "cold_start_at_not_applicable_reason",
    "pre_coverage_history_posture",
    "pre_coverage_history_posture_unknown_reason",
    "pre_coverage_history_posture_not_applicable_reason",
    "intended_cadence_mode",
    "intended_cadence_slot_count",
    "intended_cadence_delay_seconds",
    "intended_cadence_window_seconds",
    "intended_cadence_min_gap_seconds",
    "intended_cadence_max_gap_seconds",
    "intended_cadence_random_seed",
)


def require_series_identity(args: argparse.Namespace) -> None:
    """Fail fast if durability facts are supplied without a --series-id to anchor them.

    A demand-durability fact (pin value/reason, cold-start, pre-coverage posture, or any cadence
    flag) needs a series identity to ride on; without one the fact has nowhere to belong. This
    blocks durability facts with NO identity only -- a bare ``--series-id`` (degenerate declared
    series) and an absent pin (honest gap per Ob.17) both stay permitted. Validates input
    coherence only (INV-1).
    """
    if args.series_id is not None:
        return
    if any(getattr(args, attr) is not None for attr in DURABILITY_FIELD_ATTRS):
        raise ValueError(
            "--series-id is required when any demand-durability field is set"
        )
