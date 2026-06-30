from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Callable, Mapping, Sequence
from urllib.parse import urlparse

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from runners.run_source_capture_http_packet import run_source_capture_http_packet
from source_capture import (
    CaptureModeCategory,
    PacketTiming,
    SourceCaptureSlice,
    known_fact,
    not_applicable,
    not_attempted,
    unknown_with_reason,
)
from source_capture.writer import write_local_source_capture_packet

if TYPE_CHECKING:
    from data_lake.root import DataLakeRoot


SOURCE_FAMILY = "fragrance_native_database"
CAPTURE_PROFILE = "parfumo_native_direct_http_v0"
TARGETED_RENDERED_CAPTURE_PROFILE = "parfumo_native_targeted_rendered_v0"
SUMMARY_FILENAME = "parfumo_native_capture_summary.json"

DIRECT_HTTP_SLOT = "direct_http_packet"
DIRECT_HTTP_SURFACE = "parfumo_product_page_direct_http"
TARGETED_RENDERED_SLOT = "targeted_rendered_packet"
TARGETED_RENDERED_SURFACE = "parfumo_product_page_chrome_extension_targeted_rendered_session"
TARGETED_CAPTURE_PLAN_FILENAME = "parfumo_targeted_capture_plan.json"

TARGETED_SAMPLE_BUCKETS = (
    ("product_context", "rendered product context and aggregate source-visible counts"),
    ("review_latest_recent", "latest or recent source-visible review sample"),
    (
        "review_source_visible_high_rating",
        "high-rating review sample only where Parfumo exposes source-visible rating fields",
    ),
    (
        "review_source_visible_low_rating",
        "low-rating review sample only where Parfumo exposes source-visible rating fields",
    ),
    ("statement_latest_recent", "latest or recent source-visible statement sample"),
)

DEFAULT_DECISION_QUESTION = (
    "What public Parfumo product-page evidence was available for this fragrance at capture time?"
)
DEFAULT_OPERATOR_CATEGORY = "parfumo_native_capture_runner"
DEFAULT_TIMEOUT_SECONDS = 120.0
DEFAULT_HTTP_MAX_BYTES = 10_000_000

ACCEPTED_RESIDUALS = [
    "anonymous Parfumo direct HTTP capture only; no login, stored session, profile, proxy, or credential injection",
    "does not invoke Parfumo AJAX review or statement pagination endpoints or claim complete corpus coverage",
    "direct HTTP packet preserves server HTML and embedded structured attributes when publicly returned",
    "linked media assets are not independently fetched or preserved",
    "projection, ECR, cleaning, judgment scoring, and buyer-proof claims are intentionally out of scope",
]

NON_CLAIMS = [
    "not full Parfumo corpus capture",
    "not account-authenticated capture",
    "not anti-bot evasion",
    "not AJAX pagination invocation",
    "not projection",
    "not ECR design",
    "not Cleaning implementation",
    "not Judgment scoring",
    "not buyer proof",
]

TARGETED_RENDERED_ACCEPTED_RESIDUALS = [
    "operator-visible Chrome extension rendered artifacts are packaged from local files; this runner does not perform live browser control",
    "targeted sample only; does not claim full 369-review or 1390-statement corpus coverage",
    "source-visible high/low rating buckets require Parfumo rating fields in the supplied artifacts; otherwise bucket coverage remains residualized",
    "direct HTTP/AJAX is canary/fallback only in the current environment",
    "no cookies, storage state, Cloudflare clearance, proxy endpoint, or exit-IP values may be exported into packet text artifacts",
    "linked media assets are not independently fetched or preserved",
    "projection, ECR, cleaning, judgment scoring, and buyer-proof claims are intentionally out of scope",
]

TARGETED_RENDERED_NON_CLAIMS = [
    "not full Parfumo corpus capture",
    "not account-authenticated capture",
    "not anti-bot evasion",
    "not CAPTCHA solving",
    "not cookie export",
    "not browser storage export",
    "not Cloudflare clearance export",
    "not live network capture by this local packet writer",
    "not projection",
    "not ECR design",
    "not Cleaning implementation",
    "not Judgment scoring",
    "not buyer proof",
]

_BROWSER_SECRET_PATTERNS = (
    "cf_clearance",
    "Cookie:",
    "Set-Cookie",
    "storageState",
    "localStorage",
    "sessionStorage",
    "__cf_chl_",
)

PacketRunner = Callable[..., tuple[int, str | Path]]


