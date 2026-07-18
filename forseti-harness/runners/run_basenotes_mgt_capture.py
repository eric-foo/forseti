from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import zlib
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Iterable, Literal, Mapping, Sequence
from urllib.parse import urlparse

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from harness_utils import utc_now_z
from source_capture import (
    CaptureModeCategory,
    PacketTiming,
    SourceCaptureSlice,
    known_fact,
    not_applicable,
    not_attempted,
    unknown_with_reason,
)
from source_capture.adapters.browser_snapshot import (
    BROWSER_BACKEND_CHROME_CDP,
    BrowserPageObservationSuccess,
    BrowserSnapshotFailure,
    ChromeCdpPageObservationSessionEngine,
    fetch_browser_page_observation_capture,
)
from source_capture.source_detail_sufficiency import (
    SourceDetailSufficiencyRequirements,
    evaluate_source_detail_sufficiency,
)
from source_capture.content_capture import (
    CAPTURE_ARTIFACT_MODES,
    CONTENT_PROJECTION_FAILED_EXIT_CODE,
    CONTENT_RECORD_FILENAME,
)
from source_capture.packet_assembly import stage_and_write_packet, staged_file_id_map
from source_capture.basenotes_projection import (
    BASENOTES_PARSER_VERSION,
    build_basenotes_content_record,
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
    "browser_snapshot_metadata.json",
)
SCREENSHOT_FILENAME = "browser_viewport_screenshot.png"
CONTENT_CAPTURE_METADATA_FILENAME = "content_capture_metadata.json"
SCREENSHOT_TRIGGERS = (
    "route_baseline",
    "visual_content",
    "access_or_overlay_diagnostic",
    "owner_requested",
)
ScreenshotTrigger = Literal[
    "route_baseline",
    "visual_content",
    "access_or_overlay_diagnostic",
    "owner_requested",
]

DEFAULT_DECISION_QUESTION = (
    "What public Basenotes product-page evidence was available for this fragrance at capture time?"
)
DEFAULT_OPERATOR_CATEGORY = "basenotes_user_assisted_persistent_chrome_capture_runner"
DEFAULT_MAX_ARTIFACT_BYTES = 10_000_000
DEFAULT_CDP_ENDPOINT = "http://127.0.0.1:9222"
DEFAULT_CDP_TIMEOUT_SECONDS = 45.0
DEFAULT_CDP_VIEWPORT_WIDTH = 1440
DEFAULT_CDP_VIEWPORT_HEIGHT = 900
_CDP_DOM_EXTRACT_SCRIPT = "() => document.documentElement.outerHTML"

ACCEPTED_RESIDUALS = [
    "capture requires a user-visible persistent Chrome session; direct mode observes accepted "
    "content and fails on challenge markers but does not automate or solve an access gate",
    "the runner ingests public rendered DOM, visible text, non-secret metadata, and only a "
    "trigger-requested screenshot; it does not inspect or export cookies, credentials, or "
    "browser-profile data",
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
    "not Cleaning, Judgment, buyer proof, or production readiness",
]

_CHALLENGE_TEXT_RE = re.compile(
    r"performing security verification|verif(?:y|ies) you are not a bot|just a moment",
    flags=re.IGNORECASE,
)
_BROWSER_SECRET_PATTERNS = (
    "cf_clearance",
    "Cookie:",
    "Set-Cookie",
    "storageState",
    "localStorage",
    "sessionStorage",
    "__cf_chl_",
)


@dataclass(frozen=True)
class PersistentChromeBundle:
    paths: tuple[Path, ...]
    rendered_dom: str
    visible_text: str
    metadata: Mapping[str, object]
    screenshot_path: Path | None


