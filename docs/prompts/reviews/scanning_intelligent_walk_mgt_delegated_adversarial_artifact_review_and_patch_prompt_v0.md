# Scanning Intelligent Walk MGT Delegated Adversarial Artifact Review-and-Patch Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Delegated review-and-patch prompt
scope: >
  Operator-couriered, de-correlated adversarial artifact review-and-patch
  commission for the Scanning Intelligent Walk MGT operating model. The target
  is a single high-stakes authored artifact. Companion guide and repo-map edits
  are read-only context unless a later Chief Architect adjudication expands the
  patch scope.
use_when:
  - Launching a delegated, de-correlated review-and-patch pass on the scanning MGT operating-model artifact.
  - Checking whether the operating model preserves bounded intelligent walking without reintroducing generic crawling, standing registries/monitors, packet-grade scanning, or scan-core ratification.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/source-loading.md
  - forseti/product/spines/scanning/scan_core/forseti_scanning_intelligent_walk_mgt_operating_model_v0.md
  - forseti/product/spines/foundation/vertical_exploration/forseti_vertical_exploration_guide_v0.md
  - docs/decisions/forseti_mini_god_tier_doctrine_v0.md
  - docs/decisions/forseti_venue_registry_rejection_decision_v0.md
  - forseti/product/spines/scanning/scan_core/forseti_demand_scan_core_spec_v0.md
input_hashes_sha256_worktree:
  scanning_intelligent_walk_mgt_operating_model: 35E57952D9092F5B91E67BDB43FDD4EA5FAE6006D07CF47D3F0B54A41374BA74
  vertical_exploration_guide: A7E7983A939687A2AA5C2A391ED6FCFF0A945BF0675EE6C11A43071D7C4AF0C3
  mini_god_tier_doctrine: 37036A30827073664F9C3D30B9AFA81A3FFD0B6A275CEF669AA2319E807D1D14
  venue_registry_rejection_decision: A14A667289305004F7CBA9102D97310810EF168FBD159E3DC53C9E7FE37D326C
  demand_scan_core_spec: 99C4C06A089FFE9C1CD6058139A2F1FF9D0F23C92498F3F510A26C28B8BD9A7E
  delegated_review_patch_overlay: 41F18F5879D8FAAB73015822E49376D91E03FF6E5CC4A0835B4F17E6FE7C8688
  review_lanes_overlay: AD4CCF88478BC726A7711E6480890D56A427108C609D1002EBDC40C88EF57D58
  prompt_orchestration_overlay: 64740C756AEC4A19F5218BCF275E05328B15B82AB62F08D9D977BB89CF849EE5
branch_or_commit:
  branch: codex/screening-read-service-build
  prompt_created_from_head: 60a69ddfd0d3a5a13edefa3e3f6556195f0311db
stale_if:
  - The target operating-model file hash differs from the value above before review starts.
  - The Vertical Exploration Guide, Mini God Tier doctrine, venue-registry rejection decision, Demand Scan-Core Spec, or Forseti review/prompt overlay files change materially before review starts.
  - The reviewer cannot access the target file and no no-repo package is supplied.
  - The operator cannot supply a de-correlated controller family or chooses a same-family/self reviewer while expecting cross-vendor discovery claims.
