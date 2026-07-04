from __future__ import annotations

from html.parser import HTMLParser

from capture_spine.reddit_candidate_intake.models import (
    CandidateSubredditRow,
    CandidateSurface,
    CandidateThreadUrlRow,
    RedditCandidateIntakeError,
    RunEnvelope,
)
from capture_spine.reddit_candidate_intake.validation import (
    validate_old_reddit_html_listing_input_url,
    validate_old_reddit_thread_url,
    validate_run_envelope,
)


def project_old_reddit_html_listing(
    *,
    html_text: str,
    envelope: RunEnvelope,
    source_url: str,
    timestamp: str,
    source_surface: CandidateSurface = CandidateSurface.SUBREDDIT_LISTING,
    method_category: str | None = None,
) -> list[CandidateThreadUrlRow]:
    """Project old Reddit listing/search HTML into candidate thread rows only.

    Each row's ``subreddit`` is the thread's true home, parsed from the title
    anchor's target URL. For a link post (a listing entry whose title links to
    another thread), that target may live in a different subreddit than the
    declared listing; such rows are still captured and tagged with their real
    subreddit. This is honest provenance, not a ``no_subreddit_crawl`` breach:
    only the one declared page is read, never another subreddit's listing.
    """
    validate_run_envelope(envelope)
    source_subreddit = validate_old_reddit_html_listing_input_url(source_url)
    if source_surface not in envelope.candidate_surface_allowlist:
        raise RedditCandidateIntakeError(
            "undeclared_candidate_surface",
            "source_surface must be declared in candidate_surface_allowlist",
        )

    parser = _OldRedditListingParser()
    parser.feed(html_text)

    rows: list[CandidateThreadUrlRow] = []
    seen_urls: set[str] = set()
    query_or_seed = envelope.declared_topic_theme_query or source_subreddit
    row_method_category = method_category or envelope.method_category

    for href, title in parser.thread_links:
        candidate_url = _canonical_old_reddit_thread_url(href)
        if not candidate_url or candidate_url in seen_urls:
            continue
        subreddit, _thread_id = validate_old_reddit_thread_url(candidate_url)
        rows.append(
            CandidateThreadUrlRow(
                run_id=envelope.run_id,
                candidate_thread_url=candidate_url,
                subreddit=subreddit,
                source_surface=source_surface,
                query_or_seed=query_or_seed,
                timestamp=timestamp,
                method_category=row_method_category,
                visible_listing_title=title or None,
                exclusion_receipt=envelope.exclusions,
            )
        )
        seen_urls.add(candidate_url)
        if len(rows) >= envelope.max_threads_per_subreddit:
            break
    return rows


def project_old_reddit_html_candidate_subreddits(
    *,
    html_text: str,
    envelope: RunEnvelope,
    source_url: str,
    timestamp: str,
    source_surface: CandidateSurface = CandidateSurface.SEED_SUBREDDITS,
    method_category: str | None = None,
) -> list[CandidateSubredditRow]:
    """Project declared old Reddit subreddit surfaces into candidate subreddit rows."""
    validate_run_envelope(envelope)
    source_subreddit = validate_old_reddit_html_listing_input_url(source_url)
    if source_surface not in envelope.candidate_surface_allowlist:
        raise RedditCandidateIntakeError(
            "undeclared_candidate_surface",
            "source_surface must be declared in candidate_surface_allowlist",
        )

    parser = _OldRedditSubredditParser(
        source_surface=source_surface,
        source_subreddit=source_subreddit,
    )
    parser.feed(html_text)

    rows: list[CandidateSubredditRow] = []
    seen_subreddits: set[str] = set()
    query_or_seed = envelope.declared_topic_theme_query or source_subreddit
    row_method_category = method_category or envelope.method_category

    if source_surface == CandidateSurface.SEED_SUBREDDITS:
        candidates = [(source_subreddit, parser.visible_subscriber_count, parser.visible_active_user_count)]
    else:
        candidates = [
            (subreddit, None, None)
            for subreddit in parser.candidate_subreddits
        ]

    for subreddit, subscriber_count, active_user_count in candidates:
        if subreddit in seen_subreddits:
            continue
        absent_reason = None
        if subscriber_count is None and active_user_count is None:
            absent_reason = "visible_volume_not_present_on_declared_surface"
        rows.append(
            CandidateSubredditRow(
                run_id=envelope.run_id,
                candidate_subreddit=subreddit,
                source_surface=source_surface,
                source_url=f"https://old.reddit.com/r/{subreddit}/",
                query_or_seed=query_or_seed,
                timestamp=timestamp,
                method_category=row_method_category,
                exclusion_receipt=envelope.exclusions,
                visible_subscriber_count_or_none=subscriber_count,
                visible_active_user_count_or_none=active_user_count,
                visible_volume_signal_absent_reason_or_none=absent_reason,
            )
        )
        seen_subreddits.add(subreddit)
        if len(rows) >= envelope.max_subreddits:
            break
    return rows


class _OldRedditListingParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.thread_links: list[tuple[str, str]] = []
        self._current_href: str | None = None
        self._current_title_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        attr_map = {key: value or "" for key, value in attrs}
        href = attr_map.get("href", "")
        class_tokens = set(attr_map.get("class", "").split())
        if _is_candidate_title_anchor(class_tokens) and "/comments/" in href:
            self._current_href = href
            self._current_title_parts = []

    def handle_data(self, data: str) -> None:
        if self._current_href is not None:
            self._current_title_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag != "a" or self._current_href is None:
            return
        title = " ".join("".join(self._current_title_parts).split())
        self.thread_links.append((self._current_href, title))
        self._current_href = None
        self._current_title_parts = []


