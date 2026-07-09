# Cross-Vendor Blind-Run Findings — nueco_fragrance_pivot_v0 (contestant-facing case_id: b2_holdout_h7_v0)

**Status: product-learning observation record. NOT distilled.**
This document records observed facts from one by-hand exam run. It derives **no**
harness changes, method changes, promoted lessons, or judgment-quality claims.
Distillation is deferred until any finding here is proven (replicated beyond a single
case under proven — not instructed/attested — isolation). Every result below is a
product-learning observation, not a validated conclusion.

- Case (real): `nueco_fragrance_pivot_v0` (The Nue Co. — Batch 2 owner-included 7th holdout)
- Contestant-facing case_id (neutralized): `b2_holdout_h7_v0`
- Harness: `v0_14`
- Recorded: 2026-06-16 (slice 2)
- Frozen scoring key (facilitator ledger) freeze hash:
  `a9150d51b5150a4b2e69f93b335494cc1fce1058cf5bae9cf885be609e6a54c4`

---

## 0. Why this record exists (anti-cherry-pick gap closure)

nueco is the 7th pre-committed holdout in the signed Batch 2 ledger. Slice 1 (#172)
ran 6 of the 7 holdouts and **silently dropped nueco** (captures only; no packet, run,
findings, or recorded exclusion). Leaving a pre-committed case silently un-run voids the
batch's anti-cherry-pick property. This slice closes that gap: nueco was run on the full
pipeline (outcome-blind packet → blind Sonnet run → score → this findings record) and is
reported here **whatever it scored**. nueco was found feasible (7 body-verified pre-cutoff
captures, no real blocker), so it was run (option i), not documented-excluded (option ii).

## 1. Scope and cap

By-hand product-learning exercise that **uses** the harness; not a judgment-quality run.
- Contestant isolation was **instructed/attested**, not structurally proven (sub-agent,
  `tool_uses=0`, web-off by instruction). External arms not run (Claude-Sonnet arm only).
- The scorer's `memorization_probe_result` is hardcoded `not_run`. **Recognition WAS
  collected** at run time (see §3 tell-audit) given this brand's elevated fame risk.
- The frozen band inputs were **facilitator-adopted verbatim from the outcome-blind
  builder's structural read**; owner ratification is pending.
No JSG gate is cleared or advanced by this record.

## 2. Exam setup

- **Decision question (blind-framed, symmetric):** at the start of 2020, should The Nue
  Co. prioritise deepening its DTC subscription model, or redirect toward broadening the
  product range and/or expanding into new channels/geographies, or some combination?
- **Action ladder:** 0 abstain, 1 wait, 2–5 graduated recommend, 6 escalate, 7–8
  aggressive recommend (`recommend` uses {2,3,4,5,7,8}).
- **Calibrated band from the frozen key: [3, 5], band_status: normal (width 2).**
  Moderate evidence (`BASE_CEILING["moderate"]=5`), partially-independent (delta 0 →
  ceiling 5), capped to 5 by `capability: partial` / `capability_build_cost: medium`
  caps; floors of 3 driven by `opportunity_cost: moderate`, `information_decay: fast`,
  `option_value: moderate`, `upside_shape: asymmetric_up`, `urgency: medium`, dampened to
  floor 3. No floor>ceiling conflict → normal band [3,5].
- **Held outcome (revealed only for the hindsight pass; roster-stated, not independently
  verified here):** after the 2020-01-01 cutoff the brand pivoted to fragrance-first —
  fragrance grew from ~20% to ~65% of revenue, CAC roughly halved, an Ulta exclusive was
  entered. The cutoff itself (2020-01-01) is a defensible supplements-led-era anchor with
  real date uncertainty; the brand is a US/UK BORDER case treated as US-market.

## 3. Clean blind run (scored)

| contestant | vendor / family | call | vs band [3,5] | recognition (self-report) | isolation basis | score id |
|---|---|---|---|---|---|---|
| `claude_sonnet_isolated_subagent_v0` | Anthropic (claude-sonnet-4-6) | **4** | **in-band** | recognized brand = yes; attested no post-2020 info used | sub-agent, `tool_uses=0` | `01KV7SZFJHV14G0C6HG65204YF` |

The run passed evidence-id presence, pre-decision status, load-bearing citation, and
must-address coverage (MA-01…MA-03). No failure events. The contestant reported
`decision_shape: action_band`, `ladder_level: 4`, claimed band [4,5] — consistent with
the calibrated [3,5].

### JSG-08 tell-audit

- Recognition self-report: **yes** (recognized the brand), with an explicit attestation
  that no post-2020 information influenced the answer.
- Outcome-USE test: the contestant's recommendation was to **hold the product range,
  protect the gut-health core, and deepen the subscription relationship** — i.e. the
  near-**opposite** of the actual held outcome (a pivot INTO a new product category,
  fragrance, that became the revenue majority). There is no sign the held outcome leaked
  into the answer; if anything the answer diverges from it.
- Disposition: **recognition recorded as data; not quarantined** (contamination = demonstrated
  outcome-USE; none evident here).

## 4. Observations (stated as observed; no prescription)

1. **In-band (4 in [3,5]).** The Claude-Sonnet contestant's graduated-action call fell
   inside the calibrated band — a decision-quality "pass" on this case for this arm.
2. **In-band but opposite to hindsight.** The decision-quality band rewards a moderate,
   focus-protecting action given the evidence; the real winning move (a category pivot
   into fragrance) was NOT identifiable from the pre-cutoff DTC evidence and is not what
   the band scores. The contestant explicitly recommended against new-category extension.
   This is the most diagnostic fact: in-band ≠ predicted-the-future, by design.
3. **Recognition without evident use.** Unlike the slice-1 cases (no recognition data
   collected), recognition was captured here; the contestant recognized the brand yet
   produced an answer diverging from the known outcome.
4. **Single-contestant, N=1.** Whether this generalizes requires the external arms.

## 5. What remains unproven / open

- **Cross-vendor comparison** not available (GPT-5.5, Grok 4, Gemini not run; owner-executed).
- **Band inputs** were adopted from the outcome-blind builder's structural read; owner
  ratification pending. Whether `evidence_strength: moderate` (vs `weak`) is the right
  calibration for a forward capital-allocation call on DTC-surface-only evidence is a
  legitimate open facilitator question.
- **Cutoff-date uncertainty (2020-01-01)** and **BORDER US/UK** status are real limits.
- **Memorization** structurally unprobed (recognition self-reported only).

## 6. Explicitly not concluded here

- No harness change, schema change, packet redesign, or scorer change.
- No band-input (scoring key) change is made or proposed.
- No judgment-quality, readiness, or method-validation claim.

## 7. Provenance

- Score: `cases/product_learning/nueco_fragrance_pivot_v0/scores/01KV7SZFJHV14G0C6HG65204YF.yaml` (gitignored).
- Blind judgement: `runs/claude_sonnet_isolated_subagent_v0/run_001/blind_judgement.yaml`.
- Case report: `reports/product_learning/b2_holdout_h7_v0/case_report.yaml` (keyed by the
  neutralized case_id).
- Packet construction receipt: `packet_construction_receipt_v0.md` (outcome-blind build;
  neutralized bodies-only capsule; band adopted verbatim from the blind structural read).
- Neutral↔real mapping: `b2_holdout_h7_v0` = `nueco_fragrance_pivot_v0`.
