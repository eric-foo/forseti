# Review Input: Fused Skill Post-A Closeout Hardening (Verbatim Proposed Text)

```yaml
retrieval_header_version: 1
artifact_role: Review input artifact
scope: >
  Verbatim proposed post-A text of the user-level fused skill
  (~/.claude/skills/fused/SKILL.md) staged for delegated adversarial review.
  The real target file is outside this repository and protected from agent
  edit; this copy is the review target for the [fused-skill] label of the
  EP-35 delegated review commission (PR #587 lane).
use_when:
  - Reviewing the fused-skill closeout hardening (Change A) as part of the
    EP-35 delegated review commission.
  - Verifying the operator-applied user-level skill edit matches the reviewed
    text.
authority_boundary: retrieval_only
```

**Flag-only target.** Do not patch this file or any user-level skill path;
return findings only. The owner applies accepted changes to
`~/.claude/skills/fused/SKILL.md` and `~/.codex/skills/fused/SKILL.md`.

**Provenance.** Staged 2026-07-02 from the session scratchpad; SHA256 of the
raw staged file (identical to the fenced content below, byte-for-byte,
LF line endings): `00B92452FD1758CD81C114E6B2306D8CCC6354638FB02A581B4A2CFF54A8DB23`.
The three deltas vs the installed 2026-06-17 skill are: (A1) /fused itself
authorizes prompt rendering for a carried review — commission without rendered
prompt closes as blocked, never routed; (A2) 'not authorized / not requested'
removed as valid prompt-absence reasons; (A3) review_routing_status must land
in the lane's implementation commit body, checkable by a project-bound
disposition gate.

---

