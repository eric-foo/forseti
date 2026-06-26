"""Offline tests for the Phase B calibration answer-key machinery.

All synthetic, no LLM, no network, no live capture. Covers the label schema, the structural
blindness of the worklist (it must never carry a machine verdict), grouping/determinism, the
build -> fill -> load round-trip, and coverage/validity enforcement on load.
"""
from __future__ import annotations

import pytest
import yaml
from pydantic import ValidationError

import scoring.calibration_corpus as calibration_corpus
from schemas.product_mention_models import (
    Concentration,
    ProductMention,
    TranscriptSource,
    Verdict,
)
from scoring.calibration_corpus import (
    CalibrationLabel,
    build_blind_labeling_worklist,
    load_labels_from_worklist,
)


def _m(
    mention_id: str = "m1",
    *,
    brand: str = "dior",
    line: str = "sauvage",
    source: str = "quote text",
    video: str = "v1",
) -> ProductMention:
    return ProductMention(
        mention_id=mention_id,
        video_id=video,
        transcript_anchor=f"asr:{video}",
        transcript_source=TranscriptSource.ASR,
        brand=brand,
        line=line,
        concentration=Concentration.UNKNOWN,
        stance_vote=1.0,
        source_pointer=source,
        start_ms=0,
        end_ms=1,
        creator_authored=True,
        extractor_confidence=1.0,
    )


def _fill(worklist_yaml: str, verdicts) -> str:
    """Simulate the owner filling gold_verdict (str = same for all; dict keyed by (brand,line))."""
    doc = yaml.safe_load(worklist_yaml)
    for product in doc["products"]:
        if isinstance(verdicts, str):
            product["gold_verdict"] = verdicts
        else:
            product["gold_verdict"] = verdicts[(product["brand"], product["line"])]
    return yaml.safe_dump(doc)


# --- schema -----------------------------------------------------------------


def test_label_schema_accepts_valid_and_rejects_bad() -> None:
    ok = CalibrationLabel(
        creator_id="c1", brand="Dior", line="Sauvage",
        gold_verdict=Verdict.POSITIVE, labeler="owner", evidence_pointer=["m1"],
    )
    assert ok.gold_verdict == Verdict.POSITIVE
    with pytest.raises(ValidationError):  # blank creator_id
        CalibrationLabel(creator_id="  ", brand="b", line="l",
                         gold_verdict=Verdict.UNKNOWN, labeler="owner", evidence_pointer=["m1"])
    with pytest.raises(ValidationError):  # no evidence
        CalibrationLabel(creator_id="c", brand="b", line="l",
                         gold_verdict=Verdict.POSITIVE, labeler="owner", evidence_pointer=[])
    with pytest.raises(ValidationError):  # invalid verdict
        CalibrationLabel(creator_id="c", brand="b", line="l",
                         gold_verdict="great", labeler="owner", evidence_pointer=["m1"])


# --- blindness (the calibration-correctness invariant) ----------------------


def test_worklist_is_structurally_blind() -> None:
    # The builder must never pre-fill a verdict, and the module must not even reference the fusion
    # verdict -- otherwise the owner's labels would correlate with the machine (circular calibration).
    worklist = build_blind_labeling_worklist([_m("m1", brand="Dior", line="Sauvage")], creator_id="c1")
    doc = yaml.safe_load(worklist)
    assert all(product["gold_verdict"] == "" for product in doc["products"])
    assert doc["products"][0]["quotes"] == ["quote text"]
    assert doc["products"][0]["evidence_pointer"] == ["m1"]
    # structural blindness: the module never imports the fusion's verdict machinery, so it cannot
    # leak a machine verdict into the worklist (the shared Verdict enum vocabulary is not a leak;
    # referencing product_fusion's grouping in a comment is documentation, not a leak).
    assert "fuse_product_verdicts" not in dir(calibration_corpus)
    assert "ProductVerdict" not in dir(calibration_corpus)


# --- grouping + determinism -------------------------------------------------


def test_worklist_groups_case_variants_and_is_deterministic() -> None:
    mentions = [
        _m("a", brand="Dior", line="Sauvage", source="q1"),
        _m("b", brand="dior", line="sauvage", source="q2"),  # case variant -> same product
        _m("c", brand="Chanel", line="Bleu", source="q3"),
    ]
    worklist = build_blind_labeling_worklist(mentions, creator_id="c1")
    doc = yaml.safe_load(worklist)
    assert len(doc["products"]) == 2
    dior = next(p for p in doc["products"] if p["brand"].lower() == "dior")
    assert sorted(dior["evidence_pointer"]) == ["a", "b"]
    assert build_blind_labeling_worklist(mentions, creator_id="c1") == worklist


def test_build_requires_creator_id() -> None:
    with pytest.raises(ValueError):
        build_blind_labeling_worklist([_m("a")], creator_id="   ")


# --- round-trip + load enforcement ------------------------------------------


def test_roundtrip_build_fill_load() -> None:
    mentions = [
        _m("a", brand="Dior", line="Sauvage", source="nine out of ten"),
        _m("b", brand="Chanel", line="Bleu", source="meh, skip it"),
    ]
    worklist = build_blind_labeling_worklist(mentions, creator_id="c1")
    filled = _fill(worklist, {("Dior", "Sauvage"): "positive", ("Chanel", "Bleu"): "negative"})
    labels = load_labels_from_worklist(filled, labeler="owner")
    by_product = {(label.brand, label.line): label for label in labels}
    assert by_product[("Dior", "Sauvage")].gold_verdict == Verdict.POSITIVE
    assert by_product[("Dior", "Sauvage")].evidence_pointer == ["a"]
    assert by_product[("Chanel", "Bleu")].gold_verdict == Verdict.NEGATIVE
    assert all(label.labeler == "owner" and label.creator_id == "c1" for label in labels)


def test_load_rejects_unlabeled_product() -> None:
    worklist = build_blind_labeling_worklist([_m("a")], creator_id="c1")
    with pytest.raises(ValueError):  # gold_verdict still blank -> coverage failure
        load_labels_from_worklist(worklist)


def test_load_rejects_invalid_verdict() -> None:
    worklist = build_blind_labeling_worklist([_m("a")], creator_id="c1")
    with pytest.raises(ValueError):
        load_labels_from_worklist(_fill(worklist, "great"))


def test_load_rejects_malformed_worklist() -> None:
    with pytest.raises(ValueError):
        load_labels_from_worklist("not: a worklist")
    with pytest.raises(ValueError):
        load_labels_from_worklist("products: []")
