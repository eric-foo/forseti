"""I/O verifier for JSG-01 claim-support assertions (the slice-C body-read concern).

The pure composer (``composer.py``) never reads bytes. This module does: it confirms
that a claim-support assertion's verbatim ``quoted_span`` is actually present in the
hash-anchored preserved-file body it cites. This is the L2 guard — "a mechanically
successful capture is NOT claim-support until the body backs the claim" — distilled
from the Beauty Pie #3 pilot, where a clean ``how-it-works`` capture was nearly used
to support membership-pricing facts its body did not contain.

Contract (mirrors the composer's block-don't-repair discipline):

- Block, don't repair: any resolution, integrity, or presence failure raises
  ``ClaimSupportError`` — a visible block, never a silent pass and never a
  re-key toward a better-matching file.
- Conditional: nothing runs unless a claim-support assertion is supplied. Bindings
  that assert no span (e.g. aggregate/derived claims, or legacy bindings) are not
  blocked — the guard simply does not cover them.
- Integrity-anchored: the span is checked against the bytes ONLY after the file's
  sha256 is recomputed and matched (AR-04 ``raw_stored_bytes`` basis), so a tampered
  or swapped body cannot satisfy the check.

Scope — what this proves and does NOT prove (VERIFY-FIRING honesty): it proves the
asserted ``quoted_span`` is PRESENT in the hash-verified body — a necessary precondition.
It does NOT prove the span is specific enough, or that it semantically supports
``claim_id``; that judgment stays with the asserting author. And it fires only WHEN
INVOKED (by a caller or the contract test) and WHEN an assertion is declared — it is not
an automatic write-time gate on every assembly. Wiring it into a mandatory assembly/CI
boundary is a deferred follow-on (no assembly runner exists yet; JSG-01 is frozen).
Present-and-contract-tested is not the same as auto-firing on real assemblies.

Limitation (v0): the span is matched as an EXACT UTF-8 byte substring of the raw
stored body. It is therefore false-negative-biased on rendered text that differs from
the raw bytes (HTML entity-encoding, whitespace normalization, tag splits). Fail-closed
is the deliberate bias for an integrity guard; a normalized match mode is a future option.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

from evidence_binding.models import Jsg01ClaimSupportAssertion
from source_capture.models import SourceCapturePacket


class ClaimSupportError(ValueError):
    """A claim-support assertion that does not resolve or verify: a visible block."""


def verify_claim_support(
    *,
    assertion: Jsg01ClaimSupportAssertion,
    packet: SourceCapturePacket,
    packet_dir: Path,
) -> None:
    """Confirm the assertion's quoted span is present in the hash-anchored cited body.

    Raises ``ClaimSupportError`` on any key, integrity, or presence failure
    (block-don't-repair); returns ``None`` when the span is verified present.
    """
    if assertion.packet_id != packet.packet_id:
        raise ClaimSupportError(
            f"claim-support packet_id {assertion.packet_id!r} does not match the "
            f"supplied packet {packet.packet_id!r}; block-don't-repair."
        )

    slices = {source_slice.slice_id: source_slice for source_slice in packet.source_slices}
    source_slice = slices.get(assertion.evidence_slice_id)
    if source_slice is None:
        raise ClaimSupportError(
            f"evidence_slice_id {assertion.evidence_slice_id!r} names no slice in "
            f"packet {packet.packet_id!r}; block-don't-repair."
        )

    if assertion.preserved_file_id not in source_slice.preserved_file_ids:
        raise ClaimSupportError(
            f"preserved_file_id {assertion.preserved_file_id!r} is not referenced by "
            f"slice {assertion.evidence_slice_id!r}; block-don't-repair."
        )

    files = {item.file_id: item for item in packet.preserved_files}
    preserved = files.get(assertion.preserved_file_id)
    if preserved is None:
        raise ClaimSupportError(
            f"preserved_file_id {assertion.preserved_file_id!r} names no preserved file "
            f"in packet {packet.packet_id!r}; block-don't-repair."
        )

    # Containment: an integrity verifier must not read outside the packet dir, even if a
    # packet declares an escaping or absolute relative_packet_path. The producer-side
    # constraint on relative_packet_path belongs in source_capture.models; this is a
    # defensive floor in the verifier itself.
    resolved_body = (packet_dir / preserved.relative_packet_path).resolve()
    try:
        resolved_body.relative_to(packet_dir.resolve())
    except ValueError:
        raise ClaimSupportError(
            f"preserved path {preserved.relative_packet_path!r} for "
            f"{assertion.preserved_file_id!r} resolves outside the packet dir; "
            f"block-don't-repair."
        )
    if not resolved_body.is_file():
        raise ClaimSupportError(
            f"preserved body for {assertion.preserved_file_id!r} not found at "
            f"{preserved.relative_packet_path!r} under the packet dir; block-don't-repair."
        )

    data = resolved_body.read_bytes()
    recomputed = hashlib.sha256(data).hexdigest()
    if recomputed != preserved.sha256:
        raise ClaimSupportError(
            f"preserved body sha256 mismatch for {assertion.preserved_file_id!r} "
            f"(recomputed {recomputed}, manifest {preserved.sha256}); block-don't-repair."
        )
    if assertion.verified_sha256 != preserved.sha256:
        raise ClaimSupportError(
            f"assertion verified_sha256 {assertion.verified_sha256!r} disagrees with the "
            f"preserved file sha256 {preserved.sha256!r}; block-don't-repair."
        )

    if assertion.quoted_span.encode("utf-8") not in data:
        raise ClaimSupportError(
            f"quoted_span for claim {assertion.claim_id!r} is not present in the "
            f"hash-verified body of {assertion.preserved_file_id!r}: the capture does not "
            f"support the claim (L2). block-don't-repair."
        )
