# IG Daily Heartbeat Operating Policy Delegated Adversarial Review-and-Patch Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Delegated review-and-patch prompt
scope: >
  Operator-couriered, de-correlated adversarial artifact review-and-patch
  commission for the IG Daily Heartbeat Operating Policy v0. The editable target
  is one authored policy artifact; companion docs and the PR diff are read-only
  context unless a later Chief Architect adjudication expands the patch scope.
use_when:
  - Launching a delegated, de-correlated review-and-patch pass on the IG daily heartbeat policy.
  - Checking whether the policy preserves daily registered-creator monitoring while keeping onboarding separate.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/source-loading.md
  - .agents/workflow-overlay/safety-rules.md
  - docs/prompts/templates/review/adversarial_artifact_review_v0.md
  - docs/prompts/templates/shared/orca_preflight_defaults_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/instagram/ig_daily_heartbeat_operating_policy_v0.md
branch_or_commit:
  branch: codex/ig-daily-heartbeat-policy
  target_commit_before_prompt: 280fddd7a44e3b809a64f74d3b7606870a9957bf
input_hashes_sha256_worktree:
  ig_daily_heartbeat_operating_policy: 37D5AD256D51A282B1DB145330AC649692E69DE834A7C29D7E5F1EC4B56DA7C5
  delegated_review_patch_overlay: 9591607EE7783878BE5802D35AAFEA48C45269FFA72903366F0CCC21AF9085DF
  review_lanes_overlay: 74B617A202A8181D02F67C28175403E666A627632976EECB1C87F5CC5D852081
  prompt_orchestration_overlay: F471E2A263930EDCF25FD0B3AC1F695B18277081810598C0C1CD06143179EE78
  source_loading_overlay: F25AF717E382BA183CE35A3422DBEC1B5FB7396312FDECD590E31F4AC53E5467
  safety_rules_overlay: F6D22DFD6DE2285D65F3E72D0EAAC3A405EBF6CCF328168BB0CFC8D230217FFC
  adversarial_artifact_review_template: B3186C622A4C2C386AB0110F8164414A26F880E95A5E9789FC7D0EC873DAD41F
  preflight_defaults_template: B4408BF408758ECC57EB676FCE06CAB4DB81963846E51F8AF6FD09FFD94D87E8
stale_if:
  - The submitted target file hash differs before review starts.
  - The delegated-review-patch, review-lanes, prompt-orchestration, source-loading, or safety-rules overlay files change materially before review starts.
  - A later owner decision changes the IG daily heartbeat posture, onboarding separation, or two-egress 2.5k/day target.
  - The controller cannot inspect the pinned worktree or branch and no no-repo package is supplied.
```

## Prompt Status

Status: `ROUTE_OUT_PROMPT_OPERATOR_FIELDS_TO_FILL`.

This prompt was filed because the target and review purpose are inferable, but
the operator-owned route fields are not fully bound in this thread. It does not
run review, apply a patch, validate, accept, stage, commit, push, or claim the
policy is ready. It gives the operator a filed prompt to courier to a
de-correlated controller.

Operator fields to fill before launch:

```yaml
operator_to_fill:
  controller_model_family: ""
  access_mode: repo | no_repo
  controller_report_destination_confirmed: yes | no
  reviewed_by_value_for_report: ""
```

If `access_mode: repo`, the controller may patch only the single submitted
target file named below and may write the review report. If `access_mode:
no_repo`, the controller is advisory-only and must return findings, not a diff;
the Chief Architect applies any accepted change later and runs the required
bounded post-patch recheck before keep.

## Launch Prompt

````text
You are the controller for an Orca delegated adversarial artifact review-and-patch commission.

This is a `workflow-delegated-review-patch` commission in `base-subagent` mode.
De-correlation is a who-constraint, not a model recommendation. Do not add a
Recommended model block, do not rank runtime models, and do not treat this
commission as runtime model routing.

## Actor / Model-Family Receipt Gate

Before reading the target artifact or adjacent sources, complete this receipt
with actual operator/tooling facts:

```yaml
actor_model_family_receipt:
  author_home_model_family: OpenAI / GPT-family Codex lane
  controller_model_family: operator_to_fill_different_vendor_or_model_lineage
  current_receiving_actor_role: controller
  dispatch_mode: external-controller-courier
  access_mode: repo | no_repo
  de_correlation_status: satisfied | blocked
