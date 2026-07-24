"""Strict parsing of Sephora's retailer-owned ``/shop/`` catalog grids."""

from __future__ import annotations

import html as html_module
import json
import re
from dataclasses import dataclass
from html.parser import HTMLParser
from typing import Any, Iterable, Iterator
from urllib.parse import parse_qs, urlparse


SEPHORA_CATALOG_GRID_CONTENT_RECORD_VERSION = "sephora_catalog_grid_content_v1"
SEPHORA_CATALOG_PAGE_SIZE = 60
SEPHORA_CATALOG_MAX_PAGE = 12
_SEPHORA_HOSTS = frozenset({"sephora.com", "www.sephora.com"})
_PRODUCT_ANCHOR_RE = re.compile(
    r"<a\b(?P<attrs>(?=[^>]*\bdata-cnstrc-item-id=[\"'][^\"']+[\"'])[^>]*)>",
    flags=re.IGNORECASE,
)
_VISIBLE_RANGE_RE = re.compile(
    r"\b(?P<start>\d+)-(?P<end>\d+)\s+of\s+(?P<total>[\d,]+)\s+Results\b",
    flags=re.IGNORECASE,
)
_RESULT_TOTAL_RE = re.compile(r"\b(?P<total>[\d,]+)\s+Results\b", flags=re.IGNORECASE)
_RENDER_QUERY_MARKER = "Sephora.renderQueryParams"


class SephoraCatalogGridStateError(ValueError):
    """The preserved Sephora catalog-grid state is absent or malformed."""


@dataclass(frozen=True)
class SephoraCatalogGridState:
    category_slug: str
    category_name: str | None
    result_id: str | None
    category_id: str | None
    target_url: str
    sort_by: str
    sort_label: str | None
    requested_page: int
    visible_start: int
    visible_end: int
    total_products: int
    products: tuple[dict[str, Any], ...]
    has_more: bool
    serialized_country: str | None
    cached_query_params: str | None


@dataclass(frozen=True)
class SephoraCatalogAggregateState:
    category_slug: str
    category_name: str | None
    category_id: str | None
    target_url: str
    sort_by: str
    requested_page_count: int
    page_size: int
    total_products: int
    pages: tuple[SephoraCatalogGridState, ...]
    traversal_observation: dict[str, Any]

    @property
    def products(self) -> tuple[dict[str, Any], ...]:
        return tuple(product for page in self.pages for product in page.products)

    @property
    def has_more(self) -> bool:
        return len(self.products) < self.total_products


def extract_sephora_catalog_request(url: str) -> tuple[str, int, str] | None:
    """Return the bounded category slug, cumulative page, and sort encoded by ``url``."""

    parsed = urlparse(url)
    if (
        parsed.scheme != "https"
        or (parsed.hostname or "").lower() not in _SEPHORA_HOSTS
    ):
        return None
    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) != 2 or parts[0].casefold() != "shop":
        return None
    query = parse_qs(parsed.query)
    sort_values = query.get("sortBy", [])
    if sort_values != ["BEST_SELLING"]:
        return None
    page_values = query.get("currentPage", [])
    if len(page_values) != 1 or not page_values[0].isdigit():
        return None
    page = int(page_values[0])
    if page < 1 or page > SEPHORA_CATALOG_MAX_PAGE:
        return None
    return parts[1].lower(), page, "BEST_SELLING"


def load_sephora_catalog_grid_state(
    value: str, *, source_url: str | None = None
) -> SephoraCatalogGridState | None:
    """Load either the compact content record or one rendered catalog DOM."""

    compact_payload = _load_compact_payload(value)
    if compact_payload is not None:
        return _state_from_compact_payload(compact_payload)
    return _state_from_rendered_dom(value, source_url=source_url)


