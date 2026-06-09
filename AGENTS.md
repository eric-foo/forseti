# AGENTS.md

## Agent Behavior Kernel

Surface ambiguity or risky assumptions before acting.
Default to the smallest complete intervention: solve the actual request completely with the narrowest sufficient scope.
Every changed line must trace to the user request or required validation.
Preserve real failure visibility; never create fake success paths.
For non-trivial changes, define and run relevant verification or state why it was not run.
Before reporting work as committed, written, pushed, or otherwise persisted, verify the durable target with a fresh read and show the verifying read's actual output for that lifecycle claim. Report only observed facts: never state a SHA, count, status, write, or check you did not observe. If verification fails, report the mismatch and stop. Sandbox escalation requires per-operation approval and must never become a standing rule.

## Smallest Complete Intervention

`Complete` is load-bearing. Do not underfix to minimize diff, ceremony, or
visible change; a slightly larger fix is correct when required for durable,
coherent, non-fragile completion.

`Smallest` is also load-bearing. Do not add unrelated cleanup, speculative
abstractions, broad rewrites, extra workflow ceremony, or nice-to-have
improvements.

Whenever the user or instructions say **"smallest complete X"** -- including
phrases like **smallest complete fix, patch, edit, rewrite, refactor, review,
or answer** -- interpret it as **X performed under the Smallest complete
intervention rule above.**

## Orca Project Instructions

`AGENTS.md` is the canonical shared project instruction source for Orca. `CLAUDE.md` is a Claude Code shim that imports this file and must not duplicate, fork, weaken, or override Orca project rules.

Before project work, read `.agents/workflow-overlay/README.md` and follow the Orca overlay. Treat `AGENTS.md` as triggers and global behavior, not as the full workflow manual.

Keep Orca project facts, source hierarchy, source-loading rules, artifact folders, review lanes, validation gates, safety rules, prompt rules, and lifecycle boundaries in `.agents/workflow-overlay/` or another Orca-owned source named there.

For substantial, ambiguous, cross-thread, delegated, doctrine-changing, review/patch-affecting, infrastructure-building, or messy-worktree work, run the Orca Cynefin Routing Layer before planning or delegation; the owning rule is `.agents/workflow-overlay/decision-routing.md`.

Author every prompt, handoff, wrapper, rerun, or patch prompt through the `workflow-prompt-orchestrator` skill — which owns prompt source-loading and the preflight/routing contract — and never hand-draft them; the owning rule is `.agents/workflow-overlay/prompt-orchestration.md`.

When starting or "spinning up" a new unit of repo-changing work, decide and state the isolation before editing: use a worktree off `main` for writing work that runs alongside other active lanes or on a dirty base; a branch off `main` for solo, sequential writing; and neither for read-only work. Land changes via the per-lane PR flow in `docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md`.

Do not treat `jb` rules, paths, handoffs, lifecycle mechanics, product policy, validation habits, or external workflow source as Orca authority. Explicitly invoked or resolver-loaded skills may provide task-local mechanics only.

For doctrine-changing work, implementation boundaries, skill adoption, review lanes, validation, prompt orchestration, source loading, and delegated review-and-patch, load the owning overlay file instead of duplicating the rule here.

Default allowed work is documentation, decisions, prompts, reviews, migration notes, and overlay maintenance inside this workspace. Implementation or runtime work requires explicit bounded authorization in the current turn or accepted handoff.
