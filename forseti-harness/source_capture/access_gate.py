from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal
from urllib.parse import unquote, urlparse


LoginGateSignal = Literal["login_redirect", "login_page"]


@dataclass(frozen=True)
class LoginGateDetection:
    signal: LoginGateSignal
    detail: str


_AUTH_PATH_SEGMENTS = frozenset({"login", "register", "sign-in", "signin"})
_LOGIN_FORM_ACTION = re.compile(
    r"""<form\b[^>]*\baction\s*=\s*["'][^"']*(?:/login|/signin|/sign-in|/register)(?:[/?#][^"']*)?["']""",
    re.IGNORECASE,
)
_EXPLICIT_LOGIN_PAGE_MARKERS: tuple[str, ...] = (
    "please log in",
    "please sign in",
    "log in to continue",
    "sign in to continue",
)


def detect_login_gate(*, final_url: str, body_text: str) -> LoginGateDetection | None:
    """Detect a high-confidence post-fetch login gate without certifying content.

    Ordinary pages may contain navigation links such as ``Log in``. Those are
    deliberately insufficient: URL-path detection requires an auth-specific
    segment, and body detection requires a login form action or explicit
    access-gate language.
    """

    parsed = urlparse(final_url)
    path_segments = {
        unquote(segment).strip().lower()
        for segment in (parsed.path or "").split("/")
        if segment.strip()
    }
    matched_segments = sorted(path_segments & _AUTH_PATH_SEGMENTS)
    if matched_segments:
        return LoginGateDetection(
            signal="login_redirect",
            detail=(
                f"final URL landed on an auth path segment {matched_segments[0]!r}: "
                f"{final_url!r}"
            ),
        )

    if _LOGIN_FORM_ACTION.search(body_text):
        return LoginGateDetection(
            signal="login_page",
            detail="response body contains a login/sign-in form action",
        )

    body_lower = body_text.lower()
    for marker in _EXPLICIT_LOGIN_PAGE_MARKERS:
        if marker in body_lower:
            return LoginGateDetection(
                signal="login_page",
                detail=f"response body matched explicit access-gate language {marker!r}",
            )
    return None


__all__ = ["LoginGateDetection", "LoginGateSignal", "detect_login_gate"]
