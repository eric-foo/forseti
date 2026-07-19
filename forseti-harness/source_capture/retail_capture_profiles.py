from __future__ import annotations

import re
from dataclasses import dataclass
from urllib.parse import parse_qs, urlparse

from source_capture.adapters.cloakbrowser_snapshot import ScrollStopCondition
from source_capture.source_detail_sufficiency import (
    SourceDetailSufficiencyRequirements,
    validate_source_detail_sufficiency_requirements,
)


RETAIL_CAPTURE_PROFILE_SCHEMA_VERSION = 2


_AMAZON_ASIN_IN_PATH = re.compile(r"/(?:dp|gp/product|gp/aw/d)/([A-Za-z0-9]{10})(?:[/?]|$)")


def extract_amazon_asin_from_url(url: str) -> str | None:
    match = _AMAZON_ASIN_IN_PATH.search(urlparse(url).path)
    return match.group(1) if match else None


def extract_amazon_search_query_from_url(url: str) -> str | None:
    values = parse_qs(urlparse(url).query).get("k")
    if not values or not values[0].strip():
        return None
    return values[0].strip()


@dataclass(frozen=True)
class RetailCaptureProfile:
    name: str
    retailer: str
    page_kind: str
    hostname: str
    source_surface: str
    ordinary_operation: bool
    requirements: SourceDetailSufficiencyRequirements
    wait_until: str = "load"
    settle_seconds: float = 0.0
    scroll_passes: int = 0
    scroll_step_px: int = 0
    scroll_target_selector: str | None = None
    block_heavy_assets: bool = False
    derive_target_asin_from_url: bool = False
    derive_target_query_from_url: bool = False

    def requirements_for_capture(self, *, url: str) -> SourceDetailSufficiencyRequirements:
        """Sufficiency requirements for one capture, with any per-target identity resolved.

        Structural/block-detection literals stay fixed on the profile. A per-target
        identity check is layered on top from ``url`` (rather than a hardcoded canary
        product) so the gate validates the SKU/query actually being captured:

        - ``derive_target_asin_from_url``: single-SKU PDP pages. The ASIN in ``url``
          (``.../dp/<ASIN>`` or ``.../gp/product/<ASIN>``) must appear in the rendered DOM.
        - ``derive_target_query_from_url``: search-results grid pages. The ``k`` query
          parameter in ``url`` must appear in the rendered visible text (Amazon's own
          "1-N of M results for '<query>'" banner echoes it back), proving the grid
          rendered real results for the query actually searched rather than a block page
          or unrelated content.
        """
        if self.derive_target_asin_from_url:
            asin = extract_amazon_asin_from_url(url)
            if asin is None:
                raise ValueError(
                    f"retail capture profile {self.name} requires an Amazon ASIN in --url "
                    f"(expected .../dp/<ASIN> or .../gp/product/<ASIN>); got {url!r}"
                )
            target_identity = SourceDetailSufficiencyRequirements(
                rendered_dom_regexes=(re.escape(asin),),
            )
            return merge_source_detail_sufficiency_requirements(self.requirements, target_identity)
        if self.derive_target_query_from_url:
            query = extract_amazon_search_query_from_url(url)
            if query is None:
                raise ValueError(
                    f"retail capture profile {self.name} requires a non-empty Amazon search "
                    f"query in --url (expected .../s?k=<query>); got {url!r}"
                )
            target_identity = SourceDetailSufficiencyRequirements(
                visible_text_regexes=(f"(?i){re.escape(query)}",),
            )
            return merge_source_detail_sufficiency_requirements(self.requirements, target_identity)
        return self.requirements

    def scroll_stop_condition(self) -> ScrollStopCondition | None:
        if self.source_surface != "cloakbrowser_snapshot":
            return None
        if (
            not self.requirements.visible_text_contains
            and not self.requirements.visible_text_regexes
        ):
            return None
        return ScrollStopCondition(
            visible_text_contains=self.requirements.visible_text_contains,
            visible_text_regexes=self.requirements.visible_text_regexes,
        )

    def metadata(self) -> dict[str, object]:
        return {
            "schema_version": RETAIL_CAPTURE_PROFILE_SCHEMA_VERSION,
            "name": self.name,
            "retailer": self.retailer,
            "page_kind": self.page_kind,
            "expected_route_flags": {
                "hostname": self.hostname,
                "source_family": "retail_pdp",
                "source_surface": self.source_surface,
                "ordinary_operation": self.ordinary_operation,
                "wait_until": self.wait_until,
                "settle_seconds": self.settle_seconds,
                "scroll_passes": self.scroll_passes,
                "scroll_step_px": self.scroll_step_px,
                "scroll_target_selector": self.scroll_target_selector,
                "block_heavy_assets": self.block_heavy_assets,
            },
        }