def build_sephora_catalog_grid_content_record(
    *, rendered_dom: str, final_url: str
) -> dict[str, Any]:
    """Retain the ranked catalog window without the disposable browser DOM."""

    state = load_sephora_catalog_grid_state(rendered_dom, source_url=final_url)
    if state is None:
        raise SephoraCatalogGridStateError(
            "Sephora catalog-grid state is absent from the rendered DOM"
        )
    return {
        "content_record_version": SEPHORA_CATALOG_GRID_CONTENT_RECORD_VERSION,
        "retailer": "sephora",
        "final_url": final_url,
        "page": {
            "catalog": {
                "categorySlug": state.category_slug,
                "categoryName": state.category_name,
                "resultId": state.result_id,
                "categoryId": state.category_id,
                "targetUrl": state.target_url,
                "sortBy": state.sort_by,
                "sortLabel": state.sort_label,
                "requestedPage": state.requested_page,
                "visibleStart": state.visible_start,
                "visibleEnd": state.visible_end,
                "totalProducts": state.total_products,
                "products": list(state.products),
                "hasMore": state.has_more,
                "serializedCountry": state.serialized_country,
                "cachedQueryParams": state.cached_query_params,
            }
        },
    }


def load_sephora_catalog_linkstore_page(
    rendered_dom: str, *, source_url: str
) -> SephoraCatalogGridState:
    """Load one complete retailer-owned ``page.nthCategory`` payload."""

    parser = _LinkStoreParser()
    try:
        parser.feed(rendered_dom or "")
        parser.close()
    except Exception as exc:
        raise SephoraCatalogGridStateError(
            f"Sephora linkStore script parsing failed: {type(exc).__name__}"
        ) from exc
    if len(parser.documents) != 1:
        raise SephoraCatalogGridStateError(
            f"expected exactly one Sephora linkStore script; found {len(parser.documents)}"
        )
    try:
        payload = json.loads(parser.documents[0])
    except (json.JSONDecodeError, TypeError) as exc:
        raise SephoraCatalogGridStateError(
            "Sephora linkStore PageJSON is malformed"
        ) from exc
    page = payload.get("page") if isinstance(payload, dict) else None
    category = page.get("nthCategory") if isinstance(page, dict) else None
    if not isinstance(category, dict):
        raise SephoraCatalogGridStateError(
            "Sephora linkStore page.nthCategory is absent"
        )
    products = category.get("products")
    if not isinstance(products, list) or any(
        not isinstance(product, dict) for product in products
    ):
        raise SephoraCatalogGridStateError(
            "Sephora linkStore page.nthCategory.products is malformed"
        )
    target_url = _required_text(category.get("targetUrl"), "targetUrl")
    parts = [part for part in urlparse(target_url).path.split("/") if part]
    if len(parts) != 2 or parts[0].casefold() != "shop":
        raise SephoraCatalogGridStateError(
            "Sephora nthCategory targetUrl is not /shop/<category>"
        )
    current_page = _required_positive_integer(
        category.get("currentPage"), "currentPage"
    )
    page_size = _required_positive_integer(category.get("pageSize"), "pageSize")
    if page_size != SEPHORA_CATALOG_PAGE_SIZE:
        raise SephoraCatalogGridStateError(
            f"Sephora catalog pageSize changed from {SEPHORA_CATALOG_PAGE_SIZE} "
            f"to {page_size}"
        )
    sort_by = _required_text(category.get("sortOptionCode"), "sortOptionCode")
    if sort_by != "BEST_SELLING":
        raise SephoraCatalogGridStateError(
            f"Sephora catalog sort is {sort_by!r}, not BEST_SELLING"
        )
    render_params = _matching_render_query_params(
        rendered_dom, category_path=target_url
    )
    cached_query_params = _text(render_params.get("cachedQueryParams"))
    cached_query = parse_qs(cached_query_params or "")
    if cached_query.get("currentPage", []) != [str(current_page)]:
        raise SephoraCatalogGridStateError(
            "Sephora render-query currentPage contradicts nthCategory.currentPage"
        )
    if cached_query.get("sortBy", []) != ["BEST_SELLING"]:
        raise SephoraCatalogGridStateError(
            "Sephora render query did not preserve BEST_SELLING"
        )
    requested = extract_sephora_catalog_request(source_url)
    if (
        requested is None
        or requested[0] != parts[1].lower()
        or requested[1] != current_page
    ):
        raise SephoraCatalogGridStateError(
            "Sephora PageJSON does not bind the requested category/page URL"
        )
    total_products = _required_positive_integer(
        category.get("totalProducts"), "totalProducts"
    )
    expected_count = min(
        page_size, max(0, total_products - ((current_page - 1) * page_size))
    )
    if len(products) != expected_count:
        raise SephoraCatalogGridStateError(
            f"Sephora page {current_page} exposed {len(products)} products; "
            f"expected {expected_count}"
        )
    normalized: list[dict[str, Any]] = []
    for page_position, product in enumerate(products, start=1):
        row = dict(product)
        row["gridPosition"] = ((current_page - 1) * page_size) + page_position
        normalized.append(row)
    return SephoraCatalogGridState(
        category_slug=parts[1].lower(),
        category_name=_text(category.get("displayName")),
        result_id=_text(category.get("resultId")),
        category_id=_text(category.get("categoryId")),
        target_url=target_url,
        sort_by=sort_by,
        sort_label="Bestselling",
        requested_page=current_page,
        visible_start=((current_page - 1) * page_size) + 1,
        visible_end=((current_page - 1) * page_size) + len(normalized),
        total_products=total_products,
        products=tuple(normalized),
        has_more=current_page * page_size < total_products,
        serialized_country=_text(render_params.get("country")),
        cached_query_params=cached_query_params,
    )


