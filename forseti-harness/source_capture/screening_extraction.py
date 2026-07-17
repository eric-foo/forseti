from __future__ import annotations

from collections.abc import Callable
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from html.parser import HTMLParser
from urllib.parse import urlparse


@dataclass(frozen=True)
class StructuredListingCandidate:
    item_url: str
    title: str | None
    source_anchor_class: str
    item_datetime: str | None
    item_datetime_state: str
    item_datetime_detail: str | None = None
    source_container_class: str | None = None

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class StructuredListingExtractionSpec:
    container_classes: tuple[str, ...]
    anchor_classes: tuple[str, ...]
    href_must_contain: tuple[str, ...] = ()
    datetime_classes: tuple[str, ...] = ()
    allow_unclassified_datetime: bool = False
    container_tags: tuple[str, ...] = ("article", "div", "li")
    anchor_tags: tuple[str, ...] = ("a",)
    datetime_tags: tuple[str, ...] = ("time",)
    datetime_attr: str = "datetime"
    datetime_label: str = "item datetime"
    canonicalize_url: Callable[[str], str | None] | None = None


@dataclass(frozen=True)
class OldRedditThreadCandidate:
    thread_url: str
    subreddit: str
    title: str | None
    source_anchor_class: str
    submission_datetime: str | None
    submission_datetime_state: str
    submission_datetime_detail: str | None = None

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def extract_screening_fields(
    *,
    url: str,
    body_text: str,
    old_reddit_submission_min_datetime: str | None = None,
    old_reddit_submission_max_datetime: str | None = None,
) -> dict[str, object]:
    """Return bounded screen-light extraction fields from already-read text.

    This intentionally returns only locator-style fields. It never returns raw
    HTML, comment bodies, post bodies, author/profile fields, packet metadata, or
    ECR/Cleaning/Judgment data.
    """
    fields: dict[str, object] = {
        "comments_marker_count": body_text.count("/comments/"),
    }
    if _looks_like_old_reddit_listing_or_search(url):
        candidates = extract_old_reddit_thread_candidates(
            body_text=body_text,
            submission_min_datetime=old_reddit_submission_min_datetime,
            submission_max_datetime=old_reddit_submission_max_datetime,
        )
        fields["old_reddit_thread_candidates"] = [candidate.to_dict() for candidate in candidates]
        fields["old_reddit_thread_candidate_count"] = len(candidates)
    return fields


def extract_structured_listing_candidates(
    *,
    body_text: str,
    spec: StructuredListingExtractionSpec,
    item_min_datetime: str | None = None,
    item_max_datetime: str | None = None,
) -> list[StructuredListingCandidate]:
    """Extract same-shaped listing rows with targeted, row-local locators.

    Use this for public listing/search pages where a candidate item is expressed
    as a repeated row/card containing a title link and optional row-local
    datetime. It deliberately ignores page-wide datetimes and page chrome.
    """
    _validate_structured_listing_spec(spec)
    min_dt = _parse_optional_iso_datetime(item_min_datetime)
    max_dt = _parse_optional_iso_datetime(item_max_datetime)
    parser = _StructuredListingParser(spec=spec, item_min_datetime=min_dt, item_max_datetime=max_dt)
    parser.feed(body_text)
    parser.close()
    return parser.candidates


def extract_old_reddit_thread_candidates(
    *,
    body_text: str,
    submission_min_datetime: str | None = None,
    submission_max_datetime: str | None = None,
) -> list[OldRedditThreadCandidate]:
    generic_candidates = extract_structured_listing_candidates(
        body_text=body_text,
        spec=_OLD_REDDIT_LISTING_SPEC,
        item_min_datetime=submission_min_datetime,
        item_max_datetime=submission_max_datetime,
    )
    candidates: list[OldRedditThreadCandidate] = []
    for generic_candidate in generic_candidates:
        subreddit = _subreddit_from_thread_url(generic_candidate.item_url)
        if subreddit is None:
            continue
        candidates.append(
            OldRedditThreadCandidate(
                thread_url=generic_candidate.item_url,
                subreddit=subreddit,
                title=generic_candidate.title,
                source_anchor_class=generic_candidate.source_anchor_class,
                submission_datetime=generic_candidate.item_datetime,
                submission_datetime_state=generic_candidate.item_datetime_state,
                submission_datetime_detail=generic_candidate.item_datetime_detail,
            )
        )
    return candidates


