# Core Spine v0 Data Lake Bronze Full-GT Physicalization Proof Implementation-Scoping Route v0

```yaml
retrieval_header_version: 1
artifact_role: Data Lake workflow/implementation-scoping record
scope: >
  Read-only implementation-scoping route for the Bronze full-GT
  physicalization proof scope after Gate 1/Gate 2 ratification and contract
  fold-in: the A1 deterministic inventory gate plus a named deterministic
  proof gate for the six lake invariants (write-once raw, append-only
  derived/ack, read-by-key, hash verification, public AR body resolution,
  index rebuild) under the ratified packet-member relationship. Ends at a
  single owner yes/no on bounded implementation authorization.
use_when:
  - Granting or refusing bounded implementation authorization for the physicalization proof scope.
  - Starting the authorized implementation lane for STEP-01 through STEP-06.
  - Checking what the proof scope must not touch (backend, second body home, full-GT claim).
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate1_attachment_record_body_layout_adr_v0.md
  - forseti/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate2_retention_lawful_erasure_posture_adr_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md
  - forseti/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_next_material_decisions_v0.md
stale_if:
  - The owner grants, modifies, or refuses the bounded implementation authorization below (the decision then governs).
  - Either ratified gate ADR is superseded, or the folded contracts change the body-layout or erasure boundary.
  - The seam-coverage test, lane registry, DataLakeRoot primitives, or catalog public surface materially change before implementation starts.
```

## Status

`PROOF_SCOPE_ROUTE_RECORDED_V0` — read-only scoping output. Not
implementation, implementation authorization, validation, readiness, review,
serialization (A2) selection, backend selection, or a Bronze full-GT claim.

```yaml
forseti_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom proof-scope pack (both ratified gate ADRs, folded AR/storage/physicality contracts, raw-admission contract, next-material-decisions A1/A2 definitions, harness surfaces listed in the source-read ledger)
  edit_permission: docs-write (this route record only; scoped implementation stays unauthorized)
  target_scope: read-only implementation-scoping route for the physicalization proof scope.
  dirty_state_checked: yes (lane branch at fold-in commit b0c37bd0; tree clean before this artifact)
  blocked_if_missing: none
```

## Plan Intake

- Plan source: `docs/hygiene/bronze_full_gt_post_ratification_handoff_v0.md`
  (accepted cross-lane handoff; anchor goal step 2 names this route), both
  owner-ratified gate ADRs (2026-07-02), and the contract fold-in landed at
  commit `b0c37bd0`.
- Acceptance status: accepted. `acceptance_basis: accepted_explicit` — the
  owner ratified both gates in-session ("2 gates OK") and the accepted handoff
  explicitly orders this scoping step and its ending owner fork.
- Objective: make the Bronze physicalization proof scope implementable in one
  bounded lane — a deterministic A1 inventory gate plus a named, fail-capable
  proof gate for the six invariants under the ratified packet-member
  relationship.
- Expected observable change (when later authorized): new inventory module +
  fail-capable inventory gate; a named physicalization proof gate over a
  representative fixture lake; doctor/CI wiring; a closeout proof record. No
  behavior change to writers, readers, or contracts.
- A1 definition source: `core_spine_v0_data_lake_bronze_full_gt_next_material_decisions_v0.md`
  (historical but load-bearing for A1/A2): durable inventory of (1) raw packet
  writers and runner seams, (2) non-raw lake touchpoints, (3) explicit
  exclusions with reasons, (4) owner-reviewed unknowns, (5) the A2
  serialization fork each touchpoint would affect.
- Non-goals: A2 serialization selection (owner decision after A1), backend or
  engine anything (fires Gate 2 T3), a second body home, sidecar occupancy,
  tombstone machinery, third-proof work, migration/replay mechanics, and any
  full-GT claim.

## Frozen Decisions (do not reopen)

