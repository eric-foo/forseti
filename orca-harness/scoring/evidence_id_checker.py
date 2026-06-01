from __future__ import annotations

from schemas.case_models import EvidenceUnit, PreDecisionStatus
from schemas.judgement_models import BlindJudgement
from schemas.scoring_models import EvidenceIdCheckResult


def run_evidence_id_checks(
    evidence_units: list[EvidenceUnit],
    blind_judgement: BlindJudgement,
) -> EvidenceIdCheckResult:
    evidence_by_id = {unit.evidence_id: unit for unit in evidence_units}
    missing_ids: set[str] = set()
    excluded_ids: set[str] = set()
    uncertain_ids: set[str] = set()
    load_bearing_claim_citation_pass = True

    for claim in blind_judgement.evidence_used:
        if claim.claim_role == "load_bearing" and not claim.evidence_unit_ids:
            load_bearing_claim_citation_pass = False
        for evidence_id in claim.evidence_unit_ids:
            evidence_unit = evidence_by_id.get(evidence_id)
            if evidence_unit is None:
                missing_ids.add(evidence_id)
                continue
            if evidence_unit.pre_decision_status == PreDecisionStatus.EXCLUDED:
                excluded_ids.add(evidence_id)
            if evidence_unit.pre_decision_status == PreDecisionStatus.UNCERTAIN_TIMESTAMP:
                uncertain_ids.add(evidence_id)

    return EvidenceIdCheckResult(
        evidence_id_presence_pass=not missing_ids,
        pre_decision_status_pass=not excluded_ids,
        load_bearing_claim_citation_pass=load_bearing_claim_citation_pass,
        missing_evidence_ids=sorted(missing_ids),
        excluded_evidence_ids_cited=sorted(excluded_ids),
        uncertain_timestamp_evidence_ids_cited=sorted(uncertain_ids),
    )
