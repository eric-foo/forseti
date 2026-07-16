from __future__ import annotations

from dataclasses import dataclass
from functools import partial

from harness_utils import (
    HARNESS_VERSION,
    LABELING_RUBRIC_VERSION,
    MAPPING_TABLE_VERSION,
    SCORER_VERSION,
    canonical_yaml_hash,
    generate_ulid,
    utc_now_z,
)
from schemas.case_models import EvidenceUnit, FacilitatorLedger
from schemas.judgement_models import BlindJudgement
from schemas.scoring_models import (
    FailureEvent,
    MustAddressCoverageResult,
    ScoringResult,
)
from scoring.evidence_id_checker import run_evidence_id_checks
from scoring.mapping_table import derive_action_band


class MappingVersionMismatchError(RuntimeError):
    """Raised when a case ledger pin does not match the active mapping table."""

    def __init__(self, message: str, failure_events: list[FailureEvent] | None = None) -> None:
        super().__init__(message)
        self.failure_events = failure_events or []


@dataclass
class ScoreBundle:
    scoring_result: ScoringResult
    failure_events: list[FailureEvent]
    scoring_result_hash: str


def _build_failure_event(
    *,
    batch_id: str,
    case_id: str,
    contestant_id: str,
    run_id: str,
    scoring_result_ref: str | None,
    scoring_result_hash: str | None,
    failure_type: str,
    severity: str,
    mechanical_source: str,
    details: dict,
) -> FailureEvent:
    return FailureEvent(
        event_id=generate_ulid(),
        created_at=utc_now_z(),
        harness_version=HARNESS_VERSION,
        batch_id=batch_id,
        case_id=case_id,
        contestant_id=contestant_id,
        run_id=run_id,
        scoring_result_ref=scoring_result_ref,
        scoring_result_hash=scoring_result_hash,
        failure_type=failure_type,
        severity=severity,
        mechanical_source=mechanical_source,
        details=details,
    )


