import pytest
from pydantic import ValidationError

from ecr.models import EcrIdentityPosture, IdentityState


def test_resolved_clears_with_no_reason():
    posture = EcrIdentityPosture(
        packet_id="pkt", state=IdentityState.RESOLVED, clears_identity=True
    )
    assert posture.clears_identity is True
    assert posture.reason is None


def test_family_only_clears_but_carries_reason():
    # the key nuance: family_only clears AND carries a limitation
    posture = EcrIdentityPosture(
        packet_id="pkt",
        state=IdentityState.FAMILY_ONLY,
        clears_identity=True,
        reason="family known, specific identity not resolved",
    )
    assert posture.clears_identity is True
    assert posture.reason


def test_unresolved_does_not_clear_with_reason():
    posture = EcrIdentityPosture(
        packet_id="pkt",
        state=IdentityState.UNRESOLVED,
        clears_identity=False,
        reason="family not known",
    )
    assert posture.clears_identity is False
    assert posture.reason


def test_resolved_with_clears_false_rejected():
    with pytest.raises(ValidationError):
        EcrIdentityPosture(
            packet_id="pkt", state=IdentityState.RESOLVED, clears_identity=False
        )


def test_family_only_with_clears_false_rejected():
    with pytest.raises(ValidationError):
        EcrIdentityPosture(
            packet_id="pkt",
            state=IdentityState.FAMILY_ONLY,
            clears_identity=False,
            reason="r",
        )


def test_unresolved_with_clears_true_rejected():
    with pytest.raises(ValidationError):
        EcrIdentityPosture(
            packet_id="pkt",
            state=IdentityState.UNRESOLVED,
            clears_identity=True,
            reason="r",
        )


def test_resolved_with_reason_rejected():
    with pytest.raises(ValidationError):
        EcrIdentityPosture(
            packet_id="pkt",
            state=IdentityState.RESOLVED,
            clears_identity=True,
            reason="should not be present",
        )


@pytest.mark.parametrize("state", [IdentityState.FAMILY_ONLY, IdentityState.UNRESOLVED])
def test_non_resolved_missing_reason_rejected(state):
    with pytest.raises(ValidationError):
        EcrIdentityPosture(
            packet_id="pkt",
            state=state,
            clears_identity=(state == IdentityState.FAMILY_ONLY),
        )


def test_non_resolved_blank_reason_rejected():
    with pytest.raises(ValidationError):
        EcrIdentityPosture(
            packet_id="pkt",
            state=IdentityState.UNRESOLVED,
            clears_identity=False,
            reason="   ",
        )


def test_out_of_vocab_state_rejected():
    with pytest.raises(ValidationError):
        EcrIdentityPosture(
            packet_id="pkt", state="bogus", clears_identity=False, reason="r"
        )


def test_extra_field_rejected():
    with pytest.raises(ValidationError):
        EcrIdentityPosture(
            packet_id="pkt",
            state=IdentityState.RESOLVED,
            clears_identity=True,
            unexpected="x",
        )


def test_round_trip_resolved():
    posture = EcrIdentityPosture(
        packet_id="pkt", state=IdentityState.RESOLVED, clears_identity=True
    )
    assert EcrIdentityPosture.model_validate(posture.model_dump()) == posture


def test_round_trip_family_only_json_mode():
    posture = EcrIdentityPosture(
        packet_id="pkt",
        state=IdentityState.FAMILY_ONLY,
        clears_identity=True,
        reason="family only",
    )
    dumped = posture.model_dump(mode="json")
    assert dumped == {
        "packet_id": "pkt",
        "state": "family_only",
        "clears_identity": True,
        "reason": "family only",
    }
    assert EcrIdentityPosture.model_validate(dumped) == posture
