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
3. Compact courier YAML, only when useful or required.

The human summary states the decision, scope, accepted or deferred items,
blocker if any, and next authorized step. Agent-readable detail may include
source-read notes, file lists, dirty-state classification, validation-not-run
notes, report paths, exact handoff constraints, and blockers.

Courier YAML is routable state, not the decision or report itself. It should
stay compact and appear last unless an output-mode exception explicitly
requires YAML-first or YAML-only chat.

This file owns the general chat shape and exact courier YAML shapes it defines.
Output-mode exceptions, including when `review-report` may use YAML-only chat,
when `file-write` may return compact artifact receipts, and how
`paste-ready-chat` behaves, are owned by
`.agents/workflow-overlay/prompt-orchestration.md`.

Do not apply the human-summary-first rule mechanically to artifact-native
tables, paste-ready prompt bodies, or compact post-artifact receipts when the
durable artifact or pasted prompt carries the human-readable value. Do apply it
to Chief Architect sequencing, planning, implementation scoping, phase gates,
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
  summary: "Failed to write required report to docs/review-outputs/example_adversarial_review_v0.md."
  findings_count: 0
  blocking_findings: []
  advisory_findings: []
  prior_findings_remediated: []
  next_action: "Resolve the report write failure, then rerun the review-report prompt."
```

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
