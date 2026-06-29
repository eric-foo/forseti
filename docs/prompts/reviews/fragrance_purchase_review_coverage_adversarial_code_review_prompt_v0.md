# Fragrance Purchase-Review Coverage Adversarial Code Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Read-only adversarial implementation/code review prompt for PR #436,
  covering the fragrance purchase-review focused coverage docs plus the local
  no-network coverage runner/helper/tests.
use_when:
  - Dispatching an independent review of PR #436 after the delegated-review-patch request routed out of the single-artifact convention.
  - Checking whether the focused review-coverage implementation preserves MGT success signals without overclaiming source-wide review capture, downstream interpretation, ECR, Cleaning, or Judgment.
authority_boundary: retrieval_only
output_mode: review-report
required_output_path: docs/review-outputs/adversarial-artifact-reviews/fragrance_purchase_review_coverage_adversarial_code_review_v0.md
```

prompt_boundary: prompt_only; review-use boundary stated below

## Commission

Perform a read-only adversarial implementation/code review of PR #436 in:

`C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\fragrance-purchase-review-probes`

This prompt is the route-out from an explicit `workflow-delegated-review-patch`
request. Orca's delegated-review-patch overlay applies to a single high-stakes
authored artifact file. This target is a multi-file implementation/code diff,
so do not force it into that convention and do not patch. Run read-only
adversarial code review with `workflow-deep-thinking` followed by
`workflow-code-review` after source readiness.

The review is decision input only. Do not edit files, create patch queues,
commit, push, run network probes, fetch live retailer pages, move review bodies
into tracked docs, or broaden into product planning. If the operator runs this
with a de-correlated reviewer, record that as review provenance only; it is a
who-constraint / measurement fact, not runtime-model routing or a model
recommendation.

## Fitness Reference

```yaml
fitness_reference:
  goal: >
    Preserve an adaptable, focused review-coverage standard for fragrance
    purchase-review sources, starting with Luckyscent, that gives downstream
    readers useful success signals without becoming an exhaustive review scraper
    or interpretation layer.
  observable_success_signal: >
    The receipt captures enough source-visible review metadata for rating
    balance, recency, length, media, verified status, native ids/candidate keys,
    aggregate rating context, selected/skipped reasons, and residuals while
    keeping skipped bodies out of the reader set and refusing pain/pleasure,
    sentiment, integrity, buyer-proof, ECR, Cleaning, or Judgment labels.
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
    Define and preserve an adaptable focused review-coverage standard for
    fragrance retailers, starting with Luckyscent.
  output_fit_check: >
    Review receipts make downstream reading more decision-useful through rating
    balance, recency, length, media, verified status, native ids, aggregate
    rating, and residuals without substituting exhaustive scraping or downstream
    sentiment/integrity labeling.
```

## Orca Start Preflight

```yaml
orca_start_preflight:
  agents_read: required
  overlay_read: required
  preflight_defaults: docs/prompts/templates/shared/orca_preflight_defaults_v0.md v0 - constants bound; deltas stated below
  authorization_basis: current user invoked workflow-delegated-review-patch after PR #436 implementation was pushed
  source_pack: custom fragrance purchase-review focused coverage implementation review
  output_mode: review-report
  template_kind: review; repo-code-review template not registry-bound, so use Orca prompt-orchestrator fallback with workflow-code-review mechanics
  edit_permission: read-only review; report-write only to required_output_path
  target_scope: PR #436 diff from origin/main through implementation target commit bf39558342ca848736fabb622cef8aac6934c466
  expected_branch: codex/fragrance-purchase-review-probes
  expected_review_target_commit: bf39558342ca848736fabb622cef8aac6934c466
  expected_pr: 436
  dirty_state_checked: required
  dirty_state_allowance: >
    The reviewer should inspect the pinned target files by hash. The prompt
    artifact itself may exist on a later branch commit and is not part of the
    implementation review target unless it changes source authority. Any other
    modified or untracked files are out of scope unless they affect the pinned
    target files or source authority.
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
    - orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_focused_coverage_mgt_v0.md
