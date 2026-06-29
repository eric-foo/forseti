"""Vertical IG Reels capture-lane orchestrator.

Sequences IG-specific acquisition lanes while emitting shared lane receipts. It does not make
IG use YouTube acquisition methods; grid capture, per-reel deep capture, operator-assisted
product extraction, and projection each keep their own platform-specific mechanics.

Downstream targeting: with no explicit ``--platform-item-id``/``--transcript-source-key``, the
deep-capture lane FANS OUT -- every reel it persisted whose transcript is extraction-eligible
becomes a product-extract + projection target (in rank order), so a render-empty top-ranked reel
no longer masks lower-ranked reels that carry real transcripts. An explicit selector still pins a
single target.
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
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
from source_capture.ig_reels_deep_capture import ReelDeepCaptureResult
from source_capture.ig_reels_behavioral_lake import project_ig_reels_behavioral_item_from_lake
from source_capture.ig_reels_deep_capture_lake import DEEP_CAPTURE_SET_LANE, deep_capture_record_id
from source_capture.lane_orchestration import LaneReceipt, LaneRunSummary

DEFAULT_LANES = ("grid", "deep_capture", "product_extract", "projection")
LANE_ORDER = DEFAULT_LANES

# Raw deep-capture postures the downstream extraction gate treats as eligible. This mirrors
# ``ig_reels_behavioral_projection._eligibility``: a transcript source is extraction-eligible only
# when its record-set is complete, its NORMALISED posture is ``"transcribed"``, and it has >0 cues.
# The deep-capture completion check below already enforces completeness, so ``_is_extraction_eligible``
# adds the posture + cue-count half. ``"ok"`` is the legacy posture token that
# ``_normalise_deep_posture`` maps to ``"transcribed"``; both count here so this lane never drifts
# from the projection gate it feeds.
_EXTRACTION_ELIGIBLE_POSTURES = frozenset({"transcribed", "ok"})

GridRunner = Callable[..., tuple[int, str]]
DeepCaptureRunner = Callable[..., tuple[list[Any], list[CapturedReel]]]
ProjectionBuilder = Callable[..., dict[str, Any]]


@dataclass(frozen=True)
class _DownstreamTarget:
    """One reel the product-extract and projection lanes should process.

    ``platform_item_id`` is the reel shortcode; ``transcript_source_key`` is the exact deep-capture
    transcript key when known. A fanned-out (auto-selected) target carries both; an explicit
    ``--platform-item-id``/``--transcript-source-key`` request may carry only one.
    """

    platform_item_id: str | None
    transcript_source_key: str | None


def _is_extraction_eligible(result: ReelDeepCaptureResult) -> bool:
    """Whether a COMPLETE deep-capture transcript would pass the downstream extraction gate.

    Completeness is enforced separately (only persisted record-sets reach this check), so this is
    the posture + cue-count half of ``ig_reels_behavioral_projection._eligibility``.
    """
    posture = (result.transcript_posture or "").strip()
    return posture in _EXTRACTION_ELIGIBLE_POSTURES and len(result.transcript_cues) > 0


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
    # An explicit selector pins ONE downstream target; otherwise the deep-capture lane fans out to
    # every extraction-eligible reel it persisted. Product extraction and projection must then target
    # the SAME reel, so derive the shortcode from the transcript key when only the key is given, and
    # reject an id+key pair naming two different reels (else product would extract one reel while
    # projection built another -- a silent split-brain).
    explicit_selector = platform_item_id is not None or transcript_source_key is not None
    explicit_shortcode = platform_item_id
    if transcript_source_key is not None:
        key_shortcode = transcript_source_key.split(":", 1)[0] or None
        if platform_item_id is not None and key_shortcode != platform_item_id:
            raise ValueError(
                "explicit selectors name different reels: "
                f"--platform-item-id={platform_item_id} vs --transcript-source-key={transcript_source_key}"
            )
        if explicit_shortcode is None:
            explicit_shortcode = key_shortcode
    targets: list[_DownstreamTarget] = (
        [_DownstreamTarget(explicit_shortcode, transcript_source_key)] if explicit_selector else []
    )

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
        receipt, eligible_targets = _run_deep_capture_lane(
            data_root=data_root,
            handle=handle,
            top_n=top_n,
            max_rows=max_rows,
            asr_model=asr_model,
            deep_capture_runner=deep_capture_runner,
        )
        if not explicit_selector:
            targets = list(eligible_targets)
        elif explicit_platform_item_id is not None and transcript_source_key is None:
            # Enrich the explicit shortcode with its exact transcript key when the lane captured it;
            # if every eligible reel is a DIFFERENT reel, keep the explicit shortcode and flag it.
            match = next(
                (t for t in eligible_targets if t.platform_item_id == explicit_platform_item_id),
                None,
            )
            if match is not None:
                targets = [_DownstreamTarget(explicit_platform_item_id, match.transcript_source_key)]
            elif eligible_targets:
                differing = ",".join(
                    t.platform_item_id for t in eligible_targets if t.platform_item_id is not None
                )
                receipt = _receipt_with_residual(
                    receipt,
                    f"deep_capture_target_differs_from_explicit_platform_item:{explicit_platform_item_id}:{differing}",
                )
        receipts.append(receipt)

    if "product_extract" in requested:
        receipts.append(
            _run_product_lane(
                data_root=data_root,
                targets=targets,
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
                targets=targets,
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
) -> tuple[LaneReceipt, list[_DownstreamTarget]]:
    try:
        ranked, captured = deep_capture_runner(
            handle=handle,
            top_n=top_n,
            model=asr_model,
            data_root=str(data_root.path),
            max_rows=max_rows,
        )
    except Exception as exc:  # noqa: BLE001
        return LaneReceipt("deep_capture", "failed", f"{type(exc).__name__}: {exc}"), []

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

    # Fan out to every persisted reel whose transcript is extraction-eligible (rank order preserved,
    # since ``captured`` -- and therefore ``complete_items`` -- is already ranked). A complete reel
    # that rendered empty (render_unavailable / no_audio_handle / no_speech / zero cues) is recorded
    # as a residual instead of being handed downstream, so it no longer masks an eligible reel.
    eligible_targets: list[_DownstreamTarget] = []
    selected_targets: list[dict[str, Any]] = []
    for item, record_id, source_key in complete_items:
        result = item.result
        assert result is not None  # complete_items only holds ok items (result is not None)
        if _is_extraction_eligible(result):
            eligible_targets.append(_DownstreamTarget(result.reel_shortcode, source_key))
            selected_targets.append(
                {
                    "platform_item_id": result.reel_shortcode,
                    "asr_record_id": record_id,
                    "transcript_source_key": source_key,
                }
            )
        else:
            residuals.append(
                f"deep_capture_complete_not_extraction_eligible:{result.reel_shortcode}:{record_id}"
                f":posture={result.transcript_posture}:cues={len(result.transcript_cues)}"
            )

    if len(eligible_targets) > 1:
        shortcodes = ",".join(t.platform_item_id for t in eligible_targets if t.platform_item_id is not None)
        residuals.append(f"orchestrator_product_projection_fan_out_targets:{shortcodes}")

    status = "succeeded" if not failures and len(complete_items) == len([item for item in captured if item.ok]) and (captured or top_n == 0) else "failed"
    return (
        LaneReceipt(
            "deep_capture",
            status,
            f"captured={len(captured)} persisted={len(complete_items)} eligible={len(eligible_targets)} failures={len(failures)} ranked={len(ranked)}",
            outputs={
                "ranked_count": len(ranked),
                "captured_count": len(captured),
                "persisted_count": len(complete_items),
                "eligible_count": len(eligible_targets),
                "selected_targets": selected_targets,
                "items": [_captured_to_dict(item) for item in captured],
            },
            residuals=residuals,
        ),
        eligible_targets,
    )


def _run_product_lane(
    *,
    data_root: Any,
    targets: Sequence[_DownstreamTarget],
    product_model: str,
    operator_packet_out: Path | None,
    operator_packet_in: Path | None,
    operator_response_path: Path | None,
) -> LaneReceipt:
    # Import is single-packet by design: the operator imports one (packet, response) pair at a time,
    # so fan-out does not change this branch.
    if operator_response_path is not None:
        if operator_packet_in is None:
            return LaneReceipt(
                "product_extract",
                "failed",
                "operator response import requires operator_packet_in",
            )
        try:
            packet = _read_json_object(operator_packet_in)
            result = import_operator_response(
                data_root=data_root,
                packet=packet,
                response_text=operator_response_path.read_text(encoding="utf-8"),
                model=None if product_model == DEFAULT_OPERATOR_MODEL else product_model,
            )
        except Exception as exc:  # noqa: BLE001
            return LaneReceipt("product_extract", "failed", f"{type(exc).__name__}: {exc}")
        status = "succeeded" if result.get("status") in {"extracted", "skipped_done"} else "failed"
        return LaneReceipt("product_extract", status, str(result.get("status")), outputs=result)

    export_targets = [
        t for t in targets if t.platform_item_id is not None or t.transcript_source_key is not None
    ]
    if not export_targets:
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
            outputs={
                "targets": [
                    {"video_id": t.platform_item_id, "transcript_source_key": t.transcript_source_key}
                    for t in export_targets
                ]
            },
            residuals=["ig_product_operator_packet_output_path_absent"],
        )

    # Export ONE operator packet per eligible reel. A single bad target is recorded and does not
    # abort the others (mirrors the deep-capture batch's per-reel resilience).
    results: list[dict[str, Any]] = []
    statuses: list[str | None] = []
    any_failed = False
    for target in export_targets:
        label = target.platform_item_id or _source_key_label(target.transcript_source_key)
        packet_path = _per_target_packet_path(operator_packet_out, label)
        try:
            result = export_operator_packet(
                data_root=data_root,
                transcript_source_key=target.transcript_source_key,
                platform_item_id=None if target.transcript_source_key is not None else target.platform_item_id,
                model=product_model,
                output_path=packet_path,
            )
        except Exception as exc:  # noqa: BLE001
            any_failed = True
            results.append(
                {
                    "video_id": target.platform_item_id,
                    "transcript_source_key": target.transcript_source_key,
                    "status": "failed",
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )
            continue
        statuses.append(str(result.get("status")) if result.get("status") is not None else None)
        results.append(result)

    exported = [r for r in results if r.get("status") == "operator_packet_exported"]
    needs_cleanup = [r for r in results if r.get("status") == "partial_needs_cleanup"]
    if any_failed:
        status = "failed"
    elif exported or needs_cleanup:
        # operator_packet_exported -> operator must produce a response; partial_needs_cleanup ->
        # operator must clear a crash-partial mention set. Both are operator-action states, not hard
        # failures (mirrors run_ig_reels_operator_product_extract._status_exit_code's exit 4), so they
        # must not collapse into "failed"/exit 3.
        status = "blocked_operator_action_required"
    elif statuses and all(s == "complete" for s in statuses):
        status = "skipped"
    else:
        status = "failed"
    message = (
        f"targets={len(export_targets)} exported={len(exported)} "
        f"needs_cleanup={len(needs_cleanup)} failed={'yes' if any_failed else 'no'}"
    )
    return LaneReceipt("product_extract", status, message, outputs={"targets": results})


def _run_projection_lane(
    *,
    data_root: Any,
    targets: Sequence[_DownstreamTarget],
    projection_builder: ProjectionBuilder,
) -> LaneReceipt:
    ordered: list[str] = []
    seen: set[str] = set()
    for target in targets:
        shortcode = target.platform_item_id
        if shortcode is not None and shortcode not in seen:
            seen.add(shortcode)
            ordered.append(shortcode)
    if not ordered:
        return LaneReceipt(
            "projection",
            "not_attempted",
            "projection requires platform_item_id or a selected deep-captured reel",
        )

    results: list[dict[str, Any]] = []
    residuals: list[str] = []
    any_failed = False
    all_complete = True
    for shortcode in ordered:
        try:
            projection = projection_builder(
                data_root=data_root,
                platform_item_id=shortcode,
                rebuild_availability=True,
            )
        except Exception as exc:  # noqa: BLE001
            any_failed = True
            all_complete = False
            results.append(
                {
                    "platform_item_id": shortcode,
                    "behavioral_status": None,
                    "behavioral_complete": None,
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )
            continue
        completeness = projection.get("behavioral_completeness", {})
        complete = completeness.get("complete") is True
        all_complete = all_complete and complete
        results.append(
            {
                "platform_item_id": shortcode,
                "behavioral_status": completeness.get("status"),
                "behavioral_complete": completeness.get("complete"),
            }
        )
        for item in completeness.get("residuals", []):
            residuals.append(f"{shortcode}:{item}" if len(ordered) > 1 else str(item))

    if any_failed:
        status = "failed"
    elif all_complete:
        status = "succeeded"
    else:
        status = "incomplete"
    complete_count = sum(1 for r in results if r.get("behavioral_complete") is True)
    return LaneReceipt(
        "projection",
        status,
        f"targets={len(ordered)} complete={complete_count}",
        outputs={"targets": results},
        residuals=residuals,
    )


def _per_target_packet_path(base: Path, label: str) -> Path:
    """Per-reel packet path so a fan-out export never clobbers one ``--operator-packet-out`` file.

    ``<dir>/<stem><suffix>`` -> ``<dir>/<stem>.<label><suffix>`` (e.g. ``packet.json`` -> ``packet.ABC.json``).
    """
    return base.with_name(f"{base.stem}.{_safe_label(label)}{base.suffix}")


def _safe_label(label: str) -> str:
    return "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in label) or "target"


def _source_key_label(key: str | None) -> str:
    """Filename label for an explicit transcript-source-key target (``<shortcode>:asr:<rid>``)."""
    if not key:
        return "target"
    return key.split(":", 1)[0]


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
    parser.add_argument("--platform-item-id", default=None, help="IG Reel shortcode; pins a single product/projection target (no fan-out).")
    parser.add_argument("--transcript-source-key", default=None, help="Exact transcript source key; pins a single product target (no fan-out).")
    parser.add_argument(
        "--operator-packet-out",
        type=Path,
        default=None,
        help="Base path for operator-assisted extraction export; each eligible reel gets <stem>.<shortcode><suffix>.",
    )
    parser.add_argument("--operator-packet-in", type=Path, default=None, help="Packet path for operator-assisted extraction import (one packet).")
    parser.add_argument("--operator-response", type=Path, default=None, help="Strict JSON-array operator response to import (one response).")
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
