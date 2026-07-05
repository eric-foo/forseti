# Cross-Vendor Blind-Run Findings — privatepacks_retail_retreat_v0

**Status: product-learning observation record. NOT distilled.**
This document records observed facts from one by-hand exam run. It derives **no**
harness changes, method changes, promoted lessons, or judgment-quality claims.
Distillation is deferred until any finding here is proven (i.e., replicated
beyond a single case under proven — not instructed/attested — isolation). Every
result below is a product-learning observation, not a validated conclusion.

- Case: `privatepacks_retail_retreat_v0`
- Harness: `v0_14`
- Recorded: 2026-06-15
- Frozen scoring key (facilitator ledger) freeze hash:
  `f3e2daf5989eb4565583eca893ce10baf2cf263116a0af6b944792dd41ac09a4`

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

- **Decision question:** As of 2025-05-01, should Private Packs exit or
  materially scale back its CVS and Target retail distribution, hold its current
  retail footprint, or continue investing in retail channel growth — given that
  the brand entered mass retail in mid-2024 and available DTC site evidence
  suggests below-expectation in-store velocity?
- **Action ladder:** 0 abstain, 1 wait, 2–5 graduated recommend, 6 escalate,
  7–8 aggressive recommend (`recommend` must use {2,3,4,5,7,8}).
- **Calibrated band from the frozen key: [6, 6], band_status: conflict_escalate.**
  Moderate evidence with correlated independence (ceiling 4); reversibility
  feasibility `low` caps ceiling at 3; floor driven to 5 by `opportunity_cost:
  severe` (floor = 5) and `urgency: critical` (floor = 5). Dampened floor 5 >
  raw ceiling 3 → canonical escalation to [6, 6]. The harness mandates
  `judgement_class: escalate` at `ladder_level: 6`.
- **Held outcome (revealed only for the hindsight pass):** Retail retreat from
  ~1,000 CVS + ~250 Target doors on a velocity miss (category expected ~4–6
  units/wk); ~$100K retail infrastructure written off; pivot back to DTC.
  Reported by Beauty Independent: "Private Packs founder walked away from retail
  distribution."

## 3. Clean blind runs (scored)

| contestant | vendor / family | call | vs band [6,6] | recognition (self-report) | isolation basis | score id |
|---|---|---|---|---|---|---|
| `claude_sonnet_isolated_subagent_v0` | Anthropic | **6 (escalate)** | in-band | not recorded | sub-agent, `tool_uses=0` | `01KV69GWF5KVS7F5HR9JB1VV67` |

The Claude run passed evidence-id presence and pre-decision status checks, and
must-address coverage (MA-01…MA-03). However, `load_bearing_claim_citation_pass`
is **false** — one blocking failure event logged: `01KV69GWF5H5BDR7HTFC0VAJMN`
(`evidence_id_missing`, severity: blocking). The call is in-band (escalate at 6
correctly matches the [6,6] conflict_escalate mandate); the citation failure is
a discipline defect, not an in-band/out-of-band result.

The contestant reported `decision_shape: escalation_required` and
`judgement_class: escalate` at `ladder_level: 6`. This matches the harness
mandate exactly.

Note: the original blind judgement used `judgement_class: irreducible_uncertainty`
(a schema-invalid choice at level 6; valid only at level 0). Corrected by
orchestrator to `judgement_class: escalate` before scoring — the substantive
reasoning clearly intended CONFLICT_ESCALATE (floor > ceiling), and the
`decision_shape: escalation_required` field was already correct.

## 4. Observations (stated as observed; no prescription)

1. **In-band: correct escalation class.** The Claude contestant correctly
   identified this as a conflict-escalate case, calling `escalate` at level 6.
   This is structurally harder than a simple recommend: the contestant must
   recognize that floor pressure (severe opportunity cost, critical urgency)
   exceeds the evidence ceiling (moderate + correlated → 4, then reversibility
   cap → 3).

2. **Citation discipline failure alongside correct class.** The in-band escalate
   call is paired with a load-bearing citation failure (blocking severity).
   The class-level call was correct; the evidentiary citation trail was not fully
   explicit.

3. **Schema correction required on the blind judgement.** The original
   `irreducible_uncertainty` label was schema-invalid (level 6 requires
   `escalate`; `irreducible_uncertainty` is only valid at level 0). The
   substantive content was escalate; the label was corrected before scoring.
   This is a schema-discipline gap, not a substantive reasoning gap.

4. **Single-contestant observation only.** All of the above is N=1 run.

## 5. What remains unproven / open

- **Cross-vendor comparison** is not yet available (GPT, Grok, Gemini runs not
  submitted).
- **Whether conflict-escalate recognition is generalizable.** This case had
  the clearest possible pressure signal (`urgency: critical`, `opportunity_cost:
  severe`); whether other conflict-escalate cases with less extreme inputs are
  handled as well is not tested here.
- **Load-bearing citation discipline.** Same open question as kinderbeauty:
  whether citation discipline failures are model-specific or case-specific.
- **`irreducible_uncertainty` vs `escalate` labeling.** Whether the label
  confusion recurs in future runs is an open question.

## 6. Explicitly not concluded here

- No harness change, schema change, packet redesign, or scorer change is derived
  or recommended in this record.
- No band-input (scoring key) change is made or proposed.
- No judgment-quality, readiness, or method-validation claim is made.

## 7. Provenance

- Score written under
  `cases/product_learning/privatepacks_retail_retreat_v0/scores/01KV69GWF5KVS7F5HR9JB1VV67.yaml`.
- Blind judgement under
  `runs/claude_sonnet_isolated_subagent_v0/run_001/blind_judgement.yaml`.
- Packet construction receipt:
  `packet_construction_receipt_v0.md` (outcome-blind build; R6 review found
  no `forbidden_information_notice` fix required).