- Packet-member is the ratified default AR body relationship; sidecar
  reserved behind its reopen trigger; G1-D external bodies double-locked
  (Gate 1 ADR, ratified 2026-07-02).
- `hash_basis: raw_stored_bytes` is the rule for packet-member bodies
  (Gate 1 output 2, folded into the AR implementation contract).
- Gate 2 is a ratified bounded deferral: claim ceiling on all deletion
  language; forbidden backend classes/operations; triggers T1-T4 live.
- A2 (Manifest v2 vs packet-index serialization) stays an owner decision
  gated on A1's inventory; this proof scope must not select it implicitly.
- By-key discovery is authority; indexes stay rebuildable and
  non-authoritative; the public AR surface (`source_surface_catalog_rows`,
  `load_attachment_record_body`) is the only consumer resolution path.
- The consumption-seam lane (pickup/ack helper, derived_retrieval rebuild,
  metrics policy) is a separate concurrent lane; do not absorb it.

## Mutable Fields (implementer/spec may settle)

- The durable home and format of the A1 inventory output (checked-in
  generated baseline vs report emitted by the gate) — provided it never
  becomes lake authority and stays deterministic and diffable.
- Whether the six-invariant proof gate lands as one contract test, a doctor
  extension, or both — provided the proof is named, deterministic, and
  fail-capable.
- Exact representative fixture-lake composition — provided it covers the
  inventoried writer/touchpoint shapes that exist at implementation time.
- Whether the existing seam-coverage test delegates to the new inventory
  module or is superseded by the new gate — provided coverage never drops.

## Source-Read Ledger (decisive reads)

| Source | What it bounded |
| --- | --- |
| Both gate ADRs (ratified, on main) | Frozen decisions; proof obligations; stop conditions. |
| AR implementation contract (folded, `b0c37bd0`) | Acceptance checks 1-8 the proof gate must exercise; hash-basis rule. |
| Raw-admission + key grammar contract | Read-by-key must recompute `sha256(packet_id)[:3]` shard; no index/locator dependency. |
| `next_material_decisions_v0.md` | A1's five required inventory outputs; A2 held for owner. |
| `forseti-harness/tests/contract/test_capture_runner_lake_seam_coverage.py` | Existing AST writer-discovery seed (`EXPECTED_BRONZE_WRITER_RUNNERS`, `KNOWN_UNSYNCED`, recursive writer discovery) — A1's starting point. |
| `forseti-harness/data_lake/root.py` | Write-once staging/publish, append-only records, availability rebuild primitives the proofs bind to. |
| `forseti-harness/data_lake/catalog.py` | Public AR surface: `rebuild_catalog`, `source_surface_catalog_rows`, `load_attachment_record_body`. |
| `forseti-harness/data_lake/lane_registry.py` | Non-raw lane roles + front-door state — A1's non-raw touchpoint seed. |
| Existing tests: `test_data_lake_root.py`, `test_data_lake_sharding.py`, `test_data_lake_rebuild_proof.py`, `test_data_lake_doctor.py`, `test_data_lake_catalog.py` | Which invariant pieces already have unit proofs; the gap is a named, fail-capable, relationship-bound proof gate, not first coverage. |
| `forseti-harness/runners/run_data_lake_doctor.py` | Existing inspection surface the proof gate may extend (STEP-05). |

## Likely Touch Points (when authorized)

- New: `forseti-harness/data_lake/inventory.py` (or equivalent module name),
  `forseti-harness/tests/contract/test_data_lake_inventory_gate.py`, a
  physicalization proof test (e.g.
  `forseti-harness/tests/test_data_lake_physicalization_proof.py`), optional
  runner `forseti-harness/runners/run_data_lake_inventory_gate.py`.
- Extended: `forseti-harness/runners/run_data_lake_doctor.py` and/or
  `forseti-harness/tests/test_data_lake_doctor.py` (STEP-05 wiring),
  `forseti-harness/tests/contract/test_capture_runner_lake_seam_coverage.py`
  (delegation/supersession per the mutable field above).
