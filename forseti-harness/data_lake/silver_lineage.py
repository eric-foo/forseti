"""Generic Silver lineage grammar: build/validate the source-reference fields a
Silver record carries, so a downstream agent can tell source-backed evidence,
derived-record evidence, source-row evidence, and accepted limitations apart
without inventing per-lane provenance fields.

This is the additive helper/validator from the adjudicated genericity check
(`docs/workflows/silver_lineage_kit_genericity_check_v0.md`). It models REFERENCES,
not media: which raw packet/file/hash a fact came from (`raw_refs`), which exact
prior derived record it consumed (`derived_refs`, with an optional projection
`row_locator`), the source-local identity being observed (`source_object`), and
what lineage is intentionally absent (`lineage_limitations`).

Two adjudicated review findings are load-bearing here and are enforced, not just
documented:

- AR-01 (one home). The Silver Vault Common Record Header
  (`core_spine_v0_data_lake_silver_vault_record_contract_v0.md`) is the single
  persisted home for `raw_refs`/`derived_refs`/`source_surface`/timestamps/producer
  fields. This module is an in-process BUILDER, never a second persisted store:
  ``to_record_fields()`` emits header-shaped TOP-LEVEL fields a writer merges into
  the record in place. It deliberately does NOT emit a nested ``silver_lineage``
  object, so a producer cannot create two homes for the refs.
- AR-02 (projection row identity). ``SilverDerivedRef`` carries an optional
``row_locator`` (``row_id``/``row_kind``) mirroring Cleaning source-row identity, so a
fact derived from one row of a multi-row source record is not collapsed to
  ``lane + record_id`` alone.

Field names track the genericity check grammar and the Common Record Header
vocabulary: ``kind`` (not ``object_type``, AR-04) for ``source_object``, and inline
``relative_packet_path`` on raw refs (AR-03).

Scope (v0): additive helper + validator + one representative adopter. NOT a
universal record-wrapper migration, NOT a historical lake rewrite, NOT a Silver
Vault schema redesign. Those are accepted residuals in the genericity check.
"""
from __future__ import annotations

from enum import StrEnum
from typing import Literal, Mapping

from pydantic import Field, ValidationError, model_validator

from schemas.case_models import StrictModel

SILVER_LINEAGE_SCHEMA_VERSION = "silver_lineage_v0"
LINEAGE_STRUCTURE_COMPLETE_STATUS = "lineage_structure_complete"
LINEAGE_STRUCTURE_MISSING_STATUS = "lineage_structure_missing"
LINEAGE_STRUCTURE_INCOMPLETE_STATUS = "lineage_structure_incomplete"
LINEAGE_STRUCTURE_INVALID_STATUS = "lineage_structure_invalid"
LineageStructureStatus = Literal[
    "lineage_structure_complete",
    "lineage_structure_missing",
    "lineage_structure_incomplete",
    "lineage_structure_invalid",
]

# Open relation vocabularies from the genericity check grammar. Kept as Literals
# (not closed enums) because the grammar calls them illustrative-but-bounded; a
# new producer relation is a one-line addition, not a schema migration.
RawRefRelation = Literal["observed_from", "selected_from", "derived_from", "consumed"]
DerivedRefRelation = Literal[
    "derived_from", "consumed", "selected", "corrects", "supersedes", "conflicts_with"
]
# Raw-ref anchor kinds: "file" and the whole-artifact derived cases take no
# anchor value; the specific kinds point inside the file.
AnchorKind = Literal[
    "file",
    "json_pointer",
    "html_selector",
    "script_index",
    "text_pattern",
    "time_span",
    "byte_range",
    "source_locator",
]


class SilverLineageLimitationReason(StrEnum):
    """Controlled v0 reason tokens for ``lineage_limitations`` (AR-06: the rest of
    the system avoids free-text reason sets, so the limitation axis gets a
    controlled vocabulary it can mechanically check). ``other`` is the escape hatch
    for a not-yet-enumerated limitation and REQUIRES a free-text ``detail``.

    The set is intentionally minimal and v0: it covers the limitation cases the
    genericity check names (transient unpersisted media, no raw packet, no exact
    derived record, an unhashed derived record). A producer that hits a genuinely
    new limit adds a token here rather than reaching for free text."""

    TRANSIENT_SOURCE_NOT_PERSISTED = "transient_source_not_persisted"
    NO_RAW_PACKET = "no_raw_packet"
    NO_EXACT_DERIVED_RECORD = "no_exact_derived_record"
    DERIVED_RECORD_UNHASHED = "derived_record_unhashed"
    OTHER = "other"


