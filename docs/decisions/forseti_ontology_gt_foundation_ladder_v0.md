# Ontology Foundation — God-Tier Ladder v0

```yaml
retrieval_header_version: 1
artifact_role: Decision + roadmap record (owner-accepted direction — God Tier ontology foundation via a trigger-gated ladder; Mini God Tier / Smallest Complete Intervention governs sequencing)
scope: >
  Records God Tier as the accepted long-term target for the ontology foundation,
  and the trigger-gated ladder of infrastructure rungs (R0–R7) — each with a
  build-trigger, rough cost, and status — so GT is climbed incrementally as real
  need pulls each rung, never big-bang-built ahead of business validation. A
  living tracker: rung status is updated (dated) as triggers fire and rungs are
  built.
use_when:
  - Deciding whether to build a specific ontology-infrastructure capability now.
  - Checking a rung's build-trigger, rough cost, or current status.
  - Sequencing ontology-foundation work against the MGT / GT discipline.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/foundation/ontology/forseti_ontology_backbone_architecture_v0.md
  - forseti/product/spines/foundation/ontology/ontology.yaml
  - forseti/product/spines/foundation/ontology/ontology_expansion_backlog_v0.json
  - docs/decisions/orca_mini_god_tier_doctrine_v0.md
stale_if:
  - The owner amends the GT direction or the ladder.
  - A rung's build-trigger fires or a rung is built (update its status, dated).
  - The ontology backbone architecture is superseded.
```

## Status

Owner-accepted direction (2026-07-05, in-thread): **God Tier is the long-term
target for the ontology foundation, pursued via a trigger-gated ladder** under
Mini God Tier / Smallest Complete Intervention discipline — each rung is built
only when its named trigger fires, never big-bang ahead of business validation.

This is a direction + living roadmap, **not a build authorization**: each rung
keeps its own authorization boundary, and no rung is built by this record's
existence.

## Why laddered, not big-bang (the reconciliation)

GT is the right destination; the danger is building it now, all at once, before
the business is proven. Six failure modes make big-bang GT the wrong move today:

1. **Opportunity cost** — months of infrastructure while the willingness-to-pay
   / business thesis is still unvalidated (Phase 0). The cathedral with no
   congregation.
2. **Lock-in** — hardening a model still being learned (empty dupe graph,
   unmodeled identity, fragrance-only but beauty-aimed); GT converts
   cheap-to-change YAML into expensive migrations.
3. **Rot / false confidence** — a half-maintained GT graph looks authoritative
   while going silently wrong, poisoning the de-correlated demand reasoning that
   is the product's core value.
4. **Plumbing, not moat** — a graph store / resolver / query engine is
   replicable commodity engineering; the moat is judgment + longitudinal capture
   + outcome memory, which needs that time instead.
5. **Silent correctness bugs** — identity clustering especially (false-merge /
   false-split) fails silently and corrupts the independence signal.
6. **No stopping line** — "GT-completeness" has no natural stop; the ladder's
   triggers *are* the stop.

Therefore: climb by trigger. **MGT here = GT's value captured incrementally,
without standing infrastructure until a real need pulls it.**

## Current foundation state (adjudicated 2026-07-05)

**Near-GT as a governed naming backbone; early as a production knowledge graph.**
From an external four-axis eval (cross-vendor, home-adjudicated; concrete
findings verified against source, capped at `product_learning`): strong on
maintainable design + traceability discipline; **early** on retrievable (only 3
ontology↔runtime bindings — a well-named document set, not a queryable graph) and
scalable (empty dupe graph, no cross-platform identity model, hand-curated data).
Verified defects feeding R0: `action_ceiling` SSOT drift (backbone vs
`ontology.yaml`), cap 15-vs-18, `review_by` present on only 1 of 8 cards, tier
`tie_break_order` vocabulary drift.

## The ladder

Discipline: **build a rung only when its build-trigger fires. "GT-completeness"
is never itself a trigger.** Update Status (dated) when a rung is built or its
trigger fires.

