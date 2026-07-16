"""Fragrance purchase-review product discovery (route-hardening core).

Network-free logic for finding review-positive product PDPs per locked retailer,
so the rendered+widget companion no longer needs hand-fed URLs. Two vendor paths:

- Judge.me (Ministry, Luckyscent, Twisted Lily, Indigo): no public shop-level
  feed exists, so discovery enumerates products (Shopify ``products.json`` or the
  storefront sitemap) and probes the per-product widget for a review count, under
  a rate-limiter policy that respects Judge.me's burst throttling.
- Yotpo (ZGO): a public store-level reviews feed lists reviewed products
  directly, so discovery pages that feed and maps Yotpo product ids to Shopify
  ids / PDP URLs without per-product probing.

This module performs NO network I/O at import or call time; callers inject
``fetch_*`` callables (see ``source_capture/adapters/fragrance_discovery_fetch.py``)
so the core stays unit-testable and import-clean for the source-capture
no-runtime-imports contract. It discovers candidate review-positive PDPs only;
it does not capture rows, persist review bodies, score, or promote registry
fixtures.
"""
from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import Callable, Literal, Mapping, Sequence

from pydantic import Field

from schemas.case_models import StrictModel

FRAGRANCE_REVIEW_DISCOVERY_METHOD = "fragrance_review_discovery"
FRAGRANCE_REVIEW_DISCOVERY_VERSION = "v0"

# Throttle sentinel returned by an injected count fetcher when the widget host
# rate-limits the probe (distinct from "0 reviews", which is a real count).
THROTTLE = "THROTTLE"


class FragranceReviewDiscoveryInputError(ValueError):
    """A discovery input cannot be parsed without losing honesty."""


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------
class ProductRef(StrictModel):
    product_url: str
    handle: str | None = None
    shopify_product_id: str | None = None
    title: str | None = None


class ReviewPositiveCandidate(StrictModel):
    source_id: str
    vendor: Literal["judgeme", "yotpo"]
    product_url: str
    review_count: int = Field(ge=1)
    product_id: str | None = None
    title: str | None = None
    basis: str  # judgeme_widget_probe | yotpo_shop_feed


class DiscoveryReceipt(StrictModel):
    discovery_method: Literal["fragrance_review_discovery"] = FRAGRANCE_REVIEW_DISCOVERY_METHOD
    discovery_version: Literal["v0"] = FRAGRANCE_REVIEW_DISCOVERY_VERSION
    source_id: str
    vendor: Literal["judgeme", "yotpo"]
    candidates: list[ReviewPositiveCandidate] = Field(default_factory=list)
    enumerated: int = Field(ge=0, default=0)
    probed: int = Field(ge=0, default=0)
    zero_count: int = Field(ge=0, default=0)
    throttled: int = Field(ge=0, default=0)
    missing_product_id: int = Field(ge=0, default=0)
    feed_total_reviews: int | None = None
    feed_pages_read: int = Field(ge=0, default=0)
    residuals: list[str] = Field(default_factory=list)
    non_claims: list[str] = Field(
        default_factory=lambda: [
            "not source-wide review coverage",
            "not a review capture (rows/bodies)",
            "not registry promotion of any candidate",
            "not ECR, Cleaning, Judgment, or scoring",
        ]
    )


# ---------------------------------------------------------------------------
# Shopify storefront enumeration (pure)
# ---------------------------------------------------------------------------
def parse_shopify_products_json(text: str, *, store_domain: str) -> list[ProductRef]:
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise FragranceReviewDiscoveryInputError("products.json is not parseable JSON") from exc
    products = data.get("products") if isinstance(data, Mapping) else None
    if not isinstance(products, list):
        return []
    base = _store_base(store_domain)
    refs: list[ProductRef] = []
    for product in products:
        if not isinstance(product, Mapping):
            continue
        handle = product.get("handle")
        if not handle:
            continue
        pid = product.get("id")
        refs.append(
            ProductRef(
                product_url=f"{base}/products/{handle}",
                handle=str(handle),
                shopify_product_id=str(pid) if pid is not None else None,
                title=_str_or_none(product.get("title")),
            )
        )
    return refs


