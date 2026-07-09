"""ECR (Evidence Candidate Record) source-side models -- SP-3 timing slice.

Slice-1 of the ECR source-side field schema ratified in
``docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`` (387b630).
This module realizes ONLY the SP-3 row (source-side pre-decision timing/cutoff
posture) of the four-field schema. SP-1 / SP-2 / SP-6 rows are deferred and may
be added later without reshaping these models.

Design constraints (do not relax without explicit owner authorization):

- M1 carry, no coining: the cutoff vocabulary is single-sourced from
  ``source_capture.models.CUTOFF_POSTURE_VALUES`` and the residual status from
  ``source_capture.models.VisibleFactStatus``. This module declares no parallel
  posture vocabulary (validation-gates.md: "enumerate once; reference it").
- Derived source-side posture only. It does NOT bind ``EvidenceUnit``, map to
  ``pre_decision_status``, or make any JSG-01, scoring, or readiness claim.
"""
from __future__ import annotations

from enum import StrEnum

from pydantic import model_validator

from schemas.case_models import StrictModel
from source_capture.models import CUTOFF_POSTURE_VALUES, VisibleFactStatus

# A residual exists exactly when the producer did NOT assert a KNOWN cutoff
# posture; KNOWN is excluded because a known value is carried (M1), never
# recorded as a residual. Derived from the single-sourced VisibleFactStatus so
# no status vocabulary is re-declared here.
RESIDUAL_TIMING_STATUSES = frozenset(VisibleFactStatus) - {VisibleFactStatus.KNOWN}


class EcrTimingResidual(StrictModel):
    """Named residual (M3) for a slice whose cutoff posture is not KNOWN.

    Carries the producer's own non-known ``VisibleFact`` status and reason
    verbatim; it coins no posture vocabulary of its own.
    """

    status: VisibleFactStatus
    reason: str

    @model_validator(mode="after")
    def validate_residual(self) -> "EcrTimingResidual":
        if self.status not in RESIDUAL_TIMING_STATUSES:
            allowed = ", ".join(sorted(s.value for s in RESIDUAL_TIMING_STATUSES))
            raise ValueError(
                f"EcrTimingResidual.status must be a non-known VisibleFactStatus "
                f"({{{allowed}}}); got {self.status.value!r}. A KNOWN cutoff posture "
                f"is carried (M1), not recorded as a residual."
            )
        if not self.reason.strip():
            raise ValueError("EcrTimingResidual.reason must be non-empty.")
        return self


class EcrTimingPosture(StrictModel):
    """SP-3 source-side timing posture derived for one source slice.

    Exactly one of ``carried_cutoff_posture`` / ``residual`` is set:

    - ``carried_cutoff_posture``: an M1 carry of the slice's KNOWN
      ``cutoff_posture`` value, validated against the single-sourced
      ``CUTOFF_POSTURE_VALUES``. The SP-3 subpredicate clears only when this
      value is ``"pre_cutoff"``.
    - ``residual``: a named M3 residual when the producer did not assert a KNOWN
      cutoff posture. Never clears.

    ``clears_pre_cutoff`` is a stored field (not computed) so the record
    round-trips through YAML cleanly under ``extra="forbid"``; the validator
    binds it to ``True`` iff the carried value is ``"pre_cutoff"``.
    """

    slice_id: str
    carried_cutoff_posture: str | None = None
    residual: EcrTimingResidual | None = None
    clears_pre_cutoff: bool

    @model_validator(mode="after")
    def validate_posture(self) -> "EcrTimingPosture":
        has_carried = self.carried_cutoff_posture is not None
        has_residual = self.residual is not None
        if has_carried == has_residual:
            raise ValueError(
                "EcrTimingPosture requires exactly one of "
                "{carried_cutoff_posture, residual} to be set."
            )
        if has_carried and self.carried_cutoff_posture not in CUTOFF_POSTURE_VALUES:
            allowed = ", ".join(sorted(CUTOFF_POSTURE_VALUES))
            raise ValueError(
                f"carried_cutoff_posture must be one of {{{allowed}}} "
                f"(source_capture CUTOFF_POSTURE_VALUES, single-sourced); got "
                f"{self.carried_cutoff_posture!r}."
            )
        expected_clears = self.carried_cutoff_posture == "pre_cutoff"
        if self.clears_pre_cutoff != expected_clears:
            raise ValueError(
                "clears_pre_cutoff must be True iff carried_cutoff_posture == "
                f"'pre_cutoff'; got clears_pre_cutoff={self.clears_pre_cutoff} with "
                f"carried_cutoff_posture={self.carried_cutoff_posture!r}."
            )
        return self


