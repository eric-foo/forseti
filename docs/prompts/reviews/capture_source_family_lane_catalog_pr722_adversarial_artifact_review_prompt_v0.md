# Capture Source-Family Lane Catalog PR #722 Adversarial Artifact Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Repo-bound, de-correlated adversarial artifact review prompt for PR #722,
  covering the capture source-family lane catalog and its Source Capture
  Playbook, toolbox, Data Capture submap, repo-map, and family-index wiring.
use_when:
  - Commissioning an independent reviewer to inspect PR #722 before CA adjudication.
  - Checking whether the source-family lane catalog makes known capture-to-lake
    routes cold-discoverable without forking Data Lake authority or granting runtime work.
  - Verifying that the owner-ratified option-1 authority split was implemented as
    the smallest complete documentation/index intervention.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/source-loading.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/delegated-review-patch.md
  - docs/prompts/handoffs/capture_playbook_lake_sync_handoff_v0.md
  - forseti/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
  - forseti/product/spines/capture/core/source_families/README.md
branch_or_commit: >
  PR #722 branch codex/capture-playbook-lake-sync; review target commit
  d9cb8d14 before this prompt artifact was added. The reviewer must refresh PR
  state and distinguish the filed prompt/report commits from the catalog target.
stale_if:
  - PR #722 target commit changes from d9cb8d14 without this prompt being updated.
  - The source_families catalog, Source Capture Playbook, Source Capture Toolbox
    README, Data Capture submap, or repo map is restructured after d9cb8d14.
  - A later prompt supersedes this PR #722 review commission.
```

## Orca Prompt Preflight

preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` v0 - constants bound; deltas stated below.

- authorization_basis: current owner request, "delegate review prompt", for the just-created PR #722 lane.
- template_kind: `review`; template source `docs/prompts/templates/review/adversarial_artifact_review_v0.md` plus `.agents/workflow-overlay/delegated-review-patch.md` boundary checks.
- output_mode: `review-report`.
- prompt_artifact_path: `docs/prompts/reviews/capture_source_family_lane_catalog_pr722_adversarial_artifact_review_prompt_v0.md`.
- review_report_destination: `docs/review-outputs/adversarial-artifact-reviews/capture_source_family_lane_catalog_pr722_adversarial_artifact_review_v0.md`.
- edit_permission: `read-only`; no patch execution is authorized by this prompt.
- target_scope: PR #722 source-family lane catalog target at commit `d9cb8d14`, excluding later prompt/report filing commits unless the prompt itself blocks review.
- branch_or_commit_reference: `codex/capture-playbook-lake-sync` at target commit `d9cb8d14`; base `main`.
- dirty_state_allowance: expected clean worktree at target commit. If dirty, classify whether changes are prompt/report filing only before reviewing; block strict review claims if target files differ from the pinned target without explicit CA acceptance.
- source_pack: custom `capture_source_family_lane_catalog_pr722_review_pack`.
- doctrine_change_decision: this review prompt does not change doctrine. The reviewed PR records an owner-ratified workflow-authority routing split; review it as target content.
- isolation_decision: read-only review of existing PR branch; no new branch required by the reviewer.
- validation_gates_to_inspect: retrieval-header strict check, repo-map freshness strict check, `git diff --check`, cold-route spot checks for TikTok and fragrance-native DB, and pre-push doc gates. Rerun only if repo access and tool state make it cheap; otherwise inspect recorded evidence and name not-run gaps.
- thread_operating_target_continuity: omitted; no visible active `thread_operating_target` block was supplied. The fitness reference is carried from the handoff Goal Handoff below.

## Delegated Review Boundary

This is a read-only de-correlated adversarial artifact review, not a delegated
review-and-patch commission.

Reason: PR #722 is a multi-file docs/index/catalog change. The provisional
delegated-review-and-patch convention requires a CA-named bounded patch target
and patch scope. No patch execution was commissioned here.

De-correlation is a who-constraint, not a runtime model recommendation:

- author_home_vendor_family: OpenAI / GPT-family Codex thread.
- controller_vendor_family: operator_to_fill.
- de_correlation_bar: `cross_vendor_discovery` only if controller vendor differs from OpenAI / GPT-family; otherwise record `same_vendor_sanity` or `self_fallback` and do not claim no-new-seam.
- reviewed_by: operator_to_fill in the durable report.
- authored_by: OpenAI / GPT-family Codex thread, exact runtime version unrecorded unless the operator supplies it.