def run_basenotes_mgt_capture(
    *,
    url: str,
    bundle_directory: Path,
    output_root: Path,
    data_root: "DataLakeRoot | None" = None,
    decision_question: str = DEFAULT_DECISION_QUESTION,
    max_artifact_bytes: int = DEFAULT_MAX_ARTIFACT_BYTES,
    cdp_endpoint: str | None = None,
    cdp_engine: ChromeCdpPageObservationSessionEngine | None = None,
    capture_artifact_mode: Literal["content", "sample", "raw"] = "content",
    screenshot_trigger: ScreenshotTrigger | None = None,
) -> tuple[int, str]:
    """Validate a persistent-Chrome export and publish one Basenotes packet."""

    _validate_basenotes_url(url)
    _validate_positive("max_artifact_bytes", max_artifact_bytes)
    _validate_capture_mode(capture_artifact_mode)
    _validate_screenshot_trigger(screenshot_trigger)
    if cdp_endpoint is not None:
        _assert_output_root_available(output_root)
        capture_basenotes_bundle_via_cdp(
            url=url,
            bundle_directory=bundle_directory,
            cdp_endpoint=cdp_endpoint,
            max_artifact_bytes=max_artifact_bytes,
            engine=cdp_engine,
            screenshot_trigger=screenshot_trigger,
        )
    elif cdp_engine is not None:
        raise ValueError("cdp_engine requires direct CDP mode")
    bundle = _load_and_validate_bundle(
        bundle_directory=bundle_directory,
        url=url,
        max_artifact_bytes=max_artifact_bytes,
        screenshot_trigger=screenshot_trigger,
    )
    _assert_no_browser_secret_text(
        path
        for path in bundle.paths
        if path.name != SCREENSHOT_FILENAME
    )
    _prepare_output_root(output_root)

    input_paths = {
        "rendered_dom": bundle_directory / "browser_rendered_dom.html",
        "visible_text": bundle_directory / "browser_visible_text.txt",
        "browser_metadata": bundle_directory / "browser_snapshot_metadata.json",
    }
    if bundle.screenshot_path is not None:
        input_paths["screenshot"] = bundle.screenshot_path
    input_bytes = {role: path.read_bytes() for role, path in input_paths.items()}

    projection_failure: str | None = None
    content_record_bytes: bytes | None = None
    if capture_artifact_mode != "raw":
        try:
            content_record = build_basenotes_content_record(
                rendered_dom=input_bytes["rendered_dom"],
                visible_text=input_bytes["visible_text"],
                source_url=url,
            )
            content_record_bytes = _json_bytes(content_record)
            projection_status = "succeeded"
        except Exception as exc:
            projection_failure = f"{type(exc).__name__}: {exc}"
            projection_status = f"failed: {projection_failure}"
    else:
        projection_status = "not_attempted: raw mode"

    raw_projector_inputs_preserved = (
        capture_artifact_mode in {"raw", "sample"} or projection_failure is not None
    )
    preserved_by_role = {
        "rendered_dom": raw_projector_inputs_preserved,
        "visible_text": raw_projector_inputs_preserved,
        "browser_metadata": True,
        "screenshot": bundle.screenshot_path is not None,
    }
    content_capture_metadata = {
        "capture_artifact_mode": capture_artifact_mode,
        "parser_version": BASENOTES_PARSER_VERSION,
        "projection_status": projection_status,
        "screenshot_trigger": screenshot_trigger,
        "inputs": [
            {
                "role": role,
                "filename": path.name,
                "sha256": hashlib.sha256(input_bytes[role]).hexdigest(),
                "byte_count": len(input_bytes[role]),
                "preserved": preserved_by_role[role],
            }
            for role, path in input_paths.items()
        ],
    }
    staged_artifacts: list[tuple[str, bytes]] = []
    for role, path in input_paths.items():
        if preserved_by_role[role]:
            staged_artifacts.append((path.name, input_bytes[role]))
    if content_record_bytes is not None:
        staged_artifacts.append((CONTENT_RECORD_FILENAME, content_record_bytes))
    staged_artifacts.append(
        (CONTENT_CAPTURE_METADATA_FILENAME, _json_bytes(content_capture_metadata))
    )
    _assert_unique_artifact_names(staged_artifacts)
    file_ids = list(staged_file_id_map(staged_artifacts).values())

    timing = PacketTiming(
        source_publication_or_event=_unknown_source_publication(),
        source_edit_or_version=_unknown_source_edit(),
        capture_time=known_fact(str(bundle.metadata["capture_timestamp"])),
        recapture_time=_not_a_recapture(),
        cutoff_posture=_unknown_cutoff_posture(),
    )
    bundle_originated_from_cdp = (
        bundle.metadata.get("capture_transport") == "credential_free_loopback_cdp"
    )
    capture_performed_this_run = cdp_endpoint is not None
    if bundle_originated_from_cdp:
        access_posture = known_fact(
            "bundle metadata records that accepted public Basenotes product content was observed "
            "at the exact requested URL in a persistent Chrome session at capture time; challenge "
            "markers were absent and source-detail sufficiency passed; no current-run human access "
            "action is asserted"
        )
        warnings = [
            "accepted_access_observed_at_bundle_capture: exact final URL, challenge-free rendered "
            "content, and source-detail sufficiency passed"
        ]
        capture_context = (
            "bundle originating from an existing Chrome CDP public-page observation; rendered DOM, "
            "visible text, optional trigger-bound screenshot, and non-secret metadata only"
        )
        visible_mode_changes = ["persistent_user_session", "accepted_access_observed"]
        receipt_summary = (
            "Observed-access persistent Chrome packet for one public Basenotes product page "
            "with mechanically sufficient product and review evidence."
        )
    else:
        access_posture = known_fact(
            "public Basenotes product content captured only after the user completed Cloudflare "
            "verification in a persistent Chrome tab; session state was used but cookies and "
            "credentials were not inspected or exported"
        )
        warnings = [
            "user_assisted_access_gate: user completed Cloudflare verification before public "
            "page artifacts were exported"
        ]
        capture_context = (
            "user-cleared persistent Chrome public-page export; rendered DOM, visible text, "
            "optional trigger-bound screenshot, and non-secret metadata only"
        )
        visible_mode_changes = ["human_cleared_access_gate", "persistent_user_session"]
        receipt_summary = (
            "User-cleared persistent Chrome packet for one public Basenotes product page with "
            "mechanically sufficient product and review evidence."
        )
    archive_posture = not_attempted(
        "the persistent Chrome bundle did not query archive or history services"
    )
    media_posture = known_fact(
        (
            f"one viewport screenshot was preserved for trigger {screenshot_trigger!r}; "
            "linked media files were not independently preserved"
        )
        if bundle.screenshot_path is not None
        else (
            "no screenshot was requested for this capture; linked media files were not "
            "independently preserved"
        )
    )
    recapture_posture = _not_a_recapture_relationship()
    mode_changes = [
        (
            f"viewport screenshot preserved for trigger {screenshot_trigger}"
            if bundle.screenshot_path is not None
            else "no screenshot requested or preserved"
        ),
        "browser snapshot metadata preserved without browser-secret export",
    ]
    if raw_projector_inputs_preserved:
        mode_changes.extend(["rendered DOM preserved", "visible text preserved"])
    else:
        mode_changes.append(
            "rendered DOM and visible text hashed then discarded after successful capture-time projection"
        )
    if content_record_bytes is not None:
        mode_changes.append("capture-time Basenotes content record preserved")

    packet_limitations = list(ACCEPTED_RESIDUALS)
    if projection_failure is not None:
        packet_limitations.append(
            "content-mode projection failed in flight; all supplied source artifacts "
            f"were preserved as fallback: {projection_failure}"
        )
    elif capture_artifact_mode == "content":
        packet_limitations.append(
            "content-mode packet: rendered DOM and visible text discarded after hashing; "
            "browser metadata and any trigger-bound screenshot retained"
        )
    elif capture_artifact_mode == "sample":
        packet_limitations.append(
            "sample packet: rendered DOM, visible text, and derived content record preserved "
            "for parser-fit drift checks"
        )

    result = stage_and_write_packet(
        output_directory=None if data_root is not None else output_root / PERSISTENT_CHROME_SLOT,
        data_root=data_root,
        staged_artifacts=staged_artifacts,
        source_family=SOURCE_FAMILY,
        source_surface=PERSISTENT_CHROME_SURFACE,
        source_locator=known_fact(url),
        decision_question=decision_question,
        capture_context=capture_context,
        actor_audience_context=known_fact(
            "public Basenotes fragrance product page and its source-visible review audience"
        ),
        capture_mode=CaptureModeCategory.MULTIMODAL,
        operator_category=DEFAULT_OPERATOR_CATEGORY,
        session_identity=None,
        visible_mode_changes=visible_mode_changes + mode_changes,
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
                limitations=packet_limitations,
                warning_notes=warnings,
                preserved_file_ids=file_ids,
            )
        ],
        warnings=warnings,
        limitations=packet_limitations,
        receipt_summary=f"{receipt_summary} Artifact mode: {capture_artifact_mode}.",
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
            "human_cleared_access_gate": bundle.metadata.get("human_cleared_access_gate"),
            "access_readiness_basis": bundle.metadata.get("access_readiness_basis"),
            "cookies_or_credentials_exported": False,
            "proxy_used": False,
            "capture_transport": (
                "existing_chrome_cdp_loopback"
                if capture_performed_this_run
                else "none_existing_bundle"
            ),
            "bundle_origin_transport": (
                "credential_free_loopback_cdp"
                if bundle_originated_from_cdp
                else "manual_bundle"
            ),
            "capture_performed_this_run": capture_performed_this_run,
            "capture_artifact_mode": capture_artifact_mode,
            "screenshot_trigger": screenshot_trigger,
        },
        projection_status=projection_status,
    )
    summary_path = output_root / SUMMARY_FILENAME
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return (
        CONTENT_PROJECTION_FAILED_EXIT_CODE if projection_failure is not None else 0,
        str(summary_path),
    )