class InspectabilityState(StrEnum):
    """Closed SP-2 inspectability judgment for one source slice.

    These are ECR-*derived* values (SP-2 is M2 derived-read), owned here -- not a
    carry of any producer field -- so declaring them is not a re-coining of
    ``source_capture`` vocabulary (contrast SP-3, which carries the producer's
    ``cutoff_posture``). The SP-2 subpredicate clears only on
    ``INSPECTABLE_VERIFIABLE``.
    """

    INSPECTABLE_VERIFIABLE = "inspectable_verifiable"
    INSPECTABLE_REFERENCE_ONLY = "inspectable_reference_only"
    NOT_INSPECTABLE = "not_inspectable"


class EcrInspectabilityPosture(StrictModel):
    """SP-2 source-side inspectability posture derived for one source slice.

    Per-slice grain (single-grain ECR record, matching ``EcrTimingPosture``): one
    posture per source slice. ``state`` is the closed 3-value inspectability
    judgment; ``clears_inspectable`` is a stored field (not computed) so the record
    round-trips through YAML cleanly under ``extra="forbid"``, bound by the
    validator to ``True`` iff ``state == inspectable_verifiable``. ``reason`` is the
    visible non-clearing limitation: required for the two non-verifiable states,
    forbidden for the verifiable state.

    M2 derived-read over M1-carried integrity anchors: the deriver reads each
    referenced ``PreservedFile.sha256`` (recomputed at the harness, never trusted
    here) and the slice locator. It binds no ``EvidenceUnit`` and makes no JSG-01,
    scoring, or readiness claim.
    """

    slice_id: str
    state: InspectabilityState
    clears_inspectable: bool
    reason: str | None = None

    @model_validator(mode="after")
    def validate_posture(self) -> "EcrInspectabilityPosture":
        expected_clears = self.state == InspectabilityState.INSPECTABLE_VERIFIABLE
        if self.clears_inspectable != expected_clears:
            raise ValueError(
                "clears_inspectable must be True iff state == "
                f"'inspectable_verifiable'; got clears_inspectable="
                f"{self.clears_inspectable} with state={self.state.value!r}."
            )
        if expected_clears and self.reason is not None:
            raise ValueError(
                "EcrInspectabilityPosture.reason must be None when state is "
                "'inspectable_verifiable' (a cleared posture records no limitation)."
            )
        if not expected_clears and (self.reason is None or not self.reason.strip()):
            raise ValueError(
                "EcrInspectabilityPosture.reason must be a non-empty visible "
                f"limitation when state is {self.state.value!r} (does not clear)."
            )
        return self


class IdentityState(StrEnum):
    """Closed SP-1 source-identity judgment for one packet.

    ECR-*derived* (SP-1 is M2 derived-read), owned here -- not a carry of any
    producer field. The SP-1 subpredicate clears on ``{RESOLVED, FAMILY_ONLY}``
    (``FAMILY_ONLY`` carries a visible specificity limitation) and never on
    ``UNRESOLVED``.
    """

    RESOLVED = "resolved"
    FAMILY_ONLY = "family_only"
    UNRESOLVED = "unresolved"


