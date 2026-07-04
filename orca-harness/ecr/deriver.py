"""ECR SP-3 source-side timing deriver (slice-1).

A pure M1 carry of each source slice's already-closed ``cutoff_posture`` into an
``EcrTimingPosture``. It coins no vocabulary, performs no I/O, does not mutate
the input packet, binds no ``EvidenceUnit``, and makes no JSG-01, scoring, or
readiness claim. The packet->EvidenceUnit binding and the
``cutoff_posture -> pre_decision_status`` mapping are deliberately out of scope
(slice-2).
"""
from __future__ import annotations

import re

from ecr.models import (
    SOURCE_VISIBILITY_CLEARING_VALUES,
    EcrIdentityPosture,
    EcrInspectabilityPosture,
    EcrSourceVisibilityPosture,
    EcrTimingPosture,
    EcrTimingResidual,
    IdentityState,
    InspectabilityState,
    SourceVisibilityResidual,
    SourceVisibilityValue,
)
from source_capture.models import SourceCapturePacket, VisibleFactStatus

# Processing-policy token for the consumption seam's obligation envelope: bump on
# any behavior change to the four derivers below so already-acknowledged packets
# re-surface and re-derive under the new policy (the packet manifest is immutable,
# so this token is ECR's only re-trigger input).
ECR_DERIVER_VERSION = "1"


def derive_timing_postures(packet: SourceCapturePacket) -> list[EcrTimingPosture]:
    """Derive the SP-3 timing posture for each source slice, in slice order.

    For each slice, the slice's ``timing.cutoff_posture`` (a ``VisibleFact``) is
    either M1-carried verbatim when its status is KNOWN (clearing only on
    ``"pre_cutoff"``) or recorded as a named residual when the status is not
    KNOWN, preserving the producer's status and reason. One posture is returned
    per source slice.
    """
    postures: list[EcrTimingPosture] = []
    for source_slice in packet.source_slices:
        fact = source_slice.timing.cutoff_posture
        if fact.status == VisibleFactStatus.KNOWN:
            postures.append(
                EcrTimingPosture(
                    slice_id=source_slice.slice_id,
                    carried_cutoff_posture=fact.value,
                    clears_pre_cutoff=fact.value == "pre_cutoff",
                )
            )
        else:
            postures.append(
                EcrTimingPosture(
                    slice_id=source_slice.slice_id,
                    residual=EcrTimingResidual(status=fact.status, reason=fact.reason),
                    clears_pre_cutoff=False,
                )
            )
    return postures


_SHA256_HEX = re.compile(r"\A[0-9a-fA-F]{64}\Z")
_PLACEHOLDER_SHA256 = "0" * 64


def _is_verifiable_sha256(value: str) -> bool:
    """D-C: a non-placeholder sha256 is 64 hex chars (case-insensitive) and not
    the all-zero sentinel.

    The producer schema does not constrain ``sha256`` shape, so the deriver must
    make this discrimination -- a hash-shaped placeholder is not verifiability.
    """
    return bool(_SHA256_HEX.match(value)) and value.lower() != _PLACEHOLDER_SHA256


def derive_inspectability_postures(
    packet: SourceCapturePacket,
) -> list[EcrInspectabilityPosture]:
    """Derive the SP-2 inspectability posture for each source slice, in slice order.

    Per slice, fail-closed "all referenced files must verify":

    - ``inspectable_verifiable`` (clears) iff the slice references >=1 preserved
      file AND every referenced file has a non-placeholder sha256.
    - ``inspectable_reference_only`` (does not clear) when something is pointable
      but not fully verifiable: referenced files exist but not all verify, or no
      files are referenced yet the slice locator is KNOWN.
    - ``not_inspectable`` (does not clear) when nothing is inspectable: no
      referenced files and the locator is not KNOWN.

    Pure: no I/O, no packet mutation, no ``EvidenceUnit`` binding. The integrity
    hash is read by reference and recomputed elsewhere, never trusted here. One
    posture is returned per source slice.
    """
    files_by_id = {pf.file_id: pf for pf in packet.preserved_files}
    postures: list[EcrInspectabilityPosture] = []
    for source_slice in packet.source_slices:
        referenced = [
            files_by_id[file_id]
            for file_id in source_slice.preserved_file_ids
            if file_id in files_by_id
        ]
        unverifiable = [pf for pf in referenced if not _is_verifiable_sha256(pf.sha256)]
        locator_known = source_slice.locator.status == VisibleFactStatus.KNOWN

        if referenced and not unverifiable:
            postures.append(
                EcrInspectabilityPosture(
                    slice_id=source_slice.slice_id,
                    state=InspectabilityState.INSPECTABLE_VERIFIABLE,
                    clears_inspectable=True,
                )
            )
        elif referenced or locator_known:
            if referenced:
                bad = ", ".join(sorted(pf.file_id for pf in unverifiable))
                reason = (
                    f"referenced preserved file(s) with placeholder or invalid "
                    f"sha256: {bad}; bytes are held but integrity is not verifiable."
                )
            else:
                reason = (
                    "no preserved file referenced; slice locator is known "
                    "(reference only)."
                )
            postures.append(
                EcrInspectabilityPosture(
                    slice_id=source_slice.slice_id,
                    state=InspectabilityState.INSPECTABLE_REFERENCE_ONLY,
                    clears_inspectable=False,
                    reason=reason,
                )
            )
        else:
            postures.append(
                EcrInspectabilityPosture(
                    slice_id=source_slice.slice_id,
                    state=InspectabilityState.NOT_INSPECTABLE,
                    clears_inspectable=False,
                    reason="no preserved file referenced and slice locator is not known.",
                )
            )
    return postures