```

If `controller_model_family` is missing, same-family as
`author_home_model_family`, ambiguous, or still a placeholder, stop before
review and return `BLOCKED_DECORRELATION_RECEIPT_MISSING` or
`BLOCKED_CONTROLLER_NOT_DECORRELATED`. If the operator intentionally chooses a
same-vendor sanity pass, record that limitation and do not claim cross-vendor
discovery or no-new-seam coverage.

If `current_receiving_actor_role` is `controller`, proceed as the controller
after the receipt is satisfied. Do not launch a replacement controller and do
not spawn recursive or unrelated subagents.

## Commission

Submitted target label: `[ig-heartbeat-policy]`

Submitted target file:
- `forseti/product/spines/capture/core/source_families/social_media/instagram/ig_daily_heartbeat_operating_policy_v0.md`

Bounded patch scope:
- Patch only the submitted target file.
- Patch only wording, boundaries, deferred items, non-claims, source-loading
  surface, or policy clauses needed to make the IG daily heartbeat operating
  policy coherent and non-misleading.
- Do not edit the IG README, grid DOM spec, monitoring architecture, at-scale
  envelope, cadence decision, runner code, prompts, overlay files, tests, or
  any onboarding policy. Flag issues there as off-scope.

Why source-read-only review is insufficient:
- The artifact encodes a high-leverage operating boundary for future IG runner
  behavior: daily registered-creator grid heartbeat, no pagination by default,
  read-only operation, supervised challenge handling, two-egress 2.5k/day
  posture, and breakout-only deep capture while keeping onboarding separate. A
  findings-only review can identify issues, but the highest-value pass is a
  bounded hardening diff that closes ambiguous wording before the policy becomes
  a runner or strategy input.

Required durable review report path:
- `docs/review-outputs/adversarial-artifact-reviews/ig_daily_heartbeat_operating_policy_delegated_adversarial_artifact_review_v0.md`

Workspace:
- `C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\ig-daily-heartbeat-policy`

Pinned target state:
- branch at prompt creation: `codex/ig-daily-heartbeat-policy`
- target commit before this prompt artifact: `280fddd7a44e3b809a64f74d3b7606870a9957bf`
- target SHA256 at prompt creation: `37D5AD256D51A282B1DB145330AC649692E69DE834A7C29D7E5F1EC4B56DA7C5`

The branch HEAD may be later than `280fddd7` because this prompt artifact may
be committed after target creation. Proceed only if the submitted target file
hash still matches the pinned target hash, or else return `SOURCE_STALE_TARGET_CHANGED`.

Dirty-state allowance:
- The target file may be modified only by this delegated review-and-patch pass.
- The review report path may be created or overwritten only as the report for
  this commission.
- The prompt file itself may be present in the branch.
- Unrelated dirty or untracked files are out of scope. Do not inspect or patch
  them unless one narrow adjacent read is necessary to understand a target issue.
- Do not create, clone, request, or switch worktrees. Read the current worktree
  in place.

## Required Authority Sources

Read and follow:
- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/delegated-review-patch.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/validation-gates.md`
- `.agents/workflow-overlay/safety-rules.md`
- `.agents/workflow-overlay/communication-style.md`
- `docs/prompts/templates/review/adversarial_artifact_review_v0.md`
- `docs/prompts/templates/shared/orca_preflight_defaults_v0.md`
- `forseti/product/spines/capture/core/source_families/social_media/instagram/ig_daily_heartbeat_operating_policy_v0.md`

Read-only companion context:
- `forseti/product/spines/capture/core/source_families/social_media/instagram/README.md`
- `forseti/product/spines/capture/core/source_families/social_media/instagram/ig_profile_grid_dom_engagement_recon_and_spec_v0.md`
- `forseti/product/spines/capture/core/source_families/social_media/instagram/ig_at_scale_operating_envelope_v0.md`
- `forseti/product/spines/capture/core/source_families/social_media/instagram/forseti_creator_monitoring_policy_architecture_v0.md`
- `docs/decisions/ig_reels_capture_cadence_durability_doctrine_v0.md`

Do not bulk-load unrelated Capture, ECR, Cleaning, Judgment, research corpus,
review outputs, method-validation replays, `_inbox`, or prompt artifacts unless
a directly material target issue cannot be assessed without one narrow adjacent
read.

## Source-Gated Method Contract

