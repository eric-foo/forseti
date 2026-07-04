"""Daemon-ready runner: derive Parfumo Cleaning output for every committed packet.

The seam-shaped CATCH-UP entrypoint for the Parfumo Cleaning lane, mirroring the
adjudicated Fragrantica catch-up (`run_fragrantica_cleaning_catchup`, findings
F-FRAG-001/002 closed) with Parfumo constants. Until now the audit pack +
post-cleaned Silver records were written only when an operator pointed
``cleaning.parfumo_lake.derive_parfumo_cleaning_into_lake`` at one packet: the lane
had NO discovery. This runner independently scans committed availability and derives
for every packet whose current obligation is not yet acknowledged.

Pickup is the consumption seam (``data_lake.consumption``). The obligation snapshot
is policy-only: the raw packet is immutable (write-once), the Parfumo projection is
rebuilt in memory from raw bodies (committed ``projection_parfumo`` records are NOT
consumed), and the cleaning packet's ECR ref is symbolic-by-convention — so the
derivation has no growable derived-record inputs, and the envelope enumerates EVERY
output-shaping pre-existing constant (the F-FRAG-001 adjudicated convention).
Skip-if-done keys on the ACK: this lane writes no record-set completion marker
(audit + Silver are independent appends with fresh ULIDs), so an unacknowledged
fingerprint always derives a FRESH audit sibling + Silver records and the ack cites
them; a crash mid-derivation leaves unreferenced siblings and NO ack, so the packet
re-surfaces and re-derives cleanly.
Contract: ``core_spine_v0_data_lake_consumption_seam_contract_v0.md``.

SURFACE GATE (the F-FRAG-002 adjudicated allowlist convention): the
``fragrance_native_database`` family is shared with the fragrantica and basenotes
cleaning lanes, split by ``source_surface``. Parfumo owns TWO in-scope surfaces
(direct HTTP + chrome-extension targeted rendered; the lake adapter passes the
packet's surface through to the cleaning builder). KNOWN other-lane surfaces are
acknowledged with explicit out-of-scope evidence; UNKNOWN surfaces surface as a
visible ``unsupported_surface`` status, are never acknowledged, and re-surface every
run until deliberately classified — never an open-world ack that could pre-close a
future surface.

Failure stays loud and isolated per packet: a missing availability entry is a
``discovery_failed`` status; a verified-read/validation/derivation raise is a
``derive_failed`` status; both leave the packet unacknowledged and re-surfacing every
run. An ack write failure surfaces as ``ack_failed``. Acked-and-unchanged packets
emit NO per-run status entries. Per-packet availability reconcile failures surface as
``availability_reconcile_failed`` (the F-ECR-001 adjudicated shape) while healthy
packets still index and process.

No-LLM zone (`runners/`): the Cleaning derivation is mechanical — this runner needs
no transport, so ``--run`` IS the cadence entrypoint.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cleaning.models import CLEANING_CORE_VERSION
from cleaning.parfumo import PARFUMO_RATING_CARRY_RULE
from cleaning.parfumo_lake import (
    CLEANING_AUDIT_PACK_SCHEMA_VERSION,
    PARFUMO_AUDIT_PACK_PRODUCER_SCHEMA_VERSION,
    PARFUMO_CLEANING_AUDIT_LANE,
    PARFUMO_CLEANING_METHOD_ID,
    PARFUMO_CLEANING_SILVER_LANE,
    PARFUMO_RATING_METRIC_ABSENT_RESIDUAL,
    PARFUMO_SILVER_METRIC_PRODUCER_SCHEMA_VERSION,
    PARFUMO_SILVER_PRODUCER_SCHEMA_VERSION,
    SILVER_VAULT_RECORD_SCHEMA_VERSION,
    TEXT_NORMALIZATION_RULE,
    _REVIEW_RATING_METRIC_SPECS,
    derive_parfumo_cleaning_into_lake,
)
from data_lake.consumption import PickupItem, append_ack, is_acknowledged, pickup
from data_lake.root import DataLakeRootError, raw_shard
from source_capture.parfumo_projection import (
    PARFUMO_DIRECT_HTTP_SOURCE_SURFACE,
    PARFUMO_PROJECTION_CERTIFICATION,
    PARFUMO_PROJECTION_METHOD,
    PARFUMO_PROJECTION_VERSION,
    PARFUMO_TARGETED_RENDERED_SOURCE_SURFACE,
)

# Seam ack namespace = the audit-pack lane (contract rule: an ack namespace must be
# a lane declared in lane_registry.LANE_ROLES; exactly one audit pack exists per
# derivation, and the ack's evidence cites it).
_ACK_NAMESPACE = PARFUMO_CLEANING_AUDIT_LANE
_SEAM_CONSUMER = "parfumo_cleaning_catchup"
_SOURCE_FAMILY = "fragrance_native_database"
_PARFUMO_SURFACES = frozenset(
    {
        PARFUMO_DIRECT_HTTP_SOURCE_SURFACE,
        PARFUMO_TARGETED_RENDERED_SOURCE_SURFACE,
    }
)
_KNOWN_OUT_OF_SCOPE_SURFACES = frozenset(
    {
        "fragrantica_product_page_direct_http",
        "basenotes_product_page_cloakbrowser_deep_scroll_current_window",
    }
)


def _packet_obligation() -> dict:
    """The cheap obligation snapshot: constant per policy version, enumerating every
    output-shaping pre-existing constant (F-FRAG-001 convention). NON-RAISING by
    construction (pickup's obligation_fn aborts the whole loop on a raise)."""
    return {
        "obligation_schema": 1,
        "consumer": _SEAM_CONSUMER,
        "cleaning_core_version": CLEANING_CORE_VERSION,
        "projection_method": PARFUMO_PROJECTION_METHOD,
        "projection_version": PARFUMO_PROJECTION_VERSION,
        "projection_certification": PARFUMO_PROJECTION_CERTIFICATION,
        "cleaning_audit_pack_schema_version": CLEANING_AUDIT_PACK_SCHEMA_VERSION,
        "audit_pack_schema_version": PARFUMO_AUDIT_PACK_PRODUCER_SCHEMA_VERSION,
        "silver_vault_record_schema_version": SILVER_VAULT_RECORD_SCHEMA_VERSION,
        "silver_schema_version": PARFUMO_SILVER_PRODUCER_SCHEMA_VERSION,
        "silver_metric_schema_version": PARFUMO_SILVER_METRIC_PRODUCER_SCHEMA_VERSION,
        "cleaning_method_id": PARFUMO_CLEANING_METHOD_ID,
        "text_normalization_rule": TEXT_NORMALIZATION_RULE,
        "rating_carry_rule": PARFUMO_RATING_CARRY_RULE,
        "rating_metric_absent_residual": PARFUMO_RATING_METRIC_ABSENT_RESIDUAL,
        "review_rating_metric_specs": [list(spec) for spec in _REVIEW_RATING_METRIC_SPECS],
    }


def _reconcile_availability(data_root) -> list[dict]:
    """By-key reconcile backstop with per-packet failure visibility.

    ``DataLakeRoot.rebuild_availability`` is intentionally fail-loud, but this
    daemon must keep healthy packets moving when one raw manifest is corrupt.
    Rebuild the index one committed packet at a time so bad packets are status
    entries, not silent omissions from a partial availability index.
    (F-ECR-001 adjudicated shape, mirrored from run_ecr_catchup.)
    """
    failures: list[dict] = []
    avail = data_root.path / "indexes" / "availability"
    if avail.is_dir():
        for entry_file in avail.glob("*.json"):
            entry_file.unlink()
    avail.mkdir(parents=True, exist_ok=True)

    raw_dir = data_root.path / "raw"
    if not raw_dir.is_dir():
        return failures
    for shard_dir in sorted(p for p in raw_dir.iterdir() if p.is_dir()):
        for container in sorted(p for p in shard_dir.iterdir() if p.is_dir()):
            packet_id = container.name
            if not (container / "manifest.json").is_file():
                continue
            if shard_dir.name != raw_shard(packet_id):
                continue
            try:
                data_root.record_availability(packet_id)
            except Exception as exc:  # noqa: BLE001 - surface corrupt packet, continue batch
                failures.append(
                    {
                        "packet_id": packet_id,
                        "status": "availability_reconcile_failed",
                        "error": f"{type(exc).__name__}: {exc}"[:200],
                    }
                )
    return failures


def _ack_packet(data_root, item: PickupItem, evidence: list[dict]) -> str:
    """Record the lane-owned completion fact. A create collision (another completer
    won the race) is fine when the obligation is now acknowledged; anything else is
    a real ack failure surfaced as a status."""
    try:
        append_ack(
            data_root,
            raw_anchor=item.raw_anchor,
            ack_namespace=_ACK_NAMESPACE,
            obligation=item.obligation,
            evidence=evidence,
        )
    except DataLakeRootError as exc:
        if is_acknowledged(
            data_root,
            raw_anchor=item.raw_anchor,
            ack_namespace=_ACK_NAMESPACE,
            obligation=item.obligation,
        ):
            return "acked"
        return f"ack_failed: {type(exc).__name__}: {exc}"[:200]
    return "acked"


def pending_packets(*, data_root) -> list[str]:
    """Committed family packet ids whose current Cleaning obligation is not
    acknowledged. Scheduler gate helper: no derivation and no writes beyond the
    availability reconcile."""
    failures = _reconcile_availability(data_root)
    if failures:
        first = failures[0]
        raise DataLakeRootError(
            "availability reconcile failed before pending check: "
            f"{first['packet_id']}: {first['error']}"
        )
    return [
        item.raw_anchor
        for item in pickup(
            data_root,
            ack_namespace=_ACK_NAMESPACE,
            obligation_fn=lambda _pid: _packet_obligation(),
            source_family=_SOURCE_FAMILY,
            reconcile=False,
        )
    ]


def run_catchup(*, data_root) -> list[dict]:
    """The single daemon entrypoint: derive the Parfumo Cleaning audit pack +
    post-cleaned Silver for every committed family packet (both Parfumo surfaces)
    whose current obligation is unacknowledged, then acknowledge with the
    derivation as evidence.

    Known other-lane surfaces are acknowledged with explicit out-of-scope evidence;
    unknown surfaces stay visible and unacknowledged (module doc). Per-packet
    failure isolation: a raise yields ``derive_failed`` and the batch continues.
    Acked-and-unchanged packets emit no status entries. Returns one status dict per
    processed packet.
    """
    results: list[dict] = []
    # Visible reconcile opt-out per the seam contract: this runner reconciles
    # ITSELF first, per packet, so one corrupt manifest becomes a visible
    # availability_reconcile_failed status while healthy packets still index
    # and process — instead of pickup's whole-batch fail-loud default reconcile.
    results.extend(_reconcile_availability(data_root))
    for item in pickup(
        data_root,
        ack_namespace=_ACK_NAMESPACE,
        obligation_fn=lambda _pid: _packet_obligation(),
        source_family=_SOURCE_FAMILY,
        reconcile=False,
    ):
        packet_id = item.raw_anchor
        entry = data_root.read_availability(packet_id)
        if entry is None:
            results.append(
                {
                    "packet_id": packet_id,
                    "status": "discovery_failed",
                    "error": "availability entry missing after reconcile",
                }
            )
            continue
        surface = entry.get("source_surface")
        if surface not in _PARFUMO_SURFACES:
            if surface not in _KNOWN_OUT_OF_SCOPE_SURFACES:
                results.append(
                    {
                        "packet_id": packet_id,
                        "status": "unsupported_surface",
                        "source_surface": surface,
                        "error": "unrecognized fragrance_native_database surface for Parfumo Cleaning",
                    }
                )
                continue
            # Shared-family packet owned by another cleaning lane: no
            # Parfumo-cleanable content, and a surface is immutable — the
            # discovery outcome IS the completion evidence (IG grid precedent).
            evidence = [
                {
                    "kind": "no_cleanable_content_for_surface",
                    "raw_anchor": packet_id,
                    "source_surface": surface,
                    "basis": "known_non_parfumo_source_surface",
                }
            ]
            outcome = _ack_packet(data_root, item, evidence)
            if outcome != "acked":
                results.append({"packet_id": packet_id, "status": "ack_failed", "error": outcome})
            else:
                results.append(
                    {
                        "packet_id": packet_id,
                        "status": "acked_no_cleanable_content",
                        "source_surface": surface,
                    }
                )
            continue
        try:
            derived = derive_parfumo_cleaning_into_lake(data_root=data_root, packet_id=packet_id)
        except Exception as exc:  # noqa: BLE001 - per-packet failure isolation (daemon-ready)
            results.append(
                {
                    "packet_id": packet_id,
                    "status": "derive_failed",
                    "error": f"{type(exc).__name__}: {exc}"[:200],
                }
            )
            continue
        audit_record_id = derived.audit_record["record_id"]
        evidence = [
            {
                "kind": "derived_record",
                "raw_anchor": packet_id,
                "lane": PARFUMO_CLEANING_AUDIT_LANE,
                "record_id": audit_record_id,
                "content_hash": derived.audit_record["content_hash"],
            },
            {
                "kind": "silver_records",
                "raw_anchor": packet_id,
                "lane": PARFUMO_CLEANING_SILVER_LANE,
                "record_ids": [record["record_id"] for record in derived.silver_records],
                "count": len(derived.silver_records),
            },
        ]
        outcome = _ack_packet(data_root, item, evidence)
        if outcome != "acked":
            results.append({"packet_id": packet_id, "status": "ack_failed", "error": outcome})
        else:
            results.append(
                {
                    "packet_id": packet_id,
                    "status": "derived",
                    "audit_record_id": audit_record_id,
                    "silver_count": len(derived.silver_records),
                }
            )
    return results


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Parfumo Cleaning catch-up runner utilities.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Print the count of committed family packets whose Cleaning obligation is unacknowledged.",
    )
    parser.add_argument(
        "--run",
        action="store_true",
        help="Run the catch-up: derive + acknowledge every unacknowledged packet.",
    )
    parser.add_argument(
        "--data-root",
        default=None,
        help="Orca data lake root. Defaults to ORCA_DATA_ROOT.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    if args.check == args.run:
        parser.exit(status=2, message="choose exactly one of --check or --run\n")

    from data_lake.root import DataLakeRoot

    try:
        data_root = DataLakeRoot.resolve(explicit=args.data_root)
    except Exception as exc:  # noqa: BLE001 - CLI must surface root resolution failures
        parser.exit(status=2, message=f"data root required: {type(exc).__name__}: {exc}\n")
    if args.check:
        print(len(pending_packets(data_root=data_root)))
        return 0
    failures = 0
    for entry in run_catchup(data_root=data_root):
        print(json.dumps(entry, ensure_ascii=False, sort_keys=True))
        if entry["status"] not in {"derived", "acked_no_cleanable_content"}:
            failures += 1
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
