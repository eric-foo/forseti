# Parfumo Live Rendered Projection Adversarial Code Review Patch Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Repo-mode delegated adversarial code review-and-patch commission for the
  latest PR #532 Parfumo live-rendered DOM projection parser and explicit
  capture-route guard patch.
use_when:
  - Commissioning a different-family controller to review and patch the latest
    Parfumo live-rendered parser / route-default closure before home-model
    adjudication.
  - Rechecking commit 9066900f after the prior delegated review escalated
    slice-loss / duplicate-metric findings.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/review-lanes.md
  - docs/workflows/parfumo_targeted_capture_contract_v0.md
  - docs/review-outputs/parfumo_targeted_projection_metrics_delegated_code_review_v0.md
branch_or_commit: codex/parfumo-targeted-projection-metrics @ 9066900fab64d85115b5b978a777767b6e9ff07e
```

## Paste-Ready Delegated Adversarial Code Review-And-Patch Prompt

You are the independent controller for a delegated adversarial code review-and-patch pass. This is an operator-couriered, repo-mode prompt. Inspect the pinned worktree directly; do not review from this prompt text alone.

### Actor / Model-Family Receipt

- author_home_model_family: OpenAI / GPT-family Codex
- current_receiving_actor_role: controller
- dispatch_mode: external-controller-courier
- required_controller_family: a different vendor / model lineage from OpenAI / GPT-family
- controller_model_family: operator_to_fill
- de_correlation_status: satisfied only if your actual runtime family is not OpenAI / GPT-family
- If your runtime is OpenAI / GPT-family, return `BLOCKED_CONTROLLER_NOT_DECORRELATED` for the cross-vendor delegated pass, or explicitly downgrade to `same_vendor_sanity` only if the operator authorizes that weaker bar.
- This is a who-constraint, not a model recommendation. Do not include a recommended-model block.

### Orca Prompt Preflight Deltas

preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` v0 - constants bound; deltas stated below.

```yaml
authorization_basis: current owner request "delegate patch prompt" after commit 9066900f on PR #532
objective: >
  Review whether the latest Parfumo patch actually closes the accidental direct
  HTTP default route and live-rendered DOM parser underfit without reintroducing
  silent review loss, duplicate Silver MetricObservation facts, fake corpus
  completeness, or no-blur drift.
intended_decision: >
  Return source-backed findings, a bounded working-tree patch if warranted,
  validation evidence, and residual risk for home-model/CA adjudication.
fitness_reference:
  goal: >
    Keep the Parfumo targeted rendered capture -> projection -> Cleaning/Silver
    route source-visible and no-blur: browser-rendered targeted artifacts are
    the normal route, direct HTTP is explicit canary/fallback only, and
    unavailable full-corpus / high-low coverage stays residualized.
  done_looks_like: >
    The reviewer can show from code, tests, and local packet/projection evidence
    that the latest patch parses live Parfumo review and statement cards, blocks
    accidental direct-HTTP capture selection, and leaves any unresolved coverage
    or route uncertainty visible.
output_mode: file-write source prompt; delegated return is review-report plus bounded source patching
required_output_path: docs/review-outputs/parfumo_live_rendered_projection_adversarial_code_review_patch_v0.md
template_kind: delegated_code_review_and_patch; adversarial code review patch commission
edit_permission: patch-only
target_files_or_dirs:
  - orca-harness/source_capture/parfumo_projection.py
  - orca-harness/runners/run_parfumo_mgt_capture.py
  - orca-harness/tests/unit/test_parfumo_projection.py
  - orca-harness/tests/unit/test_parfumo_mgt_capture_runner.py
read_only_flag_only:
  - docs/prompts/reviews/parfumo_live_rendered_projection_adversarial_code_review_patch_prompt_v0.md
  - docs/review-outputs/parfumo_targeted_projection_metrics_delegated_code_review_v0.md
  - docs/workflows/parfumo_targeted_capture_contract_v0.md
  - all Basenotes files/routes
  - all Fragrantica reference modules
  - all no-blur infrastructure and lane registry files
  - all Cleaning, Silver, ECR, Judgment, CI, hook, and PR configuration files
branch_or_commit_reference:
  workspace: C:\Users\vmon7\Desktop\projects\orca\worktrees\parfumo-targeted-projection-metrics
  expected_branch: codex/parfumo-targeted-projection-metrics
  expected_head: 9066900fab64d85115b5b978a777767b6e9ff07e
  review_patch_range: 383f7a0b967f1d134cf63ea6caf07ddd3d7a4993..9066900fab64d85115b5b978a777767b6e9ff07e
  pr: https://github.com/eric-foo/orca/pull/532
dirty_state_allowance: >
  Clean at start, or only your own review report and bounded patch changes. If
  unrelated dirty files are present, block before review.
controlling_source_state: checked at prompt authoring for branch/head and target diff; receiver must recheck
doctrine_change_decision: none intended; do not change review, prompt, capture, no-blur, or source-access doctrine
isolation_decision: existing PR worktree; do not create a new worktree unless this worktree is inaccessible and the operator explicitly authorizes a substitute
validation_gates:
  - python -m py_compile runners\run_parfumo_mgt_capture.py source_capture\parfumo_projection.py
  - python -m pytest -q tests\unit\test_parfumo_projection.py tests\unit\test_parfumo_mgt_capture_runner.py tests\test_parfumo_native_pipeline_lake.py
  - $env:ORCA_DATA_ROOT=$null; python -m pytest -q
  - git diff --check
thread_operating_target_continuity:
  carried_forward: no
  reason: no_visible_active_target
  changed_from_input: no
  lifecycle_status: not_applicable
repo_map_decision: not_needed
repo_map_reason: >
  The prompt target, required sources, and output destinations are already bound
  by explicit user request, overlay files, existing PR #532 prompt/report, and
  named Parfumo source files.
```

