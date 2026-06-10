"""LinkedIn live-runtime (slice 3c): read-time minimizer + attended capture harness.

One-way import (runtime -> adapter -> core); nothing imports this package, so deleting
it leaves the adapter + core green. The harness runs fully offline with a StubFetcher;
the real attended BrowserFetcher (slice 3c-2b -- the only part that touches LinkedIn)
implements the Fetcher seam and stays behind the legal/ToS gate, owner-validated.
"""
from capture_spine.linkedin_lane.models import LinkedInLaneError
from capture_spine.linkedin_live_runtime.fetcher import Fetcher, StubFetcher
from capture_spine.linkedin_live_runtime.minimizer import minimize_capture_to_observation
from capture_spine.linkedin_live_runtime.runtime import CaptureTarget, run_live_capture

__all__ = [
    "LinkedInLaneError",
    "Fetcher",
    "StubFetcher",
    "CaptureTarget",
    "minimize_capture_to_observation",
    "run_live_capture",
]
