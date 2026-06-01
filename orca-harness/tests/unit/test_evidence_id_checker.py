from __future__ import annotations

from pathlib import Path

from harness_utils import load_yaml_file
from schemas.case_models import EvidenceUnit
from schemas.judgement_models import BlindJudgement
from scoring.evidence_id_checker import run_evidence_id_checks


def test_missing_evidence_id_is_detected(copied_case_dir: Path) -> None:
    evidence_units = [
        EvidenceUnit.model_validate(load_yaml_file(path))
        for path in sorted((copied_case_dir / "evidence").glob("*.yaml"))
    ]
    blind_judgement = BlindJudgement.model_validate(
        load_yaml_file(copied_case_dir / "runs" / "fixed_contestant" / "run_tr_casetext_fixed" / "blind_judgement.yaml")
    )
    mutated = blind_judgement.model_copy(
        update={
            "evidence_used": [
                blind_judgement.evidence_used[0].model_copy(
                    update={"evidence_unit_ids": blind_judgement.evidence_used[0].evidence_unit_ids + ["E999"]}
                ),
                blind_judgement.evidence_used[1],
            ]
        }
    )

    result = run_evidence_id_checks(evidence_units, mutated)
    assert result.evidence_id_presence_pass is False
    assert result.missing_evidence_ids == ["E999"]
