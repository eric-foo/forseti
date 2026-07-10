# Judgment-Spine C2 In-Case Weighting Paired-Read Probe v1 (PROPOSED — hardened-core re-run)

```yaml
retrieval_header_version: 1
artifact_role: Feasibility probe v1 (design/docs experiment — re-runs probe v0's blind paired reads under the HARDENED Instruction Core to test whether the 2026-07-10 hardening pass preserves v0's result, resolves finding P-1, and embeds verbatim with zero adaptation; binds no case, populates no ledger, runs no production machinery)
scope: >
  Round two of the paired-read probe series for
  judgment_spine_c2_in_case_evidence_weighting_doctrine_v0.md. Identical
  method, case packet, and framings as probe v0; the ONLY changed input is
  the Instruction Core, now the post-hardening wording (verdict-carrying
  partition, self-contained step 10, stakes clause, widened step-11
  missing-evidence scope, anti-order-anchoring and anti-outside-knowledge
  clauses, unknown direction option). Tests preservation, P-1 resolution,
  and the new elements' producer-side compliance.
use_when:
  - Checking what probe evidence exists for the HARDENED Instruction Core (v0 probed the pre-hardening wording only).
  - Deciding whether the doctrine is ready for owner adjudication with two-round probe evidence, or needs another wording pass.
  - Designing probe v2 or the first real-case read.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/judgment/demand_read/c2_weighting/judgment_spine_c2_in_case_weighting_paired_read_probe_v0.md  # round one: method, packet (verbatim), pre-hardening result, findings P-1..P-5
  - forseti/product/spines/judgment/demand_read/c2_weighting/judgment_spine_c2_in_case_evidence_weighting_doctrine_v0.md  # the doctrine under test (hardened wording + hardening DCP receipt)
stale_if:
  - The owner adjudicates the doctrine (adopt / amend / reject).
  - INV-1 (no-scoring boundary) is amended by the owner.
  - A later probe round or a real-case read supersedes these observations.
```

## Status

`PROPOSED` — design/docs feasibility experiment, `product_learning` tier,
authored 2026-07-10 in the judgment evidence-weighting lane on explicit owner
authorization ("proceed with probe"). Same synthetic case as v0
(`example_not_a_real_case`); **binds no signal, admits no case, populates no
ledger row, runs no conductor gate, edits no doctrine.**

Pre-registration integrity: as in v0, this Method + Pre-Registered Criteria
section is committed **before** the author consumes either reader's output;
results land in a follow-up commit.

## Probe Question

Three things about the hardened Instruction Core:

1. **Preservation:** does it still pass every v0 criterion (8/8 direction
   agreement, trap handling, verdict direction, band tolerance, FM sweep)?
2. **P-1 resolution:** does the "load_bearing **for the verdict**" wording
   make the two readers' closing load-bearing lists agree with each other
   (v0's one partial: flat set labels diverged on E7 via per-sub-claim
   granularity)?
3. **New-element compliance:** verbatim embeddability (step 10 now
   self-contained — banked by construction: the v1 reader prompts carry the
   core with zero adaptation, unlike v0's step-10 rewrite), the stakes
   clause, the widened step-11 missing-evidence scope, the `unknown`
   direction option, and the four new failure modes FM-11..FM-14.

## Method

Identical to probe v0 (see v0's Method and Case sections — the packet items
E1–E8 and both framings are reused **verbatim**): two isolated Sonnet-tier
`worker` subagents, fresh contexts, tools forbidden, one framing each
(A opportunity, E1→E8 order; B caution, E5/E8/E2/E6/E3/E7/E4/E1 order),
blind to each other, to the test purpose, to v0's existence, and to the
audit rubric. The only changed input between rounds is the Instruction Core
wording.

Named limitations: same model family for readers and auditor (Claude;
Sonnet-tier readers, main-tier auditor); the same single synthetic case
reused for round-over-round comparability (cannot test generalization to
other cases); n=2 readers per round, so round-to-round differences include
uncontrolled sampling noise, not only the wording change; auditor = packet
and expectations author.

## Pre-Registered v1 Criteria (written before consuming any read)

1. **All v0 pass criteria hold** (v0 "Paired-read pass criteria" 1–6,
   applied unchanged, including the per-item expectations table).
2. **P-1 resolution:** the two closing "load_bearing for the verdict" lists
   agree **with each other**. Predicted membership: E4 and E1 in both; E7
   admissible only if it appears in both. Per-sub-claim role splits inside
   the trace remain legal when declared; the closing lists are what is
   compared.
3. **Step-11 scope:** both closings state the general missing-evidence gap
   (what the decision needed that the packet lacks) AND the single missing
   item that would most change the weights.
4. **Stakes clause honored:** no weight rationale cites the decision's
   stakes, cost, or irreversibility as a reason an item proves more; stakes
   language may appear only on the sufficiency/recommendation side.
5. **`unknown` not misused:** every packet item has a determinable bearing,
   so `unknown` is not expected; using it to dodge a determinable call is a
   miss (its mere availability must not degrade decisiveness).
6. **FM-11..FM-14 sweep clean:** no order-position rationale (FM-11); the
   agreement of E2/E3/E6 not read as upgrading any of them (FM-12); no
   frame-valence import into fitness targets or weights (FM-13); no invented
   background facts about GripMug/Corvo — the brand is fictional, so any
   confabulated outside knowledge is FM-14 by construction.

**Pre-registered interpretation:** all six hold → the hardened core
preserves v0's result and closes P-1; the doctrine carries two-round
paired-read evidence into owner adjudication. Criterion 2 fails the same way
as v0 → the wording fix was insufficient; escalate the partition-granularity
question to the owner rather than iterating wording again. Regression on
criterion 1 → the hardening damaged something; diff the failing trace
against the specific wording change before any further edit. Auditor
expectation errors are recorded as such, per v0's rule.

## Observed Reads

`PENDING` — filled after the pre-registration commit.

## Audit Against Pre-Registered Criteria

`PENDING`.

## Findings And Disposition

`PENDING`.

## Claim Classification

```yaml
judgment_spine_claim_classification:
  evaluated_claim_surface: hardened Instruction Core feasibility (preservation + P-1 resolution + new-element compliance, one synthetic case, Sonnet-tier readers, round two)
  source_quality_state: synthetic constructed case reused from probe v0; blind isolated reads; same-model-family readers and auditor
  execution_quality_state: two blind reads dispatched; audit pending at pre-registration commit
  closeout_state: no_durable_evidence
  claim_cap: product_learning only
  weakest_missing_or_failed_gate: single synthetic case reused (no generalization test); same-family readers; auditor = author; no real-case read; no cross-family grading
  receipt_artifact_or_gap: this artifact is the round-two probe record; a real-case read or cross-family grading would be the next-stronger evidence
  non_claims:
    - not validation, readiness, or buyer proof
    - not judgment-quality evidence
    - not case admission, ledger population, or conductor involvement
    - not model-independence or real-world reliability
```

## Non-Claims

- Synthetic paper experiment, round two on the same fictional case; binds,
  populates, and runs nothing on the real machinery.
- Tests within-Claude-family behavior at Sonnet reader tier on one
  constructed case; not model-independent, not multi-case, not a demand read
  of any real product.
- `product_learning`; a pass adjusts confidence in the instruction wording,
  never claim tier, and does not make the doctrine adopted.

```text
This is advisory design input only. It is not a verdict, not implementation
authority, and not proof of readiness.
```
