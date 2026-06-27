"""Controlled label vocabulary for Tier-1 audience-inference ballots.

The deciding (``scoring/audience_fusion.py``) tallies BY EXACT LABEL, so free-text
labels split the vote ("beginner" / "newbie" / "starter" count as three different
answers and never combine). This module is the canonical allow-list + alias map the
Pass-1 router canonicalizes against before a label becomes a tallied
``EvidenceRecord``.

Pure data + a normalizer; NO LLM -> safe in the no-LLM zone (``schemas/``). The
vocabulary is vertical-scoped (fragrance/beauty v0); other verticals extend it by
adding label sets, leaving the engine (buckets, caps, abstention) untouched.

Positive router (replaces the leaky demographic DENYLIST) -- the four routes a
Pass-1 ballot label can take:

- canonical ``(field, label)`` here  -> Tier-1, allowed into the tally;
- demographic (gender / age)         -> Tier-2-A, routed to ``deferred_signals`` (gated);
- special-category                   -> Tier-3, hard-rejected;
- anything else                      -> ``other_candidate`` review telemetry,
                                        never tallied and never persisted as a
                                        profile label (surfaces candidate vocabulary
                                        for human admission into this allow-list).

The demographic + special-category predicates live with the router in
``cleaning/audience_extractor.py`` (they gate what reaches a record); this module
owns only the Tier-1 vocabulary that survives that gate.

Adoption: docs/decisions/orca_audience_ballot_taxonomy_v0.md.
"""

from __future__ import annotations

import re

from schemas.audience_inference_models import OutputField

# A non-canonical label the model proposed survives only as review telemetry under
# this sentinel -- it is never a tally key and never a persisted profile label.
OTHER_CANDIDATE = "other_candidate"

# Canonical labels per Tier-1 field. The ONLY strings Pass 2 may tally for a field.
CANONICAL_LABELS: dict[OutputField, frozenset[str]] = {
    OutputField.SEGMENT: frozenset(
        {
            "fragrance_discovery",
            "beauty_routine",
            "review_comparison",
            "dupe_affordable_alternatives",
            "scent_education",
        }
    ),
    OutputField.AUDIENCE_ROLE: frozenset(
        {
            "first_time_buyer",
            "routine_builder",
            "collector_enthusiast",
            "gift_shopper",
            "deal_seeker",
        }
    ),
    OutputField.PURCHASE_INTENT: frozenset(
        {
            "browse_inspiration",
            "compare_options",
            "ready_to_buy",
            "post_purchase_use",
            "gift_purchase",
        }
    ),
    OutputField.SKILL_LEVEL: frozenset(
        {"beginner", "intermediate", "advanced", "mixed_general"}
    ),
    OutputField.PRICE_TIER: frozenset(
        {"budget", "midrange", "premium", "luxury", "mixed_price"}
    ),
}

# Synonyms -> canonical, per field. Hand-maintained starter set; an un-aliased
# synonym does not split the vote -- it falls to ``other_candidate`` telemetry until
# admitted here (RESIDUAL: this map is curated, not exhaustive).
ALIASES: dict[OutputField, dict[str, str]] = {
    OutputField.SEGMENT: {
        "discovery": "fragrance_discovery",
        "routine": "beauty_routine",
        "reviews": "review_comparison",
        "comparison": "review_comparison",
        "dupe": "dupe_affordable_alternatives",
        "dupes": "dupe_affordable_alternatives",
        "education": "scent_education",
    },
    OutputField.AUDIENCE_ROLE: {
        "first_timer": "first_time_buyer",
        "beginner_buyer": "first_time_buyer",
        "collector": "collector_enthusiast",
        "gifter": "gift_shopper",
        "gift_giver": "gift_shopper",
        "bargain_hunter": "deal_seeker",
    },
    OutputField.PURCHASE_INTENT: {
        "inspiration": "browse_inspiration",
        "browsing": "browse_inspiration",
        "consideration": "compare_options",
        "conversion": "ready_to_buy",
        "ready": "ready_to_buy",
        "repurchase": "post_purchase_use",
    },
    OutputField.SKILL_LEVEL: {
        "newbie": "beginner",
        "starter": "beginner",
        "just_starting": "beginner",
        "beginners": "beginner",
        "novice": "beginner",
        "expert": "advanced",
        "pro": "advanced",
    },
    OutputField.PRICE_TIER: {
        "affordable": "budget",
        "cheap": "budget",
        "drugstore": "budget",
        "mid_range": "midrange",
        "mid_tier": "midrange",
        "high_end": "premium",
        "designer": "premium",
        "luxe": "luxury",
    },
}


def normalize_label(label: str) -> str:
    """Lower-case, trim, and collapse spaces/hyphens to underscores for matching."""
    return re.sub(r"[\s\-]+", "_", label.strip().lower()).strip("_")


def canonicalize(field: OutputField, label: str) -> str | None:
    """Return the canonical label for ``(field, label)``, or ``None`` if it is not in
    the field's allow-list or alias map (caller routes a ``None`` to ``other_candidate``)."""
    norm = normalize_label(label)
    if not norm:
        return None
    if norm in CANONICAL_LABELS[field]:
        return norm
    return ALIASES.get(field, {}).get(norm)
