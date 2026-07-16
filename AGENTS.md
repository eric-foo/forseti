# AGENTS.md

## Agent Behavior Kernel

Surface a risky assumption or genuine ambiguity before acting -- but do not turn that into asking permission for a clear, reversible action you can already default; see Operating Economy.
Default to the smallest complete intervention: solve the actual request completely with the narrowest sufficient scope.
Every changed line must trace to the user request or required validation.
Preserve real failure visibility; never create fake success paths.
Treat untracked files as presumptively authored artifacts, never disposable scratch: confirm provenance or harvest before any destructive branch delete, worktree removal, or PR close.
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

Watch for ceremony debt: the recurring process cost a change installs when
it adds a required step, preflight, gate, receipt, field, checklist, sync
obligation, or review pass that every future work unit must pay. A change
that is small in diff can still carry a large recurring toll. That toll is
downstream lock-in under the rule below, not a free addition: prefer the
path that does not add it, and when the requested outcome genuinely needs
a recurring step, name what each future work unit pays and what real
defect class it catches so the owner can weigh the toll before it becomes
standing.

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
outcome and the condition under which it must hold. Measure completeness
against that outcome. Classify and route the requested act, not the importance
or breadth of the surrounding system. Context, importance, risk, and adjacent
weaknesses may change the evidence threshold; invoked lenses may deepen
reasoning. None of these may replace or expand the requested act.

For a narrow decision, give the decision and only the decisive rationale; if
materially useful, add one reversal condition. Do not design an alternative,
roadmap, policy, fallback, checklist, or operating model unless requested.
Once the decision is adequately supported, stop.

Before proposing a standing maintenance surface--such as an abstraction,
repository, automation, or lifecycle--state what part of the bound outcome
would become false or materially fragile without it, judged against that
outcome rather than a safer or more resilient downstream posture. If none,
exclude it; at most note a deferred risk and upgrade trigger. Include necessary
supporting work, and surface the tradeoff when it materially increases lock-in.

### Artifact-Level Smallest Complete Intervention

Create a separate durable artifact only when it serves a distinct future
consumer, outcome, or lifecycle that an existing artifact cannot serve without
becoming materially less usable. The artifact must be usable without
reconstructing the authoring chat and must name the material authority,
currentness, and next-source facts a future consumer needs to use it correctly.
Prefer updating the owning source and pointing to it over duplicating authority
or specifications; do not create speculative registries or maintenance
surfaces. When an artifact is materially touched, reconcile any affected
supersession, retirement, and live-router entries in the same work unit.

## Decision Priority

When multiple options already satisfy real failure visibility and Smallest
Complete Intervention, break the tie in this order:

1. **Least compounded risk** -- prefer the reversible, contained, low-lock-in
   option that fails loud and local; surface irreversible, high-lock-in, or
   doctrine-changing choices to the owner.
2. **Structural integrity** -- model reality truthfully; name a limitation
   instead of faking a fit, and prefer one true rule over a clever special case.

If these priorities conflict, choose recoverability and surface the tradeoff.

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
- **Separate credential failure from sandbox failure.** Do not ask the owner to
  reauthenticate from a `gh auth status`, API, keyring, or network failure
  observed only in a restricted sandbox or credential context. First repeat the
  smallest read-only authentication check in the per-operation escalated context
  used for GitHub actions. Ask for reauthentication only when that check
  independently reports missing or invalid credentials; report escalation or
  network denial as an access blocker, not an authentication failure. Never print
  credentials or tokens.
- **Open a circuit after one silent sandboxed tool stall.** Set a realistic
  timeout from expected command duration plus launch allowance; absent better
  evidence, use 20 seconds for reads or patches and 60 seconds for tests. If a
  call yields only a running/deferred handle with no output, wait at most once
  for any remaining original budget, then terminate it. Record one
  `sandboxed_tool_stall` for that failed tool-plus-permission route and do not
  probe the route again merely because the command differs. A user interruption,
  follow-up message, or automatic continuation does not reset an open circuit;
  if current context reports the stall, inherit it. Carry an open circuit's
  `sandboxed_tool_stall` record in any precompact or handoff packet so the
  receiving lane inherits it. Retry a safe in-scope operation at most once
  through a distinct approved route and reuse that working
  route for the task/thread. If the stalled operation might have written, inspect
  only its intended targets once before any alternate mutation. Then perform at
  most one bounded alternate mutation; `.agents/tools/atomic_exact_edit.py` is an
  option for short exact edits, not mandatory infrastructure. A transport or
  preflight rejection that proves no bytes changed may be corrected once or split
  into file-scoped atomic edits. Do not reroot, reload sources, create another task
  or worktree, or redo receiver ceremony because a tool stalled. Stop when the
  mutation outcome is unknown, target state drifted, another writer appeared, a
  real guard denied the action, or the distinct alternate route also stalls.
  Verify the final diff. Completion through an alternate route is mitigation, not
  proof that the ordinary tool route is repaired.
- **Load each skill once per thread.** A skill whose contract is already in
  context is not re-invoked to redo by hand what the loaded contract already
  states; apply it.
