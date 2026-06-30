# Communication Style

```yaml
retrieval_header_version: 1
artifact_role: Orca overlay authority
scope: Orca response style, chat-output topology, courier YAML shape, and adversarial review summary pattern.
use_when:
  - Checking Orca review closeout and courier YAML shape.
  - Preparing or reviewing Orca prompt handoffs and Chief Architect sequencing.
authority_boundary: retrieval_only
```

This file records Orca-specific response style for Chief Architect sequencing,
review closeouts, and prompt handoffs. It applies to user-facing chat and
Orca-authored prompts unless a later user instruction asks for a different
shape.

## Default Shape

Use short headers when they improve scanning.

Prefer bullets when they reduce parsing, but give each bullet a small
explanation. Do not bold the bullet lead by default.

Lead with the decision, then the scope, then the next action. Keep status and
file-state language secondary unless exact repository state is the point.

## Chat Output Topology

For decision-bearing Orca chat, use this order:

1. Human summary.
2. Agent-readable detail.
3. Compact courier state, only when useful or required.

The human summary states the decision, scope, accepted or deferred items,
blocker if any, and next authorized step. Agent-readable detail may include
source-read notes, file lists, dirty-state classification, validation-not-run
notes, report paths, exact handoff constraints, and blockers.

Courier state is routable state, not the decision or report itself. Use clear
headed prose by default. Use YAML only when the user requests it, an output-mode
exception requires it, an explicit output contract needs machine-shaped fields,
or lane switching / handoff routing would materially benefit from compact
courier YAML. It should stay compact and appear last unless an output-mode
exception explicitly requires YAML-first or YAML-only chat.

This file owns the general chat shape and exact courier YAML shapes it defines.
Output-mode exceptions, including when `review-report` may use YAML-only chat,
when `file-write` may return compact artifact receipts, and how
`paste-ready-chat` behaves, are owned by
`.agents/workflow-overlay/prompt-orchestration.md`.

Do not apply the human-summary-first rule mechanically to artifact-native
tables, paste-ready prompt bodies, or compact post-artifact receipts when the
durable artifact or pasted prompt carries the human-readable value. Do apply it
to substantial decision-bearing `file-write` closeouts, Chief Architect
sequencing, planning, implementation scoping, overlay process gates,
completion reports, chat-only decisions, and failure/blocker routing.

For doctrine-changing file writes or source-changing closeouts, include the
`direction_change_propagation` receipt or
`direction_change_propagation_blocker` from
`.agents/workflow-overlay/source-of-truth.md` in the agent-readable detail or
compact courier state. Do not present that receipt as validation, readiness,
approval, acceptance, proof, implementation authorization, or source promotion.

## Readability Rules

- Use plain decision language. Say what is accepted, blocked, deferred, or
  authorized before naming artifact status.
- Separate now, next, and later. Acceptance, review, commit, and proof execution
  must not blur together.
- Explain boundaries in terms of what they mean. For example: this prepares the
  proof shape; it does not run proof or collect evidence.
- Use exact file or git-state language only when it matters. Prefer "accepted in
  chat, not committed" over abstract phrases like "persistence caveat."
- Avoid process-heavy nouns when an action phrase is clearer. Watch for
  "review state," "coherent set," "artifact adequacy," and similar phrasing.
- Keep template output readable. Use the required shape, but do not sound like a
  form is being filled in.

## Goldilocks Bullet Pattern

- Name the action or issue. Add one sentence explaining why it matters.
- Keep bullets short enough to scan, but not so short that the reader has to
  infer the decision.
- Use prose when the sequence is the point and bullets would make it choppy.

## Preferred Closeout Pattern

Use this order for sequencing decisions:

1. Decision.
2. Scope or boundary.
3. Next action.
4. What remains blocked.

## Owner-Run Command Blocks

(Added 2026-06-12, owner word: commands handed to the owner must be usable
"from anywhere".) When an agent hands the owner a command block to run
themselves — any guard-gated human step, such as landing a PR via
`.github/scripts/merge-when-green.ps1` or operating on guard-protected paths —
the block must be runnable from any directory:

- Use absolute paths for every script and file in the block; never a
  repo-relative path on its own.
- Pass explicit repo/target flags (for example `--repo owner/name`) rather
  than relying on the current working directory to imply them.
- If a command genuinely requires a specific working directory, make the
  block self-contained by starting it with an explicit
  `cd "<absolute path>"` line.

## Chief Architect Review Consumption

When an Orca Chief Architect or CA-facing handoff consumes one or more review
reports, preserve this order:

1. Commission: what the CA or owner asked the review to decide or inspect.
2. Target: the exact artifact, prompt, diff, report, or surface reviewed.
3. Authority: the Orca overlay, prompt, current instruction, or source boundary
   that controls the review result.
4. Decision criteria: the criteria the review was asked to apply.
5. Evidence: the cited findings, source reads, gaps, and not-proven limits.
6. Reviewer verdict or recommendation: the reviewer summary, if one is bound.

Reviewer recommendations in `review_summary` are courier and decision input.
They are not acceptance, approval, validation, readiness, mandatory
remediation, or patch authority unless a separate Orca decision or execution
lane binds that result. Do not add a synthesis lane by merging multiple review
reports into a new authority surface; unresolved review disagreement remains
Chief Architect adjudication unless Orca later binds another owner.

## Review Adjudication Next Step

When a Chief Architect adjudicates a review -- delegated or self-review, keeping
or vetoing findings -- the closeout's next step is derived, not improvised.
First adjudicate the review's findings, diff, verdict, and residuals as claims.
Then route the next step by the adjudicated state:

- If any blocker, major, material unresolved issue, or material uncertainty
  remains, the next step is the smallest complete closure route for that issue.
  Do not deep-think downstream material moves until the review is clean enough
  to move on.
- If no unresolved material issue remains, admin/lifecycle steps (commit, push,
  PR, merge) collapse into exactly one batched "land" step, with no
  deep-thinking -- they are rote.
- After a clean adjudication, material moves get the deep-thinking: the next 1-3
  substantive steps that need judgment, each named with why it compounds and its
  main risk. Pure admin never counts as one of those material steps.

No material moves means the one land step is the whole next step, so the pass
stays cheap on every adjudication instead of becoming ceremony. It fills the
closeout's `next_action` (YAML form) or "next authorized step" (prose form);
`next_action` stays a single string -- unresolved-review closure first when
needed; otherwise the one land step first, then the material moves when they
exist. Review prompts and review-return prompts carry this as their next-moves
tail (see `.agents/workflow-overlay/prompt-orchestration.md`, Review Prompt
Defaults). This governs an adjudicated review's next step; it does not change the
failed-write `next_action` routing below.

## Adversarial Review Summary Pattern

For adversarial artifact reviews, start with a compact copy-pasteable YAML
summary before any detailed findings. This lets later threads recover the
review state without reading a long chat block.

This file owns the courier YAML shape and allowed fields. The validity rules
for `review-report` output mode, including when YAML-only chat is allowed and
what to do when a required durable write fails, are owned by
`.agents/workflow-overlay/prompt-orchestration.md`.

Use this shape when the review writes a durable report:

```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/example_adversarial_review_v0.md
  recommendation: accept | accept_with_friction | patch_before_acceptance | reject | blocked
  reviewed_by: claude-opus-4.8     # model+version that performed the review; operator/CA-supplied; "unrecorded" if not; never fabricated; observed record, not a recommendation
  authored_by: claude-opus-4.8     # model+version that authored the reviewed artifact; same-vs-cross is computed by relating the two
  summary: "One sentence describing the review result."
  findings_count: 0
  blocking_findings: []
  advisory_findings:
    - FF-01: Short finding title
  prior_findings_remediated: []
  next_action: "One concrete next step"
```

For Orca review prompts using `review-report` output mode, `report_path` is
valid only when the durable report was actually written. If no durable report
exists because the review is explicitly chat-only or blocked before writing,
replace `report_path` with `review_location: chat_only_current_thread` and keep
the same remaining fields.

If a required `review-report` durable write fails, use the same shape with
`status: failed`, `review_location: chat_only_current_thread`, and
`recommendation: blocked`. Do not use `report_path` for an unwritten or failed
report. The `summary` and `next_action` fields should make the write failure
and routing need clear without adding extra process keys.

```yaml
review_summary:
  status: failed
  review_location: chat_only_current_thread
  recommendation: blocked
  reviewed_by: unrecorded
  authored_by: unrecorded
  summary: "Failed to write required report to docs/review-outputs/example_adversarial_review_v0.md."
  findings_count: 0
  blocking_findings: []
  advisory_findings: []
  prior_findings_remediated: []
  next_action: "Resolve the report write failure, then rerun the review-report prompt."
```