- Docs (closeout only): a proof record under
  `forseti/product/spines/data_lake/workflows/`, MGT baseline items 1/4
  annotations, repo-map row. No authority-contract edits are expected; if one
  becomes necessary it needs its own DCP receipt.
- Not touched: capture writers/runners' behavior, packet schemas, contracts'
  semantics, anything under the consumption-seam lane, any backend surface.

## Implementation Units

- **U1 — A1 deterministic inventory gate.** Extract the AST seam-discovery
  into a reusable inventory module producing the five A1 outputs; add a
  fail-capable gate (contract test, optional runner) that fails on an
  undeclared writer, undeclared non-raw touchpoint, unexplained exclusion, or
  unresolved unknown. Depends on: nothing. Risk: fake-pass (a gate that
  cannot fail) and silent-exclusion drift.
- **U2 — six-invariant proof gate under the ratified relationship.** Bind
  write-once raw, append-only derived/ack, read-by-key (shard recompute, no
  index dependency), hash verification (`raw_stored_bytes` over stored body
  bytes; corrupt-body failure visible), public AR body resolution (catalog
  rows + `load_attachment_record_body`, no private path inference — AR
  acceptance check 8), and index rebuild (byte-identical, non-authoritative)
  into one named deterministic proof over a representative fixture lake, each
  invariant with a seeded violating fixture proving the gate can fail.
  Depends on: U1 (the inventory defines the writer/touchpoint universe the
  fixture lake must represent). Risk: proving only the happy path.
- **U3 — closeout record.** Durable proof record naming what was proven,
  residuals, and non-claims; MGT baseline items 1/4 annotations; receipts per
  the DCP contract. Depends on: U1 + U2 validation evidence.

## Implementation Route

- **STEP-01 — baseline preflight (U1/U2 preflight).** Inspect the
  seam-coverage test internals, `lane_registry.LANE_ROLES`, and doctor checks;
  run the existing data-lake + seam test subset and record the green baseline.
  Verification: pytest baseline pass recorded. Stop: baseline failures stop
  the lane (fix-forward is out of scope without owner word).
- **STEP-02 — inventory module (U1).** Build the reusable discovery module
  emitting the five A1 outputs from writer AST discovery + lane-registry
  roles + append-caller enumeration; deterministic and diffable output.
  Verification: unit tests including a seeded undeclared-writer fixture that
  makes discovery report it. Stop: a touchpoint that cannot be classified
  without an owner call is recorded as an owner-reviewed unknown, never
  auto-excluded.
- **STEP-03 — fail-capable inventory gate (U1).** Contract test (+ optional
  runner) failing on undeclared writers/touchpoints, unexplained exclusions,
  or unresolved unknowns; settle the seam-test delegation/supersession shape
  without dropping coverage. Verification: gate fails on the seeded violation
  and passes on the declared current tree. Stop: any pressure to weaken the
  gate to pass is a defect, not a fix.
- **STEP-04 — six-invariant proof gate (U2).** Named deterministic proof over
  a representative fixture lake per U2, each invariant paired with its seeded
  violating fixture. Verification: all six proofs demonstrably fail on their
  violations and pass on the clean lake. Stop: if any proof would require a
  backend choice (fires Gate 2 T3), a second body home, or changing contract
  semantics — blocker, return to owner.
- **STEP-05 — doctor/CI ownership wiring (U2).** Wire the proof gate into
  `run_data_lake_doctor.py` and/or the CI-run test set so it executes
  deterministically (MGT baseline item 4, partial). Verification: doctor/CI
  run shows the gate executing and fail-capable. Stop: no new authority
  surface; the gate reports, it never becomes lake truth.
