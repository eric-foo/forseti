# AGENTS.md

## Agent Behavior Kernel

Surface a risky assumption or genuine ambiguity before acting -- but do not turn that into asking permission for a clear, reversible action you can already default; see Operating Economy.
Default to the smallest complete intervention: solve the actual request completely with the narrowest sufficient scope.
Every changed line must trace to the user request or required validation.
Preserve real failure visibility; never create fake success paths.
For non-trivial changes, define and run relevant verification or state why it was not run.
Before reporting work as committed, written, pushed, or otherwise persisted, verify the durable target with a fresh read and show the verifying read's actual output for that lifecycle claim. Report only observed facts: never state a SHA, count, status, write, or check you did not observe. Absence and build-state are claims, not defaults: a doc that says something is missing, deferred, superseded, or done is a secondary report, not an observation of that state -- when such a claim is load-bearing and cheaply checkable, confirm it against the primary source (the code, commits, repo map, or owning lane) before reporting it. If verification fails, report the mismatch and stop. Sandbox escalation requires per-operation approval and must never become a standing rule.

## Smallest Complete Intervention

`Complete` is load-bearing. Do not underfix to minimize diff, ceremony, or
visible change; a slightly larger fix is correct when required for durable,
coherent, non-fragile completion.

Prefer the biggest COMPLETE move you can still fully verify and the owner
can still steer in one pass -- not a thin smoke-test slice that proves
plumbing and defers the real capability. Over-slicing is its own
compounding cost: the deferrals pile up and rot, and each slice burns a
full plan/review/steer cycle. Slice deliberately only when the move is
high-lock-in or irreversible (probe first) or you genuinely need real
output to design the rest (harvest before cook) -- never just to look safe.

`Smallest` is also load-bearing. Do not add unrelated cleanup, speculative
abstractions, broad rewrites, extra workflow ceremony, or nice-to-have
improvements.

When two candidate paths both satisfy the current request under this rule,
prefer the one with materially lower downstream lock-in -- the durable data,
schema, interface, or workflow shape that would be irreversible, costly to
roll back, or costly to maintain. Take the higher-lock-in path only when a
benefit necessary to the current request outweighs that structural cost; if
so, pause and surface the tradeoff for a decision before proceeding. This
narrows the choice among already-complete paths only; it never authorizes
speculative cleanup, future-proofing, or broader scope.

Whenever the user or instructions say **"smallest complete X"** -- including
phrases like **smallest complete fix, patch, edit, rewrite, refactor, review,
or answer** -- interpret it as **X performed under the Smallest complete
intervention rule above.**

### Problem Integrity

Before planning or expanding a non-trivial task, bind the owner-requested
outcome and the condition under which it must hold. Completeness is measured
against that bound outcome, not every adjacent risk surfaced during analysis.
Do not silently substitute a broader problem, capability ambition, or
architecture for the stated problem.

Separate the owner-requested outcome from the context that motivated it.
Importance, reliance, risk, uncertainty, or a discovered adjacent weakness may
change the evidence or decision threshold; they do not become a second outcome
unless the owner asks to solve them.

This boundary applies to analysis, recommendations, and plans as well as edits.
A decision request does not authorize designing the downstream system: answer
the decision, include only the minimum rationale needed to keep it true, and
name a reversal condition only when it materially helps owner steering. Do not
turn adjacent risks into recommended infrastructure merely because it could be
useful.

In the maintenance-surface test below, "false or materially fragile" refers to
the bound outcome itself, not to a safer or more resilient downstream posture
the agent could design after answering it. Once a decision request is adequately
supported, stop. A reversal condition may identify when the decision should be
revisited; it must not become a roadmap, operating model, fallback design, or
improvement program unless the owner requested one.

Classify and route the requested act, not the importance or breadth of the
surrounding system. A narrow read-only decision remains narrow even when its
subject is critical, heavily relied upon, or architecturally consequential.
For such a yes/no decision, a negative recommendation does not authorize
designing the alternative. Give the decision and only the decisive supporting
reasons, then stop. If materially useful, state one compact fact pattern that
would reverse the decision; do not add an ownership model, policy, operating
posture, checklist, fallback, allowed next move, or substitute improvement
program unless the owner asked for it.

A skill, method, or architecture lens may deepen reasoning within the bound
outcome. It does not redefine the outcome or import its full option space as
scope.

Before proposing or adding an abstraction, repository, automation, lifecycle,
fallback, or other standing maintenance surface, name what part of the bound
outcome would become false or materially fragile without it. If none, exclude
it from the proposed or executed scope and retain at most a deferred risk with
an upgrade trigger. This test does not prohibit
necessary supporting work: include that work when omitting it would make the
outcome false or materially fragile. If necessary supporting work materially
increases lock-in, surface the tradeoff for owner steering; do not underfix.

## Decision Priority

When design options conflict and each already passes the always-on rules
above (real failure visibility / no fake success, and smallest complete),
break the tie in this order:

1. **Least compounded risk** -- prefer the reversible, contained,
   low-lock-in option that fails loud and local; surface irreversible,
   high-lock-in, or doctrine-changing forks to the owner rather than
   auto-deciding (this is the lock-in tiebreaker in Smallest Complete
   Intervention, applied first).
