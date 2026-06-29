# Silver Lineage Kit Delegated Adversarial Review-and-Patch Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: review_prompt
scope: >
  Filed prompt for a de-correlated delegated adversarial review-and-patch pass
  over the Silver lineage kit genericity check artifact in PR #454.
use_when:
  - Dispatching an independent reviewer to harden the Silver lineage kit genericity check.
  - Checking that the Silver lineage kit stays source-family generic without overclaiming media, raw retention, IG-specific mechanics, or Silver physicalization.
authority_boundary: retrieval_only
open_next:
  - docs/workflows/silver_lineage_kit_genericity_check_v0.md
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - docs/prompts/templates/review/adversarial_artifact_review_v0.md
input_hashes:
  - docs/workflows/silver_lineage_kit_genericity_check_v0.md: sha256:976B7D0E59BA90CEAF7AACEC33BFC29574DF880791A63E4CC74C30DAF0646149
stale_if:
  - The review target file hash differs from the value above.
  - The review target branch changes from codex/silver-lineage-kit.
  - The pinned target commit changes from 62186ef22d2bcd63eee4ed79c4adac0aeccfe453 before review dispatch.
  - PR #454 is merged, superseded, or materially retargeted before review.
  - Delegated-review-patch, review-lanes, prompt-orchestration, or the adversarial artifact review template changes.
```

preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` v0 - constants bound; deltas stated below.

## Prompt Preflight Deltas

```yaml
authorization_basis: "Current owner instruction: run workflow-delegated-review-patch before continuing the Silver lineage kit lane."
objective: >
  Commission an independent, de-correlated reviewer to adversarially review and,
  if bounded wording fixes are needed, patch only the Silver lineage kit
  genericity check artifact before CA/home-model adjudication.
intended_decision: >
  Decide whether the genericity check is strong enough to serve as the source
  basis for a later Silver lineage kit spec without becoming IG-specific,
  raw-retention-specific, transcript-specific, or over-broad across all media
  and source families.
target_files_or_dirs:
  - docs/workflows/silver_lineage_kit_genericity_check_v0.md
source_pack: custom_silver_lineage_kit_genericity_review_pack
output_mode: file-write prompt artifact, with paste-ready-chat copy below for the delegated controller
delegated_controller_return_mode: paste-ready-chat plus bounded diff
edit_permission: patch-only for the single review target; read-only for every other path
dirty_state_allowance: >
  Expected clean worktree at the pinned target commit before reviewer edits. If
  dirty, classify whether changes touch the target. Do not make strict review
  claims if the target differs from the pinned hash without explicit operator
  acceptance.
controlling_source_state: >
  Target hash, branch, and HEAD were checked by the dispatcher before prompt
  filing. Reviewer must fresh-read and verify before making strict or actionable
  claims.
branch_or_commit_reference: "codex/silver-lineage-kit at 62186ef22d2bcd63eee4ed79c4adac0aeccfe453; PR #454"
doctrine_change_decision: >
  This prompt does not change product doctrine, validation doctrine, workflow
  authority, review authority, or lifecycle boundaries. Reviewer may recommend
  doctrine or architecture changes as findings only. If a design-level correction
  is needed, return NEEDS_ARCHITECTURE_PASS and leave no patch.
isolation_decision: "Use the existing codex/silver-lineage-kit worktree; no new branch required for the reviewer unless their tooling requires isolation."
validation_gates:
  - "If patching: run git diff --check -- docs/workflows/silver_lineage_kit_genericity_check_v0.md"
  - "If patching: run python .agents/hooks/check_retrieval_header.py --strict docs/workflows/silver_lineage_kit_genericity_check_v0.md"
  - "If writing a durable report: run python .agents/hooks/check_retrieval_header.py --strict docs/review-outputs/adversarial-artifact-reviews/silver_lineage_kit_delegated_adversarial_review_v0.md"
thread_operating_target_continuity:
  carried_forward: no
  reason: no_visible_active_target_block
```

## Paste-Ready Review Prompt

