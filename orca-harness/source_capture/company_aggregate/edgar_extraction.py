"""Deterministic employee-count extractor for EDGAR 10-K narrative (Layer-2, slice 04).

A pure, regex-based parser: 10-K Item-1 "Human Capital" narrative text in -> a structured
``EmployeeCountExtraction`` out (the count + value-quality + measurement-basis + the exact
source span). No I/O, no model imports -- fully offline-testable on synthetic snippets.
Extraction is REGEX/text-parsing, NOT an LLM, so the same text + same ``PARSER_VERSION`` /
``RULESET_SHA256`` reproduce the same value (the re-derivability the observation provenance
binds, AR-05).

Honesty (the load-bearing behaviour):
- a clean single reading -> ``found`` with quality ``exact`` | ``approximate``;
- multiple readings with DIFFERENT bases -> the PRIMARY headcount is chosen (``total`` is the
  canonical company figure) and the others are recorded as ``alternates`` -- the AR-03
  one-canonical-observation-per-filing rule, not a competing observation;
- multiple readings TIED at the top basis with conflicting values -> ``ambiguous`` (no single
  trustworthy value);
- no match -> not-found with a reason. Never a guessed number.

CONSERVATIVE ACCEPTANCE (cross-vendor review F-01): a bare "N <employee-noun>" phrase is NOT
enough -- a 10-K states many non-headcount employee counts (hiring/layoff events, regional or
segment subsets, union/benefit-plan counts, generic "people"). The extractor emits a KNOWN count
ONLY when the phrase is in a workforce-TOTAL context: it carries a workforce qualifier / FTE noun,
or a possession/as-of cue (had / employ(ed) / workforce / "as of ...") sits just before it; AND it
is not an event count (an event verb immediately before) AND not a scoped count (a segment/region/
benefit-plan phrase just after). Event / scoped / un-cued phrases are an HONEST MISS, never a
guessed KNOWN -- errors are pushed to the safe (miss) direction. A regex cannot catch every
non-headcount phrasing; the residual is a recorded limitation, not a silent guess.

Basis (cross-vendor review F-02) is read from the MATCHED qualifier + noun, not a pre-count window
scan, so a grammatical "a total of N full-time employees" is ``full_time`` (the qualifier on the
noun), not ``total`` (the "a total of" before the count).

v0 scope also does NOT match the "average number of employees was N" form (number AFTER the noun)
-> an honest not-found. A later ``PARSER_VERSION`` widens coverage; the provenance versions it.

``extraction_to_measure_facts`` bridges an extraction to the observation's honesty-typed measure
fields (``employee_count`` / ``employee_count_int`` / ``value_quality`` / ``measurement_basis``)
so it plugs straight into ``EdgarHeadcountObservation``.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from harness_utils import sha256_text
from source_capture.models import VisibleFact, known_fact, not_applicable, unknown_with_reason

PARSER_METHOD = "edgar_item1_employee_regex"
PARSER_VERSION = "v0"

# Number: comma-grouped (161,000) or a bare run of 3+ digits (12500). Requiring 3+ digits keeps
# 1-2 digit noise out; EDGAR 10-K filers are large enough that this is safe for v0.
_NUMBER = r"\d{1,3}(?:,\d{3})+|\d{3,}"
_APPROX = r"(?:approximately|approx\.?|about|roughly|nearly|~)"
_QUALIFIER = r"(?:full[-\s]time|part[-\s]time|total|salaried|hourly|regular|permanent)"
_NOUN = r"(?:full[-\s]time equivalents?|FTEs?|employees|persons|people|team members|associates)"

_PATTERN = re.compile(
    rf"(?P<approx>{_APPROX}\s+)?"
    rf"(?P<count>{_NUMBER})\s+"
    rf"(?P<between>(?:{_QUALIFIER}\s+){{0,2}})"
    rf"(?P<noun>{_NOUN})",
    re.IGNORECASE,
)

# Basis detection, highest priority first (full_time_equivalent must precede full_time since the
# former contains the latter). Each value is a member of observation.MEASUREMENT_BASIS_VALUES.
# Detection runs over the MATCHED qualifier+noun only (F-02), never a pre-count window.
_BASIS_RULES: tuple[tuple[str, int, re.Pattern[str]], ...] = (
    ("total", 3, re.compile(r"\btotal\b", re.IGNORECASE)),
    ("full_time_equivalent", 2, re.compile(r"full[-\s]time equivalent|\bFTEs?\b", re.IGNORECASE)),
    ("full_time", 2, re.compile(r"full[-\s]time", re.IGNORECASE)),
    ("average", 1, re.compile(r"\baverage\b", re.IGNORECASE)),
)
_UNSPECIFIED = "unspecified"

# Workforce-total context gates (F-01). A KNOWN count requires a positive workforce signal and
# the absence of an event / scoped context.
_POSSESSION_CUE = re.compile(
    r"\b(?:had|have|has|employ(?:s|ed|ing)?|workforce|head\s?count|personnel|staffed|staffing)\b"
    r"|\bas of\b",
    re.IGNORECASE,
)
_EVENT_VERB = re.compile(
    r"\b(?:hired|hire|hiring|added|adding|recruit(?:ed|ing)?|terminat(?:ed|ing)|laid\s+off|"
    r"lay\s+off|eliminat(?:ed|ing)|reduc(?:ed|ing)|lost|separat(?:ed|ing)|furlough(?:ed)?|"
    r"onboard(?:ed|ing)?)\b",
    re.IGNORECASE,
)
_SCOPING = re.compile(
    r"\bin\s+(?:\w+\s+){0,3}"
    r"(?:segment|region|division|countr\w*|jurisdiction\w*|facilit\w*|location\w*|subsidiar\w*|geograph\w*|market\w*)s?\b"
    r"|represented\s+by|covered\s+by|enrolled\s+in|participat\w*\s+in|attended\b"
    r"|under\s+(?:our|the)\s+\w+\s+plan",
    re.IGNORECASE,
)

# Bind the provenance to the actual ruleset: a rule change (pattern OR any acceptance gate) moves
# this hash, so a re-extraction is distinguishable from a new source observation.
RULESET_SHA256 = sha256_text(
    "|".join(
        [
            _PATTERN.pattern,
            *(f"{name}:{rule.pattern}" for name, _p, rule in _BASIS_RULES),
            f"possession:{_POSSESSION_CUE.pattern}",
            f"event:{_EVENT_VERB.pattern}",
            f"scoping:{_SCOPING.pattern}",
        ]
    )
)

# The basis/quality vocabularies this extractor can emit (guarded as subsets of the observation
# closed sets by test).
EXTRACTOR_BASIS_VALUES = frozenset({name for name, _p, _r in _BASIS_RULES} | {_UNSPECIFIED})
EXTRACTOR_QUALITY_VALUES = frozenset({"exact", "approximate", "ambiguous"})


@dataclass(frozen=True)
class EmployeeCountExtraction:
    found: bool
    count_int: int | None
    raw_value: str | None
    quality: str | None  # exact | approximate | ambiguous | None(not-found)
    basis: str
    char_start: int | None
    char_end: int | None
    matched_text: str | None
    reason: str
    alternates: list[str] = field(default_factory=list)


def extract_employee_count(text: str) -> EmployeeCountExtraction:
    if not isinstance(text, str) or not text.strip():
        return _not_found("empty filing text")

    candidates: list[_Candidate] = []
    for match in _PATTERN.finditer(text):
        raw = match.group("count")
        try:
            count_int = int(raw.replace(",", ""))
        except ValueError:
            continue
        if not _is_workforce_total_context(text, match):
            continue  # event / scoped / un-cued count -> honest miss, never a guessed KNOWN (F-01)
        basis, priority = _detect_basis(match.group("between"), match.group("noun"))
        candidates.append(
            _Candidate(
                count_int=count_int,
                raw=raw,
                approx=bool(match.group("approx")),
                basis=basis,
                priority=priority,
                start=match.start(),
                end=match.end(),
                matched=match.group(0),
            )
        )

    if not candidates:
        return _not_found("no workforce-total employee-count phrase matched in the filing text")

    distinct_values = {candidate.count_int for candidate in candidates}
    if len(distinct_values) == 1:
        return _from_candidate(_richest_basis(candidates), alternates=[])

    # Multiple distinct counts. Rank by basis priority; a unique top-priority candidate is the
    # primary headcount (AR-03), the rest are alternates. A tie at the top is genuinely
    # ambiguous.
    top_priority = max(candidate.priority for candidate in candidates)
    top = [candidate for candidate in candidates if candidate.priority == top_priority]
    top_values = {candidate.count_int for candidate in top}
    if len(top_values) > 1:
        return EmployeeCountExtraction(
            found=False,
            count_int=None,
            raw_value=None,
            quality="ambiguous",
            basis=_UNSPECIFIED,
            char_start=None,
            char_end=None,
            matched_text=None,
            reason=(
                "multiple distinct employee counts at the same basis priority; "
                f"no single primary figure: {sorted(top_values)}"
            ),
            alternates=sorted({candidate.raw for candidate in candidates}),
        )

    primary = _richest_basis(top)
    alternates = sorted({candidate.raw for candidate in candidates if candidate.count_int != primary.count_int})
    return _from_candidate(primary, alternates=alternates)


def extraction_to_measure_facts(
    extraction: EmployeeCountExtraction,
) -> tuple[VisibleFact, int | None, VisibleFact, VisibleFact]:
    """Map an extraction to the observation's (employee_count, employee_count_int,
    value_quality, measurement_basis) measure fields, honoring the honesty invariant."""
    if extraction.found and extraction.count_int is not None and extraction.raw_value is not None:
        return (
            known_fact(extraction.raw_value),
            extraction.count_int,
            known_fact(extraction.quality or "exact"),
            known_fact(extraction.basis),
        )
    if extraction.quality == "ambiguous":
        return (
            unknown_with_reason(extraction.reason),
            None,
            known_fact("ambiguous"),
            not_applicable("ambiguous extraction; no single measurement basis"),
        )
    return (
        unknown_with_reason(extraction.reason),
        None,
        not_applicable("no value extracted"),
        not_applicable("no value extracted"),
    )


@dataclass(frozen=True)
class _Candidate:
    count_int: int
    raw: str
    approx: bool
    basis: str
    priority: int
    start: int
    end: int
    matched: str


def _is_workforce_total_context(text: str, match: re.Match[str]) -> bool:
    """True only when the matched count reads as a workforce TOTAL (F-01).

    Reject event counts (an event verb just before the number) and scoped counts (a segment /
    region / benefit-plan phrase just after the noun). Then require a positive workforce signal:
    a workforce qualifier / FTE noun, or a possession/as-of cue in the preceding clause."""
    count_start = match.start("count")
    immediate_before = text[max(0, count_start - 25) : count_start]
    if _EVENT_VERB.search(immediate_before):
        return False
    after_noun = text[match.end("noun") : match.end("noun") + 30]
    if _SCOPING.search(after_noun):
        return False
    if _has_workforce_qualifier(match.group("between"), match.group("noun")):
        return True
    preceding = text[max(0, count_start - 90) : count_start]
    return bool(_POSSESSION_CUE.search(preceding))


def _has_workforce_qualifier(between: str, noun: str) -> bool:
    if between.strip():
        return True  # full-time / part-time / total / salaried / ... qualifies the noun
    return bool(re.search(r"full[-\s]time equivalent|\bFTEs?\b", noun, re.IGNORECASE))


def _detect_basis(between: str, noun: str) -> tuple[str, int]:
    context = f"{between} {noun}"
    for name, priority, rule in _BASIS_RULES:
        if rule.search(context):
            return name, priority
    return _UNSPECIFIED, 0


def _richest_basis(candidates: list[_Candidate]) -> _Candidate:
    # Among same-value (or top-tier) candidates, prefer the most informative basis, then the
    # earliest occurrence -- deterministic.
    return sorted(candidates, key=lambda c: (-c.priority, c.start))[0]


def _from_candidate(candidate: _Candidate, *, alternates: list[str]) -> EmployeeCountExtraction:
    return EmployeeCountExtraction(
        found=True,
        count_int=candidate.count_int,
        raw_value=candidate.raw,
        quality="approximate" if candidate.approx else "exact",
        basis=candidate.basis,
        char_start=candidate.start,
        char_end=candidate.end,
        matched_text=candidate.matched,
        reason="",
        alternates=alternates,
    )


def _not_found(reason: str) -> EmployeeCountExtraction:
    return EmployeeCountExtraction(
        found=False,
        count_int=None,
        raw_value=None,
        quality=None,
        basis=_UNSPECIFIED,
        char_start=None,
        char_end=None,
        matched_text=None,
        reason=reason,
    )
