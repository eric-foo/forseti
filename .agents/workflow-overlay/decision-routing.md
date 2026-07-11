# Cynefin Routing Layer

```yaml
retrieval_header_version: 1
artifact_role: Forseti overlay authority
scope: Lightweight Cynefin-based pre-planning router for uncertainty-sensitive Forseti work.
use_when:
  - A material uncertainty could change decomposition, authority, source truth, or safe sequencing.
  - The user explicitly asks for Cynefin or uncertainty-regime classification.
  - Recovering a drifting or messy workstream before more agents act.
authority_boundary: retrieval_only
```

This file owns Forseti's lightweight Cynefin Routing Layer. It regulates work
when uncertainty about decomposition, authority, source truth, or sequencing
could materially change the next move.

## Rule

Run the full router only when the task is plausibly `complex`, `chaotic`, or
`mixed or unclear`, or when a `complicated` task contains a concrete unresolved
choice that could materially change decomposition, authority, or safe sequence.
Clear work and ordinary complicated work with a bound outcome, authority, and
route proceed directly.

Use the smallest complete router. This is not a full Bayesian planning system,
audit log, review lane, validation gate, or project-management ritual. It is a
short preflight that constrains the next move.

## Trigger Conditions

Run the full router when either condition is true:

- the user explicitly invokes Cynefin routing or asks for uncertainty-regime
  classification; or
- a material unknown could change the route, such as an unverified assumption
  that controls architecture or infrastructure, conflicting source/authority,
  an unclear ownership or dirty-state boundary, competing decompositions with
  different lock-in, or a drifting workstream with no visible bottleneck or
  stop condition.

Architecture, planning, scoping, delegation, cross-thread continuity, review,
patching, doctrine work, and messy worktrees are escalation cues because they
often contain those unknowns. They are not sufficient triggers by themselves.
If the outcome, authority, sources, touch points, and validation route are
already bounded, proceed without a full-router artifact.

## Bypass Conditions

Do not run the full router for clear or ordinary complicated work whose route is
already bounded, including:

- tiny edits, typo fixes, or mechanical formatting;
- direct command answers;
- already accepted implementation steps with bounded touch points and validation;
- narrow doc cleanup where ownership is obvious;
- simple bug fixes with an obvious test path;
- bounded review, doctrine, delegation, or prompt work whose controlling source,
  authority, target, and stop condition are already known.

Do not emit a bypass receipt. Surface a routing assumption only when it is risky
or genuinely ambiguous under `AGENTS.md`.

## Router Output

When the full router triggers, use compact headed prose:

```text
Smallest complete outcome: What fully satisfies the request without extra scope.
Regime and why: Complex / Chaotic / Mixed or Unclear / materially unresolved Complicated.
Current bottleneck and riskiest assumption: The constraint and unknown governing WIP.
Allowed next move: The next probe, source read, decision, or bounded action.
Stop or pivot condition: The evidence that would make the current route wrong.
Disallowed next move: What must not happen next.
```

Keep this internal when it only regulates the current actor. Put it in chat or a
durable prompt when the route itself is decision-bearing, another lane must
inherit it, or the user asks to see it.

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

When the full router triggers, it must produce an allowed next move and a
disallowed next move before planning continues. The disallowed move prevents
spare capacity from becoming non-bottleneck work.

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
reruns include Cynefin routing only when the full-router conditions above
trigger. Prompt artifacts should reference this file instead of restating the
router.

## Subagent Model Tiering

When delegating to a spawned subagent, choose the model tier per
`docs/decisions/subagent_model_tiering_doctrine_v0.md`. The same doctrine also
owns the session-lane tier defaults for delegated review lanes (its
"Session-lane tier defaults" section).

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

## Orchestrator Context Economy

In a long-running orchestrator or Chief Architect thread, every token that
enters the context is re-read by every subsequent call: orchestrator cost is
context size times remaining calls, so bulk output that lands early is paid
for hundreds of times.

Dispatch, do not inline, any mechanical work loop expected to take more than a
few (~4+) tool round-trips whose success is verifiable by exit code, diff, or
test count — test-fix loops, batch normalizations, CI polling, bulk file
edits. Route it to a pinned `worker` or `mechanical` subagent (per Subagent
Model Tiering above) with a narrow contract: target path(s), exact commands,
acceptance condition, and return shape. Bulk intermediate output (test dumps,
batch listings, poll output) stays in the subagent; only a compact summary
returns to the orchestrator context. This is a heuristic for context economy,
not a mechanical gate.

Judgment work — adjudication, doctrine wording, contract design, anything
where the orchestrator's accumulated context materially improves the output —
stays inline. The binding constraint on dispatch is judgment fidelity, not
token math.

## Non-Claims

Cynefin routing chooses a safe next-move posture; it does not validate or
authorize the underlying work.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Added the Orchestrator Context Economy rule: long-running orchestrator/CA
    threads dispatch mechanical loops (more than a few verifiable tool
    round-trips) to pinned worker/mechanical subagents with narrow contracts;
    bulk intermediate output returns as a compact summary only; judgment work
    stays inline.
  trigger: workflow_authority
  controlling_sources_updated:
    - .agents/workflow-overlay/decision-routing.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-loading.md
    - docs/workflows/orca_repo_map_v0.md
  intentionally_not_updated:
    - path: AGENTS.md
      reason: >
        AGENTS.md already routes delegated work to decision-routing.md; the new
        subsection is discovered on that existing mandatory path. No kernel
        change needed.
    - path: .agents/workflow-overlay/README.md
      reason: >
        The overlay index already names decision-routing.md for delegated-work
        routing; no section-owner change.
    - path: .agents/workflow-overlay/source-loading.md
      reason: >
        Its fresh-lane-over-compact trigger is thread-lifecycle doctrine with
        its own receipt; the dispatch rule lives here only, per the anti-fork
        rule.
    - path: docs/workflows/orca_repo_map_v0.md
      reason: >
        The repo map references decision-routing.md at file level; no section
        anchors into this file changed (checked 2026-07-02).
  stale_language_search: >
    rg -in "mechanical loop|context economy|dispatch.*mechanical|orchestrator context"
    AGENTS.md .agents/workflow-overlay/
  stale_language_search_result: >
    Executed 2026-07-02 after edits. The only hits are the new Orchestrator
    Context Economy section itself; no other surface carries a conflicting or
    duplicate dispatch rule.
  non_claims:
    - not validation
    - not readiness
    - no token-savings efficacy claim
```

Older receipts archived verbatim in `docs/decisions/dcp_receipts_archive_v0.md`.
