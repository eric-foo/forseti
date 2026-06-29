# Data Lake Capture Propagation Classification Delegated Adversarial Review-and-Patch Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Delegated review-and-patch prompt
scope: >
  Operator-couriered, de-correlated adversarial artifact review-and-patch
  commission for the Data Lake / Capture propagation classification proposal.
  The submitted target is one proposal artifact on PR #455; all other paths are
  read-only or flag-only context.
use_when:
  - Launching a delegated, de-correlated review-and-patch pass on the Data Lake / Capture propagation classification proposal.
  - Checking whether the proposal correctly keeps Data Lake, packet-runner seam, platform behavioral parity, acquisition-route, and downstream residual propagation classes separate.
  - Stress-testing the proposal's Mini God Tier fit, architecture-planning triage, and before/after claims before owner acceptance.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/source-loading.md
  - docs/prompts/templates/review/adversarial_artifact_review_v0.md
  - docs/decisions/data_lake_capture_propagation_classification_contract_proposal_v0.md
  - docs/decisions/orca_mini_god_tier_doctrine_v0.md
input_hashes_sha256_worktree:
  data_lake_capture_propagation_classification_contract_proposal: 48C9B6F6F726107BF44F965469436F13694B3BEF63B056BEE0DA4126E362F791
  delegated_review_patch_overlay: 320D44868564C505AB0B127DDC6A86FB9BA7F5AD682CD4C298FDF2952E2D1B8E
  review_lanes_overlay: 4E219765446B4B473FC773E548AC380E85DAA96E5C82F26076F389C855C09A0E
  prompt_orchestration_overlay: 64740C756AEC4A19F5218BCF275E05328B15B82AB62F08D9D977BB89CF849EE5
  source_loading_overlay: 8FADC263B98F08B73B68E44DE71709D4AAF7FEA5D2E0390602B93E7863E11AB3
  adversarial_artifact_review_template: B7355D6D02CFC522D213DEE3F28ED4B824899BC997084EFEE98DF5A710518CC4
branch_or_commit:
  branch: codex/data-lake-capture-propagation-proposal
  prompt_created_from_head: 4b20397ee426998bc727a1642d97f47d0c559a1c
  target_file_git_blob: 87cb36913dc772afdad21c4a8b67cfd05c766b48
stale_if:
  - The submitted target file hash differs before review starts.
  - The delegated-review-patch, prompt-orchestration, review-lanes, source-loading, or adversarial artifact review template sources change materially before review starts.
  - The operator cannot supply a de-correlated controller family or chooses a same-family/self reviewer while expecting cross-vendor discovery claims.
  - PR #455 or the branch target changes so the proposal under review is no longer this proposal artifact.
```

## Prompt Status

Status: `ROUTE_OUT_PROMPT_OPERATOR_FIELDS_TO_FILL`.

This prompt was generated because the target and review purpose are inferable,
but the downstream controller identity and launch access facts are
operator-owned. This prompt does not run the review, apply a patch, validate,
accept, stage, commit, push, merge, or claim the proposal is ready. It gives the
operator a filed prompt to courier to a de-correlated controller.

Operator fields to fill before launch:

```yaml
operator_to_fill:
  controller_model_family: ""
  access_mode: repo | no_repo
  controller_report_destination_confirmed: yes | no
  reviewed_by_value_for_report: ""
```

If `access_mode: repo`, the controller may patch only the single submitted
target file and may write the single report destination named below. If
`access_mode: no_repo`, the controller is advisory-only and must return findings,
not a working-tree diff; the Chief Architect applies any accepted change later.

## Binding Receipt

```yaml
delegated_review_patch_overlay_interface:
  status: provisional_opt_in
  operating_contract_pointer: .agents/workflow-overlay/delegated-review-patch.md
  protected_path_list: .agents/workflow-overlay/safety-rules.md
  model_ladder: operator-owned; no concrete model ids bound in overlay
  prompt_orchestrator_available: yes, applied for this filed prompt
  preflight_schema:
    - .agents/workflow-overlay/source-loading.md orca_start_preflight
    - docs/prompts/templates/shared/orca_preflight_defaults_v0.md
  source_context_fields: .agents/workflow-overlay/prompt-orchestration.md Source-Gated Method Contract
  output_destinations:
    delegate_return: paste-ready courier plus unified diff or no-patch statement
    durable_review_report: docs/review-outputs/adversarial-artifact-reviews/data_lake_capture_propagation_classification_delegated_adversarial_review_patch_v0.md
    patch_application: single submitted target file only, uncommitted and unstaged
