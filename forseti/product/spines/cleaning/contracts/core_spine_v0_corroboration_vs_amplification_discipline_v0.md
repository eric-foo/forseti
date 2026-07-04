# Core Spine v0 — Corroboration vs Amplification Discipline (Cleaning ↔ Judgment)

```yaml
retrieval_header_version: 1
artifact_role: Product architecture design note
scope: Layer placement and discipline for distinguishing independent corroboration from artificial amplification, and the non-destructive dedup requirement that makes it possible, across the Cleaning and Judgment spines.
use_when:
  - Building the Cleaning Spine (dedupe/clustering mechanics) or Judgment Spine Signal Integrity.
  - Deciding how dedupe/clustering versus independence/amplification judgments are split across layers.
  - Defining Evidence Candidate Record / Evidence Unit fields that must preserve independence and source identity.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
  - forseti/product/spines/foundation/product_contract/core_spine_v0_product_contract.md
```

- Status: PROPOSED (design note)
- Artifact type: Product-method design note
- Implementation authorized: no
- Source basis: `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md` (PROPOSED_FREEZE), `docs/product/core_spine_v0_product_contract.md` (Signal Integrity primitive), owner direction 2026-05-28.

## Why This Exists

Adequate capture volume matters because individually-weak public signals can become
fit evidence *in aggregate*: **independent corroboration** — many genuinely independent
voices converging — raises what the evidence can validly support. But **artificial
amplification** (botting, coordinated campaigns, copied/echoed language, vendor-managed
astroturf) imitates corroboration while carrying no independent weight.

Distinguishing genuine corroboration from artificial amplification is a central part of
Orca's wedge and is to be held as a **core competency**. It is also genuinely hard:
there is no simple rule for "naive versus proper" dedup, so this is a *judgment
competency to be sharpened over cases*, not a fixed threshold.

## The Trap

Naive or destructive dedup destroys the very repetition that creates aggregate signal.
If duplicates are collapsed or discarded *before* independence is assessed, both the
corroboration signal and the amplification tell are lost. **Dedup must be
non-destructive and must preserve source identity, independence, and count.**

## Layer Placement (do not collapse the split)

This discrimination spans layers with a clean split. Authority: the data/cleaning
boundary note's Layer Rules and Inclusion State Rule, and the Core Spine contract's
Signal Integrity primitive.

- **Capture = recall.** Gather enough that real patterns can form; preserve source
  identity, provenance, timing, and visibility. Volume serves recall and corroboration
  potential — it is never, by itself, evidence validity.
- **Cleaning Spine = non-destructive mechanics.** Owns dedupe/clustering *mechanics*,
  normalization, and raw→cleaned traceability. It MUST preserve independence,
  source-identity, and cluster structure. It MUST NOT decide credibility,
  independence-effect, exclusion, or decision strength. Per the boundary note: *once
  dedupe/clustering affects independence, credibility, uncertainty, exclusion, Decision
  Strength, or Action Ceiling, the effect belongs to the Judgment Spine.*
- **Judgment Spine (Signal Integrity) = the discrimination.** Owns the actual call: is
  clustered repetition **independent corroboration** (can support demand/strength) or
  **artificial amplification / echo / botting / copied language** (downgraded or
  excluded)? This is where the wedge competency lives.

Consequence for the make-or-break ranking (capture > cleaning > judgment, by
risk/fragility): the *differentiator* competency sits in the Judgment Spine's Signal
Integrity, even though the harness plumbing is controllable. "Judgment = OP but not
make-or-break" holds for the plumbing; the Signal-Integrity discrimination inside it is
the wedge and must stay rigorous.

## Build Implications

- Preserve provenance + independence markers **end-to-end** (capture → cleaning →
  judgment), because the discrimination happens at Judgment. If any upstream layer
  flattens source identity, cluster structure, or copied-language signal, the
  discrimination becomes impossible downstream — and that discrimination is the product.
- The Evidence Candidate Record / Evidence Unit (EvidenceUnit) contract must carry enough
  independence / source-identity / cluster / timing signal for Signal Integrity to weigh
  corroboration against amplification.
- Cleaning's dedupe/clustering is non-destructive and traceable by design; it surfaces
  structure, it does not adjudicate credibility.
- Treat the corroboration-vs-amplification call as a sharpenable judgment competency
  (e.g., consultant-loop / case backlog), not a solved rule.
- Engagement context is one of the mechanical inputs that makes this judgment
  inspectable. Cleaning may preserve high/low reaction metrics, source order,
  reply depth, repetition, and disagreement structure, but only as context for
  Judgment to inspect. High source-visible engagement should be carried forward
  as possible resonance weight with its direction, visible audience fit, baseline
  context, and discount reasons, but Cleaning must not decide the final
  resonance weight, whether high engagement equals independent corroboration, or
  whether low engagement makes the signal useless.

## Non-Claims

Advisory product-method design note. Does not claim Cleaning Spine or Judgment Spine
validation, readiness, buyer validation, or that the discrimination is solved. Does not
authorize implementation, runtime, schemas, scrapers, automation, scoring engines, or
feature planning.
```
