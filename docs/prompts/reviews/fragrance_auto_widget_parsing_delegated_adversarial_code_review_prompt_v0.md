# Fragrance Auto Widget Parsing Delegated Adversarial Code Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Filed prompt for a de-correlated, read-only adversarial implementation/code
  review of PR #436 commit b6bbef42, covering automatic Judge.me fallback
  derivation plus Judge.me JSON and Yotpo v3 review-row parsing.
use_when:
  - Dispatching an independent review of the latest fragrance purchase-review
    capture patch after the home lane added auto widget parsing.
  - Checking whether the rendered companion and focused coverage receipts now
    preserve source-visible review rows, aggregate context, native ids,
    verified flags, residuals, and provider provenance without overclaiming
    exhaustive scraping, review integrity, sentiment, ECR, Cleaning, Judgment,
    validation, readiness, or buyer proof.
authority_boundary: retrieval_only
output_mode: review-report
required_output_path: docs/review-outputs/adversarial-artifact-reviews/fragrance_auto_widget_parsing_adversarial_code_review_v0.md
open_next:
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/source-loading.md
  - .agents/workflow-overlay/validation-gates.md
  - orca-harness/source_capture/fragrance_rendered_widget_companion.py
  - orca-harness/source_capture/fragrance_review_coverage.py
input_hashes:
  orca-harness/source_capture/fragrance_rendered_widget_companion.py: 1D53A87197829CC8CB456C77761977D8242DB1722DADB3322A1578E83ECBB5D9
  orca-harness/source_capture/fragrance_review_coverage.py: AD8AAA0B2F371DA9F4E6DF4CDD60587A8326CD4C465020639A4E7A07A843CB93
  orca-harness/tests/unit/test_fragrance_rendered_widget_companion.py: 194BB39091D3DE347A2E3FC094B9DF9CEC8D92CD4C64277ADE138468A9C26EEF
  orca-harness/tests/unit/test_fragrance_review_coverage.py: 6FFF1FC205AC6624AA618372C41F7727FF3D243E97F4532990BCC7363B3FA585
branch_or_commit: codex/fragrance-purchase-review-probes @ b6bbef420b88511cd7ea7008ec5a1eabd5ba5a9d
stale_if:
  - PR #436 is rebased, amended, closed, superseded, or retargeted.
  - Any target file hash above changes.
  - The source capture playbook, focused review-row contract, or review-lane
    rules change materially before the review runs.
```

prompt_boundary: prompt_only; review-use boundary stated below

## Commission

Perform a read-only adversarial implementation/code review of commit:

`b6bbef420b88511cd7ea7008ec5a1eabd5ba5a9d`

in:

`C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\fragrance-purchase-review-probes`

Review only the delta:

`b8773277dd9858a60e72e8f512499fdfad4c4622..b6bbef420b88511cd7ea7008ec5a1eabd5ba5a9d`

PR context:

```yaml
pull_request:
  number: 436
  url: https://github.com/eric-foo/orca/pull/436
  title: "[codex] Pin fragrance purchase-review retailer recon"
  base_ref: main
  head_ref: codex/fragrance-purchase-review-probes
  head_oid_at_prompt_creation: b6bbef420b88511cd7ea7008ec5a1eabd5ba5a9d
```

This is a route-out from an explicit delegated-review request. Orca's
delegated-review-patch overlay applies to a separately commissioned single
high-stakes authored artifact or bounded patch target. This submitted target is
a multi-file implementation/code diff, so do not force it into the single-file
review-and-patch convention and do not patch. Run read-only adversarial code
review with `workflow-deep-thinking` followed by `workflow-code-review` after
source readiness.

The review is decision input only. Do not edit files, create patch queues,
commit, push, run new live retailer probes, fetch network data, move review
bodies into tracked docs, or broaden into product planning. If the operator
runs this with a de-correlated reviewer, record that as review provenance only;
it is a who-constraint / measurement fact, not runtime-model routing and not a
model recommendation.

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
  actor_model_family_receipt:
    author_home_model_family: OpenAI/GPT-family Codex lane authored the patch; exact model/version operator_to_fill or unrecorded
    controller_model_family: operator_to_fill_must_differ_from_author_home_family_for_cross_vendor_discovery
    current_receiving_actor_role: controller
    dispatch_mode: external-controller-courier
    de_correlation_status: operator_to_fill(satisfied | blocked)
  de_correlation_bar: operator_to_fill(cross_vendor_discovery | same_vendor_sanity | self_fallback | unrecorded)
  no_model_recommendation: true
  terminal_output_mode: filed review prompt plus paste-ready copy
  non_claims:
    - not a completed delegated review
    - not patch authorization
    - not a bound machine-routable delegated-review-patch lane
    - not runtime model recommendation
```

