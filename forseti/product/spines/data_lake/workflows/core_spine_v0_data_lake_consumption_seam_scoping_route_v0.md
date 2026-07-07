# Core Spine v0 Data Lake Consumption Seam Scoping Route v0

```yaml
retrieval_header_version: 1
artifact_role: Data Lake workflow/scoping record
scope: >
  Non-executing implementation route ("consumption seam v0") for the three
  seam pieces named by the consumption-seam handoff packet: (1) the shared
  derived-lane pickup/acknowledgement helper contract, (2) the
  indexes/derived_retrieval rebuild command for the three gate-opened views,
  and (3) the on-demand-first metrics policy with metric families
  parameterized as operator_to_fill. Route only: implementation requires a
  later explicit bounded owner authorization.
use_when:
  - Authorizing or starting the bounded consumption-seam implementation lane.
  - Checking what the seam implementation may touch, must validate, and must stop on.
  - Checking which seam decisions are frozen versus operator_to_fill.
authority_boundary: retrieval_only
open_next:
  - docs/hygiene/data_lake_consumption_seam_scoping_handoff_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_write_boundary_enforcement_contract_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
branch_or_commit: >
  Authored on claude/elated-cannon-a6e2cf off origin/main be5ffbca; verify
  current git state before lifecycle claims.
stale_if:
  - The Storage, Derived-Layout, Write-Boundary, Physicality, or Silver Vault contract changes the seam boundary, ack grammar, rebuild semantics, or public Bronze surfaces.
  - Gate 1 ADR ratification modifies output 4 (the public Bronze read surfaces).
  - The owner rejects or redirects this route, or a completed seam implementation closeout supersedes it.
```

## Plan Intake

- Plan source: `docs/hygiene/data_lake_consumption_seam_scoping_handoff_v0.md`
  (cold cross-lane handoff, verified reachable on `origin/main` at blob
  `3f5eed53`, identical to the authored copy), consumed under its
  confirm-don't-trust load contract with outcome REUSE: all six ledger
  pointers reverified against current source on 2026-07-02.
- Acceptance status and basis: `accepted_explicit` for the scoping lane — the
  packet records owner confirmation of the seam direction and concurrency
  ("owner confirmed direction and concurrency"), and the current user
  instruction continues exactly this lane. Acceptance of THIS route is a
  separate owner act and is not claimed here.
- Objective: an implementation lane, once explicitly authorized, delivers the
  three seam pieces so every derived lane (Silver, ECR, cleaning, projection)
  picks up committed Bronze work the same tested way, with metrics views
  rebuildable and never authoritative.
- Material intake update discovered during source reread: the packet's open
  question "has the derived_retrieval rebuild trigger formally fired?" is
  resolved — `DERIVED_RETRIEVAL_GATE_OPENED_V0` (owner-ratified 2026-06-25)
  opened the population gate for exactly three OBJECT-LEVEL views
  (`by_creator`, `by_mention`, `undone`); the builder remains a separate
  bounded work unit, not authorized by the gate opening or by this route.
- Non-goals (from packet drift guard, affirmed by contracts): no queue,
  scheduler, event bus, or notification system as pickup truth; no lake-core
  behavior additions; no backend/engine selection; no Gate ADR territory (AR
  body layout, retention/erasure); no cross-platform identity; no actor
  retrieval; no Judgment/gold semantics.

## Frozen Decisions

The implementer must not reopen these; each is owned by a named contract:

- By-key discovery over committed state is pickup authority; a queue may only
  ever optimize notification (storage contract, Write And Read Discipline +
  success signal 4).
- Acknowledgements are lane-owned, append-only, create-only records at
  `acknowledgements/<anchor_shard>/<raw-anchor>/<ack-namespace>/<ack-record-id>`;
  correction is a new ack record; the lake never consumes acks as control
  flow (derived-layout contract, Acknowledgement Addressing; storage contract
  Record-Kind Slots).
- All lake writes go through the deterministic lake-writer boundary;
  derived/ack writes are atomic create-only appends; root resolution is
  fail-closed with per-root identity marker (write-boundary contract).
- Everything under `indexes/` is rebuildable from committed material or it is
  not an index; `derived_retrieval` views are non-authoritative caches
  (derived-layout contract, Index Rebuild Contract).
- The rebuild command shape is contract-pinned:
  `lake indexes rebuild --root <FORSETI_DATA_ROOT> --target availability|derived_retrieval|all --prove-rebuildability`.
- The opened `derived_retrieval` scope is exactly `by_creator` (per-platform),
  `by_mention`, and `undone`; other views stay governance-gated; no engine is
  selected; the SQL query-lens stays scan/query-latency-gated (derived-layout
  contract, Status + Accepted Residuals).
- Bronze is consumed only through the public surfaces
  `source_surface_catalog_rows` and `load_attachment_record_body` (AR
  contract acceptance check 8; Gate 1 ADR output 4 affirms them as the only
  consumer resolution path). No private path or layout inference.
