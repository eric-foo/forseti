"""Layer-2a immutable observation for the company-aggregate forward signal (EDGAR).

The DURABLE, append-only record of one company-headcount reading extracted from a
single SEC EDGAR filing. It is keyed ONLY on durable source facts -- never on a
(provisional) canonical company identity: ``entity_key`` does not exist here. The
company-by-company series is a SEPARATE derived projection (Layer 2b, a later slice)
that resolves identity on read; this immutable record must never carry it (revised
architecture, AR-01/AR-02/AR-06).

Why ``measurement_basis`` is NOT in the identity key (AR-03 resolution): basis is
extraction-determined, so putting it in the immutable key would FORK identity on a
re-extraction that reclassifies the basis -- breaking the re-extraction-keeps-identity
model (AR-05). Instead the key is the 4-tuple ``(source, cik, accession_number,
period_of_report)`` under a ONE-CANONICAL-OBSERVATION-PER-FILING invariant: the extractor
emits the single primary headcount (basis a non-key attribute); other counts stated in the
same filing are flagged in ``alternates``, not stored as competing observations. Enforcing
that uniqueness across the append-only log is the series writer's job (a later slice); this
module fixes the shape.

Reuses, never forks: ``VisibleFact`` honesty discipline and ``RE_CAPTURE_RELATIONSHIP_VALUES``
from ``source_capture.models``, plus the closed-vocabulary validator idiom
(``_require_closed_posture``) -- a known VisibleFact VALUE drawn from a frozenset, with
``not_attempted`` / ``not_applicable`` / ``unknown_with_reason`` carrying everything off the
closed set.

NON-CLAIMS: raw observation only; a NARRATIVE-extracted figure from one 10-K's Item-1 Human
Capital text (EDGAR exposes no structured employee count); not validated, not ECR-ready until
rebound under a Decision Frame; cross-year/cross-company comparability NOT established. This
module is the immutable observation SHAPE only -- no entity resolution, no projection, no
persistence, and no extraction logic (those are later slices).
"""
from __future__ import annotations

from pydantic import Field, field_validator, model_validator

from schemas.case_models import StrictModel
from source_capture.models import (
    RE_CAPTURE_RELATIONSHIP_VALUES,
    VisibleFact,
    VisibleFactStatus,
    _require_closed_posture,
)

EDGAR_HEADCOUNT_OBSERVATION_SCHEMA_VERSION = "edgar_headcount_observation_v0"
EDGAR_SOURCE = "sec_edgar"

# Closed value vocabularies (a known VisibleFact value must be drawn from the set; everything
# else is carried by unknown_with_reason / not_attempted / not_applicable). Same discipline as
# the Ob.9/Ob.10/Ob.15 closed postures in source_capture.models.
VALUE_QUALITY_VALUES = frozenset({"exact", "approximate", "ambiguous"})
MEASUREMENT_BASIS_VALUES = frozenset(
    {"full_time", "full_time_equivalent", "total", "average", "segment", "unspecified"}
)
SPAN_LOCATOR_KIND_VALUES = frozenset({"char_offset_range"})


class EdgarObservationKey(StrictModel):
    """The durable identity: filing facts only, never a (provisional) entity id."""

    source: str
    cik: str
    accession_number: str
    period_of_report: str

    @field_validator("cik", "accession_number", "period_of_report")
    @classmethod
    def reject_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("EdgarObservationKey fields must be non-empty")
        return value

    @field_validator("source")
    @classmethod
    def source_is_edgar(cls, value: str) -> str:
        if value != EDGAR_SOURCE:
            raise ValueError(
                f"source must be {EDGAR_SOURCE!r} for an EDGAR observation; got {value!r}"
            )
        return value

    def canonical_key(self) -> str:
        return "|".join(
            [self.source, self.cik, self.accession_number, self.period_of_report]
        )


class ExtractionSpan(StrictModel):
    """Where, inside the immutable preserved filing bytes, the count was read -- the
    re-derivable receipt (full-filing in Layer 1; span selection in Layer 2, AR-04)."""

    preserved_file_id: str
    relative_packet_path: str
    source_sha256: str
    locator_kind: str
    char_start: int = Field(ge=0)
    char_end: int = Field(ge=0)
    excerpt_sha256: str
    matched_text: str

    @field_validator("locator_kind")
    @classmethod
    def validate_locator_kind(cls, value: str) -> str:
        if value not in SPAN_LOCATOR_KIND_VALUES:
            allowed = ", ".join(sorted(SPAN_LOCATOR_KIND_VALUES))
            raise ValueError(
                f"locator_kind must be one of {{{allowed}}}; got {value!r}"
            )
        return value

    @model_validator(mode="after")
    def validate_span(self) -> "ExtractionSpan":
        if self.char_end < self.char_start:
            raise ValueError(
                f"char_end ({self.char_end}) must be >= char_start ({self.char_start})"
            )
        return self