```

## Required Method Sequence

1. Read `AGENTS.md` and `.agents/workflow-overlay/README.md`.
2. Read `.agents/workflow-overlay/source-of-truth.md`, `.agents/workflow-overlay/source-loading.md`, `.agents/workflow-overlay/delegated-review-patch.md`, `.agents/workflow-overlay/prompt-orchestration.md`, `.agents/workflow-overlay/review-lanes.md`, and `.agents/workflow-overlay/validation-gates.md`.
3. REFERENCE-LOAD `workflow-deep-thinking`.
4. REFERENCE-LOAD `workflow-code-review`.
5. Do not APPLY either method yet.
6. SOURCE-LOAD all required authority, target, support, and validation evidence listed below.
7. Verify every pinned target hash below. If any hash mismatches, stop with `HASH_MISMATCH` and list the mismatched path, expected hash, actual hash, and nearest allowed next step.
8. Declare `SOURCE_CONTEXT_READY` only after the required sources and hashes are loaded. If any required source is missing, declare `SOURCE_CONTEXT_INCOMPLETE` with the gap and do not emit strict review claims.
9. Only after `SOURCE_CONTEXT_READY`, APPLY `workflow-deep-thinking` to frame failure modes and APPLY `workflow-code-review` in adversarial findings-first posture.
10. Write the full durable review report to `docs/review-outputs/adversarial-artifact-reviews/fragrance_purchase_review_coverage_adversarial_code_review_v0.md`.
11. After the report is written, return only a concise chat summary plus the fenced `review_summary` YAML block below.

If `workflow-code-review` is unavailable, unresolved, or cannot be applied, return `BLOCKED_REVIEW_LANE_UNAVAILABLE` and do not substitute a self-review.

## Target Hash Pins

Verify these SHA256 pins before review:

```text
5FF243D15797BAB0A1875FD28D611AD5D50BC624D56CFF939A13FC0B6E0172E1  docs/workflows/data_capture_spine_consolidation_map_v0.md
84F970A774A9362F012B9514EEB51942454D337C11268392B43DE08065222AFA  docs/workflows/orca_repo_map_v0.md
044EE51219D9CABA0641D1501DB8489487748161C7988A112A0B596F9773D7BD  orca-harness/README.md
082B17B3B7A72CDCFB545275DA470A35C45C17D6D586B4C18C5AB0A38433B354  orca-harness/runners/run_fragrance_review_coverage.py
35DC6024E4478840D8DA67C5F55EE482D6A0448EAD7BBDCD71E309F63002AF6A  orca-harness/source_capture/__init__.py
1E905DAA4904F4870F23F47FD6093F85EC6DAA39D0E4CFB81815B85BCE86AFA5  orca-harness/source_capture/fragrance_review_coverage.py
2321EC7DEC30313CCCB09AFE7B91A2055AECBEF5A14D975C5427628E56E1A65A  orca-harness/tests/unit/test_fragrance_review_coverage.py
A908321EE3C48AABC93A2A831B3840A08A8D324999F0725CBF3E542A694B2D39  orca/product/spines/capture/core/source_capture_toolbox/README.md
91BCB7568B51DA2C4759F1D7A0107A3619831C74879D53EFEB3F69238756D040  orca/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md
FA9B490E0FCD1AA6307E0ACD3A6E40FCD360384BCA64471AE9EFA03992BAA6B5  orca/product/spines/capture/core/source_families/retail_pdp/README.md
CEC22AF84772AC411A5930FD239FBB96C14E8418F0F32EABE638B68B1DBB360F  orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_focused_coverage_mgt_v0.md
41C5503B5525FD083D5BA6181FC45610B1FAD0EAB9DEEEEED217CE8520B5AA79  orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_retailer_recon_v0.md
938A0750DA7127DC1CA19D2AF17A5764FAC36949473FF45A81FBE3DEE2B3EAC8  orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_row_capture_pilot_v0.md
E1FB9D8542DF926D36540A0DFF1D8517FFFADBA1F7F5238A680918E9426DD91A  orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_row_contract_v0.md
7EBCCEEC92E0E6076AFCAEBB729F2FD63AB835FDE1A1405827B36AA8919A51E1  orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_site_registry_v0.md
A06BAE29A69D3B82D8E4AD2779935EEF8248E61FF721F31D3EB0CF1D3AE3884F  orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_widget_expansion_probe_v0.md
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
- `orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_focused_coverage_mgt_v0.md`
- `orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_row_contract_v0.md`
- `orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_site_registry_v0.md`
- `orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_widget_expansion_probe_v0.md`
- all target files listed under Target Hash Pins

Available but do not bulk-load by default unless they materially affect a finding:

- prior review outputs under `docs/review-outputs/`
- scratch raw probe files under ignored `orca-harness/_test_runs/`
- unrelated product or Judgment Spine files

## Implementation Summary To Verify

PR #436 is intended to establish a focused fragrance purchase-review lane and a local harness helper:

- registers the fragrance purchase-review source family docs and MGT target;
- pins Luckyscent/Judge.me route behavior and site-registry status;
- defines focused review-row capture as source-visible metadata plus selected reader rows, not all public review bodies;
- adds `source_capture/fragrance_review_coverage.py` to parse saved Judge.me widget JSON/HTML and optional PDP JSON-LD aggregate rating/count without network access;
- preserves row id/native id/candidate key, rating, timestamp/month, length bucket, verified flag, media flag, source-visible badge/product attrs, helpful counts, aggregate companion, selected/skipped ids, route health, and residuals;
- rejects interpretation fields in `source_visible_fields` such as pain, pleasure, sentiment, integrity, credibility, demand, buyer proof, or judgment;
- strips verbatim review body text from skipped/capped rows while preserving body hash, word count, metadata, and skip reasons;
- selects rows according to focused policy: 1-star, 4-star, media-attached, 75+ word, recent low-rating rows, bounded 5-star positives, and 2/3-star controls when recent or long;
- records media diagnostic disagreement when source media filter count is zero but row scan finds review media;
- adds `run_fragrance_review_coverage.py` as a no-network CLI over saved widget/PDP files;
- updates harness exports and discoverability docs;
- adds synthetic Judge.me-style tests for parser, selection, body stripping, forbidden interpretation fields, and runner JSON output.