- Metrics posture: on-demand computation is the default; precomputed views
  are rebuildable manifest-backed caches under
  `indexes/derived_retrieval/silver_vault/...` only; `MetricObservation`
  posture invariants forbid missing-evidence-as-zero (Silver Vault contract,
  Metric Observation Records + Generated Read Models).

## Mutable Fields

- **First metric families**: `operator_to_fill`. Options the owner may name
  (per packet): creator/content view-count style families over
  IG/YouTube/TikTok; movement-threshold (`SourceObjectMovementThresholdCrossingRecord`)
  derivations; or defer. STEP-04's metric-view slice stays a parameterized
  placeholder until named — the implementer must not invent a family.
- Helper module placement and exact name (lane-side; must not add behavior to
  `DataLakeRoot`, catalog, or availability) — implementation micro-decision.
- Serialization details of ack/derived record bodies (lane-owned per
  contracts; only the physical relationship is locked).

## Scoping Decision Recorded

The packet left "one shared library surface vs per-lane convention with a
shared test contract" to scoping. **Decided: both, with the test contract as
the binding half** — a shared lane-side helper surface plus a conformance
test contract that any lane pickup implementation must pass. Rationale: the
success signal requires every derived lane to pick up "the same tested way";
only a shared conformance suite makes that checkable, and a shared helper
makes conformance the cheap default. A lane may reimplement pickup only if it
passes the same conformance suite unchanged.

## Likely Touch Points

Source-backed inventory (symbols verified on `be5ffbca`):

- `forseti-harness/data_lake/root.py` — consume as-is: `append_record`,
  `append_record_set`, `is_record_set_complete`, `record_path`, `lane_dir`
  (append-only derived/ack primitives, sharded addressing already landed);
  `read_availability`, `list_available`, `rebuild_availability` (by-key
  committed-state reads). No behavior additions to this module.
- `forseti-harness/data_lake/catalog.py` — consume as-is:
  `source_surface_catalog_rows` (line 334), `load_attachment_record_body`
  (line 1180). No behavior additions.
- `forseti-harness/data_lake/lane_registry.py` — `LaneRole`,
  `validate_registry`, `role_of`: the natural home for the durable
  ack-namespace registration rule (the derived-layout residual "first lane
  needs a durable namespace-registration rule" fires with this work). Extend,
  never fork.
- New lane-side helper module + conformance test suite (placement mutable).
- New rebuild-command builder module + CLI entry for
  `--target derived_retrieval` (builder work unit; `availability` rebuild
  already exists as `DataLakeRoot.rebuild_availability`).
- New authority/contract doc for the seam (STEP-02 deliverable) under
  `forseti/product/spines/data_lake/authority/`.
- One proving consumer lane's pickup path (STEP-05; first candidate:
  transcript-silver, already lake-wired per the gate-opening receipt).

## Implementation Route

Non-executing; every step runs only inside a later explicitly authorized
bounded implementation lane.

