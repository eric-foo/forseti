# Repo-Mode Delegated Adversarial Code Review + Patch Commission -- IG Daily Heartbeat Run-Control (v0)

```yaml
retrieval_header_version: 1
artifact_role: Review prompt artifact (delegated adversarial code review-and-patch commission, repo access mode)
scope: >
  Paste-ready repo-mode commission for de-correlated adversarial CODE review
  and bounded patch of the IG daily heartbeat run-control slice added on PR #809:
  the run-control wrapper that freezes active-daily plans, date-seeded buckets,
  per-session rosters, append-only attempts, heartbeat receipt capture, and
  operational summaries under run_control/ig_daily_heartbeat/YYYY-MM-DD.
use_when:
  - Dispatching PR #809's IG heartbeat run-control slice to a repo-access-capable, non-OpenAI reviewer.
  - Re-dispatching unchanged after verifying the pinned branch, commit, and target-file hashes.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - forseti-harness/runners/run_source_capture_ig_daily_heartbeat_control.py
  - forseti-harness/tests/unit/test_ig_daily_heartbeat_control.py
branch_or_commit: codex/ig-heartbeat-run-control-v0 @ 21ab9dc8b4d42b6721ce3c58fedccdadc8928918
stale_if:
  - PR #809 changes after this prompt without updating target-file hashes.
  - The run-control target files move, split, or are superseded.
  - The delegated-review-patch or code-review output contracts change.
```

## Prompt Preflight

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S3 target deepening
  edit_permission: docs-write for this prompt artifact; downstream reviewer receives patch-only authority for the named target files only
  target_scope: docs/prompts/reviews/ig_daily_heartbeat_run_control_delegated_adversarial_code_review_patch_prompt_v0.md
  dirty_state_checked: yes (worktree clean at authoring before this prompt file)
  blocked_if_missing: independent repo-access reviewer, de-correlation receipt, pinned branch/commit visibility
preflight_defaults: docs/prompts/templates/shared/forseti_preflight_defaults_v0.md v0 - constants bound; deltas stated here.
behavior_contract: docs/prompts/templates/shared/forseti_prompt_behavior_contract_v0.md v0 - source, boundary, and non-claim rules apply.
output_mode: file-write for this prompt artifact; downstream review return is paste-ready chat with diff; durable review report written by home CA/adjudicator on ingestion.
template_kind: review + patch, delegated adversarial code review-and-patch commission.
workflow_sequence_policy: overlay_owned
workflow_sequence_source: .agents/workflow-overlay/delegated-review-patch.md + .agents/workflow-overlay/review-lanes.md
workflow_sequence_status: bound for prompt commission; downstream review remains provisional opt-in and CA-adjudicated.
doctrine_change_decision: no doctrine change intended; if the reviewer finds the design boundary wrong, return NEEDS_ARCHITECTURE_PASS rather than patching policy/docs.
isolation_decision: existing PR worktree/branch codex/ig-heartbeat-run-control-v0; this prompt is added to the same PR for review routing.
thread_operating_target_continuity: no visible active thread_operating_target carried; this is a PR-specific review commission.
```

## Pinned Fields

- Repository: `https://github.com/eric-foo/forseti`.
- PR: `https://github.com/eric-foo/forseti/pull/809`.
- Branch: `codex/ig-heartbeat-run-control-v0`.
- Pinned commit: `21ab9dc8b4d42b6721ce3c58fedccdadc8928918`.
- Review target and ONLY patchable files:
  - `forseti-harness/runners/run_source_capture_ig_daily_heartbeat_control.py` -- SHA256 `11878675acd4cd2ac925a4723b93c58d898367f6a2d7036ed9047176201d9485` (LF git blob bytes at pinned commit).
  - `forseti-harness/tests/unit/test_ig_daily_heartbeat_control.py` -- SHA256 `b291cab3c642d17870ad7408c89cbccb83fe75dabadc52dd8eaddc54b111f92f` (LF git blob bytes at pinned commit).
