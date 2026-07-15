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

## Receiver Mechanism And Write-Root Selection

Before dispatching delegated or parallel work, classify the commissioned act
and bind exactly one receiver class before the receiver loads task sources:

When a visible Codex Desktop instruction explicitly asks for a fresh launcher,
new managed task, or live proof that a project hook protects a repo-changing
gate, receiver selection is automatic: use a newly created
`codex_managed_worktree` carrying the commission in its initial prompt. A task
rooted at a local/base checkout is not a substitute, even if an individual
shell call supplies the intended worktree through a command-level `workdir`.
If the visible instruction does not authorize creating a task, keep
`receiver_to_bind`; automatic receiver selection does not invent task-creation
authority or a repository-owned Codex task API.

- `codex_managed_worktree`: an independent repo-changing Codex task created by
  Codex Desktop in its managed worktree, with the initial commission submitted
  in the same task-creation flow. The dispatcher binds the requested starting
  ref (normally `origin/main`); the receiver then verifies that its launch
  checkout is that app-created managed worktree, checks the ref/state, and runs
  the existing lane-start write/index probe before source loading. It must not
  create, discover, or target a second worktree as a substitute for its root.
- `external_direct_write`: a true independent external controller whose harness
  may start from another checkout and operate on a separately commissioned
  worktree only after the two-root identity, direct-write, and no-concurrent-
  writer proofs below pass.
- `collaboration_same_root`: an in-session collaboration subagent used for
  read-only work or for a safe contribution inside the calling task's current,
  already-isolated work unit. It is not a separately rooted repo-changing lane
  and cannot become one merely because a prompt names another worktree.
- `receiver_to_bind`: the future receiver is not known or created yet. Prompt
  preparation may continue, but dispatch readiness and receiver source loading
  remain blocked until one of the three concrete classes is bound and verified.

Record the binding once, inline in the commission or courier, using this compact
receipt; do not create a registry, daemon, standalone receipt artifact, or new
checker:

```yaml
receiver_binding:
  receiver_class: codex_managed_worktree | external_direct_write | collaboration_same_root | receiver_to_bind
  binding_state: receiver_to_bind | receiver_to_verify | receiver_verified | blocked
  launch_checkout: "<observed path | receiver_to_observe>"
  effective_target_worktree: "<observed path>" # omit only while a managed task is not yet created
  managed_starting_ref: "<origin/main or other bound ref>" # use instead while receiver_class is codex_managed_worktree and binding_state is receiver_to_verify
  required_revision: "<commit>" # required with revision_mode for a clean repo-changing receiver
  revision_mode: exact | ancestor # omit only for read-only or manifest-bound dirty work
  capability_proof: "<write/index proof, direct-write proof, read-only, or not_yet_proven>"
  no_concurrent_writer_state: "<observed state, not_applicable_read_only, or not_yet_proven>"
```

The two target fields are alternatives during preparation: a not-yet-created
managed task carries `managed_starting_ref`; a created or otherwise resolved
receiver carries `effective_target_worktree`. A `receiver_verified` repo-
changing receipt must carry the observed effective target, capability proof,
and no-concurrent-writer state.

Revision modes are explicit and non-interchangeable. `exact` means the
worktree is clean and `HEAD` equals `required_revision`. `ancestor` means the
worktree is clean and `git merge-base --is-ancestor <required_revision> HEAD`
exits zero. Use `exact` for a pinned review/diff, reproducibility gate, or any
commission that names exact bytes; every existing exact gate remains exact.
Use `ancestor` only for an intentionally advancing clean lane whose commission
requires a prerequisite commit while permitting later commits. Dirty work
continues to require the existing named dirty-file set plus manifest/byte
identity and is not relabeled as either clean revision mode.

For a `codex_managed_worktree` that will rely on the tracked project
`PreToolUse` hook before a protected gate, the live canary is mandatory after
root/revision verification and before the first protected action. From the
task root, make this exact top-level tool call with no command-level `workdir`:

```powershell
python .codex/hooks/forseti_guard_codex_adapter.py --live-adoption-probe
```

The live hook must deny the tool call with exactly
`FORSETI_CODEX_HOOK_ADOPTION=ADOPTED`. If the hook is absent or unloaded, the
command executes directly, exits nonzero, and emits exactly
`FORSETI_CODEX_HOOK_ADOPTION=NOT_INTERCEPTED`. The observed result is the
adoption state; do not persist a trust/adoption field, wrap the command, infer
success from latency, or edit Codex trust metadata. A changed hook that needs a
normal Codex trust/reload action remains blocked until Codex surfaces and the
user completes that product-owned action.

Treat the receiver's starting checkout and the commissioned source as separate
facts:

- `launch_checkout` is where the receiving session starts;
- `effective_target_worktree` is the unique registered worktree containing the
  exact commissioned bytes.

Before expensive source loading, the dispatcher or receiver completes the
class-specific preflight. `codex_managed_worktree` verifies its app-created
current root directly and requires launch/target equality. It does not search
the worktree registry for somewhere else to write. `external_direct_write`
runs the smallest complete two-root preflight: record the commissioned act and
launch checkout; resolve the unique effective target through the worktree
registry; verify its branch/revision and allowed dirty state; and, for
uncommitted work, verify the named dirty-file set plus a target manifest or
equivalent byte identity. `collaboration_same_root` verifies that any permitted
write stays in the calling task's current isolated root. A branch and HEAD alone
do not identify dirty work, and checking that branch out elsewhere is not a
substitute.

