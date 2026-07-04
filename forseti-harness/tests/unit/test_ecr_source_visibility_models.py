import pytest
from pydantic import ValidationError

from ecr.models import (
    EcrSourceVisibilityPosture,
    SourceVisibilityResidual,
    SourceVisibilityValue,
)


def test_archive_only_clears_with_no_reason():
    posture = EcrSourceVisibilityPosture(
        packet_id="pkt",
        value=SourceVisibilityValue.ARCHIVE_ONLY,
        clears_source_visibility=True,
    )
    assert posture.clears_source_visibility is True
    assert posture.residual is None


def test_not_applicable_clears():
    posture = EcrSourceVisibilityPosture(
        packet_id="pkt",
        value=SourceVisibilityValue.NOT_APPLICABLE,
        clears_source_visibility=True,
    )
    assert posture.clears_source_visibility is True


def test_non_clearing_value():
    posture = EcrSourceVisibilityPosture(
        packet_id="pkt",
        value=SourceVisibilityValue.CURRENT_CAPTURE_ONLY,
        clears_source_visibility=False,
    )
    assert posture.clears_source_visibility is False


def test_residual_does_not_clear_with_reason():
    posture = EcrSourceVisibilityPosture(
        packet_id="pkt",
        residual=SourceVisibilityResidual.RESIDUAL_ARCHIVE_DATE_UNKNOWN,
        clears_source_visibility=False,
        reason="date unknown",
    )
    assert posture.clears_source_visibility is False
    assert posture.value is None


def test_value_and_residual_both_set_rejected():
    with pytest.raises(ValidationError):
        EcrSourceVisibilityPosture(
            packet_id="pkt",
            value=SourceVisibilityValue.ARCHIVE_ONLY,
            residual=SourceVisibilityResidual.RESIDUAL_ARCHIVE_DATE_UNKNOWN,
            clears_source_visibility=True,
            reason="x",
        )


def test_neither_value_nor_residual_rejected():
    with pytest.raises(ValidationError):
        EcrSourceVisibilityPosture(packet_id="pkt", clears_source_visibility=False)


def test_archive_only_with_clears_false_rejected():
    with pytest.raises(ValidationError):
        EcrSourceVisibilityPosture(
            packet_id="pkt",
            value=SourceVisibilityValue.ARCHIVE_ONLY,
            clears_source_visibility=False,
        )


def test_non_clearing_value_with_clears_true_rejected():
    with pytest.raises(ValidationError):
        EcrSourceVisibilityPosture(
            packet_id="pkt",
            value=SourceVisibilityValue.ARCHIVE_POST_CUTOFF_ONLY,
            clears_source_visibility=True,
        )


def test_residual_with_clears_true_rejected():
    with pytest.raises(ValidationError):
        EcrSourceVisibilityPosture(
            packet_id="pkt",
            residual=SourceVisibilityResidual.RESIDUAL_NO_VISIBILITY_BASIS,
            clears_source_visibility=True,
            reason="r",
        )


def test_residual_missing_reason_rejected():
    with pytest.raises(ValidationError):
        EcrSourceVisibilityPosture(
            packet_id="pkt",
            residual=SourceVisibilityResidual.RESIDUAL_NO_VISIBILITY_BASIS,
            clears_source_visibility=False,
        )


def test_residual_blank_reason_rejected():
    with pytest.raises(ValidationError):
        EcrSourceVisibilityPosture(
            packet_id="pkt",
            residual=SourceVisibilityResidual.RESIDUAL_NO_VISIBILITY_BASIS,
            clears_source_visibility=False,
            reason="   ",
        )


def test_value_with_reason_rejected():
    # a value posture is self-describing; reasons are carried only by residuals
    with pytest.raises(ValidationError):
        EcrSourceVisibilityPosture(
            packet_id="pkt",
            value=SourceVisibilityValue.ARCHIVE_ONLY,
            clears_source_visibility=True,
            reason="should not be present",
        )


def test_extra_field_rejected():
    with pytest.raises(ValidationError):
        EcrSourceVisibilityPosture(
            packet_id="pkt",
            value=SourceVisibilityValue.ARCHIVE_ONLY,
            clears_source_visibility=True,
            unexpected="x",
        )


def test_ratified_vocab_sizes():
    # the ratified closed sets: 8 values + 6 residuals
    assert len(list(SourceVisibilityValue)) == 8
    assert len(list(SourceVisibilityResidual)) == 6


def test_round_trip_residual_json_mode():
    posture = EcrSourceVisibilityPosture(
        packet_id="pkt",
        residual=SourceVisibilityResidual.RESIDUAL_COMPARISON_NOT_RECORDED,
        clears_source_visibility=False,
        reason="no comparison fact",
    )
    assert EcrSourceVisibilityPosture.model_validate(posture.model_dump()) == posture
    assert posture.model_dump(mode="json")["residual"] == "RESIDUAL_COMPARISON_NOT_RECORDED"
