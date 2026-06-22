import pytest
from pydantic import ValidationError

from ecr.models import (
    ECR_SOURCE_SIDE_RECEIPT_SCHEMA_VERSION,
    EcrSourceSideReceipt,
    EcrSourceSideReceiptArtifact,
    EcrTimingPosture,
    EcrTimingResidual,
)
from source_capture.models import CUTOFF_POSTURE_VALUES, VisibleFactStatus


def test_carried_pre_cutoff_clears():
    posture = EcrTimingPosture(
        slice_id="s0", carried_cutoff_posture="pre_cutoff", clears_pre_cutoff=True
    )
    assert posture.clears_pre_cutoff is True
    assert posture.residual is None


def test_all_source_cutoff_postures_are_carried_with_bound_clear_condition():
    assert "pre_cutoff" in CUTOFF_POSTURE_VALUES
    for value in sorted(CUTOFF_POSTURE_VALUES):
        posture = EcrTimingPosture(
            slice_id=f"s-{value}",
            carried_cutoff_posture=value,
            clears_pre_cutoff=(value == "pre_cutoff"),
        )
        assert posture.carried_cutoff_posture == value
        assert posture.residual is None
        assert posture.clears_pre_cutoff is (value == "pre_cutoff")


@pytest.mark.parametrize("value", sorted(CUTOFF_POSTURE_VALUES - {"pre_cutoff"}))
def test_carried_non_pre_cutoff_does_not_clear(value):
    posture = EcrTimingPosture(
        slice_id="s0", carried_cutoff_posture=value, clears_pre_cutoff=False
    )
    assert posture.clears_pre_cutoff is False
    assert posture.carried_cutoff_posture == value


def test_xor_both_set_rejected():
    with pytest.raises(ValidationError):
        EcrTimingPosture(
            slice_id="s0",
            carried_cutoff_posture="pre_cutoff",
            residual=EcrTimingResidual(status=VisibleFactStatus.NOT_ATTEMPTED, reason="r"),
            clears_pre_cutoff=True,
        )


def test_xor_neither_set_rejected():
    with pytest.raises(ValidationError):
        EcrTimingPosture(slice_id="s0", clears_pre_cutoff=False)


def test_clears_inconsistent_true_rejected():
    with pytest.raises(ValidationError):
        EcrTimingPosture(
            slice_id="s0", carried_cutoff_posture="post_cutoff", clears_pre_cutoff=True
        )


def test_clears_inconsistent_false_rejected():
    with pytest.raises(ValidationError):
        EcrTimingPosture(
            slice_id="s0", carried_cutoff_posture="pre_cutoff", clears_pre_cutoff=False
        )


def test_out_of_vocab_carried_rejected():
    with pytest.raises(ValidationError):
        EcrTimingPosture(
            slice_id="s0", carried_cutoff_posture="bogus", clears_pre_cutoff=False
        )


def test_extra_field_rejected():
    with pytest.raises(ValidationError):
        EcrTimingPosture(
            slice_id="s0",
            carried_cutoff_posture="pre_cutoff",
            clears_pre_cutoff=True,
            unexpected="x",
        )


def test_residual_known_status_rejected():
    with pytest.raises(ValidationError):
        EcrTimingResidual(status=VisibleFactStatus.KNOWN, reason="r")


def test_residual_empty_reason_rejected():
    with pytest.raises(ValidationError):
        EcrTimingResidual(status=VisibleFactStatus.NOT_ATTEMPTED, reason="  ")


def test_round_trip_carried():
    posture = EcrTimingPosture(
        slice_id="s0", carried_cutoff_posture="pre_cutoff", clears_pre_cutoff=True
    )
    assert EcrTimingPosture.model_validate(posture.model_dump()) == posture


def test_round_trip_residual():
    posture = EcrTimingPosture(
        slice_id="s1",
        residual=EcrTimingResidual(
            status=VisibleFactStatus.UNKNOWN_WITH_REASON, reason="no timestamp"
        ),
        clears_pre_cutoff=False,
    )
    assert EcrTimingPosture.model_validate(posture.model_dump()) == posture


def test_round_trip_residual_json_mode_preserves_status_and_extra_forbid_shape():
    posture = EcrTimingPosture(
        slice_id="s1",
        residual=EcrTimingResidual(
            status=VisibleFactStatus.UNKNOWN_WITH_REASON, reason="no timestamp"
        ),
        clears_pre_cutoff=False,
    )
    dumped = posture.model_dump(mode="json")
    assert dumped == {
        "slice_id": "s1",
        "carried_cutoff_posture": None,
        "residual": {
            "status": "unknown_with_reason",
            "reason": "no timestamp",
        },
        "clears_pre_cutoff": False,
    }
    assert EcrTimingPosture.model_validate(dumped) == posture


def test_source_side_receipt_requires_all_posture_kinds():
    payload = _valid_source_side_receipt_payload()
    del payload["postures"]["source_visibility"]

    with pytest.raises(ValidationError, match="source_visibility"):
        EcrSourceSideReceipt.model_validate(payload)


def test_source_side_receipt_rejects_clear_mismatch():
    payload = _valid_source_side_receipt_payload()
    payload["clears"]["timing"] = False

    with pytest.raises(ValidationError, match="clears"):
        EcrSourceSideReceipt.model_validate(payload)


def test_source_side_receipt_rejects_ref_packet_mismatch():
    payload = _valid_source_side_receipt_payload()
    payload["ref_id"] = "ecr:other-packet:source_side_postures"

    with pytest.raises(ValidationError, match="ref_id"):
        EcrSourceSideReceipt.model_validate(payload)


def test_source_side_receipt_artifact_rejects_duplicate_packet_refs():
    payload = _valid_source_side_receipt_payload()

    with pytest.raises(ValidationError, match="unique"):
        EcrSourceSideReceiptArtifact.model_validate(
            {
                "schema_version": ECR_SOURCE_SIDE_RECEIPT_SCHEMA_VERSION,
                "generated_at": "2026-06-21T00:00:00Z",
                "receipts": [payload, payload],
                "non_claims": ["not_validation"],
            }
        )


def _valid_source_side_receipt_payload() -> dict[str, object]:
    return {
        "source_label": "retail:fixture",
        "packet_id": "packet-1",
        "packet_dir": "packet-dir",
        "ref_id": "ecr:packet-1:source_side_postures",
        "postures": {
            "identity": [
                {
                    "packet_id": "packet-1",
                    "state": "resolved",
                    "clears_identity": True,
                    "reason": None,
                }
            ],
            "inspectability": [
                {
                    "slice_id": "slice-1",
                    "state": "inspectable_verifiable",
                    "clears_inspectable": True,
                    "reason": None,
                }
            ],
            "timing": [
                {
                    "slice_id": "slice-1",
                    "carried_cutoff_posture": "pre_cutoff",
                    "residual": None,
                    "clears_pre_cutoff": True,
                }
            ],
            "source_visibility": [
                {
                    "packet_id": "packet-1",
                    "value": "archive_only",
                    "residual": None,
                    "clears_source_visibility": True,
                    "reason": None,
                }
            ],
        },
        "clears": {
            "identity": True,
            "inspectability": True,
            "timing": True,
            "source_visibility": True,
        },
    }
