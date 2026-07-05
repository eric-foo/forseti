from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Callable, Mapping, Sequence
from urllib.parse import urlparse

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from runners.run_source_capture_cloakbrowser_packet import run_source_capture_cloakbrowser_packet
from runners.run_source_capture_http_packet import run_source_capture_http_packet
from source_capture import CaptureModeCategory, known_fact, not_applicable, unknown_with_reason

if TYPE_CHECKING:
    from data_lake.root import DataLakeRoot


SOURCE_FAMILY = "fragrance_native_database"
CAPTURE_PROFILE = "fragrantica_mini_god_tier_v1"
SUMMARY_FILENAME = "fragrantica_mgt_capture_summary.json"

DIRECT_HTTP_SLOT = "direct_http_packet"
INITIAL_VIEWPORT_SLOT = "initial_viewport_packet"
DEEP_SCROLL_SLOT = "deep_scroll_packet"

DIRECT_HTTP_SURFACE = "fragrantica_product_page_direct_http"
INITIAL_VIEWPORT_SURFACE = "fragrantica_product_page_cloakbrowser_initial_viewport"
DEEP_SCROLL_SURFACE = "fragrantica_product_page_cloakbrowser_deep_scroll_current_window"

DEFAULT_DECISION_QUESTION = (
    "What public Fragrantica product-page evidence was available for this fragrance at capture time?"
)
DEFAULT_OPERATOR_CATEGORY = "fragrantica_mgt_capture_runner"
DEFAULT_VIEWPORT_WIDTH = 1280
DEFAULT_VIEWPORT_HEIGHT = 900
DEFAULT_INITIAL_SETTLE_SECONDS = 8.0
DEFAULT_DEEP_SETTLE_SECONDS = 10.0
DEFAULT_DEEP_SCROLL_PASSES = 25
DEFAULT_DEEP_SCROLL_STEP_PX = 500
DEFAULT_TIMEOUT_SECONDS = 120.0
DEFAULT_HTTP_MAX_BYTES = 10_000_000
DEFAULT_MAX_ARTIFACT_BYTES = 25_000_000

ACCEPTED_RESIDUALS = [
    "anonymous Mini God Tier capture only; no login, stored session, profile, proxy, or credential injection",
    "does not attempt Fragrantica's login-gated full review archive or claim complete review coverage",
    "direct HTTP packet preserves server HTML and embedded structured attributes when publicly returned",
    "rendered packets preserve current-window browser DOM, visible text, screenshot, and method metadata only",
    "linked media assets are not independently fetched or preserved beyond viewport screenshots",
    "projection, ECR, cleaning, judgment scoring, and buyer-proof claims are intentionally out of scope",
]

NON_CLAIMS = [
    "not full Fragrantica archive capture",
    "not account-authenticated capture",
    "not anti-login-gate bypass",
    "not projection",
    "not ECR design",
    "not Cleaning implementation",
    "not Judgment scoring",
    "not buyer proof",
]

PacketRunner = Callable[..., tuple[int, str | Path]]