class SilverSourceObject(StrictModel):
    """Source-LOCAL identity of the thing observed. Uses the Silver Vault
    ``entity_key`` vocabulary (``namespace + kind + native_id``, AR-04 -- ``kind``,
    never ``object_type``). It must NOT imply a global person/product/brand or any
    cross-platform identity; that is a Gold/Judgment concern, not lineage."""

    namespace: str
    kind: str
    native_id: str
    source_url: str | None = None

    @model_validator(mode="after")
    def reject_blank_identity(self) -> "SilverSourceObject":
        for field in ("namespace", "kind", "native_id"):
            if not getattr(self, field).strip():
                raise ValueError(f"SilverSourceObject.{field} must be non-empty.")
        return self


class SilverAnchor(StrictModel):
    """Where inside a raw file/packet the fact sits. ``file`` (and a bare whole
    artifact) takes no ``value``; every other kind requires one."""

    kind: AnchorKind = "file"
    value: str | None = None

    @model_validator(mode="after")
    def validate_anchor_value(self) -> "SilverAnchor":
        if self.kind == "file":
            if self.value is not None and not self.value.strip():
                raise ValueError("file anchors must not carry a blank value.")
        elif not (self.value and self.value.strip()):
            raise ValueError(f"{self.kind} anchors require a non-empty value.")
        return self


class SilverRawRef(StrictModel):
    """A reference to preserved RAW material (a SourceCapturePacket file). Carries
    enough packet/file/hash to resolve or audit. ``relative_packet_path`` is kept
    inline (AR-03) even though it is manifest-resolvable, so a lineage block is
    self-describing without a manifest round-trip. ``sha256``/``hash_basis`` are
    required together when present, and a file-level ref (``file_id`` set) must be
    hash-checkable, per the Common Record Header contract."""

    ref_type: Literal["raw_packet"] = "raw_packet"
    packet_id: str
    slice_id: str | None = None
    file_id: str | None = None
    relative_packet_path: str | None = None
    sha256: str | None = None
    hash_basis: Literal["raw_stored_bytes"] | None = None
    anchor: SilverAnchor = Field(default_factory=SilverAnchor)
    relation: RawRefRelation = "consumed"

    @model_validator(mode="after")
    def validate_raw_ref(self) -> "SilverRawRef":
        if not self.packet_id.strip():
            raise ValueError("SilverRawRef.packet_id must be non-empty.")
        for field in ("slice_id", "file_id", "relative_packet_path", "sha256", "hash_basis"):
            value = getattr(self, field)
            if value is not None and not value.strip():
                raise ValueError(f"SilverRawRef.{field} must be non-empty when set.")
        # sha256 and hash_basis travel together: a hash with no stated basis is
        # unauditable, and a basis with no hash is an empty promise.
        if bool(self.sha256) != bool(self.hash_basis):
            raise ValueError(
                "SilverRawRef.sha256 and hash_basis must both be present or both absent."
            )
        # A named preserved file IS hash-checkable (the lake re-hashes it on read),
        # so a file-level raw ref must carry the hash, per the Common Record Header.
        if self.file_id and not self.sha256:
            raise ValueError(
                "SilverRawRef with a file_id must carry sha256 + hash_basis (the file is hash-checkable)."
            )
        return self


class SilverRowLocator(StrictModel):
    """Identifies one row inside a multi-row source-derived record (AR-02),
    mirroring ``CleaningInputHandle.source_row_id``/``source_row_kind``. Both fields travel
    together: a half-specified row pointer cannot locate a row."""

    row_id: str
    row_kind: str

    @model_validator(mode="after")
    def reject_blank_locator(self) -> "SilverRowLocator":
        for field in ("row_id", "row_kind"):
            if not getattr(self, field).strip():
                raise ValueError(f"SilverRowLocator.{field} must be non-empty.")
        return self


