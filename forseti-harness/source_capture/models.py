from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import Field, field_validator, model_validator

from schemas.case_models import StrictModel


OBLIGATION_CONTRACT_VERSION = "core_spine_v0_data_capture_spine_obligation_contract_v0"
SOURCE_CAPTURE_MANIFEST_VERSION = "source_capture_packet_manifest_v1"


class CaptureModeCategory(StrEnum):
    HUMAN_LED = "human-led"
    AGENT_ASSISTED = "agent-assisted"
    STRUCTURED_ACCESS = "structured access"
    ARCHIVE_HISTORY = "archive/history"
    AUTOMATED_EXTRACTION = "automated extraction"
    MULTIMODAL = "multimodal"
    MIXED = "mixed"


class VisibleFactStatus(StrEnum):
    KNOWN = "known"
    UNKNOWN_WITH_REASON = "unknown_with_reason"
    NOT_ATTEMPTED = "not_attempted"
    NOT_APPLICABLE = "not_applicable"


class VisibleFact(StrictModel):
    status: VisibleFactStatus
    value: str | None = None
    reason: str | None = None

    @model_validator(mode="after")
    def validate_fact(self) -> "VisibleFact":
        if self.status == VisibleFactStatus.KNOWN:
            if not self.value:
                raise ValueError("known facts require a value")
            return self
        if not self.reason:
            raise ValueError("non-known facts require a reason")
        return self


# Ob.9 / Ob.10 / Ob.15 closed posture vocabularies, enforced at write-time. A
# posture is closed only on its known VALUE; not_attempted / not_applicable /
# unknown_with_reason are carried by VisibleFactStatus + reason (AR-05). Closing
# these once, at the source, stops every downstream reader from re-interpreting
# free text. access_posture (Ob.11) is intentionally left open.
CUTOFF_POSTURE_VALUES = frozenset({"pre_cutoff", "post_cutoff", "mixed", "unknown"})
ARCHIVE_HISTORY_POSTURE_VALUES = frozenset({"archived", "attempt_failed"})
RE_CAPTURE_RELATIONSHIP_VALUES = frozenset({"supersede", "supplement", "conflict", "mixed"})

# AR-04: every PreservedFile declares the recomputation basis of its sha256 as a
# closed, source-visible token -- never arbitrary prose (an unconstrained string just
# recreates the "hash-shaped string" problem under a new field name). The token names
# what the hash COVERS; the bytes are named by relative_packet_path and the algorithm
# by the sha256 field, so the basis need not repeat them. raw_stored_bytes = the sha256
# is computed over the complete, unmodified stored bytes of the file at
# relative_packet_path (recompute: sha256(read_bytes(packet_dir / relative_packet_path))).
# Add a value only when a writer path actually produces that basis (e.g. an owner-bound
# acquisition receipt); invent none ahead of a real producer.
HASH_BASIS_VALUES = frozenset({"raw_stored_bytes"})


def _require_closed_posture(
    fact: VisibleFact, *, allowed: frozenset[str], field: str, obligation: str
) -> None:
    if fact.status == VisibleFactStatus.KNOWN and fact.value not in allowed:
        allowed_list = ", ".join(sorted(allowed))
        raise ValueError(
            f"{field} known value must be one of {{{allowed_list}}} ({obligation} closed "
            f"vocabulary); got {fact.value!r}. Record capture context elsewhere (e.g. "
            f"capture_context) and use unknown_with_reason / not_attempted / not_applicable "
            f"for non-closed cases."
        )


class PacketTiming(StrictModel):
    source_publication_or_event: VisibleFact
    source_edit_or_version: VisibleFact
    capture_time: VisibleFact
    # archive_snapshot_time: when the ARCHIVE captured the surface (e.g. the Wayback Machine
    # snapshot moment), normalized to the same ISO-8601 UTC "...Z" form as capture_time. It is
    # DISTINCT from capture_time, which stays the access/fetch time (when WE obtained the bytes
    # from the archive) and is never repurposed. Additive and optional so existing manifests
    # stay readable under extra="forbid": None means this packet's producer did not set the
    # field -- a legacy packet captured before the field existed, or a non-archive capture
    # mode. An archive-mode producer always sets a VisibleFact here: known_fact(normalized)
    # when the archive declared a parseable snapshot timestamp, else unknown_with_reason(...);
    # it never falls back to fetch time. Seam published in
    # docs/decisions/source_capture_archive_snapshot_typed_timing_decision_v0.md.
    archive_snapshot_time: VisibleFact | None = None
    recapture_time: VisibleFact
    cutoff_posture: VisibleFact

    @model_validator(mode="after")
    def validate_closed_postures(self) -> "PacketTiming":
        _require_closed_posture(
            self.cutoff_posture, allowed=CUTOFF_POSTURE_VALUES, field="cutoff_posture", obligation="Ob.9"
        )
        return self


