"""LinkedIn live-runtime -- slice 3c-2b attended browser driver (the live edge).

``CdpAttachBrowserDriver`` is the ONLY part of the lane that touches LinkedIn live.
It attaches over the Chrome DevTools Protocol to the owner's ALREADY-RUNNING,
ALREADY-LOGGED-IN browser, opens its own page, navigates to the target, and returns
the rendered DOM. Clean attach, owner-accepted ``optional_poc_risk_mode`` posture:

- NO stored credentials, NO storage_state, NO cookie / session extraction -- it
  uses the owner's genuine logged-in session because the owner started the browser;
- NO proxy, NO synthetic stealth -- attaching to the owner's real, supervised
  browser is authentically human, so anti-detect would only raise risk and pull
  away from a legally-defensible posture;
- NO entitlement-gate bypass (a hard stop).

It mirrors the source_capture armory ``browser_snapshot`` engine discipline (lazy
Playwright import + dependency-unavailable handling, http(s)-only target with no
embedded credentials, fail-closed) but with a ``connect_over_cdp`` attach and a
minimal ``rendered_dom`` surface (no own-launch, no screenshot). Promoting a shared
CDP engine into the armory is a deferred, larger move; this thin driver stays in
the discovery lane (which is upstream of the armory and emits no Source Capture
Packets).

Claim boundary: the live connect/navigate path is OWNER-VALIDATED on the attended
run and is NOT unit-tested against a real browser. Its offline fail-closed guards
(bad endpoint, bad target, dependency unavailable) ARE.
"""
from __future__ import annotations

from importlib import import_module
from typing import Protocol, runtime_checkable
from urllib.parse import urlparse

from capture_spine.linkedin_lane.models import LinkedInLaneError


_ALLOWED_WAIT_UNTIL = frozenset({"commit", "domcontentloaded", "load", "networkidle"})
DEFAULT_NAV_TIMEOUT_SECONDS = 20.0


@runtime_checkable
class BrowserDriver(Protocol):
    """Returns the rendered DOM (post-JavaScript HTML) for a target URL."""

    def rendered_dom(self, target: str) -> str: ...


class CdpAttachBrowserDriver:
    """Attach to the owner's running, logged-in browser over CDP and read a page's
    rendered DOM. See module docstring for the posture and claim boundary."""

    def __init__(
        self,
        *,
        cdp_endpoint: str,
        wait_until: str = "load",
        nav_timeout_seconds: float = DEFAULT_NAV_TIMEOUT_SECONDS,
        content_ready_selector: str | None = None,
    ) -> None:
        if not isinstance(cdp_endpoint, str) or not cdp_endpoint.strip():
            raise LinkedInLaneError(
                "invalid_cdp_endpoint",
                "cdp_endpoint must be the CDP URL of the owner's already-running browser",
            )
        if wait_until not in _ALLOWED_WAIT_UNTIL:
            raise LinkedInLaneError(
                "invalid_wait_until",
                f"wait_until must be one of: {', '.join(sorted(_ALLOWED_WAIT_UNTIL))}",
            )
        if not isinstance(nav_timeout_seconds, (int, float)) or nav_timeout_seconds <= 0:
            raise LinkedInLaneError("invalid_nav_timeout", "nav_timeout_seconds must be > 0")
        self._cdp_endpoint = self._validate_cdp_endpoint(cdp_endpoint)
        self._wait_until = wait_until
        self._nav_timeout_ms = float(nav_timeout_seconds) * 1000
        # Optional CSS selector to wait for AFTER navigation. LinkedIn is a client-
        # rendered SPA: the company top-card is NOT in the DOM at the `load` event, so
        # the caller passes a content anchor (e.g. ".org-top-card-summary__title") and
        # the rendered DOM is read only after that content has hydrated. None = read
        # immediately (static pages).
        self._content_ready_selector = content_ready_selector

    def rendered_dom(self, target: str) -> str:
        normalized = self._validate_http_target(target)
        try:
            sync_api = import_module("playwright.sync_api")
        except ModuleNotFoundError as exc:
            raise LinkedInLaneError(
                "browser_dependency_unavailable",
                "Playwright is not installed; install the 'browser' optional dependency "
                "(playwright) before an attended live capture",
            ) from exc
        # OWNER-VALIDATED live path (not unit-tested). Attach to the owner's running
        # browser, open OUR OWN page (so the owner's tabs are not disturbed), navigate,
        # read the rendered DOM, and close only our page. We do NOT close the owner's
        # context; for a connect_over_cdp browser, browser.close() drops the Playwright
        # connection without closing the owner's actual browser.
        with sync_api.sync_playwright() as playwright:
            browser = playwright.chromium.connect_over_cdp(self._cdp_endpoint)
            try:
                context = browser.contexts[0] if browser.contexts else browser.new_context()
                page = context.new_page()
                try:
                    page.goto(normalized, wait_until=self._wait_until, timeout=self._nav_timeout_ms)
                    if self._content_ready_selector is not None:
                        page.wait_for_selector(self._content_ready_selector, timeout=self._nav_timeout_ms)
                    return page.content()
                finally:
                    page.close()
            finally:
                browser.close()

    @staticmethod
    def _validate_cdp_endpoint(url: str) -> str:
        # Enforce the clean-attach posture as code: a LOCAL, credential-free CDP URL for
        # the owner's own already-running browser -- no embedded creds, no remote relay
        # (review F3). connect_over_cdp accepts http(s) or ws(s) endpoints.
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https", "ws", "wss"} or not parsed.netloc:
            raise LinkedInLaneError(
                "invalid_cdp_endpoint",
                "cdp_endpoint must be an absolute http(s):// or ws(s):// CDP URL",
            )
        if parsed.username is not None or parsed.password is not None:
            raise LinkedInLaneError("invalid_cdp_endpoint", "cdp_endpoint must not embed credentials")
        if parsed.hostname not in {"localhost", "127.0.0.1", "::1"}:
            raise LinkedInLaneError(
                "invalid_cdp_endpoint",
                "cdp_endpoint must point to the owner's local already-running browser "
                "(localhost / 127.0.0.1 / ::1)",
            )
        return parsed.geturl()

    @staticmethod
    def _validate_http_target(url: str) -> str:
        if not isinstance(url, str):
            raise LinkedInLaneError("invalid_capture_target", "capture target must be a string URL")
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise LinkedInLaneError(
                "invalid_capture_target",
                "capture target must be an absolute http:// or https:// URL",
            )
        if parsed.username is not None or parsed.password is not None:
            raise LinkedInLaneError("invalid_capture_target", "capture target must not embed credentials")
        return parsed.geturl()
