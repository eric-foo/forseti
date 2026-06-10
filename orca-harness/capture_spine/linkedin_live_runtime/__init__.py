"""LinkedIn live-runtime (slice 3c-1): read-time minimizer (no live access).

One-way import (runtime -> adapter -> core); nothing imports this package, so
deleting it leaves the adapter + core green. The live browser/session fetcher
(slice 3c-2) is NOT here -- it stays behind the legal/ToS gate.
"""
from capture_spine.linkedin_lane.models import LinkedInLaneError
from capture_spine.linkedin_live_runtime.minimizer import minimize_capture_to_observation

__all__ = [
    "LinkedInLaneError",
    "minimize_capture_to_observation",
]
