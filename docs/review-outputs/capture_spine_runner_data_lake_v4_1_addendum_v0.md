# Capture Spine Runner Data Lake v4.1 Addendum v0

```yaml
retrieval_header_version: 1
artifact_role: Review report
scope: >
  v4.1-specific addendum to the Capture Spine runner data-lake dump audit:
  compares current runner lake seams, DataLakeRoot behavior, live-root evidence,
  and tests against the v4.1 forward-epoch contract.
use_when:
  - Checking whether Source Capture packet writers are v4.1 lake-write compliant.
  - Planning the smallest complete patch after the initial runner seam audit.
  - Distinguishing legacy lake-seam support from v4.1 root/ref compliance.
open_next:
  - docs/review-outputs/capture_spine_runner_data_lake_dump_audit_v0.md
  - docs/workflows/capture_spine_runner_data_lake_dump_audit_handoff_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_v4_1_forward_epoch_contract_v0.md
  - forseti-harness/data_lake/root.py
  - forseti-harness/runners/
  - forseti-harness/tests/contract/test_capture_runner_lake_seam_coverage.py
branch_or_commit: codex/ig-reels-capture-spine @ 13680dddf6b7e3ab044fa4091a6e00373b055031
stale_if:
  - DataLakeRoot root marker, raw sharding, availability, or epoch behavior changes.
  - Any Source Capture packet runner gains or loses --data-root / ORCA_DATA_ROOT support.
  - core_spine_v0_data_lake_v4_1_forward_epoch_contract_v0.md is committed, rejected, or materially changed.
  - F:\orca-data-lake is archived, deleted, migrated, or reinitialized as a v4.1 root.
authority_boundary: retrieval_only
```

## Body Opening

Purpose: updates the earlier runner seam audit with the stricter v4.1 question:
does a runner merely have a lake target, or can it commit v4.1-compatible packet
refs into a v4.1 root?

Use this addendum with the original audit report. Do not use it for Silver Vault
schema decisions, external-root cleanup authorization, live capture authorization,
or a claim that the untracked v4.1 contract is landed on main.

Authority boundary: current user instruction, `AGENTS.md`, and
`.agents/workflow-overlay/` win. Code and read-only live-root observations win
over this report when they drift.

Recheck recipe: rerun branch/head/status; reread the v4.1 contract, `root.py`,
`writer.py`, `packet_assembly.py`, runner CLIs, and seam tests; read the live
root marker/counts without writing to `F:\orca-data-lake`.

Non-claims: not validation, not readiness, not implementation authorization, not
approval to patch runners, not permission to write/delete/archive the external
root, and not a claim that the v4.1 contract is committed or merged.

## Source Loading Receipt

- `AGENTS.md`, `.agents/workflow-overlay/README.md`,
  `.agents/workflow-overlay/source-loading.md`,
  `.agents/workflow-overlay/decision-routing.md`,
  `.agents/workflow-overlay/artifact-folders.md`,
  `.agents/workflow-overlay/retrieval-metadata.md`, and
  `docs/workflows/artifact_retrievability_guide.md`: reread for Orca routing,
  source loading, accepted folder, and report metadata rules.
- `docs/workflows/capture_spine_runner_data_lake_dump_audit_handoff_v0.md`:
  reread from the corrected absolute path. Its active objective is read-only
  v4.1 runner audit/report work, not implementation.
- `docs/workflows/data_capture_spine_consolidation_map_v0.md`,
  `source_capture_playbook_v0.md`, and `capture_recon_index_v0.md`: reread for
  Capture Spine routing and packet-grade capture boundaries.
- `core_spine_v0_data_lake_core_contract_v0.md`,
  `core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md`,
  `core_spine_v0_data_lake_physicality_location_contract_v0.md`, and
  `core_spine_v0_data_lake_v4_1_forward_epoch_contract_v0.md`: reread for lake
  boundary, index rebuildability, physical-root rules, and v4.1 obligations.
