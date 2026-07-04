# Capture Source-Family Lane Catalog PR #722 Post-Patch Adversarial Artifact Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Repo-bound adversarial artifact review recheck prompt for PR #722 after the
  post-review capture source-family lane catalog seam fix at commit 414063dd.
  The review checks whether prior AR-01/AR-02 closure is real, whether AR-03
  remains only advisory friction, and whether the patch introduced any
  blocker/major route-layer regressions inside the touched scope.
use_when:
  - Commissioning a post-patch adversarial artifact review of PR #722.
  - Checking whether the vendor_pricing_page and audience-post seam fixes close
    the prior review findings without reopening the whole catalog review.
  - Verifying that the lane still preserves the owner-ratified three-way
    authority split after the seam patch.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/source-loading.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/review-lanes.md
  - docs/prompts/reviews/capture_source_family_lane_catalog_pr722_adversarial_artifact_review_prompt_v0.md
  - docs/prompts/handoffs/capture_playbook_lake_sync_handoff_v0.md
  - forseti/product/spines/capture/core/source_families/README.md
branch_or_commit: >
  PR #722 branch codex/capture-playbook-lake-sync; review target commit
  414063dd, whose parent is e4b3e29f. This prompt may be filed in a later commit
  on the same branch; the reviewer must exclude later prompt/report filing
  commits from the patch target unless they touch the named target scope.
stale_if:
  - PR #722 target commit changes from 414063dd without this prompt being updated.
  - The source_families catalog, Source Capture Toolbox README, Data Capture
    submap, repo map, vendor_pricing_page README, Instagram README, or YouTube
    README changes after 414063dd.
  - A later prompt supersedes this post-patch review commission.
```

## Forseti Prompt Preflight

preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` v0 - constants bound; deltas stated below.

- authorization_basis: current owner request, "prompt the delegate review once again", after PR #722 post-review patch commit `414063dd`.
- template_kind: `review`; template source `docs/prompts/templates/review/adversarial_artifact_review_v0.md` plus the patch-recheck economy in `workflow-prompt-orchestrator`.
- output_mode: `review-report`.
- prompt_artifact_path: `docs/prompts/reviews/capture_source_family_lane_catalog_pr722_post_patch_adversarial_artifact_review_prompt_v0.md`.
- review_report_destination: `docs/review-outputs/adversarial-artifact-reviews/capture_source_family_lane_catalog_pr722_post_patch_adversarial_artifact_review_v0.md`.
- edit_permission: `read-only` for source files; the reviewer may write only the named review report.
- target_scope: bounded post-patch review of commit `414063dd` only, with parent `e4b3e29f`; exclude later prompt/report filing commits.
- dirty_state_allowance: expected clean tracked target at `414063dd`. If dirty, classify whether changes are review-output/prompt-only before reviewing; block strict review claims if any target files differ from `414063dd` without explicit CA acceptance.
- source_pack: custom `capture_source_family_lane_catalog_pr722_post_patch_recheck_pack`.
- doctrine_change_decision: this prompt does not change doctrine. It commissions a read-only review recheck of a docs/index patch.
- isolation_decision: read-only review of existing PR branch; no new branch required by the reviewer.
- validation_gates_to_inspect: retrieval-header strict check, repo-map freshness strict check, header index, map links, `git diff --check`, and pre-push doc gates evidence when available. Rerun only if repo/tool state makes it cheap.
- thread_operating_target_continuity: omitted; no visible active `thread_operating_target` block was supplied. Fitness reference is the handoff Goal Handoff / Active Objective.

## Delegated Review Boundary

This is a read-only post-patch adversarial artifact review prompt, not a patch
execution commission and not a delegated review-and-patch prompt.

De-correlation is a who-constraint, not a runtime model recommendation:

- authored_by: OpenAI / GPT-family Codex thread, exact runtime version unrecorded unless operator supplies it.
- reviewed_by: operator_to_fill in the durable report.
- de_correlation_bar: `cross_vendor_discovery`, `same_vendor_sanity`, or `self_fallback`.
- same_vendor_rationale: required when `de_correlation_bar: same_vendor_sanity`.

