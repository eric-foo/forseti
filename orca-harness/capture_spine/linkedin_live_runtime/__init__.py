"""LinkedIn live-runtime (slice 3c): read-time minimizer + attended capture harness
+ the real attended BrowserFetcher (3c-2b).

One-way import (runtime -> adapter -> core); nothing imports this package, so deleting
it leaves the adapter + core green. The harness runs fully offline with a StubFetcher;
the real attended BrowserFetcher (3c-2b) drives a CdpAttachBrowserDriver -- the only
part that touches LinkedIn -- which stays behind the legal/ToS gate and is
owner-validated.
"""
from capture_spine.linkedin_lane.models import LinkedInLaneError
from capture_spine.linkedin_live_runtime.browser_driver import (
    BrowserDriver,
    CdpAttachBrowserDriver,
)
from capture_spine.linkedin_live_runtime.extractor import (
    CompanySignal,
    extract_company_signal,
)
from capture_spine.linkedin_live_runtime.fetcher import BrowserFetcher, Fetcher, StubFetcher
from capture_spine.linkedin_live_runtime.minimizer import minimize_capture_to_observation
from capture_spine.linkedin_live_runtime.runtime import CaptureTarget, run_live_capture

__all__ = [
    "LinkedInLaneError",
    "Fetcher",
    "StubFetcher",
    "BrowserFetcher",
    "BrowserDriver",
    "CdpAttachBrowserDriver",
    "CompanySignal",
    "extract_company_signal",
    "CaptureTarget",
    "minimize_capture_to_observation",
    "run_live_capture",
]
