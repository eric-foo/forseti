from __future__ import annotations

from collections import Counter
from pathlib import Path

from harness_utils import NON_CLAIM_NOTICE, load_yaml_documents, load_yaml_file, utc_now_z, write_yaml_file
from schemas.case_models import FacilitatorLedger
from schemas.scoring_models import CaseReport, ContestantScoreSummary, FailureEvent, ScoringResult


def build_case_report_path(project_root: Path, batch_id: str, case_id: str) -> Path:
    return project_root / "reports" / batch_id / case_id / "case_report.yaml"


def build_case_report(
    *,
    project_root: Path,
    case_dir: Path,
    ledger: FacilitatorLedger,
    facilitator_ledger_hash: str,
) -> tuple[CaseReport, Path]:
    scoring_results = _load_case_scores(case_dir)
    relevant_score_ids = {result.scoring_result_id for result in scoring_results}
    failure_events = _load_case_failure_events(project_root / "memory" / "logs" / "failure_events.yaml", relevant_score_ids)
    failure_events_by_score_id = Counter(
        event.scoring_result_ref for event in failure_events if event.severity == "blocking"
    )
    failure_types = Counter(event.failure_type for event in failure_events)
    severities = Counter(event.severity for event in failure_events)
    latest_scoring_result = scoring_results[-1] if scoring_results else None

    report = CaseReport(
        case_id=ledger.case_id,
        batch_id=ledger.batch_id,
        mapping_table_version=(
            latest_scoring_result.mapping_table_version if latest_scoring_result is not None else ledger.mapping_table_version_pin
        ),
        facilitator_ledger_hash=facilitator_ledger_hash,
        contestant_results=[
            ContestantScoreSummary(
                contestant_id=result.contestant_id,
                run_id=result.run_id,
                scoring_result_id=result.scoring_result_id,
                in_band=result.in_band,
                over_band=result.over_band,
                under_band=result.under_band,
                overreach_distance=result.overreach_distance,
                underreach_distance=result.underreach_distance,
                blocking_failures=failure_events_by_score_id[result.scoring_result_id],
            )
            for result in scoring_results
        ],
        failure_event_summary={
            "by_type": dict(sorted(failure_types.items())),
            "by_severity": dict(sorted(severities.items())),
            "total": len(failure_events),
        },
        non_claim_notice=NON_CLAIM_NOTICE,
        generated_at=utc_now_z(),
    )
    report_path = build_case_report_path(project_root, ledger.batch_id, ledger.case_id)
    write_yaml_file(report_path, report.model_dump(by_alias=True))
    return report, report_path


def _load_case_scores(case_dir: Path) -> list[ScoringResult]:
    scoring_results: list[ScoringResult] = []
    for path in sorted((case_dir / "scores").glob("*.yaml")):
        try:
            scoring_results.append(ScoringResult.model_validate(load_yaml_file(path)))
        except Exception as exc:
            raise ValueError(f"Invalid scoring result file {path}: {exc}") from exc
    return sorted(
        scoring_results,
        key=lambda result: (result.contestant_id, result.run_id, result.scored_at, result.scoring_result_id),
    )


def _load_case_failure_events(failure_log_path: Path, scoring_result_ids: set[str]) -> list[FailureEvent]:
    failure_events: list[FailureEvent] = []
    for document in load_yaml_documents(failure_log_path):
        if document.get("scoring_result_ref") not in scoring_result_ids:
            continue
        try:
            failure_events.append(FailureEvent.model_validate(document))
        except Exception as exc:
            raise ValueError(f"Invalid failure event in {failure_log_path}: {exc}") from exc
    return failure_events
