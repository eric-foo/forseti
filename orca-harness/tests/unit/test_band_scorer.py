from __future__ import annotations

from pathlib import Path

import pytest

from harness_utils import canonical_yaml_hash, hash_file, load_yaml_file
from schemas.case_models import EvidenceUnit, FacilitatorLedger
from schemas.judgement_models import BlindJudgement
from scoring.band_scorer import MappingVersionMismatchError, score_blind_judgement


def _bundle_inputs(case_dir: Path) -> tuple[FacilitatorLedger, BlindJudgement, list[EvidenceUnit]]:
    ledger = FacilitatorLedger.model_validate(load_yaml_file(case_dir / "facilitator_ledger.yaml"))
    judgement = BlindJudgement.model_validate(
        load_yaml_file(case_dir / "runs" / "fixed_contestant" / "run_tr_casetext_fixed" / "blind_judgement.yaml")
    )
    evidence_units = [
        EvidenceUnit.model_validate(load_yaml_file(path))
        for path in sorted((case_dir / "evidence").glob("*.yaml"))
    ]
    return ledger, judgement, evidence_units


def test_mapping_version_mismatch_refuses_scoring_unless_allowed(copied_case_dir: Path) -> None:
    ledger, judgement, evidence_units = _bundle_inputs(copied_case_dir)
    ledger = ledger.model_copy(update={"mapping_table_version_pin": "v0_13_old"})

    with pytest.raises(MappingVersionMismatchError) as exc_info:
        score_blind_judgement(
            participant_packet_hash=hash_file(copied_case_dir / "participant_packet.md"),
            blind_judgement_hash=hash_file(
                copied_case_dir / "runs" / "fixed_contestant" / "run_tr_casetext_fixed" / "blind_judgement.yaml"
            ),
            facilitator_ledger_hash=canonical_yaml_hash(ledger.model_dump(by_alias=True)),
            ledger=ledger,
            blind_judgement=judgement,
            evidence_units=evidence_units,
            allow_mapping_version_mismatch=False,
        )
    assert [event.failure_type for event in exc_info.value.failure_events] == ["mapping_version_mismatch"]
    assert exc_info.value.failure_events[0].severity == "blocking"
    assert exc_info.value.failure_events[0].scoring_result_ref is None

    allowed = score_blind_judgement(
        participant_packet_hash=hash_file(copied_case_dir / "participant_packet.md"),
        blind_judgement_hash=hash_file(
            copied_case_dir / "runs" / "fixed_contestant" / "run_tr_casetext_fixed" / "blind_judgement.yaml"
        ),
        facilitator_ledger_hash=canonical_yaml_hash(ledger.model_dump(by_alias=True)),
        ledger=ledger,
        blind_judgement=judgement,
        evidence_units=evidence_units,
        allow_mapping_version_mismatch=True,
    )
    assert allowed.scoring_result.action_band_result.band_status.value == "conflict_escalate"
    assert [event.failure_type for event in allowed.failure_events] == ["mapping_version_mismatch"]
