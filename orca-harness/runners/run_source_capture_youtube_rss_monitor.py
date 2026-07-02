"""Ledger-driven daily YT tier-1 RSS monitor -- one packet per roster channel.

The cheap daily tier under the owner's 2026-07-02 two-tier direction (assessed
in ``orca/product/spines/capture/core/source_families/social_media/youtube/
youtube_shorts_grid_tier_assessment_v0.md``): per admitted roster channel, one
logged-out fetch of the public channel feed
(``youtube.com/feeds/videos.xml?channel_id=<UC...>``), parsed into typed
entries (exact views, exact publish timestamps, starRating count recorded as
the like count with its provenance named), committed to the lake as one
SourceCapturePacket per channel under the NEW producer surface
``youtube_channel_rss_feed`` -- every existing YouTube consumer filters on
``source_surface`` and skips it.

First-seen semantics (three-valued, per entry): ``first_seen_baseline`` when
the channel has no prior packet on this surface; else ``true`` iff the
video_id is absent from the latest prior packet's cumulative known set, else
``false``. The cumulative set (prior known union current entries) rides in
each packet's entries artifact, so state is derived from the lake -- no
sidecar store -- and a video that leaves the 15-entry feed window stays known.

Mirrors the watch-batch discipline: injected ``fetch_fn``/``sleep_fn``/
``now_fn`` keep the core lake-free-testable against ``DataLakeRoot.for_test``;
pacing between channels; N consecutive per-channel failures trip a circuit
break that writes a runner-scoped cooldown record (a rerun during active
cooldown refuses, exit 4); a finished run with ANY per-channel failure exits
nonzero and names it. The summary is a DISPOSABLE run report, not a durable
schema. No spike rule, no trigger wiring, no registry changes, no scheduler.
This wrapper makes no ToS-safety or blocking-avoidance claim.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from data_lake.root import DataLakeRoot, DataLakeRootError
from source_capture import (
    CaptureModeCategory,
    PacketTiming,
    SourceCaptureSlice,
    known_fact,
    not_applicable,
    not_attempted,
    unknown_with_reason,
)
from source_capture.models import CoverageWindow, MetricObservation, MetricPosture
from source_capture.packet_assembly import stage_and_write_packet, staged_file_id_map
from source_capture.youtube_channel_rss import (
    YoutubeChannelFeedParse,
    YoutubeChannelFeedParseFailure,
    parse_youtube_channel_feed,
)

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_LINKAGE_LEDGER = (
    ROOT
    / "orca"
    / "product"
    / "spines"
    / "capture"
    / "core"
    / "source_families"
    / "social_media"
    / "creator_registry"
    / "creator_public_handle_linkage_ledger_v0.json"
)

SOURCE_FAMILY = "youtube"
SOURCE_SURFACE = "youtube_channel_rss_feed"
FEED_URL_TEMPLATE = "https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
ENTRIES_ARTIFACT_FILENAME = "rss_monitor_entries.json"

FIRST_SEEN_BASELINE = "baseline"
FIRST_SEEN_TRUE = "true"
FIRST_SEEN_FALSE = "false"

DEFAULT_PACE_SECONDS = 12.0
DEFAULT_BREAK_AFTER_FAILURES = 3
DEFAULT_COOLDOWN_SECONDS = 3600.0
# Mirrors the watch-batch convention: 4 = circuit break or active cooldown.
YOUTUBE_RSS_MONITOR_EXIT_CODE_BREAK = 4
DEFAULT_DECISION_QUESTION = (
    "Daily tier-1 monitor observation of roster channels' newest uploads "
    "(exact views/dates/likes) for spike-triggered deep capture."
)

STAR_RATING_PROVENANCE_NOTE = (
    "like_count is sourced from the feed's media:starRating count; validated "
    "against watch-page likeCount on 2026-07-02 (N=2, packet "
    "raw/f16/01KWHV1Q2E48SS4A9QXGRR90B5) -- provenance, not platform truth"
)
FEED_WINDOW_LIMITATION = (
    "feed carries only the 15 most recent uploads mixed across formats "
    "(Shorts/videos/VODs); comment counts absent from the feed schema"
)


def ledger_youtube_channels(ledger: Mapping[str, Any]) -> list[dict[str, Any]]:
    """The roster's YouTube rows, read-only: platform_account_id, handle label,
    and channel id (which may honestly be None -- callers must surface, not
    drop, such rows)."""
    body = ledger.get("creator_public_handle_linkage_ledger")
    if not isinstance(body, Mapping):
        raise ValueError("linkage ledger missing creator_public_handle_linkage_ledger object")
    accounts = body.get("platform_accounts")
    if not isinstance(accounts, list):
        raise ValueError("linkage ledger missing platform_accounts list")
    rows = [
        {
            "platform_account_id": account.get("platform_account_id"),
            "public_handle": account.get("public_handle"),
            "channel_id_or_none": account.get("platform_public_account_id_or_none"),
        }
        for account in accounts
        if isinstance(account, Mapping) and account.get("platform") == "youtube"
    ]
    if not rows:
        raise ValueError("linkage ledger has no YouTube platform_accounts rows")
    return rows


def _default_fetch_fn(url: str) -> tuple[int, str, bytes]:
    from youtube_capture.capture_youtube_v0 import http_get

    return http_get(url)


def default_output_root() -> Path:
    return Path(__file__).resolve().parents[1] / "_test_runs" / "youtube_rss_monitor"


def default_cooldown_ledger_path() -> Path:
    return Path(__file__).resolve().parents[1] / "_test_runs" / "youtube_rss_monitor_cooldown_ledger.json"


def run_youtube_rss_monitor(
    data_root: DataLakeRoot,
    *,
    ledger: Mapping[str, Any],
    decision_question: str = DEFAULT_DECISION_QUESTION,
    pace_seconds: float = DEFAULT_PACE_SECONDS,
    break_after_failures: int = DEFAULT_BREAK_AFTER_FAILURES,
    cooldown_seconds: float = DEFAULT_COOLDOWN_SECONDS,
    ignore_cooldown: bool = False,
    output_root: Path | None = None,
    cooldown_ledger_path: Path | None = None,
    fetch_fn: Callable[[str], tuple[int, str, bytes]] = _default_fetch_fn,
    sleep_fn: Callable[[float], None] | None = None,
    now_fn: Callable[[], datetime] | None = None,
) -> tuple[int, str]:
    """Sweep the roster's YouTube channels through one feed capture each.
    Returns ``(exit_code, summary_path)``: 0 = all channels captured (skipped
    null-id rows are visible, not failures); 2 = finished with named
    per-channel failures; 4 = circuit break or active cooldown."""
    _validate_inputs(
        pace_seconds=pace_seconds,
        break_after_failures=break_after_failures,
        cooldown_seconds=cooldown_seconds,
    )
    if sleep_fn is None:
        import time

        sleep_fn = time.sleep
    now_fn = now_fn or (lambda: datetime.now(UTC))
    output_root = output_root or default_output_root()
    cooldown_ledger_path = cooldown_ledger_path or default_cooldown_ledger_path()

    channels = ledger_youtube_channels(ledger)
    output_root.mkdir(parents=True, exist_ok=True)
    started_at = now_fn()
    summary_path = output_root / f"youtube_rss_monitor_summary_{_file_stamp(started_at)}.json"

    cooldown = _active_cooldown(cooldown_ledger_path=cooldown_ledger_path, now=started_at)
    if cooldown is not None and not ignore_cooldown:
        summary = _build_summary(
            status="cooldown_active",
            channels=channels,
            rows=[],
            break_reason=None,
            cooldown=cooldown,
            cooldown_seconds=cooldown_seconds,
            started_at=started_at,
            finished_at=now_fn(),
        )
        _write_json(summary_path, summary)
        return YOUTUBE_RSS_MONITOR_EXIT_CODE_BREAK, str(summary_path)

    prior_states = _latest_channel_states(
        data_root,
        channel_ids={
            row["channel_id_or_none"] for row in channels if row["channel_id_or_none"]
        },
    )

    rows: list[dict[str, Any]] = []
    failure_streak = 0
    break_reason: str | None = None
    cooldown_record: dict[str, Any] | None = None
    attempted_any = False

    for channel in channels:
        channel_id = channel["channel_id_or_none"]
        if not channel_id:
            rows.append(
                {
                    "platform_account_id": channel["platform_account_id"],
                    "channel_id": None,
                    "status": "skipped_no_channel_id",
                    "packet_ref_or_error": (
                        "ledger row has no platform_public_account_id_or_none; "
                        "feed URL cannot be formed"
                    ),
                    "attempted_at": None,
                }
            )
            continue

        if attempted_any and pace_seconds > 0:
            sleep_fn(pace_seconds)
        attempted_any = True

        row: dict[str, Any] = {
            "platform_account_id": channel["platform_account_id"],
            "channel_id": channel_id,
            "status": "capture_failed",
            "packet_ref_or_error": None,
            "attempted_at": _format_utc(now_fn()),
        }
        try:
            packet_id = _capture_channel(
                data_root,
                channel=channel,
                prior_state=prior_states.get(channel_id),
                decision_question=decision_question,
                fetch_fn=fetch_fn,
                now_fn=now_fn,
            )
            row["status"] = "captured"
            row["packet_ref_or_error"] = packet_id
            failure_streak = 0
        except Exception as exc:  # noqa: BLE001 - per-channel failures stay visible in the summary
            row["packet_ref_or_error"] = f"{type(exc).__name__}: {exc}"
            failure_streak += 1
        rows.append(row)

        if failure_streak >= break_after_failures:
            break_reason = (
                f"{failure_streak} consecutive channel-capture failures (threshold "
                f"{break_after_failures}); suspected transport-level blocking"
            )
            cooldown_record = _write_cooldown_record(
                cooldown_ledger_path=cooldown_ledger_path,
                cooldown_seconds=cooldown_seconds,
                now=now_fn(),
                trigger_channel_id=channel_id,
                break_reason=break_reason,
                output_root=output_root,
            )
            break

    status = (
        "stopped_circuit_break"
        if break_reason is not None
        else (
            "completed"
            if all(r["status"] in {"captured", "skipped_no_channel_id"} for r in rows)
            and len(rows) == len(channels)
            else "completed_with_failures"
        )
    )
    summary = _build_summary(
        status=status,
        channels=channels,
        rows=rows,
        break_reason=break_reason,
        cooldown=cooldown_record,
        cooldown_seconds=cooldown_seconds,
        started_at=started_at,
        finished_at=now_fn(),
    )
    _write_json(summary_path, summary)

    if status == "stopped_circuit_break":
        return YOUTUBE_RSS_MONITOR_EXIT_CODE_BREAK, str(summary_path)
    if status == "completed":
        return 0, str(summary_path)
    return 2, str(summary_path)


def _capture_channel(
    data_root: DataLakeRoot,
    *,
    channel: Mapping[str, Any],
    prior_state: Mapping[str, Any] | None,
    decision_question: str,
    fetch_fn: Callable[[str], tuple[int, str, bytes]],
    now_fn: Callable[[], datetime],
) -> str:
    """Fetch, parse, and commit one channel's feed packet. Raises on any
    failure (transport, HTTP status, parse) so the caller records it visibly."""
    channel_id = str(channel["channel_id_or_none"])
    url = FEED_URL_TEMPLATE.format(channel_id=channel_id)
    capture_time = _format_utc(now_fn())
    status, final_url, raw = fetch_fn(url)
    if status != 200:
        raise RuntimeError(f"feed fetch returned http_status={status} for {url}")
    parsed = parse_youtube_channel_feed(raw.decode("utf-8", "replace"))
    if isinstance(parsed, YoutubeChannelFeedParseFailure):
        raise RuntimeError(f"feed parse failed ({parsed.failure_kind}): {parsed.message}")

    compared_prior_packet_id = prior_state["packet_id"] if prior_state else None
    known_before: set[str] = set(prior_state["known_video_ids"]) if prior_state else set()
    entry_records = []
    for entry in parsed.entries:
        if compared_prior_packet_id is None:
            first_seen = FIRST_SEEN_BASELINE
        elif entry.video_id in known_before:
            first_seen = FIRST_SEEN_FALSE
        else:
            first_seen = FIRST_SEEN_TRUE
        entry_records.append(
            {
                "video_id": entry.video_id,
                "title": entry.title,
                "published": entry.published,
                "updated": entry.updated,
                "view_count_exact": entry.view_count,
                "star_rating_count": entry.star_rating_count,
                "first_seen": first_seen,
            }
        )
    known_cumulative = sorted(known_before | {entry.video_id for entry in parsed.entries})

    entries_payload = {
        "schema_note": "disposable-shaped entries artifact for the youtube_channel_rss_feed surface",
        "platform_account_id": channel["platform_account_id"],
        "public_handle_label": channel["public_handle"],
        "channel_id": channel_id,
        "requested_url": url,
        "final_url": final_url,
        "retrieval_time_utc": capture_time,
        "feed_channel_id_as_served": parsed.feed_channel_id_as_served,
        "feed_title": parsed.feed_title,
        "entry_channel_ids": list(parsed.entry_channel_ids),
        "compared_prior_packet_id_or_none": compared_prior_packet_id,
        "first_seen_semantics": (
            "baseline = no prior packet on this surface for this channel; "
            "true/false = video_id absent/present in the latest prior packet's "
            "known_video_ids_cumulative"
        ),
        "entries": entry_records,
        "known_video_ids_cumulative": known_cumulative,
        "raw_feed_sha256": hashlib.sha256(raw).hexdigest(),
        "limitation_notes": list(parsed.limitation_notes),
    }
    entries_bytes = f"{json.dumps(entries_payload, indent=2, ensure_ascii=False, sort_keys=True)}\n".encode(
        "utf-8"
    )
    staged_artifacts = [
        (f"feed_{channel_id}.xml", raw),
        (ENTRIES_ARTIFACT_FILENAME, entries_bytes),
    ]
    file_ids = staged_file_id_map(staged_artifacts)
    preserved_file_ids = list(file_ids.values())

    access = known_fact(
        "youtube_logged_out_channel_rss_feed_http_capture; public XML; no cookies or session"
    )
    archive = not_attempted("rss monitor does not query archive or history services")
    media = known_fact("raw feed XML preserved; media bytes out of scope")
    if compared_prior_packet_id is not None:
        # Ob.15 closed vocabulary: a daily monitor observation SUPPLEMENTS the
        # prior series (never supersedes it). The compared prior packet id is
        # recorded in the entries artifact, not here.
        recapture_relationship = known_fact("supplement")
        recapture_time = known_fact(capture_time)
    else:
        recapture_relationship = not_applicable(
            "first lake packet for this channel on this surface"
        )
        recapture_time = not_applicable(
            "first lake packet for this channel on this surface"
        )

    def timing(publication_fact) -> PacketTiming:
        return PacketTiming(
            source_publication_or_event=publication_fact,
            source_edit_or_version=unknown_with_reason(
                "rss monitor did not infer source edit/version timing"
            ),
            capture_time=known_fact(capture_time),
            recapture_time=recapture_time,
            cutoff_posture=unknown_with_reason(
                "rss monitor did not receive cutoff posture metadata"
            ),
        )

    channel_limitations = [FEED_WINDOW_LIMITATION]
    if parsed.limitation_notes:
        channel_limitations.append(
            f"feed_parse_limitations_present: {len(parsed.limitation_notes)} note(s); "
            f"see {ENTRIES_ARTIFACT_FILENAME}"
        )
    source_slices: list[SourceCaptureSlice] = [
        SourceCaptureSlice(
            slice_id="yt_rss_channel_00",
            locator=known_fact(final_url),
            timing=timing(
                unknown_with_reason("feed document is an enumeration surface, not a dated post")
            ),
            access_posture=access,
            archive_history_posture=archive,
            media_modality_posture=media,
            re_capture_relationship=recapture_relationship,
            limitations=channel_limitations,
            warning_notes=[],
            preserved_file_ids=preserved_file_ids,
            metric_observations=[],
        )
    ]
    for index, record in enumerate(entry_records, start=1):
        publication = (
            known_fact(record["published"])
            if record["published"] is not None
            else unknown_with_reason("feed entry carried no published timestamp")
        )
        source_slices.append(
            SourceCaptureSlice(
                slice_id=f"yt_rss_entry_{index:02d}_{record['video_id']}",
                locator=known_fact(f"https://www.youtube.com/watch?v={record['video_id']}"),
                timing=timing(publication),
                access_posture=access,
                archive_history_posture=archive,
                media_modality_posture=media,
                re_capture_relationship=recapture_relationship,
                limitations=[],
                warning_notes=[],
                preserved_file_ids=preserved_file_ids,
                metric_observations=_entry_metric_observations(
                    record, capture_time=capture_time
                ),
            )
        )

    first_seen_true_count = sum(
        1 for record in entry_records if record["first_seen"] == FIRST_SEEN_TRUE
    )
    result = stage_and_write_packet(
        data_root=data_root,
        staged_artifacts=staged_artifacts,
        source_slices=source_slices,
        source_family=SOURCE_FAMILY,
        source_surface=SOURCE_SURFACE,
        source_locator=known_fact(url),
        decision_question=decision_question,
        capture_context=(
            "logged-out public channel RSS feed capture; one request per channel; "
            "tier-1 daily monitor observation (exact views, exact publish "
            "timestamps, starRating-as-like-count with provenance)"
        ),
        actor_audience_context=known_fact(
            "public creator channel feed; logged-out capture; internal creator-monitoring tier-1"
        ),
        capture_mode=CaptureModeCategory.AUTOMATED_EXTRACTION,
        operator_category="youtube_rss_monitor_operator",
        session_identity=None,
        visible_mode_changes=[
            (
                f"yt_rss_monitor:entries={len(entry_records)}"
                f":first_seen_true={first_seen_true_count}"
                f":baseline={compared_prior_packet_id is None}"
            ),
        ],
        source_publication_or_event=unknown_with_reason(
            "feed document is an enumeration surface; per-entry timing governs"
        ),
        source_edit_or_version=unknown_with_reason(
            "rss monitor did not infer source edit/version timing"
        ),
        cutoff_posture=unknown_with_reason(
            "rss monitor did not receive cutoff posture metadata"
        ),
        recapture_time=recapture_time,
        access_posture=access,
        archive_history_posture=archive,
        media_modality_posture=media,
        re_capture_relationship=recapture_relationship,
        warnings=[],
        limitations=[
            FEED_WINDOW_LIMITATION,
            STAR_RATING_PROVENANCE_NOTE,
            "channel_slice_limitations_present: the channel slice carries the "
            "feed-window limitation; entry-level parse notes (if any) ride in "
            f"{ENTRIES_ARTIFACT_FILENAME}",
        ],
        receipt_summary=(
            f"Daily RSS monitor packet for channel {channel_id}: "
            f"{len(entry_records)} entries, {first_seen_true_count} first-seen"
            f"{' (baseline run)' if compared_prior_packet_id is None else ''}; "
            "exact views + publish timestamps; likes via starRating provenance."
        ),
        receipt_non_claims=[
            "not a spike decision or spike threshold",
            "not registry pipeline input (trigger-only tier-1)",
            "not Shorts-vs-video classification",
            "not comment capture (feed schema carries none)",
            "not validation, readiness, or acceptance",
            "not a ToS-safety or blocking-avoidance guarantee",
        ],
    )
    return Path(str(result.output_directory)).name


def _entry_metric_observations(
    record: Mapping[str, Any], *, capture_time: str
) -> list[MetricObservation]:
    coverage = CoverageWindow(end=capture_time)
    observations: list[MetricObservation] = []
    if record["view_count_exact"] is not None:
        observations.append(
            MetricObservation(
                metric="view_count",
                posture=MetricPosture.OBSERVED,
                value=record["view_count_exact"],
                coverage_window=coverage,
            )
        )
    else:
        observations.append(
            MetricObservation(
                metric="view_count",
                posture=MetricPosture.UNAVAILABLE_WITH_REASON,
                reason="feed entry carried no parseable media:statistics views",
                coverage_window=coverage,
            )
        )
    if record["star_rating_count"] is not None:
        observations.append(
            MetricObservation(
                metric="like_count",
                posture=MetricPosture.OBSERVED,
                value=record["star_rating_count"],
                coverage_window=coverage,
            )
        )
    else:
        observations.append(
            MetricObservation(
                metric="like_count",
                posture=MetricPosture.UNAVAILABLE_WITH_REASON,
                reason="feed entry carried no parseable media:starRating count",
                coverage_window=coverage,
            )
        )
    observations.append(
        MetricObservation(
            metric="comment_count",
            posture=MetricPosture.UNAVAILABLE_WITH_REASON,
            reason="feed schema carries no comment count",
            coverage_window=coverage,
        )
    )
    return observations


def _latest_channel_states(
    data_root: DataLakeRoot, *, channel_ids: set[str]
) -> dict[str, dict[str, Any]]:
    """Newest-first scan of this surface's committed packets, stopping once
    every wanted channel has its latest prior state. Packet ids are ULIDs, so
    the availability listing's sort order is commit-time order. On a healthy
    daily cadence this loads about one packet per channel."""
    states: dict[str, dict[str, Any]] = {}
    if not channel_ids:
        return states
    for packet_id in reversed(data_root.list_available(source_family=SOURCE_FAMILY)):
        if channel_ids <= states.keys():
            break
        entry = data_root.read_availability(packet_id)
        if not entry or entry.get("source_surface") != SOURCE_SURFACE:
            continue
        payload = _entries_artifact_payload(data_root, packet_id)
        if payload is None:
            continue
        channel_id = payload.get("channel_id")
        if not isinstance(channel_id, str) or channel_id not in channel_ids:
            continue
        if channel_id in states:
            continue
        known = payload.get("known_video_ids_cumulative")
        states[channel_id] = {
            "packet_id": packet_id,
            "known_video_ids": [v for v in known if isinstance(v, str)]
            if isinstance(known, list)
            else [],
        }
    return states


def _entries_artifact_payload(
    data_root: DataLakeRoot, packet_id: str
) -> dict[str, Any] | None:
    """Verified by-key read of a packet's entries artifact; a readback problem
    is reported as no-state (the run then treats the channel as baseline-with-
    provenance rather than silently inventing prior knowledge)."""
    try:
        loaded = data_root.load_raw_packet(packet_id)
        for entry in loaded.manifest.get("preserved_files", []):
            basename = str(entry.get("relative_packet_path", "")).rsplit("/", 1)[-1]
            original = basename.split("_", 1)[1] if "_" in basename else basename
            if original == ENTRIES_ARTIFACT_FILENAME:
                payload = json.loads(loaded.bodies[entry["file_id"]].decode("utf-8"))
                return payload if isinstance(payload, dict) else None
    except Exception:  # noqa: BLE001 - state derivation is best-effort; absence stays honest
        return None
    return None


# -- run mechanics (mirrors the watch-batch wrapper) ----------------------------

def _validate_inputs(
    *, pace_seconds: float, break_after_failures: int, cooldown_seconds: float
) -> None:
    if pace_seconds < 0:
        raise ValueError("pace_seconds must be zero or greater")
    if break_after_failures <= 0:
        raise ValueError("break_after_failures must be greater than zero")
    if cooldown_seconds < 0:
        raise ValueError("cooldown_seconds must be zero or greater")


def _active_cooldown(*, cooldown_ledger_path: Path, now: datetime) -> dict[str, Any] | None:
    if not cooldown_ledger_path.is_file():
        return None
    payload = json.loads(cooldown_ledger_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("YouTube rss monitor cooldown ledger must be a JSON object")
    raw_until = payload.get("cooldown_until")
    if not isinstance(raw_until, str):
        raise ValueError("YouTube rss monitor cooldown ledger missing cooldown_until")
    if _parse_utc(raw_until) <= now:
        return None
    out = dict(payload)
    out["cooldown_active"] = True
    return out


def _write_cooldown_record(
    *,
    cooldown_ledger_path: Path,
    cooldown_seconds: float,
    now: datetime,
    trigger_channel_id: str,
    break_reason: str,
    output_root: Path,
) -> dict[str, Any]:
    record = {
        "runner": "youtube_rss_monitor",
        "cooldown_started_at": _format_utc(now),
        "cooldown_until": _format_utc(now + timedelta(seconds=cooldown_seconds)),
        "cooldown_seconds": cooldown_seconds,
        "trigger_channel_id": trigger_channel_id,
        "trigger_reason": break_reason,
        "monitor_output_root": str(output_root),
        "non_claims": [
            "not proof of an actual platform block",
            "not a ToS-safety or blocking-avoidance guarantee",
            "not validation",
        ],
    }
    cooldown_ledger_path.parent.mkdir(parents=True, exist_ok=True)
    _write_json(cooldown_ledger_path, record)
    return record


def _build_summary(
    *,
    status: str,
    channels: Sequence[Mapping[str, Any]],
    rows: list[dict[str, Any]],
    break_reason: str | None,
    cooldown: dict[str, Any] | None,
    cooldown_seconds: float,
    started_at: datetime,
    finished_at: datetime,
) -> dict[str, Any]:
    captured = sum(1 for row in rows if row["status"] == "captured")
    skipped = sum(1 for row in rows if row["status"] == "skipped_no_channel_id")
    failed = sum(1 for row in rows if row["status"] == "capture_failed")
    return {
        "runner": "youtube_rss_monitor",
        "source_surface": SOURCE_SURFACE,
        "status": status,
        "started_at": _format_utc(started_at),
        "finished_at": _format_utc(finished_at),
        "break_reason_or_none": break_reason,
        "cooldown_or_none": cooldown,
        "cooldown_policy": {"ledger_enabled": True, "cooldown_seconds": cooldown_seconds},
        "counts": {
            "roster_total": len(channels),
            "attempted": captured + failed,
            "captured": captured,
            "skipped_no_channel_id": skipped,
            "capture_failed": failed,
            "not_attempted": len(channels) - len(rows),
        },
        "failed_channel_ids": [
            row["channel_id"] for row in rows if row["status"] == "capture_failed"
        ],
        "results": rows,
        "non_claims": [
            "disposable run report, not a durable schema",
            "not a spike decision, registry input, or scheduler",
            "not a ToS-safety or blocking-avoidance guarantee",
        ],
    }


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(
        f"{json.dumps(payload, indent=2, sort_keys=True)}\n", encoding="utf-8", newline="\n"
    )


def _file_stamp(value: datetime) -> str:
    return value.astimezone(UTC).strftime("%Y%m%dT%H%M%SZ")


def _format_utc(value: datetime) -> str:
    value = value.astimezone(UTC) if value.tzinfo is not None else value.replace(tzinfo=UTC)
    return value.isoformat().replace("+00:00", "Z")


def _parse_utc(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(UTC)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Daily tier-1 RSS monitor: one public channel-feed capture packet per "
            "roster channel, with pacing, circuit-break, cooldown, and a disposable summary."
        )
    )
    parser.add_argument("--linkage-ledger", type=Path, default=DEFAULT_LINKAGE_LEDGER)
    parser.add_argument("--data-root", default=None, help="Lake root; defaults to ORCA_DATA_ROOT.")
    parser.add_argument("--decision-question", default=DEFAULT_DECISION_QUESTION)
    parser.add_argument("--pace-seconds", type=float, default=DEFAULT_PACE_SECONDS)
    parser.add_argument("--break-after-failures", type=int, default=DEFAULT_BREAK_AFTER_FAILURES)
    parser.add_argument("--cooldown-seconds", type=float, default=DEFAULT_COOLDOWN_SECONDS)
    parser.add_argument("--ignore-cooldown", action="store_true")
    parser.add_argument("--output-root", type=Path, default=None)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        data_root = DataLakeRoot.resolve(explicit=args.data_root)
    except DataLakeRootError as exc:
        parser.exit(status=2, message=f"data lake unavailable: {exc}\n")

    ledger = json.loads(Path(args.linkage_ledger).read_text(encoding="utf-8-sig"))

    try:
        exit_code, summary_path = run_youtube_rss_monitor(
            data_root,
            ledger=ledger,
            decision_question=args.decision_question,
            pace_seconds=args.pace_seconds,
            break_after_failures=args.break_after_failures,
            cooldown_seconds=args.cooldown_seconds,
            ignore_cooldown=args.ignore_cooldown,
            output_root=args.output_root,
        )
    except ValueError as exc:
        parser.exit(status=2, message=f"youtube rss monitor failed: {exc}\n")

    summary = json.loads(Path(summary_path).read_text(encoding="utf-8"))
    counts = summary["counts"]
    print(
        f"{summary['status']}: captured={counts['captured']} failed={counts['capture_failed']} "
        f"skipped_no_id={counts['skipped_no_channel_id']} not_attempted={counts['not_attempted']} "
        f"of roster={counts['roster_total']}"
    )
    if summary["break_reason_or_none"]:
        print(f"  break: {summary['break_reason_or_none']}")
    if summary["failed_channel_ids"]:
        print(f"  failed channels: {', '.join(summary['failed_channel_ids'])}")
    print(f"  summary: {summary_path}")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
