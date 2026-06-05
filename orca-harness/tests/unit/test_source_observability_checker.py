from __future__ import annotations

import pytest
from pydantic import ValidationError

from source_observability.checker import run_source_observability_checks
from source_observability.models import ObservablePosture, SourceObservabilityRecord


def _record(**overrides: object) -> SourceObservabilityRecord:
    values = {
        "record_id": "R01",
        "source_ref": "slot3://reddit/R01",
        "source_family": "forum_thread",
        "source_language_posture": ObservablePosture.PRESERVED,
        "source_structure_posture": ObservablePosture.PRESERVED,
        "archive_body_posture": ObservablePosture.NOT_APPLICABLE,
        "media_posture": ObservablePosture.NOT_APPLICABLE,
        "access_posture": ObservablePosture.PRESERVED,
        "locator_visible": True,
        "cutoff_visible": True,
        "source_language_anchor_count": 2,
        "source_language_anchor_required": False,
        "media_required": False,
        "archive_body_expected": False,
        "limitation_notes": [],
    }
    values.update(overrides)
    return SourceObservabilityRecord.model_validate(values)


def test_checker_flags_source_language_media_archive_and_visible_access_failure() -> None:
    result = run_source_observability_checks(
        [
            _record(
                source_language_posture=ObservablePosture.POINTER_ONLY,
                archive_body_posture=ObservablePosture.NOT_ATTEMPTED,
                media_posture=ObservablePosture.POINTER_ONLY,
                access_posture=ObservablePosture.FAILED,
                source_language_anchor_count=0,
                source_language_anchor_required=True,
                media_required=True,
                archive_body_expected=True,
                limitation_notes=["Pointer-only source with visible failure posture."],
            )
        ]
    )

    assert result.record_count == 1
    assert result.has_visible_limitations is True
    assert [limitation.limitation_type for limitation in result.limitations] == [
        "source_language_anchor_missing",
        "media_not_preserved",
        "archive_body_not_retrieved",
        "access_failure_visible",
    ]


def test_checker_flags_access_failure_missing_locator_or_cutoff() -> None:
    result = run_source_observability_checks(
        [
            _record(
                access_posture=ObservablePosture.INACCESSIBLE,
                locator_visible=False,
                cutoff_visible=True,
                limitation_notes=["Host access failed."],
            )
        ]
    )

    assert [limitation.limitation_type for limitation in result.limitations] == [
        "access_failure_context_missing"
    ]


def test_checker_flags_non_preserved_postures_without_limitation_notes() -> None:
    result = run_source_observability_checks(
        [
            _record(
                source_language_posture=ObservablePosture.PARAPHRASED,
                source_structure_posture=ObservablePosture.POINTER_ONLY,
                archive_body_posture=ObservablePosture.NOT_ATTEMPTED,
            )
        ]
    )

    assert [limitation.limitation_type for limitation in result.limitations] == [
        "unnoted_non_preserved_posture",
        "unnoted_non_preserved_posture",
        "unnoted_non_preserved_posture",
    ]
    assert [limitation.posture for limitation in result.limitations] == [
        ObservablePosture.PARAPHRASED,
        ObservablePosture.POINTER_ONLY,
        ObservablePosture.NOT_ATTEMPTED,
    ]


def test_blank_limitation_note_does_not_silence_unnoted_postures() -> None:
    result = run_source_observability_checks(
        [
            _record(
                source_language_posture=ObservablePosture.PARAPHRASED,
                limitation_notes=[""],
            )
        ]
    )

    assert [limitation.limitation_type for limitation in result.limitations] == [
        "unnoted_non_preserved_posture",
    ]


def test_access_failure_is_not_double_reported_as_unnoted_posture() -> None:
    result = run_source_observability_checks(
        [
            _record(
                access_posture=ObservablePosture.FAILED,
                limitation_notes=[],
            )
        ]
    )

    assert [limitation.limitation_type for limitation in result.limitations] == [
        "access_failure_visible",
    ]


@pytest.mark.parametrize(
    ("overrides", "expected_limitation_type"),
    [
        (
            {
                "source_language_posture": ObservablePosture.POINTER_ONLY,
                "source_language_anchor_count": 0,
                "source_language_anchor_required": True,
            },
            "source_language_anchor_missing",
        ),
        (
            {
                "source_structure_posture": ObservablePosture.POINTER_ONLY,
                "source_structure_required": True,
            },
            "source_structure_not_preserved",
        ),
        (
            {
                "archive_body_posture": ObservablePosture.NOT_ATTEMPTED,
                "archive_body_expected": True,
            },
            "archive_body_not_retrieved",
        ),
        (
            {
                "media_posture": ObservablePosture.POINTER_ONLY,
                "media_required": True,
            },
            "media_not_preserved",
        ),
    ],
)
def test_dedicated_limitations_are_not_double_reported_as_unnoted_postures(
    overrides: dict[str, object],
    expected_limitation_type: str,
) -> None:
    result = run_source_observability_checks([_record(**overrides, limitation_notes=[])])

    assert [limitation.limitation_type for limitation in result.limitations] == [
        expected_limitation_type,
    ]


def test_preserved_record_has_no_visible_limitations() -> None:
    result = run_source_observability_checks([_record(source_language_anchor_required=True)])

    assert result.record_count == 1
    assert result.has_visible_limitations is False
    assert result.limitations == []


def test_preserved_language_without_anchor_count_is_still_limited_when_required() -> None:
    result = run_source_observability_checks(
        [
            _record(
                source_language_anchor_count=0,
                source_language_anchor_required=True,
            )
        ]
    )

    assert [limitation.limitation_type for limitation in result.limitations] == [
        "source_language_anchor_missing",
    ]


def test_archive_state_can_be_visible_without_body_retrieval_default() -> None:
    result = run_source_observability_checks(
        [
            _record(
                archive_body_posture=ObservablePosture.NOT_ATTEMPTED,
                archive_body_expected=False,
                limitation_notes=[
                    "Archive availability was recorded, but archive-body retrieval was not required for this slice."
                ],
            )
        ]
    )

    assert result.limitations == []


def test_posture_values_are_bounded() -> None:
    with pytest.raises(ValidationError):
        _record(source_language_posture="validated")
