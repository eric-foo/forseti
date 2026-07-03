# Creator Signal Multi-Creator Ranked Scan Default Adversarial Artifact Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Read-only adversarial artifact review prompt for the proposed default
  multi-creator Creator Signal surface: whether it should be a leaderboard-like
  contextual ranked scan table, and what display-contract guardrails must be
  settled before authoring or static projection.
use_when:
  - Commissioning review before writing the multi-creator display contract.
  - Checking whether "leaderboard" language would overclaim beyond the accepted creator profile record and surface contracts.
  - Deciding the next safe material step after the per-creator record contract landed.
authority_boundary: retrieval_only
open_next:
  - docs/prompts/templates/review/adversarial_artifact_review_v0.md
  - orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_record_contract_v0.md
  - orca/product/spines/creator_signal/creator_intelligence_profile_surface_v0.md
  - orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_v0.json
  - docs/workflows/creator_registry_record_contract_handoff_v0.md
stale_if:
  - A later accepted Creator Signal display contract defines multi-creator ranking, shortlist, lead-list, or outreach surfaces.
  - creator_profile_current_record_contract_v0.md changes ranking, comparison, non-observed metric, non_claims, limitations, or source_drill_back obligations.
  - creator_intelligence_profile_surface_v0.md changes first-screen, limitation, missingness, non-claim, or source-drill-back display policy.
```

## Prompt Preflight

```yaml
preflight_defaults: docs/prompts/templates/shared/orca_preflight_defaults_v0.md v0 - constants bound; deltas stated below.
authorization_basis: >
  Current owner instruction: test the assumption that the default customer view
  should be a leaderboard; run the first two gates together; then create a
  delegated review prompt before authoring the multi-creator surface contract.
objective: >
  Review the direction-under-review below before Orca writes a multi-creator
  display contract or static projection.
intended_decision: >
  Decide whether Batch 1 may safely specify the default multi-creator surface
  as a contextual ranked scan table, or whether leaderboard/ranking language
  should be blocked or deferred.
output_mode: review-report
prompt_artifact_path: docs/prompts/reviews/creator_signal_multi_creator_ranked_scan_default_adversarial_artifact_review_prompt_v0.md
report_artifact_path: docs/review-outputs/adversarial-artifact-reviews/creator_signal_multi_creator_ranked_scan_default_adversarial_artifact_review_v0.md
template_kind: adversarial-artifact-review
template_source: docs/prompts/templates/review/adversarial_artifact_review_v0.md
edit_permission: read-only review; reviewer may write only the bound report artifact
target_files_or_dirs:
  - docs/prompts/reviews/creator_signal_multi_creator_ranked_scan_default_adversarial_artifact_review_prompt_v0.md
  - docs/review-outputs/adversarial-artifact-reviews/creator_signal_multi_creator_ranked_scan_default_adversarial_artifact_review_v0.md
  - orca/product/spines/creator_signal/
  - orca/product/spines/capture/core/source_families/social_media/creator_registry/
source_pack: custom_creator_signal_multi_creator_ranked_scan_review
dirty_state_allowance: >
  Before review, the target worktree should be clean except for the prompt under
  review if it is not yet committed. After review, only the bound report path may
  be new or modified.
controlling_source_state: >
  Dispatcher observed this prompt lane at origin/main 41f87dd71c9ac408cc7eb7635b7a9f1cd69b43e3
  before writing the prompt. Reviewer must recheck branch, HEAD, and dirty state
  in their own worktree before strict review claims.
branch_or_commit_reference: >
  Expected source floor is origin/main at or after 41f87dd71c9ac408cc7eb7635b7a9f1cd69b43e3,
  which includes PR #633 "[codex] Pin creator profile current record contract".
doctrine_change_decision: >
  This prompt commissions review only. It does not change product doctrine,
  architecture doctrine, workflow authority, validation philosophy, review
  authority, output authority, or a lifecycle boundary.
isolation_decision: >
  Authored in a fresh worktree off origin/main because the dispatcher root
  worktree was dirty and on another active lane.
validation_gates:
  - Read AGENTS.md and the Orca overlay before review work.
  - Follow Source-Gated Method Contract: REFERENCE-LOAD methods, SOURCE-LOAD task sources, declare SOURCE_CONTEXT_READY or SOURCE_CONTEXT_INCOMPLETE, then APPLY methods.
  - Use findings-first adversarial artifact review output.
  - Write the durable report to the bound report path and verify it with a fresh read before reporting completion.
thread_operating_target_continuity:
  carried_forward: yes
  reason: same_workstream
  changed_from_input: yes
  lifecycle_status: active_thread_local
  if_changed_reason: >
    The upstream per-creator record contract has landed; this prompt continues
    the same registry-to-Creator-Signal workstream at the downstream
    multi-creator display-contract decision.
