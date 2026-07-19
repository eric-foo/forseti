"""Run the admitted Kohl's real-Chrome route without a human-operated browser.

This is a scheduled one-shot entrypoint, not a daemon. It ensures the local
browser image exists, starts one private headful Chrome under Xvfb, captures the
bound PDP and policy through the existing rung-7 packet seam, then stops and
removes the container. A named Docker volume keeps the Chrome profile between
runs; packet artifacts never include cookies or browser storage.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence
from urllib.error import URLError
from urllib.request import urlopen

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from harness_utils import generate_ulid
from runners.run_source_capture_realchrome_cdp_packet import (
    run_source_capture_realchrome_cdp_packet,
)
from source_capture.source_detail_sufficiency import (
    SourceDetailSufficiencyRequirements,
)

DEFAULT_IMAGE = "forseti-realchrome-xvfb:local"
DEFAULT_PROFILE_VOLUME = "forseti-kohls-realchrome-profile"
DEFAULT_START_TIMEOUT_SECONDS = 45.0
DEFAULT_DOCKER_TIMEOUT_SECONDS = 60.0
DOCKER_BUILD_TIMEOUT_SECONDS = 600.0
CDP_CONTAINER_PORT = "9222/tcp"
PDP_URL = (
    "https://www.kohls.com/product/prd-6715879/"
    "tower-28-beauty-lipsoftie-hydrating-tinted-lip-treatment-balm.jsp"
)
POLICY_URL = "https://www.kohls.com/faq/article/2552"
WARM_HOP_URL = "https://www.kohls.com/"


class UnattendedCaptureError(RuntimeError):
    pass


@dataclass(frozen=True)
class CaptureOutcome:
    surface: str
    exit_code: int
    packet_path: str


def _emit(**event: object) -> None:
    print(json.dumps(event, ensure_ascii=False, sort_keys=True), flush=True)


def _docker(
    args: Sequence[str],
    *,
    check: bool = True,
    capture_output: bool = True,
    timeout_seconds: float = DEFAULT_DOCKER_TIMEOUT_SECONDS,
) -> subprocess.CompletedProcess[str]:
    try:
        result = subprocess.run(
            ["docker", *args],
            check=False,
            capture_output=capture_output,
            text=True,
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired as exc:
        raise UnattendedCaptureError(
            f"docker {' '.join(args[:2])} exceeded {timeout_seconds:g}s"
        ) from exc
    if check and result.returncode != 0:
        detail = ((result.stderr or result.stdout) or "").strip()
        raise UnattendedCaptureError(
            f"docker {' '.join(args[:2])} failed with exit {result.returncode}: {detail[:2000]}"
        )
    return result


def _ensure_image(*, image: str, context: Path, rebuild: bool) -> bool:
    if not rebuild:
        inspected = _docker(["image", "inspect", image], check=False)
        if inspected.returncode == 0:
            _emit(phase="image", status="reused", image=image)
            return False
    _emit(phase="image", status="build_started", image=image, context=str(context))
    _docker(
        ["build", "--pull", "--tag", image, str(context)],
        capture_output=False,
        timeout_seconds=DOCKER_BUILD_TIMEOUT_SECONDS,
    )
    _emit(phase="image", status="build_completed", image=image)
    return True


def _start_browser(
    *,
    image: str,
    profile_volume: str,
    chrome_no_sandbox: bool,
) -> str:
    container_name = f"forseti-kohls-xvfb-{generate_ulid().lower()}"
    args = [
        "run",
        "--detach",
        "--rm",
        "--name",
        container_name,
        "--shm-size=1g",
        "--security-opt",
        "no-new-privileges=true",
        "--publish",
        f"127.0.0.1::{CDP_CONTAINER_PORT.split('/')[0]}",
        "--volume",
        f"{profile_volume}:/data/chrome-profile",
    ]
    if chrome_no_sandbox:
        args.extend(["--env", "CHROME_NO_SANDBOX=1"])
    args.append(image)
    _docker(args)
    _emit(
        phase="browser",
        status="started",
        container=container_name,
        chrome_no_sandbox=chrome_no_sandbox,
        cdp_exposure="host_loopback_only",
    )
    return container_name


def _parse_docker_port(value: str) -> int:
    lines = [line.strip() for line in value.splitlines() if line.strip()]
    for line in lines:
        host, separator, port_text = line.rpartition(":")
        if separator and host == "127.0.0.1" and port_text.isdigit():
            port = int(port_text)
            if 0 < port <= 65535:
                return port
    raise UnattendedCaptureError(
        f"docker did not report a private IPv4 host port for {CDP_CONTAINER_PORT}: {value!r}"
    )


def _wait_for_cdp(*, container_name: str, timeout_seconds: float) -> str:
    deadline = time.monotonic() + timeout_seconds
    last_error = "port not assigned"
    while time.monotonic() < deadline:
        port_result = _docker(
            ["port", container_name, CDP_CONTAINER_PORT],
            check=False,
        )
        if port_result.returncode == 0:
            try:
                port = _parse_docker_port(port_result.stdout)
                endpoint = f"http://127.0.0.1:{port}"
                with urlopen(f"{endpoint}/json/version", timeout=2) as response:
                    browser = json.loads(response.read().decode("utf-8"))
                if browser.get("webSocketDebuggerUrl"):
                    _emit(
                        phase="browser",
                        status="ready",
                        browser=browser.get("Browser"),
                        endpoint=endpoint,
                    )
                    return endpoint
            except (OSError, URLError, ValueError, json.JSONDecodeError) as exc:
                last_error = f"{type(exc).__name__}: {exc}"
        else:
            last_error = ((port_result.stderr or port_result.stdout) or "").strip()
        time.sleep(0.5)

    logs = _docker(["logs", "--tail", "80", container_name], check=False)
    log_text = ((logs.stdout or "") + (logs.stderr or "")).strip()
    raise UnattendedCaptureError(
        f"Chrome CDP did not become ready within {timeout_seconds:g}s "
        f"({last_error}); container log tail: {log_text[-4000:]}"
    )


def _stop_browser(container_name: str) -> None:
    result = _docker(["stop", "--time", "10", container_name], check=False)
    if result.returncode != 0:
        detail = ((result.stderr or result.stdout) or "").strip()
        raise UnattendedCaptureError(
            f"could not stop probe container {container_name}: {detail[:2000]}"
        )
    _emit(phase="browser", status="stopped", container=container_name)


def capture_kohls_surfaces(
    *,
    data_root: object,
    cdp_endpoint: str,
    chrome_no_sandbox: bool,
) -> list[CaptureOutcome]:
    limitations = [
        "unattended_xvfb: Chrome ran headful under a virtual X display; the CDP relay was "
        "published to host loopback only; a Docker volume supplied the reusable browser profile."
    ]
    if chrome_no_sandbox:
        limitations.append(
            "chrome_inner_sandbox_disabled: required by Docker Desktop on this probe host; "
            "the browser remained inside an unprivileged Docker container."
        )

    shared = {
        "cdp_endpoint": cdp_endpoint,
        "warm_hop_url": WARM_HOP_URL,
        "browser_provisioning": "unattended_xvfb",
        "persistent_profile_loaded": True,
        "capture_context": (
            "Unattended logged-out public capture using headful real Chrome under Xvfb; "
            "private host-loopback CDP; no proxy, credential, login, or cookie injection."
        ),
        "limitations": limitations,
        "visible_mode_changes": ["unattended_xvfb_one_shot"],
    }
    jobs = (
        {
            "surface": "pdp",
            "url": PDP_URL,
            "source_family": "retail_pdp",
            "decision_question": (
                "Does Kohl's expose the bound Tower 28 LipSoftie PDP with a product-bound USD offer?"
            ),
            "requirements": SourceDetailSufficiencyRequirements(
                require_not_access_blocked=True,
                visible_text_contains=("LipSoftie",),
                rendered_dom_regexes=(r'priceCurrency"\s+content="USD"',),
            ),
        },
        {
            "surface": "policy",
            "url": POLICY_URL,
            "source_family": "retail_policy",
            "decision_question": (
                "Does Kohl's own policy page state that it ships only to U.S. and APO/FPO addresses?"
            ),
            "requirements": SourceDetailSufficiencyRequirements(
                require_not_access_blocked=True,
                visible_text_contains=(
                    "currently only ships to U.S. addresses and APO/FPO addresses",
                ),
            ),
        },
    )

    outcomes: list[CaptureOutcome] = []
    failures: list[str] = []
    for job in jobs:
        try:
            code, packet_path = run_source_capture_realchrome_cdp_packet(
                url=job["url"],
                source_family=job["source_family"],
                source_surface="realchrome_cdp_snapshot",
                decision_question=job["decision_question"],
                data_root=data_root,
                source_detail_sufficiency_requirements=job["requirements"],
                **shared,
            )
            outcome = CaptureOutcome(
                surface=str(job["surface"]),
                exit_code=code,
                packet_path=packet_path,
            )
            outcomes.append(outcome)
            _emit(
                phase="capture",
                status="passed" if code == 0 else "failed",
                surface=outcome.surface,
                exit_code=code,
                packet_path=packet_path,
            )
            if code != 0:
                failures.append(f"{outcome.surface}: exit {code}")
        except Exception as exc:  # preserve the other surface's evidence
            failure = f"{job['surface']}: {type(exc).__name__}: {exc}"
            failures.append(failure)
            _emit(phase="capture", status="error", surface=job["surface"], error=failure[:2000])

    if failures:
        raise UnattendedCaptureError("; ".join(failures))
    return outcomes


def run_unattended_job(
    *,
    data_root: object,
    image: str = DEFAULT_IMAGE,
    profile_volume: str = DEFAULT_PROFILE_VOLUME,
    rebuild_image: bool = False,
    chrome_no_sandbox: bool = False,
    start_timeout_seconds: float = DEFAULT_START_TIMEOUT_SECONDS,
) -> list[CaptureOutcome]:
    context = Path(__file__).resolve().parents[1] / "containers" / "realchrome_xvfb"
    _ensure_image(image=image, context=context, rebuild=rebuild_image)
    container_name = _start_browser(
        image=image,
        profile_volume=profile_volume,
        chrome_no_sandbox=chrome_no_sandbox,
    )

    failure: Exception | None = None
    outcomes: list[CaptureOutcome] = []
    try:
        endpoint = _wait_for_cdp(
            container_name=container_name,
            timeout_seconds=start_timeout_seconds,
        )
        outcomes = capture_kohls_surfaces(
            data_root=data_root,
            cdp_endpoint=endpoint,
            chrome_no_sandbox=chrome_no_sandbox,
        )
    except Exception as exc:  # cleanup must still run
        failure = exc

    cleanup_failure: Exception | None = None
    try:
        _stop_browser(container_name)
    except Exception as exc:
        cleanup_failure = exc

    if failure is not None:
        if cleanup_failure is not None:
            raise UnattendedCaptureError(
                f"{failure}; browser cleanup also failed: {cleanup_failure}"
            ) from failure
        raise failure
    if cleanup_failure is not None:
        raise cleanup_failure
    return outcomes


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Run the bound Kohl's PDP and policy capture unattended through headful Chrome under Xvfb."
        )
    )
    parser.add_argument(
        "--data-root",
        default=None,
        help="Forseti data lake root; defaults to FORSETI_DATA_ROOT (legacy ORCA_DATA_ROOT).",
    )
    parser.add_argument("--image", default=DEFAULT_IMAGE)
    parser.add_argument("--profile-volume", default=DEFAULT_PROFILE_VOLUME)
    parser.add_argument("--rebuild-image", action="store_true")
    parser.add_argument(
        "--chrome-no-sandbox",
        action=argparse.BooleanOptionalAction,
        default=platform.system() == "Windows",
        help=(
            "Disable Chrome's inner sandbox inside Docker. Defaults on for Windows Docker Desktop "
            "and off elsewhere; the Docker container remains the outer isolation boundary."
        ),
    )
    parser.add_argument(
        "--start-timeout-seconds",
        type=float,
        default=DEFAULT_START_TIMEOUT_SECONDS,
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    if args.start_timeout_seconds <= 0:
        parser.error("--start-timeout-seconds must be greater than zero")
    if not str(args.profile_volume).strip():
        parser.error("--profile-volume must not be empty")

    from data_lake.root import DataLakeRoot

    try:
        data_root = DataLakeRoot.resolve(explicit=args.data_root)
        outcomes = run_unattended_job(
            data_root=data_root,
            image=args.image,
            profile_volume=args.profile_volume,
            rebuild_image=args.rebuild_image,
            chrome_no_sandbox=args.chrome_no_sandbox,
            start_timeout_seconds=args.start_timeout_seconds,
        )
    except Exception as exc:
        _emit(phase="job", status="failed", error=f"{type(exc).__name__}: {exc}"[:4000])
        return 3

    _emit(
        phase="job",
        status="passed",
        packet_count=len(outcomes),
        packet_paths=[outcome.packet_path for outcome in outcomes],
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
