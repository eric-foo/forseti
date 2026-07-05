# Cross-Vendor Blind-Run Findings — sundaily_gummy_pivot_v0

**Status: product-learning observation record. NOT distilled.**
This document records observed facts from one by-hand exam run. It derives **no**
harness changes, method changes, promoted lessons, or judgment-quality claims.
Distillation is deferred until any finding here is proven (i.e., replicated
beyond a single case under proven — not instructed/attested — isolation). Every
result below is a product-learning observation, not a validated conclusion.

- Case: `sundaily_gummy_pivot_v0`
- Harness: `v0_14`
- Recorded: 2026-06-15
- Frozen scoring key (facilitator ledger) freeze hash:
  `1ac2c3591a6a0676a8399c5a626b5d5b136233577ed48e20e9f8bddabc5361c5`

---

## 1. Scope and cap

This is a by-hand product-learning exercise that **uses** the harness; it is not
a judgment-quality run. Specifically:

- Contestant isolation was **instructed/attested**, not structurally proven
  (sub-agent with `tool_uses=0` for the Claude run; external runs not yet
  completed).
- The scorer's `memorization_probe_result` is hardcoded `not_run`; no JSG-05
  gate was applicable (no known fame risk for this brand/case).
- The frozen band inputs were facilitator-set and owner-ratified, not
  independently derived.

No JSG gate is cleared or advanced by this record. External contestant runs
(GPT, Grok, Gemini) are not yet complete; this record covers the Claude run only.

## 2. Exam setup

- **Decision question:** Should Sundots, as of 2018-10-01, pivot its brand
  positioning from a UV-protection ingestible supplement to a broader skin-health
  gummy platform and rename the brand accordingly, or should it remain focused on
  its original UV-specific ingestible product line?
- **Action ladder:** 0 abstain, 1 wait, 2–5 graduated recommend, 6 escalate,
  7–8 aggressive recommend (`recommend` must use {2,3,4,5,7,8}).
- **Calibrated band from the frozen key: [6, 6], band_status: conflict_escalate.**
  Weak evidence with correlated independence (ceiling 2); floor driven to 3 by
  `option_value: high` (`OPTION_VALUE_FLOOR["high"] = 4`, dampened to 3 by
  `evidence_strength_floor_cap["weak"] = 3`). Dampened floor 3 > raw ceiling 2
  → canonical escalation to [6, 6]. The harness mandates `judgement_class:
  escalate` at `ladder_level: 6`.
- **Held outcome (revealed only for the hindsight pass):** Brand renamed
  Sundots → Sundaily; full pivot to broader skin-health gummies. Goop
  distribution/validation followed the pivot. `getsundaily.com` domain emergence
  (Oct–Dec 2018; post-cutoff; not captured).

## 3. Clean blind runs (scored)

| contestant | vendor / family | call | vs band [6,6] | recognition (self-report) | isolation basis | score id |
|---|---|---|---|---|---|---|
| `claude_sonnet_isolated_subagent_v0` | Anthropic | **1 (wait)** | under by 5 | not recorded | sub-agent, `tool_uses=0` | `01KV69GX3SV1MZSS4DJYPVEHFY` |

The Claude run passed evidence-id presence, pre-decision status, and load-bearing
citation checks, and must-address coverage (MA-01, MA-02; only 2 required for
this case). One under_band failure event logged (info severity):
`01KV69GX3SZSE2CSB7KN0FNQRT`. Underreach distance: 5 (the maximum possible
given the band mandates level 6 and the call was level 1).

The contestant reported `decision_shape: action_band` and `judgement_class: wait`
at `ladder_level: 1`. The harness computed `band_status: conflict_escalate`. The
contestant did not recognize the conflict-escalate structure; it treated this as
a normal watch/wait case.

## 4. Observations (stated as observed; no prescription)

1. **Extreme under_band (−5): conflict-escalate case called as wait.** Level 1
   (wait) is the most conservative non-abstain call on the ladder. The harness
   mandates level 6 (escalate). The contestant interpreted the evidence ambiguity
   as a reason to pause rather than as a floor-exceeds-ceiling signal requiring
   mandatory escalation.

2. **Shape mismatch: action_band vs conflict_escalate.** This is the inverse of
   the privatepacks result (which correctly identified escalation). Here, the
   same structural situation (weak + correlated evidence + meaningful option_value
   floor) produced a non-escalate call. The difference: `option_value: high` in
   this case drives a floor of 4 (dampened to 3 by evidence weakness), while the
   evidence ceiling of 2 is even lower than joahbeauty's (also ceiling 2). The
   contestant treated high option_value as a reason to wait rather than as a floor
   pressure signal.

3. **Largest underreach in the batch.** Among the 6 holdout cases, this run
   produced the maximum underreach_distance (5). The conflict-escalate cases
   (joahbeauty, privatepacks, sundaily) represent the hardest structural class
   for a contestant to correctly identify.

4. **Single-contestant observation only.** All of the above is N=1 run.

## 5. What remains unproven / open

- **Cross-vendor comparison** is not yet available (GPT, Grok, Gemini runs not
  submitted).
- **Conflict-escalate recognition in low-ceiling, option-value-driven cases.**
  The privatepacks case had extreme urgency/opportunity_cost signals and was
  correctly called as escalate; this case has weaker pressure signals (high
  option_value only). Whether this specific structural pattern generalizes to
  under-calls is not yet testable.
- **Option_value floor interpretation.** The contestant's reasoning treated
  high option_value as evidence of upside uncertainty → wait. The harness
  uses `OPTION_VALUE_FLOOR["high"] = 4` as a floor pressure signal → mandatory
  escalation when evidence ceiling is below floor. These interpretations diverge
  in this case.
- **Recognition / leakage.** No self-reported recognition data collected. Sundots
  is a relatively obscure 2018 brand; recognition risk is low.

## 6. Explicitly not concluded here

- No harness change, schema change, packet redesign, or scorer change is derived
  or recommended in this record.
- No band-input (scoring key) change is made or proposed.
- No judgment-quality, readiness, or method-validation claim is made.

## 7. Provenance

- Score written under
  `cases/product_learning/sundaily_gummy_pivot_v0/scores/01KV69GX3SV1MZSS4DJYPVEHFY.yaml`.
- Blind judgement under
  `runs/claude_sonnet_isolated_subagent_v0/run_001/blind_judgement.yaml`.
- Packet construction receipt:
  `packet_construction_receipt_v0.md` (outcome-blind build; R6 fix to
  `forbidden_information_notice` — removed outcome-presupposing "actual strategic
  pivot" and "any brand rename" phrases).
