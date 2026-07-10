# Report Zero — Grade Against the Six D-1 Criteria

```yaml
retrieval_header_version: 1
artifact_role: Research record (rehearsal grade vs charter section 7 gate 3 — evidence lane, product_learning-capped; grades are self-assessed pending the criterion-5 round-2 cross-vendor return)
scope: >
  Grades the Report Zero dress rehearsal against the six ratified D-1 criteria,
  criterion by criterion, with the evidencing artifact named for each. Does NOT
  fire the gate: the criterion-5 ROUND-1 return was a blocker verdict
  (adjudicated and patched — see the round-1 adjudication record); criterion 5
  stays open pending a blocker/major-free round-2 return over the patched
  artifacts, and gate-firing is an owner call over the completed evidence.
use_when:
  - Preparing the owner decision on charter D-1 (foundation exit gate).
  - Adjudicating the delegated review return against this rehearsal.
authority_boundary: retrieval_only
open_next:
  - docs/research/report_zero/aphrodite_report_zero_sprint_report_v0.md
  - docs/prompts/reviews/report_zero_output_delegated_adversarial_artifact_review_prompt_v0.md
  - forseti/product/spines/creator_signal/aphrodite_carveout_charter_v0.md
stale_if:
  - The delegated review return is adjudicated (this grade then gains its criterion-5 result).
  - The charter D-1 criteria are amended.
```

## Grade table (criteria verbatim from charter §7 gate 3)

| # | Criterion | Grade | Evidence |
| --- | --- | --- | --- |
| 1 | All five panels rendered via the operator-runner transport (no API key) against a real captured creator | **EVIDENCED** | `aphrodite_report_zero_sprint_report_v0.md`: all five panels rendered for GentsScents from the frozen real corpus (15 videos, 53,749 words, 600 comments; corpus hash `0362007e…`). Transport = model-in-session hand-run under the versioned recipe, per the owner transport decision (2026-07-05, v1 handoff): **no API key, no daemon runner** used anywhere. |
| 2 | Fit panel fully DERIVED: every fit element resolves against `fragrance_reference_v0.yaml` coordinates; no operator-asserted fit facts — provable by mechanical scan | **EVIDENCED** (pending independent confirmation via criterion 5) | Every resolved fit fact in the claim records carries a `product_id` + the reference field used; tier facts cite the in-file rubric (ruling M1, provenance visible); note families come from the reference's accord-derived coordinates; mentions that do not resolve are routed to the REQUIRED `fit.unresolved_product_mentions` surface (~150+ products, coverage rate displayed) instead of being asserted. Mechanical scan: `grep -c "product_id" docs/research/report_zero/*.json` / every `"resolution": "resolved"` entry names its reference coordinates. |
| 3 | Provenance behavior end-to-end, including at least one honest withhold actually displayed | **EVIDENCED** | Seven withholds displayed in the shipped report, incl. the clone-tail block rendering the panel design's prescribed empty-graph text ("…This is not evidence of zero clone demand."), four single-cycle momentum withholds, the trajectory withhold, and the matched-reception-pair withhold. Every claim object carries the seven provenance fields + `provenance_state` — true per-claim only since the round-1 patch (AR-01), now proven by mechanical scan (30/30 corpus claims; 15/15 coded records with real 64-hex hash chains); receipts are verbatim `video_id@ms` / comment-ref quotes drilling back to the canonical lake packets via the corpus hash chain. |
| 4 | Candidate-set assembly rehearsed (register row R-3): buyer-side product-coordinate intake actually exercised, not stubbed | **EVIDENCED** | The hashed synthetic dupe-first intake (`aphrodite_report_zero_buyer_intake_v0.yaml`, `3adf664b…`) drove the fit chips, tier-position read, and both demand-space blocks; the report records the three things the intake needed that did not exist (empty dupe graph, no clone-house reference tail, no second capture cycle). Synthetic per the v1 handoff's owner-call option (b) — no waitlist buyer existed at dispatch; stated as synthetic throughout. |
| 5 | Cross-vendor adversarial review of the rehearsal output returns blocker/major-free | **ROUNDS 1–2 FAILED — patched; ROUND 3 PENDING** | Round 1 (GPT-5): blocker (AR-01..AR-06); all accepted and patched. Round 2 (GPT-5, over the patched commit): blocker — AR-04/AR-05 verified closed, but four residuals (AR-01a/b/c source_refs-units + receipt sweep + M2 reconstructability, AR-02 similarity wording, AR-03 hzq flanker material, AR-06 second occurrence); all four accepted and patched (captured_units embedded 30/30; full quote sweep from the cues substrate; exact M2 sums 176/39 from the comments substrate; hzq restructured; wording/count fixed). Every recomputation the round-2 reviewer ran PASSED (all 11 attention rows, totals, hash chains, tier distribution). See the round-2 section of `aphrodite_report_zero_review_round1_adjudication_v0.md`. Criterion 5 remains OPEN pending a blocker/major-free ROUND-3 return. |
| 6 | Bounded-effort receipt: reads/steps/time recorded, proving repeatability rather than a heroic one-off | **EVIDENCED** | `aphrodite_report_zero_run_log_v0.md`: recorded during the run — 15 videos / ~160 segments / 600 comments coded, timestamps (~9.2h wall incl. one interruption/resume), operator steps, seven named exceptions, and the speed-2 sizing read (reference-tail growth is the binding constraint, ahead of automation). |

## Honest misses and residuals (named, not waved away)

- **Criterion 5 is open — and round 1 FAILED it.** The round-1 cross-vendor
  review returned a blocker verdict; the review did exactly what it was
  commissioned to do (it caught real aggregation arithmetic errors, a
  coded-vs-corpus contradiction, and provenance-materialization gaps). All
  findings were adjudicated, accepted, and patched; the gate cannot be treated
  as fired until a ROUND-2 review over the patched artifacts returns
  blocker/major-free and is adjudicated by the home lane. All grades above are
  the authoring model's self-assessment until then.
- **Criterion 3's original evidence was overstated in one respect** (round-1
  AR-01): the seven provenance fields were carried at the record root, not per
  claim, and coded files lacked real hashes. Repaired and now mechanically
  verified (30/30, 15/15); named here rather than silently absorbed.
- **Resolved coverage is thin by design.** 11/16 reference products observed;
  <10% of the discourse resolves. The rehearsal *proves the mechanism* (derive,
  resolve, withhold) — it also proves reference v0's clone-house gap is the
  binding constraint on buyer value (the run log's speed-2 sizing point).
- **Momentum is empty.** Correctly withheld, but a real buyer's saturation
  question needs the second capture cycle (the grid clock).
- **The wall-clock includes interactive-session overhead** (one
  interruption/resume, operator conversation); a dedicated run would be
  faster — the receipt errs on the honest-slow side.

## What this rehearsal newly evidences beyond the gate mechanics

(`product_learning` only): the clone-economy decision the charter's lead lane
serves is *visible in the wild* on one creator — clone-target-selection
adjudication, saturation/timing analysis, audience dupe-petitions naming
originals, explicit review-gated purchases, and a live astroturfing callout
(polluted public ratings) that is the integrity-labeling use-case verbatim.

## Non-claims

Not validation, readiness, buyer proof, or willingness-to-pay evidence; not a
gate-firing claim (owner decision over completed evidence, after criterion 5);
`product_learning`-capped throughout. FLAG-1 (commercial use / data rights)
remains open and untouched, and carries into any Phase-1 scope conversation
per the ratified rider.