```

This binding is a route-out prompt under a provisional convention. It is not a
bound Orca review lane, validation, readiness, approval, or model-routing
decision.

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
discovery, no-new-seam coverage, or de-correlated discovery.

If `current_receiving_actor_role` is `controller`, proceed as the controller
after the receipt is satisfied. Do not launch a replacement controller and do
not spawn recursive or unrelated subagents.

## Commission

Submitted target label: `[data-lake-propagation-proposal]`

Submitted target file:
- `docs/decisions/data_lake_capture_propagation_classification_contract_proposal_v0.md`

Bounded patch scope:
- Patch only the submitted target file.
- Patch only wording, classifications, accepted residuals, non-claims, source
  basis, review questions, or owner-decision framing needed to make the proposal
  coherent and non-misleading.
- Do not edit Data Lake authority, Capture authority, ECR, Cleaning, Judgment,
  projection doctrine, overlay files, repo maps, prompt files, review outputs
  other than the report destination, code, tests, scripts, data, or PR metadata.
  Flag issues there as off-scope.

Why source-read-only review is insufficient:
- The proposal is the candidate controlling shape for future Data Lake / Capture
  propagation doctrine. A read-only review can find issues, but a bounded
  hardening diff can directly close local ambiguity in the proposal before the
  owner decides whether to accept the controlling home. The Chief Architect
  still adjudicates every returned change before anything is kept.

Required durable review report path:
- `docs/review-outputs/adversarial-artifact-reviews/data_lake_capture_propagation_classification_delegated_adversarial_review_patch_v0.md`

Workspace:
- `C:\Users\vmon7\Desktop\projects\orca\worktrees\data-lake-capture-propagation-proposal`

Pinned target state:
- branch at prompt creation: `codex/data-lake-capture-propagation-proposal`
- prompt-created-from HEAD: `4b20397ee426998bc727a1642d97f47d0c559a1c`
- target git blob at prompt creation: `87cb36913dc772afdad21c4a8b67cfd05c766b48`
- target SHA256 at prompt creation: `48C9B6F6F726107BF44F965469436F13694B3BEF63B056BEE0DA4126E362F791`
- PR: `https://github.com/eric-foo/orca/pull/455`

The branch HEAD may be later than `4b20397e...` because this prompt artifact may
be committed after target creation. Proceed only if the submitted target file
hash still matches the pinned target hash, or else return
`SOURCE_STALE_TARGET_CHANGED`.

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
- `.agents/workflow-overlay/artifact-roles.md`
- `.agents/workflow-overlay/retrieval-metadata.md`
- `docs/prompts/templates/review/adversarial_artifact_review_v0.md`
- `docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md`
- `docs/prompts/templates/shared/orca_preflight_defaults_v0.md`
- `docs/decisions/orca_mini_god_tier_doctrine_v0.md`
- `docs/decisions/data_lake_capture_propagation_classification_contract_proposal_v0.md`

Then read the proposal's `Source Basis Ledger`. Open the source files named
there when a finding, non-finding, or patch depends on the proposal's claim
about that source. Do not treat the proposal's summary as a substitute for the
named primary source when the claim is load-bearing.

Do not bulk-load unrelated Capture, ECR, Cleaning, Judgment, review outputs,
research corpus, `_inbox`, prompt artifacts, or all product docs unless a
directly material target issue cannot be assessed without one narrow adjacent
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
2. `workflow-deep-thinking` to frame the Data Lake / Capture propagation
   boundary problem, fake-success paths, and decision criteria.
3. `workflow-adversarial-artifact-review` to review the non-code target
   proposal.

If a required review lane is unavailable, unresolved, or cannot be applied
after source readiness, return `BLOCKED_REVIEW_LANE_UNAVAILABLE` with the
reason and do not patch. Do not silently emulate a strict review lane inline.

## Orca Start Preflight

