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
from source_capture import CaptureModeCategory, known_fact, not_applicable, unknown_with_reason
from source_capture.proxy_profiles import ProxyProfile, load_proxy_profile_by_label

if TYPE_CHECKING:
    from data_lake.root import DataLakeRoot


SOURCE_FAMILY = "fragrance_native_database"
CAPTURE_PROFILE = "basenotes_native_cloakbrowser_residential_proxy_v0"
SUMMARY_FILENAME = "basenotes_native_capture_summary.json"

CLOAKBROWSER_SLOT = "cloakbrowser_packet"
CLOAKBROWSER_SURFACE = "basenotes_product_page_cloakbrowser_deep_scroll_current_window"

# Capture-route facts (anonymous direct/anti-block/browser all hit Cloudflare; the
# residential-proxy CloakBrowser route is the only reaching route) are pinned in
# docs/research/orca_fragrance_native_database_live_probe_v0.md -- PIN-003 plus its
# Proxy Route Verification Addendum. Referenced here, not restated.
PROXY_PROFILE_LABEL = "reddit-res-01"

DEFAULT_DECISION_QUESTION = (
    "What public Basenotes product-page evidence was available for this fragrance at capture time?"
)
DEFAULT_OPERATOR_CATEGORY = "basenotes_native_capture_runner"
DEFAULT_TIMEOUT_SECONDS = 90.0
DEFAULT_SETTLE_SECONDS = 15.0
DEFAULT_SCROLL_PASSES = 20
DEFAULT_MAX_ARTIFACT_BYTES = 10_000_000
DEFAULT_WAIT_UNTIL = "load"
DEFAULT_VIEWPORT_WIDTH = 1280
DEFAULT_VIEWPORT_HEIGHT = 720

ACCEPTED_RESIDUALS = [
    "Basenotes is Cloudflare-blocked for anonymous direct, anti-block, and browser routes; "
    "capture uses CloakBrowser through a label-indirected residential proxy (PIN-003 addendum)",
    "rendered current-window product page only; in-page JSON-LD carries a review subset, not the "
    "declared full review corpus reachable through the /reviews/ sub-URL and sentiment tabs",
    "linked media assets are not independently fetched or preserved beyond the viewport screenshot",
    "projection, ECR, cleaning, judgment scoring, and buyer-proof claims are intentionally out of scope",
]

NON_CLAIMS = [
    "not full Basenotes review-corpus capture",
    "not account-authenticated capture",
    "not anti-bot evasion proof",
    "not review sub-URL pagination invocation",
    "not projection",
    "not ECR design",
    "not Cleaning implementation",
    "not Judgment scoring",
    "not buyer proof",
]

PacketRunner = Callable[..., tuple[int, str]]


def run_basenotes_mgt_capture(
    *,
    url: str,
    output_root: Path,
    data_root: "DataLakeRoot | None" = None,
    decision_question: str = DEFAULT_DECISION_QUESTION,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
    settle_seconds: float = DEFAULT_SETTLE_SECONDS,
    scroll_passes: int = DEFAULT_SCROLL_PASSES,
    max_artifact_bytes: int = DEFAULT_MAX_ARTIFACT_BYTES,
    proxy_profile: ProxyProfile | None = None,
    cloakbrowser_runner: PacketRunner = run_source_capture_cloakbrowser_packet,
) -> tuple[int, str]:
    """Run the Basenotes residential-proxy CloakBrowser capture recipe and write a summary.

    The live path captures via ``fetch_cloakbrowser_snapshot_capture`` (through
    ``run_source_capture_cloakbrowser_packet``) using the residential proxy profile;
    anonymous routes are Cloudflare-blocked (PIN-003 + Proxy Route Verification
    Addendum). The proxy profile is loaded by label when not injected, so a caller
    that has not provisioned the secret store can still run the no-network preflight.
    """

    _validate_basenotes_url(url)
    _validate_positive("timeout_seconds", timeout_seconds)
    _validate_positive("max_artifact_bytes", max_artifact_bytes)
    _validate_non_negative("settle_seconds", settle_seconds)
    _validate_non_negative("scroll_passes", scroll_passes)
    _prepare_output_root(output_root)

    if proxy_profile is None:
        proxy_profile = load_proxy_profile_by_label(PROXY_PROFILE_LABEL)

    exit_code, message = cloakbrowser_runner(
        url=url,
        source_family=SOURCE_FAMILY,
        source_surface=CLOAKBROWSER_SURFACE,
        decision_question=decision_question,
        output_directory=None if data_root is not None else output_root / CLOAKBROWSER_SLOT,
        data_root=data_root,
        capture_context=(
            "Basenotes native CloakBrowser anti-blocking browser capture of the rendered "
            "product page through a label-indirected residential proxy, with a settle and "
            "deep-scroll pass so the lazy-rendered review section populates; no login, "
            "stored session, browser profile, or credential injection."
        ),
        operator_category=DEFAULT_OPERATOR_CATEGORY,
        capture_mode=CaptureModeCategory.MULTIMODAL,
        session_id=None,
        proxy_profile=proxy_profile,
        actor_audience_context=_anonymous_actor_context(),
        visible_mode_changes=[
            "rendered browser viewport captured after settle and deep-scroll; "
            "no logged-in session"
        ],
        source_publication_or_event=_unknown_source_publication(),
        source_edit_or_version=_unknown_source_edit(),
        cutoff_posture=_unknown_cutoff_posture(),
        recapture_time=_not_a_recapture(),
        re_capture_relationship=_not_a_recapture_relationship(),
        warnings=[],
        limitations=ACCEPTED_RESIDUALS,
        timeout_seconds=timeout_seconds,
        wait_until=DEFAULT_WAIT_UNTIL,
        viewport_width=DEFAULT_VIEWPORT_WIDTH,
        viewport_height=DEFAULT_VIEWPORT_HEIGHT,
        max_artifact_bytes=max_artifact_bytes,
        block_heavy_assets=False,
        settle_seconds=settle_seconds,
        scroll_passes=scroll_passes,
        session_visibility_pin=_anonymous_session_pin(),
    )
    if exit_code != 0:
        return exit_code, f"{CLOAKBROWSER_SLOT} failed: {message}"
    cloak_dir = Path(message)
    _read_manifest(cloak_dir)

    summary = build_basenotes_mgt_capture_summary(
        url=url,
        output_root=output_root,
        data_root_path=Path(data_root.path) if data_root is not None else None,
        packet_directories={CLOAKBROWSER_SLOT: cloak_dir},
        capture_parameters={
            "timeout_seconds": timeout_seconds,
            "settle_seconds": settle_seconds,
            "scroll_passes": scroll_passes,
            "max_artifact_bytes": max_artifact_bytes,
            "proxy_profile_label_indirected": True,
        },
    )
    summary_path = output_root / SUMMARY_FILENAME
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0, str(summary_path)


