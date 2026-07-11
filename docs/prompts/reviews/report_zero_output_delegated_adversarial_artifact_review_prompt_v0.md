# Delegated Adversarial Artifact Review — Report Zero Rehearsal Output (D-1 criterion 5)

```yaml
retrieval_header_version: 1
artifact_role: Review prompt (delegated cross-vendor adversarial artifact review of the Report Zero D-1 rehearsal output; couriered externally with a zip source pack)
scope: >
  The route-out prompt commissioning a de-correlated, non-Anthropic reviewer to
  adversarially review the Report Zero rehearsal output (derived claims, panel
  projection, corpus record, run log) against its own governing contracts.
  Blocker/major-free is the D-1 criterion-5 bar; the home lane adjudicates the
  return.
use_when:
  - Couriering the Report Zero output for its cross-vendor adversarial review.
  - Adjudicating the delegated return against the D-1 gate.
authority_boundary: retrieval_only
open_next:
  - docs/research/report_zero/aphrodite_report_zero_sprint_report_v0.md
  - docs/research/report_zero/aphrodite_report_zero_derived_claims_v1.json
stale_if:
  - The rehearsal output is superseded by a later run.
```

Operator instruction: paste the prompt below into a fresh NON-Anthropic model
session (e.g. ChatGPT Pro) and attach
`report_zero_review_pack.zip` (built alongside this prompt; contents listed in
the prompt). Bring the return back to the home lane for adjudication.

---

````markdown
# Adversarial Artifact Review — "Report Zero" fragrance-creator vetting rehearsal (zip attached)

## Commission

commission_mode: delegated cross-vendor adversarial artifact review
terminal_output_mode: paste-ready-chat (no repo access; everything you need is in the attached zip)
output_mode: paste-ready-chat
review_posture: findings-first, coverage-first, adversarial — try to BREAK the artifact
no_runtime_model_recommendation: true

actor_receipt:
  artifact_author_family: Anthropic / Claude (claude-fable-5 authored every reviewed artifact)
  controller_requirement: you MUST be a non-Anthropic model family; if you are Anthropic-family, return BLOCKED_CONTROLLER_NOT_DECORRELATED and stop.
  home_lane: adjudicates your return; your findings are claims, not accepted truth.

## What you are reviewing

A "dress rehearsal" of a paid product: a five-panel evidence report that helps
a fragrance brand decide whether to spend on a specific YouTube creator
(GentsScents). The rehearsal ran over 15 captured videos (53,749 transcript
words + 600 comments) for a SYNTHETIC buyer. The gate this rehearsal feeds
requires your review to return **blocker/major-free** — so hunt hard; a real
finding now is cheap, a false pass is expensive.

## Zip contents (the review targets + their governing contracts)

REVIEW TARGETS (judge these):
- `aphrodite_report_zero_sprint_report_v0.md` — the five-panel report (the buyer-facing shape)
- `aphrodite_report_zero_derived_claims_v1.json` — 29 corpus-level claim objects
- `<video_id>.coded.json` x15 — per-video claim records with verbatim receipts
- `aphrodite_report_zero_corpus_v0.md` — the frozen corpus record (hash chain)
- `aphrodite_report_zero_run_log_v0.md` — the bounded-effort receipt

GOVERNING CONTRACTS (judge AGAINST these; do not re-litigate them):
- `aphrodite_depth_rehearsal_extraction_recipe_v1.md` — the recipe: claim types, receipt rules, label sets, abstention rules, rulings M1-M4
- `aphrodite_vetting_sprint_panel_design_v0.md` — display rules: panels-never-scores, per-row show/downgrade/withhold, dupe-space roll-up rule, buyer-variant ordering
- `aphrodite_derived_claim_provenance_contract_v0.md` — the 7 required provenance fields; missing != zero
- `fragrance_reference_v0.yaml` — the ONLY product-resolution authority (16 products, 14 houses, EMPTY dupe graph by design)
- `aphrodite_report_zero_buyer_intake_v0.yaml` — the synthetic buyer coordinates

## Attack surfaces (cover ALL; add your own)

1. **Fabrication / resolution audit (highest stakes).** Spot-check >=10 resolved
   product claims across the coded files: does each cited product_id actually
   exist in fragrance_reference_v0.yaml, and do the note_families/tier facts the
   report uses match the reference verbatim? Any resolved claim whose product is
   NOT in the reference = blocker. Any invented reference coordinate = blocker.
2. **Receipt integrity.** Receipts must be verbatim-quote + video_id@ms (or
   comment ref + like count). Sample receipts across videos: are any paraphrases
   dressed as quotes, or aggregate claims citing "the whole video"?
3. **Operator-assertion leak (gate criterion 2).** The fit panel claims ZERO
   operator-asserted fit facts. Hunt for any fit fact (tier, note family,
   segment share) that does NOT trace to a reference coordinate or a receipt.
4. **Withhold honesty.** The empty dupe graph must render as the prescribed
   honest-absence text (never as zero clone demand); momentum must withhold on a
   single cycle; matched reception pairs must withhold with no organic class.
   Any faked trend, any zero-filled absence, any single blended "score" =
   blocker (panels-never-scores).
5. **Rulings M1-M4 applied?** M1: tier facts render show with rubric provenance
   (not auto-downgraded). M2: engagement-weighted support shows raw count and
   like-sum as TWO numbers, never blended. M4a: within-window baselines allowed,
   cross-cycle claims not. M4b: view-allocation method disclosed on-panel.
6. **Person-level boundary.** No commenter identities, no demographics, no
   per-commenter claims; comment authors were dropped at normalization — verify
   nothing leaks back in.
7. **Overclaim in the decision read.** The report's final read must stay inside
   the evidence (and inside product_learning): does any sentence imply
   validation, buyer proof, momentum, or "pay this creator" beyond what the
   panels support? Does the synthetic-buyer disclosure survive everywhere?
8. **Internal consistency.** Do the corpus-level numbers (views, counts,
   attention shares, intent totals) reconcile with the per-video files? Recompute
   at least: total views, the 51% Sauvage attention-share claim, and one intent
   total.
9. **ASR-garble handling.** Clone-house names were ASR-garbled (Hawas/Has,
   Rasasi/Rasi). Check the coded files' garble notes: is anything resolved on a
   guess rather than a title/description anchor?

## Verdict + return contract

Return, in order:
- `review_summary` YAML: {verdict: blocker|major|minor|clean, counts by severity, fabrication_check: pass|fail, confidence}
- Findings ordered by severity; each with: the file + JSON path/section, the
  exact defect, why it matters against which contract, and the minimum fix.
- Your recomputations (surface 8) with numbers.
- Residual-risk note: what you could NOT verify from the zip (e.g. you cannot
  reach the underlying lake packets — say so; do not guess).
- Adjudication note: your findings are claims for the home lane to adjudicate,
  not accepted truth.

Do not rewrite the artifacts. Do not review the strategy (whether this product
should exist). Do not recommend runtime models. Findings only.
````
