from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Mapping, Sequence
from urllib.parse import urlparse

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from source_capture import (
    CaptureModeCategory,
    PacketTiming,
    SourceCaptureSlice,
    known_fact,
    not_applicable,
    not_attempted,
    unknown_with_reason,
    write_local_source_capture_packet,
)
from source_capture.source_detail_sufficiency import (
    SourceDetailSufficiencyRequirements,
    evaluate_source_detail_sufficiency,
)

if TYPE_CHECKING:
    from data_lake.root import DataLakeRoot


SOURCE_FAMILY = "fragrance_native_database"
CAPTURE_PROFILE = "basenotes_user_cleared_persistent_chrome_v0"
SUMMARY_FILENAME = "basenotes_native_capture_summary.json"

PERSISTENT_CHROME_SLOT = "persistent_chrome_packet"
PERSISTENT_CHROME_SURFACE = (
    "basenotes_product_page_user_cleared_persistent_chrome_current_window"
)

REQUIRED_BUNDLE_FILENAMES = (
    "browser_rendered_dom.html",
    "browser_visible_text.txt",
    "browser_viewport_screenshot.png",
    "browser_snapshot_metadata.json",
)

DEFAULT_DECISION_QUESTION = (
    "What public Basenotes product-page evidence was available for this fragrance at capture time?"
)
DEFAULT_OPERATOR_CATEGORY = "basenotes_user_assisted_persistent_chrome_capture_runner"
DEFAULT_MAX_ARTIFACT_BYTES = 10_000_000

ACCEPTED_RESIDUALS = [
    "capture requires a user-visible persistent Chrome tab whose Cloudflare access gate was "
    "completed by the user before export; the runner does not automate or solve the gate",
    "the runner ingests public rendered DOM, visible text, one viewport screenshot, and "
    "non-secret metadata; it does not inspect or export cookies, credentials, or browser-profile data",
    "rendered current-window product page only; in-page JSON-LD carries a review subset, not the "
    "declared full review corpus reachable through the /reviews/ sub-URL and sentiment tabs",
    "one successful page does not establish unattended reliability, site-wide completeness, scale, "
    "or production readiness",
]

NON_CLAIMS = [
    "not unattended Basenotes capture proof",
    "not full Basenotes review-corpus capture",
    "not login, credential, cookie, or browser-profile export",
    "not CAPTCHA automation or solving by the runner",
    "not proxy or session injection",
    "not review sub-URL pagination invocation",
    "not projection, Cleaning, Judgment, buyer proof, or production readiness",
]

_CHALLENGE_TEXT_RE = re.compile(
    r"performing security verification|verif(?:y|ies) you are not a bot|just a moment",
    flags=re.IGNORECASE,
)


@dataclass(frozen=True)
class PersistentChromeBundle:
    paths: tuple[Path, ...]
    rendered_dom: str
    visible_text: str
    metadata: Mapping[str, object]


