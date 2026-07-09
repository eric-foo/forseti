"""Pure parsers for IG wind-caller CALLS capture (logged-out og:description path).

No I/O, no deps beyond stdlib. Parses the rendered-DOM meta + grid that the
headless browser_snapshot adapter returns, into the call signal:
- per-post/reel: caption, likes, comments, date, sponsorship (#ad) flag;
- profile: follower/following/post counts;
- grid: /p/ and /reel/ permalinks to enumerate.

Substrate basis: IG serves the caption + engagement in the post/reel page
`og:description` meta to a browser-like client, logged-out (recon + headless
probe 2026-06-14). For genuinely long captions IG truncates the og value; the
parser flags `truncated` so the runner can fall back to the rendered caption
DOM node. The meta `content` attribute is HTML-entity-encoded (inner quotes are
`&quot;`), so values are unescaped before parsing.
"""
from __future__ import annotations

import html
import re
from dataclasses import dataclass

_INSTAGRAM_ORIGIN = "https://www.instagram.com"

# A meta tag, either attribute order: property=... content=... OR content=... property=...
_META_PROP_FIRST = (
    r'<meta[^>]+property=["\']{prop}["\'][^>]*\scontent=["\'](.*?)["\']'
)
_META_CONTENT_FIRST = (
    r'<meta[^>]+content=["\'](.*?)["\'][^>]*\sproperty=["\']{prop}["\']'
)

# Permalink hrefs in the rendered grid: canonical /p/<shortcode>/ or /reel/<shortcode>/,
# plus handle-prefixed variants observed in some rendered surfaces.
_PERMALINK_RE = re.compile(
    r'href=["\'](?P<path>/(?:(?P<handle>[A-Za-z0-9._]+)/(?:p|reel)|(?:p|reel))/[A-Za-z0-9_-]+/)["\']'
)

# Post/reel og:description: "<likes> likes, <comments> comments - <handle> on <Mon D, YYYY>: "<caption>". "
_LIKES_RE = re.compile(r"([\d,]+)\s+likes\b", re.IGNORECASE)
_COMMENTS_RE = re.compile(r"([\d,]+)\s+comments\b", re.IGNORECASE)
_DATE_RE = re.compile(r"\bon\s+([A-Z][a-z]+\s+\d{1,2},\s+\d{4})\s*:")
_CAPTION_RE = re.compile(
    r" on [A-Z][a-z]+ \d{1,2}, \d{4}:\s*\"(.*)$", re.DOTALL
)
# Sponsorship disclosure: the FTC #ad tag (word-bounded so #address etc. do not match) or "paid partnership".
_AD_RE = re.compile(r"(?:#ad\b|paid partnership)", re.IGNORECASE)

# Profile og:description: "<followers> Followers, <following> Following, <posts> Posts - ..."
_PROFILE_RE = re.compile(
    r"([\d.,]+[KMB]?)\s+Followers,\s+([\d.,]+[KMB]?)\s+Following,\s+([\d.,]+[KMB]?)\s+Posts",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class IgPostParse:
    """One post/reel call signal parsed from its og:description."""

    caption: str | None
    likes: int | None
    comments: int | None
    date: str | None
    is_ad: bool
    truncated: bool
    raw_og: str


@dataclass(frozen=True)
class IgProfileParse:
    """Profile-level public stats parsed from the profile og:description (raw tokens; followers may be abbreviated)."""

    followers: str | None
    following: str | None
    posts: str | None
    raw_og: str


def extract_meta_content(rendered_dom: str, prop: str) -> str | None:
    """Return the unescaped content of the <meta property=prop> tag, or None."""
    for template in (_META_PROP_FIRST, _META_CONTENT_FIRST):
        pattern = template.format(prop=re.escape(prop))
        match = re.search(pattern, rendered_dom, re.IGNORECASE | re.DOTALL)
        if match is not None:
            return html.unescape(match.group(1))
    return None


def extract_item_permalinks(rendered_dom: str, *, profile_handle: str | None = None) -> list[str]:
    """Enumerate /p/ and /reel/ permalinks from the rendered grid, deduped, order-preserving, as absolute URLs."""
    normalized_handle = profile_handle.casefold() if profile_handle else None
    seen: set[str] = set()
    out: list[str] = []
    for match in _PERMALINK_RE.finditer(rendered_dom):
        handle = match.group("handle")
        if normalized_handle and handle and handle.casefold() != normalized_handle:
            continue
        path = match.group("path")
        if path not in seen:
            seen.add(path)
            out.append(f"{_INSTAGRAM_ORIGIN}{path}")
    return out


def _to_int(token: str | None) -> int | None:
    if token is None:
        return None
    digits = token.replace(",", "").strip()
    return int(digits) if digits.isdigit() else None


def parse_ig_og_description(og: str) -> IgPostParse:
    """Parse a post/reel og:description into the call signal. `truncated` flags an unclosed (IG-capped) caption."""
    og = html.unescape(og) if "&" in og else og
    likes_m = _LIKES_RE.search(og)
    comments_m = _COMMENTS_RE.search(og)
    date_m = _DATE_RE.search(og)

    caption: str | None = None
    truncated = False
    caption_m = _CAPTION_RE.search(og)
    if caption_m is not None:
        tail = caption_m.group(1)
        # Full captions end with the closing quote then an optional ". " trailer; truncated ones do not.
        stripped = tail.rstrip()
        if stripped.endswith('".'):
            caption = stripped[:-2].rstrip()
        elif stripped.endswith('"'):
            caption = stripped[:-1].rstrip()
        else:
            caption = tail.strip()
            truncated = True

    return IgPostParse(
        caption=caption,
        likes=_to_int(likes_m.group(1)) if likes_m else None,
        comments=_to_int(comments_m.group(1)) if comments_m else None,
        date=date_m.group(1) if date_m else None,
        is_ad=bool(caption and _AD_RE.search(caption)),
        truncated=truncated,
        raw_og=og,
    )


def parse_ig_profile_og(og: str) -> IgProfileParse | None:
    """Parse profile stats from the profile og:description. Returns None if it is not a profile-stats string."""
    og = html.unescape(og) if "&" in og else og
    match = _PROFILE_RE.search(og)
    if match is None:
        return None
    return IgProfileParse(
        followers=match.group(1),
        following=match.group(2),
        posts=match.group(3),
        raw_og=og,
    )
