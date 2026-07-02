"""Runner: discover review-positive new PDPs for one fragrance retailer.

Wires the network adapter to the network-free discovery core. Judge.me retailers
enumerate products (products.json or sitemap) and cadence-probe the per-product
widget; the Yotpo retailer pages the store-level reviews feed. Emits a
DiscoveryReceipt (candidate PDP URLs + counts + residuals) to an output path.

Discovery only: it does not capture rows, persist review bodies, or promote any
candidate into the registry.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Callable
from urllib.parse import urlencode

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from source_capture.adapters.fragrance_discovery_fetch import fetch_discovery_url
from source_capture.fragrance_review_discovery import (
    THROTTLE,
    DiscoveryReceipt,
    ProductRef,
    RateLimiterPolicy,
    discover_judgeme_by_probe,
    discover_yotpo_shop_feed,
    extract_judgeme_product_id,
    judgeme_count_from_response,
    parse_shopify_products_json,
    parse_sitemap_locs,
    select_product_refs_from_sitemap,
    select_product_sitemap_locs,
)


def _enumerate_products_json(store_domain: str, *, limit: int, timeout: float) -> tuple[list[ProductRef], str | None]:
    res = fetch_discovery_url(
        f"https://{store_domain}/products.json?limit={limit}", accept="application/json", timeout_seconds=timeout
    )
    if not res.ok:
        return [], f"products_json_unavailable:{res.status}:{res.error or ''}"
    try:
        return parse_shopify_products_json(res.text, store_domain=store_domain), None
    except Exception as exc:  # noqa: BLE001
        return [], f"products_json_parse_failed:{type(exc).__name__}"


def _enumerate_sitemap(store_domain: str, *, timeout: float, max_subsitemaps: int) -> tuple[list[ProductRef], str | None]:
    index = fetch_discovery_url(f"https://{store_domain}/sitemap.xml", accept="application/xml", timeout_seconds=timeout)
    if not index.ok:
        return [], f"sitemap_unavailable:{index.status}:{index.error or ''}"
    locs = parse_sitemap_locs(index.text)
    refs: list[ProductRef] = list(select_product_refs_from_sitemap(locs))  # index-as-urlset (rare)
    for sub in select_product_sitemap_locs(locs)[:max_subsitemaps]:
        page = fetch_discovery_url(sub, accept="application/xml", timeout_seconds=timeout)
        if page.ok:
            refs.extend(select_product_refs_from_sitemap(parse_sitemap_locs(page.text)))
    seen: set[str] = set()
    deduped: list[ProductRef] = []
    for ref in refs:
        if ref.product_url in seen:
            continue
        seen.add(ref.product_url)
        deduped.append(ref)
    if not deduped:
        return [], "sitemap_yielded_no_product_urls"
    return deduped, None


def _make_judgeme_fetch_count(timeout: float) -> Callable[[str, str], object]:
    def fetch_count(shop_domain: str, product_id: str) -> object:
        query = urlencode(
            {"url": shop_domain, "shop_domain": shop_domain, "platform": "shopify", "product_id": product_id, "per_page": 1, "page": 1}
        )
        res = fetch_discovery_url("https://api.judge.me/reviews/reviews_for_widget?" + query, accept="application/json", timeout_seconds=timeout)
        if res.status != 200:
            return THROTTLE  # valid products return 200; non-200 is throttle/transient -> back off
        try:
            return judgeme_count_from_response(json.loads(res.text))
        except Exception:  # noqa: BLE001
            return None

    return fetch_count


def _make_judgeme_id_resolver(timeout: float) -> Callable[[ProductRef], str | None]:
    def resolve(ref: ProductRef) -> str | None:
        res = fetch_discovery_url(ref.product_url, accept="text/html", timeout_seconds=timeout)
        if not res.ok:
            return None
        return extract_judgeme_product_id(res.text)

    return resolve


def _make_yotpo_fetch_page(store_guid: str, *, per_page: int, timeout: float) -> Callable[[int], dict | None]:
    def fetch_page(page: int) -> dict | None:
        res = fetch_discovery_url(
            f"https://api-cdn.yotpo.com/v3/storefront/store/{store_guid}/reviews?page={page}&perPage={per_page}",
            accept="application/json",
            timeout_seconds=timeout,
        )
        if not res.ok:
            return None
        try:
            parsed = json.loads(res.text)
        except Exception:  # noqa: BLE001
            return None
        return parsed if isinstance(parsed, dict) else None

    return fetch_page


def _with_residual(receipt: DiscoveryReceipt, residual: str | None) -> DiscoveryReceipt:
    if not residual:
        return receipt
    return receipt.model_copy(update={"residuals": [residual, *receipt.residuals]})


def run(args: argparse.Namespace) -> DiscoveryReceipt:
    if args.vendor == "yotpo":
        refs, enum_residual = _enumerate_products_json(args.store_domain, limit=args.products_limit, timeout=args.timeout_seconds)
        id_to_url = {ref.shopify_product_id: ref.product_url for ref in refs if ref.shopify_product_id}
        receipt = discover_yotpo_shop_feed(
            source_id=args.source_id,
            fetch_feed_page=_make_yotpo_fetch_page(args.yotpo_store, per_page=args.yotpo_per_page, timeout=args.timeout_seconds),
            shopify_id_to_url=id_to_url,
            max_pages=args.max_pages,
            find_target=args.find_target,
        )
        receipt = _with_residual(receipt, enum_residual)
    else:
        if args.enumerate == "sitemap":
            refs, enum_residual = _enumerate_sitemap(args.store_domain, timeout=args.timeout_seconds, max_subsitemaps=args.max_subsitemaps)
            resolver: Callable[[ProductRef], str | None] | None = _make_judgeme_id_resolver(args.timeout_seconds)
        else:
            refs, enum_residual = _enumerate_products_json(args.store_domain, limit=args.products_limit, timeout=args.timeout_seconds)
            resolver = None
        receipt = discover_judgeme_by_probe(
            source_id=args.source_id,
            shop_domain=args.shop_domain,
            product_refs=refs,
            fetch_count=_make_judgeme_fetch_count(args.timeout_seconds),
            sleeper=time.sleep,
            policy=RateLimiterPolicy(min_interval_s=args.min_interval, max_interval_s=args.max_interval),
            max_probes=args.max_probes,
            find_target=args.find_target,
            exclude_handles=[args.exclude_handle] if args.exclude_handle else [],
            resolve_product_id=resolver,
        )
        receipt = _with_residual(receipt, enum_residual)
    return receipt


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Discover review-positive new fragrance PDPs for one retailer.")
    parser.add_argument("--source-id", required=True)
    parser.add_argument("--vendor", required=True, choices=["judgeme", "yotpo"])
    parser.add_argument("--store-domain", required=True, help="Storefront host, e.g. ministryofscent.com")
    parser.add_argument("--shop-domain", help="Judge.me myshopify shop domain (judgeme only).")
    parser.add_argument("--yotpo-store", help="Yotpo store guid/app key (yotpo only).")
    parser.add_argument("--exclude-handle", help="Locked fixture handle to skip.")
    parser.add_argument("--enumerate", choices=["products_json", "sitemap"], default="products_json")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--find-target", type=int, default=2)
    parser.add_argument("--max-probes", type=int, default=60)
    parser.add_argument("--min-interval", type=float, default=6.0)
    parser.add_argument("--max-interval", type=float, default=60.0)
    parser.add_argument("--max-pages", type=int, default=5)
    parser.add_argument("--max-subsitemaps", type=int, default=5)
    parser.add_argument("--products-limit", type=int, default=250)
    parser.add_argument("--yotpo-per-page", type=int, default=50)
    parser.add_argument("--timeout-seconds", type=float, default=30.0)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    if args.vendor == "judgeme" and not args.shop_domain:
        parser.error("--shop-domain is required for --vendor judgeme")
    if args.vendor == "yotpo" and not args.yotpo_store:
        parser.error("--yotpo-store is required for --vendor yotpo")
    receipt = run(args)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt.model_dump(mode="json"), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    for candidate in receipt.candidates:
        print(f"CANDIDATE count={candidate.review_count} {candidate.product_url}")
    if not receipt.candidates:
        print(f"NO_CANDIDATE residuals={receipt.residuals}")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
