from __future__ import annotations

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
