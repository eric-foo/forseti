"""Layer-2b derived entity projection for the company-aggregate forward signal (EDGAR).

Computed-on-read, NOT persisted as truth: folds the immutable, append-only observation log
(Layer 2a, ``EdgarHeadcountObservation``) into an ordered company-headcount series. The fold =
resolve (via an injected, versioned ``ResolutionMap`` port) -> group into per-``(resolution,
source)`` lanes -> collapse supersession chains -> order by ``period_of_report`` -> surface
conflicts. The immutable log is never touched; re-running the fold with a different map / version
re-derives a different projection from the same log.

Identity honesty (AR-04 / AR-05, the #1 ownership boundary): the projection emits
``provisional_filer_key`` + ``resolution_state``, and a canonical ``entity_key`` ONLY when the
injected map resolves it (the v0 ``PassthroughNullResolutionMap`` never does). A CIK is a *filer*
id, not a company id, so the v0 series is honestly a **filer-level UNRESOLVED trend** -- every
consumer sees ``resolution_state='unresolved'`` and must not treat it as canonical. This lane
authors no resolution and performs no economic merge/rollup (spine-owned, hard-STOP, AR-01).

Reproducibility (AR-06): every projection pins ``(map_version, resolver_version, event_ordering,
conflict_rule)``. A read pins a version; it never floats to "latest."
"""
from __future__ import annotations

from pydantic import Field, field_validator, model_validator

from schemas.case_models import StrictModel
from source_capture.company_aggregate.entity_resolution_port import (
    DEFAULT_RESOLUTION_MAP,
    ResolutionMap,
)
from source_capture.company_aggregate.observation import EdgarHeadcountObservation
from source_capture.models import (
    VisibleFact,
    VisibleFactStatus,
    known_fact,
    not_applicable,
    unknown_with_reason,
)

COMPANY_HEADCOUNT_PROJECTION_SCHEMA_VERSION = "company_headcount_projection_v0"

POINT_STATE_VALUES = frozenset({"single", "conflict"})
EVENT_ORDERING_VALUES = frozenset({"period_of_report_asc", "period_of_report_desc"})
CONFLICT_RULE_VALUES = frozenset({"surface_both"})

PROJECTION_NON_CLAIMS = [
    "DERIVED, computed-on-read; not persisted as truth, not a canonical record",
    "filer-level UNRESOLVED trend when resolution_state=unresolved: a CIK is a filer id, NOT a "
    "canonical company id (AR-04)",
    "provisional_filer_key is NOT a canonical entity_key; entity resolution is the (unbuilt) "
    "spine's authority (AR-05, #1 ownership boundary)",
    "per-source lane, source-tagged; sources are NOT inter-converted",
    "no economic merge/rollup; that is spine-authored and a hard-STOP for this lane (AR-01)",
    "cross-year / cross-company comparability NOT established",
    "not validated, not ECR-ready until rebound under a Decision Frame",
]


class ObservationPointRef(StrictModel):
    """An auditable pointer from a series point back to one contributing observation."""

    accession_number: str
    filing_date: str
    packet_id: str
    evidence_slice_id: str
    run_id: str
    employee_count_int: int | None = Field(default=None, ge=0)
    measurement_basis: str | None = None


class HeadcountPoint(StrictModel):
    """One point in the ordered series, for a single ``period_of_report``.

    ``single`` = one trustworthy reading (identical re-derivations collapse). ``conflict`` =
    two-or-more observations with differing values at the same period and no supersession edge to
    resolve them -> surfaced honestly with NO single value (conflict_rule='surface_both')."""

    period_of_report: str
    point_state: str
    employee_count: VisibleFact
    employee_count_int: int | None = Field(default=None, ge=0)
    value_quality: VisibleFact
    measurement_basis: VisibleFact
    observation_refs: list[ObservationPointRef] = Field(min_length=1)
    superseded_refs: list[ObservationPointRef] = Field(default_factory=list)

    @field_validator("point_state")
    @classmethod
    def validate_point_state(cls, value: str) -> str:
        if value not in POINT_STATE_VALUES:
            allowed = ", ".join(sorted(POINT_STATE_VALUES))
            raise ValueError(f"point_state must be one of {{{allowed}}}; got {value!r}")
        return value

    @model_validator(mode="after")
    def validate_point(self) -> "HeadcountPoint":
        known = self.employee_count.status == VisibleFactStatus.KNOWN
        if known and self.employee_count_int is None:
            raise ValueError("a KNOWN point employee_count must carry employee_count_int")
        if not known and self.employee_count_int is not None:
            raise ValueError("employee_count_int may be set only when employee_count is KNOWN")
        if self.point_state == "conflict":
            if known:
                raise ValueError("a 'conflict' point must not carry a single KNOWN count")
            if len(self.observation_refs) < 2:
                raise ValueError("a 'conflict' point must surface >= 2 observations")
        return self