def build_basenotes_mgt_capture_summary(
    *,
    url: str,
    output_root: Path,
    data_root_path: Path | None,
    packet_directories: Mapping[str, Path],
    capture_parameters: Mapping[str, object],
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
        "capture_profile": CAPTURE_PROFILE,
        "source_family": SOURCE_FAMILY,
        "source_url": url,
        "basenotes_product_slug": extract_basenotes_product_slug(url),
        "summary_generated_at": utc_now_z(),
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
        "projection_status": projection_status,
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
    cdp_endpoint: str | None = None,
    cdp_engine: ChromeCdpPageObservationSessionEngine | None = None,
    screenshot_trigger: ScreenshotTrigger | None = None,
) -> str:
    _validate_basenotes_url(url)
    _validate_positive("max_artifact_bytes", max_artifact_bytes)
    _validate_screenshot_trigger(screenshot_trigger)
    _assert_output_root_available(output_root)
    if cdp_endpoint is not None:
        capture_basenotes_bundle_via_cdp(
            url=url,
            bundle_directory=bundle_directory,
            cdp_endpoint=cdp_endpoint,
            max_artifact_bytes=max_artifact_bytes,
            engine=cdp_engine,
            screenshot_trigger=screenshot_trigger,
        )
    elif cdp_engine is not None:
        raise ValueError("cdp_engine requires direct CDP mode")
    _load_and_validate_bundle(
        bundle_directory=bundle_directory,
        url=url,
        max_artifact_bytes=max_artifact_bytes,
        screenshot_trigger=screenshot_trigger,
    )
    slug = extract_basenotes_product_slug(url) or "unknown"
    capture_clause = (
        "direct loopback CDP capture observed accepted challenge-free source content and wrote "
        "a reusable validated bundle; publish that bundle later without --cdp-endpoint"
        if cdp_endpoint is not None
        else "no network capture attempted"
    )
    prerequisite_clause = (
        "requires user-visible persistent Chrome"
        if cdp_endpoint is not None
        else "requires user-visible persistent Chrome plus a user-cleared access gate"
    )
    return (
        f"basenotes persistent Chrome bundle preflight passed; {capture_clause}; "
        f"{prerequisite_clause}; public-page "
        "bundle validated with no cookie, credential, browser-profile, or proxy export; "
        f"product_slug={slug}; bundle_directory={bundle_directory}; output_root={output_root}"
    )