### Cynefin Router

Smallest complete outcome: a source-backed delegated adversarial code review of the latest four-file Parfumo live-rendered parser / route-guard patch, with bounded patch only for material issues inside those four files.

Regime: Complicated.

Why: The patch is narrow, but it sits on top of prior slice/Silver findings and live DOM evidence, so correctness depends on source-visible route and parser semantics rather than a trivial diff read.

Decomposition: Risk-first within a layer-based review: route-default guard first, live DOM parser semantics second, prior F1/F2/F3 closure and residualization third, tests/validation fourth.

Current bottleneck: Whether commit 9066900f closes the accidental direct HTTP default and live rendered parser underfit without silently dropping reviews, double-counting review ratings, or overstating high/low/full-corpus coverage.

Riskiest assumption: Mapping Parfumo order/filter state (`order_date_desc`, `order_scent_desc`, `order_scent_asc`) onto latest/high/low slices is source-visible and total enough for the targeted sample without numeric-threshold invention or hidden review loss.

Stop or pivot condition: If the correct fix requires Cleaning/Silver lane changes, lane registry changes, Basenotes/proxy work, live capture, anti-bot behavior, broader architecture, or a source-access doctrine change, stop patching and return `NEEDS_ARCHITECTURE_PASS` or an off-scope finding.

Allowed next move: SOURCE-LOAD the named files, APPLY `workflow-deep-thinking`, then APPLY `workflow-code-review`, patch bounded material issues in the four target files only, validate, and write the review report.

Disallowed next move: Do not run live capture, browser automation, proxy, direct HTTP network fetch, anti-bot/Cloudflare work, Basenotes work, Silver raw-writer work, or any patch outside the four target files.

### Source-Gated Method Contract

1. REFERENCE-LOAD these method instructions before source analysis:
   - `workflow-deep-thinking`
   - `workflow-code-review`
   - `workflow-delegated-review-patch`
2. Do not APPLY them yet. Use them only to prepare a neutral source-reading lens.
3. SOURCE-LOAD the required sources below from the pinned worktree.
4. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` with missing sources and conflicts.
5. Only after source readiness, APPLY `workflow-deep-thinking` to frame failure modes, then APPLY `workflow-code-review` to produce findings and bounded patches.

### Required Source Load

Load authority and lane files first:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/decision-routing.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/delegated-review-patch.md`
- `.agents/workflow-overlay/safety-rules.md`
- `.agents/workflow-overlay/communication-style.md`

Load Parfumo contract, research, and prior review context:

- `docs/workflows/parfumo_targeted_capture_contract_v0.md`
- `docs/research/orca_fragrance_native_database_live_probe_v0.md`
- Historical handoff packet if available in the repo object database:
  `git show 5865f4d7a2fdd14114e04d8bac9fecc686fda17c:docs/workflows/fragrance_native_capture_pipeline_parfumo_basenotes_build_handoff_v0.md`
- `docs/prompts/reviews/parfumo_targeted_projection_metrics_delegated_code_review_prompt_v0.md`
- `docs/review-outputs/parfumo_targeted_projection_metrics_delegated_code_review_v0.md`

Load no-blur and front-door infrastructure for boundary checking, not patching:

- `orca-harness/data_lake/silver_record.py`
- `orca-harness/data_lake/non_silver_record.py`
- `orca-harness/data_lake/lane_registry.py`
- `.agents/hooks/check_silver_lane_registry.py`