def build_sephora_catalog_grid_aggregate_content_record(
    *,
    rendered_pages: Iterable[str],
    requested_url: str,
    page_urls: Iterable[str],
    traversal_observation: dict[str, object],
) -> dict[str, Any]:
    """Retain one verified consecutive Bestselling window."""

    doms = tuple(rendered_pages)
    urls = tuple(page_urls)
    if not doms or len(doms) != len(urls):
        raise SephoraCatalogGridStateError(
            "Sephora aggregate requires equal non-empty DOM and URL lists"
        )
    pages = tuple(
        load_sephora_catalog_linkstore_page(dom, source_url=url)
        for dom, url in zip(doms, urls)
    )
    _validate_aggregate_pages(pages, requested_url=requested_url)
    first = pages[0]
    return {
        "content_record_version": SEPHORA_CATALOG_GRID_CONTENT_RECORD_VERSION,
        "retailer": "sephora",
        "requested_url": requested_url,
        "page": {
            "catalogAggregate": {
                "categorySlug": first.category_slug,
                "categoryName": first.category_name,
                "categoryId": first.category_id,
                "targetUrl": first.target_url,
                "sortBy": first.sort_by,
                "requestedPageCount": len(pages),
                "pageSize": SEPHORA_CATALOG_PAGE_SIZE,
                "totalProducts": first.total_products,
                "pages": [
                    {
                        "currentPage": page.requested_page,
                        "pageUrl": page_url,
                        "resultId": page.result_id,
                        "serializedCountry": page.serialized_country,
                        "cachedQueryParams": page.cached_query_params,
                        "products": list(page.products),
                    }
                    for page, page_url in zip(pages, urls)
                ],
                "traversalObservation": dict(traversal_observation),
            }
        },
    }


