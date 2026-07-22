"""Resume-safe controller for one admitted TikTok creator onboarding."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import tempfile
import sys
from contextlib import redirect_stderr
from pathlib import Path
from typing import Any, Mapping, Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from capture_spine.creator_profile_current.materialize import (
    load_json,
    verify_audience_judgment_outcomes,
)
from data_lake.creator_audience_queue import (
    CreatorAudienceQueueError,
    claim_creator_audience_job,
    enqueue_creator_audience_job,
    materialize_claim_bundle,
    public_queue_view,
    require_active_claim,
    write_creator_audience_terminal,
)
from data_lake.creator_registry import (
    admit_tiktok_creator_account,
    extract_tiktok_packet_identity,
    resolve_tiktok_profile_subject_id,
)
from data_lake.root import DataLakeRoot, DataLakeRootError
from runners.run_creator_profile_current_materialize import main as materialize_main
from runners.run_tiktok_comment_attention_producer import run_comment_attention
from runners.run_tiktok_creator_audience_triangulation import (
    submit_subscription_judgment,
    prepare_subscription_judgment,
)
from runners.run_tiktok_grid_observation_producer import run_tiktok_grid_observations
from schemas.creator_audience_models import CreatorAudienceJudgmentOutcomeV1
from schemas.tiktok_audience_evidence_models import CreatorAudienceJudgmentOutcome


_ALLOWED_SILVER_STATUSES = {"derived", "already_current"}
ROOT = Path(__file__).resolve().parents[2]


def _audience_joins_by_subject(document: dict[str, Any]) -> dict[str, dict[str, Any]]:
    wrapper = document.get("creator_profile_current_view")
    profiles = wrapper.get("profiles") if isinstance(wrapper, dict) else None
    if not isinstance(profiles, list):
        raise ValueError("creator profile view has no profiles list")

    joins: dict[str, dict[str, Any]] = {}
    for profile in profiles:
        if not isinstance(profile, dict):
            continue
        joined = profile.get("audience_triangulation")
        if joined is None:
            continue
        profile_subject_id = profile.get("profile_subject_id")
        if not isinstance(profile_subject_id, str) or not profile_subject_id:
            raise ValueError("audience_triangulation join has no profile_subject_id")
        if not isinstance(joined, dict):
            raise ValueError(
                "audience_triangulation join is not an object for "
                f"profile_subject_id={profile_subject_id}"
            )
        if profile_subject_id in joins:
            raise ValueError(
                "duplicate audience_triangulation join for "
                f"profile_subject_id={profile_subject_id}"
            )
        joins[profile_subject_id] = joined
    return joins


def _verify_existing_audience_joins_preserved(
    *, previous_output: bytes | None, candidate_document: dict[str, Any]
) -> None:
    if previous_output is None:
        return
    previous_document = json.loads(previous_output)
    previous_joins = _audience_joins_by_subject(previous_document)
    candidate_joins = _audience_joins_by_subject(candidate_document)
    for profile_subject_id, previous_join in previous_joins.items():
        candidate_join = candidate_joins.get(profile_subject_id)
        if candidate_join is None:
            raise ValueError(
                "existing audience_triangulation join was not preserved for "
                f"profile_subject_id={profile_subject_id}: join is missing"
            )
        if candidate_join != previous_join:
            raise ValueError(
                "existing audience_triangulation join was not preserved for "
                f"profile_subject_id={profile_subject_id}: join changed"
            )


def _discover_retained_audience_pairs(
    *,
    previous_document: dict[str, Any],
    target_profile_subject_id: str,
) -> tuple[tuple[Path, ...], tuple[Path, ...]]:
    """Resolve prior validated joins from the current view's source inputs."""

    wrapper = previous_document.get("creator_profile_current_view")
    if not isinstance(wrapper, dict):
        return (), ()
    joins = _audience_joins_by_subject(previous_document)
    joins.pop(target_profile_subject_id, None)
    if not joins:
        return (), ()
    source_inputs = wrapper.get("source_inputs")
    if not isinstance(source_inputs, list):
        raise ValueError(
            "existing audience joins require audience snapshot source_inputs"
        )

    snapshot_candidates: list[tuple[Path, dict[str, Any]]] = []
    for source_input in source_inputs:
        if (
            not isinstance(source_input, dict)
            or source_input.get("role")
            != "validated transcript/comment audience triangulation snapshots"
        ):
            continue
        pointer = source_input.get("source_pointer")
        expected_sha256 = source_input.get("sha256")
        if not isinstance(pointer, str) or not pointer.strip():
            raise ValueError("audience snapshot source_input has no source_pointer")
        snapshot_path = Path(pointer)
        if not snapshot_path.is_absolute():
            snapshot_path = ROOT / snapshot_path
        if not snapshot_path.is_file():
            raise ValueError(
                f"audience snapshot source_input is missing: {snapshot_path}"
            )
        actual_sha256 = hashlib.sha256(
            snapshot_path.read_bytes().replace(b"\r\n", b"\n")
        ).hexdigest()
        if expected_sha256 != actual_sha256:
            raise ValueError(
                f"audience snapshot source_input hash mismatch: {snapshot_path}"
            )
        snapshots = load_json(snapshot_path)
        if not isinstance(snapshots, dict):
            raise ValueError(f"audience snapshot is not an object: {snapshot_path}")
        snapshot_candidates.append((snapshot_path, snapshots))

    retained_snapshots: list[Path] = []
    retained_outcomes: list[Path] = []
    for profile_subject_id, joined in sorted(joins.items()):
        matching_snapshots = [
            (path, snapshot)
            for path, snapshot in snapshot_candidates
            if snapshot.get("profile_subject_id") == profile_subject_id
            and snapshot.get("snapshot_id") == joined.get("snapshot_id")
            and snapshot.get("input_bundle_hash")
            == joined.get("input_bundle_hash")
        ]
        if len(matching_snapshots) != 1:
            raise ValueError(
                "existing audience join must resolve to exactly one hash-bound "
                f"snapshot source_input: profile_subject_id={profile_subject_id}"
            )
        snapshot_path, _snapshot = matching_snapshots[0]
        outcome_candidates: list[Path] = []
        for outcome_path in snapshot_path.parent.glob(
            "*creator_audience_judgment_outcome*.json"
        ):
            try:
                verify_audience_judgment_outcomes(
                    (snapshot_path,), (outcome_path,)
                )
            except (OSError, ValueError, json.JSONDecodeError):
                continue
            outcome_candidates.append(outcome_path)
        if len(outcome_candidates) != 1:
            raise ValueError(
                "existing audience join must resolve to exactly one successful "
                f"sibling Judgment outcome: profile_subject_id={profile_subject_id}"
            )
        retained_snapshots.append(snapshot_path)
        retained_outcomes.append(outcome_candidates[0])
    return tuple(retained_snapshots), tuple(retained_outcomes)


