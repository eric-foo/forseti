from __future__ import annotations

import hashlib
import html as html_lib
import json
import re
from html import unescape
from pathlib import Path
from types import SimpleNamespace
from typing import TYPE_CHECKING, Any, Literal, Mapping, Sequence
from urllib.parse import urlparse

from pydantic import Field, field_validator, model_validator

from harness_utils import generate_ulid
from schemas.case_models import StrictModel
from source_capture.models import PreservedFile, SourceCapturePacket, SourceCaptureSlice, VisibleFactStatus
from source_capture.projection_shared import is_forbidden_field_token_match

if TYPE_CHECKING:
    from data_lake.root import DataLakeRoot


RETAIL_PDP_PROJECTION_METHOD = "retail_pdp_mechanical_projection"
RETAIL_PDP_PROJECTION_VERSION = "v0"
RETAIL_PDP_PROJECTION_CERTIFICATION = "view_only; not_cleaned; not_normalized; not_judgment_ready"
SEPHORA_PDP_CONTENT_RECORD_KIND = "retail_pdp_sephora_aggregate_content"
SEPHORA_PDP_CONTENT_SCHEMA_VERSION = "retail_pdp_sephora_aggregate_content_v1"
SEPHORA_PDP_PARSER_VERSION = "retail_pdp_sephora_aggregate_parser_v1"
SEPHORA_PDP_CONTENT_PROFILE = "sephora_pdp_aggregate"
LUCKYSCENT_PDP_CONTENT_RECORD_KIND = "retail_pdp_luckyscent_aggregate_content"
LUCKYSCENT_PDP_CONTENT_SCHEMA_VERSION = "retail_pdp_luckyscent_aggregate_content_v1"
LUCKYSCENT_PDP_PARSER_VERSION = "retail_pdp_luckyscent_aggregate_parser_v1"
LUCKYSCENT_PDP_CONTENT_PROFILE = "luckyscent_pdp_aggregate"
NORDSTROM_PDP_CONTENT_RECORD_KIND = "retail_pdp_nordstrom_aggregate_content"
NORDSTROM_PDP_CONTENT_SCHEMA_VERSION = "retail_pdp_nordstrom_aggregate_content_v1"
NORDSTROM_PDP_PARSER_VERSION = "retail_pdp_nordstrom_aggregate_parser_v1"
NORDSTROM_PDP_CONTENT_PROFILE = "nordstrom_pdp_aggregate"

# Append-only derived lane namespace for the Retail/PDP projection's Silver record.
PROJECTION_RETAIL_PDP_LANE = "projection_retail_pdp"

Retailer = Literal[
    "amazon",
    "luckyscent",
    "nordstrom",
    "sephora",
    "ulta",
    "walmart",
    "target",
    "unknown",
]

_FORBIDDEN_SOURCE_VISIBLE_FIELD_NAMES = frozenset(
    {
        "action_ceiling",
        "action_supporting",
        "credibility",
        "decision_strength",
        "demand",
        "discount",
        "exclude",
        "excluded",
        "inclusion",
        "integrity",
        "judgment",
        "signal_use",
        "strength",
        "strong",
        "weak",
    }
)

_REQUIRED_RETAIL_STRUCTURE_BINDINGS = frozenset(
    {
        "sku_variant_price",
        "variant_availability",
        "review_substrate_for_product",
        "series_locale_currency",
    }
)


class RetailProjectionRawRef(StrictModel):
    packet_id: str
    slice_id: str


class RetailProjectionRawAnchor(StrictModel):
    file_id: str
    relative_packet_path: str
    sha256: str
    hash_basis: str
    anchor_kind: Literal["file", "html_selector", "script_index", "text_pattern", "json_pointer"]
    anchor_value: str | None = None

    @model_validator(mode="after")
    def validate_anchor_value(self) -> "RetailProjectionRawAnchor":
        if self.anchor_kind == "file":
            if self.anchor_value is not None:
                raise ValueError("file anchors must not carry anchor_value")
            return self
        if not (self.anchor_value and self.anchor_value.strip()):
            raise ValueError(f"{self.anchor_kind} anchors require anchor_value")
        if self.anchor_kind == "json_pointer" and not self.anchor_value.startswith("/"):
            raise ValueError("json_pointer anchors require an absolute JSON pointer")
        return self


class RetailPdpProjectionRow(StrictModel):
    row_id: str
    row_kind: Literal[
        "retail_pdp_product",
        "retail_variant_offer",
        "retail_review_substrate",
        "retail_embedded_structured_json",
        "retail_carried_module",
    ]
    retailer: Retailer
    raw_ref: RetailProjectionRawRef
    raw_anchor: RetailProjectionRawAnchor
    source_visible_fields: dict[str, Any | None] = Field(default_factory=dict)
    residuals: list[str] = Field(default_factory=list)

    @field_validator("source_visible_fields")
    @classmethod
    def reject_judgment_field_names(cls, value: dict[str, Any | None]) -> dict[str, Any | None]:
        forbidden = sorted(key for key in value if _is_forbidden_field_name(key))
        if forbidden:
            raise ValueError(
                "retail PDP projection source_visible_fields may carry raw facts only; "
                f"forbidden Judgment field(s): {', '.join(forbidden)}"
            )
        return value


class RetailPdpProjectionBinding(StrictModel):
    binding_type: Literal[
        "sku_variant_price",
        "variant_availability",
        "review_substrate_for_product",
        "series_locale_currency",
        "structured_json_for_product",
        "module_carried",
    ]
    row_id: str
    raw_ref: RetailProjectionRawRef
    raw_anchor: RetailProjectionRawAnchor
    source_visible_fields: dict[str, Any | None] = Field(default_factory=dict)

    @field_validator("source_visible_fields")
    @classmethod
    def reject_judgment_field_names(cls, value: dict[str, Any | None]) -> dict[str, Any | None]:
        forbidden = sorted(key for key in value if _is_forbidden_field_name(key))
        if forbidden:
            raise ValueError(
                "retail PDP projection bindings may carry raw facts only; "
                f"forbidden Judgment field(s): {', '.join(forbidden)}"
            )
        return value


class RetailPdpProjectionLossEntry(StrictModel):
    category: Literal["RETAIL_HERO_IMAGERY_COLLAPSED", "RETAIL_CART_NOTIFY_STATE_COLLAPSED"]
    count: int = Field(ge=0)
    raw_anchor: RetailProjectionRawAnchor
    reason: str


class RetailPdpProjectionLossLedger(StrictModel):
    collapsed: list[RetailPdpProjectionLossEntry] = Field(default_factory=list)
    preserved_evidence_rows: int = Field(ge=0)
    preserved_bindings: int = Field(ge=0)
    timing: Literal["separate_not_collapsed"] = "separate_not_collapsed"
    hierarchy_preserved: bool
    structure_preserved: bool
    certification: Literal["collapses_only_logged_frame_conditional_pdp_envelope; does_not_certify_cleaning"] = (
        "collapses_only_logged_frame_conditional_pdp_envelope; does_not_certify_cleaning"
    )


class RetailPdpProjectionPacket(StrictModel):
    projection_method: Literal["retail_pdp_mechanical_projection"] = RETAIL_PDP_PROJECTION_METHOD
    projection_version: Literal["v0"] = RETAIL_PDP_PROJECTION_VERSION
    certification: Literal["view_only; not_cleaned; not_normalized; not_judgment_ready"] = (
        RETAIL_PDP_PROJECTION_CERTIFICATION
    )
    packet_id: str
    rows: list[RetailPdpProjectionRow] = Field(default_factory=list)
    binding_map: list[RetailPdpProjectionBinding] = Field(default_factory=list)
    loss_ledger: RetailPdpProjectionLossLedger
    residuals: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_counts(self) -> "RetailPdpProjectionPacket":
        if self.loss_ledger.preserved_evidence_rows != len(self.rows):
            raise ValueError("loss_ledger.preserved_evidence_rows must match rows length")
        if self.loss_ledger.preserved_bindings != len(self.binding_map):
            raise ValueError("loss_ledger.preserved_bindings must match binding_map length")
        return self


SephoraContentAnchorKind = Literal["file", "html_selector", "script_index", "text_pattern"]


class SephoraPdpContentRow(StrictModel):
    slice_id: str
    row_id: str
    row_kind: Literal[
        "retail_pdp_product",
        "retail_variant_offer",
        "retail_review_substrate",
        "retail_embedded_structured_json",
        "retail_carried_module",
    ]
    retailer: Literal["sephora"] = "sephora"
    source_visible_fields: dict[str, Any | None] = Field(default_factory=dict)
    residuals: list[str] = Field(default_factory=list)
    source_anchor_kind: SephoraContentAnchorKind
    source_anchor_value: str | None = None

    @field_validator("source_visible_fields")
    @classmethod
    def reject_judgment_field_names(cls, value: dict[str, Any | None]) -> dict[str, Any | None]:
        forbidden = sorted(key for key in value if _is_forbidden_field_name(key))
        if forbidden:
            raise ValueError(
                "Sephora PDP content source_visible_fields may carry raw facts only; "
                f"forbidden Judgment field(s): {', '.join(forbidden)}"
            )
        return value

    @model_validator(mode="after")
    def validate_source_anchor(self) -> "SephoraPdpContentRow":
        if self.source_anchor_kind == "file":
            if self.source_anchor_value is not None:
                raise ValueError("file anchors must not carry source_anchor_value")
            return self
        if not (self.source_anchor_value and self.source_anchor_value.strip()):
            raise ValueError(f"{self.source_anchor_kind} anchors require source_anchor_value")
        return self


class SephoraPdpContentBinding(StrictModel):
    slice_id: str
    binding_type: Literal[
        "sku_variant_price",
        "variant_availability",
        "review_substrate_for_product",
        "series_locale_currency",
        "structured_json_for_product",
        "module_carried",
    ]
    row_id: str
    source_visible_fields: dict[str, Any | None] = Field(default_factory=dict)

    @field_validator("source_visible_fields")
    @classmethod
    def reject_judgment_field_names(cls, value: dict[str, Any | None]) -> dict[str, Any | None]:
        forbidden = sorted(key for key in value if _is_forbidden_field_name(key))
        if forbidden:
            raise ValueError(
                "Sephora PDP content bindings may carry raw facts only; "
                f"forbidden Judgment field(s): {', '.join(forbidden)}"
            )
        return value


class SephoraPdpContentLossEntry(StrictModel):
    category: Literal["RETAIL_HERO_IMAGERY_COLLAPSED", "RETAIL_CART_NOTIFY_STATE_COLLAPSED"]
    count: int = Field(ge=0)
    reason: str
    source_anchor_kind: SephoraContentAnchorKind
    source_anchor_value: str | None = None

    @model_validator(mode="after")
    def validate_source_anchor(self) -> "SephoraPdpContentLossEntry":
        if self.source_anchor_kind == "file":
            if self.source_anchor_value is not None:
                raise ValueError("file anchors must not carry source_anchor_value")
            return self
        if not (self.source_anchor_value and self.source_anchor_value.strip()):
            raise ValueError(f"{self.source_anchor_kind} anchors require source_anchor_value")
        return self


class SephoraPdpContentLossLedger(StrictModel):
    collapsed: list[SephoraPdpContentLossEntry] = Field(default_factory=list)
    preserved_evidence_rows: int = Field(ge=0)
    preserved_bindings: int = Field(ge=0)
    timing: Literal["separate_not_collapsed"] = "separate_not_collapsed"
    hierarchy_preserved: bool
    structure_preserved: bool
    certification: Literal[
        "collapses_only_logged_frame_conditional_pdp_envelope; does_not_certify_cleaning"
    ] = "collapses_only_logged_frame_conditional_pdp_envelope; does_not_certify_cleaning"


class SephoraPdpAggregateContentRecord(StrictModel):
    record_kind: Literal["retail_pdp_sephora_aggregate_content"] = (
        SEPHORA_PDP_CONTENT_RECORD_KIND
    )
    schema_version: Literal["retail_pdp_sephora_aggregate_content_v1"] = (
        SEPHORA_PDP_CONTENT_SCHEMA_VERSION
    )
    parser_version: Literal["retail_pdp_sephora_aggregate_parser_v1"] = (
        SEPHORA_PDP_PARSER_VERSION
    )
    capture_profile: Literal["sephora_pdp_aggregate"] = SEPHORA_PDP_CONTENT_PROFILE
    source_url: str
    rows: list[SephoraPdpContentRow] = Field(default_factory=list)
    binding_map: list[SephoraPdpContentBinding] = Field(default_factory=list)
    loss_ledger: SephoraPdpContentLossLedger
    residuals: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_counts(self) -> "SephoraPdpAggregateContentRecord":
        if self.loss_ledger.preserved_evidence_rows != len(self.rows):
            raise ValueError("loss_ledger.preserved_evidence_rows must match rows length")
        if self.loss_ledger.preserved_bindings != len(self.binding_map):
            raise ValueError("loss_ledger.preserved_bindings must match binding_map length")
        return self


LuckyscentContentAnchorKind = Literal[
    "file", "html_selector", "script_index", "text_pattern"
]


class LuckyscentPdpContentRow(StrictModel):
    slice_id: str
    row_id: str
    row_kind: Literal[
        "retail_pdp_product",
        "retail_variant_offer",
        "retail_review_substrate",
        "retail_embedded_structured_json",
        "retail_carried_module",
    ]
    retailer: Literal["luckyscent"] = "luckyscent"
    source_visible_fields: dict[str, Any | None] = Field(default_factory=dict)
    residuals: list[str] = Field(default_factory=list)
    source_anchor_kind: LuckyscentContentAnchorKind
    source_anchor_value: str | None = None

    @field_validator("source_visible_fields")
    @classmethod
    def reject_judgment_field_names(
        cls, value: dict[str, Any | None]
    ) -> dict[str, Any | None]:
        forbidden = sorted(key for key in value if _is_forbidden_field_name(key))
        if forbidden:
            raise ValueError(
                "Luckyscent PDP content source_visible_fields may carry raw facts only; "
                f"forbidden Judgment field(s): {', '.join(forbidden)}"
            )
        return value

    @model_validator(mode="after")
    def validate_source_anchor(self) -> "LuckyscentPdpContentRow":
        if self.source_anchor_kind == "file":
            if self.source_anchor_value is not None:
                raise ValueError("file anchors must not carry source_anchor_value")
            return self
        if not (self.source_anchor_value and self.source_anchor_value.strip()):
            raise ValueError(
                f"{self.source_anchor_kind} anchors require source_anchor_value"
            )
        return self


class LuckyscentPdpContentBinding(StrictModel):
    slice_id: str
    binding_type: Literal[
        "sku_variant_price",
        "variant_availability",
        "review_substrate_for_product",
        "series_locale_currency",
        "structured_json_for_product",
        "module_carried",
    ]
    row_id: str
    source_visible_fields: dict[str, Any | None] = Field(default_factory=dict)

    @field_validator("source_visible_fields")
    @classmethod
    def reject_judgment_field_names(
        cls, value: dict[str, Any | None]
    ) -> dict[str, Any | None]:
        forbidden = sorted(key for key in value if _is_forbidden_field_name(key))
        if forbidden:
            raise ValueError(
                "Luckyscent PDP content bindings may carry raw facts only; "
                f"forbidden Judgment field(s): {', '.join(forbidden)}"
            )
        return value


class LuckyscentPdpContentLossEntry(StrictModel):
    category: Literal[
        "RETAIL_HERO_IMAGERY_COLLAPSED", "RETAIL_CART_NOTIFY_STATE_COLLAPSED"
    ]
    count: int = Field(ge=0)
    reason: str
    source_anchor_kind: LuckyscentContentAnchorKind
    source_anchor_value: str | None = None

    @model_validator(mode="after")
    def validate_source_anchor(self) -> "LuckyscentPdpContentLossEntry":
        if self.source_anchor_kind == "file":
            if self.source_anchor_value is not None:
                raise ValueError("file anchors must not carry source_anchor_value")
            return self
        if not (self.source_anchor_value and self.source_anchor_value.strip()):
            raise ValueError(
                f"{self.source_anchor_kind} anchors require source_anchor_value"
            )
        return self


class LuckyscentPdpContentLossLedger(StrictModel):
    collapsed: list[LuckyscentPdpContentLossEntry] = Field(default_factory=list)
    preserved_evidence_rows: int = Field(ge=0)
    preserved_bindings: int = Field(ge=0)
    timing: Literal["separate_not_collapsed"] = "separate_not_collapsed"
    hierarchy_preserved: bool
    structure_preserved: bool
    certification: Literal[
        "collapses_only_logged_frame_conditional_pdp_envelope; does_not_certify_cleaning"
    ] = "collapses_only_logged_frame_conditional_pdp_envelope; does_not_certify_cleaning"


class LuckyscentPdpAggregateContentRecord(StrictModel):
    record_kind: Literal["retail_pdp_luckyscent_aggregate_content"] = (
        LUCKYSCENT_PDP_CONTENT_RECORD_KIND
    )
    schema_version: Literal["retail_pdp_luckyscent_aggregate_content_v1"] = (
        LUCKYSCENT_PDP_CONTENT_SCHEMA_VERSION
    )
    parser_version: Literal["retail_pdp_luckyscent_aggregate_parser_v1"] = (
        LUCKYSCENT_PDP_PARSER_VERSION
    )
    capture_profile: Literal["luckyscent_pdp_aggregate"] = (
        LUCKYSCENT_PDP_CONTENT_PROFILE
    )
    source_url: str
    rows: list[LuckyscentPdpContentRow] = Field(default_factory=list)
    binding_map: list[LuckyscentPdpContentBinding] = Field(default_factory=list)
    loss_ledger: LuckyscentPdpContentLossLedger
    residuals: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_counts(self) -> "LuckyscentPdpAggregateContentRecord":
        if self.loss_ledger.preserved_evidence_rows != len(self.rows):
            raise ValueError("loss_ledger.preserved_evidence_rows must match rows length")
        if self.loss_ledger.preserved_bindings != len(self.binding_map):
            raise ValueError("loss_ledger.preserved_bindings must match binding_map length")
        return self


NordstromContentAnchorKind = Literal[
    "file", "html_selector", "script_index", "text_pattern"
]


class NordstromPdpContentRow(StrictModel):
    slice_id: str
    row_id: str
    row_kind: Literal[
        "retail_pdp_product",
        "retail_variant_offer",
        "retail_review_substrate",
        "retail_embedded_structured_json",
        "retail_carried_module",
    ]
    retailer: Literal["nordstrom"] = "nordstrom"
    source_visible_fields: dict[str, Any | None] = Field(default_factory=dict)
    residuals: list[str] = Field(default_factory=list)
    source_anchor_kind: NordstromContentAnchorKind
    source_anchor_value: str | None = None

    @field_validator("source_visible_fields")
    @classmethod
    def reject_judgment_field_names(
        cls, value: dict[str, Any | None]
    ) -> dict[str, Any | None]:
        forbidden = sorted(key for key in value if _is_forbidden_field_name(key))
        if forbidden:
            raise ValueError(
                "Nordstrom PDP content source_visible_fields may carry raw facts only; "
                f"forbidden Judgment field(s): {', '.join(forbidden)}"
            )
        return value

    @model_validator(mode="after")
    def validate_source_anchor(self) -> "NordstromPdpContentRow":
        if self.source_anchor_kind == "file":
            if self.source_anchor_value is not None:
                raise ValueError("file anchors must not carry source_anchor_value")
            return self
        if not (self.source_anchor_value and self.source_anchor_value.strip()):
            raise ValueError(
                f"{self.source_anchor_kind} anchors require source_anchor_value"
            )
        return self