REFERENCE-LOAD:
- `workflow-delegated-review-patch`
- `workflow-deep-thinking`
- `workflow-adversarial-artifact-review`

Do not APPLY these methods before source readiness. SOURCE-LOAD the required
sources and declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.

After source readiness, APPLY:
1. `workflow-delegated-review-patch` to enforce receipt, role, scope, patch,
   citation, escalation, and Chief Architect adjudication boundaries.
2. `workflow-deep-thinking` to frame the runner-policy boundary problem and the
   fake-success paths.
3. `workflow-adversarial-artifact-review` to review the non-code target artifact.

If a required review lane is unavailable, unresolved, or cannot be applied
after source readiness, return `BLOCKED_REVIEW_LANE_UNAVAILABLE` with the
reason and do not patch. Do not silently emulate a review lane inline.

## Review Purpose And Fitness Reference

Review purpose:
- Determine whether `[ig-heartbeat-policy]` records the current owner direction
  for steady-state IG creator monitoring without reintroducing stale sparse
  cadence, pagination, platform-write actions, stealth claims, random deep
  capture, code-alignment claims, or onboarding capture scope.

Fitness reference:
- Goal: a future runner or strategy lane can implement daily registered-creator
  first-visible-grid heartbeat for IG while preserving read-only behavior,
  supervised challenge handling, additive time-series monitoring, two-egress
  2.5k/day posture, and a strict boundary between steady-state monitoring and
  onboarding.
- Observable success signal: a downstream lane can translate the policy into
  runner metadata or implementation tasks without inventing missing behavior,
  importing onboarding top-band capture, treating DOM reads as invisible,
  claiming account safety, or reviving A/B/C sparse cadence as the current
  default.

Also attack the fitness reference itself: if this goal or success signal is the
wrong target for the policy, say so as a finding instead of merely checking
whether the artifact matches it.

## Decision Criteria - Attack These Seams

Prioritize material failures over prose polish:

1. Does the policy clearly say heartbeat observations are additive time-series
   points, not destructive refreshes?
2. Does it preserve the current owner decision that all registered IG creators
   are daily for now, without quietly keeping A/B/C sparse cadence as the
   current operating default?
3. Does the 2.5k/day / two-egress posture stay honest: serious but not proven,
   no "green/yellow/red" overclaim, no exact public-IP persistence, and no
   third-egress setup unless telemetry proves need?
4. Does "first visible grid only" actually exclude pagination, scroll expansion,
   item fan-out, comment capture, and random deep captures by default?
5. Is the breakout-only deep-capture boundary sharp enough: deep capture only
   for tagged `spike_candidate`, `fresh_breakout_candidate`,
   `active_breakout_candidate`, or `durable_breakout_candidate` posts?
6. Does the policy prevent onboarding top-band/intake capture from leaking into
   steady-state daily heartbeat?
7. Does the asset posture avoid false safety or stealth claims while still
   distinguishing ordinary supervised browser loading from heavy-asset
   bandwidth mode?
8. Does the DOM language avoid the false claim that local DOM parsing is
   invisible to the platform?
9. Does challenge handling block fake success: pause, notify owner, bounded
   wait, no auto-solve, no route-around, no retry-harder behavior, and
   missingness rather than zero?
10. Does the read-only boundary ban automated likes/comments/follows/saves/DMs
    while correctly treating manual owner behavior as out of band?
11. Does the future runner metadata target avoid implying current code
    alignment, validation, account safety, platform permission, or live-capture
    authorization?
12. Do the companion docs still contradict the target in a way that would
    misroute a future agent? If yes, flag it as off-scope rather than editing
    companion docs.
13. Are any decisive claims unsupported by the target's `open_next` sources,
    loaded Orca authority, or current owner direction?

## Patch Authority

Repo access mode:
- You may patch only `[ig-heartbeat-policy]` if `access_mode: repo` and the
  receipt gate is satisfied.
- You may write the durable review report path named above.
- Everything else is read-only / flag-only.

No-repo mode:
- Do not patch. Return findings and suggested exact wording only. State that
  de-correlated patch authorship was not preserved and a bounded post-patch
  recheck is required before keep.

Hard stops:
- If a correct fix requires changing the IG README, grid DOM spec, monitoring
  architecture, at-scale envelope, cadence decision, runner code, prompt
  policy, overlay files, or onboarding policy, do not patch it. Flag it as
  off-scope.