class PreservedFile(StrictModel):
    file_id: str
    original_path: str
    relative_packet_path: str
    sha256: str
    hash_basis: str
    size_bytes: int = Field(ge=0)

    @field_validator("hash_basis")
    @classmethod
    def validate_hash_basis(cls, value: str) -> str:
        if value not in HASH_BASIS_VALUES:
            allowed_list = ", ".join(sorted(HASH_BASIS_VALUES))
            raise ValueError(
                f"hash_basis must be one of {{{allowed_list}}} (AR-04 recomputation-bound "
                f"basis); got {value!r}. Add a value only when a writer produces that basis."
            )
        return value


# Creator-momentum typed metric observation (IG capture-shape contract; spine PR #151). The
# capture->projection backbone's CORE "typed value + typed availability posture" discipline applied
# per metric: absence / out-of-window / not-attempted / blocked / not-applicable can NEVER be stored
# as an observed value (in particular, never as an observed 0). This is the one irreversible,
# un-re-capturable lock-in named by the IG capture-shape spec, landed here as the platform-agnostic
# CORE substrate. Per-platform SATELLITE pieces ride with the producer (deferred): the closed IG
# metric vocabulary (follower_count / view_count / like_count / comment_count), the value>=0
# constraint, the numeric-id identity anchor + conflict-policy version pin, and the packet-level
# coverage CLAIM (which posts were claimed/attempted). `value` is int (counts); widening to other
# value types is a future additive change.
class MetricPosture(StrEnum):
    OBSERVED = "observed"
    UNAVAILABLE_WITH_REASON = "unavailable_with_reason"
    OUT_OF_CAPTURE_WINDOW = "out_of_capture_window"
    NOT_ATTEMPTED = "not_attempted"
    NOT_APPLICABLE = "not_applicable"


class CoverageWindow(StrictModel):
    # The capture window a metric observation claims to cover (ISO-8601 UTC); either bound may be
    # None when the producer does not bound that side. This is the per-metric window, distinct from
    # a (deferred) packet-level coverage CLAIM over which posts were claimed/attempted.
    start: str | None = None
    end: str | None = None


