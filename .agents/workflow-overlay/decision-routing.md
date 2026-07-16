# Cynefin Routing Layer

```yaml
retrieval_header_version: 1
artifact_role: Forseti overlay authority
scope: Lightweight Cynefin-based pre-planning router and receiver-mechanism selector for uncertainty-sensitive Forseti work.
use_when:
  - A material uncertainty could change decomposition, authority, source truth, or safe sequencing.
  - The user explicitly asks for Cynefin or uncertainty-regime classification.
  - Recovering a drifting or messy workstream before more agents act.
  - Selecting a writable receiver before delegated or parallel repo-changing work.
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
already bounded, proceed without a full-router artifact. An explicit `/fused`
invocation supersedes the `AGENTS.md` five-phase fast path for that work unit;
a continuation that only executes already-cleared fused lanes runs under the
fast path.

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

## One-Time Writable-Root Binding

At the first repo-changing act, select and bind one effective target: neither
branch nor worktree for read-only work; a current-checkout branch for clean
solo/sequential writing; and a worktree off the required base for dirty-base,
concurrent, or independent work.

The current actor may continue the same commissioned work unit directly in its
selected worktree after one fresh snapshot records the exact target path,
revision and dirty state, and whether another writer is active. Launch checkout
and target worktree need not match. Launch-root mismatch alone is not a blocker.
A separate receiver is required only for an independent concurrent actor or
after an observed tool, sandbox, hook, or guard denial proves the current task
cannot perform a required target operation.

Reuse this binding through authoring, review, validation, commit, push, and
landing. Do not repeat root receipts, chat choreography, hook canaries, synthetic
write/index probes, or capability recitals while material state is unchanged.
Re-resolve only when the actor or target changes, revision or dirty state changes
materially, another writer appears, or a real required-tool failure invalidates
the binding. Preserve that failure.

Receiver classes remain available where another actor needs a binding:

- `codex_managed_worktree`: a new independent Codex task explicitly authorized
  and created in its managed worktree with the commission in its initial prompt;
- `external_direct_write`: an independent external controller verified once for
  exact target, direct write capability, and no concurrent writer;
- `collaboration_same_root`: an in-session subagent inside the caller's writable
  root; naming another path cannot expand it; and
- `receiver_to_bind`: preparation-only until a concrete receiver is authorized.

An independent delegate writing a separate worktree needs its own capable
receiver. This does not apply when the current actor creates or selects isolation
for the same commissioned work unit. Stop or reroot only for ambiguous target
identity, revision or dirty-byte mismatch, concurrent writing, an observed
required-tool denial or root-bound feature mismatch, or a protected-action or
server-side guard.

For a genuinely new, external, or changed receiver, record one compact
`receiver_binding`; unchanged same-lane prompts point to the active binding:

```yaml
receiver_binding:
  receiver_class: codex_managed_worktree | external_direct_write | collaboration_same_root | receiver_to_bind
  binding_state: receiver_to_bind | receiver_to_verify | receiver_verified | blocked
  launch_checkout: "<observed path | receiver_to_observe>"
  effective_target_worktree: "<observed path>"
  managed_starting_ref: "<bound ref, only before a managed task exists>"
  required_revision: "<commit>"
  revision_mode: exact | ancestor
  capability_proof: "<only when new or genuinely unknown>"
  no_concurrent_writer_state: "<required for an independent writer>"
