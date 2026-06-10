from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import sys

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from harness_utils import (
    canonical_yaml_hash,
    hash_file,
    load_yaml_file,
    split_frontmatter,
    write_yaml_file,
    append_yaml_document,
)
from reports.case_report import build_case_report
from schemas.case_models import EvidenceUnit, FacilitatorLedger, ParticipantPacketFrontmatter
from schemas.judgement_models import BlindJudgement
from schemas.scoring_models import FailureEvent, ScoringResult
from scoring.band_scorer import MappingVersionMismatchError, ScoreBundle, score_blind_judgement


@dataclass
class RunArtifacts:
    score_path: Path
    report_path: Path
    scoring_bundle: ScoreBundle
    warnings: list[str]


class DuplicateScoreError(RuntimeError):
    """Raised when scoring would duplicate an existing case/run/contestant tuple."""


def _project_root_from_case_dir(case_dir: Path, project_root: Path | None = None) -> Path:
    if project_root is not None:
        resolved_root = project_root.resolve()
        _validate_case_dir_against_project_root(case_dir, resolved_root)
        return resolved_root

    for candidate in case_dir.parents:
        if _looks_like_project_root(candidate):
            _validate_case_dir_against_project_root(case_dir, candidate)
            return candidate
    raise ValueError(f"Unable to infer harness project root from case directory: {case_dir}")


def _looks_like_project_root(path: Path) -> bool:
    required_children = (
        "pyproject.toml",
        "harness_utils.py",
        "cases",
        "reports",
        "runners",
        "schemas",
        "scoring",
    )
    return all((path / child).exists() for child in required_children)


def _validate_case_dir_against_project_root(case_dir: Path, project_root: Path) -> None:
    cases_root = project_root / "cases"
    try:
        relative_case_path = case_dir.relative_to(cases_root)
    except ValueError as exc:
        raise ValueError(f"Case directory {case_dir} is not under expected cases root {cases_root}") from exc

    if len(relative_case_path.parts) != 2:
        raise ValueError(
            "Case directory must be exactly two levels under project_root/cases (batch_id/case_id)"
        )


def _load_participant_packet(case_dir: Path) -> tuple[ParticipantPacketFrontmatter, str]:
    participant_packet_path = case_dir / "participant_packet.md"
    frontmatter, _ = split_frontmatter(participant_packet_path.read_text(encoding="utf-8"))
    return ParticipantPacketFrontmatter.model_validate(frontmatter), hash_file(participant_packet_path)


def _load_evidence_units(case_dir: Path) -> list[EvidenceUnit]:
    evidence_dir = case_dir / "evidence"
    return [
        EvidenceUnit.model_validate(load_yaml_file(path))
        for path in sorted(evidence_dir.glob("*.yaml"))
    ]


def _load_ledger(case_dir: Path) -> tuple[FacilitatorLedger, str]:
    ledger_path = case_dir / "facilitator_ledger.yaml"
    ledger_raw = load_yaml_file(ledger_path)
    ledger = FacilitatorLedger.model_validate(ledger_raw)
    ledger_without_hash = dict(ledger_raw)
    ledger_without_hash.pop("ledger_freeze_hash", None)
    computed_hash = canonical_yaml_hash(ledger_without_hash)
    if computed_hash != ledger.ledger_freeze_hash:
        raise ValueError(
            f"facilitator_ledger.yaml hash mismatch: expected {ledger.ledger_freeze_hash}, computed {computed_hash}"
        )
    return ledger, hash_file(ledger_path)


def _resolve_blind_judgement_path(case_dir: Path, blind_judgement_path: Path | None) -> Path:
    if blind_judgement_path is not None:
        return blind_judgement_path
    candidates = sorted(case_dir.glob("runs/*/*/blind_judgement.yaml"))
    if len(candidates) != 1:
        raise ValueError("Expected exactly one blind_judgement.yaml under runs/*/*/")
    return candidates[0]


def _load_scores_from_directory(score_dir: Path, label: str) -> list[ScoringResult]:
    scores: list[ScoringResult] = []
    for path in sorted(score_dir.glob("*.yaml")):
        try:
            scores.append(ScoringResult.model_validate(load_yaml_file(path)))
        except Exception as exc:
            raise ValueError(f"Invalid {label} {path}: {exc}") from exc
    return scores


def _load_existing_scores(case_dir: Path) -> list[ScoringResult]:
    return _load_scores_from_directory(case_dir / "scores", "existing score file")


def _load_archived_scores(case_dir: Path) -> list[ScoringResult]:
    return _load_scores_from_directory(case_dir / "scores" / "archive", "archived score file")


def _find_duplicate_scores(
    scoring_results: list[ScoringResult],
    *,
    case_id: str,
    contestant_id: str,
    run_id: str,
) -> list[ScoringResult]:
    return [
        result
        for result in scoring_results
        if result.case_id == case_id and result.contestant_id == contestant_id and result.run_id == run_id
    ]


