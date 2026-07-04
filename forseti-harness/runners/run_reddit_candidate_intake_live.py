from __future__ import annotations

import argparse
from datetime import UTC, datetime
import sys
from pathlib import Path
from typing import Callable, Sequence
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import ProxyHandler, Request, build_opener

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from capture_spine.reddit_candidate_intake import (
    CandidateSurface,
    CapType,
    CoverageClaim,
    RunEnvelope,
    RunProvenanceReceipt,
    StopReason,
    build_candidate_intake_output,
    project_old_reddit_html_candidate_subreddits,
    project_old_reddit_html_listing,
    write_candidate_intake_output,
)


DEFAULT_TIMEOUT_SECONDS = 20.0
DEFAULT_MAX_BYTES = 1_000_000
DEFAULT_USER_AGENT = "OrcaRedditCandidateIntake/0.1 (bounded Reddit candidate intake)"
_NO_PROXY_OPENER = build_opener(ProxyHandler({}))

FetchHtml = Callable[[str, float, int], tuple[int, str]]


def run_reddit_candidate_intake_live(
    *,
    output_directory: Path,
    run_id: str,
    run_purpose: str,
    declared_topic_theme_query: str,
    source_url: str,
    source_surface: CandidateSurface,
    seed_subreddits: tuple[str, ...],
    max_subreddits: int = 5,
    max_threads_per_subreddit: int = 25,
    max_pages_or_result_surfaces: int = 1,
    time_window_days: int = 30,
    sort_order: str = "hot",
    exclusions: tuple[str, ...] = (
        "no_link_following",
        "no_user_profile_capture",
        "no_subreddit_crawl",
        "no_recommendation_expansion",
        "no_comment_link_expansion",
    ),
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
    max_bytes: int = DEFAULT_MAX_BYTES,
    fetch_html: FetchHtml | None = None,
) -> tuple[int, str]:
    fetch = fetch_html or _fetch_old_reddit_html
    timestamp = _utc_now()
    method_category = "live_old_reddit_direct_http_candidate_intake"
    envelope = RunEnvelope(
        run_id=run_id,
        run_purpose=run_purpose,
        cap_type=CapType.PROBE,
        coverage_claim=CoverageClaim.BOUNDED_PROBE_ONLY,
        max_subreddits=max_subreddits,
        max_threads_per_subreddit=max_threads_per_subreddit,
        max_pages_or_result_surfaces=max_pages_or_result_surfaces,
        time_window_days=time_window_days,
        sort_order=sort_order,
        method_category=method_category,
        stop_condition=StopReason.SCOPE_EXHAUSTED,
        declared_topic_theme_query=declared_topic_theme_query,
        seed_subreddits=seed_subreddits,
        exclusions=exclusions,
        candidate_surface_allowlist=(source_surface,),
    )

    try:
        status, html_text = fetch(source_url, timeout_seconds, max_bytes)
    except (HTTPError, URLError, TimeoutError, OSError, ValueError) as exc:
        return _write_terminal_output(
            output_directory=output_directory,
            envelope=envelope,
            source_url=source_url,
            source_surface=source_surface,
            timestamp=timestamp,
            stop_reason=StopReason.BLOCKED_RESULT,
            status_note=f"{type(exc).__name__}: {exc}",
            candidate_subreddits=[],
            candidate_threads=[],
        )

    if status < 200 or status >= 300:
        return _write_terminal_output(
            output_directory=output_directory,
            envelope=envelope,
            source_url=source_url,
            source_surface=source_surface,
            timestamp=timestamp,
            stop_reason=StopReason.BLOCKED_RESULT,
            status_note=f"HTTP {status}",
            candidate_subreddits=[],
            candidate_threads=[],
        )

    if source_surface in {
        CandidateSurface.SEED_SUBREDDITS,
        CandidateSurface.RELATED_SUBREDDIT,
        CandidateSurface.RECOMMENDATION,
        CandidateSurface.MORE_LIKE_THIS,
        CandidateSurface.CROSS_POST,
    }:
        candidate_subreddits = project_old_reddit_html_candidate_subreddits(
            html_text=html_text,
            envelope=envelope,
            source_url=source_url,
            timestamp=timestamp,
            source_surface=source_surface,
            method_category=method_category,
        )
        candidate_threads = []
    else:
        candidate_subreddits = []
        candidate_threads = project_old_reddit_html_listing(
            html_text=html_text,
            envelope=envelope,
            source_url=source_url,
            timestamp=timestamp,
            source_surface=source_surface,
            method_category=method_category,
        )

    stop_reason = StopReason.SCOPE_EXHAUSTED
    if not candidate_subreddits and not candidate_threads:
        stop_reason = StopReason.EMPTY_RESULT
    if len(candidate_subreddits) >= max_subreddits or len(candidate_threads) >= max_threads_per_subreddit:
        stop_reason = StopReason.CAPS_REACHED

    return _write_terminal_output(
        output_directory=output_directory,
        envelope=envelope,
        source_url=source_url,
        source_surface=source_surface,
        timestamp=timestamp,
        stop_reason=stop_reason,
        status_note=f"HTTP {status}",
        candidate_subreddits=candidate_subreddits,
        candidate_threads=candidate_threads,
    )


