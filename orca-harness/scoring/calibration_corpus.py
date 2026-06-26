"""Phase B answer-key machinery for product-verdict calibration (no-LLM, pure).

Real calibration needs ground truth: the owner's OWN verdict on real mentions, against which the
fusion's constants are tuned in Phase C. This module is the machinery that lets the owner PRODUCE
that ground truth. It does NOT produce labels itself -- an agent labelling them would be circular --
and it captures nothing.

Three pieces:
  - ``CalibrationLabel``              : one owner-authored gold verdict per (creator, brand, line).
  - ``build_blind_labeling_worklist`` : mentions -> a fill-in YAML showing the QUOTES but no machine
                                        verdict, so the owner labels blind (no circular calibration).
  - ``load_labels_from_worklist``     : the filled worklist -> validated ``CalibrationLabel`` records,
                                        enforcing that every surfaced product is labelled.

BLINDNESS is structural: this module never imports the fusion verdict, so a worklist cannot leak it.
The real corpus needs the owner's live captures + blind labels; this is offline machinery only and
produces no labels and no calibration by itself.

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


def _brand_line_key(brand: str, line: str) -> tuple[str, str]:
    """Normalized grouping key (casing/whitespace-insensitive).

    Mirrors ``product_fusion``'s grouping so worklist products line up with fusion verdicts; Phase C
    normalizes both sides identically when matching a label to a verdict.
    """
    return (brand.strip().lower(), line.strip().lower())


def build_blind_labeling_worklist(mentions: list[ProductMention], *, creator_id: str) -> str:
    """Render a BLIND fill-in YAML worklist: quotes per product + a blank gold_verdict, no verdict.

    Groups ``mentions`` by normalized (brand, line); for each product lists the verified quotes and
    the contributing mention ids, with an empty ``gold_verdict`` for the owner to fill. Deterministic
    (products and ids sorted). Reads ONLY mentions -- never the fusion -- so it cannot leak a verdict.
    """
    if not creator_id or not creator_id.strip():
        raise ValueError("build_blind_labeling_worklist requires a non-empty creator_id")

    grouped: dict[tuple[str, str], list[ProductMention]] = defaultdict(list)
    display: dict[tuple[str, str], tuple[str, str]] = {}
    for mention in mentions:
        key = _brand_line_key(mention.brand, mention.line)
        grouped[key].append(mention)
        display.setdefault(key, (mention.brand, mention.line))  # first-seen original casing

    allowed = " | ".join(_GOLD_VERDICT_VALUES)
    lines = [
        f"# BLIND labeling worklist -- creator {creator_id}",
        f"# Read the quotes and set each gold_verdict to ONE of: {allowed}.",
        "# Label from the quotes alone. Do NOT consult any machine/fusion output -- that would make",
        "# calibration circular. 'unknown' is a valid, expected answer; do not force a call.",
        "products:",
    ]
    for key in sorted(grouped):
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


def load_labels_from_worklist(source: str, *, labeler: str = "owner") -> list[CalibrationLabel]:
    """Parse a filled blind worklist into validated ``CalibrationLabel`` records.

    ``source`` is the worklist YAML text (path-agnostic; the caller owns where the file lives).
    Raises ``ValueError`` if any surfaced product is left unlabelled (blank ``gold_verdict``) or
    carries an invalid verdict -- coverage is required so an abstention is recorded as an explicit
    ``unknown`` rather than silently dropped.
    """
    parsed = yaml.safe_load(source) or {}
    if not isinstance(parsed, dict) or "products" not in parsed:
        raise ValueError("worklist must be a mapping with a 'products' list")
    products = parsed["products"]
    if not isinstance(products, list) or not products:
        raise ValueError("worklist 'products' must be a non-empty list")

    labels: list[CalibrationLabel] = []
    for index, product in enumerate(products):
        if not isinstance(product, dict):
            raise ValueError(f"product #{index} must be a mapping")
        gold = product.get("gold_verdict")
        if gold is None or (isinstance(gold, str) and not gold.strip()):
            raise ValueError(
                f"product {product.get('brand', '?')}:{product.get('line', '?')} is "
                f"unlabelled (blank gold_verdict)"
            )
        if gold not in _GOLD_VERDICT_VALUES:
            raise ValueError(
                f"product #{index} has invalid gold_verdict {gold!r}; "
                f"expected one of {_GOLD_VERDICT_VALUES}"
            )
        labels.append(
            CalibrationLabel(
                creator_id=product.get("creator_id", ""),
                brand=product.get("brand", ""),
                line=product.get("line", ""),
                gold_verdict=Verdict(gold),
                labeler=labeler,
                evidence_pointer=list(product.get("evidence_pointer") or []),
                note=product.get("note") or "",
            )
        )
    return labels