Hard block rules:

- If the controller model family is missing, undisclosed, or the same vendor /
  model lineage as the author/home family, do not claim cross-vendor discovery.
  Return the nearest de-correlation blocker or record a weaker
  `same_vendor_sanity` / `self_fallback` boundary.
- If the reviewer cannot access the pinned worktree/revision, return a
  worktree/source blocker. Do not review a summary, alternate checkout,
  recreated source pack, or unpinned branch as a substitute.
- Do not include a `Recommended model` block or any runtime model
  recommendation.

## Fitness Reference

```yaml
fitness_reference:
  goal: >
    Preserve an adaptable fragrance purchase-review capture route that combines
    rendered PDP context with provider-widget review-row coverage across the
    current five target retailers, while keeping provider provenance and
    residuals explicit.
  observable_success_signal: >
    A single operator capture command can produce receipts where Judge.me sites
    auto-derive bounded fallback pages from rendered DOM when passive render
    does not fire rows, Yotpo v3 passive rows are parsed when seen, row bodies
    and native ids are available for focused reader selection, current aggregate
    rating context is present, media/verified/native-id counts are explicit, and
    mismatches or absent media stay visible rather than becoming fake success.
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
    provenance, selected/skipped review coverage, aggregate rating context,
    verified/native/media counts, and residuals without substituting exhaustive
    scraping or downstream sentiment/integrity labeling.
```

## Orca Start Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  preflight_defaults: docs/prompts/templates/shared/orca_preflight_defaults_v0.md v0 - constants bound; deltas stated below
  authorization_basis: current user asked for a delegated review prompt after commit b6bbef42 was implemented and pushed
  source_pack: custom fragrance auto widget parsing implementation review
  output_mode: review-report
  template_kind: review; repo-code-review template is unbound, so use Orca prompt-orchestrator fallback with workflow-code-review mechanics
  edit_permission: read-only review; report-write only to required_output_path
  target_scope: commit delta b8773277dd9858a60e72e8f512499fdfad4c4622..b6bbef420b88511cd7ea7008ec5a1eabd5ba5a9d
  expected_branch: codex/fragrance-purchase-review-probes
  expected_review_target_commit: b6bbef420b88511cd7ea7008ec5a1eabd5ba5a9d
  expected_pr: 436
  dirty_state_checked: yes
  dirty_state_allowance: >
    The reviewer should inspect the pinned target files by hash. This prompt
    artifact may exist on a later branch commit and is not part of the
    implementation review target unless it changes source authority. Any other
    modified or untracked files are out of scope unless they affect the pinned
    target files, prompt authority, or source authority.
  doctrine_change_decision: no doctrine change is requested by this review prompt
  isolation_decision: existing PR worktree; read-only review prompt over the current lane branch
  validation_gates:
    - target hash verification before review
    - report write verification by reviewer
    - no source edits by reviewer
    - no formal validation/readiness claim unless separately bound
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
    - orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_focused_coverage_mgt_v0.md
    - orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_rendered_companion_probe_v0.md
    - orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_row_contract_v0.md
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
11. Write the full durable review report to `docs/review-outputs/adversarial-artifact-reviews/fragrance_auto_widget_parsing_adversarial_code_review_v0.md`.
12. After the report is written, return only a concise chat summary plus the fenced `review_summary` YAML block below.

If `workflow-code-review` is unavailable, unresolved, or cannot be applied,
return `BLOCKED_REVIEW_LANE_UNAVAILABLE` and do not substitute a self-review.

## Target Hash Pins

Verify these SHA256 pins before review:

