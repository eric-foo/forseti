"""Re-derivable multi-axis classification for legacy source family/surface pairs.

The legacy strings remain capture truth.  This module is a closed compatibility
view over those strings: it neither rewrites packets nor infers an unmapped pair.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from types import MappingProxyType
from typing import Iterable, Literal


SOURCE_CLASSIFICATION_SCHEMA_VERSION = "source_classification_v0"


class EvidenceShape(StrEnum):
    THREAD = "thread"
    REVIEW = "review"
    SOCIAL_VIDEO = "social_video"
    SOCIAL_PROFILE = "social_profile"
    COMMUNITY_LISTING = "community_listing"
    COMMERCE_PDP_OFFER = "commerce_pdp_offer"
    OFFICIAL_PAGE = "official_page"


class VenueRole(StrEnum):
    SOCIAL_MEDIA = "social_media"
    SOCIAL_COMMERCE = "social_commerce"
    MARKETPLACE = "marketplace"
    RETAILER = "retailer"
    COMMUNITY = "community"
    PROFESSIONAL_NETWORK = "professional_network"
    VENDOR_OFFICIAL = "vendor_official"
    EMPLOYMENT_BOARD = "employment_board"
    ARCHIVE = "archive"
    DISCOVERY = "discovery"
    PUBLICATION = "publication"


class VenueSubtype(StrEnum):
    GENERAL = "general"
    SPECIALIST = "specialist"


class AccessCaptureOverlay(StrEnum):
    DIRECT_HTTP = "direct_http"
    RENDERED_BROWSER = "rendered_browser"
    SESSIONED_BROWSER = "sessioned_browser"
    ARCHIVE_SNAPSHOT = "archive_snapshot"
    AUDIO_CAPTURE = "audio_capture"
    CAPTION_CAPTURE = "caption_capture"
    FEED = "feed"
    OPERATOR_SUPPLIED = "operator_supplied"
    SUPERVISED_BROWSER = "supervised_browser"


_PROJECTION_MECHANICS_BY_SHAPE = MappingProxyType(
    {
        EvidenceShape.THREAD: "threaded_chain",
        EvidenceShape.REVIEW: "rated_text_recency",
        EvidenceShape.SOCIAL_VIDEO: "channel_public_output",
        EvidenceShape.SOCIAL_PROFILE: "channel_public_output",
        EvidenceShape.COMMUNITY_LISTING: "threaded_chain",
        EvidenceShape.COMMERCE_PDP_OFFER: "variant_price_availability",
        EvidenceShape.OFFICIAL_PAGE: "package_structure_memo",
    }
)


@dataclass(frozen=True)
class SourceClassificationDefinition:
    source_family: str
    source_surface: str
    operator_identity: str | None
    venue_roles: tuple[VenueRole, ...]
    venue_subtype: VenueSubtype | None
    evidence_shapes: tuple[EvidenceShape, ...]
    access_capture_overlay: tuple[AccessCaptureOverlay, ...] = ()
    residuals: tuple[str, ...] = ()
    declared_by: tuple[str, ...] = ()
    inventory_status: Literal["implemented", "classification_contract"] = "implemented"


@dataclass(frozen=True)
class SourceClassification:
    legacy_source_family: str
    legacy_source_surface: str
    mapping_status: Literal["classified", "unknown"]
    operator_identity: str | None
    venue_roles: tuple[str, ...]
    venue_subtype: str | None
    evidence_shapes: tuple[str, ...]
    projection_mechanics: tuple[str, ...]
    access_capture_overlay: tuple[str, ...]
    residuals: tuple[str, ...]
    declared_by: tuple[str, ...]
    inventory_status: Literal["implemented", "classification_contract"] | None
    schema_version: str = SOURCE_CLASSIFICATION_SCHEMA_VERSION

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "legacy_source_family": self.legacy_source_family,
            "legacy_source_surface": self.legacy_source_surface,
            "mapping_status": self.mapping_status,
            "operator_identity": self.operator_identity,
            "venue_roles": list(self.venue_roles),
            "venue_subtype": self.venue_subtype,
            "evidence_shapes": list(self.evidence_shapes),
            "projection_mechanics": list(self.projection_mechanics),
            "access_capture_overlay": list(self.access_capture_overlay),
            "residuals": list(self.residuals),
            "declared_by": list(self.declared_by),
            "inventory_status": self.inventory_status,
        }


class UnknownSourceClassificationError(ValueError):
    """Raised when strict classification receives an unregistered legacy pair."""


def _definition(
    source_family: str,
    source_surface: str,
    *,
    operator: str | None,
    roles: tuple[VenueRole, ...],
    shapes: tuple[EvidenceShape, ...],
    source: str,
    subtype: VenueSubtype | None = None,
    overlay: tuple[AccessCaptureOverlay, ...] = (),
    residuals: tuple[str, ...] = (),
    status: Literal["implemented", "classification_contract"] = "implemented",
) -> SourceClassificationDefinition:
    return SourceClassificationDefinition(
        source_family=source_family,
        source_surface=source_surface,
        operator_identity=operator,
        venue_roles=roles,
        venue_subtype=subtype,
        evidence_shapes=shapes,
        access_capture_overlay=overlay,
        residuals=residuals,
        declared_by=(source,),
        inventory_status=status,
    )


_FRAGRANCE_SOURCE = "forseti-harness/source_capture/{fragrantica,parfumo,basenotes}_projection.py"
_IG_SOURCE = "forseti-harness/source_capture/ig_*"
_TIKTOK_SOURCE = "forseti-harness/source_capture/tiktok/"
_YOUTUBE_SOURCE = "forseti-harness/source_capture/{youtube_watch_packet.py,transcript/}"
_LINKEDIN_SOURCE = "forseti-harness/capture_spine/linkedin_lane/models.py"
_FIXTURE_SOURCE = "forseti-harness/tests/fixtures/silver_compatibility/"


SOURCE_CLASSIFICATION_DEFINITIONS: tuple[SourceClassificationDefinition, ...] = (
    _definition(
        "archive_org",
        "archive_org_wayback",
        operator="archive_org",
        roles=(VenueRole.ARCHIVE,),
        shapes=(),
        overlay=(AccessCaptureOverlay.ARCHIVE_SNAPSHOT,),
        residuals=("underlying_venue_role_and_evidence_shape_not_derivable_from_legacy_pair",),
        source="forseti-harness/cases/product_learning/**/source_captures/**/manifest.json",
    ),
    _definition(
        "greenhouse_ats_board",
        "greenhouse_public_jobs_board",
        operator="greenhouse",
        roles=(VenueRole.EMPLOYMENT_BOARD,),
        shapes=(EvidenceShape.OFFICIAL_PAGE,),
        source=(
            "forseti-harness/cases/product_learning/beautypie_repricing_2023_v0/"
            "source_captures/"
        ),
    ),
    *(
        _definition(
            "fragrance_native_database",
            surface,
            operator=operator,
            roles=(VenueRole.COMMUNITY,),
            subtype=VenueSubtype.SPECIALIST,
            shapes=(EvidenceShape.REVIEW,),
            overlay=overlay,
            source=_FRAGRANCE_SOURCE,
        )
        for surface, operator, overlay in (
            (
                "basenotes_product_page_user_cleared_persistent_chrome_current_window",
                "basenotes",
                (AccessCaptureOverlay.SESSIONED_BROWSER,),
            ),
            (
                "fragrantica_product_page_cloakbrowser_deep_scroll_current_window",
                "fragrantica",
                (AccessCaptureOverlay.RENDERED_BROWSER,),
            ),
            (
                "fragrantica_product_page_cloakbrowser_initial_viewport",
                "fragrantica",
                (AccessCaptureOverlay.RENDERED_BROWSER,),
            ),
            (
                "fragrantica_product_page_direct_http",
                "fragrantica",
                (AccessCaptureOverlay.DIRECT_HTTP,),
            ),
            (
                "parfumo_product_page_chrome_extension_targeted_rendered_session",
                "parfumo",
                (AccessCaptureOverlay.SESSIONED_BROWSER,),
            ),
            (
                "parfumo_product_page_direct_http",
                "parfumo",
                (AccessCaptureOverlay.DIRECT_HTTP,),
            ),
        )
    ),
    _definition(
        "fragrance_review",
        "rendered_widget_review",
        operator=None,
        roles=(),
        shapes=(EvidenceShape.REVIEW,),
        overlay=(AccessCaptureOverlay.RENDERED_BROWSER,),
        residuals=("operator_and_venue_role_require_actual_host_facts",),
        source="forseti-harness/source_capture/fragrance_review_lake.py",
    ),
    *(
        _definition(
            "instagram_creator",
            surface,
            operator="instagram",
            roles=(VenueRole.SOCIAL_MEDIA,),
            shapes=shapes,
            overlay=overlay,
            source=_IG_SOURCE,
        )
        for surface, shapes, overlay in (
            (
                "ig_calls_browser_snapshot",
                (EvidenceShape.SOCIAL_PROFILE,),
                (AccessCaptureOverlay.RENDERED_BROWSER,),
            ),
            (
                "ig_daily_heartbeat_first_visible_reels_grid",
                (EvidenceShape.SOCIAL_VIDEO,),
                (AccessCaptureOverlay.RENDERED_BROWSER,),
            ),
            (
                "ig_reels_audio",
                (EvidenceShape.SOCIAL_VIDEO,),
                (AccessCaptureOverlay.AUDIO_CAPTURE,),
            ),
            ("ig_reels_deep_capture", (EvidenceShape.SOCIAL_VIDEO,), ()),
            (
                "ig_reels_deep_capture_render_audio",
                (EvidenceShape.SOCIAL_VIDEO,),
                (AccessCaptureOverlay.AUDIO_CAPTURE,),
            ),
            (
                "ig_reels_grid_dom_passive_json",
                (EvidenceShape.SOCIAL_VIDEO,),
                (AccessCaptureOverlay.RENDERED_BROWSER,),
            ),
        )
    ),
    _definition(
        "reddit_subreddit_grid",
        "old_reddit_direct_http",
        operator="reddit",
        roles=(VenueRole.COMMUNITY,),
        subtype=VenueSubtype.GENERAL,
        shapes=(EvidenceShape.COMMUNITY_LISTING,),
        overlay=(AccessCaptureOverlay.DIRECT_HTTP,),
        source="forseti-harness/runners/run_reddit_grid_capture.py",
    ),
    _definition(
        "reddit_subreddit_grid",
        "old_reddit_grid_packet",
        operator="reddit",
        roles=(VenueRole.COMMUNITY,),
        subtype=VenueSubtype.GENERAL,
        shapes=(EvidenceShape.COMMUNITY_LISTING,),
        source="forseti-harness/capture_spine/reddit_subreddit_grid/materializer.py",
    ),
    _definition(
        "reddit_thread",
        "old_reddit_direct_http",
        operator="reddit",
        roles=(VenueRole.COMMUNITY,),
        subtype=VenueSubtype.GENERAL,
        shapes=(EvidenceShape.THREAD,),
        overlay=(AccessCaptureOverlay.DIRECT_HTTP,),
        source="forseti-harness/runners/run_reddit_old_http_batch.py",
    ),
    _definition(
        "retail_pdp",
        "cloakbrowser_snapshot",
        operator=None,
        roles=(VenueRole.RETAILER,),
        shapes=(EvidenceShape.COMMERCE_PDP_OFFER,),
        overlay=(AccessCaptureOverlay.RENDERED_BROWSER,),
        residuals=("retailer_operator_not_derivable_from_legacy_pair",),
        source="forseti-harness/source_capture/retail_pdp_projection.py",
    ),
    _definition(
        "retail_pdp",
        "direct_http",
        operator=None,
        roles=(VenueRole.RETAILER,),
        shapes=(EvidenceShape.COMMERCE_PDP_OFFER,),
        overlay=(AccessCaptureOverlay.DIRECT_HTTP,),
        residuals=("retailer_operator_not_derivable_from_legacy_pair",),
        source="forseti-harness/runners/run_source_capture_http_packet.py",
    ),
    _definition(
        "retail_pdp",
        "sephora_bazaarvoice_onboarding",
        operator="sephora",
        roles=(VenueRole.RETAILER,),
        shapes=(EvidenceShape.REVIEW,),
        source="forseti-harness/source_capture/sephora_onboarding_capture.py",
    ),
    *(
        _definition(
            "social_media",
            surface,
            operator=operator,
            roles=(VenueRole.SOCIAL_MEDIA,),
            shapes=shapes,
            source=_FIXTURE_SOURCE,
            residuals=residuals,
        )
        for surface, operator, shapes, residuals in (
            ("instagram_reels_grid", "instagram", (EvidenceShape.SOCIAL_VIDEO,), ()),
            (
                "tiktok_creator_batch_comment_subtitle_admission",
                "tiktok",
                (EvidenceShape.SOCIAL_VIDEO, EvidenceShape.THREAD),
                (),
            ),
            (
                "web_profile_info_json_metadata",
                None,
                (EvidenceShape.SOCIAL_PROFILE,),
                ("operator_not_derivable_from_legacy_pair",),
            ),
            ("youtube_shorts", "youtube", (EvidenceShape.SOCIAL_VIDEO,), ()),
        )
    ),
    *(
        _definition(
            "tiktok",
            surface,
            operator="tiktok",
            roles=(VenueRole.SOCIAL_MEDIA,),
            shapes=shapes,
            source=_TIKTOK_SOURCE,
        )
        for surface, shapes in (
            (
                "tiktok_creator_batch_comment_subtitle_admission",
                (EvidenceShape.SOCIAL_VIDEO, EvidenceShape.THREAD),
            ),
            ("tiktok_creator_grid_window", (EvidenceShape.SOCIAL_VIDEO,)),
            (
                "tiktok_video_comment_subtitle_admission",
                (EvidenceShape.SOCIAL_VIDEO, EvidenceShape.THREAD),
            ),
        )
    ),
    *(
        _definition(
            "tiktok",
            surface,
            operator="tiktok",
            roles=(VenueRole.SOCIAL_COMMERCE, VenueRole.MARKETPLACE),
            shapes=(shape,),
            source="classification contract: TikTok Shop surface-specific compatibility inputs",
            status="classification_contract",
        )
        for surface, shape in (
            ("tiktok_shop_listing", EvidenceShape.COMMERCE_PDP_OFFER),
            ("tiktok_shop_creator_video", EvidenceShape.SOCIAL_VIDEO),
            ("tiktok_shop_review", EvidenceShape.REVIEW),
        )
    ),
    _definition(
        "vendor_pricing_page",
        "openai_chatgpt_pricing_rung15",
        operator="openai",
        roles=(VenueRole.VENDOR_OFFICIAL,),
        shapes=(EvidenceShape.COMMERCE_PDP_OFFER,),
        source="forseti-harness/runners/run_source_capture_price_payload_packet.py",
    ),
    *(
        _definition(
            "youtube",
            surface,
            operator="youtube",
            roles=(VenueRole.SOCIAL_MEDIA,),
            shapes=(EvidenceShape.SOCIAL_VIDEO,),
            overlay=overlay,
            source=_YOUTUBE_SOURCE,
        )
        for surface, overlay in (
            ("youtube_audio", (AccessCaptureOverlay.AUDIO_CAPTURE,)),
            ("youtube_captions", (AccessCaptureOverlay.CAPTION_CAPTURE,)),
            ("youtube_channel_rss_feed", (AccessCaptureOverlay.FEED,)),
            ("youtube_watch_metadata_comments", ()),
        )
    ),
    *(
        _definition(
            "linkedin_adjacent",
            surface,
            operator=operator,
            roles=roles,
            shapes=shapes,
            overlay=overlay,
            residuals=residuals,
            source=_LINKEDIN_SOURCE,
        )
        for surface, operator, roles, shapes, overlay, residuals in (
            (
                "operator_supplied_seed_list",
                None,
                (VenueRole.DISCOVERY,),
                (EvidenceShape.COMMUNITY_LISTING,),
                (AccessCaptureOverlay.OPERATOR_SUPPLIED,),
                ("operator_not_derivable_from_legacy_pair",),
            ),
            (
                "company_website_blog_press_pricing",
                None,
                (VenueRole.VENDOR_OFFICIAL,),
                (EvidenceShape.OFFICIAL_PAGE,),
                (),
                ("operator_requires_actual_host_facts",),
            ),
            (
                "conference_podcast_newsletter_publication",
                None,
                (VenueRole.PUBLICATION,),
                (EvidenceShape.OFFICIAL_PAGE,),
                (),
                ("operator_requires_actual_host_facts",),
            ),
            (
                "public_directory_or_ecosystem_list",
                None,
                (VenueRole.DISCOVERY,),
                (EvidenceShape.COMMUNITY_LISTING,),
                (),
                ("operator_requires_actual_host_facts",),
            ),
            (
                "manual_search_result_review",
                None,
                (VenueRole.DISCOVERY,),
                (EvidenceShape.COMMUNITY_LISTING,),
                (),
                ("operator_requires_actual_host_facts",),
            ),
            (
                "sales_navigator_manual_entitled",
                "linkedin",
                (VenueRole.PROFESSIONAL_NETWORK,),
                (EvidenceShape.SOCIAL_PROFILE,),
                (AccessCaptureOverlay.SESSIONED_BROWSER,),
                (),
            ),
            (
                "linkedin_company_page_or_post",
                "linkedin",
                (VenueRole.PROFESSIONAL_NETWORK,),
                (EvidenceShape.SOCIAL_PROFILE,),
                (),
                (),
            ),
            (
                "linkedin_public_or_person_url",
                "linkedin",
                (VenueRole.PROFESSIONAL_NETWORK,),
                (EvidenceShape.SOCIAL_PROFILE,),
                (),
                (),
            ),
            (
                "supervised_browser_assist",
                None,
                (),
                (),
                (AccessCaptureOverlay.SUPERVISED_BROWSER,),
                ("underlying_operator_role_and_evidence_shape_not_derivable_from_legacy_pair",),
            ),
        )
    ),
)


def projection_mechanics_for_shapes(
    evidence_shapes: Iterable[EvidenceShape],
) -> tuple[str, ...]:
    """Derive mechanics from information shape, never venue or platform."""
    return tuple(
        sorted({_PROJECTION_MECHANICS_BY_SHAPE[shape] for shape in evidence_shapes})
    )


def validate_source_classification_definitions(
    definitions: Iterable[SourceClassificationDefinition],
) -> dict[tuple[str, str], SourceClassificationDefinition]:
    """Build a deterministic closed registry and reject duplicates/conflicts."""
    registry: dict[tuple[str, str], SourceClassificationDefinition] = {}
    for definition in definitions:
        key = (definition.source_family, definition.source_surface)
        if not all(isinstance(value, str) and value.strip() for value in key):
            raise ValueError(f"source classification key must be non-blank: {key!r}")
        if key in registry:
            conflict = "duplicate" if registry[key] == definition else "conflicting"
            raise ValueError(f"{conflict} source classification mapping for {key!r}")
        if not definition.evidence_shapes and not definition.residuals:
            raise ValueError(
                f"source classification without evidence shapes must residualize: {key!r}"
            )
        if definition.source_surface.startswith("tiktok_shop_"):
            if definition.operator_identity != "tiktok":
                raise ValueError(f"TikTok Shop mapping must retain tiktok operator: {key!r}")
            required_roles = {VenueRole.SOCIAL_COMMERCE, VenueRole.MARKETPLACE}
            if set(definition.venue_roles) != required_roles:
                raise ValueError(
                    f"TikTok Shop mapping must use social-commerce + marketplace roles: {key!r}"
                )
        registry[key] = definition
    return registry


SOURCE_CLASSIFICATION_REGISTRY = MappingProxyType(
    validate_source_classification_definitions(SOURCE_CLASSIFICATION_DEFINITIONS)
)


def _classified(definition: SourceClassificationDefinition) -> SourceClassification:
    return SourceClassification(
        legacy_source_family=definition.source_family,
        legacy_source_surface=definition.source_surface,
        mapping_status="classified",
        operator_identity=definition.operator_identity,
        venue_roles=tuple(role.value for role in definition.venue_roles),
        venue_subtype=definition.venue_subtype.value if definition.venue_subtype else None,
        evidence_shapes=tuple(shape.value for shape in definition.evidence_shapes),
        projection_mechanics=projection_mechanics_for_shapes(definition.evidence_shapes),
        access_capture_overlay=tuple(
            overlay.value for overlay in definition.access_capture_overlay
        ),
        residuals=definition.residuals,
        declared_by=definition.declared_by,
        inventory_status=definition.inventory_status,
    )


def classify_source_pair(source_family: str, source_surface: str) -> SourceClassification:
    """Strictly classify one exact legacy pair; never normalize or guess."""
    definition = SOURCE_CLASSIFICATION_REGISTRY.get((source_family, source_surface))
    if definition is None:
        raise UnknownSourceClassificationError(
            "unmapped legacy source classification pair: "
            f"source_family={source_family!r}, source_surface={source_surface!r}"
        )
    return _classified(definition)


def source_classification_view(
    source_family: object, source_surface: object
) -> SourceClassification:
    """Residualizing read view for catalogs that must retain unknown raw rows."""
    if isinstance(source_family, str) and isinstance(source_surface, str):
        definition = SOURCE_CLASSIFICATION_REGISTRY.get((source_family, source_surface))
        if definition is not None:
            return _classified(definition)
    return SourceClassification(
        legacy_source_family=source_family if isinstance(source_family, str) else "",
        legacy_source_surface=source_surface if isinstance(source_surface, str) else "",
        mapping_status="unknown",
        operator_identity=None,
        venue_roles=(),
        venue_subtype=None,
        evidence_shapes=(),
        projection_mechanics=(),
        access_capture_overlay=(),
        residuals=("unmapped_legacy_source_pair",),
        declared_by=(),
        inventory_status=None,
    )


def implemented_source_pair_inventory() -> tuple[tuple[str, str], ...]:
    """Return the closed inventory discovered from committed runtime/fixtures."""
    return tuple(
        sorted(
            key
            for key, definition in SOURCE_CLASSIFICATION_REGISTRY.items()
            if definition.inventory_status == "implemented"
        )
    )


__all__ = [
    "AccessCaptureOverlay",
    "EvidenceShape",
    "SOURCE_CLASSIFICATION_DEFINITIONS",
    "SOURCE_CLASSIFICATION_REGISTRY",
    "SOURCE_CLASSIFICATION_SCHEMA_VERSION",
    "SourceClassification",
    "SourceClassificationDefinition",
    "UnknownSourceClassificationError",
    "VenueRole",
    "VenueSubtype",
    "classify_source_pair",
    "implemented_source_pair_inventory",
    "projection_mechanics_for_shapes",
    "source_classification_view",
    "validate_source_classification_definitions",
]