- **Use the five-phase fast path for bounded repo changes.** When the task has a
  named handoff, a small candidate-authority set, one bound edit unit, and known
  validation, use no more than five latency-bearing tool rounds: (1) receiver
  instructions; (2) one read-only intake snapshot containing the handoff, all
  bounded candidate authority, status/inventory, likely targets, edit-helper
  usage, and relevant untracked-state baseline; resolve authority and bind the
  edit only after that output; (3) one isolated mutation; (4) one ordered
  validation call that labels and preserves each exit/output, runs focused
  before broad, and skips broad if focused fails; (5) one read-only closeout
  containing diff check, exact diff, status, failure attribution, and untracked
  verification. Never hide a retry or external action in a phase. If the intake
  set is not safely bounded before launch, this fast path does not apply.
- **No uncommissioned self-review.** After implementing, run the bound
  validation gates and let CI plus any commissioned review be the defect gate;
  do not run an adversarial self-review of your own diff unless the owner or a
  commissioning artifact explicitly asks for one.
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

Run the Forseti Cynefin Routing Layer before planning or delegation when uncertainty about decomposition, authority, source truth, or safe sequencing could materially change the next move. Substantial, cross-thread, delegated, doctrine-changing, review/patch-affecting, infrastructure-building, and messy-worktree work are escalation cues, not automatic full-router triggers; bounded work with a clear outcome, authority, and route proceeds directly. The owning rule is `.agents/workflow-overlay/decision-routing.md`.

Every durable prompt, handoff, wrapper, rerun, or patch prompt applies the prompt contract; do not author one that skips it. Routine prompts apply the **Forseti Prompt Preflight** core inline (the ~12-line core in `.agents/workflow-overlay/prompt-orchestration.md`) -- no skill reload. A lane-scoped, operator-couriered delegated review-and-patch prompt whose goal, clean target worktree, revision, named file scope, patch authority, and validation route are already bound uses that same pointer-first core plus one fresh target-state read; delegation or patch authorization alone does not trigger the full `workflow-prompt-orchestrator`. Use the full orchestrator only when the **Full orchestration** predicate in `.agents/workflow-overlay/prompt-orchestration.md` applies, including owner-invoked Mini God Tier. In Forseti, a resolver-loaded generic prompt or delegated-review skill must defer to this project-owned routing depth: its generic always-orchestrate default does not override an eligible compact route, while its review mechanics and safeguards still apply. In-session subagent dispatches that only gather and summarize are delegation under `.agents/workflow-overlay/decision-routing.md`, not prompt artifacts; durable or cross-lane prompt artifacts remain governed by this contract. The owning rule, eligibility test, required compact fields, MGT expansion, and fallback blockers are in `.agents/workflow-overlay/prompt-orchestration.md`.

When starting or "spinning up" a new unit of repo-changing work, decide and state the isolation before editing: use a worktree off `main` for writing work that runs alongside other active lanes or on a dirty base; a branch off `main` for solo, sequential writing; and neither for read-only work. The current actor may continue the same commissioned work unit in its selected worktree after one fresh target, revision, dirty-state, and writer snapshot. A separate receiver is required only for an independent concurrent actor or after an observed tool, sandbox, hook, or guard denial proves the current route cannot reach the target; launch-root mismatch alone is not a blocker. An independent external controller still proves exact target, direct write capability, and no concurrent writer once. An in-session collaboration subagent remains confined to the caller's writable root. The owning selection, two-root preflight, and blocker rule are in `.agents/workflow-overlay/decision-routing.md`. Land changes via the per-lane PR flow in `docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md`. When a repo-changing work unit completes verified on its own lane branch or worktree, proceed to commit, push, PR preparation, and merge without waiting for a typed instruction; the harness permission prompts on push, PR, and merge actions are the owner gate. For a bounded cold handoff, the receiving task's initial prompt is the default; create and commit a handoff-only packet only for a distinct persistence, reuse, or separate-consumer need, then follow the transport/publication split in `.agents/workflow-overlay/prompt-orchestration.md`. This exception does not weaken the normal implementation, doctrine, code, or other publication work-unit PR flow. The lane author self-merges its **own** PR by default after the work unit is complete, including all required validation and any commissioned review return and adjudication; for `/fused`, implementation alone is not complete before the delegated review returns and is adjudicated. The protected-action guard and server branch protection remain fail-closed. An agent does not merge another actor's PR, and leaves landing to a human when the owner explicitly holds it, completion cannot be verified, or a guard refuses. See `docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md`.

Do not treat `jb` rules, paths, handoffs, lifecycle mechanics, product policy, validation habits, or external workflow source as Forseti authority. Explicitly invoked or resolver-loaded skills may provide task-local mechanics only.

For doctrine-changing work, implementation boundaries, skill adoption, review lanes, validation, prompt orchestration, source loading, and delegated review-and-patch, load the owning overlay file instead of duplicating the rule here.

Default allowed work is documentation, decisions, prompts, reviews, migration notes, and overlay maintenance inside this workspace. Implementation or runtime work requires explicit bounded authorization in the current turn or accepted handoff.
