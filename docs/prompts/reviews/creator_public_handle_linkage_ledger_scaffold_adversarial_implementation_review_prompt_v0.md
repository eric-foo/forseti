---
retrieval_header_version: 1
artifact_role: Orca adversarial implementation review prompt
scope: >
  Filed prompt for adversarial review of the creator public-handle linkage
  ledger scaffold update at diff 0e4881c6..a5c6e4bf. The user invoked the
  provisional delegated-review-patch convention, but this target is a multi-file
  implementation/product-doc/test diff, so the overlay routes it to an ordinary
  read-only mixed implementation review prompt unless a separate single-target
  patch-execution commission is bound.
use_when:
  - Dispatching an independent reviewer to review the creator public-handle
    linkage ledger scaffold update before adding source-backed creator rows.
  - Checking whether the empty product ledger scaffold, validator test, and
    discovery pointers preserve the public-handle-only and pre-SQLite boundary.
authority_boundary: retrieval_only
review_type: adversarial_mixed_implementation_review
output_mode: review-report
edit_permission: read-only
target_branch: codex/creator-ledger-static-fixture
target_base_commit: 0e4881c6d10bec966aa029ad1ec3435dc2cc6708
target_implementation_commit: a5c6e4bf468452dc9d6af3ac0f7a595349c6597c
durable_report_destination: docs/review-outputs/creator_public_handle_linkage_ledger_scaffold_adversarial_implementation_review_v0.md
authored_by: GPT-5 / Codex home model
reviewed_by: unrecorded
de_correlation_bar: operator_to_fill
---

# Creator Public-Handle Linkage Ledger Scaffold Adversarial Implementation Review Prompt v0

## Commission Boundary

This is a filed route-out prompt produced after `workflow-delegated-review-patch`
was invoked on the already-pushed scaffold update. The Orca delegated-review-patch
overlay is provisional and explicitly says multi-file implementation/code diffs
must not be stretched into that single-target patch convention. Therefore this
prompt routes to a read-only mixed implementation review:

- no patch authority;
- no reviewer working-tree edits;
- no patch queue;
- no runtime model recommendation;
- no validation, readiness, approval, or no-new-seam claim.

If the operator wants de-correlation, the operator/tooling chooses a reviewer
whose vendor / model lineage differs from the author/home lineage and records the
actual `reviewed_by`, `authored_by`, and `de_correlation_bar` values in the
review report. Unknown or undisclosed lineage does not satisfy a cross-vendor
discovery bar. This is a who-constraint only, not model routing.

## Orca Start Preflight

```yaml
orca_start_preflight:
  agents_read: supplied_in_task_context_or_read_before_review
  overlay_read: required_before_review
  source_pack: custom
  repo_map_decision: loaded
  repo_map_reason: the scaffold added a product JSON file and discovery pointers under the mapped Data Capture Spine surfaces
  workspace: C:\Users\vmon7\Desktop\projects\orca\worktrees\creator-ledger-static-fixture
  expected_branch: codex/creator-ledger-static-fixture
  target_base_commit: 0e4881c6d10bec966aa029ad1ec3435dc2cc6708
  target_implementation_commit: a5c6e4bf468452dc9d6af3ac0f7a595349c6597c
  target_diff: 0e4881c6d10bec966aa029ad1ec3435dc2cc6708..a5c6e4bf468452dc9d6af3ac0f7a595349c6597c
  dirty_state_allowance: prompt artifact/report artifacts may exist after dispatch; implementation target is the pinned diff above
  untracked_files_in_scope: no, except this prompt/report if created by the review lane
  edit_permission: read-only
  output_mode: review-report
  durable_report_destination: docs/review-outputs/creator_public_handle_linkage_ledger_scaffold_adversarial_implementation_review_v0.md
  doctrine_change_decision: none requested; if a needed fix changes capture/privacy/ledger doctrine, return NEEDS_ARCHITECTURE_PASS
  external_source_boundary: external workflow source and jb project policy are not Orca authority; no live social-platform access
preflight_defaults: docs/prompts/templates/shared/orca_preflight_defaults_v0.md
```

## What This Is For

Goal: decide whether the new empty product ledger scaffold is safe as the next
static, source-backed row-admission surface before any SQLite promotion or real
creator population.