class _StructuredListingParser(HTMLParser):
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

    def __init__(
        self,
        *,
        spec: StructuredListingExtractionSpec,
        item_min_datetime: datetime | None,
        item_max_datetime: datetime | None,
    ) -> None:
        super().__init__(convert_charrefs=True)
        self.spec = spec
        self.item_min_datetime = item_min_datetime
        self.item_max_datetime = item_max_datetime
        self.candidates: list[StructuredListingCandidate] = []
        self._seen_urls: set[str] = set()
        self._container_depth = 0
        self._container_class: str | None = None
        self._container_href: str | None = None
        self._container_title: str | None = None
        self._container_anchor_class: str | None = None
        self._container_datetime: str | None = None
        self._current_anchor_href: str | None = None
        self._current_anchor_class: str | None = None
        self._current_anchor_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {key: value or "" for key, value in attrs}
        class_tokens = _class_tokens(attr_map.get("class", ""))

        if self._container_depth:
            if tag not in self._VOID_TAGS:
                self._container_depth += 1
        elif tag in self.spec.container_tags:
            container_class = _first_matching_class(class_tokens, self.spec.container_classes)
            if container_class is not None:
                self._container_depth = 1
                self._container_class = container_class
                self._container_href = None
                self._container_title = None
                self._container_anchor_class = None
                self._container_datetime = None

        if not self._container_depth:
            return

        if tag in self.spec.anchor_tags:
            href = attr_map.get("href", "")
            anchor_class = _first_matching_class(class_tokens, self.spec.anchor_classes)
            if anchor_class is not None and _href_matches(href, self.spec.href_must_contain):
                self._current_anchor_href = href
                self._current_anchor_class = anchor_class
                self._current_anchor_parts = []
                return

        if self._container_datetime is None and tag in self.spec.datetime_tags:
            if _is_item_datetime_locator(class_tokens, self.spec):
                datetime_value = attr_map.get(self.spec.datetime_attr, "").strip()
                if datetime_value:
                    self._container_datetime = datetime_value

    def handle_data(self, data: str) -> None:
        if self._current_anchor_href is not None:
            self._current_anchor_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag in self.spec.anchor_tags and self._current_anchor_href is not None:
            title = " ".join("".join(self._current_anchor_parts).split()) or None
            if self._container_href is None:
                self._container_href = self._current_anchor_href
                self._container_title = title
                self._container_anchor_class = self._current_anchor_class
            self._current_anchor_href = None
            self._current_anchor_class = None
            self._current_anchor_parts = []

        if self._container_depth and tag not in self._VOID_TAGS:
            self._container_depth -= 1
            if self._container_depth == 0:
                if self._container_href is not None:
                    self._append_candidate(
                        href=self._container_href,
                        title=self._container_title,
                        anchor_class=self._container_anchor_class or "unknown",
                        item_datetime=self._container_datetime,
                        container_class=self._container_class,
                    )
                self._container_class = None
                self._container_href = None
                self._container_title = None
                self._container_anchor_class = None
                self._container_datetime = None

    def _append_candidate(
        self,
        *,
        href: str,
        title: str | None,
        anchor_class: str,
        item_datetime: str | None,
        container_class: str | None,
    ) -> None:
        item_url = _canonicalize_item_url(href, self.spec.canonicalize_url)
        if item_url is None or item_url in self._seen_urls:
            return

        state, normalized, detail = _classify_item_datetime(
            item_datetime,
            min_datetime=self.item_min_datetime,
            max_datetime=self.item_max_datetime,
            label=self.spec.datetime_label,
        )
        self.candidates.append(
            StructuredListingCandidate(
                item_url=item_url,
                title=title,
                source_anchor_class=anchor_class,
                item_datetime=normalized,
                item_datetime_state=state,
                item_datetime_detail=detail,
                source_container_class=container_class,
            )
        )
        self._seen_urls.add(item_url)


def _validate_structured_listing_spec(spec: StructuredListingExtractionSpec) -> None:
    if not spec.container_classes:
        raise ValueError("structured listing extraction requires at least one container class")
    if not spec.anchor_classes:
        raise ValueError("structured listing extraction requires at least one title anchor class")


