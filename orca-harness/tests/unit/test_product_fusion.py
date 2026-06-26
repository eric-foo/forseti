"""Pass-2 product verdict fusion: determinism + verdict-rule + abstention tests.

All synthetic mentions; no LLM, no network. Mirrors test_audience_fusion's discipline.
"""
from __future__ import annotations

import pytest
from pydantic import ValidationError

from schemas.product_mention_models import (
    Concentration,
    ProductMention,
    ProductVerdict,
    ProductVerdictSet,
    StatedRating,
    TranscriptSource,
    Verdict,
)
from scoring.product_fusion import fuse_product_verdicts


def _m(
    mention_id: str = "m1",
    *,
    video_id: str = "v1",
    brand: str = "dior",
    line: str = "sauvage",
    stance: float = 1.0,
    conf: float = 1.0,
    authored: bool = True,
    negation: bool = False,
    rating: StatedRating | None = None,
    concentration: Concentration = Concentration.ELIXIR,
) -> ProductMention:
    return ProductMention(
        mention_id=mention_id,
        video_id=video_id,
        transcript_anchor=f"asr:{video_id}",
        transcript_source=TranscriptSource.ASR,
        brand=brand,
        line=line,
        concentration=concentration,
        stance_vote=stance,
        stated_rating=rating,
        source_pointer=f"{brand} {line}",
        start_ms=0,
        end_ms=1000,
        creator_authored=authored,
        possible_negation_or_irony=negation,
        extractor_confidence=conf,
    )


def _verdict(vs: ProductVerdictSet, brand: str, line: str) -> ProductVerdict:
    return next(v for v in vs.verdicts if v.brand == brand and v.line == line)


# --- container + guards ----------------------------------------------------


def test_empty_mentions_yields_empty_set() -> None:
    vs = fuse_product_verdicts([], creator_id="c1", generated_at="t")
    assert vs.creator_id == "c1"
    assert vs.verdicts == []
    assert vs.fusion_config_version


def test_missing_creator_id_rejected() -> None:
    with pytest.raises(ValueError):
        fuse_product_verdicts([_m()], creator_id="   ", generated_at="t")


# --- verdict rule (support/oppose separated) -------------------------------


def test_single_strong_authored_positive() -> None:
    vs = fuse_product_verdicts([_m("m1", stance=1.0)], creator_id="c1", generated_at="t")
    v = _verdict(vs, "dior", "sauvage")
    assert v.verdict == Verdict.POSITIVE
    assert v.evidence_ids == ["m1"]
    assert v.counterevidence_ids == []
    assert v.mention_count == 1
    assert v.uncalibrated_support_score > _MATERIAL_MIN_FOR_TEST


def test_single_strong_negative_cites_only_counterevidence() -> None:
    vs = fuse_product_verdicts([_m("m1", stance=-1.0)], creator_id="c1", generated_at="t")
    v = _verdict(vs, "dior", "sauvage")
    assert v.verdict == Verdict.NEGATIVE
    assert v.counterevidence_ids == ["m1"]
    assert v.evidence_ids == []


def test_both_sides_material_is_mixed_not_netted() -> None:
    mentions = [_m("p1", video_id="v1", stance=1.0), _m("n1", video_id="v2", stance=-1.0)]
    vs = fuse_product_verdicts(mentions, creator_id="c1", generated_at="t")
    v = _verdict(vs, "dior", "sauvage")
    assert v.verdict == Verdict.MIXED
    assert v.evidence_ids == ["p1"]
    assert v.counterevidence_ids == ["n1"]
    assert v.mention_count == 2


def test_thin_evidence_abstains_to_unknown() -> None:
    vs = fuse_product_verdicts(
        [_m("m1", stance=0.25, authored=False)], creator_id="c1", generated_at="t"
    )
    v = _verdict(vs, "dior", "sauvage")
    assert v.verdict == Verdict.UNKNOWN
    assert "dior:sauvage" in vs.abstentions


# --- weighting: dependence / authored / negation / rating ------------------


def test_dependence_discount_one_video_not_n_endorsements() -> None:
    # 5 mentions in ONE video are weaker than 5 across DIFFERENT videos (1/sqrt(n) per cluster).
    one_video = [_m(f"a{i}", video_id="v1", stance=0.5, authored=False) for i in range(5)]
    many_videos = [_m(f"b{i}", video_id=f"v{i}", stance=0.5, authored=False) for i in range(5)]
    one = _verdict(fuse_product_verdicts(one_video, creator_id="c1", generated_at="t"), "dior", "sauvage")
    many = _verdict(fuse_product_verdicts(many_videos, creator_id="c1", generated_at="t"), "dior", "sauvage")
    assert one.uncalibrated_support_score < many.uncalibrated_support_score


