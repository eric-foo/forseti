# Cynefin Routing Layer

```yaml
retrieval_header_version: 1
artifact_role: Orca overlay authority
scope: Lightweight Cynefin-based pre-planning router for non-trivial Orca work.
use_when:
  - Deciding whether to plan, delegate, review, patch, or implement.
  - Starting substantial, ambiguous, cross-thread, or doctrine-bearing work.
  - Recovering a drifting or messy workstream before more agents act.
authority_boundary: retrieval_only
```

This file owns Orca's lightweight Cynefin Routing Layer. It prevents agents
from planning or delegating before they have classified the uncertainty regime,
named the current constraint, and chosen a safe next move.

## Rule

Run Cynefin routing before planning, delegation, prompt execution, review,
patching, or infrastructure work when the task is non-trivial and could fail
because the wrong decomposition strategy is chosen.

Use the smallest complete router. This is not a full Bayesian planning system,
audit log, review lane, validation gate, or project-management ritual. It is a
short preflight that constrains the next move.

## Trigger Conditions

Run the router when any of these are true:

- the user asks for architecture, planning, scoping, route selection, or the
  next move;
- the user asks to spawn agents, delegate work, execute a prompt, perform
  review, apply a patch, or commission another lane;
- the task references another thread as evidence or continuity context;
- the task touches `AGENTS.md`, the Orca overlay, prompt templates, review
  lanes, validation gates, source hierarchy, or durable workflow doctrine;
- the task would build infrastructure before a material assumption has been
  proven;
- the worktree, source map, or ownership boundary is dirty enough that a safe
  commit, patch, or claim boundary is unclear;
- the current thread shows drift: many artifacts or actions, unclear
  bottleneck, weak convergence, or no visible stop condition.

## Bypass Conditions

Do not run the router for narrow, clear, already-scoped work:

- tiny edits, typo fixes, or mechanical formatting;
- direct command answers;
- already accepted implementation steps with bounded touch points and validation;
- narrow doc cleanup where ownership is obvious;
- simple bug fixes with an obvious test path and no doctrine or review impact.

If bypassing could be contested, state a one-line bypass reason before acting.

## Router Output

Use compact headed prose, not YAML. The output should be readable in chat:

```text
Smallest complete outcome: What fully satisfies the actual request without extra scope.
Regime: Clear / Complicated / Complex / Chaotic / Mixed or Unclear.
Why: One sentence.
Decomposition: Functional, layer-based, risk-first probe, stabilize first, or split and classify.
Current bottleneck: The concrete constraint that should govern WIP.
Riskiest assumption: The assumption most likely to change the route.
Stop or pivot condition: The evidence that would make the current route wrong.
Allowed next move: What may happen next.
Disallowed next move: What must not happen next.
```

When the router is intentionally skipped, use one plain line:

```text
Cynefin bypass: <why this is narrow, clear, or already scoped>.
```

## Regimes

`clear`: the task is understood, bounded, and mechanically executable.
Use functional decomposition or direct execution.

`complicated`: the task needs expertise, source hierarchy, or layered ownership,
but the target can be reasoned through from current sources.
Use layer-based decomposition.

`complex`: key assumptions are uncertain, evidence could change the route, or
building first would create fragile infrastructure.
Use risk-first probes. Resolve the highest-uncertainty assumption before
expanding implementation or delegation.

`chaotic`: state is too unstable to plan safely, usually because scope, source
truth, repo state, or authority is disordered.
Stabilize first: classify dirty state, bind authority, narrow the target, or
name the hard stop before any broader task tree.

`mixed or unclear`: the request contains multiple regimes, or the regime cannot
be classified without first separating the work.
Split the task into regime-specific parts before planning. Do not force one
label when the first safe move is to separate the problem.

## Execution Contract

The router must produce an allowed next move and a disallowed next move before
planning continues. The disallowed move is load-bearing: it prevents the agent
from turning spare capacity into non-bottleneck work.

