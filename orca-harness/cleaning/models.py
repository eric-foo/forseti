"""Cleaning Spine v0 source-invariant models.

These models implement the smallest runtime substrate from the Cleaning Spine
foundation: a stable input handle keyed to raw, a non-destructive transform
ledger, and exact-identity dedupe mechanics. Source-family adapters can feed
these models, but the core does not parse sources or make Judgment claims.
"""
from __future__ import annotations

from enum import StrEnum
import re
from typing import Literal

from pydantic import Field, field_validator, model_validator

from schemas.case_models import StrictModel

CLEANING_CORE_VERSION = "v0"

REQUIRED_NON_CLAIMS = frozenset(
    {
        "no_credibility_decision",
        "no_independence_effect",
        "no_signal_use_or_action_ceiling",
    }
)

_JUDGMENT_TOKENS = frozenset(
    {
        "action_ceiling",
        "action_supporting",
        "artificial_amplification",
        "credible",
        "credibility",
        "decision_strength",
        "demand",
        "discount",
        "discounted",
        "discounting",
        "excluded",
        "independent",
        "integrity",
        "judgment_ready",
        "salience",
        "signal_integrity",
        "signal_use",
        "strong",
        "supporting",
        "weak",
    }
)

_DEFERRED_DEDUPE_TOKENS = frozenset(
    {
        "cluster",
        "clustering",
        "copied_language",
        "near_match",
        "similarity",
    }
)


def _find_token_matches(value: str, tokens: frozenset[str]) -> list[str]:
    normalized = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    padded = f"_{normalized}_"
    return sorted(token for token in tokens if f"_{token}_" in padded)


class CleaningRelation(StrEnum):
    KEYED_SIBLINGS_OVER_RAW = "keyed_siblings_over_raw"


class CleaningRuleScope(StrEnum):
    SOURCE_INVARIANT_CORE = "source_invariant_core"
    SOURCE_FAMILY_ADAPTATION = "source_family_adaptation"
    UNRESOLVED_CANDIDATE = "unresolved_candidate"


class CleaningTransformClass(StrEnum):
    NORMALIZATION = "normalization"
    TRANSLATION = "translation"
    SUMMARIZATION = "summarization"
    DEDUPE_MECHANICS = "dedupe_mechanics"
    PROPAGATION = "propagation"


class CleaningInputGrain(StrEnum):
    ROW = "row"
    CHAIN = "chain"
    BUNDLE = "bundle"
    SLICE = "slice"
    PACKET = "packet"
    GROUP = "group"


class CleaningDedupeBasis(StrEnum):
    RAW_ANCHOR_IDENTITY = "raw_anchor_identity"


