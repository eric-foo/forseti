from __future__ import annotations

from pathlib import Path

import pytest

from runners import run_source_capture_cloakbrowser_packet as cloakbrowser_runner
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
        "amazon",
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
    assert get_retail_capture_profile("sephora_grid_aggregate").scroll_target_selector is None
    assert get_retail_capture_profile("sephora_pdp_aggregate").scroll_target_selector is None
    assert (
        get_retail_capture_profile("sephora_pdp_distribution").scroll_target_selector
        == "#ratings-reviews-container"
    )
    assert get_retail_capture_profile("ulta_pdp_aggregate").scroll_passes == 0
    assert get_retail_capture_profile("target_pdp_aggregate").settle_seconds == 6.0
    assert (
        get_retail_capture_profile("amazon_pdp_distribution").wait_until
        == "domcontentloaded"
    )
    assert get_retail_capture_profile("amazon_pdp_distribution").settle_seconds == 0.0
    assert get_retail_capture_profile("amazon_grid_aggregate").scroll_passes == 0


def test_amazon_distribution_profile_accepts_changing_values_but_requires_full_data() -> None:
    profile = get_retail_capture_profile("amazon_pdp_distribution")
    visible_text = """
LANEIGE Lip Sleeping Mask
New York 10001
Currently unavailable
71K+ bought in past month
$25.50
4.7 out of 5 stars
37,104 global ratings
5 star 80%
4 star 12%
3 star 5%
2 star 1%
1 star 2%
"""
    rendered_dom = """
<html><body>
<input name="currencyOfPreference" value="USD">
<input id="ASIN" value="B07XXPHQZK">
<a href="/gp/customer-reviews/R3V62VIIGMFTE3">Read more</a>
<div>1,500 customers mention moisturizing</div>
</body></html>
"""

    result = evaluate_source_detail_sufficiency(
        requirements=profile.requirements,
        access_block_reason=None,
        visible_text=visible_text,
        rendered_dom=rendered_dom,
    )

    assert result.passed is True

    missing_insights = evaluate_source_detail_sufficiency(
        requirements=profile.requirements,
        access_block_reason=None,
        visible_text=visible_text,
        rendered_dom=rendered_dom.replace("1,500 customers mention", "insights absent"),
    )
    assert missing_insights.passed is False
    assert any(
        "customers mention" in reason
        for reason in missing_insights.failure_reasons
    )


def test_cloakbrowser_cli_uses_profile_wait_until_unless_operator_overrides(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    captured: list[dict[str, object]] = []

    def fake_run(**kwargs: object) -> tuple[int, str]:
        captured.append(kwargs)
        return 0, "packet"

    monkeypatch.setattr(
        cloakbrowser_runner,
        "run_source_capture_cloakbrowser_packet",
        fake_run,
    )
    base_args = [
        "--url",
        "https://www.amazon.com/Laneige-Sleeping-Berry/dp/B07XXPHQZK",
        "--source-family",
        "retail_pdp",
        "--source-surface",
        "cloakbrowser_snapshot",
        "--decision-question",
        "Did the Amazon profile capture its required data?",
        "--output",
        str(tmp_path / "packet"),
        "--retail-capture-profile",
        "amazon_pdp_distribution",
        "--delivery-zip",
        "10001",
    ]

    assert cloakbrowser_runner.main(base_args) == 0
    assert captured[-1]["wait_until"] == "domcontentloaded"
    assert captured[-1]["settle_seconds"] == 0.0

    assert cloakbrowser_runner.main([*base_args, "--wait-until", "load"]) == 0
    assert captured[-1]["wait_until"] == "load"


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