```yaml
orca_start_preflight:
  agents_read: required_before_review
  overlay_read: required_before_review
  source_pack: bounded custom Data Lake / Capture propagation proposal review pack
  repo_map_decision: not_needed_for_routing; this commission supplies the target and context paths
  workspace: C:\Users\vmon7\Desktop\projects\orca\worktrees\data-lake-capture-propagation-proposal
  expected_branch: codex/data-lake-capture-propagation-proposal
  branch_or_commit_reference: 4b20397ee426998bc727a1642d97f47d0c559a1c plus target hash gate
  dirty_state_allowance: target file and report path only, created or modified by this pass
  target_scope:
    - docs/decisions/data_lake_capture_propagation_classification_contract_proposal_v0.md
  output_mode: review-report
  edit_permission: patch-only single target + review-report file-write
  durable_report_destination: docs/review-outputs/adversarial-artifact-reviews/data_lake_capture_propagation_classification_delegated_adversarial_review_patch_v0.md
  doctrine_change_decision: >
    This review may patch the proposal's wording only. If the correct fix changes
    accepted product, architecture, workflow, validation, review, output, or
    lifecycle doctrine outside the submitted target, return NEEDS_ARCHITECTURE_PASS.
  isolation_decision: existing lane worktree for PR #455; no new worktree
    creation or branch switch authorized for the controller
  thread_operating_target_continuity: omitted; no visible active thread_operating_target was supplied in this launch prompt
preflight_defaults: docs/prompts/templates/shared/orca_preflight_defaults_v0.md v0 - constants bound; deltas stated here.
```

## Review Purpose And Fitness Reference

Review purpose:
- Determine whether `[data-lake-propagation-proposal]` is the right smallest
  complete proposal for classifying future propagation work across Data Lake,
  SourceCapturePacket runner lake seams, platform behavioral projections,
  source-family-local acquisition routes, and downstream residual/completeness
  semantics.

Fitness reference:
- Goal: give the owner a trustworthy choice about whether to accept a narrow
  Data Lake / Capture propagation classification contract instead of broad
  overlay workflow doctrine or platform acquisition-route convergence.
- Observable success signal: after reading the proposal and named sources, a
  future agent can decide which propagation bucket applies before patching, can
  identify when architecture planning is actually needed, can see why the shape
  is or is not Mini God Tier compatible, and can understand the before/after
  behavioral change without inferring validation, readiness, or implementation
  authority.

Treat this fitness reference as an axis to attack, not as a pass bar.

## Review Questions

Attack these axes directly:

1. Does the five-bucket classification correctly separate generic Data Lake /
   downstream boundary changes, raw packet-runner lake seams, platform
   behavioral parity, source-family-local acquisition routes, and downstream
   residual/completeness semantics?
2. Does the proposed controlling home under Data Lake authority fit the actual
   product-architecture boundary, or does the issue really require Capture,
   projection doctrine, ECR, overlay workflow authority, or a broader
   architecture-planning lane?
3. Is the statement that full `workflow-architecture-planning` is not required
   before this proposal defensible, and are the escalation triggers complete
   enough?
4. Is the Mini God Tier section correct under
   `docs/decisions/orca_mini_god_tier_doctrine_v0.md`: owner-invoked lens,
   named accepted residuals, no validation/readiness/proof claim, and no scope
   expansion?
5. Does the before/after section describe only the effect after a later accepted
   contract is patched, without implying that this proposal itself changes
   doctrine or enforcement?
6. Does the proposal correctly avoid a `direction_change_propagation` receipt
   for the proposal artifact, while clearly requiring one for any later
   controlling-source patch?
7. Does the raw packet-runner seam stay scoped to raw `SourceCapturePacket`
   producers and the existing lake-seam coverage test, without silently pulling
   every runner under Data Lake doctrine?
8. Does the behavioral parity bucket preserve shared projection obligations
   without copying YouTube acquisition mechanics into Instagram/TikTok or
   Instagram route mechanics into YouTube/TikTok?
9. Does the source-family-local bucket correctly require at least two
   non-overlapping source families plus owner acceptance before promoting a
   platform-independent primitive?
10. Does the downstream residual/completeness bucket preserve projection,
    ECR/Cleaning, Data Lake medallion, and Gold/Judgment containment boundaries?
11. Are the source basis ledger and key checked observations faithful to the
    named primary sources, or are there unsupported claims, stale hashes, or
    summary-over-source substitutions?
12. Is there any design-level defect that cannot be patched inside the proposal
    file without changing the recommended controlling home or source hierarchy?