def parse_sitemap_locs(xml_text: str) -> list[str]:
    """All ``<loc>`` values from a sitemap or sitemapindex (namespace-agnostic)."""
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as exc:
        raise FragranceReviewDiscoveryInputError("sitemap is not parseable XML") from exc
    locs: list[str] = []
    for el in root.iter():
        if el.tag.endswith("}loc") or el.tag == "loc":
            if el.text and el.text.strip():
                locs.append(el.text.strip())
    return locs


def select_product_sitemap_locs(locs: Sequence[str]) -> list[str]:
    """Sub-sitemap URLs that look product-scoped, from a sitemapindex."""
    return [u for u in locs if "product" in u.lower()]


def select_product_refs_from_sitemap(locs: Sequence[str]) -> list[ProductRef]:
    """Product PDP URLs (``/products/<handle>``) from a urlset's locs."""
    refs: list[ProductRef] = []
    seen: set[str] = set()
    for url in locs:
        if "/products/" not in url:
            continue
        tail = url.split("/products/", 1)[1].split("?", 1)[0].split("#", 1)[0].rstrip("/")
        if not tail or "/" in tail:
            continue
        if url in seen:
            continue
        seen.add(url)
        refs.append(ProductRef(product_url=url, handle=tail))
    return refs


# ---------------------------------------------------------------------------
# Judge.me review-count signal + product-id extraction (pure)
# ---------------------------------------------------------------------------
def judgeme_count_from_response(parsed: Mapping[str, object]) -> int | None:
    """Review total from a Judge.me reviews_for_widget response.

    Shop responses vary: some expose ``total_count``, others ``number_of_reviews``.
    Mirrors the companion's multi-field logic so discovery never undercounts.
    """
    for key in ("total_count", "number_of_reviews"):
        value = _int_or_none(parsed.get(key))
        if value is not None:
            return value
    pagination = parsed.get("pagination")
    if isinstance(pagination, Mapping):
        value = _int_or_none(pagination.get("total"))
        if value is not None:
            return value
    bottomline = parsed.get("bottomline")
    if isinstance(bottomline, Mapping):
        for key in ("totalReview", "totalReviews"):
            value = _int_or_none(bottomline.get(key))
            if value is not None:
                return value
    return None


_JUDGEME_PID_PATTERNS = (
    re.compile(r'data-product-id=["\'](\d{6,14})["\']'),
    re.compile(r'data-product=["\'](\d{6,14})["\']'),
    re.compile(r"gid://shopify/Product/(\d{6,14})"),
    re.compile(r'["\']?product_id["\']?\s*[:=]\s*["\']?(\d{6,14})'),
)


def extract_judgeme_product_id(html: str) -> str | None:
    """Best-effort Shopify product id from PDP HTML (for sitemap-only storefronts)."""
    for pattern in _JUDGEME_PID_PATTERNS:
        match = pattern.search(html)
        if match:
            return match.group(1)
    return None


# ---------------------------------------------------------------------------
# Yotpo shop-level feed (pure)
# ---------------------------------------------------------------------------
class YotpoShopFeedPage(StrictModel):
    page: int | None = None
    per_page: int | None = None
    total_reviews: int | None = None
    # Shopify product id -> reviews seen for it on this page.
    product_review_counts: dict[str, int] = Field(default_factory=dict)
    # Shopify product id -> product name.
    product_names: dict[str, str] = Field(default_factory=dict)


def parse_yotpo_shop_feed_page(parsed: Mapping[str, object]) -> YotpoShopFeedPage:
    yotpo_to_shopify: dict[str, str] = {}
    names: dict[str, str] = {}
    products = parsed.get("products")
    if isinstance(products, list):
        for product in products:
            if not isinstance(product, Mapping):
                continue
            yotpo_id = product.get("id")
            shopify_id = product.get("domainKey")
            if yotpo_id is None or not shopify_id:
                continue
            yotpo_to_shopify[str(yotpo_id)] = str(shopify_id)
            name = _str_or_none(product.get("name"))
            if name:
                names[str(shopify_id)] = name
    counts: dict[str, int] = {}
    reviews = parsed.get("reviews")
    if isinstance(reviews, list):
        for review in reviews:
            if not isinstance(review, Mapping):
                continue
            shopify_id = yotpo_to_shopify.get(str(review.get("product_id")))
            if shopify_id:
                counts[shopify_id] = counts.get(shopify_id, 0) + 1
    pagination = parsed.get("pagination") if isinstance(parsed.get("pagination"), Mapping) else {}
    return YotpoShopFeedPage(
        page=_int_or_none(pagination.get("page")),
        per_page=_int_or_none(pagination.get("perPage")),
        total_reviews=_int_or_none(pagination.get("total")),
        product_review_counts=counts,
        product_names=names,
    )


