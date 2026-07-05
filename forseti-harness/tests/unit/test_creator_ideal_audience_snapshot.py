from __future__ import annotations

import json
from pathlib import Path

import pytest

from capture_spine.creator_profile_current.ideal_audience_snapshot import (
    SNAPSHOT_SCHEMA_VERSION,
    SNAPSHOT_WRAPPER_KEY,
    build_creator_ideal_audience_profile_snapshot_from_evidence,
    load_creator_ideal_audience_snapshot_document,
)
from runners.run_creator_ideal_audience_profile_snapshot import main as snapshot_main


def _evidence() -> list[dict]:
    return [
        {
            "evidence_id": "ig_acct_1:audience:e1",
            "creator_id": "ig_acct_1",
            "platform": "instagram",
            "post_id": "post_1",
            "signal_id": "tier1",
            "modality": "text",
            "target_field": "segment",
            "label": "fragrance_discovery",
            "vote": 1.0,
            "base_reliability": 1.0,
            "extractor_confidence": 1.0,
            "creator_authored": True,
            "possible_negation_or_irony": False,
            "creative_cluster_id": "post_1",
            "source_pointer": "for beginners",
        }
    ]


def test_on_demand_ideal_audience_snapshot_runner_writes_joinable_snapshot(tmp_path: Path) -> None:
    evidence_path = tmp_path / "evidence_records.json"
    output_path = tmp_path / "creator_ideal_audience_profile_snapshot_v0.json"
    evidence_path.write_text(json.dumps({"evidence_records": _evidence()}), encoding="utf-8")

    result = snapshot_main(
        [
            "--evidence-records",
            str(evidence_path),
            "--output",
            str(output_path),
            "--profile-subject-id",
            "ig_acct_1",
            "--platform-scope",
            "instagram",
            "--observation-window-start",
            "2026-07-01T00:00:00Z",
            "--observation-window-end",
            "2026-07-04T00:00:00Z",
            "--computed-at",
            "2026-07-04T00:00:00Z",
        ]
    )

    assert result == 0
    snapshots = load_creator_ideal_audience_snapshot_document(output_path)
    assert len(snapshots) == 1
    snapshot = snapshots[0]
    assert snapshot["schema_version"] == SNAPSHOT_SCHEMA_VERSION
    assert snapshot["profile_subject_id"] == "ig_acct_1"
    assert snapshot["actual_audience"] == "not_estimated"
    assert snapshot["tier_2a_profile_or_none"] is None
    assert snapshot["evidence_ids"] == ["ig_acct_1:audience:e1"]
    assert snapshot["ideal_audience_profile"]["actual_audience"] == "not_estimated"

    document = json.loads(output_path.read_text(encoding="utf-8"))
    assert document[SNAPSHOT_WRAPPER_KEY]["profiles"] == [snapshot]


def test_creator_record_snapshot_requires_explicit_platform_account_ids() -> None:
    from schemas.audience_inference_models import EvidenceRecord, ModalityFamily, OutputField

    evidence = [
        EvidenceRecord(
            evidence_id="cr_1:audience:e1",
            creator_id="cr_1",
            platform="instagram",
            post_id="audience-post-1",
            signal_id="tier1-test",
            modality=ModalityFamily.TEXT,
            target_field=OutputField.SEGMENT,
            label="fragrance_discovery",
            vote=1.0,
            base_reliability=1.0,
            extractor_confidence=1.0,
            creator_authored=True,
            source_pointer="for beginners",
        )
    ]

    with pytest.raises(ValueError, match="creator_record snapshots must specify platform_account_ids"):
        build_creator_ideal_audience_profile_snapshot_from_evidence(
            evidence,
            profile_subject_kind="creator_record",
            profile_subject_id="cr_1",
            creator_record_id_or_none="cr_1",
            platform_scope="instagram",
            observation_window_start="2026-07-01T00:00:00Z",
            observation_window_end="2026-07-04T00:00:00Z",
            computed_at="2026-07-04T00:00:00Z",
        )
