"""Contract tests for the L2 claim-support verifier (evidence_binding.verifier).

The guard: a captured page is not claim-support until its hash-anchored body actually
contains the asserted span. Under-case (absent span) blocks; over-edge (present span)
passes; omitted (no assertion) leaves the pure composer untouched.
"""
from __future__ import annotations

import hashlib

import pytest
from _ecr_builders import build_packet
from pydantic import ValidationError

from evidence_binding import (
    ClaimSupportError,
    Jsg01ClaimSupportAssertion,
    Jsg01EvidenceBinding,
    Jsg01EvidenceRecord,
    verify_claim_support,
)

# A small UTF-8 HTML-ish body. Contains the £59 annual wording; deliberately lacks any
# spending-limit wording (the Beauty Pie #3 gap that motivated L2).
BODY = (
    "<html><body>Beauty Pie membership is £10 a month. "
    "The Plus membership is £59 a year.</body></html>"
).encode("utf-8")


def _packet_with_body(tmp_path, body: bytes = BODY, *, file_id="f_body", slice_id="s_body", packet_id="pkt-test"):
    """A producer-valid packet whose preserved file's real bytes live on disk.

    build_packet sets relative_packet_path == file_id, so writing tmp_path/<file_id>
    makes the verifier's packet_dir / relative_packet_path resolve to these bytes.
    """
    sha = hashlib.sha256(body).hexdigest()
    packet = build_packet(
        [{"id": slice_id, "files": [(file_id, sha)], "locator_known": True, "cutoff": "pre_cutoff"}],
        packet_id=packet_id,
    )
    (tmp_path / file_id).write_bytes(body)
    return packet, sha


def _assertion(sha, **overrides):
    kwargs = dict(
        claim_id="C1",
        evidence_id="E1",
        packet_id="pkt-test",
        evidence_slice_id="s_body",
        preserved_file_id="f_body",
        quoted_span="£59 a year",
        verified_sha256=sha,
    )
    kwargs.update(overrides)
    return Jsg01ClaimSupportAssertion(**kwargs)


# ---- over-edge: a present span verifies clean ----

def test_present_span_passes(tmp_path):
    packet, sha = _packet_with_body(tmp_path)
    assert verify_claim_support(assertion=_assertion(sha), packet=packet, packet_dir=tmp_path) is None


# ---- under-case: an absent span is the L2 catch ----

def test_absent_span_blocks(tmp_path):
    packet, sha = _packet_with_body(tmp_path)
    with pytest.raises(ClaimSupportError, match="not present in the hash-verified body"):
        verify_claim_support(
            assertion=_assertion(sha, quoted_span="£200 spending limit"),
            packet=packet,
            packet_dir=tmp_path,
        )


# ---- integrity guards: tamper + fingerprint disagreement ----

def test_body_tamper_blocks(tmp_path):
    packet, sha = _packet_with_body(tmp_path)
    # overwrite the on-disk body with different bytes than the recorded sha256
    (tmp_path / "f_body").write_bytes(BODY + b" tampered")
    with pytest.raises(ClaimSupportError, match="sha256 mismatch"):
        verify_claim_support(assertion=_assertion(sha), packet=packet, packet_dir=tmp_path)


def test_assertion_fingerprint_disagreement_blocks(tmp_path):
    packet, sha = _packet_with_body(tmp_path)
    with pytest.raises(ClaimSupportError, match="disagrees with the preserved file"):
        verify_claim_support(assertion=_assertion(sha, verified_sha256="b" * 64), packet=packet, packet_dir=tmp_path)


# ---- resolution guards: block, don't repair ----

def test_packet_id_mismatch_blocks(tmp_path):
    packet, sha = _packet_with_body(tmp_path)
    with pytest.raises(ClaimSupportError, match="does not match the supplied packet"):
        verify_claim_support(assertion=_assertion(sha, packet_id="pkt-other"), packet=packet, packet_dir=tmp_path)


def test_unknown_slice_blocks(tmp_path):
    packet, sha = _packet_with_body(tmp_path)
    with pytest.raises(ClaimSupportError, match="names no slice"):
        verify_claim_support(assertion=_assertion(sha, evidence_slice_id="s_missing"), packet=packet, packet_dir=tmp_path)


def test_preserved_file_not_in_slice_blocks(tmp_path):
    packet, sha = _packet_with_body(tmp_path)
    with pytest.raises(ClaimSupportError, match="not referenced by slice"):
        verify_claim_support(assertion=_assertion(sha, preserved_file_id="f_other"), packet=packet, packet_dir=tmp_path)


def test_missing_body_file_blocks(tmp_path):
    packet, sha = _packet_with_body(tmp_path)
    (tmp_path / "f_body").unlink()
    with pytest.raises(ClaimSupportError, match="not found"):
        verify_claim_support(assertion=_assertion(sha), packet=packet, packet_dir=tmp_path)


# ---- model guards + separation from the ratified binding ----

def test_blank_fields_rejected():
    with pytest.raises(ValidationError):
        _assertion("a" * 64, claim_id="   ")
    with pytest.raises(ValidationError):
        _assertion("a" * 64, quoted_span="")


def test_claim_support_is_separate_from_the_reference_never_merge_binding():
    # The assertion is its OWN model; Jsg01EvidenceBinding stays three keys (no content),
    # and the composed record carries no claim/span field.
    assert set(Jsg01EvidenceBinding.model_fields) == {"evidence_id", "packet_id", "evidence_slice_id"}
    assert not any(
        "claim" in name or "span" in name for name in Jsg01EvidenceRecord.model_fields
    )


# ---- containment: never read outside the packet dir (de-correlated review hardening) ----

def test_path_escape_blocks(tmp_path):
    # A packet whose preserved relative_packet_path escapes the packet dir must be refused
    # BEFORE any read — an integrity verifier does not follow an escaping/absolute path.
    sha = hashlib.sha256(BODY).hexdigest()
    packet = build_packet(
        [{"id": "s_body", "files": [("../escape.bin", sha)], "locator_known": True, "cutoff": "pre_cutoff"}],
        packet_id="pkt-test",
    )
    assertion = Jsg01ClaimSupportAssertion(
        claim_id="C1",
        evidence_id="E1",
        packet_id="pkt-test",
        evidence_slice_id="s_body",
        preserved_file_id="../escape.bin",
        quoted_span="£59 a year",
        verified_sha256=sha,
    )
    with pytest.raises(ClaimSupportError, match="resolves outside the packet dir"):
        verify_claim_support(assertion=assertion, packet=packet, packet_dir=tmp_path)
