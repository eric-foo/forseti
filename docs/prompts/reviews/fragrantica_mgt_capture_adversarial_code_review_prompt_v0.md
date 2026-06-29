# Fragrantica MGT Capture Adversarial Code Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: Repo-aware adversarial code review prompt for the Fragrantica Mini God Tier capture wrapper PR.
use_when:
  - Commissioning an independent reviewer to inspect PR #451 / codex/fragrantica-mgt-capture.
  - Checking the Fragrantica MGT capture wrapper before projection work continues.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/delegated-review-patch.md
branch_or_commit: codex/fragrantica-mgt-capture @ 9b6c36500532c741795f70d0d65d034da88feb7a
downstream_consumers:
  - docs/review-outputs/fragrantica_mgt_capture_adversarial_code_review_v0.md
stale_if:
  - PR #451 head changes from 9b6c36500532c741795f70d0d65d034da88feb7a.
  - The reviewed target files change before the independent review runs.
```

## Prompt Preflight

preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` v0 - constants bound; deltas stated below.

orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S1/S3
  edit_permission: docs-write for this prompt; receiving reviewer is read-only except writing the review report
  target_scope: PR #451 / `codex/fragrantica-mgt-capture` implementation diff
  dirty_state_checked: yes
  blocked_if_missing: source-of-truth worktree, expected revision, output destination, or workflow-code-review method

Required per-prompt deltas:
- authorization_basis: Current user explicitly invoked `workflow-delegated-review-patch`; Orca overlay routes this multi-file implementation diff to code review rather than the single-artifact delegated patch convention.
- objective / intended_decision: Find blocker/major implementation issues in the Fragrantica Mini God Tier capture wrapper before projection work continues.
- target_files_or_dirs:
  - `orca-harness/runners/run_fragrantica_mgt_capture.py`
  - `orca-harness/tests/unit/test_fragrantica_mgt_capture_runner.py`
  - `docs/workflows/orca_repo_map_v0.md`
- source_pack / bounded_reads:
  - `AGENTS.md`
  - `.agents/workflow-overlay/README.md`
  - `.agents/workflow-overlay/source-of-truth.md`
  - `.agents/workflow-overlay/source-loading.md`
  - `.agents/workflow-overlay/prompt-orchestration.md`
  - `.agents/workflow-overlay/review-lanes.md`
  - `.agents/workflow-overlay/delegated-review-patch.md`
  - `docs/prompts/templates/shared/orca_preflight_defaults_v0.md`
  - the three target files above
  - the PR diff `main...9b6c36500532c741795f70d0d65d034da88feb7a`
- output_mode: review-report
- edit_permission: read-only for implementation/code; write only the required review report.
- dirty_state_allowance: source-of-truth implementation worktree must be clean at expected HEAD; this prompt worktree may contain this prompt artifact only.
- controlling_source_state: checked while authoring; reviewer must fresh-check before review.
- branch_or_commit_reference: `codex/fragrantica-mgt-capture` @ `9b6c36500532c741795f70d0d65d034da88feb7a`.
- doctrine_change_decision: no doctrine change requested; this is prompt/review routing over an implementation PR.
- isolation_decision: prompt authored in separate worktree `worktrees/fragrantica-mgt-review-prompt` to avoid dirty root and avoid modifying PR #451.
- validation_gates: reviewer must inspect supplied validation evidence but must not convert it into validation/pass/readiness claims.
- thread_operating_target_continuity: no visible active `thread_operating_target` is carried into this prompt.

Cynefin routing:
- Smallest complete outcome: independent findings-first code review prompt for PR #451, not a self-review and not a patch execution prompt.
- Regime: complicated.
- Why: the target is an implementation/code diff with overlay-bound review boundaries and missing operator-owned de-correlation fields.
- Decomposition: layer-based review over wrapper behavior, source-capture packet contracts, lake/publication behavior, tests, and repo-map update.
- Current bottleneck: independent reviewer must inspect the pinned implementation diff directly.
- Riskiest assumption: the wrapper correctly composes packet writers without accidental lake publication, false completeness claims, or loss of raw evidence.
- Stop or pivot condition: source worktree is unavailable, HEAD differs, dirty-state is disallowed, or the reviewer cannot write the report.
- Allowed next move: run this review prompt in an independent receiving lane.
- Disallowed next move: commissioning this as a single-target delegated patch pass or letting the authoring model self-review its own implementation.

