"""Tier-1 ideal-audience fusion: CE-invariant + counterfactual tests (Slice A).

Verifies the code-enforced invariants (CE3-CE12) the spec requires fusion to
guarantee, plus the three cheap counterfactual smoke tests from the route.
All synthetic evidence; no LLM, no network.
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from schemas.audience_inference_models import (
    UNKNOWN_LABEL,
    EvidenceRecord,
    FieldResult,
    IdealAudienceProfile,
    ModalityFamily,
    OutputField,
    SupportBand,
)
from scoring.audience_fusion import MultipleCreatorsError, fuse_profile


def _ev(
    evidence_id: str = "E1",
    *,
    field: OutputField = OutputField.SEGMENT,
    modality: ModalityFamily = ModalityFamily.TEXT,
    label: str = "aspirational_beauty",
    vote: float = 1.0,
    base: float = 1.0,
    conf: float = 1.0,
    authored: bool = True,
    negation: bool = False,
    cluster: str | None = None,
    pillar: str | None = None,
    creator: str = "c1",
    platform: str = "instagram",
    post: str = "p1",
    source: str = "caption:p1:span",
) -> EvidenceRecord:
    return EvidenceRecord(
        evidence_id=evidence_id,
        creator_id=creator,
        platform=platform,
        post_id=post,
        pillar_label=pillar,
        signal_id="T1",
        modality=modality,
        target_field=field,
        label=label,
        vote=vote,
        base_reliability=base,
        extractor_confidence=conf,
        creator_authored=authored,
        possible_negation_or_irony=negation,
        creative_cluster_id=cluster,
        source_pointer=source,
    )


def _field(profile: IdealAudienceProfile, field: OutputField, pillar_idx: int = 0):
    pillar = profile.ideal_audience_profiles[pillar_idx]
    return next(fr for fr in pillar.field_results if fr.field == field)


# --- CE10: actual_audience is never estimated ------------------------------


def test_actual_audience_always_not_estimated() -> None:
    profile = fuse_profile([_ev()], generated_at="2026-06-23T00:00:00Z")
    assert profile.actual_audience == "not_estimated"


def test_schema_rejects_actual_audience_claim() -> None:
    with pytest.raises(ValidationError):
        IdealAudienceProfile(
            creator_id="c1",
            actual_audience="estimated",  # type: ignore[arg-type]
            fusion_config_version="0.1",
            generated_at="2026-06-23T00:00:00Z",
        )


def test_schema_rejects_actual_audience_copy_and_assignment() -> None:
    profile = IdealAudienceProfile(
        creator_id="c1",
        fusion_config_version="0.1",
        generated_at="2026-06-23T00:00:00Z",
    )
    with pytest.raises(ValidationError):
        profile.model_copy(update={"actual_audience": "estimated"})
    with pytest.raises(ValidationError):
        profile.actual_audience = "estimated"  # type: ignore[assignment]


# --- CE9: every evidence item must carry a source pointer ------------------


@pytest.mark.parametrize("bad", ["", "   "])
def test_ce9_source_pointer_required(bad: str) -> None:
    with pytest.raises(ValidationError):
        _ev(source=bad)


def test_ce9_source_pointer_required_on_construct_and_copy() -> None:
    with pytest.raises(ValidationError):
        EvidenceRecord.model_construct(
            evidence_id="E1",
            creator_id="c1",
            platform="instagram",
            post_id="p1",
            signal_id="T1",
            modality=ModalityFamily.TEXT,
            target_field=OutputField.SEGMENT,
            label="aspirational_beauty",
            vote=1.0,
            base_reliability=1.0,
            extractor_confidence=1.0,
            creator_authored=True,
            source_pointer="",
        )
    with pytest.raises(ValidationError):
        _ev().model_copy(update={"source_pointer": ""})


# --- CE6: abstention on thin or contested evidence -------------------------


def test_ce6_thin_evidence_abstains() -> None:
    profile = fuse_profile([_ev(base=0.5, conf=0.3)], generated_at="t")
    seg = _field(profile, OutputField.SEGMENT)
    assert seg.support_band == SupportBand.ABSTAIN
    assert seg.label == UNKNOWN_LABEL
    assert "instagram:unlabeled:segment" in profile.abstentions


def test_ce6_contested_margin_abstains() -> None:
    evidence = [
        _ev("EX", label="luxury_buyer", vote=1.0),
        _ev("EY", label="value_seeker", vote=1.0),
    ]
    profile = fuse_profile(evidence, generated_at="t")
    seg = _field(profile, OutputField.SEGMENT)
    assert seg.support_band == SupportBand.ABSTAIN
    assert seg.label == UNKNOWN_LABEL


def test_ce6_same_modality_contradiction_abstains() -> None:
    evidence = [
        *[
            _ev(
                f"P{i}",
                field=OutputField.SKILL_LEVEL,
                label="beginner",
                vote=1.0,
            )
            for i in range(10)
        ],
        *[
            _ev(
                f"N{i}",
                field=OutputField.SKILL_LEVEL,
                label="beginner",
                vote=-1.0,
            )
            for i in range(9)
        ],
    ]
    profile = fuse_profile(evidence, generated_at="t")
    skill = _field(profile, OutputField.SKILL_LEVEL)
    assert skill.support_band == SupportBand.ABSTAIN
    assert skill.label == UNKNOWN_LABEL


# --- CE8: divergent pillars are not merged ---------------------------------


def test_ce8_pillars_not_merged() -> None:
    evidence = [
        _ev("EB", label="aspirational_beauty", pillar="consumer_beauty"),
        _ev("EP", label="professional_stylist", pillar="pro_education"),
    ]
    profile = fuse_profile(evidence, generated_at="t")
    assert len(profile.ideal_audience_profiles) == 2
    labels = {_field(profile, OutputField.SEGMENT, i).label for i in range(2)}
    assert labels == {"aspirational_beauty", "professional_stylist"}


def test_ce8_unlabeled_and_literal_default_are_not_collided() -> None:
    evidence = [
        _ev("EU", label="unlabeled_audience", pillar=None),
        _ev("ED", label="default_named_audience", pillar="default"),
    ]
    profile = fuse_profile(evidence, generated_at="t")
    assert [p.pillar_label for p in profile.ideal_audience_profiles] == [
        "instagram:unlabeled",
        "instagram:default",
    ]
    labels = {_field(profile, OutputField.SEGMENT, i).label for i in range(2)}
    assert labels == {"unlabeled_audience", "default_named_audience"}


def test_ce8_platforms_not_merged_when_pillar_label_matches() -> None:
    evidence = [
        _ev("EI", label="instagram_audience", pillar="tutorials"),
        _ev("ET", label="tiktok_audience", pillar="tutorials", platform="tiktok"),
    ]
    profile = fuse_profile(evidence, generated_at="t")
    assert [p.pillar_label for p in profile.ideal_audience_profiles] == [
        "instagram:tutorials",
        "tiktok:tutorials",
    ]
    labels = {_field(profile, OutputField.SEGMENT, i).label for i in range(2)}
    assert labels == {"instagram_audience", "tiktok_audience"}


# --- CE12: a decided field carries its evidence ids ------------------------


def test_ce12_decided_field_has_evidence_ids() -> None:
    profile = fuse_profile([_ev("E42", label="aspirational_beauty")], generated_at="t")
    seg = _field(profile, OutputField.SEGMENT)
    assert seg.label == "aspirational_beauty"
    assert seg.evidence_ids == ["E42"]


def test_ce12_rejects_empty_evidence_ids_and_copy_bypass() -> None:
    with pytest.raises(ValidationError):
        _ev("", label="aspirational_beauty")
    with pytest.raises(ValidationError):
        FieldResult(
            field=OutputField.SEGMENT,
            label="aspirational_beauty",
            support_band=SupportBand.LOW,
            uncalibrated_support_score=0.5,
            evidence_ids=[""],
        )
    result = FieldResult(
        field=OutputField.SEGMENT,
        label="aspirational_beauty",
        support_band=SupportBand.LOW,
        uncalibrated_support_score=0.5,
        evidence_ids=["E42"],
    )
    with pytest.raises(ValidationError):
        result.model_copy(update={"evidence_ids": []})
    with pytest.raises(ValidationError):
        FieldResult.model_construct(
            field=OutputField.SEGMENT,
            label="aspirational_beauty",
            support_band=SupportBand.LOW,
            uncalibrated_support_score=0.5,
            evidence_ids=[],
        )


# --- CE3: aggregate comments cannot drive a field ---------------------------


def test_ce3_comment_only_abstains() -> None:
    profile = fuse_profile(
        [_ev(modality=ModalityFamily.COMMENT, vote=1.0)], generated_at="t"
    )
    seg = _field(profile, OutputField.SEGMENT)
    assert seg.support_band == SupportBand.ABSTAIN


def test_ce3_comments_are_w0_for_price_tier() -> None:
    evidence = [
        _ev(
            f"C{i}",
            field=OutputField.PRICE_TIER,
            modality=ModalityFamily.COMMENT,
            vote=1.0,
        )
        for i in range(20)
    ]
    profile = fuse_profile(evidence, generated_at="t")
    price = _field(profile, OutputField.PRICE_TIER)
    assert price.support_band == SupportBand.ABSTAIN
    assert price.uncalibrated_support_score == 0.0
    assert price.evidence_ids == []


# --- CE5: one modality family cannot dominate beyond its cap ---------------


def test_ce5_single_modality_capped() -> None:
    evidence = [_ev(f"E{i}", label="aspirational_beauty") for i in range(5)]
    profile = fuse_profile(evidence, generated_at="t")
    seg = _field(profile, OutputField.SEGMENT)
    # Five strong text votes still cannot reach HIGH alone (text cap binds).
    assert seg.support_band == SupportBand.LOW
    assert seg.label == "aspirational_beauty"


# --- CE4: creator-authored outweighs implicit -----------------------------


def test_ce4_creator_authored_outweighs_implicit() -> None:
    evidence = [
        _ev("EA", label="authored_target", vote=0.25, authored=True),
        _ev("EB", label="implicit_target", vote=0.25, authored=False),
    ]
    profile = fuse_profile(evidence, generated_at="t")
    seg = _field(profile, OutputField.SEGMENT)
    assert seg.label == "authored_target"


def test_ce4_creator_authored_outweighs_multi_modality_implicit() -> None:
    evidence = [
        _ev("EA", label="authored_target", authored=True),
        _ev(
            "EC",
            label="implicit_target",
            modality=ModalityFamily.COMMERCIAL,
            authored=False,
        ),
        _ev(
            "ES",
            label="implicit_target",
            modality=ModalityFamily.STRUCTURAL,
            authored=False,
        ),
    ]
    profile = fuse_profile(evidence, generated_at="t")
    seg = _field(profile, OutputField.SEGMENT)
    assert seg.label == "authored_target"
    assert seg.evidence_ids == ["EA"]


# --- Counterfactual smoke tests -------------------------------------------


def test_counterfactual_flip_segment_signal() -> None:
    a = fuse_profile([_ev(label="aspirational_beauty")], generated_at="t")
    b = fuse_profile([_ev(label="performance_fitness")], generated_at="t")
    assert _field(a, OutputField.SEGMENT).label == "aspirational_beauty"
    assert _field(b, OutputField.SEGMENT).label == "performance_fitness"


def test_counterfactual_strip_cta_purchase_intent_abstains() -> None:
    # Only a segment signal; nothing votes purchase_intent -> it abstains.
    profile = fuse_profile([_ev(field=OutputField.SEGMENT)], generated_at="t")
    intent = _field(profile, OutputField.PURCHASE_INTENT)
    assert intent.support_band == SupportBand.ABSTAIN
    assert "instagram:unlabeled:purchase_intent" in profile.abstentions


def test_counterfactual_oneoff_campaign_does_not_flip() -> None:
    established = [
        _ev("A1", label="aspirational_beauty", modality=ModalityFamily.TEXT),
        _ev("A2", label="aspirational_beauty", modality=ModalityFamily.STRUCTURAL),
    ]
    oneoff = [
        _ev(f"B{i}", label="budget_shopper", modality=ModalityFamily.COMMERCIAL, cluster="camp1")
        for i in range(3)
    ]
    profile = fuse_profile(established + oneoff, generated_at="t")
    seg = _field(profile, OutputField.SEGMENT)
    assert seg.label == "aspirational_beauty"


# --- Guards ----------------------------------------------------------------


def test_multiple_creators_rejected() -> None:
    with pytest.raises(MultipleCreatorsError):
        fuse_profile([_ev("E1", creator="c1"), _ev("E2", creator="c2")], generated_at="t")


def test_empty_evidence_rejected() -> None:
    with pytest.raises(ValueError):
        fuse_profile([], generated_at="t")