def score_blind_judgement(
    *,
    participant_packet_hash: str,
    blind_judgement_hash: str,
    facilitator_ledger_hash: str,
    ledger: FacilitatorLedger,
    blind_judgement: BlindJudgement,
    evidence_units: list[EvidenceUnit],
    allow_mapping_version_mismatch: bool = False,
) -> ScoreBundle:
    scoring_result_id = generate_ulid()
    failure_events: list[FailureEvent] = []
    # The five identity kwargs shared by every non-mismatch failure event, bound once.
    build_failure_event = partial(
        _build_failure_event,
        batch_id=ledger.batch_id,
        case_id=ledger.case_id,
        contestant_id=blind_judgement.contestant_id,
        run_id=blind_judgement.run_id,
        scoring_result_ref=scoring_result_id,
    )

    if ledger.mapping_table_version_pin != MAPPING_TABLE_VERSION:
        blocking_mismatch = not allow_mapping_version_mismatch
        mismatch_event = _build_failure_event(
            batch_id=ledger.batch_id,
            case_id=ledger.case_id,
            contestant_id=blind_judgement.contestant_id,
            run_id=blind_judgement.run_id,
            scoring_result_ref=None if blocking_mismatch else scoring_result_id,
            scoring_result_hash=None,
            failure_type="mapping_version_mismatch",
            severity="info" if allow_mapping_version_mismatch else "blocking",
            mechanical_source="band_scorer",
            details={
                "summary": "Ledger mapping_table_version_pin does not match the active scorer version.",
                "related_fields": ["mapping_table_version_pin"],
                "expected": MAPPING_TABLE_VERSION,
                "actual": ledger.mapping_table_version_pin,
            },
        )
        failure_events.append(mismatch_event)
        if blocking_mismatch:
            raise MappingVersionMismatchError(
                f"Refusing to score ledger pin {ledger.mapping_table_version_pin}; expected {MAPPING_TABLE_VERSION}",
                [mismatch_event],
            )

    action_band_result = derive_action_band(ledger.frozen_band_inputs)
    recommended_level = blind_judgement.recommended_action.ladder_level
    overreach_distance = max(0, recommended_level - action_band_result.action_ceiling)
    underreach_distance = max(0, action_band_result.action_floor - recommended_level)
    over_band = overreach_distance > 0
    under_band = underreach_distance > 0
    in_band = not over_band and not under_band
    underreach_primary = under_band and ledger.underreach_observability.present

    evidence_id_check_result = run_evidence_id_checks(evidence_units, blind_judgement)
    must_address_ids = [item.must_address_item_id for item in ledger.must_address_items]
    covered_ids = sorted(
        {item_id for item_id in blind_judgement.must_address_items_covered if item_id in must_address_ids}
    )
    missed_ids = sorted(set(must_address_ids) - set(blind_judgement.must_address_items_covered))
    must_address_coverage_result = MustAddressCoverageResult(
        **{
            "pass": not missed_ids,
            "covered_ids": covered_ids,
            "missed_ids": missed_ids,
        }
    )

    if over_band:
        failure_events.append(
            build_failure_event(
                scoring_result_hash=None,
                failure_type="over_band",
                severity="material",
                mechanical_source="band_scorer",
                details={
                    "summary": "Recommended action exceeds the deterministic ceiling.",
                    "related_fields": ["recommended_level", "action_ceiling"],
                    "recommended_level": recommended_level,
                    "action_floor": action_band_result.action_floor,
                    "action_ceiling": action_band_result.action_ceiling,
                },
            )
        )
    if under_band:
        failure_events.append(
            build_failure_event(
                scoring_result_hash=None,
                failure_type="under_band",
                severity="material" if underreach_primary else "info",
                mechanical_source="band_scorer",
                details={
                    "summary": "Recommended action falls below the deterministic floor.",
                    "related_fields": ["recommended_level", "action_floor"],
                    "recommended_level": recommended_level,
                    "action_floor": action_band_result.action_floor,
                    "action_ceiling": action_band_result.action_ceiling,
                },
            )
        )
    if action_band_result.band_status.value == "low_precision_band":
        failure_events.append(
            build_failure_event(
                scoring_result_hash=None,
                failure_type="low_precision_band",
                severity="minor",
                mechanical_source="mapping_table",
                details={
                    "summary": "Deterministic band is low precision.",
                    "related_fields": ["action_floor", "action_ceiling", "band_width"],
                    "action_floor": action_band_result.action_floor,
                    "action_ceiling": action_band_result.action_ceiling,
                },
            )
        )
    if not evidence_id_check_result.evidence_id_presence_pass:
        failure_events.append(
            build_failure_event(
                scoring_result_hash=None,
                failure_type="evidence_id_missing",
                severity="blocking",
                mechanical_source="evidence_id_checker",
                details={
                    "summary": "Blind judgement cited evidence IDs that do not exist in the evidence registry.",
                    "related_fields": ["evidence_unit_ids"],
                    "evidence_unit_ids": evidence_id_check_result.missing_evidence_ids,
                },
            )
        )
    if not evidence_id_check_result.pre_decision_status_pass:
        failure_events.append(
            build_failure_event(
                scoring_result_hash=None,
                failure_type="post_decision_evidence_cited",
                severity="blocking",
                mechanical_source="evidence_id_checker",
                details={
                    "summary": "Blind judgement cited excluded or post-decision evidence.",
                    "related_fields": ["evidence_unit_ids"],
                    "evidence_unit_ids": evidence_id_check_result.excluded_evidence_ids_cited,
                },
            )
        )
    if not evidence_id_check_result.load_bearing_claim_citation_pass:
        failure_events.append(
            build_failure_event(
                scoring_result_hash=None,
                failure_type="evidence_id_missing",
                severity="blocking",
                mechanical_source="evidence_id_checker",
                details={
                    "summary": "A load-bearing claim lacks any cited evidence IDs.",
                    "related_fields": ["claim_role", "evidence_unit_ids"],
                },
            )
        )
    if missed_ids:
        failure_events.append(
            build_failure_event(
                scoring_result_hash=None,
                failure_type="must_address_item_missed",
                severity="material",
                mechanical_source="band_scorer",
                details={
                    "summary": "Blind judgement did not cover every facilitator-ledger must-address item.",
                    "related_fields": ["must_address_item_ids"],
                    "must_address_item_ids": missed_ids,
                },
            )
        )

    scoring_result = ScoringResult(
        scoring_result_id=scoring_result_id,
        case_id=ledger.case_id,
        contestant_id=blind_judgement.contestant_id,
        run_id=blind_judgement.run_id,
        blind_judgement_hash=blind_judgement_hash,
        facilitator_ledger_hash=facilitator_ledger_hash,
        participant_packet_hash=participant_packet_hash,
        mapping_table_version=MAPPING_TABLE_VERSION,
        labeling_rubric_version=LABELING_RUBRIC_VERSION,
        action_band_result=action_band_result,
        recommended_level=recommended_level,
        in_band=in_band,
        over_band=over_band,
        under_band=under_band,
        overreach_distance=overreach_distance,
        underreach_distance=underreach_distance,
        underreach_primary=underreach_primary,
        evidence_id_check_result=evidence_id_check_result,
        must_address_coverage_result=must_address_coverage_result,
        memorization_probe_result="not_run",
        failure_event_ids=[event.event_id for event in failure_events],
        scored_at=utc_now_z(),
        scorer_version=SCORER_VERSION,
    )
    scoring_result_hash = canonical_yaml_hash(scoring_result.model_dump(by_alias=True))
    finalized_events = [
        event.model_copy(update={"scoring_result_hash": scoring_result_hash}) for event in failure_events
    ]
    return ScoreBundle(
        scoring_result=scoring_result,
        failure_events=finalized_events,
        scoring_result_hash=scoring_result_hash,
    )