`reviewed_by` and `authored_by` record the model+version that performed the
review and that authored the reviewed artifact (for example `claude-opus-4.8`,
`gpt-5.5`), set by the operator/CA on the durable record; each value is
`unrecorded` when the identity was not supplied and is never fabricated. Both
are present on every review summary. They are observed provenance records only
and do not recommend, rank, or select a runtime model (see
`.agents/workflow-overlay/review-lanes.md` Review Doctrine, the model-neutrality
bullet). Same-family-vs-cross-family is computed by relating the two and is
measured only when both carry real values; a present `unrecorded` value is a
visible measurement gap, not success.

Do not include these fields in Orca adversarial review summaries:

- `report_written`
- `protected_path_check`
- `hidden_ledger_read`
- `runtime_code_changed`
- `fixture_expansion_performed`
- `harness_or_compiler_or_path_b_run`

When a durable report is written, detailed review prose belongs in the report,
not in chat. The chat response should normally contain only the YAML summary
unless the user explicitly asks for inline detail. For chat-only reviews, brief
detail may follow when useful, but the YAML summary should still be sufficient
for another thread to know the review status, where to read it, the short
summary, blocking/advisory finding IDs, and the next action.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Review adjudication now carries a next-moves tail. When a Chief Architect
    adjudicates a review (delegated or self-review), the closeout's next step is
    derived: one batched admin/lifecycle "land" step (commit, push, PR, merge)
    with no deep-thinking, plus deep-thought material moves (the 1-3 substantive
    next steps, each with why-it-compounds and main risk); no material moves
    means the land step is the whole next step. communication-style.md owns the
    admin/material shape and next_action stays a single string (no schema
    change). prompt-orchestration.md Review Prompt Defaults adds the requirement
    that every review prompt and review-return/courier prompt instruct the
    adjudicator to run this pass after the verdict -- the tail mirror of the
    existing deep-thinking-first rule -- and points here for the shape. No
    external skill is edited and no hook is added; the rule rides the already
    mandatory closeout next-step output, so it is strongly habitual, not
    deterministically enforced.
  trigger: review_authority
  related_triggers:
    - output_authority
    - workflow_authority
  controlling_sources_updated:
    - .agents/workflow-overlay/communication-style.md
    - .agents/workflow-overlay/prompt-orchestration.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/review-lanes.md
    - .agents/workflow-overlay/delegated-review-patch.md
    - docs/workflows/orca_repo_map_v0.md
  intentionally_not_updated:
    - path: AGENTS.md
      reason: >
        Routes review/prompt doctrine to the overlay and carries no closeout or
        review-prompt-default mechanics; the rule lives in the two overlay files,
        so no root restatement is added.
    - path: .agents/workflow-overlay/review-lanes.md
      reason: >
        States the head deep-thinking-first lane rule (line 176); the symmetric
        next-moves tail is owned by prompt-orchestration.md Review Prompt Defaults
        plus communication-style.md for shape, and is not contradicted.
        Dual-homing the tail there would duplicate rather than single-source.
    - path: .agents/workflow-overlay/delegated-review-patch.md
      reason: >
        Its adjudication tail ("the Chief Architect then adjudicates the returned
        diff") is the trigger point, but the next-moves shape and prompt
        requirement are owned by the two updated files; it inherits by deferral
        and needs no restatement.
    - path: docs/workflows/orca_repo_map_v0.md
      reason: >
        Index lines for communication-style.md and prompt-orchestration.md stay
        accurate (review closeouts / prompt bindings); this is an additive in-file
        doctrine edit, not a structural or navigation change.
  stale_language_search: >
    rg -ni "one concrete next step|next_action|next authorized step|next-moves|land step"
    .agents/workflow-overlay
  stale_language_search_result: >
    Executed 2026-06-29 (worktree serene-burnell-d19a2c). Hits: communication-style.md:37
    (general "next authorized step" in Chat Output Topology -- now also covered by the new
    section's prose form, not contradicted); :161 (review_summary next_action "One concrete
    next step" -- now defined by Review Adjudication Next Step rather than left loose);
    :173,:188 (failed-write next_action -- a distinct pre-adjudication blocker-routing step
    the new rule explicitly does not touch); prompt-orchestration.md:551 (file-write doctrine
    receipt rule naming "next authorized step" -- orthogonal). No live surface presents the
    adjudicated-review next step as improvised or omits the admin/material split, and the
    deep-thinking-first rule is extended by a tail mirror, not contradicted.
  non_claims:
    - not validation
    - not readiness
    - not source promotion
    - not implementation authorization
```

Receipts cycled out of this inline section move verbatim to `docs/decisions/dcp_receipts_archive_v0.md`.
