"""Vertical IG Reels capture-lane orchestrator.

Sequences IG-specific acquisition lanes while emitting shared lane receipts. It does not make
IG use YouTube acquisition methods; grid capture, per-reel deep capture, operator-assisted
product extraction, and projection each keep their own platform-specific mechanics.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Callable, Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from runners.run_ig_reels_operator_product_extract import (
    DEFAULT_OPERATOR_MODEL,
    export_operator_packet,
    import_operator_response,
)
from runners.run_source_capture_ig_reels_creator_deep_capture import (
    CapturedReel,
    run_creator_deep_capture,
)
from runners.run_source_capture_ig_reels_grid_packet import run_source_capture_ig_reels_grid_packet
from source_capture.ig_reels_behavioral_lake import project_ig_reels_behavioral_item_from_lake
from source_capture.ig_reels_deep_capture_lake import DEEP_CAPTURE_SET_LANE, deep_capture_record_id
from source_capture.lane_orchestration import LaneReceipt, LaneRunSummary

DEFAULT_LANES = ("grid", "deep_capture", "product_extract", "projection")
LANE_ORDER = DEFAULT_LANES

GridRunner = Callable[..., tuple[int, str]]
DeepCaptureRunner = Callable[..., tuple[list[Any], list[CapturedReel]]]
ProjectionBuilder = Callable[..., dict[str, Any]]


def run_ig_reels_lane_orchestrator(
    *,
    data_root: Any,
    handle: str,
    lanes: Sequence[str] = DEFAULT_LANES,
    top_n: int = 1,
    max_rows: int = 12,
    asr_model: str = "small",
    product_model: str = DEFAULT_OPERATOR_MODEL,
    platform_item_id: str | None = None,
    transcript_source_key: str | None = None,
    operator_packet_out: Path | None = None,
    operator_packet_in: Path | None = None,
    operator_response_path: Path | None = None,
    grid_runner: GridRunner = run_source_capture_ig_reels_grid_packet,
    deep_capture_runner: DeepCaptureRunner = run_creator_deep_capture,
    projection_builder: ProjectionBuilder = project_ig_reels_behavioral_item_from_lake,
) -> LaneRunSummary:
    requested = _ordered_lanes(lanes)
    receipts: list[LaneReceipt] = []
    explicit_platform_item_id = platform_item_id
    target_shortcode = platform_item_id
    target_transcript_source_key = transcript_source_key

    if "grid" in requested:
        receipts.append(
            _run_grid_lane(
                data_root=data_root,
                handle=handle,
                max_rows=max_rows,
                grid_runner=grid_runner,
            )
        )

    if "deep_capture" in requested:
        receipt, captured_target, captured_source_key = _run_deep_capture_lane(
            data_root=data_root,
            handle=handle,
            top_n=top_n,
            max_rows=max_rows,
            asr_model=asr_model,
            deep_capture_runner=deep_capture_runner,
        )
        if target_shortcode is None and captured_source_key is not None:
            target_shortcode = captured_target
        if target_transcript_source_key is None and captured_source_key is not None:
            if explicit_platform_item_id is None or captured_target == explicit_platform_item_id:
                target_transcript_source_key = captured_source_key
            else:
                receipt = _receipt_with_residual(
                    receipt,
                    f"deep_capture_target_differs_from_explicit_platform_item:{explicit_platform_item_id}:{captured_target}",
                )
        receipts.append(receipt)

    if "product_extract" in requested:
        receipts.append(
            _run_product_lane(
                data_root=data_root,
                platform_item_id=None if target_transcript_source_key is not None else target_shortcode,
                transcript_source_key=target_transcript_source_key,
                product_model=product_model,
                operator_packet_out=operator_packet_out,
                operator_packet_in=operator_packet_in,
                operator_response_path=operator_response_path,
            )
        )

    if "projection" in requested:
        receipts.append(
            _run_projection_lane(
                data_root=data_root,
                platform_item_id=target_shortcode,
                projection_builder=projection_builder,
            )
        )

    return LaneRunSummary(platform="instagram", target=handle, receipts=tuple(receipts))


def _ordered_lanes(lanes: Sequence[str]) -> tuple[str, ...]:
    expanded = DEFAULT_LANES if any(lane == "all" for lane in lanes) else tuple(lanes)
    if not expanded:
        raise ValueError("at least one IG lane is required")
    unknown = sorted(set(expanded) - set(LANE_ORDER))
    if unknown:
        raise ValueError(f"unknown IG lane(s): {', '.join(unknown)}")
    requested = set(expanded)
    return tuple(lane for lane in LANE_ORDER if lane in requested)


def _run_grid_lane(
    *,
    data_root: Any,
    handle: str,
    max_rows: int,
    grid_runner: GridRunner,
) -> LaneReceipt:
    try:
        code, message = grid_runner(
            handle=handle,
            data_root=data_root,
            decision_question=f"IG reels vertical lane orchestration for @{handle.strip().lstrip('@')}",
            max_rows=max_rows,
        )
    except Exception as exc:  # noqa: BLE001 - lane receipt preserves failure without hiding it
        return LaneReceipt("grid", "failed", f"{type(exc).__name__}: {exc}")
    return LaneReceipt(
        "grid",
        "succeeded" if code == 0 else "failed",
        message,
        outputs={"exit_code": code},
    )


def _run_deep_capture_lane(
    *,
    data_root: Any,
    handle: str,
    top_n: int,
    max_rows: int,
    asr_model: str,
    deep_capture_runner: DeepCaptureRunner,
) -> tuple[LaneReceipt, str | None, str | None]:
    try:
        ranked, captured = deep_capture_runner(
            handle=handle,
            top_n=top_n,
            model=asr_model,
            data_root=str(data_root.path),
            max_rows=max_rows,
        )
    except Exception as exc:  # noqa: BLE001
        return LaneReceipt("deep_capture", "failed", f"{type(exc).__name__}: {exc}"), None, None

    residuals: list[str] = []
    failures = [item for item in captured if not item.ok or (item.persisted or "").startswith("persist-failed")]
    for item in failures:
        if item.error or item.persisted:
            residuals.append(str(item.error or item.persisted))

    complete_items: list[tuple[CapturedReel, str, str]] = []
    for item in captured:
        if not item.ok or item.result is None:
            continue
        record_id = deep_capture_record_id(item.result)
        try:
            complete = data_root.is_record_set_complete(
                subtree="derived",
                raw_anchor=item.result.reel_shortcode,
                record_id=record_id,
                completion_lane=DEEP_CAPTURE_SET_LANE,
            )
        except Exception as exc:  # noqa: BLE001
            complete = False
            residuals.append(f"deep_capture_completion_check_failed:{item.result.reel_shortcode}:{record_id}:{type(exc).__name__}")
        if complete:
            complete_items.append((item, record_id, f"{item.result.reel_shortcode}:asr:{record_id}"))
        else:
            residuals.append(f"deep_capture_not_persisted:{item.result.reel_shortcode}:{record_id}")

    selected_item = complete_items[0] if complete_items else None
    selected_shortcode = selected_item[0].result.reel_shortcode if selected_item and selected_item[0].result else None
    selected_record_id = selected_item[1] if selected_item else None
    selected_source_key = selected_item[2] if selected_item else None
    if selected_shortcode is not None and len(complete_items) > 1:
        residuals.append(
            f"orchestrator_product_projection_single_target:{selected_shortcode}:persisted_count={len(complete_items)}"
        )
    status = "succeeded" if not failures and len(complete_items) == len([item for item in captured if item.ok]) and (captured or top_n == 0) else "failed"
    return (
        LaneReceipt(
            "deep_capture",
            status,
            f"captured={len(captured)} persisted={len(complete_items)} failures={len(failures)} ranked={len(ranked)}",
            outputs={
                "ranked_count": len(ranked),
                "captured_count": len(captured),
                "persisted_count": len(complete_items),
                "selected_platform_item_id": selected_shortcode,
                "selected_asr_record_id": selected_record_id,
                "selected_transcript_source_key": selected_source_key,
                "items": [_captured_to_dict(item) for item in captured],
            },
            residuals=residuals,
        ),
        selected_shortcode,
        selected_source_key,
    )


def _run_product_lane(
    *,
    data_root: Any,
    platform_item_id: str | None,
    transcript_source_key: str | None,
    product_model: str,
    operator_packet_out: Path | None,
    operator_packet_in: Path | None,
    operator_response_path: Path | None,
) -> LaneReceipt:
    try:
        if operator_response_path is not None:
            if operator_packet_in is None:
                return LaneReceipt(
                    "product_extract",
                    "failed",
                    "operator response import requires operator_packet_in",
                )
            packet = _read_json_object(operator_packet_in)
            result = import_operator_response(
                data_root=data_root,
                packet=packet,
                response_text=operator_response_path.read_text(encoding="utf-8"),
                model=None if product_model == DEFAULT_OPERATOR_MODEL else product_model,
            )
            status = "succeeded" if result.get("status") in {"extracted", "skipped_done"} else "failed"
            return LaneReceipt("product_extract", status, str(result.get("status")), outputs=result)

        if platform_item_id is None and transcript_source_key is None:
            return LaneReceipt(
                "product_extract",
                "not_attempted",
                "product extraction export requires platform_item_id or transcript_source_key",
                residuals=["ig_product_selector_absent"],
            )
        if operator_packet_out is None:
            return LaneReceipt(
                "product_extract",
                "blocked_operator_action_required",
                "operator_packet_out is required to export an operator packet",
                outputs={"platform_item_id": platform_item_id, "transcript_source_key": transcript_source_key},
                residuals=["ig_product_operator_packet_output_path_absent"],
            )
        result = export_operator_packet(
            data_root=data_root,
            transcript_source_key=transcript_source_key,
            platform_item_id=platform_item_id,
            model=product_model,
            output_path=operator_packet_out,
        )
    except Exception as exc:  # noqa: BLE001
        return LaneReceipt("product_extract", "failed", f"{type(exc).__name__}: {exc}")

    if result.get("status") == "operator_packet_exported":
        return LaneReceipt(
            "product_extract",
            "blocked_operator_action_required",
            "operator packet exported; import strict JSON response to complete extraction",
            outputs=result,
        )
    status = "skipped" if result.get("status") == "complete" else "failed"
    return LaneReceipt("product_extract", status, str(result.get("status")), outputs=result)


def _run_projection_lane(
    *,
    data_root: Any,
    platform_item_id: str | None,
    projection_builder: ProjectionBuilder,
) -> LaneReceipt:
    if platform_item_id is None:
        return LaneReceipt(
            "projection",
            "not_attempted",
            "projection requires platform_item_id or a selected deep-captured reel",
        )
    try:
        projection = projection_builder(
            data_root=data_root,
            platform_item_id=platform_item_id,
            rebuild_availability=True,
        )
    except Exception as exc:  # noqa: BLE001
        return LaneReceipt("projection", "failed", f"{type(exc).__name__}: {exc}")
    completeness = projection.get("behavioral_completeness", {})
    status = "succeeded" if completeness.get("complete") is True else "incomplete"
    return LaneReceipt(
        "projection",
        status,
        str(completeness.get("status")),
        outputs={
            "platform_item_id": platform_item_id,
            "behavioral_status": completeness.get("status"),
            "behavioral_complete": completeness.get("complete"),
        },
        residuals=[str(item) for item in completeness.get("residuals", [])],
    )


def _receipt_with_residual(receipt: LaneReceipt, residual: str) -> LaneReceipt:
    return LaneReceipt(
        receipt.lane,
        receipt.status,
        receipt.message,
        outputs=dict(receipt.outputs),
        residuals=[*receipt.residuals, residual],
    )


def _summary_exit_code(summary: LaneRunSummary) -> int:
    if summary.complete:
        return 0
    statuses = {receipt.status for receipt in summary.receipts}
    if "failed" in statuses:
        return 3
    if "blocked_operator_action_required" in statuses:
        return 4
    return 1


def _captured_to_dict(item: CapturedReel) -> dict[str, Any]:
    return {
        "rank": item.ranked.rank,
        "shortcode": item.ranked.shortcode,
        "ok": item.ok,
        "error": item.error,
        "persisted": item.persisted,
    }


def _read_json_object(path: Path) -> dict[str, Any]:
    body = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(body, dict):
        raise ValueError(f"expected JSON object: {path}")
    return body


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run requested IG Reels capture lanes in sequence.")
    parser.add_argument("--handle", required=True, help="IG handle, with or without @.")
    parser.add_argument("--data-root", default=None, help="Orca data lake root. Defaults to ORCA_DATA_ROOT.")
    parser.add_argument("--lanes", default=",".join(DEFAULT_LANES), help="Comma list: grid,deep_capture,product_extract,projection,all.")
    parser.add_argument("--top-n", type=int, default=1, help="How many ranked reels to deep-capture.")
    parser.add_argument("--max-rows", type=int, default=12, help="How many grid rows to scan.")
    parser.add_argument("--asr-model", default="small", help="faster-whisper model size.")
    parser.add_argument("--product-model", default=DEFAULT_OPERATOR_MODEL, help="Product extraction model token.")
    parser.add_argument("--platform-item-id", default=None, help="IG Reel shortcode for product/projection lanes.")
    parser.add_argument("--transcript-source-key", default=None, help="Exact transcript source key for product export.")
    parser.add_argument("--operator-packet-out", type=Path, default=None, help="Packet path for operator-assisted extraction export.")
    parser.add_argument("--operator-packet-in", type=Path, default=None, help="Packet path for operator-assisted extraction import.")
    parser.add_argument("--operator-response", type=Path, default=None, help="Strict JSON-array operator response to import.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    if args.top_n < 0:
        parser.exit(status=2, message="ig reels lane orchestrator failed: --top-n must be >= 0\n")

    from data_lake.root import DataLakeRoot

    try:
        data_root = DataLakeRoot.resolve(explicit=args.data_root)
        summary = run_ig_reels_lane_orchestrator(
            data_root=data_root,
            handle=args.handle,
            lanes=tuple(part.strip() for part in args.lanes.split(",") if part.strip()),
            top_n=args.top_n,
            max_rows=args.max_rows,
            asr_model=args.asr_model,
            product_model=args.product_model,
            platform_item_id=args.platform_item_id,
            transcript_source_key=args.transcript_source_key,
            operator_packet_out=args.operator_packet_out,
            operator_packet_in=args.operator_packet_in,
            operator_response_path=args.operator_response,
        )
    except Exception as exc:  # noqa: BLE001
        parser.exit(status=3, message=f"ig reels lane orchestrator failed: {type(exc).__name__}: {exc}\n")

    print(json.dumps(summary.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return _summary_exit_code(summary)


if __name__ == "__main__":
    raise SystemExit(main())