def _is_specific(value: str) -> bool:
    """A plain producer string is "specific" when it is non-empty after strip.

    Minimal placeholder discrimination (coin no sentinel list): an empty or
    whitespace-only value is not a usable identity component.
    """
    return bool(value and value.strip())


def derive_identity_postures(packet: SourceCapturePacket) -> list[EcrIdentityPosture]:
    """Derive the SP-1 source-identity posture for the packet.

    Per-packet (identity is a whole-packet fact): returns exactly one
    ``EcrIdentityPosture`` in a list, for shape-consistency with the per-slice
    derivers. M2 derived-read with an M3 stop:

    - ``unresolved`` (does not clear) when ``source_family`` is not specific --
      the M3 stop; the ECR names the limitation and never invents an identity.
    - ``resolved`` (clears) when ``source_family`` and ``source_surface`` are
      specific AND ``source_locator`` is KNOWN with a specific value.
    - ``family_only`` (clears, with a specificity limitation) otherwise -- the
      family is known but the full specific identity is not.

    Pure: no I/O, no packet mutation, no ``EvidenceUnit`` binding. Binds the real
    producer fields and coins no producer vocabulary; actor/audience is
    mark-if-unavailable and does not gate ``resolved``.
    """
    family_specific = _is_specific(packet.source_family)
    surface_specific = _is_specific(packet.source_surface)
    locator = packet.source_locator
    locator_specific = (
        locator.status == VisibleFactStatus.KNOWN
        and bool(locator.value)
        and bool(locator.value.strip())
    )

    if not family_specific:
        posture = EcrIdentityPosture(
            packet_id=packet.packet_id,
            state=IdentityState.UNRESOLVED,
            clears_identity=False,
            reason=(
                "source_family is empty or whitespace-only; source identity is "
                "not resolved (not invented)."
            ),
        )
    elif surface_specific and locator_specific:
        posture = EcrIdentityPosture(
            packet_id=packet.packet_id,
            state=IdentityState.RESOLVED,
            clears_identity=True,
        )
    else:
        posture = EcrIdentityPosture(
            packet_id=packet.packet_id,
            state=IdentityState.FAMILY_ONLY,
            clears_identity=True,
            reason=(
                "source_family is known but the full specific identity "
                "(source_surface and/or a specific source_locator) is not resolved."
            ),
        )
    return [posture]


# SP-6 archive-slice identification: the producer's slice_id naming convention
# (a free str -- "implemented convention, not a contracted field"), isolated here
# so the delta-sensitivity is contained to one spot.
_ARCHIVE_SLICE_IDS = frozenset({"archive_snapshot_body", "archive_availability"})
_ARCHIVE_BODY_SLICE_ID = "archive_snapshot_body"


def _archive_body_slice(packet: SourceCapturePacket):
    """The archived-body slice (carries D = its cutoff_posture), or None."""
    for source_slice in packet.source_slices:
        if source_slice.slice_id == _ARCHIVE_BODY_SLICE_ID:
            return source_slice
    return None


def _has_current_body(packet: SourceCapturePacket) -> bool:
    """C: a current (non-archive) slice references >=1 preserved file."""
    return any(
        source_slice.slice_id not in _ARCHIVE_SLICE_IDS and source_slice.preserved_file_ids
        for source_slice in packet.source_slices
    )


def _source_visibility_posture(
    packet_id: str,
    *,
    value: SourceVisibilityValue | None = None,
    residual: SourceVisibilityResidual | None = None,
    reason: str | None = None,
) -> EcrSourceVisibilityPosture:
    clears = value in SOURCE_VISIBILITY_CLEARING_VALUES if value is not None else False
    return EcrSourceVisibilityPosture(
        packet_id=packet_id,
        value=value,
        residual=residual,
        clears_source_visibility=clears,
        reason=reason,
    )


