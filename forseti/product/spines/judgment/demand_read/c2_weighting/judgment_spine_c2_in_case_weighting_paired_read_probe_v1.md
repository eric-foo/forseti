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

## Observed Reads (compressed; full verbatim traces attached to the lane PR as a comment)

| Item | Reader A (opportunity) | Reader B (caution) | Agree? |
| --- | --- | --- | --- |
| E1 Reddit thread | supports; strong for quality, weak-to-moderate for demand; **supporting** ("doesn't by itself carry the reorder-volume question") | supports; moderate-high; **load_bearing** (retention sub-question + independent corroboration of E4, "genuine corroboration, not double-counting") | direction ✓; role differs — Finding P-6 |
| E2 TikTok #ad | weak; not_relied_on ("cheap talk, not costly behavior") | low; not_relied_on ("explains why virality happened, proves nothing") | ✓ |
| E3 press-kit trio | not_relied_on; "one source laundered through three outlets"; checked specific defeats it | not_relied_on; "one source triple-counted"; checkability is "the load-bearing check for this item and it defeats the apparent corroboration" | ✓ |
| E4 distributor report | strongly supports; strong; **load_bearing** (primary) | supports; high; **load_bearing** ("the strongest single anchor") | ✓ |
| E5 fad essay | opposes; weak-to-moderate; supporting ("correctly names a real risk category"); conflict-flagged, structurally downweighted | opposes; low; not_relied_on ("supplies no checkable facts"); conflict-flagged, "not treated as a genuine counterweight" | direction ✓; role varies (declared, neither in a verdict set) |
| E6 brand scarcity | not_relied_on; integrity-flagged unresolved, verification named; "does not add independent corroboration... the demand case rests on E4, not on E6 riding alongside it" | not_relied_on; integrity-flagged unresolved, verification named; "cannot be load-bearing while the staged-scarcity question is open" | ✓ |
| E7 search trend | **hedges** ("plateau consistent with either... doesn't distinguish"); moderate; secondary **load_bearing** | **hedges** (same reasoning, "ambiguity explicitly carried forward as a cap"); moderate-high; **load_bearing** | ✓ (both hedge — a cross-round shift from v0's "supports", consistent within-round) |
| E8 2019 stat | negligible; not_relied_on | negligible; not_relied_on | ✓ |

**Closings:** A — load-bearing = {E4, E7}, ceiling rests on these two; steelman
= E3 (what would make it strong: genuinely independent reviews, no press-kit
wording overlap); missing evidence general + single (retailer's own POS/trial
data). B — load-bearing = {E4, E1, E7}, **ceiling explicitly on the weakest =
E7** (plateau ambiguity); steelman = E6 (verified units/waitlist would make it
strong); missing evidence general + single (real second-season outcome data
for comparable viral products). **Verdicts:** both bounded staged commit at
stated moderate confidence; both used stakes only on the sufficiency side (A
verbatim: "per instruction 8, the size of this decision calls for more total
evidence than the packet supplies").

## Audit Against Pre-Registered Criteria

1. **v0 criteria — PASS with one carried exception.** Direction 8/8 within
   round (E7 = hedges in both). Verdict direction identical (bounded staged
   commit). Levels within one band, differences attributable (E5
   weak-to-moderate vs low, adjacent + declared; E1 role variance is P-6).
   All traps caught by both readers again: E3 collapsed via the checked
   wording specific, E6 integrity-routed with named verifications and
   explicitly denied additivity with E4, E5 conflict-flagged and not
   averaged (B additionally separated "E5 is no counterweight" from "E7
   genuinely tempers E4" — a cleaner conflict decomposition than v0). The
   carried exception is criterion 2.
2. **P-1 resolution — FAIL (as pre-registered).** The closing
   verdict-carrying lists differ by one member again: A {E4, E7}, B {E4, E1,
   E7}. v0 varied on E7; v1 varies on E1 — the varying member moved, so this
   is not the identical failure, but flat-list agreement was the criterion
   and it did not hold. What DID converge, in both rounds and both readers:
   E4 always load-bearing; direction and load-bearing facts identical; and
   in v1 both readers independently rest the verdict's **ceiling** on the
   same item (E7's ambiguity) — the ceiling-binding judgment converged even
   where set membership did not. Auditor expectation error recorded: the
   pre-registered membership prediction ("E4 and E1 certain, E7 admissible")
   was anchored on v0 and wrong about which member varies.
3. **Step-11 scope — PASS.** Both closings carry the general
   missing-evidence statement and the single most-impactful item.
4. **Stakes clause — PASS.** No weight rationale cites stakes; reader A
   explicitly routed decision size to the total-evidence bar. Both v1
   verdicts are somewhat more conservative than v0's (staging emphasized,
   confidence explicitly "moderate") — consistent with the stakes clause
   working on the sufficiency side; n=2, not attributable with confidence.
5. **`unknown` — PASS.** Neither reader used it; E7's "hedges" is a
   determinate direction call, not an evasion.
6. **FM-11..FM-14 — PASS with one borderline note.** FM-11: reader B's
   packet order put E4/E1 last and both still emerged load-bearing. FM-12:
   both readers explicitly refused to let E2/E3/E6 agreement upgrade
   anything; B named the E1-E4 pairing as legitimate cross-source
   corroboration and the E6-E4 pairing as non-additive — the exact
   distinction FM-12 draws. FM-13: the caution-framed reader B assigned E1 a
   HIGHER role than A did — no valence deference. FM-14 borderline: reader A
   cited "well-documented recent shifts" in the category (an outside-world
   claim not in the packet) as a secondary reason for E8's staleness
   discount; the discount stands on temporal fit alone, so the effect is
   nil, but the reflex is real — recorded, not failed.

## Findings And Disposition

- **P-6 (main finding — owner decision requested, not another wording
  edit).** In both rounds, two faithful readers' flat verdict-carrying
  load-bearing lists differ by exactly one member (v0: E7; v1: E1), each
  time an item that is load-bearing for a *sub-claim* (trajectory,
  organic-grounding/quality) rather than for the whole verdict, while
  direction, load-bearing facts, traps, verdict direction, and (in v1) the
  ceiling-binding weakest item all agree. Two rounds suggest this is
  inherent reader variance on multi-claim items, not a wording defect the
  core can fix. Per this probe's pre-registered interpretation, the
  partition-granularity question escalates to the owner. Options, with a
  recommendation: (a) **recommended** — amend the paired-read agreement
  standard so the compared objects are the ceiling-binding weakest
  load-bearing item + direction + load-bearing facts, with declared
  one-member set variance tolerated (matches the observed stable core and
  the sibling contract's judged-on-direction-plus-reasoning posture);
  (b) require per-claim load-bearing lists in the closing (heavier trace
  ceremony, pins the variance explicitly); (c) accept as-is and treat flat
  set agreement as aspirational. This probe applies none of them; the
  doctrine is unedited by v1.
  **Adjudicated:** owner adopted option (a) on 2026-07-10 (chat, this lane;
  the owner separately rejected per-claim derivation ceremony). Folded into
  the doctrine under its third `direction_change_propagation` receipt.
- **P-7 (observation).** E7's direction shifted supports→hedges from v0 to
  v1 in both readers — internally consistent each round, and the v1 reading
  ("plateau is genuinely ambiguous") is arguably the more careful one.
  Attribution between the hardened wording (step 2's anti-frame-import, the
  stakes clause) and sampling noise is not possible at n=2 per round;
  recorded as cross-round drift on an ambiguous-trajectory item, the same
  item class probe v2 (ledger series) identified as the consistency lever.
- **P-8 (positive result).** The hardened core embedded verbatim with zero
  adaptation (step 10 self-contained — the v0 deviation is closed), and the
  new elements behaved as designed on this case: stakes routed to
  sufficiency, no `unknown` misuse, FM-11/FM-12/FM-13 behaviors explicitly
  visible in the traces. Instruction-following quality did not regress
  anywhere the audit looked.

**Disposition:** the doctrine now carries two-round paired-read evidence
(`product_learning`, one synthetic case, same-family readers). The single
open item for owner adjudication alongside the doctrine itself is P-6's
agreement-standard choice. No further probe round is proposed before a real
case; the next-stronger evidence is a real-case read or cross-family
grading.

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