class NordstromPdpContentBinding(StrictModel):
    slice_id: str
    binding_type: Literal[
        "sku_variant_price",
        "variant_availability",
        "review_substrate_for_product",
        "series_locale_currency",
        "structured_json_for_product",
        "module_carried",
    ]
    row_id: str
    source_visible_fields: dict[str, Any | None] = Field(default_factory=dict)

    @field_validator("source_visible_fields")
    @classmethod
    def reject_judgment_field_names(
        cls, value: dict[str, Any | None]
    ) -> dict[str, Any | None]:
        forbidden = sorted(key for key in value if _is_forbidden_field_name(key))
        if forbidden:
            raise ValueError(
                "Nordstrom PDP content bindings may carry raw facts only; "
                f"forbidden Judgment field(s): {', '.join(forbidden)}"
            )
        return value


class NordstromPdpContentLossEntry(StrictModel):
    category: Literal[
        "RETAIL_HERO_IMAGERY_COLLAPSED", "RETAIL_CART_NOTIFY_STATE_COLLAPSED"
    ]
    count: int = Field(ge=0)
    reason: str
    source_anchor_kind: NordstromContentAnchorKind
    source_anchor_value: str | None = None

    @model_validator(mode="after")
    def validate_source_anchor(self) -> "NordstromPdpContentLossEntry":
        if self.source_anchor_kind == "file":
            if self.source_anchor_value is not None:
                raise ValueError("file anchors must not carry source_anchor_value")
            return self
        if not (self.source_anchor_value and self.source_anchor_value.strip()):
            raise ValueError(
                f"{self.source_anchor_kind} anchors require source_anchor_value"
            )
        return self


class NordstromPdpContentLossLedger(StrictModel):
    collapsed: list[NordstromPdpContentLossEntry] = Field(default_factory=list)
    preserved_evidence_rows: int = Field(ge=0)
    preserved_bindings: int = Field(ge=0)
    timing: Literal["separate_not_collapsed"] = "separate_not_collapsed"
    hierarchy_preserved: bool
    structure_preserved: bool
    certification: Literal[
        "collapses_only_logged_frame_conditional_pdp_envelope; does_not_certify_cleaning"
    ] = "collapses_only_logged_frame_conditional_pdp_envelope; does_not_certify_cleaning"


class NordstromPdpAggregateContentRecord(StrictModel):
    record_kind: Literal["retail_pdp_nordstrom_aggregate_content"] = (
        NORDSTROM_PDP_CONTENT_RECORD_KIND
    )
    schema_version: Literal["retail_pdp_nordstrom_aggregate_content_v1"] = (
        NORDSTROM_PDP_CONTENT_SCHEMA_VERSION
    )
    parser_version: Literal["retail_pdp_nordstrom_aggregate_parser_v1"] = (
        NORDSTROM_PDP_PARSER_VERSION
    )
    capture_profile: Literal["nordstrom_pdp_aggregate"] = (
        NORDSTROM_PDP_CONTENT_PROFILE
    )
    source_url: str
    rows: list[NordstromPdpContentRow] = Field(default_factory=list)
    binding_map: list[NordstromPdpContentBinding] = Field(default_factory=list)
    loss_ledger: NordstromPdpContentLossLedger
    residuals: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_counts(self) -> "NordstromPdpAggregateContentRecord":
        if self.loss_ledger.preserved_evidence_rows != len(self.rows):
            raise ValueError("loss_ledger.preserved_evidence_rows must match rows length")
        if self.loss_ledger.preserved_bindings != len(self.binding_map):
            raise ValueError("loss_ledger.preserved_bindings must match binding_map length")
        row_kinds = {row.row_kind for row in self.rows}
        required = {
            "retail_pdp_product",
            "retail_variant_offer",
            "retail_review_substrate",
        }
        if not required.issubset(row_kinds):
            raise ValueError(
                "Nordstrom content record requires product, offer, and review rows"
            )
        return self


def _retail_structure_preserved(bindings: Sequence[RetailPdpProjectionBinding]) -> bool:
    binding_types = {binding.binding_type for binding in bindings}
    return _REQUIRED_RETAIL_STRUCTURE_BINDINGS.issubset(binding_types)


class RetailPdpProjectionInputError(ValueError):
    """A packet directory cannot be projected without losing raw-file integrity."""


def build_retail_pdp_projection_from_packet_directory(*, packet_directory: Path) -> RetailPdpProjectionPacket:
    """Build a Retail/PDP projection from an existing local Source Capture Packet directory."""
    packet, raw_file_bytes_by_file_id = _load_packet_directory_projection_inputs(packet_directory)
    return build_retail_pdp_projection(packet=packet, raw_file_bytes_by_file_id=raw_file_bytes_by_file_id)


def write_retail_pdp_projection(*, packet_directory: Path, output_path: Path) -> RetailPdpProjectionPacket:
    """Write a projection JSON sidecar from an existing packet directory.

    This is a local view writer only: it reads ``manifest.json`` plus hash-verified
    preserved files, then writes the mechanical projection. It performs no capture,
    fetch, Cleaning, ECR, or Judgment work.
    """
    projection = build_retail_pdp_projection_from_packet_directory(packet_directory=packet_directory)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        f"{json.dumps(projection.model_dump(mode='json'), indent=2, sort_keys=True)}\n",
        encoding="utf-8",
    )
    return projection


def project_retail_pdp_into_lake(
    *,
    data_root: "DataLakeRoot",
    packet_id: str,
    record_id: str | None = None,
) -> tuple[RetailPdpProjectionPacket, Path]:
    """Project a committed raw packet -- read by key from the lake and
    hash-verified -- into a Retail/PDP projection, and append it as a derived
    record at ``derived/<packet_id>/projection_retail_pdp/<record_id>.json``
    (append-only; re-derive = new sibling).

    The verified read is the lake loader (``DataLakeRoot.load_raw_packet``); the
    extraction is byte-identical to the legacy directory path
    (``build_retail_pdp_projection_from_packet_directory``). This adds no capture,
    fetch, Cleaning, ECR, or Judgment. Returns the projection and the derived
    record path.
    """
    loaded = data_root.load_raw_packet(packet_id)
    packet = SourceCapturePacket.model_validate(loaded.manifest)
    projection = build_retail_pdp_projection(
        packet=packet,
        raw_file_bytes_by_file_id=loaded.bodies,
    )
    record = record_id if record_id is not None else generate_ulid()
    data = (
        f"{json.dumps(projection.model_dump(mode='json'), indent=2, sort_keys=True)}\n"
    ).encode("utf-8")
    derived_path = data_root.append_record(
        subtree="derived",
        raw_anchor=packet_id,
        lane=PROJECTION_RETAIL_PDP_LANE,
        record_id=f"{record}.json",
        data=data,
    )
    return projection, derived_path


def build_retail_pdp_projection(
    *,
    packet: SourceCapturePacket,
    raw_file_bytes_by_file_id: Mapping[str, bytes],
) -> RetailPdpProjectionPacket:
    """Derive a traceable, mechanical Retail/PDP row view from preserved packet bytes.

    This is not a parser authority, Cleaning transform, ECR schema, or Judgment
    read. It only projects rendered PDP capture bytes into inspectable rows that
    carry packet/slice/file/hash anchors and preserves embedded structured JSON
    verbatim when present.
    """
    preserved_files = {item.file_id: item for item in packet.preserved_files}
    content_files = [
        item
        for item in packet.preserved_files
        if item.relative_packet_path.replace("\\", "/").endswith("content_record.json")
    ]
    if content_files:
        if len(content_files) != 1:
            raise ValueError("Retail PDP packet must preserve exactly one content_record.json")
        content_file = content_files[0]
        content_bytes = raw_file_bytes_by_file_id.get(content_file.file_id)
        if content_bytes is None:
            raise ValueError(
                f"content record bytes are required for preserved file id: {content_file.file_id}"
            )
        record_kind = _content_record_kind(content_bytes)
        if record_kind == SEPHORA_PDP_CONTENT_RECORD_KIND:
            _validate_sephora_content_packet_metadata(
                packet=packet,
                raw_file_bytes_by_file_id=raw_file_bytes_by_file_id,
            )
            return _projection_from_sephora_content_record(
                packet=packet,
                content_file=content_file,
                content_bytes=content_bytes,
            )
        if record_kind == LUCKYSCENT_PDP_CONTENT_RECORD_KIND:
            _validate_luckyscent_content_packet_metadata(
                packet=packet,
                raw_file_bytes_by_file_id=raw_file_bytes_by_file_id,
            )
            return _projection_from_luckyscent_content_record(
                packet=packet,
                content_file=content_file,
                content_bytes=content_bytes,
            )
        if record_kind == NORDSTROM_PDP_CONTENT_RECORD_KIND:
            _validate_nordstrom_content_packet_metadata(
                packet=packet,
                raw_file_bytes_by_file_id=raw_file_bytes_by_file_id,
            )
            return _projection_from_nordstrom_content_record(
                packet=packet,
                content_file=content_file,
                content_bytes=content_bytes,
            )
        raise ValueError(f"unsupported Retail PDP content record kind: {record_kind!r}")

    rows: list[RetailPdpProjectionRow] = []
    bindings: list[RetailPdpProjectionBinding] = []
    collapsed: list[RetailPdpProjectionLossEntry] = []
    residuals: list[str] = []
    retailer = _detect_retailer(packet)

    for source_slice in packet.source_slices:
        raw_ref = RetailProjectionRawRef(packet_id=packet.packet_id, slice_id=source_slice.slice_id)
        slice_files: list[tuple[PreservedFile, bytes]] = []
        for file_id in source_slice.preserved_file_ids:
            preserved_file = preserved_files[file_id]
            body = raw_file_bytes_by_file_id.get(file_id)
            if body is None:
                raise ValueError(f"raw bytes are required for preserved file id: {file_id}")
            slice_files.append((preserved_file, body))

        html_files = [
            (preserved_file, body)
            for preserved_file, body in slice_files
            if preserved_file.relative_packet_path.lower().endswith((".html", ".htm"))
            or (
                packet.source_surface == "direct_http"
                and preserved_file.relative_packet_path.replace("\\", "/")
                .lower()
                .endswith("http_response_body.bin")
            )
        ]
        visible_text_files = [
            (preserved_file, _decode_text(body))
            for preserved_file, body in slice_files
            if preserved_file.relative_packet_path.lower().endswith(".txt")
        ]
        visible_text = "\n".join(text for _preserved_file, text in visible_text_files)

        if not html_files:
            residuals.append(f"{source_slice.slice_id}:retail_pdp_rendered_dom_absent")
            continue

        for preserved_file, body in html_files:
            html = _decode_text(body)
            projected = _project_retail_html(
                html,
                visible_text=visible_text,
                packet=packet,
                source_slice=source_slice,
                raw_ref=raw_ref,
                visible_text_files=visible_text_files,
                raw_anchor=_raw_anchor(preserved_file),
                retailer=retailer,
            )
            rows.extend(projected.rows)
            bindings.extend(projected.bindings)
            collapsed.extend(projected.collapsed)
            residuals.extend(projected.residuals)

    return RetailPdpProjectionPacket(
        packet_id=packet.packet_id,
        rows=rows,
        binding_map=bindings,
        loss_ledger=RetailPdpProjectionLossLedger(
            collapsed=collapsed,
            preserved_evidence_rows=len(rows),
            preserved_bindings=len(bindings),
            # Retail PDPs have no parent->reply thread hierarchy; retail structure is attested
            # through the binding map instead.
            hierarchy_preserved=True,
            structure_preserved=_retail_structure_preserved(bindings),
        ),
        residuals=residuals,
    )


def build_sephora_pdp_aggregate_content_record(
    *,
    rendered_dom: bytes,
    visible_text: bytes,
    source_url: str,
) -> dict[str, Any]:
    """Parse the pinned Sephora aggregate PDP without inventing packet/file identity."""
    if not isinstance(rendered_dom, bytes) or not isinstance(visible_text, bytes):
        raise TypeError("rendered_dom and visible_text must be bytes")
    parsed_url = urlparse(source_url)
    if parsed_url.scheme not in {"http", "https"} or parsed_url.hostname not in {
        "sephora.com",
        "www.sephora.com",
    }:
        raise ValueError("Sephora aggregate content records require a sephora.com source URL")

    slice_id = "cloakbrowser_snapshot_01"
    source_fact = SimpleNamespace(status=VisibleFactStatus.KNOWN, value=source_url)
    source_slice = SimpleNamespace(
        slice_id=slice_id,
        locator=source_fact,
        timing=SimpleNamespace(capture_time=None, cutoff_posture=None),
        archive_history_posture=None,
        locale_pin=None,
        currency_pin=None,
        variant_pin=None,
    )
    packet = SimpleNamespace(
        source_family="retail_pdp",
        source_surface="cloakbrowser_snapshot",
        source_locator=source_fact,
        series_id=None,
    )
    raw_ref = RetailProjectionRawRef(
        packet_id="content_record_unbound",
        slice_id=slice_id,
    )
    dom_anchor = RetailProjectionRawAnchor(
        file_id="content_input_rendered_dom",
        relative_packet_path="cloakbrowser_rendered_dom.html",
        sha256=hashlib.sha256(rendered_dom).hexdigest(),
        hash_basis="raw_stored_bytes",
        anchor_kind="file",
    )
    visible_text_file = PreservedFile(
        file_id="content_input_visible_text",
        original_path="cloakbrowser_visible_text.txt",
        relative_packet_path="cloakbrowser_visible_text.txt",
        sha256=hashlib.sha256(visible_text).hexdigest(),
        hash_basis="raw_stored_bytes",
        size_bytes=len(visible_text),
    )
    projected = _project_retail_html(
        _decode_text(rendered_dom),
        visible_text_files=[(visible_text_file, _decode_text(visible_text))],
        visible_text=_decode_text(visible_text),
        packet=packet,
        source_slice=source_slice,
        raw_ref=raw_ref,
        raw_anchor=dom_anchor,
        retailer="sephora",
    )
    record = SephoraPdpAggregateContentRecord(
        source_url=source_url,
        rows=[_sephora_content_row(row) for row in projected.rows],
        binding_map=[
            _sephora_content_binding(binding) for binding in projected.bindings
        ],
        loss_ledger=SephoraPdpContentLossLedger(
            collapsed=[
                SephoraPdpContentLossEntry(
                    category=entry.category,
                    count=entry.count,
                    reason=entry.reason,
                    source_anchor_kind=entry.raw_anchor.anchor_kind,
                    source_anchor_value=entry.raw_anchor.anchor_value,
                )
                for entry in projected.collapsed
            ],
            preserved_evidence_rows=len(projected.rows),
            preserved_bindings=len(projected.bindings),
            hierarchy_preserved=True,
            structure_preserved=_retail_structure_preserved(projected.bindings),
        ),
        residuals=projected.residuals,
    )
    return record.model_dump(mode="json")


def build_luckyscent_pdp_aggregate_content_record(
    *,
    rendered_dom: bytes,
    visible_text: bytes,
    source_url: str,
) -> dict[str, Any]:
    """Parse the pinned Luckyscent aggregate PDP without packet/file placeholders."""
    if not isinstance(rendered_dom, bytes) or not isinstance(visible_text, bytes):
        raise TypeError("rendered_dom and visible_text must be bytes")
    parsed_url = urlparse(source_url)
    if parsed_url.scheme not in {"http", "https"} or parsed_url.hostname not in {
        "luckyscent.com",
        "www.luckyscent.com",
    }:
        raise ValueError(
            "Luckyscent aggregate content records require a luckyscent.com source URL"
        )

    slice_id = "cloakbrowser_snapshot_01"
    source_fact = SimpleNamespace(status=VisibleFactStatus.KNOWN, value=source_url)
    source_slice = SimpleNamespace(
        slice_id=slice_id,
        locator=source_fact,
        timing=SimpleNamespace(capture_time=None, cutoff_posture=None),
        archive_history_posture=None,
        locale_pin=None,
        currency_pin=None,
        variant_pin=None,
    )
    packet = SimpleNamespace(
        source_family="retail_pdp",
        source_surface="cloakbrowser_snapshot",
        source_locator=source_fact,
        series_id=None,
    )
    raw_ref = RetailProjectionRawRef(
        packet_id="content_record_unbound",
        slice_id=slice_id,
    )
    dom_anchor = RetailProjectionRawAnchor(
        file_id="content_input_rendered_dom",
        relative_packet_path="cloakbrowser_rendered_dom.html",
        sha256=hashlib.sha256(rendered_dom).hexdigest(),
        hash_basis="raw_stored_bytes",
        anchor_kind="file",
    )
    visible_text_file = PreservedFile(
        file_id="content_input_visible_text",
        original_path="cloakbrowser_visible_text.txt",
        relative_packet_path="cloakbrowser_visible_text.txt",
        sha256=hashlib.sha256(visible_text).hexdigest(),
        hash_basis="raw_stored_bytes",
        size_bytes=len(visible_text),
    )
    projected = _project_retail_html(
        _decode_text(rendered_dom),
        visible_text_files=[(visible_text_file, _decode_text(visible_text))],
        visible_text=_decode_text(visible_text),
        packet=packet,
        source_slice=source_slice,
        raw_ref=raw_ref,
        raw_anchor=dom_anchor,
        retailer="luckyscent",
    )
    _validate_luckyscent_projected_content(projected, source_url=source_url)
    record = LuckyscentPdpAggregateContentRecord(
        source_url=source_url,
        rows=[_luckyscent_content_row(row) for row in projected.rows],
        binding_map=[
            _luckyscent_content_binding(binding) for binding in projected.bindings
        ],
        loss_ledger=LuckyscentPdpContentLossLedger(
            collapsed=[
                LuckyscentPdpContentLossEntry(
                    category=entry.category,
                    count=entry.count,
                    reason=entry.reason,
                    source_anchor_kind=entry.raw_anchor.anchor_kind,
                    source_anchor_value=entry.raw_anchor.anchor_value,
                )
                for entry in projected.collapsed
            ],
            preserved_evidence_rows=len(projected.rows),
            preserved_bindings=len(projected.bindings),
            hierarchy_preserved=True,
            structure_preserved=_retail_structure_preserved(projected.bindings),
        ),
        residuals=projected.residuals,
    )
    return record.model_dump(mode="json")