Load Fragrantica reference modules for parity, not copy-paste authority:

- `orca-harness/source_capture/fragrantica_projection.py`
- `orca-harness/cleaning/fragrantica.py`
- `orca-harness/cleaning/fragrantica_lake.py`
- `orca-harness/tests/test_fragrantica_capture_to_silver_e2e.py`
- `orca-harness/tests/test_fragrantica_cleaning_lake_pilot.py`

Load the four target files and inspect the patch range:

- `orca-harness/source_capture/parfumo_projection.py`
- `orca-harness/runners/run_parfumo_mgt_capture.py`
- `orca-harness/tests/unit/test_parfumo_projection.py`
- `orca-harness/tests/unit/test_parfumo_mgt_capture_runner.py`
- `git diff 383f7a0b967f1d134cf63ea6caf07ddd3d7a4993..9066900fab64d85115b5b978a777767b6e9ff07e -- orca-harness/source_capture/parfumo_projection.py orca-harness/runners/run_parfumo_mgt_capture.py orca-harness/tests/unit/test_parfumo_projection.py orca-harness/tests/unit/test_parfumo_mgt_capture_runner.py`

Optional local evidence to inspect if present, not authority and not fixture admission:

- `orca-harness/_test_runs/parfumo_rendered_latest_probe_after_live_parser/projection.json`
- `orca-harness/_test_runs/parfumo_rendered_latest_probe_after_live_parser/out/targeted_rendered_packet/manifest.json`

### Source Context Notes From The Commissioning Lane

Treat these as hypotheses to verify, not proof:

- The checked-out worktree path did not contain `docs/workflows/fragrance_native_capture_pipeline_parfumo_basenotes_build_handoff_v0.md`; the packet was recovered from the repo object database with the `git show 5865f4d...:<path>` command above.
- The current lane holds Basenotes out of scope as access-blocked for this work, even though older packet text contains residential-proxy Basenotes language.
- Commit 9066900f touched four files: the Parfumo projection parser, the Parfumo capture runner CLI route guard, and two unit test files.
- Fresh rendered local probe evidence after 9066900f reportedly produced packet `01KWCNKC6HCEJ2DWDSMKGCESD1`, 14 projection rows, 5 latest review cards, 5 statement rows, and 10 bindings from a local Chrome-extension rendered Parfumo artifact. Treat this as inspectable local scratch only if the files are present; do not treat it as durable fixture admission or full-corpus capture.

### Bounded Patch Scope

You may edit only these four files:

- `orca-harness/source_capture/parfumo_projection.py`
- `orca-harness/runners/run_parfumo_mgt_capture.py`
- `orca-harness/tests/unit/test_parfumo_projection.py`
- `orca-harness/tests/unit/test_parfumo_mgt_capture_runner.py`

Everything else is read-only / flag-only. If the correct fix requires Cleaning, Silver, lane registry, Fragrantica, Basenotes, docs contract, overlay, hook, CI, live-capture route, or PR metadata changes, do not patch those files. Return an off-scope finding with `minimum_closure_condition`, or `NEEDS_ARCHITECTURE_PASS` for design-level issues.

Do not commit, push, merge, rebase, open/modify PRs, or run live network/browser/proxy capture. Leave any bounded patch uncommitted for home-model adjudication.

### Review Axis

Attack whether commit 9066900f:

- makes browser-rendered targeted artifacts the practical route for Parfumo by requiring explicit `--targeted-rendered` or explicit `--direct-http` for actual captures;
- avoids accidental direct HTTP selection while preserving direct HTTP only as explicit canary/fallback behavior;
- handles `--preflight-only` route behavior intentionally rather than accidentally bypassing the new route guard;
- parses live Parfumo rendered review cards using source-visible structures such as `article.review`, `review_article_<id>`, `/reviews/<id>`, schema.org `ratingValue`, `datePublished`, `itemprop=author/name`, and `r_text_<id>`;
- parses live Parfumo statement cards using source-visible structures such as `statement-bubble`, `/statements/<id>`, `s_text_content_<id>`, relative date text, author `/Users/.../statements`, and Scent numeric rating;
- maps high/low/latest only from source-visible Parfumo order/filter/tab evidence (`order_scent_desc`, `order_scent_asc`, `order_date_desc`, active order state, labels) rather than hidden numeric thresholds or Fragrantica 1/4/5-star inheritance;
- prevents the prior delegated review's F1/F2/F3 class: no silent drop of captured review cards, no duplicate TextObservation or MetricObservation facts for one source-visible review rating, and no invented high/low partition claim;
- avoids parsing route receipts, screenshots, plans, metadata JSON, visible-text-only files, or author profile URLs as review/statement source items;
- makes `source_item_url` point only to item-specific review/statement URLs when source-visible, not to author `/Users/.../statements` pages;
- residualizes unavailable coverage: high/low buckets absent when only Latest is captured, full review/statement corpus not captured, media/photo surfaces not preserved, and missing date/text/author fields;
- preserves no-blur: no Silver via raw writer, no cleaned/judged facts in projection, no Silver facts emitted for absent metrics or zero-filled metrics;
- leaves tests that would fail if live-shaped review/statement cards, route explicitness, source-item URL scoping, slice partitioning, residualization, or body-file filtering regresses.

