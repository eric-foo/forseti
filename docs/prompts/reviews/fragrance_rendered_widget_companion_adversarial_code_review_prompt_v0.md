# Fragrance Rendered Widget Companion Adversarial Code Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Read-only adversarial implementation/code review prompt for PR #436 commit
  7201e6c5, covering the rendered fragrance PDP + widget response companion
  capture helper, runner, tests, and repo-map route.
use_when:
  - Dispatching an independent review of the rendered+widget companion capture route after the delegated-review-patch request routed out of the single-artifact convention.
  - Checking whether the companion route honestly preserves above-fold rendered facts, same-load widget traffic, and bounded fallback review rows without overclaiming source-wide coverage, ECR, Cleaning, Judgment, or review integrity.
authority_boundary: retrieval_only
output_mode: review-report
required_output_path: docs/review-outputs/adversarial-artifact-reviews/fragrance_rendered_widget_companion_adversarial_code_review_v0.md
```

prompt_boundary: prompt_only; review-use boundary stated below

## Commission

Perform a read-only adversarial implementation/code review of commit
`7201e6c5e8902c0a2432906bbe50d388214a5179` in:

`C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\fragrance-purchase-review-probes`

Review the delta from:

`6c730b31f8f8172dcce981bdf03c5ed8a38e0818..7201e6c5e8902c0a2432906bbe50d388214a5179`

This prompt is the route-out from an explicit `workflow-delegated-review-patch`
request. Orca's delegated-review-patch overlay applies to a separately
commissioned single high-stakes authored artifact or bounded patch target. This
submitted target is a multi-file implementation/code diff, so do not force it
into that convention and do not patch. Run read-only adversarial code review
with `workflow-deep-thinking` followed by `workflow-code-review` after source
readiness.

The review is decision input only. Do not edit files, create patch queues,
commit, push, run new live retailer probes, fetch network data, move review
bodies into tracked docs, or broaden into product planning. If the operator runs
this with a de-correlated reviewer, record that as review provenance only; it is
a who-constraint / measurement fact, not runtime-model routing or a model
recommendation.

## Delegated Review-Patch Overlay Resolution

```yaml
delegated_review_patch_resolution:
  selected_lane_mode: bound_prompt_route_out_for_code_review_not_patch_commission
  overlay_loaded: .agents/workflow-overlay/delegated-review-patch.md
  interface_fields_present:
    - status: provisional_opt_in
    - operating_contract_pointer
    - protected_path_list pointer
    - model_ladder ownership and de_correlation_criterion
    - access_modes
    - preflight_schema
    - source_context_fields
    - output_destinations
    - incomplete_commission_route_out
  interface_fields_unbound_or_operator_owned:
    - concrete_model_ids: none_bound_in_overlay
    - actual reviewer/controller identity: operator_to_fill
    - reviewed_by/authored_by provenance values: operator_or_reviewer_to_fill
  de_correlation_status: operator_to_fill; must not be claimed unless reviewed_by and authored_by establish different vendors/model lineages
  terminal_output_mode: filed review prompt plus paste-ready use instruction
  non_claims:
    - not a completed delegated review
    - not patch authorization
    - not a bound machine-routable delegated-review-patch lane
    - not runtime model recommendation
```

## Fitness Reference

```yaml
fitness_reference:
  goal: >
    Preserve an adaptable fragrance purchase-review capture route that combines
    what users likely see first on the PDP with source-visible review widget row
    coverage, while staying honest about which data was observed passively
    during render versus completed by bounded fallback.
  observable_success_signal: >
    A single operator command can produce a receipt with above-fold rendered
    facts, widget response provenance by origin, row-complete focused review
    coverage when bounded fallback URLs are supplied, and explicit residuals
    when passive render does not fire review rows; the receipt must not imply one
    literal HTTP request, source-wide review scraping, sentiment/integrity
    interpretation, ECR, Cleaning, Judgment, validation, readiness, or buyer
    proof.
```

## Thread Operating Target Continuity

```yaml
thread_operating_target_continuity:
  carried_forward: yes
  reason: same_workstream
  changed_from_input: no
  lifecycle_status: active_thread_local
thread_operating_target:
  anchor_goal: >
    Own the fragrance retailer purchase-review lane with enough source-visible
    review metadata and rendered PDP context for downstream decision-useful
    reading.
  output_fit_check: >
    Review capture receipts distinguish rendered first-view facts, widget row
    provenance, selected/skipped review coverage, aggregate rating context, and
    residuals without substituting exhaustive scraping or downstream
    sentiment/integrity labeling.
