"""Pass 2 of transcript product extraction: deterministic, LLM-free verdict fusion.

Consumes Pass-1 ``ProductMention``s for ONE creator and produces a ``ProductVerdictSet``:
one ``ProductVerdict`` per ``(brand, line)``. LLM-free by construction (it lives in the
no-LLM zone, ``scoring/``): Pass 1 READS and LABELS; this code DECIDES and COMBINES, so the
audit invariants are enforced deterministically rather than left to a model. Re-runnable for
free over cached mentions; source-agnostic (serves YouTube + IG).

Carries NO engagement/resonance signal: ``ProductMention`` has none, and engagement
interpretation is the Judgment-owned Engagement Logic Registry's domain
(``forseti/product/shared/engagement_registry/engagement_logic_registry_v0.md``) — whose
weighting method is owner-deferred. This fusion answers only "what did the creator say about
this product," never demand / credibility / independence / Action Ceiling.

Spec: youtube_transcript_product_extraction_spec_v0.md (Pass 2 / CE4) +
ig_reels_transcript_product_extraction_spec_v0.md (reuse).
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import asdict, dataclass
from math import sqrt, tanh

from harness_utils import utc_now_z
from schemas.product_mention_models import (
    ProductMention,
    ProductVerdict,
    ProductVerdictSet,
    Verdict,
)

FUSION_CONFIG_VERSION = "0.1"


@dataclass(frozen=True)
class FusionConfig:
    """The full tunable surface of Pass-2 product-verdict fusion -- one knob per field.

    These six values ARE the calibration surface. ``DEFAULT_FUSION_CONFIG`` holds the
    UNCALIBRATED v0 defaults: they were chosen by mirroring ``scoring/audience_fusion.py``,
    NOT fit to owner-labeled verdicts, so they encode a principled prior, not a measured one.
    The sensitivity harness (``scoring/product_fusion_sensitivity.py``) sweeps them; real
    calibration (a labeled corpus + owner sign-off) is owner-deferred. Rationale and the
    current defaults' consequences:
    ``docs/decisions/product_verdict_fusion_calibration_surface_v0.md``.

    Frozen so a verdict run cannot mutate the config mid-fusion; the harness builds perturbed
    copies with ``dataclasses.replace`` instead.
    """

    # Squash gain in ``side_score = tanh(gain * raw)``. Higher saturates toward 1.0 faster,
    # so beyond the first strong mention extra corroboration barely moves the score -- the
    # squashed score is near-binary, not an "endorsement intensity" signal.
    gain: float = 2.0
    # Materiality / abstain line: a side (support or oppose) counts toward the verdict only
    # when its squashed strength >= this. THE risk dial -- raise it for more 'unknown'
    # abstentions and fewer but more-confident calls; lower it for the opposite.
    material_min: float = 0.40
    # CE4 precedence: an explicit creator-authored (or creator-rated) stance carries full
    # weight; an implicit / inferred stance is discounted to ``implicit_mult``.
    creator_authored_mult: float = 1.0
    implicit_mult: float = 0.6
    # Discount when the extractor flags possible negation / irony. At 0.3 with gain 2.0 this
    # alone does NOT pull a max-stance/-confidence mention below ``material_min`` -- irony
    # abstention also relies on the extractor lowering ``stance_vote`` (see the memo).
    negation_mult: float = 0.3
    # Soft within-video dependence-discount exponent: a mention sharing its video with N
    # same-product mentions is weighted by ``N ** -exponent`` (0.5 == the original 1/sqrt(N)).
    dependence_exponent: float = 0.5

    def stance_multiplier(self, *, authored: bool, negated: bool) -> float:
        """Per-mention weight from authored-vs-implicit precedence and the irony discount."""
        mult = self.creator_authored_mult if authored else self.implicit_mult
        if negated:
            mult *= self.negation_mult
        return mult

    def dependence_factor(self, cluster_count: int) -> float:
        """Soft 1/sqrt(N)-style discount for same-video repeats; 1.0 for a lone mention."""
        if cluster_count <= 1:
            return 1.0
        if self.dependence_exponent == 0.5:
            # Preserve the exact original ``1.0 / sqrt(N)`` expression for the default.
            return 1.0 / sqrt(cluster_count)
        return cluster_count ** (-self.dependence_exponent)

    def material_strength(self, raw: float) -> float:
        """Squashed one-sided strength in [0, 1] (materiality test + stored score)."""
        return max(0.0, tanh(self.gain * raw))


DEFAULT_FUSION_CONFIG = FusionConfig()


def _brand_line_key(mention: ProductMention) -> tuple[str, str]:
    """Normalized grouping key so casing/whitespace variants are one product."""
    return (mention.brand.strip().lower(), mention.line.strip().lower())


def _fuse_product(
    brand: str,
    line: str,
    items: list[ProductMention],
    *,
    config: FusionConfig = DEFAULT_FUSION_CONFIG,
) -> ProductVerdict:
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
        mult = config.stance_multiplier(
            authored=authored, negated=mention.possible_negation_or_irony
        )
        dep = config.dependence_factor(per_video[mention.video_id])
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
    support = round(config.material_strength(support_raw), 4)
    oppose = round(config.material_strength(oppose_raw), 4)
    support_material = support >= config.material_min
    oppose_material = oppose >= config.material_min

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
    config: FusionConfig = DEFAULT_FUSION_CONFIG,
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
        verdict = _fuse_product(brand, line, by_product[key], config=config)
        verdicts.append(verdict)
        if verdict.verdict == Verdict.UNKNOWN:
            abstentions.append(f"{brand}:{line}")

    provenance = {"fusion_config_version": fusion_config_version}
    if config != DEFAULT_FUSION_CONFIG:
        # Default-path provenance is unchanged (behaviour-preserving). A NON-default config would
        # otherwise be mislabelled by fusion_config_version alone, so record the actual constants
        # so a non-default run stays re-derivable rather than silently misreported.
        provenance["fusion_config"] = asdict(config)
    return ProductVerdictSet(
        creator_id=creator_id,
        verdicts=verdicts,
        abstentions=sorted(abstentions),
        fusion_config_version=fusion_config_version,
        generated_at=generated_at or utc_now_z(),
        provenance=provenance,
    )
