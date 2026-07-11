# Forseti Data Lake Integrity Pass Receipt v0

```yaml
retrieval_header_version: 1
artifact_role: workflow operational record (executed-window receipt)
scope: >
  Observed-fact receipt for the 2026-07-10 lake integrity pass on
  F:\forseti-data-lake: relocate_to_sharded + rebuild_availability cleared the
  doctor's pre-existing legacy-flat/orphan/missing-availability issues, and the
  12 stale .staging scratch dirs were removed. Doctor went status=ok.
use_when:
  - Checking why the data-lake doctor went green on 2026-07-10.
  - Tracing where the 11 formerly-flat raw packets went (sharded homes).
authority_boundary: retrieval_only
open_next:
  - docs/workflows/forseti_data_lake_physical_rename_runbook_v0.md
stale_if:
  - A later lake operation changes packet counts or index state; this receipt
    records the 2026-07-10 window only.
```

## Window

- executed: 2026-07-10, immediately after the physical rename window (same
  quiesce regime; process scan clean at window start and re-checked before
  mutation).
- authorization: owner directive this turn accepting the deep-think step-2
  plan ("let's do those then. 1-2"), plus an explicit in-chat owner order
  naming `relocate_to_sharded` + `rebuild_availability` when the harness
  auto-mode classifier requested per-operation confirmation.
- pipeline: assumption gate (`READY_WITH_VERIFIED_LEDGER`) -> `/fused`
  (scoping `ROUTE_COMPLETE` -> spec fast-exit -> micro lock `route_ready`).

## Pre-State (doctor, observed immediately before)

- `status=issues_found`; `raw_packet_count 588`, `verified 588`,
  `availability_count 596`.
- Issues: `legacy_flat_packets` 11 (flat `raw/<packet_id>` containers,
  invisible to sharded by-key reads), `orphan_availability` 11 (the same 11
  ULIDs -- entries pointing at not-yet-existing sharded paths),
  `missing_availability` 3.
- `.staging`: 12 stale dirs (4 ULID + 8 `tiktok_funmi_*` probes; newest
  LastWriteTime 2026-07-08 23:48).

## Operations And Observed Outputs

1. `DataLakeRoot.resolve(explicit=F:\forseti-data-lake)` ->
   `relocate_to_sharded()` -> output `RELOCATED 11` (exactly the 11 flat raw
   packets; no flat derived/acknowledgement anchors existed) ->
   `rebuild_availability()` -> output `REINDEXED 599`. Exit 0.
2. Doctor re-run: `status=ok`, exit 0; `raw_packet_count 599`,
   `verified_raw_packet_count 599`, `availability_count 599`; all ten issue
   lists individually verified count 0.
3. `.staging` clear: python `shutil.rmtree` over the explicit 12-name list
   with a pre-delete name-list match gate (matched exactly); output
   `REMOVED 12 | remaining: 0`. Doctor re-run after: `status=ok`.

Raw and derived record content untouched: relocation is an atomic same-volume
directory rename keyed by packet id; the availability index is disposable and
regenerated from committed raw; staging is non-authoritative operational
scratch per the v4.1 forward-epoch contract.

## Non-Claims

Observed-fact record only. Not validation, readiness, lake-health proof,
packet-content verification beyond the doctor's own hash checks, or authority
for any future lake operation. A green doctor at this timestamp says nothing
about later windows.