- Read-only context files; flag, do not patch unless the home CA explicitly widens scope later:
  - `forseti-harness/runners/run_source_capture_ig_daily_heartbeat.py` -- SHA256 `54b60eaef8dcb447405b0449fe5163b1285647c4a9ce260ed22f04cc065c5905`.
  - `forseti-harness/tests/unit/test_ig_daily_heartbeat_runner.py` -- SHA256 `06d7380fc06473522bb9b388318d9064bda7492617ab7a49a3ef702b9d136154`.
  - `forseti/product/spines/capture/core/source_families/social_media/instagram/ig_daily_heartbeat_operating_policy_v0.md`.
  - `forseti/product/spines/capture/core/source_families/social_media/instagram/ig_creator_roster_frontier_ledger_spec_v0.md`.
  - `forseti/product/spines/capture/core/source_families/social_media/creator_registry/README.md`.
  - `forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_index_spec_v0.md`.
- Downstream durable review report destination, if the home CA ingests the returned review: `docs/review-outputs/adversarial-artifact-reviews/ig_daily_heartbeat_run_control_delegated_adversarial_code_review_patch_v0.md`.
- Authored-by family for de-correlation receipt: OpenAI / GPT-family Codex.
- Required de-correlation bar: cross-vendor discovery (`reviewed_by` must be a different upstream vendor/model lineage from OpenAI/GPT-family, or return `BLOCKED_DECORRELATION`).
- Review lane: `workflow-code-review` after source readiness; this is code/implementation review, not artifact review.
- Method pre-step: `workflow-deep-thinking` before code-review analysis, per Forseti review-lane rules.
- Access mode: `repo`.
- Patch authorship: reviewer may author a bounded patch for the two named target files only; no commits, pushes, PR updates, live IG runs, scheduled-task registration, or edits outside target files.

## Paste-Ready Commission Body

````markdown
You are the de-correlated external controller for a REPO-MODE DELEGATED ADVERSARIAL CODE REVIEW AND BOUNDED PATCH commissioned by another lane.

WHO-CONSTRAINT -- gate yourself first: the target was authored by an OpenAI / GPT-family Codex model. This commission requires a DIFFERENT upstream vendor / model lineage. Vendor means upstream model developer/provider, not host, API reseller, wrapper, or UI. If you are OpenAI/GPT-lineage, or your lineage is unknown or undisclosable, reply only with `BLOCKED_DECORRELATION` plus any permitted model-family disclosure, then stop. This is a who-constraint, not a model recommendation. State your model identity/version in your output if known and permitted.

REPOSITORY ACCESS -- inspect the pinned repository directly:
- repo: https://github.com/eric-foo/forseti
- branch: codex/ig-heartbeat-run-control-v0
- pinned commit: 21ab9dc8b4d42b6721ce3c58fedccdadc8928918
- PR: https://github.com/eric-foo/forseti/pull/809

If you cannot open the repo at all, reply only `BLOCKED_REPO_UNREADABLE`. If you can open the repo but not the pinned commit, review the branch head you can see and state the exact commit you read. If either target hash differs, state `SOURCE_CONTEXT_INCOMPLETE` and list the mismatch before reviewing.

TARGET FILES -- review and patch ONLY these files:
1. `forseti-harness/runners/run_source_capture_ig_daily_heartbeat_control.py`
   - expected SHA256 over LF git blob at pinned commit: `11878675acd4cd2ac925a4723b93c58d898367f6a2d7036ed9047176201d9485`
2. `forseti-harness/tests/unit/test_ig_daily_heartbeat_control.py`
   - expected SHA256 over LF git blob at pinned commit: `b291cab3c642d17870ad7408c89cbccb83fe75dabadc52dd8eaddc54b111f92f`

