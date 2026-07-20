"""Compare browser-compacted Sephora substrate with a verified sample packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from runners.run_sephora_pdp_parser_fit_check import (
    check_sephora_pdp_parser_fit,
)
from source_capture.models import SourceCapturePacket
from source_capture.sephora_browser_projection import (
    SEPHORA_BROWSER_SUBSTRATE_SCRIPT,
    SephoraBrowserProjectionSubstrate,
    canonical_content_bytes,
)


def run_sephora_pdp_browser_projection_probe(
    *,
    packet_or_manifest_path: Path,
    perturbation: str | None = None,
) -> tuple[int, dict[str, Any]]:
    packet_dir = (
        packet_or_manifest_path
        if packet_or_manifest_path.is_dir()
        else packet_or_manifest_path.parent
    )
    parser_fit = check_sephora_pdp_parser_fit(
        packet_or_manifest_path=packet_or_manifest_path
    )
    if parser_fit["status"] != "match":
        return 2, {
            "status": "blocked",
            "reason": "source sample parser-fit is not match",
            "parser_fit": parser_fit,
        }

    packet = SourceCapturePacket.model_validate_json(
        (packet_dir / "manifest.json").read_bytes()
    )
    files = {
        Path(preserved.relative_packet_path).name.split("_", 1)[-1]: (
            packet_dir / preserved.relative_packet_path,
            preserved.sha256,
            preserved.size_bytes,
        )
        for preserved in packet.preserved_files
    }
    rendered_dom = _verified_bytes(files, "cloakbrowser_rendered_dom.html")
    visible_text = _verified_bytes(files, "cloakbrowser_visible_text.txt")
    stored_content_bytes = _verified_bytes(files, "content_record.json")
    stored_content = json.loads(stored_content_bytes)

    try:
        from playwright.sync_api import sync_playwright
    except Exception as exc:
        return 3, {
            "status": "blocked",
            "reason": f"Playwright unavailable: {type(exc).__name__}: {exc}",
        }

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            page = browser.new_page()
            page.route(
                "https://forseti-projection.invalid/**",
                lambda route: route.fulfill(
                    status=200,
                    content_type="text/html",
                    body="<html><body>Forseti projection probe</body></html>",
                ),
            )
            page.goto("https://forseti-projection.invalid/")
            payload = page.evaluate(
                SEPHORA_BROWSER_SUBSTRATE_SCRIPT,
                {
                    "renderedDom": rendered_dom.decode("utf-8"),
                    "visibleText": visible_text.decode("utf-8"),
                },
            )
        finally:
            browser.close()

    if perturbation is not None:
        payload = _apply_perturbation(payload, perturbation)
    substrate = SephoraBrowserProjectionSubstrate.from_browser_payload(payload)
    substrate.verify_raw_provenance(
        rendered_dom=rendered_dom, visible_text=visible_text
    )
    try:
        projected = substrate.build_content_record(
            source_url=packet.source_locator.value or ""
        )
    except ValueError as exc:
        if (
            perturbation == "drop_link_store"
            and "linkStore.page.product" in str(exc)
        ):
            return 0, {
                "status": "perturbation_rejected",
                "perturbation": perturbation,
                "rejection_boundary": "sephora_product_state_admission",
                "reason": str(exc),
                "packet_id": packet.packet_id,
            }
        raise
    projected_bytes = canonical_content_bytes(projected)
    parsed_match = projected == stored_content
    byte_match = projected_bytes == stored_content_bytes
    exact_match = parsed_match and byte_match

    report: dict[str, Any] = {
        "status": "match" if exact_match else "mismatch",
        "packet_id": packet.packet_id,
        "source_url": packet.source_locator.value,
        "raw_rendered_dom_bytes": len(rendered_dom),
        "browser_compact_dom_bytes": substrate.compact_dom_byte_count,
        "stored_content_record_bytes": len(stored_content_bytes),
        "projected_content_record_bytes": len(projected_bytes),
        "parsed_content_match": parsed_match,
        "byte_content_match": byte_match,
        "compact_vs_raw_reduction_percent": round(
            (1 - substrate.compact_dom_byte_count / len(rendered_dom)) * 100, 2
        ),
        "selected_span_count": substrate.selected_span_count,
        "rendered_dom_sha256": substrate.rendered_dom_sha256,
        "compact_dom_sha256": substrate.compact_dom_sha256,
        "stored_content_sha256": hashlib.sha256(stored_content_bytes).hexdigest(),
        "projected_content_sha256": hashlib.sha256(projected_bytes).hexdigest(),
        "loss_counts": substrate.loss_counts,
        "parser_fit": parser_fit,
        "perturbation": perturbation,
    }
    if not exact_match:
        report["first_difference"] = _first_difference(stored_content, projected)
        if parsed_match and not byte_match:
            report["byte_identity_gap"] = {
                "stored_content_sha256": report["stored_content_sha256"],
                "projected_content_sha256": report["projected_content_sha256"],
            }
        return 1, report
    return 0, report


def _apply_perturbation(
    payload: dict[str, Any], perturbation: str
) -> dict[str, Any]:
    if perturbation != "drop_link_store":
        raise ValueError(f"unsupported perturbation: {perturbation}")
    compact_dom = payload.get("compactDom")
    if not isinstance(compact_dom, str):
        raise ValueError("browser payload has no compact DOM to perturb")
    changed, replacements = re.subn(
        r"<script\b(?=[^>]*\bid=[\"']linkStore[\"'])[^>]*>[\s\S]*?</script\s*>",
        "",
        compact_dom,
        count=1,
        flags=re.IGNORECASE,
    )
    if replacements != 1:
        raise ValueError("drop_link_store perturbation found no retained linkStore script")
    changed_bytes = changed.encode("utf-8")
    return {
        **payload,
        "compactDom": changed,
        "compactDomByteCount": len(changed_bytes),
        "compactDomSha256": hashlib.sha256(changed_bytes).hexdigest(),
    }


def _verified_bytes(
    files: dict[str, tuple[Path, str, int]], filename: str
) -> bytes:
    try:
        path, expected_sha256, expected_size = files[filename]
    except KeyError as exc:
        raise ValueError(f"sample packet is missing {filename}") from exc
    body = path.read_bytes()
    if len(body) != expected_size:
        raise ValueError(f"{filename} size does not match manifest")
    if hashlib.sha256(body).hexdigest() != expected_sha256:
        raise ValueError(f"{filename} sha256 does not match manifest")
    return body


def _first_difference(left: object, right: object, path: str = "$") -> str | None:
    if type(left) is not type(right):
        return f"{path}: type {type(left).__name__} != {type(right).__name__}"
    if isinstance(left, dict):
        left_keys = set(left)
        right_keys = set(right)
        if left_keys != right_keys:
            return (
                f"{path}: keys differ; missing={sorted(left_keys - right_keys)!r}; "
                f"extra={sorted(right_keys - left_keys)!r}"
            )
        for key in left:
            difference = _first_difference(left[key], right[key], f"{path}.{key}")
            if difference is not None:
                return difference
        return None
    if isinstance(left, list):
        if len(left) != len(right):
            return f"{path}: length {len(left)} != {len(right)}"
        for index, (left_item, right_item) in enumerate(zip(left, right, strict=True)):
            difference = _first_difference(
                left_item, right_item, f"{path}[{index}]"
            )
            if difference is not None:
                return difference
        return None
    if left != right:
        return f"{path}: {left!r} != {right!r}"
    return None


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Replay a verified Sephora sample through browser-side DOM compaction "
            "and require exact full-derived content equality."
        )
    )
    parser.add_argument("--packet", type=Path, required=True)
    parser.add_argument(
        "--perturbation",
        choices=("drop_link_store",),
        default=None,
        help=(
            "Seed a known compact-substrate omission and require the intended "
            "Sephora admission boundary to reject it."
        ),
    )
    args = parser.parse_args()
    try:
        exit_code, report = run_sephora_pdp_browser_projection_probe(
            packet_or_manifest_path=args.packet,
            perturbation=args.perturbation,
        )
    except Exception as exc:
        report = {
            "status": "error",
            "reason": f"{type(exc).__name__}: {exc}",
        }
        exit_code = 3
    print(json.dumps(report, indent=2, sort_keys=True))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
