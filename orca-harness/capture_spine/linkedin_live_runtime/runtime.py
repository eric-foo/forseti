"""LinkedIn live-runtime -- the attended capture runtime entry (slice 3c-2 harness).

``run_live_capture`` is the live runner skeleton. It HARD-ENFORCES the legal gate as
code: it refuses to run without (a) the owner's explicit live-run authorization, (b)
the owner confirmed present, and (c) a valid access POSTURE envelope + run envelope. It
then drives the injected ``Fetcher`` per target, minimizes each capture (3c-1), and
projects it to a candidate row (3b-2), stopping at the declared cap.

Authorization model (slice 3c-2): the ``LiveAccessEnvelope`` stays a POSTURE record
with ``execution_authorized=False`` -- it is never itself an execution authorization
(the slice-3a contract, and the 3b-2 projection binds to it unchanged). The live-run
authorization is a SEPARATE explicit owner act passed here (``live_run_authorized``),
so opening the legal gate is a deliberate runtime argument, not a flag flipped on a
stored record. No committed slice is re-opened.

This module is the no-live HARNESS: with a ``StubFetcher`` it runs fully offline. The
real attended ``BrowserFetcher`` (3c-2b) is the only part that touches LinkedIn and is
owner-validated on an attended run, not unit-tested here.
"""
from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from capture_spine.linkedin_lane.models import CandidateClass, LinkedInLaneError, RunEnvelope
from capture_spine.linkedin_lane.validation import validate_run_envelope
from capture_spine.linkedin_live_adapter.models import LiveAccessEnvelope
from capture_spine.linkedin_live_adapter.projection import project_observation_to_candidate_row
from capture_spine.linkedin_live_adapter.validation import validate_live_access_envelope
from capture_spine.linkedin_live_runtime.fetcher import Fetcher
from capture_spine.linkedin_live_runtime.minimizer import minimize_capture_to_observation


@dataclass(frozen=True)
class CaptureTarget:
    """One thing to capture, carrying the per-candidate operator judgment the
    projection requires (``candidate_class`` + ``business_relevance_note``). ``locator``
    is what the ``Fetcher`` is asked to fetch."""

    locator: str
    candidate_class: CandidateClass | str
    business_relevance_note: str


def _resolve_cap(access_envelope: LiveAccessEnvelope, max_captures: int) -> int:
    # The caps themselves are validated by validate_live_access_envelope (called before
    # this in run_live_capture) -- non-negative ints, positive total. Here we only bound
    # the run's max_captures against the declared posture total; it cannot widen it.
    if type(max_captures) is not int:  # reject bool (a bool is an int subclass) + non-int
        raise LinkedInLaneError("invalid_max_captures", "max_captures must be an integer")
    if max_captures < 1:
        raise LinkedInLaneError("invalid_max_captures", "max_captures must be >= 1")
    declared_total = sum(access_envelope.caps.values())
    if max_captures > declared_total:
        raise LinkedInLaneError(
            "max_captures_exceeds_caps",
            f"max_captures ({max_captures}) exceeds the envelope's declared caps total ({declared_total})",
        )
    return max_captures


def run_live_capture(
    *,
    access_envelope: LiveAccessEnvelope,
    run_envelope: RunEnvelope,
    targets: Sequence[CaptureTarget],
    fetcher: Fetcher,
    live_run_authorized: bool,
    owner_present_confirmed: bool,
    max_captures: int,
) -> list[dict[str, Any]]:
    """Drive an attended capture run: fetch -> minimize -> validate -> project, gated.

    Returns the list of validated candidate-row dicts (one per captured target, up to
    the cap). Raises ``LinkedInLaneError`` if the live-run gate is not satisfied, the
    posture/run envelope is invalid, the cap is invalid, or any per-capture step fails.
    """
    # --- legal gate as code: refuse without explicit owner authorization + presence ---
    if live_run_authorized is not True:
        raise LinkedInLaneError(
            "live_run_not_authorized",
            "a live run requires explicit owner execution authorization (live_run_authorized=True)",
        )
    if owner_present_confirmed is not True:
        raise LinkedInLaneError(
            "owner_not_present",
            "a live run requires the owner confirmed present (owner_present_confirmed=True)",
        )
    # Posture + run envelope must be valid. The access envelope stays a posture record
    # (execution_authorized=False); the live authorization is the separate arg above.
    validate_live_access_envelope(access_envelope.to_dict())
    validate_run_envelope(run_envelope)
    cap = _resolve_cap(access_envelope, max_captures)

    rows: list[dict[str, Any]] = []
    for target in targets:
        if len(rows) >= cap:
            break
        raw_capture = fetcher.fetch(target.locator)
        observation = minimize_capture_to_observation(raw_capture)
        row = project_observation_to_candidate_row(
            observation=observation,
            access_envelope=access_envelope,
            run_envelope=run_envelope,
            candidate_class=target.candidate_class,
            business_relevance_note=target.business_relevance_note,
        )
        rows.append(row)
    return rows