| Rung | What it is | Build-trigger (when to add) | Rough cost | Status |
| --- | --- | --- | --- | --- |
| **R0** | Defect fixes: align `action_ceiling` SSOT, reconcile cap 15/18, add `review_by` to cards, fix tier `tie_break_order` vocab | **NOW** — self-contradictions in the SSOT; cheap | hours | **done 2026-07-05** — `action_ceiling` aligned, tier vocab canonicalized, `review_by` added to all cards; cap 15/18 = verified non-issue (historical changelog, not live drift) |
| **R1** | Minimal identity mapping: assisted, human-checked same-actor mapping for the current ~200 creators (NOT the ML pipeline) | **NOW** — the 192-creator ingestion will double-count multi-platform creators | low (spreadsheet-scale) | not started |
| **R2** | Canonical dupe edge table: one authoritative dupe→original store; product-level `dupe_of` becomes a derived view | when the first citable dupe edges land (clone-house additions adopted + sourced) | low–med | not triggered (dupe graph empty) |
| **R3** | ID registry / resolver: canonical ID lookup + aliases / deprecations / redirects | when hand-lookup / alias collisions actually hurt (renamed channels; alias clashes ingestion can't resolve by eye; >~few-hundred entities) | med | not triggered |
| **R4** | Materialized node/edge/fact tables + query surface: prose relationships → query-able rows | when a real query can't be answered by reading cards (a sprint / demand-read needs cross-entity queries at scale) | med–high | not triggered |
| **R5** | Structured provenance + derived-fact lineage: per-fact assertion objects, source registry, transform lineage for LLM-extracted facts | when LLM / derived extraction actually scales (deep-layer capture + derived claims shipping to surfaces) | med–high | not triggered (partially designed — derived-claim provenance contract exists) |
| **R6** | Automated ingestion / review queues + card generation from a registry | when hand-curation actually breaks (manual YAML can't keep up with regular inflow of hundreds of creators / thousands of products) | high | not triggered |
| **R7** | Automated identity clustering (ML / heuristic) — the GT version of R1 | when manual identity mapping can't keep up (scale beyond ~low-thousands, or continuous inflow) | high; correctness-critical | not triggered |

## Accepted residuals (Mini God Tier discipline)

Consciously **not** building now: R3–R7 (and R2 until sourced edges exist).
- **Why acceptable:** the business is unvalidated (Phase 0); at current scale
  (~30 entities, ~200 creators) editable YAML + minimal identity mapping capture
  ~all the decision value at near-zero infrastructure cost; each foregone rung is
  the replicable-plumbing layer, not the moat.
- **Remaining risk:** a sudden scale / pull event (many buyers, fast roster
  growth) would hit the un-built rungs' pain later, on a compressed timeline.
- **Upgrade trigger:** each rung's build-trigger above. When one fires, build
  that rung (smallest-complete) and update its Status here, dated.

## Non-claims

- Not validation, readiness, buyer proof, or a build authorization; each rung
  keeps its own authorization boundary.
- Records an owner direction + roadmap; asserts no rung is built and mints no
  runtime / graph readiness.
- The current-state read is an adjudicated external eval capped at
  `product_learning`; not a proof of GT or of any rung.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Adds an owner-accepted direction + living roadmap: God Tier is the long-term
    target for the ontology foundation, pursued via a trigger-gated ladder
    (R0–R7) under Mini God Tier / Smallest Complete Intervention — each rung
    built only when its named trigger fires, never big-bang. Applies the MGT
    doctrine to the ontology foundation; mints no new vocabulary and changes no
    existing controlling source.
  trigger: architecture_doctrine
  related_triggers: []
  controlling_sources_updated:
    - docs/decisions/forseti_ontology_gt_foundation_ladder_v0.md   # this record (new)
  downstream_surfaces_checked:
    - forseti/product/spines/foundation/ontology/forseti_ontology_backbone_architecture_v0.md   # the ladder governs the infra roadmap over the backbone's object model; no backbone change
    - forseti/product/spines/foundation/ontology/ontology_expansion_backlog_v0.json           # sibling deferred-TYPE tracker; this ladder tracks infra RUNGS, not types; no overlap edited
    - docs/decisions/orca_mini_god_tier_doctrine_v0.md                                          # MGT lens applied here; not amended
  intentionally_not_updated:
    - path: forseti/product/spines/foundation/ontology/ontology.yaml
      reason: >
        R0 names the action_ceiling SSOT drift as a fix to make; the fix itself
        is a separate authorized edit pass, not performed by this roadmap record.
  non_claims:
    - not validation
    - not readiness
    - not buyer proof
    - not a build authorization for any rung
    - not a fix of the named defects (R0 is a planned rung, not executed here)
```