- **STEP-01 — Read-only preflight and surface inventory.** Re-verify the
  frozen contracts are unchanged (this route's `stale_if`), then inspect the
  touch-point symbols above and record the exact public surfaces the helper
  may consume. Contract-impact: `local_patch` (no edits). Verification: a
  short inventory note in the lane. Stop: any required capability that needs
  a private path, layout fact, or lake-core change — that is the
  design-is-wrong signal; stop and report.
- **STEP-02 — Author the consumption-seam contract (docs-write).** One
  authority artifact carrying: the pickup definition (by-key enumeration of
  committed work via public surfaces; `undone` = committed minus the lane's
  own acks, computed lane-side), the ack write rule (create-only
  `append_record` under the lane's registered ack-namespace; correction = new
  record), the ack-namespace registration rule bound to `lane_registry`, the
  view-independence invariant (pickup results identical with and without the
  `undone` view — the view is cache, never authority), the conformance test
  contract (pickup idempotence; ack append-only; missed-event recovery by
  rescan; view-independence), and the on-demand-first metrics policy
  (families `operator_to_fill`; precompute only as rebuildable
  manifest-backed views with full Silver Vault manifest-row obligations and
  posture invariants). Contract-impact: `contract_sensitive_with_map` (the
  map is this route's Frozen Decisions). Verification: every rule cites its
  owning contract; drift-guard scan (no queue-as-truth, no backend, no
  lake-core behavior). Review checkpoint: see Review Timing Advisory.
- **STEP-03 — Implement the shared pickup/ack helper + conformance suite.**
  New lane-side module wrapping the public read surfaces and `append_record`
  for acks; conformance tests per the STEP-02 contract. Dependency: STEP-02.
  Verification: conformance suite green; write-boundary tests prove overwrite
  of an existing ack record hard-fails; helper adds zero symbols to
  `DataLakeRoot`/catalog/availability.
- **STEP-04 — Implement the `derived_retrieval` rebuild builder.**
  `lake indexes rebuild --target derived_retrieval` populating the opened
  views in build-precondition order: `undone` and `by_mention` first;
  `by_creator` deferred behind audience-silver lake wiring (Slice C, not yet
  built). Every generated view carries manifest rows per the Silver Vault
  Generated Read Models rules (generation id, source record ids, source
  high-watermark, policy versions, generated_at, stale/drift fields).
  `--prove-rebuildability` must fail when any entry cannot regenerate from
  committed `derived/` + raw refs. Dependency: STEP-03 (the `undone` view is
  a cache of the helper's committed-minus-acks computation). Stop:
  scan/query-latency pressure suggesting an engine — engine selection belongs
  to the Storage Contract physicalization boundary, not this lane.
- **STEP-05 — Prove one consumer.** Migrate one existing derived lane's
  pickup path (first candidate: transcript-silver) onto the helper with the
  conformance suite unchanged. Verification: the lane produces identical
  derived records pre/post migration; its acks land under the registered
  namespace; no other lane touched.
- **STEP-06 — Validation closeout.** Full suite + `--prove-rebuildability`
  over `availability` and `derived_retrieval`; confirm the diff adds no
  behavior to lake-core modules; record closeout evidence in the lane.
  Explicit non-claims: no readiness, no full-GT, no gate ratification, no
  metrics-family selection.

## Review Timing Advisory

- adversarial_review: `recommended`
- highest_value_checkpoint: `after_STEP-02`
- review_target: the authored consumption-seam contract + metrics policy
  artifact
- why_this_checkpoint: a defect in the cross-lane contract (ack grammar
  misuse, queue-as-truth leakage, posture-invariant weakening) would
  propagate into the helper, the conformance suite, the builder, and every
  lane migration; post-implementation review is too late for it.
- boundary: Advisory routing only; not review, approval, validation,
  acceptance, or readiness.

## Validation Expectations

| Type | Step | Risk covered | Evidence / failure meaning |
| --- | --- | --- | --- |
| Scoping (done this lane) | route | Route claims match current contracts | Six packet ledger pointers + both unread contracts reread 2026-07-02; REUSE. Failure would have meant STALE_REREAD_REQUIRED. |
| Implementation | STEP-03 | Ack overwrite / append-only breach | Write-boundary test: existing-ack overwrite hard-fails. Failure = boundary regression; stop. |
| Implementation | STEP-03/05 | Divergent per-lane pickup semantics | Conformance suite green for helper and proving lane. Failure = contract ambiguity; return to STEP-02. |
| Implementation | STEP-04/06 | Non-rebuildable or authoritative view | `--prove-rebuildability` green. Failure = the entry is not an index; remove or fix, never promote. |
| Implementation | STEP-05 | Migration changes lane output | Pre/post record equivalence. Failure = helper semantics wrong; stop before other lanes. |
| Intentionally not run | STEP-04 | `by_creator` build | Deferred until audience-silver lake wiring (Slice C) lands. |
| Intentionally not run | policy | SQL query-lens | Stays scan/query-latency-gated per derived-layout contract. |

## Stop Conditions

Any of these blocks continuing (blocker, not a design choice):

- a step needs a lake-core primitive edit, private path, or layout inference;
- queue/scheduler/event-bus semantics would become pickup truth;
- backend/engine selection pressure;
- Gate ADR territory (AR body layout, retention/erasure) would be touched;
- `by_creator` build attempted before Slice C wiring exists;
- a metric view would be built for a family the owner has not named.

## Route Status

`route_status: ROUTE_COMPLETE`

## Implementation Start Readiness

`implementation_start_readiness: BLOCKED_BY_AUTHORIZATION` — the packet and
this route both bind implementation to a later explicit bounded owner
authorization; owner acceptance of this route is also pending.

## Current Turn Authorization

`current_turn_authorization: read_only_scoping_only` (route production).
Landing this artifact is the scoping lane's authorized docs-write
deliverable, not seam implementation.

## Blockers / Warnings

- Metric families `operator_to_fill` (owner input; STEP-04 metric slice stays
  parameterized).
- Gate 1 ADR is `GATE1_ADR_AUTHORED_AWAITING_RATIFICATION_V0`; the seam stays
  gate-independent because the public-surface rule is already bound by the AR
  contract (acceptance check 8), but if ratification modifies output 4 this
  route goes stale.
- `by_creator` view build has an unmet precondition (Slice C wiring).

## Next Authorized Step

Owner acceptance of this route; then authorize a separate bounded
implementation lane starting at STEP-01. Metric-family naming may arrive with
that authorization or later without invalidating STEP-01..STEP-03.

Recommended Implementation Model: judgment_lane — cross-lane contract design,
compounding correctness risk.

## Non-Claims

Not implementation, implementation authorization, validation, readiness,
acceptance, backend/engine/queue selection, builder authorization, gate
ratification, metric-family selection, or a Bronze full-GT claim.
