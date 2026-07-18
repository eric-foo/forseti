"""Seam cadence runner: the executable completion signal for bronze consumption.

Captures one read-only committed-packet snapshot, executes every seam CATCH-UP
entrypoint twice against that exact set, and exits nonzero if the SECOND cycle
performs any work or emits any status — "this starting bronze batch is caught
up" becomes an executable claim instead of an agent judgment. Packets committed
after the snapshot are reported as next-run work and do not poison the current
completion signal. Census
authority: ``docs/decisions/bronze_consumer_census_closure_record_v0.md``;
seam contract: ``core_spine_v0_data_lake_consumption_seam_contract_v0.md``.

This runner is an ORCHESTRATOR, not a seam consumer: it imports the catch-up
runner modules and composes their public ``pending_packets``/``run_catchup``
entrypoints. It reads the root's committed by-key packet ids to establish the
immutable start boundary without rebuilding the shared availability index,
writes no acks, and owns no pickup or acknowledgement behavior — those
semantics stay inside the composed runners (the consumer seam-coverage gate
keeps it out of the seam-consumer surface;
``tests/contract/test_seam_cadence_coverage.py`` pins this registry to that
surface).

Exit semantics (``--run``): cycle 1 is allowed to work (its entries are the
backlog being drained); cycle 2 must emit ZERO entrypoint status entries, and a
final compute-free pending sweep must find ZERO remaining backlog. Failures
never satisfy the signal: a packet that failed in cycle 1 stays
unacknowledged, re-surfaces in cycle 2, and fails the exit code. One
entrypoint raising is a visible ``entrypoint_failed`` entry for that lane
(counted as cycle work), never a silent abort of the remaining lanes.

After and only after that completion signal passes, the cadence invokes the
contract-pinned data-lake index runner for one ``derived_retrieval`` rebuild.
The exact product-mention policy pins are read by that runner from the stored
``by_mention`` manifest. A rebuild failure fails the cadence exit code loudly;
no failed cadence attempts a lake-map refresh.

ASR COST GATE: the ASR entrypoint executes local owner-operated compute on an
unskipped ``--run``. ``--skip-asr`` skips only its execution and prints a
visible ``skipped_asr_compute`` marker EVERY cycle carrying the compute-free
pending count — a skipped lane stays loud, never silent. The healthy marker is
cadence-level output and does not count as cycle-2 work (the sanctioned
compute-free cadence); remaining ASR pending work or a failed skip-path pending
check DOES count in the final pending sweep.

The three LLM extract runners are seam consumers but NOT cadence entrypoints
(``CLASSIFIED_OUT_SEAM_CONSUMERS``): their extraction is owner-gated per-turn
LLM compute, not a compute-free cadence. Their backlog is owned by their own
``--check`` surfaces.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from runners import run_asr_transcript_catchup as _asr
from runners import run_basenotes_cleaning_catchup as _basenotes
from runners import run_ecr_catchup as _ecr
from runners import run_fragrance_review_projection_catchup as _fragrance_review
from runners import run_fragrantica_cleaning_catchup as _fragrantica
from runners import run_ig_reels_grid_projection_catchup as _ig_reels_grid
from runners import run_parfumo_cleaning_catchup as _parfumo
from runners import run_tiktok_comment_attention_producer as _tiktok_comment_attention
from runners import run_tiktok_grid_observation_producer as _tiktok_grid_observation
from runners import run_data_lake_indexes_rebuild as _indexes_rebuild


@dataclass(frozen=True)
class CadenceContext:
    """Per-invocation state shared by every entrypoint call."""

    data_root: object
    transcriber_policy: dict
    asr_model: str
    asr_compute_type: str


@dataclass(frozen=True)
class CadenceEntrypoint:
    """One composed catch-up entrypoint: filename (the census/audit key), a
    compute-free pending count, and the cadence execution call."""

    runner: str
    pending: Callable[[CadenceContext, Sequence[str] | None], int]
    run: Callable[[CadenceContext, Sequence[str] | None], list]
    needs_asr_compute: bool = False


def _asr_transcribe_fn(ctx: CadenceContext):
    # Lazy: the ASR library loads only on an unskipped --run reaching this
    # entrypoint (mirrors run_asr_transcript_catchup.main).
    from source_capture.transcript.audio_asr import transcribe_audio

    def transcribe_fn(audio_path: str):
        return transcribe_audio(
            audio_path, model_name=ctx.asr_model, compute_type=ctx.asr_compute_type
        )

    return transcribe_fn


def _asr_run(
    ctx: CadenceContext, scope_packet_ids: Sequence[str] | None
) -> list:
    return _asr.run_catchup(
        data_root=ctx.data_root,
        transcribe_fn=_asr_transcribe_fn(ctx),
        transcriber_policy=ctx.transcriber_policy,
        scope_packet_ids=scope_packet_ids,
    )


# The declared cadence surface: every seam catch-up entrypoint, in execution
# order. tests/contract/test_seam_cadence_coverage.py pins this registry plus
# CLASSIFIED_OUT_SEAM_CONSUMERS to the discovered seam-consumer runner surface,
# so a new seam consumer must be classified into the cadence or out of it.
CADENCE_ENTRYPOINTS: tuple[CadenceEntrypoint, ...] = (
    CadenceEntrypoint(
        runner="run_ecr_catchup.py",
        pending=lambda ctx, scope: len(
            _ecr.pending_packets(data_root=ctx.data_root, scope_packet_ids=scope)
        ),
        run=lambda ctx, scope: _ecr.run_catchup(
            data_root=ctx.data_root, scope_packet_ids=scope
        ),
    ),
    CadenceEntrypoint(
        runner="run_fragrantica_cleaning_catchup.py",
        pending=lambda ctx, scope: len(
            _fragrantica.pending_packets(
                data_root=ctx.data_root, scope_packet_ids=scope
            )
        ),
        run=lambda ctx, scope: _fragrantica.run_catchup(
            data_root=ctx.data_root, scope_packet_ids=scope
        ),
    ),
    CadenceEntrypoint(
        runner="run_basenotes_cleaning_catchup.py",
        pending=lambda ctx, scope: len(
            _basenotes.pending_packets(
                data_root=ctx.data_root, scope_packet_ids=scope
            )
        ),
        run=lambda ctx, scope: _basenotes.run_catchup(
            data_root=ctx.data_root, scope_packet_ids=scope
        ),
    ),
    CadenceEntrypoint(
        runner="run_parfumo_cleaning_catchup.py",
        pending=lambda ctx, scope: len(
            _parfumo.pending_packets(
                data_root=ctx.data_root, scope_packet_ids=scope
            )
        ),
        run=lambda ctx, scope: _parfumo.run_catchup(
            data_root=ctx.data_root, scope_packet_ids=scope
        ),
    ),
    CadenceEntrypoint(
        runner="run_fragrance_review_projection_catchup.py",
        pending=lambda ctx, scope: len(
            _fragrance_review.pending_packets(
                data_root=ctx.data_root, scope_packet_ids=scope
            )
        ),
        run=lambda ctx, scope: _fragrance_review.run_catchup(
            data_root=ctx.data_root, scope_packet_ids=scope
        ),
    ),
    CadenceEntrypoint(
        runner="run_ig_reels_grid_projection_catchup.py",
        pending=lambda ctx, scope: len(
            _ig_reels_grid.pending_packets(
                data_root=ctx.data_root, scope_packet_ids=scope
            )
        ),
        run=lambda ctx, scope: _ig_reels_grid.run_catchup(
            data_root=ctx.data_root, scope_packet_ids=scope
        ),
    ),
    CadenceEntrypoint(
        runner="run_tiktok_comment_attention_producer.py",
        pending=lambda ctx, scope: len(
            _tiktok_comment_attention.pending_packets(
                data_root=ctx.data_root, scope_packet_ids=scope
            )
        ),
        run=lambda ctx, scope: _tiktok_comment_attention.run_catchup(
            data_root=ctx.data_root, scope_packet_ids=scope
        ),
    ),
    CadenceEntrypoint(
        runner="run_tiktok_grid_observation_producer.py",
        pending=lambda ctx, scope: len(
            _tiktok_grid_observation.pending_packets(
                data_root=ctx.data_root, scope_packet_ids=scope
            )
        ),
        run=lambda ctx, scope: _tiktok_grid_observation.run_catchup(
            data_root=ctx.data_root, scope_packet_ids=scope
        ),
    ),
    CadenceEntrypoint(
        runner="run_asr_transcript_catchup.py",
        pending=lambda ctx, scope: len(
            _asr.pending_packets(
                data_root=ctx.data_root,
                transcriber_policy=ctx.transcriber_policy,
                scope_packet_ids=scope,
            )
        ),
        run=_asr_run,
        needs_asr_compute=True,
    ),
)

# Seam consumers deliberately NOT driven by this cadence, with the census
# reason. Owned by the census-closure record; the coverage contract test
# enforces that these plus CADENCE_ENTRYPOINTS exactly cover the discovered
# seam-consumer surface.
CLASSIFIED_OUT_SEAM_CONSUMERS: dict[str, str] = {
    "run_ig_reels_product_extract.py": (
        "LLM extraction lane: owner-gated per-turn compute, not a compute-free "
        "cadence entrypoint; backlog visible via its own --check"
    ),
    "run_tiktok_product_extract.py": (
        "LLM extraction lane: owner-gated per-turn compute, not a compute-free "
        "cadence entrypoint; execution requires an injected provider transport"
    ),
    "run_transcript_product_extract.py": (
        "LLM extraction lane: owner-gated per-turn compute, not a compute-free "
        "cadence entrypoint; backlog visible via its own --check"
    ),
}


def _print(entry: dict) -> None:
    print(json.dumps(entry, ensure_ascii=False, sort_keys=True))


def run_check(ctx: CadenceContext) -> int:
    """Single compute-free pending pass. Exit 0 iff every entrypoint reports a
    zero backlog and every pending check succeeds."""
    scope_packet_ids = _capture_start_snapshot(ctx)
    if scope_packet_ids is None:
        return 1
    failures = 0
    for entrypoint in CADENCE_ENTRYPOINTS:
        try:
            count = entrypoint.pending(ctx, scope_packet_ids)
        except Exception as exc:  # noqa: BLE001 - per-entrypoint failure isolation
            _print(
                {
                    "entrypoint": entrypoint.runner,
                    "status": "pending_check_failed",
                    "error": f"{type(exc).__name__}: {exc}"[:200],
                }
            )
            failures += 1
            continue
        _print({"entrypoint": entrypoint.runner, "pending": count})
        if count:
            failures += 1
    _report_late_arrivals(ctx, scope_packet_ids)
    return 1 if failures else 0


def run_cadence(ctx: CadenceContext, *, skip_asr: bool) -> int:
    """Two full cycles over every entrypoint. Exit 0 iff cycle 2 emits ZERO
    entrypoint status entries and a final compute-free pending sweep finds ZERO
    remaining backlog (the executable completion signal). The healthy skip-asr
    marker is cadence-level output excluded from cycle-2 status accounting; a
    skipped ASR backlog still fails the final pending sweep."""
    scope_packet_ids = _capture_start_snapshot(ctx)
    if scope_packet_ids is None:
        return 1

    second_cycle_entries = 0
    for cycle in (1, 2):
        for entrypoint in CADENCE_ENTRYPOINTS:
            if skip_asr and entrypoint.needs_asr_compute:
                try:
                    pending = entrypoint.pending(ctx, scope_packet_ids)
                except Exception as exc:  # noqa: BLE001 - skipped lane must stay checkable
                    _print(
                        {
                            "cycle": cycle,
                            "entrypoint": entrypoint.runner,
                            "status": "skipped_asr_pending_check_failed",
                            "error": f"{type(exc).__name__}: {exc}"[:200],
                        }
                    )
                    if cycle == 2:
                        second_cycle_entries += 1
                    continue
                # Never a silent skip: the marker prints EVERY cycle and
                # carries the live pending count for the skipped lane.
                _print(
                    {
                        "cycle": cycle,
                        "entrypoint": entrypoint.runner,
                        "status": "skipped_asr_compute",
                        "pending": pending,
                    }
                )
                continue
            try:
                results = entrypoint.run(ctx, scope_packet_ids)
            except Exception as exc:  # noqa: BLE001 - per-entrypoint failure isolation
                results = [
                    {
                        "status": "entrypoint_failed",
                        "error": f"{type(exc).__name__}: {exc}"[:200],
                    }
                ]
            for result in results:
                _print({"cycle": cycle, "entrypoint": entrypoint.runner, **result})
            if cycle == 2:
                second_cycle_entries += len(results)
    post_cycle_pending = _post_cycle_pending_failures(ctx, scope_packet_ids)
    _report_late_arrivals(ctx, scope_packet_ids)
    return 1 if second_cycle_entries or post_cycle_pending else 0


def _capture_start_snapshot(ctx: CadenceContext) -> tuple[str, ...] | None:
    try:
        packet_ids = tuple(ctx.data_root.list_committed_packet_ids())
    except Exception as exc:  # noqa: BLE001 - boundary failure must stay loud
        _print(
            {
                "cycle": "snapshot",
                "status": "cadence_snapshot_failed",
                "error": f"{type(exc).__name__}: {exc}"[:200],
            }
        )
        return None
    digest = hashlib.sha256("\n".join(packet_ids).encode("utf-8")).hexdigest()
    _print(
        {
            "cycle": "snapshot",
            "status": "cadence_snapshot_started",
            "packet_count": len(packet_ids),
            "packet_ids_sha256": digest,
        }
    )
    return packet_ids


def _report_late_arrivals(
    ctx: CadenceContext, scope_packet_ids: Sequence[str]
) -> None:
    try:
        late = sorted(
            set(ctx.data_root.list_committed_packet_ids()) - set(scope_packet_ids)
        )
    except Exception as exc:  # noqa: BLE001 - informational check cannot poison snapshot
        _print(
            {
                "cycle": "post",
                "status": "late_arrival_check_failed",
                "error": f"{type(exc).__name__}: {exc}"[:200],
            }
        )
        return
    if late:
        _print(
            {
                "cycle": "post",
                "status": "late_arrivals_observed",
                "packet_count": len(late),
                "packet_ids": late,
            }
        )


def _post_cycle_pending_failures(
    ctx: CadenceContext, scope_packet_ids: Sequence[str]
) -> int:
    """Final no-work proof: every pending helper must report zero backlog.

    This catches fake-pass paths where an entrypoint returned no status despite
    leaving work behind, or a later entrypoint made earlier entrypoint work after
    that earlier entrypoint's cycle-2 turn.
    """
    failures = 0
    for entrypoint in CADENCE_ENTRYPOINTS:
        try:
            pending = entrypoint.pending(ctx, scope_packet_ids)
        except Exception as exc:  # noqa: BLE001 - no-work claim must fail loud
            _print(
                {
                    "cycle": "post",
                    "entrypoint": entrypoint.runner,
                    "status": "post_cycle_pending_check_failed",
                    "error": f"{type(exc).__name__}: {exc}"[:200],
                }
            )
            failures += 1
            continue
        if pending != 0:
            _print(
                {
                    "cycle": "post",
                    "entrypoint": entrypoint.runner,
                    "status": "post_cycle_pending",
                    "pending": pending,
                }
            )
            failures += 1
    return failures


def _refresh_lake_map(ctx: CadenceContext) -> int:
    """Invoke the sanctioned sole writer after the all-caught-up proof."""
    result = _indexes_rebuild.main(
        [
            "--root",
            str(ctx.data_root.path),
            "--target",
            "derived_retrieval",
            "--use-stored-product-mention-policy",
        ]
    )
    _print(
        {
            "entrypoint": "run_data_lake_indexes_rebuild.py",
            "status": "lake_map_rebuilt" if result == 0 else "lake_map_rebuild_failed",
            "exit_code": result,
            "map_scope": "live_after_snapshot_completion",
        }
    )
    return result


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Seam cadence: run every seam catch-up entrypoint twice; the second "
            "cycle must perform no work and final pending checks must be zero."
        )
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Print each entrypoint's pending count; exit nonzero if any backlog exists.",
    )
    parser.add_argument(
        "--run",
        action="store_true",
        help=(
            "Run two full catch-up cycles; exit nonzero if the second cycle emits "
            "anything or final pending checks are nonzero."
        ),
    )
    parser.add_argument(
        "--skip-asr",
        action="store_true",
        help=(
            "With --run: skip ASR execution (local compute), printing a visible "
            "skipped marker with the pending count every cycle."
        ),
    )
    parser.add_argument(
        "--model",
        default="small",
        help="faster-whisper model name (part of the ASR obligation fingerprint).",
    )
    parser.add_argument(
        "--compute-type",
        default="int8",
        help="faster-whisper compute type (part of the ASR obligation fingerprint).",
    )
    parser.add_argument(
        "--data-root",
        default=None,
        help="Forseti data lake root. Defaults to FORSETI_DATA_ROOT (legacy ORCA_DATA_ROOT).",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    if args.check == args.run:
        parser.exit(status=2, message="choose exactly one of --check or --run\n")
    if args.skip_asr and args.check:
        parser.exit(
            status=2,
            message="--skip-asr applies to --run only (--check is already compute-free)\n",
        )

    from data_lake.root import DataLakeRoot

    try:
        data_root = DataLakeRoot.resolve(explicit=args.data_root)
    except Exception as exc:  # noqa: BLE001 - CLI must surface root resolution failures
        parser.exit(status=2, message=f"data root required: {type(exc).__name__}: {exc}\n")
    ctx = CadenceContext(
        data_root=data_root,
        transcriber_policy=_asr.default_transcriber_policy(
            model_name=args.model, compute_type=args.compute_type
        ),
        asr_model=args.model,
        asr_compute_type=args.compute_type,
    )
    if args.check:
        return run_check(ctx)
    cadence_result = run_cadence(ctx, skip_asr=args.skip_asr)
    if cadence_result:
        return cadence_result
    return _refresh_lake_map(ctx)


if __name__ == "__main__":
    raise SystemExit(main())