def run_parfumo_mgt_capture(
    *,
    url: str,
    output_root: Path,
    data_root: "DataLakeRoot | None" = None,
    decision_question: str = DEFAULT_DECISION_QUESTION,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
    http_max_bytes: int = DEFAULT_HTTP_MAX_BYTES,
    http_runner: PacketRunner = run_source_capture_http_packet,
) -> tuple[int, str]:
    """Run the anonymous Parfumo direct-HTTP capture recipe and write a local summary."""

    _validate_parfumo_url(url)
    _validate_positive("timeout_seconds", timeout_seconds)
    _validate_positive("http_max_bytes", http_max_bytes)
    _prepare_output_root(output_root)

    exit_code, message = http_runner(
        url=url,
        source_family=SOURCE_FAMILY,
        source_surface=DIRECT_HTTP_SURFACE,
        decision_question=decision_question,
        output_directory=None if data_root is not None else output_root / DIRECT_HTTP_SLOT,
        data_root=data_root,
        capture_context=(
            "Parfumo native direct HTTP capture preserving publicly returned server HTML "
            "without login, session, profile, proxy, credentials, AJAX pagination, or "
            "anti-bot evasion."
        ),
        operator_category=DEFAULT_OPERATOR_CATEGORY,
        capture_mode=CaptureModeCategory.STRUCTURED_ACCESS,
        session_id=None,
        actor_audience_context=_anonymous_actor_context(),
        visible_mode_changes=["direct HTTP response body captured; no browser viewport rendered"],
        source_publication_or_event=_unknown_source_publication(),
        source_edit_or_version=_unknown_source_edit(),
        cutoff_posture=_unknown_cutoff_posture(),
        recapture_time=_not_a_recapture(),
        re_capture_relationship=_not_a_recapture_relationship(),
        warnings=[],
        limitations=ACCEPTED_RESIDUALS,
        timeout_seconds=timeout_seconds,
        max_bytes=http_max_bytes,
        session_visibility_pin=_anonymous_session_pin(),
    )
    if exit_code != 0:
        return exit_code, f"{DIRECT_HTTP_SLOT} failed: {message}"
    direct_dir = Path(message)
    _read_manifest(direct_dir)

    summary = build_parfumo_mgt_capture_summary(
        url=url,
        output_root=output_root,
        data_root_path=Path(data_root.path) if data_root is not None else None,
        packet_directories={DIRECT_HTTP_SLOT: direct_dir},
        capture_parameters={
            "timeout_seconds": timeout_seconds,
            "http_max_bytes": http_max_bytes,
        },
    )
    summary_path = output_root / SUMMARY_FILENAME
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0, str(summary_path)


