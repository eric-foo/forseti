# ChatGPT Pro Decision-Input Prompt — First Metric Families For The Data Lake Consumption Seam (v0)

```yaml
retrieval_header_version: 1
artifact_role: Product planning prompt draft
scope: >
  Owner-couriered decision-input prompt for an external ChatGPT-family lane: rank and
  recommend the first metric families Orca must be able to produce on demand from committed
  lake evidence, optimizing for buyer value / needle-moving / demo-impressiveness under the
  lake's honesty constraints. The answer feeds the operator_to_fill metric-families slot in
  core_spine_v0_data_lake_consumption_seam_contract_v0.md via owner adjudication.
use_when:
  - Dispatching the owner-commissioned metric-family recommendation to ChatGPT Pro.
  - Adjudicating the returned ranking before naming metric families in the seam contract.
authority_boundary: retrieval_only
output_mode: paste-ready-chat (body below); return = chat transcript, decision input only
stale_if:
  - The owner names the first metric families (the slot this prompt exists to fill).
  - The Silver Vault metric posture rules or the on-demand-first policy change.
```

## Preflight (Orca Prompt Preflight core)

- Output mode: `paste-ready-chat`; durable artifact = this file; receiver returns chat only.
- Template kind: none bound (decision-input research/judgment prompt; not a review; no
  adversarial token required). Registry research templates are model-postured for other
  lanes; this is a fresh cross-lane prompt authored through `workflow-prompt-orchestrator`.
- Edit permission: receiver none; this artifact docs-write on `claude/elated-cannon-a6e2cf`.
- Reviews: not a review prompt; findings/verdict vocabulary not used; no runtime-model
  recommendation — ChatGPT Pro is the OWNER'S chosen dispatch target, recorded as fact.
- Doctrine change: none (fills an operator_to_fill slot by owner adjudication; the seam
  contract records the naming when the owner accepts it).
- Destinations: input = this file; the return is couriered back to the home lane; naming
  lands in `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_consumption_seam_contract_v0.md`
  (owner-adjudicated edit, separate turn).

## Paste-ready body

````markdown
You are advising on METRIC SELECTION for a source-backed social-evidence data lake. Your
answer is decision input for the product owner — not a design of storage, schemas, or
engines. Be concrete and opinionated; rank things.

CONTEXT (facts, keep them fixed):
- The product ("Orca") captures public social-media evidence — IG, YouTube, TikTok — and
  turns it into source-backed creator/content intelligence for commercial buyers (beauty /
  fragrance brand side). Every number must trace to committed captured evidence.
- Evidence classes already on hand in the lake (committed, immutable, per-platform):
  1. Per-content and per-creator METRIC OBSERVATIONS (e.g. view counts) with an honesty
     discipline: every observation carries a posture (observed vs missing/hidden/blocked +
     reason) and a coverage window. A metric value of 0 is only ever a real observed zero.
  2. Creator metric ROLLUPS (IG and YouTube watch-data rollups per creator account).
  3. Video TRANSCRIPTS (captions + ASR) for creator content.
  4. PRODUCT MENTIONS extracted from transcripts: brand, product line, stance/sentiment
     vote, confidence, with an exact source pointer into the transcript.
  5. Audience COMMENTS captures for some content.
  6. A reserved "movement threshold crossing" record kind: "a source object crossed a
     declared movement threshold under a declared profile/baseline/window/cohort/threshold"
     (spike/momentum alerts), not yet populated.
- HARD CONSTRAINTS (violating any of these disqualifies a metric family):
  - Metrics are computed ON DEMAND from committed evidence; anything precomputed is only a
    rebuildable cache, never the source of truth.
  - Missing/hidden/blocked evidence must surface as "no evidence + reason", NEVER as a zero
    or a silently-smaller denominator.
  - Per-platform only: no cross-platform person identity unification; object-level metrics
    (creators' public accounts, content objects, brands/lines) — never person dossiers.
  - What was not captured cannot be derived: coverage limits must travel with every metric.

THE QUESTION: Which METRIC FAMILIES should this product commit to producing on demand
FIRST? Optimize for three things simultaneously:
(a) buyer value / needle-moving — changes a brand-side buyer's decision or budget;
(b) impressiveness — the "companies love this" demo effect; metrics that feel like insight,
    not bookkeeping;
(c) producibility TODAY from the evidence classes above, honestly, under the constraints.

DELIVER:
1. A ranked table of 5-8 candidate metric families. For each: name; one-line definition;
   which evidence classes (1-6 above) it derives from; buyer-value score (1-5) with the
   buyer decision it moves; impressiveness score (1-5) with the demo moment it creates;
   producibility score (1-5) with the minimum evidence needed on hand; honesty risk (the
   vanity-metric or fake-zero trap it invites, and how the posture/coverage discipline
   contains it).
2. Your TOP 2 recommendation to lock first, with a paragraph each on why these two compound
   (e.g. one baseline family + one movement/derivative family) and what a buyer-facing
   readout of each looks like in one sentence.
3. The TRAP LIST: 2-3 metric families that LOOK impressive but you would refuse first —
   because they need evidence not on hand, invite cross-platform identity, degrade into
   vanity numbers, or cannot be honest about missing data.
4. Candidates you should evaluate among others (do not limit yourself to these): raw
   view-count/reach families per creator/content; growth/velocity and
   movement-threshold/spike families; share-of-voice by brand/line from product mentions;
   stance/sentiment-weighted mention families; engagement-per-reach ratios; consistency/
   cadence families from rollups.

BOUNDARY: Decision input only. The owner adjudicates and names the families in the owning
contract; you are not selecting storage, schemas, engines, or capture work, and your answer
creates no commitment by itself.
````

## Return handling (operator)

- Courier the full response back into the home lane. The owner (or the home lane under
  owner instruction) adjudicates the ranking and names the first metric families by editing
  the seam contract's `operator_to_fill` slot — a separate, owner-gated edit.
- Non-claims: not validation, readiness, capture authorization, or a product commitment;
  per-platform and posture constraints stay owned by the lake contracts regardless of the
  recommendation.
