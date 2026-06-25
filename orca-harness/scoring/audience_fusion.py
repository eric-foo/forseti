"""Pass 2 of IG ideal-audience inference: deterministic, LLM-free fusion.

Consumes Pass-1 EvidenceRecords for ONE creator and produces an
IdealAudienceProfile over the Tier-1 fields. This module is intentionally
LLM-free (it lives in the no-LLM zone, `scoring/`): the LLM only ever READS and
LABELS in Pass 1; code DECIDES and COMBINES here, so the bias-control and
audit invariants (CE1-CE12) are enforced deterministically rather than left to a
model. Re-runnable for free over cached evidence.

Spec: ig_creator_ideal_audience_inference_spec_v0.md.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from math import sqrt, tanh

from harness_utils import utc_now_z
from schemas.audience_inference_models import (
    UNKNOWN_LABEL,
    EvidenceRecord,
    FieldResult,
    IdealAudienceProfile,
    ModalityFamily,
    OutputField,
    PillarProfile,
    SupportBand,
)

FUSION_CONFIG_VERSION = "0.1"

# CE5: per-field caps on the max |net contribution| any one modality family may
# add to a field. CE3 lives here too: comment is tiny everywhere and 0 for price.
_MODALITY_CAPS: dict[OutputField, dict[ModalityFamily, float]] = {
    OutputField.SEGMENT: {
        ModalityFamily.TEXT: 0.25,
        ModalityFamily.COMMERCIAL: 0.20,
        ModalityFamily.STRUCTURAL: 0.20,
        ModalityFamily.COMMENT: 0.05,
    },
    OutputField.AUDIENCE_ROLE: {
        ModalityFamily.TEXT: 0.35,
        ModalityFamily.COMMERCIAL: 0.20,
        ModalityFamily.STRUCTURAL: 0.20,
        ModalityFamily.COMMENT: 0.05,
    },
    OutputField.PURCHASE_INTENT: {
        ModalityFamily.TEXT: 0.20,
        ModalityFamily.COMMERCIAL: 0.50,
        ModalityFamily.STRUCTURAL: 0.15,
        ModalityFamily.COMMENT: 0.05,
    },
    OutputField.SKILL_LEVEL: {
        ModalityFamily.TEXT: 0.55,
        ModalityFamily.COMMERCIAL: 0.15,
        ModalityFamily.STRUCTURAL: 0.20,
        ModalityFamily.COMMENT: 0.05,
    },
    OutputField.PRICE_TIER: {
        ModalityFamily.TEXT: 0.10,
        ModalityFamily.COMMERCIAL: 0.65,
        ModalityFamily.STRUCTURAL: 0.15,
        ModalityFamily.COMMENT: 0.00,
    },
    # Aesthetic/vibe is stated in the creator's own words (caption/bio), with
    # hashtags as a secondary structural signal -> text-dominant, like skill_level.
    OutputField.AESTHETIC_VIBE: {
        ModalityFamily.TEXT: 0.55,
        ModalityFamily.COMMERCIAL: 0.15,
        ModalityFamily.STRUCTURAL: 0.20,
        ModalityFamily.COMMENT: 0.05,
    },
}

_GAIN = 2.0  # squash gain: score = tanh(_GAIN * raw)
_MARGIN_MIN = 0.10  # CE6: abstain when the top-two score margin is below this
_BAND_HIGH = 0.80  # CE7 band thresholds
_BAND_MEDIUM = 0.60
_BAND_LOW = 0.40
# CE4 precedence: creator-authored text outweighs implicit signals.
_CREATOR_AUTHORED_MULT = 1.0
_IMPLICIT_MULT = 0.6
_NEGATION_MULT = 0.3  # discount possible negation/irony
_UNLABELED_PILLAR_LABEL = "unlabeled"


class MultipleCreatorsError(ValueError):
    """Fusion is per-creator; evidence must reference exactly one creator_id."""


def _band(score: float) -> SupportBand:
    if score >= _BAND_HIGH:
        return SupportBand.HIGH
    if score >= _BAND_MEDIUM:
        return SupportBand.MEDIUM
    if score >= _BAND_LOW:
        return SupportBand.LOW
    return SupportBand.ABSTAIN


def _abstain(field: OutputField, score: float) -> FieldResult:
    return FieldResult(
        field=field,
        label=UNKNOWN_LABEL,
        support_band=SupportBand.ABSTAIN,
        uncalibrated_support_score=round(max(score, 0.0), 4),
    )


def _pillar_key(evidence: EvidenceRecord) -> tuple[str, str | None]:
    pillar_label = evidence.pillar_label
    if pillar_label is not None:
        pillar_label = pillar_label.strip() or None
    return (evidence.platform, pillar_label)


def _pillar_display_label(pillar_key: tuple[str, str | None]) -> str:
    platform, pillar_label = pillar_key
    return f"{platform}:{pillar_label or _UNLABELED_PILLAR_LABEL}"


def _fuse_field(field: OutputField, items: list[EvidenceRecord]) -> FieldResult:
    if not items:
        return _abstain(field, 0.0)

    caps = _MODALITY_CAPS[field]
    cluster_counts = Counter(e.creative_cluster_id for e in items if e.creative_cluster_id)

    # label -> modality -> positive/negative contribution. Cap support and
    # opposition separately so volume cannot hide high contradiction by netting first.
    fam_support: dict[str, dict[ModalityFamily, float]] = defaultdict(
        lambda: defaultdict(float)
    )
    fam_oppose: dict[str, dict[ModalityFamily, float]] = defaultdict(
        lambda: defaultdict(float)
    )
    support_ids: dict[str, list[str]] = defaultdict(list)
    oppose_ids: dict[str, list[str]] = defaultdict(list)
    creator_authored_text_labels: set[str] = set()

    for e in items:
        mult = _CREATOR_AUTHORED_MULT if e.creator_authored else _IMPLICIT_MULT
        if e.possible_negation_or_irony:
            mult *= _NEGATION_MULT
        # Dependence discount: one creative repeated is not independent evidence.
        dep = 1.0
        if e.creative_cluster_id and cluster_counts[e.creative_cluster_id] > 1:
            dep = 1.0 / sqrt(cluster_counts[e.creative_cluster_id])
        c = e.vote * e.base_reliability * e.extractor_confidence * mult * dep
        cap = caps.get(e.modality, 0.0)
        if cap <= 0.0 or c == 0.0:
            continue
        if c > 0:
            fam_support[e.label][e.modality] += c
            support_ids[e.label].append(e.evidence_id)
            if e.creator_authored and e.modality == ModalityFamily.TEXT:
                creator_authored_text_labels.add(e.label)
        else:
            fam_oppose[e.label][e.modality] += abs(c)
            oppose_ids[e.label].append(e.evidence_id)

    # Apply per-family caps (CE3/CE5), then sum to a per-label raw score.
    raw_by_label: dict[str, float] = {}
    labels = set(fam_support) | set(fam_oppose)
    for label in labels:
        raw = 0.0
        modalities = set(fam_support[label]) | set(fam_oppose[label])
        for fam in modalities:
            cap = caps.get(fam, 0.0)
            raw += min(cap, fam_support[label].get(fam, 0.0))
            raw -= min(cap, fam_oppose[label].get(fam, 0.0))
        raw_by_label[label] = raw

    if not raw_by_label:
        return _abstain(field, 0.0)

    creator_rank_labels = {
        label
        for label in creator_authored_text_labels
        if _band(max(0.0, tanh(_GAIN * raw_by_label.get(label, 0.0))))
        != SupportBand.ABSTAIN
    }

    ranked = sorted(
        raw_by_label.items(),
        key=lambda kv: (
            kv[0] in creator_rank_labels,
            max(0.0, tanh(_GAIN * kv[1])),
            kv[1],
            kv[0],
        ),
        reverse=True,
    )
    top_label, top_raw = ranked[0]
    top_score = max(0.0, tanh(_GAIN * top_raw))
    top_creator_ranked = top_label in creator_rank_labels
    second_score = 0.0
    for label, raw in ranked[1:]:
        if (label in creator_rank_labels) == top_creator_ranked:
            second_score = max(0.0, tanh(_GAIN * raw))
            break
    margin = top_score - second_score

    band = _band(top_score)
    # CE6: abstain on weak band, contested margin, or non-positive support.
    if band == SupportBand.ABSTAIN or margin < _MARGIN_MIN or top_raw <= 0:
        return _abstain(field, top_score)

    return FieldResult(
        field=field,
        label=top_label,
        support_band=band,
        uncalibrated_support_score=round(top_score, 4),
        evidence_ids=sorted(support_ids[top_label]),
        counterevidence_ids=sorted(oppose_ids[top_label]),
    )


def fuse_profile(
    evidence: list[EvidenceRecord],
    *,
    fusion_config_version: str = FUSION_CONFIG_VERSION,
    generated_at: str | None = None,
) -> IdealAudienceProfile:
    """Fuse one creator's evidence into a Tier-1 IdealAudienceProfile.

    Pillars are kept separate (CE8); each Tier-1 field is fused independently with
    modality caps (CE3/CE5), creator-authored precedence (CE4), dependence
    discounting, and abstention (CE6). actual_audience is always not_estimated (CE10).
    """
    if not evidence:
        raise ValueError("fuse_profile requires at least one EvidenceRecord")

    creator_ids = {e.creator_id for e in evidence}
    if len(creator_ids) != 1:
        raise MultipleCreatorsError(f"expected one creator_id, got {sorted(creator_ids)}")
    creator_id = next(iter(creator_ids))

    by_pillar: dict[tuple[str, str | None], list[EvidenceRecord]] = defaultdict(list)
    for e in evidence:
        by_pillar[_pillar_key(e)].append(e)

    total = len(evidence)
    pillars: list[PillarProfile] = []
    abstentions: list[str] = []

    for idx, pillar_key in enumerate(sorted(by_pillar, key=lambda key: (key[0], key[1] or ""))):
        items = by_pillar[pillar_key]
        pillar_label = _pillar_display_label(pillar_key)
        field_results: list[FieldResult] = []
        for field in OutputField:
            fr = _fuse_field(field, [e for e in items if e.target_field == field])
            field_results.append(fr)
            if fr.support_band == SupportBand.ABSTAIN:
                abstentions.append(f"{pillar_label}:{field.value}")
        pillars.append(
            PillarProfile(
                pillar_id=f"pillar_{idx:02d}",
                pillar_label=pillar_label,
                positioning_share=round(len(items) / total, 4),
                field_results=field_results,
            )
        )

    return IdealAudienceProfile(
        creator_id=creator_id,
        ideal_audience_profiles=pillars,
        abstentions=sorted(abstentions),
        fusion_config_version=fusion_config_version,
        generated_at=generated_at or utc_now_z(),
        provenance={"fusion_config_version": fusion_config_version},
    )