def _write_terminal_output(
    *,
    output_directory: Path,
    envelope: RunEnvelope,
    source_url: str,
    source_surface: CandidateSurface,
    timestamp: str,
    stop_reason: StopReason,
    status_note: str,
    candidate_subreddits: list[object],
    candidate_threads: list[object],
) -> tuple[int, str]:
    provenance = RunProvenanceReceipt(
        run_id=envelope.run_id,
        caps_applied={
            "max_subreddits": envelope.max_subreddits,
            "max_threads_per_subreddit": envelope.max_threads_per_subreddit,
            "max_pages_or_result_surfaces": envelope.max_pages_or_result_surfaces,
            "time_window_days": envelope.time_window_days,
        },
        source_surface=source_surface.value,
        query_or_listing_path=urlparse(source_url).path or source_url,
        sort_order=envelope.sort_order,
        time_window_days=envelope.time_window_days,
        method_category=envelope.method_category,
        timestamp=timestamp,
        row_counts={
            "candidate_subreddits": len(candidate_subreddits),
            "candidate_threads": len(candidate_threads),
            "outbound_urls": 0,
        },
        stop_reason=stop_reason,
        exclusions_applied=envelope.exclusions,
        non_claims=(
            "not Source Capture Packet output",
            "not body/comment/profile capture",
            "not Data Capture handoff",
            "not source-quality scoring",
            "not Armory execution",
            "not broad Reddit crawl",
            "not raw HTML persistence",
            "not commercial Reddit use",
            f"live fetch status: {status_note}",
        ),
    )
    output = build_candidate_intake_output(
        envelope=envelope,
        provenance=provenance,
        candidate_subreddits=list(candidate_subreddits),
        candidate_threads=list(candidate_threads),
    )
    output["reddit_candidate_url_intake"]["live_run_receipt"] = {
        "live_access_authorized_for_this_run": True,
        "access_mode": "old_reddit_direct_http_single_surface",
        "source_policy_posture": "source surface bound by run envelope; candidate-only projection and no raw source persistence",
        "source_url": source_url,
        "source_surface": source_surface.value,
        "status_note": status_note,
        "raw_source_persisted": False,
        "armory_invoked": False,
        "capture_packet_emitted": False,
    }
    write_result = write_candidate_intake_output(output=output, output_directory=output_directory)
    return 0, write_result["json_path"]


def _fetch_old_reddit_html(url: str, timeout_seconds: float, max_bytes: int) -> tuple[int, str]:
    if timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be greater than zero")
    if max_bytes <= 0:
        raise ValueError("max_bytes must be greater than zero")
    request = Request(
        url,
        headers={
            "User-Agent": DEFAULT_USER_AGENT,
            "Accept": "text/html,*/*;q=0.8",
        },
        method="GET",
    )
    with _NO_PROXY_OPENER.open(request, timeout=timeout_seconds) as response:
        body = response.read(max_bytes + 1)
        if len(body) > max_bytes:
            raise ValueError(f"response exceeded max_bytes={max_bytes}")
        content_type = response.headers.get("Content-Type", "")
        if "html" not in content_type.lower():
            raise ValueError(f"expected HTML response, got Content-Type={content_type!r}")
        return int(response.getcode()), body.decode("utf-8", errors="replace")


def _utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run bounded live old Reddit Candidate URL Intake for one declared subreddit/listing surface."
    )
    parser.add_argument("--output-directory", type=Path, required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--run-purpose", required=True)
    parser.add_argument("--declared-topic-theme-query", required=True)
    parser.add_argument("--source-url", required=True)
    parser.add_argument(
        "--source-surface",
        choices=[surface.value for surface in CandidateSurface],
        required=True,
    )
    parser.add_argument("--seed-subreddit", action="append", default=[])
    parser.add_argument("--max-subreddits", type=int, default=5)
    parser.add_argument("--max-threads-per-subreddit", type=int, default=25)
    parser.add_argument("--max-pages-or-result-surfaces", type=int, default=1)
    parser.add_argument("--time-window-days", type=int, default=30)
    parser.add_argument("--sort-order", default="hot")
    parser.add_argument("--exclusion", action="append", default=[])
    parser.add_argument("--timeout-seconds", type=float, default=DEFAULT_TIMEOUT_SECONDS)
    parser.add_argument("--max-bytes", type=int, default=DEFAULT_MAX_BYTES)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    exclusions = tuple(args.exclusion) if args.exclusion else (
        "no_link_following",
        "no_user_profile_capture",
        "no_subreddit_crawl",
        "no_recommendation_expansion",
        "no_comment_link_expansion",
    )
    try:
        exit_code, message = run_reddit_candidate_intake_live(
            output_directory=args.output_directory,
            run_id=args.run_id,
            run_purpose=args.run_purpose,
            declared_topic_theme_query=args.declared_topic_theme_query,
            source_url=args.source_url,
            source_surface=CandidateSurface(args.source_surface),
            seed_subreddits=tuple(args.seed_subreddit),
            max_subreddits=args.max_subreddits,
            max_threads_per_subreddit=args.max_threads_per_subreddit,
            max_pages_or_result_surfaces=args.max_pages_or_result_surfaces,
            time_window_days=args.time_window_days,
            sort_order=args.sort_order,
            exclusions=exclusions,
            timeout_seconds=args.timeout_seconds,
            max_bytes=args.max_bytes,
        )
    except Exception as exc:
        parser.exit(status=2, message=f"reddit live candidate intake failed: {exc}\n")
    print(message)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
