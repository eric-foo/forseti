# Canoo Walmart Source Packet Safety Adversarial Artifact Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: Read-only adversarial artifact review prompt for the Canoo/Walmart source packet and safety receipt before participant-packet authoring.
use_when:
  - Reviewing whether the Canoo/Walmart source packet can safely feed a zero-spoiler participant packet.
  - Checking leakage, cutoff discipline, over-priming, source sufficiency, and claim discipline before blind judgment work.
  - Preserving the Step A plumbing-only boundary while moving to the next judgment-quality case track.
authority_boundary: retrieval_only
open_next:
  - docs/research/judgment-spine/cases/canoo-walmart/source_packet_v0.md
  - docs/research/judgment-spine/cases/canoo-walmart/safety_receipt_v0.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/review-lanes.md
input_hashes:
  source_packet_v0.md: 6E2BC0894A36C08B0712C8FE045DF812D3A8857E525CA4412832866FF405E473
  safety_receipt_v0.md: 284CB7EE77AF1D9F2325317528DC0E1404AD2978AE99B10D8FBB3722BE5B9A67
branch_or_commit: main @ a2aebdd8e04c627c5102e79eb324b24b3de35226
stale_if:
  - Either target input hash changes.
  - The reviewer cannot access the pinned Orca workspace or target files.
  - A participant packet is created before this review is written.
```

You are performing a read-only adversarial artifact review for Orca.

## Commission

Review the current Canoo/Walmart source-packet safety state before any participant packet is authored.

The only gate this review may inform is whether the Canoo/Walmart source packet and safety receipt are safe enough, as decision input, to proceed to `participant_packet_v0.md` authoring under zero-spoiler discipline.

This review must not judge the actual Canoo/Walmart decision, score the case, validate the Judgment Spine, validate Step A judgment quality, or treat TR/Casetext as judgment-quality evidence.

Required boundary: plumbing works only; not judgment quality.

## Prompt Artifact And Output Binding

Prompt artifact path:

`docs/prompts/reviews/canoo_walmart_source_packet_safety_adversarial_artifact_review_prompt_v0.md`

Required output mode:

`review-report`

Required durable report path:

`docs/review-outputs/adversarial-artifact-reviews/canoo_walmart_source_packet_safety_adversarial_artifact_review_v0.md`

If the report cannot be written to that path, do not continue in chat as a substitute. Return the failed `review_summary` shape from `.agents/workflow-overlay/communication-style.md` with `status: failed`, `review_location: chat_only_current_thread`, and `recommendation: blocked`.

Edit permission:

`read-only`

Do not edit any target artifact. Do not create `participant_packet_v0.md`. Do not emit `patch_queue_entry`. Do not apply patches, stage files, commit, push, install, run implementation, or create automation.

## Repository Preflight

Use this worktree if accessible:

`C:\Users\vmon7\Desktop\projects\orca`

Expected branch and revision when this prompt was written:

```yaml
expected_branch: main
expected_head: a2aebdd8e04c627c5102e79eb324b24b3de35226
dirty_state_allowance: current dirty and untracked Orca docs are in scope for this review only
untracked_target_files_in_scope: yes
strict_readiness_claims_allowed: no
```

Do not create, clone, request, or switch to a different worktree. If launched elsewhere, change directory to the pinned worktree when accessible. If the pinned worktree or target files are inaccessible, return `SOURCE_CONTEXT_INCOMPLETE` and a blocked review summary rather than reviewing a substitute checkout.

Target input hashes:

```yaml
source_packet_v0.md: 6E2BC0894A36C08B0712C8FE045DF812D3A8857E525CA4412832866FF405E473
safety_receipt_v0.md: 284CB7EE77AF1D9F2325317528DC0E1404AD2978AE99B10D8FBB3722BE5B9A67
```

If either target hash differs, stop before full review and report stale or mismatched state unless the current user instruction explicitly accepts reviewing the changed files.

## Orca Start Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S1 plus Canoo/Walmart source packet, safety receipt, and product-proof zero-spoiler rules
  edit_permission: read-only
  target_scope: Adversarially review the Canoo/Walmart source packet and safety receipt before participant-packet authoring.
  dirty_state_checked: yes
  blocked_if_missing: AGENTS.md, overlay README, source-of-truth, source-loading, review-lanes, prompt-orchestration, communication-style, validation-gates, product-proof, target files, or required report path
```