READ-ONLY CONTEXT -- read as needed, flag issues, do not patch:
- `forseti-harness/runners/run_source_capture_ig_daily_heartbeat.py`
- `forseti-harness/tests/unit/test_ig_daily_heartbeat_runner.py`
- `forseti/product/spines/capture/core/source_families/social_media/instagram/ig_daily_heartbeat_operating_policy_v0.md`
- `forseti/product/spines/capture/core/source_families/social_media/instagram/ig_creator_roster_frontier_ledger_spec_v0.md`
- `forseti/product/spines/capture/core/source_families/social_media/creator_registry/README.md`
- `forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_index_spec_v0.md`
- `.agents/workflow-overlay/review-lanes.md`, `.agents/workflow-overlay/delegated-review-patch.md`, `.agents/workflow-overlay/prompt-orchestration.md`, and `AGENTS.md` only for review/patch boundary rules.

DO NOT run live Instagram, do not register or edit Scheduled Tasks, do not create credentials, do not change browser/session/proxy behavior, and do not patch policy docs. If the correct fix requires a policy/schema/architecture change outside the two target files, return `NEEDS_ARCHITECTURE_PASS` or an off-scope flag; do not patch around it.

SOURCE-GATED METHOD SEQUENCE:
1. REFERENCE-LOAD `workflow-deep-thinking` and `workflow-code-review` as procedural method only. Do not APPLY them yet.
2. SOURCE-LOAD the target files and the smallest necessary read-only context above.
3. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` with exact missing/conflicting sources.
4. Only after source readiness, APPLY deep-thinking to enumerate failure modes, then APPLY code review to produce findings and any bounded patch.

WHAT THE TARGET DOES:
The run-control layer sits above the existing IG daily heartbeat runner. It should freeze a daily active-IG plan from Creator Registry identity rows plus a monitoring sidecar, assign date-seeded buckets, write navigable operational artifacts under `run_control/ig_daily_heartbeat/YYYY-MM-DD/`, create per-bucket session rosters, prevent duplicate terminal attempts inside a day, call the heartbeat runner once for the selected roster, ingest heartbeat receipts into an append-only attempts ledger, and summarize session/day coverage. It must not parse IG, invent breakout/deep-capture logic, mutate Creator Registry identity rows, score metrics, paginate, perform platform writes, or claim live-run authorization.

ADVERSARIAL REVIEW AXES -- attack these first:
- Plan/source authority: Does `plan_day` correctly treat Creator Registry as identity/dedupe only and the monitoring sidecar as the active-daily source? Does it fail visibly on ambiguous or missing required identity fields rather than fabricating active roster state?
- Navigable data layout: Are all operational artifacts kept under the intended `run_control/ig_daily_heartbeat/YYYY-MM-DD/` namespace with clear file names and without pretending to be Silver/Gold/creator intelligence?
- Bucket and lane semantics: Does date-seeded bucket assignment vary by day but remain deterministic within a day? Does `run_session` avoid double-dipping across repeated sessions, max-creators slices, retry statuses, bucket locks, and lane filtering? Does the wrapper accidentally lease/start rows that the underlying heartbeat runner would skip by lane?
- Attempts ledger truthfulness: Are `leased`, `started`, and terminal receipt-derived rows append-only and interpretable? Can selected creators be left in a misleading state if the wrapped runner crashes, returns no receipt, returns duplicate receipts, or returns a receipt with a changed/cased handle?
- Receipt/status mapping: Are `succeeded`, `access_gap`, `failed`, and `skipped` handled in a way that preserves missingness and failure visibility? Are unknown statuses failed visibly rather than becoming false success or disappearing from daily summaries?
- Locking and stale-lock behavior: Is `_DayLock` robust enough on Windows/local filesystem for same-bucket concurrent runs? Does stale lock handling risk deleting an active lock or hiding a failed session?
- Retry semantics: Does `retry_statuses` do what an operator would expect without duplicating old terminal rows into misleading coverage counts?
- Sidecar/registry schema drift: Are accepted sidecar keys and registry field names broad enough for the current repository specs, but narrow enough not to silently include wrong accounts?
- Wrapped runner seam: Are arguments to `run_ig_daily_heartbeat` faithful, especially `output_root` vs `data_root`, `allow_heavy_assets` -> `block_heavy_assets`, `time_budget_seconds`, and lane id/count?
- CLI failure surface: Do `plan-day`, `run-session`, and `summarize-day` fail with useful nonzero exits and without fake outputs when required files are absent or malformed?
- Test adequacy and fake-pass risk: Could the current tests pass with an implementation that writes files to the wrong namespace, ignores lane filtering, records missing metrics/statuses as success, or fails to preserve duplicate-prevention behavior?
- Scope control: Patch only the two target files. If a fix requires changes to the existing heartbeat runner, Creator Registry spec, policy docs, or scheduler runtime, flag it as off-scope with the minimum closure condition.

BOUND PATCH RULE:
Apply the smallest complete patch inside the two target files only for findings you can support with source evidence. Return a unified diff in chat; do not commit. Each diff hunk should be tied to a finding id. If no patch is needed, say so explicitly and return no diff. If a design-level issue makes patching unsafe, return `NEEDS_ARCHITECTURE_PASS`, revert/omit any partial patch, and provide findings only.

VALIDATION EXPECTATIONS:
Run these if your environment can; otherwise report `not_run` with the blocker. Never claim a pass you did not observe.
- `python -m pytest -q tests\unit\test_ig_daily_heartbeat_control.py tests\unit\test_ig_daily_heartbeat_runner.py tests\unit\test_source_capture_ig_reels_grid_packet.py tests\unit\test_ig_reels_lane_orchestrator.py`
- `python forseti-harness\runners\run_source_capture_ig_daily_heartbeat_control.py --help`
- `git diff --check`
No live IG capture is authorized.

RETURN IN THIS ORDER:
1. `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`, with source-read ledger and target hash status.
2. `review_summary` YAML: reviewed_by, authored_by, de_correlation_bar, access, target commit, files reviewed, validation run/not-run, verdict category as decision input only.
3. Findings first. For each finding include: id, severity, confidence, target file/line or stable search key, issue, evidence, authority/evidence basis, impact, minimum_closure_condition, next_authorized_action, and whether a patch was included.
4. `considered_and_defended`: one-line candidates you checked but defeated.
5. Unified diff for the bounded patch, or `NO_DIFF_RECOMMENDED` / `NEEDS_ARCHITECTURE_PASS`.
6. Validation results with exact commands and observed outcomes.
7. Residual risk and off-scope flags.
8. `DELEGATED_CODE_REVIEW_RETURN_FOR_HOME_MODEL` courier block containing the original commission, findings, proposed diff, citations, reviewer verdict, validation evidence/not-run checks, residual risk, blockers, and off-scope flags.

Your output is decision input only. It is not approval, validation, readiness, mandatory remediation, or kept change until the home CA adjudicates it and accepts/modifies/rejects each proposed change.
````

## Dispatcher Notes

- Paste the commission body into a non-OpenAI repo-access reviewer lane.
- On return, adjudicate under `.agents/workflow-overlay/delegated-review-patch.md`: accept, modify, or reject each finding and diff hunk; keep nothing by default.
- If the reviewer returns `BLOCKED_DECORRELATION`, use a different upstream vendor/model lineage or record the same-vendor/self-fallback limitation. Do not relabel a same-family result as cross-vendor discovery.
- If a patch is accepted, rerun the validation commands and push the amended branch to PR #809.

## Review-Use Boundary

This prompt does not run the review, validate PR #809, approve runtime use, authorize live IG capture, register scheduled tasks, or create a production-readiness claim. It creates a durable commission prompt only. The delegated review output remains decision input until home-CA adjudication.