def load_sephora_catalog_aggregate_state(
    value: str,
) -> SephoraCatalogAggregateState | None:
    """Load one compact multi-page aggregate record."""

    try:
        payload = json.loads((value or "").lstrip())
    except json.JSONDecodeError:
        return None
    if not isinstance(payload, dict) or "content_record_version" not in payload:
        return None
    if (
        payload.get("content_record_version")
        != SEPHORA_CATALOG_GRID_CONTENT_RECORD_VERSION
    ):
        return None
    if payload.get("retailer") != "sephora":
        raise SephoraCatalogGridStateError(
            "Sephora catalog record retailer binding is invalid"
        )
    page = payload.get("page")
    aggregate = page.get("catalogAggregate") if isinstance(page, dict) else None
    raw_pages = aggregate.get("pages") if isinstance(aggregate, dict) else None
    if not isinstance(aggregate, dict) or not isinstance(raw_pages, list) or not raw_pages:
        return None
    category_slug = _required_text(aggregate.get("categorySlug"), "categorySlug")
    category_name = _text(aggregate.get("categoryName"))
    category_id = _text(aggregate.get("categoryId"))
    target_url = _required_text(aggregate.get("targetUrl"), "targetUrl")
    sort_by = _required_text(aggregate.get("sortBy"), "sortBy")
    page_size = _required_positive_integer(aggregate.get("pageSize"), "pageSize")
    total_products = _required_positive_integer(
        aggregate.get("totalProducts"), "totalProducts"
    )
    pages: list[SephoraCatalogGridState] = []
    for raw_page in raw_pages:
        if not isinstance(raw_page, dict):
            raise SephoraCatalogGridStateError(
                "Sephora aggregate contains a non-object page"
            )
        products = raw_page.get("products")
        if not isinstance(products, list) or any(
            not isinstance(product, dict) for product in products
        ):
            raise SephoraCatalogGridStateError(
                "Sephora aggregate page products are malformed"
            )
        current_page = _required_positive_integer(
            raw_page.get("currentPage"), "currentPage"
        )
        pages.append(
            SephoraCatalogGridState(
                category_slug=category_slug,
                category_name=category_name,
                result_id=_text(raw_page.get("resultId")),
                category_id=category_id,
                target_url=target_url,
                sort_by=sort_by,
                sort_label="Bestselling",
                requested_page=current_page,
                visible_start=((current_page - 1) * page_size) + 1,
                visible_end=((current_page - 1) * page_size) + len(products),
                total_products=total_products,
                products=tuple(dict(product) for product in products),
                has_more=current_page * page_size < total_products,
                serialized_country=_text(raw_page.get("serializedCountry")),
                cached_query_params=_text(raw_page.get("cachedQueryParams")),
            )
        )
    requested_url = _required_text(payload.get("requested_url"), "requested_url")
    page_tuple = tuple(pages)
    _validate_aggregate_pages(page_tuple, requested_url=requested_url)
    requested_page_count = _required_positive_integer(
        aggregate.get("requestedPageCount"), "requestedPageCount"
    )
    if requested_page_count != len(page_tuple):
        raise SephoraCatalogGridStateError(
            "Sephora requestedPageCount does not match retained pages"
        )
    traversal = aggregate.get("traversalObservation")
    if not isinstance(traversal, dict):
        raise SephoraCatalogGridStateError(
            "Sephora traversalObservation is absent"
        )
    return SephoraCatalogAggregateState(
        category_slug=category_slug,
        category_name=category_name,
        category_id=category_id,
        target_url=target_url,
        sort_by=sort_by,
        requested_page_count=requested_page_count,
        page_size=page_size,
        total_products=total_products,
        pages=page_tuple,
        traversal_observation=dict(traversal),
    )


def _load_compact_payload(value: str) -> dict[str, Any] | None:
    stripped = (value or "").lstrip()
    if not stripped.startswith("{"):
        return None
    try:
        payload = json.loads(stripped)
    except json.JSONDecodeError:
        return None
    if not isinstance(payload, dict) or "content_record_version" not in payload:
        return None
    if (
        payload.get("content_record_version")
        != SEPHORA_CATALOG_GRID_CONTENT_RECORD_VERSION
    ):
        return None
    if payload.get("retailer") != "sephora":
        raise SephoraCatalogGridStateError(
            "Sephora catalog content record retailer binding is invalid"
        )
    return payload


def _state_from_compact_payload(payload: dict[str, Any]) -> SephoraCatalogGridState:
    page = payload.get("page")
    catalog = page.get("catalog") if isinstance(page, dict) else None
    if not isinstance(catalog, dict):
        raise SephoraCatalogGridStateError(
            "Sephora catalog content record page.catalog is absent"
        )
    products = catalog.get("products")
    if not isinstance(products, list) or any(
        not isinstance(product, dict) for product in products
    ):
        raise SephoraCatalogGridStateError(
            "Sephora catalog content record products are malformed"
        )
    return SephoraCatalogGridState(
        category_slug=_required_text(catalog.get("categorySlug"), "categorySlug"),
        category_name=_text(catalog.get("categoryName")),
        result_id=_text(catalog.get("resultId")),
        category_id=_text(catalog.get("categoryId")),
        target_url=_required_text(catalog.get("targetUrl"), "targetUrl"),
        sort_by=_required_text(catalog.get("sortBy"), "sortBy"),
        sort_label=_text(catalog.get("sortLabel")),
        requested_page=_required_integer(catalog.get("requestedPage"), "requestedPage"),
        visible_start=_required_integer(catalog.get("visibleStart"), "visibleStart"),
        visible_end=_required_integer(catalog.get("visibleEnd"), "visibleEnd"),
        total_products=_required_integer(catalog.get("totalProducts"), "totalProducts"),
        products=tuple(products),
        has_more=_required_bool(catalog.get("hasMore"), "hasMore"),
        serialized_country=_text(catalog.get("serializedCountry")),
        cached_query_params=_text(catalog.get("cachedQueryParams")),
    )