def _packet_result(results: Sequence[dict[str, Any]], packet_id: str, lane: str) -> dict[str, Any]:
    matches = [row for row in results if row.get("packet_id") == packet_id]
    if len(matches) != 1:
        raise ValueError(f"{lane} did not return exactly one result for packet {packet_id}")
    result = matches[0]
    if result.get("status") not in _ALLOWED_SILVER_STATUSES:
        raise ValueError(f"{lane} failed for packet {packet_id}: {result}")
    return result


def prepare_onboarding(
    *,
    data_root: DataLakeRoot,
    packet_id: str,
    grid_packet_id: str | None = None,
    creator_id: str | None,
    profile_subject_id: str | None,
    question: str,
    evidence_cutoff: str,
    work_dir: Path,
) -> dict[str, Any]:
    """Produce packet-scoped Silver and a deterministic cold-Judgment handoff."""

    grid_anchor = grid_packet_id or packet_id
    if creator_id is None or profile_subject_id is None:
        identity = extract_tiktok_packet_identity(data_root, packet_id)
        expected_creator_id = f"tiktok:@{identity['public_handle']}"
        if creator_id is not None and creator_id != expected_creator_id:
            raise ValueError(
                "creator_id conflicts with the stable TikTok identity captured in the packet"
            )
        creator_id = creator_id or expected_creator_id
        profile_subject_id = resolve_tiktok_profile_subject_id(
            data_root=data_root,
            packet_id=packet_id,
            requested_id=profile_subject_id,
        )
    grid = _packet_result(
        run_tiktok_grid_observations(data_root=data_root, packet_ids=[grid_anchor]),
        grid_anchor,
        "TikTok grid observation",
    )
    comments = _packet_result(
        run_comment_attention(data_root=data_root, packet_ids=[packet_id]),
        packet_id,
        "TikTok comment attention",
    )
    work_dir.mkdir(parents=True, exist_ok=True)
    bundle_path = work_dir / f"{packet_id}.audience_bundle.json"
    prompt_path = work_dir / f"{packet_id}.audience_prompt.txt"
    prepared = prepare_subscription_judgment(
        data_root=data_root,
        packet_id=packet_id,
        grid_packet_id=grid_anchor,
        creator_id=creator_id,
        profile_subject_id=profile_subject_id,
        question=question,
        evidence_cutoff=evidence_cutoff,
        bundle_out=bundle_path,
        prompt_out=prompt_path,
    )
    return {
        **prepared,
        "status": "awaiting_judgment",
        "stage_reached": "judgment_prepared",
        "silver_prerequisites": {
            "grid_observation": grid["status"],
            "grid_packet_id": grid_anchor,
            "comment_attention": comments["status"],
            "comment_packet_id": packet_id,
        },
        "capture_reusable": True,
        "recapture_required": False,
        "safe_next_action": (
            "run one cold subscription context with prompt_out, then submit its exact "
            "response bytes through this coordinator"
        ),
    }