def _requirements(
    *,
    visible_text_contains: tuple[str, ...] = (),
    visible_text_regexes: tuple[str, ...] = (),
    rendered_dom_contains: tuple[str, ...] = (),
    rendered_dom_regexes: tuple[str, ...] = (),
) -> SourceDetailSufficiencyRequirements:
    requirements = SourceDetailSufficiencyRequirements(
        require_not_access_blocked=True,
        min_visible_text_bytes=20,
        visible_text_contains=visible_text_contains,
        visible_text_regexes=visible_text_regexes,
        rendered_dom_contains=rendered_dom_contains,
        rendered_dom_regexes=rendered_dom_regexes,
    )
    validate_source_detail_sufficiency_requirements(requirements)
    return requirements


_PROFILES = {
    profile.name: profile
    for profile in (
        RetailCaptureProfile(
            name="amazon_grid_aggregate",
            retailer="amazon",
            page_kind="grid_aggregate",
            hostname="www.amazon.com",
            source_surface="cloakbrowser_snapshot",
            ordinary_operation=True,
            wait_until="domcontentloaded",
            settle_seconds=0.0,
            derive_target_query_from_url=True,
            requirements=_requirements(
                visible_text_contains=("New York 10001",),
                visible_text_regexes=(
                    r"1-\d+ of \d+ results",
                    r"\d(?:\.\d)? out of 5 stars\s+\([\d.]+[KM]?\)",
                    r"\$\d+(?:\.\d{2})?",
                    r"\d+(?:\.\d+)?[KM]?\+ bought in past month",
                ),
            ),
        ),
        RetailCaptureProfile(
            name="amazon_pdp_aggregate",
            retailer="amazon",
            page_kind="pdp_aggregate",
            hostname="www.amazon.com",
            source_surface="cloakbrowser_snapshot",
            ordinary_operation=True,
            wait_until="domcontentloaded",
            settle_seconds=0.0,
            derive_target_asin_from_url=True,
            requirements=_requirements(
                visible_text_contains=("New York 10001",),
                visible_text_regexes=(
                    r"\d(?:\.\d)? out of 5 stars",
                    r"\$\d+(?:\.\d{2})?",
                    r"\d+(?:\.\d+)?[KM]?\+ bought in past month",
                    r"[\d,]+ global ratings",
                    r"(?:In Stock|Currently unavailable|Temporarily out of stock"
                    r"|Only \d+ left in stock)",
                ),
                rendered_dom_contains=(
                    'name="currencyOfPreference" value="USD"',
                    "/gp/customer-reviews/",
                ),
            ),
        ),
        RetailCaptureProfile(
            name="amazon_pdp_distribution",
            retailer="amazon",
            page_kind="pdp_distribution",
            hostname="www.amazon.com",
            source_surface="cloakbrowser_snapshot",
            ordinary_operation=True,
            wait_until="domcontentloaded",
            settle_seconds=0.0,
            derive_target_asin_from_url=True,
            requirements=_requirements(
                visible_text_contains=("New York 10001",),
                visible_text_regexes=(
                    r"\d(?:\.\d)? out of 5 stars",
                    r"\$\d+(?:\.\d{2})?",
                    r"\d+(?:\.\d+)?[KM]?\+ bought in past month",
                    r"[\d,]+ global ratings",
                    r"(?:In Stock|Currently unavailable|Temporarily out of stock"
                    r"|Only \d+ left in stock)",
                    r"(?s)5 star\s+\d+%\s+4 star\s+\d+%\s+3 star\s+\d+%"
                    r"\s+2 star\s+\d+%\s+1 star\s+\d+%",
                ),
                rendered_dom_contains=(
                    'name="currencyOfPreference" value="USD"',
                    "/gp/customer-reviews/",
                ),
                rendered_dom_regexes=(r"[\d,]+ customers mention",),
            ),
        ),
        RetailCaptureProfile(
            name="sephora_grid_aggregate",
            retailer="sephora",
            page_kind="grid_aggregate",
            hostname="www.sephora.com",
            source_surface="cloakbrowser_snapshot",
            ordinary_operation=True,
            settle_seconds=5.0,
            scroll_passes=1,
            scroll_step_px=350,
            requirements=_requirements(
                visible_text_contains=("Results for", "Quicklook", "Lip Sleeping Mask"),
                visible_text_regexes=(r"\d+\s+Results for", r"\$\d+\.\d{2}"),
            ),
        ),
        RetailCaptureProfile(
            name="sephora_pdp_aggregate",
            retailer="sephora",
            page_kind="pdp_aggregate",
            hostname="www.sephora.com",
            source_surface="cloakbrowser_snapshot",
            ordinary_operation=True,
            settle_seconds=5.0,
            scroll_passes=1,
            scroll_step_px=350,
            requirements=_requirements(
                visible_text_contains=("Lip Sleeping Mask", "Ratings & Reviews", "Color"),
                visible_text_regexes=(r"Ratings & Reviews \([^)]+\)", r"\$\d+\.\d{2}"),
            ),
        ),
        RetailCaptureProfile(
            name="sephora_pdp_distribution",
            retailer="sephora",
            page_kind="pdp_distribution",
            hostname="www.sephora.com",
            source_surface="cloakbrowser_snapshot",
            ordinary_operation=True,
            settle_seconds=5.0,
            scroll_passes=1,
            scroll_step_px=350,
            scroll_target_selector="#ratings-reviews-container",
            requirements=_requirements(
                visible_text_contains=(
                    "Lip Sleeping Mask",
                    "Ratings & Reviews",
                    "Color",
                    "Summary",
                    "Verified Purchase",
                ),
                visible_text_regexes=(
                    r"Ratings & Reviews \([^)]+\)",
                    r"(?s)Summary\s+5\s+4\s+3\s+2\s+1\s+\d",
                ),
            ),
        ),
        RetailCaptureProfile(
            name="luckyscent_pdp_aggregate",
            retailer="luckyscent",
            page_kind="pdp_aggregate",
            hostname="www.luckyscent.com",
            source_surface="cloakbrowser_snapshot",
            ordinary_operation=True,
            wait_until="domcontentloaded",
            settle_seconds=5.0,
            scroll_passes=4,
            scroll_step_px=500,
            requirements=_requirements(
                visible_text_contains=(
                    "Bread and Roses",
                    "Fragrance Notes",
                    "Customer Reviews",
                ),
                visible_text_regexes=(
                    r"(?s)Bread and Roses\s+Pearfat Parfum\s+\d(?:\.\d+)?\s+\(\d+\)\s+\$\d+",
                    r"(?s)Customer Reviews\s+\d(?:\.\d+)? out of 5",
                ),
                rendered_dom_contains=(
                    '"@type":"ProductGroup"',
                    'data-product-title="Bread and Roses"',
                ),
                rendered_dom_regexes=(
                    r'"hasVariant"\s*:\s*\[',
                    r'data-review-id="[^"]+"',
                ),
            ),
        ),
        RetailCaptureProfile(
            name="ulta_grid_aggregate",
            retailer="ulta",
            page_kind="grid_aggregate",
            hostname="www.ulta.com",
            source_surface="cloakbrowser_snapshot",
            ordinary_operation=False,
            settle_seconds=5.0,
            scroll_passes=1,
            requirements=_requirements(
                visible_text_contains=("Search Results", "Lip Mask", "Add to bag"),
                visible_text_regexes=(r"\d+\s+(?:Results|products)", r"\$\d+\.\d{2}"),
            ),
        ),
        RetailCaptureProfile(
            name="ulta_pdp_aggregate",
            retailer="ulta",
            page_kind="pdp_aggregate",
            hostname="www.ulta.com",
            source_surface="cloakbrowser_snapshot",
            ordinary_operation=True,
            settle_seconds=5.0,
            requirements=_requirements(
                visible_text_contains=("Night Shift Overnight Lip Mask", "Reviews", "Offers"),
                visible_text_regexes=(r"\d+(?:,\d+)* Reviews", r"\$\d+\.\d{2}"),
                rendered_dom_contains=("__APOLLO_STATE__",),
                rendered_dom_regexes=(r'"aggregateRating"',),
            ),
        ),
        RetailCaptureProfile(
            name="ulta_pdp_distribution",
            retailer="ulta",
            page_kind="pdp_distribution",
            hostname="www.ulta.com",
            source_surface="cloakbrowser_snapshot",
            ordinary_operation=True,
            settle_seconds=5.0,
            scroll_step_px=350,
            requirements=_requirements(
                visible_text_contains=(
                    "Night Shift Overnight Lip Mask",
                    "Reviews",
                    "RATINGS DISTRIBUTION",
                ),
                visible_text_regexes=(r"(?is)5 stars.*4 stars.*3 stars.*2 stars.*1 star",),
                rendered_dom_contains=("__APOLLO_STATE__",),
            ),
        ),
        RetailCaptureProfile(
            name="walmart_grid_aggregate",
            retailer="walmart",
            page_kind="grid_aggregate",
            hostname="www.walmart.com",
            source_surface="direct_http",
            ordinary_operation=True,
            requirements=_requirements(
                rendered_dom_contains=("__NEXT_DATA__",),
                rendered_dom_regexes=(r'"items"\s*:\s*\[\s*\{', r'"productId"'),
            ),
        ),
        RetailCaptureProfile(
            name="walmart_pdp_aggregate",
            retailer="walmart",
            page_kind="pdp_aggregate",
            hostname="www.walmart.com",
            source_surface="direct_http",
            ordinary_operation=True,
            requirements=_requirements(
                rendered_dom_contains=(
                    "__NEXT_DATA__",
                    "Vitamasques Cherry Vegan Collagen Lip Mask",
                ),
                rendered_dom_regexes=(r'"averageRating"\s*:', r'"numberOfReviews"\s*:'),
            ),
        ),
        RetailCaptureProfile(
            name="walmart_pdp_distribution",
            retailer="walmart",
            page_kind="pdp_distribution",
            hostname="www.walmart.com",
            source_surface="cloakbrowser_snapshot",
            ordinary_operation=True,
            settle_seconds=5.0,
            scroll_step_px=400,
            requirements=_requirements(
                visible_text_contains=(
                    "Vitamasques Cherry Vegan Collagen Lip Mask",
                    "Customer ratings & reviews",
                    "Pickup",
                    "Shipping",
                ),
                visible_text_regexes=(r"(?s)5 stars.*4 stars.*3 stars.*2 stars.*1 star",),
            ),
        ),
        RetailCaptureProfile(
            name="target_grid_aggregate",
            retailer="target",
            page_kind="grid_aggregate",
            hostname="www.target.com",
            source_surface="cloakbrowser_snapshot",
            ordinary_operation=True,
            settle_seconds=6.0,
            scroll_passes=1,
            requirements=_requirements(
                visible_text_contains=("results", "Guest Rating", "BYOMA Liptide Lip Mask"),
                visible_text_regexes=(r"\d+\s+results", r"\$\d+\.\d{2}"),
            ),
        ),
        RetailCaptureProfile(
            name="target_pdp_aggregate",
            retailer="target",
            page_kind="pdp_aggregate",
            hostname="www.target.com",
            source_surface="cloakbrowser_snapshot",
            ordinary_operation=True,
            settle_seconds=6.0,
            requirements=_requirements(
                visible_text_contains=("BYOMA Liptide Lip Mask", "reviews", "Pickup", "Shipping"),
                visible_text_regexes=(
                    r"\d(?:\.\d+)? out of 5 stars with \d+ reviews",
                    r"\$\d+\.\d{2}",
                ),
            ),
        ),
        RetailCaptureProfile(
            name="target_pdp_distribution",
            retailer="target",
            page_kind="pdp_distribution",
            hostname="www.target.com",
            source_surface="cloakbrowser_snapshot",
            ordinary_operation=True,
            settle_seconds=6.0,
            scroll_passes=1,
            requirements=_requirements(
                visible_text_contains=("BYOMA Liptide Lip Mask", "Guest ratings & reviews"),
                visible_text_regexes=(
                    r"(?s)5 stars\s+\d+%.*4 stars\s+\d+%.*3 stars\s+\d+%"
                    r".*2 stars\s+\d+%.*1 star\s+\d+%",
                ),
            ),
        ),
    )
}


