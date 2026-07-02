from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from source_capture.fragrance_review_coverage import parse_as_of_date, write_fragrance_review_coverage


def run_fragrance_review_coverage(
    *,
    widget_response_paths: Sequence[Path],
    output_path: Path,
    product_url: str,
    source_id: str,
    source_site: str,
    pdp_html_path: Path | None = None,
    widget_route: dict[str, str | None] | None = None,
    as_of_date: str | None = None,
    max_selected_rows: int | None = None,
    source_media_filter_count: int | None = None,
) -> Path:
    write_fragrance_review_coverage(
        widget_response_paths=widget_response_paths,
        pdp_html_path=pdp_html_path,
        output_path=output_path,
        source_id=source_id,
        source_site=source_site,
        product_url=product_url,
        widget_route=widget_route,
        as_of_date=parse_as_of_date(as_of_date),
        max_selected_rows=max_selected_rows,
        source_media_filter_count=source_media_filter_count,
    )
    return output_path


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Build a local, no-network focused fragrance purchase-review coverage "
            "JSON receipt from saved widget/PDP response files."
        )
    )
    parser.add_argument(
        "--widget-response",
        type=Path,
        action="append",
        required=True,
        help="Saved review-widget JSON response file. Repeat for paginated responses.",
    )
    parser.add_argument("--pdp-html", type=Path, help="Optional saved PDP HTML file for aggregate JSON-LD.")
    parser.add_argument("--output", type=Path, required=True, help="Coverage receipt JSON output path.")
    parser.add_argument("--product-url", required=True, help="Product URL the review rows are bound to.")
    parser.add_argument("--source-id", default="fragrance_retail_luckyscent", help="Source registry id.")
    parser.add_argument("--source-site", default="Luckyscent / Scent Bar", help="Human-readable source site.")
    parser.add_argument(
        "--widget-route-param",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="Optional widget route parameter to preserve in the receipt. Repeatable.",
    )
    parser.add_argument("--as-of-date", help="YYYY-MM-DD date for recency windows. Defaults to today.")
    parser.add_argument("--max-selected-rows", type=int, help="Optional adaptive cap for selected reader rows.")
    parser.add_argument(
        "--source-media-filter-count",
        type=int,
        help="Optional source media filter count, e.g. Judge.me with_pictures total_count.",
    )
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
        output_path = run_fragrance_review_coverage(
            widget_response_paths=args.widget_response,
            pdp_html_path=args.pdp_html,
            output_path=args.output,
            product_url=args.product_url,
            source_id=args.source_id,
            source_site=args.source_site,
            widget_route=_route_params(args.widget_route_param),
            as_of_date=args.as_of_date,
            max_selected_rows=args.max_selected_rows,
            source_media_filter_count=args.source_media_filter_count,
        )
    except Exception as exc:
        parser.exit(status=2, message=f"fragrance review coverage failed: {exc}\n")

    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
