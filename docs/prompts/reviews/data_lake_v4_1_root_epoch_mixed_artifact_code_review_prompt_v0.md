# Data Lake v4.1 Root Epoch Mixed Artifact Code Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Filed cross-recipient prompt for a read-only delegated mixed review of PR #421:
  implementation/code correctness plus consistency with the v4.1 forward-epoch
  data-lake contract and adjacent Silver Vault record contract.
use_when:
  - Commissioning a second-opinion review of PR #421 before CA adjudicates the root-runtime patch.
  - Checking whether DataLakeRoot v4.1 epoch enforcement faithfully implements the accepted v4.1 data-lake doctrine.
open_next:
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/source-loading.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_v4_1_forward_epoch_contract_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
  - orca-harness/data_lake/root.py
  - orca-harness/tests/test_data_lake_root.py
branch_or_commit: >
  PR #421, codex/data-lake-v4-1-runtime-migration @
  aa9f7f245a684ab1ac9ad859880a5652fdb8036d, base main @
  d4e6705b2394955c29efec11a7a2c17ddf3e9fe8
stale_if:
  - PR #421 head commit, base commit, branch state, or target worktree dirty state changes.
  - DataLakeRoot, v4.1 forward-epoch contract, Silver Vault record contract, or data-lake root tests change.
  - PR #425 delegated_code_review_and_patch doctrine changes materially and this prompt is reused as a patch-authorized commission.
authority_boundary: retrieval_only
```

## Prompt Preflight

preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` v0 - constants bound; deltas stated below.

- output_mode: `review-report`
- prompt_artifact_path: `docs/prompts/reviews/data_lake_v4_1_root_epoch_mixed_artifact_code_review_prompt_v0.md`
- review_report_destination: `docs/review-outputs/adversarial-artifact-reviews/data_lake_v4_1_root_epoch_mixed_artifact_code_review_v0.md`
- template_kind: `review`
- template_source: project-local mixed implementation/artifact review prompt pattern plus `.agents/workflow-overlay/review-lanes.md`; no bound repo-code-review registry template exists.
- authorization_basis: owner requested delegated review of the actual artifact plus code after accepting the delegated-code-review direction. This prompt is read-only and does not authorize patch execution.
- edit_permission: `read-only`; reviewer may write only the review report at the destination above.
- target_code_files:
  - `orca-harness/data_lake/__init__.py`
  - `orca-harness/data_lake/root.py`
  - `orca-harness/tests/test_data_lake_rebuild_proof.py`
  - `orca-harness/tests/test_data_lake_root.py`
- controlling_artifacts:
  - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_v4_1_forward_epoch_contract_v0.md`
  - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md`
  - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md`
- source_pack: custom PR #421 mixed review pack named in this prompt; expand only when a missing source could change a material finding.
- dirty_state_allowance: target implementation worktree must be clean at the pinned head. If it is dirty, return `SOURCE_CONTEXT_INCOMPLETE` unless the dirty files are explicitly proven irrelevant.
- expected_target_worktree: `C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\data-lake-v4-1-runtime-migration`
- expected_branch: `codex/data-lake-v4-1-runtime-migration`
- expected_head_at_prompt_authoring: `aa9f7f245a684ab1ac9ad859880a5652fdb8036d`
- expected_base_at_prompt_authoring: `d4e6705b2394955c29efec11a7a2c17ddf3e9fe8`
- expected_pr: `https://github.com/eric-foo/orca/pull/421`
- controlling_source_state_at_prompt_authoring:
  - PR #421 verified open, draft, and mergeable with head `codex/data-lake-v4-1-runtime-migration` at `aa9f7f245a684ab1ac9ad859880a5652fdb8036d`.
  - PR #421 changes 4 files with 133 additions and 13 deletions.
  - prior local validation reported `56 passed, 1 skipped`; GitHub Actions `orca-harness-tests` reported pass in `1m24s`.
