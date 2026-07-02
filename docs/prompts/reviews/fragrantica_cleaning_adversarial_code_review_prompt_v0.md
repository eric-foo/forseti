# Fragrantica Cleaning Adversarial Code Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Read-only adversarial code review prompt for the Fragrantica projection-to-
  Cleaning adapter and append-only derived Cleaning record writer.
use_when:
  - Commissioning a bounded review of the Fragrantica Cleaning implementation before CA adjudication or merge.
  - Checking that Fragrantica Cleaning preserves raw/projection evidence without overclaiming archive completeness, sentiment, demand, Judgment, or Evidence-Unit readiness.
authority_boundary: retrieval_only
branch_or_commit: codex/fragrantica-cleaning @ 4ec4eba6 target implementation commit
```

## Prompt Preflight

preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` v0 - constants bound; deltas stated below.

```yaml
orca_start_preflight:
  agents_read: yes_supplied_in_current_task_context
  overlay_read: yes_loaded_by_dispatcher
  source_pack: custom_S0_plus_fragrantica_cleaning_code_review
  repo_map_decision: loaded
  repo_map_reason: >
    The implementation branch touches the repo map; target scope was selected from
    the active Fragrantica lane and the branch diff, not by broad repo navigation.
  authorization_basis: >
    Current user explicitly invoked workflow-delegated-review-patch after the
    Fragrantica Cleaning branch was built, validated, committed, and pushed.
  objective_intended_decision: >
    Produce a source-backed read-only adversarial code review of the Fragrantica
    Cleaning implementation so the home/CA model can adjudicate findings before
    assuming the Cleaning lane is structurally ready.
  edit_permission: read-only
  target_scope:
    implementation_targets:
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\fragrantica-cleaning\orca-harness\cleaning\fragrantica.py
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\fragrantica-cleaning\orca-harness\cleaning\fragrantica_lake.py
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\fragrantica-cleaning\orca-harness\tests\test_fragrantica_cleaning_lake_pilot.py
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\fragrantica-cleaning\orca-harness\tests\unit\test_fragrantica_cleaning_projection_integration.py
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\fragrantica-cleaning\docs\workflows\orca_repo_map_v0.md
    context_only:
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\fragrantica-cleaning\AGENTS.md
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\fragrantica-cleaning\.agents\workflow-overlay\README.md
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\fragrantica-cleaning\.agents\workflow-overlay\source-loading.md
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\fragrantica-cleaning\.agents\workflow-overlay\review-lanes.md
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\fragrantica-cleaning\.agents\workflow-overlay\delegated-review-patch.md
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\fragrantica-cleaning\.agents\workflow-overlay\prompt-orchestration.md
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\fragrantica-cleaning\docs\workflows\fragrantica_capture_to_data_lake_projection_ecr_cleaning_handoff_v0.md
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\fragrantica-cleaning\orca\product\spines\cleaning\contracts\core_spine_v0_cleaning_spine_foundation_v0.md
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\fragrantica-cleaning\orca\product\spines\data_lake\authority\core_spine_v0_data_lake_silver_vault_record_contract_v0.md
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\fragrantica-cleaning\orca\product\spines\data_lake\authority\core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\fragrantica-cleaning\orca-harness\data_lake\root.py
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\fragrantica-cleaning\orca-harness\source_capture\fragrantica_projection.py
    optional_pattern_sources_if_needed:
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\fragrantica-cleaning\orca-harness\ecr\lake.py
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\fragrantica-cleaning\orca-harness\signal_content\lake.py
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\fragrantica-cleaning\orca-harness\cleaning\transcript_product_lake.py
  dirty_state_checked: yes_by_dispatcher
  branch_or_commit_reference:
    worktree: C:\Users\vmon7\Desktop\projects\orca\worktrees\fragrantica-cleaning
    branch: codex/fragrantica-cleaning
    target_implementation_commit: 4ec4eba6
    target_diff_base: origin/main...4ec4eba6
  dirty_state_allowance: >
    The implementation worktree was clean before this prompt artifact was filed.
    For review, the five implementation_targets must match the SHA256 pins below.
    This prompt file and the required review report path may be new or modified;
    other dirty target-file changes are out of scope and should produce
    SOURCE_CONTEXT_INCOMPLETE or HASH_MISMATCH.
  controlling_source_state: >
    Overlay, skill, and prompt-authority sources were loaded by the dispatcher for
    route-out. Target file hashes below were observed after the implementation
    commit and before this prompt file was written. This is not a readiness,
    approval, or validation claim.
  output_mode: file-write
  delivery_copy: paste-ready-chat copy may be used after this filed prompt artifact exists
  reviewer_output_mode: review-report
  required_review_report_path: C:\Users\vmon7\Desktop\projects\orca\worktrees\fragrantica-cleaning\docs\review-outputs\fragrantica_cleaning_adversarial_code_review_v0.md
  doctrine_change_decision: no doctrine change requested; review prompt only
  isolation_decision: existing clean worktree codex/fragrantica-cleaning; no new branch or worktree for read-only review routing
  validation_gates:
    - verify target SHA256 pins or stop with HASH_MISMATCH
    - inspect target code, tests, and listed context sources
    - inspect dispatcher-observed pytest and diff-check evidence
    - rerun focused pytest if repo execution is available; otherwise record validation_not_run
  thread_operating_target_continuity: not_carried; no visible active thread_operating_target artifact was supplied for this prompt
  blocked_if_missing:
    - AGENTS.md or .agents/workflow-overlay/README.md unavailable
    - workflow-deep-thinking or workflow-code-review unavailable
    - any required implementation target unavailable
    - reviewer cannot inspect the pinned repo/worktree and target file hashes
```