def _state_from_rendered_dom(
    rendered_dom: str, *, source_url: str | None
) -> SephoraCatalogGridState | None:
    dom = rendered_dom or ""
    browse_match = re.search(
        r"<div\b(?P<attrs>(?=[^>]*\bdata-cnstrc-browse=[\"']true[\"'])[^>]*)>",
        dom,
        flags=re.IGNORECASE,
    )
    render_params = next(
        (
            params
            for params in _iter_render_query_params(dom)
            if _text(params.get("urlPath"))
            and str(params["urlPath"]).startswith("/shop/")
        ),
        None,
    )
    if browse_match is None and render_params is None:
        return None
    if browse_match is None or render_params is None:
        raise SephoraCatalogGridStateError(
            "Sephora catalog grid requires both browse attributes and render query state"
        )

    target_url = _required_text(render_params.get("urlPath"), "renderQueryParams.urlPath")
    parts = [part for part in urlparse(target_url).path.split("/") if part]
    if len(parts) != 2 or parts[0].casefold() != "shop":
        raise SephoraCatalogGridStateError(
            "Sephora catalog render query path is not a /shop/<category> route"
        )
    category_slug = parts[1].lower()
    cached_query_params = _text(render_params.get("cachedQueryParams"))
    query = parse_qs(cached_query_params or "")
    requested_page = _single_positive_integer(query.get("currentPage", ["1"]))
    if requested_page > SEPHORA_CATALOG_MAX_PAGE:
        raise SephoraCatalogGridStateError(
            f"Sephora catalog requestedPage exceeds {SEPHORA_CATALOG_MAX_PAGE}"
        )
    sort_values = query.get("sortBy", [])
    if sort_values != ["BEST_SELLING"]:
        raise SephoraCatalogGridStateError(
            "Sephora catalog grid is not serialized in BEST_SELLING order"
        )

    browse_attrs = _attributes(browse_match.group("attrs"))
    browse_total = _integer_text(browse_attrs.get("data-cnstrc-num-results"))
    range_matches = list(_VISIBLE_RANGE_RE.finditer(dom))
    if len(range_matches) != 1:
        raise SephoraCatalogGridStateError(
            f"expected exactly one Sephora visible result range; found {len(range_matches)}"
        )
    range_match = range_matches[0]
    visible_start = int(range_match.group("start"))
    visible_end = int(range_match.group("end"))
    range_total = int(range_match.group("total").replace(",", ""))
    if browse_total is None:
        total_matches = list(_RESULT_TOTAL_RE.finditer(dom))
        browse_total = range_total if not total_matches else range_total
    if browse_total != range_total:
        raise SephoraCatalogGridStateError(
            "Sephora catalog browse total does not match the visible range total"
        )

    product_matches = list(_PRODUCT_ANCHOR_RE.finditer(dom))
    products: list[dict[str, Any]] = []
    for index, match in enumerate(product_matches):
        end = (
            product_matches[index + 1].start()
            if index + 1 < len(product_matches)
            else range_match.start()
        )
        segment = dom[match.start() : max(match.end(), end)]
        attrs = _attributes(match.group("attrs"))
        product_id = _text(attrs.get("data-cnstrc-item-id"))
        name = _text(attrs.get("data-cnstrc-item-name"))
        product_url = _text(attrs.get("href"))
        if product_id is None or name is None or product_url is None:
            products.append(
                {
                    "productId": product_id,
                    "displayName": name,
                    "targetUrl": product_url,
                    "gridPosition": index + 1,
                }
            )
            continue
        brand_match = re.search(
            r"ProductTile-content.*?<span\b[^>]*>(?P<brand>[^<]+)</span>",
            segment,
            flags=re.IGNORECASE | re.DOTALL,
        )
        rating_match = re.search(
            r'aria-label=["\'](?P<rating>\d+(?:\.\d+)?)\s+stars["\']',
            segment,
            flags=re.IGNORECASE,
        )
        review_match = re.search(
            r'data-at=["\']review_count["\'][^>]*aria-label=["\']'
            r'(?P<count>[\d,.KkMm]+)\s+reviews?["\']',
            segment,
            flags=re.IGNORECASE,
        )
        price = _text(attrs.get("data-cnstrc-item-price"))
        products.append(
            {
                "productId": product_id,
                "displayName": html_module.unescape(name),
                "targetUrl": html_module.unescape(product_url),
                "brandName": (
                    html_module.unescape(brand_match.group("brand")).strip()
                    if brand_match is not None
                    else None
                ),
                "currentSku": {
                    "skuId": _text(attrs.get("data-cnstrc-item-variation-id")),
                    "listPrice": f"${price}" if price and not price.startswith("$") else price,
                },
                "rating": (
                    float(rating_match.group("rating")) if rating_match is not None else None
                ),
                "reviews": (
                    _abbreviated_count(review_match.group("count"))
                    if review_match is not None
                    else None
                ),
                "gridPosition": index + 1,
            }
        )
    if not products:
        raise SephoraCatalogGridStateError(
            "Sephora catalog grid exposed no ranked product anchors"
        )

    heading_match = re.search(
        r"<h1\b[^>]*>(?P<heading>.*?)</h1>",
        dom,
        flags=re.IGNORECASE | re.DOTALL,
    )
    sort_label_match = re.search(
        r"Sort\s+by:\s*</?[^>]*>\s*(?P<label>Bestselling)",
        dom,
        flags=re.IGNORECASE,
    )
    if sort_label_match is None and "Bestselling" in dom:
        sort_label = "Bestselling"
    else:
        sort_label = (
            sort_label_match.group("label") if sort_label_match is not None else None
        )
    return SephoraCatalogGridState(
        category_slug=category_slug,
        category_name=(
            _plain_text(heading_match.group("heading"))
            if heading_match is not None
            else None
        ),
        result_id=_text(browse_attrs.get("data-cnstrc-result-id")),
        category_id=_text(browse_attrs.get("data-cnstrc-filter-value")),
        target_url=target_url,
        sort_by="BEST_SELLING",
        sort_label=sort_label,
        requested_page=requested_page,
        visible_start=visible_start,
        visible_end=visible_end,
        total_products=range_total,
        products=tuple(products),
        has_more="Show More Products" in dom,
        serialized_country=_text(render_params.get("country")),
        cached_query_params=cached_query_params,
    )