def _projection_from_sephora_content_record(
    *,
    packet: SourceCapturePacket,
    content_file: PreservedFile,
    content_bytes: bytes,
) -> RetailPdpProjectionPacket:
    try:
        record = SephoraPdpAggregateContentRecord.model_validate_json(content_bytes)
    except Exception as exc:
        raise ValueError(f"invalid Sephora PDP content record: {exc}") from exc
    if packet.source_family != "retail_pdp" or packet.source_surface != "cloakbrowser_snapshot":
        raise ValueError(
            "Sephora PDP content records require retail_pdp/cloakbrowser_snapshot packets"
        )
    if _detect_retailer(packet) != "sephora":
        raise ValueError("Sephora PDP content record does not match packet retailer identity")

    slice_by_id = {source_slice.slice_id: source_slice for source_slice in packet.source_slices}
    matching_source_urls = {
        _fact_value(source_slice.locator)
        for source_slice in packet.source_slices
        if _fact_value(source_slice.locator)
    }
    if record.source_url not in matching_source_urls:
        raise ValueError(
            f"Sephora content record source_url {record.source_url!r} does not match "
            "a packet source-slice locator"
        )

    rows: list[RetailPdpProjectionRow] = []
    for index, content_row in enumerate(record.rows):
        source_slice = slice_by_id.get(content_row.slice_id)
        if source_slice is None or content_file.file_id not in source_slice.preserved_file_ids:
            raise ValueError(
                f"Sephora content row references invalid source slice: {content_row.slice_id}"
            )
        fields = dict(content_row.source_visible_fields)
        if content_row.row_kind == "retail_pdp_product":
            fields = _product_context_fields(packet, source_slice, "sephora")
        rows.append(
            RetailPdpProjectionRow(
                row_id=content_row.row_id,
                row_kind=content_row.row_kind,
                retailer="sephora",
                raw_ref=RetailProjectionRawRef(
                    packet_id=packet.packet_id,
                    slice_id=content_row.slice_id,
                ),
                raw_anchor=_sephora_content_record_anchor(
                    content_file, f"/rows/{index}"
                ),
                source_visible_fields=fields,
                residuals=content_row.residuals,
            )
        )

    bindings: list[RetailPdpProjectionBinding] = []
    for index, content_binding in enumerate(record.binding_map):
        source_slice = slice_by_id.get(content_binding.slice_id)
        if source_slice is None or content_file.file_id not in source_slice.preserved_file_ids:
            raise ValueError(
                "Sephora content binding references invalid source slice: "
                f"{content_binding.slice_id}"
            )
        fields = dict(content_binding.source_visible_fields)
        if content_binding.binding_type == "series_locale_currency":
            fields = {
                "series_id": packet.series_id,
                "locale_pin": _fact_value(source_slice.locale_pin),
                "currency_pin": _fact_value(source_slice.currency_pin),
                "variant_pin": _fact_value(source_slice.variant_pin),
            }
        bindings.append(
            RetailPdpProjectionBinding(
                binding_type=content_binding.binding_type,
                row_id=content_binding.row_id,
                raw_ref=RetailProjectionRawRef(
                    packet_id=packet.packet_id,
                    slice_id=content_binding.slice_id,
                ),
                raw_anchor=_sephora_content_record_anchor(
                    content_file, f"/binding_map/{index}"
                ),
                source_visible_fields=fields,
            )
        )

    collapsed = [
        RetailPdpProjectionLossEntry(
            category=entry.category,
            count=entry.count,
            reason=entry.reason,
            raw_anchor=_sephora_content_record_anchor(
                content_file, f"/loss_ledger/collapsed/{index}"
            ),
        )
        for index, entry in enumerate(record.loss_ledger.collapsed)
    ]
    return RetailPdpProjectionPacket(
        packet_id=packet.packet_id,
        rows=rows,
        binding_map=bindings,
        loss_ledger=RetailPdpProjectionLossLedger(
            collapsed=collapsed,
            preserved_evidence_rows=len(rows),
            preserved_bindings=len(bindings),
            hierarchy_preserved=record.loss_ledger.hierarchy_preserved,
            structure_preserved=record.loss_ledger.structure_preserved,
        ),
        residuals=record.residuals,
    )


def _projection_from_luckyscent_content_record(
    *,
    packet: SourceCapturePacket,
    content_file: PreservedFile,
    content_bytes: bytes,
) -> RetailPdpProjectionPacket:
    try:
        record = LuckyscentPdpAggregateContentRecord.model_validate_json(content_bytes)
    except Exception as exc:
        raise ValueError(f"invalid Luckyscent PDP content record: {exc}") from exc
    if packet.source_family != "retail_pdp" or packet.source_surface != "cloakbrowser_snapshot":
        raise ValueError(
            "Luckyscent PDP content records require retail_pdp/cloakbrowser_snapshot packets"
        )
    if _detect_retailer(packet) != "luckyscent":
        raise ValueError(
            "Luckyscent PDP content record does not match packet retailer identity"
        )

    slice_by_id = {source_slice.slice_id: source_slice for source_slice in packet.source_slices}
    matching_source_urls = {
        _fact_value(source_slice.locator)
        for source_slice in packet.source_slices
        if _fact_value(source_slice.locator)
    }
    if record.source_url not in matching_source_urls:
        raise ValueError(
            f"Luckyscent content record source_url {record.source_url!r} does not match "
            "a packet source-slice locator"
        )

    rows: list[RetailPdpProjectionRow] = []
    for index, content_row in enumerate(record.rows):
        source_slice = slice_by_id.get(content_row.slice_id)
        if source_slice is None or content_file.file_id not in source_slice.preserved_file_ids:
            raise ValueError(
                f"Luckyscent content row references invalid source slice: {content_row.slice_id}"
            )
        fields = dict(content_row.source_visible_fields)
        if content_row.row_kind == "retail_pdp_product":
            fields = _product_context_fields(packet, source_slice, "luckyscent")
        rows.append(
            RetailPdpProjectionRow(
                row_id=content_row.row_id,
                row_kind=content_row.row_kind,
                retailer="luckyscent",
                raw_ref=RetailProjectionRawRef(
                    packet_id=packet.packet_id,
                    slice_id=content_row.slice_id,
                ),
                raw_anchor=_luckyscent_content_record_anchor(
                    content_file, f"/rows/{index}"
                ),
                source_visible_fields=fields,
                residuals=content_row.residuals,
            )
        )

    bindings: list[RetailPdpProjectionBinding] = []
    for index, content_binding in enumerate(record.binding_map):
        source_slice = slice_by_id.get(content_binding.slice_id)
        if source_slice is None or content_file.file_id not in source_slice.preserved_file_ids:
            raise ValueError(
                "Luckyscent content binding references invalid source slice: "
                f"{content_binding.slice_id}"
            )
        fields = dict(content_binding.source_visible_fields)
        if content_binding.binding_type == "series_locale_currency":
            fields = {
                "series_id": packet.series_id,
                "locale_pin": _fact_value(source_slice.locale_pin),
                "currency_pin": _fact_value(source_slice.currency_pin),
                "variant_pin": _fact_value(source_slice.variant_pin),
            }
        bindings.append(
            RetailPdpProjectionBinding(
                binding_type=content_binding.binding_type,
                row_id=content_binding.row_id,
                raw_ref=RetailProjectionRawRef(
                    packet_id=packet.packet_id,
                    slice_id=content_binding.slice_id,
                ),
                raw_anchor=_luckyscent_content_record_anchor(
                    content_file, f"/binding_map/{index}"
                ),
                source_visible_fields=fields,
            )
        )

    collapsed = [
        RetailPdpProjectionLossEntry(
            category=entry.category,
            count=entry.count,
            reason=entry.reason,
            raw_anchor=_luckyscent_content_record_anchor(
                content_file, f"/loss_ledger/collapsed/{index}"
            ),
        )
        for index, entry in enumerate(record.loss_ledger.collapsed)
    ]
    return RetailPdpProjectionPacket(
        packet_id=packet.packet_id,
        rows=rows,
        binding_map=bindings,
        loss_ledger=RetailPdpProjectionLossLedger(
            collapsed=collapsed,
            preserved_evidence_rows=len(rows),
            preserved_bindings=len(bindings),
            hierarchy_preserved=record.loss_ledger.hierarchy_preserved,
            structure_preserved=record.loss_ledger.structure_preserved,
        ),
        residuals=record.residuals,
    )


def _sephora_content_row(row: RetailPdpProjectionRow) -> SephoraPdpContentRow:
    fields = dict(row.source_visible_fields)
    if row.row_kind == "retail_pdp_product":
        fields = {}
    return SephoraPdpContentRow(
        slice_id=row.raw_ref.slice_id,
        row_id=row.row_id,
        row_kind=row.row_kind,
        retailer="sephora",
        source_visible_fields=fields,
        residuals=row.residuals,
        source_anchor_kind=row.raw_anchor.anchor_kind,
        source_anchor_value=row.raw_anchor.anchor_value,
    )


def _sephora_content_binding(
    binding: RetailPdpProjectionBinding,
) -> SephoraPdpContentBinding:
    fields = dict(binding.source_visible_fields)
    if binding.binding_type == "series_locale_currency":
        fields = {}
    return SephoraPdpContentBinding(
        slice_id=binding.raw_ref.slice_id,
        binding_type=binding.binding_type,
        row_id=binding.row_id,
        source_visible_fields=fields,
    )


def _luckyscent_content_row(
    row: RetailPdpProjectionRow,
) -> LuckyscentPdpContentRow:
    fields = dict(row.source_visible_fields)
    if row.row_kind == "retail_pdp_product":
        fields = {}
    return LuckyscentPdpContentRow(
        slice_id=row.raw_ref.slice_id,
        row_id=row.row_id,
        row_kind=row.row_kind,
        retailer="luckyscent",
        source_visible_fields=fields,
        residuals=row.residuals,
        source_anchor_kind=row.raw_anchor.anchor_kind,
        source_anchor_value=row.raw_anchor.anchor_value,
    )


def _luckyscent_content_binding(
    binding: RetailPdpProjectionBinding,
) -> LuckyscentPdpContentBinding:
    fields = dict(binding.source_visible_fields)
    if binding.binding_type == "series_locale_currency":
        fields = {}
    return LuckyscentPdpContentBinding(
        slice_id=binding.raw_ref.slice_id,
        binding_type=binding.binding_type,
        row_id=binding.row_id,
        source_visible_fields=fields,
    )


def _sephora_content_record_anchor(
    content_file: PreservedFile,
    json_pointer: str,
) -> RetailProjectionRawAnchor:
    return RetailProjectionRawAnchor(
        file_id=content_file.file_id,
        relative_packet_path=content_file.relative_packet_path,
        sha256=content_file.sha256,
        hash_basis=content_file.hash_basis,
        anchor_kind="json_pointer",
        anchor_value=json_pointer,
    )


def _luckyscent_content_record_anchor(
    content_file: PreservedFile,
    json_pointer: str,
) -> RetailProjectionRawAnchor:
    return RetailProjectionRawAnchor(
        file_id=content_file.file_id,
        relative_packet_path=content_file.relative_packet_path,
        sha256=content_file.sha256,
        hash_basis=content_file.hash_basis,
        anchor_kind="json_pointer",
        anchor_value=json_pointer,
    )


def _validate_sephora_content_packet_metadata(
    *,
    packet: SourceCapturePacket,
    raw_file_bytes_by_file_id: Mapping[str, bytes],
) -> None:
    def _one_json(filename: str) -> dict[str, Any]:
        matches = [
            item
            for item in packet.preserved_files
            if item.relative_packet_path.replace("\\", "/").endswith(filename)
        ]
        if len(matches) != 1:
            raise ValueError(
                f"Sephora content packet must preserve exactly one {filename}"
            )
        body = raw_file_bytes_by_file_id.get(matches[0].file_id)
        if body is None:
            raise ValueError(
                f"preserved bytes are required for {matches[0].file_id}: {filename}"
            )
        try:
            value = json.loads(body)
        except Exception as exc:
            raise ValueError(f"invalid {filename}: {exc}") from exc
        if not isinstance(value, dict):
            raise ValueError(f"{filename} must contain a JSON object")
        return value

    capture_metadata = _one_json("content_capture_metadata.json")
    if capture_metadata.get("parser_version") != SEPHORA_PDP_PARSER_VERSION:
        raise ValueError("Sephora content packet parser version does not match current")
    if capture_metadata.get("projection_status") != "succeeded":
        raise ValueError("Sephora content packet projection did not succeed")
    if capture_metadata.get("capture_artifact_mode") not in {"content", "sample"}:
        raise ValueError("Sephora content packet must use content or sample mode")

    browser_metadata = _one_json("cloakbrowser_snapshot_metadata.json")
    profile = browser_metadata.get("retail_capture_profile")
    if not isinstance(profile, dict) or profile.get("name") != SEPHORA_PDP_CONTENT_PROFILE:
        raise ValueError("Sephora content packet capture profile does not match")
    if browser_metadata.get("pin_confirmed") is not True:
        raise ValueError("Sephora content packet does not carry a confirmed US/USD market pin")


def _validate_luckyscent_content_packet_metadata(
    *,
    packet: SourceCapturePacket,
    raw_file_bytes_by_file_id: Mapping[str, bytes],
) -> None:
    def _one_json(filename: str) -> dict[str, Any]:
        matches = [
            item
            for item in packet.preserved_files
            if item.relative_packet_path.replace("\\", "/").endswith(filename)
        ]
        if len(matches) != 1:
            raise ValueError(
                f"Luckyscent content packet must preserve exactly one {filename}"
            )
        body = raw_file_bytes_by_file_id.get(matches[0].file_id)
        if body is None:
            raise ValueError(
                f"preserved bytes are required for {matches[0].file_id}: {filename}"
            )
        try:
            value = json.loads(body)
        except Exception as exc:
            raise ValueError(f"invalid {filename}: {exc}") from exc
        if not isinstance(value, dict):
            raise ValueError(f"{filename} must contain a JSON object")
        return value

    capture_metadata = _one_json("content_capture_metadata.json")
    if capture_metadata.get("parser_version") != LUCKYSCENT_PDP_PARSER_VERSION:
        raise ValueError("Luckyscent content packet parser version does not match current")
    if capture_metadata.get("projection_status") != "succeeded":
        raise ValueError("Luckyscent content packet projection did not succeed")
    if capture_metadata.get("capture_artifact_mode") not in {"content", "sample"}:
        raise ValueError("Luckyscent content packet must use content or sample mode")

    browser_metadata = _one_json("cloakbrowser_snapshot_metadata.json")
    profile = browser_metadata.get("retail_capture_profile")
    if (
        not isinstance(profile, dict)
        or profile.get("name") != LUCKYSCENT_PDP_CONTENT_PROFILE
    ):
        raise ValueError("Luckyscent content packet capture profile does not match")
    if browser_metadata.get("pin_confirmed") is not True:
        raise ValueError(
            "Luckyscent content packet does not carry a confirmed US/USD market pin"
        )


def build_nordstrom_pdp_aggregate_content_record(
    *,
    rendered_dom: bytes,
    visible_text: bytes,
    source_url: str,
) -> dict[str, Any]:
    """Parse the pinned Nordstrom aggregate PDP without inventing packet identity."""
    if not isinstance(rendered_dom, bytes) or not isinstance(visible_text, bytes):
        raise TypeError("rendered_dom and visible_text must be bytes")
    parsed_url = urlparse(source_url)
    product_id = _nordstrom_product_id_from_url(source_url)
    if (
        parsed_url.scheme not in {"http", "https"}
        or parsed_url.hostname not in {"nordstrom.com", "www.nordstrom.com"}
        or product_id is None
    ):
        raise ValueError(
            "Nordstrom aggregate content records require a nordstrom.com "
            "/s/<slug>/<numeric-id> source URL"
        )

    slice_id = "cloakbrowser_snapshot_01"
    source_fact = SimpleNamespace(status=VisibleFactStatus.KNOWN, value=source_url)
    source_slice = SimpleNamespace(
        slice_id=slice_id,
        locator=source_fact,
        timing=SimpleNamespace(capture_time=None, cutoff_posture=None),
        archive_history_posture=None,
        locale_pin=None,
        currency_pin=None,
        variant_pin=None,
    )
    packet = SimpleNamespace(
        source_family="retail_pdp",
        source_surface="cloakbrowser_snapshot",
        source_locator=source_fact,
        series_id=None,
    )
    raw_ref = RetailProjectionRawRef(
        packet_id="content_record_unbound",
        slice_id=slice_id,
    )
    dom_anchor = RetailProjectionRawAnchor(
        file_id="content_input_rendered_dom",
        relative_packet_path="cloakbrowser_rendered_dom.html",
        sha256=hashlib.sha256(rendered_dom).hexdigest(),
        hash_basis="raw_stored_bytes",
        anchor_kind="file",
    )
    visible_text_file = PreservedFile(
        file_id="content_input_visible_text",
        original_path="cloakbrowser_visible_text.txt",
        relative_packet_path="cloakbrowser_visible_text.txt",
        sha256=hashlib.sha256(visible_text).hexdigest(),
        hash_basis="raw_stored_bytes",
        size_bytes=len(visible_text),
    )
    projected = _project_retail_html(
        _decode_text(rendered_dom),
        visible_text_files=[(visible_text_file, _decode_text(visible_text))],
        visible_text=_decode_text(visible_text),
        packet=packet,
        source_slice=source_slice,
        raw_ref=raw_ref,
        raw_anchor=dom_anchor,
        retailer="nordstrom",
    )
    offer_rows = [
        row for row in projected.rows if row.row_kind == "retail_variant_offer"
    ]
    review_rows = [
        row for row in projected.rows if row.row_kind == "retail_review_substrate"
    ]
    if len(offer_rows) != 1 or len(review_rows) != 1:
        raise ValueError(
            "Nordstrom aggregate projection requires exactly one offer and one review row"
        )
    offer = offer_rows[0].source_visible_fields
    review = review_rows[0].source_visible_fields
    if _string_or_none(offer.get("product_id")) != product_id:
        raise ValueError("Nordstrom projected product id does not match the requested URL")
    if _string_or_none(offer.get("price_currency")) != "USD":
        raise ValueError("Nordstrom projected offer does not carry USD")
    if _string_or_none(offer.get("seller")) != "Nordstrom":
        raise ValueError("Nordstrom projected offer lacks target-bound seller evidence")
    if not _string_or_none(offer.get("availability")):
        raise ValueError("Nordstrom projected offer lacks target-bound availability")
    if (
        not _string_or_none(review.get("rating"))
        or not _string_or_none(review.get("review_count"))
        or not isinstance(review.get("rating_distribution_buckets"), dict)
        or not review.get("rendered_reviews")
    ):
        raise ValueError(
            "Nordstrom projected review substrate lacks rating, count, histogram, "
            "or rendered review bodies"
        )

    record = NordstromPdpAggregateContentRecord(
        source_url=source_url,
        rows=[_nordstrom_content_row(row) for row in projected.rows],
        binding_map=[
            _nordstrom_content_binding(binding) for binding in projected.bindings
        ],
        loss_ledger=NordstromPdpContentLossLedger(
            collapsed=[
                NordstromPdpContentLossEntry(
                    category=entry.category,
                    count=entry.count,
                    reason=entry.reason,
                    source_anchor_kind=entry.raw_anchor.anchor_kind,
                    source_anchor_value=entry.raw_anchor.anchor_value,
                )
                for entry in projected.collapsed
            ],
            preserved_evidence_rows=len(projected.rows),
            preserved_bindings=len(projected.bindings),
            hierarchy_preserved=True,
            structure_preserved=_retail_structure_preserved(projected.bindings),
        ),
        residuals=projected.residuals,
    )
    return record.model_dump(mode="json")


