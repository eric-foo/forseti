# Evidence Condensation Hierarchy — Deferred Direction v0

```yaml
retrieval_header_version: 1
artifact_role: Research artifact (deferred design direction)
scope: >
  Owner-requested durable record of the hierarchical mini-judgment
  (condensation) design for scaling evidence volume into Judgment, preserved
  for a future capability upgrade; deliberately not commissioned now.
use_when:
  - Evidence volume outgrows single-prompt judgment (a subject's corpus exceeds enumerate-and-read).
  - The owner asks to "improve / go to GT" on judgment scaling, or commissions the hierarchy architecture.
  - Designing the pull-to-assemble loop and needing the agreed downstream shape it must feed.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/packing_judgment_scaling_owner_agreement_register_v0.md
  - forseti-harness/judgment/creator_audience.py
  - docs/research/packing-phase/README.md
stale_if:
  - A commissioned judgment-scaling architecture artifact supersedes this note.
  - The claim compiler, alias/manifest machinery, or Packing boundary changes materially.
  - The owner reverses the condensation direction.
```

## Status

```yaml
status: DEFERRED_DIRECTION
commissioned: no
implementation_authorized: no
validation_or_readiness_claim: not_proven
recorded_because: >
  Owner direction 2026-07-21: "i dont think we need that machinery now, but in
  future for sure write it down somewhere that when we want to improve / go to
  GT etc it would be there present."
```

This note preserves an owner-agreed *direction* and its design reasoning. It
authorizes nothing. A future lane picks it up by commissioning a real
architecture artifact against then-current source.

## Pickup Triggers

Any of these justifies commissioning the architecture:

- A subject's evidence corpus can no longer be judged by enumerate-and-read
  into one prompt (cost, context limits, or observed mid-context accuracy loss).
- Judgment quality on large bundles degrades in ways consistent with
  "lost in the middle" (evidence buried mid-context gets ignored).
- The owner requests the capability upgrade explicitly.

## The Stack (agreed shape)

```text
capture -> cleaning -> pull-to-assemble (Judgment-side agent enumerates/queries
the lake, gathers a working set, logs its retrieval trail)
-> freeze (assembly side stamps the working set: bundle id + hash)
-> Level 0: per-partition mini-judgment rounds (descriptive claims, line-cited)
-> Level 1: topic/axis rounds over promoted claims (optional at moderate scale)
-> Level 2: final judgment over judged_claim rows
-> compile: aliases expand transitively to durable IDs
-> audit descent (the fourth surface): any final claim unwinds to raw lines on demand
```

Packing packs the model-facing view at *every* level and never selects;
Judgment owns every meaning-bearing act including condensation.

## Condensation Mechanics (how, concretely)

Condensation is a mini-judgment round, not a separate summarizer:

1. **Partition** — per video / per capture unit at Level 0 (the lake's
   structure provides this for free); cluster by topic/axis only at Level 1.
2. **Run the existing machinery with a descriptive method deck** — extract
   recurring, decision-relevant observations; every claim cites its exact
   supporting lines; report spread ("14 comments across 3 months"); flag
   within-partition contradictions; do NOT judge hire-worthiness.
3. **Compile and validate with the existing claim compiler** — citation
   closure, representative-within-support, banned-language guards; claims get
   durable claim IDs with member evidence IDs expanded.
4. **Promote** each compiled claim to next-level evidence:
   `{evidence_id: <claim_id>, kind: judged_claim, text: <statement>}`, aliased
   like any evidence row.
5. **Compression knob = claim cap per round** (roughly 5-15), bounding fan-in
   at the next level regardless of partition size. Dropped material is the
   accepted lossy cost; lineage keeps it auditable.
6. **Cross-partition aggregation adds new signal** — near-identical claims
   group across partitions and multiplicity becomes evidence ("recurs in 40 of
   300 videos"), a claim no single round could make.

## Invariants To Preserve (owner-agreed)

- Citation capability survives every level exactly; no whole-transcript or
  whole-partition aliases, ever.
- One citation system: mini-rounds emit the existing claim shape; no parallel
  scheme.
- Derived claims are labeled (`judged_claim` or successor kind); second-hand
  evidence is never disguised as observed evidence.
- Lineage expansion is transitive: final claim -> intermediate claims -> raw
  lines.
- A cross-partition contradiction surface is mandatory (same-axis,
  opposite-polarity claims from different partitions must be paired and put in
  front of the final round).
- Audit provenance stays out of model-visible views; one lookup away via
  manifests; support topology stays model-visible.
- Nowcasting mode is "recorded, not blind" (frozen judged set + retrieval
  log); blindness constraints apply only to backtests.
- Packer determinism (same input -> same bytes) at every level.

## Known Risks (accepted or mitigated by design)

- **Partition blindness** — contradictions spanning partitions are invisible
  to both; the contradiction pass exists for this. Biggest real risk.
- **Confirmation-seeking retrieval** (pull-loop risk, not a mechanism):
  mitigate with the retrieval log as provenance plus coverage obligations in
  the pull method (enumerate the full window before narrowing; at least one
  disconfirming query per emerging theme).
- **Lossy by construction** — what a round drops is gone for the final judge;
  accepted because lineage keeps it auditable and raw dumps lose accuracy to
  mid-context degradation anyway.

## Prior Art (corroboration; the design is owner-original)

- **GraphRAG** (Microsoft Research, 2024) — entity graph, community
  detection, per-community LLM summaries with provenance, query-time
  map-reduce. Same architecture class; validates the pattern at ~1M-token
  corpora. Our contradiction pass is the GraphRAG-flavored move (cross-partition
  relationships).
- **RAPTOR** (Stanford, 2024) — recursive embed-cluster-summarize tree;
  retrieval at any level. Validates level-appropriate reading; our Level 1
  topic clustering is the RAPTOR-flavored move.
- **"Lost in the Middle"** (Liu et al., 2023) — mid-context evidence is
  measurably under-used even when it fits; condensation protects accuracy, not
  just cost.
- This design is stricter than both papers in one respect: intermediate nodes
  are mechanically validated, citation-closed claims, not free-form summaries.

## Decided At Commissioning Time (deliberately open now)

- Partition scheme beyond per-video Level 0; when Level 1 activates.
- `judged_claim` schema/version and its capability-manifest treatment.
- Claim cap values; dedupe/grouping rules across partitions.
- Contradiction-pass mechanics (pairing heuristics, surfacing format).
- Round orchestration and failure behavior; retrieval-log provenance format.
- SQL-index integration (owner is standing up a SQL index over the lake as a
  parallel effort; the pull loop may assume address-based enumeration now and
  SQL lookup later).
- Validation design for the whole ladder.

## Non-Claims

- Nothing here is implemented, validated, ready, accepted architecture, or an
  implementation grant.
- Prior-art citations corroborate the pattern; they do not import those
  systems' designs as requirements.
