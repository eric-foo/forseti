"""Controlled label vocabulary: canonicalization, alias mapping, allow-list invariants.

Pure data + a normalizer; no LLM, no network. Guards the property the deciding relies
on: a label that reaches a tally is a single canonical key, and the alias map can never
reintroduce vote-splitting.
"""

from __future__ import annotations

from schemas.audience_inference_models import OutputField
from schemas.audience_label_ontology import (
    ALIASES,
    CANONICAL_LABELS,
    OTHER_CANDIDATE,
    canonicalize,
    normalize_label,
)


def test_every_output_field_has_a_nonempty_canonical_set() -> None:
    assert set(CANONICAL_LABELS) == set(OutputField)
    assert all(CANONICAL_LABELS[f] for f in OutputField)


def test_canonical_label_passes_through() -> None:
    assert canonicalize(OutputField.SKILL_LEVEL, "beginner") == "beginner"
    assert canonicalize(OutputField.PRICE_TIER, "luxury") == "luxury"


def test_alias_maps_to_canonical() -> None:
    assert canonicalize(OutputField.SKILL_LEVEL, "newbie") == "beginner"
    assert canonicalize(OutputField.PURCHASE_INTENT, "conversion") == "ready_to_buy"
    assert canonicalize(OutputField.PRICE_TIER, "affordable") == "budget"


def test_normalization_is_case_and_separator_insensitive() -> None:
    assert canonicalize(OutputField.SKILL_LEVEL, " Just Starting ") == "beginner"
    assert canonicalize(OutputField.PRICE_TIER, "High-End") == "premium"
    assert normalize_label("  Mid-Range ") == "mid_range"


def test_unknown_or_empty_label_returns_none() -> None:
    assert canonicalize(OutputField.SEGMENT, "totally_made_up") is None
    assert canonicalize(OutputField.SEGMENT, "") is None
    assert canonicalize(OutputField.SEGMENT, "   ") is None


def test_alias_targets_are_all_canonical() -> None:
    # No alias may point at a non-canonical label -- that would reintroduce a second
    # tally key and re-split the vote the alias map exists to merge.
    for field, amap in ALIASES.items():
        for source, target in amap.items():
            assert target in CANONICAL_LABELS[field], (field, source, target)


def test_aliases_do_not_shadow_canonical_labels() -> None:
    # An alias key must not also be a canonical label for that field (ambiguous routing).
    for field, amap in ALIASES.items():
        assert not (set(amap) & CANONICAL_LABELS[field]), field


def test_other_candidate_sentinel_is_never_a_canonical_label() -> None:
    assert all(OTHER_CANDIDATE not in CANONICAL_LABELS[f] for f in OutputField)
