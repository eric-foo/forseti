# Bronze Catalog Source Surface Coverage Adversarial Code Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Read-only adversarial code review prompt for PR #491's Bronze Catalog
  source-surface coverage slice: source_surfaces.json generation, inspect/rebuild
  report coverage, registered vs universal_only extractor labeling, and tests.
use_when:
  - Commissioning a post-merge review of Bronze Catalog source-surface retrievability.
  - Checking whether the merged source-surface coverage slice preserves Bronze as generated, non-authoritative read state over verified raw packets.
authority_boundary: retrieval_only
branch_or_commit: codex/bronze-v41-clean-verify @ 0342a3b3602513e57acce457bf2035fb297a68b1
downstream_consumers:
  - docs/review-outputs/bronze_catalog_source_surface_coverage_adversarial_code_review_v0.md
stale_if:
  - PR #491 is reverted or amended.
  - orca-harness/data_lake/catalog.py or orca-harness/tests/test_data_lake_catalog.py changes after the pinned hashes below.
```

## Prompt Preflight

preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` v0 - constants bound; deltas stated below.

```yaml
orca_start_preflight:
  agents_read: yes_supplied_in_current_task_context
  overlay_read: yes_loaded_by_dispatcher
  source_pack: custom_S0_plus_bronze_catalog_pr491_diff
  repo_map_decision: loaded
  repo_map_reason: >
    PR #491 materially touched the repo map's Bronze Catalog navigation row, so the map
    is part of the review target rather than broad background.
  authorization_basis: >
    Owner merged PR #491 and invoked workflow-delegated-review-patch for a post-merge
    hardening pass; Orca overlay routes this multi-file implementation/code diff to
    read-only workflow-code-review unless separate patch execution is bound.
  objective: >
    Determine whether the merged Bronze Catalog source-surface coverage slice creates
    traceable, rebuildable, non-authoritative retrieval coverage for current and future
    capture lanes without false completeness, stale-index, or schema-consumer risks.
  intended_decision: >
    Give the home model actionable findings to adjudicate: accept current state,
    open a follow-up patch branch for material issues, or name a blocker/design gap.
  edit_permission: read-only
  reviewer_write_permission: report-write only to required_review_report_path
  output_mode: file-write
  delivery_copy: paste-ready-chat copy may be used after this filed prompt artifact exists
  reviewer_output_mode: review-report
  target_scope:
    implementation_targets:
      - C:\Users\vmon7\Desktop\projects\orca\orca-harness\data_lake\catalog.py
      - C:\Users\vmon7\Desktop\projects\orca\orca-harness\tests\test_data_lake_catalog.py
    documentation_target:
      - C:\Users\vmon7\Desktop\projects\orca\docs\workflows\orca_repo_map_v0.md
    code_diff_range:
      base: 230511aa3730873bbace10ac969a3992df9271b5
      head: c197ec46db874181e5b9c3499bfce8290b062e6c
      merged_on_branch: codex/bronze-v41-clean-verify
      merge_commit: 0342a3b3602513e57acce457bf2035fb297a68b1
      pr_url: https://github.com/eric-foo/orca/pull/491
  dirty_state_checked: yes_by_dispatcher
  dirty_state_allowance: >
    Review the pinned target files and PR diff only. The root checkout had unrelated
    untracked files and is out of scope. This prompt was authored in isolated worktree
    C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-lane-coverage-review-prompt.
  controlling_source_state: >
    Target code/doc files are clean at merge commit 0342a3b3602513e57acce457bf2035fb297a68b1
    before this prompt artifact is added; this prompt branch adds only this review prompt.
  branch_or_commit_reference: >
    Inspect code at merge commit 0342a3b3602513e57acce457bf2035fb297a68b1 or any descendant
    where the target file hashes below still match.
  required_review_report_path: C:\Users\vmon7\Desktop\projects\orca\docs\review-outputs\bronze_catalog_source_surface_coverage_adversarial_code_review_v0.md
  doctrine_change_decision: no doctrine change requested; review prompt only
  isolation_decision: >
    Branch/worktree off refreshed origin/codex/bronze-v41-clean-verify because the root
    checkout is dirty and PR #491 is already merged.
  thread_operating_target_continuity:
    carried_forward: no
    reason: no_visible_active_target
    changed_from_input: no
    lifecycle_status: not_applicable
    if_changed_reason: not_applicable
  validation_gates:
    - Verify target hash pins before reviewing.
    - Inspect the PR #491 diff and merged target files.
    - If repo execution is available, rerun focused Bronze Catalog tests.
  blocked_if_missing:
    - Any target file is unavailable or hash mismatches.
    - Reviewer cannot distinguish generated Bronze catalog read state from raw-packet authority.
    - Reviewer cannot invoke or apply workflow-code-review after source context is ready.
```

## Commission

Run a read-only adversarial implementation/code review of PR #491's merged Bronze Catalog source-surface coverage slice.

This prompt was routed from an explicit `workflow-delegated-review-patch` invocation. Orca's delegated-review-patch overlay marks multi-file implementation/code diffs as non-eligible for the provisional single-artifact bounded patch convention unless separate patch execution is bound. Therefore this is a read-only `workflow-code-review` commission with adversarial posture. No patch execution, patch queue, formal verdict, readiness claim, approval, validation claim, or runtime model recommendation is authorized by this prompt.

If the operator is using this as a de-correlated delegated review, the who-constraint is operator-owned: record the actual reviewer and author families in the output provenance fields. Cross-vendor discovery is measured only when the reviewer and author vendors are real and different. Do not fabricate model identity and do not recommend, prescribe, rank, or imply runtime model choice.

Fitness reference:

- Goal: make Bronze Catalog retrieval coverage powerful enough for downstream lanes to discover which source-family/source-surface pairs exist, while Bronze remains rebuildable generated read state over verified raw packets.
- Done looks like: the review identifies whether source-surface coverage, registered/universal_only labeling, stale-index detection, future-lane adaptability, and tests are strong enough to support follow-up Silver/projection coordination without false completeness or authority overclaims.

## Method Order

REFERENCE-LOAD these methods first. Do not APPLY them yet:

- `C:\Users\vmon7\.codex\plugins\cache\agent-workflow-local\agent-workflow\0.1.87\skills\workflow-deep-thinking\SKILL.md`
- `C:\Users\vmon7\.codex\plugins\cache\agent-workflow-local\agent-workflow\0.1.87\skills\workflow-code-review\SKILL.md`

Then SOURCE-LOAD the target files, the PR diff range, and any controlling overlay files needed to resolve review-output boundaries. Declare either `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` with missing sources and material gaps. Only after that declaration, APPLY `workflow-deep-thinking` to frame failure modes, then APPLY `workflow-code-review` for findings-first review.

## Target Hash Pins

Verify these SHA256 pins before review:

```text
2AC2394DBAC31D0B648F9486ECF8EFBEC03FAA7BFBCADFFA23B1D55510C4B40D  orca-harness\data_lake\catalog.py
77D8F8E1031224439628EBCD6992C1AEA0A03E3B9DCC0FAE3E11E86F0649A1EA  orca-harness\tests\test_data_lake_catalog.py
45B38255218C17EDF6C65C895CDBBB4704D57E300244AE631F41DD5EEC10ED44  docs\workflows\orca_repo_map_v0.md
```

If any hash mismatches, stop with `HASH_MISMATCH` and list the mismatched path, expected hash, actual hash, and nearest allowed next step.

## Review Axes To Attack

Focus on concrete correctness, retrieval, schema, and review-confidence failures. In particular, inspect:

- Whether `source_surfaces.json` is wholly generated from verified raw packet manifests and cannot become a second source of authority over capture-lane truth.
- Whether `inspect_catalog` detects missing, stale, orphaned, and unreadable generated source-surface files with the same honesty as `by_packet` and other catalog outputs.
- Whether `facet_extractor: registered | universal_only` is accurate for each observed `(source_family, source_surface)` pair and cannot be misread as semantic completeness, capture support, Silver readiness, or downstream projection coverage.
- Whether future unknown capture lanes remain visible through universal facets without requiring hardcoded source-family lists, and whether unknown lanes avoid false negatives in retrievability.
- Whether grouping by `(source_family, source_surface)` handles `None`, empty strings, multiple packets, mixed extractor coverage, and deterministic ordering without unstable generated bytes.
- Whether `facet_namespaces` gives useful retrieval hints without overclaiming that all creator/content/product identifiers are discoverable for a surface.
- Whether adding `source_surface_count` and `source_surfaces` to inspect/rebuild reports is schema-compatible for existing CLI or programmatic consumers.
- Whether the tests protect meaningful behavior: registered IG coverage, universal-only Reddit coverage, future unknown surfaces, generated-file parity, and stale/orphan detection.
- Whether the repo map wording accurately describes the feature without calling Bronze "god tier", authoritative, validated, runtime-ready, or complete across all capture lanes.
- Whether any downstream Silver/projection lane could still fail to coordinate creator/source tags because the catalog lacks a stable query path, source-locator linkage, packet ids, or facet namespace signal.

## Validation Evidence To Inspect

Dispatcher-observed focused validation from this prompt-authoring turn:

```powershell
cd C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-lane-coverage-review-prompt\orca-harness
$env:PYTHONDONTWRITEBYTECODE=1; python -m pytest -p no:cacheprovider tests\test_data_lake_catalog.py
```

Observed result:

```text
8 passed, 1 skipped in 2.45s
```

Treat this as evidence to inspect, not as a formal validation or review claim. If you have repo execution access, rerun the focused test and report the observed result. If you cannot run it, report `validation_not_run` and review from source.

## Output Contract

Write the durable review report to:

`C:\Users\vmon7\Desktop\projects\orca\docs\review-outputs\bronze_catalog_source_surface_coverage_adversarial_code_review_v0.md`

If filesystem write is unavailable, return the same findings-first report in chat and set `review_location: chat_only_current_thread`. Do not claim chat is equivalent to a missing durable report.

Report findings first, ordered by materiality. Each finding must include:

- `finding_id`
- commissioned target and purpose
- file and line or stable structural anchor
- implementation evidence
- authority or evidence basis
- correctness, retrieval, validation, schema, or review-confidence impact
- `minimum_closure_condition`
- `next_authorized_action`
- verification expectation
- whether `patch_queue_entry` is authorized: always `no` for this prompt

Also include:

- source-read ledger
- strict-only blockers and `not proven` boundaries
- validation run status
- open questions
- residual risk
- review-use boundary: findings are decision input only; they are not approval, validation, readiness, mandatory remediation, or executor-ready patch authority until separately accepted or authorized

Use these provenance fields in the durable report or chat output:

```yaml
reviewed_by: operator_or_reviewer_to_fill_or_unrecorded
authored_by: OpenAI/Codex
de_correlation_bar: operator_to_fill_cross_vendor_discovery_same_vendor_sanity_self_fallback_or_unrecorded
same_vendor_rationale: not_applicable_unless_same_vendor_sanity_is_claimed
```

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
- reviewer verdict or recommendation, if the review lane binds one
- validation evidence and not-run checks
- residual risk
- blockers, off-scope flags, and not-proven boundaries
```

For this prompt, `proposed patch`, `diff`, `exact requested edits`, formal verdict, severity authority, readiness, approval, validation pass/fail, and patch queue are `NOT_CLAIMED` unless a later owner instruction binds them.