This prompt does not change product doctrine, architecture doctrine, workflow authority, validation philosophy, review authority, output authority, or lifecycle boundaries. If you find that review execution would require changing any of those, block and name the needed owner decision.

## Source Hierarchy

Use this authority order:

1. Current user instruction for the review run.
2. `AGENTS.md`.
3. `.agents/workflow-overlay/README.md`.
4. Orca overlay files under `.agents/workflow-overlay/`.
5. Orca docs under `docs/`, when they do not conflict with the overlay.
6. Reusable workflow methods only as mechanics after source readiness.

`jb` rules, paths, lifecycle mechanics, product policy, validation habits, and handoffs are not Orca authority. Wrong-lane Reddit or attention-lens material is excluded unless a separate Orca decision explicitly adjudicates it into scope.

## Required Authority Reads

Read these first:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/artifact-roles.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/communication-style.md`
- `.agents/workflow-overlay/validation-gates.md`
- `.agents/workflow-overlay/retrieval-metadata.md`
- `.agents/workflow-overlay/product-proof.md`
- `.agents/workflow-overlay/safety-rules.md`

Then read the review targets:

- `docs/research/judgment-spine/cases/canoo-walmart/source_packet_v0.md`
- `docs/research/judgment-spine/cases/canoo-walmart/safety_receipt_v0.md`

Optional orientation only, not review targets:

- `docs/research/judgment-spine/cases/canoo-walmart/case_track_preflight_v0.md`
- `docs/research/judgment-spine/cases/canoo-walmart/case_index.md`
- `docs/research/judgment-spine/manifest_v0.md`

Do not widen to public web research, post-cutoff research, review-output history, Reddit material, attention-lens material, TR/Casetext reasoning, or all Judgment Spine files. If a source-sufficiency question cannot be answered from the target artifacts and allowed orientation files, record that as a source gap or `not proven`.

## Source-Gated Method Contract

REFERENCE-LOAD these method instructions before source loading. Do not APPLY them yet:

- `workflow-deep-thinking`
- `workflow-adversarial-artifact-review`

Before `SOURCE_CONTEXT_READY`, use those methods only to prepare neutral source-reading questions and failure-mode checklists. Do not produce findings, recommendations, verdicts, rankings, or conclusions before source readiness.

After authority and target sources are loaded, declare exactly one:

```yaml
source_context: SOURCE_CONTEXT_READY
```

or:

```yaml
source_context: SOURCE_CONTEXT_INCOMPLETE
missing_sources:
  - path or source
source_gaps:
  - gap
excluded_sources:
  - excluded source and reason
conflicts:
  - conflict