- If the target has a design-level problem rather than patch-level wording or
  contract defects, return `NEEDS_ARCHITECTURE_PASS`, stop patching, revert any
  partial diff, and report findings only. A partial patch must not survive by
  inertia.

Do not stage, commit, push, install dependencies, run live network access, run
browser automation, operate IG/YT/TikTok, capture source packets, or perform
ECR, Cleaning, Judgment, outreach, or buyer-contact work.

## Output Contract

Write the full review report to:
- `docs/review-outputs/adversarial-artifact-reviews/ig_daily_heartbeat_operating_policy_delegated_adversarial_artifact_review_v0.md`

Report structure:
1. Commission, lane binding, and actor/model-family receipt.
2. Source context status, including target hash verification.
3. Findings first, ordered by severity: critical, major, minor.
4. For each finding: artifact label `[ig-heartbeat-policy]`, location, issue,
   evidence, impact, minimum_closure_condition, next_authorized_action, and
   whether patched.
5. Unified diff for any target-file changes.
6. Per-change neutral source citations that are decision-sufficient in substance.
7. Controller verdict and residual-risk note.
8. Validation/readback status, including exact commands or searches run or not
   run.
9. Off-scope flags.
10. Chief Architect adjudication packet.
11. Review-use boundary.

Controller output contract:
- invoke the selected review lane; if unavailable, return
  `BLOCKED_REVIEW_LANE_UNAVAILABLE` and do not patch;
- return findings plus any bounded unified diff;
- keep citation authority with the controller;
- keep citations neutral in tone and decision-sufficient in substance;
- return `NEEDS_ARCHITECTURE_PASS` for design-level problems, with no kept
  partial diff;
- do not commit, stage, or claim acceptance.

Chief Architect adjudication packet:
- state that the diff, citations, and verdict are claims to adjudicate, not
  premises to inherit;
- list each proposed change with its citation and intended closure condition;
- state whether each change is ready for Chief Architect accept / modify /
  reject adjudication;
- state any rejected/off-scope/design-level findings separately;
- do not claim a patch is kept, accepted, validated, or ready until the Chief
  Architect adjudicates it.

Validation/readback expectations:
- If you patch the target, run a targeted readback of the patched sections and
  `git diff --check`.
- Run a stale-language search for at least: `A/B/C sparse cadence current`,
  `random 0-2`, `paginate`, `scroll expansion`, `DOM invisible`, `stealth`,
  `auto-solve`, `route around`, `platform write`, `onboarding top-band`,
  `code alignment`, `validated`, and `account-safety proof`.
- If you do not patch, state `not_run` and why.

After writing the report, return a compact chat summary with:
- report path;
- whether patches were applied;
- changed files;
- validation/readback evidence;
- verdict or recommendation;
- next action: Chief Architect adjudication if any diff was proposed.

Review-use boundary:
This delegated review-and-patch result is decision input only. The controller's
diff, citations, and verdict are claims to adjudicate, not premises to inherit.
It is not owner acceptance, validation proof, readiness, account-safety proof,
platform permission, anti-detection proof, live-capture authorization, runner
implementation alignment, onboarding policy, source-capture authorization, or
permission to keep any patch without Chief Architect adjudication.
````

## Prompt-Orchestrator Receipt

