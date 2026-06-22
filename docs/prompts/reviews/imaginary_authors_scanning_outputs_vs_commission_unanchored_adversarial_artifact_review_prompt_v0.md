# Imaginary Authors Scanning Outputs vs Commission Unanchored Adversarial Artifact Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Filed paste-ready read-only adversarial artifact review prompt for an
  unanchored reviewer to compare both Imaginary Authors scanning outputs against
  the CSB-first discovery commission and scanning-source obligations.
use_when:
  - Commissioning an unanchored review of the first discovery output and buyer-language rerun together.
  - Checking whether either output, or the two-output state, satisfies the owner commission without overclaiming demand proof, Capture authority, or candidate readiness.
  - Deciding whether the rerun resolves the earlier scan gap, creates a new overcorrection, or leaves a bounded rerun/patch need.
authority_boundary: retrieval_only
open_next:
  - docs/research/orca_commission_signal_board_imaginary_authors_forward_v0.md
  - docs/research/orca_discovery_candidate_scan_imaginary_authors_core_satellite_csb_v0.md
  - docs/research/orca_discovery_candidate_scan_imaginary_authors_demand_origin_discovery_v0.md
  - docs/research/orca_discovery_candidate_scan_imaginary_authors_buyer_language_rerun_v0.md
  - orca/product/spines/scanning/README.md
  - orca/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md
  - orca/product/spines/scanning/scan_core/orca_demand_scan_core_spec_v0.md
branch_or_commit: review target artifacts at 18ff46bcccb8555a968be5feceef5072cc377632 on codex/scanning-ia-buyer-language-rerun
stale_if:
  - Either reviewed scan output changes after 18ff46bcccb8555a968be5feceef5072cc377632.
  - The CSB board, returned core-satellite CSB scan, or scanning MGT/scan-core sources are superseded.
  - The owner changes the commission from CSB-first venue/hidden-venue discovery to candidate execution, Capture, ECR, Cleaning, or Judgment.
```

## Prompt Authoring Preflight

```yaml
orchestrator_mode: filed_review_prompt_plus_paste_ready_copy
preflight_defaults: docs/prompts/templates/shared/orca_preflight_defaults_v0.md v0 - constants bound; deltas stated below.
orca_start_preflight:
  agents_read: yes - AGENTS.md supplied in current task context
  overlay_read: yes - .agents/workflow-overlay/README.md read in current task context
  source_pack: custom_scanning_outputs_vs_commission_unanchored_review
  edit_permission: docs-write for this prompt; downstream reviewer is read-only
  target_scope: compare two Imaginary Authors scanning outputs against the CSB-first commission and scanning obligations
  dirty_state_checked: yes - scanning worktree checked; unrelated untracked prior review output is excluded from this prompt and from staging
  blocked_if_missing: commission/CSB sources, both scan outputs, scanning README/MGT/scan-core, output-mode boundary
workspace_path: C:\Users\vmon7\Desktop\projects\orca\worktrees\scanning-fragrance-commission
expected_branch: codex/scanning-ia-buyer-language-rerun
review_target_artifacts_commit: 18ff46bcccb8555a968be5feceef5072cc377632
dirty_state_allowance: prompt file may be added; ignore unrelated untracked review outputs unless the current user separately supplies them as review sources
controlling_source_state: target artifacts clean at review target commit; prior untracked review report intentionally excluded to preserve unanchored comparison
output_mode: paste-ready-chat
downstream_report_destination: none - reviewer returns chat-only/advisory comparison unless separately given repo write authority
template_kind: review
template_source: docs/prompts/templates/review/adversarial_artifact_review_v0.md
workflow_sequence_policy: overlay_owned
workflow_sequence_source: active_overlay plus current user instruction
workflow_sequence_status: bound
thread_operating_target_continuity:
  carried_forward: no
  reason: no_visible_active_target
  changed_from_input: no
  lifecycle_status: not_applicable
doctrine_change_decision: >
  This prompt commissions a read-only comparison review. It does not change
  product doctrine, architecture doctrine, workflow authority, validation
  philosophy, review authority, output authority, or a lifecycle boundary.
non_claims:
  - not review execution
  - not patch authorization
  - not validation
  - not readiness
  - not acceptance of either scan output
  - not candidate admission
  - not Capture authorization