# ---------------------------------------------------------------------------
# Rate-limiter policy (pure): min spacing + exponential backoff on throttle
# ---------------------------------------------------------------------------
@dataclass
class RateLimiterPolicy:
    min_interval_s: float = 6.0
    backoff_factor: float = 2.0
    max_interval_s: float = 60.0
    _interval: float = field(init=False, default=0.0)

    def __post_init__(self) -> None:
        if self.min_interval_s <= 0:
            raise FragranceReviewDiscoveryInputError("min_interval_s must be > 0")
        self._interval = self.min_interval_s

    @property
    def interval_s(self) -> float:
        return self._interval

    def on_ok(self) -> float:
        self._interval = self.min_interval_s
        return self._interval

    def on_throttle(self) -> float:
        self._interval = min(self.max_interval_s, max(self.min_interval_s, self._interval) * self.backoff_factor)
        return self._interval


# ---------------------------------------------------------------------------
# Orchestration (network injected via callables)
# ---------------------------------------------------------------------------
def discover_judgeme_by_probe(
    *,
    source_id: str,
    shop_domain: str,
    product_refs: Sequence[ProductRef],
    fetch_count: Callable[[str, str], object],
    sleeper: Callable[[float], None],
    policy: RateLimiterPolicy | None = None,
    max_probes: int = 60,
    find_target: int = 2,
    exclude_handles: Sequence[str] = (),
    resolve_product_id: Callable[[ProductRef], str | None] | None = None,
) -> DiscoveryReceipt:
    """Cadence-controlled per-product Judge.me probing.

    ``fetch_count(shop_domain, product_id)`` returns an int count, ``None`` (no
    count field), or ``THROTTLE``. The sleeper applies the policy's spacing
    between calls and the backoff interval after a throttle. When a ref carries
    no ``shopify_product_id`` (e.g. sitemap-only storefronts), the optional
    ``resolve_product_id`` is called lazily — only for refs actually reached —
    to recover the id from the PDP before probing.
    """
    policy = policy or RateLimiterPolicy()
    excluded = set(exclude_handles)
    found: list[ReviewPositiveCandidate] = []
    probed = zeros = throttled = missing_id = 0
    residuals: list[str] = []
    for ref in product_refs:
        if probed >= max_probes or len(found) >= find_target:
            break
        if ref.handle is not None and ref.handle in excluded:
            continue
        product_id = ref.shopify_product_id
        if product_id is None and resolve_product_id is not None:
            product_id = resolve_product_id(ref)
        if product_id is None:
            missing_id += 1
            continue
        probed += 1
        result = fetch_count(shop_domain, product_id)
        if result == THROTTLE:
            throttled += 1
            sleeper(policy.on_throttle())
            continue
        count = result if isinstance(result, int) else None
        if count is not None and count > 0:
            found.append(
                ReviewPositiveCandidate(
                    source_id=source_id,
                    vendor="judgeme",
                    product_url=ref.product_url,
                    review_count=count,
                    product_id=product_id,
                    title=ref.title,
                    basis="judgeme_widget_probe",
                )
            )
        else:
            zeros += 1
        sleeper(policy.on_ok())
    found.sort(key=lambda candidate: candidate.review_count, reverse=True)
    if throttled and not found:
        residuals.append("judgeme_probe_throttled_no_candidate")
    if not found:
        residuals.append("new_pdp_not_found_in_bounded_probe")
    return DiscoveryReceipt(
        source_id=source_id,
        vendor="judgeme",
        candidates=found,
        enumerated=len(product_refs),
        probed=probed,
        zero_count=zeros,
        throttled=throttled,
        missing_product_id=missing_id,
        residuals=residuals,
    )


