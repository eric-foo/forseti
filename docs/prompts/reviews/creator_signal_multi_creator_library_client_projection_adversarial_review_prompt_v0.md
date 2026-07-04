# Creator Signal Multi-Creator Library Client Projection Adversarial Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Read-only delegated adversarial artifact review prompt for the
  client-readable Creator Signal multi-creator library projection v0: whether
  it safely presents the reviewed static projection as a lighter client surface
  without hiding load-bearing trust cues, implying leaderboard semantics,
  outreach priority, buyer proof, or cross-platform ranking.
use_when:
  - Commissioning an independent review before treating the client projection as customer-showable.
  - Checking whether progressive disclosure from client row to audit row preserves limitations, non-claims, and source drill-back.
  - Verifying that the client projection remains a presentation projection over the reviewed static projection, not a new source of truth.
authority_boundary: retrieval_only
open_next:
  - docs/prompts/templates/review/adversarial_artifact_review_v0.md
  - orca/product/spines/creator_signal/creator_signal_multi_creator_library_client_projection_v0.md
  - orca/product/spines/creator_signal/creator_signal_multi_creator_library_static_projection_v0.md
  - orca/product/spines/creator_signal/creator_signal_multi_creator_library_surface_v0.md
  - docs/review-outputs/adversarial-artifact-reviews/creator_signal_multi_creator_library_static_projection_v0_adversarial_artifact_review_v0.md
stale_if:
  - creator_signal_multi_creator_library_client_projection_v0.md changes row fields, copy, audit links, sort framing, or accepted residuals.
  - creator_signal_multi_creator_library_static_projection_v0.md changes row counts, platform mix, metric postures, row order, details anchors, non-claims, or source drill-back structure.
  - A later accepted contract authorizes runtime UI, cross-platform rollups, populated ideal-audience rows, outreach/export use, or populated posting_cadence/recent_velocity.
```

## Prompt Preflight

```yaml
preflight_defaults: docs/prompts/templates/shared/orca_preflight_defaults_v0.md v0 - constants bound; deltas stated below.
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom_creator_signal_client_projection_review
  edit_permission: docs-write for this prompt only; downstream reviewer is read-only except for the bound report artifact
  target_scope: >
    Write a delegated adversarial review prompt for the existing client
    projection artifact. Do not review, patch, implement, dashboard, capture,
    export, or run source/lake/runtime work in this lane.
  dirty_state_checked: yes
  blocked_if_missing: target worktree branch/head/dirty-state check; review target file; report destination binding
authorization_basis: >
  Current owner instruction: "delegate review prompt - just in case" after the
  client-readable projection was created from the reviewed static projection.
objective: >
  Commission an independent read-only adversarial review of the client
  projection's safety as a customer-showable presentation layer over the static
  projection.
intended_decision: >
  Decide whether the client projection can be shown as a lightweight
  pre-client/client-facing preview once the owner chooses to use it, or whether
  it needs a patch before customer use.
fitness_reference: >
  Current workstream goal, stated from the owner discussion: a client can scan
  the current Creator Signal Library without reading every audit detail by
  default, while every row still exposes enough trust posture and a reachable
  audit path to avoid overclaiming source-backed metrics as proof, creator
  standing, outreach priority, or cross-platform ranking.
success_signal: >
  The reviewer can verify that all 33 client rows preserve platform separation,
  visible sample/freshness/deferred-metric cues, client-safe row notes, and
  working audit links, and that the surface does not introduce any claim the
  display contract or static projection did not authorize.
output_mode: review-report
prompt_artifact_path: docs/prompts/reviews/creator_signal_multi_creator_library_client_projection_adversarial_review_prompt_v0.md
report_artifact_path: docs/review-outputs/adversarial-artifact-reviews/creator_signal_multi_creator_library_client_projection_v0_adversarial_artifact_review_v0.md
template_kind: adversarial-artifact-review
template_source: docs/prompts/templates/review/adversarial_artifact_review_v0.md
edit_permission: read-only review; reviewer may write only the bound report artifact
target_files_or_dirs:
  - orca/product/spines/creator_signal/creator_signal_multi_creator_library_client_projection_v0.md
  - docs/review-outputs/adversarial-artifact-reviews/creator_signal_multi_creator_library_client_projection_v0_adversarial_artifact_review_v0.md