class CompanyHeadcountProjection(StrictModel):
    """One per-``(resolution, source)`` lane: the derived, version-pinned headcount series."""

    schema_version: str = COMPANY_HEADCOUNT_PROJECTION_SCHEMA_VERSION

    # Resolution identity (AR-04/05): provisional filer key always; entity_key only when resolved.
    provisional_filer_key: str
    entity_key: str | None = None
    resolution_state: str
    source: str

    # Version binding (AR-06): a read pins these, never floats to "latest".
    map_version: str
    resolver_version: str
    event_ordering: str
    conflict_rule: str

    points: list[HeadcountPoint] = Field(default_factory=list)
    non_claims: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)

    @field_validator("schema_version")
    @classmethod
    def validate_schema_version(cls, value: str) -> str:
        if value != COMPANY_HEADCOUNT_PROJECTION_SCHEMA_VERSION:
            raise ValueError(
                f"schema_version must be {COMPANY_HEADCOUNT_PROJECTION_SCHEMA_VERSION!r}; got {value!r}"
            )
        return value

    @field_validator("provisional_filer_key", "resolution_state", "source", "map_version", "resolver_version", "event_ordering", "conflict_rule")
    @classmethod
    def reject_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("CompanyHeadcountProjection string fields must be non-empty")
        return value

    @model_validator(mode="after")
    def validate_identity_honesty(self) -> "CompanyHeadcountProjection":
        if self.resolution_state not in {"unresolved", "resolved"}:
            raise ValueError(f"resolution_state must be 'unresolved' or 'resolved'; got {self.resolution_state!r}")
        # AR-05: an unresolved projection must never carry a canonical entity_key.
        if self.resolution_state == "unresolved" and self.entity_key is not None:
            raise ValueError("an unresolved projection must not carry a canonical entity_key (AR-05)")
        if self.resolution_state == "resolved" and not (self.entity_key and self.entity_key.strip()):
            raise ValueError("a resolved projection must carry a non-empty entity_key")
        return self


def project_company_headcount(
    observations: list[EdgarHeadcountObservation],
    *,
    resolution_map: ResolutionMap = DEFAULT_RESOLUTION_MAP,
    event_ordering: str = "period_of_report_asc",
    conflict_rule: str = "surface_both",
) -> list[CompanyHeadcountProjection]:
    """Fold an observation log into one version-pinned series per ``(resolution, source)`` lane.

    ``resolution_map`` is injected and consumed, never authored here (the #1 boundary). The default
    passthrough-null leaves every lane filer-level unresolved.
    """
    if event_ordering not in EVENT_ORDERING_VALUES:
        allowed = ", ".join(sorted(EVENT_ORDERING_VALUES))
        raise ValueError(f"event_ordering must be one of {{{allowed}}}; got {event_ordering!r}")
    if conflict_rule not in CONFLICT_RULE_VALUES:
        allowed = ", ".join(sorted(CONFLICT_RULE_VALUES))
        raise ValueError(f"conflict_rule must be one of {{{allowed}}}; got {conflict_rule!r}")

    lanes: dict[tuple[str, str], dict] = {}
    for observation in observations:
        outcome = resolution_map.resolve(source=observation.key.source, cik=observation.key.cik)
        group = outcome.entity_key if outcome.resolution_state == "resolved" else outcome.provisional_filer_key
        lane_key = (group, observation.key.source)
        lane = lanes.setdefault(lane_key, {"outcome": outcome, "observations": []})
        lane["observations"].append(observation)

    projections: list[CompanyHeadcountProjection] = []
    for lane_key in sorted(lanes):
        lane = lanes[lane_key]
        outcome = lane["outcome"]
        projections.append(
            CompanyHeadcountProjection(
                provisional_filer_key=outcome.provisional_filer_key,
                entity_key=outcome.entity_key,
                resolution_state=outcome.resolution_state,
                source=lane_key[1],
                map_version=resolution_map.map_version,
                resolver_version=resolution_map.resolver_version,
                event_ordering=event_ordering,
                conflict_rule=conflict_rule,
                points=_build_points(lane["observations"], event_ordering=event_ordering),
                non_claims=list(PROJECTION_NON_CLAIMS),
            )
        )
    return projections


