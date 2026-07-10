# Report Zero — Grade Against the Six D-1 Criteria

```yaml
retrieval_header_version: 1
artifact_role: Research record (rehearsal grade vs charter section 7 gate 3 — evidence lane, product_learning-capped; grades are self-assessed pending the criterion-5 cross-vendor return)
scope: >
  Grades the Report Zero dress rehearsal against the six ratified D-1 criteria,
  criterion by criterion, with the evidencing artifact named for each. Does NOT
  fire the gate: criterion 5 is parked pending the couriered cross-vendor
  review return, and gate-firing is an owner call over the completed evidence.
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
| 3 | Provenance behavior end-to-end, including at least one honest withhold actually displayed | **EVIDENCED** | Seven withholds displayed in the shipped report, incl. the clone-tail block rendering the panel design's prescribed empty-graph text ("…This is not evidence of zero clone demand."), four single-cycle momentum withholds, the trajectory withhold, and the matched-reception-pair withhold. Every claim object carries the seven provenance fields + `provenance_state`; receipts are verbatim `video_id@ms` / comment-ref quotes drilling back to the canonical lake packets via the corpus hash chain. |
| 4 | Candidate-set assembly rehearsed (register row R-3): buyer-side product-coordinate intake actually exercised, not stubbed | **EVIDENCED** | The hashed synthetic dupe-first intake (`aphrodite_report_zero_buyer_intake_v0.yaml`, `3adf664b…`) drove the fit chips, tier-position read, and both demand-space blocks; the report records the three things the intake needed that did not exist (empty dupe graph, no clone-house reference tail, no second capture cycle). Synthetic per the v1 handoff's owner-call option (b) — no waitlist buyer existed at dispatch; stated as synthetic throughout. |
| 5 | Cross-vendor adversarial review of the rehearsal output returns blocker/major-free | **PARKED — commissioned, return pending** | Commission authored (`report_zero_output_delegated_adversarial_artifact_review_prompt_v0.md`) + 24-file zip source pack built; requires an external non-Anthropic controller couriered by the owner. Per the v1 handoff: the rehearsal parks at criterion 5 with 1–4 + 6 evidenced; a same-family self-review is NOT substituted. |
| 6 | Bounded-effort receipt: reads/steps/time recorded, proving repeatability rather than a heroic one-off | **EVIDENCED** | `aphrodite_report_zero_run_log_v0.md`: recorded during the run — 15 videos / ~160 segments / 600 comments coded, timestamps (~9.2h wall incl. one interruption/resume), operator steps, seven named exceptions, and the speed-2 sizing read (reference-tail growth is the binding constraint, ahead of automation). |

## Honest misses and residuals (named, not waved away)

- **Criterion 5 is open.** The gate cannot be treated as fired until the
  couriered review returns blocker/major-free and is adjudicated by the home
  lane. All grades above are the authoring model's self-assessment until then.
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
