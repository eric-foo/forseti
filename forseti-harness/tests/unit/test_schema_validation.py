from __future__ import annotations

from pathlib import Path

from harness_utils import load_yaml_file, split_frontmatter
from schemas.case_models import EvidenceUnit, FacilitatorLedger, ParticipantPacketFrontmatter
from schemas.judgement_models import BlindJudgement


def test_tr_casetext_fixture_schema_validation(copied_case_dir: Path) -> None:
    packet_path = copied_case_dir / "participant_packet.md"
    frontmatter, _ = split_frontmatter(packet_path.read_text(encoding="utf-8"))
    packet = ParticipantPacketFrontmatter.model_validate(frontmatter)
    ledger = FacilitatorLedger.model_validate(load_yaml_file(copied_case_dir / "facilitator_ledger.yaml"))
    evidence = [
        EvidenceUnit.model_validate(load_yaml_file(path))
        for path in sorted((copied_case_dir / "evidence").glob("*.yaml"))
    ]
    judgement = BlindJudgement.model_validate(
        load_yaml_file(copied_case_dir / "runs" / "fixed_contestant" / "run_tr_casetext_fixed" / "blind_judgement.yaml")
    )

    assert packet.case_id == ledger.case_id == judgement.case_id
    assert len(evidence) == 7
    assert ledger.fixture_status == "QUARANTINED"
    assert ledger.fixture_grade == "plumbing_grade"
    assert ledger.underreach_observability.present is False
    assert judgement.judgement_class == "escalate"
    assert judgement.recommended_action.ladder_level == 6