```

## Workstream Context

The upstream handoff goal was a live, self-sustaining creator-metric registry a
downstream consumer can trust: one current record per creator/account holding
identity, current computed stats, declared-deferred global stats, and
traceable source posture. The per-creator record contract has since landed on
main through PR #633.

The next product-layer question is whether the first multi-creator customer
surface should default to a leaderboard-like ranked scan table.

Do not soften the terminology problem:

- "Leaderboard" is unsafe if it means one universal creator rank, composite
  score, lead-list, outreach queue, or cross-platform aggregate influence.
- A ranked default may be safe if it is a contextual ranked scan table: the rank
  is tied to one eligible observed metric, compatible platform/window/scope, and
  visible posture gates.
- The review should attack whether that distinction is sufficient or whether
  the word "leaderboard" should be blocked until a stronger display contract
  exists.

## Cynefin Route For This Commission

Smallest complete outcome: produce a read-only adversarial artifact review of
the direction-under-review, with a durable report that tells the owner whether
Batch 1 may proceed as a contextual ranked scan table and what must be true
before Batch 2 static projection.

Regime: complicated with a complex-risk edge.

Why: the source contracts are readable and mostly settled, but the product
semantics of ranking can silently overclaim if the surface implies a universal
creator ordering or lead-list.

Decomposition: risk-first, then layer-based. First attack rank semantics and
claim language; then decide what display contract and static projection may
follow.

Current bottleneck: whether the default surface can rank without implying a
global/composite creator score, populated momentum metric, cross-platform
identity proof, buyer proof, or outreach authorization.

Riskiest assumption: a buyer-facing default can look leaderboard-like while
still preserving missingness, limitations, non_claims, source drill-back, and
metric comparability constraints.

Stop or pivot condition: if the only useful customer default is a universal
leaderboard, composite score, lead-list, or outreach workflow, this direction
is unstable and must route to a fuller product/display-contract decision before
projection.

Allowed next move: adversarial review of this direction and its source basis.

Disallowed next move: implementation, dashboarding, new capture, lake writes,
identity-ledger writes, composite scoring, outreach/export design, or
cross-platform aggregate ranking.

## Direction Under Review

```yaml
direction_under_review:
  name: creator_signal_multi_creator_contextual_ranked_scan_default
  batch_1:
    proposed_output: >
      Author a separate Creator Signal multi-creator display contract before
      implementation. The default customer view is a contextual ranked scan
      table, not a universal leaderboard.
    intended_customer_shape: >
      A scan-first table/grid that initially sorts creators by one selected,
      eligible, observed metric such as average_views within compatible
      platform/window/scope, while keeping posture, sample support, freshness,
      and claim-boundary cues visible or immediately reachable.
    forbidden_batch_1_shape:
      - universal creator rank
      - composite creator score
      - cross-platform aggregate influence without promoted linkage and accepted rollup recipe
      - ranking by posting_cadence or recent_velocity while they remain not_attempted
      - ranking non-observed values as zero
      - lead-list, outreach queue, export, or contact authorization
      - buyer proof, validation, readiness, or guaranteed performance
  batch_2:
    proposed_output: >
      After the display contract, produce a static projection over the current
      committed view. Populate existing observed current-window fields from the
      view. For declared-deferred global metrics, carry field names, recipes,
      source-owner links, and not_attempted reasons only; do not imply numeric
      population or formula-ready ranking.
    intended_use: >
      Exercise customer-surface information architecture and row treatment
      before storage engine, dashboard, API, or capture/lake work.
  premise_to_attack: >
    "Default view should be leaderboard-like" is acceptable only if it means
    contextual ranked scan table under explicit comparability and claim guards.