def _class_tokens(value: str) -> set[str]:
    return {token for token in value.split() if token}


def _first_matching_class(class_tokens: set[str], allowed_classes: tuple[str, ...]) -> str | None:
    for class_name in allowed_classes:
        if class_name in class_tokens:
            return class_name
    return None


def _href_matches(href: str, required_substrings: tuple[str, ...]) -> bool:
    return bool(href.strip()) and all(substring in href for substring in required_substrings)


def _is_item_datetime_locator(class_tokens: set[str], spec: StructuredListingExtractionSpec) -> bool:
    if not spec.datetime_classes:
        return True
    if _first_matching_class(class_tokens, spec.datetime_classes) is not None:
        return True
    return spec.allow_unclassified_datetime and not class_tokens


def _canonicalize_item_url(
    href: str,
    canonicalize_url: Callable[[str], str | None] | None,
) -> str | None:
    if canonicalize_url is not None:
        return canonicalize_url(href)
    stripped = href.strip().split("#", 1)[0]
    return stripped or None


_OLD_REDDIT_LISTING_SPEC = StructuredListingExtractionSpec(
    container_classes=("thing", "search-result"),
    anchor_classes=("search-title", "title"),
    href_must_contain=("/comments/",),
    datetime_classes=("live-timestamp",),
    allow_unclassified_datetime=True,
    datetime_label="submission datetime",
    canonicalize_url=lambda href: _canonical_old_reddit_thread_url(href),
)


def _canonical_old_reddit_thread_url(href: str) -> str | None:
    # helper-delta: extra www.reddit.com -> old.reddit.com rewrite vs
    # projection_shared.canonical_old_reddit_thread_url, which admits only
    # old.reddit.com hosts; keep this copy local for the www rewrite.
    stripped = href.strip()
    if stripped.startswith("/r/"):
        stripped = f"https://old.reddit.com{stripped}"
    if stripped.startswith("https://www.reddit.com/r/"):
        stripped = "https://old.reddit.com/r/" + stripped.split("https://www.reddit.com/r/", 1)[1]
    if not stripped.startswith("https://old.reddit.com/r/"):
        return None
    stripped = stripped.split("#", 1)[0].split("?", 1)[0]
    if "/comments/" not in stripped:
        return None
    if not stripped.endswith("/"):
        stripped += "/"
    return stripped


def _subreddit_from_thread_url(url: str) -> str | None:
    parsed = urlparse(url)
    parts = parsed.path.split("/")
    if len(parts) < 3 or parts[1] != "r" or not parts[2]:
        return None
    subreddit = parts[2]
    if not subreddit.replace("_", "").isalnum():
        return None
    return subreddit


def _looks_like_old_reddit_listing_or_search(url: str) -> bool:
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    if host not in {"old.reddit.com", "www.reddit.com"}:
        return False
    path = (parsed.path or "").rstrip("/")
    if "/comments/" in path:
        return False
    return path.startswith("/r/")


def _classify_item_datetime(
    value: str | None,
    *,
    min_datetime: datetime | None,
    max_datetime: datetime | None,
    label: str,
) -> tuple[str, str | None, str | None]:
    if value is None:
        return "unknown_absent", None, f"no targeted listing time element was found for this row"
    parsed = _parse_optional_iso_datetime(value)
    if parsed is None:
        return "invalid", None, f"could not parse {label} {value!r}"
    if min_datetime is not None and parsed < min_datetime:
        return (
            "out_of_range",
            _format_utc(parsed),
            f"{label} is before range minimum {_format_utc(min_datetime)}",
        )
    if max_datetime is not None and parsed > max_datetime:
        return (
            "out_of_range",
            _format_utc(parsed),
            f"{label} is after range maximum {_format_utc(max_datetime)}",
        )
    return "known", _format_utc(parsed), None


def _parse_optional_iso_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    text = value.strip()
    if text.endswith("Z"):
        text = f"{text[:-1]}+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC).replace(microsecond=0)


def _format_utc(value: datetime) -> str:
    return value.astimezone(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


__all__ = [
    "OldRedditThreadCandidate",
    "StructuredListingCandidate",
    "StructuredListingExtractionSpec",
    "extract_old_reddit_thread_candidates",
    "extract_screening_fields",
    "extract_structured_listing_candidates",
]
