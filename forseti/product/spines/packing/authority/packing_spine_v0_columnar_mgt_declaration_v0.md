# Packing Spine v0 Columnar MGT Declaration v0

```yaml
retrieval_header_version: 1
artifact_role: Product architecture declaration (capability tier)
scope: >
  Declares the columnar packer v0 (payload-agnostic core + creator-audience
  adapter) Mini God Tier for the bound capability of model-facing serialization
  of an already-selected evidence set, with named accepted residuals; explicitly
  refuses a full God Tier claim.
use_when:
  - Checking what capability tier the current packing implementation may be described as.
  - Deciding whether a residual's upgrade trigger has fired.
  - Planning the next packing capability slice.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/packing/authority/packing_spine_v0_serialization_contract_v0.md
  - docs/decisions/forseti_mini_god_tier_doctrine_v0.md
  - forseti-harness/packing/columnar.py
  - forseti-harness/tests/unit/test_packing_columnar_v0.py
stale_if:
  - Any residual below is closed, reassigned, or its trigger fires.
  - A later owner decision declares full God Tier or supersedes this tier.
  - The serialization contract's boundary or invariants are amended.
```

## Status

`PACKING_COLUMNAR_MGT_DECLARED_V0`.

Owner-invoked 2026-07-21 in-thread ("is this form of packing MGT / GT then?",
ratified with "proceed"). Per the Mini God Tier doctrine this is a capability
*target* record with mandatory accepted residuals — not validation, readiness,
proof, or a measured achievement percentage.

## What The Tier Means (bound capability)

The bound capability is model-facing serialization of an already-selected
evidence set. Within that bound, v0 delivers:

1. A payload-agnostic dense-table core with declared-column validation and
   fail-loud drift errors, reusable by any future view without core changes.
2. Deterministic bytes and an exact deep-equal rehydration contract.
3. Citation capability preserved exactly (aliases untouched; durable IDs and
   audit paths excluded from the packed surface by construction and by test).
4. A proven adapter recipe spanning two platforms through one view schema.
5. A real measured payoff: -49.6% evidence-view bytes on a live-lake 8-video
   bundle rebuild (98,805 B -> 49,840 B; whole prompt ~116 KB -> ~66 KB),
   with the honest small-fixture inversion (+8.3% at one row per table)
   recorded rather than suppressed.

This is the "small version that does most of what god tier does": one module,
no standing infrastructure, reversible.

## Accepted Residuals (mandatory under the MGT doctrine)

| Residual | Why accepted now | Upgrade trigger |
| --- | --- | --- |
| Frozen-form verification declared, not built (canonical bytes + hash stamp + verify-on-read) | Freeze integrity currently rests on the assembly receipt; no lane yet needs to prove a judged bundle unaltered. | First lane that must verify a frozen bundle's form independently of its assembly receipt. |
| One adapter in existence | The adapter recipe is proven across two platforms, but no second view family has exercised the core. | A second judgment lane (e.g. retail) defines a model-facing view. |
| Byte-optimal, not token-optimal; no cache-aware layout | Judgment runs on subscription where token shaping and cache control are unavailable; bytes are the honest measurable today. | API migration of bulk judgment. |
| No `judged_claim` table class | The condensation hierarchy is deferred by owner decision; declaring its table now would be speculative schema. | Condensation-hierarchy commissioning. |

Each residual is a foregone slice of the maximal version of the *bound*
capability, consciously accepted for speed, low lock-in, and reversibility.
Adjacent problems (selection, freezing events, retrieval, caching strategy)
are out of the bound target and are not residuals.

## Why Not Full God Tier

The residuals above are material: a maximal packer would verify frozen forms,
serve multiple view families, shape for the tokenizer, and carry the hierarchy
table class. Claiming GT now would either overclaim or force standing
infrastructure ahead of any consumer — the rejected maximal shape. When the
triggers fire and the slices land with their own validation, a successor
declaration may claim the higher tier; this record then remains as upgrade-path
provenance.

## Non-Claims

- Not validation, readiness, proof, or a numeric achievement measurement.
- Not implementation authorization for any residual's upgrade slice.
- The tier label asserts nothing about judgment quality, prompt quality, or
  product outcomes.