class SilverDerivedRef(StrictModel):
    """A reference to the EXACT prior derived record a fact consumed. ``lane`` +
    ``record_id`` must be exact (never just a shortcode/video id) -- this is what
    closes the same-shortcode product-mention ambiguity. ``row_locator`` is set when
    the consumed record is a multi-row projection record and the fact depends on one
    row (AR-02)."""

    ref_type: Literal["derived_record"] = "derived_record"
    raw_anchor: str
    lane: str
    record_id: str
    row_locator: SilverRowLocator | None = None
    sha256: str | None = None
    hash_basis: Literal["derived_record_bytes"] | None = None
    content_hash: str | None = None
    content_hash_basis: Literal["canonical_json_excluding_content_hash"] | None = None
    relation: DerivedRefRelation = "consumed"
    record_set_completion_lane: str | None = None

    @model_validator(mode="after")
    def validate_derived_ref(self) -> "SilverDerivedRef":
        # Exactness is the crux: a derived ref that cannot name the exact record is
        # the same-shortcode collapse the kit exists to prevent.
        for field in ("raw_anchor", "lane", "record_id"):
            if not getattr(self, field).strip():
                raise ValueError(f"SilverDerivedRef.{field} must be non-empty (exact lane+record_id required).")
        for field in (
            "sha256",
            "hash_basis",
            "content_hash",
            "content_hash_basis",
            "record_set_completion_lane",
        ):
            value = getattr(self, field)
            if value is not None and not value.strip():
                raise ValueError(f"SilverDerivedRef.{field} must be non-empty when set.")
        if bool(self.sha256) != bool(self.hash_basis):
            raise ValueError(
                "SilverDerivedRef.sha256 and hash_basis must both be present or both absent."
            )
        if bool(self.content_hash) != bool(self.content_hash_basis):
            raise ValueError(
                "SilverDerivedRef.content_hash and content_hash_basis must both be present "
                "or both absent."
            )
        return self


class SilverLineageLimitation(StrictModel):
    """A declared, intentional gap in lineage. A limitation is not a defect by
    itself, but a record carrying only limitations cannot claim full source-backed
    completeness (see ``SilverLineage.is_source_backed_complete``)."""

    reason: SilverLineageLimitationReason
    detail: str | None = None

    @model_validator(mode="after")
    def validate_detail(self) -> "SilverLineageLimitation":
        if self.detail is not None and not self.detail.strip():
            raise ValueError("SilverLineageLimitation.detail must be non-empty when set.")
        if self.reason == SilverLineageLimitationReason.OTHER and not (self.detail and self.detail.strip()):
            raise ValueError("lineage_limitations reason 'other' requires a free-text detail.")
        return self


