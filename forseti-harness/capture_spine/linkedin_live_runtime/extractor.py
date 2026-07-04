"""LinkedIn live-runtime -- slice 3c-2b page extractor (no live access, offline).

The per-source WRAPPER: rendered LinkedIn company-page DOM -> a minimized
``CompanySignal`` (the business entity's display name + visible follower band).
Pure HTML->fields with the stdlib ``html.parser``; mirrors the
``reddit_candidate_intake`` projection's region-tracked ``HTMLParser`` pattern. It
runs on a string the driver already fetched -- no I/O, no browser -- so it is
fully offline-testable with synthetic fixtures (real structure, fake data).

Discipline (the s6.2 minimization boundary at the read edge):
- FAIL-CLOSED: a page with no recognizable company top-card title -> ``None``
  (capture nothing), never a guess.
- BUSINESS SIGNAL ONLY: captures the company display name + the visible follower
  count as a coarse band. It NEVER descends into the secondary-content /
  social-proof region, which carries connection / person names -- exactly the
  network/person data the lane forbids.
- counts / coarse bands only: the follower value is normalized to a bare count
  band (e.g. "2M  followers" -> "2M"); a value that is not a clean count/band is
  dropped to ``None`` rather than emitted. The observation gate
  (``validate_live_observation``) is the final authority; this just avoids
  emitting free text into a counts-only field.

Scope (3c-2b): ONE company top-card per page (the runtime model is one locator ->
one observation). Location / industry / employee-band extraction is DEFERRED --
reliably classifying those info-list items needs more page samples, and emitting a
mis-classified field would be over-capture, so this slice captures only the two
unambiguous signals.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from html.parser import HTMLParser


# Exact class tokens for the primary-entity title + info-list items (matched by
# token membership, not substring, so a class that merely contains the text does
# not trip them).
_TITLE_CLASS = "org-top-card-summary__title"
_INFO_ITEM_CLASS = "org-top-card-summary-info-list__info-item"

# Substrings marking the secondary-content / social-proof region (connection and
# person names). Capture is suppressed anywhere inside it -- a broad substring
# guard is intentional here: over-blocking person data is safe, under-blocking is
# not.
_BLOCKED_REGION_MARKERS: tuple[str, ...] = ("org-top-card-secondary-content", "social-proof")

_VOID_TAGS: frozenset[str] = frozenset(
    {
        "area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr",
    }
)

# Conservative count / coarse-band shape for the follower value. Intentionally a
# SUBSET of shared_validation._VISIBLE_INFLUENCE_VALUE_RE: a value matching here
# will pass the observation gate; anything else is dropped to ``None`` rather than
# risking a free-text value that fails downstream.
_FOLLOWER_VALUE_RE = re.compile(r"^\d{1,3}(?:,\d{3})*(?:\.\d+)?[KkMm]?\+?$")


@dataclass(frozen=True)
class CompanySignal:
    """The minimized business signal pulled from a company-page top-card."""

    display_name: str
    visible_follower_count_or_none: str | None = None


def extract_company_signal(rendered_dom: str) -> CompanySignal | None:
    """Extract the minimized company signal from a rendered LinkedIn company page.

    Returns a ``CompanySignal`` when the DOM has a recognizable company top-card
    title; returns ``None`` (fail-closed) for any unrecognized page. Captures only
    the business entity's display name and visible follower band -- never person /
    connection / social-proof content.
    """
    if not isinstance(rendered_dom, str) or not rendered_dom.strip():
        return None
    parser = _CompanyTopCardParser()
    parser.feed(rendered_dom)
    # Fail-closed recognition: require the display name AND a non-empty summary info-list,
    # and reject a page that exposed more than one top-card title (a lone title class, a
    # partial / truncated page, or a duplicate title -> None; review F2).
    if not parser.display_name or parser.ambiguous_title or not parser.info_items:
        return None
    follower = _follower_band_from_info_items(parser.info_items)
    return CompanySignal(
        display_name=parser.display_name,
        visible_follower_count_or_none=follower,
    )


def _collapse_ws(text: str) -> str:
    return " ".join(text.split())


def _follower_band_from_info_items(info_items: list[str]) -> str | None:
    """Return the minimized follower count band from the first 'followers' info-item.

    "2M  followers" -> "2M"; "1,753,723 followers" -> "1,753,723". A value that is
    not a clean count/band is dropped to ``None`` (fail-closed)."""
    for item in info_items:
        if "follower" in item.lower():
            value = _collapse_ws(re.split(r"follower", item, maxsplit=1, flags=re.IGNORECASE)[0])
            if value and _FOLLOWER_VALUE_RE.fullmatch(value):
                return value
            return None
    return None


class _CompanyTopCardParser(HTMLParser):
    """Region-tracked parser: captures the company top-card title text and the
    summary info-list item texts, and refuses to read inside the secondary-content
    / social-proof region (connection / person names). Mirrors the reddit listing
    parser's depth-counter discipline."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.display_name: str | None = None
        self.info_items: list[str] = []
        self.ambiguous_title = False
        self._blocked_stack: list[str] = []
        self._title_depth = 0
        self._title_parts: list[str] = []
        self._item_depth = 0
        self._item_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        void = tag in _VOID_TAGS
        attr_map = {key: (value or "") for key, value in attrs}
        class_attr = attr_map.get("class", "")
        class_tokens = set(class_attr.split())

        # Blocked region (person / social-proof): enter or descend; capture nothing.
        # Tag-aware STACK (not a bare depth counter): only a matching end tag exits the
        # region, so unmatched / malformed end tags OVER-block rather than leak (review F1).
        if self._blocked_stack:
            if not void:
                self._blocked_stack.append(tag)
            return
        if any(marker in class_attr for marker in _BLOCKED_REGION_MARKERS):
            if not void:
                self._blocked_stack.append(tag)
            return

        # Title region: the first title-classed element captures; a SECOND one (after the
        # name is set) marks the page ambiguous -> fail-closed in extract_company_signal
        # (review F2). Detected here at start-tag time -- the endtag never sees it because
        # the capture guard below stops re-entering the title region once a name is set.
        if self._title_depth:
            if not void:
                self._title_depth += 1
        elif _TITLE_CLASS in class_tokens:
            if self.display_name is None:
                self._title_depth = 1
                self._title_parts = []
            else:
                self.ambiguous_title = True

        # Info-item region.
        if self._item_depth:
            if not void:
                self._item_depth += 1
        elif _INFO_ITEM_CLASS in class_tokens:
            self._item_depth = 1
            self._item_parts = []

    def handle_data(self, data: str) -> None:
        if self._blocked_stack:
            return
        if self._title_depth:
            self._title_parts.append(data)
        if self._item_depth:
            self._item_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag in _VOID_TAGS:
            return
        if self._blocked_stack:
            # Only a matching end tag exits the blocked region; an unmatched end tag is
            # ignored (over-block malformed DOM rather than leak person data -- review F1).
            if tag == self._blocked_stack[-1]:
                self._blocked_stack.pop()
            return
        if self._title_depth:
            self._title_depth -= 1
            if self._title_depth == 0:
                text = _collapse_ws("".join(self._title_parts))
                if text and self.display_name is None:
                    self.display_name = text
                self._title_parts = []
        if self._item_depth:
            self._item_depth -= 1
            if self._item_depth == 0:
                text = _collapse_ws("".join(self._item_parts))
                if text:
                    self.info_items.append(text)
                self._item_parts = []
