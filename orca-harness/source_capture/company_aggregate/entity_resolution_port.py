"""PROVISIONAL entity-resolution port for the company-aggregate projection (AR-07).

A deliberately-provisional PORT that the (unbuilt) entity-resolution spine will OWN and replace.
The capture lane only *applies* a resolution map (consumes it); it NEVER authors canonical entity
identity -- the #1 ownership boundary. This module is therefore a stub/seam, not an authoritative
resolver, and lives here only so the projection has something to depend on until the spine exists.

The v0 default, ``PassthroughNullResolutionMap``, resolves NOTHING: it returns a filer-level
``provisional_filer_key`` derived from the CIK and leaves ``entity_key`` null with
``resolution_state='unresolved'`` -- because a CIK is a *filer* id, not a canonical company id
(AR-04). Economic merge/rollup across filers is spine-authored and a hard-STOP for this lane
(AR-01); a passthrough-null performs no merges. A real (spine-authored) map is injected, never
written here.

``map_version`` / ``resolver_version`` exist so a projection can PIN the exact resolution it used;
reads never float to "latest" (AR-06).
"""
from __future__ import annotations

from typing import Protocol, runtime_checkable

from pydantic import field_validator, model_validator

from schemas.case_models import StrictModel

RESOLUTION_STATE_VALUES = frozenset({"unresolved", "resolved"})


class ResolutionOutcome(StrictModel):
    """The result of applying a ResolutionMap to one ``(source, cik)``.

    AR-05 honesty invariant: an ``unresolved`` outcome must NEVER carry a canonical ``entity_key``
    (emitting a provisional value in a canonical-named field leaks a de-facto canonical id); a
    ``resolved`` outcome MUST carry one.
    """

    provisional_filer_key: str
    entity_key: str | None = None
    resolution_state: str
    note: str = ""

    @field_validator("provisional_filer_key")
    @classmethod
    def reject_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("provisional_filer_key must be non-empty")
        return value

    @field_validator("resolution_state")
    @classmethod
    def validate_state(cls, value: str) -> str:
        if value not in RESOLUTION_STATE_VALUES:
            allowed = ", ".join(sorted(RESOLUTION_STATE_VALUES))
            raise ValueError(f"resolution_state must be one of {{{allowed}}}; got {value!r}")
        return value

    @model_validator(mode="after")
    def validate_identity_honesty(self) -> "ResolutionOutcome":
        if self.resolution_state == "unresolved" and self.entity_key is not None:
            raise ValueError(
                "an unresolved outcome must not carry a canonical entity_key (AR-05): "
                "a provisional value in a canonical-named field leaks a de-facto canonical id"
            )
        if self.resolution_state == "resolved" and not (self.entity_key and self.entity_key.strip()):
            raise ValueError("a resolved outcome must carry a non-empty entity_key")
        return self


@runtime_checkable
class ResolutionMap(Protocol):
    """The port the spine replaces. Carries a pinned ``(map_version, resolver_version)`` (AR-06)."""

    map_version: str
    resolver_version: str

    def resolve(self, *, source: str, cik: str) -> ResolutionOutcome: ...


class PassthroughNullResolutionMap:
    """v0 default: resolves NOTHING.

    A filer-level ``provisional_filer_key`` from the CIK; ``entity_key`` stays null and
    ``resolution_state`` stays ``unresolved``. It performs no merges (AR-01) and authors no
    canonical identity (the #1 boundary) -- it is the honest "the spine has not resolved this."
    """

    map_version = "passthrough_null_v0"
    resolver_version = "v0"

    def resolve(self, *, source: str, cik: str) -> ResolutionOutcome:
        return ResolutionOutcome(
            provisional_filer_key=f"{source}:CIK{cik}",
            entity_key=None,
            resolution_state="unresolved",
            note="passthrough-null: filer-level, entity not resolved by the spine",
        )


DEFAULT_RESOLUTION_MAP = PassthroughNullResolutionMap()