def capture_basenotes_bundle_via_cdp(
    *,
    url: str,
    bundle_directory: Path,
    cdp_endpoint: str,
    max_artifact_bytes: int = DEFAULT_MAX_ARTIFACT_BYTES,
    timeout_seconds: float = DEFAULT_CDP_TIMEOUT_SECONDS,
    engine: ChromeCdpPageObservationSessionEngine | None = None,
    screenshot_trigger: ScreenshotTrigger | None = None,
) -> Path:
    """Create the manual-mode bundle after observing accepted content in a CDP session."""

    _validate_basenotes_url(url)
    _validate_positive("max_artifact_bytes", max_artifact_bytes)
    _validate_positive("timeout_seconds", timeout_seconds)
    _validate_cdp_endpoint(cdp_endpoint)
    _validate_screenshot_trigger(screenshot_trigger)
    _assert_bundle_output_available(bundle_directory)

    capture_engine = engine or ChromeCdpPageObservationSessionEngine(cdp_endpoint=cdp_endpoint)
    try:
        observation = fetch_browser_page_observation_capture(
            url=url,
            dom_extract_script=_CDP_DOM_EXTRACT_SCRIPT,
            dom_extract_arg=None,
            response_url_predicate=lambda _url: False,
            timeout_seconds=timeout_seconds,
            wait_until="load",
            viewport_width=DEFAULT_CDP_VIEWPORT_WIDTH,
            viewport_height=DEFAULT_CDP_VIEWPORT_HEIGHT,
            max_response_bytes=max_artifact_bytes,
            settle_seconds=2.0,
            proxy_profile=None,
            storage_state_path=None,
            headless=False,
            browser_channel=None,
            browser_backend=BROWSER_BACKEND_CHROME_CDP,
            engine=capture_engine,
        )
        if isinstance(observation, BrowserSnapshotFailure):
            raise ValueError(f"direct CDP page observation failed: {observation.message}")
        if not isinstance(observation, BrowserPageObservationSuccess):
            raise ValueError("direct CDP page observation returned an unsupported result")
        if not isinstance(observation.dom_observation, str) or not observation.dom_observation:
            raise ValueError("direct CDP page observation returned no rendered DOM")

        metadata: dict[str, object] = {
            "capture_timestamp": observation.metadata.get("capture_timestamp") or utc_now_z(),
            "requested_url": url,
            "final_url": observation.final_url,
            "title": observation.title,
            "browser_channel": "existing_chrome_cdp",
            "headless": False,
            "persistent_user_session": True,
            "human_cleared_access_gate": False,
            "access_readiness_basis": "observed_exact_url_challenge_free_sufficient_content",
            "cookies_exported": False,
            "credentials_exported": False,
            "proxy_used": False,
            "capture_transport": "credential_free_loopback_cdp",
        }
        _validate_captured_page_content(
            rendered_dom=observation.dom_observation,
            visible_text=observation.visible_text,
            title=observation.title,
            url=url,
        )
        _validate_bundle_metadata(metadata=metadata, url=url)
        _validate_artifact_size(
            name="browser_rendered_dom.html",
            body=observation.dom_observation.encode("utf-8"),
            max_artifact_bytes=max_artifact_bytes,
        )
        _validate_artifact_size(
            name="browser_visible_text.txt",
            body=observation.visible_text.encode("utf-8"),
            max_artifact_bytes=max_artifact_bytes,
        )
        screenshot_png = (
            capture_engine.capture_current_viewport_png(timeout_seconds=timeout_seconds)
            if screenshot_trigger is not None
            else None
        )
    finally:
        capture_engine.close()

    if screenshot_png is not None:
        _validate_png_bytes(screenshot_png)
        _validate_artifact_size(
            name=SCREENSHOT_FILENAME,
            body=screenshot_png,
            max_artifact_bytes=max_artifact_bytes,
        )
    metadata_bytes = (json.dumps(metadata, indent=2, sort_keys=True) + "\n").encode("utf-8")
    _validate_artifact_size(
        name="browser_snapshot_metadata.json",
        body=metadata_bytes,
        max_artifact_bytes=max_artifact_bytes,
    )

    bundle_directory.mkdir(parents=True, exist_ok=True)
    (bundle_directory / "browser_rendered_dom.html").write_text(
        observation.dom_observation, encoding="utf-8"
    )
    (bundle_directory / "browser_visible_text.txt").write_text(
        observation.visible_text, encoding="utf-8"
    )
    if screenshot_png is not None:
        (bundle_directory / SCREENSHOT_FILENAME).write_bytes(screenshot_png)
    (bundle_directory / "browser_snapshot_metadata.json").write_bytes(metadata_bytes)
    return bundle_directory