## Commission

Run a read-only adversarial code review of the Fragrantica Cleaning implementation. The target is the five implementation files listed in preflight: the Fragrantica Cleaning adapter, its lake writer, its focused tests, and the repo-map update. The target is not a live Fragrantica capture run, not a browser/auth probe, not full-archive review acquisition, not ECR redesign, not Judgment, and not product-demand interpretation.

This prompt was routed from an explicit `workflow-delegated-review-patch` request, but Orca's delegated-review-patch overlay marks multi-file implementation/code diffs as non-eligible for that provisional bounded patch convention unless separate patch-execution authority is bound. Therefore this is a read-only `workflow-code-review` commission with adversarial posture. No patch execution, patch queue, formal verdict, readiness claim, approval, validation pass/fail claim, or runtime model recommendation is authorized.

Actor/de-correlation receipt for operator use:

```yaml
author_home_model_family: OpenAI/Codex
controller_model_family: operator_to_fill
current_receiving_actor_role: controller
dispatch_mode: operator-couriered repo-bound review prompt
de_correlation_bar: operator_to_fill_cross_vendor_discovery_or_same_vendor_sanity_or_unrecorded
de_correlation_status: >
  To claim cross-vendor discovery, the receiving reviewer must be from a different
  vendor/model lineage than OpenAI/Codex. If same-vendor, unknown, or unrecorded,
  record the limitation and do not claim discovery/no-new-seam coverage.
```

This is a who-constraint and provenance receipt, not a model recommendation or routing instruction.

Fitness reference:

- Goal: harden the Fragrantica Cleaning lane so current-window Fragrantica projection data can produce non-destructive Cleaning packets and append-only derived records without inventing archive completeness, sentiment, demand, Judgment, persisted-ECR certainty, or Evidence-Unit readiness.
- Done looks like: the review identifies whether handle construction, transform-ledger semantics, residual/raw-pull carry, ECR references, Silver envelope fields, derived-lake placement, append-only behavior, and tests are correct enough for home-model adjudication, with concrete closure conditions for any material finding.

## Method Order

REFERENCE-LOAD these methods first. Do not APPLY them yet:

- `C:\Users\vmon7\.codex\plugins\cache\agent-workflow-local\agent-workflow\0.1.87\skills\workflow-deep-thinking\SKILL.md`
- `C:\Users\vmon7\.codex\plugins\cache\agent-workflow-local\agent-workflow\0.1.87\skills\workflow-code-review\SKILL.md`

Then SOURCE-LOAD the target files and context-only files listed in preflight. Verify the target SHA256 pins. Declare either `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` with missing sources, mismatches, dirty-state surprises, and material gaps. Only after that declaration, APPLY `workflow-deep-thinking` to frame boundary failures and review risks, then APPLY `workflow-code-review` for findings-first review.

