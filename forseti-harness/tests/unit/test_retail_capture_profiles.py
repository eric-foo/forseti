from __future__ import annotations

import pytest

from source_capture.retail_capture_profiles import (
    get_retail_capture_profile,
    merge_source_detail_sufficiency_requirements,
    retail_capture_profile_names,
    validate_retail_capture_profile_route,
)
from source_capture.source_detail_sufficiency import (
    SourceDetailSufficiencyRequirements,
    evaluate_source_detail_sufficiency,
)


def test_profiles_cover_each_retailer_and_page_kind_with_explicit_route_flags() -> None:
    profiles = [get_retail_capture_profile(name) for name in retail_capture_profile_names()]

    assert {profile.retailer for profile in profiles} == {
        "sephora",
        "ulta",
        "walmart",
        "target",
    }
    assert {profile.page_kind for profile in profiles} == {
        "grid_aggregate",
        "pdp_aggregate",
        "pdp_distribution",
    }
    assert {profile.source_surface for profile in profiles} == {
        "cloakbrowser_snapshot",
        "direct_http",
    }
    assert get_retail_capture_profile("ulta_grid_aggregate").ordinary_operation is False
    assert get_retail_capture_profile("walmart_grid_aggregate").source_surface == "direct_http"
    assert (
        get_retail_capture_profile("target_grid_aggregate").source_surface
        == "cloakbrowser_snapshot"
    )
    assert get_retail_capture_profile("sephora_pdp_aggregate").scroll_step_px == 350
    assert get_retail_capture_profile("ulta_pdp_aggregate").scroll_passes == 0
    assert get_retail_capture_profile("target_pdp_aggregate").settle_seconds == 6.0


@pytest.mark.parametrize("name", retail_capture_profile_names())
def test_content_sparse_shell_fails_every_profile_without_transport_or_block_failure(
    name: str,
) -> None:
    profile = get_retail_capture_profile(name)

    result = evaluate_source_detail_sufficiency(
        requirements=profile.requirements,
        access_block_reason=None,
        visible_text="Be Right Back",
        rendered_dom="<html><body>Be Right Back</body></html>",
    )

    assert result.enabled is True
    assert result.passed is False
    assert result.failure_reasons


def test_profile_route_validation_fails_before_capture_on_wrong_host_or_rung() -> None:
    profile = get_retail_capture_profile("target_grid_aggregate")

    with pytest.raises(ValueError, match="requires hostname www.target.com"):
        validate_retail_capture_profile_route(
            profile,
            url="https://www.walmart.com/search?q=lip+mask",
            source_family="retail_pdp",
            source_surface="cloakbrowser_snapshot",
        )
    with pytest.raises(ValueError, match="requires source_surface cloakbrowser_snapshot"):
        validate_retail_capture_profile_route(
            profile,
            url="https://www.target.com/s?searchTerm=lip%20mask",
            source_family="retail_pdp",
            source_surface="direct_http",
        )


def test_profile_requirements_merge_with_explicit_requirements_without_weakening_either() -> None:
    explicit = SourceDetailSufficiencyRequirements(
        min_visible_text_bytes=100,
        visible_text_contains=("operator marker",),
    )
    profile = get_retail_capture_profile("sephora_pdp_aggregate")

    merged = merge_source_detail_sufficiency_requirements(explicit, profile.requirements)

    assert merged is not None
    assert merged.require_not_access_blocked is True
    assert merged.min_visible_text_bytes == 100
    assert merged.visible_text_contains == (
        "operator marker",
        "Lip Sleeping Mask",
        "Ratings & Reviews",
        "Color:",
    )
