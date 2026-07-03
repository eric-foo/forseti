# Creator Signal Multi-Creator Library Surface v0 Adversarial Artifact Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Read-only adversarial artifact review prompt for the newly authored
  multi-creator Creator Signal library display contract: whether it actually
  closes MC-01 through MC-04 from the prior ranked-scan-default review as
  structural rules, whether it correctly inherits the record contract and the
  single-profile Creator Signal surface without weakening them, and whether it
  introduces any new gap.
use_when:
  - Reviewing orca/product/spines/creator_signal/creator_signal_multi_creator_library_surface_v0.md before or after PR #638 merges.
  - Checking whether the multi-creator display contract's structural guards are self-enforcing rather than prose-only.
  - Deciding whether the Step 3 static projection may proceed from this contract as written.
authority_boundary: retrieval_only
open_next:
  - docs/prompts/templates/review/adversarial_artifact_review_v0.md
  - orca/product/spines/creator_signal/creator_signal_multi_creator_library_surface_v0.md
  - docs/review-outputs/adversarial-artifact-reviews/creator_signal_multi_creator_ranked_scan_default_adversarial_artifact_review_v0.md
  - orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_record_contract_v0.md
  - orca/product/spines/creator_signal/creator_intelligence_profile_surface_v0.md
stale_if:
  - A later accepted patch to creator_signal_multi_creator_library_surface_v0.md changes its structural rules, default view name, or non-claims panel.
  - creator_profile_current_record_contract_v0.md or creator_intelligence_profile_surface_v0.md change in a way the library contract has not reconciled with.
  - Step 3 static projection lands and exposes a gap this review did not anticipate.
