# Bronze Silver Dedupe AR PR520 Adversarial Code Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Filed route-out prompt for de-correlated adversarial implementation/code
  review of PR #520's Silver projection discovery dedupe and Bronze Attachment
  Record physicalization changes.
use_when:
  - Commissioning an independent reviewer to inspect PR #520 before merge.
  - Checking the prompt source, target revision, output binding, and de-correlation receipt for this review.
authority_boundary: retrieval_only
open_next:
  - AGENTS.md
  - .agents/workflow-overlay/README.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/source-loading.md
  - .agents/workflow-overlay/validation-gates.md
  - .agents/workflow-overlay/safety-rules.md
implementation_under_review: eb29555ae771821d2c9581f4e8ca17061bb229ef..1cacaa6e96a855e02fe80d0f48d2b8d1e86d6100
prompt_carrier_note: >
  This prompt may be committed after the implementation commit. The
  implementation target under review ends at 1cacaa6e96a855e02fe80d0f48d2b8d1e86d6100;
  prompt-only carrier commits do not change the implementation target unless
  they modify the named target files.
stale_if:
  - PR #520 is amended after the target hashes below.
  - Any named implementation target file changes after 1cacaa6e96a855e02fe80d0f48d2b8d1e86d6100 and before review.
  - The review-output destination already exists and the operator has not authorized a new version.
  - The receiving actor cannot inspect the named repo/worktree or target commit in place.
downstream_consumers:
  - docs/review-outputs/bronze_silver_dedupe_ar_pr520_adversarial_code_review_v0.md
```

## Orca Prompt Preflight

preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` v0 - constants bound; deltas stated below.

```yaml
orca_start_preflight:
  agents_read: yes_supplied_in_current_task_context
  overlay_read: yes_loaded_by_dispatcher
  source_pack: custom_S0_plus_pr520_targets_and_data_lake_contract_context
  repo_map_decision: not_loaded_for_this_prompt
  repo_map_reason: >
    Target files and owning overlay/lake contracts are already known. Repo-map
    navigation is not needed unless the reviewer discovers a placement or
    retrievability issue.
  authorization_basis: >
    Owner requested a delegated review prompt after PR #520 was opened. No
    reviewer patch authority was explicitly commissioned in this turn, so the
    receiving reviewer is read-only for source files and writes only the named
    review report.
  objective: >
    Independently attack whether PR #520 correctly hardens Silver/read-model
    projection discovery over mixed flat/sharded derived layouts and promotes
    Bronze Attachment Records to MGT manifest-equivalent typed entries over
    preserved raw packet bodies without overclaiming validation, authority, or
    source-family semantics.
  intended_decision: >
    Give the home model a de-correlated implementation/code review report to
    adjudicate before merge or follow-up patch authorization.
  output_mode: file-write prompt artifact; downstream receiver output is review-report
  edit_permission:
    source_files: read-only
    report_file: write-only at the named report destination
    patch_authority: none in this commission
  target_files_or_dirs:
    - orca-harness/capture_spine/creator_profile_current/instagram_metric_seed.py
    - orca-harness/data_lake/catalog.py
    - orca-harness/runners/run_instagram_reels_creator_metric_seed_materialize.py
    - orca-harness/tests/test_data_lake_catalog.py
    - orca-harness/tests/unit/test_instagram_reels_creator_metric_seed.py
  branch_or_commit_reference:
    pr: https://github.com/eric-foo/orca/pull/520
    state_observed_by_dispatcher: OPEN
    base_branch: codex/bronze-v41-clean-verify
    base_commit: eb29555ae771821d2c9581f4e8ca17061bb229ef
    head_branch: codex/bronze-silver-dedupe-ar
    implementation_head_commit: 1cacaa6e96a855e02fe80d0f48d2b8d1e86d6100
  dirty_state_allowance: >
    Review the target commit/range and pinned target files. Later prompt-only
    carrier commits are allowed only if the named implementation target files
    still match the hashes below. Any source-file drift must be reported before
    review.
  controlling_source_state: >
    Target code/test files were clean at implementation commit 1cacaa6e before
    this prompt artifact was added. This prompt does not alter implementation
    target files.
  doctrine_change_decision: >
    This prompt does not change doctrine. It asks the reviewer to inspect code
    that implements existing Data Lake/Silver/AR directions. If the reviewer
    finds a design-level contract conflict, return it as a finding or
    NEEDS_ARCHITECTURE_PASS; do not patch or rewrite doctrine.
  isolation_decision: >
    Prompt authored in the existing PR #520 worktree/branch. The implementation
    target is pinned to the commit before any prompt carrier change.
  thread_operating_target_continuity:
    carried_forward: no
    reason: no_visible_active_target
    changed_from_input: no
    lifecycle_status: not_applicable
    if_changed_reason: not_applicable
  validation_gates:
    - Verify target file hash pins before reviewing.
    - Inspect the PR #520 diff range and target files.
    - Rerun focused tests if repo execution is available.
    - If broader tests are rerun, account for operator-local ORCA_DATA_ROOT effects.
  blocked_if_missing:
    - Any target file hash mismatches and the operator has not supplied a newer pin.
    - The reviewer cannot distinguish raw authority from generated catalog/index/read-model state.
    - The reviewer cannot keep source files read-only.
    - The reviewer cannot invoke or apply workflow-code-review after source context is ready.
```

