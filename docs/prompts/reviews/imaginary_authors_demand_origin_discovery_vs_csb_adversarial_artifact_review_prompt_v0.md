# Imaginary Authors Demand-Origin Discovery vs CSB Adversarial Artifact Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Filed read-only adversarial artifact review prompt for checking whether the
  Imaginary Authors demand-origin discovery scan is complete enough relative to
  the Commission Signal Board and returned core-satellite CSB scan.
use_when:
  - Commissioning an adversarial review of the fresh Imaginary Authors discovery scan against its CSB obligations.
  - Checking whether the scan's no-candidate closeout is adequately supported without overclaiming absence, demand proof, or capture authority.
  - Deciding whether a patch, rerun, or Capture/community-screening follow-up is needed before using the scan artifact.
authority_boundary: retrieval_only
open_next:
  - docs/research/orca_discovery_candidate_scan_imaginary_authors_demand_origin_discovery_v0.md
  - docs/research/orca_discovery_candidate_scan_imaginary_authors_core_satellite_csb_v0.md
  - docs/research/orca_commission_signal_board_imaginary_authors_forward_v0.md
  - docs/review-outputs/adversarial-artifact-reviews/imaginary_authors_demand_origin_discovery_vs_csb_adversarial_artifact_review_v0.md # nonresolving: expected reviewer output path created by running this prompt
branch_or_commit: review target commit 7d97b759be465a49edc64d89b01abefdf10bc7c0
stale_if:
  - The demand-origin discovery artifact changes after 7d97b759be465a49edc64d89b01abefdf10bc7c0.
  - The CSB board or returned core-satellite CSB scan is superseded.
  - The report destination below is already occupied by a different review.
```

## Prompt Authoring Preflight

```yaml
orchestrator_mode: filed_review_prompt
preflight_defaults: docs/prompts/templates/shared/orca_preflight_defaults_v0.md v0 - constants bound; deltas stated below.
orca_start_preflight:
  agents_read: yes - AGENTS.md supplied in current task context
  overlay_read: yes - .agents/workflow-overlay/README.md read in current task context
  source_pack: custom_scanning_csb_completeness_review
  edit_permission: docs-write for this prompt; downstream reviewer is read-only except report write
  target_scope: Imaginary Authors demand-origin discovery artifact completeness versus CSB board and returned CSB scan
  dirty_state_checked: yes - worktree clean before this prompt file was added
  blocked_if_missing: target artifact, CSB board, returned CSB scan, scanning MGT/scan-core authority, report destination
workspace_path: C:\Users\vmon7\Desktop\projects\orca\worktrees\scanning-fragrance-commission
expected_branch: codex/scanning-csb-first-followup
review_target_commit: 7d97b759be465a49edc64d89b01abefdf10bc7c0
dirty_state_allowance: clean checkout preferred; prompt/report files may be added after the target commit
controlling_source_state: clean at review target commit; prompt file is a later routing artifact
output_mode: review-report
report_destination: docs/review-outputs/adversarial-artifact-reviews/imaginary_authors_demand_origin_discovery_vs_csb_adversarial_artifact_review_v0.md
template_kind: review
template_source: docs/prompts/templates/review/adversarial_artifact_review_v0.md
workflow_sequence_policy: overlay_owned
workflow_sequence_source: active_overlay
workflow_sequence_status: bound
thread_operating_target_continuity:
  carried_forward: no
  reason: no_visible_active_target
  changed_from_input: no
  lifecycle_status: not_applicable
doctrine_change_decision: >
  This prompt commissions a read-only review of a research artifact. It does not
  change product doctrine, workflow authority, review authority, or a lifecycle
  boundary.
non_claims:
  - not review execution
  - not patch authorization
  - not validation
  - not readiness
  - not acceptance of the scan artifact
  - not Capture authorization
