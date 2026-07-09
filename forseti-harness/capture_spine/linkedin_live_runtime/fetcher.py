"""LinkedIn live-runtime -- the Fetcher seam (slice 3c-2 harness + 3c-2b live).

The injectable boundary between the live page fetch and the no-live minimization
pipeline. A ``Fetcher`` returns a raw, possibly over-captured field bag for a target;
the runtime feeds that bag through the minimizer (3c-1) -> validate -> project (3b-2).

Implementations here:
- ``StubFetcher`` -- offline, pre-seeded bags; exercises the runtime wiring with no
  network/browser.
- ``BrowserFetcher`` (slice 3c-2b) -- the real attended fetcher. It drives a
  ``BrowserDriver`` to get the owner's logged-in rendered DOM, extracts ONLY the
  minimized company signal, and assembles a CLEAN bag (never the raw DOM, never
  person / network data). Its composition is offline-testable with a fake driver;
  the live ``CdpAttachBrowserDriver`` it is given is the only part that touches
  LinkedIn and is owner-validated on the attended run.
"""
from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any, Protocol, runtime_checkable
from urllib.parse import urlparse

from harness_utils import sha256_text, utc_now_z

from capture_spine.linkedin_lane.models import LinkedInLaneError
from capture_spine.linkedin_live_runtime.browser_driver import BrowserDriver
from capture_spine.linkedin_live_runtime.extractor import extract_company_signal


@runtime_checkable
class Fetcher(Protocol):
    """Returns a raw capture bag (field -> value, possibly over-captured) for a target.

    The bag is fetcher-agnostic; the runtime is the single point that minimizes it.
    Implementations MUST NOT minimize, validate, or project -- they only fetch.
    """

    def fetch(self, target: str) -> Mapping[str, Any]: ...


class StubFetcher:
    """Offline ``Fetcher`` for exercising the runtime wiring -- never touches a network.

    Maps each target locator to a pre-seeded raw bag, and raises ``KeyError`` for an
    unknown target so a test cannot silently pass on a missing fixture.
    """

    def __init__(self, bags_by_target: Mapping[str, Mapping[str, Any]]) -> None:
        self._bags: dict[str, Mapping[str, Any]] = dict(bags_by_target)

    def fetch(self, target: str) -> Mapping[str, Any]:
        if target not in self._bags:
            raise KeyError(f"StubFetcher has no seeded bag for target: {target!r}")
        return self._bags[target]


class BrowserFetcher:
    """The real attended ``Fetcher`` (slice 3c-2b) -- the only path that turns a live
    LinkedIn page into a capture bag.

    It drives the injected ``BrowserDriver`` to get the owner's logged-in rendered
    DOM, runs the offline ``extract_company_signal`` extractor, and assembles a CLEAN
    raw bag: the run context it is constructed with (ids, surface, entity type,
    minimization rule) plus only the page-derived business signal (display name +
    visible follower band). The raw DOM and any person / network / social-proof
    content NEVER enter the bag. ``run_live_capture`` still minimizes + validates +
    projects the bag, so a future fetcher bug cannot widen what is retained
    (defense in depth).

    Fail-closed: a page the extractor does not recognize raises
    ``unrecognized_capture_page`` (capture nothing), never a guessed row.
    """

    def __init__(
        self,
        *,
        driver: BrowserDriver,
        live_access_id: str,
        run_id: str,
        observed_source_surface: str,
        observed_entity_type: str = "business_entity",
        minimization_rule: str = "business_entity_only",
        now: Callable[[], str] = utc_now_z,
    ) -> None:
        self._driver = driver
        self._live_access_id = live_access_id
        self._run_id = run_id
        self._observed_source_surface = observed_source_surface
        self._observed_entity_type = observed_entity_type
        self._minimization_rule = minimization_rule
        self._now = now

    def fetch(self, target: str) -> Mapping[str, Any]:
        # Self-enforce the clean-bag boundary: validate the locator HERE (http(s), no
        # embedded credentials) rather than trusting the injected driver, so the bag's
        # observed_source_locator can never carry a credentialed URL (review F4).
        locator = _validate_http_locator(target)
        rendered_dom = self._driver.rendered_dom(locator)
        signal = extract_company_signal(rendered_dom)
        if signal is None:
            raise LinkedInLaneError(
                "unrecognized_capture_page",
                "the captured page did not match a known LinkedIn company top-card; "
                "capturing nothing (fail-closed)",
            )
        captured_at = self._now()
        bag: dict[str, Any] = {
            "observation_id": f"obs-{sha256_text(f'{locator}|{captured_at}')[:24]}",
            "live_access_id": self._live_access_id,
            "run_id": self._run_id,
            "observed_entity_type": self._observed_entity_type,
            "observed_display_name": signal.display_name,
            "observed_source_surface": self._observed_source_surface,
            "observed_source_locator": locator,
            "provenance_timestamp": captured_at,
            "minimization_rule": self._minimization_rule,
        }
        if signal.visible_follower_count_or_none is not None:
            bag["visible_follower_count_or_none"] = signal.visible_follower_count_or_none
        return bag


def _validate_http_locator(url: str) -> str:
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