## Lane Binding

```yaml
overlay_status: provisional_opt_in
operating_contract_pointer:
  - AGENTS.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/delegated-review-patch.md
review_lane: code (workflow-code-review)
mode: read-only delegated implementation/code review; no patch authority in this commission
actor_model_family_receipt:
  author_home_model_family: OpenAI/Codex
  controller_model_family: operator_to_fill_must_differ_from_author_for_cross_vendor_discovery
  current_receiving_actor_role: controller
  dispatch_mode: external-controller-courier
  de_correlation_status: blocked_until_receiving_reviewer_records_different_vendor_or_family
de_correlation: >
  The controller must be a different upstream vendor/model lineage from the
  author/home model to claim cross-vendor discovery. This is a who-constraint,
  not a runtime model recommendation. If the receipt is missing, same-vendor,
  or undisclosed, return advisory findings only and do not claim cross-vendor
  discovery or no-new-seam.
subagent_authority: >
  No tester/testee shortcut. The authoring or adjudicating model must not
  satisfy this by reviewing its own work. The receiving controller reviews in
  its own lane and does not launch a replacement controller.
prompt_rendering: >
  This filed prompt is the orchestrated prompt artifact. Do not substitute a
  summary, context pack, alternate checkout, or recreated-source review for
  inspecting the pinned repo/worktree source.
```

## Commission

Run an adversarial implementation/code review of PR #520: "Harden Bronze AR and
Silver projection discovery".

Review purpose:

1. Attack whether lake-native IG reels projection discovery correctly handles
   both legacy flat `derived/<anchor>/<lane>/...` and v4.1 sharded
   `derived/<shard>/<anchor>/<lane>/...` layouts.
2. Attack whether exact duplicate projection files are deduped by content hash
   without hiding semantically different projections or weakening the existing
   username/currentness selection rule.
3. Attack whether local raw drill-back pointers now handle sharded raw packet
   layout without breaking legacy flat derived paths or non-derived inputs.
4. Attack whether the metric seed runner's `--from-lake` / `--data-root` mode
   is fail-closed, operator-ergonomic, and compatible with explicit
   `--projection` mode.
5. Attack whether Bronze Attachment Records are now honestly physicalized as
   manifest-equivalent typed entries over preserved raw packet bodies: typed,
   source-family-agnostic, hash-checkable, replay-pinned, and still clear that
   bodies remain raw packet members rather than copied `attachments/` bodies.
6. Attack whether schema/version changes are explicit enough and whether tests
   would catch stale AR fields, mismatched structured `body_ref`, hash/path drift,
   mixed layout projection duplication, and runner-mode misuse.

The reviewer is read-only for source in this commission. If you find a bounded
fix, state the minimum closure condition and recommended next authorized action.
Do not edit files, emit an executor-ready patch queue, commit, push, merge, or
mutate a live data lake.

