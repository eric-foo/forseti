# CSB Prompt Structure Rename Adversarial Artifact Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: Read-only adversarial artifact review prompt for the CSB Prompt Structure filename/path rename patch.
use_when:
  - Commissioning an adversarial review of commit c992fe7efb4bd8cadf53797b380fde25e83834e5.
  - Checking whether the CSB Prompt Structure and Prompt Structure Rules rename was fully propagated without stale live references.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/README.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - docs/prompts/templates/review/adversarial_artifact_review_v0.md
  - orca/product/spines/commission_signal_board/README.md
  - orca/product/spines/commission_signal_board/spine.yaml
  - orca/product/spines/commission_signal_board/prompts/orca_commission_signal_board_prompt_structure_v0.md
  - orca/product/spines/commission_signal_board/authority/orca_commission_signal_board_prompt_structure_rules_v0.md
stale_if:
  - Commit c992fe7efb4bd8cadf53797b380fde25e83834e5 is amended, reverted, or superseded.
  - The CSB Prompt Structure files move again.
  - Orca review-lane or prompt-orchestration rules change.
```

## Orca Prompt Preflight

- Output mode: `review-report`; report destination `docs/review-outputs/adversarial-artifact-reviews/csb_prompt_structure_rename_adversarial_artifact_review_v0.md`.
- Template kind: `adversarial-artifact-review`; source template `docs/prompts/templates/review/adversarial_artifact_review_v0.md`.
- Edit permission / targets / branch: read-only review; target commit `c992fe7efb4bd8cadf53797b380fde25e83834e5` on branch `codex/search-surface-mgt-p0-captures-ws` in worktree `C:/Users/vmon7/Desktop/projects/orca/worktrees/search-surface-mgt-p0-captures`.
- Reviews: findings-first adversarial artifact review; no approval, readiness, validation, mandatory remediation, or patch queue authority.
- Doctrine change: none introduced by this prompt; the review target is a path/name propagation patch.
- Destinations: this prompt artifact is `docs/prompts/reviews/csb_prompt_structure_rename_adversarial_artifact_review_prompt_v0.md`; the reviewer writes the report path above.

## Delegated Review-And-Patch Route Note

`workflow-delegated-review-patch` was invoked as requested. Its strict repo-mode review-and-patch shape is not the right terminal here because the target is a multi-file rename propagation patch, not a single high-stakes authored artifact file. Per the Orca delegated-review-patch overlay, route this to the appropriate review prompt instead: read-only adversarial artifact review of the committed patch. Do not patch in the review lane.

De-correlation: operator/tooling owned. If the operator wants to claim cross-vendor discovery, the receiving reviewer must be from a different vendor/model lineage than the authoring CA. If that is not true or not recorded, set `de_correlation_bar: same_vendor_sanity` or `unrecorded` and do not claim no-new-seam discovery.

## Prompt Body

You are performing a read-only adversarial artifact review for Orca.

### Review Target

Review commit:

```text
c992fe7efb4bd8cadf53797b380fde25e83834e5 docs: rename csb prompt structure artifacts
```

Review the patch delta from `c992fe7efb4bd8cadf53797b380fde25e83834e5^` to `c992fe7efb4bd8cadf53797b380fde25e83834e5` in this worktree:

```text
C:/Users/vmon7/Desktop/projects/orca/worktrees/search-surface-mgt-p0-captures
```

The intended rename is:

```text
orca/product/spines/commission_signal_board/prompts/orca_commission_signal_board_prompt_v0.md
-> orca/product/spines/commission_signal_board/prompts/orca_commission_signal_board_prompt_structure_v0.md

orca/product/spines/commission_signal_board/authority/orca_commission_signal_board_prompt_adjudication_packet_v0.md
-> orca/product/spines/commission_signal_board/authority/orca_commission_signal_board_prompt_structure_rules_v0.md
```

### Review Purpose

Adversarially check whether the rename fully eliminates confusing live canonical names without breaking CSB source loading, moved-path resolution, existing prompt/review references, or downstream lane pointers.

The review should specifically attack:

- stale live references to the old canonical filenames or old canonical paths;
- incorrect updates that turn historical absent old paths into invented historical paths;
- missed `open_next`, `canonical_artifacts`, prompt, playbook, review prompt, review output, capture, judgment, or source-capture references;
- inconsistent role labels for `Prompt Structure` and `Prompt Structure Rules`;
- broken moved-path resolver semantics;
- bad retention of old names outside explicitly historical absent-path resolver sections or frozen review-input snapshots;
- invalid retrieval headers or prompt-preflight regressions;
- validation overclaims.

### Fitness Reference

Goal: make CSB future-agent source loading unambiguous by giving the two CSB prompt-structure artifacts role-aligned live filenames.

Success signal: live CSB and adjacent lane references point to the new filenames; old filenames survive only as explicitly historical absent-path resolver entries or frozen snapshots; validators and stale-reference sweeps do not show live old-path dependencies.

### Required Authority Sources

Load these before reviewing:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/artifact-roles.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/validation-gates.md`
- `.agents/workflow-overlay/delegated-review-patch.md`
- `docs/prompts/templates/review/adversarial_artifact_review_v0.md`

Then source-load the target commit and changed files. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` before findings.

### Required Method

Use `workflow-deep-thinking` first to frame boundary risks and failure modes. Then use `workflow-adversarial-artifact-review` after `SOURCE_CONTEXT_READY`.

If either method is unavailable or cannot be applied, return blocked/advisory-only and do not emit strict review, readiness, validation, or approval claims.

### Suggested Verification Commands

Run or inspect equivalents, and report exact results:

```powershell
git show --name-status --find-renames c992fe7efb4bd8cadf53797b380fde25e83834e5
git diff --check c992fe7efb4bd8cadf53797b380fde25e83834e5^ c992fe7efb4bd8cadf53797b380fde25e83834e5
python -B .agents/hooks/check_commission_signal_board_output.py --selftest
rg -n "orca/product/spines/commission_signal_board/(prompts/orca_commission_signal_board_prompt_v0|authority/orca_commission_signal_board_prompt_adjudication_packet_v0)" .agents docs orca -g "*.md" -g "*.yaml" -g "*.py"
rg -n "orca_commission_signal_board_prompt_v0|orca_commission_signal_board_prompt_adjudication_packet_v0|prompt_adjudication_packet|authority_packet:" .agents docs orca -g "*.md" -g "*.yaml" -g "*.py"
```

Expected boundary: the live old canonical-path sweep should return no matches. The broader old-filename sweep may return only explicitly historical absent-path resolver entries or frozen review-input snapshots; any live-source reference is a finding.

### Output Contract

Write the durable review report to:

```text
docs/review-outputs/adversarial-artifact-reviews/csb_prompt_structure_rename_adversarial_artifact_review_v0.md
```

The report must be findings-first. Include:

- `reviewed_by`: operator/tooling supplied value, or `unrecorded` if not supplied;
- `authored_by`: `gpt-5-codex-current-thread` if accepted by operator/tooling, otherwise `unrecorded`;
- `de_correlation_bar`: `cross_vendor_discovery`, `same_vendor_sanity`, or `unrecorded`;
- if `same_vendor_sanity`, include `same_vendor_rationale`;
- source context status;
- commands run and exact results;
- findings ordered by severity: critical, major, minor;
- for each finding: severity, location, issue, evidence, impact, minimum_closure_condition, next_authorized_action, recommended correction;
- residual risks and validation gaps.

Do not include `patch_queue_entry`. This is read-only review. Findings are decision input only, not approval, validation, mandatory remediation, readiness, or executor-ready patch authority.