def _load_and_validate_bundle(
    *,
    bundle_directory: Path,
    url: str,
    max_artifact_bytes: int,
    screenshot_trigger: ScreenshotTrigger | None,
) -> PersistentChromeBundle:
    if not bundle_directory.is_dir():
        raise ValueError(f"persistent Chrome bundle directory does not exist: {bundle_directory}")
    actual_names = {path.name for path in bundle_directory.iterdir()}
    required_names = set(REQUIRED_BUNDLE_FILENAMES)
    allowed_names = required_names | {SCREENSHOT_FILENAME}
    if not required_names.issubset(actual_names) or not actual_names.issubset(allowed_names):
        missing = sorted(required_names - actual_names)
        unexpected = sorted(actual_names - allowed_names)
        raise ValueError(
            "persistent Chrome bundle must contain DOM, visible text, metadata, and only an "
            "optional screenshot; "
            f"missing={missing}; unexpected={unexpected}"
        )
    screenshot_path = (
        bundle_directory / SCREENSHOT_FILENAME
        if SCREENSHOT_FILENAME in actual_names
        else None
    )
    if screenshot_path is not None and screenshot_trigger is None:
        raise ValueError("a supplied screenshot requires screenshot_trigger")
    if screenshot_path is None and screenshot_trigger is not None:
        raise ValueError("screenshot_trigger requires a supplied screenshot")
    paths = tuple(
        bundle_directory / name
        for name in (*REQUIRED_BUNDLE_FILENAMES, *([SCREENSHOT_FILENAME] if screenshot_path else []))
    )
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

    rendered_dom = (bundle_directory / "browser_rendered_dom.html").read_text(encoding="utf-8")
    visible_text = (bundle_directory / "browser_visible_text.txt").read_text(encoding="utf-8")
    if screenshot_path is not None:
        _validate_png_bytes(screenshot_path.read_bytes())
    try:
        metadata = json.loads(
            (bundle_directory / "browser_snapshot_metadata.json").read_text(encoding="utf-8")
        )
    except json.JSONDecodeError as exc:
        raise ValueError(f"persistent Chrome metadata is not valid JSON: {exc}") from exc
    if not isinstance(metadata, dict):
        raise ValueError("persistent Chrome metadata must be a JSON object")
    _validate_bundle_metadata(metadata=metadata, url=url)

    _validate_captured_page_content(
        rendered_dom=rendered_dom,
        visible_text=visible_text,
        title=str(metadata.get("title") or ""),
        url=url,
    )
    return PersistentChromeBundle(
        paths=paths,
        rendered_dom=rendered_dom,
        visible_text=visible_text,
        metadata=metadata,
        screenshot_path=screenshot_path,
    )