def submit_onboarding(
    *,
    data_root: DataLakeRoot,
    bundle_path: Path,
    response_bytes: bytes,
    snapshot_out: Path,
) -> dict[str, Any]:
    return submit_subscription_judgment(
        data_root=data_root,
        bundle_path=bundle_path,
        response_bytes=response_bytes,
        snapshot_out=snapshot_out,
    )


def enqueue_onboarding(
    *, data_root: DataLakeRoot, bundle_path: Path, prompt_path: Path
) -> dict[str, Any]:
    return enqueue_creator_audience_job(
        data_root=data_root, bundle_path=bundle_path, prompt_path=prompt_path
    )


def claim_onboarding_job(
    *, data_root: DataLakeRoot, worker_id: str, prompt_out: Path
) -> dict[str, Any]:
    claim = claim_creator_audience_job(
        data_root=data_root, worker_id=worker_id, prompt_out=prompt_out
    )
    if claim.get("status") != "claimed":
        return claim
    job = require_active_claim(
        data_root=data_root,
        job_id=str(claim["job_id"]),
        lease_id=str(claim["lease_id"]),
    )
    outcomes = _validated_outcomes_for_job(data_root, job)
    if len(outcomes) > 1:
        raise CreatorAudienceQueueError(
            "queue recovery found multiple validated outcomes for one bundle"
        )
    if not outcomes:
        return claim
    outcome_path, outcome = outcomes[0]
    completed = complete_onboarding_to_lake(
        data_root=data_root,
        packet_id=str(job["raw_anchor"]),
        outcome_path=outcome_path,
    )
    terminal = write_creator_audience_terminal(
        data_root=data_root,
        job_id=str(job["job_id"]),
        lease_id=str(claim["lease_id"]),
        status="succeeded",
        details=_success_terminal_details(data_root, outcome_path, outcome, completed),
    )
    prompt_out.unlink(missing_ok=True)
    return {
        "status": "recovered_succeeded",
        "job_id": job["job_id"],
        "lease_id": claim["lease_id"],
        "terminal": terminal,
        "registry_completion": completed,
        "model_api_calls": 0,
    }


def submit_onboarding_job(
    *,
    data_root: DataLakeRoot,
    job_id: str,
    lease_id: str,
    response_bytes: bytes,
) -> dict[str, Any]:
    job = require_active_claim(
        data_root=data_root, job_id=job_id, lease_id=lease_id
    )
    with tempfile.TemporaryDirectory(prefix="forseti-creator-audience-queue-") as work:
        work_dir = Path(work)
        bundle_path = materialize_claim_bundle(job, work_dir / "bundle.json")
        result = submit_onboarding(
            data_root=data_root,
            bundle_path=bundle_path,
            response_bytes=response_bytes,
            snapshot_out=work_dir / "snapshot.json",
        )
    if result.get("status") != "validated":
        return {
            **result,
            "judgment_status": result.get("status"),
            "status": "correction_required",
            "queue_state": "running",
            "job_id": job_id,
            "lease_id": lease_id,
            "safe_next_action": (
                "return only validation_errors to the same cold context and resubmit "
                "before lease expiry, explicitly block, or allow lease recovery"
            ),
        }
    outcome_path = Path(str(result["judgment_outcome_path"]))
    outcome = load_json(outcome_path)
    completed = complete_onboarding_to_lake(
        data_root=data_root,
        packet_id=str(job["raw_anchor"]),
        outcome_path=outcome_path,
    )
    terminal = write_creator_audience_terminal(
        data_root=data_root,
        job_id=job_id,
        lease_id=lease_id,
        status="succeeded",
        details=_success_terminal_details(data_root, outcome_path, outcome, completed),
    )
    return {
        "status": "succeeded",
        "job_id": job_id,
        "lease_id": lease_id,
        "judgment": result,
        "registry_completion": completed,
        "terminal": terminal,
        "model_api_calls": 0,
    }


