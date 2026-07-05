# Cross-Vendor Blind-Run Findings — kinderbeauty_box_pivot_2023_v0

**Status: product-learning observation record. NOT distilled.**
This document records observed facts from one by-hand exam run. It derives **no**
harness changes, method changes, promoted lessons, or judgment-quality claims.
Distillation is deferred until any finding here is proven (i.e., replicated
beyond a single case under proven — not instructed/attested — isolation). Every
result below is a product-learning observation, not a validated conclusion.

- Case: `kinderbeauty_box_pivot_2023_v0`
- Harness: `v0_14`
- Recorded: 2026-06-15
- Frozen scoring key (facilitator ledger) freeze hash:
  `a337fc7095ed15e520e09837d6a77be71986ba5d7a6bbb8881d16a18ad869ffc`

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

- **Decision question:** At the cutoff (2023-03-01), should Kinder Beauty pivot
  its subscription box economics — including pricing, box frequency, tier
  structure, or curation model — to address apparent strain in the DTC beauty box
  segment, and how confidently can that recommendation be made on the available
  pre-cutoff public evidence, given the absence of subscriber count, churn, and
  margin data?
- **Action ladder:** 0 abstain, 1 wait, 2–5 graduated recommend, 6 escalate,
  7–8 aggressive recommend (`recommend` must use {2,3,4,5,7,8}).
- **Calibrated band from the frozen key: [3, 4], band_status: normal (ceiling_trap).**
  Moderate evidence with correlated independence (`BASE_CEILING["moderate"] = 5`,
  delta −1 for correlated → ceiling 4); loss_shape asymmetric_down cap at 6
  non-binding; floor driven to 3 by `opportunity_cost: moderate` and
  `option_value: moderate` (both `= 3`). Width 1 (ceiling_trap shape).
- **Held outcome (revealed only for the hindsight pass):** Shutdown January 2024;
  pre-announcement decay in subscriber experience reported by r/BeautyBoxes
  community.

## 3. Clean blind runs (scored)

| contestant | vendor / family | call | vs band [3,4] | recognition (self-report) | isolation basis | score id |
|---|---|---|---|---|---|---|
| `claude_sonnet_isolated_subagent_v0` | Anthropic | **3** | in-band (floor) | not recorded | sub-agent, `tool_uses=0` | `01KV69RP7C2P278W8RM0MGQ8CD` |

The Claude run passed evidence-id presence, pre-decision status checks, and
must-address coverage (MA-01…MA-03). However, `load_bearing_claim_citation_pass`
is **false** — one blocking failure event logged: `01KV69RP7C4RCH5MHAXQ1T8DWD`
(`evidence_id_missing`, severity: blocking). The call is in-band; the citation
failure is a discipline defect, not an in-band/out-of-band result.

The contestant reported `decision_shape: ceiling_trap`, correctly matching the
harness-computed `band_status: normal` (ceiling_trap shape).

## 4. Observations (stated as observed; no prescription)

1. **In-band at floor with one blocking citation failure.** Level-3 call lands
   at the floor of the [3, 4] ceiling-trap band. The in-band result is not in
   dispute; the citation failure means a load-bearing claim was not backed by
   an explicit evidence ID citation in the judgement.

2. **Shape match (ceiling_trap).** Contestant correctly diagnosed `ceiling_trap`
   — the asymmetric-down loss shape combined with correlated evidence creates
   a narrow band where the ceiling is one above the floor. The citation discipline
   failure does not change the shape-recognition result.

3. **Single-contestant observation only.** All of the above is N=1 run.

## 5. What remains unproven / open

- **Cross-vendor comparison** is not yet available (GPT, Grok, Gemini runs not
  submitted).
- **Load-bearing citation discipline.** Whether the citation failure reflects a
  model-specific pattern or case-specific evidence sparsity is not determined.
- **Band ceiling [4] as ceiling_trap floor [3].** A ceiling-trap band provides
  one level of slack; this case has none of the room for error that a wider band
  would provide. Whether the ceiling should be 4 or 5 is facilitator-set.

## 6. Explicitly not concluded here

- No harness change, schema change, packet redesign, or scorer change is derived
  or recommended in this record.
- No band-input (scoring key) change is made or proposed.
- No judgment-quality, readiness, or method-validation claim is made.

## 7. Provenance

- Score written under
  `cases/product_learning/kinderbeauty_box_pivot_2023_v0/scores/01KV69RP7C2P278W8RM0MGQ8CD.yaml`.
- Blind judgement under
  `runs/claude_sonnet_isolated_subagent_v0/run_001/blind_judgement.yaml`.
- Packet construction receipt:
  `packet_construction_receipt_v0.md` (outcome-blind build; R6 fix to
  `forbidden_information_notice`; schema fix removing `url:` from evidence
  YAMLs — field not in `EvidenceUnit` schema, URL preserved in `source` field).
