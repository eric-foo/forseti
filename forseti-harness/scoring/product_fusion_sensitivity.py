"""Calibration sensitivity harness for Pass-2 product-verdict fusion (no-LLM, pure).

Makes the deterministic fusion's constants LEGIBLE before any calibration: given a set of
mentions it sweeps each ``FusionConfig`` knob and reports how the verdict + uncalibrated
scores move, and it scans the single-mention decision boundary (stance x confidence ->
verdict) that governs the "single-witness" behaviour. It changes NOTHING in the fusion; it
only re-runs it under perturbed configs and observes the result.

This is a CONSEQUENCE tool, not calibration: it shows what a constant DOES, never what it
SHOULD be. Picking constants needs a labeled corpus of real mentions + owner sign-off
(owner-deferred). The boundary facts it surfaces (single-witness bar, irony floor, saturation)
are PROPERTIES OF THE CONSTANTS -- true regardless of which data they run on -- so demonstrating
them on archetypal mentions is sound; the trap calibration must avoid is *choosing* constants
from synthetic data, which this tool does not do.

Procedure for the real corpus: docs/workflows/product_verdict_calibration_labeling_protocol_v0.md.
Findings + the current defaults' consequences:
docs/decisions/product_verdict_fusion_calibration_surface_v0.md.

No LLM, no network (scoring/ no-LLM zone). Imports only stdlib + the fusion module/schemas.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from math import atanh, inf

from schemas.product_mention_models import (
    Concentration,
    ProductMention,
    TranscriptSource,
    Verdict,
)
from scoring.product_fusion import (
    DEFAULT_FUSION_CONFIG,
    FusionConfig,
    fuse_product_verdicts,
)

# FusionConfig fields the harness may sweep, in calibration-priority order (risk dial first).
SWEEPABLE_KNOBS: tuple[str, ...] = (
    "material_min",
    "gain",
    "creator_authored_mult",
    "implicit_mult",
    "negation_mult",
    "dependence_exponent",
)

# Single-mention archetypes for the boundary scan: how the extractor flagged the mention.
ARCHETYPES: dict[str, dict[str, bool]] = {
    "authored": {"authored": True, "negated": False},
    "implicit": {"authored": False, "negated": False},
    "authored+irony": {"authored": True, "negated": True},
}

# Reproducible default sweep ranges (so the memo + __main__ demo are re-derivable).
DEFAULT_MATERIAL_MIN_SWEEP: tuple[float, ...] = (0.20, 0.30, 0.40, 0.50, 0.60)
DEFAULT_GAIN_SWEEP: tuple[float, ...] = (1.0, 1.5, 2.0, 3.0, 4.0)
DEFAULT_NEGATION_MULT_SWEEP: tuple[float, ...] = (0.0, 0.15, 0.30, 0.50, 1.0)
DEFAULT_BOUNDARY_STANCES: tuple[float, ...] = (0.2, 0.3, 0.5, 0.7, 1.0)
DEFAULT_BOUNDARY_CONFIDENCES: tuple[float, ...] = (0.3, 0.5, 0.7, 1.0)
DEFAULT_CORROBORATION_COUNTS: tuple[int, ...] = (1, 2, 3, 5)

_VERDICT_ABBR: dict[Verdict, str] = {
    Verdict.POSITIVE: "pos",
    Verdict.MIXED: "mix",
    Verdict.NEGATIVE: "neg",
    Verdict.UNKNOWN: "unk",
}


@dataclass(frozen=True)
class KnobSweepPoint:
    """One verdict outcome at one knob value, over a fixed mention set."""

    knob: str
    value: float
    verdict: Verdict
    support_score: float
    oppose_score: float


@dataclass(frozen=True)
class BoundaryCell:
    """One single-mention outcome: (stance, confidence) -> verdict under one archetype."""

    archetype: str
    stance: float
    confidence: float
    support_score: float
    oppose_score: float
    verdict: Verdict


@dataclass(frozen=True)
class CorroborationPoint:
    """Support score as N independent (different-video) max-stance mentions accumulate."""

    mention_count: int
    support_score: float
    verdict: Verdict


def min_clearing_raw(config: FusionConfig = DEFAULT_FUSION_CONFIG) -> float:
    """Idealized (pre-rounding) per-side raw where UNROUNDED support equals ``material_min``:
    ``atanh(material_min)/gain``.

    The "single-witness bar": for a lone authored mention (mult 1.0, dependence 1.0) the raw
    contribution is ``stance_vote * extractor_confidence``, so a product at or above this value
    decides a confident verdict. NOTE: fusion rounds support to 4 decimals BEFORE the
    ``>= material_min`` test, so the OPERATIONAL bar is marginally below this idealized value (and
    at ``material_min >= 1`` a large enough raw can still round up to 1.0000 and clear). Returns
    ``inf`` when unrounded support can never reach ``material_min`` (``material_min >= 1``) and
    ``0.0`` when it always does (``material_min <= 0``).
    """
    if config.material_min >= 1.0:
        return inf
    if config.material_min <= 0.0:
        return 0.0
    return atanh(config.material_min) / config.gain


def _demo_mention(
    stance: float,
    confidence: float,
    *,
    authored: bool,
    negated: bool,
    mention_id: str = "m",
    video_id: str = "v",
) -> ProductMention:
    """A minimal single-product mention for boundary/sweep probing (archetype-controlled)."""
    return ProductMention(
        mention_id=mention_id,
        video_id=video_id,
        transcript_anchor=f"asr:{video_id}",
        transcript_source=TranscriptSource.ASR,
        brand="brand",
        line="line",
        concentration=Concentration.UNKNOWN,
        stance_vote=stance,
        source_pointer="probe",
        start_ms=0,
        end_ms=1,
        creator_authored=authored,
        possible_negation_or_irony=negated,
        extractor_confidence=confidence,
    )


def _single_product_verdict(
    mentions: list[ProductMention], *, config: FusionConfig, creator_id: str = "sensitivity"
):
    """Fuse a SINGLE-product mention set and return the one verdict (``None`` if empty).

    Raises ``ValueError`` if the mentions span more than one ``(brand, line)`` product: the
    sweep/boundary tables describe ONE product, so silently reporting whichever sorts first would
    misrepresent a multi-product input (e.g. a real Phase C corpus).
    """
    verdict_set = fuse_product_verdicts(
        mentions, creator_id=creator_id, generated_at="sweep", config=config
    )
    if not verdict_set.verdicts:
        return None
    if len(verdict_set.verdicts) > 1:
        raise ValueError(
            f"sensitivity probes require a single-product mention set; got "
            f"{len(verdict_set.verdicts)} products"
        )
    return verdict_set.verdicts[0]


def sweep_knob(
    mentions: list[ProductMention],
    knob: str,
    values: tuple[float, ...],
    *,
    base_config: FusionConfig = DEFAULT_FUSION_CONFIG,
    creator_id: str = "sensitivity",
) -> list[KnobSweepPoint]:
    """Re-fuse a fixed (single-product) mention set across ``knob`` values; report each verdict.

    Every other knob stays at ``base_config``; only ``knob`` varies, so the result isolates that
    one constant's effect. Deterministic (no clock/RNG); inputs should be a single product.
    """
    if knob not in SWEEPABLE_KNOBS:
        raise ValueError(f"unknown knob {knob!r}; expected one of {SWEEPABLE_KNOBS}")
    points: list[KnobSweepPoint] = []
    for value in values:
        config = replace(base_config, **{knob: value})
        verdict = _single_product_verdict(mentions, config=config, creator_id=creator_id)
        if verdict is None:
            points.append(KnobSweepPoint(knob, value, Verdict.UNKNOWN, 0.0, 0.0))
        else:
            points.append(
                KnobSweepPoint(
                    knob,
                    value,
                    verdict.verdict,
                    verdict.uncalibrated_support_score,
                    verdict.uncalibrated_oppose_score,
                )
            )
    return points


def boundary_scan(
    *,
    archetype: str = "authored",
    stances: tuple[float, ...] = DEFAULT_BOUNDARY_STANCES,
    confidences: tuple[float, ...] = DEFAULT_BOUNDARY_CONFIDENCES,
    config: FusionConfig = DEFAULT_FUSION_CONFIG,
) -> list[BoundaryCell]:
    """Scan a lone mention's (stance x confidence) grid -> verdict, under one extractor archetype.

    This visualises the decision boundary a SINGLE mention faces -- the "single-witness" surface.
    """
    if archetype not in ARCHETYPES:
        raise ValueError(f"unknown archetype {archetype!r}; expected one of {sorted(ARCHETYPES)}")
    spec = ARCHETYPES[archetype]
    cells: list[BoundaryCell] = []
    for stance in stances:
        for confidence in confidences:
            mention = _demo_mention(
                stance, confidence, authored=spec["authored"], negated=spec["negated"]
            )
            verdict = _single_product_verdict([mention], config=config)
            assert verdict is not None  # a single mention always yields exactly one verdict
            cells.append(
                BoundaryCell(
                    archetype,
                    stance,
                    confidence,
                    verdict.uncalibrated_support_score,
                    verdict.uncalibrated_oppose_score,
                    verdict.verdict,
                )
            )
    return cells


def render_knob_sweep(points: list[KnobSweepPoint]) -> str:
    """Markdown table of a knob sweep: value | verdict | support | oppose."""
    if not points:
        return "(empty sweep)"
    knob = points[0].knob
    lines = [f"| {knob} | verdict | support | oppose |", "|---|---|---|---|"]
    for point in points:
        lines.append(
            f"| {point.value:g} | {point.verdict.value} | "
            f"{point.support_score:.4f} | {point.oppose_score:.4f} |"
        )
    return "\n".join(lines)


def corroboration_curve(
    counts: tuple[int, ...] = DEFAULT_CORROBORATION_COUNTS,
    *,
    archetype: str = "authored",
    config: FusionConfig = DEFAULT_FUSION_CONFIG,
) -> list[CorroborationPoint]:
    """Fuse N independent (different-video) max-stance mentions for each N; report the score.

    Surfaces SATURATION: past the first strong mention the squashed score barely rises, so the
    score is near-binary rather than an "endorsement intensity" measure.
    """
    if archetype not in ARCHETYPES:
        raise ValueError(f"unknown archetype {archetype!r}; expected one of {sorted(ARCHETYPES)}")
    spec = ARCHETYPES[archetype]
    points: list[CorroborationPoint] = []
    for count in counts:
        mentions = [
            _demo_mention(
                1.0,
                1.0,
                authored=spec["authored"],
                negated=spec["negated"],
                mention_id=f"m{index}",
                video_id=f"v{index}",
            )
            for index in range(count)
        ]
        verdict = _single_product_verdict(mentions, config=config) if mentions else None
        if verdict is None:
            points.append(CorroborationPoint(count, 0.0, Verdict.UNKNOWN))
        else:
            points.append(
                CorroborationPoint(count, verdict.uncalibrated_support_score, verdict.verdict)
            )
    return points


def render_corroboration_curve(points: list[CorroborationPoint]) -> str:
    """Markdown table: mentions | support | verdict (support shown to 5dp to expose saturation)."""
    if not points:
        return "(empty curve)"
    lines = ["| mentions | support | verdict |", "|---|---|---|"]
    for point in points:
        lines.append(f"| {point.mention_count} | {point.support_score:.5f} | {point.verdict.value} |")
    return "\n".join(lines)


def render_boundary_scan(cells: list[BoundaryCell]) -> str:
    """Markdown grid: rows = stance, cols = confidence, cell = verdict abbreviation."""
    if not cells:
        return "(empty scan)"
    archetype = cells[0].archetype
    stances: list[float] = []
    confidences: list[float] = []
    for cell in cells:
        if cell.stance not in stances:
            stances.append(cell.stance)
        if cell.confidence not in confidences:
            confidences.append(cell.confidence)
    by_key = {(cell.stance, cell.confidence): cell.verdict for cell in cells}
    header = f"| {archetype} | " + " | ".join(f"conf {c:g}" for c in confidences) + " |"
    divider = "|---|" + "|".join("---" for _ in confidences) + "|"
    lines = [header, divider]
    for stance in stances:
        row = [f"stance {stance:g}"]
        for confidence in confidences:
            row.append(_VERDICT_ABBR[by_key[(stance, confidence)]])
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def build_default_report(config: FusionConfig = DEFAULT_FUSION_CONFIG) -> str:
    """Assemble the canonical illustrative report (used by ``__main__`` and pasted into the memo).

    ARCHETYPAL inputs only -- this shows what the constants DO, not what real creators said.
    """
    # A borderline implicit mention (score near the abstain line) so the material_min risk dial
    # visibly flips the verdict; a saturated strong product would be insensitive to it.
    borderline = [_demo_mention(0.5, 0.6, authored=False, negated=False)]
    parts = [
        "# product_fusion sensitivity report (illustrative archetypes, NOT calibration data)",
        "",
        f"Config: gain={config.gain:g} material_min={config.material_min:g} "
        f"authored={config.creator_authored_mult:g} implicit={config.implicit_mult:g} "
        f"negation={config.negation_mult:g} dependence_exp={config.dependence_exponent:g}",
        f"Single-witness bar [idealized, pre-rounding] (min stance*conf that decides a lone "
        f"authored verdict): {min_clearing_raw(config):.4f}",
        "",
        "## material_min sweep (one borderline implicit mention, stance 0.5 x conf 0.6)",
        render_knob_sweep(
            sweep_knob(borderline, "material_min", DEFAULT_MATERIAL_MIN_SWEEP, base_config=config)
        ),
        "",
        "## corroboration curve (N independent max authored mentions -- saturation)",
        render_corroboration_curve(
            corroboration_curve(DEFAULT_CORROBORATION_COUNTS, archetype="authored", config=config)
        ),
        "",
        "## negation_mult sweep (one authored, irony-flagged, max stance/confidence)",
        render_knob_sweep(
            sweep_knob(
                [_demo_mention(1.0, 1.0, authored=True, negated=True)],
                "negation_mult",
                DEFAULT_NEGATION_MULT_SWEEP,
                base_config=config,
            )
        ),
        "",
        "## boundary scan -- authored archetype (single mention)",
        render_boundary_scan(boundary_scan(archetype="authored", config=config)),
        "",
        "## boundary scan -- authored+irony archetype (single mention)",
        render_boundary_scan(boundary_scan(archetype="authored+irony", config=config)),
    ]
    return "\n".join(parts)


if __name__ == "__main__":  # pragma: no cover - thin CLI for re-deriving the report
    print(build_default_report())
