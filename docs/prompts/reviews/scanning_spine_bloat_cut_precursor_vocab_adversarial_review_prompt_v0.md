# Scanning Spine Bloat Cut + Precursor Vocab Adversarial Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Filed adversarial review prompt for the scanning spine bloat-cut and precursor
  vocabulary change packet at commit 8e70605c1e24ad38997d7c94bcdbd67da1728f3f.
use_when:
  - Commissioning an independent adversarial review of the scanning spine cleanup change packet.
  - Checking the route-out from delegated-review-patch when the target is multi-file and patch authority is not bound.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/review-lanes.md
branch_or_commit: 8e70605c1e24ad38997d7c94bcdbd67da1728f3f
stale_if:
  - The target commit is rebased, amended, or superseded.
  - The delegated-review-patch overlay becomes a bound multi-file patch lane.
  - The report destination below is already occupied by a different review.
```

## Prompt Orchestrator Receipt

```yaml
orchestrator_mode: route_out_review_prompt
requested_skill: workflow-delegated-review-patch
lane_mode: provisional_opt_in_route_out
terminal_output_mode: filed_prompt_plus_paste_ready_copy
why_not_bound_delegated_patch: >
  Orca delegated review-and-patch is provisional and single-target for patch
  authority. The inferred target here is a multi-file docs/product-spine change
  packet, so this prompt routes to read-only adversarial artifact review. It does
  not authorize patching.
preflight_defaults: docs/prompts/templates/shared/orca_preflight_defaults_v0.md v0 - constants bound; deltas stated below.
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom_change_packet_review
  edit_permission: read-only
  target_scope: scanning spine bloat cut plus precursor vocabulary alignment commit
  dirty_state_checked: yes
  blocked_if_missing: repo access to the target commit or a pasted source capsule
repo_map_decision: loaded
repo_map_reason: repo map was updated by the target commit and is one of the reviewed surfaces
workspace_path: C:\Users\vmon7\Desktop\projects\orca\worktrees\screening-read-service-build
expected_branch: codex/screening-read-service-build
target_commit: 8e70605c1e24ad38997d7c94bcdbd67da1728f3f
target_parent: 777a3988b2ad10e5c37269fa1ca80bd0f1d5724d
dirty_state_allowance: clean checkout preferred; unrelated dirty state blocks strict review claims
controlling_source_state: clean when prompt was authored, before this prompt file was added
output_mode: review-report
report_destination: docs/review-outputs/adversarial-artifact-reviews/scanning_spine_bloat_cut_precursor_vocab_adversarial_review_v0.md
template_kind: review
template_source: docs/prompts/templates/review/adversarial_artifact_review_v0.md
workflow_sequence_policy: overlay_owned
workflow_sequence_source: active_overlay
workflow_sequence_status: bound
thread_operating_target_continuity:
  carried_forward: no
  reason: no_visible_active_target
  changed_from_input: no
  lifecycle_status: not_applicable
doctrine_change_decision: >
  The reviewed commit changes product/workflow routing inside the scanning
  spine; the prompt itself is a review prompt and does not change doctrine.
non_claims:
  - not a bound delegated review-and-patch execution
  - not patch authorization
  - not validation
  - not readiness
  - not acceptance of the target commit
