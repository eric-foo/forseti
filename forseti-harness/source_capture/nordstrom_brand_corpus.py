"""Fail-closed projection and corpus receipts for public Nordstrom brand capture."""

from __future__ import annotations

import hashlib
import html
import json
import re
from pathlib import Path
from urllib.parse import urljoin, urlparse

from pydantic import Field

from schemas.case_models import StrictModel
from source_capture.adapters.nordstrom_country_preference import (
    confirm_nordstrom_us_storefront,
    observe_nordstrom_deep_review_window,
)
from source_capture.models import VisibleFactStatus
from source_capture.retail_grid_projection import (
    load_verified_source_capture_packet_directory,
)


NORDSTROM_GRID_PARSER_VERSION = "nordstrom_brand_grid_v1"
NORDSTROM_CORPUS_SCHEMA_VERSION = "nordstrom_brand_corpus_v1"
NORDSTROM_DEEP_CAPTURE_LIMIT = 100
_PRODUCT_URL = re.compile(r"/s/[^\"'?#]+/(\d{7})(?:[?\"'#]|$)", re.I)


class NordstromGridCard(StrictModel):
    position: int
    product_id: str
    product_url: str
    brand_name: str
    product_name: str
    review_count: int
    rating: float | None = None


class NordstromGridProjection(StrictModel):
    schema_version: str = NORDSTROM_GRID_PARSER_VERSION
    source_url: str
    brand_name: str
    brand_id: str
    declared_count: int
    cards: list[NordstromGridCard]
    status: str
    residuals: list[str] = Field(default_factory=list)


class NordstromPdpEvidence(StrictModel):
    product_id: str
    source_url: str
    final_url: str
    brand_name: str
    product_name: str
    seller: str
    country_code: str = "US"
    currency_code: str = "USD"
    packet_directory: str
    manifest_sha256: str
    rendered_dom_sha256: str


class NordstromReviewRow(StrictModel):
    position: int
    review_id: str
    source_row_id: str
    source_url: str
    content_sha256: str


class NordstromReviewOrderReceipt(StrictModel):
    requested_sort: str
    observed_sort: str
    source_url: str
    source_total_count: int | None
    observed_row_count: int
    retained_row_count: int
    continuation_available: bool
    continuation_activations: int
    rows: list[NordstromReviewRow]
    rendered_dom_sha256: str
    status: str
    shortfalls: list[str] = Field(default_factory=list)


class NordstromDeepPdpReceipt(StrictModel):
    product_id: str
    source_url: str
    selection_basis: str
    most_helpful: NordstromReviewOrderReceipt
    most_recent: NordstromReviewOrderReceipt
    status: str
    residuals: list[str] = Field(default_factory=list)


class NordstromCorpusReceipt(StrictModel):
    schema_version: str = NORDSTROM_CORPUS_SCHEMA_VERSION
    brand_name: str
    grid_product_count: int
    unique_grid_product_count: int
    pdp_count: int
    seller: str
    country_code: str
    currency_code: str
    deep_product_id: str
    status: str
    residuals: list[str] = Field(default_factory=list)


def build_nordstrom_grid_projection(
    *, rendered_dom: str, source_url: str
) -> NordstromGridProjection:
    """Project the terminal brand grid and reconcile declared/card/identity counts."""
    subject = re.search(r"/brands/([a-z0-9-]+)--(\d+)", urlparse(source_url).path, re.I)
    if subject is None:
        raise ValueError("Nordstrom brand URL does not expose slug and brand id")
    declared = re.search(r"\b(\d+)\s+items\b", _text(rendered_dom), re.I)
    if declared is None:
        raise ValueError("Nordstrom grid does not expose a declared item count")
    cards: list[NordstromGridCard] = []
    articles = re.findall(r"<article\b[\s\S]*?</article>", rendered_dom, re.I)
    for article in articles:
        url_match = _PRODUCT_URL.search(article)
        if url_match is None:
            continue
        product_id = url_match.group(1)
        href_match = re.search(
            rf'href=["\']([^"\']*/{re.escape(product_id)}(?:\?[^"\']*)?)["\']',
            article,
            re.I,
        )
        heading = re.search(r"<h3\b[\s\S]*?</h3>", article, re.I)
        name_text = _text(heading.group(0)) if heading else ""
        brand_match = re.match(r"([A-Z][A-Z0-9 &'+.-]+)\s+(.+)", name_text)
        if brand_match is None:
            continue
        review_match = re.search(
            r'aria-label=["\'](\d(?:\.\d+)?) out of 5 stars["\'][\s\S]{0,300}?'
            r">\s*\(([\d,]+)\)",
            article,
            re.I,
        )
        cards.append(
            NordstromGridCard(
                position=len(cards) + 1,
                product_id=product_id,
                product_url=urljoin(
                    "https://www.nordstrom.com",
                    html.unescape(href_match.group(1)) if href_match else "",
                ),
                brand_name=brand_match.group(1).strip(),
                product_name=brand_match.group(2).strip(),
                review_count=(
                    int(review_match.group(2).replace(",", "")) if review_match else 0
                ),
                rating=float(review_match.group(1)) if review_match else None,
            )
        )
    declared_count = int(declared.group(1))
    residuals: list[str] = []
    ids = [card.product_id for card in cards]
    if declared_count != len(cards):
        residuals.append(
            f"declared_count={declared_count} differs from card_count={len(cards)}"
        )
    if len(set(ids)) != len(ids):
        residuals.append("grid contains duplicate product ids")
    brand_name = subject.group(1).replace("-", " ").upper()
    mismatches = [card.product_id for card in cards if card.brand_name != brand_name]
    if mismatches:
        residuals.append(f"brand mismatch on product ids: {','.join(mismatches)}")
    return NordstromGridProjection(
        source_url=source_url,
        brand_name=brand_name,
        brand_id=subject.group(2),
        declared_count=declared_count,
        cards=cards,
        status="complete" if not residuals else "partial",
        residuals=residuals,
    )


