"""Phase B answer-key machinery for product-verdict calibration (no-LLM, pure).

Real calibration needs ground truth: the owner's OWN verdict on real mentions, against which the
fusion's constants are tuned in Phase C. This module is the machinery that lets the owner PRODUCE
that ground truth. It does NOT produce labels itself -- an agent labelling them would be circular --
and it captures nothing.

Three pieces:
  - ``CalibrationLabel``              : one owner-authored gold verdict per (creator, brand, line).
  - ``build_blind_labeling_worklist`` : mentions -> a fill-in YAML showing the QUOTES but no machine
                                        verdict, plus a coverage manifest, so the owner labels blind.
  - ``load_labels_from_worklist``     : the filled worklist -> validated ``CalibrationLabel`` records,
                                        enforcing strict row shape, full coverage, and explicit
                                        owner provenance.

BLINDNESS is structural: this module never imports the fusion verdict, so a worklist cannot leak it
(guarded by an AST import test). The real corpus needs the owner's live captures + blind labels;
this is offline machinery only and produces no labels and no calibration by itself.

Procedure: docs/workflows/product_verdict_calibration_labeling_protocol_v0.md.
No LLM, no network (scoring/ no-LLM zone). Imports only stdlib + yaml + the mention/verdict schemas.
"""
from __future__ import annotations

import json
from collections import defaultdict

import yaml
from pydantic import Field, field_validator

from schemas.case_models import StrictModel
from schemas.product_mention_models import ProductMention, Verdict

_GOLD_VERDICT_VALUES: tuple[str, ...] = tuple(v.value for v in Verdict)