```

Only after that declaration may you APPLY `workflow-deep-thinking` to frame the boundary problem, failure modes, and decision criteria. Then APPLY `workflow-adversarial-artifact-review` to produce findings.

If `workflow-adversarial-artifact-review` is unavailable, unresolved, or not applied after `SOURCE_CONTEXT_READY`, return only a blocked or advisory-only result. Do not emit formal verdicts, severity authority, blocked/ready status, validation claims, readiness claims, mandatory remediation, patch queues, executor-ready handoffs, or alignment-complete claims.

## Review Target

Primary targets:

- `docs/research/judgment-spine/cases/canoo-walmart/source_packet_v0.md`
- `docs/research/judgment-spine/cases/canoo-walmart/safety_receipt_v0.md`

Review purpose:

- Detect leakage of actual public action, agreement terms, implementation path, post-cutoff facts, bankruptcy/liquidation, outcome, result quality, or source titles/URLs/snippets/filenames that reveal those.
- Detect over-priming toward a predetermined answer, especially overweighting liquidity risk or an alternative-supplier benchmark.
- Test whether the pre-cutoff source substrate is sufficient to reconstruct retailer demand, supplier promise, supplier risk, alternatives, and decision uncertainty without post-cutoff material.
- Check whether any source classes are missing before participant-packet authoring.
- Check that the source packet and safety receipt preserve the Step A boundary: plumbing works only; not judgment quality.
- Check that TR/Casetext remains quarantined and plumbing-grade only.

## Decision Criteria

Treat these as material failure modes:

- A participant-facing packet built from the target artifacts would reveal or strongly imply the actual action, later outcome, post-cutoff facts, or later case result.
- Source labels, URLs, snippets, filenames, or titles would leak the answer even if the prose avoids it.
- The packet makes the blind judgment too easy by turning the case into a single-factor liquidity-risk exercise.
- The packet makes the blind judgment too easy by over-weighting an alternative supplier as obviously superior.
- The packet omits a source class needed to preserve genuine decision uncertainty before participant-packet authoring.
- The artifacts confuse source-packet safety, harness plumbing, or duplicate protection with Judgment Spine validation.
- The artifacts allow the dirty or untracked workspace state to be silently upgraded into readiness, acceptance, validation, or source-of-truth status.

Severity labels are finding-priority labels only:

- `critical`: a leak, contamination, or overclaim that would make participant-packet authoring unsafe without correction or owner risk acceptance.
- `major`: a material source, priming, or claim-discipline defect that could distort blind judgment or downstream routing.
- `minor`: a clarity, retrieval, or hygiene defect that should be fixed but does not by itself block a bounded next step.

These labels do not create approval, rejection, validation, readiness, mandatory remediation, or patch authority.

## Required Report Shape

Write the durable report to:

`docs/review-outputs/adversarial-artifact-reviews/canoo_walmart_source_packet_safety_adversarial_artifact_review_v0.md`

The report must include:

1. The compact `review_summary` YAML shape from `.agents/workflow-overlay/communication-style.md`.
2. Commission, target, authority, decision criteria, evidence, and reviewer recommendation in that order.
3. `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` declaration.
4. A concise source-read ledger.
5. Findings first after the required summary and context sections, ordered by severity.
6. For each actionable finding:
   - severity;
   - location;
   - issue;
   - evidence;
   - impact;
   - `minimum_closure_condition`;
   - `next_authorized_action`;
   - recommended correction or advisory remediation direction.
7. Non-findings and residual risks.
8. Review-use boundary.

Allowed `review_summary.recommendation` values:

- `accept`
- `accept_with_friction`
- `patch_before_acceptance`
- `reject`
- `blocked`

Use recommendation values as reviewer decision input only. They are not acceptance, approval, validation, readiness, mandatory remediation, or executor-ready authority.

If no issues are found, say so clearly and list residual risks or test gaps.

## Forbidden Outputs

Do not include:

- `patch_queue_entry`;
- executor-ready patch instructions;
- model runtime recommendations or rankings;
- participant-facing packet prose;
- a Canoo/Walmart judgment or score;
- a claim that Step A proves judgment quality;
- a claim that TR/Casetext is judgment-quality evidence;
- a claim that this review validates the Judgment Spine;
- a claim that dirty or untracked artifacts are accepted, ready, source-of-truth, or validation evidence;
- public web research beyond the sources already named in the target artifacts;
- wrong-lane Reddit or attention-lens material.

## Chat Closeout After Report Write

After the durable report is successfully written, return only a compact chat closeout:

```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/adversarial-artifact-reviews/canoo_walmart_source_packet_safety_adversarial_artifact_review_v0.md
  recommendation: accept | accept_with_friction | patch_before_acceptance | reject | blocked
  summary: "One sentence describing the review result."
  findings_count: 0
  blocking_findings: []
  advisory_findings: []
  prior_findings_remediated: []
  next_action: "One concrete next step."
```

Do not add extra YAML keys.

## Review-Use Boundary

This is a read-only adversarial artifact review. Findings and non-findings are decision input only. They are not approval, validation, product proof, mandatory remediation, source-of-truth promotion, implementation authorization, or executor-ready instructions unless a separate authorized Orca decision, patch, validation, or implementation lane accepts them.

Required boundary: plumbing works only; not judgment quality.