## Delegated Review-Patch Route Result

This is a route-out from `workflow-delegated-review-patch`, not a bound delegated patch commission.

Reason: `.agents/workflow-overlay/delegated-review-patch.md` says multi-file implementation/code diffs are not eligible for the single-artifact delegated review-and-patch convention unless a separate patch-execution commission is explicitly bound. This PR touches code, tests, and repo map. Therefore route to `workflow-code-review` in read-only findings mode with a durable report.

Actor / model-family receipt:
- author_home_model_family: OpenAI / GPT-family Codex agent
- controller_model_family: operator_to_fill; must differ from author/home family to claim cross-vendor discovery
- current_receiving_actor_role: controller
- dispatch_mode: external-controller-courier
- de_correlation_status: operator_to_fill (`satisfied` only if controller vendor/family differs from OpenAI/GPT; otherwise record `same_vendor_sanity` or `self_fallback`)
- no runtime model recommendation is made by this prompt

## Review Prompt

You are the independent controller for an Orca adversarial code review. Do not edit implementation files. Write only the required review report.

Source-of-truth worktree:
- Absolute path: `C:\Users\vmon7\Desktop\projects\orca\worktrees\fragrantica-mgt-capture`
- Expected branch: `codex/fragrantica-mgt-capture`
- Expected HEAD: `9b6c36500532c741795f70d0d65d034da88feb7a`
- PR: `https://github.com/eric-foo/orca/pull/451`
- Dirty-state allowance: clean worktree only.

Review output binding:
- Review output mode: filesystem-output / review-report.
- Required output path: `docs/review-outputs/fragrantica_mgt_capture_adversarial_code_review_v0.md`
- Write the full review report to that path in the worktree you are using for the review report.
- If you cannot write the report, return `FAILED_REVIEW_OUTPUT_WRITE`; do not claim chat is equivalent to the missing durable report.

Method loading:
1. REFERENCE-LOAD `workflow-deep-thinking`. Do not apply it yet.
2. REFERENCE-LOAD `workflow-code-review`. Do not apply it yet.
3. Read the Orca authority and bounded source pack named in this prompt.
4. SOURCE-LOAD the target diff and target files from the pinned implementation worktree.
5. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
6. After source readiness, APPLY `workflow-deep-thinking` to identify the highest-risk failure modes.
7. Then APPLY `workflow-code-review` in zero-config findings-only advisory mode unless you can bind a stricter Orca implementation-review lane from current overlay authority.

Review target:
- Diff: `git diff main...9b6c36500532c741795f70d0d65d034da88feb7a`
- Files:
  - `orca-harness/runners/run_fragrantica_mgt_capture.py`
  - `orca-harness/tests/unit/test_fragrantica_mgt_capture_runner.py`
  - `docs/workflows/orca_repo_map_v0.md`

Commission:
Review PR #451 for correctness and failure visibility before projection work continues. Focus on blocker/major issues that could make capture output misleading, unsafe to publish into bronze, hard to project correctly, or falsely complete.

Decision criteria:
- The wrapper must preserve the Fragrantica Mini God Tier boundary: anonymous current-window capture only; no login/archive/full-review-coverage claim.
- It must compose existing direct HTTP and CloakBrowser packet writers without bypassing their packet contracts or fake-success behavior.
- It must not implicitly publish to the data lake; lake publication must require explicit `--data-root`.
- It must record accepted residuals and non-claims accurately.
- It must keep projection, ECR, Cleaning, Judgment, and buyer-proof work out of scope.
- It must fail visibly on unsafe output roots, missing packet manifests, wrong source URL, or packet-writer failure.
- Tests must cover the wrapper behavior without requiring live network.
- Repo-map changes must describe the new runner without overstating validation/readiness.