def _iter_render_query_params(rendered_dom: str) -> Iterator[dict[str, Any]]:
    decoder = json.JSONDecoder()
    cursor = 0
    while True:
        marker = rendered_dom.find(_RENDER_QUERY_MARKER, cursor)
        if marker < 0:
            return
        equals = rendered_dom.find("=", marker + len(_RENDER_QUERY_MARKER))
        if equals < 0:
            return
        start = equals + 1
        while start < len(rendered_dom) and rendered_dom[start].isspace():
            start += 1
        try:
            value, consumed = decoder.raw_decode(rendered_dom[start:])
        except json.JSONDecodeError:
            cursor = start + 1
            continue
        if isinstance(value, dict):
            yield value
        cursor = start + consumed


def _matching_render_query_params(
    rendered_dom: str, *, category_path: str
) -> dict[str, Any]:
    matches = [
        params
        for params in _iter_render_query_params(rendered_dom)
        if params.get("urlPath") == category_path
    ]
    if len(matches) != 1:
        raise SephoraCatalogGridStateError(
            f"expected one matching Sephora render-query object; found {len(matches)}"
        )
    return matches[0]


def _validate_aggregate_pages(
    pages: tuple[SephoraCatalogGridState, ...], *, requested_url: str
) -> None:
    request = extract_sephora_catalog_request(requested_url)
    if request is None or request[1] != 1:
        raise SephoraCatalogGridStateError(
            "Sephora aggregate requested URL must bind currentPage=1"
        )
    if not pages or len(pages) > SEPHORA_CATALOG_MAX_PAGE:
        raise SephoraCatalogGridStateError(
            f"Sephora aggregate requires 1-{SEPHORA_CATALOG_MAX_PAGE} pages"
        )
    first = pages[0]
    identities: list[str] = []
    positions: list[int] = []
    for expected_page, page in enumerate(pages, start=1):
        if page.requested_page != expected_page:
            raise SephoraCatalogGridStateError(
                f"Sephora page sequence expected {expected_page}, "
                f"got {page.requested_page}"
            )
        if (
            page.category_slug != first.category_slug
            or page.target_url != first.target_url
            or page.sort_by != first.sort_by
            or page.total_products != first.total_products
            or page.serialized_country != "US"
        ):
            raise SephoraCatalogGridStateError(
                f"Sephora catalog bindings changed on page {expected_page}"
            )
        for product in page.products:
            identities.append(_required_text(product.get("productId"), "productId"))
            positions.append(
                _required_positive_integer(
                    product.get("gridPosition"), "gridPosition"
                )
            )
    if len(identities) != len(set(identities)):
        raise SephoraCatalogGridStateError(
            "Sephora catalog window contains duplicate product identities"
        )
    if positions != list(range(1, len(positions) + 1)):
        raise SephoraCatalogGridStateError(
            "Sephora catalog window ranks are not contiguous"
        )


