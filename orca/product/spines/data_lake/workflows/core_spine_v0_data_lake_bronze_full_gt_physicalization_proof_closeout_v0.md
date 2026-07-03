# Core Spine v0 Data Lake Bronze Full-GT Physicalization Proof Closeout v0

```yaml
retrieval_header_version: 1
artifact_role: Data Lake workflow/evidence record
scope: >
  Closeout record for the owner-authorized physicalization proof scope
  (STEP-01..06 of the proof scoping route): the A1 deterministic touchpoint
  inventory gate and the named six-invariant proof gate (PROOF-01..06) under
  the ratified packet-member relationship, with fail-capability evidence,
  CI ownership, residuals, and non-claims.
use_when:
  - Checking what the Bronze physicalization proof scope proved, at what tier, and with which tests.
  - Deciding the next Bronze full-GT move (A2 serialization decision, third-proof threshold, final de-correlated review).
  - Checking which MGT baseline items 1 and 4 obligations are closed versus still open.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_physicalization_proof_scoping_route_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_bronze_mgt_baseline_declaration_v0.md
  - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate1_attachment_record_body_layout_adr_v0.md
stale_if:
  - The inventory module, gate test, or proof test materially changes.
  - A later accepted decision closes A2, the third-proof threshold, or the final de-correlated review.
  - Either ratified gate ADR is superseded.
```

## Status