```

## Fitness Reference

Goal: the scanning spine should become easier to enter and harder to misuse.

Done looks like: a fresh reviewer can follow one front door, understand precursor
signals without treating them as demand proof or capture authority, and find no
live stale routing from the moved AEO probe artifacts back into product-spine
authority.

The goal and signal are review axes to attack, not a pass-if-matches bar.

## Paste-Ready Prompt

````markdown
# Adversarial Review Prompt: Scanning Spine Bloat Cut + Precursor Vocab

You are performing a read-only adversarial artifact review for Orca.

Do not patch files. Do not commit, stage, push, merge, or open a PR. If the right
fix requires patching, report the finding and the minimum closure condition only.

## Required Method Sequence

1. REFERENCE-LOAD these method instructions as procedural guidance only:
   - `workflow-deep-thinking`
   - `workflow-adversarial-artifact-review`
2. Do not APPLY either method yet.
3. SOURCE-LOAD the required sources below.
4. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
5. Only after source readiness, APPLY `workflow-deep-thinking` to frame failure
   modes and review criteria.
6. Then APPLY `workflow-adversarial-artifact-review`.

If `workflow-adversarial-artifact-review` is unavailable, unresolved, or cannot
be applied after source readiness, return a blocked or advisory-only result. Do
not emit formal verdicts, validation claims, readiness claims, mandatory
remediation, patch queues, executor-ready handoffs, or alignment-complete claims.

## Review Target

Target commit:
`8e70605c1e24ad38997d7c94bcdbd67da1728f3f`

Target parent:
`777a3988b2ad10e5c37269fa1ca80bd0f1d5724d`

Branch:
`codex/screening-read-service-build`

Review the change packet, not the entire repository. Use:

```powershell
git show --find-renames --stat --patch 8e70605c1e24ad38997d7c94bcdbd67da1728f3f
```

Changed files in scope:

- `docs/migration/repo_structure_spine_first_v0/moved_paths_index.md`
- `docs/migration/repo_structure_spine_first_v0/moves_manifest.csv`
- `docs/research/answer_engine/aeo_capture_feasibility_probe_phase0_v0.md`
- `docs/research/answer_engine/aeo_capture_feasibility_probe_phase0_v0_evidence.json`
- `docs/workflows/orca_repo_map_v0.md`
- `orca/product/spines/scanning/README.md`
- `orca/product/spines/scanning/scan_core/orca_demand_scan_core_spec_v0.md`
- `orca/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md`
- `orca/product/spines/scanning/source_families/answer_engine/demand_search_interest_sourcing_and_gate_delta_spec_v0.md`
- `orca/product/spines/scanning/source_families/linkedin/data_capture_spine_linkedin_discovery_planning_lane_architecture_v0.md`
- `orca/product/spines/scanning/source_families/linkedin/data_capture_spine_linkedin_lane_index_v0.md`
- `orca/product/spines/scanning/source_families/reddit/data_capture_spine_reddit_graph_frontier_lane_architecture_v0.md`

## Delegated Review-Patch Route-Out Boundary

The request came through `workflow-delegated-review-patch`, but Orca's current
delegated review-and-patch convention is provisional and patch-authorized only
for a single Chief-Architect-named target artifact. This target is a multi-file
docs/product-spine change packet. Therefore:

- perform read-only adversarial artifact review;
- do not apply patches;
- do not claim repo-mode delegated review-and-patch ran;
- do not claim cross-vendor no-new-seam unless the operator actually supplies a
  cross-vendor reviewer and the report records that fact;
- if a patch is needed, report a finding with `minimum_closure_condition` and
  `next_authorized_action: CA adjudication or bounded patch commission`.

This is a who-constraint only, not runtime model routing or a model
recommendation. Runtime reviewer choice is operator/tooling owned.

## Review Purpose

Decide whether the scanning-spine cleanup introduced material routing,
authority, vocabulary, or stale-reference defects that should be adjudicated
before the branch is merged.

Attack these axes:

- whether the new scanning front door really reduces source-loading bloat
  without becoming a new authority layer;
- whether `precursor_signal`, `precursor_surface`, and `signal_stage` stay
  separate from gate proof, candidate promotion, and capture authorization;
- whether scan-core's `capture_request` alias keeps old "capture-needs list"
  language searchable without preserving stale vocabulary as authority;
- whether Reddit, LinkedIn, and answer-engine adapters map local terms into the
  shared vocabulary without losing source-specific hard stops;
- whether moving AEO Phase-0 evidence to `docs/research/answer_engine/` removes
  product-spine authority leakage and leaves live resolver paths coherent;
- whether repo-map and migration resolver edits are sufficient, or whether live
  stale references remain outside historical migration/review snapshots;
- whether the direction-change propagation receipt in
  `orca/product/spines/scanning/README.md` is complete enough for future agents;
- whether validation evidence is accurately characterized, especially the
  placement checker's exit-0 advisory debt.

## Fitness Reference

Goal: the scanning spine should become easier to enter and harder to misuse.

Done looks like: a fresh reviewer can follow one front door, understand precursor
signals without treating them as demand proof or capture authority, and find no
live stale routing from the moved AEO probe artifacts back into product-spine
authority.

Attack this goal and signal. Do not treat them as a pass bar.

## Required Authority Sources

Read these first:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/delegated-review-patch.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/validation-gates.md`
- `.agents/workflow-overlay/communication-style.md`
- `.agents/workflow-overlay/retrieval-metadata.md`
- `.agents/workflow-overlay/artifact-roles.md`

