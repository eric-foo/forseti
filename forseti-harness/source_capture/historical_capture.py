"""Cross-archive historical-capture LOCATE orchestrator (slice E).

This is the thin orchestrator **above** the per-archive adapters (it never lives inside
``archive_org.py`` / ``archive_today.py`` / ``publisher_history.py``, which stay the isolated rungs).
On a backtest, "what did this URL look like at or before a cutoff?" must not depend on a single
archive: a Wayback miss or body-fail used to be a single-archive single-point-of-failure. This
orchestrator runs a bounded, cheapest-first **locate ladder** across independent archives and stops
at the first rung that yields a VERIFIED pre-cutoff body.

Ordered ladder (the fixed, mechanical priority order):

1. **Wayback** (``archive_org.fetch_archive_org_capture``) -- the primary general archive.
2. **archive.today** (``archive_today.fetch_archive_today_capture``) -- the second general archive,
   closing the brand/retailer single-archive SPOF that publisher-history cannot (publisher-history
   is N/A for ordinary pages). No-gate-defeat is honored inside the adapter: a challenge STOPs.
3. **publisher version-history** (``publisher_history``) -- conditional, only when the source *is* a
   doc/wiki/repo and explicit coordinates are supplied (MediaWiki page-history / GitHub commit
   history). It takes different inputs than a plain URL, so it is an opt-in typed rung, never
   guessed from the URL.

Design invariants:

- **No fake uniform protocol.** The three adapters' success dataclasses do not share a clean
  interface (Wayback uses 14-digit timestamps + a separate ``body_verification.ok`` field;
  publisher-history uses ISO-8601 timestamps and folds body verification inline, so a
  ``DirectHttpCaptureSuccess`` body IS the verified body). Each rung therefore has its own small
  extractor that normalizes its result into a neutral :class:`RungOutcome`; the branching is
  contained there, not hidden behind a lie of a shared shape.
- **Stop at the first VERIFIED pre-cutoff body.** A rung that locates a pre-cutoff memento but
  fails to retrieve/verify its body is a PARTIAL outcome -> the ladder escalates to the next rung;
  it is never rolled up into a fake success.
- **INV-1 neutral facts only.** ``archives_tried`` / ``archive_selected`` record the fixed priority
  order and each rung's mechanical outcome (located? verified body? served timestamp? what
  happened). They carry no score, weight, ranking, or quality verdict.
- **One canonical cutoff.** The orchestrator takes an ISO-8601 cutoff (publisher-history's native
  form), converts it once to the 14-digit Wayback form for the two general-archive rungs, and
  preserves the per-rung ``<=cutoff`` leak guard each adapter already enforces.

This module performs no I/O of its own beyond delegating to the adapters, imports no writer, and
constructs no packet; a runner translates the selected rung's result into a packet.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import TypeAlias

from source_capture.adapters.archive_org import (
    DEFAULT_CDX_ENDPOINT,
    DEFAULT_MAX_ATTEMPTS,
    DEFAULT_RETRY_BACKOFF_SECONDS,
    DEFAULT_SNAPSHOT_BASE_URL,
    ArchiveOrgCaptureFailure,
    ArchiveOrgCaptureResult,
    ArchiveOrgCaptureSuccess,
    fetch_archive_org_capture,
)
from source_capture.adapters.archive_today import (
    DEFAULT_TIMEMAP_BASE_URL,
    ArchiveTodayCaptureFailure,
    ArchiveTodayCaptureResult,
    ArchiveTodayCaptureSuccess,
    fetch_archive_today_capture,
)
from source_capture.adapters.direct_http import (
    DEFAULT_MAX_BYTES,
    DEFAULT_TIMEOUT_SECONDS,
    DirectHttpCaptureFailure,
    DirectHttpCaptureSuccess,
)
from source_capture.adapters.publisher_history import (
    PublisherHistoryCaptureFailure,
    PublisherHistoryCaptureResult,
    PublisherHistoryCaptureSuccess,
    fetch_github_history_capture,
    fetch_mediawiki_history_capture,
)


# --------------------------------------------------------------------------------------------------
# Publisher-history rung specs (typed, opt-in -- never guessed from the URL)
# --------------------------------------------------------------------------------------------------


@dataclass(frozen=True)
class MediaWikiRung:
    wiki_api_base: str
    title: str


@dataclass(frozen=True)
class GitHubRung:
    owner: str
    repo: str
    path: str


PublisherHistoryRung: TypeAlias = MediaWikiRung | GitHubRung

_RungResult: TypeAlias = (
    ArchiveOrgCaptureResult
    | ArchiveTodayCaptureResult
    | PublisherHistoryCaptureResult
    | None
)


@dataclass(frozen=True)
class RungOutcome:
    """One archive rung's neutral mechanical outcome (INV-1: facts, not judgment).

    ``rung`` is the fixed rung label (``wayback`` | ``archive_today`` | ``publisher_history:<kind>``).
    ``located`` is whether a pre-cutoff memento/revision was found. ``verified_body`` is whether a
    pre-cutoff body was retrieved AND passed that rung's verification. ``selected_timestamp`` is the
    selected memento/revision's served timestamp in the rung's native form (14-digit for the general
    archives, ISO-8601 for publisher-history). ``locate_detail`` / ``body_detail`` are factual
    descriptions of what happened (no quality verdict). ``result`` is the raw adapter result a runner
    translates into a packet. ``gate_defeat_stop`` records an honored no-gate-defeat STOP, if any.
    """

    rung: str
    located: bool
    verified_body: bool
    selected_timestamp: str | None
    locate_detail: str
    body_detail: str
    result: _RungResult = None
    gate_defeat_stop: str | None = None


@dataclass(frozen=True)
class HistoricalCaptureResult:
    """The bundled cross-archive locate result.

    ``archives_tried`` is the ordered list of rungs actually attempted (the ladder stops after the
    first verified body, so later rungs are not attempted and not listed). ``archive_selected`` is
    the rung that produced the verified pre-cutoff body, or ``None`` for an honest NO-GO after the
    bounded ladder. ``selected_outcome`` is that rung's outcome (or ``None``). All are neutral facts.
    """

    original_url: str
    cutoff_timestamp_iso: str | None
    archives_tried: list[RungOutcome]
    archive_selected: str | None
    selected_outcome: RungOutcome | None = None


def fetch_historical_capture(
    *,
    original_url: str,
    cutoff_timestamp_iso: str | None = None,
    include_archive_today: bool = True,
    publisher_history_rung: PublisherHistoryRung | None = None,
    wayback_cdx_endpoint: str = DEFAULT_CDX_ENDPOINT,
    wayback_snapshot_base_url: str = DEFAULT_SNAPSHOT_BASE_URL,
    archive_today_timemap_base_url: str = DEFAULT_TIMEMAP_BASE_URL,
    archive_today_hosts: frozenset[str] | None = None,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
    max_bytes: int = DEFAULT_MAX_BYTES,
    max_attempts: int = DEFAULT_MAX_ATTEMPTS,
    retry_backoff_seconds: float = DEFAULT_RETRY_BACKOFF_SECONDS,
) -> HistoricalCaptureResult:
    """Run the bounded cross-archive locate ladder, stopping at the first verified pre-cutoff body."""
    normalized_original_url = original_url
    cutoff_iso: str | None = None
    cutoff_wayback: str | None = None
    if cutoff_timestamp_iso is not None:
        cutoff_dt = _parse_iso8601(cutoff_timestamp_iso)
        cutoff_iso = cutoff_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        cutoff_wayback = cutoff_dt.strftime("%Y%m%d%H%M%S")

    archives_tried: list[RungOutcome] = []
    selected: RungOutcome | None = None

    # Rung 1: Wayback (primary general archive).
    wayback_result = fetch_archive_org_capture(
        original_url=normalized_original_url,
        cutoff_timestamp=cutoff_wayback,
        cdx_endpoint=wayback_cdx_endpoint,
        snapshot_base_url=wayback_snapshot_base_url,
        timeout_seconds=timeout_seconds,
        max_bytes=max_bytes,
        max_attempts=max_attempts,
        retry_backoff_seconds=retry_backoff_seconds,
    )
    wayback_outcome = _wayback_outcome(wayback_result)
    archives_tried.append(wayback_outcome)
    if wayback_outcome.verified_body:
        selected = wayback_outcome

    # Rung 2: archive.today (second general archive -- closes the brand/retailer SPOF).
    if selected is None and include_archive_today:
        archive_today_kwargs: dict[str, object] = {}
        if archive_today_hosts is not None:
            archive_today_kwargs["archive_today_hosts"] = archive_today_hosts
        archive_today_result = fetch_archive_today_capture(
            original_url=normalized_original_url,
            cutoff_timestamp=cutoff_wayback,
            timemap_base_url=archive_today_timemap_base_url,
            timeout_seconds=timeout_seconds,
            max_bytes=max_bytes,
            max_attempts=max_attempts,
            retry_backoff_seconds=retry_backoff_seconds,
            **archive_today_kwargs,  # type: ignore[arg-type]
        )
        archive_today_outcome = _archive_today_outcome(archive_today_result)
        archives_tried.append(archive_today_outcome)
        if archive_today_outcome.verified_body:
            selected = archive_today_outcome

    # Rung 3: publisher version-history (conditional, opt-in).
    if selected is None and publisher_history_rung is not None:
        publisher_outcome = _run_publisher_history(
            publisher_history_rung,
            cutoff_iso=cutoff_iso,
            timeout_seconds=timeout_seconds,
            max_bytes=max_bytes,
        )
        archives_tried.append(publisher_outcome)
        if publisher_outcome.verified_body:
            selected = publisher_outcome

    return HistoricalCaptureResult(
        original_url=normalized_original_url,
        cutoff_timestamp_iso=cutoff_iso,
        archives_tried=archives_tried,
        archive_selected=selected.rung if selected is not None else None,
        selected_outcome=selected,
    )


# --------------------------------------------------------------------------------------------------
# Per-rung extractors -- each contains its own branching (no fake uniform protocol)
# --------------------------------------------------------------------------------------------------


def _wayback_outcome(result: ArchiveOrgCaptureResult) -> RungOutcome:
    rung = "wayback"
    if isinstance(result, ArchiveOrgCaptureFailure):
        return RungOutcome(
            rung=rung,
            located=False,
            verified_body=False,
            selected_timestamp=None,
            locate_detail=f"availability lookup failed: {result.availability_result.message}",
            body_detail="not attempted (availability failed)",
            result=result,
        )
    assert isinstance(result, ArchiveOrgCaptureSuccess)
    selected = result.selected_snapshot
    if selected is None:
        return RungOutcome(
            rung=rung,
            located=False,
            verified_body=False,
            selected_timestamp=None,
            locate_detail="no pre-cutoff snapshot located",
            body_detail="not attempted (no snapshot)",
            result=result,
        )
    timestamp = selected.timestamp
    verification = result.body_verification
    status_failure = _direct_http_status_failure(result.body_result)
    if (
        isinstance(result.body_result, DirectHttpCaptureSuccess)
        and status_failure is None
        and verification is not None
        and verification.ok
    ):
        return RungOutcome(
            rung=rung,
            located=True,
            verified_body=True,
            selected_timestamp=timestamp,
            locate_detail=f"located pre-cutoff snapshot {timestamp}",
            body_detail=f"verified body served at {verification.served_timestamp or timestamp}",
            result=result,
        )
    return RungOutcome(
        rung=rung,
        located=True,
        verified_body=False,
        selected_timestamp=timestamp,
        locate_detail=f"located pre-cutoff snapshot {timestamp}",
        body_detail=_archive_body_detail(
            result.body_result, verification_reason=status_failure or _verification_reason(verification)
        ),
        result=result,
    )


def _archive_today_outcome(result: ArchiveTodayCaptureResult) -> RungOutcome:
    rung = "archive_today"
    if isinstance(result, ArchiveTodayCaptureFailure):
        gate_defeat = result.gate_defeat_stop
        locate_detail = (
            f"gate-defeat STOP on TimeMap: {gate_defeat}"
            if gate_defeat is not None
            else "TimeMap lookup failed or returned no usable listing"
        )
        return RungOutcome(
            rung=rung,
            located=False,
            verified_body=False,
            selected_timestamp=None,
            locate_detail=locate_detail,
            body_detail="not attempted",
            result=result,
            gate_defeat_stop=gate_defeat,
        )
    assert isinstance(result, ArchiveTodayCaptureSuccess)
    selected = result.selected_memento
    if selected is None:
        return RungOutcome(
            rung=rung,
            located=False,
            verified_body=False,
            selected_timestamp=None,
            locate_detail="no pre-cutoff memento located",
            body_detail="not attempted (no memento)",
            result=result,
        )
    timestamp = selected.timestamp
    if result.gate_defeat_stop is not None:
        return RungOutcome(
            rung=rung,
            located=True,
            verified_body=False,
            selected_timestamp=timestamp,
            locate_detail=f"located pre-cutoff memento {timestamp}",
            body_detail=f"gate-defeat STOP on body fetch: {result.gate_defeat_stop}",
            result=result,
            gate_defeat_stop=result.gate_defeat_stop,
        )
    verification = result.body_verification
    status_failure = _direct_http_status_failure(result.body_result)
    if (
        isinstance(result.body_result, DirectHttpCaptureSuccess)
        and status_failure is None
        and verification is not None
        and verification.ok
    ):
        return RungOutcome(
            rung=rung,
            located=True,
            verified_body=True,
            selected_timestamp=timestamp,
            locate_detail=f"located pre-cutoff memento {timestamp}",
            body_detail=f"verified body served at {verification.served_timestamp or timestamp}",
            result=result,
        )
    return RungOutcome(
        rung=rung,
        located=True,
        verified_body=False,
        selected_timestamp=timestamp,
        locate_detail=f"located pre-cutoff memento {timestamp}",
        body_detail=_archive_body_detail(
            result.body_result, verification_reason=status_failure or _verification_reason(verification)
        ),
        result=result,
    )


def _run_publisher_history(
    rung: PublisherHistoryRung,
    *,
    cutoff_iso: str | None,
    timeout_seconds: float,
    max_bytes: int,
) -> RungOutcome:
    if cutoff_iso is None:
        # publisher-history selection is defined relative to a cutoff; without one there is nothing
        # to locate "at or before". Record an honest skip rather than guessing a cutoff.
        return RungOutcome(
            rung="publisher_history",
            located=False,
            verified_body=False,
            selected_timestamp=None,
            locate_detail="skipped: publisher-history rung requires a cutoff timestamp",
            body_detail="not attempted",
            result=None,
        )
    if isinstance(rung, MediaWikiRung):
        result = fetch_mediawiki_history_capture(
            wiki_api_base=rung.wiki_api_base,
            title=rung.title,
            cutoff_timestamp=cutoff_iso,
            timeout_seconds=timeout_seconds,
            max_bytes=max_bytes,
        )
        return _publisher_history_outcome(result, kind="mediawiki")
    if isinstance(rung, GitHubRung):
        result = fetch_github_history_capture(
            owner=rung.owner,
            repo=rung.repo,
            path=rung.path,
            cutoff_timestamp=cutoff_iso,
            timeout_seconds=timeout_seconds,
            max_bytes=max_bytes,
        )
        return _publisher_history_outcome(result, kind="github")
    raise TypeError(f"unsupported publisher-history rung: {type(rung).__name__}")


def _publisher_history_outcome(result: PublisherHistoryCaptureResult, *, kind: str) -> RungOutcome:
    rung = f"publisher_history:{kind}"
    if isinstance(result, PublisherHistoryCaptureFailure):
        return RungOutcome(
            rung=rung,
            located=False,
            verified_body=False,
            selected_timestamp=None,
            locate_detail=f"history listing failed: {result.listing_result.message}",
            body_detail="not attempted (listing failed)",
            result=result,
        )
    assert isinstance(result, PublisherHistoryCaptureSuccess)
    selected = result.selected_revision
    if selected is None:
        return RungOutcome(
            rung=rung,
            located=False,
            verified_body=False,
            selected_timestamp=None,
            locate_detail=result.selection_warning or "no pre-cutoff revision located",
            body_detail="not attempted (no revision)",
            result=result,
        )
    timestamp = selected.served_timestamp
    # publisher-history folds body verification inline: a Success body_result already passed the
    # rung's identity + timestamp checks (PH-01/PH-02), so it IS the verified body. A Failure
    # body_result is the PARTIAL outcome (located, body not usable).
    if isinstance(result.body_result, DirectHttpCaptureSuccess):
        return RungOutcome(
            rung=rung,
            located=True,
            verified_body=True,
            selected_timestamp=timestamp,
            locate_detail=f"located pre-cutoff revision {selected.identity} served {timestamp}",
            body_detail="verified body (publisher-history identity+timestamp bound)",
            result=result,
        )
    body_detail = "body not retrieved"
    if isinstance(result.body_result, DirectHttpCaptureFailure):
        body_detail = f"body not usable: {result.body_result.message}"
    return RungOutcome(
        rung=rung,
        located=True,
        verified_body=False,
        selected_timestamp=timestamp,
        locate_detail=f"located pre-cutoff revision {selected.identity} served {timestamp}",
        body_detail=body_detail,
        result=result,
    )


# --------------------------------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------------------------------


def _verification_reason(verification: object) -> str | None:
    return getattr(verification, "reason", None)


def _direct_http_status_failure(
    body_result: DirectHttpCaptureSuccess | DirectHttpCaptureFailure | None,
) -> str | None:
    if not isinstance(body_result, DirectHttpCaptureSuccess):
        return None
    if 200 <= body_result.status < 300:
        return None
    return f"body HTTP {body_result.status} {body_result.reason or 'without reason'} is not usable"


def _archive_body_detail(
    body_result: DirectHttpCaptureSuccess | DirectHttpCaptureFailure | None,
    *,
    verification_reason: str | None,
) -> str:
    if body_result is None:
        return "body not attempted"
    if isinstance(body_result, DirectHttpCaptureFailure):
        return f"body not usable: {body_result.message}"
    if verification_reason is not None:
        return f"body retrieved but verification failed: {verification_reason}"
    return "body retrieved but not verified"


def _parse_iso8601(value: str) -> datetime:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("cutoff_timestamp_iso must be a non-empty ISO-8601 string")
    text = value.strip()
    if text.endswith("Z"):
        text = f"{text[:-1]}+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError as exc:
        raise ValueError(f"cutoff_timestamp_iso must be an ISO-8601 timestamp; got {value!r}") from exc
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)