def build_basenotes_mgt_capture_summary(
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
        "source_family": SOURCE_FAMILY,
        "source_url": url,
        "basenotes_product_slug": extract_basenotes_product_slug(url),
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


def extract_basenotes_product_slug(url: str) -> str | None:
    parsed = urlparse(url)
    match = re.search(r"/fragrances/([^/?#]+)", parsed.path, flags=re.IGNORECASE)
    return match.group(1) if match else None


def preflight_basenotes_mgt_capture(*, url: str, output_root: Path) -> str:
    _validate_basenotes_url(url)
    _assert_output_root_available(output_root)
    slug = extract_basenotes_product_slug(url) or "unknown"
    return (
        "basenotes native capture preflight passed; no network capture attempted; "
        f"product_slug={slug}; proxy_profile_label={PROXY_PROFILE_LABEL}; output_root={output_root}"
    )


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


def _validate_basenotes_url(url: str) -> None:
    parsed = urlparse(url)
    hostname = (parsed.hostname or "").lower()
    if (
        parsed.scheme not in {"http", "https"}
        or not _is_basenotes_hostname(hostname)
        or not re.search(r"^/fragrances/[^/]+", parsed.path, flags=re.IGNORECASE)
    ):
        raise ValueError(
            "Basenotes native capture requires an absolute basenotes.com /fragrances/ product URL"
        )


def _is_basenotes_hostname(hostname: str) -> bool:
    return hostname == "basenotes.com" or hostname.endswith(".basenotes.com")


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
        "anonymous public Basenotes visitor through a label-indirected residential proxy; "
        "no login, stored session, browser profile, or credentials supplied"
    )


def _anonymous_session_pin():
    return known_fact(
        "anonymous logged-out capture; no stored session, browser profile, or credentials supplied"
    )


def _unknown_source_publication():
    return unknown_with_reason("Basenotes product page publication or event timing was not supplied")


def _unknown_source_edit():
    return unknown_with_reason("Basenotes product page edit or version timing was not supplied")


def _unknown_cutoff_posture():
    return unknown_with_reason("Basenotes native capture does not model an external cutoff posture")


def _not_a_recapture():
    return not_applicable("Basenotes native wrapper did not receive a prior packet recapture time")


def _not_a_recapture_relationship():
    return not_applicable("Basenotes native wrapper did not receive a prior packet relationship")


def _utc_now_z() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Run the Basenotes native CloakBrowser residential-proxy capture recipe "
            "(anonymous routes are Cloudflare-blocked; see live-probe PIN-003 addendum)."
        )
    )
    parser.add_argument("--url", required=True)
    parser.add_argument("--output-root", type=Path, required=True)
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
    parser.add_argument("--settle-seconds", type=float, default=DEFAULT_SETTLE_SECONDS)
    parser.add_argument("--scroll-passes", type=int, default=DEFAULT_SCROLL_PASSES)
    parser.add_argument("--max-artifact-bytes", type=int, default=DEFAULT_MAX_ARTIFACT_BYTES)
    parser.add_argument(
        "--preflight-only",
        action="store_true",
        help="Validate Basenotes URL and output-root availability, then exit without network capture.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        if args.preflight_only:
            print(preflight_basenotes_mgt_capture(url=args.url, output_root=args.output_root))
            return 0

        data_root = None
        if args.data_root is not None:
            from data_lake.root import DataLakeRoot

            data_root = DataLakeRoot.resolve(explicit=args.data_root)

        exit_code, message = run_basenotes_mgt_capture(
            url=args.url,
            output_root=args.output_root,
            data_root=data_root,
            decision_question=args.decision_question,
            timeout_seconds=args.timeout_seconds,
            settle_seconds=args.settle_seconds,
            scroll_passes=args.scroll_passes,
            max_artifact_bytes=args.max_artifact_bytes,
        )
    except ValueError as exc:
        parser.exit(status=2, message=f"basenotes native capture failed: {exc}\n")
    except Exception as exc:
        parser.exit(status=3, message=f"basenotes native capture failed: {exc}\n")

    if exit_code == 0:
        print(message)
        return 0
    parser.exit(status=exit_code, message=f"basenotes native capture failed: {message}\n")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