source_pack: custom_creator_signal_client_projection_review
dirty_state_allowance: >
  Before review, the target worktree should be clean except for this prompt if
  it has not yet been committed. After review, only the bound report path may be
  new or modified. If the target artifact itself is dirty, stop and ask the
  owner whether to review the dirty artifact or the committed branch.
controlling_source_state: >
  Dispatcher observed the review target at worktrees/creator-signal-client-projection,
  branch codex/creator-signal-client-projection, commit
  737be633049df7cb595cab930b3973e63212f92a. Dispatcher observed a clean target
  scope before writing this prompt. Reviewer must recheck branch, HEAD, dirty
  state, and target/report path state in their own worktree before strict
  review claims.
branch_or_commit_reference: >
  codex/creator-signal-client-projection @
  737be633049df7cb595cab930b3973e63212f92a. The client projection is dependent
  on the reviewed static-projection content in the same branch history; if the
  upstream static projection has merged or been rebased by review time, verify
  content equivalence rather than assuming this commit remains current.
doctrine_change_decision: >
  This prompt commissions review only. It does not change product doctrine,
  architecture doctrine, workflow authority, validation philosophy, review
  authority, output authority, or a lifecycle boundary.
isolation_decision: >
  Authored in the existing clean client-projection worktree because the prompt
  reviews that branch's new artifact and does not require touching the dirty
  dispatcher root worktree.
validation_gates:
  - Read AGENTS.md and the Orca overlay before review work.
  - Follow Source-Gated Method Contract: REFERENCE-LOAD methods, SOURCE-LOAD task sources, declare SOURCE_CONTEXT_READY or SOURCE_CONTEXT_INCOMPLETE, then APPLY methods.
  - Use findings-first adversarial artifact review output.
  - Write the durable report to the bound report path and verify it with a fresh read before reporting completion.
thread_operating_target_continuity:
  carried_forward: no
  reason: no_visible_active_target
  changed_from_input: no
  lifecycle_status: not_applicable
  if_changed_reason:
```

## Delegated Review Boundary

This is a delegated review prompt, not a self-review request.

The review may claim delegated discovery only when the controller is a
different vendor/model lineage from the author/home family. This is a
who-constraint, not a runtime model recommendation. Do not include any
recommended-model language.

```yaml
actor_model_family_receipt_required:
  author_home_model_family: OpenAI / GPT family, per dispatcher provenance for the client projection authoring lane; if the receiver cannot accept that provenance, record authored_by as unrecorded and block de-correlation claims.
  controller_model_family: receiver must fill from its actual runtime provenance
  current_receiving_actor_role: controller
  de_correlation_bar: cross_vendor_discovery
  de_correlation_status: satisfied | blocked
blocked_if:
  - The current receiving actor is the authoring/home model family and would be reviewing its own artifact.
  - The reviewer cannot record a controller family different from the author/home family but still wants to claim delegated discovery.
```

If the receiving actor is same-vendor/same-family, it may not claim delegated
discovery. Return `BLOCKED_CONTROLLER_NOT_DECORRELATED` unless the owner
explicitly downgrades the pass to same-vendor sanity in the launch instruction.

No patch authority is granted. If the reviewer finds a self-closable issue, it
still reports the issue and the minimum closure condition; the home/CA lane
adjudicates and applies any patch separately.

## Workstream Context

The static projection is the audit substrate: it exposes the full row details,
limitations, non-claims, source drill-back pointers, and calculation lineage
for the current 33 committed Creator Signal Library rows.

The client projection is a lighter presentation projection over that substrate.
It is meant to show the customer the useful scan table first, with trust cues
still visible and full audit detail one click away. It must not become a
leaderboard, composite creator score, lead list, outreach queue, buyer proof,
runtime dashboard, API, data-lake write, or new source of truth.

Dispatcher-observed count checks before this prompt was written:

```yaml
observed_counts:
  source_profiles_total: 33
  client_rows: 33
  audit_links: 33
  youtube_rows: 30
  instagram_rows: 3
  client_projection_commit: 737be633049df7cb595cab930b3973e63212f92a