The home model / Chief Architect adjudicates every finding. Your report,
citations, and recommendation are decision input only, not approval, validation,
mandatory remediation, readiness, or merge authorization.

## Source-Gated Method Contract

1. Read this prompt.
2. Read `AGENTS.md` and `.agents/workflow-overlay/README.md`.
3. REFERENCE-LOAD `workflow-deep-thinking` if available in your environment.
4. REFERENCE-LOAD `workflow-code-review` if available in your environment.
5. REFERENCE-LOAD `workflow-delegated-review-patch` only as commission mechanics. Do not APPLY it as patch authority.
6. Do not APPLY any method yet.
7. SOURCE-LOAD the required authority, target files, PR diff range, and relevant lake contracts below.
8. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` with missing sources, conflicts, unavailable tools, and any target-file drift.
9. Only after source readiness, APPLY deep-thinking to frame material failure modes, then APPLY workflow-code-review for findings-first implementation/code review.
10. If `workflow-code-review` is unavailable, use findings-first advisory code review and mark strict review-lane claims `NOT_CLAIMED`.

## Required Reads

Authority and boundary files:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/delegated-review-patch.md`
- `.agents/workflow-overlay/validation-gates.md`
- `.agents/workflow-overlay/safety-rules.md`
- `.agents/workflow-overlay/source-of-truth.md`

Target implementation files:

- `orca-harness/capture_spine/creator_profile_current/instagram_metric_seed.py`
- `orca-harness/data_lake/catalog.py`
- `orca-harness/runners/run_instagram_reels_creator_metric_seed_materialize.py`
- `orca-harness/tests/test_data_lake_catalog.py`
- `orca-harness/tests/unit/test_instagram_reels_creator_metric_seed.py`

Data Lake context, read only as needed for the claim being reviewed:

- `orca-harness/data_lake/root.py`
- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md`
- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md`
- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md`
- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md`
- `docs/decisions/orca_mini_god_tier_doctrine_v0.md`

Optional targeted reads if a finding depends on them:

- `orca-harness/source_capture/ig_reels_grid_projection.py`
- `orca-harness/tests/test_data_lake_sharding.py`
- `orca-harness/tests/test_data_lake_rebuild_proof.py`
- `orca-harness/tests/unit/test_ig_reels_behavioral_lake.py`
- `orca-harness/runners/run_data_lake_catalog.py`

Do not bulk-load review outputs, all prompts, all product docs, proof packets,
research corpus files, or live lake data by default.

## Target Diff And Hash Pins

Implementation target range:

```text
eb29555ae771821d2c9581f4e8ca17061bb229ef..1cacaa6e96a855e02fe80d0f48d2b8d1e86d6100
```

Observed PR #520 metadata at dispatch:

```yaml
url: https://github.com/eric-foo/orca/pull/520
state: OPEN
base_ref: codex/bronze-v41-clean-verify
head_ref: codex/bronze-silver-dedupe-ar
head_oid: 1cacaa6e96a855e02fe80d0f48d2b8d1e86d6100
title: Harden Bronze AR and Silver projection discovery
```

Use this command shape as the reviewed implementation diff:

```powershell
git diff eb29555ae771821d2c9581f4e8ca17061bb229ef..1cacaa6e96a855e02fe80d0f48d2b8d1e86d6100 -- orca-harness/capture_spine/creator_profile_current/instagram_metric_seed.py orca-harness/data_lake/catalog.py orca-harness/runners/run_instagram_reels_creator_metric_seed_materialize.py orca-harness/tests/test_data_lake_catalog.py orca-harness/tests/unit/test_instagram_reels_creator_metric_seed.py
```

Windows worktree SHA256 pins for target files at implementation head:

```text
44CE15171CCAD0F763FF875184450F412BFC22BD8DAB3889C3627679419C1984  orca-harness/capture_spine/creator_profile_current/instagram_metric_seed.py
FFD4E4903EE93DF36CFE3665A23FA76EC98CC9623FDB0B15E926A2286AA0F860  orca-harness/data_lake/catalog.py
9CD2A5F71587EA2488A48F7F6B5FDBA6A468E5978A8675E750DBED802AFD5F43  orca-harness/runners/run_instagram_reels_creator_metric_seed_materialize.py
DF7372D3E4AA3CE55870F5AE4B40F5121E76BBE6745586C1BA5941392AE1A44C  orca-harness/tests/test_data_lake_catalog.py
E637CCA36CA1B9CAFA1FF1A70254D78DB3D2B20E4609CAAE2E38614123F81BFC  orca-harness/tests/unit/test_instagram_reels_creator_metric_seed.py
```

If any hash mismatches, stop with `HASH_MISMATCH` and list the path, expected
hash, actual hash, and nearest allowed next step. If the branch contains a later
prompt-only commit, verify whether the five target files still match the pins;
if yes, review the pinned implementation target.

## Validation Evidence To Inspect

The author observed these checks after the implementation commit:

```powershell
python -m pytest -q orca-harness\tests\unit\test_instagram_reels_creator_metric_seed.py
python -m pytest -q orca-harness\tests\test_data_lake_catalog.py
python -m pytest -q orca-harness\tests\test_data_lake_sharding.py
python -m pytest -q orca-harness\tests\test_data_lake_rebuild_proof.py
python -m pytest -q orca-harness\tests\unit\test_ig_reels_behavioral_lake.py
python orca-harness\runners\run_instagram_reels_creator_metric_seed_materialize.py --help
Remove-Item Env:ORCA_DATA_ROOT -ErrorAction SilentlyContinue
python -m pytest -q orca-harness\tests
```

Observed validation notes:

- Focused metric-seed tests exited 0.
- Bronze catalog tests exited 0.
- Data lake sharding tests exited 0.
- Data lake rebuild-proof test exited 0.
- IG reels behavioral lake tests exited 0.
- Runner `--help` exited 0 and showed `--from-lake` / `--data-root`.
- Full `orca-harness/tests` exited 0 after `ORCA_DATA_ROOT` was removed for the test process.
- A prior full-suite run with this shell's operator-local `ORCA_DATA_ROOT` set failed two operator-local/live-root checks: a fail-closed source-capture CLI test saw the implicit root, and a YouTube live-lake ledger check rejected the local root UUID. Treat that as environment-sensitive evidence to inspect, not an implementation pass/fail by itself.
- `git diff --check` exited 0 before commit.
- Implementation commit readback: `1cacaa6e Harden Bronze AR and Silver projection discovery`, 5 files changed, 261 insertions, 16 deletions.

Independently rerun the validation commands you judge necessary. If you do not
rerun a command, report it as author-supplied and not independently revalidated.
Do not run live capture, public web research, live lake mutation, Cleaning/ECR/
Judgment materialization, Silver/Gold migration, or final Attachment Record body
copy migration.

## Review Scope

Attack these questions:

- Does `discover_instagram_reels_projection_paths_from_lake` correctly and deterministically scan both flat and sharded derived layouts without treating unrelated JSON files as IG reels projections?
- Is exact-content dedupe by SHA-256 the right physical duplicate boundary, or can it hide a material duplicate/source distinction the metric seed needs?
- Does the builder still count and select projection inputs honestly after lake discovery dedupe, especially when weak/strong projections share usernames?
- Does `_source_packet_pointer` compute sharded raw pointers only when the derived path shape proves v4.1 sharding, while preserving legacy flat behavior?
- Does the runner reject ambiguous `--from-lake` plus explicit `--projection`, require `--from-lake` for `--data-root`, and retain existing explicit projection behavior?
- Does the AR schema/version bump cover all generated shape changes without creating false compatibility claims?
- Do `attachment_record_physicalization`, `body_ref`, `payload_schema_version`, and `replay_version_pins` satisfy the AR contract's compact typed-entry expectations without inventing source-family lake-core fields?
- Does `load_attachment_record_body` verify structured `body_ref` strongly enough, and do its error paths remain useful after the new nested-reference checks?
- Does the AR catalog remain generated read state under `indexes/derived_retrieval`, with raw manifests and preserved bytes still authoritative?
- Does the prompt's MGT/90-95% claim boundary hold: high utility now, accepted residual that bodies are not copied to `attachments/`, no Manifest v2, no source-family payload validation, no downstream currentness/readiness claim?
- Do tests cover mixed flat/sharded duplicates, exact dedupe, raw pointer derivation, runner mode shape, AR manifest fields, structured body ref, replay pins, stale/missing catalog files, and body path/hash drift?
- Does any touched code leak Gold/Judgment semantics into Silver/Bronze, or freeze source-family semantics into physical folders or lake-core fields?