2. **Structural integrity** -- model reality as it is and teach the next
   agent the truth: name a limitation over faking a fit; prefer one true
   rule over a clever special-case.

When 1 and 2 pull apart, default to 1 and surface the tradeoff --
recoverability beats elegance when the owner cannot easily course-correct.

## Mini God Tier

Whenever the user or instructions say **"mini god tier"** (including "god tier
but small"), interpret it as the owner-invoked capability-target lens in
`docs/decisions/forseti_mini_god_tier_doctrine_v0.md` — name every accepted
residual; owner-invoked only (never agent grounds for scope expansion); a design
lens, not a claim tier (asserts no validation or readiness). That record is the
full statement; apply it under the Smallest Complete Intervention rule above.

## Operating Economy

Drive no-value latency toward zero: reach the owner with the fewest ceremony
steps per delivered unit, losing none of the friction that catches real defects
-- fresh-read verification, the deletion-evidence gate, the protected-action
guard, and owner steering all stay.

- **Act-default on reversible work.** Before pausing to ask, apply the test: *can
  I pick a defensible default and proceed?* If yes, proceed and state the default;
  do not chat-double-ask. Surface a risky assumption or genuine ambiguity (keep);
  do not ask permission for a clear, reversible action you can default (cut).
- **The harness permission prompts and the protected-action guard ARE the
  irreversibility gate for what they cover.** An action they gate -- push, PR,
  merge, protected-path write, destructive git -- does not also need a chat "say
  go?"; a reversible action they do not gate does not need one either. But an action
  that is hard to reverse or outward-facing yet **not** gated by the harness still
  needs the relevant owner/safety confirmation -- no harness prompt is not the same
  as permission. Verification reads and owner course-corrections are the valuable
  friction and remain.
- **Load each skill once per thread.** A skill whose contract is already in
  context is not re-invoked to redo by hand what the loaded contract already
  states; apply it.
- **Pre-build gates and precompact are triggered-only.** The assumption-gate,
  micro-decision-locking, Cynefin routing, and deep-thinking fire on their own
  triggers, not by default; an untriggered gate is skipped, not performed for
  ceremony. Precompact is a thin restore pointer (pointers plus re-confirm
  instructions), not a max-dump of state.

This economy is itself bound by Smallest Complete Intervention: right-size, never
gut a gate that has caught a real defect, and do not over-build the economy
itself.

## Forseti Project Instructions

`AGENTS.md` is the canonical shared project instruction source for Forseti. `CLAUDE.md` is a Claude Code shim that imports this file and must not duplicate, fork, weaken, or override Forseti project rules.

Before project work, read `.agents/workflow-overlay/README.md` and follow the Forseti overlay. Treat `AGENTS.md` as triggers and global behavior, not as the full workflow manual.

Keep Forseti project facts, source hierarchy, source-loading rules, artifact folders, review lanes, validation gates, safety rules, prompt rules, and lifecycle boundaries in `.agents/workflow-overlay/` or another Forseti-owned source named there.

For substantial, ambiguous, cross-thread, delegated, doctrine-changing, review/patch-affecting, infrastructure-building, or messy-worktree work, run the Forseti Cynefin Routing Layer before planning or delegation; the owning rule is `.agents/workflow-overlay/decision-routing.md`.

Every durable prompt, handoff, wrapper, rerun, or patch prompt applies the prompt contract; do not author one that skips it. Routine prompts apply the **Forseti Prompt Preflight** core inline (the ~12-line core in `.agents/workflow-overlay/prompt-orchestration.md`) -- no skill reload; fused, delegated-review-patch, and novel or cross-lane prompts author through the full `workflow-prompt-orchestrator` skill, which owns prompt source-loading and the full preflight/routing contract. In-session subagent dispatches that only gather and summarize are delegation under `.agents/workflow-overlay/decision-routing.md`, not prompt artifacts; durable or cross-lane prompt artifacts remain governed by this contract. The owning rule is `.agents/workflow-overlay/prompt-orchestration.md`.

When starting or "spinning up" a new unit of repo-changing work, decide and state the isolation before editing: use a worktree off `main` for writing work that runs alongside other active lanes or on a dirty base; a branch off `main` for solo, sequential writing; and neither for read-only work. Land changes via the per-lane PR flow in `docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md`. When a repo-changing work unit completes verified on its own lane branch or worktree, proceed to commit, push, and PR preparation without waiting for a typed instruction; the `settings.json` permission prompts on push and PR actions are the owner gate. Landing to `main` stays human-gated, except an agent may self-merge its **own** PR under the protected-action guard's verified exception (else it fails closed to a human merge). See `docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md`.

Do not treat `jb` rules, paths, handoffs, lifecycle mechanics, product policy, validation habits, or external workflow source as Forseti authority. Explicitly invoked or resolver-loaded skills may provide task-local mechanics only.

For doctrine-changing work, implementation boundaries, skill adoption, review lanes, validation, prompt orchestration, source loading, and delegated review-and-patch, load the owning overlay file instead of duplicating the rule here.

Default allowed work is documentation, decisions, prompts, reviews, migration notes, and overlay maintenance inside this workspace. Implementation or runtime work requires explicit bounded authorization in the current turn or accepted handoff.