def run_fragrantica_mgt_capture(
    *,
    url: str,
    output_root: Path,
    data_root: "DataLakeRoot | None" = None,
    decision_question: str = DEFAULT_DECISION_QUESTION,
    viewport_width: int = DEFAULT_VIEWPORT_WIDTH,
    viewport_height: int = DEFAULT_VIEWPORT_HEIGHT,
    initial_settle_seconds: float = DEFAULT_INITIAL_SETTLE_SECONDS,
    deep_settle_seconds: float = DEFAULT_DEEP_SETTLE_SECONDS,
    deep_scroll_passes: int = DEFAULT_DEEP_SCROLL_PASSES,
    deep_scroll_step_px: int = DEFAULT_DEEP_SCROLL_STEP_PX,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
    http_max_bytes: int = DEFAULT_HTTP_MAX_BYTES,
    max_artifact_bytes: int = DEFAULT_MAX_ARTIFACT_BYTES,
    http_runner: PacketRunner = run_source_capture_http_packet,
    cloakbrowser_runner: PacketRunner = run_source_capture_cloakbrowser_packet,
) -> tuple[int, str]:
    """Run the anonymous Fragrantica MGT capture recipe and write a local bundle summary."""

    _validate_fragrantica_url(url)
    _validate_positive("viewport_width", viewport_width)
    _validate_positive("viewport_height", viewport_height)
    _validate_positive("timeout_seconds", timeout_seconds)
    _validate_positive("http_max_bytes", http_max_bytes)
    _validate_positive("max_artifact_bytes", max_artifact_bytes)
    _validate_non_negative("initial_settle_seconds", initial_settle_seconds)
    _validate_non_negative("deep_settle_seconds", deep_settle_seconds)
    _validate_non_negative("deep_scroll_passes", deep_scroll_passes)
    _validate_non_negative("deep_scroll_step_px", deep_scroll_step_px)
    _prepare_output_root(output_root)

    direct_dir: Path
    initial_dir: Path
    deep_dir: Path

    exit_code, message = http_runner(
        url=url,
        source_family=SOURCE_FAMILY,
        source_surface=DIRECT_HTTP_SURFACE,
        decision_question=decision_question,
        output_directory=None if data_root is not None else output_root / DIRECT_HTTP_SLOT,
        data_root=data_root,
        capture_context=(
            "Fragrantica Mini God Tier direct HTTP capture preserving publicly returned "
            "server HTML and embedded structured attributes without login, session, proxy, "
            "stored profile, or archive access."
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

    exit_code, message = cloakbrowser_runner(
        url=url,
        source_family=SOURCE_FAMILY,
        source_surface=INITIAL_VIEWPORT_SURFACE,
        decision_question=decision_question,
        output_directory=None if data_root is not None else output_root / INITIAL_VIEWPORT_SLOT,
        data_root=data_root,
        capture_context=(
            "Fragrantica Mini God Tier initial-viewport browser capture preserving the rendered "
            "above-fold/current viewport state without login, session, proxy, stored profile, "
            "credential injection, or archive access."
        ),
        operator_category=DEFAULT_OPERATOR_CATEGORY,
        capture_mode=CaptureModeCategory.MULTIMODAL,
        session_id=None,
        proxy_profile=None,
        actor_audience_context=_anonymous_actor_context(),
        visible_mode_changes=[
            "rendered browser page captured after settle without scrolling; intended to preserve initial viewport evidence"
        ],
        source_publication_or_event=_unknown_source_publication(),
        source_edit_or_version=_unknown_source_edit(),
        cutoff_posture=_unknown_cutoff_posture(),
        recapture_time=_not_a_recapture(),
        re_capture_relationship=_not_a_recapture_relationship(),
        warnings=[],
        limitations=ACCEPTED_RESIDUALS,
        timeout_seconds=timeout_seconds,
        wait_until="load",
        viewport_width=viewport_width,
        viewport_height=viewport_height,
        max_artifact_bytes=max_artifact_bytes,
        block_heavy_assets=False,
        settle_seconds=initial_settle_seconds,
        scroll_passes=0,
        load_more_selector=None,
        load_more_clicks=0,
        scroll_step_px=0,
        session_visibility_pin=_anonymous_session_pin(),
    )
    if exit_code != 0:
        return exit_code, f"{INITIAL_VIEWPORT_SLOT} failed: {message}"
    initial_dir = Path(message)
    _read_manifest(initial_dir)

    exit_code, message = cloakbrowser_runner(
        url=url,
        source_family=SOURCE_FAMILY,
        source_surface=DEEP_SCROLL_SURFACE,
        decision_question=decision_question,
        output_directory=None if data_root is not None else output_root / DEEP_SCROLL_SLOT,
        data_root=data_root,
        capture_context=(
            "Fragrantica Mini God Tier deep-scroll browser capture preserving the anonymous "
            "current-window rendered page after bounded incremental scrolling without login, "
            "session, proxy, stored profile, credential injection, or archive access."
        ),
        operator_category=DEFAULT_OPERATOR_CATEGORY,
        capture_mode=CaptureModeCategory.MULTIMODAL,
        session_id=None,
        proxy_profile=None,
        actor_audience_context=_anonymous_actor_context(),
        visible_mode_changes=[
            "rendered browser page captured after settle, incremental scrolling, and bounded scroll passes"
        ],
        source_publication_or_event=_unknown_source_publication(),
        source_edit_or_version=_unknown_source_edit(),
        cutoff_posture=_unknown_cutoff_posture(),
        recapture_time=_not_a_recapture(),
        re_capture_relationship=_not_a_recapture_relationship(),
        warnings=[],
        limitations=ACCEPTED_RESIDUALS,
        timeout_seconds=timeout_seconds,
        wait_until="load",
        viewport_width=viewport_width,
        viewport_height=viewport_height,
        max_artifact_bytes=max_artifact_bytes,
        block_heavy_assets=False,
        settle_seconds=deep_settle_seconds,
        scroll_passes=deep_scroll_passes,
        load_more_selector=None,
        load_more_clicks=0,
        scroll_step_px=deep_scroll_step_px,
        session_visibility_pin=_anonymous_session_pin(),
    )
    if exit_code != 0:
        return exit_code, f"{DEEP_SCROLL_SLOT} failed: {message}"
    deep_dir = Path(message)
    _read_manifest(deep_dir)

    summary = build_fragrantica_mgt_capture_summary(
        url=url,
        output_root=output_root,
        data_root_path=Path(data_root.path) if data_root is not None else None,
        packet_directories={
            DIRECT_HTTP_SLOT: direct_dir,
            INITIAL_VIEWPORT_SLOT: initial_dir,
            DEEP_SCROLL_SLOT: deep_dir,
        },
        capture_parameters={
            "viewport_width": viewport_width,
            "viewport_height": viewport_height,
            "initial_settle_seconds": initial_settle_seconds,
            "deep_settle_seconds": deep_settle_seconds,
            "deep_scroll_passes": deep_scroll_passes,
            "deep_scroll_step_px": deep_scroll_step_px,
            "timeout_seconds": timeout_seconds,
            "http_max_bytes": http_max_bytes,
            "max_artifact_bytes": max_artifact_bytes,
        },
    )
    summary_path = output_root / SUMMARY_FILENAME
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0, str(summary_path)


def build_fragrantica_mgt_capture_summary(
    *,
    url: str,
    output_root: Path,
    data_root_path: Path | None,
    packet_directories: Mapping[str, Path],
    capture_parameters: Mapping[str, object],
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
        "capture_profile": CAPTURE_PROFILE,
        "tier": "mini_god_tier",
        "source_family": SOURCE_FAMILY,
        "source_url": url,
        "fragrantica_product_id": extract_fragrantica_product_id(url),
        "summary_generated_at": _utc_now_z(),
        "packet_publication_mode": (
            "data_lake_raw_packets_with_local_summary"
            if data_root_path is not None
            else "local_output_bundle"
        ),
        "data_root": str(data_root_path) if data_root_path is not None else None,
        "output_root": str(output_root),
        "packet_roles": packet_roles,
        "accepted_residuals": list(ACCEPTED_RESIDUALS),
        "non_claims": list(NON_CLAIMS),
        "capture_parameters": dict(capture_parameters),
        "projection_status": "not_run; projection is a later lane over the raw packet evidence",
    }


def extract_fragrantica_product_id(url: str) -> str | None:
    parsed = urlparse(url)
    match = re.search(r"-(\d+)\.html$", parsed.path)
    return match.group(1) if match else None


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


def preflight_fragrantica_mgt_capture(*, url: str, output_root: Path) -> str:
    _validate_fragrantica_url(url)
    _assert_output_root_available(output_root)
    product_id = extract_fragrantica_product_id(url) or "unknown"
    return (
        "fragrantica MGT capture preflight passed; no network capture attempted; "
        f"product_id={product_id}; output_root={output_root}"
    )


def _read_manifest(packet_dir: Path) -> dict[str, object]:
    manifest_path = packet_dir / "manifest.json"
    if not manifest_path.exists():
        raise ValueError(f"packet manifest not found: {manifest_path}")
    loaded = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise ValueError(f"packet manifest is not a JSON object: {manifest_path}")
    return loaded


def _validate_fragrantica_url(url: str) -> None:
    parsed = urlparse(url)
    hostname = (parsed.hostname or "").lower()
    if parsed.scheme not in {"http", "https"} or not _is_fragrantica_hostname(hostname):
        raise ValueError("Fragrantica MGT capture requires an absolute fragrantica.com URL")


def _is_fragrantica_hostname(hostname: str) -> bool:
    return hostname == "fragrantica.com" or hostname.endswith(".fragrantica.com")


def _validate_positive(name: str, value: int | float) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be positive")


def _validate_non_negative(name: str, value: int | float) -> None:
    if value < 0:
        raise ValueError(f"{name} must be non-negative")


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
        "anonymous public Fragrantica visitor; no login, stored session, profile, proxy, or credentials supplied"
    )


def _anonymous_session_pin():
    return known_fact("anonymous logged-out capture; no stored session, profile, proxy, or credentials supplied")


def _unknown_source_publication():
    return unknown_with_reason("Fragrantica product page publication or event timing was not supplied")


def _unknown_source_edit():
    return unknown_with_reason("Fragrantica product page edit or version timing was not supplied")


def _unknown_cutoff_posture():
    return unknown_with_reason("Fragrantica MGT capture does not model an external cutoff posture")


def _not_a_recapture():
    return not_applicable("Fragrantica MGT wrapper did not receive a prior packet recapture time")


def _not_a_recapture_relationship():
    return not_applicable("Fragrantica MGT wrapper did not receive a prior packet relationship")


def _utc_now_z() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Run the anonymous Fragrantica Mini God Tier capture recipe: direct HTTP, "
            "initial rendered viewport, and bounded deep-scroll rendered packet."
        )
    )
    parser.add_argument("--url", required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument(
        "--data-root",
        type=Path,
        default=None,
        help=(
            "Optional explicit Forseti data lake root. When supplied, sub-packets are committed "
            "to raw/<shard>/<packet_id>; the bundle summary remains under --output-root."
        ),
    )
    parser.add_argument("--decision-question", default=DEFAULT_DECISION_QUESTION)
    parser.add_argument("--viewport-width", type=int, default=DEFAULT_VIEWPORT_WIDTH)
    parser.add_argument("--viewport-height", type=int, default=DEFAULT_VIEWPORT_HEIGHT)
    parser.add_argument("--initial-settle-seconds", type=float, default=DEFAULT_INITIAL_SETTLE_SECONDS)
    parser.add_argument("--deep-settle-seconds", type=float, default=DEFAULT_DEEP_SETTLE_SECONDS)
    parser.add_argument("--deep-scroll-passes", type=int, default=DEFAULT_DEEP_SCROLL_PASSES)
    parser.add_argument("--deep-scroll-step-px", type=int, default=DEFAULT_DEEP_SCROLL_STEP_PX)
    parser.add_argument("--timeout-seconds", type=float, default=DEFAULT_TIMEOUT_SECONDS)
    parser.add_argument("--http-max-bytes", type=int, default=DEFAULT_HTTP_MAX_BYTES)
    parser.add_argument("--max-artifact-bytes", type=int, default=DEFAULT_MAX_ARTIFACT_BYTES)
    parser.add_argument(
        "--preflight-only",
        action="store_true",
        help="Validate Fragrantica URL and output-root availability, then exit without network capture.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        if args.preflight_only:
            print(preflight_fragrantica_mgt_capture(url=args.url, output_root=args.output_root))
            return 0

        data_root = None
        if args.data_root is not None:
            from data_lake.root import DataLakeRoot

            data_root = DataLakeRoot.resolve(explicit=args.data_root)

        exit_code, message = run_fragrantica_mgt_capture(
            url=args.url,
            output_root=args.output_root,
            data_root=data_root,
            decision_question=args.decision_question,
            viewport_width=args.viewport_width,
            viewport_height=args.viewport_height,
            initial_settle_seconds=args.initial_settle_seconds,
            deep_settle_seconds=args.deep_settle_seconds,
            deep_scroll_passes=args.deep_scroll_passes,
            deep_scroll_step_px=args.deep_scroll_step_px,
            timeout_seconds=args.timeout_seconds,
            http_max_bytes=args.http_max_bytes,
            max_artifact_bytes=args.max_artifact_bytes,
        )
    except ValueError as exc:
        parser.exit(status=2, message=f"fragrantica MGT capture failed: {exc}\n")
    except Exception as exc:
        parser.exit(status=3, message=f"fragrantica MGT capture failed: {exc}\n")

    if exit_code == 0:
        print(message)
        return 0
    parser.exit(status=exit_code, message=f"fragrantica MGT capture failed: {message}\n")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