- `orca-harness/data_lake/root.py`, `orca-harness/source_capture/writer.py`,
  `orca-harness/source_capture/packet_assembly.py`, `orca-harness/runners/`,
  and `orca-harness/tests/`: reread/scanned for current implementation and tests.

## Current State

- Branch/head observed for this addendum: `codex/ig-reels-capture-spine`,
  `13680dddf6b7e3ab044fa4091a6e00373b055031`.
- Worktree is dirty outside this report lane. The v4.1 contract is currently an
  untracked workspace source, and the physicality/location contract is modified.
  Treat them as current lane evidence, not as a landed/mainline claim.
- Existing audit report
  `docs/review-outputs/capture_spine_runner_data_lake_dump_audit_v0.md` is
  committed at HEAD and has no working-tree diff.
- Fresh read-only live root marker: `F:\orca-data-lake\.orca-data-root` has
  `contract_version` `v0`, label `orca-canonical`, and root UUID
  `01KW1E6N133JT0XCN2KCN0V5A4`.
- Fresh read-only live counts: `242` raw manifests, `343` derived files,
  `242` availability entries, `0` derived_retrieval files.
- Fresh availability scan: `241` entries have sharded `raw/<shard>/<packet_id>`
  paths; `1` entry is unsharded, the previously recorded accidental test packet.

## v4.1 Findings

### V41-F1 - High - No current runner is fully v4.1-compliant

Three direct packet writers expose the lake target, but their shared write path
still uses the current `DataLakeRoot`, whose marker and refs are v0/legacy:

- `core_spine_v0_data_lake_v4_1_forward_epoch_contract_v0.md:136-159` requires
  a v4.1 root marker plus `.orca-lake-epoch.json`.
- `core_spine_v0_data_lake_v4_1_forward_epoch_contract_v0.md:161-170` requires
  forward packet writers to fail closed on a v4.1 root, publish under
  `raw/<packet_shard>/<packet_id>/`, write content-free availability, and expose
  `--data-root` or `ORCA_DATA_ROOT` unless intentionally local-only.
- `orca-harness/data_lake/root.py:39-40` sets
  `ROOT_MARKER_CONTRACT_VERSION = "v0"`.
- `orca-harness/data_lake/root.py:202-203` emits unsharded availability refs:
  `raw/{packet_id}` and `raw/{packet_id}/manifest.json`.
- `orca-harness/data_lake/root.py:423-451` stages/publishes to
  `raw/<packet_id>`, not `raw/<packet_shard>/<packet_id>`.

Result: `run_source_capture_packet.py`, `run_source_capture_http_packet.py`, and
`run_source_capture_ig_reels_grid_packet.py` are lake-seam-capable, but not
v4.1-compliant until `DataLakeRoot` is patched and tested for v4.1 root/ref
semantics.

### V41-F2 - High - The live root is not a v4.1 validation target

The live root remains a legacy/mixed root, not a clean v4.1 root:

- Marker says `contract_version` `v0`, not `v4.1`.
- `.orca-lake-epoch.json` is not established by the observed marker contract.
- Availability entries are mixed: `241` sharded legacy entries and `1` unsharded
  incident entry.

Result: use the live root only as read-only legacy evidence. Do not treat a write
into `F:\orca-data-lake` as proving v4.1 compliance, and do not use this lane to
clean up the accidental packet.

### V41-F3 - High - Tests enforce seam presence, not v4.1 behavior

Current tests catch some runner lake-seam drift but do not enforce the v4.1
contract:

- `test_capture_runner_lake_seam_coverage.py:18-21` classifies packet producers
  by writer tokens and the seam by substring `data_root`.
- `test_capture_runner_lake_seam_coverage.py:26-36` allowlists nine unsynced
  direct packet writers.
- `test_data_lake_availability.py:45` asserts `entry["raw_path"] ==
  f"raw/{pid}"`, the legacy unsharded path.
- `test_data_lake_root.py:90-92` checks the root marker against the current
  `ROOT_MARKER_CONTRACT_VERSION`, which is `v0` in `root.py:40`.

