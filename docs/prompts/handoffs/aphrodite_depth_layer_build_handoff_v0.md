# Aphrodite Depth-Layer Build — Cold Handoff v0

```yaml
retrieval_header_version: 1
artifact_role: Implementation handoff packet (planning artifact — NOT a build authorization)
scope: >
  Cold cross-lane handoff for the Aphrodite depth-now moat build: the
  niche-complete fragrance roster, the fragrance ontology, and the
  entity-resolved, receipt-stamped content layer over transcripts and page-1
  comments that feed the five Vetting Sprint evidence panels. Packages the work
  unit, its controlling context, its gates, and the recommended first bounded
  slice for a future authorized build lane. Executing it requires explicit
  owner build-authorization plus implementation scoping; this packet grants
  neither.
use_when:
  - A future lane is authorized to build the Aphrodite depth layer and needs the full context cold.
  - Checking what is gated, what substrate already exists, and what the recommended first slice is.
authority_boundary: retrieval_only
stale_if:
  - The charter or either pre-build gate artifact is amended or superseded.
  - Owner build-authorization is granted (replace this packet's OPEN gate status).
  - The capture substrate this packet points at is materially restructured.
```

## What this is — and is NOT

This is a **cold handoff packet**: a future build lane, with none of this
thread's context, should be able to pick up the Aphrodite depth-layer build
from this document plus the sources it names. It is a **planning artifact**. It
does **not** authorize the build, capture, a runner, a model choice, or any
source edit. Executing it requires (a) explicit owner build-authorization and
(b) implementation scoping — both OPEN (see Gates).

## Goal handoff (front-loaded)

```yaml
goal_handoff:
  anchor_goal: >
    Cash the Aphrodite "depth-now" moat layer: turn already-capturable creator
    content (transcripts, page-1 comments) into entity-resolved, receipt-stamped
    derived claims that make the Vetting Sprint report decision-grade — fit,
    ad-reception, purchase-intent, brand-adjacency, momentum — for the niche
    fragrance roster.
  success_signal: >
    A single-creator end-to-end depth rehearsal produces a decision-grade fit
    panel AND an ad-reception panel, each carrying complete derivation
    provenance, that survives honest grading; and the ways it falls short size
    the remaining build (the "practice dinner" for the depth layer).
```

## Read first (controlling context, in order)

1. `forseti/product/spines/creator_signal/aphrodite_carveout_charter_v0.md` —
   owner-ratified direction; Sections 3 (two-layer moat), 4 (five panels), 6
   (stratified capture policy), 7 (pre-build gates), 9 (accepted residuals).
2. `forseti/product/spines/creator_signal/aphrodite_derived_claim_provenance_contract_v0.md`
   — **binds all derived output**; the extractor must emit its fields.
3. `forseti/product/spines/creator_signal/aphrodite_depth_capture_tos_risk_sanity_check_v0.md`
   — capture is inside the accepted boundary; carries FLAG 1 (commercial
   use/data rights, Phase-1 owner+legal) and FLAG 2 (materiality reacquisition).
4. `forseti/product/spines/creator_signal/creator_signal_product_architecture_v0.md`
   — the Signal claim layer and the KEEP/BUILD/DEFER frame the depth layer sits in.
5. `docs/decisions/orca_creator_signal_spine_promotion_binding_v0.md` — the
   Capture ↔ Creator Signal ownership boundary the build must respect.

## The work unit

Build the depth-now moat layer = three coupled pieces:

- **(a) Niche-complete fragrance roster** — the admission-judged set of creators
  that *matter* in fragrance. Completeness is what makes any read trustworthy
  (charter Section 3). The monitoring-policy allocator already models a roster
  (IG target 1,000, gated 250→500→1,000) — reuse, don't reinvent.
- **(b) Fragrance ontology** — houses, products, notes, accords,
  dupe-relationships, and scene vocabulary; the entity graph transcripts and
  comments resolve against. This is the accumulated craft a horizontal player
  won't build per-vertical.
- **(c) Entity-resolved, receipt-stamped content layer** — over stratified
  transcripts + page-1 comments, producing the derived claims that feed the
  five panels, every claim carrying provenance per the contract (item 2).

## Gates (must all be clear before source edits)

| Gate | Status | Note |
| --- | --- | --- |
| ToS-risk sanity check (charter gate 2) | **CLEAR** | Foundation-stage capture inside accepted boundary; see the sanity-check artifact. FLAG 1/FLAG 2 carried. |
| Derived-claim provenance contract (charter gate 1) | **CLEAR (exists)** | The build must bind to it; operational satisfaction checked at build. |
| Explicit owner build-authorization | **OPEN — the hard gate** | Charter authorizes no build; runtime/capture work needs bounded owner authorization in the turn (AGENTS.md). |
| Implementation scoping | **OPEN** | After authorization, route through `workflow-implementation-scoping` before edits. |
| Foundation exit gate definition (charter D-1) | **OPEN (parked)** | Not blocking the *rehearsal*; blocks the Vetting-v0 productization. Recommended: practice-run gate. |

## Recommended first bounded slice (Mini God Tier — do NOT build it all up front)

**A single-creator end-to-end depth rehearsal.** Take one creator already in
the registry, hand-build the minimal ontology slice their content needs,
produce one fit panel + one ad-reception panel with complete derivation
provenance, and grade honestly. Rationale: it exercises the whole pipeline
(roster → ontology → extraction → provenance → panel) on one subject, produces
the evidence to size the real roster/ontology build, and its failure modes are
the shopping list — the depth-layer analog of the charter's "practice-run"
foundation gate. Explicitly **not** a full roster completion or full ontology
build as the first move; those are demand-/evidence-pulled after the rehearsal.

## Substrate that already exists (reuse, do not rebuild)

- YouTube transcript extraction runner — landed
  [PR #640](https://github.com/eric-foo/orca/pull/640).
- Creator monitoring-policy allocator (roster/tier/cadence) —
  `orca_creator_monitoring_policy_architecture_v0.md`.
- Source-access tooling first tranche (capture packet, direct HTTP, archive,
  honest browser) — authorized per the source-access method plan.
- IG capture runners and the creator registry / current-view spine.

## Hard boundaries (carry into the build)

- The charter forbidden set + the derived-claim provenance contract bind all
  output; no unstamped derived claim, no person-level/demographic inference, no
  vanity score, no zero-fill.
- Carve-out conformance: bounded, self-terminating, pre-authorized capture
  sessions; account caps (≤10, start ≤5); **no standing crawler**.
- Capture ↔ Creator Signal boundary: the extractor/recipe/storage are
  capture/computation-lane; Creator Signal owns the display/claim rule only.
- FLAG 1 (commercial use / data rights) is an owner+legal gate at Phase-1 sell
  time; the build does not resolve it and must not assume it.

## Open decisions the build lane must route to the owner

- Foundation exit-gate definition (charter D-1; recommended practice-run gate).
- Ontology scope/depth for v0 (how much of the fragrance graph the rehearsal needs).
- Roster target and gating for the build (monitoring policy's 1,000 is a reference, not a commitment).

## Preflight / boundary receipt

```yaml
output_mode: file-write (this planning packet only)
template_kind: handoff
edit_permission: none for the build — this packet grants no source-changing authority
receiving_lane_first_move: obtain owner build-authorization, then workflow-implementation-scoping
doctrine_change: none (planning handoff; the build's own DCP fires when it lands)
non_claims: [not build authorization, not capture authorization, not validation, not readiness, not commercial-use/data-rights clearance]
```
