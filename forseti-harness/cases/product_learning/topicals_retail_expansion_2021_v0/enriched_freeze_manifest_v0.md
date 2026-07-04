# Enriched Read — Freeze Manifest v0 (Topicals retail-expansion, qualitative C0–C4 read)

```yaml
artifact_role: Freeze manifest — pins the participant-packet read input + evidence for the qualitative C0–C4 demand read
case_id: topicals_retail_expansion_2021_v0
packet_variant: enriched_v0
cutoff: 2021-03-15
freeze_status: FROZEN_FOR_QUALITATIVE_READ
freeze_anchor: 2026-06-15 (capture session; receipts carry per-capture UTC timestamps)
authority_boundary: retrieval_only
```

## What is frozen

- **Contestant read input (the only file the contestant reads):**
  `participant_packet_enriched_v0.md`
  - sha256: `eec447a4d202ff06ffe05ac033677d8fe8aa66d7f687aa0ebbff14f2e1fa0c28`
- **Pinned evidence bodies (captured ≤cutoff, hash-pinned):**

| EU | Capture | Snapshot | Body sha256 |
| --- | --- | --- | --- |
| E6 | e6_careers_20210303 | 20210303084505 | db147fc02195e872957d588be376a935aee0fda584960dbd10d063912a0d981b |
| E7 | e7_faded_pdp | 20210210010815 | 49b3ecabd81a5052e15febd87270d19d7775e1179b81ebea3ba79459ded32154 |
| E8 | e8_like_butter_pdp | 20210303090202 | ff2db40f4359009784388df6bdecf1a0d452bae31a2f456a5ee86690043497b2 |
| E9 | e9_press_index | 20210303074312 | 02664e7f037153bc9be6b4e9457be9989c6e7a74a0149b43e44cb6cb7e42cb5c |
| E10 | e10_skininfluencers_post1 | 20210303081931 | d2c5605995bc898bce3ade75849ff81438d75eac4d488db8ba2c805ec7df4471 |
| E11 | e11_nordstrom_brand | 20201109194021 | 8a03c41ad0ae268bd431eabee82614214649e6f9aa868c3f8c99d11713db07a0 |

## Attestations

- **Blind construction:** the participant packet was built by the main lane agent as blind
  constructor, who has not read the facilitator-only sealed outcome. Evidence is ≤2021-03-15 only.
- **R6 independent pre-freeze leakage review — PASS (2026-06-15).** An independent, outcome-aware
  reviewer (separate subagent) read the sealed outcome and cleared all three checks: (1) no outcome
  leakage in the packet/decision-question; (2) all quoted signals verbatim-true to the captured
  bodies; (3) source labels accurate (E6–E10 brand-own-site; E11 independent retailer). The
  reviewer returned its verdict **without disclosing any outcome content**; the constructor/caller
  remains outcome-blind.
- **Firewall for the read:** the contestant (Phase 4) is a fresh isolated outcome-blind session
  reading only `participant_packet_enriched_v0.md`. The grade (Phase 5) is performed by a delegated
  outcome-aware subagent against the sealed outcome; the sealed verdict is compared to the outcome
  and tell-audited.

## Non-Claims

- `product_learning`, N=1. This freeze pins the read input for auditability; it is not validation,
  not judgment-quality, and not buyer proof. It is additive to (does not alter) the original frozen
  band-scorer fixture. The qualitative C0–C4 read does not use the FacilitatorLedger / band-scorer
  runtime (so `model_valid` does not apply).
```text
This is a freeze manifest. It is not a verdict, not a grade, and not proof of readiness.
```
