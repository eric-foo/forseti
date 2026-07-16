"""Prepare and submit one Instagram creator-audience Judgment from admitted Silver."""
from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from data_lake.root import DataLakeRoot, DataLakeRootError
from evidence_binding.instagram_audience_triangulation import (
    build_instagram_creator_audience_evidence_bundle,
)
from evidence_binding.tiktok_audience_triangulation import (
    ASSEMBLY_RECEIPT_LANE,
    build_assembly_receipt,
)
from judgment.creator_audience import build_creator_audience_prompt, load_method_deck
from runners.run_tiktok_creator_audience_triangulation import (
    _write_new,
    _write_new_json,
    submit_subscription_judgment,
)
from source_capture.ig_reels_deep_capture_lake import (
    AUDIENCE_COMMENTS_LANE,
    REEL_TRANSCRIPT_LANE,
    current_deep_capture_record,
)


def _load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def _load_admitted_silver_record(
    data_root: DataLakeRoot, path: Path, *, lane: str
) -> dict[str, Any]:
    resolved = path.resolve(strict=True)
    try:
        resolved.relative_to(data_root.path.resolve())
    except ValueError as exc:
        raise ValueError(
            f"record is outside the admitted Silver lane {lane}: {path}"
        ) from exc
    raw_anchor = resolved.parent.parent.name
    expected_lane = data_root.lane_dir(
        subtree="derived", raw_anchor=raw_anchor, lane=lane
    ).resolve()
    if resolved.parent != expected_lane:
        raise ValueError(f"record is outside the admitted Silver lane {lane}: {path}")
    record = _load_object(resolved)
    if isinstance(record.get("payload"), Mapping):
        record_id = record.get("record_id")
        if not isinstance(record_id, str):
            raise ValueError(f"Silver envelope lacks record_id: {path}")
        expected_path = data_root.record_path(
            subtree="derived", raw_anchor=raw_anchor, lane=lane, record_id=record_id
        ).resolve()
        if resolved != expected_path or not current_deep_capture_record(
            data_root,
            record=record,
            raw_anchor=raw_anchor,
            lane=lane,
            record_id=record_id,
        ):
            raise ValueError(f"Silver envelope is not current and source-valid: {path}")
    elif record.get("reel_shortcode") != raw_anchor:
        raise ValueError(f"legacy Silver record does not match its Reel anchor: {path}")
    return record


def prepare_instagram_subscription_judgment(
    *,
    data_root: DataLakeRoot,
    creator_id: str,
    profile_subject_id: str,
    primary_raw_anchor: str,
    comment_record_paths: Sequence[Path],
    transcript_record_paths: Sequence[Path],
    question: str,
    evidence_cutoff: str,
    bundle_out: Path,
    prompt_out: Path,
) -> dict[str, Any]:
    if bundle_out.resolve() == prompt_out.resolve():
        raise ValueError("bundle_out and prompt_out must be different files")
    bundle = build_instagram_creator_audience_evidence_bundle(
        creator_id=creator_id,
        profile_subject_id=profile_subject_id,
        primary_raw_anchor=primary_raw_anchor,
        comment_records=[
            _load_admitted_silver_record(data_root, path, lane=AUDIENCE_COMMENTS_LANE)
            for path in comment_record_paths
        ],
        transcript_records=[
            _load_admitted_silver_record(data_root, path, lane=REEL_TRANSCRIPT_LANE)
            for path in transcript_record_paths
        ],
        question=question,
        evidence_cutoff=evidence_cutoff,
    )
    _write_new_json(bundle_out, bundle)
    _write_new(prompt_out, build_creator_audience_prompt(bundle) + "\n")

    receipt = build_assembly_receipt(bundle)
    receipt_bytes = (
        json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8")
        + b"\n"
    )
    receipt_path = data_root.record_path(
        subtree="derived",
        raw_anchor=primary_raw_anchor,
        lane=ASSEMBLY_RECEIPT_LANE,
        record_id=str(receipt["record_id"]),
    )
    if receipt_path.exists():
        if receipt_path.read_bytes() != receipt_bytes:
            raise ValueError("existing Instagram audience assembly receipt differs")
    else:
        data_root.append_record(
            subtree="derived",
            raw_anchor=primary_raw_anchor,
            lane=ASSEMBLY_RECEIPT_LANE,
            record_id=str(receipt["record_id"]),
            data=receipt_bytes,
        )
    _, method_hash = load_method_deck()
    return {
        "status": "SUBSCRIPTION_JUDGMENT_REQUIRED",
        "creator_id": bundle["creator_id"],
        "profile_subject_id": bundle["profile_subject_id"],
        "platform_scope": "instagram",
        "primary_raw_anchor": primary_raw_anchor,
        "bundle_id": bundle["bundle_id"],
        "bundle_hash": bundle["bundle_hash"],
        "method_deck_sha256": method_hash,
        "bundle_out": str(bundle_out),
        "prompt_out": str(prompt_out),
        "assembly_receipt_record_id": receipt["record_id"],
        "compatibility_residual_count": len(
            bundle["source_refs"]["compatibility_residuals"]
        ),
        "model_api_calls": 0,
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    prepare = subparsers.add_parser("prepare")
    prepare.add_argument("--data-root", required=True)
    prepare.add_argument("--creator-id", required=True)
    prepare.add_argument("--profile-subject-id", required=True)
    prepare.add_argument("--primary-raw-anchor", required=True)
    prepare.add_argument("--comment-record", type=Path, action="append", required=True)
    prepare.add_argument("--transcript-record", type=Path, action="append", required=True)
    prepare.add_argument("--question", required=True)
    prepare.add_argument("--evidence-cutoff", required=True)
    prepare.add_argument("--bundle-out", type=Path, required=True)
    prepare.add_argument("--prompt-out", type=Path, required=True)

    submit = subparsers.add_parser("submit")
    submit.add_argument("--data-root", required=True)
    submit.add_argument("--bundle", type=Path, required=True)
    response = submit.add_mutually_exclusive_group(required=True)
    response.add_argument("--response", type=Path)
    response.add_argument("--response-stdin", action="store_true")
    submit.add_argument("--snapshot-out", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command == "prepare":
            result = prepare_instagram_subscription_judgment(
                data_root=DataLakeRoot.resolve(explicit=args.data_root),
                creator_id=args.creator_id,
                profile_subject_id=args.profile_subject_id,
                primary_raw_anchor=args.primary_raw_anchor,
                comment_record_paths=args.comment_record,
                transcript_record_paths=args.transcript_record,
                question=args.question,
                evidence_cutoff=args.evidence_cutoff,
                bundle_out=args.bundle_out,
                prompt_out=args.prompt_out,
            )
        else:
            response_bytes = (
                sys.stdin.buffer.read()
                if args.response_stdin
                else args.response.read_bytes()
            )
            result = submit_subscription_judgment(
                data_root=DataLakeRoot.resolve(explicit=args.data_root),
                bundle_path=args.bundle,
                response_bytes=response_bytes,
                snapshot_out=args.snapshot_out,
            )
    except (DataLakeRootError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, indent=2, sort_keys=True))
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 2 if result.get("status") == "blocked" else 0


if __name__ == "__main__":
    raise SystemExit(main())