```

## Orca Start Preflight

```yaml
orca_start_preflight:
  agents_read: required
  overlay_read: required
  preflight_defaults: docs/prompts/templates/shared/orca_preflight_defaults_v0.md v0 - constants bound; deltas stated below
  authorization_basis: current user invoked workflow-delegated-review-patch after the rendered+widget companion commit was pushed
  source_pack: custom fragrance rendered+widget companion implementation review
  output_mode: review-report
  template_kind: review; repo-code-review template is unbound, so use Orca prompt-orchestrator fallback with workflow-code-review mechanics
  edit_permission: read-only review; report-write only to required_output_path
  target_scope: commit delta 6c730b31f8f8172dcce981bdf03c5ed8a38e0818..7201e6c5e8902c0a2432906bbe50d388214a5179
  expected_branch: codex/fragrance-purchase-review-probes
  expected_review_target_commit: 7201e6c5e8902c0a2432906bbe50d388214a5179
  expected_pr: 436
  dirty_state_checked: required
  dirty_state_allowance: >
    The reviewer should inspect the pinned target files by hash. This prompt
    artifact may exist on a later branch commit and is not part of the
    implementation review target unless it changes source authority. Any other
    modified or untracked files are out of scope unless they affect the pinned
    target files, prompt authority, or source authority.
  doctrine_change_decision: no doctrine change is requested by this review prompt
  isolation_decision: existing PR worktree; read-only review prompt over the current lane branch
  blocked_if_missing:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/delegated-review-patch.md
    - .agents/workflow-overlay/prompt-orchestration.md
    - .agents/workflow-overlay/review-lanes.md
    - .agents/workflow-overlay/validation-gates.md
    - .agents/workflow-overlay/template-registry.md
    - orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_rendered_companion_probe_v0.md
    - orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_focused_coverage_mgt_v0.md
```

## Required Method Sequence

1. Read this prompt.
2. Read `AGENTS.md` and `.agents/workflow-overlay/README.md`.
3. Read `.agents/workflow-overlay/source-of-truth.md`, `.agents/workflow-overlay/source-loading.md`, `.agents/workflow-overlay/delegated-review-patch.md`, `.agents/workflow-overlay/prompt-orchestration.md`, `.agents/workflow-overlay/review-lanes.md`, `.agents/workflow-overlay/validation-gates.md`, and `.agents/workflow-overlay/template-registry.md`.
4. REFERENCE-LOAD `workflow-deep-thinking`.
5. REFERENCE-LOAD `workflow-code-review`.
6. Do not APPLY either method yet.
7. SOURCE-LOAD all required authority, target, support, and validation evidence listed below.
8. Verify every pinned target hash below. If any hash mismatches, stop with `HASH_MISMATCH` and list the mismatched path, expected hash, actual hash, and nearest allowed next step.
9. Declare `SOURCE_CONTEXT_READY` only after the required sources and hashes are loaded. If any required source is missing, declare `SOURCE_CONTEXT_INCOMPLETE` with the gap and do not emit strict review claims.
10. Only after `SOURCE_CONTEXT_READY`, APPLY `workflow-deep-thinking` to frame failure modes and APPLY `workflow-code-review` in adversarial findings-first posture.
11. Write the full durable review report to `docs/review-outputs/adversarial-artifact-reviews/fragrance_rendered_widget_companion_adversarial_code_review_v0.md`.
12. After the report is written, return only a concise chat summary plus the fenced `review_summary` YAML block below.

If `workflow-code-review` is unavailable, unresolved, or cannot be applied,
return `BLOCKED_REVIEW_LANE_UNAVAILABLE` and do not substitute a self-review.

## Target Hash Pins

Verify these SHA256 pins before review:

```text
13F5E6B587B4F65D6C28C476A5FA4A37F9036DCC40D6F25B96C5542820B6BF26  docs/workflows/orca_repo_map_v0.md
B489EE8901168CEC702ACD4B837356D94D4BA1C73D4C3D78B0C4A316D516415D  orca-harness/runners/run_fragrance_rendered_widget_companion.py
AAB349906A305015FC89A1482E6CFA5566BC0FF5652765CA1CAAB9EC96E508E4  orca-harness/source_capture/__init__.py
527DC52DC6E729AF9053D0BEE24E37A78CB346CF4A2A76050660E5268A15C79F  orca-harness/source_capture/fragrance_rendered_widget_companion.py
609447E26A52D2A76957E69E9E2D624ECFBD3787A34C3A022582010F3419A12F  orca-harness/tests/unit/test_fragrance_rendered_widget_companion.py
```

Support-source pins to verify when citing adjacent behavior:

```text
AD102D9E0B34FB834A041A0140A9104AB57E2A91AF3D75B087C1F6B69A489EA5  orca-harness/source_capture/fragrance_review_coverage.py
5DCD77F98C1635C502F71E5BBCAD612DA9D80B03EBCF5F8A82926966130A65BF  orca-harness/tests/unit/test_fragrance_review_coverage.py
2FC41796E3D78EB740580497B70592F155B1D433EFD63B8E31654D350E209CB8  orca-harness/source_capture/adapters/browser_snapshot.py
```

## Required Source Basis

SOURCE-LOAD these authority and support files:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/delegated-review-patch.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/validation-gates.md`
- `.agents/workflow-overlay/template-registry.md`
- `docs/prompts/templates/shared/orca_preflight_defaults_v0.md`
- `orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_rendered_companion_probe_v0.md`
- `orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_focused_coverage_mgt_v0.md`
- `orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_row_contract_v0.md`
- all target files listed under Target Hash Pins
- support files listed under support-source pins when needed to evaluate integration behavior

