"""Offline tests for the deterministic creator-gender fusion + its schema (no LLM, no network).

Covers the soft-lean schema invariants (a hard categorical label is unrepresentable — including
the typed-provenance back door and a bounded basis; finite/range/required guards) and the fusion
behavior (signed aggregation + direction, abstain below the floor, conflicting cues net to abstain,
product-marketed-gender EXCLUDED from decisive fusion, single-creator precondition, empty input,
evidence citation).
"""
from __future__ import annotations

import math

import pytest
from pydantic import ValidationError

from schemas.creator_gender_models import (
    CREATOR_GENDER_BASIS_MAX_CHARS,
    CREATOR_GENDER_DECISIVE_CONFIDENCE_FLOOR,
    CreatorGenderLean,
    CreatorGenderSignal,
    GenderCueKind,
)
from scoring.creator_gender_fusion import (
    FUSION_CONFIG_VERSION,
    MultipleCreatorsError,
    fuse_creator_gender,
)


def _sig(
    *,
    creator_id: str = "c1",
    signal_id: str = "s1",
    reel_ref: str = "ABC123",
    gender_lean: float = 0.0,
    confidence: float = 1.0,
    cue_kind: GenderCueKind = GenderCueKind.SELF_PRESENTATION,
    basis: str = "as a guy who loves frags",
) -> CreatorGenderSignal:
    return CreatorGenderSignal(
        creator_id=creator_id, signal_id=signal_id, reel_ref=reel_ref,
        gender_lean=gender_lean, confidence=confidence, cue_kind=cue_kind, basis=basis,
    )


def _fuse(signals, creator_id: str = "c1"):
    return fuse_creator_gender(signals, creator_id=creator_id, generated_at="2026-06-28T00:00:00Z")


# --- schema: a hard categorical label is UNREPRESENTABLE ----------------------


def test_no_categorical_gender_field_on_either_model() -> None:
    assert "gender" not in CreatorGenderSignal.model_fields
    assert "gender" not in CreatorGenderLean.model_fields


def test_signal_rejects_extra_categorical_field() -> None:
    with pytest.raises(ValidationError):
        CreatorGenderSignal(
            creator_id="c1", signal_id="s1", reel_ref="r", gender_lean=0.5, confidence=0.9,
            cue_kind=GenderCueKind.SELF_PRESENTATION, basis="x", gender="male",  # extra=forbid
        )


def test_signal_rejects_nested_categorical_provenance_backdoor() -> None:
    # The typed provenance closes the untyped-dict back door (F1): a categorical gender or
    # commenter-gender key cannot hide inside provenance.
    with pytest.raises(ValidationError):
        CreatorGenderSignal(
            creator_id="c1", signal_id="s1", reel_ref="r", gender_lean=0.5, confidence=0.9,
            cue_kind=GenderCueKind.SELF_PRESENTATION, basis="x",
            provenance={"gender": "male", "commenter_gender": "female"},
        )


# --- schema: finite + range + required + bounded guards -----------------------


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), float("-inf")])
def test_signal_rejects_nonfinite_lean(bad: float) -> None:
    with pytest.raises(ValidationError):
        _sig(gender_lean=bad)


def test_signal_rejects_out_of_range() -> None:
    with pytest.raises(ValidationError):
        _sig(gender_lean=1.5)
    with pytest.raises(ValidationError):
        _sig(confidence=1.5)


def test_signal_requires_non_empty_fields() -> None:
    with pytest.raises(ValidationError):
        _sig(creator_id="  ")
    with pytest.raises(ValidationError):
        _sig(basis="")


def test_signal_rejects_overlong_basis() -> None:
    with pytest.raises(ValidationError):
        _sig(basis="x" * (CREATOR_GENDER_BASIS_MAX_CHARS + 1))


# --- fusion: signed aggregation + direction -----------------------------------


def test_strong_self_presentation_is_confident_male_lean() -> None:
    r = _fuse([_sig(gender_lean=1.0, confidence=1.0)])
    assert r.abstained is False
    assert r.gender_lean > 0
    assert r.gender_lean == pytest.approx(round(math.tanh(2.0), 4))  # ~0.964
    assert r.confidence == pytest.approx(round(math.tanh(2.0), 4))
    assert r.evidence_ids == ["s1"]


def test_female_lean_is_negative() -> None:
    r = _fuse([_sig(gender_lean=-1.0, confidence=1.0)])
    assert r.abstained is False and r.gender_lean < 0


# --- fusion: abstain ----------------------------------------------------------