```markdown
You are the delegated controller for an Orca adversarial artifact review-and-patch hardening pass.

This is a de-correlated delegated review-and-patch commission. The author/home
model family is OpenAI / Codex / GPT-family. To satisfy cross-vendor discovery,
the controller must be from a different vendor/model lineage. If you are not
from a different vendor/model lineage, continue only as `same_vendor_sanity` or
`self_fallback` and state that the cross-vendor discovery bar is not satisfied.
Do not present model family as a runtime quality recommendation; it is only a
who-constraint.

Current receiving actor role: controller.
Dispatch mode: operator_to_fill.
controller_model_family: operator_to_fill.
author_home_model_family: OpenAI / Codex / GPT-family.
de_correlation_status: operator_to_verify_before_review.

Workspace:
`C:\Users\vmon7\Desktop\projects\orca\worktrees\silver-lineage-kit`

PR:
https://github.com/eric-foo/orca/pull/454

Expected branch/reference:
`codex/silver-lineage-kit` at `62186ef22d2bcd63eee4ed79c4adac0aeccfe453`.

Pinned review target hash:
`docs/workflows/silver_lineage_kit_genericity_check_v0.md`
`sha256:976B7D0E59BA90CEAF7AACEC33BFC29574DF880791A63E4CC74C30DAF0646149`

Prompt source:
`docs/prompts/reviews/silver_lineage_kit_delegated_adversarial_review_patch_prompt_v0.md`

Review target and only editable file:
`docs/workflows/silver_lineage_kit_genericity_check_v0.md`

Review report destination:
`docs/review-outputs/adversarial-artifact-reviews/silver_lineage_kit_delegated_adversarial_review_v0.md`

Review purpose:
Adversarially review whether the Silver lineage kit genericity check is broad
enough to cover Orca's current source families while preserving explicit
limitations: no media-retention overclaim, no transcript-only narrowing, no
IG-only mechanics, no claim that all source families already expose the same raw
or evidence packet structure, and no accidental authorization of Silver
implementation or shared core changes. If bounded wording fixes materially
improve that target, patch only the target file.

Fitness reference:
The target succeeds only if a later CA can safely use it as the source-backed
basis for a generic Silver lineage kit design. That means it must name the right
source-reference grammar and admitted limitations across source captures, product
source capsules, transcripts/audio packets, cleaning outputs, and projected
Silver records without implying complete raw media retention or behavioral
parity where the sources do not support it.

Required method and authority loading:
1. Read `AGENTS.md`.
2. Read `.agents/workflow-overlay/README.md`.
3. REFERENCE-LOAD these method/contract sources. Do not APPLY them yet:
   - `workflow-deep-thinking`
   - `workflow-adversarial-artifact-review`
   - `.agents/workflow-overlay/source-of-truth.md`
   - `.agents/workflow-overlay/source-loading.md`
   - `.agents/workflow-overlay/artifact-folders.md`
   - `.agents/workflow-overlay/artifact-roles.md`
   - `.agents/workflow-overlay/delegated-review-patch.md`
   - `.agents/workflow-overlay/review-lanes.md`
   - `.agents/workflow-overlay/prompt-orchestration.md`
   - `.agents/workflow-overlay/validation-gates.md`
   - `.agents/workflow-overlay/communication-style.md`
   - `docs/prompts/templates/review/adversarial_artifact_review_v0.md`
4. SOURCE-LOAD the review target and these controlling sources:
   - `docs/workflows/silver_lineage_kit_genericity_check_v0.md`
   - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md`
   - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md`
   - `orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md`
   - `orca-harness/data_lake/root.py`
5. For strict claims about source-family coverage, selectively inspect the
   relevant current implementation/source artifacts rather than relying on the
   target's summary. Start with:
   - `orca-harness/source_capture/reddit_projection.py`
   - `orca-harness/source_capture/retail_pdp_projection.py`
   - `orca-harness/source_capture/fragrantica_projection.py`
   - `orca-harness/source_capture/ig_reels_grid_projection.py`
   - `orca-harness/source_capture/transcript/asr_packet.py`
   - `orca-harness/source_capture/transcript/ig_reels_audio_packet.py`
   - `orca-harness/source_capture/ig_reels_deep_capture_lake.py`
   - `orca-harness/cleaning/models.py`
   - `orca-harness/cleaning/transcript_product_lake.py`
6. Verify before review:
   - `git status --short --branch`
   - `git rev-parse HEAD`
   - `Get-FileHash docs\workflows\silver_lineage_kit_genericity_check_v0.md -Algorithm SHA256`
7. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` before
   applying any method. If incomplete, name the missing file/source and stop
   unless the missing source cannot affect the finding.
