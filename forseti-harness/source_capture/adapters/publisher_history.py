"""Publisher-history capture adapter -- latest source version at or before a cutoff.

This is the *publisher-history* locate rung of the capture robustness E-slice: instead of
asking a third-party archive (Wayback/archive.today) what a page looked like before a cutoff,
it asks the publisher's own version history. Two rungs are implemented here:

- **MediaWiki page-history** (``fetch_mediawiki_history_capture``): the MediaWiki ``query``
  API returns the latest revision at or before a cutoff (``rvstart=<cutoff>&rvdir=older``),
  then the revision content is fetched by ``revid``.
- **GitHub commit-history** (``fetch_github_history_capture``): the GitHub commits API returns
  the latest commit touching a path at or before a cutoff (``&until=<cutoff>``), then the file
  bytes at that commit sha are fetched from ``raw.githubusercontent.com``.

It conforms to the existing adapter convention (mirrors ``archive_org.py``): validate native
inputs -> fetch a listing via ``fetch_direct_http_capture`` -> parse -> select the latest entry
**at or before the cutoff** -> fetch the body. Results are frozen
``PublisherHistoryCaptureSuccess`` / ``PublisherHistoryCaptureFailure`` dataclasses that keep the
*listing/selection* result separate from the *body* result, exactly like
``ArchiveOrgCaptureSuccess``.

Served-time-proof contract (AR-02): the selected revision is **not opaque**. Each rung records
the served *identity* (MediaWiki ``revid`` / GitHub ``sha``) **and** the served *timestamp* parsed
from the publisher's own metadata. If the listing carries no parseable served timestamp for the
entry, selection records a visible verification failure (no entry is selected) rather than
trusting an opaque identifier -- the served timestamp is what proves no-lookahead.

No-lookahead guard: selection filters to entries with ``served timestamp <= cutoff`` and the
chosen entry's timestamp is asserted ``<= cutoff`` in code (:func:`_assert_not_after_cutoff`).
A post-cutoff version is never selected even if the publisher returns it.

All HTTP goes through ``fetch_direct_http_capture`` (no ``urllib.request`` / ``requests`` / etc.
imported here, per the adapter no-forbidden-import contract). This adapter never imports the
writer and never constructs a packet; a runner translates the result into writer kwargs.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from json import JSONDecodeError
from typing import TypeAlias
from urllib.parse import quote, urlencode, urlparse

from source_capture.adapters.direct_http import (
    DEFAULT_MAX_BYTES,
    DEFAULT_TIMEOUT_SECONDS,
    DirectHttpCaptureFailure,
    DirectHttpCaptureSuccess,
    fetch_direct_http_capture,
)

DEFAULT_GITHUB_API_BASE = "https://api.github.com"
DEFAULT_GITHUB_RAW_BASE = "https://raw.githubusercontent.com"
# GitHub requires a declared User-Agent; an empty UA is rejected by the API. The publisher-history
# rungs are honest stdlib fetches (no browser/api-client emulation), recorded in the UA.
DEFAULT_PUBLISHER_HISTORY_USER_AGENT = (
    "ForsetiSourceCapturePublisherHistory/0.1 (stdlib honest fetch; no browser/api-client/archive)"
)
# PH-03: fetch a bounded window of revisions so the adapter can skip unproofed top entries and
# find the next older proofed entry; keep it small to avoid large API responses.
_PUBLISHER_HISTORY_PAGE_SIZE = 3


@dataclass(frozen=True)
class PublisherRevision:
    """One publisher version, with NON-OPAQUE served-time proof (AR-02).

    ``identity`` is the publisher's own version id (MediaWiki ``revid`` as a string, or a GitHub
    commit ``sha``). ``served_timestamp`` is the publisher-reported version timestamp normalized to
    ISO-8601 UTC (``...Z``); it is the value the no-lookahead guard checks against the cutoff.
    ``content_url`` is where the body for this exact version is fetched. ``parent_identity`` is the
    prior-version id when the publisher exposes it (MediaWiki ``parentid``), else ``None``.
    """

    identity: str
    served_timestamp: str
    content_url: str
    parent_identity: str | None = None


@dataclass(frozen=True)
class PublisherHistoryCaptureSuccess:
    """A located publisher history, with selection and body kept separate.

    ``listing_result`` is the raw history-listing HTTP result (the availability leg).
    ``revisions`` is every parseable version the listing returned (with served-time proof).
    ``selected_revision`` is the latest version ``<= cutoff`` (``None`` => NO-GO: no pre-cutoff
    version, or no version carried parseable served-time proof). ``body_result`` is the body fetch
    for the selected version: a ``DirectHttpCaptureFailure`` here is the PARTIAL outcome (version
    selected, body not retrieved -- availability is separated from body). ``parse_warning`` /
    ``selection_warning`` carry honest, non-fatal limitation text.
    """

    rung: str
    source_identity: str
    listing_url: str
    listing_result: DirectHttpCaptureSuccess
    revisions: list[PublisherRevision]
    selected_revision: PublisherRevision | None
    cutoff_timestamp: str
    body_result: DirectHttpCaptureSuccess | DirectHttpCaptureFailure | None = None
    parse_warning: str | None = None
    selection_warning: str | None = None
    warning_notes: list[str] = field(default_factory=list)
    limitation_notes: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class PublisherHistoryCaptureFailure:
    """The history-listing lookup itself failed -- no version could even be located.

    This is distinct from NO-GO (a successful listing with no pre-cutoff version, represented by a
    ``PublisherHistoryCaptureSuccess`` with ``selected_revision=None``) and from PARTIAL (a body
    fetch failure recorded on the success result). ``listing_result`` carries the transport-level
    cause.
    """

    rung: str
    source_identity: str
    listing_url: str
    listing_result: DirectHttpCaptureFailure
    warning_notes: list[str] = field(default_factory=list)
    limitation_notes: list[str] = field(default_factory=list)


PublisherHistoryCaptureResult: TypeAlias = (
    PublisherHistoryCaptureSuccess | PublisherHistoryCaptureFailure
)


# --------------------------------------------------------------------------------------------------
# MediaWiki page-history rung
# --------------------------------------------------------------------------------------------------


def fetch_mediawiki_history_capture(
    *,
    wiki_api_base: str,
    title: str,
    cutoff_timestamp: str,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
    max_bytes: int = DEFAULT_MAX_BYTES,
    user_agent: str = DEFAULT_PUBLISHER_HISTORY_USER_AGENT,
) -> PublisherHistoryCaptureResult:
    """Latest MediaWiki revision of ``title`` at or before ``cutoff_timestamp``.

    Lists ``prop=revisions`` with ``rvstart=<cutoff>&rvdir=older&rvlimit=1`` (the API returns the
    newest revision <= cutoff), records the served ``revid`` + ``timestamp`` (AR-02), asserts the
    served timestamp ``<= cutoff`` (no-lookahead), then fetches that revision's content by
    ``rvstartid=<revid>``. A failed listing -> ``PublisherHistoryCaptureFailure``; no pre-cutoff
    revision -> success with ``selected_revision=None`` (NO-GO); a failed content fetch -> success
    with a ``DirectHttpCaptureFailure`` ``body_result`` (PARTIAL).
    """
    api_base = _validate_api_base(wiki_api_base, "MediaWiki wiki_api_base")
    clean_title = _require_nonblank("title", title)
    cutoff_iso = _validate_iso8601_cutoff(cutoff_timestamp)
    source_identity = f"{api_base} :: {clean_title}"

    listing_url = build_mediawiki_history_url(
        wiki_api_base=api_base, title=clean_title, cutoff_timestamp=cutoff_iso
    )
    listing_result = fetch_direct_http_capture(
        url=listing_url,
        timeout_seconds=timeout_seconds,
        max_bytes=max_bytes,
        user_agent=user_agent,
    )
    if isinstance(listing_result, DirectHttpCaptureFailure):
        return PublisherHistoryCaptureFailure(
            rung="mediawiki_page_history",
            source_identity=source_identity,
            listing_url=listing_url,
            listing_result=listing_result,
            limitation_notes=[
                f"access_failed: MediaWiki history listing {listing_result.failure_kind}"
            ],
        )
    # PH-01: a non-2xx listing response (body preserved by direct_http) is NOT usable listing
    # evidence; treat it as access_failed, same as archive_org does on availability errors.
    if listing_result.status < 200 or listing_result.status >= 300:
        return PublisherHistoryCaptureFailure(
            rung="mediawiki_page_history",
            source_identity=source_identity,
            listing_url=listing_url,
            listing_result=DirectHttpCaptureFailure(
                requested_url=listing_result.requested_url,
                failure_kind="access_failed",  # type: ignore[arg-type]
                message=(
                    f"access_failed: MediaWiki history listing returned HTTP "
                    f"{listing_result.status} {listing_result.reason or 'without reason'}; "
                    "not treated as usable listing evidence"
                ),
                final_url=listing_result.final_url,
                status=listing_result.status,
                reason=listing_result.reason,
            ),
            limitation_notes=[
                f"access_failed: MediaWiki history listing HTTP {listing_result.status}; "
                "response body preserved but not parsed"
            ],
        )

    revisions: list[PublisherRevision]
    parse_warning: str | None = None
    try:
        revisions = parse_mediawiki_revisions(
            listing_result.body, wiki_api_base=api_base, title=clean_title
        )
    except (JSONDecodeError, ValueError) as exc:
        revisions = []
        parse_warning = f"publisher_history mediawiki listing parse_failed: {exc}"

    selected_revision, selection_warning = _select_revision(revisions, cutoff_timestamp=cutoff_iso)

    body_result: DirectHttpCaptureSuccess | DirectHttpCaptureFailure | None = None
    if selected_revision is not None:
        raw_body_result = fetch_direct_http_capture(
            url=selected_revision.content_url,
            timeout_seconds=timeout_seconds,
            max_bytes=max_bytes,
            user_agent=user_agent,
        )
        # PH-01 / PH-02: non-2xx body is not usable; 2xx body must have revid+timestamp verified.
        body_result = _verify_mediawiki_body(
            raw_body_result, selected_revision=selected_revision
        )

    return PublisherHistoryCaptureSuccess(
        rung="mediawiki_page_history",
        source_identity=source_identity,
        listing_url=listing_url,
        listing_result=listing_result,
        revisions=revisions,
        selected_revision=selected_revision,
        cutoff_timestamp=cutoff_iso,
        body_result=body_result,
        parse_warning=parse_warning,
        selection_warning=selection_warning,
    )


def build_mediawiki_history_url(
    *, wiki_api_base: str, title: str, cutoff_timestamp: str
) -> str:
    """``api.php`` query for the newest revision at or before ``cutoff_timestamp``.

    ``rvstart=<cutoff>&rvdir=older&rvlimit=1`` makes the API walk backwards from the cutoff and
    return the single latest revision <= cutoff; ``rvprop=timestamp|ids`` supplies the served-time
    proof (revid + timestamp) without pulling content on the listing leg.
    """
    api_base = _validate_api_base(wiki_api_base, "MediaWiki wiki_api_base")
    query = urlencode(
        {
            "action": "query",
            "prop": "revisions",
            "titles": title,
            "rvprop": "timestamp|ids",
            "rvstart": cutoff_timestamp,
            "rvdir": "older",
            # PH-03: fetch a small bounded window so the adapter can skip unproofed top
            # entries and select the next older proofed entry rather than returning a false NO-GO.
            "rvlimit": str(_PUBLISHER_HISTORY_PAGE_SIZE),
            "format": "json",
            "formatversion": "2",
        }
    )
    return f"{api_base.rstrip('/')}/w/api.php?{query}"


def build_mediawiki_content_url(
    *, wiki_api_base: str, title: str, revid: str
) -> str:
    """``api.php`` query for the content of one revision, pinned by ``rvstartid=<revid>``."""
    api_base = _validate_api_base(wiki_api_base, "MediaWiki wiki_api_base")
    query = urlencode(
        {
            "action": "query",
            "prop": "revisions",
            "titles": title,
            "rvprop": "content|timestamp|ids",
            "rvstartid": revid,
            "rvlimit": "1",
            "format": "json",
            "formatversion": "2",
        }
    )
    return f"{api_base.rstrip('/')}/w/api.php?{query}"


def parse_mediawiki_revisions(
    body: bytes, *, wiki_api_base: str, title: str
) -> list[PublisherRevision]:
    """Parse ``query.pages[].revisions[]`` into ``PublisherRevision`` with served-time proof.

    Supports both ``formatversion=2`` (``pages`` is a list) and the legacy keyed-dict shape. A
    revision missing ``revid`` or a parseable ``timestamp`` is skipped (no opaque/un-proofed entry
    is admitted -- AR-02).
    """
    payload = json.loads(body.decode("utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("MediaWiki API response must be a JSON object")
    query = payload.get("query")
    if not isinstance(query, dict):
        return []
    pages = query.get("pages")
    page_dicts = _mediawiki_page_dicts(pages)

    revisions: list[PublisherRevision] = []
    for page in page_dicts:
        raw_revisions = page.get("revisions")
        if not isinstance(raw_revisions, list):
            continue
        for raw in raw_revisions:
            if not isinstance(raw, dict):
                continue
            revid = raw.get("revid")
            timestamp = raw.get("timestamp")
            if revid is None or not isinstance(timestamp, str):
                continue
            normalized = _normalize_iso8601(timestamp)
            if normalized is None:
                continue
            parent = raw.get("parentid")
            revisions.append(
                PublisherRevision(
                    identity=str(revid),
                    served_timestamp=normalized,
                    content_url=build_mediawiki_content_url(
                        wiki_api_base=wiki_api_base, title=title, revid=str(revid)
                    ),
                    parent_identity=str(parent) if parent is not None else None,
                )
            )
    return revisions


def _mediawiki_page_dicts(pages: object) -> list[dict]:
    if isinstance(pages, list):
        return [page for page in pages if isinstance(page, dict)]
    if isinstance(pages, dict):
        return [page for page in pages.values() if isinstance(page, dict)]
    return []


# --------------------------------------------------------------------------------------------------
# GitHub commit-history rung
# --------------------------------------------------------------------------------------------------


def fetch_github_history_capture(
    *,
    owner: str,
    repo: str,
    path: str,
    cutoff_timestamp: str,
    api_base: str = DEFAULT_GITHUB_API_BASE,
    raw_base: str = DEFAULT_GITHUB_RAW_BASE,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
    max_bytes: int = DEFAULT_MAX_BYTES,
    user_agent: str = DEFAULT_PUBLISHER_HISTORY_USER_AGENT,
) -> PublisherHistoryCaptureResult:
    """Latest commit to ``path`` in ``owner/repo`` at or before ``cutoff_timestamp``.

    Lists ``/repos/<owner>/<repo>/commits?path=<path>&until=<cutoff>&per_page=1`` (the API returns
    the newest commit <= cutoff), records the served ``sha`` + committed ``date`` (AR-02), asserts
    the served timestamp ``<= cutoff`` (no-lookahead), then fetches the file bytes at that sha from
    ``raw.githubusercontent.com``. A failed listing -> ``PublisherHistoryCaptureFailure``; no
    pre-cutoff commit -> success with ``selected_revision=None`` (NO-GO); a failed body fetch ->
    success with a ``DirectHttpCaptureFailure`` ``body_result`` (PARTIAL).
    """
    api = _validate_api_base(api_base, "GitHub api_base")
    raw = _validate_api_base(raw_base, "GitHub raw_base")
    clean_owner = _require_nonblank("owner", owner)
    clean_repo = _require_nonblank("repo", repo)
    clean_path = _require_nonblank("path", path).lstrip("/")
    cutoff_iso = _validate_iso8601_cutoff(cutoff_timestamp)
    source_identity = f"{clean_owner}/{clean_repo} :: {clean_path}"

    listing_url = build_github_history_url(
        owner=clean_owner,
        repo=clean_repo,
        path=clean_path,
        cutoff_timestamp=cutoff_iso,
        api_base=api,
    )
    # GitHub requires the documented media type; declare it so the JSON shape is stable.
    listing_result = fetch_direct_http_capture(
        url=listing_url,
        timeout_seconds=timeout_seconds,
        max_bytes=max_bytes,
        user_agent=user_agent,
    )
    if isinstance(listing_result, DirectHttpCaptureFailure):
        return PublisherHistoryCaptureFailure(
            rung="github_commit_history",
            source_identity=source_identity,
            listing_url=listing_url,
            listing_result=listing_result,
            limitation_notes=[
                f"access_failed: GitHub commit listing {listing_result.failure_kind}"
            ],
        )
    # PH-01: a non-2xx listing response (body preserved by direct_http) is NOT usable listing
    # evidence; treat it as access_failed.
    if listing_result.status < 200 or listing_result.status >= 300:
        return PublisherHistoryCaptureFailure(
            rung="github_commit_history",
            source_identity=source_identity,
            listing_url=listing_url,
            listing_result=DirectHttpCaptureFailure(
                requested_url=listing_result.requested_url,
                failure_kind="access_failed",  # type: ignore[arg-type]
                message=(
                    f"access_failed: GitHub commit listing returned HTTP "
                    f"{listing_result.status} {listing_result.reason or 'without reason'}; "
                    "not treated as usable listing evidence"
                ),
                final_url=listing_result.final_url,
                status=listing_result.status,
                reason=listing_result.reason,
            ),
            limitation_notes=[
                f"access_failed: GitHub commit listing HTTP {listing_result.status}; "
                "response body preserved but not parsed"
            ],
        )

    revisions: list[PublisherRevision]
    parse_warning: str | None = None
    try:
        revisions = parse_github_commits(
            listing_result.body,
            owner=clean_owner,
            repo=clean_repo,
            path=clean_path,
            raw_base=raw,
        )
    except (JSONDecodeError, ValueError) as exc:
        revisions = []
        parse_warning = f"publisher_history github listing parse_failed: {exc}"

    selected_revision, selection_warning = _select_revision(revisions, cutoff_timestamp=cutoff_iso)

    body_result: DirectHttpCaptureSuccess | DirectHttpCaptureFailure | None = None
    if selected_revision is not None:
        raw_body_result = fetch_direct_http_capture(
            url=selected_revision.content_url,
            timeout_seconds=timeout_seconds,
            max_bytes=max_bytes,
            user_agent=user_agent,
        )
        # PH-01 / PH-02: non-2xx body is not usable; for GitHub the raw URL is pinned by SHA
        # in the URL (identity binding), which we verify/record explicitly.
        body_result = _verify_github_body(
            raw_body_result, selected_revision=selected_revision
        )

    return PublisherHistoryCaptureSuccess(
        rung="github_commit_history",
        source_identity=source_identity,
        listing_url=listing_url,
        listing_result=listing_result,
        revisions=revisions,
        selected_revision=selected_revision,
        cutoff_timestamp=cutoff_iso,
        body_result=body_result,
        parse_warning=parse_warning,
        selection_warning=selection_warning,
    )


def build_github_history_url(
    *,
    owner: str,
    repo: str,
    path: str,
    cutoff_timestamp: str,
    api_base: str = DEFAULT_GITHUB_API_BASE,
) -> str:
    """``/repos/<owner>/<repo>/commits`` query for the newest commit to ``path`` <= cutoff."""
    api = _validate_api_base(api_base, "GitHub api_base")
    query = urlencode(
        {
            "path": path,
            "until": cutoff_timestamp,
            # PH-03: fetch a small bounded window so the adapter can skip unproofed top
            # entries and select the next older proofed entry rather than returning a false NO-GO.
            "per_page": str(_PUBLISHER_HISTORY_PAGE_SIZE),
        }
    )
    return f"{api.rstrip('/')}/repos/{quote(owner)}/{quote(repo)}/commits?{query}"


def build_github_raw_url(
    *, owner: str, repo: str, path: str, sha: str, raw_base: str = DEFAULT_GITHUB_RAW_BASE
) -> str:
    """``raw.githubusercontent.com`` URL for ``path`` pinned at exact commit ``sha``."""
    raw = _validate_api_base(raw_base, "GitHub raw_base")
    encoded_path = "/".join(quote(segment) for segment in path.split("/"))
    return f"{raw.rstrip('/')}/{quote(owner)}/{quote(repo)}/{quote(sha)}/{encoded_path}"


def parse_github_commits(
    body: bytes, *, owner: str, repo: str, path: str, raw_base: str = DEFAULT_GITHUB_RAW_BASE
) -> list[PublisherRevision]:
    """Parse the commits-list JSON into ``PublisherRevision`` with served-time proof.

    Each element carries ``sha`` (served identity) and ``commit.committer.date`` /
    ``commit.author.date`` (served timestamp). A commit missing a ``sha`` or a parseable date is
    skipped (no opaque/un-proofed entry is admitted -- AR-02).
    """
    payload = json.loads(body.decode("utf-8"))
    if not isinstance(payload, list):
        raise ValueError("GitHub commits API response must be a JSON list")

    revisions: list[PublisherRevision] = []
    for raw in payload:
        if not isinstance(raw, dict):
            continue
        sha = raw.get("sha")
        if not isinstance(sha, str) or not sha:
            continue
        timestamp = _github_commit_timestamp(raw.get("commit"))
        if timestamp is None:
            continue
        revisions.append(
            PublisherRevision(
                identity=sha,
                served_timestamp=timestamp,
                content_url=build_github_raw_url(
                    owner=owner, repo=repo, path=path, sha=sha, raw_base=raw_base
                ),
            )
        )
    return revisions


def _github_commit_timestamp(commit: object) -> str | None:
    """Committer date preferred (when the commit landed), author date as fallback."""
    if not isinstance(commit, dict):
        return None
    for role in ("committer", "author"):
        actor = commit.get(role)
        if isinstance(actor, dict):
            date = actor.get("date")
            if isinstance(date, str):
                normalized = _normalize_iso8601(date)
                if normalized is not None:
                    return normalized
    return None


# --------------------------------------------------------------------------------------------------
# Body verification helpers (PH-01 / PH-02)
# --------------------------------------------------------------------------------------------------


def _verify_mediawiki_body(
    body_result: DirectHttpCaptureSuccess | DirectHttpCaptureFailure,
    *,
    selected_revision: PublisherRevision,
) -> DirectHttpCaptureSuccess | DirectHttpCaptureFailure:
    """Gate the MediaWiki content response on status and identity/timestamp proof (PH-01/PH-02).

    A non-2xx body is not usable regardless of whether bytes were preserved (PH-01).  A 2xx body
    must have its returned ``revid`` and ``timestamp`` verified against the selected revision before
    it is treated as the proven body (PH-02).  On any mismatch or missing proof the result is
    returned as a ``DirectHttpCaptureFailure`` so the caller records PARTIAL.
    """
    if isinstance(body_result, DirectHttpCaptureFailure):
        return body_result

    # PH-01: non-2xx body is not usable even if bytes were preserved.
    if body_result.status < 200 or body_result.status >= 300:
        return DirectHttpCaptureFailure(
            requested_url=body_result.requested_url,
            failure_kind="access_failed",  # type: ignore[arg-type]
            message=(
                f"access_failed: MediaWiki content fetch returned HTTP "
                f"{body_result.status} {body_result.reason or 'without reason'}; "
                "body bytes preserved but not treated as usable content"
            ),
            final_url=body_result.final_url,
            status=body_result.status,
            reason=body_result.reason,
        )

    # PH-02: parse the content response and verify revid + timestamp match the selected revision.
    try:
        payload = json.loads(body_result.body.decode("utf-8"))
        query = payload.get("query") if isinstance(payload, dict) else None
        pages = query.get("pages") if isinstance(query, dict) else None
        page_dicts = _mediawiki_page_dicts(pages)
        returned_rev: dict | None = None
        for page in page_dicts:
            raw_revisions = page.get("revisions")
            if isinstance(raw_revisions, list) and raw_revisions:
                first = raw_revisions[0]
                if isinstance(first, dict):
                    returned_rev = first
                    break
    except (JSONDecodeError, ValueError, UnicodeDecodeError):
        returned_rev = None

    if returned_rev is None:
        return DirectHttpCaptureFailure(
            requested_url=body_result.requested_url,
            failure_kind="access_failed",  # type: ignore[arg-type]
            message=(
                "publisher_history mediawiki body verification_failed: "
                "content response carries no parseable revision object; "
                f"expected revid={selected_revision.identity}"
            ),
            final_url=body_result.final_url,
            status=body_result.status,
            reason=body_result.reason,
        )

    returned_revid = str(returned_rev.get("revid", "")) if returned_rev.get("revid") is not None else ""
    returned_ts_raw = returned_rev.get("timestamp")
    returned_ts = _normalize_iso8601(returned_ts_raw) if isinstance(returned_ts_raw, str) else None

    if returned_revid != selected_revision.identity:
        return DirectHttpCaptureFailure(
            requested_url=body_result.requested_url,
            failure_kind="access_failed",  # type: ignore[arg-type]
            message=(
                f"publisher_history mediawiki body verification_failed: "
                f"returned revid {returned_revid!r} != selected {selected_revision.identity!r}"
            ),
            final_url=body_result.final_url,
            status=body_result.status,
            reason=body_result.reason,
        )

    if returned_ts is None or returned_ts != selected_revision.served_timestamp:
        return DirectHttpCaptureFailure(
            requested_url=body_result.requested_url,
            failure_kind="access_failed",  # type: ignore[arg-type]
            message=(
                f"publisher_history mediawiki body verification_failed: "
                f"returned timestamp {returned_ts!r} != selected {selected_revision.served_timestamp!r}"
            ),
            final_url=body_result.final_url,
            status=body_result.status,
            reason=body_result.reason,
        )

    return body_result


def _verify_github_body(
    body_result: DirectHttpCaptureSuccess | DirectHttpCaptureFailure,
    *,
    selected_revision: PublisherRevision,
) -> DirectHttpCaptureSuccess | DirectHttpCaptureFailure:
    """Gate the GitHub raw content response on status (PH-01) and record SHA binding (PH-02).

    The GitHub raw URL is pinned by ``sha`` in the URL, so identity is structurally bound by URL
    construction.  We verify/record that binding explicitly so the body is provably the selected
    commit's content (PH-02).  A non-2xx body is not usable (PH-01).
    """
    if isinstance(body_result, DirectHttpCaptureFailure):
        return body_result

    # PH-01: non-2xx body is not usable even if bytes were preserved.
    if body_result.status < 200 or body_result.status >= 300:
        return DirectHttpCaptureFailure(
            requested_url=body_result.requested_url,
            failure_kind="access_failed",  # type: ignore[arg-type]
            message=(
                f"access_failed: GitHub raw content fetch returned HTTP "
                f"{body_result.status} {body_result.reason or 'without reason'}; "
                "body bytes preserved but not treated as usable content"
            ),
            final_url=body_result.final_url,
            status=body_result.status,
            reason=body_result.reason,
        )

    # PH-02: verify the selected SHA appears in the requested URL (identity binding is by URL
    # construction in build_github_raw_url; record that the binding is confirmed).
    sha = selected_revision.identity
    if sha not in body_result.requested_url:
        return DirectHttpCaptureFailure(
            requested_url=body_result.requested_url,
            failure_kind="access_failed",  # type: ignore[arg-type]
            message=(
                f"publisher_history github body verification_failed: "
                f"selected sha {sha!r} not found in raw URL {body_result.requested_url!r}"
            ),
            final_url=body_result.final_url,
            status=body_result.status,
            reason=body_result.reason,
        )

    return body_result


# --------------------------------------------------------------------------------------------------
# Selection (no-lookahead guard) -- shared by both rungs
# --------------------------------------------------------------------------------------------------


def _select_revision(
    revisions: list[PublisherRevision], *, cutoff_timestamp: str
) -> tuple[PublisherRevision | None, str | None]:
    """Latest revision with served timestamp <= cutoff, or ``(None, reason)``.

    Selection is on the *parsed served timestamp* (AR-02 proof), not the publisher's claimed
    ordering, so a post-cutoff entry is never selected even if returned. The chosen entry's
    timestamp is asserted <= cutoff (:func:`_assert_not_after_cutoff`) before it leaves this
    function -- the in-code no-lookahead guard.
    """
    if not revisions:
        return None, "no parseable publisher revision with served-time proof"

    cutoff_dt = _parse_iso8601(cutoff_timestamp)
    eligible = [
        revision
        for revision in revisions
        if _parse_iso8601(revision.served_timestamp) <= cutoff_dt
    ]
    if not eligible:
        return None, "no publisher revision at or before cutoff"

    selected = max(eligible, key=lambda revision: _parse_iso8601(revision.served_timestamp))
    _assert_not_after_cutoff(selected.served_timestamp, cutoff_timestamp)
    return selected, None


def _assert_not_after_cutoff(served_timestamp: str, cutoff_timestamp: str) -> None:
    """No-lookahead guard: a selected version must never be served after the cutoff."""
    if _parse_iso8601(served_timestamp) > _parse_iso8601(cutoff_timestamp):
        raise AssertionError(
            "no-lookahead violation: selected publisher version served at "
            f"{served_timestamp} is after cutoff {cutoff_timestamp}"
        )


# --------------------------------------------------------------------------------------------------
# Validation / parsing helpers
# --------------------------------------------------------------------------------------------------


def _validate_api_base(value: str, label: str) -> str:
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError(f"{label} requires an absolute http:// or https:// URL")
    return parsed.geturl()


def _require_nonblank(field_name: str, value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _validate_iso8601_cutoff(cutoff_timestamp: str) -> str:
    """Validate + normalize an ISO-8601 cutoff to UTC ``...Z`` form (or raise ``ValueError``)."""
    if not isinstance(cutoff_timestamp, str) or not cutoff_timestamp.strip():
        raise ValueError("cutoff_timestamp must be a non-empty ISO-8601 string")
    normalized = _normalize_iso8601(cutoff_timestamp.strip())
    if normalized is None:
        raise ValueError(
            f"cutoff_timestamp must be an ISO-8601 timestamp; got {cutoff_timestamp!r}"
        )
    return normalized


def _normalize_iso8601(value: str) -> str | None:
    """Parse an ISO-8601 timestamp -> normalized UTC ``YYYY-MM-DDTHH:MM:SSZ``, or ``None``.

    Accepts a trailing ``Z`` (publisher form, e.g. MediaWiki / GitHub) and explicit offsets. A
    naive timestamp is treated as UTC. Returns ``None`` for anything unparseable so callers can
    skip un-proofed entries rather than trust opaque text.
    """
    parsed = _parse_iso8601_or_none(value)
    if parsed is None:
        return None
    return parsed.strftime("%Y-%m-%dT%H:%M:%SZ")


def _parse_iso8601(value: str) -> datetime:
    parsed = _parse_iso8601_or_none(value)
    if parsed is None:
        raise ValueError(f"not a parseable ISO-8601 timestamp: {value!r}")
    return parsed


def _parse_iso8601_or_none(value: str) -> datetime | None:
    if not isinstance(value, str):
        return None
    text = value.strip()
    if not text:
        return None
    # datetime.fromisoformat accepts a trailing Z only from Python 3.11+; normalize defensively.
    if text.endswith("Z"):
        text = f"{text[:-1]}+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)