## Intended Closure Check

Treat these as claims to verify, not accepted truth:

- `silver_dedupe_01`: lake-native projection discovery works across flat and sharded `derived/` layouts.
- `silver_dedupe_02`: exact physical duplicate projections are deduped without weakening semantic per-username selection.
- `silver_dedupe_03`: sharded raw drill-back pointers are correct where layout proves v4.1 and legacy behavior is preserved.
- `ar_mgt_01`: AR rows are typed manifest-equivalent entries over preserved raw packet bodies, not positional `file_id` inheritance.
- `ar_mgt_02`: AR entries carry enough replay/version/body-ref material to resolve and verify bodies without source-family interpretation.
- `ar_mgt_03`: residuals remain explicit: no copied attachments body, no Manifest v2, no payload validation, no downstream currentness/readiness.
- `test_durability_01`: tests would catch the main regressions above.

For each, report one of:

- `closed`: implementation and tests cover the failure mode.
- `partially_closed`: some protection exists but a material variant remains.
- `not_closed`: the original failure mode remains.
- `not_assessed`: source or environment prevented assessment.

If `partially_closed` or `not_closed`, include evidence and a minimum closure condition.

## Strict-Claim Boundary

This review must not claim formal implementation-review authority, readiness,
acceptance, validation, approval, or merge status unless Orca overlay authority is
supplied separately. Use findings-first advisory implementation/code review. Do
not emit `patch_queue_entry`; do not edit source files; do not commit, push, PR,
merge, or run live capture/lake operations.

If you find no blocker or major issue, say so and state residual risks or
validation gaps. If you find an issue, findings lead the report and must include:

- finding id
- severity as `blocker`, `major`, or `minor` for prioritization only, not formal Orca verdict authority
- target file and stable line/anchor
- evidence from the implementation
- authority or evidence basis
- concrete impact
- minimum closure condition
- next authorized action
- validation expectation

## Output Contract

Write the full review report to:

`docs/review-outputs/bronze_silver_dedupe_ar_pr520_adversarial_code_review_v0.md`

The report must include:

- `reviewed_by: operator_to_fill`
- `authored_by: openai-gpt-5-codex`
- `de_correlation_bar: cross_vendor_discovery | same_vendor_sanity | self_fallback`
- `same_vendor_rationale:` required if `de_correlation_bar` is `same_vendor_sanity`
- source-read ledger
- `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`
- findings first
- open questions and residual risk
- validation commands run, skipped, or blocked
- intended closure check for all closure items named above
- review-use boundary: findings are decision input only, not approval, validation, mandatory remediation, readiness, merge authorization, or executor-ready patch authority until separately accepted or authorized

After writing the report, fresh-read the written report path and return compact
courier YAML in chat:

```yaml
review_summary:
  status: completed | blocked | failed
  report_path: docs/review-outputs/bronze_silver_dedupe_ar_pr520_adversarial_code_review_v0.md
  recommendation: accept | accept_with_friction | patch_before_merge | needs_architecture_pass | blocked
  reviewed_by: operator_to_fill
  authored_by: openai-gpt-5-codex
  de_correlation_bar: cross_vendor_discovery | same_vendor_sanity | self_fallback
  summary: ""
  findings_count: 0
  blocking_findings: []
  advisory_findings: []
  next_action: ""
```

Review findings are decision input only; they are not approval, validation,
mandatory remediation, readiness, merge authorization, or executor-ready patch
authority until the Chief Architect separately accepts or authorizes them.