Severity labels (`critical`/`major`/`minor`) are finding-priority only. Findings
need `severity`, `location`, `issue`, `evidence` with source citation, `impact`,
`minimum_closure_condition`, `next_authorized_action`, and advisory remediation
direction.

## Bounded Patch

- Patch ONLY the submitted target file, directly in the working tree. Do not
  commit, stage, push, update the PR, or edit any other file.
- Patch what your accepted-by-you findings justify under Smallest Complete
  Intervention. No style sweeps, no broader doctrine rewrite, no source-map
  patch, and no nice-to-have refactor.
- Off-scope is flag-only: if the correct fix lies in Data Lake authority,
  Capture authority, projection doctrine, ECR, Cleaning, Judgment, the overlay,
  the repo map, validation hooks, code, tests, or another proposal/report, record
  it as a finding and leave those files untouched.
- Escalation valve: if the artifact's problem is design-level rather than
  patch-level, return `NEEDS_ARCHITECTURE_PASS`, stop patching, revert any
  partial target diff, and return findings only.
- Citations: provide neutral, decision-sufficient citations for each change.

## Required Validation

For this artifact pass, validation means document and repository hygiene, not
runtime, platform, data-lake, or implementation validation.

Run after any patch, or state why each command could not be run:

```powershell
git diff --check
python .agents\hooks\check_retrieval_header.py --strict --changed
python .agents\hooks\check_dcp_receipt.py --strict --changed
python .agents\hooks\check_dcp_receipt_hygiene.py --strict --changed
python .agents\hooks\check_review_output_provenance.py --strict --changed
```

Also fresh-read:

- the patched target section(s);
- the report file after writing it;
- `git diff --stat`;
- `git status --short --branch`.

Do not run live capture, web capture, data migration, lake archive commands,
storage writes, implementation tests, or package installs unless a later
separate authority explicitly binds them.

## Output Contract

Write the durable report to exactly:

`docs/review-outputs/adversarial-artifact-reviews/data_lake_capture_propagation_classification_delegated_adversarial_review_patch_v0.md`

The report must include:

1. Actor receipt:
   - `authored_by`: OpenAI / GPT-family Codex lane; exact model/version
     `unrecorded` unless operator supplies it.
   - `reviewed_by`: operator/tooling-supplied; use `unrecorded` if not supplied.
   - `de_correlation_bar`: `cross_vendor_discovery`, `same_vendor_sanity`, or
     `self_fallback`.
   - `controller_model_family`: recorded family or `unrecorded`; if not
     different from OpenAI / GPT-family Codex, do not claim cross-vendor
     discovery.
2. `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
3. Findings first, ordered by severity: `critical`, `major`, `minor`.
4. For each finding:
   - target location;
   - evidence with source citation;
   - impact;
   - minimum closure condition;
   - next authorized action;
   - whether you patched it.
5. Patch summary, if any.
6. Unified diff, if any.
7. Validation commands and observed output, or not-run reasons.
8. Accepted residuals and remaining risk.
9. Verdict: `PATCHED_FOR_CA_ADJUDICATION`,
   `NO_PATCH_NEEDED_FOR_CA_ADJUDICATION`, `NEEDS_ARCHITECTURE_PASS`, or
   `BLOCKED`.

Then return a compact courier message in chat:

```yaml
review_summary:
  status: completed | failed
  report_path: docs/review-outputs/adversarial-artifact-reviews/data_lake_capture_propagation_classification_delegated_adversarial_review_patch_v0.md
  recommendation: PATCHED_FOR_CA_ADJUDICATION | NO_PATCH_NEEDED_FOR_CA_ADJUDICATION | NEEDS_ARCHITECTURE_PASS | BLOCKED
  summary: "<one paragraph>"
  next_action: "<what the Chief Architect should adjudicate next>"
```

Your diff, citations, and verdict are claims to adjudicate, not premises to
inherit. The Chief Architect/home model decides what is kept and may reject any
patch even if individually defensible.

## Non-Claims

This commission runs under a provisional, opt-in convention. It creates no
formal review lane, validation, readiness, proof, lifecycle claim, owner
acceptance, implementation authorization, runtime authority, source-access
authorization, commit authority, push authority, PR authority, or model-routing
decision. The target remains a proposal pending Chief Architect adjudication and
owner steering regardless of this pass's outcome.
````