def run_basenotes_mgt_capture(
    *,
    url: str,
    bundle_directory: Path,
    output_root: Path,
    data_root: "DataLakeRoot | None" = None,
    decision_question: str = DEFAULT_DECISION_QUESTION,
    max_artifact_bytes: int = DEFAULT_MAX_ARTIFACT_BYTES,
) -> tuple[int, str]:
    """Validate a user-cleared persistent-Chrome export and publish one packet.

    The browser controller is deliberately outside this runner. The operator supplies
    the four public-page artifacts after completing any visible Cloudflare gate in a
    persistent, headed Chrome tab. This runner fails closed on challenge-only content,
    missing product/review evidence, unexpected files, proxy use, headless capture, or
    metadata that says cookies or credentials were exported.
    """

    _validate_basenotes_url(url)
    _validate_positive("max_artifact_bytes", max_artifact_bytes)
    bundle = _load_and_validate_bundle(
        bundle_directory=bundle_directory,
        url=url,
        max_artifact_bytes=max_artifact_bytes,
    )
    _prepare_output_root(output_root)

    timing = PacketTiming(
        source_publication_or_event=_unknown_source_publication(),
        source_edit_or_version=_unknown_source_edit(),
        capture_time=known_fact(str(bundle.metadata["capture_timestamp"])),
        recapture_time=_not_a_recapture(),
        cutoff_posture=_unknown_cutoff_posture(),
    )
    access_posture = known_fact(
        "public Basenotes product content captured only after the user completed Cloudflare "
        "verification in a persistent Chrome tab; session state was used but cookies and "
        "credentials were not inspected or exported"
    )
    archive_posture = not_attempted(
        "the persistent Chrome bundle did not query archive or history services"
    )
    media_posture = known_fact(
        "rendered DOM, visible text, and one viewport screenshot were preserved; linked media "
        "files were not independently preserved"
    )
    recapture_posture = _not_a_recapture_relationship()
    warnings = [
        "user_assisted_access_gate: user completed Cloudflare verification before public page "
        "artifacts were exported"
    ]

    result = write_local_source_capture_packet(
        output_directory=None if data_root is not None else output_root / PERSISTENT_CHROME_SLOT,
        data_root=data_root,
        input_files=list(bundle.paths),
        source_family=SOURCE_FAMILY,
        source_surface=PERSISTENT_CHROME_SURFACE,
        source_locator=known_fact(url),
        decision_question=decision_question,
        capture_context=(
            "user-cleared persistent Chrome public-page export; rendered DOM, visible text, "
            "viewport screenshot, and non-secret metadata only"
        ),
        actor_audience_context=known_fact(
            "public Basenotes fragrance product page and its source-visible review audience"
        ),
        capture_mode=CaptureModeCategory.MULTIMODAL,
        operator_category=DEFAULT_OPERATOR_CATEGORY,
        session_identity=None,
        visible_mode_changes=["human_cleared_access_gate", "persistent_user_session"],
        source_publication_or_event=timing.source_publication_or_event,
        source_edit_or_version=timing.source_edit_or_version,
        cutoff_posture=timing.cutoff_posture,
        recapture_time=timing.recapture_time,
        access_posture=access_posture,
        archive_history_posture=archive_posture,
        media_modality_posture=media_posture,
        re_capture_relationship=recapture_posture,
        source_slices=[
            SourceCaptureSlice(
                slice_id="browser_snapshot_01",
                locator=known_fact(str(bundle.metadata["final_url"])),
                timing=timing,
                access_posture=access_posture,
                archive_history_posture=archive_posture,
                media_modality_posture=media_posture,
                re_capture_relationship=recapture_posture,
                limitations=list(ACCEPTED_RESIDUALS),
                warning_notes=warnings,
                preserved_file_ids=["file_01", "file_02", "file_03", "file_04"],
            )
        ],
        warnings=warnings,
        limitations=list(ACCEPTED_RESIDUALS),
        receipt_summary=(
            "User-cleared persistent Chrome packet for one public Basenotes product page with "
            "mechanically sufficient product and review evidence."
        ),
        receipt_non_claims=list(NON_CLAIMS),
    )
    packet_dir = Path(result.output_directory)
    _read_manifest(packet_dir)

    summary = build_basenotes_mgt_capture_summary(
        url=url,
        output_root=output_root,
        data_root_path=Path(data_root.path) if data_root is not None else None,
        packet_directories={PERSISTENT_CHROME_SLOT: packet_dir},
        capture_parameters={
            "bundle_directory": str(bundle_directory),
            "max_artifact_bytes": max_artifact_bytes,
            "persistent_user_session": True,
            "human_cleared_access_gate": True,
            "cookies_or_credentials_exported": False,
            "proxy_used": False,
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


def preflight_basenotes_mgt_capture(
    *,
    url: str,
    bundle_directory: Path,
    output_root: Path,
    max_artifact_bytes: int = DEFAULT_MAX_ARTIFACT_BYTES,
) -> str:
    _validate_basenotes_url(url)
    _validate_positive("max_artifact_bytes", max_artifact_bytes)
    _assert_output_root_available(output_root)
    _load_and_validate_bundle(
        bundle_directory=bundle_directory,
        url=url,
        max_artifact_bytes=max_artifact_bytes,
    )
    slug = extract_basenotes_product_slug(url) or "unknown"
    return (
        "basenotes persistent Chrome bundle preflight passed; no network capture attempted; "
        "requires user-visible persistent Chrome plus a user-cleared access gate; public-page "
        "bundle validated with no cookie, credential, browser-profile, or proxy export; "
        f"product_slug={slug}; bundle_directory={bundle_directory}; output_root={output_root}"
    )


def _load_and_validate_bundle(
    *, bundle_directory: Path, url: str, max_artifact_bytes: int
) -> PersistentChromeBundle:
    if not bundle_directory.is_dir():
        raise ValueError(f"persistent Chrome bundle directory does not exist: {bundle_directory}")
    actual_names = {path.name for path in bundle_directory.iterdir()}
    required_names = set(REQUIRED_BUNDLE_FILENAMES)
    if actual_names != required_names:
        missing = sorted(required_names - actual_names)
        unexpected = sorted(actual_names - required_names)
        raise ValueError(
            "persistent Chrome bundle must contain exactly the four public-page artifacts; "
            f"missing={missing}; unexpected={unexpected}"
        )
    paths = tuple(bundle_directory / name for name in REQUIRED_BUNDLE_FILENAMES)
    for path in paths:
        if not path.is_file() or path.is_symlink():
            raise ValueError(f"persistent Chrome bundle artifact must be a regular file: {path}")
        size = path.stat().st_size
        if size <= 0:
            raise ValueError(f"persistent Chrome bundle artifact is empty: {path}")
        if size > max_artifact_bytes:
            raise ValueError(
                f"persistent Chrome bundle artifact exceeds max_artifact_bytes: {path} ({size})"
            )

    rendered_dom = paths[0].read_text(encoding="utf-8")
    visible_text = paths[1].read_text(encoding="utf-8")
    if paths[2].read_bytes()[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("persistent Chrome screenshot is not a PNG")
    try:
        metadata = json.loads(paths[3].read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"persistent Chrome metadata is not valid JSON: {exc}") from exc
    if not isinstance(metadata, dict):
        raise ValueError("persistent Chrome metadata must be a JSON object")
    _validate_bundle_metadata(metadata=metadata, url=url)

    title = str(metadata.get("title") or "")
    challenge_text = f"{title}\n{visible_text}"
    access_block_reason = (
        "persistent Chrome export contains Cloudflare challenge text"
        if _CHALLENGE_TEXT_RE.search(challenge_text)
        else None
    )
    sufficiency = evaluate_source_detail_sufficiency(
        requirements=_sufficiency_requirements(url),
        access_block_reason=access_block_reason,
        visible_text=visible_text,
        rendered_dom=rendered_dom,
    )
    if not sufficiency.passed:
        raise ValueError(
            "persistent Chrome bundle failed source-detail sufficiency: "
            + "; ".join(sufficiency.failure_reasons)
        )
    return PersistentChromeBundle(
        paths=paths,
        rendered_dom=rendered_dom,
        visible_text=visible_text,
        metadata=metadata,
    )


def _sufficiency_requirements(url: str) -> SourceDetailSufficiencyRequirements:
    product_path = urlparse(url).path.lstrip("/")
    return SourceDetailSufficiencyRequirements(
        require_not_access_blocked=True,
        min_visible_text_bytes=500,
        rendered_dom_regexes=(
            rf"(?is){re.escape(product_path)}",
            r'(?is)"@type"\s*:\s*"(?:https?://schema\.org/)?Product"',
            r'(?is)"review"\s*:',
            r'(?is)"reviewBody"\s*:',
        ),
    )


def _validate_bundle_metadata(*, metadata: Mapping[str, object], url: str) -> None:
    required_values = {
        "requested_url": url,
        "final_url": url,
        "headless": False,
        "persistent_user_session": True,
        "human_cleared_access_gate": True,
        "cookies_exported": False,
        "credentials_exported": False,
        "proxy_used": False,
    }
    for key, expected in required_values.items():
        if metadata.get(key) != expected:
            raise ValueError(
                f"persistent Chrome metadata requires {key}={expected!r}; "
                f"observed {metadata.get(key)!r}"
            )
    browser_channel = metadata.get("browser_channel")
    if not isinstance(browser_channel, str) or not browser_channel.strip():
        raise ValueError("persistent Chrome metadata requires a non-blank browser_channel")
    capture_timestamp = metadata.get("capture_timestamp")
    if not isinstance(capture_timestamp, str) or not capture_timestamp.strip():
        raise ValueError("persistent Chrome metadata requires capture_timestamp")
    try:
        datetime.fromisoformat(capture_timestamp.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("persistent Chrome metadata capture_timestamp must be ISO-8601") from exc


def _slice_postures(manifest: Mapping[str, object]) -> list[dict[str, object]]:
    source_slices = manifest.get("source_slices")
    if not isinstance(source_slices, list):
        return []
    return [
        {
            "slice_id": source_slice.get("slice_id"),
            "access_posture": source_slice.get("access_posture"),
            "archive_history_posture": source_slice.get("archive_history_posture"),
        }
        for source_slice in source_slices
        if isinstance(source_slice, dict)
    ]


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


def _prepare_output_root(output_root: Path) -> None:
    _assert_output_root_available(output_root)
    output_root.mkdir(parents=True, exist_ok=True)


def _assert_output_root_available(output_root: Path) -> None:
    if output_root.exists() and not output_root.is_dir():
        raise ValueError(f"output root exists and is not a directory: {output_root}")
    if output_root.exists() and any(output_root.iterdir()):
        raise ValueError(f"output root must be absent or empty: {output_root}")


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
            "Validate and publish a public-page export from a user-cleared persistent Chrome "
            "Basenotes product tab. The runner does not launch Chrome or automate the access gate."
        )
    )
    parser.add_argument("--url", required=True)
    parser.add_argument("--bundle-directory", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument(
        "--data-root",
        type=Path,
        default=None,
        help=(
            "Optional explicit Forseti data lake root. When supplied, the packet is committed "
            "to raw/<shard>/<packet_id>; the bundle summary remains under --output-root."
        ),
    )
    parser.add_argument("--decision-question", default=DEFAULT_DECISION_QUESTION)
    parser.add_argument("--max-artifact-bytes", type=int, default=DEFAULT_MAX_ARTIFACT_BYTES)
    parser.add_argument(
        "--preflight-only",
        action="store_true",
        help=(
            "Validate URL, exact four-file public-page bundle, route metadata, sufficiency, and "
            "output-root availability, then exit without publishing a packet."
        ),
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        if args.preflight_only:
            print(
                preflight_basenotes_mgt_capture(
                    url=args.url,
                    bundle_directory=args.bundle_directory,
                    output_root=args.output_root,
                    max_artifact_bytes=args.max_artifact_bytes,
                )
            )
            return 0

        data_root = None
        if args.data_root is not None:
            from data_lake.root import DataLakeRoot

            data_root = DataLakeRoot.resolve(explicit=args.data_root)

        exit_code, message = run_basenotes_mgt_capture(
            url=args.url,
            bundle_directory=args.bundle_directory,
            output_root=args.output_root,
            data_root=data_root,
            decision_question=args.decision_question,
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