```

## Fused Assumption Gate Snapshot

Use this as input to review; do not treat it as validation or acceptance.

```yaml
assumption_gate:
  status: READY_WITH_VERIFIED_LEDGER
  applies_to: >
    Gate 1 + Gate 2: default multi-creator contextual ranked scan table, then
    static projection over creator_profile_current.
  proceed_premise: >
    "Leaderboard" means contextual ranked scan table. It does not mean universal
    creator ordering, composite score, lead-list, outreach workflow, or
    cross-platform aggregate ranking.
  load_bearing_assumptions:
    - assumption: >
        A ranked default can deliver the customer scanning value without
        implying a universal leaderboard.
      why_load_bearing: >
        If false, writing the display contract around rank bakes in the wrong
        product claim and forces rework.
      verify_by: source_read
      verdict: verified_real_under_proceed_premise
      evidence: >
        Record contract allows only comparisons whose metrics are observed,
        compatible, and visibly qualified; Creator Signal says multi-creator
        ranking needs a separate display contract before implementation.
    - assumption: >
        Current committed rows can exercise a first static projection enough to
        test ranked-scan display rules.
      why_load_bearing: >
        If current rows lack enough observed comparable metrics, Batch 2 would
        become a fake populated leaderboard.
      verify_by: source_read
      verdict: verified_real_for_current_window_metrics
      evidence: >
        Dispatcher observed origin/main 41f87dd7 view summary: 33
        platform_account profiles; 30 YouTube and 3 Instagram; average_views and
        median_views observed for 33; average_like_count and
        average_comment_count observed for 32 and unavailable for 1;
        engagement_rate observed for 31 and unavailable for 2; posting_cadence
        and recent_velocity not_attempted for 33. Reviewer must rederive this
        from the JSON view before relying on it.
    - assumption: >
        Declared-deferred global metrics may be carried as formula/source links
        only without implying they are populated.
      why_load_bearing: >
        If false, the projection would mislead customers into treating
        posting_cadence or recent_velocity as sortable or available.
      verify_by: source_read
      verdict: verified_real_as_a_constraint
      evidence: >
        The record contract states posting_cadence and recent_velocity remain
        not_attempted until Silver-side longitudinal inputs exist; formula or
        field name alone must not imply populated, formula-ready, or zero.
  prerequisites:
    - item: >
        Bind "default ranked scan table" language in the multi-creator display
        contract before building or projecting the surface.
      triage: blocker
      owner: agent
      order: 1
      basis: >
        The existing per-profile contract explicitly does not define
        multi-creator ranking/grid/shortlist/lead-list surfaces.
    - item: >
        Decide whether public/customer copy may say "leaderboard" or must say
        ranked table / ranked scan.
      triage: blocker
      owner: owner
      order: 2
      basis: >
        This is product language and claim posture, not a source fact.
    - item: >
        Static projection over current view after the display contract.
      triage: blocker_for_batch_2
      owner: agent
      order: 3
      basis: >
        Projection before the display contract risks encoding ranking semantics
        by accident.
    - item: composite score, cross-platform aggregate rank, lead-list/outreach/export
      triage: deferrable
      owner: owner
      order: 4
      basis: >
        These require stronger product proof, display rules, identity linkage,
        and/or additional source contracts outside this lane.
```

## Required Method Sequence

REFERENCE-LOAD these method instructions first. Do not APPLY either method yet:

- `workflow-deep-thinking`
- `workflow-adversarial-artifact-review`

Use them only to prepare a neutral source-reading lens. Then SOURCE-LOAD the
task sources below. Declare `SOURCE_CONTEXT_READY` or
`SOURCE_CONTEXT_INCOMPLETE`. Only after that declaration, APPLY
`workflow-deep-thinking` to frame failure modes and decision criteria, then
APPLY `workflow-adversarial-artifact-review` to produce findings.

If `workflow-adversarial-artifact-review` is unavailable, unresolved, or cannot
be applied after source readiness, return a blocked or advisory-only result. Do
not emit strict formal review claims, readiness, validation, mandatory
remediation, patch queues, or executor-ready handoffs.

## Required Authority Reads

Read these before strict review claims:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/artifact-roles.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/validation-gates.md`
- `.agents/workflow-overlay/communication-style.md`
- `.agents/workflow-overlay/template-registry.md`

## Required Task Sources

Read the review target and these source files from the review worktree:

- This prompt, especially `Direction Under Review` and `Fused Assumption Gate Snapshot`.
- `docs/workflows/creator_registry_record_contract_handoff_v0.md`
- `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_record_contract_v0.md`
- `orca/product/spines/creator_signal/creator_intelligence_profile_surface_v0.md`
- `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_spec_v0.md`
- `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_v0.json`
- `orca-harness/capture_spine/creator_profile_current/materialize.py` targeted to update-from-source and profile materialization semantics.
- `orca-harness/capture_spine/creator_profile_current/validation.py` targeted to posture/value coupling, allowed metrics, counts, non-claims, and representativeness limits.
- `docs/review-outputs/adversarial-artifact-reviews/creator_profile_current_record_contract_customer_surface_adversarial_artifact_review_v0.md` targeted to prior review findings and residuals.

Available but not default reads unless a finding depends on them:

- `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_metric_silver_record_contract_v0.md`
- `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_lake_native_record_mapping_v0.md`
- `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_spec_v0.md`
- `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_v0.json`

Do not read or write `F:\orca-data-lake`. Do not run capture, materialization
with `--write`, lake jobs, live browsers, or identity-ledger edits.