A bounded post-patch sanity review may use `same_vendor_sanity`; it must not
claim full discovery or no-new-seam unless the operator actually supplies a
cross-vendor discovery reviewer. Do not recommend, rank, or imply any runtime
model choice.

If patch execution is needed, return a finding with
`next_authorized_action: CA adjudication / patch authorization required`. Do not
edit source files and do not emit `patch_queue_entry`.

## Required Method Sequence

1. REFERENCE-LOAD these method/authority sources. Do not APPLY them yet:
   - `AGENTS.md`
   - `.agents/workflow-overlay/README.md`
   - `.agents/workflow-overlay/source-of-truth.md`
   - `.agents/workflow-overlay/source-loading.md`
   - `.agents/workflow-overlay/review-lanes.md`
   - `.agents/workflow-overlay/prompt-orchestration.md`
   - `.agents/workflow-overlay/validation-gates.md`
   - `workflow-deep-thinking`
   - `workflow-adversarial-artifact-review`
2. SOURCE-LOAD the target source pack below.
3. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`. If incomplete, name missing sources and whether findings are blocked or advisory-only.
4. APPLY `workflow-deep-thinking` to frame the bounded patch-recheck failure modes before findings.
5. APPLY `workflow-adversarial-artifact-review` to produce findings.

If `workflow-adversarial-artifact-review` is unavailable, unresolved, or cannot
be applied after source readiness, return a blocked or advisory-only result. Do
not emit formal validation, readiness, approval, mandatory remediation, or patch
authority claims.

## Review Target

PR: https://github.com/eric-foo/orca/pull/722

Review target branch: `codex/capture-playbook-lake-sync`

Pinned post-patch target commit: `414063dd`

Patch parent: `e4b3e29f`

Prior catalog target reviewed: `d9cb8d14`

Post-patch target files changed by `414063dd`:

- `docs/workflows/data_capture_spine_consolidation_map_v0.md`
- `docs/workflows/forseti_repo_map_v0.md`
- `docs/workflows/repo_map_recent_changes/capture_source_family_lane_catalog_v0.md`
- `forseti/product/spines/capture/core/source_capture_toolbox/README.md`
- `forseti/product/spines/capture/core/source_families/README.md`
- `forseti/product/spines/capture/core/source_families/social_media/instagram/README.md`
- `forseti/product/spines/capture/core/source_families/social_media/youtube/README.md`
- `forseti/product/spines/capture/core/source_families/vendor_pricing_page/README.md`

Observed post-patch commit stat at prompt drafting:

```text
414063dd docs: cover missing capture lane catalog seams
8 files changed, 75 insertions(+), 6 deletions(-)
create mode 100644 forseti/product/spines/capture/core/source_families/vendor_pricing_page/README.md
```

This prompt may be filed after `414063dd`. Review the patch at `414063dd`
against `e4b3e29f` unless the CA explicitly updates this prompt.

## Prior Review Context

Prior review prompt:

`docs/prompts/reviews/capture_source_family_lane_catalog_pr722_adversarial_artifact_review_prompt_v0.md`

Prior review report path expected by that prompt:

`docs/review-outputs/adversarial-artifact-reviews/capture_source_family_lane_catalog_pr722_adversarial_artifact_review_v0.md`

At post-patch prompt drafting, that report existed as a local untracked file in
the lane worktree, not as a committed branch artifact. Local SHA256 observed:

`BCD8858D885A9F6D1E1F8F03437FE7418F4344E4940A34014FBAC558AB6BBD67`

If the prior report is unavailable in your review environment, use the frozen
prior-finding capsule below as the unresolved-delta source. Do not substitute a
summary for inspecting the post-patch repo target itself.

Frozen prior findings capsule:

- `AR-01 critical`: `vendor_pricing_page` was a landed, literal source family (`run_source_capture_price_payload_packet.py` emits `source_family="vendor_pricing_page"`) but had no source-family lane index or catalog/toolbox/submap/repo-map route. Minimum closure: add a lane index/row across routing surfaces or record explicit out-of-scope authority; preserve enough inventory evidence to show the miss class is not recurring.
- `AR-02 major`: `audience_post` capture/cleaning seam for Instagram and YouTube (`source_capture/audience_post_packet.py`, `cleaning/audience_post_input.py`, `cleaning/audience_extractor.py`) was invisible from both family route maps. Minimum closure: named row or explicit cross-reference in both Instagram and YouTube route maps.
- `AR-03 minor`: the original catalog did not preserve reviewable evidence of the inventory sweep prescribed by the handoff. Minimum closure: preserve command output or equivalent retrievable artifact when treating completeness as proven; otherwise retain as advisory friction.

## Review Purpose

Decide whether post-patch commit `414063dd` closes prior AR-01 and AR-02 without
introducing any blocker/major route-layer regressions inside the touched patch
scope, and whether AR-03 is now closed, still advisory, or newly material.

Fitness reference:

- Goal pointer: `docs/prompts/handoffs/capture_playbook_lake_sync_handoff_v0.md` -> Goal Handoff / Active Objective.
- Done looks like: a cold agent given "capture <source X> and land it in the lake" reaches source X's lane index from the toolbox/playbook within the cold-lane budget, and that lane index names access route, harness runner/projection/lake seam pointers, and Cleaning seam for every landed source family covered by the PR.

Treat this as an attack axis, not a pass bar.

## Source Pack

Do not review from this prompt text alone. If you cannot open the repo and the
PR branch or target commit, return `BLOCKED_REPO_ACCESS_MISSING`.

Minimum required reads:

1. `AGENTS.md` and `.agents/workflow-overlay/README.md`.
2. `.agents/workflow-overlay/source-loading.md`, `.agents/workflow-overlay/source-of-truth.md`, `.agents/workflow-overlay/review-lanes.md`, `.agents/workflow-overlay/prompt-orchestration.md`, `.agents/workflow-overlay/retrieval-metadata.md`, and `.agents/workflow-overlay/validation-gates.md`.
3. PR #722 metadata and diff, refreshed from current source rather than trusting this prompt. Preferred checks:
   - `gh pr view 722 --repo eric-foo/orca --json number,title,state,isDraft,url,headRefName,headRefOid,baseRefName,baseRefOid,statusCheckRollup`
   - `git status --short --branch`
   - `git diff --name-status e4b3e29f..414063dd`
   - `git diff e4b3e29f..414063dd -- <target files listed above>`
4. The prior review prompt and the prior report if available:
   - `docs/prompts/reviews/capture_source_family_lane_catalog_pr722_adversarial_artifact_review_prompt_v0.md`
   - `docs/review-outputs/adversarial-artifact-reviews/capture_source_family_lane_catalog_pr722_adversarial_artifact_review_v0.md` (optional if unavailable; use frozen capsule above)
5. The handoff packet: `docs/prompts/handoffs/capture_playbook_lake_sync_handoff_v0.md`.
6. The post-patch target files listed in `Review Target` above.
7. Code evidence only as needed to verify the two closure claims:
   - `orca-harness/runners/run_source_capture_price_payload_packet.py`
   - `orca-harness/source_capture/price_payload_extraction.py`
   - `orca-harness/source_capture/audience_post_packet.py`
   - `orca-harness/cleaning/audience_post_input.py`
   - `orca-harness/cleaning/audience_extractor.py`

Available but do not bulk-load unless a finding depends on them:

- all other `orca-harness/` runner/source_capture/cleaning files;
- all historical `docs/workflows/*handoff*` lane packets;
- all review outputs except the prior report above;
- all product proof, Judgment Spine, or external workflow artifacts.

## Review Checks

Run this as a smallest-complete bounded blast-radius recheck:

1. AR-01 closure: verify `vendor_pricing_page` now has a source-family README, a row in the source-family catalog, and discoverability from the toolbox README, Data Capture submap, repo map, and recent-change note. Verify the route points to the actual runner/parser and does not hide under Retail/PDP.
2. AR-02 closure: verify Instagram and YouTube route maps now surface the audience post-text Cleaning seam with the capture packet and cleaning adapter/extractor pointers, without inventing `audience_post` as a fake top-level source family.
3. AR-03 status: decide whether the post-patch lane preserved enough inventory evidence to close the process/evidence friction, or whether it remains an advisory finding. Do not upgrade AR-03 solely because the original prompt did not require committing raw census output; upgrade only if the absence now blocks AR-01/AR-02 closure or creates a blocker/major route risk.
4. Patch-caused blocker/major scan: inside the eight touched files only, check for broken paths, missing retrieval header, wrong `authority_boundary`, false runtime/capture/lake-write authority, Data Lake doctrine restatement, stale target commit language, or repo-map/submap asymmetry that would make the patch unsafe to accept.
5. No full-review reset: do not re-open unrelated prior catalog questions, minor copyedits, or old unpatched concerns outside `414063dd` unless the patch itself exposes a blocker/major issue.
6. Validation evidence: inspect or cheaply rerun `git diff --check`, retrieval-header strict check, repo-map freshness strict check, header index, map links, and pre-push doc gate evidence. Preserve pass/fail/blocked/not-run status; do not convert validation into approval or readiness.

## Output Contract

Write the durable review report to:

`docs/review-outputs/adversarial-artifact-reviews/capture_source_family_lane_catalog_pr722_post_patch_adversarial_artifact_review_v0.md`

The report must include:

- retrieval header with `artifact_role: Review output` and `authority_boundary: retrieval_only`;
- `reviewed_by` and `authored_by` provenance fields, with `unrecorded` allowed when not supplied;
- `de_correlation_bar`: `cross_vendor_discovery`, `same_vendor_sanity`, or `self_fallback`;
- `same_vendor_rationale` when `de_correlation_bar: same_vendor_sanity`;
- current PR metadata and branch/commit freshness receipt, including observed head, base, dirty state, and whether the review target is still `414063dd`;
- source-read ledger with file paths and exact sections, commands, or line windows used;
- one compact `review_summary` YAML block using `.agents/workflow-overlay/communication-style.md`;
- findings first, ordered by `critical`, `major`, then `minor`;
- for each finding: severity, confidence, location, issue, evidence, impact, `minimum_closure_condition`, `next_authorized_action`, and advisory remediation direction;
- `prior_findings_remediated` entries for AR-01, AR-02, and AR-03 status;
- `considered_and_defended` for candidate findings defeated by source evidence;
- explicit validation evidence inspected, rerun, blocked, failed, or not run.

Return only the compact `review_summary` YAML in chat after the report is
written. If the report cannot be written, return the failed `review_summary`
shape with `review_location: chat_only_current_thread` and
`recommendation: blocked`.

Suggested chat courier shape:

```yaml
review_summary:
  status: completed | blocked | advisory_only | failed
  report_path: docs/review-outputs/adversarial-artifact-reviews/capture_source_family_lane_catalog_pr722_post_patch_adversarial_artifact_review_v0.md
  recommendation: accept | accept_with_friction | patch_before_acceptance | reject | blocked
  reviewed_by: operator_to_fill
  authored_by: OpenAI / GPT-family Codex thread
  de_correlation_bar: cross_vendor_discovery | same_vendor_sanity | self_fallback
  summary: "One sentence describing the post-patch review result."
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

- Do not review from a summary or context pack instead of inspecting the repo target at `414063dd`.
- Do not widen beyond the `414063dd` post-patch scope except for the named prior-finding closure checks.
- Do not patch files, emit `patch_queue_entry`, commit, push, merge, mark the PR ready, or open another PR.
- Do not run captures, write lake data, edit runners, edit projections, edit Cleaning adapters, or operate runtime systems.
- Do not build the enforcement hook; only review whether its deferral/evaluation remains adequate if the patch touched that area.
- Do not claim validation, readiness, approval, mergeability, lifecycle completion, source-of-truth promotion, or no-new-seam status from this review.
- Do not recommend, rank, or imply runtime model choice.
- Do not import `jb` project policy or external workflow source as Orca/Forseti authority.
