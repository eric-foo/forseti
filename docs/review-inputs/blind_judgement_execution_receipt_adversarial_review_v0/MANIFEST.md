# MANIFEST — Blind-Judgment Execution Receipt Spec, Adversarial Review (no_repo)

```yaml
retrieval_header_version: 1
artifact_role: Review courier manifest (disposable; no_repo bundle)
scope: Manifest + paste-ready prompt for a cross-vendor adversarial artifact review of the blind-judgment execution-receipt behavior spec v0. Disposable courier; not source-of-truth; not committed.
use_when:
  - Sending the blind-judgment execution-receipt spec for a no-repo cross-vendor adversarial review.
authority_boundary: retrieval_only
open_next:
  - blind_judgement_execution_receipt_spec_v0.md
stale_if:
  - The review completes and findings are adjudicated, or the spec changes.
```

## Review parameters

- **Target:** `blind_judgement_execution_receipt_spec_v0.md` (a behavior spec; not code, not validated).
- **Bar:** cross-vendor **discovery** (new seam) — find blind spots and unsound assumptions, not a sanity check.
- **De-correlation:** reviewer must be a **different upstream vendor than the author (Anthropic/Claude)** — e.g. an OpenAI/Google/other-vendor model. `de_correlation_bar: cross_vendor_discovery`; `same_vendor_rationale: n/a`.
- **Claim cap:** product-learning. Do not credit the spec as validated, ready, or judgment-quality evidence.
- **Adjudication:** home-side. The reviewer finds; the home model adjudicates and patches on the owner's go. The reviewer does not patch.

## Bundle contents

| File | Role |
| --- | --- |
| `blind_judgement_execution_receipt_spec_v0.md` | review target |
| `contestant_no_tools_execution_contract_v0.md` | controlling isolation/provenance doctrine |
| `sp5_finalization_receipt_spec_v0.md` | separate-record precedent |
| `probe_models.py` | `ContestantExecutionIsolation` (reused isolation receipt) + probe gate logic |
| `judgement_models.py` | `BlindJudgement` (the judgment record the receipt sits beside) |
| `gate_and_conductor_excerpts.md` | JSG-04 row + Isolation Topology + by-hand isolation cap (the grounding the spec cites) |

## Paste-ready review prompt

````markdown
# Adversarial Artifact Review — Blind-Judgment Execution Receipt Spec v0

You are an adversarial artifact reviewer from a different vendor than the author. You have no repository access — review only the attached bundle. Your job is **discovery**: find blind spots, unsound assumptions, and ways this contract could fail or be gamed — not a sanity check.

## What this is
A **behavior spec** (what-must-be-true; not code, not validated) for a *separate* "execution receipt" artifact that binds a blind-judgment run's proof of no-tools isolation + auditable live-execution provenance, kept as a sibling file to `blind_judgement.yaml`. The owning system grades only at **product-learning** — do not credit this as validated, ready, or judgment-quality evidence. The owner just decided to store this proof in a *separate file* rather than inside the judgment record or as a change to it.

## Attack this artifact on
1. **Shape soundness.** The spec keeps isolation OUT of the `BlindJudgement` record and in a separate sibling receipt, arguing the gate reads receipts out-of-band. Is that actually safe? Construct any case where the gate would need isolation *inside* the judgment record, or where a sibling file breaks an audit/atomicity property.
2. **Laundering / non-gate-clearing integrity.** The spec says dry / fake-transport / by-hand receipts are permanently non-gate-clearing even if their computed `isolation_result` is `proven`. Find any path where such a receipt could clear the gate or be mistaken for a live one.
3. **Binding integrity.** The receipt binds to its judgment via `case_id`/`run_id`/`contestant_id` + `prompt_hash`/`raw_response_hash`. Can a receipt certify the wrong judgment (replay, copy, or spoof)? Is the binding sufficient?
4. **Provenance completeness.** Against the no-tools contract's Receipt Provenance Boundary, is any required field missing, under-specified, or placeable in a way that defeats auditability?
5. **Scope leakage.** Does the spec anywhere authorize a build, a live call, a gate clearance, or claim a tier above product-learning, despite saying it does not?
6. **Consistency.** Any contradiction with the no-tools contract, `ContestantExecutionIsolation`, `BlindJudgement`, the SP-5 spec, or the gate-ownership/conductor excerpts.

## Return (in chat, for the operator to courier back)
```
review_summary:
  verdict: <sound | sound_with_fixes | unsound>
  findings:
    - id: F1
      severity: <critical | major | minor>
      where: <section / field>
      problem: <what is wrong or unproven>
      suggested_fix: <smallest change, if any>
  blind_spots: <anything the spec does not consider>
```
Cite the spec's own sections/fields. If a claim cannot be evaluated from the bundle, say so rather than assuming.
````