If `workflow-code-review` is unavailable, unresolved, or cannot be applied, return `BLOCKED_REVIEW_LANE_UNAVAILABLE` with the reason. Do not emulate a strict review lane inline.

## Target SHA256 Pins

Verify these pins before review:

```text
0299EF121A7F879F64536EFC5D0F771EBDA16D472FBD8A6181D6E1B3E2C10258  orca-harness\cleaning\fragrantica.py
2BE51947D0B0EA9BD3316BC445D13FE4F397B4ADA7C8F047BACFF6B63986B623  orca-harness\cleaning\fragrantica_lake.py
EAEB039444C907F10CBCA29FCCABB5A7835248BF3F8B1FD082452C2F734E8908  orca-harness\tests\test_fragrantica_cleaning_lake_pilot.py
B0DA2BA91F8447C8A2FBC3AB376E9CF916ACE4C12ABF065775F81109F63B4FE7  orca-harness\tests\unit\test_fragrantica_cleaning_projection_integration.py
EDA96E222ED550A714CF6809CE9BED7C9F0B1214577E778BDA1C6D1DB6DA1DFA  docs\workflows\orca_repo_map_v0.md
```

If any target hash mismatches, stop with `HASH_MISMATCH` and list the mismatched path, expected hash, actual hash, and nearest allowed next step.

## Required Source Basis

SOURCE-LOAD these authority and support files:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/delegated-review-patch.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `docs/workflows/fragrantica_capture_to_data_lake_projection_ecr_cleaning_handoff_v0.md`
- `orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md`
- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md`
- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md`
- `orca-harness/data_lake/root.py`
- `orca-harness/source_capture/fragrantica_projection.py`
- all target files listed under Target SHA256 Pins.

Optional pattern sources, only if a finding or comparison depends on them:

- `orca-harness/ecr/lake.py`
- `orca-harness/signal_content/lake.py`
- `orca-harness/cleaning/transcript_product_lake.py`

## Implementation Summary To Verify

The implementation is intended to:

- convert every Fragrantica projection row into a Cleaning input handle keyed back to raw/projection evidence;
- add review-card transform ledger entries only for non-destructive source-family adaptation: review text whitespace normalization, author display-name whitespace normalization, review text length binning, and source-visible vote-field carry;
- leave non-review rows addressable but untransformed;
- carry projection residuals and raw-pull triggers, including current-window and archive-completeness warnings;
- attach an ECR source-side posture reference by convention unless disabled;
- re-derive projection from a raw packet when writing the derived Cleaning record;
- append a Silver-compatible Cleaning record under `derived/<raw_shard>/<packet_id>/cleaning_fragrantica/`;
- include non-claims for archive completeness, demand signal, Evidence-Unit binding, Judgment, and sentiment analysis;
- preserve append-only behavior for default record IDs and fail on duplicate explicit record IDs.

Treat this summary as a checklist to verify against source, not as truth.

## Review Axes To Attack

Be adversarial about material correctness, contract, lineage, and false-confidence risks:

- Whether handle construction preserves one handle per projection row, raw anchors, projection references, source family/surface, row residuals, packet residuals, and raw-pull triggers without losing row-level inspectability.
- Whether transform ledger entries are genuinely non-destructive Cleaning operations and do not smuggle sentiment, credibility, evidence-unit binding, demand, archive completeness, or Judgment claims.
- Whether `CleaningPreservationCheck` values are truthful for each transform, especially for length bins and vote-field carry where hierarchy/count/semantic preservation can be easy to overstate.
- Whether identical `original_value` and `transformed_value` in whitespace normalization and vote carry are useful ledger facts, redundant noise, or contractually acceptable method evidence.
- Whether attaching an ECR reference by convention risks implying a persisted ECR set exists in the same lake when a temp/test lake or unsequenced lane may not contain one.
- Whether re-deriving projection from raw inside `derive_fragrantica_cleaning_into_lake` and leaving `derived_refs` empty satisfies the Silver/derived-lake lineage contract, or whether a persisted projection record reference should be required when available.
- Whether the Silver record envelope fields are correct and stable: schema versions, `record_kind`, `payload_kind`, producer fields, `observed_at`/`captured_at`, `raw_refs`, `coverage`, `content_hash`, and canonical hash basis.
- Whether `raw_refs` in the record header retain enough inspectable anchor detail, or whether critical `anchor_kind` / `anchor_value` information is only buried in the payload.
- Whether append-only behavior is actually enforced by the writer and tested for both default ULID record IDs and explicit duplicate IDs.
- Whether test fixtures and assertions cover the source-family risks that matter: current-window-only residuals, review-card-only transforms, source-visible vote carry, non-review rows, non-claims, content hash stability, append-only writes, and no overwrite behavior.
- Whether repo-map changes accurately describe the implementation without turning Cleaning into ECR, Projection, Judgment, or product-proof readiness.