Then read the review target diff and only the target files or targeted sections
needed to support findings. Prefer the commit diff over full-file loading. If a
full-file read is needed, prioritize:

- `orca/product/spines/scanning/README.md`
- `orca/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md`
- `orca/product/spines/scanning/scan_core/orca_demand_scan_core_spec_v0.md`
- `orca/product/spines/scanning/source_families/answer_engine/demand_search_interest_sourcing_and_gate_delta_spec_v0.md`

Available but not default-loaded unless material:

- historical review snapshots under `docs/review-inputs/**`;
- older search-lane migration package under `docs/migration/repo_structure_search_lane_v0/**`;
- unrelated scanning/capture/case-family artifacts outside the changed files.

## Validation Evidence To Inspect

Dispatcher reported these before filing this prompt. Treat them as claims to
inspect or rerun only when useful; they are not approval:

- `git diff --cached --check`: clean before commit.
- `python .agents/hooks/check_retrieval_header.py --changed`: exit 0.
- `python .agents/hooks/check_repo_map_freshness.py --changed`: exit 0.
- `python .agents/hooks/check_map_links.py --strict`: OK, 0 findings.
- `python .agents/hooks/check_placement.py --check`: exit 0 with known
  repo-wide advisory debt: 11 violations, 4 freshness warnings, 869
  legacy-tolerated items.
- Stale-language scans found remaining precursor/gate hits only in explicit
  "not proof" safeguards, old capture-needs wording only in an explicit alias,
  and old AEO path hits only in live resolver rows or historical migration/review
  records.

If you rerun checks, state the exact command, cwd, and observed result. If you
do not rerun, say `not_run`.

## Output Mode

Use `review-report`.

Write the durable report to:

`docs/review-outputs/adversarial-artifact-reviews/scanning_spine_bloat_cut_precursor_vocab_adversarial_review_v0.md`

The report is read-only review output. Include a retrieval header. Record:

- `reviewed_by`: operator/tooling-supplied model+version, or `unrecorded`;
- `authored_by`: `gpt-5-codex` if accepted by the operator as the artifact
  author provenance, otherwise `unrecorded`;
- `de_correlation_bar`: `cross_vendor_discovery` | `same_vendor_sanity` |
  `self_fallback` | `unrecorded`;
- for `same_vendor_sanity`, include `same_vendor_rationale`.

Do not fabricate provenance. A present `unrecorded` value is a visible
measurement gap, not success.

After writing the report, return only this courier YAML in chat:

```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/adversarial-artifact-reviews/scanning_spine_bloat_cut_precursor_vocab_adversarial_review_v0.md
  recommendation: accept | accept_with_friction | patch_before_acceptance | reject | blocked
  reviewed_by: unrecorded
  authored_by: gpt-5-codex
  summary: "One sentence describing the review result."
  findings_count: 0
  blocking_findings: []
  advisory_findings: []
  prior_findings_remediated: []
  next_action: "One concrete next step."
```

If the report cannot be written, do not use `report_path`. Return the failed
chat-only summary shape from `.agents/workflow-overlay/communication-style.md`
and name the failed path.

## Findings Contract

List findings first in the report, ordered by severity:

- `critical`
- `major`
- `minor`

For each finding include:

- severity;
- location with file and line where possible;
- issue;
- evidence;
- impact;
- `minimum_closure_condition`;
- `next_authorized_action`;
- advisory remediation direction.

Do not include `patch_queue_entry`. Do not provide executor-ready patch
instructions. Optional hardening may be listed only when clearly labeled
optional and non-required.

If no issues are found, say so clearly and list residual risks or test gaps.

## Review-Use Boundary

This review is decision input only. It is not approval, validation, readiness,
mandatory remediation, product proof, merge authorization, or executor-ready
patch authority. The Chief Architect adjudicates any findings or proposed next
steps separately.
````