class MetricObservation(StrictModel):
    # A typed momentum metric observation: a typed value coupled to a typed availability posture so
    # absence is never stored as a value. `metric` is the metric identity (closed per-platform at
    # the satellite producer, not here). `value` is present iff posture == observed; `reason` is
    # present iff posture != observed.
    metric: str
    posture: MetricPosture
    value: int | None = None
    reason: str | None = None
    coverage_window: CoverageWindow | None = None

    @field_validator("metric")
    @classmethod
    def validate_metric_non_empty(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("metric identity must be a non-empty token")
        return stripped

    @field_validator("reason")
    @classmethod
    def normalize_reason(cls, value: str | None) -> str | None:
        # A whitespace-only reason is no reason: normalize it to None so the value<->posture
        # coupling below rejects a blank "reason" on a non-observed metric (no fake reasons).
        if value is None:
            return None
        stripped = value.strip()
        return stripped or None

    @model_validator(mode="after")
    def validate_observation(self) -> "MetricObservation":
        if self.posture == MetricPosture.OBSERVED:
            if self.value is None:
                raise ValueError("an observed metric requires a value")
            if self.reason is not None:
                raise ValueError("an observed metric must not carry a reason")
            return self
        if self.value is not None:
            raise ValueError(
                f"a non-observed metric (posture={self.posture}) must not carry a value "
                f"(absence must never be stored as an observed value, e.g. an observed 0)"
            )
        if not self.reason:
            raise ValueError(f"a non-observed metric (posture={self.posture}) requires a reason")
        return self


class SourceCaptureSlice(StrictModel):
    slice_id: str
    locator: VisibleFact
    timing: PacketTiming
    access_posture: VisibleFact
    archive_history_posture: VisibleFact
    media_modality_posture: VisibleFact
    re_capture_relationship: VisibleFact
    # Demand-durability pins (Lane 1 Element 1; capture_envelope_durability_delta_spec_v0).
    # Additive and optional so existing manifests stay valid under extra="forbid": None
    # means this slice's producer did not set the pin (a non-durability capture, or a
    # legacy slice). A demand-durability observation sets each as a VisibleFact
    # (known_fact / unknown_with_reason / not_applicable). These fix comparability across
    # a series; they are observed facts, never weights or scores (INV-1).
    session_visibility_pin: VisibleFact | None = None
    locale_pin: VisibleFact | None = None
    currency_pin: VisibleFact | None = None
    variant_pin: VisibleFact | None = None
    limitations: list[str] = Field(default_factory=list)
    warning_notes: list[str] = Field(default_factory=list)
    preserved_file_ids: list[str] = Field(default_factory=list)
    # Creator-momentum typed metric observations for this slice (IG capture-shape contract). Additive
    # and optional (default empty) so existing manifests stay valid under extra="forbid": an empty
    # list means this slice's producer captured no typed momentum metric (a non-momentum capture, or
    # a legacy slice). Each entry couples a typed value to a typed availability posture so absence is
    # never stored as an observed value. Same back-compat pattern as the demand-durability pins above.
    metric_observations: list[MetricObservation] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_closed_postures(self) -> "SourceCaptureSlice":
        _require_closed_posture(
            self.archive_history_posture,
            allowed=ARCHIVE_HISTORY_POSTURE_VALUES,
            field="archive_history_posture",
            obligation="Ob.10",
        )
        _require_closed_posture(
            self.re_capture_relationship,
            allowed=RE_CAPTURE_RELATIONSHIP_VALUES,
            field="re_capture_relationship",
            obligation="Ob.15",
        )
        return self


class ReceiptMetadata(StrictModel):
    title: str
    generated_at: str
    summary: str
    non_claims: list[str] = Field(default_factory=list)

    @field_validator("generated_at", mode="before")
    @classmethod
    def normalize_generated_at(cls, value: object) -> object:
        if isinstance(value, datetime):
            return value.isoformat().replace("+00:00", "Z")
        return value


class SourceCapturePacket(StrictModel):
    packet_id: str
    manifest_version: str
    obligation_contract_version: str
    source_family: str
    source_surface: str
    source_locator: VisibleFact
    requested_decision_context: VisibleFact
    capture_context: VisibleFact
    actor_audience_context: VisibleFact
    capture_mode: CaptureModeCategory
    operator_category: str
    session_identity: str
    visible_mode_changes: list[str] = Field(default_factory=list)
    timing: PacketTiming
    access_posture: VisibleFact
    archive_history_posture: VisibleFact
    media_modality_posture: VisibleFact
    re_capture_relationship: VisibleFact
    # Demand-durability series facts (Lane 1 Elements 2 & 4; capture_envelope_durability_delta_spec_v0).
    # Additive and optional (extra="forbid" back-compat): None means this packet is not part
    # of a tracked durability series, or is legacy. A demand-durability series sets series_id
    # on every observation; cold_start_at + pre_coverage_history_posture mark the series origin
    # (set on the first / cold-start observation); intended_cadence carries the declared
    # CadencePlan.to_dict() shape (a typed CadenceDeclaration model is deferred to avoid coupling
    # the envelope to cadence.py). Series-diff (Element 3) is deferred — it is a cross-packet
    # record, not a single-packet field. All are observed facts, never weights (INV-1); whether a
    # series shows durable vs hollow demand is downstream Judgment.
    series_id: str | None = None
    cold_start_at: VisibleFact | None = None
    pre_coverage_history_posture: VisibleFact | None = None
    intended_cadence: dict[str, object] | None = None
    source_slices: list[SourceCaptureSlice] = Field(min_length=1)
    preserved_files: list[PreservedFile] = Field(min_length=1)
    warnings: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    receipt_metadata: ReceiptMetadata

    def derived_source_classification(self) -> dict[str, object]:
        """Return the re-derivable view without changing persisted packet fields."""
        from source_capture.source_classification import classify_source_pair

        return classify_source_pair(self.source_family, self.source_surface).to_dict()

    @model_validator(mode="after")
    def validate_closed_postures(self) -> "SourceCapturePacket":
        _require_closed_posture(
            self.archive_history_posture,
            allowed=ARCHIVE_HISTORY_POSTURE_VALUES,
            field="archive_history_posture",
            obligation="Ob.10",
        )
        _require_closed_posture(
            self.re_capture_relationship,
            allowed=RE_CAPTURE_RELATIONSHIP_VALUES,
            field="re_capture_relationship",
            obligation="Ob.15",
        )
        return self

    @model_validator(mode="after")
    def validate_preserved_file_references(self) -> "SourceCapturePacket":
        preserved_ids = {item.file_id for item in self.preserved_files}
        if len(preserved_ids) != len(self.preserved_files):
            raise ValueError("preserved file IDs must be unique")

        referenced_ids: set[str] = set()
        for source_slice in self.source_slices:
            unknown_ids = set(source_slice.preserved_file_ids) - preserved_ids
            if unknown_ids:
                unknown_list = ", ".join(sorted(unknown_ids))
                raise ValueError(f"source slice references unknown preserved file IDs: {unknown_list}")
            referenced_ids.update(source_slice.preserved_file_ids)

        unreferenced_ids = preserved_ids - referenced_ids
        if unreferenced_ids:
            unreferenced_list = ", ".join(sorted(unreferenced_ids))
            raise ValueError(f"preserved files are not referenced by any source slice: {unreferenced_list}")
        return self


class PacketWriteResult(StrictModel):
    output_directory: str
    manifest_path: str
    receipt_path: str
    packet: SourceCapturePacket


def known_fact(value: str) -> VisibleFact:
    return VisibleFact(status=VisibleFactStatus.KNOWN, value=value)


def unknown_with_reason(reason: str) -> VisibleFact:
    return VisibleFact(status=VisibleFactStatus.UNKNOWN_WITH_REASON, reason=reason)


def not_attempted(reason: str) -> VisibleFact:
    return VisibleFact(status=VisibleFactStatus.NOT_ATTEMPTED, reason=reason)


def not_applicable(reason: str) -> VisibleFact:
    return VisibleFact(status=VisibleFactStatus.NOT_APPLICABLE, reason=reason)