Done looks like: a future operator can add source-backed IG/TikTok/YouTube public
handle rows without the artifact implying live capture authority, person identity
proof, contact/outreach permission, follower/audience graphs, or existing creator
coverage.

Treat that goal as an axis to attack, not a pass bar. If the goal or observable
signal is underbound, say so as a finding rather than inventing a broader product
objective.

## Required Method Sequence

1. Read `AGENTS.md`.
2. Read `.agents/workflow-overlay/README.md`.
3. Read `.agents/workflow-overlay/source-loading.md`,
   `.agents/workflow-overlay/review-lanes.md`,
   `.agents/workflow-overlay/delegated-review-patch.md`,
   `.agents/workflow-overlay/prompt-orchestration.md`,
   `.agents/workflow-overlay/safety-rules.md`, and
   `.agents/workflow-overlay/validation-gates.md`.
4. REFERENCE-LOAD `workflow-deep-thinking`, `workflow-code-review`, and
   `workflow-adversarial-artifact-review`; do not APPLY them before source
   context is ready.
5. SOURCE-LOAD the target diff, target files, read-only context files, and
   validation evidence below.
6. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
7. After `SOURCE_CONTEXT_READY`, APPLY `workflow-deep-thinking` to frame the
   failure modes, then APPLY `workflow-code-review` to code/test/JSON behavior
   and `workflow-adversarial-artifact-review` to the product/docs surface.
8. Return findings-first. Do not edit files. Do not stage, commit, push, install,
   deploy, run live capture, call external services, or start SQLite migration
   work.

If a required review skill is unavailable, return
`BLOCKED_REVIEW_LANE_UNAVAILABLE` for the missing lane rather than emulating a
strict review inline.

## Target Diff And Files

Review this exact diff:

```powershell
git diff 0e4881c6d10bec966aa029ad1ec3435dc2cc6708..a5c6e4bf468452dc9d6af3ac0f7a595349c6597c
```

Changed files in scope:

- `orca/product/spines/capture/core/source_families/social_media/creator_public_handle_linkage_ledger_v0.json`
- `orca/product/spines/capture/core/source_families/social_media/creator_public_handle_linkage_ledger_spec_v0.md`
- `orca-harness/tests/unit/test_creator_public_handle_linkage.py`
- `docs/workflows/data_capture_spine_consolidation_map_v0.md`
- `orca/product/spines/capture/core/source_capture_toolbox/README.md`

Do not review this prompt file as part of the implementation target.

## Read-Only Context To Inspect

Read when material to a finding:

- `docs/decisions/wind_caller_calibration_carveout_v0.md`
- `orca-harness/capture_spine/creator_public_handle_linkage/models.py`
- `orca-harness/capture_spine/creator_public_handle_linkage/validation.py`
- `orca-harness/tests/fixtures/creator_public_handle_linkage/valid_synthetic_ledger.json`
- `docs/review-outputs/creator_public_handle_linkage_ledger_delegated_adversarial_code_review_patch_v0.md`
- `docs/prompts/reviews/creator_public_handle_linkage_ledger_delegated_adversarial_code_review_patch_prompt_v0.md`
- `orca/product/spines/capture/core/source_families/social_media/instagram/ig_creator_roster_frontier_ledger_spec_v0.md`
- `orca/product/spines/capture/core/source_families/social_media/instagram/ig_creator_ideal_audience_inference_spec_v0.md`
- `docs/workflows/data_capture_spine_consolidation_map_v0.md`
- `orca/product/spines/capture/core/source_capture_toolbox/README.md`

The ideal-audience source is context only. The linkage ledger must not silently
absorb Tier-2-A aggregate audience demographics, contact information, follower
or audience graphs, or person identity claims. If a home is needed for audience
or target-audience attributes, flag that as a separate architecture decision.

## Validation Evidence To Inspect

Author-reported checks for the scaffold commit:

```powershell
$env:PYTHONDONTWRITEBYTECODE=1; Remove-Item Env:ORCA_DATA_ROOT -ErrorAction SilentlyContinue; python -m pytest -p no:cacheprovider --no-header --no-summary --basetemp 'pytest_creator_ledger_tmp_final' 'orca-harness\tests\unit\test_creator_public_handle_linkage.py'
```