Available but do not bulk-load by default unless they materially affect a finding:

- prior review outputs under `docs/review-outputs/`
- ignored live smoke receipts under `orca-harness/_test_runs/`
- unrelated PR #436 files outside the target delta
- unrelated product, scanning, Cleaning, ECR, or Judgment Spine files

## Implementation Summary To Verify

Commit `7201e6c5` is intended to add a combined rendered+widget companion route:

- captures one fragrance PDP render with above-fold DOM geometry and visible text hash;
- passively preserves same-load review-widget responses whose URLs match Judge.me or Yotpo v3 review endpoints;
- records each widget response with `response_origin` as either `render_passive` or `bounded_fallback`;
- builds a focused review-coverage subreceipt from all preserved review response bodies;
- marks fallback needed when no rows are present or deduped row count is below widget total count;
- fetches bounded fallback widget URLs only after the first render/passive attempt proves incomplete;
- exposes repeated `--fallback-widget-url` in the runner;
- validates fallback URLs as supported widget endpoints and rejects embedded credentials;
- records non-claims including not one literal HTTP request, not source-wide review coverage, not durable Attachment Records, and not ECR/Cleaning/Judgment;
- updates package exports and repo-map route text;
- adds synthetic tests for passive success, incomplete widget rows, fallback success when passive rows do not fire, and URL filtering.

The intended operator semantics are one command / one capture run, not one
literal network request. The design must preserve provenance rather than hide
that fallback direct widget requests completed what the render did not expose.

## Validation Evidence To Inspect

The implementation author observed these checks before this prompt was filed:

```text
python -m py_compile source_capture\fragrance_rendered_widget_companion.py runners\run_fragrance_rendered_widget_companion.py
```

Observed result: exit 0, no output.

```text
pytest -p no:cacheprovider -q --tb=short tests\unit\test_fragrance_rendered_widget_companion.py tests\unit\test_fragrance_review_coverage.py
```

Observed result:

```text
...........                                                              [100%]
```

Package export smoke:

```text
python -c "import source_capture; print(source_capture.FRAGRANCE_RENDERED_WIDGET_COMPANION_METHOD); print(source_capture.FragranceWidgetResponseCapture.__name__)"
```

Observed result:

```text
fragrance_rendered_widget_companion
FragranceWidgetResponseCapture
```

Live Luckyscent rendered+fallback smoke command wrote:

```text
_test_runs\fragrance_rendered_widget_companion_smoke_20260629\luckyscent_desktop_companion_with_fallback.json
```

Observed receipt summary:

```text
passive_count: 0
fallback_count: 2
fallback_needed: False
total_rows: 14
widget_total: 14
selected: 8
rating_counts: {"2":2,"3":4,"4":4,"5":4}
native_ids: 14
verified_true: 3
media_true: 0
aggregate_rating: 3.71
aggregate_count: 14
residuals: passive_widget_not_observed_during_render
coverage_residuals: none observed
```

Observed comparison against the earlier render-only companion:

```text
without_fallback: passive_count=0, fallback_count=0, fallback_needed=True, total_rows=null, widget_total=null, residuals=passive_widget_not_observed_during_render,passive_widget_review_responses_absent,bounded_direct_widget_fallback_needed_for_row_completion
with_fallback: passive_count=0, fallback_count=2, fallback_needed=False, total_rows=14, widget_total=14, residuals=passive_widget_not_observed_during_render
```

Fresh lifecycle reads observed after push:

```text
git log -1 --oneline
7201e6c5 Add rendered fragrance widget capture fallback

git status --short --branch
## codex/fragrance-purchase-review-probes...origin/codex/fragrance-purchase-review-probes

git ls-remote origin refs/heads/codex/fragrance-purchase-review-probes
7201e6c5e8902c0a2432906bbe50d388214a5179 refs/heads/codex/fragrance-purchase-review-probes
```

