# Data Lake v4.1 Runner Unblock Adversarial Code Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Filed cross-recipient prompt for a read-only adversarial code review of PR #422,
  the Data Lake v4.1 runner unblock implementation.
use_when:
  - Commissioning a second-opinion implementation/code review of PR #422.
  - Checking whether the runner unblock patch really makes packet-producing runners v4.1-friendly without live-root writes.
open_next:
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_v4_1_forward_epoch_contract_v0.md
  - orca-harness/data_lake/root.py
  - orca-harness/runners/
  - orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py
branch_or_commit: >
  PR #422, codex/data-lake-v4-1-runner-unblock @
  39bb8729982c66aacd69b128b3ae38276a2cc9de, base main @
  190e1ef25a579a6f9085ab14d16fcd3deb813411
stale_if:
  - PR #422 head commit, base commit, branch state, or target worktree dirty state changes.
  - DataLakeRoot, runner CLIs, seam coverage tests, sharding tests, or the v4.1 contract changes.
  - A later implementation patch changes v4.1 root/epoch/sharding behavior.
authority_boundary: retrieval_only
```

## Prompt Preflight

preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` v0 - constants bound; deltas stated below.

- output_mode: `review-report`
- prompt_artifact_path: `docs/prompts/reviews/data_lake_v4_1_runner_unblock_adversarial_code_review_prompt_v0.md`
- review_report_destination: `docs/review-outputs/data_lake_v4_1_runner_unblock_adversarial_code_review_v0.md`
- template_kind: `adversarial-code-review`
- template_source: project-local code-review prompt pattern plus `.agents/workflow-overlay/review-lanes.md`; no bound repo-code-review registry template exists.
- authorization_basis: current owner request invoked `workflow-delegated-review-patch`; Orca overlay routes multi-file implementation/code diffs to the appropriate read-only implementation/code review prompt unless separate patch execution is explicitly commissioned.
- edit_permission: `read-only`; reviewer may write only the review report at the destination above.
- target_files_or_dirs:
  - `orca-harness/data_lake/__init__.py`
  - `orca-harness/data_lake/root.py`
  - `orca-harness/runners/run_source_capture_antiblock_http_packet.py`
  - `orca-harness/runners/run_source_capture_archive_packet.py`
  - `orca-harness/runners/run_source_capture_authenticated_browser_packet.py`
  - `orca-harness/runners/run_source_capture_browser_packet.py`
  - `orca-harness/runners/run_source_capture_cloakbrowser_packet.py`
  - `orca-harness/runners/run_source_capture_historical_packet.py`
  - `orca-harness/runners/run_source_capture_http_packet.py`
  - `orca-harness/runners/run_source_capture_ig_calls_packet.py`
  - `orca-harness/runners/run_source_capture_ig_reels_grid_packet.py`
  - `orca-harness/runners/run_source_capture_media_packet.py`
  - `orca-harness/runners/run_source_capture_packet.py`
  - `orca-harness/runners/run_source_capture_price_payload_packet.py`
  - `orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py`
  - `orca-harness/tests/test_data_lake_root.py`
  - `orca-harness/tests/test_data_lake_sharding.py`
  - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_v4_1_forward_epoch_contract_v0.md`
- source_pack: custom PR #422 implementation review pack named in this prompt; expand only when a missing source could change a material finding.
- dirty_state_allowance: target implementation worktree must be clean at the pinned head. If it is dirty, return `SOURCE_CONTEXT_INCOMPLETE` unless the dirty files are explicitly proven irrelevant.
- expected_target_worktree: `C:\Users\vmon7\Desktop\projects\orca\worktrees\data-lake-v4-1-runner-unblock-merge-update`
- expected_pr_branch: `codex/data-lake-v4-1-runner-unblock`
- expected_local_branch_at_prompt_authoring: `codex/data-lake-v4-1-runner-unblock-merge-update`
- expected_head_at_prompt_authoring: `39bb8729982c66aacd69b128b3ae38276a2cc9de`
- expected_base_at_prompt_authoring: `190e1ef25a579a6f9085ab14d16fcd3deb813411`
- expected_pr: `https://github.com/eric-foo/orca/pull/422`
- controlling_source_state_at_prompt_authoring:
  - PR #422 verified open and draft with head `codex/data-lake-v4-1-runner-unblock` and base `main`.
  - implementation worktree status was clean: `## codex/data-lake-v4-1-runner-unblock-merge-update...origin/codex/data-lake-v4-1-runner-unblock`
  - prompt worktree was updated onto `origin/main` after PR #421 and PR #427 merged.
- doctrine_change_decision: no doctrine change requested. If a design-level issue prevents a safe review conclusion, return it as a finding or `NEEDS_ARCHITECTURE_PASS`; do not edit doctrine.
- isolation_decision: prompt authored on clean docs-only branch `codex/data-lake-v4-1-delegated-review-prompt`; review itself is read-only.
- validation_gates:
  - Required source reads and file:line evidence for load-bearing claims.
  - No live capture, no live runner execution against real targets, and no writes to `F:\orca-data-lake`.
  - If tests are rerun, use temporary data roots only and guard or unset ambient `ORCA_DATA_ROOT`.
  - Do not treat implementer-reported validation as proof unless independently observed or clearly labeled.