```

The reviewer must rederive these counts from the files before relying on them.

## Cynefin Route For This Commission

Smallest complete outcome: produce a read-only adversarial artifact review of
the client projection, with a durable report that tells the owner whether it is
safe to show as a lightweight client preview or needs a patch first.

Regime: complicated with a complex-risk edge.

Why: the artifact is a single docs projection, but its failure mode is semantic:
making a lighter customer surface can accidentally hide the exact caveats that
made the audit substrate safe.

Decomposition: first attack client-facing claim posture, then row/mechanics
coverage, then audit-link/progressive-disclosure reachability.

Current bottleneck: whether the light client view preserves enough trust posture
for a customer scan without exposing all audit detail by default.

Riskiest assumption: that "one click away" is enough for limitations,
non-claims, source drill-back, and unavailable metric explanation when the
default table is what a customer will scan first.

Stop or pivot condition: if the client projection hides a load-bearing cue in a
way that lets a row be read as creator standing, outreach priority, cross-platform
rank, buyer proof, or channel-wide performance, route to a patch before customer
use.

Allowed next move: delegated adversarial artifact review and durable report.

Disallowed next move: patching this artifact, implementation, dashboarding, new
capture, source/lake writes, identity-ledger edits, cross-platform rollups,
composite scoring, outreach/export design, or customer-proof claims.

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
- `.agents/workflow-overlay/retrieval-metadata.md`

## Required Task Sources

Read these source files from the review worktree:

- This prompt, especially `Delegated Review Boundary`, `Workstream Context`, and `Review Questions To Attack`.
- `orca/product/spines/creator_signal/creator_signal_multi_creator_library_client_projection_v0.md` (the review target, full read).
- `orca/product/spines/creator_signal/creator_signal_multi_creator_library_static_projection_v0.md` (full read or targeted enough to verify row details, non-claims, limitations, source drill-back anchors, and calculation lineage the client projection links to).
- `orca/product/spines/creator_signal/creator_signal_multi_creator_library_surface_v0.md` (full read or targeted enough to verify display-tier, default-view, forbidden-language, and progressive-disclosure obligations).
- `docs/review-outputs/adversarial-artifact-reviews/creator_signal_multi_creator_library_static_projection_v0_adversarial_artifact_review_v0.md` (targeted read for static-projection residuals and accepted patch record).
- `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_v0.json` (targeted structural tabulation of counts, platforms, metric posture, sample support, and source row identity).

Available but not default reads unless a finding depends on them:

- `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_record_contract_v0.md`
- `orca/product/spines/creator_signal/creator_intelligence_profile_surface_v0.md`
- `docs/review-outputs/adversarial-artifact-reviews/creator_signal_multi_creator_library_surface_v0_adversarial_artifact_review_v0.md`
- `docs/review-outputs/adversarial-artifact-reviews/creator_signal_multi_creator_ranked_scan_default_adversarial_artifact_review_v0.md`

Do not read or write `F:\orca-data-lake`. Do not run capture, materialization
with `--write`, lake jobs, live browsers, identity-ledger edits, or customer
exports.

## Review Questions To Attack

1. Does the client projection preserve the static projection's safe structure,
   or does the lighter copy create a new presentation claim not backed by the
   display contract?
2. Is the default table readable as a platform-separated library view, not a
   leaderboard, global creator rank, cross-platform comparison, composite score,
   lead list, or outreach queue?
3. Are the visible trust cues sufficient on every row: platform, subject id,
   average views, engagement posture, sample support, freshness,
   cadence/velocity unavailability, client-safe note, and audit link?
4. Is "Client-safe note" itself safe language, or does it imply the row is
   approved for client action beyond the source-backed scan?
5. Are limitations, non-claims, calculation lineage, and source drill-back
   genuinely reachable from every row through the audit links, and do the links
   resolve to existing detail anchors?
6. Does the surface handle the two engagement-unavailable rows and every
   posting_cadence/recent_velocity not-attempted row without implying zero,
   absence of activity, or lower creator quality?
7. Does the "What This Does Not Prove" section appear early and concrete enough
   for a customer-facing preview, or is it too easy for a customer to consume
   the table while missing non-claims?
8. Does any copy suggest buyer readiness, audience fit, creator quality,
   representative channel-wide performance, guaranteed performance, or outreach
   priority?
9. Does the accepted residuals section accurately preserve the current source
   limits without turning them into internal-only caveats hidden from the
   customer's likely path?
10. Is there any row-count, platform-count, row-order, metric-format, audit-link,
    or anchor mismatch between the client projection, static projection, and
    source JSON?

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

Do not include `patch_queue_entry`. This is a read-only review prompt, not
patch authority.

The detailed report must include a concise recommendation under this field:

```yaml
client_projection_recommendation: CLIENT_PROJECTION_ACCEPT | CLIENT_PROJECTION_ACCEPT_WITH_FRICTION | CLIENT_PROJECTION_PATCH_BEFORE_CUSTOMER_USE | CLIENT_PROJECTION_REJECT_AS_OVERCLAIM | BLOCKED_SOURCE_INCOMPLETE
```

Interpretation:

- `CLIENT_PROJECTION_ACCEPT`: no material blockers or major gaps; residuals are
  already named and acceptable for a customer-showable preview.
- `CLIENT_PROJECTION_ACCEPT_WITH_FRICTION`: no blocker, but named caveats should
  travel with owner use or be patched opportunistically.
- `CLIENT_PROJECTION_PATCH_BEFORE_CUSTOMER_USE`: at least one material claim,
  visibility, link, row, or progressive-disclosure issue should be patched before
  showing to a customer.
- `CLIENT_PROJECTION_REJECT_AS_OVERCLAIM`: the artifact's client-facing posture
  cannot be made safe without rethinking the presentation structure.
- `BLOCKED_SOURCE_INCOMPLETE`: required source context is missing,
  contradictory, dirty in a disallowed way, or not accessible.

## Output Contract

Write the durable report to:

`docs/review-outputs/adversarial-artifact-reviews/creator_signal_multi_creator_library_client_projection_v0_adversarial_artifact_review_v0.md`

The report must include:

- source-read ledger with `full`, `targeted`, `grep`, or `skip` dispositions;
- `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`;
- review target and purpose;
- actor/model-family receipt and de-correlation status;
- fitness reference and success signal from this prompt;
- the `client_projection_recommendation` enum above;
- row/link/count verification results, including source row count, client row count, audit link count, YouTube row count, and Instagram row count;
- findings, if any;
- residual risks and source gaps;
- reviewed_by and authored_by fields, using operator/CA-supplied values or `unrecorded`; never fabricate provenance;
- review-use boundary.

After the report is written, verify it with a fresh read and return only the
compact courier YAML shape from `.agents/workflow-overlay/communication-style.md`:

```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/adversarial-artifact-reviews/creator_signal_multi_creator_library_client_projection_v0_adversarial_artifact_review_v0.md
  recommendation: accept | accept_with_friction | patch_before_acceptance | reject | blocked
  reviewed_by: unrecorded
  authored_by: unrecorded
  summary: "One sentence describing the review result."
  findings_count: 0
  blocking_findings: []
  advisory_findings: []
  prior_findings_remediated: []
  next_action: "If material issues remain, route the smallest closure first; if clean, land/admin next plus 1-5 material moves or explicit none."
```

If the report cannot be written, return the failed chat-only shape required by
`.agents/workflow-overlay/communication-style.md`; do not claim a report path.

## Review-Use Boundary

This review is decision input only. It is not approval, validation, readiness,
buyer proof, mandatory remediation, source-of-truth promotion, implementation
authorization, dashboard authorization, live capture authorization, lake-write
authorization, identity-write authorization, or outreach/lead-list authority.