class ExtractionProvenance(StrictModel):
    """Deterministic parser identity so a value is auditable and re-derivable (AR-05).

    Extraction is regex / text-parsing, NOT an LLM: same filing bytes + same
    ``parser_version`` + ``ruleset_sha256`` reproduce the same value. ``run_id`` /
    ``derived_at`` are audit metadata only -- never identity, never inputs to a value."""

    parser_method: str
    parser_version: str
    ruleset_sha256: str
    run_id: str
    derived_at: str

    @field_validator("parser_method", "parser_version", "ruleset_sha256", "run_id", "derived_at")
    @classmethod
    def reject_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("ExtractionProvenance fields must be non-empty")
        return value


class ObservationRef(StrictModel):
    """A pointer to a prior observation (durable key + the extraction that produced it)."""

    key: EdgarObservationKey
    parser_version: str
    run_id: str

    @field_validator("parser_version", "run_id")
    @classmethod
    def reject_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("ObservationRef fields must be non-empty")
        return value


class HeadcountSupersession(StrictModel):
    """A supersession edge to a prior observation. Reuses the Ob.15
    ``RE_CAPTURE_RELATIONSHIP_VALUES`` vocabulary verbatim (supersede / supplement /
    conflict / mixed) rather than inventing a parallel one."""

    relationship: str
    prior: ObservationRef
    reason: str

    @field_validator("relationship")
    @classmethod
    def validate_relationship(cls, value: str) -> str:
        if value not in RE_CAPTURE_RELATIONSHIP_VALUES:
            allowed = ", ".join(sorted(RE_CAPTURE_RELATIONSHIP_VALUES))
            raise ValueError(
                f"relationship must be one of {{{allowed}}} (reused Ob.15 vocabulary); got {value!r}"
            )
        return value

    @field_validator("reason")
    @classmethod
    def reject_blank_reason(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("HeadcountSupersession.reason must be non-empty")
        return value


class EdgarHeadcountObservation(StrictModel):
    """One immutable, append-only company-headcount reading from a single EDGAR filing.

    Carries NO entity identity (no ``entity_key`` / ``provisional_filer_key`` /
    ``resolution_state``) -- those belong only to the derived Layer-2b projection."""

    schema_version: str = EDGAR_HEADCOUNT_OBSERVATION_SCHEMA_VERSION
    key: EdgarObservationKey

    # Structured filing facts (KNOWN at source from EDGAR submission metadata; carried, not
    # narrative-extracted). period_of_report (the trend-ordering as-of) lives in the key.
    form_type: str
    filing_date: str

    # The measure. employee_count is the honesty primitive (KNOWN -> value is the as-stated
    # figure; else a named absence + reason). employee_count_int is the parsed integer,
    # present ONLY when the count is KNOWN -- absence is never a silent null int.
    employee_count: VisibleFact
    employee_count_int: int | None = Field(default=None, ge=0)
    value_quality: VisibleFact
    measurement_basis: VisibleFact

    extraction_span: ExtractionSpan
    extraction: ExtractionProvenance
    supersedes: HeadcountSupersession | None = None

    # Packet provenance -- the ECR binding handle (packet_id, evidence_slice_id), referenced
    # never replaced; manifest_sha256 + the span's source_sha256 make the reading re-verifiable.
    packet_id: str
    evidence_slice_id: str
    manifest_sha256: str

    # AR-03 one-canonical-per-filing: other counts stated in the same filing are flagged here,
    # not stored as competing observations.
    alternates: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    non_claims: list[str] = Field(default_factory=list)

    @field_validator("schema_version")
    @classmethod
    def validate_schema_version(cls, value: str) -> str:
        if value != EDGAR_HEADCOUNT_OBSERVATION_SCHEMA_VERSION:
            raise ValueError(
                f"schema_version must be {EDGAR_HEADCOUNT_OBSERVATION_SCHEMA_VERSION!r}; got {value!r}"
            )
        return value

    @field_validator("form_type", "filing_date", "packet_id", "evidence_slice_id", "manifest_sha256")
    @classmethod
    def reject_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("EdgarHeadcountObservation string fields must be non-empty")
        return value

    @model_validator(mode="after")
    def validate_closed_vocabularies(self) -> "EdgarHeadcountObservation":
        _require_closed_posture(
            self.value_quality, allowed=VALUE_QUALITY_VALUES, field="value_quality", obligation="AR-03"
        )
        _require_closed_posture(
            self.measurement_basis,
            allowed=MEASUREMENT_BASIS_VALUES,
            field="measurement_basis",
            obligation="AR-07",
        )
        return self

    @model_validator(mode="after")
    def validate_honesty(self) -> "EdgarHeadcountObservation":
        known = self.employee_count.status == VisibleFactStatus.KNOWN
        if known and self.employee_count_int is None:
            raise ValueError("a KNOWN employee_count must carry a parsed employee_count_int")
        if not known and self.employee_count_int is not None:
            raise ValueError(
                "employee_count_int may be set only when employee_count.status is KNOWN "
                "(absence is a named VisibleFact state, never a silent int)"
            )
        if self.value_quality.status == VisibleFactStatus.KNOWN:
            quality = self.value_quality.value
            if quality == "ambiguous" and known:
                raise ValueError(
                    "value_quality 'ambiguous' requires employee_count to be non-KNOWN "
                    "(ambiguous means no single trustworthy value)"
                )
            if quality in {"exact", "approximate"} and not known:
                raise ValueError(
                    f"value_quality {quality!r} requires a KNOWN employee_count"
                )
        return self
