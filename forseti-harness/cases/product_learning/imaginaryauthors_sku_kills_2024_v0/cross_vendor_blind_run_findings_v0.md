# Cross-Vendor Blind-Run Findings — imaginaryauthors_sku_kills_2024_v0

**Status: product-learning observation record. NOT distilled.**
This document records observed facts from one by-hand exam run. It derives **no**
harness changes, method changes, promoted lessons, or judgment-quality claims.
Distillation is deferred until any finding here is proven (i.e., replicated
beyond a single case under proven — not instructed/attested — isolation). Every
result below is a product-learning observation, not a validated conclusion.

- Case: `imaginaryauthors_sku_kills_2024_v0`
- Harness: `v0_14`
- Recorded: 2026-06-15
- Frozen scoring key (facilitator ledger) freeze hash:
  `238d4c82135dd729f5116655fbf6177a70c94e54f507f7ed54c0daaf34b9cb02`

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

- **Decision question:** At the cutoff (2024-08-01), should Imaginary Authors
  quietly discontinue Whispered Myths and Telegrama from its active DTC catalog —
  and, if so, how confidently can that recommendation be made on the available
  pre-cutoff public evidence, given the absence of internal sales data and the
  brand's dependence on enthusiast community trust?
- **Action ladder:** 0 abstain, 1 wait, 2–5 graduated recommend, 6 escalate,
  7–8 aggressive recommend (`recommend` must use {2,3,4,5,7,8}).
- **Calibrated band from the frozen key: [3, 5], band_status: normal.**
  Floor 3 is driven by `option_value: moderate` (`OPTION_VALUE_FLOOR["moderate"] = 3`);
  ceiling 5 by `evidence_strength: moderate` with `evidence_independence: partially_independent`
  (`BASE_CEILING["moderate"] = 5`, delta 0). Reversibility cap at 5 (medium
  feasibility) was non-binding. Decision shape: normal (width 2).
- **Held outcome (revealed only for the hindsight pass):** Whispered Myths and
  Telegrama confirmed permanently discontinued; final-bottle buying reported in
  Basenotes/Fragrantica community comments. Low-sales rationale stated (sales
  deadline Aug 18; "allocating production funds toward better-selling fragrances").
  Pointer to 8-total-quiet-kills product-info page not captured (no Wayback
  coverage).

## 3. Clean blind runs (scored)

| contestant | vendor / family | call | vs band [3,5] | recognition (self-report) | isolation basis | score id |
|---|---|---|---|---|---|---|
| `claude_sonnet_isolated_subagent_v0` | Anthropic | **3** | in-band (floor) | not recorded | sub-agent, `tool_uses=0` | `01KV69GVK7RRKEMQYW7XDA0EGK` |

The Claude run passed all evidence-id checks (presence, pre-decision status,
load-bearing citation) and must-address coverage (MA-01…MA-03). No failure
events logged. The call lands at the band floor.

## 4. Observations (stated as observed; no prescription)

1. **In-band at floor.** The Claude contestant recommended level 3 (cautious
   action), landing at the floor of the [3, 5] band. The band reflects moderate
   evidence strength with partial independence — width 2 signals genuine
   uncertainty in the key; the level-3 call is conservative within that
   uncertainty space.

2. **Shape match.** Contestant reported `decision_shape: action_band`; harness
   computed `band_status: normal`. These are consistent; the contestant correctly
   identified this as a non-escalation case.

3. **Single-contestant observation only.** All of the above is N=1 run. No
   cross-vendor comparison is possible until external runs complete.

## 5. What remains unproven / open

- **Cross-vendor comparison** is not yet available (GPT, Grok, Gemini runs not
  submitted).
- **Band floor [3] placement.** `option_value: moderate` drives floor to 3; this
  is facilitator-set. Not contested by this run (contestant landed at 3).
- **Recognition / leakage.** No self-reported recognition data collected for
  this run.
- **Isolation was instructed, not proven** (sub-agent with no web tools; not
  a structural isolation guarantee).

## 6. Explicitly not concluded here

- No harness change, schema change, packet redesign, or scorer change is derived
  or recommended in this record.
- No band-input (scoring key) change is made or proposed.
- No judgment-quality, readiness, or method-validation claim is made.

## 7. Provenance

- Score written under
  `cases/product_learning/imaginaryauthors_sku_kills_2024_v0/scores/01KV69GVK7RRKEMQYW7XDA0EGK.yaml`.
- Blind judgement under
  `runs/claude_sonnet_isolated_subagent_v0/run_001/blind_judgement.yaml`.
- Packet construction receipt:
  `packet_construction_receipt_v0.md` (outcome-blind build, R6 fix to
  `forbidden_information_notice`).
