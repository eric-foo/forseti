"""Resume-safe controller for one admitted TikTok creator onboarding."""
from __future__ import annotations

import argparse
import io
import json
import os
import tempfile
import sys
from contextlib import redirect_stderr
from pathlib import Path
from typing import Any, Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from capture_spine.creator_profile_current.materialize import load_json
from data_lake.root import DataLakeRoot, DataLakeRootError
from runners.run_creator_profile_current_materialize import main as materialize_main
from runners.run_tiktok_comment_attention_producer import run_comment_attention
from runners.run_tiktok_creator_audience_triangulation import (
    submit_subscription_judgment,
    prepare_subscription_judgment,
)
from runners.run_tiktok_grid_observation_producer import run_tiktok_grid_observations
from schemas.tiktok_audience_evidence_models import CreatorAudienceJudgmentOutcome


_ALLOWED_SILVER_STATUSES = {"derived", "already_current"}


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
    creator_id: str,
    profile_subject_id: str,
    question: str,
    evidence_cutoff: str,
    work_dir: Path,
) -> dict[str, Any]:
    """Produce packet-scoped Silver and a deterministic cold-Judgment handoff."""

    grid = _packet_result(
        run_tiktok_grid_observations(data_root=data_root, packet_ids=[packet_id]),
        packet_id,
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
            "comment_attention": comments["status"],
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


def complete_onboarding(
    *,
    snapshot_path: Path,
    outcome_path: Path,
    output_path: Path,
    account_ledger_path: Path,
    creator_registry_index_path: Path,
    metric_seed_paths: Sequence[Path],
    generated_at_utc: str | None,
    preflight_receipt_path: Path | None,
) -> dict[str, Any]:
    """Materialize and verify a candidate before atomically publishing it."""

    outcome = CreatorAudienceJudgmentOutcome.model_validate(load_json(outcome_path))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    previous_output = output_path.read_bytes() if output_path.exists() else None
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
        "--audience-triangulation-snapshot",
        str(snapshot_path),
        "--audience-judgment-outcome",
        str(outcome_path),
        "--write",
    ]
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


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    prepare = subparsers.add_parser("prepare")
    prepare.add_argument("--data-root", required=True)
    prepare.add_argument("--packet-id", required=True)
    prepare.add_argument("--creator-id", required=True)
    prepare.add_argument("--profile-subject-id", required=True)
    prepare.add_argument("--question", required=True)
    prepare.add_argument("--evidence-cutoff", required=True)
    prepare.add_argument("--work-dir", type=Path, required=True)

    submit = subparsers.add_parser("submit")
    submit.add_argument("--data-root", required=True)
    submit.add_argument("--bundle", type=Path, required=True)
    response = submit.add_mutually_exclusive_group(required=True)
    response.add_argument("--response", type=Path)
    response.add_argument("--response-stdin", action="store_true")
    submit.add_argument("--snapshot-out", type=Path, required=True)

    complete = subparsers.add_parser("complete")
    complete.add_argument("--snapshot", type=Path, required=True)
    complete.add_argument("--outcome", type=Path, required=True)
    complete.add_argument("--output", type=Path, required=True)
    complete.add_argument("--account-ledger", type=Path, required=True)
    complete.add_argument("--creator-registry-index", type=Path, required=True)
    complete.add_argument("--metric-seed", type=Path, action="append", default=[])
    complete.add_argument("--generated-at-utc")
    complete.add_argument("--preflight-receipt", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command == "prepare":
            result = prepare_onboarding(
                data_root=DataLakeRoot.resolve(explicit=args.data_root),
                packet_id=args.packet_id,
                creator_id=args.creator_id,
                profile_subject_id=args.profile_subject_id,
                question=args.question,
                evidence_cutoff=args.evidence_cutoff,
                work_dir=args.work_dir,
            )
        elif args.command == "submit":
            response_bytes = (
                sys.stdin.buffer.read()
                if args.response_stdin
                else args.response.read_bytes()
            )
            result = submit_onboarding(
                data_root=DataLakeRoot.resolve(explicit=args.data_root),
                bundle_path=args.bundle,
                response_bytes=response_bytes,
                snapshot_out=args.snapshot_out,
            )
        else:
            result = complete_onboarding(
                snapshot_path=args.snapshot,
                outcome_path=args.outcome,
                output_path=args.output,
                account_ledger_path=args.account_ledger,
                creator_registry_index_path=args.creator_registry_index,
                metric_seed_paths=args.metric_seed,
                generated_at_utc=args.generated_at_utc,
                preflight_receipt_path=args.preflight_receipt,
            )
    except (DataLakeRootError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, indent=2, sort_keys=True))
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 2 if result.get("status") == "blocked" else 0


if __name__ == "__main__":
    raise SystemExit(main())