def derive_source_visibility_postures(
    packet: SourceCapturePacket,
) -> list[EcrSourceVisibilityPosture]:
    """Derive the SP-6 source-visibility posture for the packet.

    Per-packet (flat) M2 derived-read realizing the ratified residual-first
    decision table over the producer's already-closed facts: returns exactly one
    ``EcrSourceVisibilityPosture`` in a list (shape-consistent with the per-slice
    derivers). Inputs, all read from the packet:

    - A = ``packet.archive_history_posture`` (packet-level; closed
      ``{archived, attempt_failed}`` on KNOWN, else its ``VisibleFactStatus``);
    - D = the archive-body slice's ``cutoff_posture`` class (the 641cf15
      amendment: a pre/post CLASS, never a timestamp);
    - C = a current (non-archive) slice with a preserved file.

    Comparison rows route to ``RESIDUAL_COMPARISON_NOT_RECORDED`` (M / D2 absent);
    the immutable/official ``not_applicable`` clear (the row-1 X condition) is
    deferred, so a not-archived packet with no current body residualizes
    ``RESIDUAL_NO_VISIBILITY_BASIS`` rather than inventing a clear.

    Pure: no I/O, no packet mutation, no ``EvidenceUnit`` binding; no JSG-01,
    scoring, or readiness claim.
    """
    packet_id = packet.packet_id
    archive = packet.archive_history_posture
    archive_known = archive.status == VisibleFactStatus.KNOWN

    if archive_known and archive.value == "archived":
        body = _archive_body_slice(packet)
        cutoff = body.timing.cutoff_posture if body is not None else None
        d_class = (
            cutoff.value
            if cutoff is not None and cutoff.status == VisibleFactStatus.KNOWN
            else None
        )
        current = _has_current_body(packet)
        if d_class == "pre_cutoff":
            if current:
                return [
                    _source_visibility_posture(
                        packet_id,
                        residual=SourceVisibilityResidual.RESIDUAL_COMPARISON_NOT_RECORDED,
                        reason=(
                            "pre-cutoff archive and a current capture body are both "
                            "present, but no recorded archive-vs-current comparison "
                            "fact exists (D2/M absent)."
                        ),
                    )
                ]
            return [
                _source_visibility_posture(packet_id, value=SourceVisibilityValue.ARCHIVE_ONLY)
            ]
        if d_class == "post_cutoff":
            if current:
                return [
                    _source_visibility_posture(
                        packet_id,
                        residual=SourceVisibilityResidual.RESIDUAL_ARCHIVE_POST_CUTOFF_WITH_CURRENT,
                        reason=(
                            "archive is post-cutoff dated and a current capture body "
                            "is present; cannot establish pre-cutoff visibility."
                        ),
                    )
                ]
            return [
                _source_visibility_posture(
                    packet_id, value=SourceVisibilityValue.ARCHIVE_POST_CUTOFF_ONLY
                )
            ]
        return [
            _source_visibility_posture(
                packet_id,
                residual=SourceVisibilityResidual.RESIDUAL_ARCHIVE_DATE_UNKNOWN,
                reason=(
                    "archive history is 'archived' but the archive snapshot's "
                    "pre/post-cutoff class is not resolvable from the archive slice "
                    "cutoff_posture."
                ),
            )
        ]

    if archive_known and archive.value == "attempt_failed":
        return [
            _source_visibility_posture(packet_id, value=SourceVisibilityValue.ATTEMPT_FAILED)
        ]

    if archive.status == VisibleFactStatus.UNKNOWN_WITH_REASON:
        return [
            _source_visibility_posture(
                packet_id,
                residual=SourceVisibilityResidual.RESIDUAL_ARCHIVE_POSTURE_UNKNOWN,
                reason=(
                    "archive_history_posture is unknown_with_reason; the archive "
                    "posture is not resolved."
                ),
            )
        ]

    if _has_current_body(packet):
        return [
            _source_visibility_posture(
                packet_id, value=SourceVisibilityValue.CURRENT_CAPTURE_ONLY
            )
        ]

    if archive.status == VisibleFactStatus.NOT_ATTEMPTED:
        return [
            _source_visibility_posture(packet_id, value=SourceVisibilityValue.NOT_ATTEMPTED)
        ]

    return [
        _source_visibility_posture(
            packet_id,
            residual=SourceVisibilityResidual.RESIDUAL_NO_VISIBILITY_BASIS,
            reason="no archived body and no current capture body; no source-visibility basis.",
        )
    ]
