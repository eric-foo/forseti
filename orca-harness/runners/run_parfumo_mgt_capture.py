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

from runners.run_source_capture_http_packet import run_source_capture_http_packet
from source_capture import CaptureModeCategory, known_fact, not_applicable, unknown_with_reason

if TYPE_CHECKING:
    from data_lake.root import DataLakeRoot


SOURCE_FAMILY = "fragrance_native_database"
CAPTURE_PROFILE = "parfumo_native_direct_http_v0"
SUMMARY_FILENAME = "parfumo_native_capture_summary.json"

DIRECT_HTTP_SLOT = "direct_http_packet"
DIRECT_HTTP_SURFACE = "parfumo_product_page_direct_http"

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


def build_parfumo_mgt_capture_summary(
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
        "accepted_residuals": list(ACCEPTED_RESIDUALS),
        "non_claims": list(NON_CLAIMS),
        "capture_parameters": dict(capture_parameters),
        "projection_status": "not_run; projection is a later lane over the raw packet evidence",
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
        if args.data_root is not None:
            from data_lake.root import DataLakeRoot

            data_root = DataLakeRoot.resolve(explicit=args.data_root)

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