- thread_operating_target_continuity: no active `thread_operating_target` carried into this prompt.

## Cynefin Routing

Smallest complete outcome: a read-only adversarial code review report for PR #422 that tells the owner whether the v4.1 runner unblock patch is safe to keep, needs patching, or needs architecture reconsideration.

Regime: Complicated.

Why: the task is source-backed implementation review across shared lake behavior, runner seams, and tests, with bounded files and a pinned PR.

Decomposition: layer-based, with risk-first attention on `DataLakeRoot` invariants before runner wiring.

Current bottleneck: verifying that one shared v4.1 layout contract covers raw writes, derived writes, availability lookup/rebuild, and all 12 packet-producing runners after the post-review seam-coverage hardening and CI test-alignment commits.

Riskiest assumption: the strengthened seam coverage plus focused tests prove old flat/v0 behavior cannot still be reached through an unreviewed runner path, environment fallback, or packet-writer bypass.

Stop or pivot condition: if the pinned worktree/commit cannot be opened cleanly, or if the implementation contradicts the v4.1 owner sharding decision, stop and return `SOURCE_CONTEXT_INCOMPLETE` or `NEEDS_ARCHITECTURE_PASS`.

Allowed next move: read the pinned repo state, apply `workflow-deep-thinking`, then apply `workflow-code-review`, and write the review report.

Disallowed next move: patch files, run live capture, write to `F:\orca-data-lake`, widen into orchestrator/live-root migration, or treat this as delegated review-and-patch.

## Review Commission

You are performing a read-only adversarial implementation/code review for Orca.

Review target:
PR #422, `codex/data-lake-v4-1-runner-unblock` at commit `39bb8729982c66aacd69b128b3ae38276a2cc9de`.

Target worktree:
`C:\Users\vmon7\Desktop\projects\orca\worktrees\data-lake-v4-1-runner-unblock-merge-update`

Review purpose:
Attack whether the implementation really makes all current packet-producing runners v4.1-friendly through the shared Data Lake root, without silently preserving v0/flat layout behavior, false-passing tests, or live-root write risk.

This is not a delegated review-and-patch commission. The target is a multi-file implementation/code diff, so `.agents/workflow-overlay/delegated-review-patch.md` routes it to the appropriate read-only code review prompt unless patch execution is separately bound. Do not patch. If a fix is needed, request patch authorization in the review output.

Owner decision locked for this review:

- `packet_shard = sha256(packet_id).hexdigest()[:3]`
- `anchor_shard = sha256(raw_anchor).hexdigest()[:3]`
- lowercase hex, no salt
- v4.1 is a clean forward epoch, not a compatibility migration
- old v0 or mixed roots must fail closed rather than silently write mixed layouts
- no live capture or writes to `F:\orca-data-lake`

Fitness reference:
The review is successful if the owner can decide whether PR #422 should proceed, be patched, or be redesigned based on source-backed answers to these questions:

1. Does `DataLakeRoot` enforce v4.1 root/epoch markers and route raw, derived, availability, lookup, load, and rebuild behavior through the sharded layout?
2. Do all 12 packet-producing runners have real `--data-root` / `ORCA_DATA_ROOT` lake seams without breaking existing explicit local-output behavior?
3. Do the tests meaningfully catch old v0/flat layout writes, missing epoch markers, broken availability references, and runner seam regressions?

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
2. `orca-harness/data_lake/root.py`
3. `orca-harness/data_lake/__init__.py`
4. all 12 runner files listed in Prompt Preflight
5. `orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py`
6. `orca-harness/tests/test_data_lake_root.py`
7. `orca-harness/tests/test_data_lake_sharding.py`
8. any directly referenced tests for the touched runners when a finding depends on runner behavior

Do not bulk-load unrelated review outputs, all prompts, all research, all product files, or live data-lake contents.

Before review, verify:

```powershell
git status --short --branch
git rev-parse HEAD
git diff --name-only origin/main...HEAD
```

If the status is dirty, the head is not the expected commit, the local branch cannot be tied to the PR branch, or the diff target cannot be inspected in place, return `SOURCE_CONTEXT_INCOMPLETE` and do not review a pasted summary as a substitute.

## Required Method Sequence

1. Read this prompt.
2. REFERENCE-LOAD `workflow-deep-thinking`.
3. REFERENCE-LOAD `workflow-code-review`.
4. Do not APPLY either method yet.
5. SOURCE-LOAD the authority and task sources above.
6. Declare `SOURCE_CONTEXT_READY` with a compact source-read ledger, or `SOURCE_CONTEXT_INCOMPLETE` with missing sources, conflicts, and blocked claims.
7. APPLY `workflow-deep-thinking` to frame the highest-risk failure modes and review boundary.
8. APPLY `workflow-code-review` to review the implementation.
9. Write the report to the bound destination.