If you believe patch execution is required, return
`BLOCKED_PATCH_EXECUTION_UNBOUND` with the material finding. Do not edit files.
Do not emit `patch_queue_entry`.

## Required Method Sequence

1. REFERENCE-LOAD these method/authority sources. Do not APPLY them yet:
   - `AGENTS.md`
   - `.agents/workflow-overlay/README.md`
   - `.agents/workflow-overlay/source-of-truth.md`
   - `.agents/workflow-overlay/source-loading.md`
   - `.agents/workflow-overlay/delegated-review-patch.md`
   - `.agents/workflow-overlay/review-lanes.md`
   - `.agents/workflow-overlay/prompt-orchestration.md`
   - `.agents/workflow-overlay/validation-gates.md`
   - `workflow-deep-thinking`
   - `workflow-adversarial-artifact-review`
2. SOURCE-LOAD the target source pack below.
3. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`. If incomplete, name missing sources and whether findings are blocked or advisory-only.
4. APPLY `workflow-deep-thinking` to frame failure modes and decision criteria.
5. APPLY `workflow-adversarial-artifact-review` to produce findings.

If `workflow-adversarial-artifact-review` is unavailable, unresolved, or cannot
be applied after source readiness, return a blocked or advisory-only result. Do
not emit formal validation, readiness, approval, mandatory remediation, or patch
authority claims.

## Review Target

PR: https://github.com/eric-foo/orca/pull/722

Review target branch: `codex/capture-playbook-lake-sync`

Pinned review target commit: `d9cb8d14`

Observed at prompt drafting:

- PR #722 was open and draft.
- Head branch: `codex/capture-playbook-lake-sync`.
- Head SHA: `d9cb8d14fafe1b4363de3adef5ca321b84c73683`.
- Base branch: `main`.
- Base SHA observed by connector: `e8ca2093ce7fad5d3d8b96b030c874f81655824a`.
- Target diff at `d9cb8d14`: 13 files changed, 534 insertions, 40 deletions.

This prompt artifact may be filed in a later commit on the same branch. Review
the catalog target at `d9cb8d14` unless the CA explicitly updates this prompt.

Target changed files at `d9cb8d14`:

- `docs/prompts/handoffs/capture_playbook_lake_sync_handoff_v0.md`
- `docs/workflows/data_capture_spine_consolidation_map_v0.md`
- `docs/workflows/forseti_repo_map_v0.md`
- `docs/workflows/repo_map_recent_changes/capture_source_family_lane_catalog_v0.md`
- `forseti/product/spines/capture/core/source_capture_toolbox/README.md`
- `forseti/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md`
- `forseti/product/spines/capture/core/source_families/README.md`
- `forseti/product/spines/capture/core/source_families/fragrance_native_database/README.md`
- `forseti/product/spines/capture/core/source_families/retail_pdp/README.md`
- `forseti/product/spines/capture/core/source_families/social_media/instagram/README.md`
- `forseti/product/spines/capture/core/source_families/social_media/reddit/README.md`
- `forseti/product/spines/capture/core/source_families/social_media/tiktok/README.md`
- `forseti/product/spines/capture/core/source_families/social_media/youtube/README.md`

## Review Purpose

Decide whether PR #722 gives future capture lanes a cold-discoverable,
source-specific route from the Source Capture Playbook/toolbox to every landed
capture-to-lake family index, while preserving the ratified authority split:

1. Source Capture Playbook / toolbox owns access method and shared capture discipline.
2. `source_families/` owns source-specific route homes tying access, runners, lake pointers, projection/ECR/Cleaning seams, and residuals.
3. Data Lake authority docs remain the storage/admission/bronze/silver authority and are pointed to, not restated or forked.

Fitness reference:

- Goal pointer: `docs/prompts/handoffs/capture_playbook_lake_sync_handoff_v0.md` -> Goal Handoff / Active Objective.
- Done looks like: a cold agent given "capture <source X> and land it in the lake" reaches source X's lane index from the toolbox/playbook within the cold-lane budget, and that lane index names access route, harness runner/projection/lake seam pointers, and Cleaning seam for every landed source family covered by the PR.

Treat this as a review axis to attack, not a pass bar.

## Source Pack

Do not review from this prompt text alone. If you cannot open the repo and the
PR branch or target commit, return `BLOCKED_REPO_ACCESS_MISSING`.

Minimum required reads:

1. `AGENTS.md` and `.agents/workflow-overlay/README.md`.
2. `.agents/workflow-overlay/source-loading.md`, `.agents/workflow-overlay/source-of-truth.md`, `.agents/workflow-overlay/review-lanes.md`, `.agents/workflow-overlay/prompt-orchestration.md`, `.agents/workflow-overlay/artifact-roles.md`, `.agents/workflow-overlay/retrieval-metadata.md`, and `.agents/workflow-overlay/validation-gates.md`.
3. PR #722 metadata and diff, refreshed from current source rather than trusting this prompt. Preferred checks:
   - `gh pr view 722 --repo eric-foo/orca --json number,title,state,isDraft,url,headRefName,headRefOid,baseRefName,baseRefOid,statusCheckRollup`
   - `git status --short --branch`
   - `git diff --name-status d9cb8d14^..d9cb8d14`
4. The handoff packet: `docs/prompts/handoffs/capture_playbook_lake_sync_handoff_v0.md`.
5. The Source Capture Toolbox and playbook surfaces:
   - `forseti/product/spines/capture/core/source_capture_toolbox/README.md`
   - `forseti/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md`
6. The new source-family catalog and family indexes:
   - `forseti/product/spines/capture/core/source_families/README.md`
   - `forseti/product/spines/capture/core/source_families/fragrance_native_database/README.md`
   - `forseti/product/spines/capture/core/source_families/retail_pdp/README.md`
   - `forseti/product/spines/capture/core/source_families/social_media/instagram/README.md`
   - `forseti/product/spines/capture/core/source_families/social_media/reddit/README.md`
   - `forseti/product/spines/capture/core/source_families/social_media/tiktok/README.md`
   - `forseti/product/spines/capture/core/source_families/social_media/youtube/README.md`
7. Navigation surfaces:
   - `docs/workflows/data_capture_spine_consolidation_map_v0.md`
   - `docs/workflows/forseti_repo_map_v0.md`
   - `docs/workflows/repo_map_recent_changes/capture_source_family_lane_catalog_v0.md`
8. Data Lake authority docs only as needed to check pointer-vs-restatement risk:
   - `forseti/product/spines/data_lake/README.md`
   - `forseti/product/spines/data_lake/authority/`

Available but do not bulk-load unless a finding depends on them:

- all `orca-harness/` runner/source_capture/cleaning files;
- all historical `docs/workflows/*handoff*` lane packets;
- all review outputs;
- all product proof or Judgment Spine artifacts;
- external workflow source outside this repo.

## Review Checks

Attack these failure modes first:

1. Cold route failure: from Source Capture Playbook/toolbox, a future lane still cannot find the right source-family route without repo archaeology.
2. Underfixing: the PR covers fragrance-native DB but leaves another landed source family with capture-to-lake code unhomed or unreachable from the catalog.
3. Overreach: the PR moves or restates Data Lake admission/storage/bronze/silver authority into playbook or lane indexes instead of pointing to lake authority.
4. Misclassification: Fragrantica, Parfumo, or Basenotes are incorrectly treated as `retail_pdp` instead of `fragrance_native_database`, or fragrance purchase-review surfaces are silently mis-homed.
5. Pointer asymmetry: source-family catalog, family READMEs, toolbox README, playbook, Data Capture submap, repo map, and recent-change note are not mutually discoverable enough for cold retrieval.
6. Source-specific route gaps: TikTok, YouTube, Reddit, Instagram, Retail/PDP, or fragrance-native DB indexes omit access route, runner/projection/lake/cleaning seam pointers, or residuals needed to keep later agents from rediscovering the lane.
7. False authority: a lane index or map row implies capture-run authorization, lake-write authorization, runtime readiness, validation, or source-of-truth promotion.
8. Handoff drift: the handoff still presents owner ratification as pending, uses "minimal" language that promotes underfixing, or contradicts the current owner instruction to apply SCI.
9. Enforcement candidate drift: the PR either skips evaluating the hook candidate entirely, or builds/commissions enforcement beyond the docs/index lane authority.
10. Repo-map freshness defect: `forseti_repo_map_v0.md` or the recent-change note fails to make the new route visible from standard map entry points.
11. Retrieval metadata defect: new or materially touched durable artifacts lack appropriate retrieval headers, open_next pointers, stale conditions, or correct `authority_boundary: retrieval_only`.
12. Review-scope contamination: this prompt or later report-filing commit is accidentally treated as part of the catalog target instead of a review artifact.

## Validation Evidence To Inspect

Use current evidence for final claims. The home lane reported these checks for
target commit `d9cb8d14`:

- `python .agents\hooks\check_retrieval_header.py --changed --strict`
- `python .agents\hooks\check_repo_map_freshness.py --changed --strict --message "repo-map-ack: worktrees/ is a local multi-worktree container, not a tracked navigation target."`
- `git diff --check HEAD~1..HEAD`
- cold-route spot checks for TikTok and Fragrantica;
- pre-push doc gates passed: `pre-push doc gates: OK (3 gate(s))`.

Do not convert recorded validation evidence into approval or readiness. Inspect
it, rerun it only when cheap and relevant, and preserve pass, fail, blocked, or
not-run status.

## Output Contract

Write the durable review report to:

`docs/review-outputs/adversarial-artifact-reviews/capture_source_family_lane_catalog_pr722_adversarial_artifact_review_v0.md`

The report must include:

- retrieval header with `artifact_role: Review output` and `authority_boundary: retrieval_only`;
- `reviewed_by` and `authored_by` provenance fields, with `unrecorded` allowed when not supplied;
- `de_correlation_bar`: `cross_vendor_discovery`, `same_vendor_sanity`, or `self_fallback`;
- `same_vendor_rationale` when `de_correlation_bar: same_vendor_sanity`;
- current PR metadata and branch/commit freshness receipt, including observed head, base, dirty state, and whether the review target is still `d9cb8d14`;
- source-read ledger with file paths and exact sections, commands, or line windows used;
- one compact `review_summary` YAML block using `.agents/workflow-overlay/communication-style.md`;
- findings first, ordered by `critical`, `major`, then `minor`;
- for each finding: severity, location, issue, evidence, impact, `minimum_closure_condition`, `next_authorized_action`, and advisory remediation direction;
- residual-risk note;
- explicit validation evidence inspected, rerun, blocked, failed, or not run.

Return only the compact `review_summary` YAML in chat after the report is
written. If the report cannot be written, return the failed `review_summary`
shape with `review_location: chat_only_current_thread` and
`recommendation: blocked`.

Suggested chat courier shape:

```yaml
review_summary:
  status: completed | blocked | advisory_only
  report_path: docs/review-outputs/adversarial-artifact-reviews/capture_source_family_lane_catalog_pr722_adversarial_artifact_review_v0.md
  recommendation: accept | accept_with_friction | patch_before_acceptance | reject | blocked
  reviewed_by: operator_to_fill
  authored_by: OpenAI / GPT-family Codex thread
  de_correlation_bar: cross_vendor_discovery | same_vendor_sanity | self_fallback
  summary: "One sentence describing the review result."
  findings_count: 0
  blocking_findings: []
  advisory_findings: []
  prior_findings_remediated: []
  next_action: "One concrete next step."
```

Review-use boundary: findings and non-findings are decision input only. They are
not approval, validation, product proof, mandatory remediation, patch authority,
merge readiness, or runtime authorization until the CA separately adjudicates
them.

## Forbidden Moves

- Do not review from a summary or context pack instead of inspecting the repo or PR branch directly.
- Do not widen the review beyond PR #722 source-family lane catalog target at `d9cb8d14`.
- Do not patch files, emit `patch_queue_entry`, commit, push, merge, mark the PR ready, or open another PR.
- Do not run captures, write lake data, edit runners, edit projections, edit Cleaning adapters, or operate runtime systems.
- Do not build the enforcement hook; review whether its deferral/evaluation is adequate.
- Do not claim validation, readiness, approval, mergeability, lifecycle completion, source-of-truth promotion, or no-new-seam status from this review.
- Do not recommend, rank, or imply runtime model choice.
- Do not import `jb` project policy or external workflow source as Orca/Forseti authority.