```yaml
prompt_orchestrator_receipt:
  requested_template_kind: review
  template_source_used:
    - docs/prompts/templates/review/adversarial_artifact_review_v0.md
    - docs/prompts/templates/shared/orca_preflight_defaults_v0.md
  delegated_review_patch_overlay_status: provisional_opt_in
  operating_contract_pointer: .agents/workflow-overlay/delegated-review-patch.md
  selected_review_lane: workflow-adversarial-artifact-review
  mode: base-subagent
  terminal_output_mode: filed_prompt_plus_paste_ready_copy
  output_mode: file-write
  downstream_review_output_mode: review-report
  downstream_report_path: docs/review-outputs/adversarial-artifact-reviews/ig_daily_heartbeat_operating_policy_delegated_adversarial_artifact_review_v0.md
  actor_model_family_receipt_required: true
  actor_model_family_receipt_status: operator_to_fill_at_courier_runtime
  patch_authority: single submitted target file only
  target_file: forseti/product/spines/capture/core/source_families/social_media/instagram/ig_daily_heartbeat_operating_policy_v0.md
  read_only_context:
    - forseti/product/spines/capture/core/source_families/social_media/instagram/README.md
    - forseti/product/spines/capture/core/source_families/social_media/instagram/ig_profile_grid_dom_engagement_recon_and_spec_v0.md
    - forseti/product/spines/capture/core/source_families/social_media/instagram/ig_at_scale_operating_envelope_v0.md
    - forseti/product/spines/capture/core/source_families/social_media/instagram/forseti_creator_monitoring_policy_architecture_v0.md
    - docs/decisions/ig_reels_capture_cadence_durability_doctrine_v0.md
  ca_adjudication_required_before_keep: true
  needs_architecture_pass_valve: true
  source_context_status: prompt_author_sources_loaded_for_prompt_creation
  validation_status: prompt_artifact_written_only; delegated_review_not_run
  operator_to_fill:
    - controller_model_family
    - access_mode
    - controller_report_destination_confirmed
    - reviewed_by_value_for_report
  non_claims:
    - review not run by this prompt artifact
    - delegated patch not applied or kept by this prompt artifact
    - no auto-keep; all delegated diffs require Chief Architect adjudication
    - no validation/readiness/acceptance claim
    - no runtime model recommendation or model ranking
    - no IG/YT/TikTok operation, browser automation, live capture, capture packet, source-access, ECR, Cleaning, Judgment, outreach, or buyer-contact authorization
```

## Authoring Preflight Receipt

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom
  edit_permission: docs-write
  target_scope: >
    File one durable delegated adversarial review-and-patch prompt for the IG
    daily heartbeat operating policy. Does not run the review, patch the policy,
    or change runner behavior.
  dirty_state_checked: yes
  blocked_if_missing: none
preflight_defaults: docs/prompts/templates/shared/orca_preflight_defaults_v0.md v0 - constants bound; deltas stated in this prompt.
authorization_basis: current user instruction to delegate adversarial review patch.
objective_intended_decision: >
  Enable an independent de-correlated controller to harden the IG daily
  heartbeat policy, then return a diff and citations for Chief Architect
  adjudication.
target_files_or_dirs:
  - docs/prompts/reviews/ig_daily_heartbeat_operating_policy_delegated_adversarial_review_patch_prompt_v0.md
source_pack_bounded_reads:
  - AGENTS.md supplied in thread
  - .agents/workflow-overlay/README.md
  - .agents/workflow-overlay/source-of-truth.md
  - .agents/workflow-overlay/source-loading.md
  - .agents/workflow-overlay/decision-routing.md
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/template-registry.md
  - .agents/workflow-overlay/artifact-folders.md
  - .agents/workflow-overlay/artifact-roles.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/retrieval-metadata.md
  - .agents/workflow-overlay/validation-gates.md
  - .agents/workflow-overlay/safety-rules.md
  - .agents/workflow-overlay/communication-style.md
  - docs/prompts/templates/review/adversarial_artifact_review_v0.md
  - docs/prompts/templates/shared/orca_preflight_defaults_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/instagram/ig_daily_heartbeat_operating_policy_v0.md
  - representative prior delegated review-and-patch prompt examples
output_mode: file-write
edit_permission: docs-write for this prompt artifact only
dirty_state_allowance: clean worktree before prompt file creation; prompt file is the only intended new dirty file
controlling_source_state: checked for target branch prompt authoring; prompt file does not assert overlay readiness or runner validation
branch_or_commit_reference: codex/ig-daily-heartbeat-policy @ 280fddd7a44e3b809a64f74d3b7606870a9957bf before prompt file creation
doctrine_change_decision: no doctrine change by prompt artifact; it routes a review of the policy and changes no policy itself
isolation_decision: existing clean PR worktree on codex/ig-daily-heartbeat-policy; prompt attaches to the reviewed policy branch without creating a second branch
validation_gates:
  - git diff --check
  - python .agents/hooks/check_placement.py --strict
  - targeted stale/leakage search for prompt anti-patterns
thread_operating_target_continuity: no visible active thread_operating_target supplied; omitted
```

## Non-Claims

- This prompt does not run the delegated review.
- This prompt does not patch, validate, accept, or keep the IG policy.
- This prompt does not create a bound Orca review lane.
- This prompt does not recommend, rank, or select a runtime model.
- This prompt does not authorize runner implementation, live capture, browser automation, source access, platform interaction, or onboarding-policy changes.
