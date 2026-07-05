"""Offline tests for the Phase B calibration answer-key machinery.

All synthetic, no LLM, no network, no live capture. Covers the label schema, the structural
blindness of the worklist (it must never carry or import a machine verdict), grouping/determinism,
the build -> fill -> load round-trip, and the strict load enforcement: explicit provenance, strict
row shape, full coverage, and valid/non-blank verdicts.
"""
from __future__ import annotations

import ast
import pathlib

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


def test_worklist_builder_never_prefills_a_verdict() -> None:
    worklist = build_blind_labeling_worklist([_m("m1", brand="Dior", line="Sauvage")], creator_id="c1")
    doc = yaml.safe_load(worklist)
    assert all(product["gold_verdict"] == "" for product in doc["products"])
    assert doc["products"][0]["quotes"] == ["quote text"]
    assert doc["products"][0]["evidence_pointer"] == ["m1"]


def test_module_never_imports_the_fusion_verdict() -> None:
    # Structural blindness: importing the fusion verdict (under ANY alias) would let a worklist
    # correlate with the machine. An AST scan is robust to aliasing where a name check is not.
    source = pathlib.Path(calibration_corpus.__file__).read_text(encoding="utf-8")
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.ImportFrom):
            assert not (node.module or "").startswith("scoring.product_fusion")
        elif isinstance(node, ast.Import):
            assert all(not alias.name.startswith("scoring.product_fusion") for alias in node.names)


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


# --- round-trip -------------------------------------------------------------


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


# --- load: provenance (F3) --------------------------------------------------


def test_load_requires_explicit_labeler() -> None:
    filled = _fill(build_blind_labeling_worklist([_m("a")], creator_id="c1"), "positive")
    with pytest.raises(TypeError):  # labeler has no default
        load_labels_from_worklist(filled)
    with pytest.raises(ValueError):  # blank labeler rejected
        load_labels_from_worklist(filled, labeler="  ")
    assert load_labels_from_worklist(filled, labeler="eric")[0].labeler == "eric"


# --- load: coverage (F1) ----------------------------------------------------


def test_load_rejects_unlabeled_product() -> None:
    worklist = build_blind_labeling_worklist([_m("a")], creator_id="c1")
    with pytest.raises(ValueError):  # gold_verdict still blank -> coverage failure
        load_labels_from_worklist(worklist, labeler="owner")


def test_load_rejects_deleted_product() -> None:
    mentions = [_m("a", brand="Dior", line="Sauvage"), _m("b", brand="Chanel", line="Bleu")]
    doc = yaml.safe_load(build_blind_labeling_worklist(mentions, creator_id="c1"))
    for product in doc["products"]:
        product["gold_verdict"] = "positive"
    del doc["products"][0]  # owner dropped a surfaced product
    with pytest.raises(ValueError):
        load_labels_from_worklist(yaml.safe_dump(doc), labeler="owner")


def test_load_rejects_duplicate_product() -> None:
    doc = yaml.safe_load(build_blind_labeling_worklist([_m("a", brand="Dior", line="Sauvage")], creator_id="c1"))
    doc["products"][0]["gold_verdict"] = "positive"
    doc["products"].append(dict(doc["products"][0]))  # duplicate normalized product
    with pytest.raises(ValueError):
        load_labels_from_worklist(yaml.safe_dump(doc), labeler="owner")


# --- load: row strictness (F2) ----------------------------------------------


def test_load_rejects_contaminated_machine_output_field() -> None:
    doc = yaml.safe_load(build_blind_labeling_worklist([_m("a")], creator_id="c1"))
    doc["products"][0]["gold_verdict"] = "positive"
    doc["products"][0]["fusion_verdict"] = "positive"  # leaked machine output
    with pytest.raises(ValidationError):
        load_labels_from_worklist(yaml.safe_dump(doc), labeler="owner")


def test_load_rejects_malformed_evidence_pointer() -> None:
    doc = yaml.safe_load(build_blind_labeling_worklist([_m("a")], creator_id="c1"))
    doc["products"][0]["gold_verdict"] = "positive"
    doc["products"][0]["evidence_pointer"] = "m1"  # bare string, not a list
    with pytest.raises(ValidationError):
        load_labels_from_worklist(yaml.safe_dump(doc), labeler="owner")


def test_load_rejects_invalid_verdict() -> None:
    worklist = build_blind_labeling_worklist([_m("a")], creator_id="c1")
    with pytest.raises(ValueError):
        load_labels_from_worklist(_fill(worklist, "great"), labeler="owner")


def test_load_rejects_malformed_worklist() -> None:
    with pytest.raises(ValueError):
        load_labels_from_worklist("not: a worklist", labeler="owner")
    with pytest.raises(ValueError):
        load_labels_from_worklist("expected_products: []\nproducts: []", labeler="owner")
