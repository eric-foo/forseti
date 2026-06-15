# First By-Hand Demand Read — Findings + Grade v0 (Topicals retail-expansion, enriched read)

```yaml
artifact_role: Findings + grade record for the demand-read lane's first honestly-graded by-hand C0–C4 read
case_id: topicals_retail_expansion_2021_v0
packet_variant: enriched_v0
cutoff: 2021-03-15
claim_cap: product_learning  # N=1; not validation, not judgment-quality, not buyer-proof
case_status: GRADED  # outcome recorded here, but NOT burned: a fresh blind lane that does NOT read this findings doc or the sealed-outcome file can still reuse the participant packet.
read_count: 1        # increment per graded read; prefer less-famous cases for re-reads (Topicals is recognition-prone)
authority_boundary: retrieval_only
```

## What this is

The grade of the demand-read lane's **first** end-to-end by-hand read of the new qualitative C0–C4
core on **real ≤cutoff data**, run outcome-blind in an isolated session against the frozen enriched
packet (`participant_packet_enriched_v0.md`, sha256 `eec447a4…`), then graded by a delegated
outcome-aware grader (JSG-08 reveal + tell-audit). This is the lane's first-earned-trust artifact.

## The sealed call (outcome-blind contestant)

- **demand_state_verdict:** TRANSIENT (given real) — basis: no observed post-trigger persistence in the packet.
- **action_ceiling:** HOLD / low-commitment (time-boxed pilot at most); NOT broad commit.
- **C1 gate:** CAPPED — 1 independent origin (Nordstrom, placement-only, zero independent volume); first-party PDP reviews = floor, not independent origin; <2 independent converging origins.
- **C2:** de-correlated E6–E10 as same-origin (brand's own site); flagged sold-out as ambiguous (thin inventory/ops-immaturity vs. excess demand); tied the open Supply Chain Manager role to the E4 execution risk.
- **C4 counterfactual:** a 2nd independent costly-behavior origin with gradeable volume (third-party reviews / community at scale / Nordstrom sell-through) converging + observed persistence + demonstrated operational readiness would justify a bigger move.
- **recognition:** recognized the brand; attested no non-packet knowledge used.

## The outcome (revealed at grade)

Demand proved **durable** and the broad-retail move **won**: ~8 days after the cutoff the brand
entered Sephora (Accelerate program), reportedly tripled sales in 2021, was branded the
"fastest-growing skincare brand at Sephora," raised a $10M Series A (2022-11), scaled
internationally, and was still an established Sephora brand at its 2025 five-year mark.
*(Growth multiples are company-disclosed/PR figures, directional, not audited.)*

## The grade (four axes)

| Axis | Result |
| --- | --- |
| **Verdict (transient)** | **Correct-given-evidence, but outcome differed.** The demand was durable, so the label was wrong about the world — but the packet carried no persistence signal to observe, so transient-as-floor was the method-faithful call. The epistemic state ("I have not seen persistence") was accurate. |
| **Ceiling (hold)** | **Appropriate given the evidence** — driven by a real evidence gap (1 placement-only independent origin, no persistence, live ops-execution risk), not by misreading present evidence. Not "too conservative" (no missed lift signal). Honest cost: it left the real upside on the table. |
| **Evidence-defensibility** | **PASS — no missed ≤cutoff lift signal.** Every signal handled correctly (first-party floor, Nordstrom placement-only, sold-out ambiguity, SCM ops-risk). The upside was real but not yet visible at the cutoff. |
| **C4 quality** | **High — named the real driver.** The actual move was justified post-cutoff by exactly what C4 said to look for: independent retail demand at scale (Sephora sell-through) + sustained scaling (persistence) + closing the ops gap. |
| **JSG-08 tell-audit** | **CLEAN.** The read resolved every ambiguity *against* the known-successful outcome (anti-tells); no assertion of the outcome, no non-packet knowledge used to resolve ambiguity. The no-contamination attestation is verified despite brand recognition. |

## What this read DOES and DOES NOT demonstrate (N=1)

- **Earned (process integrity):** the method's discipline **held under a known-and-tempting answer**.
  A contestant who recognized a now-famous success still produced a conservative, evidence-bounded
  call that ran against the outcome at every ambiguous fork — strong evidence that the
  transient-default and C1/C2 gating do real epistemic work rather than rationalizing a known
  result. Tell-audit genuinely clean; C4 calibrated to the real driver.
- **NOT earned (outcome-accuracy):** the headline call (TRANSIENT / HOLD) was **wrong about the
  world** — the demand was durable and the broad move won. The method optimizes for "defensible
  given evidence," not "right about the future"; this case is a clean example of the two coming
  apart.
- **Named structural limitation (now demonstrated, not theoretical):** the method's conservatism
  **misses upside on genuinely under-evidenced winners** — a young brand pre-catalyst, judged on
  thin ≤cutoff evidence, gets capped at hold even when it is about to break out. Here the decisive
  catalyst (the Sephora deal) was ~8 days future and invisible at the cutoff. This is the method's
  designed cost (false-positive resistance traded for missed under-evidenced upside), to be carried
  forward as an accepted limitation, not papered over.

## Non-Claims

- `product_learning`, N=1. Not validation, not judgment-quality (needs N≥K + reveal/calibration),
  not buyer-proof. One honestly-graded read demonstrates process integrity on one case, not method
  accuracy. The growth figures in the outcome are PR-sourced and directional.
- The outcome is recorded here, but the case is **NOT burned**: reuse is preserved for any fresh blind
  lane that does not read this findings doc or the sealed-outcome file. Track reuse via `read_count`;
  prefer less-famous cases for re-reads (Topicals is recognition-prone).

## Owner refinement (2026-06-15) — grade the calling sequence, not the outcome label

The owner corrected the grade's framing: **calling TRANSIENT at t=0 was correct, not "wrong about the
world."** Per the calling sequence, demand *starts* transient and earns *durable* only via observed
post-trigger monitoring. The demand here did exactly that (transient at cutoff → durable after the
catalyst). A **single backtest read structurally cannot perform the monitoring step** (no post-trigger
window), so it can never earn durable — meaning the transient call is the correct *and complete* call a
t=0 read can make; "wrong about the world" mis-applies the rubric. **HOLD was the right action on the
packet's evidence** (the real actor committed broadly because they held the Sephora deal — information
not in the packet). Distillation for the judgment lanes: grade demand reads on **(1) calling-sequence
faithfulness** (correctly default transient; would monitoring have earned the durable upgrade) and
**(2) action-appropriateness-given-evidence** — **not** outcome-label-match. Full distillation deferred
to the case deep-dive.
```text
This is a graded first-read findings record. It is product-learning evidence about method process
integrity on one case — not validation, readiness, or buyer proof.
```
