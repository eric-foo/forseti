# TikTok Scanner Hardening Delegated Adversarial Code Review Patch Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Prompt artifact
scope: >
  Repo-mode delegated adversarial code review-and-patch commission for the
  TikTok creator-scanner hardening diff (P1-P5: link-hub outcome contract,
  CDP session probe, frontier lake writer + runner, registry preflight gates)
  on branch claude/tiktok-scanner-hardening.
use_when:
  - Commissioning an independent cross-vendor reviewer/controller to inspect
    and patch the scanner-hardening implementation before home-model
    adjudication and merge.
authority_boundary: retrieval_only
```

preflight_defaults: `docs/prompts/templates/shared/forseti_preflight_defaults_v0.md` - constants bound; deltas stated below.

## Forseti Prompt Preflight Deltas

```yaml
authorization_basis: >
  owner "proceed" on the audited P1-P5 patch set (scanner contract audit,
  2026-07-10) plus the carried adversarial_review: recommended advisory at
  after_all_steps_pre_closeout from the lane's implementation scoping
objective: >
  Adversarially review and, within the named file set, patch the scanner
  hardening diff so the new receipt schema, validators, probe, lake writer,
  and preflight gates cannot fake-pass, leak forbidden fields, or weaken
  existing contracts.
intended_decision: >
  Return source-backed findings, a bounded working-tree patch if warranted,
  validation evidence, and residual risk for home-model/CA adjudication.
output_mode: review-report; durable report to docs/review-outputs/tiktok_scanner_hardening_delegated_adversarial_code_review_v0.md, delegated return also summarized in chat/courier block
template_kind: review + bounded patch commission; no runtime model routing
edit_permission: patch-only within target_files_or_dirs
target_files_or_dirs:
  - forseti-harness/capture_spine/tiktok_creator_discovery_frontier/models.py
  - forseti-harness/capture_spine/tiktok_creator_discovery_frontier/validation.py
  - forseti-harness/capture_spine/tiktok_creator_discovery_frontier/register_lake_writer.py
  - forseti-harness/capture_spine/tiktok_creator_discovery_frontier/__init__.py
  - forseti-harness/source_capture/adapters/browser_session_probe.py
  - forseti-harness/runners/run_tiktok_creator_discovery_register.py
  - forseti-harness/runners/run_creator_profile_current_materialize.py
  - forseti-harness/tests/unit/test_tiktok_creator_discovery_frontier.py
  - forseti-harness/tests/unit/test_tiktok_creator_discovery_frontier_selector.py
  - forseti-harness/tests/unit/test_browser_session_probe.py
  - forseti-harness/tests/unit/test_creator_profile_materialize_preflight.py