class CalibrationLabel(StrictModel):
    """One owner-authored gold verdict for a (creator, brand, line) product.

    GROUND TRUTH -- an independent human judgment, never a machine-derived or agent-asserted value.
    ``gold_verdict`` reuses the fusion's ``Verdict`` vocabulary so a label and a machine verdict are
    directly comparable in Phase C.
    """

    creator_id: str
    brand: str
    line: str
    gold_verdict: Verdict
    labeler: str
    evidence_pointer: list[str] = Field(min_length=1)
    note: str = ""

    @field_validator("creator_id", "brand", "line", "labeler")
    @classmethod
    def _required_non_empty(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("field must be non-empty")
        return value

    @field_validator("evidence_pointer")
    @classmethod
    def _pointers_non_empty(cls, value: list[str]) -> list[str]:
        cleaned = [pointer for pointer in value if pointer and pointer.strip()]
        if not cleaned:
            raise ValueError("evidence_pointer must cite at least one non-empty mention id")
        return cleaned


class _WorklistRow(StrictModel):
    """Strict shape of ONE filled worklist row.

    ``extra='forbid'`` (inherited from ``StrictModel``) rejects any unknown key -- including a leaked
    machine-output field such as ``fusion_verdict`` -- and the typed ``evidence_pointer`` rejects
    malformed provenance (a bare string would otherwise be split into characters; a mapping into its
    keys). ``gold_verdict`` is a plain string here so a blank can be detected as a coverage failure.
    """

    creator_id: str
    brand: str
    line: str
    evidence_pointer: list[str]
    gold_verdict: str = ""
    quotes: list[str] = Field(default_factory=list)
    note: str = ""


def brand_line_key(brand: str, line: str) -> tuple[str, str]:
    """Canonical normalized (brand, line) grouping key (casing/whitespace-insensitive).

    The ONE shared normalization for product identity: worklist grouping here and the
    product-fusion grouping (``scoring.product_fusion`` imports this) both use it, so Phase C
    matches a label to a verdict under identical normalization. It lives HERE rather than in
    ``product_fusion`` because structural blindness forbids this module importing anything from
    ``scoring.product_fusion`` (see ``test_module_never_imports_the_fusion_verdict``); the
    reverse import leaks nothing into the worklist.
    """
    return (brand.strip().lower(), line.strip().lower())


def _expected_pairs(expected: object) -> list[tuple[str, str]]:
    """Parse the coverage manifest into (brand, line) display pairs, rejecting a malformed manifest."""
    if not isinstance(expected, list):
        raise ValueError("expected_products must be a list of [brand, line] pairs")
    pairs: list[tuple[str, str]] = []
    for item in expected:
        if not (isinstance(item, list) and len(item) == 2 and all(isinstance(x, str) for x in item)):
            raise ValueError(f"expected_products entry must be a [brand, line] pair, got {item!r}")
        pairs.append((item[0], item[1]))
    return pairs


def build_blind_labeling_worklist(mentions: list[ProductMention], *, creator_id: str) -> str:
    """Render a BLIND fill-in YAML worklist: quotes per product + a blank gold_verdict, no verdict.

    Groups ``mentions`` by normalized (brand, line); for each product lists the verified quotes and
    contributing mention ids with an empty ``gold_verdict`` for the owner to fill, and stamps an
    ``expected_products`` coverage manifest so the loader can detect a dropped or duplicated product.
    Deterministic (products and ids sorted). Reads ONLY mentions -- never the fusion -- so it cannot
    leak a verdict.
    """
    if not creator_id or not creator_id.strip():
        raise ValueError("build_blind_labeling_worklist requires a non-empty creator_id")

    grouped: dict[tuple[str, str], list[ProductMention]] = defaultdict(list)
    display: dict[tuple[str, str], tuple[str, str]] = {}
    for mention in mentions:
        key = brand_line_key(mention.brand, mention.line)
        grouped[key].append(mention)
        display.setdefault(key, (mention.brand, mention.line))  # first-seen original casing

    keys = sorted(grouped)
    allowed = " | ".join(_GOLD_VERDICT_VALUES)
    lines = [
        f"# BLIND labeling worklist -- creator {creator_id}",
        f"# Read the quotes and set each gold_verdict to ONE of: {allowed}.",
        "# Label from the quotes alone. Do NOT consult any machine/fusion output -- that would make",
        "# calibration circular. 'unknown' is a valid, expected answer; do not force a call.",
        "# Label EVERY product and delete none -- abstentions are recorded as 'unknown'.",
        "expected_products:   # coverage manifest -- do NOT edit",
    ]
    for key in keys:
        brand, line = display[key]
        lines.append(f"  - [{json.dumps(brand)}, {json.dumps(line)}]")
    lines.append("products:")
    for key in keys:
        brand, line = display[key]
        items = grouped[key]
        ids = sorted(mention.mention_id for mention in items)
        quotes = sorted({mention.source_pointer for mention in items})
        lines.append(f"  - creator_id: {json.dumps(creator_id)}")
        lines.append(f"    brand: {json.dumps(brand)}")
        lines.append(f"    line: {json.dumps(line)}")
        lines.append(f"    evidence_pointer: [{', '.join(json.dumps(i) for i in ids)}]")
        lines.append("    quotes:")
        for quote in quotes:
            lines.append(f"      - {json.dumps(quote)}")
        lines.append(f'    gold_verdict: ""        # <-- fill: {allowed}')
        lines.append('    note: ""')
    return "\n".join(lines) + "\n"


def load_labels_from_worklist(source: str, *, labeler: str) -> list[CalibrationLabel]:
    """Parse a filled blind worklist into validated ``CalibrationLabel`` records.

    ``source`` is the worklist YAML text (path-agnostic; the caller owns where the file lives).
    ``labeler`` is REQUIRED and names the human who produced these labels -- it is not defaulted, so
    a copied or agent-filled file cannot silently become owner-authored ground truth.

    Enforces, in order: explicit provenance; strict per-row shape (``_WorklistRow`` -- rejects a
    leaked machine-output field or malformed ``evidence_pointer``); no duplicate products; full
    coverage against the ``expected_products`` manifest (no product dropped or added); and a valid,
    non-blank ``gold_verdict`` for every product (so an abstention is an explicit ``unknown`` rather
    than silently dropped). Raises ``ValueError``/``ValidationError`` on any violation.
    """
    if not labeler or not labeler.strip():
        raise ValueError("load_labels_from_worklist requires an explicit labeler (owner provenance)")

    parsed = yaml.safe_load(source) or {}
    if not isinstance(parsed, dict) or "products" not in parsed:
        raise ValueError("worklist must be a mapping with a 'products' list")
    if "expected_products" not in parsed:
        raise ValueError(
            "worklist missing coverage manifest 'expected_products'; "
            "regenerate via build_blind_labeling_worklist"
        )
    raw_products = parsed["products"]
    if not isinstance(raw_products, list) or not raw_products:
        raise ValueError("worklist 'products' must be a non-empty list")

    rows = [_WorklistRow.model_validate(row) for row in raw_products]

    present = [brand_line_key(row.brand, row.line) for row in rows]
    if len(set(present)) != len(present):
        raise ValueError("worklist has duplicate products (same normalized brand/line)")
    expected = {brand_line_key(brand, line) for brand, line in _expected_pairs(parsed["expected_products"])}
    present_set = set(present)
    missing = expected - present_set
    extra = present_set - expected
    if missing or extra:
        raise ValueError(
            f"worklist coverage mismatch vs manifest: missing={sorted(missing)} extra={sorted(extra)}"
        )

    labels: list[CalibrationLabel] = []
    for row in rows:
        gold = row.gold_verdict
        if not gold or not gold.strip():
            raise ValueError(f"product {row.brand}:{row.line} is unlabelled (blank gold_verdict)")
        if gold not in _GOLD_VERDICT_VALUES:
            raise ValueError(
                f"product {row.brand}:{row.line} has invalid gold_verdict {gold!r}; "
                f"expected one of {_GOLD_VERDICT_VALUES}"
            )
        labels.append(
            CalibrationLabel(
                creator_id=row.creator_id,
                brand=row.brand,
                line=row.line,
                gold_verdict=Verdict(gold),
                labeler=labeler,
                evidence_pointer=row.evidence_pointer,
                note=row.note,
            )
        )
    return labels