def retail_capture_profile_names() -> tuple[str, ...]:
    return tuple(sorted(_PROFILES))


def get_retail_capture_profile(name: str) -> RetailCaptureProfile:
    try:
        return _PROFILES[name]
    except KeyError as exc:
        raise ValueError(f"unknown retail capture profile: {name}") from exc


def validate_retail_capture_profile_route(
    profile: RetailCaptureProfile,
    *,
    url: str,
    source_family: str,
    source_surface: str,
) -> None:
    hostname = (urlparse(url).hostname or "").lower()
    if hostname != profile.hostname:
        raise ValueError(
            f"retail capture profile {profile.name} requires hostname {profile.hostname}; "
            f"got {hostname or 'none'}"
        )
    if source_family != "retail_pdp":
        raise ValueError(
            f"retail capture profile {profile.name} requires source_family retail_pdp"
        )
    if source_surface != profile.source_surface:
        raise ValueError(
            f"retail capture profile {profile.name} requires source_surface "
            f"{profile.source_surface}; "
            f"got {source_surface}"
        )


def merge_source_detail_sufficiency_requirements(
    first: SourceDetailSufficiencyRequirements | None,
    second: SourceDetailSufficiencyRequirements | None,
) -> SourceDetailSufficiencyRequirements | None:
    if first is None:
        return second
    if second is None:
        return first

    def unique(values: tuple[str, ...]) -> tuple[str, ...]:
        return tuple(dict.fromkeys(values))

    minimums = [
        value
        for value in (first.min_visible_text_bytes, second.min_visible_text_bytes)
        if value is not None
    ]
    merged = SourceDetailSufficiencyRequirements(
        require_not_access_blocked=(
            first.require_not_access_blocked or second.require_not_access_blocked
        ),
        min_visible_text_bytes=max(minimums) if minimums else None,
        visible_text_contains=unique(first.visible_text_contains + second.visible_text_contains),
        visible_text_regexes=unique(first.visible_text_regexes + second.visible_text_regexes),
        rendered_dom_contains=unique(first.rendered_dom_contains + second.rendered_dom_contains),
        rendered_dom_regexes=unique(first.rendered_dom_regexes + second.rendered_dom_regexes),
    )
    validate_source_detail_sufficiency_requirements(merged)
    return merged
