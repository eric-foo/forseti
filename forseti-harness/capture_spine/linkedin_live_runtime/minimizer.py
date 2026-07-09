"""LinkedIn live-runtime -- slice 3c-1 read-time minimizer (no live access).

The READ-TIME minimization point: given an over-captured raw field bag (whatever a
fetcher pulled off a page, possibly including forbidden over-capture -- a profile
body, contact fields, a follower list, raw html), keep ONLY the named minimized
``LiveObservation`` fields and DROP everything else, then validate. Default-deny: a
key that is not a ``LiveObservation`` content field is never read, so it cannot
survive into the observation; the minimization-boundary flags are forced to their
safe defaults (never read from the bag). This is the runtime half of the §6.2
boundary -- the "tape-test" proof that what we KEEP is a strict minimization of what
was READ.

No I/O, no browser, no LinkedIn access: a pure transform over a field bag. The bag is
fetcher-agnostic (field -> value); the actual page fetch + parse is slice 3c-2 (the
browser/session fetcher, behind the legal/ToS gate), which fills the bag. One-way
import (runtime -> adapter -> core); nothing imports this package, so deleting it
leaves prior slices green.

Scope (3c-1): minimize-SILENTLY -- drop forbidden over-capture, force the flags safe.
It does NOT reject a bag merely because it shows evidence of over-capture (that
fetcher-trust / observability concern is deferred). Content smuggled INTO an allowed
field (e.g. a bio pasted into a display name) is caught by the observation gate's
length/format caps, which this minimizer runs on its output.
"""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import fields
from typing import Any

from capture_spine.linkedin_lane.models import LinkedInLaneError
from capture_spine.linkedin_lane.shared_validation import require_fields
from capture_spine.linkedin_live_adapter.models import LiveObservation
from capture_spine.linkedin_live_adapter.validation import validate_live_observation


# Fields the minimizer FORCES to their safe dataclass default -- never read from the
# raw bag. The minimization-boundary flags must stay False, schema_version is fixed,
# and exclusions is a runtime-generated receipt (not raw page text), so a bag claiming
# contact_fields_retained=True, a wrong schema, or narrative in exclusions cannot set
# them: the minimizer simply does not carry them across (cross-vendor 3c-1 review).
_FORCED_SAFE_FIELDS: frozenset[str] = frozenset(
    {
        "schema_version",
        "exclusions",
        "contact_fields_retained",
        "network_or_follower_list_retained",
        "profile_body_captured",
        "content_captured",
    }
)

# The content fields the minimizer carries from the bag -- every LiveObservation field
# EXCEPT the forced-safe ones. Derived from the dataclass so it tracks the schema with
# zero drift (a new field is carried unless explicitly forced safe).
_MINIMIZED_OBSERVATION_FIELDS: tuple[str, ...] = tuple(
    f.name for f in fields(LiveObservation) if f.name not in _FORCED_SAFE_FIELDS
)

# Required content the bag must supply (the LiveObservation non-default fields). A bag
# missing one fails closed with a LinkedInLaneError, not a bare constructor TypeError.
_REQUIRED_RAW_CAPTURE_FIELDS: tuple[str, ...] = (
    "observation_id",
    "live_access_id",
    "run_id",
    "observed_entity_type",
    "observed_display_name",
    "observed_source_surface",
    "observed_source_locator",
    "provenance_timestamp",
    "minimization_rule",
)


def minimize_capture_to_observation(raw_capture: Mapping[str, Any]) -> LiveObservation:
    """Minimize an over-captured raw field bag to a validated ``LiveObservation``.

    Keeps ONLY the named minimized fields (default-deny on every other key), forces
    the minimization-boundary flags to their safe defaults, and validates the result.
    Returns the validated ``LiveObservation``; raises ``LinkedInLaneError`` if the bag
    is not a mapping, lacks a required field, or the minimized result fails the §6.2
    observation gate.
    """
    if not isinstance(raw_capture, Mapping):
        raise LinkedInLaneError(
            "invalid_raw_capture",
            "raw_capture must be a field mapping (the fetcher-agnostic capture bag)",
        )
    # Default-deny read: only the named minimized fields are carried; every other key
    # in the bag (profile body, contact, follower list, raw html, ...) is dropped.
    kept = {name: raw_capture[name] for name in _MINIMIZED_OBSERVATION_FIELDS if name in raw_capture}
    require_fields(kept, _REQUIRED_RAW_CAPTURE_FIELDS, "raw_capture")
    observation = LiveObservation(**kept)
    # Validate the MINIMIZED output (catches content smuggled into an allowed field via
    # the length/format caps, the person gate, etc.). Returns only a validated record.
    validate_live_observation(observation.to_dict())
    return observation
