# Cross-Vendor Blind-Run Findings — joahbeauty_cvs_kill_2024_v0

**Status: product-learning observation record. NOT distilled.**
This document records observed facts from one by-hand exam run. It derives **no**
harness changes, method changes, promoted lessons, or judgment-quality claims.
Distillation is deferred until any finding here is proven (i.e., replicated
beyond a single case under proven — not instructed/attested — isolation). Every
result below is a product-learning observation, not a validated conclusion.

- Case: `joahbeauty_cvs_kill_2024_v0`
- Harness: `v0_14`
- Recorded: 2026-06-15
- Frozen scoring key (facilitator ledger) freeze hash:
  `b969d7acc3a8d35ef7efe411c07cf4785261895fa19f37c35cfa6e1b66b41ba8`

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

- **Decision question:** At the 2024-06-01 cutoff, should Joah Beauty (Kiss
  Products' K-beauty mass-retail line) wind down, significantly scale back, or
  continue and expand its CVS-exclusive distribution strategy (~4,000 doors),
  given available pre-cutoff public DTC evidence about brand health, product
  breadth, and channel signaling?
- **Action ladder:** 0 abstain, 1 wait, 2–5 graduated recommend, 6 escalate,
  7–8 aggressive recommend (`recommend` must use {2,3,4,5,7,8}).
- **Calibrated band from the frozen key: [6, 6], band_status: conflict_escalate.**
  Weak evidence (`BASE_CEILING["weak"] = 3`) with correlated independence
  (delta −1 → ceiling 2) is suppressed to 2 by the evidence ceiling; floor is
  driven to 3 by `opportunity_cost: moderate` and `option_value: moderate`
  floors (both = 3). Dampened floor 3 > raw ceiling 2 → canonical escalation
  to [6, 6]. The harness mandates `judgement_class: escalate` at `ladder_level: 6`
  for this shape.
- **Held outcome (revealed only for the hindsight pass):** April 2025 closure +
  50%-off liquidation. The silent wind-down was first detected by r/BeautyGuruChatter
  and entered the trade record via Beauty Independent (April 2025). Social media
  accounts wiped after June 2024 (post-cutoff detection signal).

## 3. Clean blind runs (scored)

| contestant | vendor / family | call | vs band [6,6] | recognition (self-report) | isolation basis | score id |
|---|---|---|---|---|---|---|
| `claude_sonnet_isolated_subagent_v0` | Anthropic | **4** | under by 2 | not recorded | sub-agent, `tool_uses=0` | `01KV69GVWT2MSY6HVTZ0TXN2M8` |

The Claude run passed evidence-id presence, pre-decision status, and load-bearing
citation checks, and must-address coverage (MA-01…MA-03). One under_band failure
event logged (info severity): `01KV69GVWT6BRW4FZZQ4GA70HE`.

The contestant reported `decision_shape: action_band` and `ladder_level: 4`
(`recommend`). The harness computed `band_status: conflict_escalate` — the
evidence ceiling is below the pressure floor, mandating escalation at level 6.
The contestant did not recognize the conflict-escalate structure.

## 4. Observations (stated as observed; no prescription)

1. **Under_band at −2 (conflict-escalate case).** The Claude contestant
   recommended level 4 (active, graduated recommend) in a case where the harness
   mandates escalate at level 6. The underreach is structural: weak + correlated
   evidence with meaningful floor pressure produces a floor-exceeds-ceiling
   conflict that the key resolves as mandatory escalation. The contestant provided
   a definite call where the key says the evidence doesn't support one.

2. **Shape mismatch.** Contestant reported `decision_shape: action_band`;
   harness computed `band_status: conflict_escalate`. The contestant diagnosed
   this as a normal action case; the harness disagrees. This is the single most
   diagnostic fact from this run.

3. **Single-contestant observation only.** All of the above is N=1 run. Whether
   this shape-mismatch pattern is model-specific or general requires replication.

## 5. What remains unproven / open

- **Cross-vendor comparison** is not yet available (GPT, Grok, Gemini runs not
  submitted).
- **Conflict-escalate recognition.** Whether any blind contestant correctly
  identifies the [6,6] mandate when evidence is weak+correlated and floor
  pressure is present is an open question.
- **Key floor inputs.** `opportunity_cost: moderate` and `option_value: moderate`
  both drive floors to 3; `evidence_strength: weak` limits the ceiling to 2.
  Whether moderate opportunity cost accurately characterizes this case is
  facilitator-set, not independently verified.
- **Recognition / leakage.** No self-reported recognition data collected for
  this run.

## 6. Explicitly not concluded here

- No harness change, schema change, packet redesign, or scorer change is derived
  or recommended in this record.
- No band-input (scoring key) change is made or proposed.
- No judgment-quality, readiness, or method-validation claim is made.

## 7. Provenance

- Score written under
  `cases/product_learning/joahbeauty_cvs_kill_2024_v0/scores/01KV69GVWT2MSY6HVTZ0TXN2M8.yaml`.
- Blind judgement under
  `runs/claude_sonnet_isolated_subagent_v0/run_001/blind_judgement.yaml`.
- Packet construction receipt:
  `packet_construction_receipt_v0.md` (outcome-blind build; schema correction
  applied to evidence YAML `source_type` and `hash_basis` fields; packet content
  unchanged).