def block_onboarding_job(
    *, data_root: DataLakeRoot, job_id: str, lease_id: str, reason: str
) -> dict[str, Any]:
    if not reason.strip():
        raise CreatorAudienceQueueError("queue block reason must be nonblank")
    job = require_active_claim(
        data_root=data_root, job_id=job_id, lease_id=lease_id
    )
    if _validated_outcomes_for_job(data_root, job):
        raise CreatorAudienceQueueError(
            "cannot block a job that has a validated outcome awaiting completion"
        )
    terminal = write_creator_audience_terminal(
        data_root=data_root,
        job_id=job_id,
        lease_id=lease_id,
        status="blocked",
        details={"reason": reason.strip()},
    )
    return {
        "status": "blocked",
        "job_id": job_id,
        "lease_id": lease_id,
        "terminal": terminal,
        "registry_written": False,
        "model_api_calls": 0,
    }


def _validated_outcomes_for_job(
    data_root: DataLakeRoot, job: Mapping[str, Any]
) -> list[tuple[Path, dict[str, Any]]]:
    lane = data_root.lane_dir(
        subtree="derived",
        raw_anchor=str(job["raw_anchor"]),
        lane="creator_audience_judgment_outcome",
    )
    if not lane.is_dir():
        return []
    matches: list[tuple[Path, dict[str, Any]]] = []
    for path in sorted(lane.iterdir(), key=lambda item: item.name):
        if not path.is_file():
            continue
        outcome = load_json(path)
        if (
            outcome.get("schema_version") == "creator_audience_judgment_outcome_v1"
            and outcome.get("status") == "validated"
            and outcome.get("bundle_hash") == job["bundle_hash"]
            and outcome.get("profile_subject_id") == job["profile_subject_id"]
            and outcome.get("raw_anchor") == job["raw_anchor"]
        ):
            matches.append((path, outcome))
    return matches


def _success_terminal_details(
    data_root: DataLakeRoot,
    outcome_path: Path,
    outcome: Mapping[str, Any],
    completed: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "judgment_outcome_record_id": outcome.get("record_id"),
        "judgment_outcome_record_ref": outcome_path.resolve()
        .relative_to(data_root.path.resolve())
        .as_posix(),
        "snapshot_id": outcome.get("snapshot_id_or_none"),
        "registry_admission_record_id": completed.get("record_id"),
        "profile_subject_id": completed.get("platform_account_id"),
    }