Observed output:

```text
22 passed in 0.08s
```

```powershell
$env:PYTHONDONTWRITEBYTECODE=1; Remove-Item Env:ORCA_DATA_ROOT -ErrorAction SilentlyContinue; python -m pytest -p no:cacheprovider --no-header --no-summary --basetemp 'pytest_orca_harness_unit_tmp_cleanenv' 'orca-harness\tests\unit'
```

Observed output:

```text
1587 passed, 1 skipped in 78.03s
```

Earlier broad-suite attempt without clearing `ORCA_DATA_ROOT` failed with 14
source-capture/data-lake tests writing under `F:\orca-data-lake`; the clean-env
rerun passed. Treat that as an environmental test caveat, not as hidden ledger
success.

Additional observed checks:

```powershell
python -m json.tool 'orca\product\spines\capture\core\source_families\social_media\creator_public_handle_linkage_ledger_v0.json' > $null
python '.agents\hooks\check_retrieval_header.py' --changed --strict
python '.agents\hooks\check_repo_map_freshness.py' --changed --strict --message "repo-map-ack: creator public-handle linkage map now includes the static ledger scaffold and the owning spec open_next points to the ledger JSON."
python '.agents\hooks\check_map_links.py' --changed --strict
git diff --check
```

Observed result: all passed; `check_map_links` reported `OK (0 findings)` and
33 annotated nonresolving debt entries. `git diff --check` emitted only Git
line-ending warnings on existing Markdown/JSON paths.

Known residual check:

```powershell
python '.agents\hooks\check_placement.py' --changed --strict
```

Observed result: failed on repo-wide pre-existing placement/top-level/legacy
classification debt. The reviewer should verify whether the new ledger JSON or
prompt/report paths add a new placement blocker; do not treat repo-wide inherited
placement debt as a pass.

## Review Questions

Prioritize blocker and major issues. Minor findings are welcome only when they
materially reduce false-success, source-loading drift, or boundary-drift risk.

1. Does the empty `public_handle_ledger` scaffold validate through the existing
   validator without weakening the synthetic-fixture guards or letting forbidden
   person/audience/contact data into future real rows?
2. Does the product JSON truthfully represent an empty/manual-ready ledger, or
   could a downstream reader infer creators are already populated, live capture
   is authorized, or SQLite promotion has begun?
3. Does `test_product_public_handle_ledger_scaffold_loads_and_validates` locate
   the product file robustly from the test file and assert the right minimum
   invariants, without making the test brittle to normal worktree layout?
4. Do the spec and indexes point to the product JSON without changing source
   authority, granting runtime capture, or creating stale paths?
5. Does the added scaffold preserve the relational/table-shaped migration path
   to SQLite, with `creator_records`, `platform_accounts`, and
   `account_link_evidence` staying explicit even when empty?
6. Is the known `check_placement.py` failure truly pre-existing for this patch,
   or did the new product JSON create a fresh placement concern that the author
   missed?
7. Does the prompt/report/ledger language keep cross-platform identity stitching
   at the public-handle-to-public-handle level, with LLM evidence treated as
   assistive only and never sufficient by itself?

## Output Contract

Write the review report to:

`docs/review-outputs/creator_public_handle_linkage_ledger_scaffold_adversarial_implementation_review_v0.md`

The report must include:

- `reviewed_by`, `authored_by`, and `de_correlation_bar` fields; use
  `unrecorded` only when the value was not supplied, never fabricate provenance;
- source context status: `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`;
- findings first, ordered by severity/priority, with file/line citations and
  concise evidence;
- `minimum_closure_condition` and `next_authorized_action` for actionable
  findings;
- explicit non-findings or residual risks for the ledger-empty boundary,
  no-live-capture boundary, no-person-identity boundary, and placement-hook
  residual;
- validation evidence inspected and validation gaps;
- a compact courier summary for the commissioning CA.

Allowed recommendation vocabulary:

- `no_blocker_or_major_findings`
- `patch_recommended`
- `architecture_pass_needed`
- `blocked_source_context_incomplete`

Do not emit `PASS`, readiness, approval, validation success, mandatory patch
queue, or executor-ready instructions. Advisory remediation direction is allowed;
`patch_queue_entry` is not.