- **STEP-06 — closeout record (U3).** Write the proof record + MGT baseline
  annotations + receipts; run `python .agents/hooks/check_dcp_receipt.py
  --strict` and the stale-language searches. Verification: receipt gate green;
  record carries explicit non-claims (no full-GT claim — third proof, final
  de-correlated review, A2, and backend remain open). Stop: any wording that
  reads as a full-GT or readiness claim.

## Review Timing Advisory

- `adversarial_review: recommended`
- `highest_value_checkpoint: after_all_steps_pre_closeout`
- `review_target`: the completed U1+U2 diff (inventory gate + proof gate),
  with emphasis on fail-capability (can every proof actually fail?).
- `why_this_checkpoint`: the dominant risk is fake-pass proofs and silent
  inventory exclusions, which are visible only in the completed diff; earlier
  review would mostly add ceremony. The owner may fold this into the final
  full-GT de-correlated review over contracts + code (brief Full-GT Distance
  item 5), per the standing handoff recommendation.
- `boundary`: Advisory routing only; not review, approval, validation,
  acceptance, or readiness.

## Validation Matrix

| Type | Step | Risk covered | Evidence | Failure means |
| --- | --- | --- | --- | --- |
| Scoping | this record | route unsourced/unbounded | ledger above; ADRs + contracts on main; harness reads | route invalid; re-scope |
| Implementation | STEP-01 | dirty baseline hides regressions | recorded green pytest baseline | stop lane |
| Implementation | STEP-02/03 | fake-pass inventory; silent exclusion | seeded undeclared-writer fixture fails the gate | gate not fail-capable; do not proceed to STEP-04 |
| Implementation | STEP-04 | happy-path-only invariant proof | six seeded violating fixtures each fail | proof invalid; no proof claim |
| Implementation | STEP-05 | gate exists but never runs | doctor/CI execution evidence | MGT item 4 stays open |
| Implementation | STEP-06 | claim inflation; receipt drift | `check_dcp_receipt.py --strict`; stale-language searches | closeout blocked |
| Not run (intentional) | — | production-lake validation, all-source coverage | — | out of scope by design; proofs are fixture-lake deterministic checks, not production validation |

## Rollback / Containment

All steps are additive (new modules/tests/wiring/docs) on a lane branch via
the per-lane PR flow; containment is revert-of-lane-PR. STEP-05 doctor wiring
is the only touch on an existing runner; keep it a separable commit.

## Bloat-Cut Queue

Cut from this scope: A2 serialization comparison, tombstone-honoring reads,
third-proof fixtures, backend spikes, catalog performance work, actor/
retrieval surfaces, consumption-seam integration. Defer: promoting the proof
gate into branch-protection-required CI (owner call at closeout).

## Route Status Block

- `route_status: ROUTE_COMPLETE`
- `implementation_start_readiness: BLOCKED_BY_AUTHORIZATION` — the single
  owner decision below is the only missing binding.
- `current_turn_authorization: read_only_scoping_only` (this record is the
  route, not a start).

## Owner Authorization Fork (single yes/no)

> Authorize bounded implementation of STEP-01 through STEP-06: the A1
> deterministic inventory gate plus the six-invariant physicalization proof
> gate and closeout record — code, tests, doctor/CI wiring, and closeout docs
> only; no backend choice (would fire Gate 2 T3), no second body home, no A2
> selection, no full-GT claim.

**yes** → a bounded implementation lane starts at STEP-01 under the per-lane
PR flow. **no / modify** → this route is revised or shelved; nothing is
implemented.

## Non-Claims

- Not implementation, patching, or an implementation start.
- Not validation, readiness, review, approval, or acceptance.
- Not A2/Manifest v2/serialization, backend, engine, or migration selection.
- Not erasure capability (Gate 2 claim ceiling governs all deletion language).
- Not a Bronze full-GT claim: even with STEP-01..06 done and proven, the
  materially-different third proof, the final de-correlated review over
  contracts + code, A2, and backend posture remain open.

Recommended Implementation Model: judgment_lane — fake-pass-prone validation gates need care.