Validation evidence to inspect, not to trust blindly:
- `python -m pytest -q orca-harness/tests/unit/test_fragrantica_mgt_capture_runner.py orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py`
- `python -m pytest -q orca-harness/tests/unit/test_fragrantica_projection.py orca-harness/tests/test_fragrantica_projection_lake_pilot.py`
- `python -m pytest -q orca-harness/tests/unit/test_fragrantica_mgt_capture_runner.py orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py orca-harness/tests/unit/test_fragrantica_projection.py orca-harness/tests/test_fragrantica_projection_lake_pilot.py`
- Preflight command: `python orca-harness/runners/run_fragrantica_mgt_capture.py --url https://www.fragrantica.com/perfume/Chanel/Chanel-No-5-33519.html --output-root _scratch/fragrantica_mgt_preflight --preflight-only`
- Live local smoke output, if still present: `orca-harness/_test_runs/fragrance_native_20260629/fragrantica_mgt_capture_wrapper_smoke/fragrantica_mgt_capture_summary.json`
- Observed smoke packet IDs from the commissioning lane: direct HTTP `01KW9EDCS9V5KY837BJFWB8ENY`, initial viewport `01KW9EDRTM36N24PMMDJDADEV5`, deep scroll `01KW9EHHSPYCNW1RE70BKSHBBN`.

Hard constraints:
- Do not edit implementation files, tests, repo map, prompts, or overlay files.
- Do not emit `patch_queue_entry`; patch execution is not bound.
- Do not claim validation, readiness, approval, or merge safety.
- Do not recommend, prescribe, rank, or imply a runtime model.
- Do not review a substitute checkout, summary, recreated source, or stale branch if the pinned worktree/revision cannot be confirmed.
- Do not widen into projection, ECR, Cleaning, Judgment, product proof, login-gated archive capture, or full Fragrantica archive design.

Report requirements:
- Findings first, ordered by materiality.
- Each finding must include file/line or stable search key, implementation evidence, impact, `minimum_closure_condition`, `next_authorized_action`, verification expectation, and whether patch execution is authorized (`no` unless a later prompt changes it).
- Include strict-only blockers and `not proven` boundaries separately from findings.
- Include open questions and residual risk.
- Include a short review-use boundary: findings are decision input only; not approval, validation, mandatory remediation, executor-ready patch authority, readiness, or merge safety.
- Include `reviewed_by` and `authored_by`; if the operator has not supplied either, use `unrecorded` rather than fabricating it.
- If this was run with a controller family different from OpenAI/GPT, record `de_correlation_bar: cross_vendor_discovery`; otherwise record `same_vendor_sanity` or `self_fallback` with rationale and do not claim discovery/no-new-seam.

After successful report write, return a compact human summary and this courier YAML:

```yaml
review_courier:
  output_mode: filesystem-output
  report_path: docs/review-outputs/fragrantica_mgt_capture_adversarial_code_review_v0.md
  commission: "Adversarial code review of PR #451 Fragrantica MGT capture wrapper before projection work continues."
  target: "codex/fragrantica-mgt-capture @ 9b6c36500532c741795f70d0d65d034da88feb7a"
  authority: "AGENTS.md plus Orca overlay review/prompt/delegated-review boundaries"
  decision_criteria: "Capture-only MGT correctness, packet contract preservation, false-completeness avoidance, explicit lake publication, no projection/ECR/Cleaning claim."
  evidence_summary: "<short source-backed summary>"
  reviewer_verdict: "NOT_CLAIMED unless a bound verdict vocabulary is supplied"
  finding_ids: []
  minimum_closure_conditions: []
  next_authorized_action: "<CA adjudication, patch authorization, or proceed if no material findings>"
  non_claims:
    - "not approval"
    - "not validation"
    - "not readiness"
    - "not merge safety"
    - "not patch authority"
```

Append this delegated-return block for the home model:

```text
DELEGATED_CODE_REVIEW_RETURN_FOR_HOME_MODEL

Here is the delegated code review result. Adjudicate it under the delegated-review-patch return contract.

Include:
- original commission or review target
- implementation context, diff, and reviewed files
- findings and implementation evidence
- proposed patch direction, if any, as advisory only unless separately authorized
- citations
- reviewer verdict or NOT_CLAIMED
- validation evidence and not-run checks
- residual risk
- blockers, off-scope flags, and not-proven boundaries
```