If `workflow-code-review` is unavailable, unresolved, or cannot be applied after source readiness, return only a blocked or advisory-only result. Do not emit strict verdicts, readiness claims, validation claims, mandatory remediation, patch queues, or executor-ready handoffs.

## Review Checks

Findings first. Be adversarial within this commission:

1. Does `DataLakeRoot` require both `.orca-data-root` with `contract_version: "v4.1"` and `.orca-lake-epoch.json` with `lake_epoch: "v4.1"` where the contract requires them?
2. Do missing, old v0, mixed, malformed, or stale roots fail closed before any write can happen?
3. Do raw packets land only under `raw/<sha256(packet_id)[:3]>/<packet_id>/`, and do manifests, refs, and lookup methods agree on that path?
4. Do derived records land only under `derived/<sha256(raw_anchor)[:3]>/<raw_anchor>/<lane_namespace>/...`, and is `raw_anchor` safely treated as a path component without path escape or accidental hierarchy injection?
5. Do availability entries, `find_packet`, `load_raw_packet`, and `rebuild_availability` all use sharded refs rather than old flat refs?
6. Does the v4.1 contract doc match actual runtime behavior, or did the patch make doc/code drift?
7. Are the 12 packet-producing runners truly seamed, and is `KNOWN_UNSYNCED` empty only because each runner has a real lake seam?
8. Is `ORCA_DATA_ROOT` fallback scoped correctly so explicit `--output` behavior stays local and tests cannot accidentally write to a real ambient root?
9. Are temp-root tests strong enough to catch accidental writes to old flat layout or missing epoch markers?
10. Do runner unit tests exercise actual lake writes or only CLI argument presence?
11. Are old root compatibility, migration, and orchestrator/live-root concerns correctly out of scope, or did the implementation accidentally depend on them?
12. Does any touched runner still bypass `DataLakeRoot`, duplicate lake path logic, or silently diverge from shared behavior?
13. Do path escape and write-once protections still hold for raw and derived writes after sharding?
14. Does the patch introduce packaging/import issues from the `orca-harness/data_lake/__init__.py` change?
15. Are there untested edge cases around packet IDs, raw anchors, lane namespaces, uppercase/lowercase hash prefixes, or malformed metadata that could corrupt the lake?

## Implementer-Reported Validation To Verify Or Label

The implementer reported these checks after updating PR #422 onto current `origin/main`, hardening the runner seam contract, and aligning the ig reels grid output-precedence unit test. Treat this as evidence to verify, not as a substitute for your source review:

```powershell
git diff --check
```

```text
no output reported
```

```powershell
python -m compileall orca-harness\runners\run_source_capture_antiblock_http_packet.py orca-harness\runners\run_source_capture_archive_packet.py orca-harness\runners\run_source_capture_authenticated_browser_packet.py orca-harness\runners\run_source_capture_browser_packet.py orca-harness\runners\run_source_capture_cloakbrowser_packet.py orca-harness\runners\run_source_capture_historical_packet.py orca-harness\runners\run_source_capture_http_packet.py orca-harness\runners\run_source_capture_ig_calls_packet.py orca-harness\runners\run_source_capture_ig_reels_grid_packet.py orca-harness\runners\run_source_capture_media_packet.py orca-harness\runners\run_source_capture_packet.py orca-harness\runners\run_source_capture_price_payload_packet.py
```

```text
compile succeeded for all listed runner files
```

```powershell
python -m pytest -p no:cacheprovider --basetemp pytest_tmp_datalake_v41_runner_current_main orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py orca-harness/tests/test_data_lake_root.py orca-harness/tests/test_data_lake_availability.py orca-harness/tests/test_data_lake_sharding.py orca-harness/tests/test_data_lake_record_set.py orca-harness/tests/test_data_lake_rebuild_proof.py orca-harness/tests/test_data_lake_read_loader.py orca-harness/tests/unit/test_anti_blocking_http_adapter.py orca-harness/tests/unit/test_source_capture_media_asset.py orca-harness/tests/unit/test_price_payload_retry.py orca-harness/tests/unit/test_source_capture_archive_org.py orca-harness/tests/unit/test_run_source_capture_historical_packet.py orca-harness/tests/unit/test_source_capture_browser_snapshot.py orca-harness/tests/unit/test_source_capture_authenticated_browser_snapshot.py orca-harness/tests/unit/test_source_capture_cloakbrowser_snapshot.py orca-harness/tests/unit/test_source_capture_ig_calls_packet.py orca-harness/tests/unit/test_source_capture_ig_reels_grid_packet.py
```

```text
...................................s.................................... [ 28%]
........................................................................ [ 56%]
........................................................................ [ 84%]
.......................................                                  [100%]
254 passed, 1 skipped in 26.30s
```

If you rerun tests, use temp roots only. Do not write to `F:\orca-data-lake` and do not run live capture.

## Output Contract

Write the durable report to:

`docs/review-outputs/data_lake_v4_1_runner_unblock_adversarial_code_review_v0.md`

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
