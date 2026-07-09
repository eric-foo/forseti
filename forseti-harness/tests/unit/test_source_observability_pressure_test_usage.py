from __future__ import annotations

import pytest

from source_observability.checker import run_source_observability_checks
from source_observability.models import ObservablePosture, SourceObservabilityRecord


@pytest.fixture
def pressure_test_records() -> list[SourceObservabilityRecord]:
    return [
        SourceObservabilityRecord(
            record_id="SLOT1-MI-BIWS",
            source_ref="slot1://mi-biws/pricing-and-bundles",
            source_family="pricing_offer_surface",
            source_language_posture=ObservablePosture.PARAPHRASED,
            source_structure_posture=ObservablePosture.PARAPHRASED,
            archive_body_posture=ObservablePosture.NOT_ATTEMPTED,
            media_posture=ObservablePosture.NOT_ATTEMPTED,
            access_posture=ObservablePosture.PRESERVED,
            locator_visible=True,
            cutoff_visible=True,
            source_language_anchor_count=0,
            source_language_anchor_required=True,
            source_structure_required=True,
            media_required=True,
            archive_body_expected=True,
            limitation_notes=[
                "Slot 1 preserved useful pricing facts but not verbatim language, packaging structure, or archive bodies."
            ],
        ),
        SourceObservabilityRecord(
            record_id="SLOT2-TEAL",
            source_ref="slot2://teal/public-host-failure",
            source_family="public_host_page",
            source_language_posture=ObservablePosture.INACCESSIBLE,
            source_structure_posture=ObservablePosture.INACCESSIBLE,
            archive_body_posture=ObservablePosture.FAILED,
            media_posture=ObservablePosture.NOT_APPLICABLE,
            access_posture=ObservablePosture.FAILED,
            locator_visible=True,
            cutoff_visible=True,
            source_language_anchor_count=0,
            archive_body_expected=True,
            limitation_notes=["Slot 2 preserved access-failure posture, not source body content."],
        ),
        SourceObservabilityRecord(
            record_id="SLOT3-REDDIT-WSO",
            source_ref="slot3://reddit-wso/forum-pain-language",
            source_family="forum_discourse",
            source_language_posture=ObservablePosture.PRESERVED,
            source_structure_posture=ObservablePosture.PARAPHRASED,
            archive_body_posture=ObservablePosture.NOT_ATTEMPTED,
            media_posture=ObservablePosture.PRESERVED,
            access_posture=ObservablePosture.PRESERVED,
            locator_visible=True,
            cutoff_visible=True,
            source_language_anchor_count=4,
            source_language_anchor_required=True,
            source_structure_required=True,
            media_required=True,
            archive_body_expected=True,
            limitation_notes=[
                "Slot 3 preserved source-language anchors and recaptured media, but carried WSO structure and archive-body limitations."
            ],
        ),
    ]


def test_helper_expresses_first_pressure_test_batch_lessons(
    pressure_test_records: list[SourceObservabilityRecord],
) -> None:
    result = run_source_observability_checks(pressure_test_records)

    limitation_types_by_record = {
        record.record_id: [
            limitation.limitation_type
            for limitation in result.limitations
            if limitation.record_id == record.record_id
        ]
        for record in pressure_test_records
    }

    assert result.record_count == 3
    assert limitation_types_by_record == {
        "SLOT1-MI-BIWS": [
            "source_language_anchor_missing",
            "source_structure_not_preserved",
            "media_not_preserved",
            "archive_body_not_retrieved",
        ],
        "SLOT2-TEAL": [
            "archive_body_not_retrieved",
            "access_failure_visible",
        ],
        "SLOT3-REDDIT-WSO": [
            "source_structure_not_preserved",
            "archive_body_not_retrieved",
        ],
    }
    assert "unnoted_non_preserved_posture" not in {
        limitation.limitation_type for limitation in result.limitations
    }
