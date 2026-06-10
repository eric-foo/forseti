"""Source-agnostic spine tests for rung-1.5 ("isolate, don't abstract", Option A).

These prove the embedded-payload primitives carry NO price/vendor semantics: a
non-price toy payload extracts at a caller-supplied anchor and certifies through
the scaffold with a caller-supplied domain check, and the honesty backstop (a
body that is an undecoded/encoded shell can never certify) still fires on the
generic path. This is what turns "generic" from a claim into a demonstration.
"""
from source_capture.price_payload_extraction import (
    CertificationCheck,
    PayloadBody,
    certify_payload,
    extract_object_at_anchor,
)


def test_extract_object_at_anchor_is_source_agnostic():
    # a non-price embedded object, recovered at a caller-supplied anchor, with JS
    # unquoted keys -- no 'chatgpt.'/price assumptions reach the spine primitive.
    text = "x=flags:{a:{on:1},b:{on:0}};"
    obj = extract_object_at_anchor(text, r"flags:\{")
    assert obj == {"a": {"on": 1}, "b": {"on": 0}}


def test_extract_object_at_anchor_absent_anchor_is_a_loud_miss():
    import pytest

    with pytest.raises(ValueError):
        extract_object_at_anchor("no anchor here", r"flags:\{")


def test_certify_payload_certifies_a_non_price_payload():
    obj = {"a": {"on": 1}, "b": {"on": 0}}
    domain_ok = CertificationCheck("all_flags_present", set(obj) == {"a", "b"}, "")
    v = certify_payload(
        bodies=[PayloadBody("page", "content_unverified", 200, None)],
        payload_parsed=bool(obj),
        domain_checks=[domain_ok],
        discriminator="toy_payload_v0",
    )
    assert v.certified, [c.name for c in v.checks if not c.passed]
    # the scaffold note is generic (no price/currency wording) when none supplied
    assert "INTERNAL-CONSISTENCY" in v.as_dict()["discriminator_note"]


def test_certify_payload_refuses_an_encoded_body_generically():
    # honesty backstop transfers to the generic path: an undecoded/encoded body
    # never certifies, even with every domain check passing.
    v = certify_payload(
        bodies=[PayloadBody("page", "content_unverified", 200, "encoded_body_uninspectable")],
        payload_parsed=True,
        domain_checks=[CertificationCheck("ok", True, "")],
        discriminator="toy_payload_v0",
    )
    assert not v.certified
    assert "page_body_inspectable" in {c.name for c in v.checks if not c.passed}


def test_certify_payload_refuses_a_200_with_no_payload():
    # a 200 alone is never certified as content: no parsed payload -> refuse.
    v = certify_payload(
        bodies=[PayloadBody("page", "content_unverified", 200, None)],
        payload_parsed=False,
        domain_checks=[CertificationCheck("ok", True, "")],
        discriminator="toy_payload_v0",
    )
    assert not v.certified
    assert "payload_parsed" in {c.name for c in v.checks if not c.passed}


def test_certify_payload_refuses_without_backing_bodies():
    # vacuous-pass guard: a parsed payload with NO backing body cannot certify.
    v = certify_payload(
        bodies=[],
        payload_parsed=True,
        domain_checks=[CertificationCheck("ok", True, "")],
        discriminator="toy_payload_v0",
    )
    assert not v.certified
    assert "body_provenance_present" in {c.name for c in v.checks if not c.passed}


def test_certify_payload_refuses_without_domain_checks():
    # vacuous-pass guard: transport + parse alone (no domain consistency check)
    # cannot certify -- "certified" must mean internal consistency, not "an object exists".
    v = certify_payload(
        bodies=[PayloadBody("page", "content_unverified", 200, None)],
        payload_parsed=True,
        domain_checks=[],
        discriminator="toy_payload_v0",
    )
    assert not v.certified
    assert "domain_checks_present" in {c.name for c in v.checks if not c.passed}