## Validation Evidence To Inspect

Dispatcher-observed focused validation from this prompt-authoring turn:

```powershell
cd C:\Users\vmon7\Desktop\projects\orca\worktrees\fragrantica-cleaning\orca-harness
$env:PYTHONDONTWRITEBYTECODE='1'
python -m pytest -p no:cacheprovider -q tests\test_fragrantica_cleaning_lake_pilot.py tests\unit\test_fragrantica_cleaning_projection_integration.py tests\test_fragrantica_projection_lake_pilot.py
```

Observed result:

```text
...........                                                              [100%]
```

Dispatcher-observed whitespace/diff check:

```powershell
git diff --check origin/main...HEAD -- orca-harness/cleaning/fragrantica.py orca-harness/cleaning/fragrantica_lake.py orca-harness/tests/test_fragrantica_cleaning_lake_pilot.py orca-harness/tests/unit/test_fragrantica_cleaning_projection_integration.py docs/workflows/orca_repo_map_v0.md
```

Observed result: no output.

Treat this as evidence to inspect, not as a formal validation claim. If you have repo execution access, rerun the pytest command and report the observed result. If you cannot run it, report `validation_not_run` and review from source.

## Output Contract

Preferred reviewer output is a durable report at:

`C:\Users\vmon7\Desktop\projects\orca\worktrees\fragrantica-cleaning\docs\review-outputs\fragrantica_cleaning_adversarial_code_review_v0.md`

If filesystem write is unavailable, return the same findings-first report in chat and set `review_location: chat_only_current_thread`. Do not claim chat is equivalent to a missing durable report.

Report findings first, ordered by materiality. Each finding must include:

- `finding_id`
- commissioned target and purpose
- file and line or stable structural anchor
- implementation evidence
- authority or evidence basis
- correctness, validation, runtime, lineage, lake-contract, or review-confidence impact
- `minimum_closure_condition`
- `next_authorized_action`
- verification expectation
- whether `patch_queue_entry` is authorized: always `no` for this prompt

Also include:

- source-read ledger
- target hash verification result
- strict-only blockers and `not proven` boundaries
- validation run status
- open questions
- residual risk
- review-use boundary: findings are decision input only; they are not approval, validation, readiness, mandatory remediation, or executor-ready patch authority until separately accepted or authorized

Use these provenance fields in the durable report or chat output:

```yaml
reviewed_by: operator_or_reviewer_to_fill_or_unrecorded
authored_by: OpenAI/Codex
de_correlation_bar: operator_to_fill_cross_vendor_discovery_or_same_vendor_sanity_or_unrecorded
same_vendor_rationale: not_applicable_unless_same_vendor_sanity_is_claimed
```

Do not fabricate model identity. Do not recommend, prescribe, rank, or imply runtime model choice.

Close with this courier block so the home model can adjudicate later:

```text
DELEGATED_CODE_REVIEW_RETURN_FOR_HOME_MODEL

Here is the delegated code review result. Adjudicate it under the delegated-review-patch return contract.

Include:
- original commission or review target
- implementation context, diff, and reviewed files
- findings and implementation evidence
- proposed patch, diff, or exact requested edits, if separately authorized
- citations
- reviewer verdict or recommendation, if the review lane and prompt authorize one
- validation evidence and not-run checks
- residual risk
- blockers, off-scope flags, and not-proven boundaries
```

For this prompt, `proposed patch`, `diff`, `exact requested edits`, formal verdict, severity authority beyond finding priority, readiness, approval, validation pass/fail, and patch queue are `NOT_CLAIMED` unless a later owner instruction binds them.