def test_empty_signals_abstain() -> None:
    r = _fuse([])
    assert r.abstained is True and r.gender_lean == 0.0 and r.confidence == 0.0
    assert r.evidence_ids == []


def test_conflicting_cues_net_to_abstain() -> None:
    r = _fuse([
        _sig(signal_id="m", gender_lean=1.0, confidence=1.0),
        _sig(signal_id="f", gender_lean=-1.0, confidence=1.0),
    ])
    assert r.abstained is True and r.gender_lean == 0.0


def test_weak_self_presentation_abstains_but_keeps_audit_evidence() -> None:
    r = _fuse([_sig(signal_id="weak", gender_lean=0.1, confidence=0.5)])
    assert r.abstained is True
    assert r.gender_lean == 0.0
    assert 0.0 < r.confidence < CREATOR_GENDER_DECISIVE_CONFIDENCE_FLOOR
    assert r.evidence_ids == ["weak"]


# --- fusion: product-marketed-gender is EXCLUDED from decisive fusion (F2) -----


def test_product_cue_is_excluded_from_decisive_fusion() -> None:
    # Even a max-confidence product cue must NOT decide a lean (it would be circular).
    r = _fuse([_sig(gender_lean=1.0, confidence=1.0, cue_kind=GenderCueKind.PRODUCT_MARKETED_GENDER)])
    assert r.abstained is True and r.gender_lean == 0.0
    assert r.confidence == 0.0
    assert r.evidence_ids == []


def test_product_cue_does_not_offset_self_presentation() -> None:
    self_only = _fuse([_sig(signal_id="self", gender_lean=-1.0, confidence=1.0)])
    with_product = _fuse([
        _sig(signal_id="self", gender_lean=-1.0, confidence=1.0),
        _sig(signal_id="prod", gender_lean=1.0, confidence=1.0,
             cue_kind=GenderCueKind.PRODUCT_MARKETED_GENDER),
    ])
    assert with_product.gender_lean == self_only.gender_lean  # product cannot offset
    assert with_product.evidence_ids == ["self"]


# --- fusion: single-creator precondition --------------------------------------


def test_foreign_creator_id_raises() -> None:
    with pytest.raises(MultipleCreatorsError):
        _fuse([_sig(creator_id="c1"), _sig(signal_id="s2", creator_id="c2")], creator_id="c1")


def test_blank_creator_id_raises() -> None:
    with pytest.raises(ValueError):
        fuse_creator_gender([_sig()], creator_id="  ")


# --- output shape -------------------------------------------------------------


def test_output_is_creator_gender_lean_with_provenance() -> None:
    r = _fuse([_sig(gender_lean=0.8, confidence=0.9)])
    assert isinstance(r, CreatorGenderLean)
    assert r.creator_id == "c1"
    assert r.fusion_config_version == FUSION_CONFIG_VERSION
    assert r.provenance.fusion_config_version == FUSION_CONFIG_VERSION


def test_lean_schema_rejects_incoherent_output_states() -> None:
    base = {
        "creator_id": "c1",
        "fusion_config_version": FUSION_CONFIG_VERSION,
        "generated_at": "2026-06-28T00:00:00Z",
        "provenance": {"fusion_config_version": FUSION_CONFIG_VERSION},
    }
    with pytest.raises(ValidationError):
        CreatorGenderLean(
            **base, gender_lean=0.9, confidence=0.9, abstained=True, evidence_ids=[],
        )
    with pytest.raises(ValidationError):
        CreatorGenderLean(
            **base, gender_lean=0.9, confidence=0.9, abstained=False, evidence_ids=[],
        )
    with pytest.raises(ValidationError):
        CreatorGenderLean(
            **base, gender_lean=0.0, confidence=0.0, abstained=False, evidence_ids=["s1"],
        )
    with pytest.raises(ValidationError):
        CreatorGenderLean(
            **base, gender_lean=0.9, confidence=0.9, abstained=False, evidence_ids=[""],
        )


def test_lean_schema_revalidates_copy_and_construct_paths() -> None:
    result = _fuse([_sig(signal_id="self", gender_lean=1.0, confidence=1.0)])
    with pytest.raises(ValidationError):
        result.model_copy(update={"evidence_ids": []})
    with pytest.raises(ValidationError):
        CreatorGenderLean.model_construct(
            creator_id="c1",
            gender_lean=0.0,
            confidence=0.0,
            abstained=False,
            evidence_ids=["s1"],
            fusion_config_version=FUSION_CONFIG_VERSION,
            generated_at="2026-06-28T00:00:00Z",
            provenance={"fusion_config_version": FUSION_CONFIG_VERSION},
        )