def complete_onboarding(
    *,
    snapshot_path: Path,
    outcome_path: Path,
    retained_snapshot_paths: Sequence[Path] = (),
    retained_outcome_paths: Sequence[Path] = (),
    output_path: Path,
    account_ledger_path: Path,
    creator_registry_index_path: Path,
    metric_seed_paths: Sequence[Path],
    generated_at_utc: str | None,
    preflight_receipt_path: Path | None,
) -> dict[str, Any]:
    """Materialize and verify a candidate before atomically publishing it."""

    if len(retained_snapshot_paths) != len(retained_outcome_paths):
        raise ValueError(
            "retained audience snapshot and Judgment outcome counts must match"
        )
    raw_outcome = load_json(outcome_path)
    outcome_model = (
        CreatorAudienceJudgmentOutcomeV1
        if raw_outcome.get("schema_version") == "creator_audience_judgment_outcome_v1"
        else CreatorAudienceJudgmentOutcome
    )
    outcome = outcome_model.model_validate(raw_outcome)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    previous_output = output_path.read_bytes() if output_path.exists() else None
    if (
        previous_output is not None
        and not retained_snapshot_paths
        and not retained_outcome_paths
    ):
        (
            retained_snapshot_paths,
            retained_outcome_paths,
        ) = _discover_retained_audience_pairs(
            previous_document=json.loads(previous_output),
            target_profile_subject_id=outcome.profile_subject_id,
        )
    with tempfile.NamedTemporaryFile(
        dir=output_path.parent,
        prefix=f".{output_path.name}.",
        suffix=".candidate",
        delete=False,
    ) as candidate_file:
        candidate_path = Path(candidate_file.name)
    if previous_output is None:
        candidate_path.unlink()
    else:
        candidate_path.write_bytes(previous_output)

    argv = [
        "--output",
        str(candidate_path),
        "--account-ledger",
        str(account_ledger_path),
        "--creator-registry-index",
        str(creator_registry_index_path),
        "--write",
    ]
    audience_pairs = sorted(
        zip(
            (*retained_snapshot_paths, snapshot_path),
            (*retained_outcome_paths, outcome_path),
            strict=True,
        ),
        key=lambda pair: str(pair[0].resolve()),
    )
    for audience_snapshot, _audience_outcome in audience_pairs:
        argv.extend(("--audience-triangulation-snapshot", str(audience_snapshot)))
    for _audience_snapshot, audience_outcome in audience_pairs:
        argv.extend(("--audience-judgment-outcome", str(audience_outcome)))
    for metric_seed in metric_seed_paths:
        argv.extend(("--metric-seed", str(metric_seed)))
    if generated_at_utc:
        argv.extend(("--generated-at-utc", generated_at_utc))
    if preflight_receipt_path:
        argv.extend(("--preflight-receipt", str(preflight_receipt_path)))

    stderr = io.StringIO()
    try:
        try:
            with redirect_stderr(stderr):
                exit_code = materialize_main(argv)
        except SystemExit as exc:
            raise ValueError(
                f"creator profile materialization failed with exit {exc.code}: "
                f"{stderr.getvalue().strip()}"
            ) from exc
        if exit_code != 0:
            raise ValueError(
                f"creator profile materialization failed with exit {exit_code}: "
                f"{stderr.getvalue().strip()}"
            )

        document = load_json(candidate_path)
        wrapper = document.get("creator_profile_current_view")
        profiles = wrapper.get("profiles") if isinstance(wrapper, dict) else None
        if not isinstance(profiles, list):
            raise ValueError("materialized creator profile view has no profiles list")
        matches = [
            profile
            for profile in profiles
            if isinstance(profile, dict)
            and profile.get("profile_subject_id") == outcome.profile_subject_id
        ]
        if len(matches) != 1:
            raise ValueError("materialized view does not contain exactly one target profile")
        joined = matches[0].get("audience_triangulation")
        if (
            not isinstance(joined, dict)
            or joined.get("snapshot_id") != outcome.snapshot_id_or_none
            or joined.get("input_bundle_hash") != outcome.bundle_hash
        ):
            raise ValueError("materialized profile did not join the exact validated snapshot")
        _verify_existing_audience_joins_preserved(
            previous_output=previous_output,
            candidate_document=document,
        )

        current_output = output_path.read_bytes() if output_path.exists() else None
        if current_output != previous_output:
            raise ValueError("creator profile output changed during materialization")
        os.replace(candidate_path, output_path)
    finally:
        candidate_path.unlink(missing_ok=True)

    return {
        "status": "complete",
        "stage_reached": "verified_materialization",
        "creator_id": outcome.creator_id,
        "profile_subject_id": outcome.profile_subject_id,
        "packet_id": outcome.raw_anchor,
        "bundle_id": outcome.bundle_id,
        "bundle_hash": outcome.bundle_hash,
        "snapshot_id": outcome.snapshot_id_or_none,
        "registry_field_joined": "audience_triangulation",
        "output": str(output_path),
        "model_api_calls": 0,
    }


