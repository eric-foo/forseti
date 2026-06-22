# IG Cleaning Raw-vs-Cleaned Adversarial Artifact Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: Claude-ready prompt for independently comparing IG raw JSON anchors against Cleaning handles.
use_when:
  - Commissioning a read-only raw-vs-cleaned interpretation review for the IG Cleaning smoke packet.
  - Checking whether Cleaning preserved raw meaning without overcleaning or Judgment leakage.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/README.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - docs/prompts/templates/review/adversarial_artifact_review_v0.md
branch_or_commit: codex/cleaning-spine-continuation @ 81a46445
```

## Orca Prompt Preflight

```yaml
output_mode: review-report
prompt_artifact_path: docs/prompts/reviews/ig_cleaning_raw_vs_cleaned_adversarial_artifact_review_prompt_v0.md
review_output_path: docs/review-outputs/adversarial-artifact-reviews/ig_cleaning_raw_vs_cleaned_adversarial_artifact_review_v0.md
template_kind: adversarial-artifact-review
template_source: docs/prompts/templates/review/adversarial_artifact_review_v0.md
edit_permission: read-only
target_workspace: C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\cleaning-spine-continuation
target_branch: codex/cleaning-spine-continuation
target_commit: 81a46445
dirty_state_allowance: generated _test_runs artifacts may be untracked or ignored; source changes are not authorized
target_artifacts:
  - orca-harness/_test_runs/ig_cleaning_spine_stage1_20260621/raw_cleaned_review_packet/packet_manifest.json
  - orca-harness/_test_runs/ig_cleaning_spine_stage1_20260621/raw_cleaned_review_packet/raw_cleaned_pairs.json
  - orca-harness/_test_runs/ig_cleaning_spine_stage1_20260621/raw_cleaned_review_packet/review_prompt.md
  - orca-harness/_test_runs/ig_cleaning_spine_stage1_20260621/stitched/cleaning_packet.json
  - orca-harness/_test_runs/ig_cleaning_spine_stage1_20260621/stitched/ecr_source_side_receipts.json
  - orca-harness/_test_runs/ig_cleaning_spine_stage1_20260621/stitched/smoke_summary.json
reviews:
  findings_first: true
  formal_verdicts_allowed:
    - bounded_raw_to_cleaned_trace_supported
    - partially_supported
    - not_supported
  severity_labels: critical | major | minor
doctrine_change: none
receiver: Claude, or another read-only reviewer with filesystem access to the target workspace
```

## Prompt To Run

You are performing a read-only adversarial artifact review for Orca.

Your job is to determine whether the IG Cleaning smoke preserved source meaning from raw evidence into cleaned handles, or whether it overcleaned, lost anchors, hid residuals, or introduced Judgment semantics.

Do not edit files. Do not run live capture. Do not infer demand, credibility, salience, product quality, creator quality, actionability, or any Judgment output.

### Required Source Loading

Start by reading:

1. `AGENTS.md`
2. `.agents/workflow-overlay/README.md`
3. `.agents/workflow-overlay/source-of-truth.md`
4. `.agents/workflow-overlay/source-loading.md`
5. `.agents/workflow-overlay/review-lanes.md`
6. `.agents/workflow-overlay/prompt-orchestration.md`
7. `.agents/workflow-overlay/validation-gates.md`

Then read the review packet:

1. `orca-harness/_test_runs/ig_cleaning_spine_stage1_20260621/raw_cleaned_review_packet/packet_manifest.json`
2. `orca-harness/_test_runs/ig_cleaning_spine_stage1_20260621/raw_cleaned_review_packet/raw_cleaned_pairs.json`
3. `orca-harness/_test_runs/ig_cleaning_spine_stage1_20260621/raw_cleaned_review_packet/review_prompt.md`

Then read the source outputs referenced by that packet when needed:

1. `orca-harness/_test_runs/ig_cleaning_spine_stage1_20260621/stitched/cleaning_packet.json`
2. `orca-harness/_test_runs/ig_cleaning_spine_stage1_20260621/stitched/ecr_source_side_receipts.json`
3. `orca-harness/_test_runs/ig_cleaning_spine_stage1_20260621/stitched/smoke_summary.json`
4. The projection JSON and raw JSON files referenced by selected `raw_cleaned_pairs.json` entries.

Declare `SOURCE_CONTEXT_READY` only after the above source context is loaded. If any required file is missing or inaccessible, declare `SOURCE_CONTEXT_INCOMPLETE` and return a blocked review; do not substitute another checkout or packet.

### Review Target

Primary target:

`orca-harness/_test_runs/ig_cleaning_spine_stage1_20260621/raw_cleaned_review_packet/raw_cleaned_pairs.json`

Report destination:

`docs/review-outputs/adversarial-artifact-reviews/ig_cleaning_raw_vs_cleaned_adversarial_artifact_review_v0.md`

### Review Question

Can a reviewer derive the cleaned handle/projection meaning from the raw anchor and packet metadata without adding meaning, hiding uncertainty, or losing traceability?

Attack these failure modes:

- raw JSON Pointer does not resolve;
- raw file hash does not match the anchor;
- projection row value/posture/reason is not mechanically supported by raw value and packet metadata;
- Cleaning handle loses packet, slice, file, hash, JSON Pointer, projection ref, ECR ref, or `relation`;
- Cleaning introduces Judgment vocabulary or conclusions;
- Cleaning suppresses ECR residuals such as `current_capture_only` or missing cutoff posture;
- review packet misrepresents the source `cleaning_packet.json`;
- unavailable or not-applicable metrics are turned into fake observed zeros;
- captions or source text are summarized or semantically rewritten without authority.

### Sampling Requirement

Review all packet-level counts and integrity summaries. For row-level inspection, use either all rows or a defensible sample that includes at least:

- one `follower_count` row;
- one observed `like_count` row;
- one observed `comment_count` row;
- one observed `view_count` row;
- one `view_count:not_applicable` row;
- one `view_count:unavailable_with_reason` row;
- at least one row from each source label:
  - `instagram:curlyscents`
  - `instagram:funmimonet`
  - `instagram:jeremyfragrance`
  - `instagram:theperfumeguy`

If you sample rather than inspect all 134 rows, say exactly what was sampled and what residual risk remains.

### Required Output

Write the review report to:

`docs/review-outputs/adversarial-artifact-reviews/ig_cleaning_raw_vs_cleaned_adversarial_artifact_review_v0.md`

Use findings-first structure.

Include:

1. Verdict: exactly one of:
   - `bounded_raw_to_cleaned_trace_supported`
   - `partially_supported`
   - `not_supported`
2. Findings ordered by severity. For each finding include:
   - severity;
   - source label;
   - handle ID or artifact path;
   - raw evidence;
   - cleaned/projection evidence;
   - issue;
   - impact;
   - minimum closure condition;
   - next authorized action.
3. A specific answer to:
   - Did Cleaning overclean meaning?
   - Did Cleaning underclean traceability?
   - Did Cleaning lose anchors?
   - Did Cleaning introduce Judgment semantics?
   - Did Cleaning preserve residuals?
4. A plain-language explanation of exactly what Cleaning cleaned and did not clean.
5. Non-claims:
   - not live IG capture;
   - not data-lake promotion;
   - not production validation;
   - not E2E product readiness;
   - not Judgment scoring;
   - not product or creator proof.

After writing the report, verify the file exists with a fresh read and report the observed path and a concise summary in chat. If you cannot write the report, return the review in chat and state that the durable report write failed.

### Review-Use Boundary

This review is decision input only. It is not approval, validation, product proof, production readiness, or authorization to change code.