### Non-Goals / Forbidden Work

- No Basenotes work. Hold Basenotes as access-blocked/out of scope for this lane.
- No full Parfumo corpus claim.
- No live Parfumo capture, browser control, network fetch, proxy use, cookie/storage export, Cloudflare clearance handling, CAPTCHA solving, stealth/fingerprint tooling, retry storm, or anti-bot escalation.
- No Silver writes through the raw writer.
- No Fragrantica rating-scale inheritance.
- No broad refactor or shared abstraction unless required to close a material finding inside the four-file scope.
- No prompt artifact edits; this prompt is read-only review input.

### Validation Evidence From Authoring Lane

The authoring lane reported these checks green after 9066900f. Treat them as evidence to inspect, not proof; re-run relevant checks after any patch.

- `python -m py_compile runners\run_parfumo_mgt_capture.py source_capture\parfumo_projection.py`
- `python -m pytest -q tests\unit\test_parfumo_projection.py tests\unit\test_parfumo_mgt_capture_runner.py tests\test_parfumo_native_pipeline_lake.py` -> 24 passed
- `$env:ORCA_DATA_ROOT=$null; python -m pytest -q` -> full suite passed with one unrelated warning
- `git diff --check` -> clean

### Controller Output Contract

Write the full review report to:

`docs/review-outputs/parfumo_live_rendered_projection_adversarial_code_review_patch_v0.md`

The report must be findings-first and include:

- `reviewed_by`: your actual model/tool identity, or `unrecorded` if unavailable.
- `authored_by`: `OpenAI / GPT-family Codex`.
- `de_correlation_bar`: `cross_vendor_discovery` if your runtime is not OpenAI/GPT-family; otherwise `same_vendor_sanity` or `self_fallback` with rationale.
- `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
- Source-read ledger with file paths and line citations for load-bearing claims.
- Findings ordered by materiality, each with:
  - finding id;
  - location;
  - implementation evidence;
  - authority/evidence basis;
  - impact;
  - `minimum_closure_condition`;
  - `next_authorized_action`;
  - whether patched in this pass.
- Unified diff for any patches you applied.
- Validation commands run and exact pass/fail/not-run status.
- Off-scope flags.
- Verdict and residual-risk note. The verdict is decision input only, not approval, validation, readiness, or merge authorization.
- `DELEGATED_CODE_REVIEW_RETURN_FOR_HOME_MODEL` courier block for adjudication.

After writing the report, return a compact chat summary plus this courier YAML:

```yaml
review_courier:
  output_mode: filesystem-output
  report_path: docs/review-outputs/parfumo_live_rendered_projection_adversarial_code_review_patch_v0.md
  commission: delegated adversarial code review-and-patch for PR #532 commit 9066900f
  target: latest Parfumo live-rendered projection parser and explicit capture-route guard patch
  authority: provisional delegated review-and-patch; code review lane findings-first; patch-only within four target files
  de_correlation_bar: <cross_vendor_discovery | same_vendor_sanity | self_fallback | blocked>
  reviewer_verdict: <decision input only>
  finding_ids: []
  patched_files: []
  validation: []
  minimum_closure_conditions: []
  next_authorized_action: home-model adjudication of findings/diff
  non_claims:
    - not approval
    - not validation
    - not readiness
    - not merge authorization
```

### Escalation

Return `NEEDS_ARCHITECTURE_PASS` and leave no kept partial patch if the issue is design-level or cannot be fixed inside the bounded four-file scope. Return `BLOCKED_REVIEW_LANE_UNAVAILABLE` if you cannot invoke `workflow-code-review` after source readiness. Return the nearest blocker if the worktree, branch, head SHA, source files, output path, or dirty-state conditions do not match this prompt.

Adjudicator next step, after the delegated return: first adjudicate the findings, diff, verdict, and residuals as claims. If any blocker, major issue, material unresolved issue, or material uncertainty remains, route the smallest complete closure step for that issue. Only after a clean adjudication, batch admin/lifecycle follow-ups into one land step and deep-think only the 1-3 material next moves that need judgment.
