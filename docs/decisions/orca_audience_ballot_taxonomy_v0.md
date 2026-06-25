# Orca Audience-Inference Ballot Taxonomy v0

```yaml
retrieval_header_version: 1
artifact_role: owner-adjudicated design-adoption decision record
scope: >
  Adopts the Tier-1 "ballot" taxonomy for creator ideal-audience inference: the
  output-field (bucket) set, a canonical label vocabulary + alias map, and a positive
  4-way router that replaces the leaky demographic denylist. Records the SETTLED answer
  to the Tier-1/Tier-2-A collapse question and the sequencing for taking Tier-2-A
  demographics live. Design adoption only -- not validation, readiness, or product proof.
use_when:
  - Changing the audience-inference bucket set, label vocabulary, or the Tier-1 routing guard.
  - Deciding whether to collapse Tier-1 and Tier-2-A (answered here: no).
  - Sequencing the Tier-2-A (gender/age) demographics slice.
authority_boundary: retrieval_only
open_next:
  - orca-harness/schemas/audience_label_ontology.py
  - orca-harness/schemas/audience_inference_models.py
  - orca-harness/cleaning/audience_extractor.py
  - orca-harness/scoring/audience_fusion.py
  - docs/decisions/wind_caller_calibration_carveout_v0.md
  - docs/prompts/deep-thinking/orca_audience_ballot_bucket_taxonomy_prompt_v0.md
stale_if:
  - The Tier-1/Tier-2-A/Tier-3 boundary or the Tier-2-A carve-out is amended.
  - A SubNiche hierarchy or `use_context` field is adopted (deferred here).
  - The fusion modality-cap / abstention model changes.
```

## Status

`OWNER_ADJUDICATED_DESIGN_LOCK` — adopted in-repo 2026-06-25 after an external
(ChatGPT-Pro, no-repo) reasoning pass on the prompt artifact named above, applied
under Smallest Complete Intervention + mini-god-tier. This is a design-adoption
record, not validation, readiness, calibration, or buyer proof. The owning authority
for the tier boundary remains `docs/decisions/wind_caller_calibration_carveout_v0.md`;
the owning spec remains the IG creator ideal-audience inference spec.

## Problem

The deciding (`scoring/audience_fusion.py`) tallies BY EXACT LABEL. With free-text
labels, synonyms split the vote (`beginner` / `newbie` / `starter` = three answers
that never combine), and the Tier-1/Tier-2-A boundary was guarded by a **denylist**
that leaks on novel phrasings. Both weaken the inference.

## Decision (adopted)

1. **Bucket set = 6 Tier-1 fields.** The existing five (`segment`, `audience_role`,
   `purchase_intent`, `skill_level`, `price_tier`) plus **`aesthetic_vibe`** (content
   style/tone). Aesthetic gets its own field because, folded under `segment`, it
   collides with topical labels in the exact-label tally.
2. **Canonical label vocabulary + alias map** (`schemas/audience_label_ontology.py`).
   The deciding tallies only canonical labels; synonyms are aliased to a canonical key,
   never independent tally keys. Vertical-scoped (fragrance/beauty v0); other verticals
   extend by adding label sets — the engine (buckets, caps, abstention) is unchanged
   and platform-general.
3. **Positive 4-way router replaces the denylist** (`cleaning/audience_extractor.py`,
   after the verbatim-pointer guard):
   - canonical `(field,label)` → tallied `EvidenceRecord` (with the canonical label);
   - demographic (gender/age) → `deferred_signals` (transient Tier-2-A "reminder base", gated);
   - special-category (health/religion/politics/sexuality) → **hard reject** (Tier-3);
   - anything else → `other_candidates` **review telemetry** — never tallied, never a
     persisted profile label; surfaces candidate vocabulary for human admission.
4. **`other_candidate` is an escape, not a tally key.** A label outside the allow-list
   cannot reach a record by default — so a label that is not yet admitted is held for
   review rather than silently splitting or smuggling.

## Settled: do NOT collapse Tier-1 and Tier-2-A

The owner asked whether to collapse the tiers into one "allowed" space. **No.** This is
not a preference — the signed carve-out states *"the Tier-1 slice never votes gender"*
and confines the demographic prior *"to the Tier-2-A slice"* (carve-out, 2026-06-23).
Collapsing would route demographic inference through the Tier-1 exact-label tally with
no sourced base rate, no defeasibility, and no aggregate/transient handling —
contradicting a signed direction-lock and re-opening the demographic-label backdoor
that #368 closed. Tiers are **handling, not permission**: keeping them separate is what
lets a vibe's age-coding be *used* (as Tier-2-A evidence) instead of *leaked* (into Tier-1).

## Deferred (named residuals — mini-god-tier)

- **Schema-level `(field,label)` guard:** canonicalization is enforced at the
  extractor/router boundary (the only `EvidenceRecord` producer), not as a rigid schema
  constraint. Lower lock-in; the schema-level guard stays deferred until a second
  producer appears. *Residual:* a second producer could bypass canonicalization.
- **Alias map + denylist predicates are hand-maintained.** An un-aliased synonym falls
  to `other_candidate` until admitted; the demographic + special-category predicates can
  miss novel phrasings — they are the SECOND line behind the positive allow-list.
- **SubNiche hierarchy + `use_context` field:** deferred until evidence volume justifies
  them. Canonical+alias is the complete minimum now.
- **`aesthetic_vibe` as a possible age proxy:** any audience-age it implies is routed to
  Tier-2-A, never read off the Tier-1 label; the field is sparse and will often abstain early.

## Tier-2-A demographics — sequencing to "live"

The owner wants gender/age live. The **legal gate is already cleared** (carve-out,
council-confirmed 2026-06-23). What remains is **build/data**, and it is its own slice
(not a fold into Tier-1):

1. a roster-ledger **aggregate-audience-attribute schema home** (the ledger currently
   forbids demographic fields);
2. a **sourced, versioned per-category base-rate table** (owner-supplied/approved; a
   general base rate is obtainable to start, refined over time);
3. a **defeasible-prior deciding module** — base rates applied **in code**, *"sourced +
   versioned (not model-gut)"*, that creator-specific content evidence updates and
   overrides, with prior-dominated vs evidence-dominated transparency.

The LLM only *labels* the demographic ballot (already quarantined into `deferred_signals`);
**code does the judging** — that is the anti-bias mechanism. Binding posture on activation
(carve-out): aggregate-only, text-only / no-biometric, legitimate-interests, transient with
no individual-follower retention, no special-category. *Residual:* early output is
prior-dominated until creator evidence accrues; a stale/wrong base rate biases
prior-dominated creators until overridden.

## What this record is not

Not validation, readiness, calibration, or buyer proof. Not Tier-2-A activation (its
build/data gates are open). Not a change to the carve-out or the spec — it adopts a
Tier-1 design within them. The profile always carries `actual_audience = not_estimated`;
this lane is never "gold" (gold = the Judgment layer).