```text
1D53A87197829CC8CB456C77761977D8242DB1722DADB3322A1578E83ECBB5D9  orca-harness/source_capture/fragrance_rendered_widget_companion.py
AD8AAA0B2F371DA9F4E6DF4CDD60587A8326CD4C465020639A4E7A07A843CB93  orca-harness/source_capture/fragrance_review_coverage.py
194BB39091D3DE347A2E3FC094B9DF9CEC8D92CD4C64277ADE138468A9C26EEF  orca-harness/tests/unit/test_fragrance_rendered_widget_companion.py
6FFF1FC205AC6624AA618372C41F7727FF3D243E97F4532990BCC7363B3FA585  orca-harness/tests/unit/test_fragrance_review_coverage.py
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
- `orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_focused_coverage_mgt_v0.md`
- `orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_rendered_companion_probe_v0.md`
- `orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_row_contract_v0.md`
- all target files listed under Target Hash Pins

Available but do not bulk-load by default unless they materially affect a finding:

- prior review prompts and review outputs under `docs/prompts/reviews/` and `docs/review-outputs/`
- ignored live smoke receipts under `orca-harness/_test_runs/fragrance_live_widget_probe_after_patch_20260629/`
- unrelated PR #436 files outside the target delta
- unrelated product, scanning, Cleaning, ECR, Judgment, or proof files

## Implementation Summary To Verify

Commit `b6bbef42` is intended to make the rendered+widget companion and focused
coverage route provider-aware across the current fragrance review targets:

- DOM observation now extracts Judge.me provider metadata from rendered HTML,
  including Judge.me presence, MyShopify domains, product ids, JSON-LD aggregate
  rating, and review count.
- The capture helper auto-derives bounded Judge.me fallback URLs from that DOM
  metadata only when the first render/passive attempt still needs fallback and
  no manual fallback URLs were supplied.
- Judge.me fallback is bounded to 10 reviews per page and at most 5 pages.
- Parseable review response kinds now include both `judgeme_reviews_for_widget`
  and `yotpo_v3_reviews`.
- Focused review coverage now parses Judge.me JSON review lists, including
  native ids / UUIDs, verified flags, body HTML converted to text, date, rating,
  reviewer display, helpful votes, badges, media flags, aggregate totals, and
  widget aggregate fallback when PDP JSON-LD aggregate is absent.
- Focused review coverage now parses Yotpo v3 review rows and labels them with
  `row_source: yotpo_v3_review` and `source_widget: yotpo`.
- Aggregate mismatches between PDP JSON-LD counts and widget totals remain
  visible as residuals instead of being silently normalized.
- Tests cover auto Judge.me route derivation, Judge.me JSON-list parsing, and
  Yotpo v3 row parsing.

The intended operator semantics remain one capture run / one operator command,
not one literal network request. The route must preserve provenance:
`render_passive` rows are different from bounded fallback rows, and a fallback
row-complete receipt still carries the passive-render residual when the widget
did not fire during render.

## Validation Evidence To Inspect

The implementation author observed these checks before this prompt was filed:

```text
git diff --check
```

Observed result: exit 0, no output.

```text
$env:PYTHONDONTWRITEBYTECODE=1; python -m pytest -p no:cacheprovider --no-header --no-summary tests\unit\test_fragrance_review_coverage.py tests\unit\test_fragrance_rendered_widget_companion.py -q
```

Observed result:

```text
..........................                                               [100%]
```

Live five-source smoke receipts were observed under:

`orca-harness\_test_runs\fragrance_live_widget_probe_after_patch_20260629`

Observed summary:

```text
Indigo:      fallback_needed=False, rows=13, selected=2, native_ids=13, verified=12, media=0, residuals=passive_widget_not_observed_during_render
Ministry:    fallback_needed=False, rows=4,  selected=3, native_ids=4,  verified=3,  media=0, residuals=passive_widget_not_observed_during_render
TwistedLily: fallback_needed=False, rows=6,  selected=6, native_ids=6,  verified=6,  media=0, residuals=passive_widget_not_observed_during_render
Luckyscent:  fallback_needed=False, rows=14, selected=8, native_ids=14, verified=3,  media=0, residuals=passive_widget_not_observed_during_render
ZGO:         fallback_needed=False, rows=1,  selected=1, native_ids=1,  verified=1,  media=0, coverage_residuals=aggregate_review_count_widget_total_count_mismatch
```

Fresh lifecycle reads observed after push:

```text
git log -1 --oneline
b6bbef42 Add auto fragrance review widget parsing

git status --short --branch
## codex/fragrance-purchase-review-probes...origin/codex/fragrance-purchase-review-probes