def complete_onboarding_to_lake(
    *, data_root: DataLakeRoot, packet_id: str, outcome_path: Path
) -> dict[str, Any]:
    """Promote one validated outcome without writing any repository projection."""
    result = admit_tiktok_creator_account(
        data_root=data_root,
        packet_id=packet_id,
        judgment_outcome_path=outcome_path,
    )
    return {
        **result,
        "stage_reached": "lake_registry_admission_published_and_read_back",
        "registry_authority": "data_lake",
        "repository_projection_written": False,
        "model_api_calls": 0,
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    prepare = subparsers.add_parser("prepare")
    prepare.add_argument("--data-root", required=True)
    prepare.add_argument("--packet-id", required=True)
    prepare.add_argument("--grid-packet-id")
    prepare.add_argument("--creator-id")
    prepare.add_argument("--profile-subject-id")
    prepare.add_argument("--question", required=True)
    prepare.add_argument("--evidence-cutoff", required=True)
    prepare.add_argument("--work-dir", type=Path, required=True)
    prepare.add_argument("--enqueue", action="store_true")

    submit = subparsers.add_parser("submit")
    submit.add_argument("--data-root", required=True)
    submit.add_argument("--bundle", type=Path, required=True)
    response = submit.add_mutually_exclusive_group(required=True)
    response.add_argument("--response", type=Path)
    response.add_argument("--response-stdin", action="store_true")
    submit.add_argument("--snapshot-out", type=Path, required=True)

    complete = subparsers.add_parser("complete")
    complete.add_argument("--data-root", required=True)
    complete.add_argument("--packet-id", required=True)
    complete.add_argument("--outcome", type=Path, required=True)

    enqueue = subparsers.add_parser("queue-enqueue")
    enqueue.add_argument("--data-root", required=True)
    enqueue.add_argument("--bundle", type=Path, required=True)
    enqueue.add_argument("--prompt", type=Path, required=True)

    show = subparsers.add_parser("queue-show")
    show.add_argument("--data-root", required=True)

    claim = subparsers.add_parser("queue-claim")
    claim.add_argument("--data-root", required=True)
    claim.add_argument("--worker-id", required=True)
    claim.add_argument("--prompt-out", type=Path, required=True)

    queue_submit = subparsers.add_parser("queue-submit")
    queue_submit.add_argument("--data-root", required=True)
    queue_submit.add_argument("--job-id", required=True)
    queue_submit.add_argument("--lease-id", required=True)
    queue_response = queue_submit.add_mutually_exclusive_group(required=True)
    queue_response.add_argument("--response", type=Path)
    queue_response.add_argument("--response-stdin", action="store_true")

    block = subparsers.add_parser("queue-block")
    block.add_argument("--data-root", required=True)
    block.add_argument("--job-id", required=True)
    block.add_argument("--lease-id", required=True)
    block.add_argument("--reason", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        data_root = DataLakeRoot.resolve(explicit=args.data_root)
        if args.command == "prepare":
            result = prepare_onboarding(
                data_root=data_root,
                packet_id=args.packet_id,
                grid_packet_id=args.grid_packet_id,
                creator_id=args.creator_id,
                profile_subject_id=args.profile_subject_id,
                question=args.question,
                evidence_cutoff=args.evidence_cutoff,
                work_dir=args.work_dir,
            )
            if args.enqueue:
                result = {
                    **result,
                    "queue": enqueue_onboarding(
                        data_root=data_root,
                        bundle_path=Path(str(result["bundle_out"])),
                        prompt_path=Path(str(result["prompt_out"])),
                    ),
                }
        elif args.command == "submit":
            response_bytes = (
                sys.stdin.buffer.read()
                if args.response_stdin
                else args.response.read_bytes()
            )
            result = submit_onboarding(
                data_root=data_root,
                bundle_path=args.bundle,
                response_bytes=response_bytes,
                snapshot_out=args.snapshot_out,
            )
        elif args.command == "complete":
            result = complete_onboarding_to_lake(
                data_root=data_root,
                packet_id=args.packet_id,
                outcome_path=args.outcome,
            )
        elif args.command == "queue-enqueue":
            result = enqueue_onboarding(
                data_root=data_root,
                bundle_path=args.bundle,
                prompt_path=args.prompt,
            )
        elif args.command == "queue-show":
            result = public_queue_view(data_root)
        elif args.command == "queue-claim":
            result = claim_onboarding_job(
                data_root=data_root,
                worker_id=args.worker_id,
                prompt_out=args.prompt_out,
            )
        elif args.command == "queue-submit":
            response_bytes = (
                sys.stdin.buffer.read()
                if args.response_stdin
                else args.response.read_bytes()
            )
            result = submit_onboarding_job(
                data_root=data_root,
                job_id=args.job_id,
                lease_id=args.lease_id,
                response_bytes=response_bytes,
            )
        else:
            result = block_onboarding_job(
                data_root=data_root,
                job_id=args.job_id,
                lease_id=args.lease_id,
                reason=args.reason,
            )
    except (DataLakeRootError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, indent=2, sort_keys=True))
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 2 if result.get("status") in {"blocked", "correction_required"} else 0


if __name__ == "__main__":
    raise SystemExit(main())
