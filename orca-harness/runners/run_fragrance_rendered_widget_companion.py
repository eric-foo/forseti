from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from source_capture.fragrance_rendered_widget_companion import write_fragrance_rendered_widget_companion
from source_capture.fragrance_review_coverage import parse_as_of_date


def run_fragrance_rendered_widget_companion(
    *,
    url: str,
    output_path: Path,
    source_id: str,
    source_site: str,
    product_url: str | None = None,
    widget_route: dict[str, str | None] | None = None,
    as_of_date: str | None = None,
    max_selected_rows: int | None = None,
    source_media_filter_count: int | None = None,
    timeout_seconds: float = 45.0,
    wait_until: str = "load",
    viewport_width: int = 1365,
    viewport_height: int = 900,
    max_response_bytes: int = 5_000_000,
    settle_seconds: float = 3.0,
    lazy_load_scroll_passes: int = 0,
    lazy_load_scroll_step_px: int = 0,
    selector: str | None = None,
    selector_timeout_seconds: float = 5.0,
    block_heavy_assets: bool = False,
    browser_channel: str | None = None,
    fallback_widget_urls: Sequence[str] = (),
) -> Path:
    write_fragrance_rendered_widget_companion(
        output_path=output_path,
        url=url,
        source_id=source_id,
        source_site=source_site,
        product_url=product_url,
        widget_route=widget_route,
        as_of_date=parse_as_of_date(as_of_date),
        max_selected_rows=max_selected_rows,
        source_media_filter_count=source_media_filter_count,
        timeout_seconds=timeout_seconds,
        wait_until=wait_until,
        viewport_width=viewport_width,
        viewport_height=viewport_height,
        max_response_bytes=max_response_bytes,
        settle_seconds=settle_seconds,
        lazy_load_scroll_passes=lazy_load_scroll_passes,
        lazy_load_scroll_step_px=lazy_load_scroll_step_px,
        selector=selector,
        selector_timeout_seconds=selector_timeout_seconds,
        block_heavy_assets=block_heavy_assets,
        browser_channel=browser_channel,
        fallback_widget_urls=fallback_widget_urls,
    )
    return output_path


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Capture one fragrance PDP render, preserve review-widget responses observed "
            "during that browser load, and optionally complete missing row pages with "
            "bounded fallback widget URLs in the same operator command."
        )
    )
    parser.add_argument("--url", required=True, help="PDP URL to render.")
    parser.add_argument("--output", type=Path, required=True, help="Combined companion JSON output path.")
    parser.add_argument("--source-id", required=True, help="Source registry id.")
    parser.add_argument("--source-site", required=True, help="Human-readable source site.")
    parser.add_argument("--product-url", help="Product URL to bind review rows to. Defaults to --url.")
    parser.add_argument(
        "--widget-route-param",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="Optional widget route parameter to preserve in the receipt. Repeatable.",
    )
    parser.add_argument(
        "--fallback-widget-url",
        action="append",
        default=[],
        help=(
            "Optional bounded widget URL to fetch only if passive render traffic does not "
            "yield row-complete review coverage. Repeatable."
        ),
    )
    parser.add_argument("--as-of-date", help="YYYY-MM-DD date for recency windows. Defaults to today.")
    parser.add_argument("--max-selected-rows", type=int, help="Optional adaptive cap for selected review rows.")
    parser.add_argument(
        "--source-media-filter-count",
        type=int,
        help="Optional source media filter count, e.g. Judge.me with_pictures total_count.",
    )
    parser.add_argument("--timeout-seconds", type=float, default=45.0)
    parser.add_argument("--wait-until", choices=["commit", "domcontentloaded", "load", "networkidle"], default="load")
    parser.add_argument("--viewport-width", type=int, default=1365)
    parser.add_argument("--viewport-height", type=int, default=900)
    parser.add_argument("--max-response-bytes", type=int, default=5_000_000)
    parser.add_argument("--settle-seconds", type=float, default=3.0)
    parser.add_argument(
        "--lazy-load-scroll-passes",
        type=int,
        default=0,
        help=(
            "After preserving no-scroll above-fold DOM facts, perform this many bounded "
            "scroll passes to trigger lazy review widgets and preserve newly observed responses."
        ),
    )
    parser.add_argument(
        "--lazy-load-scroll-step-px",
        type=int,
        default=0,
        help="Optional pixel step for lazy-load scroll passes; default scrolls to page bottom per pass.",
    )
    parser.add_argument("--selector", help="Optional selector to wait for before extracting DOM geometry.")
    parser.add_argument("--selector-timeout-seconds", type=float, default=5.0)
    parser.add_argument("--block-heavy-assets", action="store_true")
    parser.add_argument("--browser-channel", help="Optional local Chromium channel, for example chrome or msedge.")
    return parser


def _route_params(values: Sequence[str]) -> dict[str, str | None]:
    params: dict[str, str | None] = {}
    for value in values:
        if "=" not in value:
            raise argparse.ArgumentTypeError("--widget-route-param must be KEY=VALUE")
        key, raw = value.split("=", 1)
        if not key:
            raise argparse.ArgumentTypeError("--widget-route-param key must be non-empty")
        params[key] = raw or None
    return params


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        output_path = run_fragrance_rendered_widget_companion(
            url=args.url,
            output_path=args.output,
            source_id=args.source_id,
            source_site=args.source_site,
            product_url=args.product_url,
            widget_route=_route_params(args.widget_route_param),
            as_of_date=args.as_of_date,
            max_selected_rows=args.max_selected_rows,
            source_media_filter_count=args.source_media_filter_count,
            timeout_seconds=args.timeout_seconds,
            wait_until=args.wait_until,
            viewport_width=args.viewport_width,
            viewport_height=args.viewport_height,
            max_response_bytes=args.max_response_bytes,
            settle_seconds=args.settle_seconds,
            lazy_load_scroll_passes=args.lazy_load_scroll_passes,
            lazy_load_scroll_step_px=args.lazy_load_scroll_step_px,
            selector=args.selector,
            selector_timeout_seconds=args.selector_timeout_seconds,
            block_heavy_assets=args.block_heavy_assets,
            browser_channel=args.browser_channel,
            fallback_widget_urls=args.fallback_widget_url,
        )
    except Exception as exc:
        parser.exit(status=2, message=f"fragrance rendered widget companion failed: {exc}\n")

    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