def test_creator_authored_outweighs_implicit() -> None:
    authored = _verdict(
        fuse_product_verdicts([_m("a", stance=0.35, authored=True)], creator_id="c1", generated_at="t"),
        "dior", "sauvage",
    )
    implicit = _verdict(
        fuse_product_verdicts([_m("b", stance=0.35, authored=False)], creator_id="c1", generated_at="t"),
        "dior", "sauvage",
    )
    assert authored.uncalibrated_support_score > implicit.uncalibrated_support_score


def test_negation_discounts_stance() -> None:
    plain = _verdict(
        fuse_product_verdicts([_m("a", stance=0.6, authored=False)], creator_id="c1", generated_at="t"),
        "dior", "sauvage",
    )
    ironic = _verdict(
        fuse_product_verdicts(
            [_m("b", stance=0.6, authored=False, negation=True)], creator_id="c1", generated_at="t"
        ),
        "dior", "sauvage",
    )
    assert ironic.uncalibrated_support_score < plain.uncalibrated_support_score


def test_stated_rating_treated_as_witnessed_authored() -> None:
    rating = StatedRating(value=9, scale_max=10, source_pointer="nine out of ten")
    rated = _verdict(
        fuse_product_verdicts(
            [_m("a", stance=0.5, authored=False, negation=True, rating=rating)],
            creator_id="c1", generated_at="t",
        ),
        "dior", "sauvage",
    )
    plain = _verdict(
        fuse_product_verdicts(
            [_m("b", stance=0.5, authored=False, negation=True)], creator_id="c1", generated_at="t"
        ),
        "dior", "sauvage",
    )
    assert rated.uncalibrated_support_score > plain.uncalibrated_support_score


# --- grouping + determinism ------------------------------------------------


def test_products_grouped_by_normalized_brand_line() -> None:
    mentions = [
        _m("a", brand="dior", line="sauvage", stance=1.0),
        _m("b", brand="chanel", line="bleu", stance=1.0),
        _m("c", brand="Dior", line="Sauvage", stance=1.0),  # case variant -> merges with "a"
    ]
    vs = fuse_product_verdicts(mentions, creator_id="c1", generated_at="t")
    assert len(vs.verdicts) == 2
    dior = _verdict(vs, "dior", "sauvage")
    assert dior.mention_count == 2
    assert dior.evidence_ids == ["a", "c"]


def test_determinism_same_input_same_output() -> None:
    mentions = [_m("a", stance=1.0), _m("b", brand="chanel", line="bleu", stance=-1.0)]
    a = fuse_product_verdicts(mentions, creator_id="c1", generated_at="t")
    b = fuse_product_verdicts(mentions, creator_id="c1", generated_at="t")
    assert a.model_dump() == b.model_dump()


# --- schema invariant ------------------------------------------------------


def test_schema_decided_verdict_needs_side_correct_evidence() -> None:
    # positive must cite supporting evidence (not just *any* side)
    with pytest.raises(ValidationError):
        ProductVerdict(brand="d", line="s", verdict=Verdict.POSITIVE, mention_count=1)
    with pytest.raises(ValidationError):  # positive with only counterevidence is unsound
        ProductVerdict(brand="d", line="s", verdict=Verdict.POSITIVE, mention_count=1, counterevidence_ids=["n1"])
    with pytest.raises(ValidationError):  # negative with only support is unsound
        ProductVerdict(brand="d", line="s", verdict=Verdict.NEGATIVE, mention_count=1, evidence_ids=["p1"])
    with pytest.raises(ValidationError):  # mixed with one side is unsound
        ProductVerdict(brand="d", line="s", verdict=Verdict.MIXED, mention_count=1, evidence_ids=["p1"])
    # valid shapes: positive+support, negative+counter, mixed+both, unknown+none
    ProductVerdict(brand="d", line="s", verdict=Verdict.POSITIVE, mention_count=1, evidence_ids=["p1"])
    ProductVerdict(brand="d", line="s", verdict=Verdict.NEGATIVE, mention_count=1, counterevidence_ids=["n1"])
    ProductVerdict(
        brand="d", line="s", verdict=Verdict.MIXED, mention_count=2, evidence_ids=["p1"], counterevidence_ids=["n1"]
    )
    ProductVerdict(brand="d", line="s", verdict=Verdict.UNKNOWN, mention_count=0)


def test_negated_rating_is_still_discounted() -> None:
    # A rating gives authored weight but does NOT cancel the extractor's irony flag:
    # a weak, flagged-ironic, rated mention must not flip to a confident positive (F2).
    rating = StatedRating(value=10, scale_max=10, source_pointer="ten out of ten")
    v = _verdict(
        fuse_product_verdicts(
            [_m("a", stance=0.5, authored=False, negation=True, rating=rating)],
            creator_id="c1", generated_at="t",
        ),
        "dior", "sauvage",
    )
    assert v.verdict == Verdict.UNKNOWN


# Materiality floor mirrored from the fusion module for readable assertions.
_MATERIAL_MIN_FOR_TEST = 0.40