Result: a runner can pass current seam coverage while still writing v0 refs.
v4.1 needs tests for marker contract, epoch marker, sharded raw path, availability
refs, rebuild behavior, and explicit output/data-root mutual exclusion.

### V41-F4 - Medium - The prior report remains useful but is stale for v4.1

The prior report correctly inventories lake seam support and the live
sharded/unsharded conflict. It should now be read as the legacy seam inventory.
This addendum is the v4.1 overlay: the decisive question is no longer only
"does the runner expose `data_root`?", but "does that exposed target write v4.1
root/ref semantics?"

## v4.1 Runner Matrix

| Runner group | Lake seam today | v4.1 status |
| --- | --- | --- |
| `run_source_capture_packet.py` | Yes: `--data-root` / `ORCA_DATA_ROOT`, shared writer | Not v4.1-compliant until `DataLakeRoot` writes v4.1 marker/epoch/sharded refs |
| `run_source_capture_http_packet.py` | Yes: `--data-root` / `ORCA_DATA_ROOT`, `stage_and_write_packet` | Same blocker: uses shared `DataLakeRoot` semantics |
| `run_source_capture_ig_reels_grid_packet.py` | Yes: mutually exclusive `--output` / `--data-root`, env support | Same blocker: uses shared `DataLakeRoot` semantics |
| Nine known-unsynced direct packet writers | No: required local `--output` only | Not v4.1-compliant; first needs lake seam, then v4.1 writer behavior |
| `run_source_capture_durability_series.py` | No: child writer argv owns `--output` | Needs separate design: child raw packets may belong in lake, series state may not |
| `run_reddit_old_http_batch.py` | No: required `--output-root` local batch | Needs separate design: raw child packets vs local batch summaries |
| Bootstrap/config, projection/reporting, candidate/frontier/screening runners | Not packet writers by current source evidence | Excluded unless they start emitting Source Capture Packets |

## Patch Recommendation

Smallest complete v4.1 patch sequence:

1. Add test safety first.
   - Prevent inherited `ORCA_DATA_ROOT` from directing unit/contract tests at a
     real operator root unless the test explicitly creates a `DataLakeRoot.for_test`
     root.
   - This is still first because the previous audit observed a real live-root
     write during tests.

2. Patch `DataLakeRoot` to v4.1 before broad runner wiring.
   - Add v4.1 root initialization/verification with `.orca-data-root`
     `contract_version: "v4.1"` plus `.orca-lake-epoch.json`.
   - Add a packet shard helper and publish raw packets under
     `raw/<packet_shard>/<packet_id>/`.
   - Update availability write/read/rebuild refs to match the sharded path.
   - Update root/read/availability tests so unqualified `raw/<packet_id>` is no
     longer the v4.1 expectation.

3. Upgrade seam tests from token coverage to v4.1 behavior coverage.
   - Keep the current producer/seam matrix as a cheap guard, but add execution
     tests for v4.1 marker, sharded raw path, content-free availability, and
     output/data-root mutual exclusion for every patched runner.

4. Then wire missing direct packet writers in lowest-churn order.
   - Start with `stage_and_write_packet` users (`antiblock_http`, `media`,
     `price_payload`) after the shared v4.1 writer path is correct.
   - Patch direct `write_local_source_capture_packet` users next with a shared
     safe staging pattern rather than per-runner temp-location inventions.

5. Treat orchestrators separately.
   - Decide whether durability-series and Reddit batch child raw packets commit
     into the lake while series/batch summaries remain local or move later as
     derived/ack records.

## Validation

- Fresh source reads and static runner/test scans completed.
- Fresh live-root reads completed without writing to `F:\orca-data-lake`.
- No runner, test, data-lake implementation, Silver Vault, physicality contract,
  or external data-root edit was made.
- Pytest was not run for this addendum because the change is documentation-only;
  rerun targeted tests only after clearing or guarding `ORCA_DATA_ROOT`.
