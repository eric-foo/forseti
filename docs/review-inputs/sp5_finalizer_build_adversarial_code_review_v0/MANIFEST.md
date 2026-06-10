# MANIFEST — SP-5 Finalizer Build, Adversarial Code Review (no_repo)

```yaml
retrieval_header_version: 1
artifact_role: Review courier manifest (disposable; no_repo bundle)
scope: Manifest + paste-ready prompt for a cross-vendor adversarial CODE review of the SP-5 FinalizationReceipt finalizer-half build (model + validate-only consumer + tests). Disposable courier; not source-of-truth; not committed.
use_when:
  - Sending the SP-5 finalizer-half build for a no-repo cross-vendor adversarial code review.
authority_boundary: retrieval_only
open_next:
  - finalization_models.py
  - sp5_finalization_receipt_spec_v0.md
stale_if:
  - The review completes and findings are adjudicated, or finalization_models.py changes.
```

## Review parameters

- **Target:** `finalization_models.py` (the built SP-5 finalizer half) against its reviewed spec `sp5_finalization_receipt_spec_v0.md`.
- **Bar:** cross-vendor **discovery** (new JQ-machinery seam) — find correctness/security holes and spec deviations, not a sanity check.
- **De-correlation:** reviewer must be a **different upstream vendor than the author (Anthropic/Claude)**. `de_correlation_bar: cross_vendor_discovery`; `same_vendor_rationale: n/a`.
- **Claim cap:** product-learning. This build does **not** unfreeze JSG-01 (it is the finalizer half only; the EvidenceUnit binding + a real packet are separate). Do not credit it as validated/ready/JQ.
- **Adjudication:** home-side. The reviewer finds; the home model adjudicates and patches on the owner's go.

## Bundle contents

| File | Role |
| --- | --- |
| `finalization_models.py` | review target — the built finalizer half (model + builder + validate-only consumer) |
| `test_finalization_models.py` | unit tests (all passing) |
| `test_finalization_models_contract.py` | purity/no-IO contract test (passing) |
| `sp5_finalization_receipt_spec_v0.md` | the reviewed behavior spec it implements |
| `harness_utils.py` | the reused primitives (`canonical_yaml_hash`, `generate_ulid`, `utc_now_z`) |
| `case_models.py` | `StrictModel` + `PreDecisionStatus` (the reused base + enum) |

## Paste-ready review prompt

````markdown
# Adversarial Code Review — SP-5 FinalizationReceipt finalizer half

You are an adversarial code reviewer from a different vendor than the author. No repo access — review only the attached bundle. Your job is **discovery**: find correctness holes, gaming paths, and spec deviations. Product-learning grade; this build does NOT unfreeze JSG-01.

## What this is
`finalization_models.py` implements the SP-5 finalizer half per the attached reviewed spec: a `FinalizationReceipt` model + a builder + a **validate-only, block-don't-repair** consumer that resolves the JSG-01 finalization-provenance subpredicate. Two mechanisms were locked: `binding_hash` = `canonical_yaml_hash` over `(evidence_id + finalized_over)`; current-designation = **supersedes-via-ULID** (each receipt has a `receipt_id`; a correction carries `supersedes`; current = the single un-superseded receipt; 0 or >1 ⇒ block).

## Attack it on
1. **block-don't-repair integrity.** Find ANY path where `evaluate_finalization_provenance` returns `CLEARED` with a `final_pre_decision_status` that did not come from a single valid current receipt, or where it authors/defaults/infers a value. The BLOCKED path must never carry a status.
2. **current-designation (supersedes-via-ULID).** Break `select_current_receipt`: supersede cycles, dangling `supersedes` (pointing outside the set) that hides the true current, duplicate `receipt_id`s, a correction that re-introduces a superseded value, or any case where it returns the wrong "current" or fails to block on real ambiguity. Is "the single un-superseded receipt" actually the right invariant?
3. **cross-family.** The consumer dropped an explicit finalizer-vs-run-judge check, relying on (receipt.judge == run judge) + the model's (finalizer != judge) invariant to imply (finalizer != run judge). Is that reasoning airtight, or is there a hole (e.g., the model invariant bypassable, or the judge-match check insufficient)?
4. **binding_hash.** Is it genuinely deterministic + tamper-evident? Probe canonicalization gaps: enum vs string, key ordering, unicode/whitespace in the basis, or two distinct inputs colliding.
5. **spec fidelity.** Deviations from the spec: separate record indexed (not keyed) by `evidence_id`; immutable/append-only; exactly-one-current; validate-only consumer; no EvidenceUnit change; no value authoring.
6. **scope/claim creep.** Does anything overstep — author a value, mutate state, do I/O, or imply a JSG-01 unfreeze?

## Return (in chat, for the operator to courier back)
```
review_summary:
  verdict: <sound | sound_with_fixes | unsound>
  findings:
    - id: F1
      severity: <critical | major | minor>
      where: <file:symbol/line>
      problem: <what is wrong / a concrete failing case>
      suggested_fix: <smallest change, if any>
  blind_spots: <anything the build/tests do not consider>
```
Cite concrete code paths and, where possible, a failing input. If a claim can't be evaluated from the bundle, say so.
````
