from __future__ import annotations

import hashlib
import html as html_lib
import json
import re
from html import unescape
from pathlib import Path
from types import SimpleNamespace
from typing import TYPE_CHECKING, Any, Literal, Mapping, Sequence
from urllib.parse import parse_qs, urlparse

from pydantic import Field, field_validator, model_validator

from harness_utils import generate_ulid
from schemas.case_models import StrictModel
from source_capture.models import PreservedFile, SourceCapturePacket, SourceCaptureSlice, VisibleFactStatus
from source_capture.projection_shared import is_forbidden_field_token_match

if TYPE_CHECKING:
    from data_lake.root import DataLakeRoot


RETAIL_PDP_PROJECTION_METHOD = "retail_pdp_mechanical_projection"
RETAIL_PDP_PROJECTION_VERSION = "v1"
RETAIL_PDP_PROJECTION_CERTIFICATION = "view_only; not_cleaned; not_normalized; not_judgment_ready"
SEPHORA_PDP_CONTENT_RECORD_KIND = "retail_pdp_sephora_aggregate_content"
SEPHORA_PDP_CONTENT_SCHEMA_VERSION = "retail_pdp_sephora_aggregate_content_v2"
SEPHORA_PDP_PARSER_VERSION = "retail_pdp_sephora_aggregate_parser_v2"
SEPHORA_PDP_CONTENT_PROFILE = "sephora_pdp_aggregate"
LUCKYSCENT_PDP_CONTENT_RECORD_KIND = "retail_pdp_luckyscent_aggregate_content"
LUCKYSCENT_PDP_CONTENT_SCHEMA_VERSION = "retail_pdp_luckyscent_aggregate_content_v1"
LUCKYSCENT_PDP_PARSER_VERSION = "retail_pdp_luckyscent_aggregate_parser_v1"
LUCKYSCENT_PDP_CONTENT_PROFILE = "luckyscent_pdp_aggregate"
NORDSTROM_PDP_CONTENT_RECORD_KIND = "retail_pdp_nordstrom_aggregate_content"
NORDSTROM_PDP_CONTENT_SCHEMA_VERSION = "retail_pdp_nordstrom_aggregate_content_v2"
NORDSTROM_PDP_PARSER_VERSION = "retail_pdp_nordstrom_aggregate_parser_v5"
NORDSTROM_PDP_CONTENT_PROFILE = "nordstrom_pdp_aggregate"
ULTA_PDP_CONTENT_RECORD_KIND = "retail_pdp_ulta_aggregate_content"
ULTA_PDP_CONTENT_SCHEMA_VERSION = "retail_pdp_ulta_aggregate_content_v1"
ULTA_PDP_PARSER_VERSION = "retail_pdp_ulta_aggregate_parser_v1"
ULTA_PDP_CONTENT_PROFILE = "ulta_pdp_aggregate"

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
    category: Literal[
        "RETAIL_HERO_IMAGERY_COLLAPSED",
        "RETAIL_CART_NOTIFY_STATE_COLLAPSED",
        "RETAIL_NAVIGATION_FOOTER_PROMOTION_COLLAPSED",
        "RETAIL_SCRIPT_STYLE_TELEMETRY_COLLAPSED",
        "RETAIL_RECOMMENDATION_CAROUSEL_COLLAPSED",
        "RETAIL_GALLERY_COMMUNITY_MEDIA_COLLAPSED",
        "RETAIL_FLEXIBLE_PAYMENT_CHROME_COLLAPSED",
    ]
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
    projection_version: Literal["v1"] = RETAIL_PDP_PROJECTION_VERSION
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
    category: Literal[
        "RETAIL_HERO_IMAGERY_COLLAPSED",
        "RETAIL_CART_NOTIFY_STATE_COLLAPSED",
        "RETAIL_NAVIGATION_FOOTER_PROMOTION_COLLAPSED",
        "RETAIL_SCRIPT_STYLE_TELEMETRY_COLLAPSED",
        "RETAIL_RECOMMENDATION_CAROUSEL_COLLAPSED",
        "RETAIL_GALLERY_COMMUNITY_MEDIA_COLLAPSED",
        "RETAIL_FLEXIBLE_PAYMENT_CHROME_COLLAPSED",
    ]
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
    schema_version: Literal[
        "retail_pdp_sephora_aggregate_content_v1",
        "retail_pdp_sephora_aggregate_content_v2",
    ] = (
        SEPHORA_PDP_CONTENT_SCHEMA_VERSION
    )
    parser_version: Literal[
        "retail_pdp_sephora_aggregate_parser_v1",
        "retail_pdp_sephora_aggregate_parser_v2",
    ] = (
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
        expected_pair = {
            "retail_pdp_sephora_aggregate_content_v1": "retail_pdp_sephora_aggregate_parser_v1",
            "retail_pdp_sephora_aggregate_content_v2": "retail_pdp_sephora_aggregate_parser_v2",
        }
        if expected_pair[self.schema_version] != self.parser_version:
            raise ValueError("Sephora content schema and parser versions must match")
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
        "RETAIL_HERO_IMAGERY_COLLAPSED",
        "RETAIL_CART_NOTIFY_STATE_COLLAPSED",
        "RETAIL_MEDIA_BINARY_NOT_PRESERVED",
        "RETAIL_REVIEW_DEFAULT_VIEW_NOT_SEPARATELY_RETAINED",
        "RETAIL_REVIEW_INCENTIVE_FILTER_NOT_EXPOSED",
        "RETAIL_REVIEW_DEMOGRAPHICS_NOT_EXPOSED",
        "RETAIL_REVIEW_FIELDS_NOT_EXPOSED",
        "RETAIL_AI_SENTIMENT_NOT_EXPOSED",
        "RETAIL_QA_NOT_EXPOSED",
        "RETAIL_VARIANT_MERCHANDISING_FLAGS_NOT_EXPOSED",
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
    omitted_or_not_exposed: list[NordstromPdpContentLossEntry] = Field(
        default_factory=list
    )
    preserved_evidence_rows: int = Field(ge=0)
    preserved_bindings: int = Field(ge=0)
    timing: Literal["separate_not_collapsed"] = "separate_not_collapsed"
    hierarchy_preserved: bool
    structure_preserved: bool
    certification: Literal[
        "collapses_only_logged_frame_conditional_pdp_envelope; does_not_certify_cleaning",
        "explicitly_logs_source_visible_omissions_and_not_exposed_surfaces; does_not_certify_cleaning",
    ] = (
        "explicitly_logs_source_visible_omissions_and_not_exposed_surfaces; "
        "does_not_certify_cleaning"
    )


class NordstromPdpAggregateContentRecord(StrictModel):
    record_kind: Literal["retail_pdp_nordstrom_aggregate_content"] = (
        NORDSTROM_PDP_CONTENT_RECORD_KIND
    )
    schema_version: Literal[
        "retail_pdp_nordstrom_aggregate_content_v1",
        "retail_pdp_nordstrom_aggregate_content_v2",
    ] = (
        NORDSTROM_PDP_CONTENT_SCHEMA_VERSION
    )
    parser_version: Literal[
        "retail_pdp_nordstrom_aggregate_parser_v1",
        "retail_pdp_nordstrom_aggregate_parser_v2",
        "retail_pdp_nordstrom_aggregate_parser_v3",
        "retail_pdp_nordstrom_aggregate_parser_v4",
        "retail_pdp_nordstrom_aggregate_parser_v5",
    ] = NORDSTROM_PDP_PARSER_VERSION
    capture_profile: Literal["nordstrom_pdp_aggregate"] = (
        NORDSTROM_PDP_CONTENT_PROFILE
    )
    source_url: str
    rows: list[NordstromPdpContentRow] = Field(default_factory=list)
    binding_map: list[NordstromPdpContentBinding] = Field(default_factory=list)
    loss_ledger: NordstromPdpContentLossLedger
    information_extraction_coverage: dict[str, Any] = Field(default_factory=dict)
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
        if (
            self.parser_version
            in {
                "retail_pdp_nordstrom_aggregate_parser_v4",
                "retail_pdp_nordstrom_aggregate_parser_v5",
            }
            and not self.information_extraction_coverage
        ):
            raise ValueError(
                "Nordstrom parser v4+ requires information_extraction_coverage"
            )
        return self


UltaContentAnchorKind = Literal[
    "file", "html_selector", "script_index", "text_pattern"
]


class UltaPdpContentRow(StrictModel):
    slice_id: str
    row_id: str
    row_kind: Literal[
        "retail_pdp_product",
        "retail_variant_offer",
        "retail_review_substrate",
        "retail_carried_module",
    ]
    retailer: Literal["ulta"] = "ulta"
    source_visible_fields: dict[str, Any | None] = Field(default_factory=dict)
    residuals: list[str] = Field(default_factory=list)
    source_anchor_kind: UltaContentAnchorKind
    source_anchor_value: str | None = None

    @field_validator("source_visible_fields")
    @classmethod
    def reject_judgment_field_names(
        cls, value: dict[str, Any | None]
    ) -> dict[str, Any | None]:
        forbidden = sorted(key for key in value if _is_forbidden_field_name(key))
        if forbidden:
            raise ValueError(
                "Ulta PDP content source_visible_fields may carry raw facts only; "
                f"forbidden Judgment field(s): {', '.join(forbidden)}"
            )
        return value

    @model_validator(mode="after")
    def validate_source_anchor(self) -> "UltaPdpContentRow":
        if self.source_anchor_kind == "file":
            if self.source_anchor_value is not None:
                raise ValueError("file anchors must not carry source_anchor_value")
            return self
        if not (self.source_anchor_value and self.source_anchor_value.strip()):
            raise ValueError(
                f"{self.source_anchor_kind} anchors require source_anchor_value"
            )
        return self


class UltaPdpAggregateContentRecord(StrictModel):
    """Lean canonical content; loader envelopes remain represented by input hashes."""

    record_kind: Literal["retail_pdp_ulta_aggregate_content"] = (
        ULTA_PDP_CONTENT_RECORD_KIND
    )
    schema_version: Literal["retail_pdp_ulta_aggregate_content_v1"] = (
        ULTA_PDP_CONTENT_SCHEMA_VERSION
    )
    parser_version: Literal["retail_pdp_ulta_aggregate_parser_v1"] = (
        ULTA_PDP_PARSER_VERSION
    )
    capture_profile: Literal["ulta_pdp_aggregate"] = ULTA_PDP_CONTENT_PROFILE
    source_url: str
    rows: list[UltaPdpContentRow] = Field(default_factory=list)
    residuals: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_required_rows(self) -> "UltaPdpAggregateContentRecord":
        counts = {
            kind: sum(row.row_kind == kind for row in self.rows)
            for kind in (
                "retail_pdp_product",
                "retail_variant_offer",
                "retail_review_substrate",
            )
        }
        if any(count != 1 for count in counts.values()):
            raise ValueError(
                "Ulta content record requires exactly one product, offer, and "
                "review-substrate row"
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
        content_payload = _content_record_payload(content_bytes)
        record_kind = content_payload.get("record_kind")
        if record_kind == SEPHORA_PDP_CONTENT_RECORD_KIND:
            _validate_sephora_content_packet_metadata(
                packet=packet,
                raw_file_bytes_by_file_id=raw_file_bytes_by_file_id,
                expected_parser_version=content_payload.get("parser_version"),
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
    html = _decode_text(rendered_dom)
    product_state = _extract_sephora_link_store_product(html)
    if product_state is None:
        raise ValueError(
            "Sephora aggregate content admission requires linkStore.page.product"
        )
    expected_product_id = _sephora_product_id_from_url(source_url)
    product_id = _string_or_none(product_state.get("productId"))
    if expected_product_id and product_id != expected_product_id:
        raise ValueError(
            "Sephora linkStore productId does not match the source URL product"
        )
    dom_fields = _sephora_dom_offer_fields(html)
    dom_sku = _string_or_none(dom_fields.get("dom_sku"))
    current_sku = product_state.get("currentSku")
    current_sku_id = (
        _string_or_none(current_sku.get("skuId"))
        if isinstance(current_sku, dict)
        else None
    )
    if not dom_sku or current_sku_id != dom_sku:
        raise ValueError(
            "Sephora selected DOM SKU does not match linkStore.page.product.currentSku"
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
        html,
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
            fields = {
                **_product_context_fields(packet, source_slice, "sephora"),
                **fields,
            }
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
        fields = {
            key: value
            for key, value in fields.items()
            if key
            not in {
                "retailer",
                "source_family",
                "source_surface",
                "source_locator",
                "slice_locator",
                "series_id",
                "locale_pin",
                "currency_pin",
                "variant_pin",
                "location_pin",
                "capture_time",
                "cutoff_posture",
                "archive_history_posture",
            }
        }
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
    expected_parser_version: object,
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

    try:
        capture_metadata = _one_json("content_extraction_metadata.json")
        metadata_is_current = True
    except ValueError:
        capture_metadata = _one_json("content_capture_metadata.json")
        metadata_is_current = False
    if expected_parser_version not in {
        "retail_pdp_sephora_aggregate_parser_v1",
        SEPHORA_PDP_PARSER_VERSION,
    }:
        raise ValueError("Sephora content packet parser version is unknown")
    version_key = "extractor_version" if metadata_is_current else "parser_version"
    if capture_metadata.get(version_key) != expected_parser_version:
        raise ValueError("Sephora content packet parser version does not match its record")
    if metadata_is_current:
        if capture_metadata.get("extraction_status") != "succeeded":
            raise ValueError("Sephora content packet extraction did not succeed")
        if capture_metadata.get("retention_outcome") != "content":
            raise ValueError("Sephora content packet must have content retention outcome")
    else:
        if capture_metadata.get("projection_status") != "succeeded":
            raise ValueError("legacy Sephora content packet projection did not succeed")
        if capture_metadata.get("capture_artifact_mode") not in {"content", "sample"}:
            raise ValueError("legacy Sephora content packet mode is invalid")

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

    try:
        capture_metadata = _one_json("content_extraction_metadata.json")
        metadata_is_current = True
    except ValueError:
        capture_metadata = _one_json("content_capture_metadata.json")
        metadata_is_current = False
    version_key = "extractor_version" if metadata_is_current else "parser_version"
    if capture_metadata.get(version_key) != LUCKYSCENT_PDP_PARSER_VERSION:
        raise ValueError("Luckyscent content packet parser version does not match current")
    if metadata_is_current:
        if capture_metadata.get("extraction_status") != "succeeded":
            raise ValueError("Luckyscent content packet extraction did not succeed")
        if capture_metadata.get("retention_outcome") != "content":
            raise ValueError("Luckyscent content packet must have content retention outcome")
    else:
        if capture_metadata.get("projection_status") != "succeeded":
            raise ValueError("legacy Luckyscent content packet projection did not succeed")
        if capture_metadata.get("capture_artifact_mode") not in {"content", "sample"}:
            raise ValueError("legacy Luckyscent content packet mode is invalid")

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


def build_ulta_pdp_aggregate_content_record(
    *,
    rendered_dom: bytes,
    visible_text: bytes,
    source_url: str,
) -> dict[str, Any]:
    """Retain target-bound Ulta facts without retaining its loader envelope."""
    if not isinstance(rendered_dom, bytes) or not isinstance(visible_text, bytes):
        raise TypeError("rendered_dom and visible_text must be bytes")
    requested_sku = _ulta_sku_from_source_url(source_url)
    if requested_sku is None:
        raise ValueError(
            "Ulta aggregate content records require an ulta.com PDP URL with "
            "exactly one numeric sku"
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
        variant_pin=SimpleNamespace(
            status=VisibleFactStatus.KNOWN,
            value=f"sku={requested_sku}",
        ),
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
        retailer="ulta",
    )
    if projected.residuals:
        raise ValueError(
            "Ulta aggregate content requires a residual-free target binding; "
            f"found: {', '.join(projected.residuals)}"
        )

    product_rows = [
        row for row in projected.rows if row.row_kind == "retail_pdp_product"
    ]
    offer_rows = [
        row for row in projected.rows if row.row_kind == "retail_variant_offer"
    ]
    review_rows = [
        row for row in projected.rows if row.row_kind == "retail_review_substrate"
    ]
    if not (
        len(product_rows) == len(offer_rows) == len(review_rows) == 1
    ):
        raise ValueError(
            "Ulta aggregate content requires exactly one product, offer, and "
            "review-substrate row"
        )
    offer = offer_rows[0].source_visible_fields
    review = review_rows[0].source_visible_fields
    if _string_or_none(offer.get("sku")) != requested_sku:
        raise ValueError("Ulta projected SKU does not match the requested URL")
    if _string_or_none(offer.get("price_currency")) != "USD":
        raise ValueError("Ulta projected offer does not carry USD")
    if not _string_or_none(offer.get("price")):
        raise ValueError("Ulta projected offer lacks target-bound price evidence")
    if not _string_or_none(offer.get("availability")):
        raise ValueError("Ulta projected offer lacks target-bound availability")
    if (
        not _string_or_none(review.get("rating"))
        or not _string_or_none(review.get("review_count"))
        or not _string_or_none(review.get("ld_json_rating"))
        or not _string_or_none(review.get("apollo_rating"))
    ):
        raise ValueError(
            "Ulta projected review substrate lacks agreeing JSON-LD/Apollo "
            "rating or count evidence"
        )

    product_document, breadcrumb_document = _ulta_target_documents(
        projected.rows, requested_sku=requested_sku
    )
    if product_document is None:
        raise ValueError("Ulta target Product JSON-LD was not retained by the parser")
    product_fields = _ulta_product_content_fields(
        product_document,
        breadcrumb_document=breadcrumb_document,
        source_url=source_url,
    )
    content_rows = [
        UltaPdpContentRow(
            slice_id=slice_id,
            row_id=product_rows[0].row_id,
            row_kind="retail_pdp_product",
            source_visible_fields=product_fields,
            residuals=product_rows[0].residuals,
            source_anchor_kind="script_index",
            source_anchor_value=f"ld_json Product sku={requested_sku}",
        ),
        _ulta_content_row(offer_rows[0]),
        _ulta_content_row(review_rows[0]),
        *[
            _ulta_content_row(row)
            for row in projected.rows
            if row.row_kind == "retail_carried_module"
        ],
    ]
    record = UltaPdpAggregateContentRecord(
        source_url=source_url,
        rows=content_rows,
        residuals=[],
    )
    return record.model_dump(mode="json")


def _ulta_content_row(row: RetailPdpProjectionRow) -> UltaPdpContentRow:
    return UltaPdpContentRow(
        slice_id=row.raw_ref.slice_id,
        row_id=row.row_id,
        row_kind=row.row_kind,
        retailer="ulta",
        source_visible_fields=dict(row.source_visible_fields),
        residuals=row.residuals,
        source_anchor_kind=row.raw_anchor.anchor_kind,
        source_anchor_value=row.raw_anchor.anchor_value,
    )


def _ulta_target_documents(
    rows: Sequence[RetailPdpProjectionRow],
    *,
    requested_sku: str,
) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    product: dict[str, Any] | None = None
    breadcrumb: dict[str, Any] | None = None
    for row in rows:
        if row.row_kind != "retail_embedded_structured_json":
            continue
        fields = row.source_visible_fields
        if fields.get("structured_json_kind") != "ld_json":
            continue
        raw = fields.get("raw_json_text")
        if not isinstance(raw, str):
            continue
        try:
            document = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if not isinstance(document, dict):
            continue
        document_type = document.get("@type")
        if (
            document_type == "Product"
            and _string_or_none(document.get("sku")) == requested_sku
        ):
            product = document
        elif document_type == "BreadcrumbList":
            breadcrumb = document
    return product, breadcrumb


def _ulta_product_content_fields(
    product: Mapping[str, object],
    *,
    breadcrumb_document: Mapping[str, object] | None,
    source_url: str,
) -> dict[str, Any | None]:
    brand_value = product.get("brand")
    brand = (
        _string_or_none(brand_value.get("name"))
        if isinstance(brand_value, Mapping)
        else _string_or_none(brand_value)
    )
    breadcrumb: list[str] = []
    if breadcrumb_document is not None:
        items = breadcrumb_document.get("itemListElement")
        if isinstance(items, list):
            for item in items:
                if not isinstance(item, Mapping):
                    continue
                nested = item.get("item")
                name = (
                    _string_or_none(nested.get("name"))
                    if isinstance(nested, Mapping)
                    else _string_or_none(item.get("name"))
                )
                if name:
                    breadcrumb.append(name)
    return {
        "product_id": _string_or_none(product.get("productID")),
        "sku": _string_or_none(product.get("sku")),
        "product_name": _string_or_none(product.get("name")),
        "brand": brand,
        "description": _string_or_none(product.get("description")),
        "scent": _string_or_none(product.get("scent")),
        "source_product_url": source_url,
        "breadcrumb": breadcrumb,
    }


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
    structured_state_rows = [
        row
        for row in projected.rows
        if row.row_kind == "retail_embedded_structured_json"
        and row.source_visible_fields.get("structured_json_kind")
        == "nordstrom_initial_product_state"
    ]
    if len(structured_state_rows) != 1:
        raise ValueError(
            "Nordstrom aggregate content requires one target-bound initial product state"
        )
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
    coverage = _nordstrom_information_extraction_coverage(
        html=_decode_text(rendered_dom),
        offer=offer,
        review=review,
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
            omitted_or_not_exposed=_nordstrom_standard_omissions(
                coverage=coverage,
                offer=offer,
                review=review,
            ),
            preserved_evidence_rows=len(projected.rows),
            preserved_bindings=len(projected.bindings),
            hierarchy_preserved=True,
            structure_preserved=_retail_structure_preserved(projected.bindings),
        ),
        information_extraction_coverage=coverage,
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

    try:
        capture_metadata = _one_json("content_extraction_metadata.json")
        metadata_is_current = True
    except ValueError:
        capture_metadata = _one_json("content_capture_metadata.json")
        metadata_is_current = False
    version_key = "extractor_version" if metadata_is_current else "parser_version"
    if capture_metadata.get(version_key) not in {
        "retail_pdp_nordstrom_aggregate_parser_v1",
        "retail_pdp_nordstrom_aggregate_parser_v2",
        NORDSTROM_PDP_PARSER_VERSION,
    }:
        raise ValueError(
            "Nordstrom content packet parser version is not a supported durable version"
        )
    if metadata_is_current:
        if capture_metadata.get("extraction_status") != "succeeded":
            raise ValueError("Nordstrom content packet extraction did not succeed")
        if capture_metadata.get("retention_outcome") != "content":
            raise ValueError("Nordstrom content packet must have content retention outcome")
    else:
        if capture_metadata.get("projection_status") != "succeeded":
            raise ValueError("legacy Nordstrom content packet projection did not succeed")
        if capture_metadata.get("capture_artifact_mode") not in {"content", "sample"}:
            raise ValueError("legacy Nordstrom content packet mode is invalid")

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


def _content_record_payload(content_bytes: bytes) -> dict[str, Any]:
    try:
        payload = json.loads(content_bytes)
    except Exception as exc:
        raise ValueError(f"invalid Retail PDP content record JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError("Retail PDP content record must contain a JSON object")
    return payload


class _ProjectedRetailHtml(StrictModel):
    rows: list[RetailPdpProjectionRow] = Field(default_factory=list)
    bindings: list[RetailPdpProjectionBinding] = Field(default_factory=list)
    collapsed: list[RetailPdpProjectionLossEntry] = Field(default_factory=list)
    residuals: list[str] = Field(default_factory=list)


class _StructuredJsonEntry(StrictModel):
    kind: Literal[
        "ld_json",
        "apollo_state",
        "next_data",
        "nordstrom_initial_product_state",
        "sephora_link_store_product",
        "sephora_rendered_interactions",
    ]
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
    if retailer == "sephora":
        structured_entries.extend(
            _sephora_full_derived_entries(html=html, raw_anchor=raw_anchor)
        )
        residuals.extend(
            [
                "sephora_exact_stock_quantity_not_observed",
                "sephora_sold_units_not_observed",
                "sephora_delivery_location_not_capture_pinned",
                "sephora_displayed_reviews_first_page_only",
                "sephora_displayed_qa_rendered_sample_only",
                "sephora_linked_review_media_not_independently_preserved",
            ]
        )
    if retailer == "nordstrom":
        nordstrom_product_state = _nordstrom_initial_product_state_entry(
            html=html,
            source_url=_fact_value(source_slice.locator)
            or _fact_value(packet.source_locator),
            raw_anchor=raw_anchor,
        )
        if nordstrom_product_state is not None:
            structured_entries.append(nordstrom_product_state)
        structured_entries = _nordstrom_target_structured_entries(
            structured_entries,
            source_url=_fact_value(source_slice.locator)
            or _fact_value(packet.source_locator),
        )
    product_row_id = f"{source_slice.slice_id}:{retailer}:pdp"
    product_fields = _product_context_fields(packet, source_slice, retailer)
    if retailer == "sephora":
        product_fields["rendered_visible_text"] = visible_text
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

    collapsed.extend(
        _collapse_entries(
            html=html,
            visible_text=visible_text,
            raw_anchor=raw_anchor,
            retailer=retailer,
        )
    )
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


def _extract_sephora_link_store_product(html: str) -> dict[str, Any] | None:
    match = re.search(
        r"<script\b[^>]*\bid=[\"']linkStore[\"'][^>]*>([\s\S]*?)</script\s*>",
        html,
        flags=re.IGNORECASE,
    )
    if match is None:
        return None
    payload = _safe_json_loads(match.group(1).strip())
    if not isinstance(payload, dict):
        return None
    page = payload.get("page")
    if not isinstance(page, dict):
        return None
    product = page.get("product")
    return product if isinstance(product, dict) else None


def _sephora_full_derived_entries(
    *,
    html: str,
    raw_anchor: RetailProjectionRawAnchor,
) -> list[_StructuredJsonEntry]:
    entries: list[_StructuredJsonEntry] = []
    product = _extract_sephora_link_store_product(html)
    if product is not None:
        entries.append(
            _StructuredJsonEntry(
                kind="sephora_link_store_product",
                index=0,
                raw_text=json.dumps(
                    product,
                    ensure_ascii=False,
                    separators=(",", ":"),
                    sort_keys=True,
                ),
                parsed=product,
                raw_anchor=_with_anchor(
                    raw_anchor,
                    "script_index",
                    "linkStore#/page/product",
                ),
            )
        )

    interactions = {
        "displayed_reviews": _sephora_component_records(html, "Review"),
        "displayed_questions": _sephora_component_records(html, "Question"),
        "displayed_answers": _sephora_component_records(html, "Answer"),
    }
    if any(interactions.values()):
        entries.append(
            _StructuredJsonEntry(
                kind="sephora_rendered_interactions",
                index=0,
                raw_text=json.dumps(
                    interactions,
                    ensure_ascii=False,
                    separators=(",", ":"),
                    sort_keys=True,
                ),
                parsed=interactions,
                raw_anchor=_with_anchor(
                    raw_anchor,
                    "html_selector",
                    '[data-comp^="Review "], [data-comp^="Question "], [data-comp^="Answer "]',
                ),
            )
        )
    return entries


def _sephora_component_records(html: str, component: str) -> list[dict[str, Any]]:
    fragments = _extract_balanced_div_fragments(
        html,
        rf'data-comp=["\']{re.escape(component)}(?:\s|["\'])',
    )
    records: list[dict[str, Any]] = []
    for index, fragment in enumerate(fragments):
        records.append(
            {
                "display_index": index,
                "raw_html": fragment,
                "visible_text": _clean_html_text(fragment),
                "rating": _first_regex(
                    fragment,
                    (r'aria-label=["\'](\d+(?:\.\d+)?) out of 5 stars',),
                ),
                "verified_purchaser": bool(
                    re.search(r"Verified Purchaser", fragment, flags=re.IGNORECASE)
                ),
                "incentivized": bool(
                    re.search(r"Incentivized", fragment, flags=re.IGNORECASE)
                ),
                "recommended": bool(
                    re.search(r"\bRecommended\b", fragment, flags=re.IGNORECASE)
                ),
                "media_urls": sorted(
                    set(
                        re.findall(
                            r'https?://[^"\'\s<>]+',
                            html_lib.unescape(fragment),
                            flags=re.IGNORECASE,
                        )
                    )
                ),
            }
        )
    return records


def _extract_balanced_div_fragments(html: str, attribute_pattern: str) -> list[str]:
    fragments: list[str] = []
    starts = list(
        re.finditer(
            rf"<div\b[^>]*{attribute_pattern}[^>]*>",
            html,
            flags=re.IGNORECASE,
        )
    )
    tag_pattern = re.compile(r"<div\b[^>]*>|</div\s*>", flags=re.IGNORECASE)
    for start in starts:
        depth = 1
        for tag in tag_pattern.finditer(html, start.end()):
            depth += -1 if tag.group(0).lower().startswith("</div") else 1
            if depth == 0:
                fragments.append(html[start.start() : tag.end()])
                break
    return fragments


def _sephora_product_state(
    structured_entries: Sequence[_StructuredJsonEntry],
) -> dict[str, Any] | None:
    for entry in structured_entries:
        if (
            entry.kind == "sephora_link_store_product"
            and isinstance(entry.parsed, dict)
        ):
            return entry.parsed
    return None


def _sephora_product_id_from_url(source_url: str) -> str | None:
    match = re.search(r"(?:^|-)P(\d+)(?:$|[/?#])", source_url, flags=re.IGNORECASE)
    return f"P{match.group(1)}" if match else None


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
    apollo_fields, apollo_anchor = (
        _ulta_apollo_offer_fields(
            structured_entries,
            preferred_sku=_sku_from_variant_pin(
                _fact_value(source_slice.variant_pin)
            ),
        )
        if retailer == "ulta"
        else ({}, None)
    )
    if retailer == "ulta" and not apollo_fields and _ulta_apollo_offer_substrate_present(structured_entries):
        residuals.append(f"{source_slice.slice_id}:ulta:variant_offer_substrate_present_but_unextracted")
    if retailer == "sephora" and selected_sku and not structured_fields:
        substrate_skus = _sephora_structured_offer_substrate_skus(structured_entries)
        if substrate_skus and selected_sku not in substrate_skus:
            residuals.append("sephora_selected_sku_absent_from_structured_variants")
    if sephora_dom_fields:
        product_state = _sephora_product_state(structured_entries)
        current_sku = (
            product_state.get("currentSku")
            if isinstance(product_state, dict)
            else None
        )
        child_skus = (
            product_state.get("regularChildSkus")
            if isinstance(product_state, dict)
            else None
        )
        structured_fields = {
            **structured_fields,
            "product_id": _string_or_none(sephora_dom_fields.get("dom_product_id"))
            or structured_fields.get("product_id"),
            "sku": selected_sku or structured_fields.get("sku"),
            **sephora_dom_fields,
            "selected_sku": selected_sku,
            "selection_binding_source": "sephora_dom_product_page",
            "selected_variant_state": current_sku,
            "all_variant_states": child_skus if isinstance(child_skus, list) else [],
            "variant_count": len(child_skus) if isinstance(child_skus, list) else None,
            "product_details_state": (
                product_state.get("productDetails")
                if isinstance(product_state, dict)
                else None
            ),
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
        fields, residuals = _ulta_review_fields(
            structured_entries,
            requested_sku=_ulta_sku_from_source_url(source_url or ""),
        )
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
    if len(structured_rows) not in {1, 2}:
        raise ValueError(
            "Luckyscent content projection requires one or two target "
            "structured-JSON rows"
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


def _nordstrom_initial_product_state_entry(
    *,
    html: str,
    source_url: str | None,
    raw_anchor: RetailProjectionRawAnchor,
) -> _StructuredJsonEntry | None:
    """Retain only the requested public product subtree from initial page state."""
    product_id = _nordstrom_product_id_from_url(source_url)
    if product_id is None:
        return None
    marker = re.search(r"window\.__INITIAL_CONFIG__\s*=\s*", html)
    if marker is None:
        return None
    try:
        initial_config, _end = json.JSONDecoder().raw_decode(html[marker.end() :])
    except (TypeError, ValueError):
        return None
    if not isinstance(initial_config, dict):
        return None
    product_display = initial_config.get("productDisplay")
    if not isinstance(product_display, dict):
        return None
    displays = product_display.get("productDisplaysById")
    if not isinstance(displays, dict):
        return None
    entities = displays.get("entities")
    if not isinstance(entities, dict):
        return None
    product = entities.get(product_id)
    if not isinstance(product, dict) or _string_or_none(product.get("id")) != product_id:
        return None
    interactions = product_display.get("interactions")
    selection: object = None
    if isinstance(interactions, dict):
        interaction = interactions.get(f"product-page::{product_id}")
        if isinstance(interaction, dict):
            candidate = interaction.get("selections")
            if isinstance(candidate, dict):
                selection = candidate
    target_state = {
        "product_id": product_id,
        "product_display": product,
        "selected_options": selection,
    }
    return _StructuredJsonEntry(
        kind="nordstrom_initial_product_state",
        index=0,
        raw_text=json.dumps(
            target_state,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ),
        parsed=target_state,
        raw_anchor=_with_anchor(
            raw_anchor,
            "script_index",
            f"window.__INITIAL_CONFIG__#/productDisplay/productDisplaysById/entities/{product_id}",
        ),
    )


def _nordstrom_information_extraction_coverage(
    *,
    html: str,
    offer: Mapping[str, Any],
    review: Mapping[str, Any],
) -> dict[str, Any]:
    review_start = html.find('id="product-page-reviews"')
    review_html = html[review_start:] if review_start >= 0 else ""
    ai_sentiment_exposed = bool(
        re.search(
            r"AI[- ]generated|artificial intelligence|customers often note|"
            r"review sentiment|review summary",
            review_html,
            flags=re.IGNORECASE,
        )
    )
    qa_exposed = bool(
        re.search(
            r'id=["\']product-page-(?:questions|qa)["\']|'
            r">\s*(?:Questions\s*&\s*Answers|Customer Questions)\s*<",
            html,
            flags=re.IGNORECASE,
        )
    )
    review_exposure = review.get("review_field_exposure")
    review_exposure_map = (
        review_exposure if isinstance(review_exposure, Mapping) else {}
    )
    unsupported_review_card_fields = review.get("unsupported_review_card_fields")
    if (
        isinstance(unsupported_review_card_fields, list)
        and unsupported_review_card_fields
    ):
        raise ValueError(
            "Nordstrom review-card fields became source-visible but have no "
            f"lossless parser: {', '.join(unsupported_review_card_fields)}; "
            "raw fallback required"
        )
    for label, exposed in (
        (
            "Nordstrom incentive-review controls",
            review_exposure_map.get("incentive_filter") == "exposed",
        ),
        (
            "Nordstrom reviewer-demographic controls",
            review_exposure_map.get("reviewer_demographics") == "exposed",
        ),
        ("Nordstrom AI review sentiment", ai_sentiment_exposed),
        ("Nordstrom product Q&A", qa_exposed),
    ):
        if exposed:
            raise ValueError(
                f"{label} became source-visible but has no lossless v4 parser; "
                "raw fallback required"
            )
    variants = offer.get("variants")
    media = offer.get("media")
    rendered_reviews = review.get("rendered_reviews")
    return {
        "target_identity": {
            "status": "retained",
            "product_id": offer.get("product_id"),
            "sku": offer.get("sku"),
            "item_number": offer.get("item_number"),
            "core_product_id": offer.get("core_product_id"),
            "breadcrumbs": offer.get("breadcrumbs"),
        },
        "product_and_variants": {
            "status": "exact_target_product_state_and_flattened_inventory_retained",
            "variant_count": len(variants) if isinstance(variants, list) else 0,
            "out_of_stock_variant_count": offer.get("out_of_stock_variant_count"),
            "raw_field_path_count": len(
                offer.get("product_state_raw_field_inventory", [])
            ),
            "merchandising_flag_observation": offer.get(
                "variant_merchandising_flag_observation"
            ),
        },
        "media": {
            "status": "references_and_metadata_retained_binary_not_fetched",
            "reference_count": len(media) if isinstance(media, list) else 0,
        },
        "reviews": {
            "status": "bounded_most_recent_rows_and_most_helpful_pair_retained",
            "aggregate_review_count": review.get("review_count"),
            "captured_review_body_count": (
                len(rendered_reviews) if isinstance(rendered_reviews, list) else 0
            ),
            "most_helpful_review_pair_count": review.get(
                "most_helpful_review_pair_count"
            ),
            "sort_posture": review.get("review_sort_posture"),
            "field_exposure": dict(review_exposure_map),
            "raw_review_field_inventory": review.get(
                "raw_review_field_inventory"
            ),
        },
        "ai_review_sentiment": {
            "status": "not_exposed_on_target_pdp",
            "chip_count": 0,
        },
        "questions_and_answers": {
            "status": "not_exposed_on_target_pdp",
            "aggregate_question_count": None,
            "captured_question_rows": 0,
            "captured_answer_rows": 0,
        },
    }


def _nordstrom_standard_omissions(
    *,
    coverage: Mapping[str, Any],
    offer: Mapping[str, Any],
    review: Mapping[str, Any],
) -> list[NordstromPdpContentLossEntry]:
    entries = [
        NordstromPdpContentLossEntry(
            category="RETAIL_REVIEW_DEFAULT_VIEW_NOT_SEPARATELY_RETAINED",
            count=1,
            reason=(
                "the interaction mutates the main review list to Most Recent before "
                "snapshot; the persistent most-helpful positive/critical pair is "
                "retained, but the initial main-list ordering is not separately retained"
            ),
            source_anchor_kind="file",
        ),
        NordstromPdpContentLossEntry(
            category="RETAIL_REVIEW_INCENTIVE_FILTER_NOT_EXPOSED",
            count=1,
            reason=(
                "the target review controls expose Verified Purchases but no "
                "non-incentivized filter or incentive disclosure vocabulary; captured "
                "reviews must not be described as non-incentivized"
            ),
            source_anchor_kind="file",
        ),
        NordstromPdpContentLossEntry(
            category="RETAIL_REVIEW_DEMOGRAPHICS_NOT_EXPOSED",
            count=1,
            reason=(
                "no reviewer age or other demographic filter vocabulary is exposed on "
                "the target review surface; no demographic breakdown is claimed"
            ),
            source_anchor_kind="file",
        ),
        NordstromPdpContentLossEntry(
            category="RETAIL_REVIEW_FIELDS_NOT_EXPOSED",
            count=4,
            reason=(
                "recommendation, unhelpful count, demographic declarations, and tag "
                "fields are not exposed in the rendered review cards"
            ),
            source_anchor_kind="file",
        ),
        NordstromPdpContentLossEntry(
            category="RETAIL_AI_SENTIMENT_NOT_EXPOSED",
            count=1,
            reason=(
                "no retailer AI review summary or positive/negative sentiment chips are "
                "exposed on the target PDP"
            ),
            source_anchor_kind="file",
        ),
        NordstromPdpContentLossEntry(
            category="RETAIL_QA_NOT_EXPOSED",
            count=1,
            reason=(
                "no product Q&A aggregate, question rows, answer rows, sort control, or "
                "continuation is exposed on the target PDP"
            ),
            source_anchor_kind="file",
        ),
        NordstromPdpContentLossEntry(
            category="RETAIL_VARIANT_MERCHANDISING_FLAGS_NOT_EXPOSED",
            count=4,
            reason=(
                "limited-edition, limited-time-offer, new, and back-in-stock flags are "
                "not present in the target product state; sold-out lists and salability "
                "remain retained exactly"
            ),
            source_anchor_kind="file",
        ),
    ]
    media = offer.get("media")
    media_count = len(media) if isinstance(media, list) else 0
    if media_count:
        entries.append(
            NordstromPdpContentLossEntry(
                category="RETAIL_MEDIA_BINARY_NOT_PRESERVED",
                count=media_count,
                reason=(
                    "source media URLs, ordering, variant binding, and metadata are "
                    "retained; linked image bytes are not independently fetched"
                ),
                source_anchor_kind="file",
            )
        )
    return entries


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
        if not isinstance(parsed, dict):
            continue
        if entry.kind == "nordstrom_initial_product_state":
            if _string_or_none(parsed.get("product_id")) == product_id:
                selected.append(entry)
            continue
        if parsed.get("@type") == "BreadcrumbList":
            selected.append(entry)
            continue
        if parsed.get("@type") != "Product":
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


def _nordstrom_product_state(
    entries: list[_StructuredJsonEntry],
) -> dict[str, Any] | None:
    for entry in entries:
        if entry.kind != "nordstrom_initial_product_state":
            continue
        if isinstance(entry.parsed, dict):
            return entry.parsed
    return None


def _raw_field_path_inventory(value: object) -> list[str]:
    paths: set[str] = set()

    def walk(item: object, prefix: str) -> None:
        if isinstance(item, Mapping):
            for raw_key, child in item.items():
                key = str(raw_key)
                path = f"{prefix}.{key}" if prefix else key
                paths.add(path)
                walk(child, path)
        elif isinstance(item, list):
            array_path = f"{prefix}[]" if prefix else "[]"
            paths.add(array_path)
            for child in item:
                walk(child, array_path)

    walk(value, "")
    return sorted(paths)


def _nordstrom_breadcrumb_inventory(
    entries: list[_StructuredJsonEntry],
) -> list[dict[str, Any]]:
    for entry in entries:
        parsed = entry.parsed
        if not isinstance(parsed, dict) or parsed.get("@type") != "BreadcrumbList":
            continue
        rows = parsed.get("itemListElement")
        if not isinstance(rows, list):
            continue
        return [dict(row) for row in rows if isinstance(row, Mapping)]
    return []


def _nordstrom_variant_inventory(
    product_state: Mapping[str, Any],
) -> list[dict[str, Any]]:
    product = product_state.get("product_display")
    if not isinstance(product, Mapping):
        return []
    selected_options = product_state.get("selected_options")
    selected = selected_options if isinstance(selected_options, Mapping) else {}
    aggregate_propositions = product.get("propositions")
    aggregate_rows = (
        [row for row in aggregate_propositions if isinstance(row, Mapping)]
        if isinstance(aggregate_propositions, list)
        else []
    )
    sold_out_skus = {
        str(value)
        for proposition in aggregate_rows
        for selection in (
            proposition.get("coreChoiceSelections")
            if isinstance(proposition.get("coreChoiceSelections"), list)
            else []
        )
        if isinstance(selection, Mapping)
        for value in (
            selection.get("soldOutSkus")
            if isinstance(selection.get("soldOutSkus"), list)
            else []
        )
    }
    core_products = product.get("coreProducts")
    if not isinstance(core_products, list):
        return []
    variants: list[dict[str, Any]] = []
    for core_product_index, core_product in enumerate(core_products):
        if not isinstance(core_product, Mapping):
            continue
        choices = core_product.get("coreChoices")
        if not isinstance(choices, list):
            continue
        for choice_index, choice in enumerate(choices):
            if not isinstance(choice, Mapping):
                continue
            items = choice.get("items")
            if not isinstance(items, list):
                continue
            for item_index, item in enumerate(items):
                if not isinstance(item, Mapping):
                    continue
                sku = item.get("sku")
                sku_map = sku if isinstance(sku, Mapping) else {}
                sku_id = _string_or_none(sku_map.get("skuId"))
                propositions = sku_map.get("propositions")
                proposition_rows = (
                    [row for row in propositions if isinstance(row, Mapping)]
                    if isinstance(propositions, list)
                    else []
                )
                primary = proposition_rows[0] if proposition_rows else {}
                salability = primary.get("salability")
                salability_map = (
                    salability if isinstance(salability, Mapping) else {}
                )
                availability = primary.get("availability")
                availability_map = (
                    availability if isinstance(availability, Mapping) else {}
                )
                status = _string_or_none(salability_map.get("status"))
                explicitly_unavailable = availability_map.get("isAvailable") is False
                out_of_stock = (
                    sku_id in sold_out_skus
                    or explicitly_unavailable
                    or (status is not None and status != "SELLABLE")
                )
                size = item.get("sizeDimension1")
                size_map = size if isinstance(size, Mapping) else {}
                choice_id = _string_or_none(choice.get("coreChoiceId"))
                size_label = _string_or_none(size_map.get("label"))
                variants.append(
                    {
                        "source_order": len(variants) + 1,
                        "core_product_index": core_product_index,
                        "core_choice_index": choice_index,
                        "item_index": item_index,
                        "core_product_id": _string_or_none(
                            core_product.get("coreProductId")
                        ),
                        "core_choice_id": choice_id,
                        "display_color_description": _string_or_none(
                            choice.get("displayColorDescription")
                        ),
                        "color_family": choice.get("colorFamily"),
                        "npin": _string_or_none(item.get("npin")),
                        "sku_id": sku_id,
                        "size": size,
                        "display_size": _string_or_none(
                            item.get("concatenatedDisplaySize")
                        ),
                        "upcs": item.get("upcs"),
                        "age": item.get("age"),
                        "skin_types": item.get("skinTypes"),
                        "product_set_ids": item.get("productSetIds"),
                        "propositions": proposition_rows,
                        "selected": (
                            choice_id is not None
                            and choice_id == _string_or_none(selected.get("coreChoice"))
                            and (
                                _string_or_none(selected.get("size")) is None
                                or size_label
                                == _string_or_none(selected.get("size"))
                            )
                        ),
                        "out_of_stock": out_of_stock,
                        "limited_edition": None,
                        "limited_time_offer": None,
                        "new": None,
                        "back_in_stock": None,
                    }
                )
    return variants


def _nordstrom_media_inventory(
    product_state: Mapping[str, Any],
) -> list[dict[str, Any]]:
    product = product_state.get("product_display")
    if not isinstance(product, Mapping):
        return []
    core_products = product.get("coreProducts")
    if not isinstance(core_products, list):
        return []
    media: list[dict[str, Any]] = []
    for core_product in core_products:
        if not isinstance(core_product, Mapping):
            continue
        core_product_id = _string_or_none(core_product.get("coreProductId"))
        for source_name in ("editorialShots",):
            shots = core_product.get(source_name)
            if isinstance(shots, list):
                for shot in shots:
                    if isinstance(shot, Mapping):
                        media.append(
                            {
                                "source_order": len(media) + 1,
                                "source": source_name,
                                "core_product_id": core_product_id,
                                "core_choice_id": None,
                                "shot": dict(shot),
                            }
                        )
        choices = core_product.get("coreChoices")
        if not isinstance(choices, list):
            continue
        for choice in choices:
            if not isinstance(choice, Mapping):
                continue
            shots = choice.get("orderedShots")
            if not isinstance(shots, list):
                continue
            for shot in shots:
                if isinstance(shot, Mapping):
                    media.append(
                        {
                            "source_order": len(media) + 1,
                            "source": "orderedShots",
                            "core_product_id": core_product_id,
                            "core_choice_id": _string_or_none(
                                choice.get("coreChoiceId")
                            ),
                            "shot": dict(shot),
                        }
                    )
    return media


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
    product_state = _nordstrom_product_state(structured_entries)
    if product_state is None:
        return {}, ["nordstrom_target_initial_product_state_absent"]
    product_display = product_state.get("product_display")
    if not isinstance(product_display, Mapping):
        return {}, ["nordstrom_target_initial_product_display_absent"]
    variants = _nordstrom_variant_inventory(product_state)
    if not variants:
        return {}, ["nordstrom_target_variant_inventory_absent"]
    media = _nordstrom_media_inventory(product_state)
    selected_variants = [row for row in variants if row.get("selected") is True]
    selected_variant = selected_variants[0] if len(selected_variants) == 1 else variants[0]
    propositions = selected_variant.get("propositions")
    selected_proposition = (
        propositions[0]
        if isinstance(propositions, list)
        and propositions
        and isinstance(propositions[0], Mapping)
        else {}
    )
    structured_availability = selected_proposition.get("availability")
    availability_map = (
        structured_availability
        if isinstance(structured_availability, Mapping)
        else {}
    )
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
    variant_name = _string_or_none(selected_variant.get("display_size")) or _first_regex(
        main_text, (r"(One Size)",)
    )
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
        "sku": _string_or_none(selected_variant.get("sku_id")),
        "item_number": item_number,
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
        "structured_salability": selected_proposition.get("salability"),
        "structured_availability": structured_availability,
        "seller": seller,
        "shipping_destination_display": (
            f"Shipping to {shipping_destination}" if shipping_destination else None
        ),
        "shipping_availability": availability_map.get("isShipAvailable"),
        "pickup_availability": _first_literal(
            main_text, ("No stores found near your location", "Pickup at choose store")
        ),
        "delivery_availability": availability_map.get("isAvailable"),
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
        "exact_inventory_quantity": {
            key: availability_map.get(key)
            for key in ("shipQuantity", "marketPickQuantity", "pickQuantity")
        },
        "sold_units": "not_observed",
        "variant_count": len(variants),
        "out_of_stock_variant_count": sum(
            row.get("out_of_stock") is True for row in variants
        ),
        "variants": variants,
        "selected_options": product_state.get("selected_options"),
        "media": media,
        "media_reference_count": len(media),
        "breadcrumbs": _nordstrom_breadcrumb_inventory(structured_entries),
        "product_features": product_display.get("copyFeatures"),
        "product_state_raw_field_inventory": _raw_field_path_inventory(
            product_state
        ),
        "variant_merchandising_flag_observation": {
            "limited_edition": "not_exposed_in_target_product_state",
            "limited_time_offer": "not_exposed_in_target_product_state",
            "new": "not_exposed_in_target_product_state",
            "back_in_stock": "not_exposed_in_target_product_state",
        },
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
    rendered_reviews = _nordstrom_rendered_review_inventory(review_html)
    unsupported_review_card_fields = _nordstrom_unsupported_review_card_fields(
        review_html
    )

    highlighted_reviews = {
        kind: _nordstrom_highlighted_review(review_html, kind=kind)
        for kind in ("positive", "critical")
    }
    review_text = _bounded_text_section(
        visible_text, start="Reviews", end="Recommended for You"
    )
    review_sort_posture = _first_regex(
        review_html,
        (
            r'id=["\']sort-by-filter-[^"\']+-anchor["\'][\s\S]{0,500}?'
            r"Sort by\s*<strong>\s*([^<]+?)\s*</strong>",
        ),
    )
    review_load_more_control_text = _first_regex(
        review_html,
        (
            r'<a\b[^>]*href=["\']\?page=\d+["\'][^>]*>\s*'
            r"(Load\s+[\d,]+\s+more reviews)\s*</a>",
        ),
    )
    review_load_more_batch_size_text = _first_regex(
        review_load_more_control_text or "",
        (r"Load\s+([\d,]+)\s+more reviews",),
    )
    review_load_more_batch_size = (
        int(review_load_more_batch_size_text.replace(",", ""))
        if review_load_more_batch_size_text
        else None
    )
    filter_end = review_html.find('id="reviews-container"')
    filter_html = review_html[:filter_end] if filter_end >= 0 else review_html
    incentive_filter_exposed = bool(
        re.search(
            r"incentivized|free product|sweepstakes",
            filter_html,
            flags=re.IGNORECASE,
        )
    )
    demographic_filter_exposed = bool(
        re.search(
            r"age range|reviewer age|skin type|age-group",
            filter_html,
            flags=re.IGNORECASE,
        )
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
    if any(value is None for value in highlighted_reviews.values()):
        residuals.append("nordstrom_most_helpful_review_pair_incomplete")

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
                "nordstrom_target_product_json_ld_rendered_review_microdata_and_"
                "highlighted_review_cards"
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
            "review_sort_posture": review_sort_posture,
            "rendered_review_count": len(rendered_reviews),
            "rendered_reviews": rendered_reviews,
            "unsupported_review_card_fields": unsupported_review_card_fields,
            "raw_review_field_inventory": sorted(
                {
                    field_name
                    for row in rendered_reviews
                    for field_name in row.get("raw_field_names", [])
                }
            ),
            "review_field_exposure": {
                "unfiltered_initial_view": "not_separately_retained",
                "most_recent_view": (
                    "retained" if review_sort_posture == "Most Recent" else "not_observed"
                ),
                "most_helpful_snapshot": (
                    "positive_and_critical_pair_retained"
                    if all(value is not None for value in highlighted_reviews.values())
                    else "incomplete"
                ),
                "incentive_filter": (
                    "exposed" if incentive_filter_exposed else "not_exposed"
                ),
                "reviewer_demographics": (
                    "exposed" if demographic_filter_exposed else "not_exposed"
                ),
                "recommendation": "not_exposed_in_rendered_review_cards",
                "unhelpful_count": "not_exposed_in_rendered_review_cards",
                "variant": (
                    "retained"
                    if any(row.get("reviewed_variant") for row in rendered_reviews)
                    else "not_exposed_in_rendered_review_cards"
                ),
                "review_media": (
                    "retained_as_references"
                    if any(row.get("media_urls") for row in rendered_reviews)
                    else "not_exposed_in_rendered_review_cards"
                ),
                "tags": "not_exposed_in_rendered_review_cards",
            },
            "most_helpful_positive_review": highlighted_reviews["positive"],
            "most_helpful_critical_review": highlighted_reviews["critical"],
            "most_helpful_review_pair_count": sum(
                value is not None for value in highlighted_reviews.values()
            ),
            "review_load_more_control_text": review_load_more_control_text,
            "review_load_more_batch_size": review_load_more_batch_size,
            "review_continuation_available": (
                review_load_more_control_text is not None
            ),
        },
        residuals,
    )


def _nordstrom_rendered_review_inventory(
    review_html: str,
) -> list[dict[str, Any]]:
    microdata_pattern = re.compile(
        r'itemprop=["\']review["\'][\s\S]*?'
        r'itemprop=["\']name["\']\s+content=["\'](?P<title>[^"\']*)["\'][\s\S]*?'
        r'itemprop=["\']author["\']\s+content=["\'](?P<author>[^"\']*)["\'][\s\S]*?'
        r'itemprop=["\']datePublished["\']\s+content=["\'](?P<date>[^"\']*)["\'][\s\S]*?'
        r'itemprop=["\']ratingValue["\']\s+content=["\'](?P<rating>[^"\']*)["\'][\s\S]*?'
        r'itemprop=["\']reviewBody["\']\s+content=["\'](?P<body>[^"\']*)["\']',
        flags=re.IGNORECASE,
    )
    microdata_rows = list(microdata_pattern.finditer(review_html))
    starts = list(
        re.finditer(
            r'<div\b[^>]*\bid=["\']review-(\d+)["\'][^>]*>',
            review_html,
            flags=re.IGNORECASE,
        )
    )
    if len(microdata_rows) != len(starts):
        return []
    reviews: list[dict[str, Any]] = []
    for display_position, (start, microdata) in enumerate(
        zip(starts, microdata_rows, strict=True), start=1
    ):
        card = _balanced_div_fragment(review_html, start=start.start())
        if card is None:
            continue
        raw_values = microdata.groupdict()
        helpful_count = _first_regex(
            card,
            (
                r"<strong>\s*([\d,]+)\s*</strong>"
                r"[\s\S]{0,300}?found this helpful",
            ),
        )
        reposted_from = _first_regex(
            card,
            (r"Reposted from\s+([^<]+)",),
        )
        reviewed_variant = {
            field_name: _clean_html_text(value)
            for field_name, value in (
                (
                    "size_purchased",
                    _first_regex(
                        card,
                        (
                            r"<strong>\s*Size purchased:\s*</strong>\s*([^<]+)",
                        ),
                    ),
                ),
                (
                    "color",
                    _first_regex(
                        card,
                        (r"<strong>\s*Color:\s*</strong>\s*([^<]+)",),
                    ),
                ),
            )
            if value is not None
        }
        media_urls = sorted(
            set(
                html_lib.unescape(value)
                for value in re.findall(
                    r'https?://n\.nordstrommedia\.com/[^"\'\s<>]+',
                    card,
                    flags=re.IGNORECASE,
                )
            )
        )
        raw_field_names = [
            "itemprop.author.content",
            "itemprop.datePublished.content",
            "itemprop.name.content",
            "itemprop.ratingValue.content",
            "itemprop.reviewBody.content",
        ]
        if helpful_count is not None:
            raw_field_names.append("found_this_helpful.count")
        if "Verified purchase" in _clean_html_text(card):
            raw_field_names.append("verified_purchase.badge")
        if reposted_from is not None:
            raw_field_names.append("reposted_from.label")
        raw_field_names.extend(
            f"reviewed_variant.{field_name}"
            for field_name in sorted(reviewed_variant)
        )
        if media_urls:
            raw_field_names.append("review_media.url")
        reviews.append(
            {
                key: html_lib.unescape(value or "").strip()
                for key, value in raw_values.items()
            }
            | {
                "source_card_id": f"review-{start.group(1)}",
                "source_display_position": display_position,
                "helpful_count": helpful_count,
                "verified_purchase": "Verified purchase" in _clean_html_text(card),
                "reposted_from": (
                    html_lib.unescape(reposted_from).strip()
                    if reposted_from
                    else None
                ),
                "reviewed_variant": reviewed_variant or None,
                "media_urls": media_urls,
                "raw_field_names": sorted(raw_field_names),
            }
        )
    return reviews


def _nordstrom_unsupported_review_card_fields(review_html: str) -> list[str]:
    field_labels = {
        "recommendation": r"(?:would\s+recommend|recommendation|recommended?)",
        "unhelpful_count": r"(?:not\s+helpful|unhelpful)",
        "variant": r"(?:reviewed\s+variant|variant)",
        "demographic_declarations": r"(?:age(?:\s+range)?|skin\s+type)",
        "tags": r"(?:tags?|pros?|cons?|best\s+uses?)",
    }
    exposed: set[str] = set()
    for start in re.finditer(
        r'<div\b[^>]*\bid=["\']review-\d+["\'][^>]*>',
        review_html,
        flags=re.IGNORECASE,
    ):
        card = _balanced_div_fragment(review_html, start=start.start())
        if card is None:
            continue
        for field_name, label_pattern in field_labels.items():
            if re.search(
                rf"<(?:dt|th|label|strong|b|span|div)\b[^>]*>\s*"
                rf"{label_pattern}\s*:?\s*</(?:dt|th|label|strong|b|span|div)>",
                card,
                flags=re.IGNORECASE,
            ) or re.search(
                rf"\b(?:aria-label|name|data-[\w-]+)=([\"'])"
                rf"[^\"']*(?<![A-Za-z]){label_pattern}(?![A-Za-z])[^\"']*\1",
                card,
                flags=re.IGNORECASE,
            ):
                exposed.add(field_name)
    return sorted(exposed)


def _nordstrom_highlighted_review(
    review_html: str,
    *,
    kind: str,
) -> dict[str, str | int | bool | None] | None:
    marker = f'id="review-stars-{kind}"'
    marker_index = review_html.find(marker)
    if marker_index < 0:
        return None
    starts = [
        match.start()
        for match in re.finditer(
            r'<div\b[^>]*\bclass=["\'][^"\']*\bNgN2G\b[^"\']*["\'][^>]*>',
            review_html,
            flags=re.IGNORECASE,
        )
        if match.start() < marker_index
    ]
    if not starts:
        return None
    card_start = starts[-1]
    card_html = _balanced_div_fragment(review_html, start=card_start)
    if card_html is None:
        return None
    expected_heading = f"Most helpful {kind} review"
    if expected_heading.lower() not in _clean_html_text(card_html).lower():
        return None

    star_tail = card_html[card_html.find(marker) :]
    rating = _first_regex(
        star_tail,
        (
            rf'id=["\']review-stars-{re.escape(kind)}["\'][^>]*'
            r'aria-label=["\']Rated\s+(\d+(?:\.\d+)?)\s+out of 5 stars?\.',
        ),
    )
    date = _first_regex(
        star_tail,
        (
            r'id=["\']review-stars-[^"\']+["\'][\s\S]{0,500}?'
            r"</span>\s*<span\b[^>]*>([^<]+)</span>",
        ),
    )
    title = _first_regex(
        card_html,
        (
            r'<div\b[^>]*\bclass=["\'][^"\']*\b(?:OF9oA|gBRHe)\b'
            r'[^"\']*["\'][^>]*>\s*<strong>(.*?)</strong>',
        ),
    )
    body = _first_regex(
        card_html,
        (
            r'<div\b[^>]*\bclass=["\'][^"\']*\b(?:OF9oA|gBRHe)\b'
            r'[^"\']*["\'][^>]*>\s*<strong>.*?</strong>\s*</div>'
            r"\s*<div\b[^>]*>\s*<div\b[^>]*>(.*?)</div>\s*</div>",
        ),
    )
    if body is None:
        body = _first_regex(
            card_html,
            (
                r'<div\b[^>]*\bclass=["\'][^"\']*\b(?:rqqDZ|cbVo0|MA5lT)\b'
                r'[^"\']*["\'][^>]*>(.*?)</div>',
            ),
        )
    author = _first_regex(
        card_html,
        (
            r'<div\b[^>]*\bclass=["\'][^"\']*\bqd8jM\b'
            r'[^"\']*["\'][^>]*>(.*?)</div>',
        ),
    )
    helpful_count = _first_regex(
        card_html,
        (
            r"<strong>\s*([\d,]+)\s*</strong>"
            r"[\s\S]{0,300}?found this helpful",
        ),
    )
    card_text = _clean_html_text(card_html)
    reposted_from = _first_regex(
        card_html,
        (
            r'<div\b[^>]*\bclass=["\'][^"\']*\bqd8jM\b[^"\']*["\'][^>]*>'
            r".*?</div>\s*<div\b[^>]*>\s*(Reposted from [^<]+)\s*</div>",
        ),
    )
    return {
        "highlight_kind": kind,
        "rating": rating,
        "date": html_lib.unescape(date).strip() if date else None,
        "title": _clean_html_text(title) if title else None,
        "body": _clean_html_text(body) if body else None,
        "author": _clean_html_text(author) if author else None,
        "helpful_count": helpful_count,
        "verified_purchase": "Verified purchase" in card_text,
        "reposted_from": reposted_from,
    }


def _balanced_div_fragment(html: str, *, start: int) -> str | None:
    """Return the exact div element beginning at start, including nested divs."""
    depth = 0
    for token in re.finditer(r"<div\b[^>]*>|</div\s*>", html[start:], flags=re.I):
        if token.group(0).lower().startswith("<div"):
            depth += 1
            continue
        depth -= 1
        if depth == 0:
            return html[start : start + token.end()]
    return None


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
    *,
    preferred_sku: str | None = None,
) -> tuple[dict[str, Any | None], RetailProjectionRawAnchor | None]:
    for entry in structured_entries:
        if entry.kind != "apollo_state":
            continue
        best: dict[str, object] | None = None
        for item in _walk_dicts(entry.parsed):
            if item.get("skuId") and item.get("productName") and (item.get("listPrice") or item.get("salePrice")):
                if (
                    preferred_sku is not None
                    and _string_or_none(item.get("skuId")) != preferred_sku
                ):
                    continue
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
            "apollo_requested_sku": preferred_sku,
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
    product_state = _sephora_product_state(structured_entries)
    interactions = next(
        (
            entry.parsed
            for entry in structured_entries
            if entry.kind == "sephora_rendered_interactions"
            and isinstance(entry.parsed, dict)
        ),
        {},
    )
    displayed_reviews = interactions.get("displayed_reviews", [])
    if not isinstance(displayed_reviews, list):
        displayed_reviews = []
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
        "recommended_percent": _first_regex(
            review_section_html or visible_text,
            (r"(\d+%)\s+of reviewers recommend",),
        ),
        "review_filters": (
            product_state.get("reviewFilters")
            if isinstance(product_state, dict)
            else None
        ),
        "review_sentiments": (
            product_state.get("sentiments")
            if isinstance(product_state, dict)
            else None
        ),
        "review_images": (
            product_state.get("reviewImages")
            if isinstance(product_state, dict)
            else None
        ),
        "displayed_review_range": _first_regex(
            visible_text,
            (r"(\d+\s*[–-]\s*\d+\s+of\s+[^\n]+)",),
        ),
        "displayed_review_rows": displayed_reviews,
        "displayed_review_body_count": len(displayed_reviews),
        "review_body_coverage": "rendered_first_page_only",
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


def _ulta_review_fields(
    structured_entries: list[_StructuredJsonEntry],
    *,
    requested_sku: str | None,
) -> tuple[dict[str, Any | None], list[str]]:
    residuals: list[str] = []
    ld_count = None
    ld_rating = None
    apollo_count = None
    apollo_rating = None
    reviews: list[dict[str, Any | None]] = []
    for entry in structured_entries:
        for item in _walk_dicts(entry.parsed):
            aggregate = item.get("aggregateRating") if isinstance(item, dict) else None
            if entry.kind == "ld_json" and isinstance(aggregate, dict):
                item_sku = _string_or_none(item.get("sku"))
                if requested_sku and item_sku != requested_sku:
                    continue
                ld_count = _string_or_none(aggregate.get("reviewCount")) or ld_count
                ld_rating = _string_or_none(aggregate.get("ratingValue")) or ld_rating
                if not reviews:
                    reviews = _ulta_review_body_rows(item.get("review"))
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
        "displayed_review_body_count": len(reviews),
        "review_body_coverage": "target_product_json_ld",
        "reviews": reviews,
    }, residuals


def _ulta_review_body_rows(value: object) -> list[dict[str, Any | None]]:
    if not isinstance(value, list):
        return []
    reviews: list[dict[str, Any | None]] = []
    for item in value:
        if not isinstance(item, Mapping) or item.get("@type") != "Review":
            continue
        author_value = item.get("author")
        location_value = item.get("locationCreated")
        rating_value = item.get("reviewRating")
        reviews.append(
            {
                "title": _string_or_none(item.get("name")),
                "body": _string_or_none(item.get("reviewBody")),
                "date_published": _string_or_none(item.get("datePublished")),
                "author": (
                    _string_or_none(author_value.get("name"))
                    if isinstance(author_value, Mapping)
                    else _string_or_none(author_value)
                ),
                "location": (
                    _string_or_none(location_value.get("name"))
                    if isinstance(location_value, Mapping)
                    else _string_or_none(location_value)
                ),
                "rating": (
                    _string_or_none(rating_value.get("ratingValue"))
                    if isinstance(rating_value, Mapping)
                    else None
                ),
            }
        )
    return reviews


def _ulta_sku_from_source_url(source_url: str) -> str | None:
    parsed = urlparse(source_url)
    requested_skus = parse_qs(parsed.query).get("sku", [])
    if (
        parsed.scheme not in {"http", "https"}
        or parsed.hostname not in {"ulta.com", "www.ulta.com"}
        or len(requested_skus) != 1
        or not requested_skus[0].isdigit()
    ):
        return None
    return requested_skus[0]


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
    retailer: Retailer,
) -> list[RetailPdpProjectionLossEntry]:
    entries: list[RetailPdpProjectionLossEntry] = []
    hero_count = len(re.findall(r"hero|ProductHero|imageBlock|main-hero", html, flags=re.IGNORECASE))
    if hero_count:
        entries.append(
            RetailPdpProjectionLossEntry(
                category="RETAIL_HERO_IMAGERY_COLLAPSED",
                count=hero_count,
                raw_anchor=_with_anchor(raw_anchor, "text_pattern", "hero|ProductHero|imageBlock|main-hero"),
                reason=(
                    "hero image binary bytes and gallery layout are not retained in the semantic "
                    "projection; source URLs/state and rendered copy remain in derived rows"
                ),
            )
        )
    cart_count = len(
        re.findall(
            r"add to cart|add to bag|add to basket|add for ship|out of stock|notify me",
            visible_text,
            flags=re.IGNORECASE,
        )
    )
    if cart_count:
        entries.append(
            RetailPdpProjectionLossEntry(
                category="RETAIL_CART_NOTIFY_STATE_COLLAPSED",
                count=cart_count,
                raw_anchor=_with_anchor(
                    raw_anchor,
                    "text_pattern",
                    "add to cart|add to bag|add to basket|add for ship|out of stock|notify me",
                ),
                reason="cart/notify button chrome collapsed while variant availability binding is carried",
            )
        )
    if retailer == "sephora":
        extra_specs = (
            (
                "RETAIL_NAVIGATION_FOOTER_PROMOTION_COLLAPSED",
                r"GlobalNavigation|footer|TopNav|promotion",
                "navigation, footer, and promotional shell omitted; rendered PDP text is retained",
            ),
            (
                "RETAIL_SCRIPT_STYLE_TELEMETRY_COLLAPSED",
                r"<script\b|<style\b|analytics|telemetry",
                "executable scripts, styles, and telemetry shell omitted; linkStore.page.product is retained",
            ),
            (
                "RETAIL_RECOMMENDATION_CAROUSEL_COLLAPSED",
                r"recommendation|Make it a routine|You May Also Like",
                "recommendation carousel presentation omitted; its presence remains logged",
            ),
            (
                "RETAIL_GALLERY_COMMUNITY_MEDIA_COLLAPSED",
                r"gallery|community|UGC|ProductImage",
                "gallery and community-media binaries/layout omitted; media URLs in retained state and review rows remain",
            ),
            (
                "RETAIL_FLEXIBLE_PAYMENT_CHROME_COLLAPSED",
                r"Klarna|Afterpay|4 x \$|4 payments|pay in 4",
                "flexible-payment widget chrome omitted; rendered allocation text remains in the product row",
            ),
        )
        for category, pattern, reason in extra_specs:
            count = len(re.findall(pattern, html, flags=re.IGNORECASE))
            if not count:
                count = len(
                    re.findall(pattern, visible_text, flags=re.IGNORECASE)
                )
            if count:
                entries.append(
                    RetailPdpProjectionLossEntry(
                        category=category,
                        count=count,
                        raw_anchor=_with_anchor(
                            raw_anchor,
                            "text_pattern",
                            pattern,
                        ),
                        reason=reason,
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
    "ULTA_PDP_CONTENT_PROFILE",
    "ULTA_PDP_CONTENT_RECORD_KIND",
    "ULTA_PDP_CONTENT_SCHEMA_VERSION",
    "ULTA_PDP_PARSER_VERSION",
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
    "UltaPdpAggregateContentRecord",
    "build_nordstrom_pdp_aggregate_content_record",
    "build_retail_pdp_projection",
    "build_retail_pdp_projection_from_packet_directory",
    "build_sephora_pdp_aggregate_content_record",
    "build_ulta_pdp_aggregate_content_record",
]