Repo-changing work additionally requires demonstrated write capability to the
effective target and confirmation that no other actor will write it during the
delegated pass. A path or successful read is not write-capability proof. Use the
existing lane-start write/index probe for `codex_managed_worktree` and
harness/tool direct-write evidence for `external_direct_write`. A prepared
prompt may leave receiver-only observations as `receiver_to_observe`, but it
must remain `receiver_to_bind` or `receiver_to_verify` until the receiver fills
them before source loading.

Creating a user-visible Codex task still requires explicit user authorization,
but authorization is semantic rather than a magic phrase: a visible instruction
that explicitly asks to create, start, spin up, or hand off to a new Codex task
or managed worktree satisfies it, and the task is created with its initial
commission in that same operation. Generic `proceed` by itself does not silently
authorize task creation, and no instruction grants standing creation authority
beyond the task or handoff it places in scope. Do not chat-double-ask when the
visible instruction already supplies that explicit intent.

Only `external_direct_write` may operate when launch and target differ. After
the exact target and capability are proven, use target-rooted tool workdirs,
absolute paths, and `git -C <effective_target_worktree>`; do not reconstruct its
dirty state in the launch checkout. Recheck target identity immediately before
the first edit and stop as `BLOCKED_TARGET_DRIFT_DURING_REVIEW` if it changed.

A local/base-rooted Codex task plus command-level `workdir` substitution is
never `external_direct_write` and never a valid repo-changing receiver. The
override changes one command's process directory; it does not change the task
root, project-hook root/trust decision, sandbox write root, or receiver
identity.

Return `BLOCKED_RECEIVER_REROOT_REQUIRED` only for a genuine binding or
capability failure: the target is missing or ambiguous, its bytes do not match,
required write capability is absent, concurrent writing cannot be excluded, or
a guard requires a target-rooted receiver that the current task is not. If a
Codex task was launched in the wrong checkout, it must not create or find another
worktree and then attempt an impossible reroot. The recovery action is a newly
created, owner-authorized `codex_managed_worktree` task carrying the commission
in its initial prompt. Do not bypass or weaken the protected-action guard. The
write-boundary enforcement and lane-start write/index probe remain owned by
`.agents/hooks/README.md` and
`docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md`.

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
    Repo-changing dispatch now binds one of four receiver classes before source
    loading: Codex managed tasks are created in their managed worktree with the
    initial commission, external controllers retain the proven two-root route,
    collaboration stays same-root, and unknown couriers remain preparation-only.
  trigger: workflow_authority
  related_triggers: [output_authority, lifecycle_boundary]
  controlling_sources_updated:
    - .agents/workflow-overlay/decision-routing.md
    - .agents/workflow-overlay/prompt-orchestration.md
    - .agents/workflow-overlay/validation-gates.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/hooks/README.md
    - .codex/hooks.json
    - .codex/hooks/forseti_guard_codex_adapter.py
    - docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
    - docs/workflows/forseti_repo_map_v0.md
    - CLAUDE.md
  intentionally_not_updated:
    - {path: AGENTS.md, reason: "The kernel already points receiver selection to this file and states the same external-controller and collaboration boundaries."}
    - {path: .agents/workflow-overlay/source-loading.md, reason: "It already requires receiver selection before source loading; class mechanics stay in the routing owner."}
    - {path: .agents/hooks/README.md and .codex/hooks/forseti_guard_codex_adapter.py, reason: "The Codex non-current-worktree denial remains intentionally fail-closed; dispatch now supplies the correctly rooted receiver."}
    - {path: docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md, reason: "The existing managed-root write/index probe remains the capability gate without implementation change."}
    - {path: docs/workflows/forseti_repo_map_v0.md and CLAUDE.md, reason: "No owner, path, or shim behavior changed."}
  stale_language_search: >
    rg -n -i "operator_to_fill.*(receiver|worktree|launch)|receiver_to_bind|receiver_to_verify|managed.worktree|self-created|find.*another worktree|reroot|required.*target-root|launch.checkout|effective_target_worktree|collaboration.*worktree|magic phrase"
    AGENTS.md CLAUDE.md .agents/workflow-overlay .agents/hooks/README.md .codex/hooks
    docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md docs/workflows/forseti_repo_map_v0.md
  stale_language_search_result: >
    Executed 2026-07-15 after the patch. Live routing, prompt, and validation
    hits carry the class-specific contract. Remaining reroot wording is confined
    to the unchanged fail-closed Codex adapter/readme and the generic sandboxed
    lane-start doctrine; those surfaces require opening/reopening on the active
    root and do not authorize a Codex task to write another registered worktree.
    AGENTS.md remains a compatible pointer to this controlling route.
  non_claims:
    - not validation or readiness
    - not automatic task creation from generic proceed
    - not a guard weakening or cross-worktree Codex write route
    - not permission for concurrent writers
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
