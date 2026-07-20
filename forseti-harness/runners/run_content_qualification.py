"""Qualify one rendered content extractor against operator scratch inputs.

Exit codes: 0 match and scratch released; 1 drift/failure with scratch
preserved; 2 usage error.  This runner never reads or writes lake packets.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Callable, Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from source_capture.basenotes_projection import (  # noqa: E402
    BASENOTES_PARSER_VERSION,
    build_basenotes_content_record,
)
from source_capture.content_qualification import (  # noqa: E402
    ContentQualificationError,
    qualify_rendered_content,
)
from source_capture.fragrantica_projection import (  # noqa: E402
    FRAGRANTICA_PARSER_VERSION,
    build_fragrantica_content_record,
)
from source_capture.parfumo_projection import (  # noqa: E402
    PARFUMO_TARGETED_PARSER_VERSION,
    build_parfumo_targeted_content_record,
)
from source_capture.retail_pdp_projection import (  # noqa: E402
    LUCKYSCENT_PDP_PARSER_VERSION,
    NORDSTROM_PDP_PARSER_VERSION,
    SEPHORA_PDP_PARSER_VERSION,
    build_luckyscent_pdp_aggregate_content_record,
    build_nordstrom_pdp_aggregate_content_record,
    build_sephora_pdp_aggregate_content_record,
)

Extractor = Callable[[bytes, bytes, str], dict[str, Any]]


def _rendered(
    builder: Callable[..., dict[str, Any]], **fixed: Any
) -> Extractor:
    def extract(rendered_dom: bytes, visible_text: bytes, source_url: str) -> dict[str, Any]:
        return builder(
            rendered_dom=rendered_dom,
            visible_text=visible_text,
            source_url=source_url,
            **fixed,
        )

    return extract


_ROUTES: dict[str, tuple[str, Extractor]] = {
    "basenotes": (
        BASENOTES_PARSER_VERSION,
        _rendered(build_basenotes_content_record),
    ),
    "fragrantica_initial": (
        FRAGRANTICA_PARSER_VERSION,
        _rendered(
            build_fragrantica_content_record,
            source_surface="fragrantica_product_page_cloakbrowser_initial_viewport",
        ),
    ),
    "fragrantica_deep": (
        FRAGRANTICA_PARSER_VERSION,
        _rendered(
            build_fragrantica_content_record,
            source_surface="fragrantica_product_page_cloakbrowser_deep_scroll_current_window",
        ),
    ),
    "parfumo": (
        PARFUMO_TARGETED_PARSER_VERSION,
        _rendered(build_parfumo_targeted_content_record),
    ),
    "sephora": (
        SEPHORA_PDP_PARSER_VERSION,
        _rendered(build_sephora_pdp_aggregate_content_record),
    ),
    "luckyscent": (
        LUCKYSCENT_PDP_PARSER_VERSION,
        _rendered(build_luckyscent_pdp_aggregate_content_record),
    ),
    "nordstrom": (
        NORDSTROM_PDP_PARSER_VERSION,
        _rendered(build_nordstrom_pdp_aggregate_content_record),
    ),
}


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Qualify deterministic content extraction on disposable scratch inputs."
    )
    parser.add_argument("--route", choices=sorted(_ROUTES), required=True)
    parser.add_argument("--scratch-root", type=Path, required=True)
    parser.add_argument("--rendered-dom", type=Path, required=True)
    parser.add_argument("--visible-text", type=Path, required=True)
    parser.add_argument("--expected-content-record", type=Path, required=True)
    parser.add_argument("--source-url", required=True)
    parser.add_argument("--report", type=Path, required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    try:
        args = _parser().parse_args(argv)
        extractor_version, extractor = _ROUTES[args.route]
        exit_code, report = qualify_rendered_content(
            scratch_root=args.scratch_root,
            rendered_dom_path=args.rendered_dom,
            visible_text_path=args.visible_text,
            expected_content_record_path=args.expected_content_record,
            report_path=args.report,
            extractor_version=extractor_version,
            source_url=args.source_url,
            extractor=extractor,
        )
    except ContentQualificationError as exc:
        print(json.dumps({"status": "usage_error", "code": exc.code, "message": str(exc)}))
        return 2
    print(json.dumps(report, indent=2, sort_keys=True))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