def _projection_from_nordstrom_content_record(
    *,
    packet: SourceCapturePacket,
    content_file: PreservedFile,
    content_bytes: bytes,
) -> RetailPdpProjectionPacket:
    try:
        record = NordstromPdpAggregateContentRecord.model_validate_json(content_bytes)
    except Exception as exc:
        raise ValueError(f"invalid Nordstrom PDP content record: {exc}") from exc
    if (
        packet.source_family != "retail_pdp"
        or packet.source_surface != "cloakbrowser_snapshot"
    ):
        raise ValueError(
            "Nordstrom PDP content records require retail_pdp/cloakbrowser_snapshot packets"
        )
    if _detect_retailer(packet) != "nordstrom":
        raise ValueError(
            "Nordstrom PDP content record does not match packet retailer identity"
        )

    slice_by_id = {
        source_slice.slice_id: source_slice for source_slice in packet.source_slices
    }
    matching_source_urls = {
        _fact_value(source_slice.locator)
        for source_slice in packet.source_slices
        if _fact_value(source_slice.locator)
    }
    if record.source_url not in matching_source_urls:
        raise ValueError(
            f"Nordstrom content record source_url {record.source_url!r} does not "
            "match a packet source-slice locator"
        )

    rows: list[RetailPdpProjectionRow] = []
    for index, content_row in enumerate(record.rows):
        source_slice = slice_by_id.get(content_row.slice_id)
        if (
            source_slice is None
            or content_file.file_id not in source_slice.preserved_file_ids
        ):
            raise ValueError(
                "Nordstrom content row references invalid source slice: "
                f"{content_row.slice_id}"
            )
        fields = dict(content_row.source_visible_fields)
        if content_row.row_kind == "retail_pdp_product":
            fields = _product_context_fields(packet, source_slice, "nordstrom")
        rows.append(
            RetailPdpProjectionRow(
                row_id=content_row.row_id,
                row_kind=content_row.row_kind,
                retailer="nordstrom",
                raw_ref=RetailProjectionRawRef(
                    packet_id=packet.packet_id,
                    slice_id=content_row.slice_id,
                ),
                raw_anchor=_nordstrom_content_record_anchor(
                    content_file, f"/rows/{index}"
                ),
                source_visible_fields=fields,
                residuals=content_row.residuals,
            )
        )

    bindings: list[RetailPdpProjectionBinding] = []
    for index, content_binding in enumerate(record.binding_map):
        source_slice = slice_by_id.get(content_binding.slice_id)
        if (
            source_slice is None
            or content_file.file_id not in source_slice.preserved_file_ids
        ):
            raise ValueError(
                "Nordstrom content binding references invalid source slice: "
                f"{content_binding.slice_id}"
            )
        fields = dict(content_binding.source_visible_fields)
        if content_binding.binding_type == "series_locale_currency":
            fields = {
                "series_id": packet.series_id,
                "locale_pin": _fact_value(source_slice.locale_pin),
                "currency_pin": _fact_value(source_slice.currency_pin),
                "variant_pin": _fact_value(source_slice.variant_pin),
            }
        bindings.append(
            RetailPdpProjectionBinding(
                binding_type=content_binding.binding_type,
                row_id=content_binding.row_id,
                raw_ref=RetailProjectionRawRef(
                    packet_id=packet.packet_id,
                    slice_id=content_binding.slice_id,
                ),
                raw_anchor=_nordstrom_content_record_anchor(
                    content_file, f"/binding_map/{index}"
                ),
                source_visible_fields=fields,
            )
        )

    collapsed = [
        RetailPdpProjectionLossEntry(
            category=entry.category,
            count=entry.count,
            reason=entry.reason,
            raw_anchor=_nordstrom_content_record_anchor(
                content_file, f"/loss_ledger/collapsed/{index}"
            ),
        )
        for index, entry in enumerate(record.loss_ledger.collapsed)
    ]
    return RetailPdpProjectionPacket(
        packet_id=packet.packet_id,
        rows=rows,
        binding_map=bindings,
        loss_ledger=RetailPdpProjectionLossLedger(
            collapsed=collapsed,
            preserved_evidence_rows=len(rows),
            preserved_bindings=len(bindings),
            hierarchy_preserved=record.loss_ledger.hierarchy_preserved,
            structure_preserved=record.loss_ledger.structure_preserved,
        ),
        residuals=record.residuals,
    )


def _nordstrom_content_row(
    row: RetailPdpProjectionRow,
) -> NordstromPdpContentRow:
    fields = dict(row.source_visible_fields)
    if row.row_kind == "retail_pdp_product":
        fields = {}
    return NordstromPdpContentRow(
        slice_id=row.raw_ref.slice_id,
        row_id=row.row_id,
        row_kind=row.row_kind,
        retailer="nordstrom",
        source_visible_fields=fields,
        residuals=row.residuals,
        source_anchor_kind=row.raw_anchor.anchor_kind,
        source_anchor_value=row.raw_anchor.anchor_value,
    )


def _nordstrom_content_binding(
    binding: RetailPdpProjectionBinding,
) -> NordstromPdpContentBinding:
    fields = dict(binding.source_visible_fields)
    if binding.binding_type == "series_locale_currency":
        fields = {}
    return NordstromPdpContentBinding(
        slice_id=binding.raw_ref.slice_id,
        binding_type=binding.binding_type,
        row_id=binding.row_id,
        source_visible_fields=fields,
    )


def _nordstrom_content_record_anchor(
    content_file: PreservedFile,
    json_pointer: str,
) -> RetailProjectionRawAnchor:
    return RetailProjectionRawAnchor(
        file_id=content_file.file_id,
        relative_packet_path=content_file.relative_packet_path,
        sha256=content_file.sha256,
        hash_basis=content_file.hash_basis,
        anchor_kind="json_pointer",
        anchor_value=json_pointer,
    )


def _validate_nordstrom_content_packet_metadata(
    *,
    packet: SourceCapturePacket,
    raw_file_bytes_by_file_id: Mapping[str, bytes],
) -> None:
    def _one_json(filename: str) -> dict[str, Any]:
        matches = [
            item
            for item in packet.preserved_files
            if item.relative_packet_path.replace("\\", "/").endswith(filename)
        ]
        if len(matches) != 1:
            raise ValueError(
                f"Nordstrom content packet must preserve exactly one {filename}"
            )
        body = raw_file_bytes_by_file_id.get(matches[0].file_id)
        if body is None:
            raise ValueError(
                f"preserved bytes are required for {matches[0].file_id}: {filename}"
            )
        try:
            value = json.loads(body)
        except Exception as exc:
            raise ValueError(f"invalid {filename}: {exc}") from exc
        if not isinstance(value, dict):
            raise ValueError(f"{filename} must contain a JSON object")
        return value

    capture_metadata = _one_json("content_capture_metadata.json")
    if capture_metadata.get("parser_version") != NORDSTROM_PDP_PARSER_VERSION:
        raise ValueError("Nordstrom content packet parser version does not match current")
    if capture_metadata.get("projection_status") != "succeeded":
        raise ValueError("Nordstrom content packet projection did not succeed")
    if capture_metadata.get("capture_artifact_mode") not in {"content", "sample"}:
        raise ValueError("Nordstrom content packet must use content or sample mode")

    browser_metadata = _one_json("cloakbrowser_snapshot_metadata.json")
    profile = browser_metadata.get("retail_capture_profile")
    if (
        not isinstance(profile, dict)
        or profile.get("name") != NORDSTROM_PDP_CONTENT_PROFILE
    ):
        raise ValueError("Nordstrom content packet capture profile does not match")
    if browser_metadata.get("pin_confirmed") is not True:
        raise ValueError(
            "Nordstrom content packet does not carry a confirmed US/USD storefront pin"
        )


