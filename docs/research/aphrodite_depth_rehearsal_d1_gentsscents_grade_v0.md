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
stale_if:
  - Cross-vendor adversarial review returns findings that require patching.
  - The D-1 charter criteria are amended.
```

## Status

`D1_REHEARSAL_PARKED_AT_CRITERION_5` - the artifacts are ready for the required review checkpoint. D-1 has not fired.

## Criterion Table

| D-1 criterion | Status | Evidence |
|---|---|---|
| 1. All five panels rendered via operator-runner/no API against real captured creator | `OBSERVED_FOR_REHEARSAL` | GentsScents real captured corpus, 15 existing YouTube packet pairs, five panels rendered in `aphrodite_depth_rehearsal_d1_gentsscents_panel_projection_v0.md`. |
| 2. Fit fully derived; every fit element resolves against `fragrance_reference_v0.yaml`; no operator-asserted fit facts | `OBSERVED_WITH_RESIDUALS` | Shown/downgraded product-coordinate fit claims cite ontology reference coordinates; clone-tail withholds on empty `dupe_relationships`; unresolved tail is disclosed. Residual: SoV extraction is rehearsal-grade, not durable silver-lane output. |
| 3. Provenance behavior end-to-end including honest withhold | `OBSERVED_FOR_REVIEW` | Claim record emits all required provenance fields on 30 claims; withholds are explicit for dupe-tail, organic comparator, and momentum trend. |
| 4. Candidate-set assembly rehearsed | `OBSERVED_FOR_SYNTHETIC_BUYER` | Locked buyer profile is synthetic skeptical dupe-first; panels project candidate/fit evidence around Sauvage, Aventus, comparable products, and dupe/comment texture. |
| 5. Cross-vendor adversarial review blocker/major-free | `BLOCKED_PENDING_CROSS_VENDOR_REVIEW` | No cross-vendor review has run. Same-vendor review is explicitly insufficient. Review input is prepared in `docs/review-inputs/aphrodite_depth_rehearsal_d1_gentsscents_adversarial_review_input_v0.md`. |
| 6. Bounded-effort receipt | `OBSERVED_WITH_LIMITATION` | Reads, counts, steps, exceptions, and known count mismatches are recorded below. Exact wall-clock duration was not independently timer-instrumented, so this is an effort receipt, not a benchmark. |

## Grade

The D-1 rehearsal is mechanically promising but not gate-complete.

- Fit: useful but not decision-grade. Direct-original attention is real; clone-tail fit is withheld because the ontology has no dupe graph and the low-confidence tail matters to the buyer.
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

Exceptions and residuals:

- The accepted recipe-v1 adjudication has a 29-vs-30 claim-count discrepancy; this run emits all 30 appendix claim types and records the discrepancy.
- Current raw count and prior round-2 count differ for comments and words; both are disclosed.
- Initial broad raw-lake search was too noisy for binding use; the run switched to selected packet inspection.
- Current crude URL regex over-counted malformed snippets, so the grade uses the round-2 exact affiliate-link count.
- The SoV output is a research record, not a durable product mention silver lane.
- Cross-vendor review is not available inside this OpenAI-family session and must be run externally or in a genuinely decorrelated lane.

## Next Gate

Run the review input in `docs/review-inputs/aphrodite_depth_rehearsal_d1_gentsscents_adversarial_review_input_v0.md` through a different-vendor reviewer. Only after blocker/major-free review plus home-lane adjudication can criterion 5 be marked observed. Until then, any claim that D-1 fired is false.

## Non-Claims

- Not D-1 passage, readiness, validation, buyer proof, or commercial-use clearance.
- Not a build of a runner, crawler, data lake lane, or UI surface.
- Not a recommendation to contact buyers or resolve FLAG-1.
