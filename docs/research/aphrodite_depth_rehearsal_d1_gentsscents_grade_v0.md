# Aphrodite Depth Rehearsal - D-1 GentsScents Grade v0

```yaml
retrieval_header_version: 1
artifact_role: Research record (honest D-1 rehearsal grade and gate receipt; blocked at cross-vendor review)
scope: >
  Grades the GentsScents D-1 dress rehearsal against the Aphrodite charter's
  six D-1 criteria, records bounded-effort receipts and residual risks, and
  parks the gate at the required cross-vendor adversarial review.
use_when:
  - Checking the D-1 rehearsal status after reading the corpus, claim record, and panel projection.
  - Preparing or adjudicating the required cross-vendor adversarial review.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/creator_signal/aphrodite_carveout_charter_v0.md
  - docs/research/aphrodite_depth_rehearsal_d1_gentsscents_panel_projection_v0.md
  - docs/review-inputs/aphrodite_depth_rehearsal_d1_gentsscents_adversarial_review_input_v0.md
  - docs/review-outputs/adversarial-artifact-reviews/aphrodite_depth_rehearsal_d1_gentsscents_adversarial_artifact_review_v0.md
stale_if:
  - Cross-vendor adversarial review returns findings that require patching.
  - The D-1 charter criteria are amended.
```

## Status

`D1_REHEARSAL_PATCHED_AFTER_NOT_BLOCKER_MAJOR_FREE_REVIEW` - cross-vendor review returned 0 blockers and 4 majors. This artifact now records the home-lane patch response. D-1 has not fired.

## Criterion Table

| D-1 criterion | Status | Evidence |
|---|---|---|
| 1. All five panels rendered via operator-runner/no API against real captured creator | `OBSERVED_FOR_REHEARSAL` | GentsScents real captured corpus, 15 existing YouTube packet pairs, five panels rendered in `aphrodite_depth_rehearsal_d1_gentsscents_panel_projection_v0.md`. |
| 2. Fit fully derived; every fit element resolves against `fragrance_reference_v0.yaml`; no operator-asserted fit facts | `PATCHED_WITH_RESIDUALS_AWAITING_RECHECK` | Product-coordinate fit claims cite ontology reference coordinates; note-family chips are explicit; clone-tail withholds on empty `dupe_relationships`; unresolved tail is disclosed. Residual: SoV-derived fit rows still drill back to aggregate tables, not committed per-mention transcript receipts. |
| 3. Provenance behavior end-to-end including honest withhold | `PATCHED_WITH_RESIDUALS_AWAITING_RECHECK` | Claim record emits all required provenance fields on 30 claims; aggregate-only SoV drill-back is now named where it applies; withholds are explicit for dupe-tail, organic comparator, and momentum trend. |
| 4. Candidate-set assembly rehearsed | `PATCHED_FOR_STRUCTURED_SYNTHETIC_BUYER` | Buyer profile now includes structured intake fields and `intake_source_state` for the synthetic coordinates, including withheld occasion targets. |
| 5. Cross-vendor adversarial review blocker/major-free | `BLOCKED_REVIEW_RETURNED_MAJOR_FINDINGS_PATCH_RESPONSE_PREPARED` | Cross-vendor review report returned `NOT_BLOCKER_MAJOR_FREE` with 4 major findings. This patch response does not itself satisfy criterion 5; it needs cross-vendor recheck or explicit home-lane adjudication. |
| 6. Bounded-effort receipt | `OBSERVED_WITH_LIMITATION` | Reads, counts, steps, exceptions, and known count mismatches are recorded below. Exact wall-clock duration was not independently timer-instrumented, so this is an effort receipt, not a benchmark. |

## Grade

The D-1 rehearsal is mechanically promising but not gate-complete.

- Fit: useful but not decision-grade. Direct-original attention is real only at aggregate-table drill-back depth; clone-tail fit is withheld because the ontology has no dupe graph and the low-confidence tail matters to the buyer.
- Brand adjacency: useful for original-reference adjacency; insufficient for organic or clone-house adjacency.
- Purchase intent: strongest buyer-relevant signal in this slice. The 42 dupe/clone comments and 36 bought/bought-because comments matter, but product-resolution and full-thread coverage are not enough for a sold claim.
- Ad reception: commercially dense and link-bearing, but no matched organic comparator.
- Momentum: intentionally withheld beyond capture-window state.

## Bounded-Effort Receipt

Inputs read or consumed:

- Handoff: `docs/prompts/handoffs/aphrodite_depth_layer_build_handoff_v1.md`
- Charter: `forseti/product/spines/creator_signal/aphrodite_carveout_charter_v0.md`
- Panel design and provenance sources loaded through the handoff and overlay source-loading path.
- Recipe adjudication: `docs/research/aphrodite_recipe_v1_second_opinion_adjudication_v0.md`
- Round-2 GentsScents grade and SoV records.
- Ontology: `forseti/product/spines/foundation/ontology/fragrance_reference_v0.yaml`
- Existing raw packet set under `F:/orca-data-lake/raw` for the selected GentsScents videos.

Observed counts:

- 15 selected videos.
- 30 packet inputs in the current freeze: newest watch plus newest caption packet per video.
- 552,859 total views and 26,305 total likes in the current pass.
- 600 visible comments in the current parse; prior round-2 count 591 comments.
- 55,572 caption/transcript words in the current parse; prior round-2 count 53,749 transcript words.
- 85 affiliate links from the round-2 exact record.
- 417 raw product mentions, 415 after intra-video dedupe, 340 distinct products, and 55 low-confidence mentions in the round-2 SoV record.

Operator steps:

1. Loaded Orca overlay, fused skill, implementation-scoping, spec-writing, micro-decision-locking, prompt-orchestrator, and delegated-review-patch contracts.
2. Routed the work as a bounded D-1 rehearsal with a required review checkpoint.
3. Created isolated worktree `codex/aphrodite-d1-depth-rehearsal` from source branch `claude/recipe-v1-second-opinion-adjudication`.
4. Froze the 15-video GentsScents corpus from existing raw packets.
5. Authored recipe v1, corpus receipt, claim record, panel projection, and this grade.
6. Prepared the cross-vendor adversarial review input.
7. Recorded the cross-vendor review report at `docs/review-outputs/adversarial-artifact-reviews/aphrodite_depth_rehearsal_d1_gentsscents_adversarial_artifact_review_v0.md`.
8. Patched the target artifacts for AR-01 through AR-06 without claiming D-1 passage.

Exceptions and residuals:

- The accepted recipe-v1 adjudication has a 29-vs-30 claim-count discrepancy; this run emits all 30 appendix claim types and records the discrepancy.
- Current raw count and prior round-2 count differ for comments and words; both are disclosed.
- Initial broad raw-lake search was too noisy for binding use; the run switched to selected packet inspection.
- Current crude URL regex over-counted malformed snippets, so the grade uses the round-2 exact affiliate-link count.
- The SoV output is a research record, not a durable product mention silver lane.
- Per review AR-01, SoV-derived fit rows still drill back only to aggregate tables in this branch; per-mention transcript receipts must be recovered or re-derived for full provenance closure.
- Cross-vendor review is available only through a genuinely decorrelated reviewer; same-family review remains insufficient.

## Cross-Vendor Review Response

Review report: `docs/review-outputs/adversarial-artifact-reviews/aphrodite_depth_rehearsal_d1_gentsscents_adversarial_artifact_review_v0.md`.

| Finding | Home-lane disposition |
|---|---|
| AR-01 aggregate-only fit receipts | Accepted. SoV-derived fit rows are downgraded or explicitly limited to aggregate-table drill-back; no missing per-mention receipts are fabricated. |
| AR-02 silent note-family drops | Accepted with correction. All 10 buyer target note families are explicit chips. They are not marked absent because direct originals carry those note coordinates; they are marked aggregate-receipt-only. |
| AR-03 tier row too broad for `show` | Accepted. Row is downgraded and narrowed to top-8 tier view plus buyer-anchor tier comparison; it is not the full ratified distribution. |
| AR-04 flat buyer intake | Accepted. Structured synthetic intake with `intake_source_state` is now encoded in the claim record. |
| AR-05 lane convention ambiguity | Resolved here: plain `workflow-adversarial-artifact-review` is the criterion-5 vehicle for a no-patch cross-vendor evidence review; `workflow-delegated-review-patch` is reserved for a commissioned patch lane. |
| AR-06 creator-choice traceability | Accepted. Corpus receipt now records owner-locked GentsScents creator choice. |

## Next Gate

Run a cross-vendor post-patch recheck, or have the home lane explicitly adjudicate this patch response against the review report. Only after blocker/major-free review or accepted adjudication can criterion 5 be marked observed. Until then, any claim that D-1 fired is false.

## Non-Claims

- Not D-1 passage, readiness, validation, buyer proof, or commercial-use clearance.
- Not a build of a runner, crawler, data lake lane, or UI surface.
- Not a recommendation to contact buyers or resolve FLAG-1.