def _append_failure_events(failure_log_path: Path, failure_events: list[FailureEvent]) -> None:
    for event in failure_events:
        append_yaml_document(failure_log_path, event.model_dump(by_alias=True))


def run_fixed_case(
    case_dir: Path,
    *,
    blind_judgement_path: Path | None = None,
    allow_duplicate_score: bool = False,
    allow_mapping_version_mismatch: bool = False,
    project_root: Path | None = None,
) -> RunArtifacts:
    case_dir = case_dir.resolve()
    project_root = _project_root_from_case_dir(case_dir, project_root)
    participant_packet, participant_packet_hash = _load_participant_packet(case_dir)
    ledger, facilitator_ledger_hash = _load_ledger(case_dir)
    evidence_units = _load_evidence_units(case_dir)

    blind_judgement_path = _resolve_blind_judgement_path(case_dir, blind_judgement_path)
    blind_judgement = BlindJudgement.model_validate(load_yaml_file(blind_judgement_path))
    blind_judgement_hash = hash_file(blind_judgement_path)

    if participant_packet.case_id != ledger.case_id or ledger.case_id != blind_judgement.case_id:
        raise ValueError("Case ID mismatch across participant packet, facilitator ledger, and blind judgement")

    warnings: list[str] = []
    duplicate_scores = _find_duplicate_scores(
        _load_existing_scores(case_dir),
        case_id=ledger.case_id,
        contestant_id=blind_judgement.contestant_id,
        run_id=blind_judgement.run_id,
    )
    if duplicate_scores and not allow_duplicate_score:
        duplicate_ids = ", ".join(result.scoring_result_id for result in duplicate_scores)
        raise DuplicateScoreError(
            "Refusing duplicate score for "
            f"({ledger.case_id}, {blind_judgement.run_id}, {blind_judgement.contestant_id}); "
            f"existing scoring_result_id(s): {duplicate_ids}. Use --allow-duplicate-score to override."
        )

    archived_duplicate_scores = _find_duplicate_scores(
        _load_archived_scores(case_dir),
        case_id=ledger.case_id,
        contestant_id=blind_judgement.contestant_id,
        run_id=blind_judgement.run_id,
    )
    if archived_duplicate_scores:
        archived_duplicate_ids = ", ".join(result.scoring_result_id for result in archived_duplicate_scores)
        warnings.append(
            "Archived score file(s) already exist for "
            f"({ledger.case_id}, {blind_judgement.run_id}, {blind_judgement.contestant_id}): "
            f"{archived_duplicate_ids}. Archived scores are audit history and are ignored by active reports."
        )

    failure_log_path = project_root / "memory" / "logs" / "failure_events.yaml"
    try:
        scoring_bundle = score_blind_judgement(
            participant_packet_hash=participant_packet_hash,
            blind_judgement_hash=blind_judgement_hash,
            facilitator_ledger_hash=facilitator_ledger_hash,
            ledger=ledger,
            blind_judgement=blind_judgement,
            evidence_units=evidence_units,
            allow_mapping_version_mismatch=allow_mapping_version_mismatch,
        )
    except MappingVersionMismatchError as exc:
        _append_failure_events(failure_log_path, exc.failure_events)
        raise

    score_path = case_dir / "scores" / f"{scoring_bundle.scoring_result.scoring_result_id}.yaml"
    if score_path.exists():
        raise FileExistsError(f"Refusing to overwrite existing score file: {score_path}")
    write_yaml_file(score_path, scoring_bundle.scoring_result.model_dump(by_alias=True))

    _append_failure_events(failure_log_path, scoring_bundle.failure_events)

    _, report_path = build_case_report(
        project_root=project_root,
        case_dir=case_dir,
        ledger=ledger,
        facilitator_ledger_hash=facilitator_ledger_hash,
    )
    return RunArtifacts(
        score_path=score_path,
        report_path=report_path,
        scoring_bundle=scoring_bundle,
        warnings=warnings,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the fixed Step A case scorer.")
    parser.add_argument("case_dir", type=Path)
    parser.add_argument("--blind-judgement-path", type=Path, default=None)
    parser.add_argument("--allow-duplicate-score", action="store_true")
    parser.add_argument("--allow-mapping-version-mismatch", action="store_true")
    parser.add_argument("--project-root", type=Path, default=None)
    args = parser.parse_args()

    try:
        artifacts = run_fixed_case(
            args.case_dir,
            blind_judgement_path=args.blind_judgement_path,
            allow_duplicate_score=args.allow_duplicate_score,
            allow_mapping_version_mismatch=args.allow_mapping_version_mismatch,
            project_root=args.project_root,
        )
    except MappingVersionMismatchError as exc:
        parser.exit(status=2, message=f"{exc}\n")
    except DuplicateScoreError as exc:
        parser.exit(status=3, message=f"{exc}\n")

    for warning in artifacts.warnings:
        print(f"WARNING: {warning}", file=sys.stderr)
    print(artifacts.score_path)
    print(artifacts.report_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