class EcrIdentityPosture(StrictModel):
    """SP-1 source-side identity posture derived for one packet.

    Per-packet grain (identity is a whole-packet fact): one posture per packet,
    keyed by ``packet_id``. ``state`` is the closed 3-value identity judgment.

    M2 derived-read with an M3 stop: derived from the producer's
    ``source_family`` / ``source_surface`` / ``source_locator`` (binds the real
    fields, coins no producer vocabulary); ``UNRESOLVED`` is the M3 stop -- a
    named limitation, never an invented identity. Actor/audience is
    mark-if-unavailable (Ob.7) and does not gate ``RESOLVED``.

    ``clears_identity`` is stored (not computed) for clean YAML round-trip under
    ``extra="forbid"``; the validator binds it to ``True`` iff ``state`` is in
    ``{RESOLVED, FAMILY_ONLY}``. ``reason`` is the visible limitation: required
    for ``{FAMILY_ONLY, UNRESOLVED}``, forbidden for ``{RESOLVED}``. Note this
    differs from the timing/inspectability rows: ``reason``-presence is NOT the
    same partition as ``clears_identity`` (``FAMILY_ONLY`` clears yet carries a
    limitation).
    """

    packet_id: str
    state: IdentityState
    clears_identity: bool
    reason: str | None = None

    @model_validator(mode="after")
    def validate_posture(self) -> "EcrIdentityPosture":
        expected_clears = self.state in (
            IdentityState.RESOLVED,
            IdentityState.FAMILY_ONLY,
        )
        if self.clears_identity != expected_clears:
            raise ValueError(
                "clears_identity must be True iff state is in "
                f"{{resolved, family_only}}; got clears_identity="
                f"{self.clears_identity} with state={self.state.value!r}."
            )
        reason_required = self.state in (
            IdentityState.FAMILY_ONLY,
            IdentityState.UNRESOLVED,
        )
        if reason_required and (self.reason is None or not self.reason.strip()):
            raise ValueError(
                "EcrIdentityPosture.reason must be a non-empty visible limitation "
                f"when state is {self.state.value!r} (family_only and unresolved "
                "both carry a limitation)."
            )
        if not reason_required and self.reason is not None:
            raise ValueError(
                "EcrIdentityPosture.reason must be None when state is 'resolved' "
                "(a fully resolved identity records no limitation)."
            )
        return self


class SourceVisibilityValue(StrEnum):
    """Closed SP-6 source-visibility value set (8, ECR-owned; ratified 387b630).

    ECR-*derived* values (SP-6 is M2 derived-read over producer facts), owned
    here -- not a carry of a producer field. The SP-6 visibility-sufficiency
    grade (decision C) clears only on ``{ARCHIVE_ONLY, NOT_APPLICABLE}``.

    Two members are declared but the deriver never emits them today:
    ``ARCHIVE_CORROBORATED`` / ``ARCHIVE_DIVERGED`` need a recorded
    archive-vs-current comparison fact (M / D2) the producer does not store, so
    those rows route to ``RESIDUAL_COMPARISON_NOT_RECORDED`` (D1). And
    ``NOT_APPLICABLE`` (the immutable/official-source clear) needs the row-1 X
    condition, which the ratified contract leaves "consumed, not designed"; it is
    deferred, so v1 clears only on ``ARCHIVE_ONLY``.
    """

    ARCHIVE_CORROBORATED = "archive_corroborated"
    ARCHIVE_ONLY = "archive_only"
    ARCHIVE_DIVERGED = "archive_diverged"
    CURRENT_CAPTURE_ONLY = "current_capture_only"
    ARCHIVE_POST_CUTOFF_ONLY = "archive_post_cutoff_only"
    ATTEMPT_FAILED = "attempt_failed"
    NOT_ATTEMPTED = "not_attempted"
    NOT_APPLICABLE = "not_applicable"


# Decision C (387b630): the SP-6 grade clears on exactly these values.
SOURCE_VISIBILITY_CLEARING_VALUES = frozenset(
    {SourceVisibilityValue.ARCHIVE_ONLY, SourceVisibilityValue.NOT_APPLICABLE}
)