- doctrine_change_decision: no doctrine change requested by this prompt. If the implementation and doctrine cannot both be made coherent inside PR #421, return `NEEDS_ARCHITECTURE_PASS` or source-backed findings; do not edit doctrine.
- isolation_decision: prompt authored on clean docs-only branch `codex/data-lake-v4-1-root-epoch-mixed-review-prompt`; review itself is read-only.
- validation_gates:
  - Required source reads and file:line evidence for load-bearing claims.
  - No live root writes and no mutation of `F:\orca-data-lake`.
  - If tests are rerun, use temporary data roots only and guard or unset ambient `ORCA_DATA_ROOT`.
  - Do not treat implementer-reported validation as proof unless independently observed or clearly labeled.
- thread_operating_target_continuity: no active `thread_operating_target` carried into this prompt.

## Cynefin Routing

Smallest complete outcome: a read-only delegated mixed review report for PR #421 that tells the owner whether the root-runtime patch faithfully implements v4.1 doctrine, needs patching, or needs architecture reconsideration.

Regime: Complicated.

Why: the task is bounded but spans two authority layers: code behavior and accepted data-lake contracts.

Decomposition: layer-based with risk-first attention to doctrine/code mismatch.

Current bottleneck: proving that `DataLakeRoot` enforcement, markers, skeleton, old-root rejection, tests, and generated read-model folders match the v4.1 forward-epoch contract without creating accidental compatibility migration or query-layer authority.

Riskiest assumption: because PR #421 tests pass, the implementation may appear safe while still under-enforcing the clean epoch, over-encoding Silver Vault read-model shape, or making old v0 roots fail in a way that breaks intended runner cutover sequencing.

Stop or pivot condition: if the pinned worktree/commit cannot be opened cleanly, or if the v4.1 contract and implementation have a design-level mismatch that cannot be fixed by a small PR patch, stop and return `SOURCE_CONTEXT_INCOMPLETE` or `NEEDS_ARCHITECTURE_PASS`.

Allowed next move: read the pinned repo state, apply `workflow-deep-thinking`, then apply `workflow-code-review` for code and adversarial artifact consistency checks for the contracts, and write the review report.

Disallowed next move: patch files, run live capture, write to `F:\orca-data-lake`, widen into runner compliance PR #422, or treat this as merge authorization.

## Review Commission

You are performing a read-only delegated mixed review for Orca.

Review target:
PR #421, `codex/data-lake-v4-1-runtime-migration` at commit `aa9f7f245a684ab1ac9ad859880a5652fdb8036d`.

Target worktree:
`C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\data-lake-v4-1-runtime-migration`

Review purpose:
Attack whether the implementation really makes the data-lake root v4.1-only at the runtime foundation layer, while staying faithful to the v4.1 forward-epoch contract, the Silver Vault record/read-model boundary, and the physicality/location contract.

This is not a delegated review-and-patch commission. Do not patch. If a fix is needed, return source-backed findings and minimum closure conditions so the CA can adjudicate and authorize a follow-up patch.

Owner decisions locked for this review:

- v4.1 is a clean forward epoch, not a compatibility migration of the small old lake.
- Old v0 roots must not remain writable as forward roots.
- `raw/`, `derived/`, `acknowledgements/`, `indexes/availability/`, and `indexes/derived_retrieval/silver_vault/...` are canonical physical slots for the forward root.
- `derived/` is append-only Silver authority when record bodies satisfy the v4.1 record contract.
- `indexes/derived_retrieval/silver_vault/...` is generated, rebuildable retrieval/read-model surface, not authority.
- This patch must not mutate, archive, or rewrite the live `F:\orca-data-lake` root.

Fitness reference:
The review is successful if the owner can decide whether PR #421 should proceed, be patched, or be redesigned based on source-backed answers to these questions:

1. Does PR #421 enforce the v4.1 root/epoch contract at the right runtime boundary without embedding stale bronze/silver/gold or compatibility-migration semantics?
2. Does the implementation faithfully create and verify the root marker, epoch marker, staging slot, sharded raw/derived behavior, availability/retrieval split, and Silver Vault generated-folder skeleton required by the contracts?
3. Do the tests meaningfully catch missing epoch markers, old v0 markers, root-identity swaps, generated retrieval directory assumptions, and old-root acceptance regressions?

## Required Authority Sources

Read these before strict findings:

1. `AGENTS.md`
2. `.agents/workflow-overlay/README.md`
3. `.agents/workflow-overlay/source-loading.md`
4. `.agents/workflow-overlay/decision-routing.md`
5. `.agents/workflow-overlay/review-lanes.md`
6. `.agents/workflow-overlay/prompt-orchestration.md`
7. `.agents/workflow-overlay/validation-gates.md`
8. `docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md`

Then source-load the task sources from the pinned target worktree:

1. `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_v4_1_forward_epoch_contract_v0.md`
2. `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md`
3. `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md`
4. `orca-harness/data_lake/root.py`
5. `orca-harness/data_lake/__init__.py`
6. `orca-harness/tests/test_data_lake_root.py`
7. `orca-harness/tests/test_data_lake_rebuild_proof.py`
8. other directly referenced data-lake tests only when a finding depends on them

Do not bulk-load unrelated review outputs, all prompts, all research, all product files, PR #422 runner work, or live data-lake contents.

Before review, verify in the target worktree:

```powershell
git status --short --branch
git rev-parse HEAD
git diff --name-only origin/main...HEAD
```

If the status is dirty, the branch/head is not the expected one, or the diff target cannot be inspected in place, return `SOURCE_CONTEXT_INCOMPLETE` and do not review a pasted summary as a substitute.

## Required Method Sequence

1. Read this prompt.
2. REFERENCE-LOAD `workflow-deep-thinking`.
3. REFERENCE-LOAD `workflow-code-review`.
4. REFERENCE-LOAD `workflow-adversarial-artifact-review` for artifact/code consistency only.
5. Do not APPLY any method yet.
6. SOURCE-LOAD the authority and task sources above.
7. Declare `SOURCE_CONTEXT_READY` with a compact source-read ledger, or `SOURCE_CONTEXT_INCOMPLETE` with missing sources, conflicts, and blocked claims.
8. APPLY `workflow-deep-thinking` to frame the highest-risk failure modes and review boundary.
9. APPLY `workflow-code-review` to review the implementation files.
10. APPLY the artifact-review lens only to consistency between the contracts and code; do not widen into full data-lake architecture review.
11. Write the report to the bound destination.

If a required review skill is unavailable, unresolved, or cannot be applied after source readiness, return only a blocked or advisory-only result. Do not emit strict verdicts, readiness claims, validation claims, mandatory remediation, patch queues, or executor-ready handoffs.

## Review Checks

Findings first. Be adversarial within this commission:

1. Does `DataLakeRoot` reject old v0 roots, missing epoch markers, malformed epoch markers, and roots declaring compatibility migration?
2. Does `DataLakeRoot.resolve()` fail closed before any write path can use a legacy or mixed root?
3. Does `DataLakeRoot.initialize()` create the correct v4.1 marker pair and directory skeleton, including `.staging/` and Silver Vault generated retrieval homes?
4. Does `DataLakeRoot.for_test()` preserve test-only behavior without creating production fallback or weakening v4.1 requirements?
5. Does `_reverify()` catch both root identity swaps and epoch marker loss or mutation before write sessions?
6. Does the implementation preserve existing raw and derived sharding behavior (`raw/<packet_shard>/<packet_id>/`, `derived/<anchor_shard>/<raw_anchor>/<lane>/<record_id>`) rather than regressing into flat layout?
7. Does the generated `indexes/derived_retrieval/silver_vault/...` skeleton stay non-authoritative and rebuildable, or does code imply it contains truth?
8. Does the rebuild-proof test correctly allow empty directory skeletons while still forbidding un-rebuildable files?
9. Do root marker defaults (`contract_version`, label, `lake_epoch`, `epoch_policy`, `legacy_roots`, `compatibility_migration`) match the v4.1 contract exactly?
10. Is `legacy_roots` recorded without turning into compatibility migration behavior?
11. Are errors clear enough for operators to archive/abandon old roots instead of trying to mix v0 and v4.1?
12. Does exporting new constants from `data_lake/__init__.py` create any import or package-surface risk?
13. Are tests strong enough to fail if old v0 roots are accepted, epoch markers are absent, retrieval directories are treated as files, or marker identity changes are masked by contract-version failures?
14. Does the implementation overfit to current Silver Vault folder names in a way that conflicts with the contract's generated/read-model boundary?
15. Does the patch leave live-root archive/cutover behavior correctly out of scope, or does it accidentally claim migration/cutover completion?