read_only_flag_only:
  - forseti-harness/capture_spine/tiktok_creator_discovery_frontier/register_writer.py
  - forseti-harness/capture_spine/tiktok_creator_discovery_frontier/frontier_selector.py
  - forseti-harness/data_lake/root.py
  - forseti-harness/capture_spine/creator_profile_current/** (incl. registry_match_preflight.py, materialize.py)
  - forseti-harness/tests/contract/** (esp. test_source_capture_packet_no_runtime_imports.py, test_capture_runner_lake_seam_coverage.py)
  - forseti-harness/tests/unit/test_instagram_reels_creator_metric_seed.py and its seed JSON (historical provenance pin)
  - docs/review-inputs/*_scan_receipt_*.json and fragranceknowledge_tiktok_creator_discovery_frontier_register_20260708.json (committed provenance; the v0 receipts stay v0 history)
  - .agents/hooks/** and all legacy ORCA_DATA_ROOT/.orca-* compatibility fallback chains
branch_or_commit_reference:
  workspace: a fresh worktree/checkout of eric-foo/forseti
  expected_branch: claude/tiktok-scanner-hardening
  base_pin: 2e8b0b80 (origin/main at branch cut)
  expected_head: branch tip at dispatch; review scope is the full branch diff vs the base pin
  pr: lane PR for this branch (operator_to_fill number)
dirty_state_allowance: clean tree at dispatch; your own working-tree patch stays uncommitted
doctrine_change_decision: none intended; do not change review, prompt, capture, or lake doctrine
isolation_decision: review/patch in the named branch checkout only
validation_gates:
  - python -m pytest tests/unit/test_tiktok_creator_discovery_frontier.py tests/unit/test_tiktok_creator_discovery_frontier_selector.py tests/unit/test_browser_session_probe.py tests/unit/test_creator_profile_materialize_preflight.py -q
  - python -m pytest tests/unit tests/contract -q
  - git diff --check
thread_operating_target_continuity:
  carried_forward: yes
  reason: same_workstream (cold-agent creator scanning without silent misses)
  lifecycle_status: active_thread_local
```

## Delegated Review-And-Patch Commission

You are the independent receiving controller for a `delegated_code_review_and_patch`
pass. The author/home dispatcher is `Anthropic/Claude-family`. Fill your own
`controller_model_family` before review. If your controller family is not
different from the author/home family, label the pass `same_vendor_sanity` or
`self_fallback`; do not claim cross-vendor discovery or no-new-seam.

```yaml
lane_binding:
  overlay_status: provisional_opt_in
  operating_contract_pointer: .agents/workflow-overlay/delegated-review-patch.md
  review_lane: workflow-code-review under Review Prompt Defaults, with workflow-deep-thinking before the source-gated method
  mode: base-subagent
  access: repo
  current_receiving_actor_role: controller
  dispatch_mode: external-controller-courier
  de_correlation_status: operator_to_fill
```

Source-gated method sequence:

1. `REFERENCE-LOAD` method instructions for `workflow-deep-thinking` and
   `workflow-code-review`. Do not apply them yet.
2. `SOURCE-LOAD` the required sources below from the named checkout.
3. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
4. Only then `APPLY` deep-thinking, then code review, then bounded patch execution.

Required source reads:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/delegated-review-patch.md`
- `.agents/workflow-overlay/safety-rules.md`
- the full branch diff vs the base pin, then every file in `target_files_or_dirs`
- `forseti-harness/capture_spine/tiktok_creator_discovery_frontier/register_writer.py` (builder the new pieces attach to)
- `forseti-harness/data_lake/root.py` (append_record semantics the lake writer relies on)
- `forseti-harness/capture_spine/creator_profile_current/registry_match_preflight.py` (has_blocking_preflight_results consumed by the materialize gate)
- `forseti-harness/capture_spine/linkedin_live_runtime/browser_driver.py` `_validate_cdp_endpoint` (the local-only posture the probe mirrors)
- `forseti-harness/tests/contract/test_source_capture_packet_no_runtime_imports.py` (why the probe lives under source_capture/adapters/)
- `docs/workflows/forseti_data_lake_rename_execution_closeout_handoff_v0.md` (workstream scope + drift guard)

Context the diff encodes (verify, do not trust): the scan-receipt schema is
bumped to `tiktok_creator_discovery_scan_receipt_v1` with a required
`link_hub_capture_status` (closed vocab `captured|blocked|deferred_not_authorized|none_visible`)
plus `link_hub_url_or_none`; PROMOTE frontier decisions now require a non-null
`registry_preflight_status_or_none` on the selected node; a probe-and-report-only
CDP endpoint probe exists; frontier registers can be appended to the lake as
derived records anchored to the parent-grid packet; and materializing new
registry accounts requires a non-blocking preflight receipt.

Review focus (adversarial - try to break it):

- Fake-pass paths: can a receipt or register still validate green while a
  visible link hub was skipped, a PROMOTE lands without preflight, or a
  "captured" claim carries no evidence? Can the new guards be satisfied by
  vacuous values?
- Schema-bump completeness: any other producer/consumer of scan receipts that
  still emits/expects v0 and now silently diverges?
- Probe posture: can the probe be coaxed into non-local hosts, credentialed
  URLs, attaching, or leaking forbidden keys (`session`, `cookies`) into
  receipts embedding its report?
- Lake writer: does `append_record` usage preserve write-once/append-only
  semantics, correct anchoring, and fail-closed behavior on a missing parent
  packet anchor? Any path to a second writable home or overwrite?
- Materialize gate: bypass routes inside the named set (flag out-of-scope
  bypasses such as direct `materialize.py` calls as residuals, read-only).
- Runner: mutual-exclusion of `--output` vs lake target; error visibility.
- Existing-contract regressions across the touched files.

Non-goals and hard constraints:

- No live TikTok/IG capture, browser control, or network fetch (the probe's
  own unit tests use injected openers; keep it that way).
- No registry-to-lake migration, no CSB hook edits, no scanner-runner executor
  build-out, no schema redesign beyond the committed v1 shape.
- No edits to provenance files, contract tests, compatibility fallbacks, or
  anything outside `target_files_or_dirs` - flag only.
- Do not commit, push, merge, rebase, or open/modify PRs.

Return contract:

Start with findings first. If a patch is warranted, apply it in the working
tree and leave it uncommitted. Write the durable report to
`docs/review-outputs/tiktok_scanner_hardening_delegated_adversarial_code_review_v0.md`
and, after the final write, run
`python .agents/hooks/check_review_output_provenance.py --strict <report-path>`
and report the observed exit. Then return:

```text
DELEGATED_CODE_REVIEW_RETURN_FOR_HOME_MODEL

- de_correlation_receipt: author/home family, controller family, status
- source_context_status: READY or INCOMPLETE, with missing sources
- findings: file/line citations, impact, minimum closure condition
- patch_summary: changed files and why each change is inside scope
- diff: unified diff or clear changed-file summary
- validation_results: commands run and exact pass/fail/not-run status
- residual_risks: remaining uncertainty
- off_scope_flags: anything outside the named target set
- reviewer_verdict: decision input only, not CA acceptance
```

Instruct the commissioning Chief Architect to close the adjudication per
`.agents/workflow-overlay/communication-style.md` -> Review Adjudication Next
Step: adjudicate findings/diff/verdict/residuals as claims, close self-closable
material issues in the same turn, route smallest-complete closure steps only
where genuinely needed, then one batched land step plus the deep-thought 1-5
material next moves.

If the correct fix requires contract-test rewrite, schema redesign, registry
relocation, or scanner-executor architecture, return `NEEDS_ARCHITECTURE_PASS`
and do not keep a partial patch.