The smallest complete outcome is also load-bearing. It names what would satisfy
the actual request, so correct classification does not become permission for
extra cleanup, adjacent refactors, broader prompt sweeps, or infrastructure.

The bottleneck and stop-or-pivot condition must be concrete enough to govern
action. Do not write vague bottlenecks such as "uncertainty" or vague stops such
as "if it seems too hard." Name the specific unknown, evidence, failure signal,
owner decision, source gap, or boundary breach that changes the route.

For complex work, the allowed next move should normally be a probe, source read,
owner decision, scoped contract, or narrow adapter/surface step that resolves
the riskiest assumption. Do not estimate end dates or build infrastructure
around unproven assumptions.

For chaotic work, do not assign parallel work until the bottleneck is visible.
Idle agents are acceptable when non-bottleneck work would increase WIP or blur
claim boundaries.

## Enforcement Placement

Routing also governs *how* a rule is enforced, not only how the next move is
chosen: a load-bearing rule that is mechanically checkable at a tool boundary
belongs in a deterministic substrate (hook, gate, or checker) at that boundary,
not in an actor-carried instruction that fires only when the model attends to
it. This principle, the per-rule classification, and the active instances are
owned by `.agents/workflow-overlay/validation-gates.md` (-> "Enforcement
Placement") and
`docs/decisions/overlay_enforcement_placement_classification_v0.md`; reserve
resident instruction for genuinely judgment-based rules.

## Subagent Runtime Payload Safety

For forked-context subagents, inherited runtime defaults mean omitted fields.
Do not set `agent_type`, `model`, `reasoning_effort`, `service_tier`, or
equivalent runtime fields to `default`, `null`, empty, or same-as-parent. If a
forked spawn is rejected for explicit type/model fields, retry with only
`fork_context: true` and the task `message` or `items`; if an override is
required, use a bounded source capsule instead of full-history fork or stop for
the owner/tooling decision.

## Prompt Propagation

Repo-aware prompts, wrappers, handoffs, review prompts, patch prompts, and
reruns must include Cynefin routing when their task matches the trigger
conditions. Prompt artifacts should reference this file instead of restating
the whole router.

## Subagent Model Tiering

When delegating to a spawned subagent, choose the model tier per
`docs/decisions/subagent_model_tiering_doctrine_v0.md`.

In Claude Code, default delegable work to the Sonnet `worker` agent type;
trivial rote to the Haiku `mechanical` type; reserve Opus (`general-purpose`,
which inherits the main tier, or an explicit `model: opus`) for genuine
judgment. A subagent spawned with no model silently inherits the parent (Opus)
tier, so route to a pinned type to avoid paying Opus for non-judgment work. Do
not set `CLAUDE_CODE_SUBAGENT_MODEL` (it hard-caps all subagents and blocks
Opus escalation — over-restraint).

In Codex, classify the delegated task before the `spawn_agent` call:
mechanical/trivial rote, ordinary delegated work, or genuine judgment. Choose
any explicit model override from the current tool surface only after checking
that the name is actually available in the current session; otherwise omit the
override or stop for an owner/tooling decision. `agent_type` remains a role
selector (`explorer`, `worker`, or omitted), not the model tier. Do not turn a
dated observed model list into durable routing doctrine.

Model tiering does not imply source loading. A spawned subagent does not
automatically read lane playbooks or overlay sources because it is called a
capture worker, explorer, or judgment lane. For any subagent output the chief
architect will consume, the dispatch must provide forked context, a bounded
source capsule, or explicit required reads plus the source-readiness and
return-shape contract in `.agents/workflow-overlay/prompt-orchestration.md`.

## Non-Claims

Cynefin routing is not validation, readiness, approval, acceptance, review,
implementation authorization, source-of-truth promotion, or proof that a route
will work. It is a pre-planning constraint on how the next move is chosen.