## Implementer-Reported Validation To Verify Or Label

The implementer reported these checks for PR #421. Treat them as evidence to verify, not a substitute for your source review:

```powershell
python -c "from pathlib import Path; [compile(Path(p).read_text(encoding='utf-8'), p, 'exec') for p in ['orca-harness/data_lake/root.py','orca-harness/data_lake/__init__.py','orca-harness/tests/test_data_lake_root.py','orca-harness/tests/test_data_lake_rebuild_proof.py']]"
```

```powershell
git diff --check origin/main...HEAD
```

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python -m pytest -p no:cacheprovider --basetemp pytest_tmp_datalake_v41 tests\test_data_lake_root.py tests\test_data_lake_sharding.py tests\test_data_lake_availability.py tests\test_data_lake_read_loader.py tests\test_data_lake_rebuild_proof.py
```

Reported result: `56 passed, 1 skipped`; GitHub Actions `orca-harness-tests` reported pass in `1m24s`.

If you rerun tests, use temp roots only. Do not write to `F:\orca-data-lake` and do not run live capture.

## Output Contract

Write the durable report to:

`docs/review-outputs/adversarial-artifact-reviews/data_lake_v4_1_root_epoch_mixed_artifact_code_review_v0.md`

The report must include:

- retrieval header with `authority_boundary: retrieval_only`;
- `reviewed_by` and `authored_by` fields in the body; use `unrecorded` only if not supplied, never fabricate;
- `de_correlation_bar` set from actual operator/tooling provenance when known (`cross_vendor_discovery`, `same_vendor_sanity`, or `self_fallback`), otherwise `unrecorded`;
- source-read ledger with file paths and line references for load-bearing claims;
- findings first, ordered by severity: `critical`, `major`, `minor`;
- for each finding:
  - severity;
  - location;
  - issue;
  - evidence with file:line cites;
  - impact;
  - minimum_closure_condition;
  - next_authorized_action;
  - recommended correction or advisory remediation direction;
- explicit answers to the three fitness-reference questions;
- validation commands actually run and observed output, or `not_run` with reason;
- residual risk;
- verdict: `ACCEPTABLE_FOR_CA_ADJUDICATION`, `PATCH_BEFORE_KEEP`, `NEEDS_ARCHITECTURE_PASS`, or `BLOCKED`;
- review-use boundary.

Do not include `patch_queue_entry`. Do not edit source files. Do not run live capture. Do not write to `F:\orca-data-lake`.

After writing the report, return a compact chat summary with:

```yaml
review_summary:
  status: completed | failed | blocked
  review_location: durable_report | chat_only_current_thread
  report_path:
  top_findings:
    - severity:
      issue:
      location:
  recommendation:
  next_action:
```

Review-use boundary:
This review is decision input only. It is not approval, validation, readiness, mandatory remediation, implementation authorization, merge authorization, or executor-ready patch authority until separately accepted or authorized by Orca owner / Chief Architect.