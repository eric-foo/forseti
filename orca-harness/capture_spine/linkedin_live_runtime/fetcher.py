"""LinkedIn live-runtime -- the Fetcher seam (slice 3c-2 harness).

The injectable boundary between the live page fetch and the no-live minimization
pipeline. A ``Fetcher`` returns a raw, possibly over-captured field bag for a target;
the runtime feeds that bag through the minimizer (3c-1) -> validate -> project (3b-2).

The real attended ``BrowserFetcher`` (slice 3c-2b -- the only part that touches
LinkedIn) implements this Protocol and is built + validated separately under the
owner's attended run; it is NOT in this harness. The ``StubFetcher`` here lets the
runtime wiring be exercised entirely offline (no network, no browser).
"""
from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Protocol, runtime_checkable


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