def discover_yotpo_shop_feed(
    *,
    source_id: str,
    fetch_feed_page: Callable[[int], Mapping[str, object] | None],
    shopify_id_to_url: Mapping[str, str],
    max_pages: int = 5,
    find_target: int = 2,
    exclude_product_ids: Sequence[str] = (),
) -> DiscoveryReceipt:
    """Page the Yotpo store reviews feed and emit reviewed-product candidates.

    ``fetch_feed_page(page)`` returns the parsed feed JSON (or ``None`` to stop).
    ``shopify_id_to_url`` resolves a Shopify product id to its PDP URL (built by
    the caller from the storefront's products.json); ids that cannot be resolved
    are counted as a residual rather than guessed.
    """
    excluded = set(exclude_product_ids)
    counts: dict[str, int] = {}
    names: dict[str, str] = {}
    total_reviews: int | None = None
    pages_read = 0
    residuals: list[str] = []
    for page in range(1, max_pages + 1):
        parsed = fetch_feed_page(page)
        if not isinstance(parsed, Mapping):
            break
        feed = parse_yotpo_shop_feed_page(parsed)
        pages_read += 1
        if feed.total_reviews is not None:
            total_reviews = feed.total_reviews
        for shopify_id, count in feed.product_review_counts.items():
            counts[shopify_id] = counts.get(shopify_id, 0) + count
        names.update(feed.product_names)
        resolvable = [pid for pid in counts if pid not in excluded and pid in shopify_id_to_url]
        if len(resolvable) >= find_target:
            break
    candidates: list[ReviewPositiveCandidate] = []
    unresolved = 0
    for shopify_id, count in counts.items():
        if shopify_id in excluded:
            continue
        url = shopify_id_to_url.get(shopify_id)
        if not url:
            unresolved += 1
            continue
        candidates.append(
            ReviewPositiveCandidate(
                source_id=source_id,
                vendor="yotpo",
                product_url=url,
                review_count=count,
                product_id=shopify_id,
                title=names.get(shopify_id),
                basis="yotpo_shop_feed",
            )
        )
    candidates.sort(key=lambda candidate: candidate.review_count, reverse=True)
    if unresolved:
        residuals.append(f"yotpo_feed_products_unresolved_to_pdp_url:{unresolved}")
    if not candidates:
        residuals.append("new_pdp_not_found_in_shop_feed")
    return DiscoveryReceipt(
        source_id=source_id,
        vendor="yotpo",
        candidates=candidates[:find_target] if find_target > 0 else candidates,
        enumerated=len(counts),
        feed_total_reviews=total_reviews,
        feed_pages_read=pages_read,
        residuals=residuals,
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _store_base(store_domain: str) -> str:
    domain = store_domain.strip().rstrip("/")
    if domain.startswith("http://") or domain.startswith("https://"):
        return domain
    return f"https://{domain}"


def _int_or_none(value: object) -> int | None:
    # helper-delta: int(float(...)) truncation accepts bool/signed/decimal strings, unlike harness_utils.int_or_none.
    if value is None or value == "":
        return None
    try:
        return int(float(str(value).replace(",", "")))
    except (TypeError, ValueError):
        return None


def _str_or_none(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


__all__ = [
    "FRAGRANCE_REVIEW_DISCOVERY_METHOD",
    "FRAGRANCE_REVIEW_DISCOVERY_VERSION",
    "THROTTLE",
    "DiscoveryReceipt",
    "FragranceReviewDiscoveryInputError",
    "ProductRef",
    "RateLimiterPolicy",
    "ReviewPositiveCandidate",
    "YotpoShopFeedPage",
    "discover_judgeme_by_probe",
    "discover_yotpo_shop_feed",
    "extract_judgeme_product_id",
    "judgeme_count_from_response",
    "parse_shopify_products_json",
    "parse_sitemap_locs",
    "parse_yotpo_shop_feed_page",
    "select_product_refs_from_sitemap",
    "select_product_sitemap_locs",
]
