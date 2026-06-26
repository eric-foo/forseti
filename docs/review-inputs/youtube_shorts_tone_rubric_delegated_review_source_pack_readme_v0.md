# YouTube Shorts Tone Rubric Delegated Review Source Pack README v0

```yaml
retrieval_header_version: 1
artifact_role: Review input README
scope: Entry note for the no-repo source pack supporting the delegated review of the YouTube Shorts transcript tone rubric.
use_when:
  - Giving a no-repo reviewer the files needed to run advisory-only review of the rubric.
  - Verifying which source file should be opened first inside the source pack.
authority_boundary: retrieval_only
open_next:
  - docs/prompts/reviews/youtube_shorts_transcript_tone_rubric_delegated_adversarial_artifact_review_patch_prompt_v0.md
```

Open the prompt first:

`docs/prompts/reviews/youtube_shorts_transcript_tone_rubric_delegated_adversarial_artifact_review_patch_prompt_v0.md`

If you do not have repo access, you are in `no_repo` mode. That means advisory
review only: do not claim repo patch authorship, do not return a working-tree
diff, and do not claim the delegated review-and-patch discovery bar. Return
findings plus exact proposed edits for the target rubric. The CA applies any
accepted edits and runs a bounded post-patch re-review before keep.

## Target

The only patch target in repo mode, and the only proposed-edit target in no-repo
mode:

`docs/review-inputs/youtube_shorts_fragrance_transcript_tone_rubric_v0.md`

## Supporting Evidence

- `docs/review-inputs/youtube_shorts_fragrance_tone_fixture_hard30_v0.md`
- `docs/review-inputs/youtube_shorts_fragrance_tone_fixture_hard30_v0.json`
- `docs/review-inputs/youtube_shorts_fragrance_tone_labeling_run_v0.md`
- `docs/review-inputs/youtube_shorts_fragrance_tone_labeling_run_v0.json`

## Included Authority And Method Files

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/validation-gates.md`
- `.agents/workflow-overlay/delegated-review-patch.md`
- `docs/prompts/templates/review/adversarial_artifact_review_v0.md`
- `docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md`
- `docs/prompts/templates/shared/orca_preflight_defaults_v0.md`

## Non-Claims

This source pack is review input only. It is not validation, readiness,
acceptance, benchmark proof, product proof, runtime model routing, or a claim
that a no-repo reviewer can perform repo-mode patch authorship.