class SourceVisibilityResidual(StrEnum):
    """Closed SP-6 named-residual set (6, ECR-owned; ratified 387b630).

    The D1 honesty surface: emitted (never invented) when the producer holds
    neither the value nor the derivable inputs.
    ``RESIDUAL_SLICE_DIVERGENT_VISIBILITY`` -- the per-slice no-hide rollup
    residual -- is declared but not emitted by this per-packet (flat) deriver
    (see ``EcrSourceVisibilityPosture``).
    """

    RESIDUAL_ARCHIVE_POST_CUTOFF_WITH_CURRENT = "RESIDUAL_ARCHIVE_POST_CUTOFF_WITH_CURRENT"
    RESIDUAL_COMPARISON_NOT_RECORDED = "RESIDUAL_COMPARISON_NOT_RECORDED"
    RESIDUAL_ARCHIVE_DATE_UNKNOWN = "RESIDUAL_ARCHIVE_DATE_UNKNOWN"
    RESIDUAL_ARCHIVE_POSTURE_UNKNOWN = "RESIDUAL_ARCHIVE_POSTURE_UNKNOWN"
    RESIDUAL_NO_VISIBILITY_BASIS = "RESIDUAL_NO_VISIBILITY_BASIS"
    RESIDUAL_SLICE_DIVERGENT_VISIBILITY = "RESIDUAL_SLICE_DIVERGENT_VISIBILITY"


class EcrSourceVisibilityPosture(StrictModel):
    """SP-6 source-side source-visibility posture derived for one packet.

    Per-packet grain (flat) -- resolving the ratified field's ``not_proven``
    vector-vs-flat refinement to *flat*: one posture per packet, keyed by
    ``packet_id``. Justification: the producer builds single-source packets and
    its packet-level ``archive_history_posture`` is already conservative, so
    there is no intra-packet slice divergence for a no-hide rollup to guard. If
    multi-source packets are ever introduced, add a per-slice vector + rollup
    then -- this per-packet value becomes the one-entry rollup.

    Exactly one of ``value`` / ``residual`` is set:

    - ``value``: a ratified closed ``SourceVisibilityValue``.
    - ``residual``: a ratified named ``SourceVisibilityResidual`` (D1 honesty);
      never clears; carries a ``reason``.

    ``clears_source_visibility`` is stored (not computed) for clean YAML
    round-trip under ``extra="forbid"``; the validator binds it to ``True`` iff
    ``value`` is in the decision-C clearing set ``{archive_only, not_applicable}``.

    D-source amendment (recorded inline at the boundary doc's Direction Change
    Propagation, commit 641cf15): the archive-date class ``D`` is the archive
    slice's ``cutoff_posture`` consumed as a closed pre/post CLASS (never a
    timestamp; AR-03). M2 derived-read; binds no ``EvidenceUnit`` and makes no
    JSG-01, scoring, or readiness claim.
    """

    packet_id: str
    value: SourceVisibilityValue | None = None
    residual: SourceVisibilityResidual | None = None
    clears_source_visibility: bool
    reason: str | None = None

    @model_validator(mode="after")
    def validate_posture(self) -> "EcrSourceVisibilityPosture":
        has_value = self.value is not None
        has_residual = self.residual is not None
        if has_value == has_residual:
            raise ValueError(
                "EcrSourceVisibilityPosture requires exactly one of "
                "{value, residual} to be set."
            )
        expected_clears = has_value and self.value in SOURCE_VISIBILITY_CLEARING_VALUES
        if self.clears_source_visibility != expected_clears:
            raise ValueError(
                "clears_source_visibility must be True iff value is in "
                "{archive_only, not_applicable} (decision C); got "
                f"clears_source_visibility={self.clears_source_visibility} with "
                f"value={self.value!r}, residual={self.residual!r}."
            )
        if has_residual and (self.reason is None or not self.reason.strip()):
            raise ValueError(
                "EcrSourceVisibilityPosture.reason must be a non-empty visible "
                f"limitation when a residual is set (got residual={self.residual!r})."
            )
        if has_value and self.reason is not None:
            raise ValueError(
                "EcrSourceVisibilityPosture.reason must be None when a value is "
                "set; reasons are carried only by residual postures."
            )
        return self