git rev-parse HEAD origin/codex/fragrance-purchase-review-probes
b6bbef420b88511cd7ea7008ec5a1eabd5ba5a9d
b6bbef420b88511cd7ea7008ec5a1eabd5ba5a9d
```

## Review Questions

Be adversarial about material implementation risks:

1. Can Judge.me auto fallback derive the wrong `shop_domain` or `product_id`
   from noisy page HTML, multiple products, recommendations, bundled widgets,
   or stale JSON-LD?
2. Can the bounded Judge.me fallback become falsely green when review count is
   higher than 50, when pages beyond the cap contain the only selected rows, or
   when page totals disagree with row count?
3. Does the route preserve the difference between passive render traffic and
   bounded fallback enough for downstream data-integrity reasoning?
4. Can `fallback_needed` become falsely green for duplicate-only fallback
   pages, empty rows with widget totals, malformed bodies, or provider payloads
   that parse but omit review text?
5. Does Judge.me JSON parsing preserve real review bodies without accidentally
   retaining markup, script text, hidden fields, generic widget chrome, or
   source-visible fields that imply sentiment/integrity interpretation?
6. Does Yotpo v3 parsing generalize enough for the observed ZGO payload without
   overfitting to one row or conflating PDP aggregate count with the endpoint's
   review count?
7. Is the aggregate fallback rule correct: PDP JSON-LD aggregate wins when
   present, widget JSON aggregate fills only when PDP aggregate is absent, and
   mismatches stay visible?
8. Is media detection broad enough for observed Judge.me/Yotpo payload shapes
   without overcounting avatars, product images, badge icons, or generic hosted
   video metadata?
9. Are verified-purchase flags normalized without treating missing/unknown as
   false success?
10. Are native review ids and candidate keys stable enough across provider
    shapes, and are weaker-key residuals still visible?
11. Do the tests cover the highest-risk failure modes: multiple product ids,
    missing shop domain, capped page count, duplicate page rows, widget aggregate
    fallback, PDP-vs-widget aggregate mismatch, empty review bodies, non-review
    JSON responses, and media false positives?
12. Does the current code avoid ECR, Cleaning, Judgment, pain/pleasure,
    sentiment, credibility, review-integrity, source-wide scraping, fixture
    admission, validation, readiness, and buyer-proof claims?
13. Are live-smoke residuals represented at the correct layer? In particular,
    is ZGO's aggregate mismatch easy enough for a downstream reader to see even
    though the top-level route residuals are empty?
14. Is the next move correctly bounded: more provider parser/fallback hardening
    and smoke fixtures, not retailer-specific adapters or downstream
    interpretation?

## Findings Standard

Report findings first, ordered by severity. Use these labels for priority only;
they are not formal verdict authority:

- `critical`: defect can create fake row-complete success, hide provider
  mismatch, misrepresent provenance, expose forbidden review bodies, or
  authorize forbidden downstream/source access behavior.
- `major`: defect can materially mislead downstream readers/agents, break core
  rendered+widget success signals, hide material residuals, or leave a high-risk
  test gap before merge.
- `minor`: bounded correctness, documentation, test, or maintainability issue
  that should be considered but does not block the branch by itself.
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

`docs/review-outputs/adversarial-artifact-reviews/fragrance_auto_widget_parsing_adversarial_code_review_v0.md`

The report must include these provenance fields, supplied by the
operator/reviewer or set to `unrecorded` if unavailable:

```yaml
reviewed_by: <operator_supplied_or_unrecorded>
authored_by: <operator_supplied_or_unrecorded; at minimum note b6bbef42 implementation authored by Codex/GPT-family if the operator accepts that provenance>
de_correlation_bar: cross_vendor_discovery | same_vendor_sanity | self_fallback | unrecorded
same_vendor_rationale: <required when de_correlation_bar is same_vendor_sanity>
```

After successful write, return a concise chat summary plus:

```yaml
review_summary:
  status: completed | blocked
  report_path: docs/review-outputs/adversarial-artifact-reviews/fragrance_auto_widget_parsing_adversarial_code_review_v0.md
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
  provider_parser_risk:
    judge_me_auto_fallback: ok | finding | not_assessed
    judge_me_json_rows: ok | finding | not_assessed
    yotpo_v3_rows: ok | finding | not_assessed
    aggregate_mismatch_visibility: ok | finding | not_assessed
    media_visibility: ok | finding | not_assessed
  next_action: <owner/implementer next action>
```

Review-use boundary: findings are decision input only. This review does not
approve, validate, mandate remediation, authorize patches, authorize commits,
authorize source capture, authorize commercial/runtime use, or create ECR,
Cleaning, Judgment, buyer-proof, fixture-admission, or readiness evidence.
