import pytest
from pydantic import ValidationError

from ecr.models import EcrInspectabilityPosture, InspectabilityState


def test_verifiable_clears_with_no_reason():
    posture = EcrInspectabilityPosture(
        slice_id="s0",
        state=InspectabilityState.INSPECTABLE_VERIFIABLE,
        clears_inspectable=True,
    )
    assert posture.clears_inspectable is True
    assert posture.reason is None


@pytest.mark.parametrize(
    "state",
    [
        InspectabilityState.INSPECTABLE_REFERENCE_ONLY,
        InspectabilityState.NOT_INSPECTABLE,
    ],
)
def test_non_verifiable_states_do_not_clear_and_require_reason(state):
    posture = EcrInspectabilityPosture(
        slice_id="s0",
        state=state,
        clears_inspectable=False,
        reason="a visible limitation",
    )
    assert posture.clears_inspectable is False
    assert posture.state is state
    assert posture.reason


def test_clears_inconsistent_true_rejected():
    with pytest.raises(ValidationError):
        EcrInspectabilityPosture(
            slice_id="s0",
            state=InspectabilityState.NOT_INSPECTABLE,
            clears_inspectable=True,
            reason="r",
        )


def test_clears_inconsistent_false_rejected():
    with pytest.raises(ValidationError):
        EcrInspectabilityPosture(
            slice_id="s0",
            state=InspectabilityState.INSPECTABLE_VERIFIABLE,
            clears_inspectable=False,
        )


def test_verifiable_with_reason_rejected():
    with pytest.raises(ValidationError):
        EcrInspectabilityPosture(
            slice_id="s0",
            state=InspectabilityState.INSPECTABLE_VERIFIABLE,
            clears_inspectable=True,
            reason="should not be present",
        )


def test_non_verifiable_missing_reason_rejected():
    with pytest.raises(ValidationError):
        EcrInspectabilityPosture(
            slice_id="s0",
            state=InspectabilityState.INSPECTABLE_REFERENCE_ONLY,
            clears_inspectable=False,
        )


def test_non_verifiable_blank_reason_rejected():
    with pytest.raises(ValidationError):
        EcrInspectabilityPosture(
            slice_id="s0",
            state=InspectabilityState.NOT_INSPECTABLE,
            clears_inspectable=False,
            reason="   ",
        )


def test_out_of_vocab_state_rejected():
    with pytest.raises(ValidationError):
        EcrInspectabilityPosture(
            slice_id="s0", state="bogus", clears_inspectable=False, reason="r"
        )


def test_extra_field_rejected():
    with pytest.raises(ValidationError):
        EcrInspectabilityPosture(
            slice_id="s0",
            state=InspectabilityState.INSPECTABLE_VERIFIABLE,
            clears_inspectable=True,
            unexpected="x",
        )


def test_round_trip_verifiable():
    posture = EcrInspectabilityPosture(
        slice_id="s0",
        state=InspectabilityState.INSPECTABLE_VERIFIABLE,
        clears_inspectable=True,
    )
    assert EcrInspectabilityPosture.model_validate(posture.model_dump()) == posture


def test_round_trip_reference_only_json_mode():
    posture = EcrInspectabilityPosture(
        slice_id="s1",
        state=InspectabilityState.INSPECTABLE_REFERENCE_ONLY,
        clears_inspectable=False,
        reason="reference only",
    )
    dumped = posture.model_dump(mode="json")
    assert dumped == {
        "slice_id": "s1",
        "state": "inspectable_reference_only",
        "clears_inspectable": False,
        "reason": "reference only",
    }
    assert EcrInspectabilityPosture.model_validate(dumped) == posture