def load_verified_rendered_dom(packet_directory: Path) -> tuple[object, str, str]:
    """Load a hash-verified packet and its sole rendered DOM."""
    packet, bodies = load_verified_source_capture_packet_directory(packet_directory)
    rendered = [
        item
        for item in packet.preserved_files
        if item.relative_packet_path.replace("\\", "/").endswith(
            "cloakbrowser_rendered_dom.html"
        )
    ]
    if len(rendered) != 1 or rendered[0].file_id not in bodies:
        raise ValueError("packet must retain exactly one verified rendered DOM")
    body = bodies[rendered[0].file_id]
    return packet, body.decode("utf-8", errors="replace"), hashlib.sha256(body).hexdigest()


def load_nordstrom_grid_packet(
    *, packet_directory: Path, requested_url: str
) -> NordstromGridProjection:
    packet, rendered_dom, _ = load_verified_rendered_dom(packet_directory)
    if packet.source_locator.status != VisibleFactStatus.KNOWN:
        raise ValueError("grid packet source locator is not known")
    if _canonical_url(str(packet.source_locator.value)) != _canonical_url(requested_url):
        raise ValueError("grid packet does not bind the requested brand URL")
    confirmation = confirm_nordstrom_us_storefront(rendered_dom)
    if not confirmation.confirmed:
        raise ValueError(f"grid packet is not confirmed US/USD: {confirmation.detail}")
    projection = build_nordstrom_grid_projection(
        rendered_dom=rendered_dom, source_url=requested_url
    )
    if projection.status != "complete":
        raise ValueError("; ".join(projection.residuals))
    return projection


def build_nordstrom_pdp_evidence(
    *, packet_directory: Path, expected_product_id: str, expected_brand: str
) -> NordstromPdpEvidence:
    packet, dom, dom_sha256 = load_verified_rendered_dom(packet_directory)
    final_url = str(packet.source_locator.value or "")
    match = _PRODUCT_URL.search(urlparse(final_url).path + "?")
    if match is None or match.group(1) != expected_product_id:
        raise ValueError("PDP final URL does not bind the expected product id")
    confirmation = confirm_nordstrom_us_storefront(dom)
    if not confirmation.confirmed:
        raise ValueError(f"PDP is not confirmed US/USD: {confirmation.detail}")
    seller_match = re.search(r"\bSold by\s+([^<\n]+)", dom, re.I)
    seller = _text(seller_match.group(1)) if seller_match else ""
    if seller != "Nordstrom":
        raise ValueError(f"unexpected PDP seller {seller!r}")
    product = _product_json_ld(dom, expected_product_id)
    brand = _json_ld_brand(product)
    if brand.casefold() != expected_brand.casefold():
        raise ValueError(f"unexpected PDP brand {brand!r}")
    product_name = str(product.get("name") or "").strip()
    if not product_name:
        raise ValueError("PDP Product JSON-LD has no name")
    manifest_path = packet_directory / "manifest.json"
    return NordstromPdpEvidence(
        product_id=expected_product_id,
        source_url=final_url,
        final_url=final_url,
        brand_name=brand,
        product_name=product_name,
        seller=seller,
        packet_directory=str(packet_directory.resolve()),
        manifest_sha256=_sha256_path(manifest_path),
        rendered_dom_sha256=dom_sha256,
    )