```

## Prompt Status

Status: `ROUTE_OUT_PROMPT_OPERATOR_FIELDS_TO_FILL`.

This prompt was generated because the target and purpose are inferable, but the
operator-owned route fields are not fully bound in this thread. It does not run
review, apply a patch, validate, accept, stage, commit, push, or claim the
artifact is ready. It gives the operator a filed prompt to courier to a
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
You are the controller for a Forseti delegated adversarial artifact review-and-patch commission.

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

Submitted target label: `[scan-mgt-model]`

Submitted target file:
- `forseti/product/spines/scanning/scan_core/forseti_scanning_intelligent_walk_mgt_operating_model_v0.md`

Bounded patch scope:
- Patch only the submitted target file.
- Patch only wording, boundaries, fields, accepted residuals, non-claims, or
  source-loading surface needed to make the MGT intelligent-walk operating
  model coherent and non-misleading.
- Do not edit the Vertical Exploration Guide, repo map, scan-core spec,
  delegated-review overlay, prompt overlay, review-lane overlay, MGT doctrine,
  venue-registry decision, source-family docs, capture docs, tests, code, or
  prompt files. Flag issues there as off-scope.

Why source-read-only review is insufficient:
- The artifact encodes a new high-leverage operating boundary after a rejected
  hybrid scan/capture direction. A read-only review can find issues, but the
  highest-value pass is a bounded hardening diff that closes ambiguous wording
  before the operating model is reused by later scan prompts or source-family
  adapters.

Required durable review report path:
- `docs/review-outputs/adversarial-artifact-reviews/scanning_intelligent_walk_mgt_operating_model_delegated_adversarial_artifact_review_v0.md`

Workspace:
- `C:\Users\vmon7\Desktop\projects\orca\worktrees\screening-read-service-build`

Pinned target state:
- branch at prompt creation: `codex/screening-read-service-build`
- prompt-created-from HEAD: `60a69ddfd0d3a5a13edefa3e3f6556195f0311db`
- target SHA256 at prompt creation: `35E57952D9092F5B91E67BDB43FDD4EA5FAE6006D07CF47D3F0B54A41374BA74`

The branch HEAD may be later than `60a69dd...` because this prompt artifact may
be committed after target creation. Proceed only if the submitted target file
hash still matches the pinned target hash, or else return `SOURCE_STALE_TARGET_CHANGED`.

Dirty-state allowance:
- The target file may be modified only by this delegated review-and-patch pass.
- The review report path may be created or overwritten only as the report for
  this commission.
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
- `docs/decisions/forseti_mini_god_tier_doctrine_v0.md`
- `docs/decisions/forseti_venue_registry_rejection_decision_v0.md`
- `forseti/product/spines/foundation/vertical_exploration/forseti_vertical_exploration_guide_v0.md`
- `forseti/product/spines/scanning/scan_core/forseti_scanning_intelligent_walk_mgt_operating_model_v0.md`
- `forseti/product/spines/scanning/scan_core/forseti_demand_scan_core_spec_v0.md`
- `forseti/product/spines/scanning/admissibility_checkability/forseti_demand_scan_gate_adjudication_packet_v0.md`
- `docs/decisions/screening_reddit_read_route_decision_v0.md`
- `docs/workflows/screening_read_service_build_receipt_v0.md`

Read source-family docs only if a target claim depends on a specific family:
- `forseti/product/spines/scanning/source_families/reddit/data_capture_spine_reddit_graph_frontier_lane_architecture_v0.md`
- `forseti/product/spines/scanning/source_families/linkedin/data_capture_spine_linkedin_lane_index_v0.md`
- `forseti/product/spines/scanning/source_families/answer_engine/demand_search_interest_sourcing_and_gate_delta_spec_v0.md`

Do not bulk-load unrelated Capture, ECR, Cleaning, Judgment, historical review
outputs, method-validation replays, research corpus, `_inbox`, or prompt
artifacts unless a directly material target issue cannot be assessed without one
narrow adjacent read.

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
2. `workflow-deep-thinking` to frame the operating-boundary problem and the
   artifact's fake-success paths.
3. `workflow-adversarial-artifact-review` to review the non-code target artifact.

If a required review lane is unavailable, unresolved, or cannot be applied
after source readiness, return `BLOCKED_REVIEW_LANE_UNAVAILABLE` with the
reason and do not patch. Do not silently emulate a review lane inline.

## Review Purpose And Fitness Reference

Review purpose:
- Determine whether `[scan-mgt-model]` correctly smiths scanning toward an MGT
  bounded intelligent-walk operating model without reopening forbidden crawler,
  registry, monitor, capture, route-binding, scan-authorization, or scan-core
  ratification scope.

Fitness reference:
- Goal: scanning should act like a high-signal scout: choose valuable public
  reads, summarize screen-light observations, promote only minimum-qualified
  evidence, and hand Capture precise capture requests.
- Observable success signal: a future scan prompt can use this artifact to
  steer frontier selection, branch decay/pivot, minimum evidence, and capture
  handoff while preserving explicit non-claims and accepted residuals.

Also attack the fitness reference itself: if this goal or success signal is the
wrong target for scanning MGT, say so as a finding instead of merely checking
whether the artifact matches it.

## Decision Criteria - Attack These Seams

Prioritize material failures over prose polish:

1. Does the artifact accidentally reintroduce generic crawling, standing
   monitoring, source atlas/registry, source map, dashboard, storage, or
   scheduler behavior despite saying it does not?
2. Does "bounded intelligent walk" differ operationally from generic crawling,
   or is it a relabel without enforceable frontier, pivot, and stop mechanics?
3. Is branch-aware pivoting coherent with the Vertical Exploration Guide's dry
   rule, or does it create a loophole that lets scans continue indefinitely?
4. Are the stop conditions strong enough for minimal/zero value, budget, access,
   source-policy, and capture-owned-route boundaries?
5. Is "minimum evidence, not quotas" concrete enough for a downstream scanner to
   know when a move promotes to observation and when an observation promotes to
   candidate observation?
6. Does the shared vocabulary normalize source-family outputs without
   weakening local source-family restrictions, especially Reddit
   orchestrator-mediated reads, LinkedIn no-contact/privacy rails, and AEO/search
   proposed/gap-bound status?
7. Is the capture_request contract sharp enough to prevent route binding,
   packet-grade capture, ECR, Cleaning, Judgment, or packet commitment from
   moving into scanning?
8. Does the gate-packaging section preserve the gate as inference instead of
   replacing it with quotas or raw counts?
9. Do accepted residuals satisfy the Mini God Tier doctrine: named, bounded,
   justified, remaining risk stated, upgrade trigger stated?
10. Does the artifact overclaim MGT as validation, readiness, source authority,
    buyer proof, live scan authorization, or scan-core ratification?
11. Does the artifact under-specify anything a future prompt author would
    otherwise invent, especially frontier expected-value reasons, branch close
    evidence, route-binding state, and capture-request fields?
12. Are any decisive claims unsupported by the target's `open_next` sources or
    by loaded Forseti authority?

## Patch Authority

Repo access mode:
- You may patch only `[scan-mgt-model]` if `access_mode: repo` and the receipt
  gate is satisfied.
- You may write the durable review report path named above.
- Everything else is read-only / flag-only.

No-repo mode:
- Do not patch. Return findings and suggested exact wording only. State that
  de-correlated patch authorship was not preserved and a bounded post-patch
  recheck is required before keep.

Hard stops:
- If a correct fix requires changing the Vertical Exploration Guide, scan-core
  spec, MGT doctrine, venue-registry decision, source-family docs, capture docs,
  review/prompt overlay, source code, tests, or another prompt, do not patch it.
  Flag it as off-scope.
- If the target has a design-level problem rather than patch-level wording or
  contract defects, return `NEEDS_ARCHITECTURE_PASS`, stop patching, revert any
  partial diff, and report findings only. A partial patch must not survive by
  inertia.

Do not stage, commit, push, install dependencies, run live network access, run
browser automation, invoke source-capture runners, generate packets, or perform
ECR, Cleaning, Judgment, outreach, or buyer-contact work.

## Output Contract

Write the full review report to:
- `docs/review-outputs/adversarial-artifact-reviews/scanning_intelligent_walk_mgt_operating_model_delegated_adversarial_artifact_review_v0.md`

Report structure:
1. Commission, lane binding, and actor/model-family receipt.
2. Source context status, including target hash verification.
3. Findings first, ordered by severity: critical, major, minor.
4. For each finding: artifact label `[scan-mgt-model]`, location, issue,
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
- Run a stale-language search for at least: generic crawler approval, standing
  monitor/registry approval, packet-grade scanning, route binding by scanning,
  live scan authorization, scan-core ratification, and readiness/validation
  overclaims.
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
It is not owner acceptance, validation proof, readiness, scan authorization,
capture authorization, crawler approval, registry approval, monitor approval,
source-access authorization, buyer proof, or permission to keep any patch
without Chief Architect adjudication.
````

## Prompt-Orchestrator Receipt

```yaml
prompt_orchestrator_receipt:
  requested_template_kind: review
  template_source_used:
    - docs/prompts/templates/review/adversarial_artifact_review_v0.md
    - docs/prompts/templates/shared/forseti_preflight_defaults_v0.md
  delegated_review_patch_overlay_status: provisional_opt_in
  operating_contract_pointer: .agents/workflow-overlay/delegated-review-patch.md
  selected_review_lane: workflow-adversarial-artifact-review
  mode: base-subagent
  terminal_output_mode: filed_prompt_plus_paste_ready_copy
  output_mode: file-write
  downstream_review_output_mode: review-report
  downstream_report_path: docs/review-outputs/adversarial-artifact-reviews/scanning_intelligent_walk_mgt_operating_model_delegated_adversarial_artifact_review_v0.md
  actor_model_family_receipt_required: true
  actor_model_family_receipt_status: operator_to_fill_at_courier_runtime
  patch_authority: single submitted target file only
  target_file: forseti/product/spines/scanning/scan_core/forseti_scanning_intelligent_walk_mgt_operating_model_v0.md
  read_only_context:
    - forseti/product/spines/foundation/vertical_exploration/forseti_vertical_exploration_guide_v0.md
    - docs/workflows/orca_repo_map_v0.md
    - docs/decisions/forseti_mini_god_tier_doctrine_v0.md
    - docs/decisions/forseti_venue_registry_rejection_decision_v0.md
    - forseti/product/spines/scanning/scan_core/forseti_demand_scan_core_spec_v0.md
  ca_adjudication_required_before_keep: true
  needs_architecture_pass_valve: true
  source_context_status: prompt_author_sources_loaded_for_prompt_creation
  validation_status: prompt_artifact_written_only; delegated_review_not_run
  operator_to_fill:
    - controller_model_family
    - access_mode
    - reviewed_by_value_for_report
  non_claims:
    - review not run by this prompt artifact
    - delegated patch not applied or kept by this prompt artifact
    - no auto-keep; all delegated diffs require Chief Architect adjudication
    - no validation/readiness/acceptance claim
    - no runtime model recommendation or model ranking
    - no scan, capture, crawler, monitor, registry, packet, ECR, Cleaning, Judgment, outreach, or buyer-contact authorization
```