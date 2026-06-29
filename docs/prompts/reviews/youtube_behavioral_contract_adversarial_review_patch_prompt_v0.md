# YouTube Behavioral Contract Adversarial Review-And-Patch Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Repo-mode delegated adversarial review-and-patch commission for the YouTube
  behavioral contract extraction workflow artifact on PR #430.
use_when:
  - Commissioning a de-correlated controller to verify and patch the YouTube behavioral contract extraction artifact before IG sync.
  - Recovering the exact target, source pack, patch boundary, and CA adjudication contract for this delegated review-and-patch pass.
authority_boundary: retrieval_only
```

## Prompt-Orchestrator Receipt

preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` v0 - constants bound; deltas stated below.

orca_start_preflight:

- agents_read: yes
- overlay_read: yes
- source_pack: custom S3 target-deepening
- edit_permission: patch-only for the named target artifact; read-only for everything else
- target_scope: `docs/workflows/youtube_behavioral_contract_from_merged_main_v0.md`
- dirty_state_checked: yes
- blocked_if_missing: target artifact, local repo/worktree access, de-correlation receipt, source-readiness declaration

Per-prompt deltas:

- authorization_basis: current owner invocation of `workflow-delegated-review-patch` after PR #430 was created for step 1.
- objective: de-correlated adversarially review and, if needed, patch the YouTube behavioral contract extraction artifact so it is a source-backed YT reference for the next IG sync lane.
- intended_decision: whether the target artifact is materially accurate, bounded, and usable as a YT reference contract after CA adjudication of any proposed diff.
- prompt_artifact_path: `docs/prompts/reviews/youtube_behavioral_contract_adversarial_review_patch_prompt_v0.md`
- target_files_or_dirs: `docs/workflows/youtube_behavioral_contract_from_merged_main_v0.md`
- output_mode: file-write for this durable prompt artifact; paste-ready-chat copy is the courier surface for the filed prompt.
- downstream_controller_return_mode: paste-ready-chat delegated return; no durable review report is commissioned by this prompt.
- edit_permission: patch-only inside the target artifact; no commits, pushes, PR actions, code changes, or other docs edits.
- dirty_state_allowance: the receiving controller must start from a clean worktree except for the controller's own uncommitted patch to the named target.
- branch_or_commit_reference: branch `codex/youtube-behavioral-contract-extract`; target artifact was introduced at `5ebf288857003d8ee790a682bb407dca38e36173`.
- target_artifact_sha256: `2D0108FF40C7F8DC5F22EE6A2FE3FA2B2B32E7BF7F05E6939B850A27F6413DA8`
- doctrine_change_decision: no doctrine change authorized; this is a delegated review-and-patch prompt under existing provisional convention.
- isolation_decision: use the existing PR branch/worktree for review; do not create a new implementation lane unless the CA asks.
- validation_gates: fresh source read, target SHA check before edits, `git diff --check`, strict retrieval-header check on the target if patched, and final diff readback.
- thread_operating_target_continuity: no visible active `thread_operating_target` is carried; current workstream is PR #430 YT contract extraction.

Cynefin routing:

- Smallest complete outcome: review and patch only the YT contract extraction artifact, then return diff/citations/verdict for CA adjudication.
- Regime: complicated.
- Why: overlay review authority, source hierarchy, and target source claims must be checked, but the target and patch boundary are stable.
- Decomposition: layer-based source check, then artifact review, then bounded patch if needed.
- Current bottleneck: whether the artifact accurately reflects the named YT implementation/tests without overclaiming shared-core or acquisition parity.
- Riskiest assumption: the artifact's summary of residual/status/source-key semantics may omit a source-backed edge case or imply a broader contract than the YT implementation supports.
- Stop or pivot condition: return `NEEDS_ARCHITECTURE_PASS` if the issue is design-level rather than patchable inside the target artifact.
- Allowed next move: patch only the named target artifact and return an uncommitted diff plus citations.
- Disallowed next move: review your own work as the author, patch code, patch IG/shared-core design, edit adjacent docs, commit, push, or claim approval/readiness.

## Delegated Review-And-Patch Commission

Lane binding:

- overlay_status: provisional_opt_in
- operating_contract_pointer: `.agents/workflow-overlay/delegated-review-patch.md`
- review_lane: artifact (`workflow-adversarial-artifact-review`), with delegated patch execution bound only to the named target artifact
- mode: base-subagent
- access_mode: repo
- actor_model_family_receipt:
  - author_home_model_family: OpenAI/GPT, Codex/GPT-5 family
  - controller_model_family: `operator_to_fill`; must be a different upstream vendor/model lineage from OpenAI/GPT to satisfy cross-vendor discovery
  - current_receiving_actor_role: controller
  - dispatch_mode: external-controller-courier
  - de_correlation_status: controller must declare `satisfied` before review/patch work; if not satisfied, return `BLOCKED_CONTROLLER_NOT_DECORRELATED`
- de_correlation: this is a who-constraint, not a model recommendation. There is no recommended model block.
- subagent_authority: do not launch a replacement controller. If you are the controller, verify the receipt and proceed. If you are the author/home family, return `BLOCKED_CONTROLLER_NOT_DECORRELATED`.
- prompt_rendering: this filed prompt is the prompt-orchestrated route-out artifact. Do not substitute a summary, context pack, alternate checkout, or recreated source for direct repo/source inspection.

Target:

- label: `[yt-contract]`
- path: `docs/workflows/youtube_behavioral_contract_from_merged_main_v0.md`
- bounded_patch_scope: factual corrections, missing source-backed caveats, retrieval-header hygiene, and boundary tightening inside this one artifact only.
- why_read_only_insufficient: this artifact is the YT behavioral reference for the next IG sync/shared-core planning step; source-read-only critique would still require a correlated CA patch round-trip on the same blind spots. A de-correlated bounded patch pass is proportionate before handoff.
- off_scope: read-only/flag-only for every other file, including YT implementation, tests, IG artifacts, shared-core design notes, prompt templates, overlay files, generated/canonical/hash-pinned sources, review outputs, and any source outside this worktree.

Roles:

- author / CA / home model: adjudicates; owns what is kept.
- controller: de-correlated reviewer; owns findings, patch proposal, citations, verdict, and residual-risk note. The controller verdict is decision input, not final over the CA.
- patch executor: not split out for this small judgment-coupled artifact. Do not create a separate executor.

Review standard:

The controller's citations and changes are decision input only. The CA reserves final authority over what is kept and may veto any change at discretion when it judges the change adds no benefit or is net-negative, even an individually defensible change. Citations must be neutral in tone but decision-sufficient in substance; the argument belongs in the verdict and residual-risk note, not in the citations.

Escalation valve:

Return `NEEDS_ARCHITECTURE_PASS` and leave no kept patch if the target's problem is design-level, such as the whole artifact being the wrong abstraction or requiring a shared-core architecture decision before it can be corrected. Do not patch over design-level failure.

## Receiving Controller Instructions

You are performing a repo-mode delegated adversarial review-and-patch pass for Orca.

Do not start findings or patching until source context is ready.

1. REFERENCE-LOAD these method instructions. Do not APPLY them yet:
   - `workflow-deep-thinking`
   - `workflow-adversarial-artifact-review`
2. SOURCE-LOAD the required task sources below.
3. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
4. Only after source readiness, APPLY `workflow-deep-thinking` to frame failure modes and decision criteria.
5. Then APPLY `workflow-adversarial-artifact-review` to the target artifact.
6. Patch only `[yt-contract]` if a source-backed fix is smaller and more complete than returning findings alone.

If either required workflow skill is unavailable or cannot be applied after source readiness, return `BLOCKED_REVIEW_LANE_UNAVAILABLE` with the reason and do not patch.

If the runtime cannot open the named repo/worktree, sees the wrong target file hash before edits, sees a dirty state not caused by this pass, or cannot verify the named source files directly, return the nearest blocker rather than reviewing this prompt's summary.

## Repository Preflight

Expected repo/worktree:

- workspace path: `C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-behavioral-contract-extract`
- branch: `codex/youtube-behavioral-contract-extract`
- target artifact commit: `5ebf288857003d8ee790a682bb407dca38e36173`
- PR: `https://github.com/eric-foo/orca/pull/430`

Before reviewing:

