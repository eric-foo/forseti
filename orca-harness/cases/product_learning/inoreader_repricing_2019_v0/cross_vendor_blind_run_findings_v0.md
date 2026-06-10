# Cross-Vendor Blind-Run Findings — inoreader_repricing_2019_v0

**Status: product-learning observation record. NOT distilled.**
This document records observed facts from one by-hand exam run. It derives **no**
harness changes, method changes, promoted lessons, or judgment-quality claims.
Distillation is deferred until any finding here is proven (i.e., replicated
beyond a single case under proven — not instructed/attested — isolation). Every
result below is a product-learning observation, not a validated conclusion.

- Case: `inoreader_repricing_2019_v0`
- Harness: `v0_14`
- Recorded: 2026-06-10
- Frozen scoring key (facilitator ledger) freeze hash:
  `b580099d4c453b7b1ad205a33d300a1f799072b948591fd284650c2ea2890c46`

---

## 1. Scope and cap

This is a by-hand product-learning exercise that **uses** the harness; it is not
a judgment-quality run. Specifically:

- Contestant isolation was **instructed/attested**, not structurally proven
  (sub-agent for one run; external paste + self-attestation for the rest).
- The scorer's `memorization_probe_result` is hardcoded `not_run`; the
  recognition signal lives only in each contestant's self-report, held outside
  the score.
- The frozen band inputs were facilitator-set and owner-ratified, not
  independently derived.

No JSG gate is cleared or advanced by this record. JSG-01 remains frozen.

## 2. Exam setup

- **Decision question:** at the 2019-02-06 cutoff, how aggressively should
  Inoreader gate power-user Rules automation into higher paid tiers
  (watch / hold / narrow / phase-in / commit-aggressive), on pre-cutoff evidence
  only.
- **Action ladder:** 0 abstain, 1 wait, 2–5 graduated recommend, 6 escalate,
  7–8 aggressive recommend (`recommend` must use {2,3,4,5,7,8}).
- **Calibrated band from the frozen key: [4, 5].** Floor 4 is driven by
  `option_value: high` (`OPTION_VALUE_FLOOR["high"] = 4`); ceiling 5 by
  `evidence_strength: moderate` with `evidence_independence: partially_independent`
  (`BASE_CEILING["moderate"] = 5`, delta 0). Other inputs (loss_shape
  asymmetric_down, reversibility_feasibility high, authority/capability full, etc.)
  did not bind below 5 / above 4.
- **Held outcome (revealed only for the hindsight pass):** Feb 2019 Inoreader
  repackaged with aggressive gating of Rules below the top tier → immediate user
  backlash → partial walk-back within days (loosened allowances, grandfathering).
  The aggressive end of the ladder was punished; both narrow (3) and moderate (4)
  avoided the rupture.

## 3. Clean blind runs (scored)

| contestant | vendor / family | call | vs band [4,5] | recognition (self-report) | isolation basis | score id |
|---|---|---|---|---|---|---|
| `claude_sonnet_isolated_subagent_v0` | Anthropic | **3** | under by 1 | partial product / outcome unknown | sub-agent, `tool_uses=0` verified | `01KTRSD5PRX3E7J7H6HX470AGF` |
| `gpt_5_5_isolated_external_v0` | OpenAI | **4** | in-band | recognized product / outcome unknown | external, attested | `01KTRW0Y0K56HV4CEVD8FFPVSM` |
| `grok_4_isolated_external_v0` | xAI | **3** | under by 1 | **none / outcome unknown** | external, attested | `01KTRX9N9GQHAHQ509JCX1B0YW` |

All three passed evidence-id checks (presence, pre-decision status, load-bearing
citation) and must-address coverage (MA-01…MA-05). The Claude run logged one
underreach failure event; the GPT run logged none. Band status `normal`,
width 1, in every case.

Assembly note: `grok` supplied an invalid `decision_shape: narrow_phase_in`
(not an enum value); normalized to `action_band` on assembly. The substantive
call (`ladder_level: 3`) was not altered.

## 4. Excluded run (contaminated)

| contestant | vendor | blind call | reason excluded |
|---|---|---|---|
| Gemini | Google (owner-confirmed) | 4 | `believe_know_outcome: true` — self-reported knowing the actual outcome, including the grandfathering walk-back, before the hindsight pass |