```

`exact` means a clean worktree whose `HEAD` equals `required_revision`.
`ancestor` means a clean advancing lane where
`git merge-base --is-ancestor <required_revision> HEAD` succeeds. Dirty work
still requires the named dirty-file set plus byte identity. Existing exact gates
remain exact.

Creating a user-visible Codex task still requires explicit product/user
authorization. A visible instruction to create, start, spin up, or hand off to a
new managed task is sufficient. A durable commission may carry the bounded
`receiver_creation_authorization` owned by `prompt-orchestration.md`. Generic
`proceed`, ordinary implementation authority, and read-only/scoping/review work
do not create that authority; a task's mere existence is never authority.

When a real pre-edit mismatch invalidates the binding, route to an already-
authorized capable receiver when one exists, including a valid one-task creation
authorization without chat-double-asking. Return
`BLOCKED_RECEIVER_REROOT_REQUIRED` only when target identity, revision or dirty-
byte identity, writer isolation, or required capability cannot be established,
no authorized capable route exists, or the one allowed creation fails. Capable
means able to perform the required operation against the exact target while the
state checks hold; it does not require launch-root equality.

The live-adoption canary remains documented in `.agents/hooks/README.md` only
for work commissioned to test hook adoption; ordinary work does not run it.

This rule does not authorize automatic task creation without product/user
authority, destructive Git, concurrent writers, ignored dirty state, weakened
revision pins, or bypass of protected-action or server-side guards.

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

For a newly created Codex cold receiving/handoff thread, explicitly set
`thinking: high` on `create_thread`; do not default the receiving thread to
`xhigh`. Keep the model omitted unless the owner separately requests a model
override. Moving an existing thread with `handoff_thread` cannot change its
reasoning effort because that surface exposes no effort field; preserve the
existing setting and do not claim otherwise.

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
test count — test-fix loops, batch normalizations, CI polling, bulk file edits.
First apply Receiver Mechanism And Write-Root Selection above: read-only or safe
same-root work may use a pinned `worker` or `mechanical` subagent (per Subagent
Model Tiering above), while an independent repo-changing lane uses a receiver
launched in its worktree or an independent external controller that completes
the two-root capability preflight. Give the selected receiver a narrow contract:
target path(s), exact commands, acceptance condition, and return shape. Bulk
intermediate output (test dumps, batch listings, poll output) stays in the
receiver; only a compact summary returns to the orchestrator context. This is a
heuristic for context economy, not a mechanical gate.

Judgment work — adjudication, doctrine wording, contract design, anything
where the orchestrator's accumulated context materially improves the output —
stays inline. The binding constraint on dispatch is judgment fidelity, not
token math.

## Non-Claims

Cynefin routing chooses a safe next-move posture. It is not review or proof that
the route will work, and it does not validate, establish readiness, authorize,
or promote the underlying work to source-of-truth status.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Repo-changing work now selects isolation at the first write, binds the task's
    registered root once, and reuses that sole writable root through landing.
    Same-lane prompts point to the active binding; exact root and capability
    details recur only for a new, external, or materially changed receiver or
    genuinely unknown capability. The registered cross-worktree guard remains
    fail-closed as the backstop, while synthetic write/index probes and routine
    hook canaries are retired.
  trigger: workflow_authority
  related_triggers: [validation_philosophy, output_authority, lifecycle_boundary]
  controlling_sources_updated:
    - .agents/workflow-overlay/decision-routing.md
    - .agents/workflow-overlay/prompt-orchestration.md
    - .agents/workflow-overlay/validation-gates.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/hooks/README.md
    - docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
    - docs/prompts/templates/shared/forseti_preflight_defaults_v0.md
    - forseti-harness/tests/unit/test_ci_hook_wiring.py
    - .codex/hooks/forseti_guard_codex_adapter.py
  downstream_surfaces_checked:
    - AGENTS.md
    - CLAUDE.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/safety-rules.md
    - .codex/hooks.json
    - .agents/hooks/guard_protected_actions.py
    - .agents/hooks/check_prompt_output_mode.py
    - docs/workflows/forseti_repo_map_v0.md
  intentionally_not_updated:
    - {path: AGENTS.md and CLAUDE.md, reason: "The kernel and shim already route isolation and receiver binding to the owning overlay; repeating the detailed one-time-binding contract would fork authority."}
    - {path: .agents/hooks/guard_protected_actions.py and .codex/hooks.json, reason: "The registered cross-worktree guard's conditions, authorization, wiring, and fail-closed enforcement remain unchanged."}
    - {path: .agents/hooks/check_prompt_output_mode.py, reason: "Its receiver-binding fields remain required for the still-valid new managed-receiver and external delegated-courier shells, not same-lane repetition."}
    - {path: docs/workflows/forseti_repo_map_v0.md, reason: "No source location, precedence, or live-router ownership changed."}
    - {path: docs/decisions/archive/direction_change_propagation_log_v0.md, reason: "The archive is frozen history and receives no new entries."}
  stale_language_search: >
    rg -n -i "lane-start write|write/index probe|live adoption probe|live-adoption-probe|receiver_binding|capability proof|no-concurrent-writer|BLOCKED_RECEIVER_REROOT_REQUIRED|command-level.{0,30}workdir|sole writable root"
    AGENTS.md CLAUDE.md .agents/workflow-overlay .agents/hooks/README.md .codex/hooks
    docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
    docs/prompts/templates/shared/forseti_preflight_defaults_v0.md docs/workflows/forseti_repo_map_v0.md
    .agents/hooks/check_prompt_output_mode.py forseti-harness/tests/unit/test_ci_hook_wiring.py
  stale_language_search_result: >
    Executed 2026-07-16 against the owning overlay, prompt defaults, hook docs,
    adapter, prompt checker, doctrine, repo map, and focused contract test.
    Live normative hits are the new one-time binding, its same-lane versus
    new/external receiver split, and the preserved fail-closed reroute blocker.
    The prompt checker intentionally retains receiver_binding for new managed or
    external receiver shells. Historical inline DCP receipts retain their dated
    probe/canary wording, and --live-adoption-probe remains available only when a
    hook adoption test is itself commissioned. The adapter denial now points to
    the active binding or an already-authorized capable worktree-backed task.
    No live authority requires routine lane-start write/index probes, repeated
    root receipts, or command-workdir rerooting.
  non_claims:
    - not validation or readiness
    - not automatic task creation when the product or user has not authorized it
    - not cross-worktree write authority or permission for concurrent writers
    - not permission for destructive Git or ignoring dirty-state changes
    - not permission to weaken target-revision pins or bypass the registered-worktree guard
    - not proof that any receiver, provider, or controller has the claimed capability
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    Fresh Codex protected-gate commissions now automatically use a correctly
    rooted managed task, prove live project-hook adoption through one fail-closed
    top-level probe, and bind clean exact/ancestor revision semantics without
    weakening any exact gate.
  trigger: workflow_authority
  related_triggers: [validation_philosophy, lifecycle_boundary]
  controlling_sources_updated:
    - .agents/workflow-overlay/decision-routing.md
    - .agents/workflow-overlay/validation-gates.md
  downstream_surfaces_checked:
    - AGENTS.md
    - CLAUDE.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/safety-rules.md
    - .agents/workflow-overlay/prompt-orchestration.md
    - .agents/hooks/README.md
    - .codex/hooks.json
    - .codex/hooks/forseti_guard_codex_adapter.py
    - forseti-harness/tests/unit/test_ci_hook_wiring.py
    - docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
    - docs/prompts/templates/shared/forseti_preflight_defaults_v0.md
    - docs/workflows/efficiency/tool_calling_efficiency_improvement_sequence_2026_07_15_v0.md
    - docs/workflows/forseti_repo_map_v0.md
  intentionally_not_updated:
    - path: .agents/workflow-overlay/README.md
      reason: >
        Decision-routing and validation-gates remain the existing owners; no
        overlay section or owner changed.
    - path: .agents/workflow-overlay/source-of-truth.md
      reason: Source precedence and doctrine-propagation mechanics are unchanged.
    - path: .agents/workflow-overlay/source-loading.md
      reason: >
        It already requires receiver selection and managed-root verification
        before source loading. The live canary occurs later, before a protected
        gate, so restating it here would duplicate authority.
    - path: .agents/workflow-overlay/safety-rules.md
      reason: >
        The authorization boundary and protected-action policy are unchanged;
        this patch proves hook adoption without granting new edit scope.
    - path: .agents/workflow-overlay/prompt-orchestration.md
      reason: >
        It already creates explicitly authorized managed tasks with the initial
        commission, rejects self-rerooting, and distinguishes exact pins from
        permitted ancestry. Decision-routing now owns the precise revision and
        live-canary assertions; no conflicting prompt route remains.
    - path: .codex/hooks.json
      reason: >
        The existing PowerShell/Bash PreToolUse registration already reaches the
        adapter; the probe changes adapter behavior, not hook topology.
    - path: docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
      reason: >
        Its managed-root write/index probe and protected-action boundary remain
        compatible and unchanged.
    - path: docs/prompts/templates/shared/forseti_preflight_defaults_v0.md
      reason: >
        It already requires prompts to state exact-pin versus required-ancestry
        semantics and defers receiver mechanics to prompt-orchestration.
    - path: docs/workflows/forseti_repo_map_v0.md
      reason: >
        Existing routes already point receiver selection and validation to the
        changed owners and hook wiring to the existing README; no path family or
        owner changed.
    - path: AGENTS.md and CLAUDE.md
      reason: >
        AGENTS.md already routes receiver selection, validation, and hook
        mechanics to their owners; CLAUDE.md remains its compatibility shim.
  stale_language_search: >
    rg -n -i "live-adoption-probe|hook.adoption|not_intercepted|workdir.{0,60}(receiver|worktree)|revision_mode|exact.{0,50}ancestor|ancestor.{0,50}exact|managed.worktree"
    AGENTS.md CLAUDE.md .agents/workflow-overlay .agents/hooks/README.md .codex/hooks
    docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
    docs/prompts/templates/shared/forseti_preflight_defaults_v0.md
    docs/workflows/forseti_repo_map_v0.md
    forseti-harness/tests/unit/test_ci_hook_wiring.py
    docs/workflows/efficiency/tool_calling_efficiency_improvement_sequence_2026_07_15_v0.md
  stale_language_search_result: >
    Executed 2026-07-15 after edits. Defining probe, revision, and workdir hits
    are confined to decision-routing, validation, adapter/wiring documentation,
    focused regression assertions, and the observed efficiency ledger. Prompt
    orchestration retains the compatible managed-root and exact-versus-ancestry
    route; source-loading retains the compatible pre-source receiver check. No
    checked surface authorizes a base-root task plus workdir override, persists
    adoption state, treats ancestry as an exact pin, or claims Forseti can create
    Codex trust.
  non_claims:
    - not validation
    - not readiness
    - not automatic task creation without explicit user intent
    - not persisted trust or adoption state
    - not a Forseti-owned Codex task or trust API
    - not a weakening of existing exact or protected-action gates
```

Older receipts archived verbatim in `docs/decisions/dcp_receipts_archive_v0.md`.