def build_nordstrom_review_order_receipt(
    *, packet_directory: Path, requested_sort: str, limit: int = 100
) -> NordstromReviewOrderReceipt:
    packet, dom, dom_sha256 = load_verified_rendered_dom(packet_directory)
    observation = observe_nordstrom_deep_review_window(
        dom,
        requested_sort=requested_sort,
        limit=NORDSTROM_DEEP_CAPTURE_LIMIT,
    )
    if observation["admitted"] is not True:
        raise ValueError(
            f"{requested_sort} deep window not admitted: {observation['status']}"
        )
    source_url = str(packet.source_locator.value or "")
    review_start = dom.find('id="product-page-reviews"')
    review_html = dom[review_start:]
    starts = list(
        re.finditer(
            r'<div\b[^>]*\bid=["\']review-(\d+)["\'][^>]*>',
            review_html,
            re.I,
        )
    )
    rows: list[NordstromReviewRow] = []
    for index, start in enumerate(starts[:limit]):
        end = starts[index + 1].start() if index + 1 < len(starts) else len(review_html)
        normalized = " ".join(_text(review_html[start.start() : end]).split())
        digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
        rows.append(
            NordstromReviewRow(
                position=index + 1,
                review_id=f"sha256:{digest}",
                source_row_id=f"review-{start.group(1)}",
                source_url=f"{source_url}#product-page-reviews",
                content_sha256=digest,
            )
        )
    shortfalls: list[str] = []
    if len(rows) < limit:
        shortfalls.append(
            f"source exhausted at {len(rows)} rows before requested limit {limit}"
        )
    return NordstromReviewOrderReceipt(
        requested_sort=requested_sort,
        observed_sort=requested_sort,
        source_url=source_url,
        source_total_count=observation["source_total_count"],
        observed_row_count=int(observation["captured_review_count"]),
        retained_row_count=len(rows),
        continuation_available=bool(observation["continuation_available"]),
        continuation_activations=int(observation["continuation_activations"]),
        rows=rows,
        rendered_dom_sha256=dom_sha256,
        status="complete",
        shortfalls=shortfalls,
    )


def verify_nordstrom_corpus(
    *,
    grid: NordstromGridProjection,
    pdps: list[NordstromPdpEvidence],
    deep: NordstromDeepPdpReceipt,
) -> NordstromCorpusReceipt:
    residuals: list[str] = []
    grid_ids = [card.product_id for card in grid.cards]
    pdp_ids = [pdp.product_id for pdp in pdps]
    if grid.status != "complete":
        residuals.append("grid projection is incomplete")
    if len(pdp_ids) != len(grid_ids) or set(pdp_ids) != set(grid_ids):
        residuals.append("PDP identities are not an exact one-to-one grid match")
    if len(set(pdp_ids)) != len(pdp_ids):
        residuals.append("duplicate PDP identities")
    if any(pdp.seller != "Nordstrom" for pdp in pdps):
        residuals.append("one or more PDP sellers are not Nordstrom")
    candidate = min(
        grid.cards, key=lambda card: (-card.review_count, card.position, card.product_id)
    )
    if deep.product_id != candidate.product_id:
        residuals.append("deep PDP is not the deterministic highest-review grid candidate")
    if deep.status != "complete":
        residuals.append("deep PDP receipt is incomplete")
    return NordstromCorpusReceipt(
        brand_name=grid.brand_name,
        grid_product_count=len(grid_ids),
        unique_grid_product_count=len(set(grid_ids)),
        pdp_count=len(pdp_ids),
        seller="Nordstrom",
        country_code="US",
        currency_code="USD",
        deep_product_id=deep.product_id,
        status="complete" if not residuals else "partial",
        residuals=residuals,
    )


def _product_json_ld(dom: str, product_id: str) -> dict[str, object]:
    products: dict[str, dict[str, object]] = {}
    for script in re.findall(
        r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>'
        r"([\s\S]*?)</script>",
        dom,
        re.I,
    ):
        try:
            root = json.loads(html.unescape(script))
        except (TypeError, ValueError):
            continue
        pending = [root]
        while pending:
            item = pending.pop()
            if isinstance(item, list):
                pending.extend(item)
            elif isinstance(item, dict):
                pending.extend(item.values())
                types = item.get("@type")
                if (
                    types == "Product"
                    or isinstance(types, list)
                    and "Product" in types
                ):
                    serialized = json.dumps(item, sort_keys=True)
                    products[serialized] = item
                    if f"/{product_id}" in serialized:
                        return item
    if len(products) == 1:
        return next(iter(products.values()))
    raise ValueError("target Product JSON-LD is absent")


def _json_ld_brand(product: dict[str, object]) -> str:
    brand = product.get("brand")
    if isinstance(brand, dict):
        return str(brand.get("name") or "").strip()
    return str(brand or "").strip()


def _text(value: str) -> str:
    return " ".join(
        html.unescape(re.sub(r"<[^>]+>", " ", value or "")).split()
    )


def _canonical_url(value: str) -> str:
    parsed = urlparse(value)
    return f"https://www.nordstrom.com{parsed.path.rstrip('/')}"


def _sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
