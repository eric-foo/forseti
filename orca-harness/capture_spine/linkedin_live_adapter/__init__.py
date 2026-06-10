"""LinkedIn live-adapter (slice 3a): Live Access Envelope contract record + validator.

No-runtime satellite. Imports the no-live core one-way (adapter -> core); the
core never imports this package, so deleting it leaves slices 1+2 intact.
"""
from capture_spine.linkedin_live_adapter.models import (
    DEFAULT_LINKEDIN_LIVE_ADAPTER_NON_CLAIMS,
    LINKEDIN_LIVE_ACCESS_ENVELOPE_SCHEMA_VERSION,
    LINKEDIN_LIVE_OBSERVATION_SCHEMA_VERSION,
    LinkedInLaneError,
    LiveAccessEnvelope,
    LiveAccessMode,
    LiveObservation,
)
from capture_spine.linkedin_live_adapter.validation import (
    validate_live_access_envelope,
    validate_live_observation,
)

__all__ = [
    "DEFAULT_LINKEDIN_LIVE_ADAPTER_NON_CLAIMS",
    "LINKEDIN_LIVE_ACCESS_ENVELOPE_SCHEMA_VERSION",
    "LINKEDIN_LIVE_OBSERVATION_SCHEMA_VERSION",
    "LinkedInLaneError",
    "LiveAccessEnvelope",
    "LiveAccessMode",
    "LiveObservation",
    "validate_live_access_envelope",
    "validate_live_observation",
]