## Review Questions

Be adversarial about material implementation risks:

1. Does the companion receipt preserve the intended distinction between rendered above-fold observation, passive widget responses, and bounded fallback completion?
2. Can `fallback_needed` become falsely green when fallback responses are HTTP 200 but empty, malformed, duplicate-only, non-review bodies, or partial pages?
3. Does deduplication by `(requested_url, status)` risk dropping distinct response bodies or masking page-param differences?
4. Are direct fallback requests bounded enough, including URL validation, byte caps, timeout handling, non-cookie headers, and failure visibility?
5. Does the helper overclaim one command / one capture run in a way that a downstream reader could confuse with one literal HTTP request?
6. Does the model shape create backward-compatibility risk by replacing `passive_widget_responses` with `widget_responses`, and are package exports/tests adequate for that migration?
7. Is the browser-render observation sufficient for above-fold user-visible facts without hidden layout shifts, blocked-resource side effects, or false positives from duplicated nested text nodes?
8. Should the next implementation add a bounded DOM/interaction stage for lazy widgets: initial above-fold extract, scroll/click/wait for a review anchor, preserve newly fired widget traffic, then extract review-section DOM? If yes, identify the minimum design constraints and failure modes; do not patch in this review.
9. If review rows are visible in post-scroll DOM but widget API rows are absent, should the route parse DOM rows as a third origin (`rendered_dom_review_rows`) or keep direct widget fallback as the only row source? Assess risk, not implementation.
10. Does the current design correctly avoid ECR, Cleaning, Judgment, sentiment, pain/pleasure, integrity, credibility, demand, buyer-proof, validation, readiness, and source-wide scraping claims?
11. Are tests strong enough for malformed fallback, duplicate/partial fallback pages, non-200 fallback, unsupported fallback URL, direct fallback disabled, and passive+fallback mixed pages?
12. Does the repo-map wording accurately describe the new helper/runner without overclaiming capture completeness or delegated review readiness?

## Findings Standard

Report findings first, ordered by severity. Use these labels for priority only;
they are not a formal verdict authority:

- `critical`: defect can create fake row-complete success, hide fallback failure, misrepresent captured provenance, expose forbidden review bodies, or authorize forbidden downstream/source access behavior.
- `major`: defect can materially mislead downstream readers/agents, break core rendered+widget success signals, hide material residuals, or leave a high-risk test gap before merge.
- `minor`: bounded correctness, documentation, test, or maintainability issue that should be considered but does not block the branch by itself.
- `advisory`: optional hardening or future-work note.

Every actionable finding must include:

- finding id;
- severity;
- location;
- implementation evidence;
- authority/evidence basis;
- impact;
- minimum closure condition;
- next authorized action.

Do not emit `patch_queue_entry`; this is read-only review. Suggested remediation
direction is allowed only as advisory prose, not executor-ready instructions.

## Output Contract

Write the full durable report to:

`docs/review-outputs/adversarial-artifact-reviews/fragrance_rendered_widget_companion_adversarial_code_review_v0.md`

The report must include these provenance fields, supplied by the operator/reviewer or set to `unrecorded` if unavailable:

```yaml
reviewed_by: <operator_supplied_or_unrecorded>
authored_by: <operator_supplied_or_unrecorded; at minimum note 7201e6c5 implementation authored by Codex/GPT-5 if the operator accepts that provenance>
de_correlation_bar: cross_vendor_discovery | same_vendor_sanity | self_fallback | unrecorded
same_vendor_rationale: <required when de_correlation_bar is same_vendor_sanity>
```

After successful write, return a concise chat summary plus:

```yaml
review_summary:
  status: completed | blocked
  report_path: docs/review-outputs/adversarial-artifact-reviews/fragrance_rendered_widget_companion_adversarial_code_review_v0.md
  review_mode: read_only_adversarial_code_review
  recommendation: accept | accept_with_minor_findings | revise_before_merge | blocked
  findings_count:
    critical: <n>
    major: <n>
    minor: <n>
    advisory: <n>
  blocking_or_major_findings:
    - <id and one-line summary, or none>
  strict_only_blockers_or_not_proven_boundaries:
    - <lane/output/validation/de-correlation boundary, or none>
  dom_lazyload_recommendation: add_bounded_dom_trigger | keep_widget_fallback_only | blocked_or_not_assessed
  next_action: <owner/implementer next action>
```

Review-use boundary: findings are decision input only. This review does not
approve, validate, mandate remediation, authorize patches, authorize commits,
authorize source capture, authorize commercial/runtime use, or create ECR,
Cleaning, Judgment, buyer-proof, fixture-admission, or readiness evidence.