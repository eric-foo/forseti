# Cross-Vendor Blind-Run Findings — selflessbyhyram_target_entry_2023_v0

**Status: product-learning observation record. NOT distilled.**
This document records observed facts from one by-hand exam run. It derives **no**
harness changes, method changes, promoted lessons, or judgment-quality claims.
Distillation is deferred until any finding here is proven (i.e., replicated
beyond a single case under proven — not instructed/attested — isolation). Every
result below is a product-learning observation, not a validated conclusion.

- Case: `selflessbyhyram_target_entry_2023_v0`
- Harness: `v0_14`
- Recorded: 2026-06-15
- Frozen scoring key (facilitator ledger) freeze hash:
  `8d0c8f00931bc532c2c03c60700f55d2b69ce56456e3c07f238982d91dee9815`

---

## 1. Scope and cap

This is a by-hand product-learning exercise that **uses** the harness; it is not
a judgment-quality run. Specifically:

- Contestant isolation was **instructed/attested**, not structurally proven
  (sub-agent with `tool_uses=0` for the Claude run; external runs not yet
  completed).
- The scorer's `memorization_probe_result` is hardcoded `not_run`. This case
  carries `known_fame_risk: high_fame_beauty_influencer_skincare_brand` and
  `memorization_probe_required: true` in the ledger (JSG-05). The memorization
  probe notice was included in the contestant's packet (body section, not YAML
  frontmatter). The contestant's self-report is advisory; no scorer-enforced JSG-05
  gate result is available from this run.
- The frozen band inputs were facilitator-set and owner-ratified, not
  independently derived.

No JSG gate is cleared or advanced by this record. External contestant runs
(GPT, Grok, Gemini) are not yet complete; this record covers the Claude run only.

## 2. Exam setup

- **Decision question:** Should Selfless by Hyram pursue mass-retail distribution
  through Target at a repositioned (lower) price point relative to its current
  DTC pricing, or maintain its DTC-first premium positioning and direct community
  model — and how confident can a recommendation be given the available pre-cutoff
  evidence?
- **Action ladder:** 0 abstain, 1 wait, 2–5 graduated recommend, 6 escalate,
  7–8 aggressive recommend (`recommend` must use {2,3,4,5,7,8}).
- **Calibrated band from the frozen key: [3, 4], band_status: normal (ceiling_trap).**
  Moderate evidence with correlated independence (ceiling 4); floor 3 from
  `option_value: moderate` and `opportunity_cost: moderate`. Width 1 (ceiling_trap
  shape). Urgency `low` did not bind above floor.
- **Held outcome (revealed only for the hindsight pass):** Target exit April 2025;
  the mass-retail strategy did not hold. Full channel saga: Sephora exit → Target
  repricing entry (Feb 2023) → founder buyback → Target exit (Apr 2025). Post-cutoff
  material; not captured.

## 3. Clean blind runs (scored)

| contestant | vendor / family | call | vs band [3,4] | jsg05 (self-report) | isolation basis | score id |
|---|---|---|---|---|---|---|
| `claude_sonnet_isolated_subagent_v0` | Anthropic | **4** | in-band (ceiling) | `unproven` (self-reported; harness: `not_run`) | sub-agent, `tool_uses=0` | `01KV69GWSK85V5PVTECC0QM27Z` |

The Claude run passed all evidence-id checks (presence, pre-decision status,
load-bearing citation) and must-address coverage (MA-01…MA-03). No failure
events logged. The call lands at the ceiling of the ceiling-trap band.

The contestant self-reported `jsg05_isolation_result: unproven` in the advisory
phase_1 fields of the blind judgement, with notes that it flagged some
possibility of training-data exposure but could not self-verify. The harness
does not score this field; it is recorded here as an advisory observation only.

The contestant reported `decision_shape: action_band`; harness computed
`band_status: normal` (ceiling_trap). These are consistent on the in-band/out-of-band
result, though the contestant did not label the shape as `ceiling_trap`.

## 4. Observations (stated as observed; no prescription)

1. **In-band at ceiling (ceiling-trap shape).** The level-4 call lands at the
   ceiling of the [3, 4] band. The ceiling-trap shape (width 1) means there is
   no upward slack; a level-5 call would have been over_band. The contestant
   avoided this.

2. **JSG-05 advisory flag.** The contestant self-reported `unproven` isolation
   on the fame-risk probe. This is consistent with `known_fame_risk:
   high_fame_beauty_influencer_skincare_brand` (Hyram is a well-known creator).
   The self-report does not constitute a proven contamination; it is an advisory
   flag. Whether the level-4 call is inflated by recognition is not determinable
   from this run.

3. **Shape partial mismatch.** Contestant used `action_band` where the band
   status is `ceiling_trap` (a sub-classification of normal bands). The
   in-band result is correct; the shape label is imprecise.

4. **Single-contestant observation only.** All of the above is N=1 run.

## 5. What remains unproven / open

- **JSG-05 contamination risk.** The `unproven` self-report means contamination
  cannot be ruled out for this run. The `memorization_probe_result: not_run`
  in the score reflects harness-side: no scorer-enforced gate. This is the most
  significant unclosed concern for this case.
- **Cross-vendor comparison** is not yet available (GPT, Grok, Gemini runs not
  submitted).
- **Whether the ceiling hit reflects fame-signal inflating the call.** If the
  contestant recognized the brand direction (mass-retail entry), that knowledge
  would push toward level 4 (commit to explore) rather than 3 (cautious). Not
  resolvable from this run.
- **Band ceiling [4] as ceiling_trap.** Whether the ceiling should be 4 or 5
  is facilitator-set. The ceiling_trap shape means any single-level upward
  error would be scoring-relevant.

## 6. Explicitly not concluded here

- No harness change, schema change, packet redesign, or scorer change is derived
  or recommended in this record.
- No band-input (scoring key) change is made or proposed.
- No judgment-quality, readiness, or method-validation claim is made.
- The JSG-05 `unproven` flag does not exclude this run; it is recorded as an
  advisory observation, not a finding of contamination.

## 7. Provenance

- Score written under
  `cases/product_learning/selflessbyhyram_target_entry_2023_v0/scores/01KV69GWSK85V5PVTECC0QM27Z.yaml`.
- Blind judgement under
  `runs/claude_sonnet_isolated_subagent_v0/run_001/blind_judgement.yaml`.
- Packet construction receipt:
  `packet_construction_receipt_v0.md` (outcome-blind build; R6 fix to
  memorization probe notice — moved from YAML frontmatter to Markdown body;
  JSG-05 isolation screen required per ledger).