`PHYSICALIZATION_PROOF_SCOPE_IMPLEMENTED_V0` — fixture-lake tier, CI-owned,
delegated review pending. Not validation of a production lake, not all-source
coverage, not A2/backend selection, not readiness, not a Bronze full-GT claim.

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: proof-scope pack (scoping route + both gate ADRs + folded contracts + harness surfaces; spec + micro-decision lock in-lane)
  edit_permission: implementation-authorized (owner yes on the route's single fork, 2026-07-02, /fused)
  target_scope: STEP-01..06 implementation + this closeout; no backend, no second body home, no A2 selection.
  dirty_state_checked: yes (lane branch claude/bronze-proof-scope-impl off origin/main @ 1dfbb2d0)
  blocked_if_missing: none
```

## What Landed

- **A1 deterministic inventory gate** (STEP-02/03):
  `orca-harness/data_lake/inventory.py` single-sources the AST discovery the
  seam-coverage test seeds (writers, orchestrators, recursive writer-function
  closure, non-raw touchpoints) and builds the checked-in record
  `orca-harness/data_lake/lake_touchpoint_inventory_v0.json` — five families:
  runner seams (22), writer functions (10), non-raw touchpoints (45 call
  sites), reasoned exclusions, owner-dispositioned unknowns (0 on the current
  tree), plus a deterministic `a2_fork_impact` routing tag per entry
  (`manifest_shape` / `packet_index` / `none`; metadata for the deferred A2
  decision, not a selection). The gate
  `orca-harness/tests/contract/test_data_lake_inventory_gate.py` fails on
  undeclared or stale entries in either direction, reasonless exclusions, and
  unknowns without a resolved owner disposition (owner attribution = the
  human-gated PR merge; never self-certified). The seam-coverage test now
  imports discovery from the module with its assertion baselines unchanged.
- **Six-invariant proof gate** (STEP-04):
  `orca-harness/tests/test_data_lake_physicalization_proof.py`, PROOF-01..06
  under the ratified packet-member relationship, each proof in a clean half
  plus a seeded-violation half exercised through the same public API:
  - PROOF-01 write-once raw (second stage AND bypass publish both refused);
  - PROOF-02 append-only derived/ack (rewrite refused in both subtrees);
  - PROOF-03 read-by-key (shard recomputed; verified read works with
    `indexes/` deleted; missing packet fails closed);
  - PROOF-04 hash verification (`hash_basis: raw_stored_bytes`; tampered
    stored bytes fail the verified read);
  - PROOF-05 public AR body resolution (`source_surface_catalog_rows` +
    `load_attachment_record_body` resolve and re-hash the packet-member body;
    tampered body fails public resolution);
  - PROOF-06 index rebuild (availability + Bronze catalog rebuild
    byte-identical from committed packet material; reads survive index loss —
    indexes carry no authority).
- **CI ownership** (STEP-05): `.github/workflows/ci.yml` runs `python -m
  pytest` with default collection from `orca-harness/`, so both gates run on
  every PR and main push. `run_data_lake_doctor.py` was deliberately not
  extended (micro-lock: the doctor inspects real lakes; fixture proofs are CI
  tests; the route's "and/or" permits CI-only).

## Validation Evidence

- Full suite: `python -m pytest` from `orca-harness/` exits 0 with
  `ORCA_DATA_ROOT` unset (CI-equivalent), 2026-07-02.
- Fail-capability is itself tested: seeded undeclared writer, stale declared
  entry, reasonless exclusion, and undispositioned unknown each trip the
  inventory gate; each PROOF-0x violation half asserts the guarded refusal.
- Determinism: the inventory record regenerates byte-identically on unchanged
  source (tested).
- Environment finding (pre-existing, out of scope, surfaced separately): two
  tests (`tests/unit/test_run_source_capture_packet_lake.py::test_cli_requires_exactly_one_target`,
  `tests/unit/test_youtube_creator_observation_ledger.py::test_youtube_shorts_fragrance_creator_observation_ledger_live_lake_refs_when_available`)
  touch the LIVE lake when `ORCA_DATA_ROOT` is set locally; runs on this
  machine published junk packets `raw/b84/01KWHEKSMH48YM867TWQVHH3DH` and
  `raw/e6c/01KWHEPTZPE9BD85WFG65WM18R` (plus an earlier session's
  `raw/18c/01KWH4E076VKH9VHVWKFZ3M2F4`, `raw/e20/01KWH4DJF2JADQ2PBHVYQX921A`).
  Hermetic-isolation fix is a spawned follow-up task; removing the junk
  packets from the live lake is an owner decision (raw is write-once).

## Residuals (still open toward full GT)

- **A2** — Manifest v2 vs manifest-equivalent packet index: owner decision,
  now unblocked by the A1 inventory (`a2_fork_impact` tags mark which
  surfaces each fork touches). Not selected here.
- **Materially-different third proof** — only if a source shape crosses the
  brief's threshold; the YouTube ambiguous-AR branch stays
  code-present/not-test-proven.
- **Final de-correlated review** over the finished contracts + code path
  (brief Full-GT Distance item 5); the delegated review commissioned from
  this lane covers this diff, not the full closeout review.
- **Backend posture** — unselected; any backend ADR fires Gate 2 trigger T3.
- **"Real lane fixtures" breadth** (MGT item 4 tail): the proof gate runs on
  representative fixture lakes; broader real-lane fixture coverage stays open.
- Gate 2's ratified deferral stands: the claim ceiling caps all deletion
  language; tombstone posture is not exercised by this scope.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Bronze MGT baseline full-GT distance items 1 and 4 change status: item 1
    (deterministic discovery gate for raw-packet writers and non-raw lake
    touchpoints) is closed at source-inventory tier by the A1 inventory gate;
    item 4 (promote rebuild checks into a CI-owned gate over representative
    fixture lakes) is partially closed by the CI-owned PROOF-01..06 fixture
    proofs, with real-lane-fixture breadth still open. No other doctrine
    changes: the ratified gate ADRs, folded contracts, A2 deferral, and Gate 2
    posture are consumed, not modified.
  trigger: architecture_doctrine
  controlling_sources_updated:
    - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_physicalization_proof_closeout_v0.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_bronze_mgt_baseline_declaration_v0.md
    - docs/workflows/orca_repo_map_v0.md
  downstream_surfaces_checked:
    - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_physicalization_proof_scoping_route_v0.md
    - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate1_attachment_record_body_layout_adr_v0.md
    - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_next_material_decisions_v0.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
  intentionally_not_updated:
    - path: orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_physicalization_proof_scoping_route_v0.md
      reason: >
        Its stale_if self-fired when the owner granted the route's single
        yes/no (2026-07-02, /fused); it is now the historical route record and
        this closeout is the continuation anchor.
    - path: orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_next_material_decisions_v0.md
      reason: >
        Historical A1/A2 definition record (already superseded as continuation
        anchor by the brief); its A1 definition was consumed faithfully and A2
        remains open exactly as it states.
    - path: orca/product/spines/data_lake/authority/ (AR implementation, storage contracts)
      reason: >
        The proof scope implements against their folded text without changing
        any contract semantics; acceptance checks 1-8 are exercised by
        PROOF-01..06, not amended.
  stale_language_search: >
    rg -n "deterministic discovery gate|manual runner|not yet a fail-capable|inventory gate"
    orca/product/spines/data_lake docs/workflows/orca_repo_map_v0.md
  stale_language_search_result: >
    Executed 2026-07-02 after edits. Remaining hits are the annotated MGT
    baseline items themselves, this closeout, the repo-map rows updated in
    this lane, historical gate-framing records (brief, next-material-decisions,
    batch plan - all superseded/historical by their own stale_if), and the
    scoping route (historical since owner authorization). No live surface
    still claims the discovery gate is missing or the rebuild checks are
    manual-only.
  non_claims:
    - not validation of a production lake
    - not all-source coverage
    - not A2, backend, or serialization selection
    - not readiness or a Bronze full-GT claim
```

## Non-Claims

- Not a Bronze full-GT claim: A2, the materially-different third proof, the
  final de-correlated review over contracts + code, and backend posture remain
  open (see Residuals).
- Not erasure capability; Gate 2's ratified claim ceiling governs all
  deletion language.
- Not production-lake validation; all proofs run on deterministic fixture
  lakes.
- Delegated review of this lane's diff is commissioned, not completed;
  acceptance is home-model adjudication's call under its own authority.
