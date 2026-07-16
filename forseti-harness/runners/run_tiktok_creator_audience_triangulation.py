"""Prepare and validate one subscription-only creator-audience triangulation."""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from capture_spine.creator_profile_current.tiktok_comment_attention_producer import (
    COMMENT_ATTENTION_LANE,
    COMMENT_ATTENTION_POLICY_FINGERPRINT,
    COMMENT_ATTENTION_RECIPE_VERSION,
)
from capture_spine.creator_profile_current.tiktok_grid_observation_producer import (
    SOCIAL_METRIC_OBSERVATION_SET_LANE,
    TIKTOK_GRID_OBSERVATION_POLICY_FINGERPRINT,
    TIKTOK_GRID_OBSERVATION_POLICY_VERSION,
)
from data_lake.root import DataLakeRoot, DataLakeRootError
from data_lake.silver_record import (
    CURRENT_SOURCE_BACKED_AUTHORITY,
    classify_silver_vault_record_sources,
)
from evidence_binding.tiktok_audience_triangulation import (
    ASSEMBLY_RECEIPT_LANE,
    _canonical_bytes,
    build_assembly_receipt,
    build_creator_audience_evidence_bundle,
)
from judgment.creator_audience import (
    METHOD_DECK_RELATIVE_PATH,
    build_creator_audience_prompt,
    load_method_deck,
    parse_creator_audience_response,
)
from judgment.tiktok_audience_triangulation import TriangulationValidationError
from source_capture.tiktok.batch_packet import (
    TIKTOK_BATCH_CAPTURE_JSON_NAME,
    TIKTOK_BATCH_CAPTURE_SURFACE,
)

from pydantic import ValidationError

from schemas.creator_audience_models import CreatorAudienceJudgmentOutcomeV1


JUDGMENT_OUTCOME_SCHEMA_VERSION = "creator_audience_judgment_outcome_v1"
JUDGMENT_OUTCOME_LANE = "creator_audience_judgment_outcome"


