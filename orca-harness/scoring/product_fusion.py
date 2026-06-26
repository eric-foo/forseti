"""Pass 2 of transcript product extraction: deterministic, LLM-free verdict fusion.

Consumes Pass-1 ``ProductMention``s for ONE creator and produces a ``ProductVerdictSet``:
one ``ProductVerdict`` per ``(brand, line)``. LLM-free by construction (it lives in the
no-LLM zone, ``scoring/``): Pass 1 READS and LABELS; this code DECIDES and COMBINES, so the
audit invariants are enforced deterministically rather than left to a model. Re-runnable for
free over cached mentions; source-agnostic (serves YouTube + IG).

Carries NO engagement/resonance signal: ``ProductMention`` has none, and engagement
interpretation is the Judgment-owned Engagement Logic Registry's domain
(``orca/product/shared/engagement_registry/engagement_logic_registry_v0.md``) — whose
weighting method is owner-deferred. This fusion answers only "what did the creator say about
this product," never demand / credibility / independence / Action Ceiling.

Spec: youtube_transcript_product_extraction_spec_v0.md (Pass 2 / CE4) +
ig_reels_transcript_product_extraction_spec_v0.md (reuse).
"""
from __future__ import annotations

from collections import defaultdict
from math import sqrt, tanh

from harness_utils import utc_now_z
from schemas.product_mention_models import (
    ProductMention,
    ProductVerdict,
    ProductVerdictSet,
    Verdict,
)

FUSION_CONFIG_VERSION = "0.1"

_GAIN = 2.0  # squash gain: score = tanh(_GAIN * raw)
_MATERIAL_MIN = 0.40  # a side (support / oppose) counts only when its squashed strength >= this
# CE4 precedence: creator-authored / explicitly-rated stance outweighs implicit.
_CREATOR_AUTHORED_MULT = 1.0
_IMPLICIT_MULT = 0.6
_NEGATION_MULT = 0.3  # discount possible negation / irony


def _brand_line_key(mention: ProductMention) -> tuple[str, str]:
    """Normalized grouping key so casing/whitespace variants are one product."""
    return (mention.brand.strip().lower(), mention.line.strip().lower())


def _material(raw: float) -> float:
    """Squashed one-sided strength in [0, 1]."""
    return max(0.0, tanh(_GAIN * raw))


def _fuse_product(brand: str, line: str, items: list[ProductMention]) -> ProductVerdict:
    """Fuse one product's mentions into a verdict. Support and opposition accumulate
    separately, so a genuinely divided product lands on ``mixed`` rather than netting to
    ``unknown``."""
    # Dependence discount (SOFT): repeats within ONE video are down-weighted by 1/sqrt(N) per
    # mention (cluster = video_id), mirroring audience_fusion. It is a graceful discount toward
    # "one creative", NOT a hard one-video-one-vote cap -- several strong in-video mentions still
    # accumulate (see test_dependence_discount_one_video_not_n_endorsements).
    per_video: dict[str, int] = defaultdict(int)
    for mention in items:
        per_video[mention.video_id] += 1

    support_raw = 0.0
    oppose_raw = 0.0
    support_ids: list[str] = []
    oppose_ids: list[str] = []

    for mention in items:
        # A creator-stated rating ("8/10") is a witnessed, explicit evaluation: it carries
        # creator-authored weight. But the extractor's irony flag is STILL honored — a flagged
        # rating is not assumed sincere (a sarcastic "10/10" must not flip to a confident
        # positive). Magnitude comes from stance_vote (the extractor sets it consistent with the
        # rating). Calibration deferred.
        witnessed = mention.stated_rating is not None
        authored = mention.creator_authored or witnessed
        mult = _CREATOR_AUTHORED_MULT if authored else _IMPLICIT_MULT
        if mention.possible_negation_or_irony:
            mult *= _NEGATION_MULT
        dep = 1.0 / sqrt(per_video[mention.video_id])
        contribution = mention.stance_vote * mention.extractor_confidence * mult * dep
        if contribution > 0:
            support_raw += contribution
            support_ids.append(mention.mention_id)
        elif contribution < 0:
            oppose_raw += abs(contribution)
            oppose_ids.append(mention.mention_id)
        # contribution == 0 (neutral / zero-confidence): counted in mention_count only.

    # Round once and use the SAME value for the materiality test and the stored score, so a
    # reported score can never contradict the verdict at the boundary (e.g. stored 0.4 + unknown).
    support = round(_material(support_raw), 4)
    oppose = round(_material(oppose_raw), 4)
    support_material = support >= _MATERIAL_MIN
    oppose_material = oppose >= _MATERIAL_MIN

    if support_material and oppose_material:
        verdict = Verdict.MIXED
    elif support_material:
        verdict = Verdict.POSITIVE
    elif oppose_material:
        verdict = Verdict.NEGATIVE
    else:
        verdict = Verdict.UNKNOWN

    return ProductVerdict(
        brand=brand,
        line=line,
        verdict=verdict,
        mention_count=len(items),
        evidence_ids=sorted(support_ids),
        counterevidence_ids=sorted(oppose_ids),
        uncalibrated_support_score=support,
        uncalibrated_oppose_score=oppose,
    )


def fuse_product_verdicts(
    mentions: list[ProductMention],
    *,
    creator_id: str,
    fusion_config_version: str = FUSION_CONFIG_VERSION,
    generated_at: str | None = None,
) -> ProductVerdictSet:
    """Fuse ONE creator's ``ProductMention``s into per-``(brand, line)`` ``ProductVerdict``s.

    Deterministic and LLM-free. Verdicts and their cited mention ids are sorted for a stable,
    re-derivable result.

    PRECONDITION (caller-enforced): every mention in ``mentions`` MUST belong to the one creator
    named by ``creator_id``. ``ProductMention`` carries no creator field, so -- unlike
    ``audience_fusion`` (which rejects multi-creator input) -- this function CANNOT detect and
    will SILENTLY fuse across creators if a caller batches them. The durable guard (a
    ``creator_id`` on ``ProductMention``, asserted here like audience_fusion) is part of the
    deferred cross-creator work; until it lands, the caller owns single-creator scoping.
    """
    if not creator_id or not creator_id.strip():
        raise ValueError("fuse_product_verdicts requires a non-empty creator_id")

    by_product: dict[tuple[str, str], list[ProductMention]] = defaultdict(list)
    display: dict[tuple[str, str], tuple[str, str]] = {}
    for mention in mentions:
        key = _brand_line_key(mention)
        by_product[key].append(mention)
        display.setdefault(key, (mention.brand, mention.line))  # first-seen original casing

    verdicts: list[ProductVerdict] = []
    abstentions: list[str] = []
    for key in sorted(by_product):
        brand, line = display[key]
        verdict = _fuse_product(brand, line, by_product[key])
        verdicts.append(verdict)
        if verdict.verdict == Verdict.UNKNOWN:
            abstentions.append(f"{brand}:{line}")

    return ProductVerdictSet(
        creator_id=creator_id,
        verdicts=verdicts,
        abstentions=sorted(abstentions),
        fusion_config_version=fusion_config_version,
        generated_at=generated_at or utc_now_z(),
        provenance={"fusion_config_version": fusion_config_version},
    )