```

## Fitness Reference

Goal: an unanchored reviewer should determine whether the two scanning outputs
actually answer the owner commission: start from CSB, test unresolved public
venue value / hidden venue value, preserve Capture as preservation-only, and
only promote a candidate when scan-core demand-origin rules are met.

Done looks like: the reviewer can say, with source citations, whether output A,
output B, or the combined two-output state is complete enough for CA
adjudication, and exactly what remains patch/rerun-worthy if not.

This goal and signal are review axes to attack, not a pass-if-matches bar.

## Paste-Ready Prompt

````markdown
# Unanchored Adversarial Artifact Review: Imaginary Authors Scanning Outputs vs Commission

You are performing a **read-only unanchored adversarial artifact review** for
Orca.

Your job is to compare two scanning outputs against the original commission and
CSB/scanning obligations. Do not accept prior agent summaries, PR descriptions,
chat conclusions, or review reports as evidence. Start from the named sources.

Do not patch files. Do not commit, stage, push, merge, open a PR, run Capture,
run ECR, run Cleaning, run Judgment, contact anyone, or perform a new live scan.
If a fix or rerun is needed, report the finding and the minimum closure condition
only.

## Access Gate

If you have repo/filesystem access, open the required files and cite file/line
or stable section anchors for every load-bearing claim.

If you do not have repo/filesystem access, stop and request a source capsule or
pasted copies of the required sources. Do not review from memory, summaries, or
chat claims.

## Required Method Sequence

1. REFERENCE-LOAD these method instructions as procedural guidance only:
   - `workflow-deep-thinking`
   - `workflow-adversarial-artifact-review`
2. Do not APPLY either method yet.
3. SOURCE-LOAD the required sources below.
4. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
5. Only after source readiness, APPLY `workflow-deep-thinking` to frame failure
   modes, commission-fit criteria, and boundary risks.
6. Then APPLY `workflow-adversarial-artifact-review`.

If those local skills are unavailable, state `METHOD_UNAVAILABLE` and continue
only as advisory source-backed critique. Do not emit strict review claims,
validation claims, readiness claims, mandatory remediation, patch queues,
executor-ready handoffs, or alignment-complete claims.

## Required Sources

Authority and prompt/review rules:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/artifact-roles.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/validation-gates.md`
- `.agents/workflow-overlay/communication-style.md`

Commission and CSB/scanning sources:

- `docs/research/orca_commission_signal_board_imaginary_authors_forward_v0.md`
- `docs/research/orca_discovery_candidate_scan_imaginary_authors_core_satellite_csb_v0.md`
- `orca/product/spines/scanning/README.md`
- `orca/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md`
- `orca/product/spines/scanning/scan_core/orca_demand_scan_core_spec_v0.md`
- `orca/product/spines/foundation/vertical_exploration/orca_vertical_exploration_guide_v0.md` targeted to Walker Equipment Kit / public-source and access-note boundaries only

Reviewed outputs:

- Output A: `docs/research/orca_discovery_candidate_scan_imaginary_authors_demand_origin_discovery_v0.md`
- Output B: `docs/research/orca_discovery_candidate_scan_imaginary_authors_buyer_language_rerun_v0.md`

Excluded by default:

- Prior adversarial review reports.
- PR descriptions, branch summaries, chat summaries, or agent closeouts.
- Public web reruns or new URL checks.

Use excluded sources only if the current user explicitly supplies them as review
inputs. If you need a new public source check to resolve a finding, report that
as a rerun need instead of performing the scan.

## Owner Commission Capsule

Treat this as user-stated commission context to compare against the repo sources,
not as a substitute for reading the files.

The owner wanted the next discovery pass to start from the returned CSB-first
scan and answer the unresolved value question: whether any public venue exposes
independent demand-origin signal or hidden venue value that CSB did not already
surface.

The requested work was:

- route Capture only for preservation of volatile official/partner pages, not as
  proof or candidate promotion;
- probe public buyer-origin venues for `A Little Secret`, `Dipped in Chocolate`,
  and `First Peach of the Season`;
- prioritize dated review text, forum/community language, stockout/restock
  discussion, and buyer behavior;
- treat counts alone, owned availability, retailer assortment, editorial
  visibility, and partner/channel motion as insufficient for demand proof;
- recheck retailer review venues only when they expose dated buyer language;
- verify partner/channel pointers as org-motion/channel evidence unless they
  expose buyer-origin behavior;
- fold exact-query discovery into scanning with a small cap for CSB gaps;
- create a fresh artifact rather than updating the returned scan;
- keep precursor language limited to venues that route discovery;
- choose closeout from `candidate_ready_for_next_lane`,
  `capture_preservation_only`, or `no_candidate_after_discovery`.

## Review Questions

Answer these directly before detailed findings:

1. Did Output A satisfy the commission by itself?
2. Did Output B satisfy the commission by itself?
3. Do Output A and Output B together create a coherent CA-usable state, or do
   they conflict / leave an unresolved ambiguity?
4. Did Output B legitimately resolve a missing venue-value rung from Output A,
   or did it overcorrect into candidate promotion from a thin single venue?
5. What is the next authorized action: accept as CA input, patch wording, bounded
   rerun, Capture preservation, or blocked?

## Review Axes To Attack

Use these as adversarial axes. Do not pass an output merely because it mentions a
term.

1. CSB-first discipline: Does each output start from the CSB/returned scan rather
   than inventing a generic scan route?
2. Venue-value focus: Does each output evaluate public venue value and hidden
   venue value, or does it collapse too quickly into candidate hunting?
3. Buyer-origin standard: Does each output distinguish dated buyer-language and
   costly behavior from counts, availability, assortment, editorial visibility,
   owned motion, and partner/channel evidence?
4. Exact-query adequacy: Were exact queries targeted to CSB gaps, and are
   no-yield claims phrased at the right strength?
5. Missing venue rungs: Did either output miss cheap public venues named or
   implied by the CSB route, especially specialist fragrance communities such as
   Parfumo/Basenotes/Fragrantica and public retailer review surfaces?
6. Rerun integrity: Did Output B remain a fresh rerun rather than silently
   updating or overwriting Output A? Does it preserve what Output A already
   settled?
7. Candidate promotion: If Output B emits candidate entries, does that comply
   with scan-core promotion rules? Is the `hold_low_commitment` ceiling clear
   enough, or is there an overclaim from one venue family?
8. Capture boundary: Are capture_requests preservation-only and Capture-owned?
   Is there any route binding, packet commitment, ECR/Cleaning/Judgment leakage,
   or proof-by-Capture language?
9. Precursor boundary: Is precursor language limited to routing venues, not used
   as proof or candidate support?
10. Negative/access-note integrity: Are Basenotes/Fragrantica/Reddit/access-limited
    outcomes recorded as access notes or bounded negatives without global absence
    overclaims?
11. Freshness and stale-use: Are retrieval dates and reverify-after boundaries
    visible enough for future use?
12. Combined-state clarity: Can a future CA tell what changed from Output A to
    Output B, what Output B supersedes, and what still remains unproven?

## Severity Guidance

Use `critical`, `major`, and `minor` as finding-priority labels only. They do
not create validation, readiness, acceptance, rejection, or mandatory remediation
authority.

- Critical: a defect that makes the combined scan state materially untrustworthy
  or smuggles in forbidden authority.
- Major: a missing commission obligation, missed cheap venue rung, unsupported
  candidate/no-candidate closeout, source-support gap, or boundary leak that
  should be patched or rerun before CA relies on the output.
- Minor: wording, discoverability, friction, or optional hardening that improves
  future use but does not invalidate the comparison.

## Output Contract

Return chat-only. Start with this YAML shape:

```yaml
review_summary:
  status: completed | blocked | advisory_only
  recommendation: accept_as_ca_input | patch_before_ca_use | bounded_rerun_required | capture_preservation_only | blocked
  reviewed_by: unrecorded
  authored_by: unrecorded
  source_context: SOURCE_CONTEXT_READY | SOURCE_CONTEXT_INCOMPLETE
  output_a_result: complete | incomplete | overclaiming | blocked | not_reviewed
  output_b_result: complete | incomplete | overclaiming | blocked | not_reviewed
  combined_state_result: coherent | coherent_with_friction | conflicting | blocked
  findings_count: 0
  blocking_findings: []
  advisory_findings: []
  next_action: "One concrete next step."
```

Then provide findings first, ordered by severity. For each finding include:

- finding id, e.g. `IA-COMP-AR-01`;
- severity;
- target: `Output A`, `Output B`, `combined_state`, or `commission_fit`;
- location anchor;
- source evidence;
- issue;
- strongest defense of the current output and why that defense fails;
- impact;
- minimum_closure_condition;
- next_authorized_action;
- patch_queue_authorized: `no`.

Do not emit `patch_queue_entry`. Advisory remediation direction is allowed, but
executor-ready how-to is not.

If no blocker or major issues are found, say that clearly and list residual
risks or optional hardening. A no-finding result is not validation, readiness,
proof, acceptance, candidate admission, or Capture authorization.

## Review-Use Boundary

This is a read-only unanchored adversarial comparison. Findings are decision
input only. They are not approval, validation, product proof, mandatory
remediation, patch authority, candidate admission, Capture authorization, or
executor-ready work unless a separate Orca decision or execution lane accepts
them.
````