class _OldRedditSubredditParser(HTMLParser):
    _SURFACE_CLASS_TOKENS = {
        CandidateSurface.RELATED_SUBREDDIT: {"related-subreddits", "related-subreddit"},
        CandidateSurface.RECOMMENDATION: {"recommended-subreddits", "recommended-subreddit"},
        CandidateSurface.MORE_LIKE_THIS: {"more-like-this"},
        CandidateSurface.CROSS_POST: {"crosspost-subreddits", "crosspost-subreddit"},
        CandidateSurface.REDDIT_SEARCH_LISTING: {"subreddit-search-results", "search-subreddits"},
    }

    _VOID_TAGS = {
        "area",
        "base",
        "br",
        "col",
        "embed",
        "hr",
        "img",
        "input",
        "link",
        "meta",
        "param",
        "source",
        "track",
        "wbr",
    }

    def __init__(self, *, source_surface: CandidateSurface, source_subreddit: str) -> None:
        super().__init__(convert_charrefs=True)
        self.source_surface = source_surface
        self.source_subreddit = source_subreddit
        self.candidate_subreddits: list[str] = []
        self.visible_subscriber_count: str | None = None
        self.visible_active_user_count: str | None = None
        self._surface_depth = 0
        self._side_depth = 0
        self._titlebox_depth = 0
        self._sidebar_related_depth = 0
        self._users_online_depth = 0
        self._capturing_number_for: str | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {key: value or "" for key, value in attrs}
        class_tokens = set(attr_map.get("class", "").split())
        self._advance_region_depths(tag, class_tokens)
        if "users-online" in class_tokens:
            self._users_online_depth += 1
        elif self._users_online_depth and tag not in self._VOID_TAGS:
            self._users_online_depth += 1
        if tag == "span" and "number" in class_tokens and self._titlebox_depth:
            self._capturing_number_for = "active_users" if self._users_online_depth else "subscribers"
        if tag == "a" and self._candidate_subreddit_area_active():
            subreddit = _subreddit_name_from_url(attr_map.get("href", ""))
            if subreddit and subreddit.lower() != self.source_subreddit.lower():
                self.candidate_subreddits.append(subreddit)

    def handle_data(self, data: str) -> None:
        if self._capturing_number_for is None:
            return
        value = " ".join(data.split())
        if not value:
            return
        if self._capturing_number_for == "active_users":
            self.visible_active_user_count = value
        elif self.visible_subscriber_count is None:
            self.visible_subscriber_count = value

    def handle_endtag(self, tag: str) -> None:
        if tag not in self._VOID_TAGS:
            if self._surface_depth:
                self._surface_depth -= 1
            if self._sidebar_related_depth:
                self._sidebar_related_depth -= 1
            if self._titlebox_depth:
                self._titlebox_depth -= 1
            if self._side_depth:
                self._side_depth -= 1
            if self._users_online_depth:
                self._users_online_depth -= 1
        if tag == "span":
            self._capturing_number_for = None

    def _advance_region_depths(self, tag: str, class_tokens: set[str]) -> None:
        if self._is_surface_container(class_tokens):
            self._surface_depth += 1
        elif self._surface_depth and tag not in self._VOID_TAGS:
            self._surface_depth += 1

        if "side" in class_tokens:
            self._side_depth += 1
        elif self._side_depth and tag not in self._VOID_TAGS:
            self._side_depth += 1

        if "titlebox" in class_tokens:
            self._titlebox_depth += 1
        elif self._titlebox_depth and tag not in self._VOID_TAGS:
            self._titlebox_depth += 1

        if (
            self.source_surface == CandidateSurface.RELATED_SUBREDDIT
            and self._side_depth
            and ("usertext-body" in class_tokens or "md-container" in class_tokens)
        ):
            self._sidebar_related_depth += 1
        elif self._sidebar_related_depth and tag not in self._VOID_TAGS:
            self._sidebar_related_depth += 1

    def _candidate_subreddit_area_active(self) -> bool:
        return bool(self._surface_depth or self._sidebar_related_depth)

    def _is_surface_container(self, class_tokens: set[str]) -> bool:
        expected = self._SURFACE_CLASS_TOKENS.get(self.source_surface, set())
        return bool(expected & class_tokens)


def _canonical_old_reddit_thread_url(href: str) -> str | None:
    stripped = href.strip()
    if stripped.startswith("/r/"):
        stripped = f"https://old.reddit.com{stripped}"
    if not stripped.startswith("https://old.reddit.com/r/"):
        return None
    stripped = stripped.split("#", 1)[0].split("?", 1)[0]
    if "/comments/" not in stripped:
        return None
    if not stripped.endswith("/"):
        stripped += "/"
    return stripped


def _is_candidate_title_anchor(class_tokens: set[str]) -> bool:
    return "title" in class_tokens or "search-title" in class_tokens


def _subreddit_name_from_url(href: str) -> str | None:
    stripped = href.strip()
    for prefix in (
        "https://old.reddit.com",
        "http://old.reddit.com",
        "https://www.reddit.com",
        "http://www.reddit.com",
        "https://reddit.com",
        "http://reddit.com",
    ):
        if stripped.startswith(prefix):
            stripped = stripped.removeprefix(prefix)
            break
    if not stripped.startswith("/r/"):
        return None
    parts = stripped.split("/")
    if len(parts) < 3 or not parts[2]:
        return None
    subreddit = parts[2]
    if not subreddit.replace("_", "").isalnum():
        return None
    return subreddit
