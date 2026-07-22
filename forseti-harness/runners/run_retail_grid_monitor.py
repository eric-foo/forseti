from __future__ import annotations

import argparse
import io
import re
import sys
from contextlib import redirect_stderr, redirect_stdout
from datetime import date
from pathlib import Path
from typing import Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from data_lake.root import DataLakeRoot
from runners.run_source_capture_cloakbrowser_packet import main as cloakbrowser_main
from source_capture.retail_grid_monitoring import (
    MonitorRoute,
    RetailGridCaptureAttempt,
    load_monitor_manifest,
    run_monitor_round,
)


DEFAULT_MANIFEST = (
    Path(__file__).resolve().parents[1] / "config" / "retail_grid_monitored_brands.json"
)
REPO_ROOT = Path(__file__).resolve().parents[2]

_PROJECTION_RE = re.compile(r"derived observation preserved at (?P<path>.+)$")
_RAW_SAMPLE_RE = re.compile(
    r"raw sample preserved at (?P<path>.+?); derived observation preserved at "
)
_FAILED_PACKET_RE = re.compile(r"packet preserved at (?P<path>.+?)(?:;|$)")


def _capture_argv(
    *, route: MonitorRoute, data_root: DataLakeRoot, retain_raw_sample: bool
) -> list[str]:
    argv = [
        "--url",
        route.url,
        "--source-family",
        "retail_pdp",
        "--source-surface",
        "cloakbrowser_snapshot",
        "--decision-question",
        (
            "What products and placements are source-visible for "
            f"{route.brand_name} at {route.retailer}?"
        ),
        "--data-root",
        str(data_root.path),
        "--retail-capture-profile",
        route.profile,
        "--series-id",
        route.series_id,
        "--block-heavy-assets",
    ]
    if route.retailer == "sephora":
        argv.extend(("--sephora-market", "US", "--timeout-seconds", "90"))
    elif route.retailer == "ulta":
        argv.extend(("--ulta-market", "US"))
    elif route.retailer == "target":
        argv.extend(("--timeout-seconds", "240"))
    elif route.retailer == "amazon":
        assert route.page_count is not None
        argv.extend(
            (
                "--delivery-zip",
                "10001",
                "--amazon-grid-page-count",
                str(route.page_count),
            )
        )
    if retain_raw_sample:
        argv.append("--retain-retail-grid-raw-sample")
    return argv


def capture_route(
    route: MonitorRoute,
    retain_raw_sample: bool,
    *,
    data_root: DataLakeRoot,
) -> RetailGridCaptureAttempt:
    stdout = io.StringIO()
    stderr = io.StringIO()
    try:
        with redirect_stdout(stdout), redirect_stderr(stderr):
            exit_code = cloakbrowser_main(
                _capture_argv(
                    route=route,
                    data_root=data_root,
                    retain_raw_sample=retain_raw_sample,
                )
            )
    except SystemExit as exc:
        exit_code = int(exc.code) if isinstance(exc.code, int) else 3

    output = stdout.getvalue().strip()
    error = stderr.getvalue().strip()
    message = output if exit_code == 0 else error or output
    projection_match = _PROJECTION_RE.search(message)
    raw_match = _RAW_SAMPLE_RE.search(message)
    if raw_match is None and exit_code != 0:
        raw_match = _FAILED_PACKET_RE.search(message)
    projection_path = Path(projection_match.group("path")) if projection_match else None
    raw_packet_path = Path(raw_match.group("path")) if raw_match else None
    if exit_code == 0 and projection_path is None:
        return RetailGridCaptureAttempt(
            exit_code=4,
            message=f"monitor could not parse a derived observation path: {message}",
            raw_packet_path=raw_packet_path,
        )
    return RetailGridCaptureAttempt(
        exit_code=exit_code,
        message=message,
        projection_path=projection_path,
        raw_packet_path=raw_packet_path,
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Run one operator-triggered daily round of configured retail-grid brand monitors."
        )
    )
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--data-root", required=True)
    parser.add_argument("--state-dir", type=Path, required=True)
    parser.add_argument("--round-id", default=None, help="Defaults to the local YYYY-MM-DD date.")
    parser.add_argument(
        "--qa-sample",
        action="append",
        default=[],
        metavar="BRAND_ID:RETAILER",
        help="Force a successful raw QA sample for one configured pair; repeatable.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        if not args.state_dir.is_absolute():
            raise ValueError("--state-dir must be an absolute path")
        state_dir = args.state_dir.resolve()
        try:
            state_dir.relative_to(REPO_ROOT.resolve())
        except ValueError:
            pass
        else:
            raise ValueError("--state-dir must be outside the repository")
        data_root = DataLakeRoot.resolve(explicit=args.data_root)
        manifest = load_monitor_manifest(args.manifest.resolve())
        exit_code, report_path, report = run_monitor_round(
            manifest=manifest,
            data_root=data_root,
            state_dir=state_dir,
            round_id=args.round_id or date.today().isoformat(),
            qa_samples=set(args.qa_sample),
            capture_route=lambda route, retain: capture_route(
                route, retain, data_root=data_root
            ),
        )
    except ValueError as exc:
        parser.exit(status=2, message=f"retail-grid monitor failed: {exc}\n")
    except Exception as exc:
        parser.exit(
            status=3,
            message=f"retail-grid monitor failed: {type(exc).__name__}: {exc}\n",
        )
    print(
        f"retail-grid monitor {report['status']}: report={report_path}; "
        f"series={report['configured_series_count']}; failures={report['failure_count']}"
    )
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