def _validate_captured_page_content(
    *, rendered_dom: str, visible_text: str, title: str | None, url: str
) -> None:
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


def _validate_png_bytes(body: bytes) -> None:
    if len(body) < 45 or body[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("persistent Chrome screenshot is not a genuine PNG")
    offset = 8
    seen_ihdr = False
    seen_idat = False
    seen_iend = False
    while offset + 12 <= len(body):
        chunk_length = int.from_bytes(body[offset : offset + 4], "big")
        chunk_type = body[offset + 4 : offset + 8]
        chunk_end = offset + 12 + chunk_length
        if chunk_end > len(body):
            raise ValueError("persistent Chrome screenshot is not a genuine PNG")
        chunk_data = body[offset + 8 : offset + 8 + chunk_length]
        observed_crc = int.from_bytes(body[offset + 8 + chunk_length : chunk_end], "big")
        expected_crc = zlib.crc32(chunk_type + chunk_data) & 0xFFFFFFFF
        if observed_crc != expected_crc:
            raise ValueError("persistent Chrome screenshot is not a genuine PNG")
        if not seen_ihdr:
            if chunk_type != b"IHDR" or chunk_length != 13:
                raise ValueError("persistent Chrome screenshot is not a genuine PNG")
            width = int.from_bytes(chunk_data[:4], "big")
            height = int.from_bytes(chunk_data[4:8], "big")
            if width <= 0 or height <= 0:
                raise ValueError("persistent Chrome screenshot is not a genuine PNG")
            seen_ihdr = True
        if chunk_type == b"IDAT" and chunk_length > 0:
            seen_idat = True
        if chunk_type == b"IEND":
            if chunk_length != 0 or chunk_end != len(body):
                raise ValueError("persistent Chrome screenshot is not a genuine PNG")
            seen_iend = True
            break
        offset = chunk_end
    if not seen_ihdr or not seen_idat or not seen_iend:
        raise ValueError("persistent Chrome screenshot is not a genuine PNG")


def _validate_artifact_size(*, name: str, body: bytes, max_artifact_bytes: int) -> None:
    if not body:
        raise ValueError(f"persistent Chrome bundle artifact is empty: {name}")
    if len(body) > max_artifact_bytes:
        raise ValueError(
            f"persistent Chrome bundle artifact exceeds max_artifact_bytes: {name} ({len(body)})"
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
    capture_transport = metadata.get("capture_transport")
    if capture_transport not in {None, "manual_bundle", "credential_free_loopback_cdp"}:
        raise ValueError(
            "persistent Chrome metadata capture_transport must be manual_bundle or "
            "credential_free_loopback_cdp"
        )
    required_values = {
        "requested_url": url,
        "final_url": url,
        "headless": False,
        "persistent_user_session": True,
        "cookies_exported": False,
        "credentials_exported": False,
        "proxy_used": False,
    }
    if capture_transport == "credential_free_loopback_cdp":
        required_values.update(
            {
                "human_cleared_access_gate": False,
                "access_readiness_basis": (
                    "observed_exact_url_challenge_free_sufficient_content"
                ),
            }
        )
    else:
        required_values["human_cleared_access_gate"] = True
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


def _validate_capture_mode(capture_artifact_mode: str) -> None:
    if capture_artifact_mode not in CAPTURE_ARTIFACT_MODES:
        raise ValueError(
            f"capture_artifact_mode must be one of {CAPTURE_ARTIFACT_MODES}, "
            f"got {capture_artifact_mode!r}"
        )


def _validate_screenshot_trigger(screenshot_trigger: str | None) -> None:
    if screenshot_trigger is not None and screenshot_trigger not in SCREENSHOT_TRIGGERS:
        raise ValueError(
            f"screenshot_trigger must be one of {SCREENSHOT_TRIGGERS}, "
            f"got {screenshot_trigger!r}"
        )


def _assert_no_browser_secret_text(paths: Iterable[Path]) -> None:
    for path in paths:
        sample = path.read_bytes().decode("utf-8", errors="ignore")
        for pattern in _BROWSER_SECRET_PATTERNS:
            if pattern in sample:
                raise ValueError(
                    f"browser-secret material is forbidden in supplied artifact "
                    f"{path.name}: {pattern}"
                )


def _json_bytes(value: Mapping[str, object]) -> bytes:
    return (json.dumps(dict(value), indent=2, sort_keys=True) + "\n").encode("utf-8")


def _assert_unique_artifact_names(staged_artifacts: Sequence[tuple[str, bytes]]) -> None:
    names = [name for name, _body in staged_artifacts]
    if len(names) != len(set(names)):
        raise ValueError("staged Basenotes artifact names must be unique")


def _is_basenotes_hostname(hostname: str) -> bool:
    return hostname == "basenotes.com" or hostname.endswith(".basenotes.com")


def _validate_cdp_endpoint(cdp_endpoint: str) -> None:
    parsed = urlparse(cdp_endpoint)
    if (
        parsed.scheme not in {"http", "https"}
        or parsed.username is not None
        or parsed.password is not None
        or parsed.hostname not in {"localhost", "127.0.0.1", "::1"}
        or parsed.path not in {"", "/"}
        or parsed.query
        or parsed.fragment
    ):
        raise ValueError("cdp_endpoint must be a credential-free loopback http(s) endpoint")
    try:
        parsed.port
    except ValueError as exc:
        raise ValueError("cdp_endpoint has an invalid port") from exc


def _assert_bundle_output_available(bundle_directory: Path) -> None:
    if bundle_directory.exists() and not bundle_directory.is_dir():
        raise ValueError(f"CDP bundle output exists and is not a directory: {bundle_directory}")
    if bundle_directory.exists() and any(bundle_directory.iterdir()):
        raise ValueError(f"CDP bundle output must be absent or empty: {bundle_directory}")


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


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Validate and publish a public-page export from a user-cleared persistent Chrome "
            "Basenotes product tab. Optional direct mode attaches to an existing local Chrome "
            "CDP session; neither mode automates the access gate."
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
        "--capture-mode",
        choices=CAPTURE_ARTIFACT_MODES,
        default="content",
        help=(
            "Artifact mode. Content is the pinned-route default; sample retains "
            "projector inputs for parser-fit checks and raw preserves legacy inputs."
        ),
    )
    parser.add_argument(
        "--screenshot-trigger",
        choices=SCREENSHOT_TRIGGERS,
        default=None,
        help=(
            "Capture/preserve a screenshot only for a named visual-evidence trigger. "
            "Omit for ordinary repeat semantic capture."
        ),
    )
    parser.add_argument(
        "--cdp-endpoint",
        default=None,
        help=(
            "Enable direct mode against a credential-free loopback endpoint such as "
            f"{DEFAULT_CDP_ENDPOINT}; --bundle-directory becomes the fresh generated bundle."
        ),
    )
    parser.add_argument(
        "--preflight-only",
        action="store_true",
        help=(
            "Validate URL, public-page bundle, route metadata, sufficiency, and "
            "output-root availability, then exit without publishing a packet. With "
            "--cdp-endpoint this performs live capture and writes the reusable fresh bundle; "
            "publish it in a later run without --cdp-endpoint."
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
                    cdp_endpoint=args.cdp_endpoint,
                    screenshot_trigger=args.screenshot_trigger,
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
            cdp_endpoint=args.cdp_endpoint,
            capture_artifact_mode=args.capture_mode,
            screenshot_trigger=args.screenshot_trigger,
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
