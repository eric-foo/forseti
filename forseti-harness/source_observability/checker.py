from __future__ import annotations

from source_observability.models import (
    ObservablePosture,
    SourceObservabilityCheckResult,
    SourceObservabilityLimitation,
    SourceObservabilityRecord,
)


NON_PRESERVED_POSTURES = {
    ObservablePosture.PARAPHRASED,
    ObservablePosture.POINTER_ONLY,
    ObservablePosture.INACCESSIBLE,
    ObservablePosture.FAILED,
    ObservablePosture.NOT_ATTEMPTED,
}

ACCESS_FAILURE_POSTURES = {
    ObservablePosture.INACCESSIBLE,
    ObservablePosture.FAILED,
}


def run_source_observability_checks(
    records: list[SourceObservabilityRecord],
) -> SourceObservabilityCheckResult:
    limitations: list[SourceObservabilityLimitation] = []

    for record in records:
        limitations.extend(_check_source_language(record))
        limitations.extend(_check_source_structure(record))
        limitations.extend(_check_media(record))
        limitations.extend(_check_archive_body(record))
        limitations.extend(_check_access_failure(record))
        limitations.extend(_check_unnoted_non_preserved_postures(record))

    return SourceObservabilityCheckResult(
        record_count=len(records),
        limitations=limitations,
    )


def _check_source_language(record: SourceObservabilityRecord) -> list[SourceObservabilityLimitation]:
    if not record.source_language_anchor_required:
        return []
    if record.source_language_posture == ObservablePosture.PRESERVED and record.source_language_anchor_count > 0:
        return []
    return [
        SourceObservabilityLimitation(
            record_id=record.record_id,
            source_ref=record.source_ref,
            limitation_type="source_language_anchor_missing",
            posture=record.source_language_posture,
            detail="Source-language anchors are required but not visibly preserved.",
        )
    ]


def _check_source_structure(record: SourceObservabilityRecord) -> list[SourceObservabilityLimitation]:
    if not record.source_structure_required or record.source_structure_posture == ObservablePosture.PRESERVED:
        return []
    return [
        SourceObservabilityLimitation(
            record_id=record.record_id,
            source_ref=record.source_ref,
            limitation_type="source_structure_not_preserved",
            posture=record.source_structure_posture,
            detail="Visible source structure is required but not visibly preserved.",
        )
    ]


def _check_media(record: SourceObservabilityRecord) -> list[SourceObservabilityLimitation]:
    if not record.media_required or record.media_posture == ObservablePosture.PRESERVED:
        return []
    return [
        SourceObservabilityLimitation(
            record_id=record.record_id,
            source_ref=record.source_ref,
            limitation_type="media_not_preserved",
            posture=record.media_posture,
            detail="Media or layout evidence is required but not visibly preserved.",
        )
    ]


def _check_archive_body(record: SourceObservabilityRecord) -> list[SourceObservabilityLimitation]:
    if not record.archive_body_expected or record.archive_body_posture == ObservablePosture.PRESERVED:
        return []
    return [
        SourceObservabilityLimitation(
            record_id=record.record_id,
            source_ref=record.source_ref,
            limitation_type="archive_body_not_retrieved",
            posture=record.archive_body_posture,
            detail="Archive body content is expected but not visibly retrieved.",
        )
    ]


def _check_access_failure(record: SourceObservabilityRecord) -> list[SourceObservabilityLimitation]:
    if record.access_posture not in ACCESS_FAILURE_POSTURES:
        return []
    if record.locator_visible and record.cutoff_visible:
        return [
            SourceObservabilityLimitation(
                record_id=record.record_id,
                source_ref=record.source_ref,
                limitation_type="access_failure_visible",
                posture=record.access_posture,
                detail="Access failure is visible with locator and cutoff context.",
            )
        ]
    return [
        SourceObservabilityLimitation(
            record_id=record.record_id,
            source_ref=record.source_ref,
            limitation_type="access_failure_context_missing",
            posture=record.access_posture,
            detail="Access failure is visible but missing locator or cutoff context.",
        )
    ]


def _check_unnoted_non_preserved_postures(
    record: SourceObservabilityRecord,
) -> list[SourceObservabilityLimitation]:
    if any(note.strip() for note in record.limitation_notes):
        return []

    dedicated_fields = _dedicated_limitation_fields(record)
    checked_postures = {
        "source_language_posture": record.source_language_posture,
        "source_structure_posture": record.source_structure_posture,
        "archive_body_posture": record.archive_body_posture,
        "media_posture": record.media_posture,
    }
    return [
        SourceObservabilityLimitation(
            record_id=record.record_id,
            source_ref=record.source_ref,
            limitation_type="unnoted_non_preserved_posture",
            posture=posture,
            detail=f"{field_name} is {posture.value} without a limitation note.",
        )
        for field_name, posture in checked_postures.items()
        if field_name not in dedicated_fields and posture in NON_PRESERVED_POSTURES
    ]


def _dedicated_limitation_fields(record: SourceObservabilityRecord) -> set[str]:
    fields: set[str] = set()
    if record.source_language_anchor_required and not (
        record.source_language_posture == ObservablePosture.PRESERVED
        and record.source_language_anchor_count > 0
    ):
        fields.add("source_language_posture")
    if record.source_structure_required and record.source_structure_posture != ObservablePosture.PRESERVED:
        fields.add("source_structure_posture")
    if record.archive_body_expected and record.archive_body_posture != ObservablePosture.PRESERVED:
        fields.add("archive_body_posture")
    if record.media_required and record.media_posture != ObservablePosture.PRESERVED:
        fields.add("media_posture")
    return fields
