# Parfumo Targeted Capture Delegated Adversarial Code Review Patch Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Prompt artifact
scope: >
  Repo-mode delegated adversarial review-and-patch commission for the Parfumo
  targeted rendered capture packet route on PR #529.
use_when:
  - Commissioning an independent reviewer/controller to inspect and patch the
    Parfumo targeted capture implementation before home-model adjudication.
authority_boundary: retrieval_only
```

preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` v0 - constants bound; deltas stated below.

## Orca Prompt Preflight Deltas

```yaml
authorization_basis: current owner request "delegate review patch" for the active Parfumo lane
objective: >
  Review and patch PR #529's Parfumo targeted rendered capture route so the
  packet runner lake-seam contract is satisfied without widening scope.
intended_decision: >
  Return source-backed findings, a bounded working-tree patch if warranted,
  validation evidence, and residual risk for home-model/CA adjudication.
output_mode: file-write source prompt; delegated return in chat or courier block
template_kind: review + bounded patch commission; no runtime model routing
edit_permission: patch-only
target_files_or_dirs:
  - docs/workflows/parfumo_targeted_capture_contract_v0.md
  - orca-harness/runners/run_parfumo_mgt_capture.py
  - orca-harness/tests/unit/test_parfumo_mgt_capture_runner.py
read_only_flag_only:
  - orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py
  - all Basenotes files/routes
  - projection, Cleaning, Silver, ECR, and Judgment code
branch_or_commit_reference:
  workspace: C:\Users\vmon7\Desktop\projects\orca\worktrees\parfumo-native-pipeline
  expected_branch: codex/parfumo-native-pipeline
  expected_head: 2227287f425cc9631c5cb4401f9e67ec3a920eb6
  pr: https://github.com/eric-foo/orca/pull/529
dirty_state_allowance: >
  Before the delegated patch, the three target files should match expected_head.
  An untracked copy of this dispatch prompt may exist and is not part of the
  review target.
doctrine_change_decision: none intended; do not change review, prompt, capture, or no-blur doctrine
isolation_decision: existing worktree lane off main; continue there for this patch
validation_gates:
  - python -m py_compile runners/run_parfumo_mgt_capture.py tests/unit/test_parfumo_mgt_capture_runner.py
  - python -m pytest -q tests/unit/test_parfumo_mgt_capture_runner.py
  - python -m pytest -q tests/contract/test_capture_runner_lake_seam_coverage.py
  - python -m pytest -q tests/unit/test_parfumo_projection.py tests/unit/test_parfumo_cleaning_projection_integration.py tests/unit/test_parfumo_non_silver_record_roles.py tests/test_parfumo_native_pipeline_lake.py
  - git diff --check
thread_operating_target_continuity:
  carried_forward: yes
  reason: same_workstream
  lifecycle_status: active_thread_local
```

## Delegated Review-And-Patch Commission

You are the independent receiving controller for a delegated review-and-patch pass. The author/home dispatcher is `OpenAI/GPT-family Codex`. Fill your own `controller_model_family` before review. If your controller family is not different from the author/home family, label the pass `same_vendor_sanity` or `self_fallback`; do not claim cross-vendor discovery or no-new-seam.

```yaml
lane_binding:
  overlay_status: provisional_opt_in
  operating_contract_pointer: .agents/workflow-overlay/delegated-review-patch.md
  review_lane: mixed; code via workflow-code-review, contract-doc boundary via workflow-adversarial-artifact-review when available
  mode: base-subagent
  access: repo
  current_receiving_actor_role: controller
  dispatch_mode: external-controller-courier
  de_correlation_status: operator_to_fill
```

Source-gated method sequence:

1. `REFERENCE-LOAD` method instructions for `workflow-deep-thinking`, `workflow-code-review`, and, for `docs/workflows/parfumo_targeted_capture_contract_v0.md` only, `workflow-adversarial-artifact-review` if available. Do not apply them yet.
2. `SOURCE-LOAD` the required sources below from the named worktree.
3. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
4. Only then `APPLY` deep-thinking, then the relevant review lane(s), then bounded patch execution.