```

## Fitness Reference

Goal: the fresh discovery scan should answer the user's follow-up question:
whether the unresolved public buyer-origin / hidden-venue value from the CSB
route was tested completely enough to justify its `no_candidate_after_discovery`
closeout.

Done looks like: a reviewer can compare the scan against the CSB board and
returned CSB scan and either (a) find no blocker/major completeness gaps, or
(b) name exactly which CSB obligation, output-contract field, source-family
question, or overclaim prevents the artifact from being complete enough.

This goal and signal are review axes to attack, not a pass-if-matches bar.

## Paste-Ready Prompt

````markdown
# Adversarial Artifact Review Prompt: Imaginary Authors Demand-Origin Discovery vs CSB

You are performing a **read-only adversarial artifact review** for Orca.

Do not patch files. Do not commit, stage, push, merge, open a PR, run Capture,
run ECR, run Cleaning, run Judgment, contact anyone, or perform a new live scan.
If a fix or rerun is needed, report the finding and the minimum closure condition
only.

## Required Method Sequence

1. REFERENCE-LOAD these method instructions as procedural guidance only:
   - `workflow-deep-thinking`
   - `workflow-adversarial-artifact-review`
2. Do not APPLY either method yet.
3. SOURCE-LOAD the required sources below.
4. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
5. Only after source readiness, APPLY `workflow-deep-thinking` to frame failure
   modes, completeness criteria, and boundary risks.
6. Then APPLY `workflow-adversarial-artifact-review`.

If `workflow-adversarial-artifact-review` is unavailable, unresolved, or cannot
be applied after source readiness, return a blocked or advisory-only result. Do
not emit formal verdicts, validation claims, readiness claims, mandatory
remediation, patch queues, executor-ready handoffs, or alignment-complete claims.

## Review Target

Primary target artifact:

```text
docs/research/orca_discovery_candidate_scan_imaginary_authors_demand_origin_discovery_v0.md
```

Review target commit:

```text
7d97b759be465a49edc64d89b01abefdf10bc7c0
```

Branch:

```text
codex/scanning-csb-first-followup
```

The branch may contain a later commit that adds this review prompt. Do not treat
this prompt as part of the scan under review. The target is the discovery
artifact as of the pinned commit above.

## Required Durable Report

Output mode:

```text
review-report
```

Write the human-readable review report here:

```text
docs/review-outputs/adversarial-artifact-reviews/imaginary_authors_demand_origin_discovery_vs_csb_adversarial_artifact_review_v0.md
```

After the report is written, return only the compact `review_summary` YAML shape
from `.agents/workflow-overlay/communication-style.md` plus a short one-paragraph
human summary if useful.

If the report cannot be written, return `status: failed`,
`review_location: chat_only_current_thread`, and `recommendation: blocked` in the
review_summary shape. Do not use `report_path` for an unwritten report.

## Required Sources

Authority and prompt/review rules:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/artifact-roles.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/validation-gates.md`
- `.agents/workflow-overlay/communication-style.md`
- `.agents/workflow-overlay/retrieval-metadata.md`

Task sources:

- `docs/research/orca_discovery_candidate_scan_imaginary_authors_demand_origin_discovery_v0.md`
- `docs/research/orca_discovery_candidate_scan_imaginary_authors_core_satellite_csb_v0.md`
- `docs/research/orca_commission_signal_board_imaginary_authors_forward_v0.md`
- `orca/product/spines/scanning/README.md`
- `orca/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md`
- `orca/product/spines/scanning/scan_core/orca_demand_scan_core_spec_v0.md`
- `orca/product/spines/foundation/vertical_exploration/orca_vertical_exploration_guide_v0.md` targeted to the Walker Equipment Kit / access-note rules only

Optional targeted sources, only if they materially change a finding:

- `docs/workflows/orca_repo_map_v0.md` for discoverability / map reachability
- prior Imaginary Authors scan artifacts named by the target or returned scan,
  only for anti-repeat or lineage checks; do not treat their observations as
  fresh evidence unless the target reverified them.

Do not perform a new public web scan. You may inspect URLs already cited by the
target only if needed to test a specific source-support or overclaim issue. If
that would become broad source research, stop and report a source-gap finding.

## Review Purpose

Determine whether the fresh demand-origin discovery artifact is complete enough
relative to the CSB board and returned core-satellite CSB scan.

This review is not deciding whether Imaginary Authors is a good candidate. It is
deciding whether the scan artifact did the promised follow-up work well enough:
CSB-first, fresh artifact, demand-origin/hidden-venue focused, no candidate by
implication, capture only as preservation triage, and no demand-proof overclaim.

## Fitness Reference

Goal: the fresh discovery scan should answer whether the unresolved public
buyer-origin / hidden-venue value from the CSB route was tested completely enough
to justify its `no_candidate_after_discovery` closeout.

Done looks like: the review can either find no blocker/major completeness gaps,
or name exactly which CSB obligation, output-contract field, source-family
question, source-support gap, or overclaim prevents the artifact from being
complete enough.

Attack the goal itself: if this is the wrong success bar, report that as a
finding instead of silently using a different bar.

## Completeness Axes To Attack

Check the target artifact against these criteria. Treat these as adversarial
review axes, not a checklist that automatically passes when mentioned.

1. CSB comparison: Does the artifact correctly use the CSB board as a route map,
   and does it disposition the material CSB rows for this follow-up scope,
   especially SBR-005 forums/community, SBR-006 reviews, SBR-007 exact-query
   discovery, and SBR-010 partner/org motion?
2. Returned-scan comparison: Does it carry forward the returned scan's
   load-bearing results, CR-001/CR-002, hidden venue pointer, negatives, access
   notes, and no-candidate baseline without editing, overwriting, or treating
   old observations as fresh unless reverified?