def _build_points(
    observations: list[EdgarHeadcountObservation], *, event_ordering: str
) -> list[HeadcountPoint]:
    by_period: dict[str, list[EdgarHeadcountObservation]] = {}
    for observation in observations:
        by_period.setdefault(observation.key.period_of_report, []).append(observation)

    periods = sorted(by_period, reverse=event_ordering == "period_of_report_desc")
    points: list[HeadcountPoint] = []
    for period in periods:
        group = sorted(by_period[period], key=lambda o: o.key.accession_number)
        active, superseded = _split_supersession(group)
        refs = [_ref(o) for o in active]
        superseded_refs = [_ref(o) for o in superseded]
        signatures = {_value_signature(o) for o in active}
        if len(signatures) <= 1:
            representative = active[0]
            points.append(
                HeadcountPoint(
                    period_of_report=period,
                    point_state="single",
                    employee_count=representative.employee_count,
                    employee_count_int=representative.employee_count_int,
                    value_quality=_collapse_quality(active),
                    measurement_basis=representative.measurement_basis,
                    observation_refs=refs,
                    superseded_refs=superseded_refs,
                )
            )
        else:
            reason = (
                f"multiple conflicting observations at period {period}: "
                + ", ".join(_describe(o) for o in active)
            )
            points.append(
                HeadcountPoint(
                    period_of_report=period,
                    point_state="conflict",
                    employee_count=unknown_with_reason(reason),
                    employee_count_int=None,
                    value_quality=known_fact("ambiguous"),
                    measurement_basis=not_applicable("conflicting observations; no single basis"),
                    observation_refs=refs,
                    superseded_refs=superseded_refs,
                )
            )
    return points


def _split_supersession(
    group: list[EdgarHeadcountObservation],
) -> tuple[list[EdgarHeadcountObservation], list[EdgarHeadcountObservation]]:
    """A 'supersede' edge marks its prior observation as collapsed (kept in the log, off the point)."""
    superseded_keys = {
        o.supersedes.prior.key.canonical_key()
        for o in group
        if o.supersedes is not None and o.supersedes.relationship == "supersede"
    }
    active = [o for o in group if o.key.canonical_key() not in superseded_keys]
    superseded = [o for o in group if o.key.canonical_key() in superseded_keys]
    if not active:  # defensive: never drop the whole period
        return group, []
    return active, superseded


def _value_signature(observation: EdgarHeadcountObservation) -> tuple:
    return (
        observation.employee_count.status,
        observation.employee_count_int,
        _known_value(observation.measurement_basis),
    )


def _collapse_quality(active: list[EdgarHeadcountObservation]) -> VisibleFact:
    """Conservative, deterministic value_quality for a collapsed single point (F-03).

    Same-value observations may disagree on quality (exact vs approximate). Rather than silently
    inheriting whichever accession sorts first, never overstate precision: if any contributor is
    'approximate', the point is approximate. ``active`` is accession-sorted, so this is
    deterministic."""
    for observation in active:
        if _known_value(observation.value_quality) == "approximate":
            return observation.value_quality
    return active[0].value_quality


def _ref(observation: EdgarHeadcountObservation) -> ObservationPointRef:
    return ObservationPointRef(
        accession_number=observation.key.accession_number,
        filing_date=observation.filing_date,
        packet_id=observation.packet_id,
        evidence_slice_id=observation.evidence_slice_id,
        run_id=observation.extraction.run_id,
        employee_count_int=observation.employee_count_int,
        measurement_basis=_known_value(observation.measurement_basis),
    )


def _describe(observation: EdgarHeadcountObservation) -> str:
    count = observation.employee_count_int if observation.employee_count_int is not None else "absent"
    return f"{observation.key.accession_number}={count}"


def _known_value(fact: VisibleFact) -> str | None:
    return fact.value if fact.status == VisibleFactStatus.KNOWN else None