## Validation Evidence To Inspect

The implementation author observed these commands/results before this prompt was filed:

```text
python -m pytest -p no:cacheprovider -q --tb=short tests/unit/test_retail_pdp_projection.py tests/unit/test_fragrance_review_coverage.py
```

Observed result:

```text
25 passed
```

```text
python -c "from source_capture import build_fragrance_review_coverage, write_fragrance_review_coverage; print(build_fragrance_review_coverage.__name__, write_fragrance_review_coverage.__name__)"
```

Observed result:

```text
build_fragrance_review_coverage write_fragrance_review_coverage
```

```text
git diff --check
```

Observed result: exit 0, no output.

```text
python .agents\hooks\check_repo_map_freshness.py --changed --strict
```

Observed result: exit 0, no output.

Advisory placement check was also run:

```text
python .agents\hooks\check_placement.py --check
```

Observed result: exit 0 with pre-existing root/map warnings plus legacy-tolerated file listings; not a failure of this target.

## Review Questions

Be adversarial about material implementation risks:

1. Does the helper actually preserve the MGT success signals without drifting into source-wide review scraping or downstream interpretation?
2. Can any receipt field imply pain/pleasure, sentiment, review integrity, buyer proof, credibility, demand, ECR, Cleaning, Judgment, validation, readiness, or commercial proof?
3. Is Judge.me HTML parsing robust enough for nested review bodies, void tags, self-closing tags, native ids, rating/date attrs, verified flags, helpful counts, badges, and media containers without misclassifying avatars/generic images as review media?
4. Is media diagnosis honest when widget filter counts and row scans disagree?
5. Does the selection policy match the focused MGT contract, including month-window recency, 4-star importance, bounded 5-star positives, 2/3-star controls, and low-rating fallback when no 1-star rows exist?
6. Does body stripping for skipped/capped rows actually prevent context blowup while retaining enough metadata and hashability for integrity/readback?
7. Are candidate keys stable enough when native ids are absent, and are weaker-key residuals visible where needed?
8. Are aggregate rating/count semantics honest when PDP JSON-LD and widget totals are split or mismatched?
9. Does the runner stay no-network/local-file-only, fail visibly on malformed inputs, and avoid hidden success paths?
10. Are tests strong enough for the highest-risk paths, including 1-star rows, JSON review rows, malformed/missing widgets, aggregate absence, native-id absence, duplicate rows, media false positives/positives, adaptive caps, and interpretation-field rejection?
11. Do the docs and repo maps accurately describe implemented behavior without overclaiming review coverage, storage, fixture admission, source access, or downstream readiness?
12. Is any branch-wide doc introduced by PR #436 stale, contradictory, or out of sync with the code implementation?

## Findings Standard

Report findings first, ordered by severity. Use these labels for priority only; they are not a formal verdict authority:

- `critical`: defect can create fake capture success, preserve or expose raw review bodies where the lane forbids it, silently misrepresent source-visible review data, or authorize forbidden downstream/source access behavior.
- `major`: defect can materially mislead downstream readers/agents, break core MGT success signals, hide material residuals, or leave a high-risk test gap before merge.
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

Do not emit `patch_queue_entry`; this is read-only review. Suggested remediation direction is allowed only as advisory prose, not executor-ready instructions.

## Output Contract

Write the full durable report to:

`docs/review-outputs/adversarial-artifact-reviews/fragrance_purchase_review_coverage_adversarial_code_review_v0.md`

The report must include these provenance fields, supplied by the operator/reviewer or set to `unrecorded` if unavailable:

```yaml
reviewed_by: <operator_supplied_or_unrecorded>
authored_by: <operator_supplied_or_unrecorded; at minimum note bf395583 implementation authored by Codex/GPT-5 if the operator accepts that provenance>
de_correlation_bar: cross_vendor_discovery | same_vendor_sanity | self_fallback | unrecorded
same_vendor_rationale: <required when de_correlation_bar is same_vendor_sanity>
```

After successful write, return a concise chat summary plus:

```yaml
review_summary:
  status: completed | blocked
  report_path: docs/review-outputs/adversarial-artifact-reviews/fragrance_purchase_review_coverage_adversarial_code_review_v0.md
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
  next_action: <owner/implementer next action>
```

Review-use boundary: findings are decision input only. This review does not approve, validate, mandate remediation, authorize patches, authorize commits, authorize source capture, authorize commercial/runtime use, or create ECR, Cleaning, Judgment, buyer-proof, fixture-admission, or readiness evidence.