The Gemini run also self-reported its model identity as "Claude 3.5 Sonnet"
(identity confabulation; owner confirms it was Gemini). It was **not scored** and
is excluded from the clean set: an outcome-aware contestant is not a blind
contestant. Its recommendation leaned on grandfathering — the actual walk-back
mechanism — consistent with outcome leakage into the reasoning.

## 5. Observations (stated as observed; no prescription)

1. **Anti-over-reach replicated across three vendors.** Every clean contestant
   (Anthropic, OpenAI, xAI) rejected aggressive gating (7–8) and landed
   conservative/moderate (3–4), each leaning on the E3/E4 backlash base rate,
   MA-04 (no internal tolerance data), and E5 (accepted WTP band ≠ acceptance of
   aggressive gating).

2. **The under-band result is shared, not model-specific.** Two of three clean
   models (Claude and Grok) landed at 3, below the band floor of 4. An earlier
   in-session claim that the underreach was "Claude-specific / the key is
   validated" was based on Claude vs GPT only and is **withdrawn**: Grok — the
   cleanest contestant (zero recognition) — also landed at 3. The band floor [4]
   is contested by independent blind judges.

3. **Recognition correlated with a higher call (N=4, suggestive only).**
   Ordered by recognition: Gemini (knew outcome)=4, GPT (knew product)=4,
   Claude (partial)=3, Grok (none)=3 — monotonic. The real outcome settled near
   moderate-with-grandfathering (≈4), so this is consistent with recognition
   pulling calls upward toward the actual outcome. Not proven; small N.

4. **The "obscure case" leakage control was inadequate; the recognition probe
   caught it.** One frontier model fully recalled the outcome despite the
   ledger's `known_fame_risk: low_fame_obscure_case`. The contestant's recognition
   self-report is what surfaced the contamination.

5. **The hindsight-extraction pass did not function as error-correction on this
   case.** Two hindsight passes were run (Gemini, Grok) critiquing the Claude
   level-3 call against the revealed outcome:
   - Neither was seduced into the wrong direction (neither said "should have been
     *more* cautious").
   - Neither moved off its own blind prior (`own_view_movement: moved=no` for
     both). Each hindsight verdict mirrored the critiquing model's own blind call:
     Gemini (blind 4) → "under-reach, go to 4"; Grok (blind 3) → "well-calibrated
     at 3."
   - The one "under-reach" diagnosis (Gemini) was contaminated.
   Observed result: the hindsight pass restated each model's prior rather than
   surfacing a catchable factor a model would not already use blind.

## 6. What remains unproven / open

- **Band floor [4] vs clean-modal call 3.** Whether `option_value: high` is the
  right input (it forces floor 4) or whether clean-blind models share a
  conservative lean is unresolved. The key was facilitator-set; JSG-01 frozen.
  (No change made here.)
- **Single case.** All of the above is N=1 case, 3 clean runs. None of it
  generalizes without replication.
- **Recognition→call pattern** is N=4 and suggestive only.
- **Hindsight method** is inconclusive-to-negative on this case; not demonstrated
  to add value, not demonstrated useless in general.
- **Packet steer (known confound).** The participant packet's "Known
  Uncertainties" names E3/E4/E5 as the possibly-decisive base rate, and the
  must-address rubric (esp. MA-02) leans conservative. This was held **constant**
  across all clean runs, so it does not confound the cross-vendor *comparison*,
  but it remains a confound for any *absolute* calibration claim.
- **Isolation was attested, not proven**, for the external runs; the scorer's
  memorization probe is hardcoded `not_run`.

## 7. Explicitly not concluded here

- No harness change, schema change, packet redesign, or scorer change is derived
  or recommended in this record.
- No band-input (scoring key) change is made or proposed; the contested floor is
  logged as an open question only.
- No judgment-quality, readiness, or method-validation claim is made.
- The cross-vendor convergence is a product-learning observation, not proof that
  the method produces defensible judgment.

## 8. Provenance

- Scores written under `cases/product_learning/inoreader_repricing_2019_v0/scores/`:
  `01KTRSD5PRX3E7J7H6HX470AGF` (claude), `01KTRW0Y0K56HV4CEVD8FFPVSM` (gpt),
  `01KTRX9N9GQHAHQ509JCX1B0YW` (grok).
- Blind judgements under `runs/<contestant>/run_001/blind_judgement.yaml`.
- External-run `temperature` recorded as `1.0` is an **unverified** interface
  default (not reported by the contestants).
- All artifacts in this case directory are uncommitted at time of writing.
