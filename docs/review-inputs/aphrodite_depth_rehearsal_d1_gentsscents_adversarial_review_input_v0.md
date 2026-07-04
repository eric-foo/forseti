# Aphrodite D-1 GentsScents Adversarial Review Input v0

```yaml
retrieval_header_version: 1
artifact_role: Canonical review input (cross-vendor adversarial artifact review prompt for Aphrodite D-1 GentsScents rehearsal)
scope: >
  Commissioning prompt for the required cross-vendor adversarial review of the
  GentsScents D-1 rehearsal artifacts. The review determines whether D-1
  criterion 5 can be marked blocker/major-free after home-lane adjudication.
use_when:
  - Dispatching the GentsScents D-1 artifact set to a genuinely decorrelated reviewer.
  - Checking why this fused lane parked before claiming D-1 passage.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/delegated-review-patch.md
  - docs/research/aphrodite_depth_rehearsal_d1_gentsscents_grade_v0.md
stale_if:
  - Any target artifact is patched after this prompt is written.
  - The review-lane or delegated-review-patch overlay changes the cross-vendor/decorrelation bar.
```

## Dispatch Status

`READY_FOR_CROSS_VENDOR_REVIEW_DISPATCH` - this is a review input only. It is not the review result, not a pass, and not D-1 criterion 5.

## Decorrelation Requirement

- Author/home family: OpenAI/GPT/Codex.
- Required reviewer: different vendor and model lineage from OpenAI/GPT/Codex.
- Same-family review may still find defects, but it cannot satisfy Aphrodite D-1 criterion 5.
- If you are the same vendor/model family as the authoring lane, return `BLOCKED_REVIEW_LANE_UNAVAILABLE_FOR_D1_CRITERION_5` and stop after any optional advisory notes.

## Target Branch and Files

Review branch: `codex/aphrodite-d1-depth-rehearsal`

Target artifacts:

- `docs/research/aphrodite_depth_rehearsal_extraction_recipe_v1.md`
- `docs/research/aphrodite_depth_rehearsal_d1_gentsscents_corpus_v0.md`
- `docs/research/aphrodite_depth_rehearsal_d1_gentsscents_claims_v0.json`
- `docs/research/aphrodite_depth_rehearsal_d1_gentsscents_panel_projection_v0.md`
- `docs/research/aphrodite_depth_rehearsal_d1_gentsscents_grade_v0.md`

Required control sources:

- `docs/prompts/handoffs/aphrodite_depth_layer_build_handoff_v1.md`
- `forseti/product/spines/creator_signal/aphrodite_carveout_charter_v0.md`
- `docs/research/aphrodite_recipe_v1_second_opinion_adjudication_v0.md`
- `docs/research/aphrodite_depth_rehearsal_round2_gentsscents_grade_v0.md`
- `docs/research/aphrodite_depth_rehearsal_round2_share_of_voice_v0.md`
- `forseti/product/spines/foundation/ontology/fragrance_reference_v0.yaml`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/delegated-review-patch.md`

Output path:

- `docs/review-outputs/adversarial-artifact-reviews/aphrodite_depth_rehearsal_d1_gentsscents_adversarial_artifact_review_v0.md`

## Paste-Ready Prompt

You are a cross-vendor adversarial artifact reviewer for the Orca repository.

Before reviewing, load and follow your local equivalents of:

- `workflow-deep-thinking`
- `workflow-adversarial-artifact-review`

If those skills are unavailable, continue only if you can still perform a source-backed adversarial artifact review with findings-first severity discipline. If you cannot access the repository or the required files, return `BLOCKED_REVIEW_INPUT_NO_SOURCE_ACCESS`. A no-repo review is advisory only and cannot satisfy Aphrodite D-1 criterion 5 unless the operator supplies the full target artifacts and control sources.

Review objective:

Determine whether the GentsScents D-1 rehearsal artifacts are blocker/major-free for Aphrodite D-1 criterion 5, subject to home-lane adjudication. You are not deciding that D-1 fires. You are reviewing whether the artifact set honestly satisfies, with visible residuals, criteria 1, 2, 3, 4, and 6, and whether it correctly blocks criterion 5 pending cross-vendor review.

Read, in this order:

1. `.agents/workflow-overlay/review-lanes.md`
2. `.agents/workflow-overlay/delegated-review-patch.md`
3. `docs/prompts/handoffs/aphrodite_depth_layer_build_handoff_v1.md`
4. `forseti/product/spines/creator_signal/aphrodite_carveout_charter_v0.md`
5. `docs/research/aphrodite_recipe_v1_second_opinion_adjudication_v0.md`
6. `docs/research/aphrodite_depth_rehearsal_round2_gentsscents_grade_v0.md`
7. `docs/research/aphrodite_depth_rehearsal_round2_share_of_voice_v0.md`
8. `forseti/product/spines/foundation/ontology/fragrance_reference_v0.yaml`
9. The five target artifacts listed above.

Adversarial questions:

- Does any artifact fake D-1 passage, readiness, validation, buyer proof, FLAG-1 resolution, or commercial-use clearance?
- Are all five panels actually represented, with no hidden score or numeric readiness substitute?
- For fit claims, does every shown or downgraded product-coordinate conclusion resolve against `fragrance_reference_v0.yaml`, or explicitly withhold/downgrade when it cannot?
- Does the dupe-space behavior honestly withhold on empty `dupe_relationships` while still showing direct-original attention?
- Does the claim JSON carry all required provenance fields on every claim?
- Does it preserve the M2 rule by keeping raw comment counts and `sum(like_count)` separate instead of blending them into a fake support metric?
- Does the synthetic skeptical buyer profile remain an intake coordinate rather than being treated as market proof?
- Are count mismatches, low-confidence tail, affiliate-heavy corpus, no organic comparator, and single-cycle momentum limitations visible enough to prevent downstream misuse?
- Are the criterion table and grade too generous anywhere?
- Are the review input and grade explicit enough that same-family review cannot be mistaken for criterion 5 satisfaction?

Output format:

Start with findings first, ordered by severity.

Use severities:

- `BLOCKER`: would invalidate the artifact set for D-1 criterion 5 review or creates a fake pass.
- `MAJOR`: materially weakens gate confidence or could mislead downstream routing.
- `MINOR`: should be patched but does not block review confidence.
- `NOTE`: non-actionable observation or residual risk.

For each finding, include:

- severity;
- file and line reference if available;
- exact problem;
- why it matters against the control sources;
- smallest complete patch direction, if any.

Then include:

- `Criterion 5 review verdict: BLOCKER_MAJOR_FREE | NOT_BLOCKER_MAJOR_FREE | BLOCKED_NO_SOURCE_ACCESS | BLOCKED_NOT_DECORRELATED`
- `Can home lane consider D-1 criterion 5 observed after adjudication? yes/no`
- Residual risks that remain even if blocker/major-free.
- Test or validation suggestions.

Do not patch files unless explicitly commissioned. Do not invent source facts. Do not treat this prompt as D-1 passage.
