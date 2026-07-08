# ChatGPT Pro Prompt - Orca Data-Lake Architecture Pass v0

You are doing a read-only architecture-planning pass for Orca's **whole data lake**, not an IG-only lane.

The attached source pack contains selected current-main Orca documents and code. Treat those sources as the evidence base for this pass. Do not assume any unstated repo context, prior chat context, or external product policy.

## Goal

Recommend the architecture shape for Orca's general capture data lake:

- how source captures land durably;
- how they become queryable;
- how ECR-derived records pick them up;
- how Projection and Cleaning consume them;
- how tenant/source-family-specific payloads fit without turning one tenant's schema into the whole lake schema.

The output should let the owner decide the **lake + derivation + sequencing shape** without re-deriving it.

## Critical Correction To Attack

A prior pass leaned on an IG example. That is not enough.

Do **not** promote the IG `MetricObservation` shape into the universal lake schema. IG typed metrics are a tenant/source-family contract. The lake-wide core should be more general: packet identity, provenance, preservation, timing, slice identity, version pins, rebuild rules, and derivation boundaries.

IG is only one tenant/stress case. Also use the included Reddit/thread, Retail PDP, demand-durability/time-series, ECR, Projection, Signal Content, and Cleaning sources.

## Method

1. Read this prompt.
2. Source-load the included files. Do not produce a recommendation before source readiness.
3. Declare either `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
4. Then produce architecture planning. Treat all proposed docs as proposed unless the source itself states stronger status.

## Decision To Make

Choose and justify the general shape:

- **Lake truth:** what is immutable and durable?
- **Tenant contracts:** what is source-family/tenant-specific?
- **Queryable projections:** what should be materialized, and what must remain rebuildable?
- **Capture -> ECR pickup:** is this a mutable sync pipeline, an event/scan derivation pass, or something else?
- **Projection/Cleaning sequencing:** does Cleaning consume raw packets, ECR outputs, projection rows, or a raw-keyed input handle with optional sibling refs?
- **Dedup/time-series placement:** where do exact dedupe, near-match grouping, cumulative-at-capture metrics, and cross-run series logic belong?
- **Versioning:** what version pins are required so rebuilds are honest?

## Candidate To Attack

Candidate recommendation:

```text
Immutable SourceCapturePacket log is truth.
Tenant/source-family typed payloads are specific contracts over that packet/slice substrate.
Queryable projections are rebuildable caches, not second sources of truth.
ECR, Signal Content, Projection, Cleaning, and later Judgment are sibling derivations keyed back to packet/slice/raw handles.
Capture-to-ECR "sync" should be an idempotent derivation over packet IDs or batches, not mutable store-to-store state.
Cleaning should consume one raw-keyed input handle that may attach projection and ECR references when present.
```

Attack this. Confirm it, weaken it, or replace it. Do not preserve it just because it is supplied.

## Criteria

Use these criteria:

- invariant conformance: reference-never-merge, re-derive-not-migrate, carry-or-residualize, no second source of truth;
- rebuildability: can projections/ECR/Cleaning be rebuilt from durable inputs without migrations?
- tenant neutrality: does the lake core avoid becoming IG/Retail/Reddit-specific?
- query usefulness: does the shape support real reads without making caches authoritative?
- correctness and observability of pickup/sync: can new packets be detected, derived, retried, and audited?
- source-family evolution: can new tenants add payload contracts without breaking the core lake?
- version honesty: are metric registries, projection rules, identity/conflict policies, and deriver versions pinned where needed?
- downstream sequencing: does Cleaning get the inputs it needs without depending on a fragile total order?
- lock-in: what decisions are one-way doors versus rebuildable/deferred choices?

## Output Contract

Return:

1. **Recommended architecture** in plain but precise terms.
2. **Option comparison**: at least compare stateful pipeline vs immutable log + derivation DAG vs immutable log + materialized projection cache.
3. **Layer contract**: lake core, tenant contracts, projection, ECR, Signal Content, Cleaning, Judgment boundary.
4. **Sequencing answer**: what runs first, what can run in parallel, what depends on what.
5. **Versioning/rebuild input set**: what must be pinned and where.
6. **Failure modes**: the strongest reasons this recommendation could be wrong.
7. **Verified vs assumed** against the supplied sources.
8. **Smallest next decision or artifact** the owner should commission if adopting the shape.

## Boundaries

- Read-only architecture planning only.
- Do not build, implement, patch code, write schema, or design a runner.
- Do not unfreeze Judgment or claim readiness/validation.
- Do not claim owner adoption unless a supplied source proves it.
- Do not make a generic data warehouse recommendation from outside best practices alone. This pass is about fitting Orca's actual source hierarchy and doctrine.

## Source Pack

Use `SOURCE_MANIFEST.md` for the included file list and source role notes.