def run_parfumo_targeted_rendered_capture(
    *,
    url: str,
    output_root: Path,
    rendered_dom_path: Path,
    visible_text_path: Path,
    route_receipt_path: Path,
    screenshot_path: Path | None = None,
    data_root: "DataLakeRoot | None" = None,
    decision_question: str = DEFAULT_DECISION_QUESTION,
) -> tuple[int, str]:
    """Package operator-visible rendered Parfumo artifacts into a targeted packet.

    This is a local packet writer for fixtures or owner-supplied Chrome-extension
    artifacts. It does not drive Chrome, fetch Parfumo, export browser state, or
    invoke first-party AJAX endpoints.
    """

    _validate_parfumo_url(url)
    _prepare_output_root(output_root)
    supplied_files = [
        rendered_dom_path,
        visible_text_path,
        route_receipt_path,
        *([screenshot_path] if screenshot_path is not None else []),
    ]
    resolved_files = [path.resolve() for path in supplied_files]
    _assert_input_files_readable(resolved_files)
    _assert_no_browser_secret_text(resolved_files)

    metadata_dir = output_root / "_targeted_rendered_metadata"
    metadata_dir.mkdir(parents=True, exist_ok=True)
    plan_path = metadata_dir / TARGETED_CAPTURE_PLAN_FILENAME
    plan_path.write_text(
        json.dumps(_targeted_capture_plan(url), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    input_files = [*resolved_files, plan_path]
    file_ids = [f"file_{index:02d}" for index, _ in enumerate(input_files, start=1)]
    source_slices = _targeted_source_slices(
        url=url,
        file_ids=file_ids,
        limitations=TARGETED_RENDERED_ACCEPTED_RESIDUALS,
    )

    result = write_local_source_capture_packet(
        output_directory=None if data_root is not None else output_root / TARGETED_RENDERED_SLOT,
        data_root=data_root,
        input_files=input_files,
        source_family=SOURCE_FAMILY,
        source_surface=TARGETED_RENDERED_SURFACE,
        source_locator=known_fact(url),
        decision_question=decision_question,
        capture_context=(
            "Parfumo targeted high-value rendered packet from operator-visible Chrome "
            "extension artifacts; local writer only, no live browser control, no cookie "
            "or browser-storage export, no full-corpus claim."
        ),
        actor_audience_context=known_fact(
            "operator-visible Chrome browser with Codex extension; no exported cookies, storage state, or clearance tokens"
        ),
        capture_mode=CaptureModeCategory.HUMAN_LED,
        operator_category=DEFAULT_OPERATOR_CATEGORY,
        visible_mode_changes=[
            "rendered DOM preserved from operator-visible browser artifacts",
            "visible text preserved from operator-visible browser artifacts",
            "route receipt preserved without browser-secret export",
        ],
        access_posture=known_fact(
            "operator-visible Chrome extension rendered Parfumo public product page artifacts supplied locally"
        ),
        archive_history_posture=not_attempted("targeted rendered Parfumo packet does not query archives"),
        media_modality_posture=not_attempted(
            "linked media assets were not independently fetched or preserved"
        ),
        re_capture_relationship=not_applicable("first targeted rendered Parfumo packet"),
        source_slices=source_slices,
        warnings=[],
        limitations=TARGETED_RENDERED_ACCEPTED_RESIDUALS,
        receipt_summary=(
            "Targeted Parfumo rendered packet for current-window/high-value review "
            "and statement samples. The packet preserves supplied local artifacts only "
            "and does not claim full corpus coverage."
        ),
        receipt_non_claims=TARGETED_RENDERED_NON_CLAIMS,
    )

    packet_dir = Path(result.output_directory)
    summary = build_parfumo_mgt_capture_summary(
        url=url,
        output_root=output_root,
        data_root_path=Path(data_root.path) if data_root is not None else None,
        packet_directories={TARGETED_RENDERED_SLOT: packet_dir},
        capture_parameters={
            "rendered_dom_path": str(rendered_dom_path),
            "visible_text_path": str(visible_text_path),
            "route_receipt_path": str(route_receipt_path),
            "screenshot_path": str(screenshot_path) if screenshot_path is not None else None,
        },
        capture_profile=TARGETED_RENDERED_CAPTURE_PROFILE,
        accepted_residuals=TARGETED_RENDERED_ACCEPTED_RESIDUALS,
        non_claims=TARGETED_RENDERED_NON_CLAIMS,
        projection_status="not_run; projection is Batch 2 over the targeted rendered packet",
    )
    summary_path = output_root / SUMMARY_FILENAME
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0, str(summary_path)


def build_parfumo_mgt_capture_summary(
    *,
    url: str,
    output_root: Path,
    data_root_path: Path | None,
    packet_directories: Mapping[str, Path],
    capture_parameters: Mapping[str, object],
    capture_profile: str = CAPTURE_PROFILE,
    accepted_residuals: Sequence[str] = ACCEPTED_RESIDUALS,
    non_claims: Sequence[str] = NON_CLAIMS,
    projection_status: str = "not_run; projection is a later lane over the raw packet evidence",
) -> dict[str, object]:
    packet_roles: dict[str, dict[str, object]] = {}
    for slot, packet_dir in packet_directories.items():
        manifest = _read_manifest(packet_dir)
        packet_roles[slot] = {
            "packet_id": manifest.get("packet_id"),
            "source_family": manifest.get("source_family"),
            "source_surface": manifest.get("source_surface"),
            "packet_path": str(packet_dir),
            "access_posture": manifest.get("access_posture"),
            "archive_history_posture": manifest.get("archive_history_posture"),
            "slice_postures": _slice_postures(manifest),
        }

    return {
        "capture_profile": capture_profile,
        "source_family": SOURCE_FAMILY,
        "source_url": url,
        "parfumo_product_slug": extract_parfumo_product_slug(url),
        "summary_generated_at": _utc_now_z(),
        "packet_publication_mode": (
            "data_lake_raw_packets_with_local_summary"
            if data_root_path is not None
            else "local_output_bundle"
        ),
        "data_root": str(data_root_path) if data_root_path is not None else None,
        "output_root": str(output_root),
        "packet_roles": packet_roles,
        "accepted_residuals": list(accepted_residuals),
        "non_claims": list(non_claims),
        "capture_parameters": dict(capture_parameters),
        "projection_status": projection_status,
    }


def extract_parfumo_product_slug(url: str) -> str | None:
    parsed = urlparse(url)
    match = re.search(r"/Perfumes/([^/]+/[^/?#]+)", parsed.path, flags=re.IGNORECASE)
    return match.group(1) if match else None


def preflight_parfumo_mgt_capture(*, url: str, output_root: Path) -> str:
    _validate_parfumo_url(url)
    _assert_output_root_available(output_root)
    slug = extract_parfumo_product_slug(url) or "unknown"
    return (
        "parfumo native capture preflight passed; no network capture attempted; "
        f"product_slug={slug}; output_root={output_root}"
    )


def _targeted_capture_plan(url: str) -> dict[str, object]:
    return {
        "contract": "docs/workflows/parfumo_targeted_capture_contract_v0.md",
        "source_surface": TARGETED_RENDERED_SURFACE,
        "url": url,
        "sample_buckets": [
            {"bucket": bucket, "description": description}
            for bucket, description in TARGETED_SAMPLE_BUCKETS
        ],
        "residuals": list(TARGETED_RENDERED_ACCEPTED_RESIDUALS),
        "non_claims": list(TARGETED_RENDERED_NON_CLAIMS),
    }


def _targeted_source_slices(
    *,
    url: str,
    file_ids: Sequence[str],
    limitations: Sequence[str],
) -> list[SourceCaptureSlice]:
    timing = PacketTiming(
        source_publication_or_event=unknown_with_reason(
            "Parfumo product-page publication or review/statement event timing is per-row projection work"
        ),
        source_edit_or_version=unknown_with_reason(
            "Parfumo product-page edit or version timing was not supplied"
        ),
        capture_time=known_fact(_utc_now_z()),
        recapture_time=not_applicable("first targeted rendered Parfumo packet"),
        cutoff_posture=unknown_with_reason(
            "Parfumo targeted rendered capture does not model an external cutoff posture"
        ),
    )
    access = known_fact(
        "operator-visible Chrome extension rendered Parfumo public product page artifacts supplied locally"
    )
    archive = not_attempted("targeted rendered Parfumo packet does not query archives")
    media = not_attempted("linked media assets were not independently fetched or preserved")
    recapture = not_applicable("first targeted rendered Parfumo packet")

    return [
        SourceCaptureSlice(
            slice_id=f"parfumo_targeted:{bucket}",
            locator=known_fact(url),
            timing=timing,
            access_posture=access,
            archive_history_posture=archive,
            media_modality_posture=media,
            re_capture_relationship=recapture,
            limitations=list(limitations),
            warning_notes=[],
            preserved_file_ids=list(file_ids),
        )
        for bucket, _ in TARGETED_SAMPLE_BUCKETS
    ]


def _slice_postures(manifest: Mapping[str, object]) -> list[dict[str, object]]:
    source_slices = manifest.get("source_slices")
    if not isinstance(source_slices, list):
        return []

    postures: list[dict[str, object]] = []
    for source_slice in source_slices:
        if not isinstance(source_slice, dict):
            continue
        postures.append(
            {
                "slice_id": source_slice.get("slice_id"),
                "access_posture": source_slice.get("access_posture"),
                "archive_history_posture": source_slice.get("archive_history_posture"),
            }
        )
    return postures


def _read_manifest(packet_dir: Path) -> dict[str, object]:
    manifest_path = packet_dir / "manifest.json"
    if not manifest_path.exists():
        raise ValueError(f"packet manifest not found: {manifest_path}")
    loaded = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise ValueError(f"packet manifest is not a JSON object: {manifest_path}")
    return loaded


def _assert_input_files_readable(paths: Sequence[Path]) -> None:
    for path in paths:
        if not path.exists():
            raise FileNotFoundError(f"targeted rendered artifact does not exist: {path}")
        if not path.is_file():
            raise ValueError(f"targeted rendered artifact is not a file: {path}")


def _assert_no_browser_secret_text(paths: Sequence[Path]) -> None:
    for path in paths:
        sample = path.read_bytes().decode("utf-8", errors="ignore")
        for pattern in _BROWSER_SECRET_PATTERNS:
            if pattern in sample:
                raise ValueError(
                    "targeted rendered artifact appears to contain browser-secret material "
                    f"({pattern!r}) at {path}"
                )


def _validate_parfumo_url(url: str) -> None:
    parsed = urlparse(url)
    hostname = (parsed.hostname or "").lower()
    if (
        parsed.scheme not in {"http", "https"}
        or not _is_parfumo_hostname(hostname)
        or not re.search(r"^/Perfumes/[^/]+/[^/]+", parsed.path, flags=re.IGNORECASE)
    ):
        raise ValueError("Parfumo native capture requires an absolute parfumo.com /Perfumes/ product URL")


def _is_parfumo_hostname(hostname: str) -> bool:
    return hostname == "parfumo.com" or hostname.endswith(".parfumo.com")


def _validate_positive(name: str, value: int | float) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be positive")


def _prepare_output_root(output_root: Path) -> None:
    _assert_output_root_available(output_root)
    output_root.mkdir(parents=True, exist_ok=True)


def _assert_output_root_available(output_root: Path) -> None:
    if output_root.exists() and not output_root.is_dir():
        raise ValueError(f"output root exists and is not a directory: {output_root}")
    if output_root.exists() and any(output_root.iterdir()):
        raise ValueError(f"output root must be absent or empty: {output_root}")


def _anonymous_actor_context():
    return known_fact(
        "anonymous public Parfumo visitor; no login, stored session, profile, proxy, or credentials supplied"
    )


def _anonymous_session_pin():
    return known_fact("anonymous logged-out capture; no stored session, profile, proxy, or credentials supplied")


def _unknown_source_publication():
    return unknown_with_reason("Parfumo product page publication or event timing was not supplied")


def _unknown_source_edit():
    return unknown_with_reason("Parfumo product page edit or version timing was not supplied")


def _unknown_cutoff_posture():
    return unknown_with_reason("Parfumo native capture does not model an external cutoff posture")


def _not_a_recapture():
    return not_applicable("Parfumo native wrapper did not receive a prior packet recapture time")


def _not_a_recapture_relationship():
    return not_applicable("Parfumo native wrapper did not receive a prior packet relationship")


def _utc_now_z() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the anonymous Parfumo native direct-HTTP capture recipe."
    )
    parser.add_argument("--url", required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument(
        "--targeted-rendered",
        action="store_true",
        help="Package local Chrome-extension rendered artifacts instead of running direct HTTP.",
    )
    parser.add_argument("--rendered-dom", type=Path, default=None)
    parser.add_argument("--visible-text", type=Path, default=None)
    parser.add_argument("--route-receipt", type=Path, default=None)
    parser.add_argument("--screenshot", type=Path, default=None)
    parser.add_argument(
        "--data-root",
        type=Path,
        default=None,
        help=(
            "Optional explicit Orca data lake root. When supplied, the packet is committed "
            "to raw/<shard>/<packet_id>; the bundle summary remains under --output-root."
        ),
    )
    parser.add_argument("--decision-question", default=DEFAULT_DECISION_QUESTION)
    parser.add_argument("--timeout-seconds", type=float, default=DEFAULT_TIMEOUT_SECONDS)
    parser.add_argument("--http-max-bytes", type=int, default=DEFAULT_HTTP_MAX_BYTES)
    parser.add_argument(
        "--preflight-only",
        action="store_true",
        help="Validate Parfumo URL and output-root availability, then exit without network capture.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        if args.preflight_only:
            print(preflight_parfumo_mgt_capture(url=args.url, output_root=args.output_root))
            return 0

        data_root = None
        data_root_requested = args.data_root is not None or os.environ.get("ORCA_DATA_ROOT")
        if data_root_requested:
            from data_lake.root import DataLakeRoot

            data_root = DataLakeRoot.resolve(explicit=args.data_root)

        if args.targeted_rendered:
            missing = [
                name
                for name, value in (
                    ("--rendered-dom", args.rendered_dom),
                    ("--visible-text", args.visible_text),
                    ("--route-receipt", args.route_receipt),
                )
                if value is None
            ]
            if missing:
                raise ValueError("--targeted-rendered requires " + ", ".join(missing))
            exit_code, message = run_parfumo_targeted_rendered_capture(
                url=args.url,
                output_root=args.output_root,
                rendered_dom_path=args.rendered_dom,
                visible_text_path=args.visible_text,
                route_receipt_path=args.route_receipt,
                screenshot_path=args.screenshot,
                data_root=data_root,
                decision_question=args.decision_question,
            )
        else:
            exit_code, message = run_parfumo_mgt_capture(
                url=args.url,
                output_root=args.output_root,
                data_root=data_root,
                decision_question=args.decision_question,
                timeout_seconds=args.timeout_seconds,
                http_max_bytes=args.http_max_bytes,
            )
    except ValueError as exc:
        parser.exit(status=2, message=f"parfumo native capture failed: {exc}\n")
    except Exception as exc:
        parser.exit(status=3, message=f"parfumo native capture failed: {exc}\n")

    if exit_code == 0:
        print(message)
        return 0
    parser.exit(status=exit_code, message=f"parfumo native capture failed: {message}\n")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