Required source reads:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/delegated-review-patch.md`
- `.agents/workflow-overlay/safety-rules.md`
- `docs/workflows/parfumo_targeted_capture_contract_v0.md`
- `docs/research/orca_fragrance_native_database_live_probe_v0.md`
- historical packet content if available: `docs/workflows/fragrance_native_capture_pipeline_parfumo_basenotes_build_handoff_v0.md`
- `orca-harness/runners/run_parfumo_mgt_capture.py`
- `orca-harness/tests/unit/test_parfumo_mgt_capture_runner.py`
- `orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py`
- analogous seam reference: `orca-harness/runners/run_source_capture_http_packet.py`
- search current runners/tests for `ORCA_DATA_ROOT`, `DataLakeRoot.resolve`, and `args.output is None and os.environ.get("ORCA_DATA_ROOT")`.

Known failure to verify first:

- A prior CI run for PR #529 failed `tests/contract/test_capture_runner_lake_seam_coverage.py`.
- Reported failures were:
  - `run_parfumo_mgt_capture.py: ORCA_DATA_ROOT fallback`
  - missing `explicit --output + --data-root rejection`
  - missing `ORCA_DATA_ROOT gated on --output being omitted`
- Do not trust this as current state. Re-run the contract test locally or inspect current CI if available.

Patch scope:

- You may patch only:
  - `docs/workflows/parfumo_targeted_capture_contract_v0.md`
  - `orca-harness/runners/run_parfumo_mgt_capture.py`
  - `orca-harness/tests/unit/test_parfumo_mgt_capture_runner.py`
- Prefer fixing `orca-harness/runners/run_parfumo_mgt_capture.py` and its unit tests.
- Treat `orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py` as read-only/flag-only unless you can prove the contract checker is stale; if so, stop and return `NEEDS_ARCHITECTURE_PASS` or an explicit off-scope flag rather than editing it.

Non-goals and hard constraints:

- No live Parfumo capture, browser control, proxy use, or network fetch.
- No Basenotes work; Basenotes is held access-blocked for this lane despite older packet language.
- No cookie/storage/Cloudflare-clearance/proxy/exit-IP export.
- No CAPTCHA solving, stealth/fingerprint tooling, retry storm, or anti-bot escalation.
- No projection, Cleaning, Silver, ECR, or Judgment implementation.
- No Silver writes through the raw writer.
- Do not commit, push, merge, rebase, or open/modify PRs.

Review focus:

- Does the Parfumo runner satisfy the packet-runner lake seam contract for both direct HTTP and targeted-rendered modes?
- Are local-output and lake-output modes mutually exclusive?
- Is `ORCA_DATA_ROOT` used only when `--output-root`/local output is omitted, mirroring the accepted runner seam?
- Does the fix preserve the targeted-rendered contract: local artifact packaging only, source surface `parfumo_product_page_chrome_extension_targeted_rendered_session`, no full-corpus claim, and browser-secret rejection?
- Does any change accidentally weaken the no-blur boundary or create a fake success path?

Return contract:

Start with findings first. If a patch is warranted, apply it in the working tree and leave it uncommitted. Then return:

```text
DELEGATED_CODE_REVIEW_RETURN_FOR_HOME_MODEL

- de_correlation_receipt: author/home family, controller family, status
- source_context_status: READY or INCOMPLETE, with missing sources
- findings: file/line citations, impact, minimum closure condition
- patch_summary: changed files and why each change is inside scope
- diff: unified diff or clear changed-file summary
- validation_results: commands run and exact pass/fail/not-run status
- residual_risks: remaining uncertainty
- off_scope_flags: anything outside the three target files
- reviewer_verdict: decision input only, not CA acceptance
```

If the correct fix requires broader architecture, contract-test rewrite, Basenotes, live capture, anti-bot route changes, or downstream Projection/Cleaning/Silver work, return `NEEDS_ARCHITECTURE_PASS` and do not keep a partial patch.