def _load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def _write_new(path: Path, text: str) -> None:
    encoded = text.encode("utf-8")
    if path.exists():
        if path.read_bytes() == encoded:
            return
        raise FileExistsError(f"refusing to replace existing output: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def _write_new_json(path: Path, value: Mapping[str, Any]) -> None:
    _write_new(path, json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def _read_lane(data_root: DataLakeRoot, *, raw_anchor: str, lane: str) -> list[dict[str, Any]]:
    directory = data_root.lane_dir(subtree="derived", raw_anchor=raw_anchor, lane=lane)
    if not directory.is_dir():
        return []
    records: list[dict[str, Any]] = []
    for path in sorted(directory.iterdir()):
        if not path.is_file():
            continue
        value = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            raise ValueError(f"derived record must be an object: {path}")
        records.append(value)
    return records


def _record_id(record: Mapping[str, Any]) -> str:
    return str(record.get("record_id") or "<missing-record-id>")


def _silver_eligibility_residual(
    data_root: DataLakeRoot, record: Mapping[str, Any], *, lane: str
) -> dict[str, Any] | None:
    authority = classify_silver_vault_record_sources(data_root, record)
    if authority.status == CURRENT_SOURCE_BACKED_AUTHORITY:
        return None
    residual = {
        "lane": lane,
        "record_id": _record_id(record),
        "status": authority.status,
        "reason_code": authority.reason_code,
    }
    if authority.error:
        residual["error"] = authority.error
    return residual


def _select_comment_attention_records(
    data_root: DataLakeRoot, records: Sequence[Mapping[str, Any]],
) -> tuple[list[Mapping[str, Any]], list[dict[str, Any]]]:
    selected: list[Mapping[str, Any]] = []
    residuals: list[dict[str, Any]] = []
    for record in records:
        ineligible = _silver_eligibility_residual(
            data_root, record, lane=COMMENT_ATTENTION_LANE
        )
        if ineligible is not None:
            residuals.append(ineligible)
            continue
        provenance = record.get("provenance") if isinstance(record.get("provenance"), Mapping) else {}
        actual_version = provenance.get("calculation_recipe_version")
        actual_fingerprint = provenance.get("policy_fingerprint_sha256")
        if (
            actual_version != COMMENT_ATTENTION_RECIPE_VERSION
            or actual_fingerprint != COMMENT_ATTENTION_POLICY_FINGERPRINT
        ):
            residuals.append({
                "lane": COMMENT_ATTENTION_LANE,
                "record_id": _record_id(record),
                "status": "policy_mismatch",
                "actual_policy_version": actual_version,
                "actual_policy_fingerprint_sha256": actual_fingerprint,
            })
            continue
        selected.append(record)
    return selected, residuals


def _select_grid_observation_records(
    data_root: DataLakeRoot, records: Sequence[Mapping[str, Any]],
) -> tuple[list[Mapping[str, Any]], list[dict[str, Any]]]:
    selected: list[Mapping[str, Any]] = []
    residuals: list[dict[str, Any]] = []
    for record in records:
        ineligible = _silver_eligibility_residual(
            data_root, record, lane=SOCIAL_METRIC_OBSERVATION_SET_LANE
        )
        if ineligible is not None:
            residuals.append(ineligible)
            continue
        payload = record.get("payload") if isinstance(record.get("payload"), Mapping) else {}
        observation = (
            payload.get("observation") if isinstance(payload.get("observation"), Mapping) else {}
        )
        actual_version = observation.get("policy_version")
        actual_fingerprint = observation.get("policy_fingerprint_sha256")
        if (
            actual_version != TIKTOK_GRID_OBSERVATION_POLICY_VERSION
            or actual_fingerprint != TIKTOK_GRID_OBSERVATION_POLICY_FINGERPRINT
        ):
            residuals.append({
                "lane": SOCIAL_METRIC_OBSERVATION_SET_LANE,
                "record_id": _record_id(record),
                "status": "policy_mismatch",
                "actual_policy_version": actual_version,
                "actual_policy_fingerprint_sha256": actual_fingerprint,
            })
            continue
        selected.append(record)
    if len(selected) > 1:
        raise ValueError("ambiguous current-policy TikTok grid-observation records")
    return selected, residuals


def select_current_audience_silver_records(
    *,
    data_root: DataLakeRoot,
    comment_attention_records: Sequence[Mapping[str, Any]],
    grid_observation_records: Sequence[Mapping[str, Any]],
) -> tuple[list[Mapping[str, Any]], list[Mapping[str, Any]], list[dict[str, Any]]]:
    attention, attention_residuals = _select_comment_attention_records(
        data_root, comment_attention_records
    )
    grid, grid_residuals = _select_grid_observation_records(
        data_root, grid_observation_records
    )
    return attention, grid, attention_residuals + grid_residuals


def _load_batch(data_root: DataLakeRoot, packet_id: str) -> dict[str, Any]:
    loaded = data_root.load_raw_packet(packet_id)
    if loaded.manifest.get("source_surface") != TIKTOK_BATCH_CAPTURE_SURFACE:
        raise ValueError(f"packet {packet_id} is not a TikTok creator batch admission")
    matches = [
        row
        for row in loaded.manifest.get("preserved_files", [])
        if isinstance(row, Mapping)
        and str(row.get("relative_packet_path") or "").endswith(TIKTOK_BATCH_CAPTURE_JSON_NAME)
    ]
    if len(matches) != 1:
        raise ValueError(f"packet {packet_id} requires exactly one preserved TikTok batch JSON")
    body = loaded.bodies.get(str(matches[0].get("file_id") or ""))
    if body is None:
        raise ValueError(f"packet {packet_id} TikTok batch body is absent")
    value = json.loads(body.decode("utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"packet {packet_id} TikTok batch body must be an object")
    return value


def _grid_refs(records: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "record_id": row.get("record_id"),
            "content_hash": row.get("content_hash"),
            "policy_fingerprint_sha256": (
                row.get("payload", {}).get("observation", {}).get("policy_fingerprint_sha256")
                if isinstance(row.get("payload"), Mapping)
                else None
            ),
        }
        for row in records
    ]


def prepare_subscription_judgment(
    *,
    data_root: DataLakeRoot,
    packet_id: str,
    creator_id: str,
    profile_subject_id: str,
    question: str,
    evidence_cutoff: str,
    bundle_out: Path,
    prompt_out: Path,
) -> dict[str, Any]:
    if bundle_out.resolve() == prompt_out.resolve():
        raise ValueError("bundle_out and prompt_out must be different files")
    batch = _load_batch(data_root, packet_id)
    attention_records = _read_lane(
        data_root, raw_anchor=packet_id, lane=COMMENT_ATTENTION_LANE
    )
    grid_records = _read_lane(
        data_root, raw_anchor=packet_id, lane=SOCIAL_METRIC_OBSERVATION_SET_LANE
    )
    attention, grid_records, silver_residuals = select_current_audience_silver_records(
        comment_attention_records=attention_records,
        grid_observation_records=grid_records,
        data_root=data_root,
    )
    if not attention:
        raise ValueError(
            "SILVER_AUDIENCE_EVIDENCE_REQUIRED: run the packet-scoped TikTok comment-attention producer"
        )
    if not grid_records:
        raise ValueError(
            "SILVER_AUDIENCE_EVIDENCE_REQUIRED: run the packet-scoped TikTok grid-observation producer"
        )
    method_text, method_hash = load_method_deck()
    bundle = build_creator_audience_evidence_bundle(
        creator_id=creator_id,
        profile_subject_id=profile_subject_id,
        raw_anchor=packet_id,
        batch_payload=batch,
        comment_attention_records=attention,
        grid_observation_refs=_grid_refs(grid_records),
        question=question,
        evidence_cutoff=evidence_cutoff,
        method_deck_path=METHOD_DECK_RELATIVE_PATH,
        method_deck_sha256=method_hash,
        silver_selection_residuals=silver_residuals,
    )
    _write_new_json(bundle_out, bundle)
    _write_new(
        prompt_out,
        build_creator_audience_prompt(bundle, method_text=method_text) + "\n",
    )

    receipt = build_assembly_receipt(bundle)
    receipt_path = data_root.record_path(
        subtree="derived",
        raw_anchor=packet_id,
        lane=ASSEMBLY_RECEIPT_LANE,
        record_id=str(receipt["record_id"]),
    )
    receipt_bytes = json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8") + b"\n"
    if receipt_path.exists():
        if receipt_path.read_bytes() != receipt_bytes:
            raise ValueError("existing audience assembly receipt differs")
    else:
        data_root.append_record(
            subtree="derived",
            raw_anchor=packet_id,
            lane=ASSEMBLY_RECEIPT_LANE,
            record_id=str(receipt["record_id"]),
            data=receipt_bytes,
        )
    return {
        "status": "SUBSCRIPTION_JUDGMENT_REQUIRED",
        "creator_id": bundle["creator_id"],
        "profile_subject_id": bundle["profile_subject_id"],
        "packet_id": packet_id,
        "bundle_id": bundle["bundle_id"],
        "bundle_hash": bundle["bundle_hash"],
        "bundle_out": str(bundle_out),
        "prompt_out": str(prompt_out),
        "assembly_receipt_record_id": receipt["record_id"],
        "silver_selection_residual_count": len(silver_residuals),
        "model_api_calls": 0,
    }


def validate_subscription_judgment(
    *, bundle_path: Path, response_path: Path, snapshot_out: Path
) -> dict[str, Any]:
    bundle = _load_object(bundle_path)
    response_text = response_path.read_text(encoding="utf-8")
    snapshot = parse_creator_audience_response(response_text, bundle)
    document = snapshot.model_dump(mode="json")
    _write_new_json(snapshot_out, document)
    return {
        "status": "validated",
        "creator_id": snapshot.creator_id,
        "profile_subject_id": snapshot.profile_subject_id,
        "snapshot_id": snapshot.snapshot_id,
        "snapshot_out": str(snapshot_out),
        "model_api_calls": 0,
    }


_BUNDLE_DERIVED_KEYS = frozenset({"bundle_hash", "bundle_id", "serialized_utf8_bytes"})


def _verify_bundle_integrity(
    data_root: DataLakeRoot, bundle: Mapping[str, Any], bundle_path: Path
) -> None:
    """Reject a scratch bundle whose declared hash does not close over its content.

    The bundle is a transport file, so its self-declared identity is only
    evidence once recomputed; every downstream identity check chains off it.
    """

    core = {key: value for key, value in bundle.items() if key not in _BUNDLE_DERIVED_KEYS}
    expected_hash = f"sha256:{hashlib.sha256(_canonical_bytes(core)).hexdigest()}"
    if bundle.get("bundle_hash") != expected_hash:
        raise ValueError(
            f"bundle_hash does not close over bundle content: {bundle_path}"
        )
    serialized_core = {
        key: value for key, value in bundle.items() if key != "serialized_utf8_bytes"
    }
    if bundle.get("serialized_utf8_bytes") != len(_canonical_bytes(serialized_core)):
        raise ValueError(
            f"serialized_utf8_bytes does not close over bundle content: {bundle_path}"
        )

    expected_receipt = build_assembly_receipt(bundle)
    receipt_path = data_root.record_path(
        subtree="derived",
        raw_anchor=str(bundle.get("raw_anchor")),
        lane=ASSEMBLY_RECEIPT_LANE,
        record_id=str(expected_receipt["record_id"]),
    )
    if not receipt_path.is_file():
        raise ValueError(
            f"persisted audience assembly receipt is missing for bundle: {bundle_path}"
        )
    if _load_object(receipt_path) != expected_receipt:
        raise ValueError(
            f"persisted audience assembly receipt does not match bundle: {bundle_path}"
        )


def submit_subscription_judgment(
    *,
    data_root: DataLakeRoot,
    bundle_path: Path,
    response_bytes: bytes,
    snapshot_out: Path,
) -> dict[str, Any]:
    """Persist an exact response and either one validated snapshot or all blockers."""

    bundle = _load_object(bundle_path)
    _verify_bundle_integrity(data_root, bundle, bundle_path)
    response_sha256 = f"sha256:{hashlib.sha256(response_bytes).hexdigest()}"
    snapshot_document: dict[str, Any] | None = None
    snapshot_text: str | None = None
    validation_errors: list[str] = []
    try:
        response_text = response_bytes.decode("utf-8-sig")
        snapshot = parse_creator_audience_response(response_text, bundle)
        snapshot_document = snapshot.model_dump(mode="json")
        snapshot_text = (
            json.dumps(
                snapshot_document, ensure_ascii=False, indent=2, sort_keys=True
            )
            + "\n"
        )
    except TriangulationValidationError as exc:
        validation_errors = list(exc.errors)
    except ValidationError as exc:
        validation_errors = [
            f"{'.'.join(str(part) for part in error['loc'])}: {error['msg']}"
            for error in exc.errors(include_url=False)
        ]
    except (UnicodeDecodeError, ValueError) as exc:
        validation_errors = [str(exc)]

    status = "validated" if snapshot_document is not None else "blocked"
    snapshot_sha256 = (
        f"sha256:{hashlib.sha256(snapshot_text.encode('utf-8')).hexdigest()}"
        if snapshot_text is not None
        else None
    )
    record_key = "\0".join(
        (
            str(bundle.get("raw_anchor")),
            str(bundle.get("bundle_hash")),
            response_sha256,
        )
    ).encode("utf-8")
    record_id = f"cajo_{hashlib.sha256(record_key).hexdigest()[:20]}"
    outcome = CreatorAudienceJudgmentOutcomeV1.model_validate(
        {
            "schema_version": JUDGMENT_OUTCOME_SCHEMA_VERSION,
            "record_id": record_id,
            "raw_anchor": bundle.get("raw_anchor"),
            "creator_id": bundle.get("creator_id"),
            "profile_subject_id": bundle.get("profile_subject_id"),
            "bundle_id": bundle.get("bundle_id"),
            "bundle_hash": bundle.get("bundle_hash"),
            "status": status,
            "response_sha256": response_sha256,
            "response_size_bytes": len(response_bytes),
            "response_bytes_b64": base64.b64encode(response_bytes).decode("ascii"),
            "validation_errors": validation_errors,
            "snapshot_id_or_none": (
                snapshot_document.get("snapshot_id") if snapshot_document else None
            ),
            "snapshot_sha256_or_none": snapshot_sha256,
            "snapshot_or_none": snapshot_document,
            "model_api_calls": 0,
        }
    ).model_dump(mode="json")
    outcome_bytes = (
        json.dumps(outcome, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8")
        + b"\n"
    )
    outcome_path = data_root.record_path(
        subtree="derived",
        raw_anchor=str(bundle["raw_anchor"]),
        lane=JUDGMENT_OUTCOME_LANE,
        record_id=record_id,
    )
    if outcome_path.exists():
        if outcome_path.read_bytes() != outcome_bytes:
            raise ValueError("existing audience Judgment outcome differs")
    else:
        data_root.append_record(
            subtree="derived",
            raw_anchor=str(bundle["raw_anchor"]),
            lane=JUDGMENT_OUTCOME_LANE,
            record_id=record_id,
            data=outcome_bytes,
        )

    if snapshot_text is not None:
        _write_new(snapshot_out, snapshot_text)
        return {
            "status": "validated",
            "creator_id": outcome["creator_id"],
            "profile_subject_id": outcome["profile_subject_id"],
            "bundle_id": outcome["bundle_id"],
            "bundle_hash": outcome["bundle_hash"],
            "response_sha256": response_sha256,
            "snapshot_id": outcome["snapshot_id_or_none"],
            "snapshot_sha256": snapshot_sha256,
            "snapshot_out": str(snapshot_out),
            "judgment_outcome_path": str(outcome_path),
            "model_api_calls": 0,
        }
    return {
        "status": "blocked",
        "blocked_at": "judgment_validation",
        "creator_id": outcome["creator_id"],
        "profile_subject_id": outcome["profile_subject_id"],
        "bundle_id": outcome["bundle_id"],
        "bundle_hash": outcome["bundle_hash"],
        "response_sha256": response_sha256,
        "validation_errors": validation_errors,
        "capture_reusable": True,
        "silver_reusable": True,
        "recapture_required": False,
        "safe_next_action": "submit a separately authorized corrected response",
        "judgment_outcome_path": str(outcome_path),
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
    prepare.add_argument("--bundle-out", type=Path, required=True)
    prepare.add_argument("--prompt-out", type=Path, required=True)
    validate = subparsers.add_parser("validate")
    validate.add_argument("--bundle", type=Path, required=True)
    validate.add_argument("--response", type=Path, required=True)
    validate.add_argument("--snapshot-out", type=Path, required=True)
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
            result = prepare_subscription_judgment(
                data_root=DataLakeRoot.resolve(explicit=args.data_root),
                packet_id=args.packet_id,
                creator_id=args.creator_id,
                profile_subject_id=args.profile_subject_id,
                question=args.question,
                evidence_cutoff=args.evidence_cutoff,
                bundle_out=args.bundle_out,
                prompt_out=args.prompt_out,
            )
        elif args.command == "validate":
            result = validate_subscription_judgment(
                bundle_path=args.bundle,
                response_path=args.response,
                snapshot_out=args.snapshot_out,
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