class CleaningDerivedRecordRef(StrictModel):
    """Locates a DERIVED lake record (``derived/<raw_anchor>/<lane>/<record_id>``) that has no
    preserved-file substrate -- the cleaning-input form for ASR transcripts and future derived
    sources. Carried by a ``CleaningRawAnchor`` with ``anchor_kind="derived_record"``. The lake's
    segment grammar (``data_lake.root``) is enforced at resolution time, so a malformed
    lane/record_id surfaces as a fail-closed audit finding rather than a crash."""

    subtree: Literal["derived"] = "derived"
    lane: str
    record_id: str

    @field_validator("lane", "record_id")
    @classmethod
    def reject_blank_ref_fields(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("CleaningDerivedRecordRef lane/record_id must be non-empty.")
        return value


class CleaningRawAnchor(StrictModel):
    # A preserved-file anchor (the default) keys to a packet's preserved file via
    # slice_id/file_id/relative_packet_path. A ``derived_record`` anchor instead keys to a derived
    # lake record via ``derived_record_ref`` and carries NONE of the preserved-file fields.
    packet_id: str
    slice_id: str | None = None
    file_id: str | None = None
    relative_packet_path: str | None = None
    sha256: str
    hash_basis: str
    anchor_kind: Literal[
        "file", "json_pointer", "html_selector", "script_index", "text_pattern", "derived_record"
    ] = "file"
    anchor_value: str | None = None
    json_pointer: str | None = None
    derived_record_ref: CleaningDerivedRecordRef | None = None

    @field_validator("packet_id", "sha256", "hash_basis")
    @classmethod
    def reject_blank_anchor_fields(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("CleaningRawAnchor fields must be non-empty.")
        return value

    @field_validator("slice_id", "file_id", "relative_packet_path")
    @classmethod
    def reject_blank_optional_anchor_fields(cls, value: str | None) -> str | None:
        # Optional: absent (None) for a derived_record anchor; non-empty when present. WHICH kinds
        # require them is enforced in validate_anchor_substrate. This field validator runs BEFORE
        # the model validators, so it must tolerate None or a derived_record anchor cannot construct.
        if value is not None and not value.strip():
            raise ValueError("CleaningRawAnchor preserved-file fields must be non-empty when set.")
        return value

    @model_validator(mode="after")
    def validate_anchor_specificity(self) -> "CleaningRawAnchor":
        if self.anchor_kind == "json_pointer" and not (
            self.json_pointer and self.json_pointer.strip()
        ):
            raise ValueError("json_pointer anchors require json_pointer.")
        # "file" and "derived_record" take the whole artifact -- no anchor_value; the remaining
        # specific kinds require one.
        if self.anchor_kind not in {"file", "json_pointer", "derived_record"} and not (
            self.anchor_value and self.anchor_value.strip()
        ):
            raise ValueError(f"{self.anchor_kind} anchors require anchor_value.")
        return self

    @model_validator(mode="after")
    def validate_anchor_substrate(self) -> "CleaningRawAnchor":
        """Enforce the two anchor shapes are never mixed: a ``derived_record`` anchor references a
        lake record (``derived_record_ref``, no preserved-file fields, no anchor_value/json_pointer);
        every other kind references a preserved file (slice_id/file_id/relative_packet_path present,
        no derived_record_ref)."""
        preserved_fields = (self.slice_id, self.file_id, self.relative_packet_path)
        if self.anchor_kind == "derived_record":
            if self.derived_record_ref is None:
                raise ValueError("derived_record anchors require derived_record_ref.")
            if any(field is not None for field in preserved_fields):
                raise ValueError(
                    "derived_record anchors must not carry slice_id/file_id/relative_packet_path."
                )
            if self.anchor_value is not None or self.json_pointer is not None:
                raise ValueError(
                    "derived_record anchors must not carry anchor_value or json_pointer."
                )
        else:
            if self.derived_record_ref is not None:
                raise ValueError(f"{self.anchor_kind} anchors must not carry derived_record_ref.")
            if any(field is None or not field.strip() for field in preserved_fields):
                raise ValueError(
                    f"{self.anchor_kind} anchors require slice_id, file_id, and relative_packet_path."
                )
        return self


class CleaningProjectionRef(StrictModel):
    projection_method: str
    projection_version: str
    certification: str
    packet_id: str
    row_id: str | None = None
    row_kind: str | None = None

    @field_validator("projection_method", "projection_version", "certification", "packet_id")
    @classmethod
    def reject_blank_projection_fields(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("CleaningProjectionRef fields must be non-empty.")
        return value

    @model_validator(mode="after")
    def validate_projection_is_not_cleaning_or_judgment(self) -> "CleaningProjectionRef":
        cert = self.certification.lower()
        if "not_cleaned" not in cert or "not_judgment_ready" not in cert:
            raise ValueError(
                "CleaningProjectionRef.certification must show the projection is "
                "not cleaned and not Judgment-ready."
            )
        return self


class CleaningEcrRef(StrictModel):
    packet_id: str
    ref_id: str
    posture_kind: str | None = None
    status: str | None = None

    @field_validator("packet_id", "ref_id")
    @classmethod
    def reject_blank_ecr_fields(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("CleaningEcrRef fields must be non-empty.")
        return value


class CleaningInputHandle(StrictModel):
    handle_id: str
    source_family: str
    source_surface: str
    raw_anchor: CleaningRawAnchor
    projection_ref: CleaningProjectionRef | None = None
    ecr_ref: CleaningEcrRef | None = None
    relation: CleaningRelation = CleaningRelation.KEYED_SIBLINGS_OVER_RAW
    residuals: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    raw_pull_triggers: list[str] = Field(default_factory=list)

    @field_validator("handle_id", "source_family", "source_surface")
    @classmethod
    def reject_blank_handle_fields(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("CleaningInputHandle fields must be non-empty.")
        return value

    @field_validator("residuals", "warnings", "raw_pull_triggers")
    @classmethod
    def reject_judgment_handle_reasons(cls, value: list[str]) -> list[str]:
        for item in value:
            forbidden = _find_token_matches(item, _JUDGMENT_TOKENS)
            if forbidden:
                raise ValueError(
                    "Cleaning input handle warnings/residuals/raw-pull triggers must use "
                    "layer-owned mechanical reasons, not Judgment vocabulary: "
                    + ", ".join(forbidden)
                )
        return value

    @model_validator(mode="after")
    def validate_refs_stay_keyed_to_raw(self) -> "CleaningInputHandle":
        if self.projection_ref is not None and self.projection_ref.packet_id != self.raw_anchor.packet_id:
            raise ValueError("projection_ref.packet_id must match raw_anchor.packet_id.")
        if self.ecr_ref is not None and self.ecr_ref.packet_id != self.raw_anchor.packet_id:
            raise ValueError("ecr_ref.packet_id must match raw_anchor.packet_id.")
        return self


class CleaningPreservationCheck(StrictModel):
    originals_addressable: bool
    source_identity_preserved: bool
    timing_preserved: bool
    hierarchy_preserved: bool
    semantic_binding_preserved: bool
    counts_preserved: bool

    @model_validator(mode="after")
    def validate_all_required_preservation_holds(self) -> "CleaningPreservationCheck":
        failed = [
            field
            for field in (
                "originals_addressable",
                "source_identity_preserved",
                "timing_preserved",
                "hierarchy_preserved",
                "semantic_binding_preserved",
                "counts_preserved",
            )
            if getattr(self, field) is not True
        ]
        if failed:
            raise ValueError(
                "Cleaning core v0 transform entries require preservation to hold: "
                + ", ".join(failed)
            )
        return self


class CleaningTransform(StrictModel):
    transform_class: CleaningTransformClass
    rule_scope: CleaningRuleScope
    method_or_rule: str
    input_grain: CleaningInputGrain
    output_view_ref: str | None = None
    original_value: str | None = None
    transformed_value: str | None = None

    @field_validator("method_or_rule")
    @classmethod
    def validate_method_or_rule(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("method_or_rule must be non-empty.")
        forbidden = _find_token_matches(value, _JUDGMENT_TOKENS)
        if forbidden:
            raise ValueError(
                "Cleaning transform method_or_rule must not carry Judgment vocabulary: "
                + ", ".join(forbidden)
            )
        return value

    @model_validator(mode="after")
    def validate_transform_contract(self) -> "CleaningTransform":
        method = re.sub(r"[^a-z0-9]+", "_", self.method_or_rule.lower()).strip("_")
        if self.transform_class == CleaningTransformClass.DEDUPE_MECHANICS:
            if method != "exact_identity":
                raise ValueError("core v0 dedupe_mechanics must use method_or_rule='exact_identity'.")
        deferred = _find_token_matches(self.method_or_rule, _DEFERRED_DEDUPE_TOKENS)
        if deferred:
            raise ValueError(
                "near-match, copied-language, and clustering mechanics are deferred in core v0: "
                + ", ".join(deferred)
            )
        if self.transform_class in {
            CleaningTransformClass.NORMALIZATION,
            CleaningTransformClass.TRANSLATION,
        } and (self.original_value is None or self.transformed_value is None):
            raise ValueError(
                "normalization and translation entries must preserve original_value "
                "and transformed_value."
            )
        if self.transform_class == CleaningTransformClass.SUMMARIZATION and (
            self.transformed_value is None and self.output_view_ref is None
        ):
            raise ValueError("summarization entries require transformed_value or output_view_ref.")
        return self


class CleaningTransformLedgerEntry(StrictModel):
    input_handle_id: str
    transform: CleaningTransform
    preservation: CleaningPreservationCheck
    omissions: list[str] = Field(default_factory=list)
    residuals: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    raw_pull_triggers: list[str] = Field(default_factory=list)
    non_claims: list[str] = Field(default_factory=lambda: sorted(REQUIRED_NON_CLAIMS))

    @field_validator("input_handle_id")
    @classmethod
    def reject_blank_input_handle_id(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("input_handle_id must be non-empty.")
        return value

    @field_validator("omissions", "residuals", "warnings", "raw_pull_triggers")
    @classmethod
    def reject_judgment_warning_reasons(cls, value: list[str]) -> list[str]:
        for item in value:
            forbidden = _find_token_matches(item, _JUDGMENT_TOKENS)
            if forbidden:
                raise ValueError(
                    "Cleaning warnings/residuals/raw-pull triggers must use layer-owned "
                    "mechanical reasons, not Judgment vocabulary: "
                    + ", ".join(forbidden)
                )
        return value

    @model_validator(mode="after")
    def validate_required_non_claims(self) -> "CleaningTransformLedgerEntry":
        missing = sorted(REQUIRED_NON_CLAIMS - set(self.non_claims))
        if missing:
            raise ValueError("Cleaning transform entry missing required non_claims: " + ", ".join(missing))
        return self


class CleaningDedupeGroup(StrictModel):
    group_id: str
    basis: CleaningDedupeBasis
    member_handle_ids: list[str] = Field(min_length=2)
    instance_count: int = Field(ge=2)

    @model_validator(mode="after")
    def validate_group_membership(self) -> "CleaningDedupeGroup":
        if self.instance_count != len(self.member_handle_ids):
            raise ValueError("instance_count must match member_handle_ids length.")
        if len(set(self.member_handle_ids)) != len(self.member_handle_ids):
            raise ValueError("member_handle_ids must be unique.")
        return self


class CleaningPacket(StrictModel):
    cleaning_version: Literal["v0"] = CLEANING_CORE_VERSION
    handles: list[CleaningInputHandle] = Field(min_length=1)
    transform_ledger: list[CleaningTransformLedgerEntry] = Field(default_factory=list)
    exact_identity_duplicate_groups: list[CleaningDedupeGroup] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_references(self) -> "CleaningPacket":
        handle_ids = [handle.handle_id for handle in self.handles]
        duplicate_handle_ids = sorted(
            handle_id for handle_id in set(handle_ids) if handle_ids.count(handle_id) > 1
        )
        if duplicate_handle_ids:
            raise ValueError("CleaningPacket handle_id values must be unique: " + ", ".join(duplicate_handle_ids))

        handle_id_set = set(handle_ids)
        unknown_transform_refs = sorted(
            entry.input_handle_id
            for entry in self.transform_ledger
            if entry.input_handle_id not in handle_id_set
        )
        if unknown_transform_refs:
            raise ValueError(
                "transform_ledger references unknown input_handle_id values: "
                + ", ".join(unknown_transform_refs)
            )

        unknown_group_refs = sorted(
            member
            for group in self.exact_identity_duplicate_groups
            for member in group.member_handle_ids
            if member not in handle_id_set
        )
        if unknown_group_refs:
            raise ValueError(
                "exact_identity_duplicate_groups reference unknown handle ids: "
                + ", ".join(unknown_group_refs)
            )
        return self