class _LinkStoreParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self._in_link_store = False
        self._parts: list[str] = []
        self.documents: list[str] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        if tag.lower() != "script":
            return
        attributes = {key.lower(): value or "" for key, value in attrs}
        if attributes.get("id") == "linkStore":
            self._in_link_store = True
            self._parts = []

    def handle_data(self, data: str) -> None:
        if self._in_link_store:
            self._parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "script" and self._in_link_store:
            self.documents.append("".join(self._parts))
            self._parts = []
            self._in_link_store = False


def _attributes(value: str) -> dict[str, str]:
    return {
        key.lower(): html_module.unescape(item)
        for key, _, item in re.findall(
            r"([:\w-]+)\s*=\s*([\"'])(.*?)\2", value, flags=re.DOTALL
        )
    }


def _plain_text(value: str) -> str | None:
    text = re.sub(r"<[^>]+>", " ", value)
    text = re.sub(r"\s+", " ", html_module.unescape(text)).strip()
    return text or None


def _abbreviated_count(value: str) -> int | None:
    normalized = value.replace(",", "").strip().upper()
    multiplier = 1
    if normalized.endswith("K"):
        multiplier = 1_000
        normalized = normalized[:-1]
    elif normalized.endswith("M"):
        multiplier = 1_000_000
        normalized = normalized[:-1]
    try:
        return int(float(normalized) * multiplier)
    except ValueError:
        return None


def _single_positive_integer(values: list[str]) -> int:
    if len(values) != 1 or not values[0].isdigit() or int(values[0]) < 1:
        raise SephoraCatalogGridStateError(
            "Sephora catalog currentPage must be one positive integer"
        )
    return int(values[0])


def _integer_text(value: object) -> int | None:
    text = _text(value)
    return int(text) if text is not None and text.isdigit() else None


def _required_integer(value: object, field: str) -> int:
    if isinstance(value, int) and not isinstance(value, bool) and value >= 0:
        return value
    raise SephoraCatalogGridStateError(
        f"Sephora catalog content record {field} is invalid"
    )


def _required_positive_integer(value: object, field: str) -> int:
    if isinstance(value, int) and not isinstance(value, bool) and value > 0:
        return value
    raise SephoraCatalogGridStateError(
        f"Sephora catalog content record {field} is invalid"
    )


def _required_bool(value: object, field: str) -> bool:
    if isinstance(value, bool):
        return value
    raise SephoraCatalogGridStateError(
        f"Sephora catalog content record {field} is invalid"
    )


def _required_text(value: object, field: str) -> str:
    text = _text(value)
    if text is None:
        raise SephoraCatalogGridStateError(
            f"Sephora catalog content record {field} is invalid"
        )
    return text


def _text(value: object) -> str | None:
    if isinstance(value, (str, int, float)) and not isinstance(value, bool):
        text = str(value).strip()
        return text or None
    return None


__all__ = [
    "SEPHORA_CATALOG_GRID_CONTENT_RECORD_VERSION",
    "SEPHORA_CATALOG_PAGE_SIZE",
    "SEPHORA_CATALOG_MAX_PAGE",
    "SephoraCatalogAggregateState",
    "SephoraCatalogGridState",
    "SephoraCatalogGridStateError",
    "build_sephora_catalog_grid_aggregate_content_record",
    "build_sephora_catalog_grid_content_record",
    "extract_sephora_catalog_request",
    "load_sephora_catalog_aggregate_state",
    "load_sephora_catalog_grid_state",
    "load_sephora_catalog_linkstore_page",
]