8. After source context is ready, APPLY `workflow-deep-thinking` to frame the
   boundary problem and failure modes, then APPLY
   `workflow-adversarial-artifact-review` to the loaded target and sources.

Patch authority:
- You may patch only
  `docs/workflows/silver_lineage_kit_genericity_check_v0.md`.
- You may write the review report only to
  `docs/review-outputs/adversarial-artifact-reviews/silver_lineage_kit_delegated_adversarial_review_v0.md`.
- Do not patch this prompt artifact.
- Do not patch overlay files, prompt templates, workflow contracts, source
  capture code, cleaning code, data lake code, tests, JSON ledgers, raw data,
  data-lake paths, docs/workflows repo-map files, or shared core surfaces.
- Do not stage, commit, push, open or update PRs, merge, or claim acceptance,
  validation, readiness, mandatory remediation, or product proof.
- Flag off-scope issues as findings only.

Escalation valve:
If the target is design-level wrong rather than patchably rough, return
`NEEDS_ARCHITECTURE_PASS`, leave no patch, and provide findings only.

Attack these failure modes first:
- The target silently narrows Silver lineage to IG or transcript mechanics.
- The target silently over-broadens to all media, all source families, or full
  raw retention without source evidence.
- The target treats derived thumbnails, audio snippets, ASR, product capsules,
  post/comment captures, cleaning outputs, or projected records as if they have
  identical source-object semantics.
- The target fails to preserve source-reference identity: source family, capture
  run, source item, raw/evidence packet, derived artifact, projection record,
  cleaning output, and limitation/admission should not collapse into one field.
- The target omits material limitations around rawless IG one-render deep
  capture, Attachment Record absence, product source capsules, absent comments,
  or unavailable audio/transcript details.
- The target makes future implementation, bronze/silver physicalization, shared
  core, runner sync, or data-lake migration sound authorized.
- The target's source matrix is self-certifying or stale because it does not
  cite the current contracts/code it depends on.
- The target's agent-use guidance is not mechanical enough for future agents to
  apply consistently.
- The target lacks enough stale-if/source-loading metadata to avoid later agents
  relying on outdated genericity claims.

If you patch, run:
- `git diff --check -- docs/workflows/silver_lineage_kit_genericity_check_v0.md`
- `python .agents/hooks/check_retrieval_header.py --strict docs/workflows/silver_lineage_kit_genericity_check_v0.md`
- `python .agents/hooks/check_retrieval_header.py --strict docs/review-outputs/adversarial-artifact-reviews/silver_lineage_kit_delegated_adversarial_review_v0.md`

Return in chat to the commissioning CA:

```yaml
delegated_review_return:
  source_context: SOURCE_CONTEXT_READY | SOURCE_CONTEXT_INCOMPLETE
  de_correlation_bar: cross_vendor_discovery | same_vendor_sanity | self_fallback
  controller_family: "<operator/tooling supplied; do not fabricate>"
  author_home_family: "OpenAI / Codex / GPT-family"
  verdict: NEEDS_ARCHITECTURE_PASS | PATCHED_FOR_CA_ADJUDICATION | NO_PATCH_FINDINGS_ONLY
  patch_scope: "docs/workflows/silver_lineage_kit_genericity_check_v0.md only"
  report_path: "docs/review-outputs/adversarial-artifact-reviews/silver_lineage_kit_delegated_adversarial_review_v0.md"
  validation:
    - command: ""
      result: passed | failed | not_run
      evidence: ""
  residual_risk: ""
  ca_adjudication_required: true
```

Then list findings first, ordered `critical`, `major`, `minor`. For each finding
include severity, location, issue, evidence, impact, minimum_closure_condition,
next_authorized_action, and recommended correction/advisory remediation. Do not
include `patch_queue_entry`.

If you patched, include a unified diff for the target file only. The diff,
citations, and verdict are claims for CA adjudication, not accepted truth. The CA
may accept, modify, or reject any change.

Review-use boundary:
Your findings and patch are decision input only. They are not approval,
validation, readiness, mandatory remediation, product proof, executor-ready
authority, or evidence that the Silver lineage kit is complete until the
commissioning CA adjudicates them.
```