```

## Prompt Preflight

```yaml
preflight_defaults: docs/prompts/templates/shared/orca_preflight_defaults_v0.md v0 - constants bound; deltas stated below.
authorization_basis: >
  Owner instruction: read and execute the authoring handoff
  docs/prompts/handoffs/creator_signal_multi_creator_library_display_contract_authoring_prompt_v0.md,
  then delegate a review prompt for the drafted contract, per that handoff's
  Completion Contract ("recommend a separate adversarial artifact review
  prompt for the drafted contract after the PR is ready or landed").
objective: >
  Review the newly authored multi-creator Creator Signal library display
  contract for whether it actually closes the four structural guards named by
  the prior ranked-scan-default review, and whether it introduces any new gap.
intended_decision: >
  Decide whether the contract as landed is safe to build a static projection
  or implementation against, or whether it needs a patch first.
output_mode: review-report
prompt_artifact_path: docs/prompts/reviews/creator_signal_multi_creator_library_surface_v0_adversarial_artifact_review_prompt_v0.md
report_artifact_path: docs/review-outputs/adversarial-artifact-reviews/creator_signal_multi_creator_library_surface_v0_adversarial_artifact_review_v0.md
template_kind: adversarial-artifact-review
template_source: docs/prompts/templates/review/adversarial_artifact_review_v0.md
edit_permission: read-only review; reviewer may write only the bound report artifact
target_files_or_dirs:
  - orca/product/spines/creator_signal/creator_signal_multi_creator_library_surface_v0.md
  - docs/review-outputs/adversarial-artifact-reviews/creator_signal_multi_creator_library_surface_v0_adversarial_artifact_review_v0.md
source_pack: custom_creator_signal_multi_creator_library_surface_review
dirty_state_allowance: >
  Before review, the target worktree should be clean except for this prompt if
  it is not yet committed. After review, only the bound report path may be new
  or modified.
controlling_source_state: >
  Dispatcher observed the review target at
  worktrees/multi-creator-library-contract-prompt, branch
  codex/multi-creator-library-contract-prompt, commit 02c2d77e (pushed to
  origin, PR #638 open against main, not yet merged). Reviewer must recheck
  branch, HEAD, dirty state, and merge state in their own worktree before
  strict review claims; if the reviewer works from origin/main and PR #638 has
  not merged, the target file will not resolve there -- check the named branch
  or PR diff instead.
branch_or_commit_reference: >
  codex/multi-creator-library-contract-prompt @ 02c2d77e (PR #638). If merged
  by review time, origin/main will carry the same content; verify via
  `git log --oneline -- orca/product/spines/creator_signal/creator_signal_multi_creator_library_surface_v0.md`.
doctrine_change_decision: >
  This prompt commissions review only. It does not change product doctrine,
  architecture doctrine, workflow authority, validation philosophy, review
  authority, output authority, or a lifecycle boundary.
isolation_decision: >
  Authored in-place in the existing authoring worktree
  (worktrees/multi-creator-library-contract-prompt) alongside the just-landed
  contract commit, since the lane was clean immediately after that commit;
  a reviewer may use the same worktree, a fresh clone of the PR branch, or any
  worktree that can check out codex/multi-creator-library-contract-prompt.
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
    The upstream ranked-scan-default review recommended pinning four
    structural guards before authoring; the contract now exists. This prompt
    continues the same registry-to-Creator-Signal workstream at the
    post-authoring verification decision.
```

## Workstream Context

The per-creator record contract landed via PR #633. The ranked-scan-default
adversarial review (`creator_signal_multi_creator_ranked_scan_default_adversarial_artifact_review_v0.md`)
then recommended `DEFAULT_CONTEXTUAL_RANKED_SCAN_TABLE`, conditional on four
structural guards (MC-01 through MC-04) being pinned as contract rules rather
than prose, plus blocking the literal word "leaderboard" from customer-facing
copy. The authoring handoff
(`docs/prompts/handoffs/creator_signal_multi_creator_library_display_contract_authoring_prompt_v0.md`)
commissioned exactly that contract. It has now been authored at
`orca/product/spines/creator_signal/creator_signal_multi_creator_library_surface_v0.md`
and pushed on PR #638.

This review checks the authored contract against its own commission: did it
actually close MC-01 through MC-04 as structural rules, not merely restate
them as prose in a new document? Does it correctly inherit
`creator_profile_current_record_contract_v0.md`'s Metric Comparison Rules and
posture/value coupling, and `creator_intelligence_profile_surface_v0.md`'s
single-profile claim/limitation/non-claim rules, without narrowing or
contradicting either? Does the Step 3 static-projection handoff boundary it
defines actually match what the current 33-row data posture can support
without inviting overclaim?

Do not treat this as a rubber-stamp confirmation pass. The contract under
review was authored to close a known finding set; the sharper question is
whether the closure is self-enforcing (a structural rule an implementer
cannot easily route around) or whether it re-creates the same "guard in prose,
unenforced against the data shape" problem the prior review found in the
direction it reviewed.

## Cynefin Route For This Commission

Smallest complete outcome: produce a read-only adversarial artifact review of
the authored multi-creator library contract, with a durable report that tells
the owner whether the contract is safe to build Step 3 (static projection) or
any later implementation against, or whether it needs a patch first.

Regime: complicated with a complex-risk edge, same as the prior review this
one follows up.

Why: the review target is a single readable docs artifact and its named source
contracts, but whether its structural language actually forecloses the naive
non-compliant implementation (rather than merely restating the guard) is a
judgment call that must be checked against the same data shape that broke the
guard in the direction under the prior review.

Decomposition: finding-by-finding against MC-01 through MC-04, then a fresh
sweep for any new gap the contract's own new sections (Step 3 boundary,
Forbidden Language, Display Tiers) might introduce.

Current bottleneck: whether the landed contract is fit to authorize Step 3 or
whether MC-01 through MC-04 (or a new finding) still block it.

Riskiest assumption: that naming a rule "structural" in the contract text is
sufficient to make it self-enforcing; the review must check whether the
contract gives an implementer a concrete mechanism (tab, mandatory filter,
required visible cue) rather than another layer of prose guidance.

Stop or pivot condition: if the contract's structural language is itself as
unenforced as the direction the prior review found unsafe, or if closing one
MC finding reopens another (e.g., a platform-tab requirement stated without
saying what happens when a tab has 3 rows vs 30), route back to a contract
patch before Step 3 proceeds.

Allowed next move: adversarial review of the landed contract and its source
basis.

Disallowed next move: implementation, static projection (Step 3), dashboarding,
new capture, lake writes, identity-ledger writes, composite scoring,
outreach/export design, or patching the contract directly from this review
lane.

## Review Target

```yaml
review_target:
  artifact: orca/product/spines/creator_signal/creator_signal_multi_creator_library_surface_v0.md
  authored_by_commission: docs/prompts/handoffs/creator_signal_multi_creator_library_display_contract_authoring_prompt_v0.md
  landed_on: codex/multi-creator-library-contract-prompt @ 02c2d77e (PR #638, open against main)
  prior_review_setting_the_bar: docs/review-outputs/adversarial-artifact-reviews/creator_signal_multi_creator_ranked_scan_default_adversarial_artifact_review_v0.md
  claimed_closures:
    - finding: MC-01
      claim: >
        Default View section states platform-scoped-by-default as a
        structural rule (tabs/sections/mandatory filter), forbids a single
        default list spanning platforms, and forbids mixed-platform global
        rank.
    - finding: MC-02
      claim: >
        Row Model and Sorting Semantics sections require posting_cadence and
        recent_velocity to render a visible "not yet available" state at
        scan-row granularity for every row, and forbid offering them as sort
        keys while not_attempted.
    - finding: MC-03
      claim: >
        Display Tiers section requires the sample-support cue to be
        always-visible (not merely reachable) specifically whenever the
        library is in a sorted state.
    - finding: MC-04
      claim: >
        Non-Claims section requires a reachable non_claims affordance visible
        from the library's first screen, not only inside each opened profile.
  premise_to_attack: >
    Naming a rule "structural" or "required, not merely reachable" in contract
    prose is not the same as making it self-enforcing against a real
    implementation choice. Attack whether each claimed closure above actually
    forecloses the naive non-compliant build the prior review worried about,
    or whether it is the same prose-guard problem restated in the new
    document.
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

- This prompt, especially `Review Target` and `Workstream Context`.
- `orca/product/spines/creator_signal/creator_signal_multi_creator_library_surface_v0.md` (the review target, full read).
- `docs/review-outputs/adversarial-artifact-reviews/creator_signal_multi_creator_ranked_scan_default_adversarial_artifact_review_v0.md` (full read; the finding set MC-01 through MC-04 and NF-1/2/3 this contract must close).
- `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_record_contract_v0.md` (full read; Metric Comparison Rules, posture/value coupling, declared-deferred recipes).
- `orca/product/spines/creator_signal/creator_intelligence_profile_surface_v0.md` (full read; single-profile claim/limitation/non-claim rules this contract must inherit, not narrow).
- `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_v0.json` (targeted structural tabulation of `platform_accounts[].platform`, `metric_rollups.posting_cadence`/`recent_velocity` posture, and `sample_support.sample_adequacy` across all profiles, to reconfirm the Current Data Posture section's counts).
- `docs/prompts/handoffs/creator_signal_multi_creator_library_display_contract_authoring_prompt_v0.md` (targeted; the commission this contract was authored against, including its Contract Requirements and Hard Constraints sections).

Available but not default reads unless a finding depends on them:

- `orca-harness/capture_spine/creator_profile_current/materialize.py`
- `orca-harness/capture_spine/creator_profile_current/validation.py`
- `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_spec_v0.md`

Do not read or write `F:\orca-data-lake`. Do not run capture, materialization
with `--write`, lake jobs, live browsers, or identity-ledger edits. Do not
patch the reviewed contract from this review lane.

## Review Questions To Attack

1. Does the Default View section's platform-scoping rule actually force a
   structural mechanism (tab, section, or mandatory filter) for every
   implementation reading of the contract, or does it leave enough room for
   an implementer to still build one combined sortable list with a platform
   column (the same failure mode MC-01 named against the prior direction)?
2. Does the Row Model / Sorting Semantics treatment of `posting_cadence` and
   `recent_velocity` actually require a visible per-row "not yet available"
   state, or does it only require this "where shown," leaving room for a
   collapsed row to omit the columns entirely (re-opening MC-02)?
3. Is the sample-support cue's "always-visible... whenever the library is in
   a sorted state" language enforceable, or does "sorted state" leave a gap
   for an unranked-but-filtered view to omit the cue while still creating an
   implicit ordering impression?
4. Does the non_claims affordance requirement in Non-Claims / Display Tiers
   actually bind a first-screen-reachable mechanism, or does "reachable"
   remain as under-specified as it was in the surface contract MC-04
   attacked?
5. Does the Static Projection Handoff Boundary (Step 3) section correctly and
   completely list every state Step 3 must not invent, matching this
   contract's own Current Data Posture counts, or did it omit a state (e.g.
   candidate/rejected linkage rows, `identity_state` values other than
   `single_platform_observed`) that current data could actually produce?
6. Does the Forbidden Language section fully close the load-bearing reason
   "leaderboard" was unsafe (MC-04's finding that no non_claims display
   surface existed), or does it only address the word itself while leaving
   the same mechanism gap if an implementer picks a different but equally
   claim-heavy term not literally named "leaderboard"?
7. Does anything in the newly authored contract narrow, contradict, or
   silently relax a rule from `creator_profile_current_record_contract_v0.md`
   (Metric Comparison Rules, posture/value coupling) or
   `creator_intelligence_profile_surface_v0.md` (single-profile claim,
   limitation, non-claim rules) rather than extending it to the multi-row
   case?
8. Is there any rule in the contract that is internally inconsistent (e.g.,
   a Row Model requirement contradicted by a Display Tiers collapsing
   allowance), and if so does it favor the stricter or the looser reading by
   default?
9. Given this contract as written, is the current data (33 rows, 30
   YouTube/3 Instagram, 0 ideal-audience, 0 cross-platform, 2 thin-n/1
   limited-n rows) sufficient for Step 3 to exercise every rule this contract
   states, or does a rule exist that current data cannot actually test
   (analogous to MC-05 for ideal-audience)?

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
contract_closure_recommendation: CLOSES_MC01_MC04_AS_STRUCTURAL | CLOSES_WITH_RESIDUAL_GAPS | PARTIALLY_CLOSES_NEEDS_PATCH | DOES_NOT_CLOSE_REOPEN_PRIOR_FINDINGS | BLOCKED_SOURCE_INCOMPLETE
```

Interpretation:

- `CLOSES_MC01_MC04_AS_STRUCTURAL`: all four claimed closures hold as
  self-enforcing structural rules; Step 3 may proceed once separately
  authorized.
- `CLOSES_WITH_RESIDUAL_GAPS`: the core closures hold, but named minor gaps
  should be patched opportunistically; not blocking for Step 3.
- `PARTIALLY_CLOSES_NEEDS_PATCH`: at least one MC-01 through MC-04 closure is
  not actually structural (still prose-level); recommend a patch before Step 3.
- `DOES_NOT_CLOSE_REOPEN_PRIOR_FINDINGS`: the contract fails to close one or
  more of MC-01 through MC-04 in substance; treat the corresponding prior
  finding as still open.
- `BLOCKED_SOURCE_INCOMPLETE`: required source context is missing or
  contradictory.

## Output Contract

Write the durable report to:

`docs/review-outputs/adversarial-artifact-reviews/creator_signal_multi_creator_library_surface_v0_adversarial_artifact_review_v0.md`

The report must include:

- source-read ledger with `full`, `targeted`, `grep`, or `skip` dispositions;
- `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`;
- review target and purpose;
- fitness reference: the long-term creator registry consumer-trust goal from
  `docs/workflows/creator_registry_record_contract_handoff_v0.md`, plus this
  prompt's intended decision;
- the `contract_closure_recommendation` enum above;
- an explicit disposition for each of MC-01 through MC-04 (closed / partially
  closed / not closed), citing the exact contract section checked;
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
  report_path: docs/review-outputs/adversarial-artifact-reviews/creator_signal_multi_creator_library_surface_v0_adversarial_artifact_review_v0.md
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