class SilverLineage(StrictModel):
    """The in-process builder for a Silver record's lineage. Validated on
    construction (fail-closed: an invalid lineage cannot be built). Emit with
    ``to_record_fields()`` to merge header-shaped fields into a record IN PLACE --
    this type is never itself persisted as a nested block (AR-01)."""

    schema_version: Literal["silver_lineage_v0"] = SILVER_LINEAGE_SCHEMA_VERSION
    producer_id: str
    producer_schema_version: str
    source_surface: str
    source_object: SilverSourceObject | None = None
    observed_at: str | None = None
    captured_at: str | None = None
    raw_refs: list[SilverRawRef] = Field(default_factory=list)
    derived_refs: list[SilverDerivedRef] = Field(default_factory=list)
    lineage_limitations: list[SilverLineageLimitation] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_lineage(self) -> "SilverLineage":
        for field in ("producer_id", "producer_schema_version", "source_surface"):
            if not getattr(self, field).strip():
                raise ValueError(f"SilverLineage.{field} must be non-empty.")
        for field in ("observed_at", "captured_at"):
            value = getattr(self, field)
            if value is not None and not value.strip():
                raise ValueError(f"SilverLineage.{field} must be non-empty when set.")
        # A lineage block must say SOMETHING: at least one resolvable ref, or an
        # explicit limitation. A wholly empty lineage is the silent-omission the
        # write-boundary check forbids.
        if not (self.raw_refs or self.derived_refs or self.lineage_limitations):
            raise ValueError(
                "SilverLineage must carry at least one raw_ref, derived_ref, or lineage_limitation "
                "(a record may not silently omit lineage)."
            )
        # A record with no resolvable ref MUST declare why (mandatory limitation),
        # so rawless/derivedless facts are visibly incomplete rather than silently so.
        if not (self.raw_refs or self.derived_refs) and not self.lineage_limitations:
            raise ValueError(
                "SilverLineage with no raw_ref and no derived_ref requires an explicit lineage_limitation."
            )
        return self

    def has_reference_structure(self) -> bool:
        """True iff the record declares at least one raw or derived ref.

        This is structural only; physical authority requires the root-aware
        classifier in data_lake.silver_record."""
        return bool(self.raw_refs or self.derived_refs)

    def to_record_fields(self) -> dict:
        """Header-shaped fields to merge into a Silver record IN PLACE (AR-01: one
        home for the refs). Returns flat top-level keys -- NOT a nested
        ``silver_lineage`` object -- so a record never gets a second home for
        ``raw_refs``/``derived_refs``.

        The lineage block's own version is emitted as ``lineage_schema_version`` (not
        ``schema_version``) so it is never mistaken for, and never clobbers, a record's
        Common Record Header ``schema_version`` (``silver_vault_record_v0``)."""
        return {
            "lineage_schema_version": self.schema_version,
            "producer_id": self.producer_id,
            "producer_schema_version": self.producer_schema_version,
            "source_surface": self.source_surface,
            "source_object": (
                self.source_object.model_dump(mode="json") if self.source_object is not None else None
            ),
            "observed_at": self.observed_at,
            "captured_at": self.captured_at,
            "raw_refs": [ref.model_dump(mode="json") for ref in self.raw_refs],
            "derived_refs": [ref.model_dump(mode="json") for ref in self.derived_refs],
            "lineage_limitations": [lim.model_dump(mode="json") for lim in self.lineage_limitations],
        }


def validate_silver_lineage(lineage: SilverLineage) -> SilverLineage:
    """Explicit write-boundary validation hook. ``SilverLineage`` already validates
    on construction, so this re-runs the model validators and returns the same
    object (or raises ``pydantic.ValidationError``) -- a single call a producer can
    make at the write boundary to assert a lineage block is well-formed before it is
    persisted."""
    return SilverLineage.model_validate(lineage.model_dump(mode="json"))


def silver_record_lineage_structure_status(
    record: Mapping[str, object],
) -> LineageStructureStatus:
    """Describe persisted lineage shape without making an authority claim.

    The current Silver Vault envelope owns top-level raw_refs and derived_refs.
    lineage_schema_version is a legacy lineage-kit marker, not a requirement of
    that official envelope. Authority-making readers must use the root-aware
    classifier in data_lake.silver_record; this helper deliberately cannot return
    source_backed_complete.
    """
    if "raw_refs" not in record or "derived_refs" not in record:
        return LINEAGE_STRUCTURE_MISSING_STATUS
    if (
        "lineage_schema_version" in record
        and record.get("lineage_schema_version") != SILVER_LINEAGE_SCHEMA_VERSION
    ):
        return LINEAGE_STRUCTURE_INVALID_STATUS
    for field in ("producer_id", "producer_schema_version", "source_surface"):
        value = record.get(field)
        if not isinstance(value, str) or not value.strip():
            return LINEAGE_STRUCTURE_INVALID_STATUS
    raw_refs = record.get("raw_refs")
    derived_refs = record.get("derived_refs")
    if not isinstance(raw_refs, list) or not isinstance(derived_refs, list):
        return LINEAGE_STRUCTURE_INVALID_STATUS
    if not raw_refs and not derived_refs:
        return LINEAGE_STRUCTURE_INCOMPLETE_STATUS
    if any(not isinstance(ref, Mapping) for ref in [*raw_refs, *derived_refs]):
        return LINEAGE_STRUCTURE_INVALID_STATUS
    return LINEAGE_STRUCTURE_COMPLETE_STATUS


def has_complete_silver_lineage_structure(record: Mapping[str, object]) -> bool:
    """Boolean structural wrapper; never a physical source-authority decision."""
    return (
        silver_record_lineage_structure_status(record)
        == LINEAGE_STRUCTURE_COMPLETE_STATUS
    )
