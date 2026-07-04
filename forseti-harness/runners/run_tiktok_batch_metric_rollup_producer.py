"""Operator runner: derive TikTok creator-metric Silver rollups from committed
batch-admission lake packets -- the TikTok counterpart of
``run_youtube_watch_packet_metric_rollup_producer``.

One TikTok metric cycle on the operator box:

1. admit the creator batch into the lake
   (``run_source_capture_tiktok_batch_packet ... --data-root ...``);
2. THIS runner: build the TikTok metric document from the latest committed
   batch-admission packet per creator handle (fail-closed on ties, non-integer
   stats, and unmapped handles) and append MetricObservation +
   MetricRollupObservation Silver records with a fresh ``--generated-at-utc``
   (defaults to now);
3. ``run_creator_metric_rollup_snapshot --platform tiktok`` to advance the
   committed snapshot (the selection manifest's run-order chain guards the
   advance);
4. ``run_creator_profile_current_materialize --write`` to refresh the view.

Account identity stays fenced: there is NO TikTok row in the linkage ledger yet
(identity additions are a separate owner-gated lane), so this runner resolves
captured creator handles through the linkage ledger's ``tiktok`` platform
accounts when they exist, merged with explicit operator-attested
``--account-map handle=account_id`` entries. A captured handle with no mapping
fails closed with a clear message; this runner never writes the ledger.

Each cycle appends -- never rewrites -- so the longitudinal per-account rollup
history accrues in the lake; ``run_creator_rollup_formula_revalidation`` can
recompute the whole history at any time.

This runner WRITES to the lake: the producer is append-only with no dry-run, so
each invocation deposits durable records (durable real-lake writes stay
owner-gated and operator-box-only). CI never resolves the real lake; the
testable core (``run_tiktok_batch_producer``) runs against
``DataLakeRoot.for_test``, and ``main``/``resolve`` is the only real-lake-bound
path.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from capture_spine.creator_profile_current.tiktok_metric_seed import (
    TIKTOK_BATCH_METRIC_RECIPE_VERSION,
    build_tiktok_batch_creator_metric_seed_document,
)
from capture_spine.creator_profile_current.tiktok_silver_metric_producer import (
    TiktokCreatorMetricSilverResult,
    derive_tiktok_creator_metric_silver_records_from_seed,
)
from data_lake.root import DataLakeRoot, DataLakeRootError

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ACCOUNT_LEDGER = (
    ROOT
    / "forseti"
    / "product"
    / "spines"
    / "capture"
    / "core"
    / "source_families"
    / "social_media"
    / "creator_registry"
    / "creator_public_handle_linkage_ledger_v0.json"
)


def _load_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def _now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def run_tiktok_batch_producer(
    data_root: DataLakeRoot,
    *,
    account_id_by_handle: Mapping[str, str],
    generated_at_utc: str,
) -> TiktokCreatorMetricSilverResult:
    """Build the TikTok batch metric document, then append its observation +
    rollup records to the lake. The testable core -- lake-parameterized so it
    runs against ``DataLakeRoot.for_test``."""
    document = build_tiktok_batch_creator_metric_seed_document(
        data_root,
        account_id_by_handle=account_id_by_handle,
        generated_at_utc=generated_at_utc,
    )
    return derive_tiktok_creator_metric_silver_records_from_seed(
        data_root=data_root,
        seed_document=document,
    )


def resolve_account_map(
    cli_entries: Sequence[str] | None,
    account_ledger: Mapping[str, Any],
) -> dict[str, str]:
    """Merge the linkage ledger's ``tiktok`` platform accounts with explicit
    ``handle=account_id`` CLI entries into one handle->account map.

    Fail-closed rules: a malformed CLI entry, a blank handle/account id, two
    CLI entries disagreeing for one handle, or a CLI entry contradicting a
    ledger row all raise ``ValueError`` (an ambiguous identity mapping must
    never pick silently). An empty combined map raises too -- with no TikTok
    identity anywhere, every captured handle would fail downstream, so fail
    here with the actionable message instead."""
    mapping: dict[str, str] = {}
    accounts = account_ledger.get("platform_accounts")
    if isinstance(accounts, list):
        for account in accounts:
            if not isinstance(account, Mapping) or account.get("platform") != "tiktok":
                continue
            handle = account.get("public_handle")
            account_id = account.get("platform_account_id")
            if not isinstance(handle, str) or not handle.strip():
                raise ValueError("ledger tiktok platform account must carry public_handle")
            if not isinstance(account_id, str) or not account_id.strip():
                raise ValueError(
                    f"ledger tiktok account for @{handle} must carry platform_account_id"
                )
            key = handle.strip().lstrip("@").casefold()
            account_id = account_id.strip()
            existing = mapping.get(key)
            if existing is not None and existing != account_id:
                raise ValueError(
                    f"ledger has two tiktok accounts for @{handle} ({existing!r} and "
                    f"{account_id!r}); an ambiguous identity mapping must be resolved in the "
                    "ledger, not picked silently"
                )
            mapping[key] = account_id

    for entry in cli_entries or []:
        handle, separator, account_id = entry.partition("=")
        handle = handle.strip().lstrip("@")
        account_id = account_id.strip()
        if not separator or not handle or not account_id:
            raise ValueError(
                f"--account-map entry {entry!r} is not of the form handle=account_id"
            )
        key = handle.casefold()
        existing = mapping.get(key)
        if existing is not None and existing != account_id:
            raise ValueError(
                f"--account-map entry {entry!r} conflicts with the mapping already "
                f"resolved for @{handle} ({existing!r}); an ambiguous identity mapping "
                "must be resolved explicitly, not picked silently"
            )
        mapping[key] = account_id

    if not mapping:
        raise ValueError(
            "no TikTok account mappings available: the linkage ledger has no tiktok "
            "platform accounts yet (identity additions are a separate owner-gated lane); "
            "pass --account-map handle=account_id for each captured creator"
        )
    return mapping


def _account_of(record: Mapping[str, Any]) -> str | None:
    try:
        return record["payload"]["observation"]["subject"]["ref"]["orca_platform_account_id"]
    except (KeyError, TypeError):
        return None


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Append TikTok creator-metric Silver rollups to the data lake from the latest "
            "committed batch-admission packet per captured creator handle "
            f"(recipe {TIKTOK_BATCH_METRIC_RECIPE_VERSION})."
        )
    )
    parser.add_argument("--account-ledger", type=Path, default=DEFAULT_ACCOUNT_LEDGER)
    parser.add_argument(
        "--account-map",
        action="append",
        dest="account_map",
        default=None,
        metavar="HANDLE=ACCOUNT_ID",
        help=(
            "Operator-attested TikTok handle->platform_account_id mapping (repeatable). "
            "Merged with the linkage ledger's tiktok accounts; a captured handle with no "
            "mapping fails closed. This runner never writes the ledger."
        ),
    )
    parser.add_argument("--data-root", default=None, help="Lake root; defaults to FORSETI_DATA_ROOT (legacy ORCA_DATA_ROOT).")
    parser.add_argument(
        "--generated-at-utc",
        default=None,
        help="computed_at for the derived rollups. Defaults to now (UTC).",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    generated_at = args.generated_at_utc or _now_utc()

    account_document = _load_json(args.account_ledger)
    account_ledger = account_document.get("creator_public_handle_linkage_ledger", account_document)
    try:
        account_id_by_handle = resolve_account_map(args.account_map, account_ledger)
    except ValueError as exc:
        parser.exit(status=2, message=f"{exc}\n")

    try:
        data_root = DataLakeRoot.resolve(explicit=args.data_root)
    except DataLakeRootError as exc:
        parser.exit(status=2, message=f"data lake unavailable: {exc}\n")

    data_root.rebuild_availability()  # batch-packet discovery reads the availability index

    try:
        result = run_tiktok_batch_producer(
            data_root,
            account_id_by_handle=account_id_by_handle,
            generated_at_utc=generated_at,
        )
    except Exception as exc:  # noqa: BLE001 - operator feedback; fail-closed, no partial-success masking
        parser.exit(
            status=2,
            message=(
                "tiktok batch creator metric rollup producer failed: "
                f"{type(exc).__name__}: {exc}\n"
            ),
        )

    accounts = sorted({a for a in (_account_of(r) for r in result.rollup_records) if a})
    print(
        f"appended {len(result.rollup_records)} rollup(s) + "
        f"{len(result.observation_records)} observation(s) for {len(accounts)} account(s) "
        f"at computed_at={generated_at}"
    )
    for path in result.rollup_paths:
        print(f"  rollup: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