1. Run `git status --short --branch`.
2. Confirm the target exists at `docs/workflows/youtube_behavioral_contract_from_merged_main_v0.md`.
3. Confirm the target SHA256 equals `2D0108FF40C7F8DC5F22EE6A2FE3FA2B2B32E7BF7F05E6939B850A27F6413DA8` before edits, or return `BLOCKED_TARGET_HASH_MISMATCH`.
4. Confirm you are a controller de-correlated from OpenAI/GPT family, or return `BLOCKED_CONTROLLER_NOT_DECORRELATED`.

## Required Sources

Authority and workflow sources:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/artifact-roles.md`
- `.agents/workflow-overlay/retrieval-metadata.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/delegated-review-patch.md`
- `.agents/workflow-overlay/decision-routing.md`

Review target:

- `[yt-contract]` `docs/workflows/youtube_behavioral_contract_from_merged_main_v0.md`

YT implementation/test sources that the target claims to summarize:

- `orca-harness/youtube_capture/behavioral_projection.py`
- `orca-harness/tests/unit/test_youtube_behavioral_projection.py`
- `orca-harness/tests/contract/test_youtube_behavioral_projection_no_runtime_imports.py`
- `orca-harness/data_lake/root.py`

Available but not default:

- `docs/workflows/shared_capture_core_ig_youtube_tiktok_planning_v0.md` only if needed to check whether the target's IG/shared-core transfer notes overstate the upstream goal.
- PR metadata for #430 only if needed to verify branch/revision context.

Do not bulk-load unrelated review outputs, all prompts, all product docs, all IG sources, or all harness code.

## Fitness Reference

This is an intent-bearing review target.

Goal: make `[yt-contract]` a reliable, source-backed YouTube behavior reference for the next IG sync lane.

Observable success signal: a fresh CA can compare IG behavior against YT behavior using `[yt-contract]` without relying on false YT source claims, acquisition-parity implications, or unmarked residual risk. This is an alignment axis to attack, not approval, validation, readiness, or a pass-if-matches bar.

## Review Focus

Attack material decision-relevant failure modes:

- inaccurate or incomplete extraction of YT metadata/comment, transcript-source, source-key, eligibility, rollup, residual, canonical-source, and acquisition-boundary behavior;
- claims that are not supported by the implementation/tests named above;
- omission of edge cases that materially affect IG comparison;
- accidental instruction that IG should copy YT acquisition machinery, source priority, packet shape, or transcript route;
- overclaiming validation, readiness, merge status, source-of-truth status, or shared-core design;
- retrieval metadata defects that make the artifact hard to recover correctly;
- review-target leakage from `jb` or external workflow policy.

Do not review whether the shared core should exist. Do not design the shared core. Do not patch IG behavior. Do not patch YT code or tests.

## Output Contract

Return findings first, ordered by severity:

- critical
- major
- minor

For each finding include:

- severity
- label: `[yt-contract]`
- location
- issue
- evidence with neutral source citation
- impact
- minimum_closure_condition
- next_authorized_action
- proposed correction or explanation why no patch is safe

If you patch:

- leave the patch uncommitted;
- return a unified diff for `[yt-contract]`;
- include per-change citations keyed to `[yt-contract]`;
- include the fresh post-patch target SHA256;
- run or state not-run for:
  - `git diff --check`
  - `python .agents/hooks/check_retrieval_header.py --strict docs/workflows/youtube_behavioral_contract_from_merged_main_v0.md`
- run a final readback of the patched target sections you changed.

If no patch is needed:

- say `NO_PATCH_NEEDED`;
- list residual risks or test/source gaps.

If blocked:

- return the nearest blocker and do not patch.

Close with:

```yaml
delegated_review_patch_return:
  status: PATCH_PROPOSED | NO_PATCH_NEEDED | NEEDS_ARCHITECTURE_PASS | BLOCKED
  de_correlation_status:
  access_mode: repo
  target_label: "[yt-contract]"
  target_path: docs/workflows/youtube_behavioral_contract_from_merged_main_v0.md
  target_sha_before:
  target_sha_after:
  patch_touched_files:
  validation:
  verdict:
  residual_risk:
  ca_adjudication_required: true
```

Review-use boundary: this return is decision input only. It is not approval, validation, readiness, mandatory remediation, source-of-truth promotion, or executor authority beyond the uncommitted bounded patch proposal. The CA must adjudicate every finding and diff hunk before anything is kept.