def _content_record_kind(content_bytes: bytes) -> object:
    try:
        payload = json.loads(content_bytes)
    except Exception as exc:
        raise ValueError(f"invalid Retail PDP content record JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError("Retail PDP content record must contain a JSON object")
    return payload.get("record_kind")


class _ProjectedRetailHtml(StrictModel):
    rows: list[RetailPdpProjectionRow] = Field(default_factory=list)
    bindings: list[RetailPdpProjectionBinding] = Field(default_factory=list)
    collapsed: list[RetailPdpProjectionLossEntry] = Field(default_factory=list)
    residuals: list[str] = Field(default_factory=list)


class _StructuredJsonEntry(StrictModel):
    kind: Literal["ld_json", "apollo_state", "next_data"]
    index: int
    raw_text: str
    parsed: object | None
    raw_anchor: RetailProjectionRawAnchor


def _project_retail_html(
    html: str,
    *,
    visible_text_files: Sequence[tuple[PreservedFile, str]],
    visible_text: str,
    packet: SourceCapturePacket,
    source_slice: SourceCaptureSlice,
    raw_ref: RetailProjectionRawRef,
    raw_anchor: RetailProjectionRawAnchor,
    retailer: Retailer,
) -> _ProjectedRetailHtml:
    rows: list[RetailPdpProjectionRow] = []
    bindings: list[RetailPdpProjectionBinding] = []
    residuals: list[str] = []
    collapsed: list[RetailPdpProjectionLossEntry] = []

    structured_entries = _extract_structured_json_entries(html, raw_anchor=raw_anchor)
    source_url = _fact_value(source_slice.locator) or _fact_value(packet.source_locator)
    if retailer == "luckyscent":
        structured_entries = _luckyscent_target_structured_entries(
            structured_entries,
            source_url=source_url,
        )
    if retailer == "nordstrom":
        structured_entries = _nordstrom_target_structured_entries(
            structured_entries,
            source_url=_fact_value(source_slice.locator)
            or _fact_value(packet.source_locator),
        )
    product_row_id = f"{source_slice.slice_id}:{retailer}:pdp"
    product_fields = _product_context_fields(packet, source_slice, retailer)
    rows.append(
        RetailPdpProjectionRow(
            row_id=product_row_id,
            row_kind="retail_pdp_product",
            retailer=retailer,
            raw_ref=raw_ref,
            raw_anchor=raw_anchor,
            source_visible_fields=product_fields,
        )
    )

    for entry in structured_entries:
        row_id = f"{source_slice.slice_id}:{retailer}:structured:{entry.kind}:{entry.index}"
        rows.append(
            RetailPdpProjectionRow(
                row_id=row_id,
                row_kind="retail_embedded_structured_json",
                retailer=retailer,
                raw_ref=raw_ref,
                raw_anchor=entry.raw_anchor,
                source_visible_fields={
                    "structured_json_kind": entry.kind,
                    "script_index": entry.index,
                    "raw_json_text": entry.raw_text,
                    "parse_status": "parsed" if entry.parsed is not None else "malformed_json",
                    "parsed_type": _json_type(entry.parsed),
                },
                residuals=[] if entry.parsed is not None else [f"{entry.kind}_{entry.index}_malformed_json"],
            )
        )
        bindings.append(
            RetailPdpProjectionBinding(
                binding_type="structured_json_for_product",
                row_id=row_id,
                raw_ref=raw_ref,
                raw_anchor=entry.raw_anchor,
                source_visible_fields={"product_row_id": product_row_id, "structured_json_kind": entry.kind},
            )
        )

    variant_fields, variant_anchor, variant_residuals = _variant_offer_fields(
        retailer=retailer,
        html=html,
        visible_text=visible_text,
        packet=packet,
        source_slice=source_slice,
        structured_entries=structured_entries,
        fallback_anchor=raw_anchor,
    )
    residuals.extend(variant_residuals)
    if variant_fields:
        sku = _string_or_none(variant_fields.get("sku")) or _string_or_none(variant_fields.get("product_id")) or "unknown"
        variant_row_id = f"{source_slice.slice_id}:{retailer}:variant:{_row_token(sku)}"
        rows.append(
            RetailPdpProjectionRow(
                row_id=variant_row_id,
                row_kind="retail_variant_offer",
                retailer=retailer,
                raw_ref=raw_ref,
                raw_anchor=variant_anchor,
                source_visible_fields=variant_fields,
                residuals=variant_residuals,
            )
        )
        bindings.extend(
            [
                RetailPdpProjectionBinding(
                    binding_type="sku_variant_price",
                    row_id=variant_row_id,
                    raw_ref=raw_ref,
                    raw_anchor=variant_anchor,
                    source_visible_fields={
                        "sku": variant_fields.get("sku"),
                        "variant_name": variant_fields.get("variant_name"),
                        "price": variant_fields.get("price"),
                        "price_currency": variant_fields.get("price_currency"),
                    },
                ),
                RetailPdpProjectionBinding(
                    binding_type="variant_availability",
                    row_id=variant_row_id,
                    raw_ref=raw_ref,
                    raw_anchor=variant_anchor,
                    source_visible_fields={
                        "sku": variant_fields.get("sku"),
                        "variant_name": variant_fields.get("variant_name"),
                        "availability": variant_fields.get("availability"),
                        "shipping_availability": variant_fields.get("shipping_availability"),
                        "pickup_availability": variant_fields.get("pickup_availability"),
                        "delivery_availability": variant_fields.get("delivery_availability"),
                        "seller": variant_fields.get("seller"),
                    },
                ),
                RetailPdpProjectionBinding(
                    binding_type="series_locale_currency",
                    row_id=variant_row_id,
                    raw_ref=raw_ref,
                    raw_anchor=raw_anchor,
                    source_visible_fields={
                        "series_id": packet.series_id,
                        "locale_pin": _fact_value(source_slice.locale_pin),
                        "currency_pin": _fact_value(source_slice.currency_pin),
                        "variant_pin": _fact_value(source_slice.variant_pin),
                    },
                ),
            ]
        )
    else:
        residuals.append(f"{source_slice.slice_id}:{retailer}:variant_offer_absent")

    review_fields, review_anchor, review_residuals = _review_substrate_fields(
        retailer=retailer,
        html=html,
        visible_text=visible_text,
        structured_entries=structured_entries,
        fallback_anchor=raw_anchor,
        source_url=source_url,
    )
    residuals.extend(review_residuals)
    if review_fields:
        review_row_id = f"{source_slice.slice_id}:{retailer}:review_substrate"
        rows.append(
            RetailPdpProjectionRow(
                row_id=review_row_id,
                row_kind="retail_review_substrate",
                retailer=retailer,
                raw_ref=raw_ref,
                raw_anchor=review_anchor,
                source_visible_fields=review_fields,
                residuals=review_residuals,
            )
        )
        bindings.append(
            RetailPdpProjectionBinding(
                binding_type="review_substrate_for_product",
                row_id=review_row_id,
                raw_ref=raw_ref,
                raw_anchor=review_anchor,
                source_visible_fields={
                    "product_row_id": product_row_id,
                    "review_substrate_source": review_fields.get("review_substrate_source"),
                    "review_count": review_fields.get("review_count"),
                    "rating_count": review_fields.get("rating_count"),
                    "written_review_count": review_fields.get("written_review_count"),
                    "filtered_review_count": review_fields.get("filtered_review_count"),
                    "rating": review_fields.get("rating"),
                    "rating_distribution_basis": review_fields.get("rating_distribution_basis"),
                    "rating_distribution_buckets": review_fields.get("rating_distribution_buckets"),
                    "displayed_review_count": review_fields.get("displayed_review_count"),
                    "displayed_review_body_count": review_fields.get(
                        "displayed_review_body_count"
                    ),
                    "review_body_coverage": review_fields.get("review_body_coverage"),
                },
            )
        )
    else:
        residuals.append(f"{source_slice.slice_id}:{retailer}:review_substrate_absent")

    for module in _carried_module_fields(
        retailer=retailer,
        html=html,
        visible_text_files=visible_text_files,
        raw_anchor=raw_anchor,
    ):
        module_row_id = f"{source_slice.slice_id}:{retailer}:module:{module['module_type']}"
        rows.append(
            RetailPdpProjectionRow(
                row_id=module_row_id,
                row_kind="retail_carried_module",
                retailer=retailer,
                raw_ref=raw_ref,
                raw_anchor=module["raw_anchor"],
                source_visible_fields={key: value for key, value in module.items() if key != "raw_anchor"},
            )
        )
        bindings.append(
            RetailPdpProjectionBinding(
                binding_type="module_carried",
                row_id=module_row_id,
                raw_ref=raw_ref,
                raw_anchor=module["raw_anchor"],
                source_visible_fields={"module_type": module["module_type"]},
            )
        )

    collapsed.extend(_collapse_entries(html=html, visible_text=visible_text, raw_anchor=raw_anchor))
    return _ProjectedRetailHtml(rows=rows, bindings=bindings, collapsed=collapsed, residuals=residuals)


def _extract_structured_json_entries(html: str, *, raw_anchor: RetailProjectionRawAnchor) -> list[_StructuredJsonEntry]:
    entries: list[_StructuredJsonEntry] = []
    for index, raw_text in enumerate(_extract_ld_json_texts(html)):
        stripped = raw_text.strip()
        entries.append(
            _StructuredJsonEntry(
                kind="ld_json",
                index=index,
                raw_text=stripped,
                parsed=_safe_json_loads(stripped),
                raw_anchor=_with_anchor(raw_anchor, "script_index", f"ld_json[{index}]"),
            )
        )

    apollo_text = _extract_apollo_state_text(html)
    if apollo_text is not None:
        entries.append(
            _StructuredJsonEntry(
                kind="apollo_state",
                index=0,
                raw_text=apollo_text,
                parsed=_safe_json_loads(apollo_text),
                raw_anchor=_with_anchor(raw_anchor, "script_index", "window.__APOLLO_STATE__"),
            )
        )
    next_data_text = _extract_next_data_text(html)
    if next_data_text is not None:
        entries.append(
            _StructuredJsonEntry(
                kind="next_data",
                index=0,
                raw_text=next_data_text,
                parsed=_safe_json_loads(next_data_text),
                raw_anchor=_with_anchor(raw_anchor, "script_index", "__NEXT_DATA__"),
            )
        )
    return entries


def _variant_offer_fields(
    *,
    retailer: Retailer,
    html: str,
    visible_text: str,
    packet: SourceCapturePacket,
    source_slice: SourceCaptureSlice,
    structured_entries: list[_StructuredJsonEntry],
    fallback_anchor: RetailProjectionRawAnchor,
) -> tuple[dict[str, Any | None], RetailProjectionRawAnchor, list[str]]:
    residuals: list[str] = []
    if retailer == "amazon":
        fields = _amazon_variant_offer_fields(html=html, visible_text=visible_text, packet=packet, source_slice=source_slice)
        amazon_residuals = (
            ["amazon_price_from_unanchored_visible_text_fallback"]
            if fields.get("price_isolation") == "unanchored_visible_text_fallback"
            else []
        )
        return fields, _with_anchor(fallback_anchor, "html_selector", "#ASIN/#corePrice_feature_div/#availability"), amazon_residuals

    if retailer == "walmart":
        fields = _walmart_variant_offer_fields(
            html=html, visible_text=visible_text, packet=packet, source_slice=source_slice, structured_entries=structured_entries
        )
        residuals.extend(_retail_commerce_absence_residuals(retailer, fields))
        return fields, _with_anchor(fallback_anchor, "html_selector", "#__NEXT_DATA__"), residuals

    if retailer == "target":
        fields = _target_variant_offer_fields(
            html=html, visible_text=visible_text, packet=packet, source_slice=source_slice
        )
        residuals.extend(_retail_commerce_absence_residuals(retailer, fields))
        return fields, _with_anchor(fallback_anchor, "html_selector", "#ratingReviewId"), residuals

    if retailer == "luckyscent":
        fields, anchor, luckyscent_residuals = _luckyscent_variant_offer_fields(
            visible_text=visible_text,
            packet=packet,
            source_slice=source_slice,
            structured_entries=structured_entries,
        )
        residuals.extend(luckyscent_residuals)
        return fields, anchor or fallback_anchor, residuals

    if retailer == "nordstrom":
        fields, nordstrom_residuals = _nordstrom_variant_offer_fields(
            visible_text=visible_text,
            packet=packet,
            source_slice=source_slice,
            structured_entries=structured_entries,
        )
        return (
            fields,
            _with_anchor(
                fallback_anchor,
                "html_selector",
                "main product / target Product JSON-LD",
            ),
            nordstrom_residuals,
        )

    sephora_dom_fields = _sephora_dom_offer_fields(html) if retailer == "sephora" else {}
    selected_sku = _string_or_none(sephora_dom_fields.get("dom_sku"))
    structured_fields, structured_anchor = _structured_variant_offer_fields(
        structured_entries,
        preferred_sku=selected_sku,
    )
    apollo_fields, apollo_anchor = _ulta_apollo_offer_fields(structured_entries) if retailer == "ulta" else ({}, None)
    if retailer == "ulta" and not apollo_fields and _ulta_apollo_offer_substrate_present(structured_entries):
        residuals.append(f"{source_slice.slice_id}:ulta:variant_offer_substrate_present_but_unextracted")
    if retailer == "sephora" and selected_sku and not structured_fields:
        substrate_skus = _sephora_structured_offer_substrate_skus(structured_entries)
        if substrate_skus and selected_sku not in substrate_skus:
            residuals.append("sephora_selected_sku_absent_from_structured_variants")
    if sephora_dom_fields:
        structured_fields = {
            **structured_fields,
            "product_id": _string_or_none(sephora_dom_fields.get("dom_product_id"))
            or structured_fields.get("product_id"),
            "sku": selected_sku or structured_fields.get("sku"),
            **sephora_dom_fields,
            "selected_sku": selected_sku,
            "selection_binding_source": "sephora_dom_product_page",
        }
    if retailer == "sephora" and structured_fields:
        structured_fields = {
            **structured_fields,
            "exact_stock_quantity": "not_observed",
            "sold_units": "not_observed",
        }
        if selected_sku and not _string_or_none(structured_fields.get("availability")):
            residuals.append("sephora_selected_variant_availability_absent")
    residuals.extend(_structured_price_residuals(retailer=retailer, structured_fields=structured_fields))
    if retailer == "ulta" and structured_fields and apollo_fields:
        for key in ("sku", "product_id", "price", "availability"):
            left = _string_or_none(structured_fields.get(key))
            right = _string_or_none(apollo_fields.get(key))
            if left and right and not _equivalent_offer_value(key, left, right):
                residuals.append(f"ulta_ld_json_apollo_{key}_mismatch")
        apollo_prefixed = {
            key if key.startswith("apollo_") else f"apollo_{key}": value for key, value in apollo_fields.items()
        }
        merged = {**structured_fields, **apollo_prefixed}
        _residualize_ulta_requested_sku_mismatch(merged, residuals, source_slice=source_slice)
        return merged, structured_anchor or apollo_anchor or fallback_anchor, residuals
    if structured_fields:
        if retailer == "ulta":
            _residualize_ulta_requested_sku_mismatch(structured_fields, residuals, source_slice=source_slice)
        return structured_fields, structured_anchor or fallback_anchor, residuals
    if apollo_fields:
        _residualize_ulta_requested_sku_mismatch(apollo_fields, residuals, source_slice=source_slice)
        return apollo_fields, apollo_anchor or fallback_anchor, residuals
    return {}, fallback_anchor, residuals


def _luckyscent_target_structured_entries(
    entries: Sequence[_StructuredJsonEntry],
    *,
    source_url: str | None,
) -> list[_StructuredJsonEntry]:
    if not source_url:
        return []
    return [
        entry
        for entry in entries
        if any(
            _luckyscent_product_matches_source(item, source_url)
            for item in _walk_dicts(entry.parsed)
        )
    ]


def _luckyscent_product_matches_source(
    item: Mapping[str, object],
    source_url: str,
) -> bool:
    item_type = item.get("@type")
    if item_type not in {"Product", "ProductGroup"}:
        return False
    for candidate in (item.get("url"), item.get("@id")):
        value = _string_or_none(candidate)
        if value and _normalized_url_identity(value) == _normalized_url_identity(
            source_url
        ):
            return True
    return False


def _luckyscent_target_product_group(
    structured_entries: Sequence[_StructuredJsonEntry],
    *,
    source_url: str | None,
) -> tuple[dict[str, object], RetailProjectionRawAnchor] | None:
    if not source_url:
        return None
    for entry in structured_entries:
        for item in _walk_dicts(entry.parsed):
            if (
                item.get("@type") == "ProductGroup"
                and _luckyscent_product_matches_source(item, source_url)
            ):
                return item, entry.raw_anchor
    return None


def _luckyscent_variant_offer_fields(
    *,
    visible_text: str,
    packet: SourceCapturePacket,
    source_slice: SourceCaptureSlice,
    structured_entries: Sequence[_StructuredJsonEntry],
) -> tuple[
    dict[str, Any | None],
    RetailProjectionRawAnchor | None,
    list[str],
]:
    source_url = _fact_value(source_slice.locator) or _fact_value(
        packet.source_locator
    )
    target = _luckyscent_target_product_group(
        structured_entries,
        source_url=source_url,
    )
    if target is None:
        return {}, None, ["luckyscent_target_product_group_absent"]
    product, anchor = target
    raw_variants = product.get("hasVariant")
    if not isinstance(raw_variants, list):
        return {}, anchor, ["luckyscent_target_variants_absent"]

    variants: list[dict[str, Any | None]] = []
    residuals: list[str] = []
    for index, candidate in enumerate(raw_variants):
        if not isinstance(candidate, dict):
            residuals.append(f"luckyscent_variant_{index}_malformed")
            continue
        offer = candidate.get("offers")
        if not isinstance(offer, dict):
            residuals.append(f"luckyscent_variant_{index}_offer_absent")
            offer = {}
        seller_value = offer.get("seller")
        seller = (
            _string_or_none(seller_value.get("name"))
            if isinstance(seller_value, dict)
            else _string_or_none(seller_value)
        )
        variants.append(
            {
                "sku": _string_or_none(candidate.get("sku")),
                "name": _string_or_none(candidate.get("name")),
                "size": _string_or_none(candidate.get("size")),
                "url": _string_or_none(candidate.get("url")),
                "price": _string_or_none(offer.get("price")),
                "price_currency": _string_or_none(offer.get("priceCurrency")),
                "availability": _string_or_none(offer.get("availability")),
                "seller": seller,
            }
        )
    if not variants:
        return {}, anchor, [*residuals, "luckyscent_target_variants_absent"]

    brand_value = product.get("brand")
    brand = (
        _string_or_none(brand_value.get("name"))
        if isinstance(brand_value, dict)
        else _string_or_none(brand_value)
    )
    first_variant = variants[0]
    sellers = {
        value
        for value in (_string_or_none(item.get("seller")) for item in variants)
        if value
    }
    currencies = {
        value
        for value in (
            _string_or_none(item.get("price_currency")) for item in variants
        )
        if value
    }
    if len(sellers) > 1:
        residuals.append("luckyscent_variant_seller_mismatch")
    if len(currencies) > 1:
        residuals.append("luckyscent_variant_currency_mismatch")
    fields: dict[str, Any | None] = {
        "product_id": _string_or_none(product.get("productGroupID")),
        "sku": first_variant.get("sku"),
        "product_name": _string_or_none(product.get("name")),
        "brand": brand,
        "description": _string_or_none(product.get("description")),
        "source_product_url": _string_or_none(product.get("url")),
        "variant_name": first_variant.get("size") or first_variant.get("name"),
        "price": first_variant.get("price"),
        "price_currency": first_variant.get("price_currency"),
        "availability": first_variant.get("availability"),
        "seller": first_variant.get("seller"),
        "variants": variants,
        "variant_count": len(variants),
        "displayed_price": _luckyscent_displayed_price(
            visible_text,
            product_name=_string_or_none(product.get("name")),
            brand=brand,
        ),
        "gender": _line_after_heading(visible_text, "Gender"),
        "concentration": _line_after_heading(visible_text, "Concentration"),
        "main_note": _line_after_heading(visible_text, "Main Note"),
        "country": _line_after_heading(visible_text, "Country"),
        "released": _line_after_heading(visible_text, "Released"),
        "fragrance_notes": _line_after_heading(visible_text, "Fragrance Notes"),
        "fragrance_style": _line_after_heading(visible_text, "Fragrance Style"),
        "scoop": _text_section(
            visible_text,
            start_heading="The Scoop",
            end_heading="You May Also Like",
        ),
        "delivery_location": None,
        "delivery_location_posture": "not_observed",
        "variant_binding_source": "luckyscent_target_product_group_and_visible_text",
    }
    return fields, anchor, residuals


def _luckyscent_displayed_price(
    visible_text: str,
    *,
    product_name: str | None,
    brand: str | None,
) -> str | None:
    if not product_name or not brand:
        return None
    return _first_regex(
        visible_text,
        (
            rf"{re.escape(product_name)}\s+{re.escape(brand)}\s+"
            rf"\d(?:\.\d+)?\s+\([\d,]+\)\s+\$([\d,.]+)",
        ),
    )


def _review_substrate_fields(
    *,
    retailer: Retailer,
    html: str,
    visible_text: str,
    structured_entries: list[_StructuredJsonEntry],
    fallback_anchor: RetailProjectionRawAnchor,
    source_url: str | None = None,
) -> tuple[dict[str, Any | None], RetailProjectionRawAnchor, list[str]]:
    if retailer == "amazon":
        return _amazon_review_fields(html=html, visible_text=visible_text), _with_anchor(
            fallback_anchor, "html_selector", "#averageCustomerReviews/#acrCustomerReviewText"
        ), []
    if retailer == "sephora":
        fields = _sephora_review_fields(html=html, visible_text=visible_text, structured_entries=structured_entries)
        residuals = []
        if fields.get("review_count_isolation") == "unanchored_fallback":
            residuals.append("sephora_review_count_from_unanchored_fallback")
        if not fields.get("target_widget_review_count"):
            residuals.append("sephora_target_widget_exact_review_count_absent")
        if not fields.get("rating_distribution_histogram"):
            residuals.append("sephora_target_widget_rating_distribution_absent")
        structured_count = _string_or_none(fields.get("structured_review_count"))
        target_dom_count = _string_or_none(fields.get("target_widget_review_count")) or _string_or_none(
            fields.get("displayed_review_count_text")
        )
        if (
            structured_count
            and target_dom_count
            and not _equivalent_review_count(structured_count, target_dom_count)
        ):
            residuals.append("sephora_ld_json_review_count_differs_from_target_dom")
        section_anchor = _sephora_review_section_anchor(html)
        anchor = (
            _with_anchor(fallback_anchor, "html_selector", section_anchor)
            if section_anchor
            else _with_anchor(fallback_anchor, "text_pattern", "Ratings & Reviews")
        )
        return fields, anchor, residuals
    if retailer == "ulta":
        fields, residuals = _ulta_review_fields(structured_entries)
        return fields, _with_anchor(fallback_anchor, "script_index", "ld_json/apollo_state review modules"), residuals
    if retailer == "walmart":
        return _walmart_review_fields(visible_text), _with_anchor(fallback_anchor, "html_selector", "#__NEXT_DATA__"), []
    if retailer == "target":
        fields = _target_review_fields(visible_text)
        residuals = [] if fields.get("written_review_count") is not None else ["target_written_review_count_not_observed"]
        return fields, _with_anchor(fallback_anchor, "html_selector", "#ratingReviewId"), residuals
    if retailer == "luckyscent":
        fields, residuals = _luckyscent_review_fields(
            html=html,
            visible_text=visible_text,
            structured_entries=structured_entries,
            source_url=source_url,
        )
        return (
            fields,
            _with_anchor(
                fallback_anchor,
                "html_selector",
                ".jdgm-review-widget .jdgm-rev[data-product-url]",
            ),
            residuals,
        )
    if retailer == "nordstrom":
        fields, residuals = _nordstrom_review_fields(
            html=html,
            visible_text=visible_text,
            structured_entries=structured_entries,
        )
        return (
            fields,
            _with_anchor(fallback_anchor, "html_selector", "#product-page-reviews"),
            residuals,
        )
    yotpo_fields, yotpo_residuals = _yotpo_review_fields(html)
    if yotpo_fields:
        return (
            yotpo_fields,
            _with_anchor(
                fallback_anchor,
                "html_selector",
                "#yotpo-reviews-section-data",
            ),
            yotpo_residuals,
        )
    return {}, fallback_anchor, []


def _luckyscent_review_fields(
    *,
    html: str,
    visible_text: str,
    structured_entries: Sequence[_StructuredJsonEntry],
    source_url: str | None,
) -> tuple[dict[str, Any | None], list[str]]:
    target = _luckyscent_target_product_group(
        structured_entries,
        source_url=source_url,
    )
    if target is None:
        return {}, ["luckyscent_target_product_group_absent"]
    product, _anchor = target
    product_name = _string_or_none(product.get("name"))
    brand_value = product.get("brand")
    brand = (
        _string_or_none(brand_value.get("name"))
        if isinstance(brand_value, dict)
        else _string_or_none(brand_value)
    )
    aggregate = product.get("aggregateRating")
    aggregate = aggregate if isinstance(aggregate, dict) else {}
    structured_rating = _string_or_none(aggregate.get("ratingValue"))
    structured_count = _string_or_none(aggregate.get("reviewCount"))
    displayed_rating, displayed_count = _luckyscent_displayed_rating_and_count(
        visible_text,
        product_name=product_name,
        brand=brand,
    )
    reviews = _luckyscent_target_reviews(
        html,
        product_name=product_name,
        source_url=source_url,
    )
    histogram = _luckyscent_review_histogram(html)
    residuals: list[str] = []
    if displayed_rating and structured_rating and displayed_rating != structured_rating:
        residuals.append("luckyscent_displayed_structured_rating_mismatch")
    if (
        displayed_count
        and structured_count
        and not _equivalent_review_count(displayed_count, structured_count)
    ):
        residuals.append("luckyscent_displayed_structured_review_count_mismatch")
    if structured_count and len(reviews) != int(structured_count.replace(",", "")):
        residuals.append("luckyscent_rendered_structured_review_count_mismatch")
    if not reviews:
        residuals.append("luckyscent_rendered_reviews_absent")
    return {
        "review_substrate_source": "luckyscent_target_judgeme_widget_and_ld_json",
        "product_name": product_name,
        "source_product_url": _string_or_none(product.get("url")),
        "rating": displayed_rating or structured_rating,
        "displayed_rating": displayed_rating,
        "structured_rating": structured_rating,
        "review_count": structured_count or displayed_count,
        "displayed_review_count": displayed_count,
        "structured_review_count": structured_count,
        "written_review_count": str(len(reviews)),
        "rating_count": structured_count or displayed_count,
        "rating_distribution_basis": "count_and_percent" if histogram else None,
        "rating_distribution_buckets": histogram,
        "reviews": reviews,
    }, residuals


def _luckyscent_displayed_rating_and_count(
    visible_text: str,
    *,
    product_name: str | None,
    brand: str | None,
) -> tuple[str | None, str | None]:
    if not product_name or not brand:
        return None, None
    match = re.search(
        rf"{re.escape(product_name)}\s+{re.escape(brand)}\s+"
        rf"(\d(?:\.\d+)?)\s+\(([\d,]+)\)\s+\$[\d,.]+",
        visible_text,
        flags=re.IGNORECASE,
    )
    return (match.group(1), match.group(2)) if match else (None, None)


def _luckyscent_target_reviews(
    html: str,
    *,
    product_name: str | None,
    source_url: str | None,
) -> list[dict[str, Any | None]]:
    if not product_name or not source_url:
        return []
    target_path = urlparse(source_url).path.rstrip("/")
    blocks = re.findall(
        r'(?is)(<div class="jdgm-rev jdgm-divider-top[^"]*"'
        r".*?)(?=<div class=\"jdgm-rev jdgm-divider-top|"
        r"<div class=\"jdgm-paginate|</body>)",
        html,
    )
    reviews: list[dict[str, Any | None]] = []
    for block in blocks:
        start_tag = block[: block.find(">") + 1]
        if _html_attr_value(start_tag, "data-product-title") != product_name:
            continue
        product_path = (_html_attr_value(start_tag, "data-product-url") or "").rstrip(
            "/"
        )
        if product_path != target_path:
            continue
        body_html = _first_regex(
            block,
            (r'<div class="jdgm-rev__body">\s*<p>(.*?)</p>',),
        )
        variant = _first_regex(
            block,
            (
                r'<div class="jdgm-rev__prod-variant-wrapper">.*?'
                r"<span[^>]*>([^<]+)</span>\s*</div>",
            ),
        )
        collection_type = _first_regex(
            block,
            (r'data-badge-type="([^"]+)"',),
        )
        collection_text = _first_regex(
            block,
            (
                r'<div class="jdgm-rev__transparency-badge"[^>]*>(.*?)</div>',
            ),
        )
        reviews.append(
            {
                "review_id": _html_attr_value(start_tag, "data-review-id"),
                "product_name": product_name,
                "product_url": product_path,
                "verified_buyer": (
                    _html_attr_value(start_tag, "data-verified-buyer") == "true"
                ),
                "rating": _first_regex(block, (r'data-score="([^"]+)"',)),
                "timestamp": _first_regex(
                    block,
                    (r'jdgm-rev__timestamp"[^>]*data-content="([^"]+)"',),
                ),
                "displayed_date": _first_regex(
                    block,
                    (r'jdgm-rev__timestamp"[^>]*>([^<]+)</span>',),
                ),
                "author": _html_text(
                    _first_regex(
                        block,
                        (r'jdgm-rev__author">([^<]+)</span>',),
                    )
                ),
                "location": _html_text(
                    _first_regex(
                        block,
                        (r'jdgm-rev__location">([^<]+)</span>',),
                    )
                ),
                "body": _html_text(body_html),
                "variant": _html_text(variant),
                "collection_type": collection_type,
                "collection_text": _html_text(collection_text),
            }
        )
    return reviews


def _luckyscent_review_histogram(html: str) -> list[dict[str, int]]:
    buckets: list[dict[str, int]] = []
    for rating, frequency, percentage in re.findall(
        r'class="jdgm-histogram__row"[^>]*data-rating="(\d)"'
        r'[^>]*data-frequency="(\d+)"[^>]*data-percentage="(\d+)"',
        html,
        flags=re.IGNORECASE,
    ):
        buckets.append(
            {
                "stars": int(rating),
                "value": int(frequency),
                "source_percent": int(percentage),
            }
        )
    return buckets


def _validate_luckyscent_projected_content(
    projected: _ProjectedRetailHtml,
    *,
    source_url: str,
) -> None:
    variant_rows = [
        row for row in projected.rows if row.row_kind == "retail_variant_offer"
    ]
    review_rows = [
        row for row in projected.rows if row.row_kind == "retail_review_substrate"
    ]
    structured_rows = [
        row
        for row in projected.rows
        if row.row_kind == "retail_embedded_structured_json"
    ]
    if len(variant_rows) != 1:
        raise ValueError(
            "Luckyscent content projection requires exactly one aggregate offer row"
        )
    if len(review_rows) != 1:
        raise ValueError(
            "Luckyscent content projection requires exactly one review-substrate row"
        )
    if len(structured_rows) != 2:
        raise ValueError(
            "Luckyscent content projection requires the two target structured-JSON rows"
        )

    variant_fields = variant_rows[0].source_visible_fields
    variants = variant_fields.get("variants")
    if not isinstance(variants, list) or not variants:
        raise ValueError("Luckyscent content projection has no target variants")
    required_variant_fields = {
        "sku",
        "name",
        "size",
        "url",
        "price",
        "price_currency",
        "availability",
        "seller",
    }
    incomplete = [
        index
        for index, variant in enumerate(variants)
        if not isinstance(variant, dict)
        or any(not _string_or_none(variant.get(key)) for key in required_variant_fields)
    ]
    if incomplete:
        raise ValueError(
            f"Luckyscent content projection has incomplete target variant(s): {incomplete}"
        )
    if _normalized_url_identity(
        _string_or_none(variant_fields.get("source_product_url")) or ""
    ) != _normalized_url_identity(source_url):
        raise ValueError("Luckyscent content projection bound a different product URL")

    review_fields = review_rows[0].source_visible_fields
    reviews = review_fields.get("reviews")
    review_count = _string_or_none(review_fields.get("review_count"))
    if not isinstance(reviews, list) or not reviews or review_count is None:
        raise ValueError("Luckyscent content projection has no complete review substrate")
    if len(reviews) != int(review_count.replace(",", "")):
        raise ValueError(
            "Luckyscent rendered review rows do not match the target structured review count"
        )
    target_path = urlparse(source_url).path.rstrip("/")
    if any(
        not isinstance(review, dict)
        or review.get("product_url") != target_path
        or not _string_or_none(review.get("review_id"))
        or not _string_or_none(review.get("body"))
        for review in reviews
    ):
        raise ValueError(
            "Luckyscent content projection contains an incomplete or off-target review"
        )
def _nordstrom_product_id_from_url(url: str | None) -> str | None:
    if not url:
        return None
    match = re.search(r"/s/[^/?]+/(\d+)(?:[/?]|$)", urlparse(url).path)
    return match.group(1) if match else None


def _nordstrom_target_structured_entries(
    entries: list[_StructuredJsonEntry],
    *,
    source_url: str | None,
) -> list[_StructuredJsonEntry]:
    """Keep only Product JSON-LD bound to the requested Nordstrom PDP.

    Nordstrom currently repeats the target Product JSON-LD and also emits
    breadcrumbs. An entry carrying the requested product URL establishes the
    target name/brand pair; only matching Product entries survive. Recommendation
    products and unrelated structured state cannot establish that pair.
    """
    product_id = _nordstrom_product_id_from_url(source_url)
    if product_id is None:
        return []
    target: tuple[str, str] | None = None
    for entry in entries:
        parsed = entry.parsed
        if not isinstance(parsed, dict) or parsed.get("@type") != "Product":
            continue
        offers = parsed.get("offers")
        if not isinstance(offers, dict):
            continue
        offer_url = _string_or_none(offers.get("url"))
        if _nordstrom_product_id_from_url(offer_url) != product_id:
            continue
        brand = parsed.get("brand")
        brand_name = (
            _string_or_none(brand.get("name")) if isinstance(brand, dict) else None
        )
        name = _string_or_none(parsed.get("name"))
        if name and brand_name:
            target = (name, brand_name)
            break
    if target is None:
        return []
    selected: list[_StructuredJsonEntry] = []
    for entry in entries:
        parsed = entry.parsed
        if not isinstance(parsed, dict) or parsed.get("@type") != "Product":
            continue
        brand = parsed.get("brand")
        brand_name = (
            _string_or_none(brand.get("name")) if isinstance(brand, dict) else None
        )
        if (_string_or_none(parsed.get("name")), brand_name) == target:
            selected.append(entry)
    return selected


def _nordstrom_target_product(
    entries: list[_StructuredJsonEntry],
) -> tuple[dict[str, object], RetailProjectionRawAnchor] | None:
    for entry in entries:
        if isinstance(entry.parsed, dict) and entry.parsed.get("@type") == "Product":
            return entry.parsed, entry.raw_anchor
    return None


def _nordstrom_variant_offer_fields(
    *,
    visible_text: str,
    packet: SourceCapturePacket,
    source_slice: SourceCaptureSlice,
    structured_entries: list[_StructuredJsonEntry],
) -> tuple[dict[str, Any | None], list[str]]:
    target = _nordstrom_target_product(structured_entries)
    source_url = _fact_value(source_slice.locator) or _fact_value(
        packet.source_locator
    )
    product_id = _nordstrom_product_id_from_url(source_url)
    if target is None or product_id is None:
        return {}, ["nordstrom_target_product_json_ld_absent"]
    product, _anchor = target
    offers = product.get("offers")
    if not isinstance(offers, dict):
        return {}, ["nordstrom_target_offer_json_ld_absent"]
    brand = product.get("brand")
    brand_name = (
        _string_or_none(brand.get("name")) if isinstance(brand, dict) else None
    )
    main_text = _bounded_text_section(
        visible_text, start="Main content", end="You Might Also Like"
    )
    details_text = _bounded_text_section(
        visible_text, start="Highlights", end="Reviews"
    )
    highlights_text = _bounded_text_section(
        details_text, start="Highlights", end="Details & care"
    )
    details_and_care = _bounded_text_section(
        details_text, start="Details & care", end="Ingredients"
    )
    ingredients = _bounded_text_section(
        details_text, start="Ingredients", end="Shipping & returns"
    )
    shipping_returns = _bounded_text_section(
        details_text, start="Shipping & returns", end="Gift options"
    )
    shipping_destination = _first_regex(
        main_text, (r"Shipping to\s+([^\r\n]+)",)
    )
    seller = _first_regex(main_text, (r"Sold by\s+([^\r\n]+)",))
    variant_name = _first_regex(main_text, (r"(One Size)",))
    item_number = _first_regex(details_text, (r"Item #([A-Za-z0-9-]+)",))
    core_product_id = _first_regex(
        details_text, (r"Core Product ID\s+([A-Za-z0-9-]+)",)
    )
    residuals: list[str] = []
    if shipping_destination:
        residuals.append(
            "nordstrom_shipping_destination_display_is_not_delivery_pin"
        )
    else:
        residuals.append("nordstrom_shipping_destination_display_absent")
    fields: dict[str, Any | None] = {
        "product_id": product_id,
        "sku": item_number,
        "core_product_id": core_product_id,
        "product_name": _string_or_none(product.get("name")),
        "brand": brand_name,
        "variant_name": variant_name,
        "price": _string_or_none(offers.get("price")),
        "price_display": _first_regex(
            main_text, (r"Current Price\s+(\$\d+(?:\.\d{2})?)",)
        ),
        "price_isolation": "nordstrom_target_product_json_ld",
        "price_currency": _string_or_none(offers.get("priceCurrency")),
        "availability": _string_or_none(offers.get("availability")),
        "seller": seller,
        "shipping_destination_display": (
            f"Shipping to {shipping_destination}" if shipping_destination else None
        ),
        "shipping_availability": None,
        "pickup_availability": _first_literal(
            main_text, ("No stores found near your location", "Pickup at choose store")
        ),
        "delivery_availability": None,
        "add_to_bag_present": "Add to Bag" in main_text,
        "description_html": _string_or_none(product.get("description")),
        "highlights": [
            line
            for line in _nonempty_lines(highlights_text)
            if line != "Highlights"
        ],
        "details_and_care_text": _compact_excerpt(details_and_care),
        "ingredients_text": _compact_excerpt(ingredients),
        "shipping_returns_text": _compact_excerpt(shipping_returns),
        "exact_inventory_quantity": "not_observed",
        "sold_units": "not_observed",
    }
    residuals.extend(_retail_commerce_absence_residuals("nordstrom", fields))
    return fields, list(dict.fromkeys(residuals))


def _nordstrom_review_fields(
    *,
    html: str,
    visible_text: str,
    structured_entries: list[_StructuredJsonEntry],
) -> tuple[dict[str, Any | None], list[str]]:
    target = _nordstrom_target_product(structured_entries)
    if target is None:
        return {}, ["nordstrom_target_product_json_ld_absent"]
    product, _anchor = target
    aggregate = product.get("aggregateRating")
    if not isinstance(aggregate, dict):
        return {}, ["nordstrom_target_aggregate_rating_absent"]

    review_section_start = html.find('id="product-page-reviews"')
    review_html = html[review_section_start:] if review_section_start >= 0 else ""
    rendered_reviews: list[dict[str, str]] = []
    review_pattern = re.compile(
        r'itemprop="review"[\s\S]*?'
        r'itemprop="name"\s+content="(?P<title>[^"]*)"[\s\S]*?'
        r'itemprop="author"\s+content="(?P<author>[^"]*)"[\s\S]*?'
        r'itemprop="datePublished"\s+content="(?P<date>[^"]*)"[\s\S]*?'
        r'itemprop="ratingValue"\s+content="(?P<rating>[^"]*)"[\s\S]*?'
        r'itemprop="reviewBody"\s+content="(?P<body>[^"]*)"',
        flags=re.IGNORECASE,
    )
    for match in review_pattern.finditer(review_html):
        rendered_reviews.append(
            {
                key: html_lib.unescape(value).strip()
                for key, value in match.groupdict().items()
            }
        )

    review_text = _bounded_text_section(
        visible_text, start="Reviews", end="Recommended for You"
    )
    buckets = {
        star: _first_regex(
            review_text, (rf"{star}\s+stars?\s+(\d+%)",)
        )
        for star in ("5", "4", "3", "2", "1")
    }
    residuals: list[str] = []
    percentages = [
        int(value[:-1])
        for value in buckets.values()
        if isinstance(value, str) and value.endswith("%")
    ]
    if len(percentages) != 5:
        residuals.append("nordstrom_rating_distribution_incomplete")
    elif sum(percentages) != 100:
        residuals.append(
            f"nordstrom_rating_distribution_source_rounding_total_{sum(percentages)}"
        )
    if not rendered_reviews:
        residuals.append("nordstrom_rendered_reviews_absent")

    structured_rating = _string_or_none(aggregate.get("ratingValue"))
    structured_count = _string_or_none(aggregate.get("reviewCount"))
    displayed_rating = _first_regex(
        review_text, (r"(\d+(?:\.\d+)?) out of 5",)
    )
    displayed_count = _first_regex(review_text, (r"Reviews\s+\(([\d,]+)\)",))
    if (
        structured_rating
        and displayed_rating
        and structured_rating != displayed_rating
    ):
        residuals.append("nordstrom_structured_displayed_rating_mismatch")
    if (
        structured_count
        and displayed_count
        and not _equivalent_review_count(structured_count, displayed_count)
    ):
        residuals.append("nordstrom_structured_displayed_review_count_mismatch")
    return (
        {
            "review_substrate_source": (
                "nordstrom_target_product_json_ld_and_rendered_review_microdata"
            ),
            "rating": displayed_rating or structured_rating,
            "structured_rating": structured_rating,
            "displayed_rating": displayed_rating,
            "review_count": displayed_count or structured_count,
            "structured_review_count": structured_count,
            "displayed_review_count": displayed_count,
            "rating_count": displayed_count or structured_count,
            "written_review_count": displayed_count or structured_count,
            "filtered_review_count": None,
            "rating_distribution_basis": "source_displayed_percent_rounded",
            "rating_distribution_buckets": buckets,
            "rendered_review_count": len(rendered_reviews),
            "rendered_reviews": rendered_reviews,
        },
        residuals,
    )


def _bounded_text_section(text: str, *, start: str, end: str) -> str:
    start_index = text.find(start)
    if start_index < 0:
        return ""
    end_index = text.find(end, start_index + len(start))
    if end_index < 0:
        return text[start_index:]
    return text[start_index:end_index]


def _nonempty_lines(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if line.strip()]


def _amazon_variant_offer_fields(
    *,
    html: str,
    visible_text: str,
    packet: SourceCapturePacket,
    source_slice: SourceCaptureSlice,
) -> dict[str, Any | None]:
    asin = _first_regex(
        html,
        (
            r"<input[^>]+(?:id|name)=[\"']ASIN[\"'][^>]+value=[\"']([^\"']+)[\"']",
            r"<input[^>]+value=[\"']([^\"']+)[\"'][^>]+(?:id|name)=[\"']ASIN[\"']",
            r"/dp/([A-Z0-9]{10})",
        ),
    )
    if asin is None:
        return {}
    price = _first_regex(
        html,
        (
            r"name=[\"']items\[0\.base\]\[customerVisiblePrice\]\[amount\][\"'][^>]+value=[\"']([^\"']+)[\"']",
            r"value=[\"']([^\"']+)[\"'][^>]+name=[\"']items\[0\.base\]\[customerVisiblePrice\]\[amount\][\"']",
        ),
    )
    # The DOM price input is target-anchored; the visible-text "$N" fallback is
    # position-dependent, so fallback-only price reads are carried but residualized.
    price_isolation = "amazon_dom_target_input"
    if price is None:
        price = _first_regex(visible_text, (r"\$(\d+(?:\.\d{2})?)",))
        price_isolation = "unanchored_visible_text_fallback" if price is not None else "absent"
    availability = _first_literal(visible_text, ("In Stock", "Currently unavailable", "Out of Stock"))
    variant_name = _first_regex(visible_text, (r"Style:\s*([^\n]+)",))
    return {
        "product_id": asin,
        "sku": asin,
        "variant_name": variant_name or _fact_value(source_slice.variant_pin),
        "price": price,
        "price_isolation": price_isolation,
        "price_currency": _fact_value(source_slice.currency_pin) or "USD",
        "availability": availability,
        "series_id": packet.series_id,
        "locale_pin": _fact_value(source_slice.locale_pin),
        "currency_pin": _fact_value(source_slice.currency_pin),
        "variant_pin": _fact_value(source_slice.variant_pin),
        "variant_binding_source": "amazon_dom_js",
    }


def _walmart_variant_offer_fields(
    *,
    html: str,
    visible_text: str,
    packet: SourceCapturePacket,
    source_slice: SourceCaptureSlice,
    structured_entries: list[_StructuredJsonEntry],
) -> dict[str, Any | None]:
    product_id = _retail_product_id(packet=packet, source_slice=source_slice, retailer="walmart")
    product = _walmart_next_data_product(structured_entries, product_id) or {}
    if not product and product_id is None:
        return {}
    price_info = product.get("priceInfo") if isinstance(product.get("priceInfo"), dict) else {}
    current_price = (
        price_info.get("currentPrice")
        if isinstance(price_info.get("currentPrice"), dict)
        else {}
    )
    line_price = (
        _string_or_none(price_info.get("linePrice"))
        or _string_or_none(price_info.get("linePriceDisplay"))
        or _string_or_none(current_price.get("priceString"))
        or _string_or_none(current_price.get("priceDisplay"))
    )
    price = _string_or_none(product.get("price")) or _string_or_none(current_price.get("price")) or line_price
    if price and price.startswith("$"):
        price = price[1:]
    availability_v2 = product.get("availabilityStatusV2") if isinstance(product.get("availabilityStatusV2"), dict) else {}
    channels = _fulfillment_channel_fields(visible_text)
    seller = _string_or_none(product.get("sellerName")) or _first_regex(visible_text, (r"Sold and shipped by\s+([^\n]+)",))
    return {
        "product_id": product_id or _string_or_none(product.get("usItemId")),
        "sku": product_id or _string_or_none(product.get("usItemId")),
        "product_name": _string_or_none(product.get("name")) or _meta_content(html, "property", "og:title"),
        "variant_name": _walmart_selected_variant(product, product_id) or _fact_value(source_slice.variant_pin),
        "price": price,
        "price_isolation": "walmart_next_data_product" if price else "absent",
        "price_currency": _fact_value(source_slice.currency_pin)
        or _string_or_none(current_price.get("currencyUnit"))
        or ("USD" if line_price and line_price.startswith("$") else None),
        "availability": _string_or_none(availability_v2.get("display")) or _string_or_none(product.get("availabilityStatus")) or _availability_summary(channels),
        **channels,
        "seller": seller,
        "location_context": _location_context(visible_text, "walmart"),
        "series_id": packet.series_id,
        "locale_pin": _fact_value(source_slice.locale_pin),
        "currency_pin": _fact_value(source_slice.currency_pin),
        "variant_pin": _fact_value(source_slice.variant_pin),
        "exact_inventory_quantity": None,
        "exact_inventory_quantity_posture": "not_observed",
        "sold_units": None,
        "sold_units_posture": "not_observed",
        "variant_binding_source": "walmart_next_data_and_rendered_dom",
    }


def _target_variant_offer_fields(
    *,
    html: str,
    visible_text: str,
    packet: SourceCapturePacket,
    source_slice: SourceCaptureSlice,
) -> dict[str, Any | None]:
    product_id = _retail_product_id(packet=packet, source_slice=source_slice, retailer="target")
    if product_id is None:
        return {}
    price = _first_regex(
        html,
        (r'data-test=["\'](?:current-price|product-price)["\'][\s\S]*?\$([\d,.]+)',),
    ) or _first_regex(visible_text, (r"^\$([\d,.]+)$",))
    channels = _fulfillment_channel_fields(visible_text)
    return {
        "product_id": product_id,
        "sku": product_id,
        "product_name": _meta_content(html, "property", "og:title") or _title_text(html),
        "variant_name": _fact_value(source_slice.variant_pin),
        "price": price,
        "price_isolation": "target_rendered_dom_current_price" if price else "absent",
        "price_currency": _fact_value(source_slice.currency_pin) or ("USD" if price else None),
        "availability": _availability_summary(channels),
        **channels,
        "seller": "Target" if "Target" in html else None,
        "location_context": _location_context(visible_text, "target"),
        "series_id": packet.series_id,
        "locale_pin": _fact_value(source_slice.locale_pin),
        "currency_pin": _fact_value(source_slice.currency_pin),
        "variant_pin": _fact_value(source_slice.variant_pin),
        "exact_inventory_quantity": None,
        "exact_inventory_quantity_posture": "not_observed",
        "sold_units": None,
        "sold_units_posture": "not_observed",
        "variant_binding_source": "target_rendered_dom",
    }


def _retail_commerce_absence_residuals(retailer: Retailer, fields: Mapping[str, object]) -> list[str]:
    if not fields:
        return []
    residuals = [f"{retailer}_exact_inventory_quantity_not_observed", f"{retailer}_sold_units_not_observed"]
    if not _string_or_none(fields.get("location_context")):
        residuals.append(f"{retailer}_location_pin_absent")
    return residuals


def _walmart_next_data_product(structured_entries: Sequence[_StructuredJsonEntry], product_id: str | None) -> dict[str, object] | None:
    if product_id is None:
        return None
    candidates = [
        item
        for entry in structured_entries
        if entry.kind == "next_data"
        for item in _walk_dicts(entry.parsed)
        if item.get("name") and item.get("usItemId")
        and _string_or_none(item.get("usItemId")) == product_id
    ]
    if not candidates:
        return None
    return max(candidates, key=lambda item: sum(value is not None for value in (item.get("price"), item.get("priceInfo"), item.get("averageRating"), item.get("availabilityStatusV2"), item.get("sellerName"))))


def _walmart_selected_variant(product: Mapping[str, object], product_id: str | None) -> str | None:
    variants = product.get("variantList")
    if not isinstance(variants, list):
        return None
    for variant in variants:
        if isinstance(variant, dict) and (product_id is None or _string_or_none(variant.get("usItemId")) == product_id):
            return _string_or_none(variant.get("displayName")) or _string_or_none(variant.get("name"))
    return None


def _target_review_fields(visible_text: str) -> dict[str, Any | None]:
    match = re.search(r"(\d+(?:\.\d+)?) out of 5 stars with ([\d,]+) reviews", visible_text, flags=re.IGNORECASE)
    rating = match.group(1) if match else None
    rating_count = match.group(2) if match else None
    filtered = _first_regex(visible_text, (r"We found ([\d,]+) matching reviews",))
    buckets = _rating_distribution_buckets(visible_text, basis="percent")
    if not any((rating, rating_count, filtered, buckets)):
        return {}
    return {
        "review_substrate_source": "target_rendered_review_widget",
        "rating": rating,
        "rating_count": rating_count,
        "review_count": None,
        "written_review_count": None,
        "filtered_review_count": filtered,
        "rating_distribution_basis": "percent" if buckets else None,
        "rating_distribution_buckets": buckets,
    }


def _walmart_review_fields(visible_text: str) -> dict[str, Any | None]:
    rating = _first_regex(visible_text, (r"Customer ratings & reviews\s+(\d+(?:\.\d+)?) out of 5",))
    counts = re.search(r"([\d,]+) ratings\|([\d,]+) reviews", visible_text, flags=re.IGNORECASE)
    rating_count = counts.group(1) if counts else _first_regex(visible_text, (r"([\d,]+) ratings",))
    written = counts.group(2) if counts else _first_regex(visible_text, (r"View all reviews \(([\d,]+)\)",))
    buckets = _rating_distribution_buckets(visible_text, basis="count")
    if not any((rating, rating_count, written, buckets)):
        return {}
    return {
        "review_substrate_source": "walmart_rendered_review_widget",
        "rating": rating,
        "rating_count": rating_count,
        "review_count": written,
        "written_review_count": written,
        "filtered_review_count": None,
        "rating_distribution_basis": "count" if buckets else None,
        "rating_distribution_buckets": buckets,
    }


def _yotpo_review_fields(
    html: str,
) -> tuple[dict[str, Any | None], list[str]]:
    section_match = re.search(
        r"<div\b(?=[^>]*\bid=[\"']yotpo-reviews-section-data[\"'])[^>]*>"
        r"(?P<body>.*?)</div>",
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if section_match is None:
        return {}, []
    section = section_match.group("body")
    aggregate = re.search(
        r"Overall\s+rating:\s*</strong>\s*"
        r"(?P<rating>\d+(?:\.\d+)?)\s*/\s*5\s+from\s+"
        r"(?P<count>[\d,]+)\s+reviews?\b",
        section,
        flags=re.IGNORECASE | re.DOTALL,
    )
    rating = aggregate.group("rating") if aggregate is not None else None
    review_count = aggregate.group("count") if aggregate is not None else None

    displayed_reviews: list[dict[str, str | None]] = []
    for article_match in re.finditer(
        r"<article\b(?P<attrs>[^>]*)>(?P<body>.*?)</article>",
        section,
        flags=re.IGNORECASE | re.DOTALL,
    ):
        attrs = article_match.group("attrs")
        class_value = _html_attr_value(attrs, "class") or ""
        if "yotpo-review" not in class_value.split():
            continue
        article = article_match.group("body")
        displayed_reviews.append(
            {
                "reviewer": _html_attr_value(attrs, "data-reviewer"),
                "rating": _html_attr_value(attrs, "data-rating"),
                "title": _html_element_text_by_class(
                    article,
                    tag="h4",
                    class_name="yotpo-review-title",
                ),
                "body": _html_element_text_by_class(
                    article,
                    tag="p",
                    class_name="yotpo-review-body",
                ),
            }
        )

    ai_summary_section = _first_regex(
        section,
        (
            r"<section\b[^>]*\bid=[\"']yotpo-reviews-ai-summary[\"'][^>]*>"
            r"(.*?)</section>",
        ),
    )
    ai_summary = (
        _html_element_text_by_classless_tag(ai_summary_section, tag="p")
        if ai_summary_section is not None
        else None
    )
    body_count = sum(
        1
        for review in displayed_reviews
        if isinstance(review.get("body"), str) and review["body"]
    )
    if rating is None and review_count is None and not displayed_reviews:
        return {}, []

    residuals: list[str] = []
    numeric_review_count = (
        int(review_count.replace(",", "")) if review_count is not None else None
    )
    if (
        numeric_review_count is not None
        and len(displayed_reviews) < numeric_review_count
    ):
        residuals.append(
            "yotpo_displayed_review_subset_"
            f"{len(displayed_reviews)}_of_{numeric_review_count}"
        )
    if body_count < len(displayed_reviews):
        residuals.append(
            f"yotpo_review_bodies_present_{body_count}_of_{len(displayed_reviews)}"
        )

    return {
        "review_substrate_source": "yotpo_server_rendered_review_section",
        "rating": rating,
        "rating_count": review_count,
        "review_count": review_count,
        "written_review_count": review_count,
        "filtered_review_count": None,
        "rating_distribution_basis": None,
        "rating_distribution_buckets": [],
        "displayed_review_count": len(displayed_reviews),
        "displayed_review_body_count": body_count,
        "displayed_reviews": displayed_reviews,
        "review_body_coverage": (
            "displayed_subset_not_complete_corpus"
            if numeric_review_count is not None
            and len(displayed_reviews) < numeric_review_count
            else "displayed_rows_only"
        ),
        "ai_summary_type": "retailer_labeled_ai_generated",
        "ai_generated_review_summary": ai_summary,
    }, residuals


def _rating_distribution_buckets(visible_text: str, *, basis: Literal["count", "percent"]) -> list[dict[str, int]]:
    buckets: list[dict[str, int]] = []
    for stars in range(5, 0, -1):
        if basis == "count":
            match = re.search(rf"{stars} stars?\s+(\d+)%\s*\(([\d,]+)\)", visible_text, flags=re.IGNORECASE)
            if match:
                buckets.append({"stars": stars, "value": int(match.group(2).replace(",", "")), "source_percent": int(match.group(1))})
        else:
            match = re.search(rf"{stars} stars?\s+(\d+)%", visible_text, flags=re.IGNORECASE)
            if match:
                buckets.append({"stars": stars, "value": int(match.group(1))})
    return buckets


def _fulfillment_channel_fields(visible_text: str) -> dict[str, str | None]:
    return {
        "shipping_availability": _line_after_heading(visible_text, "Shipping"),
        "pickup_availability": _line_after_heading(visible_text, "Pickup"),
        "delivery_availability": _line_after_heading(visible_text, "Delivery"),
    }


def _line_after_heading(text: str, heading: str) -> str | None:
    lines = [line.strip() for line in text.splitlines()]
    for index, line in enumerate(lines):
        if line.lower() == heading.lower():
            return next((candidate for candidate in lines[index + 1 : index + 4] if candidate), None)
    return None


def _availability_summary(channels: Mapping[str, object]) -> str | None:
    parts = [f"{name.removesuffix('_availability')}={value}" for name, value in channels.items() if isinstance(value, str) and value.strip()]
    return "; ".join(parts) or None


def _location_context(visible_text: str, retailer: Retailer) -> str | None:
    if retailer == "walmart":
        return _first_regex(visible_text, (r"([A-Za-z .'-]+,\s*\d{5})",))
    if retailer == "target":
        return _first_regex(visible_text, (r"(Ship to\s+\d{5})",))
    return None


def _retail_product_id(*, packet: SourceCapturePacket, source_slice: SourceCaptureSlice, retailer: Retailer) -> str | None:
    locator = _fact_value(source_slice.locator) or _fact_value(packet.source_locator) or ""
    if retailer == "target":
        return _first_regex(locator, (r"/A-(\d+)",))
    if retailer == "walmart":
        return _first_regex(locator, (r"/(\d+)(?:[/?#]|$)",))
    return None


def _meta_content(html: str, attr_name: str, attr_value: str) -> str | None:
    for match in re.finditer(r"<meta\b[^>]*>", html, flags=re.IGNORECASE):
        tag = match.group(0)
        if (_html_attr_value(tag, attr_name) or "").lower() == attr_value.lower():
            return _html_attr_value(tag, "content")
    return None


def _title_text(html: str) -> str | None:
    return _first_regex(html, (r"<title[^>]*>(.*?)</title>",))


def _structured_variant_offer_fields(
    structured_entries: list[_StructuredJsonEntry],
    *,
    preferred_sku: str | None = None,
) -> tuple[dict[str, Any | None], RetailProjectionRawAnchor | None]:
    for entry in structured_entries:
        for product in _walk_dicts(entry.parsed):
            product_type = product.get("@type")
            if isinstance(product_type, list):
                product_type_values = set(str(item) for item in product_type)
            else:
                product_type_values = {str(product_type)} if product_type is not None else set()
            if "ProductGroup" in product_type_values:
                variants = product.get("hasVariant")
                if isinstance(variants, list) and variants:
                    candidates = [item for item in variants if isinstance(item, dict)]
                    variant = (
                        next(
                            (
                                item
                                for item in candidates
                                if _string_or_none(item.get("sku")) == preferred_sku
                            ),
                            None,
                        )
                        if preferred_sku
                        else next(iter(candidates), None)
                    )
                    if variant is not None:
                        offer = variant.get("offers") if isinstance(variant.get("offers"), dict) else {}
                        return _offer_fields_from_product(product, variant, offer, entry.kind), entry.raw_anchor
            if "Product" in product_type_values:
                if preferred_sku and _string_or_none(product.get("sku")) != preferred_sku:
                    continue
                raw_offers = product.get("offers")
                if isinstance(raw_offers, dict):
                    offer = raw_offers
                elif isinstance(raw_offers, list):
                    candidates = [item for item in raw_offers if isinstance(item, dict)]
                    offer = (
                        next(
                            (
                                item
                                for item in candidates
                                if _string_or_none(item.get("sku"))
                                == _string_or_none(product.get("sku"))
                            ),
                            None,
                        )
                        or next(
                            (
                                item
                                for item in candidates
                                if _string_or_none(item.get("price")) is not None
                                and _string_or_none(item.get("priceCurrency")) is not None
                            ),
                            None,
                        )
                        or {}
                    )
                else:
                    offer = {}
                return _offer_fields_from_product(product, product, offer, entry.kind), entry.raw_anchor
    return {}, None


def _sephora_structured_offer_substrate_skus(structured_entries: list[_StructuredJsonEntry]) -> set[str]:
    skus: set[str] = set()
    for entry in structured_entries:
        for product in _walk_dicts(entry.parsed):
            product_type = product.get("@type")
            if isinstance(product_type, list):
                product_type_values = set(str(item) for item in product_type)
            else:
                product_type_values = {str(product_type)} if product_type is not None else set()
            if "ProductGroup" in product_type_values:
                variants = product.get("hasVariant")
                if isinstance(variants, list):
                    for item in variants:
                        if isinstance(item, dict):
                            sku = _string_or_none(item.get("sku"))
                            if sku:
                                skus.add(sku)
            if "Product" in product_type_values:
                sku = _string_or_none(product.get("sku"))
                if sku:
                    skus.add(sku)
    return skus


def _offer_fields_from_product(
    group_or_product: Mapping[str, object],
    variant: Mapping[str, object],
    offer: Mapping[str, object],
    source: str,
) -> dict[str, Any | None]:
    return {
        "product_id": _string_or_none(group_or_product.get("productGroupID"))
        or _string_or_none(group_or_product.get("productID"))
        or _string_or_none(variant.get("productID")),
        "sku": _string_or_none(variant.get("sku")),
        "variant_name": _string_or_none(variant.get("color")) or _string_or_none(variant.get("scent")) or _string_or_none(variant.get("name")),
        "price": _string_or_none(offer.get("price")),
        "price_isolation": "structured_json_offer" if _string_or_none(offer.get("price")) else "absent",
        "price_currency": _string_or_none(offer.get("priceCurrency")),
        "availability": _string_or_none(offer.get("availability")),
        "price_binding_source": source,
        "variant_binding_source": source,
    }


def _ulta_apollo_offer_fields(
    structured_entries: list[_StructuredJsonEntry],
) -> tuple[dict[str, Any | None], RetailProjectionRawAnchor | None]:
    for entry in structured_entries:
        if entry.kind != "apollo_state":
            continue
        requested_sku = _first_regex(entry.raw_text, (r'\\"sku\\":\\"([^\\"]+)\\"', r'"sku":"([^"]+)"'))
        best: dict[str, object] | None = None
        for item in _walk_dicts(entry.parsed):
            if item.get("skuId") and item.get("productName") and (item.get("listPrice") or item.get("salePrice")):
                best = item
                break
        if best is None:
            return {}, entry.raw_anchor
        price = _string_or_none(best.get("salePrice")) or _string_or_none(best.get("listPrice"))
        return {
            "product_id": _string_or_none(best.get("productId")),
            "sku": _string_or_none(best.get("skuId")),
            "variant_name": _string_or_none(best.get("productName")),
            "price": price[1:] if isinstance(price, str) and price.startswith("$") else price,
            "price_currency": "USD" if price else None,
            "availability": _first_literal(json.dumps(entry.parsed), ("InStock", "OutOfStock")),
            "apollo_requested_sku": requested_sku,
            "variant_binding_source": "apollo_state",
        }, entry.raw_anchor
    return {}, None


def _ulta_apollo_offer_substrate_present(structured_entries: list[_StructuredJsonEntry]) -> bool:
    for entry in structured_entries:
        if entry.kind != "apollo_state":
            continue
        for item in _walk_dicts(entry.parsed):
            if item.get("skuId") and (item.get("listPrice") or item.get("salePrice")):
                return True
    return False


def _sephora_dom_offer_fields(html: str) -> dict[str, Any | None]:
    for match in re.finditer(r"<[^>]*data-comp=\"ProductPage[^\"]*\"[^>]*>", html, flags=re.IGNORECASE):
        tag = match.group(0)
        price = _html_attr_value(tag, "data-cnstrc-item-price")
        if price is None:
            continue
        return {
            "dom_product_id": _html_attr_value(tag, "data-cnstrc-item-id"),
            "dom_sku": _html_attr_value(tag, "data-cnstrc-item-variation-id"),
            "dom_price": price.lstrip("$"),
            "price": price.lstrip("$"),
            "price_isolation": "sephora_dom_product_page",
            "price_binding_source": "rendered_dom_product_page",
        }
    return {}


def _structured_price_residuals(
    *,
    retailer: Retailer,
    structured_fields: Mapping[str, object],
) -> list[str]:
    if (
        retailer == "sephora"
        and _string_or_none(structured_fields.get("price"))
        and structured_fields.get("price_isolation") == "structured_json_offer"
    ):
        return ["sephora_price_from_structured_json_without_target_dom_price"]
    return []


def _sku_from_variant_pin(variant_pin: str | None) -> str | None:
    if variant_pin is None:
        return None
    return _first_regex(variant_pin, (r"\bsku=([A-Za-z0-9_-]+)", r"\bsku:\s*([A-Za-z0-9_-]+)"))


def _amazon_review_fields(*, html: str, visible_text: str) -> dict[str, Any | None]:
    rating = _first_regex(visible_text, (r"Customer reviews\s+(\d+(?:\.\d+)?) out of 5", r"(\d+(?:\.\d+)?) out of 5 stars"))
    count = _first_regex(visible_text, (r"([\d,]+) global ratings", r"([\d,]+) ratings"))
    best_sellers_rank = _first_regex(visible_text, (r"(Best Sellers Rank:[^\n]+(?:\n#[^\n]+)*)",))
    ld_json_present = bool(_extract_ld_json_texts(html))
    average_customer_reviews_node_present = "averageCustomerReviews" in html
    acr_customer_review_text_node_present = "acrCustomerReviewText" in html
    if not any(
        (
            rating,
            count,
            best_sellers_rank,
            ld_json_present,
            average_customer_reviews_node_present,
            acr_customer_review_text_node_present,
        )
    ):
        return {}
    return {
        "review_substrate_source": "amazon_dom_js",
        "ld_json_present": ld_json_present,
        "average_customer_reviews_node_present": average_customer_reviews_node_present,
        "acr_customer_review_text_node_present": acr_customer_review_text_node_present,
        "rating": rating,
        "review_count": count,
        "best_sellers_rank_text": best_sellers_rank,
    }


def _sephora_review_fields(
    *,
    html: str,
    visible_text: str,
    structured_entries: list[_StructuredJsonEntry],
) -> dict[str, Any | None]:
    # The target header's abbreviated count, the exact ReviewsStats count, and JSON-LD
    # are separate source observations. Preserve all three rather than normalizing them.
    review_section_html = _sephora_review_section_html(html)
    html_displayed_count = _first_regex(
        review_section_html,
        (r"Ratings\s*&(?:amp;)?\s*Reviews\s*\(([^)]+)\)",),
    )
    visible_displayed_count = _first_regex(
        visible_text,
        (r"Ratings & Reviews\s*\(([^)]+)\)",),
    )
    anchored_count = html_displayed_count or visible_displayed_count
    fallback_count = _first_regex(visible_text, (r"([^\s]+)\s+Reviews\*?",))
    displayed_count = anchored_count or fallback_count
    review_count_isolation = (
        "target_anchored" if anchored_count else ("unanchored_fallback" if fallback_count else "absent")
    )

    target_widget_review_count = _first_regex(
        review_section_html,
        (r">\s*([\d,]+)\s+Reviews\*\s*<",),
    )
    if target_widget_review_count is None and anchored_count:
        visible_target_start = re.search(
            r"Ratings & Reviews\s*\([^)]+\)",
            visible_text,
            flags=re.IGNORECASE,
        )
        if visible_target_start:
            target_widget_review_count = _first_regex(
                visible_text[visible_target_start.end() : visible_target_start.end() + 3000],
                (r"([\d,]+)\s+Reviews\*",),
            )

    rating = _first_regex(visible_text, (r"Summary\s+5\s+4\s+3\s+2\s+1\s+(\d+(?:\.\d+)?)",))
    ld_count = None
    ld_rating = None
    for entry in structured_entries:
        if entry.kind != "ld_json":
            continue
        for item in _walk_dicts(entry.parsed):
            aggregate = item.get("aggregateRating")
            if isinstance(aggregate, dict):
                ld_count = _string_or_none(aggregate.get("reviewCount")) or ld_count
                ld_rating = _string_or_none(aggregate.get("ratingValue")) or ld_rating
    recommendation_counts = re.findall(
        r'data-cnstrc-item=["\']recommendation["\'][\s\S]{0,1400}?aria-label=["\']([^"\']+ reviews)["\']',
        html,
        flags=re.IGNORECASE,
    )
    return {
        "review_substrate_source": "sephora_target_dom",
        "bazaarvoice_api_config_present": "api.bazaarvoice.com" in html.lower(),
        "rating": rating or ld_rating,
        "review_count": displayed_count,
        "displayed_review_count_text": displayed_count,
        "target_widget_review_count": target_widget_review_count,
        "structured_review_count": ld_count,
        "review_count_isolation": review_count_isolation,
        "ld_json_review_count": ld_count,
        "ld_json_rating": ld_rating,
        "rating_distribution_histogram": _sephora_rating_distribution(review_section_html),
        "recommendation_review_count_examples": recommendation_counts[:5],
        "recommendation_counts_are_not_target_substrate": bool(recommendation_counts),
    }


def _sephora_review_section_anchor(html: str) -> str | None:
    match = re.search(
        r'data-at=["\']ratings_reviews_section["\']',
        html,
        flags=re.IGNORECASE,
    )
    return match.group(0) if match else None


def _sephora_review_section_html(html: str) -> str:
    anchor = re.search(
        r'data-at=["\']ratings_reviews_section["\']',
        html,
        flags=re.IGNORECASE,
    )
    if anchor is None:
        return ""
    return html[anchor.start() : anchor.start() + 6000]


def _sephora_rating_distribution(review_section_html: str) -> dict[str, Any] | None:
    matches = re.findall(
        r'Histogram-label[^>]*>\s*([1-5])\s*</span>[\s\S]{0,800}?style=["\'][^"\']*width:\s*([0-9]+(?:\.[0-9]+)?)%;',
        review_section_html,
        flags=re.IGNORECASE,
    )
    percentages: dict[int, str] = {}
    ambiguous_ratings: set[int] = set()
    for raw_rating, raw_value in matches:
        rating = int(raw_rating)
        if rating in percentages and percentages[rating] != raw_value:
            ambiguous_ratings.add(rating)
        percentages.setdefault(rating, raw_value)
    if ambiguous_ratings or set(percentages) != {1, 2, 3, 4, 5}:
        return None
    return {
        "basis": "percent",
        "order": "5_to_1",
        "buckets": [
            {"rating": rating, "value": percentages[rating]}
            for rating in (5, 4, 3, 2, 1)
        ],
    }


def _equivalent_review_count(left: str, right: str) -> bool:
    return left.replace(",", "").strip() == right.replace(",", "").strip()


def _ulta_review_fields(structured_entries: list[_StructuredJsonEntry]) -> tuple[dict[str, Any | None], list[str]]:
    residuals: list[str] = []
    ld_count = None
    ld_rating = None
    apollo_count = None
    apollo_rating = None
    for entry in structured_entries:
        for item in _walk_dicts(entry.parsed):
            aggregate = item.get("aggregateRating") if isinstance(item, dict) else None
            if entry.kind == "ld_json" and isinstance(aggregate, dict):
                ld_count = _string_or_none(aggregate.get("reviewCount")) or ld_count
                ld_rating = _string_or_none(aggregate.get("ratingValue")) or ld_rating
            if entry.kind == "apollo_state" and item.get("reviewCount") and item.get("rating"):
                apollo_count = _string_or_none(item.get("reviewCount")) or apollo_count
                apollo_rating = _string_or_none(item.get("rating")) or apollo_rating
    if ld_count and apollo_count and ld_count != apollo_count:
        residuals.append("ulta_ld_json_apollo_review_count_mismatch")
    if ld_rating and apollo_rating and ld_rating != apollo_rating:
        residuals.append("ulta_ld_json_apollo_rating_mismatch")
    return {
        "review_substrate_source": "ulta_ld_json_and_apollo_state",
        "review_count": apollo_count or ld_count,
        "rating": apollo_rating or ld_rating,
        "ld_json_review_count": ld_count,
        "ld_json_rating": ld_rating,
        "apollo_review_count": apollo_count,
        "apollo_rating": apollo_rating,
    }, residuals


def _carried_module_fields(
    *,
    retailer: Retailer,
    html: str,
    visible_text_files: Sequence[tuple[PreservedFile, str]],
    raw_anchor: RetailProjectionRawAnchor,
) -> list[dict[str, Any]]:
    modules: list[dict[str, Any]] = []
    module_specs = [
        ("shipping", ("FREE delivery", "standard shipping", "same day delivery", "deliveryBlock")),
        ("loyalty", ("Beauty Insider", "earn points", "Store Card", "Rewards")),
        ("recommendations", ("data-cnstrc-item=\"recommendation\"", "customers bought together", "Make it a routine")),
    ]
    anchorable_texts = [
        ("rendered_dom", html, raw_anchor),
        *[
            ("visible_text", text, _raw_anchor(preserved_file))
            for preserved_file, text in visible_text_files
        ],
    ]
    for module_type, patterns in module_specs:
        match = _first_module_anchor_match(anchorable_texts, patterns)
        if match is None:
            continue
        source_label, matched, anchor_fragment, excerpt, match_anchor = match
        modules.append(
            {
                "module_type": module_type,
                "retailer": retailer,
                "anchor_pattern": matched,
                "anchor_source": source_label,
                "text_excerpt": excerpt,
                "raw_anchor": _with_anchor(match_anchor, "text_pattern", anchor_fragment),
            }
        )
    return modules


def _collapse_entries(
    *,
    html: str,
    visible_text: str,
    raw_anchor: RetailProjectionRawAnchor,
) -> list[RetailPdpProjectionLossEntry]:
    entries: list[RetailPdpProjectionLossEntry] = []
    hero_count = len(re.findall(r"hero|ProductHero|imageBlock|main-hero", html, flags=re.IGNORECASE))
    if hero_count:
        entries.append(
            RetailPdpProjectionLossEntry(
                category="RETAIL_HERO_IMAGERY_COLLAPSED",
                count=hero_count,
                raw_anchor=_with_anchor(raw_anchor, "text_pattern", "hero|ProductHero|imageBlock|main-hero"),
                reason="hero imagery presence collapsed to raw-anchored ledger entry; raw bytes remain canonical",
            )
        )
    cart_count = len(re.findall(r"add to cart|add to bag|add for ship|out of stock|notify me", visible_text, flags=re.IGNORECASE))
    if cart_count:
        entries.append(
            RetailPdpProjectionLossEntry(
                category="RETAIL_CART_NOTIFY_STATE_COLLAPSED",
                count=cart_count,
                raw_anchor=_with_anchor(raw_anchor, "text_pattern", "add to cart|add to bag|add for ship|out of stock|notify me"),
                reason="cart/notify button chrome collapsed while variant availability binding is carried",
            )
        )
    return entries


def _product_context_fields(
    packet: SourceCapturePacket,
    source_slice: SourceCaptureSlice,
    retailer: str,
) -> dict[str, Any | None]:
    return {
        "retailer": retailer,
        "source_family": packet.source_family,
        "source_surface": packet.source_surface,
        "source_locator": _fact_value(packet.source_locator),
        "slice_locator": _fact_value(source_slice.locator),
        "series_id": packet.series_id,
        "locale_pin": _fact_value(source_slice.locale_pin),
        "currency_pin": _fact_value(source_slice.currency_pin),
        "variant_pin": _fact_value(source_slice.variant_pin),
        "location_pin": None,
        "capture_time": _fact_value(source_slice.timing.capture_time),
        "cutoff_posture": _fact_value(source_slice.timing.cutoff_posture),
        "archive_history_posture": _fact_value(source_slice.archive_history_posture),
    }


def _detect_retailer(packet: SourceCapturePacket) -> Retailer:
    haystack = " ".join(
        item
        for item in [
            packet.series_id or "",
            _fact_value(packet.source_locator) or "",
            packet.requested_decision_context.value if packet.requested_decision_context.status == VisibleFactStatus.KNOWN else "",
        ]
        if item
    ).lower()
    if "amazon." in haystack or "amazon_" in haystack or "amazon " in haystack:
        return "amazon"
    if "nordstrom." in haystack or "nordstrom_" in haystack or "nordstrom " in haystack:
        return "nordstrom"
    if "sephora." in haystack or "sephora_" in haystack or "sephora " in haystack:
        return "sephora"
    if (
        "luckyscent." in haystack
        or "luckyscent_" in haystack
        or "luckyscent " in haystack
    ):
        return "luckyscent"
    if "ulta." in haystack or "ulta_" in haystack or "ulta " in haystack:
        return "ulta"
    if "walmart." in haystack or "walmart_" in haystack or "walmart " in haystack:
        return "walmart"
    if "target." in haystack or "target_" in haystack or "target " in haystack:
        return "target"
    return "unknown"


def _extract_ld_json_texts(html: str) -> list[str]:
    return [
        match.group("body")
        for match in re.finditer(
            r"<script\b(?P<attrs>[^>]*)>(?P<body>.*?)</script>",
            html,
            flags=re.IGNORECASE | re.DOTALL,
        )
        if re.search(r"type\s*=\s*['\"]application/ld\+json['\"]", match.group("attrs"), flags=re.IGNORECASE)
    ]


def _extract_next_data_text(html: str) -> str | None:
    for match in re.finditer(r"<script\b(?P<attrs>[^>]*)>(?P<body>.*?)</script>", html, flags=re.IGNORECASE | re.DOTALL):
        if re.search(r"\bid\s*=\s*['\"]__NEXT_DATA__['\"]", match.group("attrs"), flags=re.IGNORECASE):
            return match.group("body").strip()
    return None


def _extract_apollo_state_text(html: str) -> str | None:
    marker = "window.__APOLLO_STATE__"
    marker_index = html.find(marker)
    if marker_index < 0:
        return None
    start = html.find("{", marker_index)
    if start < 0:
        return None
    return _balanced_json_object(html, start)


def _balanced_json_object(text: str, start: int) -> str | None:
    depth = 0
    in_string = False
    escaped = False
    for index in range(start, len(text)):
        char = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[start : index + 1]
    return None


def _safe_json_loads(raw_text: str | None) -> object | None:
    if raw_text is None:
        return None
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        return None


def _walk_dicts(value: object) -> list[dict[str, object]]:
    found: list[dict[str, object]] = []
    if isinstance(value, dict):
        found.append(value)
        for child in value.values():
            found.extend(_walk_dicts(child))
    elif isinstance(value, list):
        for child in value:
            found.extend(_walk_dicts(child))
    return found


def _raw_anchor(preserved_file: PreservedFile) -> RetailProjectionRawAnchor:
    return RetailProjectionRawAnchor(
        file_id=preserved_file.file_id,
        relative_packet_path=preserved_file.relative_packet_path,
        sha256=preserved_file.sha256,
        hash_basis=preserved_file.hash_basis,
        anchor_kind="file",
    )


def _with_anchor(raw_anchor: RetailProjectionRawAnchor, anchor_kind: str, anchor_value: str) -> RetailProjectionRawAnchor:
    return RetailProjectionRawAnchor(
        file_id=raw_anchor.file_id,
        relative_packet_path=raw_anchor.relative_packet_path,
        sha256=raw_anchor.sha256,
        hash_basis=raw_anchor.hash_basis,
        anchor_kind=anchor_kind,
        anchor_value=anchor_value,
    )


def _load_packet_directory_projection_inputs(packet_directory: Path) -> tuple[SourceCapturePacket, dict[str, bytes]]:
    manifest_path = packet_directory / "manifest.json"
    raw_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(raw_manifest, dict):
        raise RetailPdpProjectionInputError(f"manifest is not a JSON object: {manifest_path}")

    packet = SourceCapturePacket.model_validate(raw_manifest)
    raw_file_bytes_by_file_id: dict[str, bytes] = {}
    for preserved_file in packet.preserved_files:
        file_path = _resolve_packet_relative_path(
            packet_directory=packet_directory,
            relative_packet_path=preserved_file.relative_packet_path,
            file_id=preserved_file.file_id,
        )
        if not file_path.is_file():
            raise RetailPdpProjectionInputError(
                f"preserved file for {preserved_file.file_id!r} not found at "
                f"{preserved_file.relative_packet_path!r} under the packet dir; block-don't-repair."
            )
        body = file_path.read_bytes()
        if len(body) != preserved_file.size_bytes:
            raise RetailPdpProjectionInputError(
                f"preserved file size mismatch for {preserved_file.file_id!r} "
                f"(read {len(body)}, manifest {preserved_file.size_bytes}); block-don't-repair."
            )
        recomputed_sha256 = hashlib.sha256(body).hexdigest()
        if recomputed_sha256 != preserved_file.sha256:
            raise RetailPdpProjectionInputError(
                f"preserved file sha256 mismatch for {preserved_file.file_id!r} "
                f"(recomputed {recomputed_sha256}, manifest {preserved_file.sha256}); block-don't-repair."
            )
        raw_file_bytes_by_file_id[preserved_file.file_id] = body
    return packet, raw_file_bytes_by_file_id


def _resolve_packet_relative_path(*, packet_directory: Path, relative_packet_path: str, file_id: str) -> Path:
    candidate = Path(relative_packet_path)
    if candidate.is_absolute():
        raise RetailPdpProjectionInputError(
            f"preserved path {relative_packet_path!r} for {file_id!r} is absolute; block-don't-repair."
        )
    packet_root = packet_directory.resolve()
    resolved = (packet_root / candidate).resolve()
    try:
        resolved.relative_to(packet_root)
    except ValueError as exc:
        raise RetailPdpProjectionInputError(
            f"preserved path {relative_packet_path!r} for {file_id!r} resolves outside the packet dir; "
            f"block-don't-repair."
        ) from exc
    return resolved


def _decode_text(body: bytes) -> str:
    return body.decode("utf-8", errors="replace")


def _fact_value(fact: object | None) -> str | None:
    if fact is None:
        return None
    if getattr(fact, "status", None) == VisibleFactStatus.KNOWN:
        return getattr(fact, "value", None)
    return None


def _json_type(value: object | None) -> str | None:
    if isinstance(value, dict):
        at_type = value.get("@type")
        return str(at_type) if at_type is not None else "object"
    if isinstance(value, list):
        return "list"
    return None


def _first_regex(text: str, patterns: tuple[str, ...]) -> str | None:
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL)
        if match:
            return " ".join(match.group(1).split())
    return None


def _first_literal(text: str, literals: tuple[str, ...]) -> str | None:
    lower = text.lower()
    for literal in literals:
        if literal.lower() in lower:
            return literal
    return None


def _html_attr_value(tag: str, attr_name: str) -> str | None:
    return _first_regex(tag, (rf"\b{re.escape(attr_name)}=[\"']([^\"']+)[\"']",))


def _html_element_text_by_class(
    fragment: str,
    *,
    tag: str,
    class_name: str,
) -> str | None:
    raw = _first_regex(
        fragment,
        (
            rf"<{re.escape(tag)}\b"
            rf"(?=[^>]*\bclass=[\"'][^\"']*\b{re.escape(class_name)}\b[^\"']*[\"'])"
            rf"[^>]*>(.*?)</{re.escape(tag)}>",
        ),
    )
    return _clean_html_text(raw) if raw is not None else None


def _html_element_text_by_classless_tag(
    fragment: str,
    *,
    tag: str,
) -> str | None:
    raw = _first_regex(
        fragment,
        (rf"<{re.escape(tag)}\b[^>]*>(.*?)</{re.escape(tag)}>",),
    )
    return _clean_html_text(raw) if raw is not None else None


def _clean_html_text(value: str) -> str | None:
    text = html_lib.unescape(re.sub(r"<[^>]+>", " ", value))
    compact = " ".join(text.split())
    return compact or None


def _string_or_none(value: object) -> str | None:
    # helper-delta: does not strip and also renders float/bool, unlike harness_utils.string_or_none.
    if value is None:
        return None
    if isinstance(value, (str, int, float)):
        text = str(value)
        return text if text else None
    return None


def _normalized_url_identity(value: str) -> str:
    parsed = urlparse(value)
    return (
        f"{parsed.scheme.lower()}://{(parsed.hostname or '').lower()}"
        f"{parsed.path.rstrip('/')}"
    )


def _text_section(
    text: str,
    *,
    start_heading: str,
    end_heading: str,
) -> str | None:
    lines = [line.strip() for line in text.splitlines()]
    try:
        start = next(
            index
            for index, line in enumerate(lines)
            if line.lower() == start_heading.lower()
        )
    except StopIteration:
        return None
    end = next(
        (
            index
            for index in range(start + 1, len(lines))
            if lines[index].lower() == end_heading.lower()
        ),
        len(lines),
    )
    value = " ".join(line for line in lines[start + 1 : end] if line)
    return value or None


def _html_text(value: str | None) -> str | None:
    if value is None:
        return None
    text = unescape(re.sub(r"<[^>]+>", " ", value))
    compact = " ".join(text.split())
    return compact or None


def _equivalent_offer_value(key: str, left: str, right: str) -> bool:
    if left == right:
        return True
    if key == "availability":
        return left.rstrip("/").endswith(right.rstrip("/")) or right.rstrip("/").endswith(left.rstrip("/"))
    return False


def _residualize_ulta_requested_sku_mismatch(
    fields: Mapping[str, Any | None],
    residuals: list[str],
    *,
    source_slice: SourceCaptureSlice | None = None,
) -> None:
    requested_sku = _string_or_none(fields.get("apollo_requested_sku"))
    if requested_sku is None and source_slice is not None:
        requested_sku = _sku_from_variant_pin(_fact_value(source_slice.variant_pin))
    rendered_sku = _string_or_none(fields.get("sku")) or _string_or_none(fields.get("apollo_sku"))
    residual = "ulta_requested_sku_rendered_sku_mismatch"
    if requested_sku and rendered_sku and requested_sku != rendered_sku and residual not in residuals:
        residuals.append(residual)


def _row_token(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.:-]+", "_", value) or "unknown"


def _excerpt(text: str, pattern: str, *, radius: int = 140) -> str:
    index = text.lower().find(pattern.lower())
    if index < 0:
        return ""
    return _compact_excerpt(text[max(0, index - radius) : index + len(pattern) + radius])


def _first_module_anchor_match(
    anchorable_texts: Sequence[tuple[str, str, RetailProjectionRawAnchor]],
    patterns: Sequence[str],
) -> tuple[str, str, str, str, RetailProjectionRawAnchor] | None:
    for pattern in patterns:
        for source_label, text, raw_anchor in anchorable_texts:
            index = _case_preferred_index(text, pattern)
            if index < 0:
                continue
            anchor_fragment = _raw_excerpt_fragment(text, index, len(pattern))
            return source_label, pattern, anchor_fragment, _compact_excerpt(anchor_fragment), raw_anchor
    return None


def _case_preferred_index(text: str, pattern: str) -> int:
    exact_index = text.find(pattern)
    if exact_index >= 0:
        return exact_index
    return text.lower().find(pattern.lower())


def _raw_excerpt_fragment(text: str, index: int, pattern_length: int, *, leading_radius: int = 40, trailing_radius: int = 180) -> str:
    return text[max(0, index - leading_radius) : index + pattern_length + trailing_radius].strip()


def _compact_excerpt(text: str) -> str:
    return " ".join(text.split())


def _is_forbidden_field_name(key: str) -> bool:
    return is_forbidden_field_token_match(key, _FORBIDDEN_SOURCE_VISIBLE_FIELD_NAMES)


__all__ = [
    "LUCKYSCENT_PDP_CONTENT_PROFILE",
    "LUCKYSCENT_PDP_CONTENT_RECORD_KIND",
    "LUCKYSCENT_PDP_CONTENT_SCHEMA_VERSION",
    "LUCKYSCENT_PDP_PARSER_VERSION",
    "NORDSTROM_PDP_CONTENT_PROFILE",
    "NORDSTROM_PDP_CONTENT_RECORD_KIND",
    "NORDSTROM_PDP_CONTENT_SCHEMA_VERSION",
    "NORDSTROM_PDP_PARSER_VERSION",
    "RETAIL_PDP_PROJECTION_CERTIFICATION",
    "RETAIL_PDP_PROJECTION_METHOD",
    "RETAIL_PDP_PROJECTION_VERSION",
    "SEPHORA_PDP_CONTENT_PROFILE",
    "SEPHORA_PDP_CONTENT_RECORD_KIND",
    "SEPHORA_PDP_CONTENT_SCHEMA_VERSION",
    "SEPHORA_PDP_PARSER_VERSION",
    "PROJECTION_RETAIL_PDP_LANE",
    "Retailer",
    "RetailPdpProjectionInputError",
    "RetailPdpProjectionBinding",
    "RetailPdpProjectionLossEntry",
    "RetailPdpProjectionLossLedger",
    "RetailPdpProjectionPacket",
    "RetailPdpProjectionRow",
    "RetailProjectionRawAnchor",
    "RetailProjectionRawRef",
    "LuckyscentPdpAggregateContentRecord",
    "SephoraPdpAggregateContentRecord",
    "build_luckyscent_pdp_aggregate_content_record",
    "NordstromPdpAggregateContentRecord",
    "SephoraPdpAggregateContentRecord",
    "build_nordstrom_pdp_aggregate_content_record",
    "build_retail_pdp_projection",
    "build_retail_pdp_projection_from_packet_directory",
    "build_sephora_pdp_aggregate_content_record",
    "project_retail_pdp_into_lake",
    "write_retail_pdp_projection",
]