## Review Questions To Attack

1. Is a contextual ranked scan table actually the right default, or should the
   first multi-creator surface default to a neutral scan table until ranking
   rules are stronger?
2. If ranking is allowed, what exact semantic boundary must the display contract
   state so rank is contextual, metric-specific, and not a universal creator
   score?
3. Which default sort basis is least misleading from the current data:
   average_views, median_views, engagement_rate, platform-separated tabs, or no
   default sort? Consider observed posture, platform/window compatibility, and
   sample support.
4. How must rows with `unavailable_with_reason`, `not_attempted`,
   `out_of_window`, or `not_applicable` metrics be displayed, excluded, parked,
   or labeled so missing values are not ranked as zero?
5. Does "leaderboard" as customer-facing vocabulary create a forbidden
   implication of winner/loser, buyer proof, performance guarantee, lead-list,
   or outreach priority even if the internal contract is careful?
6. What first-screen cues are required for limitations, missingness, freshness,
   sample support, non_claims, and source drill-back if full details are
   collapsed for scanability?
7. Does Batch 2 static projection have enough current source-backed rows to be
   useful without overclaiming, given the platform split and absent
   creator_record/cross_platform rollups?
8. Are declared-deferred posting_cadence and recent_velocity safe to show as
   formula/source-link-only fields, or should they be hidden from the default
   ranked view until populated?
9. Should the next authoring artifact be a Creator Signal multi-creator display
   contract, a narrower decision record, or something else?

## Findings Contract

Use findings first, ordered by severity. Use these severity labels only as
finding-priority labels: `critical`, `major`, `minor`.

For each finding include:

- severity
- location
- issue
- evidence
- impact
- minimum_closure_condition
- next_authorized_action
- recommended correction or advisory remediation direction

Do not include `patch_queue_entry`. This is a read-only review prompt, not patch
authority.

The detailed report must include a concise recommendation under this field:

```yaml
default_view_recommendation: DEFAULT_CONTEXTUAL_RANKED_SCAN_TABLE | DEFAULT_NEUTRAL_SCAN_TABLE | BLOCK_LEADERBOARD_LANGUAGE | NEEDS_OWNER_DECISION | BLOCKED_SOURCE_INCOMPLETE
```

Interpretation:

- `DEFAULT_CONTEXTUAL_RANKED_SCAN_TABLE`: rank may be the default only under
  explicit contextual/comparability/display guards.
- `DEFAULT_NEUTRAL_SCAN_TABLE`: multi-creator table can proceed, but default
  ranking should be user-selected or deferred.
- `BLOCK_LEADERBOARD_LANGUAGE`: ranking may be technically possible, but the
  "leaderboard" framing itself is too claim-heavy.
- `NEEDS_OWNER_DECISION`: source facts do not decide the product language or
  rank/default tradeoff.
- `BLOCKED_SOURCE_INCOMPLETE`: required source context is missing or
  contradictory.

## Output Contract

Write the durable report to:

`docs/review-outputs/adversarial-artifact-reviews/creator_signal_multi_creator_ranked_scan_default_adversarial_artifact_review_v0.md`

The report must include:

- source-read ledger with `full`, `targeted`, `grep`, or `skip` dispositions;
- `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`;
- review target and purpose;
- fitness reference: the long-term creator registry consumer-trust goal from
  `docs/workflows/creator_registry_record_contract_handoff_v0.md`, plus this
  prompt's intended decision;
- the `default_view_recommendation` enum above;
- findings, if any;
- residual risks and source gaps;
- reviewed_by and authored_by fields, using operator/CA-supplied values or
  `unrecorded`; never fabricate provenance;
- review-use boundary.

After the report is written, verify it with a fresh read and return only the
compact courier YAML shape from `.agents/workflow-overlay/communication-style.md`:

```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/adversarial-artifact-reviews/creator_signal_multi_creator_ranked_scan_default_adversarial_artifact_review_v0.md
  recommendation: accept | accept_with_friction | patch_before_acceptance | reject | blocked
  reviewed_by: unrecorded
  authored_by: unrecorded
  summary: "One sentence describing the review result."
  findings_count: 0
  blocking_findings: []
  advisory_findings: []
  prior_findings_remediated: []
  next_action: "One concrete next step."
```

If the report cannot be written, return the failed chat-only shape required by
`.agents/workflow-overlay/communication-style.md`; do not claim a report path.

## Review-Use Boundary

This review is decision input only. It is not approval, validation, readiness,
buyer proof, mandatory remediation, source-of-truth promotion, implementation
authorization, dashboard authorization, live capture authorization, lake-write
authorization, identity-write authorization, or outreach/lead-list authority.
