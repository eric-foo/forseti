"""Pass 2 of the IG creator-gender demographic signal: deterministic, LLM-free fusion.

Consumes per-reel `CreatorGenderSignal` cues for ONE creator and produces a single soft
`CreatorGenderLean`. LLM-free by construction (no-LLM zone, `scoring/`): the inference that
populates the per-reel cues is the DEFERRED agent-in-the-loop cleaning step; this code only
DECIDES/COMBINES deterministically. Sibling to `audience_fusion` / `product_fusion` — it is NOT
folded into product-stance.

Cues are weighted by kind (see `GenderCueKind`): self-presentation is trusted and circularity-
free; product-marketed-gender is EXCLUDED from decisive fusion in this slice because it risks
circularity with the downstream gender x product-stance cut (a single confident product cue at a
low-but-nonzero weight could otherwise clear the floor and decide a lean by itself). The lean is
signed and SOFT, abstaining below a confidence floor; never a hard label.

UNCALIBRATED v0: the constants below are OWN constants, deliberately NOT the shared
audience/product prior (the gender-lean distribution differs; an independent calibration is a
recorded decision, not copy-paste). Real calibration is owner/corpus-gated and deferred.

Scope: docs/decisions/ig_creator_gender_demographic_signal_lane_scope_defer_v0.md.
"""

from __future__ import annotations

from math import tanh

from harness_utils import utc_now_z
from schemas.creator_gender_models import (
    CREATOR_GENDER_DECISIVE_CONFIDENCE_FLOOR,
    CreatorGenderLean,
    CreatorGenderSignal,
    GenderCueKind,
)

FUSION_CONFIG_VERSION = "0.1"

# UNCALIBRATED v0 — OWN constants (independent of the shared audience/product prior).
_GAIN = 2.0  # tanh squash speed on the accumulated signed lean.
_CONFIDENCE_FLOOR = CREATOR_GENDER_DECISIVE_CONFIDENCE_FLOOR
# Per-cue weights: self-presentation trusted; product-marketed-gender is input-auditable but
# NON-DECISIVE (0.0) until a non-circular, owner-approved use exists — at any nonzero weight a
# confident product cue can clear the floor alone, which is the circularity we are avoiding.
_CUE_WEIGHTS: dict[GenderCueKind, float] = {
    GenderCueKind.SELF_PRESENTATION: 1.0,
    GenderCueKind.PRODUCT_MARKETED_GENDER: 0.0,
}


class MultipleCreatorsError(ValueError):
    """Fusion is per-creator; every signal must reference exactly one creator_id."""


def fuse_creator_gender(
    signals: list[CreatorGenderSignal],
    *,
    creator_id: str,
    fusion_config_version: str = FUSION_CONFIG_VERSION,
    generated_at: str | None = None,
) -> CreatorGenderLean:
    """Fuse one creator's per-reel gender cues into a single soft lean.

    Each cue contributes ``gender_lean * confidence * cue_weight``; contributions accumulate, the
    signed total is squashed with tanh, and the result ABSTAINS (lean reported 0.0) when the
    squashed strength is below the confidence floor, when cues net out (genuinely contested), or
    when there is no usable signal. Cue kinds with weight 0 (currently product-marketed-gender)
    contribute nothing and are not cited. Deterministic and re-runnable; evidence_ids are sorted.

    PRECONDITION: every signal must belong to ``creator_id`` (``CreatorGenderSignal`` carries
    ``creator_id``, so it is asserted here, unlike ``product_fusion``'s caller-only contract).
    """
    if not creator_id or not creator_id.strip():
        raise ValueError("fuse_creator_gender requires a non-empty creator_id")

    foreign = sorted({s.creator_id for s in signals if s.creator_id != creator_id})
    if foreign:
        raise MultipleCreatorsError(
            f"signals must all belong to {creator_id!r}; got foreign creator_ids {foreign}"
        )

    raw = 0.0
    evidence_ids: list[str] = []
    for s in signals:
        weight = _CUE_WEIGHTS.get(s.cue_kind, 0.0)
        contribution = s.gender_lean * s.confidence * weight
        if weight <= 0.0 or contribution == 0.0:
            continue  # zero-weight cue kind or neutral/zero-confidence cue: not evidence
        raw += contribution
        evidence_ids.append(s.signal_id)

    contributed = bool(evidence_ids)
    squashed = tanh(_GAIN * raw) if contributed else 0.0
    strength = round(abs(squashed), 4)
    lean = round(squashed, 4)
    abstained = strength < _CONFIDENCE_FLOOR
    if abstained:
        lean = 0.0  # report neutral; `strength` is retained as the sub-floor confidence for audit

    return CreatorGenderLean(
        creator_id=creator_id,
        gender_lean=lean,
        confidence=strength,
        abstained=abstained,
        evidence_ids=sorted(evidence_ids),
        fusion_config_version=fusion_config_version,
        generated_at=generated_at or utc_now_z(),
        provenance={"fusion_config_version": fusion_config_version},
    )