3. Output contract: Does it report the required fields from the implementation
   plan: source_context_status, CSB rows consumed, screening moves used, exact
   queries used, venues tested, hidden venue pointers, observations, negatives,
   access notes, capture_requests, and candidate decision?
4. Demand-origin adequacy: Does it distinguish public buyer-origin evidence from
   owned availability, retailer assortment, review counts, editorial visibility,
   partner/channel motion, and low-stock language? Does the no-candidate closeout
   follow from the scan-core promotion floor?
5. Exact-query adequacy: Are the exact queries targeted enough to close the CSB
   gaps they claim to close? Are no-yield conclusions supported at the right
   strength, or do they overclaim absence from thin search evidence?
6. Retail/review adequacy: Does the artifact correctly handle Ministry of Scent,
   Luckyscent, official review widgets, Anthropologie review counts, and missing
   dated buyer text? Is any retailer count accidentally used as demand-origin
   proof?
7. Access-note adequacy: Does it correctly record Reddit/Basenotes-style venues
   as orchestrator-mediated or access-limited without crossing into scraping,
   capture, or an unearned `blocked` verdict? If no `screening_read` route was
   available, does the artifact say enough to justify stopping?
8. Capture triage: Does it preserve CR-001 and CR-002 as Capture-owned
   preservation options only, without setting a route, asking for ECR/Cleaning/
   Judgment, or treating capture as proof?
9. Boundary control: Does the artifact avoid crawler, monitor, registry, atlas,
   source-class ratification, route binding, candidate admission, demand proof,
   buyer proof, readiness, validation, or client-output language?
10. Freshness and stale-use: Does the artifact make the 2026-06-22 retrieval date
    and 2026-07-13 reverify-after boundary visible enough for future lanes?
11. Source support: Are the artifact's public-source claims and negative claims
    backed by enough URL/query/date evidence for a future reader to understand
    what was actually checked?
12. Operator usefulness: If the artifact is incomplete, is the missing work a
    patch, a bounded rerun, Capture preservation, or orchestrator-mediated
    community screening? Do not prescribe execution; name the next authorized
    action only.

## Severity Guidance

Use `critical`, `major`, and `minor` as finding-priority labels only. They do
not create validation, readiness, acceptance, rejection, or mandatory remediation
authority.

- Critical: a defect that makes the no-candidate / completeness closeout
  materially untrustworthy or smuggles in forbidden authority.
- Major: a missing CSB/source-family/output-contract element, unsupported
  no-yield claim, or boundary leak that should be patched or rerun before the
  artifact is used as routing evidence.
- Minor: wording, discoverability, friction, or optional hardening that improves
  future use but does not invalidate the closeout.

## Required Report Shape

Write findings first, ordered by severity. For each finding include:

- finding id, e.g. `IA-CSB-AR-01`;
- severity;
- phase: `correctness` or `friction`;
- location anchor in the target artifact;
- source evidence from the CSB board, returned CSB scan, scanning README/MGT,
  scan-core, or vertical guide;
- issue;
- strongest defense of the current artifact and why that defense fails;
- impact;
- minimum_closure_condition;
- next_authorized_action;
- whether a patch queue is authorized: `no`.

Do not emit `patch_queue_entry`. Advisory remediation direction is allowed, but
executor-ready how-to is not.

If no blocker or major issues are found, say that clearly and list residual
risks or optional hardening. A no-finding result is not validation, readiness,
proof, acceptance, or candidate admission.

At the top of the report, include the `review_summary` YAML shape from
`.agents/workflow-overlay/communication-style.md` with:

- `status: completed`
- `report_path: docs/review-outputs/adversarial-artifact-reviews/imaginary_authors_demand_origin_discovery_vs_csb_adversarial_artifact_review_v0.md`
- `recommendation: accept | accept_with_friction | patch_before_acceptance | reject | blocked`
- `reviewed_by: unrecorded` unless the operator supplies the reviewer identity
- `authored_by: unrecorded` unless the operator supplies the author identity
- finding ids in `blocking_findings` and `advisory_findings` as appropriate

Recommendation semantics for this review:

- `accept`: no blocker/major completeness gap found; only residual risk remains.
- `accept_with_friction`: no blocker/major gap, but minor friction should be known.
- `patch_before_acceptance`: blocker/major issue exists and can likely be fixed
  by patching the artifact or its map/reference context.
- `reject`: the artifact is structurally the wrong answer to the CSB follow-up
  and should be replaced by a fresh scan artifact rather than patched.
- `blocked`: required source context, output destination, or method invocation is
  unavailable.

## Review-Use Boundary

This is a read-only adversarial review. Findings are decision input only. They
are not approval, validation, product proof, mandatory remediation, patch
authority, candidate admission, Capture authorization, or executor-ready work
unless a separate Orca decision or execution lane accepts them.
````