```markdown
---
name: fused
description: "Explicit entry point for the fused implementation turn. Use only when explicitly invoking `fused` (`/fused`); never inferred. Runs the pre-implementation pipeline in one turn and in order: implementation scoping (entry gate), spec writing, micro-decision locking, implementation. It proceeds only while each lane clears, with the go-decision at the micro `route_ready` tail; recommended review does not interrupt implementation but triggers `workflow-delegated-review-patch` after implementation finishes, while required review checkpoints route to `workflow-delegated-review-patch` and stop for delegated review in another lane. Never itself scopes, specs, locks, edits, installs, deploys, stages, commits, pushes, or claims readiness; it sequences the lanes and hands off to the overlay-owned implementation lane."
---

# Fused Implementation Turn

## Purpose

Run the pre-implementation pipeline as one gated turn instead of separate turns,
for routine implementation lanes. This skill only sequences existing lanes; it
owns no route, spec, lock, or edit of its own.

## Trigger

Explicit invocation only: the user types `/fused` (or invokes `fused`). Never
trigger by inference, phrasing, or because a plan looks ready. Without explicit
`/fused`, do not run this pipeline — route ordinary scoping to
`workflow-implementation-scoping`, which stops after the route by default.

Invoking `/fused` is itself the implementation authorization for this turn. It
is a precondition to enter, never an override: any lane below may veto or pause,
and `/fused` cannot force a clear.

## The Four Lanes, In Order

Run each lane and stop at the first that does not clear.

1. **implementation scoping** (`workflow-implementation-scoping`) — entry and
   route gate. Apply its Conditional Implementation Gate. If it blocks or pauses
   for route, contract, validation, authority, or context-risk reasons, stop
   here and report; do not continue. If it emits a Review Timing Advisory with
   `adversarial_review: recommended` and still clears the route, keep it as a
   closeout advisory rather than a stop. If it emits
   `required_by_bound_gate` and still clears the route, carry the checkpoint
   forward instead of stopping at scoping.
2. **spec writing** (`workflow-spec-writing`) — behavior-contract gate.
   Fast-exits when no contract is at stake. If it returns a blocker or
   unresolved choice, pause; otherwise continue.
3. **micro-decision locking** (`micro-decision-locking`) — execution gate. If
   `blocked` or `route_ready: false`, pause; if `locked` or `not_needed` with
   `route_ready: true`, continue.
4. **implementation** — the overlay-owned execution phase, not a kernel skill;
   the kernel never performs it. It begins only after lane 3 returns
   `route_ready: true` and the overlay's edit authority is bound; it makes the
   edits, runs the overlay's own post-edit validation, and is the pipeline's
   only non-read-only step. Scoping's `Recommended Implementation Model`
   (`mechanical_lane` / `judgment_lane`) advises which executor the overlay
   routes here. If scoping carried a required review checkpoint, implementation
   proceeds only to that checkpoint, then routes to
   `workflow-delegated-review-patch` and stops; review, patching, adjudication,
   and any later resume happen in another lane or later turn. If scoping only
   recommended review, implementation may complete all route steps, then must
   trigger delegated review as a post-implementation handoff before final
   closeout.

The first three lanes gate and hand off; the fourth executes. This is the
existing kernel/overlay boundary — the kernel gates, the overlay owns execution
contracts.

## Review Checkpoint Routing

When implementation scoping emits a Review Timing Advisory and the route still
clears, `/fused` does not stop at scoping just because review is recommended or
required. Preserve these fields through spec writing and micro-decision locking:

- `adversarial_review`;
- `highest_value_checkpoint`;
- `review_target`;
- `why_this_checkpoint`.

For `adversarial_review: recommended`, do not interrupt implementation by
default. Treat `highest_value_checkpoint`, `review_target`, and
`why_this_checkpoint` as an advisory note to carry into closeout. Complete the
route when spec, micro, validation, and overlay authority otherwise clear; after
the implementation steps and their validation finish, trigger
`workflow-delegated-review-patch` in the same turn as a post-implementation
handoff. This trigger is not a bound checkpoint and must not be used to stop
before or during implementation; it only changes the closeout behavior from an
optional next-lane report to an automatic delegated-review handoff.

For `adversarial_review: required_by_bound_gate`, execute only as far as the
named `highest_value_checkpoint`:

- `before_STEP-*`: trigger `workflow-delegated-review-patch` before changing
  source for that step, then stop;
- `after_STEP-*`: complete that step and its local validation, then trigger
  `workflow-delegated-review-patch` and stop before dependent steps continue;
- `after_all_steps_pre_closeout`: complete all route steps and validation, then
  trigger `workflow-delegated-review-patch` and stop before final closeout or
  acceptance claims;
- `not_applicable`: no review checkpoint is carried.

Required review is a hard pause: trigger `workflow-delegated-review-patch` at
the checkpoint and do not continue past the guarded dependent step or closeout
until the delegated pass and home-model adjudication are resolved under their
own authority. A `required_by_bound_gate` result without a safe concrete
`highest_value_checkpoint` does not clear the fused entry gate.

`workflow-delegated-review-patch` produces the delegated commission and
adjudication contract; it does not run the review or render the final routing
prompt. For a carried recommended or required review, invoking `/fused` is
itself the authorization to render the routing prompt: route the commission to
`workflow-prompt-orchestrator` in the same turn and stop after the paste-ready
or saved review prompt is produced. A commission without a rendered prompt
closes as `blocked` with the named render blocker, never as `routed`. For
recommended review this is a post-implementation closeout handoff; for
required review it is a hard checkpoint. Fused never resumes implementation in
the same turn after a required delegated-review checkpoint is triggered.

Whenever `/fused` reaches a stop or final closeout without producing a
paste-ready or saved adversarial-review prompt, report the prompt absence
explicitly. Name the reason, such as `adversarial_review: not_needed`, no Review
Timing Advisory was carried, the pipeline stopped before a review trigger was
reached, or prompt rendering was blocked by a named orchestrator/delegation
blocker. 'Not authorized' and 'not requested' are never valid reasons for a
carried review — `/fused` authorizes rendering. Do not leave prompt absence
implicit when the turn mentions review routing, review timing, delegated
review, or final closeout.

Every `/fused` stop or final closeout must include exactly one
`review_routing_status` field with one of these values:

- `routed`: a delegated-review commission, prompt-orchestrator handoff, or
  orchestrated prompt was produced for the carried review obligation;
- `blocked`: review was carried or required but the handoff or prompt could not
  be produced; include the precise blocker and do not claim final closeout
  success;
- `not_needed`: no Review Timing Advisory or loaded review obligation was
  carried, or the carried value was explicitly `not_needed` / `not_applicable`.

Do not use `not_needed` for a carried `recommended` or
`required_by_bound_gate` review. Do not replace `review_routing_status` with
`why_not_created`: the status is the required visible review disposition, while
`why_not_created` explains prompt absence. A fused closeout that omits
`review_routing_status`, uses another value, or lets a carried review reach
closeout without `routed` or `blocked` is invalid.

`review_routing_status` is not chat-only. Hand the status line — plus the
review prompt path when `routed` — to the overlay-owned commit step so it
lands in the lane's implementation commit body, where a project-bound
disposition gate can check it. A fused lane whose commit body omits the status
line is a closeout defect even when the chat closeout carried it.

When delegated reviewer output from a prior fused-triggered handoff is couriered
back in a later turn, route that return to `workflow-delegated-review-patch`
review-return adjudication. Do not resume fused sequencing or treat reviewer
output as accepted until home-model adjudication emits
`operator_closeout_source`.

## Non-Implementation Artifact Exit

If lane 1 does not clear because the current work is not source-changing
implementation, `/fused` still preserves any loaded review obligation when the
same turn is explicitly routed to an authorized artifact-writing lane. When that
lane authors a design, spec, doctrine, ratification, or other non-code artifact
that loaded authority says must be reviewed before ratification,
implementation, downstream use, package/deploy surfaces, or strict closeout
claims, the review handoff is immediate after artifact write/readback:

- trigger `workflow-delegated-review-patch` for the authored artifact;
- if a paste-ready or saved review prompt is required, route the commission to
  `workflow-prompt-orchestrator`;
- stop after the commission or prompt handoff is produced.

Do not treat the required review prompt as a merely optional "next step" after
authoring a review-gated artifact. Do not ratify, implement from, propagate,
or claim acceptance/readiness for that artifact until delegated review and
home-model adjudication resolve under their own authority.

## Stop And Pause Contract

- A lane's blocker stops the pipeline at that lane. Report the lane, its status,
  and what is needed; do not skip a lane or proceed past a veto.
- A recommended review advisory is not a lane blocker and does not interrupt
  implementation by default; after implementation finishes, it triggers a
  same-turn delegated-review handoff before final closeout. A required review
  checkpoint is not a scoping blocker when the checkpoint is concrete and
  reachable; it becomes a hard checkpoint obligation during implementation.
- Final closeout is invalid when `adversarial_review: recommended` was carried
  through implementation and implementation finished but the turn produced no
  `workflow-delegated-review-patch` handoff, no prompt-orchestrator handoff for
  that commission, and no precise blocker explaining why the handoff could not
  be produced.
- Every stop and final closeout must include
  `review_routing_status: routed | blocked | not_needed`. A carried
  recommended or required review may close only as `routed` or `blocked`; it may
  never disappear into `not_needed` or an omitted field.
- If no adversarial-review prompt is produced, the closeout must include a
  concise `why_not_created` reason. A missing reason is a closeout defect even
  when review was not needed.
- A non-implementation reroute does not erase a loaded review obligation. If the
  rerouted lane authors the review-gated artifact, delegated-review commission
  or prompt handoff is part of the same stop, not a later optional follow-up.
- If spec writing or micro-decision locking changes the touch points,
  validation, or authority surface scoping bound, re-enter lane 1 before
  implementing rather than proceeding on a stale route.
- Each lane keeps its own ownership, output, and bindings. This skill relaxes
  none of them and adds no parallel status vocabulary.

## Boundary

This skill sequences only. It does not itself scope, write specs, lock
decisions, produce prompts, or edit source, and it makes no route, spec, lock,
validation, or readiness claim of its own. Edit permission, validation gates,
and write boundaries remain overlay-owned; the implementation lane is the
overlay's, not this skill's.

```