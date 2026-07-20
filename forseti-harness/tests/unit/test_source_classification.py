from __future__ import annotations

import pytest

from source_capture.source_classification import (
    EvidenceShape,
    SOURCE_CLASSIFICATION_REGISTRY,
    SourceClassificationDefinition,
    UnknownSourceClassificationError,
    VenueRole,
    VenueSubtype,
    classify_source_pair,
    implemented_source_pair_inventory,
    projection_mechanics_for_shapes,
    source_classification_view,
    validate_source_classification_definitions,
)


def test_inventory_is_closed_source_cited_and_deterministic() -> None:
    inventory = implemented_source_pair_inventory()

    assert len(inventory) == 42
    assert inventory == tuple(sorted(inventory))
    assert len(set(inventory)) == len(inventory)
    assert all(
        SOURCE_CLASSIFICATION_REGISTRY[pair].declared_by for pair in inventory
    )


def test_unknown_pair_fails_strict_and_residualizes_in_catalog_view() -> None:
    with pytest.raises(UnknownSourceClassificationError, match="unmapped legacy"):
        classify_source_pair("future_family", "future_surface")

    view = source_classification_view("future_family", "future_surface")

    assert view.mapping_status == "unknown"
    assert view.operator_identity is None
    assert view.venue_roles == ()
    assert view.evidence_shapes == ()
    assert view.residuals == ("unmapped_legacy_source_pair",)


def test_registry_validation_rejects_duplicate_and_conflicting_mappings() -> None:
    first = SourceClassificationDefinition(
        source_family="community",
        source_surface="thread",
        operator_identity="first",
        venue_roles=(VenueRole.COMMUNITY,),
        venue_subtype=VenueSubtype.GENERAL,
        evidence_shapes=(EvidenceShape.THREAD,),
    )
    conflicting = SourceClassificationDefinition(
        source_family="community",
        source_surface="thread",
        operator_identity="second",
        venue_roles=(VenueRole.COMMUNITY,),
        venue_subtype=VenueSubtype.SPECIALIST,
        evidence_shapes=(EvidenceShape.THREAD,),
    )

    with pytest.raises(ValueError, match="duplicate"):
        validate_source_classification_definitions((first, first))
    with pytest.raises(ValueError, match="conflicting"):
        validate_source_classification_definitions((first, conflicting))


def test_thread_mechanics_do_not_change_with_community_subtype() -> None:
    general = SourceClassificationDefinition(
        source_family="general_community",
        source_surface="thread",
        operator_identity="general",
        venue_roles=(VenueRole.COMMUNITY,),
        venue_subtype=VenueSubtype.GENERAL,
        evidence_shapes=(EvidenceShape.THREAD,),
    )
    specialist = SourceClassificationDefinition(
        source_family="specialist_community",
        source_surface="thread",
        operator_identity="specialist",
        venue_roles=(VenueRole.COMMUNITY,),
        venue_subtype=VenueSubtype.SPECIALIST,
        evidence_shapes=(EvidenceShape.THREAD,),
    )

    assert general.venue_subtype != specialist.venue_subtype
    assert projection_mechanics_for_shapes(general.evidence_shapes) == (
        "threaded_chain",
    )
    assert projection_mechanics_for_shapes(specialist.evidence_shapes) == (
        "threaded_chain",
    )


def test_review_is_an_evidence_shape_not_a_universal_venue() -> None:
    view = classify_source_pair("fragrance_review", "rendered_widget_review")

    assert view.evidence_shapes == ("review",)
    assert view.venue_roles == ()
    assert view.operator_identity is None
    assert view.residuals == ("operator_and_venue_role_require_actual_host_facts",)


def test_tiktok_shop_and_retailer_coexist_without_role_or_shape_flattening() -> None:
    ordinary_tiktok = classify_source_pair(
        "tiktok", "tiktok_video_comment_subtitle_admission"
    )
    shop_listing = classify_source_pair("tiktok", "tiktok_shop_listing")
    shop_video = classify_source_pair("tiktok", "tiktok_shop_creator_video")
    shop_review = classify_source_pair("tiktok", "tiktok_shop_review")
    retailer = classify_source_pair("retail_pdp", "cloakbrowser_snapshot")

    assert ordinary_tiktok.operator_identity == "tiktok"
    assert ordinary_tiktok.venue_roles == ("social_media",)
    assert ordinary_tiktok.evidence_shapes == ("social_video", "thread")

    for shop_view in (shop_listing, shop_video, shop_review):
        assert shop_view.operator_identity == "tiktok"
        assert set(shop_view.venue_roles) == {"social_commerce", "marketplace"}
        assert "social_media" not in shop_view.venue_roles

    assert shop_listing.evidence_shapes == ("commerce_pdp_offer",)
    assert shop_video.evidence_shapes == ("social_video",)
    assert shop_review.evidence_shapes == ("review",)
    assert retailer.operator_identity is None
    assert retailer.venue_roles == ("retailer",)
    assert retailer.evidence_shapes == ("commerce_pdp_offer",)
