# Prompt Orchestration

```yaml
retrieval_header_version: 1
artifact_role: Forseti overlay authority
scope: Prompt artifact families, receiver routing, output modes, preflight fields, and prompt validation gates.
use_when:
  - Creating or reviewing Forseti prompt artifacts.
  - Checking prompt output mode, preflight, or review-report rules.
  - Dispatching cross-lane or repo-changing work to a receiver with a matching write root.
authority_boundary: retrieval_only
```

This file defines Forseti's lightweight prompt-orchestration layer: Forseti-owned prompt mechanics, output modes, preflight, and validation gates, without importing `jb` project policy and preserving Forseti's explicit-authorization boundary for implementation and runtime work.

**Routine read shape** (owned by `.agents/workflow-overlay/source-loading.md`,
Targeted Read Protocol): for routine prompt authoring, read the "Forseti Prompt
Preflight" section below plus the single section for your prompt family.
Lane-scoped delegated review-and-patch prompt authoring also reads "Lane-Scoped
Delegated Patch Prompt Default" below and the targeted commissioning sections
named in `delegated-review-patch.md`; delegation alone is not a full-file-read
trigger. A full-file read is for a prompt matching the **Full orchestration**
predicate below, and for editing this contract.

## Forseti Prompt Preflight

Routine Forseti prompts apply this core inline — no skill reload. For an
ordinary, already-scoped, single-target prompt, this core is the complete
preflight contract; it does not inherit the Escalated Preflight Fields or require
a `forseti_start_preflight` receipt. Review Prompt Defaults and Output Modes still
govern when their task-specific triggers apply. State, per prompt:

1. **Output mode** — exactly one of `chat-only` · `file-write` · `review-report` · `paste-ready-chat` · `patch-queue`, plus its write/report destination.
2. **Template kind** — the bound template from `.agents/workflow-overlay/template-registry.md`, or `none`; template targets are prompt-shaping labels, never runtime-model routing.
3. **Edit permission · targets · branch** — `read-only` | `docs-write` | `patch-only` | `implementation-authorized`; target files or dirs; workspace, branch, and dirty-state allowance when repository state matters. Planning or scoping is a phase, not an authority downgrade: preserve `implementation-authorized` when the commissioning instruction grants it, and apply the receiver-creation clause below when that commission selects a not-yet-verified Codex managed receiver.
4. **Reviews** — findings-first by default; bind any formal verdict, severity, or patch queue explicitly; no runtime-model recommendation, ranking, or implication.
5. **Doctrine change** — work that changes product, architecture, workflow, validation, review, or output doctrine, or a lifecycle boundary, carries a `direction_change_propagation` receipt or blocker (`.agents/workflow-overlay/source-of-truth.md`).
6. **Destinations** — the input prompt source the receiver treats as run-authoritative (canonical artifact path, lane PR body/comment, or ignored scratch path), and the exact output-artifact path it writes when the mode writes a durable artifact.

Repo-constant fields (workspace path, required reads, external-source boundary,
retrieval-header defaults) may be referenced via
`docs/prompts/templates/shared/forseti_preflight_defaults_v0.md` when escalated
preflight applies. Routine prompts state only the core above; do not add unused
field placeholders or a start receipt for form completeness. Fused and
genuinely escalated prompt work author through `workflow-prompt-orchestrator`
and use the escalated contract below. A lane-scoped delegated review-and-patch
prompt uses the compact default below when its eligibility conditions hold;
delegation or patch authorization alone does not escalate it.

## Source Boundary

Forseti-specific facts, product constraints, artifact paths, review lanes, validation gates, and safety rules must come from `AGENTS.md`, this overlay, or accepted Forseti docs named in `.agents/workflow-overlay/source-of-truth.md`. Prompt mechanics come from those same sources; see Escalated Preflight Fields below when the routine core is insufficient.

Prompt-policy, handoff, wrapper, review, output-mode, or execution-contract
changes that alter durable agent behavior are doctrine-changing when they touch
product doctrine, architecture doctrine, workflow authority, validation
philosophy, review authority, output authority, or lifecycle boundaries. They
must follow the Doctrine Change Propagation Contract in
`.agents/workflow-overlay/source-of-truth.md`.

Product-proof prompts and customer-discovery prompts must read
`.agents/workflow-overlay/product-proof.md` when they define buyer
qualification, trust objections, disqualifiers, kill criteria, pull grading, or
graduation rules. Do not redefine trust-objection semantics locally when the
overlay applies.

`prompt_orchestrator.yaml`, `product-ultraplan.yaml`, and `feature-ultraplan.yaml` are non-executable queue records unless later accepted source creates real workflow skills and Forseti validates adoption. Do not create `SKILL.md`, install skills, or copy `jb` templates from Forseti prompt-orchestration work.

## Prompt Orchestrator Binding

```yaml
prompt_orchestrator:
  source_loading_policy: .agents/workflow-overlay/source-loading.md
```

All Forseti prompt-orchestrator work must use the source-loading policy above; do not substitute generic, `jb`, plugin, or installed-skill defaults.

## Source-Gated Method Contract

Repo-aware prompts that orchestrate one or more workflow methods as an explicit
reasoning pipeline over task sources must separate method reference loading from
method application. An eligible **Lane-Scoped Delegated Patch Prompt Default**
may point to its already-bound review lane or skill as routing shorthand: the
receiver still reads the operating instructions and real target sources before
forming findings, but the prompt need not require the named
`REFERENCE-LOAD`/`APPLY` phases or a `SOURCE_CONTEXT_READY` phrase. Adding a
multi-method pipeline, Mini God Tier, or another full-orchestration condition
re-enables this contract.

Use these terms precisely:

- `REFERENCE-LOAD` a method: read the method or skill instructions as
  procedural guidance only. The receiver may prepare neutral source-reading
  questions or checklists, but must not use the method to analyze, frame,
  critique, rank, synthesize, decide, or recommend.
- `SOURCE-LOAD`: read the task-specific source material and build the working
  source context under `.agents/workflow-overlay/source-loading.md`.
- `SOURCE_CONTEXT_READY`: declare that the required source context has been
  loaded, or declare `SOURCE_CONTEXT_INCOMPLETE` with missing sources, source
  gaps, excluded sources, and conflicts.
- `APPLY` a method: use the method to analyze, frame, classify, reason,
  evaluate, synthesize, decide, recommend, or produce findings from the loaded
  source context.

Required sequence when this contract triggers:

1. Read authority and operating instructions.
2. `REFERENCE-LOAD` required method or skill instructions.
3. Do not `APPLY` any method yet. Before source readiness, only neutral
   source-reading lenses are allowed.
4. `SOURCE-LOAD` task-specific source material.
5. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
6. Only after that declaration, `APPLY` the methods to the loaded source
   context.
7. Synthesize and verify against the source context.

Before `SOURCE_CONTEXT_READY`, a prompt must not ask the receiver to produce a
problem frame, architecture recommendation, review finding, option ranking,
root-cause claim, verdict, conclusion, or recommendation unless the method
itself is the source-loading task.

Generated prompts should avoid vague instructions such as "use these skills"
before source loading. Use explicit wording such as:

```text
REFERENCE-LOAD the following method instructions. Do not APPLY them yet. Use
them only to prepare a neutral source-reading lens. After task sources are
loaded and SOURCE_CONTEXT_READY is declared, APPLY the methods to the loaded
source context.
```

Subagents, model-facing prompts, and blind contestant prompts for which this
contract triggers must satisfy the same sequence. Do not send such a subagent
only the method and question when the task requires source-backed reasoning;
provide the same source pack or a bounded source capsule, or require the
subagent to perform its own source-readiness gate.

For an orientation or research subagent whose output returns to an agent, bind
the return shape, not just the source side. Require a terse, schema-bound verdict
— the exact fields named in the dispatch prompt, one line per field, a `file:line`
cite for every load-bearing claim, and `unknown` for an absent field — not a
prose dump. For an execution or source-changing subagent — one that edits,
installs, commits, pushes, or opens a PR — extend that return with
lifecycle-verification fields: branch, base and commit SHA, push/PR state, and
`merged` state, plus a per-surface change list carrying one `file:line` cite
each, so the dispatching CA can verify the durable target on a fresh read per
`AGENTS.md` rather than trust a `done`; a raw diff dump is not a substitute (it
is a prose dump in another form), and `merged` must reflect observed state,
never an assumption. Source-readiness stays governed by the rule above and
`.agents/workflow-overlay/source-loading.md` (the load-side owner); here the
spawning CA names that load in the dispatch, escalates minimally, and validates
the return on receipt: reject or re-prompt a non-conforming or citation-less
reply rather than consuming it. "Returns to an agent" covers any output an agent
will act on, summarize, or route — even output later shown to a human; the only
exception is a deliverable meant directly for a human with no agent acting on it.
The return dimension is distinct from subagent source-readiness (above) and from
forked-context runtime-payload safety (`decision-routing.md`).

For a subagent that introduces or materially changes a validation hook, checker,
or CI gate, bind a validation-probe timeout in the dispatch and return contract.
The subagent must smoke-run the new or changed command under a child-scoped
30-second timeout before any raw full-run, repeated retry, or completion claim.
If the smoke probe times out, the subagent stops and returns
`VALIDATION_HOOK_TIMEOUT` with command, cwd, touched files, and observed process
state; it must not invoke the same hung command again. The 30-second limit is a
hang detector for new/custom validation surfaces, not the timeout for known
repo-wide gates or CI jobs. After the smoke probe passes, run the normal required
gate with its ordinary timeout. Cleanup may target only a process tree launched
by the current actor; otherwise stop for owner/tooling intervention rather than
killing inferred unrelated system processes.

## Thread Operating Target Continuity

When a workflow prompt, wrapper, rerun, review prompt, patch prompt, or handoff
continues the same workstream with a visible active `thread_operating_target`,
preserve that target verbatim near the top of the generated prompt and include
a compact continuity disclosure. The target is required only when the generated
prompt continues the same workstream or claims the same anchor goal; explain
any omission or the omission is a prompt-quality defect.

Use this disclosure shape:

```yaml
thread_operating_target_continuity:
  carried_forward: yes | no
  reason: same_workstream | different_workstream | no_visible_active_target | retired_or_blocked | owner_omitted | conflict
  changed_from_input: no | yes
  lifecycle_status:
  if_changed_reason:
```

`thread_operating_target` is thread-local orientation only — not source authority, validation evidence, readiness, approval, lifecycle completion, durable goal state, artifact authority, workflow sequencing authority, automatic routing, cross-thread memory, registry state, or permission to edit protected paths. Retirement requires explicit owner intent, achieved output satisfying the current `output_fit_check`, or a visible blocker; name the blocker and what remains allowed. Downstream lanes may recommend retirement but must not execute it without explicit prompt or owner authority.

## Project Template Registry

Forseti-local prompt templates live under `docs/prompts/templates/`.
The active Forseti template registry is
`.agents/workflow-overlay/template-registry.md`.

The registry binds template kinds, template targets, output modes, and template
paths for Forseti. Template targets are prompt-shaping labels only; they are not
runtime model routing. Check the registry before using any generic
prompt-orchestration template.

## Supported Prompt Families

| Family | Purpose | Default artifact destination | Default output mode |
| --- | --- | --- | --- |
| Product planning | Frame product bets, evidence standards, kill criteria, and handoff boundaries | `docs/prompts/product-planning/` | `chat-only` or `file-write` |
| Feature planning | Turn an accepted product bet into evidence-producing capability plans | `docs/prompts/feature-planning/` | `chat-only` or `file-write` |
| Deep reasoning | Compare options, downgrade weak candidates, preserve assumptions, and recommend | `docs/prompts/deep-thinking/` | `chat-only` |
| Implementation handoff | Prepare a source-changing unit after implementation is explicitly authorized | `docs/prompts/handoffs/` | `file-write` |
| Review | Ask a read-only or patch-authorized reviewer to inspect artifacts | `docs/prompts/reviews/` or `docs/review-inputs/` | `review-report` |
| Rerun or patch | Retry an unresolved finding without reopening settled decisions | `docs/prompts/reruns/` or `docs/prompts/patches/` | `patch-queue` |

Typed child folders under `docs/prompts/` may be created when the first prompt of that family is authored. Source-changing handoff prompts may target implementation only when the current turn or an accepted handoff explicitly authorizes bounded implementation; otherwise they must target documentation or overlay work only.

Goal-fitness-judged source-changing work must bind a concrete goal and observable success signal before edits begin; technical or consistency-judged work is exempt; when ambiguous prefer binding a pointer but do not block absent the trigger. Owning decision: `docs/decisions/work_unit_fitness_reference_v0.md`.

Prompt templates may also use `paste-ready-chat` when the intended output is a
single prompt, wrapper, or handoff body meant to be pasted into another model,
agent, thread, or worktree.

## Author Through The Prompt Orchestrator

Every durable Forseti prompt, handoff, wrapper, rerun, or patch prompt applies the
prompt contract; authoring one that skips it is a prompt-quality defect even when
the surface text looks complete — the defect is the skipped contract, not the
surface. The contract is applied at two depths, with the compact delegated path
as an unnamed specialization of routine depth:

- **Routine prompts** apply the **Forseti Prompt Preflight** core (above) inline — no
  skill reload. The core fully satisfies the contract for an ordinary,
  already-scoped, single-target prompt; it owes no escalated fields or durable
  start receipt solely because it is repo-aware.
- **Lane-scoped delegated review-and-patch prompts** use the compact default
  below when eligible. Delegation, adversarial wording, patch authorization,
  executor-ready wording, multiple named files in one bounded technical diff,
  or a high-stakes label alone is not an escalation trigger.
- **Full orchestration** applies when the prompt is fused, reusable/canonical,
  novel or genuinely cross-lane, no-repo/portable, source-heavy,
  doctrine-changing, materially ambiguous or dirty, complex-output-routing,
  first-of-kind, or owner-invoked Mini God Tier. These are routing conditions,
  not user-facing modes. A missing eligibility fact routes to the full
   `workflow-prompt-orchestrator` contract or the nearest honest blocker; do not
   invent it.

An unchanged same-lane prompt points to the active one-time writable-root
binding in `decision-routing.md`; it does not repeat root, capability, or writer-
isolation details. New/external receivers and changed bindings carry the exact
details required below.

### Implementation Commission Receiver-Creation Clause

Every durable or cross-recipient commission with edit permission
`implementation-authorized` that selects a new `codex_managed_worktree` and may
begin in a task that is not the receiver must make the task-creation request
explicit in the visible commission. Include this bounded block next to that new
receiver's single `receiver_binding` receipt. A prompt continuing the active
binding includes neither block merely for lifecycle continuity.

```yaml
receiver_creation_authorization:
  authorization: create_exactly_one_fresh_codex_managed_worktree_task
  condition: current_task_not_receiver_verified
  managed_starting_ref: "<bound ref>"
  required_revision: "<commit>"
  revision_mode: exact | ancestor
  initial_prompt: this_frozen_commission_verbatim
  dispatch: immediate_same_turn
```

This block is the commission's explicit user request to create at most one task;
`implementation-authorized` by itself is not task-creation authority. When the
condition is observed, create and dispatch that one managed-worktree task in the
same turn with the frozen commission as its initial prompt, then stop repo-
changing work in the original task. Do not ask for a confirmation phrase. If
creation fails or the created receiver fails its bound preflight, return the
observed blocker and do not create a second task.

The block is commission-local, conditional, and single-use. It grants no
standing task-creation permission and must not appear in a truly read-only,
scoping-only, or review-only commission. Planning or scoping inside an
implementation-authorized commission does not change its declared authority:
route and status output must retain the implementation authorization. The
status `current_turn_authorization: read_only_scoping_only` is valid only when
the current user instruction or accepted handoff is actually read-only; it is a
prompt-quality defect when emitted merely because planning or scoping happened
before the authorized implementation.

**Forseti precedence bridge.** A resolver-loaded generic prompt or
delegated-review skill supplies task-local method mechanics, not Forseti routing
authority. Its generic requirement to render every strict controller prompt
through the full orchestrator is satisfied, for an eligible Forseti lane, by the
compact renderer below. The skill's review, de-correlation, scope, validation,
and adjudication safeguards still apply. If a receiver cannot honor this
project binding, return a visible routing blocker instead of silently taking the
generic heavy route. This bridge changes no installed skill artifact and makes
no deployment claim.

### Lane-Scoped Delegated Patch Prompt Default

This is the unnamed default, not a mode selector. Use it only when all of these
conditions hold:

- the deliverable is one current-lane, operator-couriered, paste-ready prompt;
- the future delegate must have direct `repo` access and a different upstream
  vendor/model lineage from the author;
- the visible request supplies or safely determines a goal and success signal,
  one matching target worktree or managed starting ref, branch/revision,
  dirty-state allowance, named file set, bounded patch authority, and validation
  route;
- the rendered prompt binds an external controller under
  `.agents/workflow-overlay/decision-routing.md`; an already selected controller
  carries the two-root preflight, and an unknown future courier receiver stays
  preparation-only as `receiver_to_bind`;
- none of the **Full orchestration** routing conditions immediately above apply;
  and
- there is no unresolved authority, target, state, or scope conflict.

The author records the single inline `receiver_binding` receipt owned
by `.agents/workflow-overlay/decision-routing.md`. A bound active receiver then
performs exactly one fresh target-state read: worktree path, branch and HEAD,
dirty state, named or changed files, and the material validation commands or
evidence already bound to the lane. An unknown courier completes that read and
the external direct-write capability proof as its first action, before source
loading. The author does not pre-load the receiver's target sources, reconstruct the receiver's source
ledger, traverse the template registry, or claim the delegated lane execution-
ready before the binding is verified.

An explicit `delegate patch` invocation is an authoring request: return exactly
one paste-ready prompt for the operator to courier. Do not inspect installed
controllers, create or dispatch a task, fork or spawn another agent, or execute
the review. The commission includes `delivery: operator_courier_only`,
`access: repo`, and
`delegate_eligibility: different_vendor_lineage_with_direct_repo_access`.
Same-vendor, unknown-lineage, no-repo, self, and Codex-managed substitutes are
invalid. If no eligible controller is available, the prompt remains unexecuted.

Render one compact pointer-first prompt containing:

1. the plain goal and what done looks like;
2. the exact worktree or managed starting ref, branch/revision, dirty-state
   allowance, named targets and patch scope, plus the single `receiver_binding`
   receipt (using `receiver_to_observe` only for facts the not-yet-launched
   receiver must observe);
3. the different-vendor controller constraint plus author/home family and
   delegate family, using `operator_to_fill` only for an inferable but genuinely
   operator-owned value;
4. pointers to `AGENTS.md`, `.agents/workflow-overlay/README.md`, the targeted
   sections of `.agents/workflow-overlay/delegated-review-patch.md`, the
   relevant review skill or lane, and the `environment_baseline` constant in
   `docs/prompts/templates/shared/forseti_preflight_defaults_v0.md`;
5. named validation expectations with real failure and not-run reporting;
6. the controller return: findings, bounded diff, neutral citations, validation
   evidence, verdict, and residual risk;
7. Chief Architect adjudication before any returned change is kept, plus
   `NEEDS_ARCHITECTURE_PASS` for design-level blockers; and
8. the delegate hard stop: no commit, push, PR, merge, stash, reset, worktree
   cleanup, or repository-hygiene action.

Prompt rendering and execution are separate states. A prompt with
`receiver_class: receiver_to_bind` may be returned for a manual unknown courier,
but it must label itself preparation-only, must not claim dispatch readiness,
and must block receiver source loading until rebound to a verified concrete
class. A delegated review-and-patch courier prompt must not carry
`receiver_creation_authorization` and must not select `codex_managed_worktree`;
the general receiver-creation clause above remains available for other explicit
implementation commissions but is not a fallback for this lane. Generic
`proceed`, implementation authority, unavailable external tooling, or a
same-vendor sanity label never authorizes dispatch.

The default receiving output is chat or the lane PR/comment. Do not require a
durable review report, `review_summary` courier, provenance checker, full source
pack receipt, template-registry traversal, or `SOURCE_CONTEXT_READY` phrase
solely because the task is delegated, adversarial, or patch-authorized. The
receiver still reads the actual target diff and sources, performs the real
review, and runs relevant validation. Pointer over copy: if an eligibility
condition fails, use full orchestration or block on the missing authority.

### Owner-Invoked Mini God Tier Uplift

Mini God Tier is the only named assurance uplift for this prompt family. It is
owner-invoked only and never inferred. It selects the bounded capability target
defined by `docs/decisions/forseti_mini_god_tier_doctrine_v0.md`; it does not
widen scope, establish readiness, or create a claim tier. Use full orchestration
and add deep-thinking, source-gated method sequencing, durable reporting, and
provenance evidence only to the degree necessary for that target, remaining
pointer-first and naming every accepted residual.

The compact default deliberately retains four residuals: the receiver must
still read the real diff and sources and run validation; genuine no-repo,
canonical, doctrine-changing, source-heavy, ambiguous, or cross-lane cases
still take the full route; eligibility remains a judgment rather than new
standing infrastructure; and Mini God Tier cannot guarantee cross-vendor
availability or prove quality. Revisit the first two if repeated work shows
duplicate receiver reads, the third after three confirmed misroutes or omitted
guards, and the fourth if an actor treats the label as validation.

**Prompt filing is classified by source role, not by recipient count.** A
prompt, handoff, wrapper, rerun, review request, or patch prompt must still apply
the prompt contract at the correct depth before use; the filing question is
separate:

- **Canonical prompt artifacts** are filed under the accepted `docs/prompts/**`
  family. This includes reusable templates, doctrine-bearing prompts,
  first-of-kind workflow prompts, standard handoffs/wrappers/reruns/review
  requests meant to be reused beyond the current lane, and any prompt promoted
  as a Forseti source artifact. For these prompts, `paste-ready-chat` carries a
  copy of the filed body for pasting and is **not a substitute for filing**.
- **Lane-scoped execution prompts** are not standalone prompt artifacts. A
  one-off review dispatch, adversarial prompt, rerun launcher, patch prompt,
  wrapper, courier, or model/agent/thread/worktree message whose only job is to
  advance one work-unit lane is attached to the overall lane PR body/comment or
  kept in ignored `docs/_inbox/` scratch when a disk handoff is useful. Do not
  open a separate prompt-only PR for that material, and do not commit it solely
  to manufacture a durable prompt artifact. The durable record is the lane PR
  plus the downstream artifact the prompt asks the receiver to write. Closeout
  notes and other lane-continuity docs follow the same filing rule: they ride
  the originating work-unit lane PR or stay in ignored scratch until consumed,
  and get a standalone PR only when the doc itself is the bounded publication
  work unit. Handoff-only packets follow the transport/publication split
  immediately below; commissioning the packet alone does not make it a bounded
  publication work unit.
- If a lane-scoped prompt later becomes reusable, doctrine-bearing, or otherwise
  source-like, promote it through the canonical `docs/prompts/**` path in the
  same lane PR when that lane owns the change, or in a dedicated prompt PR only
  when the prompt artifact itself is the work unit.

### Handoff Transport Versus Publication

A handoff-only packet has two distinct lifecycle states:

- **Dispatch-ready / transport.** The receiving cold lane has a concrete,
  `receiver_verified` binding and can resolve the exact packet bytes through
  that receiver's actual mechanism before dispatch. A prepared unknown-receiver
  courier remains preparation-only and cannot enter this state. Commit is
  the stable local transport boundary; once its SHA is couriered as the packet's
  revision handle, that commit is not rewritten (no amend, rebase, or squash) for
  the packet's transport lifetime, and a required history change re-couriers the
  new SHA, because a `git show <sha>:<path>` fallback resolves nothing against an
  orphaned SHA. The courier/context identifies the
  repository or worktree access route, repository-relative packet path,
  branch/ref and commit SHA when revision access is needed, and an explicit
  fallback such as `git show <sha>:<path>`. Include a same-filesystem absolute
  path only when that is the receiver's actual route. The dispatcher verifies
  discoverability by reading the packet through that actual route; path
  existence in the author's checkout or a path merely written in chat is not
  verification for a different receiver mechanism. If the receiver cannot use
  the authoring worktree or local ref, push the branch and verify the remote ref
  before dispatch. If no verified route exists, stop with a visible transport
  blocker.
- **Publication-ready / landing.** The packet independently merits durable
  publication on `main`, another landing artifact requires it, or the owner
  requests landing. Only this state opens a packet PR. A PR is never created
  merely to make the packet discoverable; it publishes an independently
  justified durable artifact.

This split is specific to handoff-only transport. A packet that rides an
existing implementation, doctrine, code, or other publication work unit still
lands in that work unit's normal PR. A handoff-only branch is pushed only when
the receiving mechanism cannot reach the local worktree/ref, not by default.

The `docs/prompts/**` PostToolUse hook (`check_prompt_provenance.py`) fires only
for canonical filed prompt writes and injects the preflight — output mode, edit
permission, source pack / required reads, the Source-Gated Method Contract, and
the doctrine-change receipt. Lane-scoped prompts use an accepted PR-carried or
scratch-carried path, so an eligible delegated review-and-patch prompt carries
the compact default above rather than the escalated receipt. Other lane-scoped
prompts carry the applicable routine or full fields; missing applicable
preflight remains a prompt-quality defect.

If `workflow-prompt-orchestrator` is not resolver-available when a case needs it,
apply this file's full contract or return a visible blocker; this routing default
does not claim the skill is an adopted or resolver-validated executable.

## Default Path Assignment

The user is not responsible for naming routine Forseti artifact paths.

When a user asks for a canonical prompt artifact without naming a path, choose
the narrowest accepted Forseti folder from
`.agents/workflow-overlay/artifact-folders.md` and the Supported Prompt Families
table above, and create a deterministic, descriptive versioned filename.
Example: a reusable review prompt goes to
`docs/prompts/reviews/<descriptive_slug>_prompt_vN.md` with a downstream report
at `docs/review-outputs/adversarial-artifact-reviews/<descriptive_slug>_review_vN.md`
(or `docs/review-outputs/<descriptive_slug>_review_vN.md` when no narrower child
folder is bound).

When the request is for a lane-scoped execution prompt and no reusable prompt
artifact is requested, default to attaching the prompt to the lane PR
body/comment. If the lane PR is not open yet and a file handoff is useful, use
ignored `docs/_inbox/` scratch and carry the prompt into the lane PR at PR prep.
Do not create a standalone prompt PR for that default. A handoff-only packet
that must remain findable across a cold lane uses the dispatch-ready transport
contract above instead of this scratch default.

Repo-aware prompts handed to another model, agent, thread, or worktree must
state both:

- the input prompt source the reviewer or downstream agent should treat as
  authoritative for that run: a canonical prompt artifact path, a lane PR
  body/comment location, or an ignored `docs/_inbox/` scratch path; and
- the exact output artifact path the reviewer or downstream agent should write,
  when the output mode writes a durable artifact.

For a handoff-only packet, those fields are insufficient by themselves: the
courier also carries the verified transport route, repository-relative path,
branch/ref, commit SHA, and explicit revision-read fallback required by
"Handoff Transport Versus Publication" above.

Ask the user for a path only when the destination cannot be determined from the
artifact role, accepted folders, requested workflow, or collision state. If a
chosen path already exists, choose the next version suffix or return a visible
collision blocker when versioning would change the intended target.

## Full Prompt Versus Thin Wrapper

A full prompt is the durable artifact. It must include:

- the retrieval header from `.agents/workflow-overlay/retrieval-metadata.md`
  when the prompt is new or materially touched;
- objective and intended decision;
- Forseti source hierarchy and required reads;
- source paths plus hashes or revisions when stability matters;
- hard constraints and forbidden imports;
- output mode and exact output contract;
- target artifact roles and write permissions;
- validation gates and required verdicts;
- assumptions, unknowns, and blocked conditions.

A thin wrapper is a short invocation of a full prompt. It must include:

- referenced full prompt path and hash or revision;
- workspace path, branch or revision, and dirty-state allowance;
- target files or directories;
- output mode and edit permission;
- only the delta needed for this run.

Thin wrappers must not restate or fork project policy. If policy changes are needed, update the full prompt or overlay first.
Use a retrieval header for a wrapper only when the wrapper is durable and
expected to route future work.

## Fitness-Reference Surfacing (Durable / Cross-Recipient Prompts)

For durable or cross-recipient prompts — handoffs, commissions, reviews, and patch
prompts (the saved or `paste-ready-chat` families), not trivial inline `chat-only`
prompts — surface the work unit's `fitness_reference` (goal + observable success
signal, the object owned by `docs/decisions/work_unit_fitness_reference_v0.md`),
**reusing that concept; do not mint a new goal/success vocabulary.** Surface it in
two places:

- **Chat return (for the dispatcher):** show the goal + success signal beside the
  prompt path or link, in **plain language a non-expert reads at a glance** — no
  skill jargon, no internal vocabulary. If it cannot be stated plainly, that is a
  prompt-quality defect, not a styling nit.
- **Prompt body (for the receiving executor):** carry it **pointer-preferred**
  (cite the controlling upstream goal/signal when one exists; fresh compact prose
  only when none does) as a clearly-labeled "what this is for / done looks like"
  entry. A cross-recipient prompt travels without this chat, so the body is the
  only place its executor sees the target; this extends, and does not duplicate,
  the already-required "objective and intended decision."

Label the carried reference **executor target + review axis-to-attack, not a review
pass bar.** This preserves `prompt_body_injection: no` and the alignment-axis
guardrail from `work_unit_fitness_reference_v0`: a later review of the commissioned
work treats the goal/signal as a pointer-preferred axis it must attack, never as a
conformance bar graded against the generating prompt. Carrying the target for the
executor is not making it the review bar.

Generic shape (illustrative only — keep your wording specific to the work; do not
anchor to this):

> **Goal:** the one outcome this work must achieve, in plain words.
> **Done looks like:** the observable check that says it worked — what a good result
> shows, not a restatement of the task.

This **extends the surfacing** of `work_unit_fitness_reference_v0` (scope-locked at
enactment to adversarial artifact review plus the fused gate) to durable and
cross-recipient prompts generally. It changes none of that decision's substance:
not its review back-pressure, not the scoped fused gate, not `prompt_body_injection:
no`, and not the alignment-axis-not-pass-bar guardrail.

## Review Prompt Defaults

Forseti review prompts include a deep-thinking framing pass before the relevant
review skill when the owner explicitly invokes `workflow-deep-thinking` or Mini
God Tier, or when the review is doctrine- or authority-changing, source-heavy,
materially ambiguous, or carries substantial seam risk whose framing could
change the review route. Adversarial wording, a formal-verdict request,
delegation, patch authorization, multiple named files in one bounded technical
diff, or a high-stakes label alone does not trigger deep-thinking. A bounded
technical review with an exact revision, file scope, authority, and validation
route may omit it. For a review commission, the review lane's own internalized
failure-mode-framing discipline satisfies the pass -- the adversarial review
skill carries it and the review templates define it -- without a second skill
load; a separate `workflow-deep-thinking` load remains the route for
owner-invoked decision work.

When the framing pass is triggered, the reviewer may `REFERENCE-LOAD` the
methods before source loading, but must not `APPLY` the framing pass or the
review method until the required source context is ready. The step frames the
boundary problem, failure modes, and decision criteria before findings are
listed. It does not
widen review scope, authorize patching, or turn a narrow review into product
planning.

Review prompts should still return the requested review output shape. The final
answer remains a review result with findings, non-findings, not-proven
boundaries, and next authorized step whether deep-thinking was triggered or
explicitly omitted.

Every Forseti review prompt and any review-return or courier prompt must also
instruct the *adjudicator* -- the reviewer in a self-review, the commissioning
Chief Architect in a delegated pass, never the delegate mid-review -- to close
adjudication in this order: first adjudicate the findings, diff, verdict, and
residuals as claims; close self-closable material issues (closure within the
adjudicator's own authority and the commissioned scope) in the same turn; route
the smallest complete closure step only for an issue that needs another review
round, another lane, an architecture pass, or an owner decision; once no
unresolved material issue remains, batch all admin/lifecycle follow-ups
(commit, push, PR, merge) into exactly one named land step with no
deep-thinking. If a visible active goal, `thread_operating_target`, or accepted
next objective exists, deep-think the 1-5 material moves that best advance it in
the same turn. If none exists, record that compactly and do not invent material
moves. The closure/land step plus this goal-conditioned material-move check are
a required closeout tail; do not defer the check to another turn. This is the
tail mirror of the deep-thinking-first rule above: it runs after adjudication,
does not widen review scope or authorize patching, and produces the closeout's
next step. The exact shape is owned by
`.agents/workflow-overlay/communication-style.md` (Review Adjudication Next
Step); do not restate it here.

Delegated review-and-patch commissions require direct repo access. `no_repo` is
outside that lane and routes to a separately named ordinary read-only review;
it must not be presented as delegated patch authorship. Couriered or paste-ready
delivery changes transport only, never the direct-repo requirement.

Review prompts, wrappers, handoffs, and closeouts must not recommend,
prescribe, rank, or imply runtime model choice for review lanes. They may route
by review lane, method/skill, target, authority, output mode, destination, and
prompt-template target only. Template targets are prompt-shaping guidance;
runtime model choice for review work is outside Forseti review-lane authority.

Review prompts must require the durable review output to record two provenance
fields -- `reviewed_by` (the model and version that performed the review) and
`authored_by` (the model and version that authored the reviewed artifact) --
operator/tooling-supplied, value `unrecorded` when not supplied, never
fabricated, on new or materially touched review outputs (not backfilled). They
are set by the operator/CA on the durable record (a no-repo or portable reviewer
need not self-emit them) and are observed provenance facts only; they must not
be expressed as, or turned into, a runtime model recommendation, ranking, or
selection. Same-family-vs-cross-family is computed by relating the two and is
measured only when both carry real values, so a present `unrecorded` value is a
visible measurement gap, not success.

Every Forseti adversarial artifact review prompt must invoke
`workflow-adversarial-artifact-review` after `SOURCE_CONTEXT_READY`. If that
skill is unavailable, unresolved, or not applied, the run may return only a
blocked or advisory-only result and must not emit formal verdicts, severity
authority, blocked/ready status, validation claims, readiness claims, mandatory
remediation, patch queues, executor-ready handoffs, or alignment-complete
claims.

Review prompts are findings-first by default. Formal verdicts, blocked/ready
status, validation pass/fail claims, approval, readiness, mandatory
remediation, patch queues, and executor-ready handoffs must be explicitly bound
by the prompt or `.agents/workflow-overlay/review-lanes.md`. If a prompt asks
for severity labels, it must either use a Forseti-bound severity set such as
`critical`, `major`, and `minor` for finding priority only, or define the
prompt-specific severity contract.

Actionable review findings should include:

- `minimum_closure_condition`: what must become true before the finding can be
  treated as closed. It states the required end state, not how to implement it;
- `next_authorized_action`: what the current lane may do next under its
  authority;
- `confidence`: the reviewer's certainty the finding is real (`high`, `medium`,
  or `low`) -- a priority label only, never a reporting threshold.

Within the commission-bound target and purpose, adversarial review prompts
should ask reviewers to be maximally adversarial and coverage-first: report
every issue found, including uncertain and low-severity ones, each labeled
with estimated severity and confidence; do not filter for importance or
confidence at the find stage -- the adjudication pass ranks and filters.
Low-confidence or minor findings may use a compact one-line form, and
steelman-defeated candidates are listed one line each in a
`considered_and_defended` section rather than silently dropped. Optional
hardening may be named only when clearly labeled optional and non-required.

For intent-bearing review targets, review prompts should bind or point at the
`fitness_reference` (a goal plus an observable success signal, pointer-preferred)
so the review's decision criteria are anchored to the work unit's intended
outcome rather than re-derived from scratch. If no fitness reference exists, the
prompt must ask the review to name the gap (`no checkable success bar bound`)
rather than invent the goal. The reference is an alignment axis the reviewer must
also attack, never a pass-if-matches bar. This applies to adversarial artifact
review only; see `.agents/workflow-overlay/review-lanes.md` and
`docs/decisions/work_unit_fitness_reference_v0.md`.

Do not request `patch_queue_entry` from a read-only review. It means
executor-ready how-to and belongs only in a patch-queue review or separately
authorized patch/integration execution lane. Read-only review prompts may ask
for advisory remediation direction, but must not turn that direction into
patch authority.

CA-facing review prompts, handoffs, and closeouts must preserve the consumption
order from `.agents/workflow-overlay/communication-style.md`: commission ->
target -> authority -> decision criteria -> evidence -> reviewer verdict or
recommendation. Do not introduce a synthesis lane for multi-review
reconciliation unless Forseti later binds one explicitly.

Review prompts using `review-report` output mode must bind a durable report
destination under `docs/review-outputs/` or a typed child folder unless the
review is explicitly chat-only before review work starts. For `review-report`,
the human-readable review value belongs in the durable report; chat YAML is
courier output, not a substitute review artifact.

YAML-only chat is valid for `review-report` only after the required durable
report has been successfully written. The chat response then uses the compact
YAML summary defined in `.agents/workflow-overlay/communication-style.md`, with
`report_path` pointing to the written report and listing the core summary,
findings, and next action.

### No Runtime Model Routing

Review prompts, wrappers, and handoffs must not recommend, prescribe, rank, or
imply runtime model choice. Template retrieval never claims a prompt will run
on a particular model.

Template retrieval must not:

- claim a prompt will run on a particular model;
- recommend a runtime model;
- rank models;
- bind reviewer or executor selection;
- create implementation, validation, readiness, or lifecycle authority.

If the required durable report cannot be written after `review-report` is
selected, do not treat the YAML as a substitute artifact. Return a failed
blocked result in chat with `review_location: chat_only_current_thread`, do not
use `report_path`, name the failed report path, and include enough human-
readable failure detail to route. Use chat-only review only when write authority
or report destination is not bound before the review begins.

## Escalated Preflight Fields

Prompts matching the **Full orchestration** predicate above include or reference
the `forseti_start_preflight` receipt owned by
`.agents/workflow-overlay/source-loading.md`. These cases must make their start
state portable because another actor or later lane will rely on it. Repo-constant
fields may be referenced via
`docs/prompts/templates/shared/forseti_preflight_defaults_v0.md`; required
escalated deltas in that artifact remain explicit. Routine prompts stop at the
core above.

An eligible lane-scoped delegated review-and-patch prompt instead uses the
compact default above: core prompt fields plus one fresh target-state read and
the eight pointer-first commission fields. It does not inherit this escalated
receipt solely from delegation, adversarial wording, patch authorization,
executor-ready wording, or a bounded multi-file target.

Every escalated prompt must state:

- whether `AGENTS.md` and `.agents/workflow-overlay/README.md` were read or
  supplied in the current task context;
- selected source pack from `.agents/workflow-overlay/source-loading.md`, or a
  bounded custom source pack;
- `repo_map_decision: loaded | not_needed | unavailable`, plus `repo_map_reason`. Source-loading (`.agents/workflow-overlay/source-loading.md`) owns the read-pack rule; this field records the prompt author's routing decision and must not make the repo map a mandatory read;
- workspace path or repository identifier;
- expected branch, detached revision, or commit hash when source stability matters;
- a pointer to the active one-time writable-root binding for same-lane work, or
  the single inline `receiver_binding` from `decision-routing.md` when the
  prompt creates a new/external receiver or materially changes the binding;
- the commission-local `receiver_creation_authorization` block above when an
  implementation-authorized managed receiver may need to be created from the
  visible commission;
- dirty-state allowance and whether untracked files are in scope;
- controlling-source state when strict claims depend on Forseti overlay,
  source-loading, repo-map, prompt-policy, validation, or artifact-role files:
  clean, modified, untracked, stale, or not checked;
- whether the work changes product doctrine, architecture doctrine, workflow
  authority, validation philosophy, review authority, output authority, or a
  lifecycle boundary, and if so which propagation surfaces must be checked
  before closeout;
- target files or directories;
- source hierarchy for the task;
- edit permission: `read-only`, `patch-only`, `docs-write`, or
  `implementation-authorized` (enum owned by `forseti_start_preflight` in
  `.agents/workflow-overlay/source-loading.md`);
- output mode: `chat-only`, `file-write`, `review-report`,
  `paste-ready-chat`, or `patch-queue`;
- required validation gates and where evidence is recorded;
- external source boundary, including the rule that external workflow source is read-only from Forseti work and `jb` is not Forseti authority.

### Repo-Bound Review Target Resolution

Repo-bound review and delegated-review prompts first bind the receiver class
under `.agents/workflow-overlay/decision-routing.md`. Only
`external_direct_write` uses two distinct roots: its `launch_checkout` and the
commissioned `effective_target_worktree`; a mismatch is a resolution trigger,
not an automatic blocker. `codex_managed_worktree` requires the task's launch
checkout and effective target to be the same app-created managed worktree.
`collaboration_same_root` remains in the calling task's root.
`receiver_to_bind` is preparation-only. Prompts may render before a future
launch checkout is observable, but they must not claim dispatch readiness or
begin receiver source loading until the binding is verified.

Target identity is an exact revision/hash pin or required commit ancestry. For
uncommitted work it also includes the allowed dirty-file set and a target
manifest or equivalent byte identity; branch and HEAD alone cannot identify
dirty bytes. Exact pins remain exact, while an advancing lane head may continue
only when the prompt explicitly uses ancestry semantics.

Receiving preflight establishes one binding, then stops repeating it:

1. Reuse the active work-unit binding when receiver, task, root, target, and
   material state are unchanged.
2. For a new managed receiver, bind the app-created worktree as that task's root;
   do not inspect, create, or select a nested worktree as an alternate target.
3. For a new `external_direct_write` receiver only, resolve the unique target and
   establish direct write capability plus no-concurrent-writer state once.
4. Same-root collaboration stays inside the caller's active binding.
5. Re-resolve only on a receiver/root/target change, genuinely unknown
   capability, or observed mismatch/dirty-state drift. Synthetic write/index
   probes and hook canaries are not routine preflight.
6. On a pre-edit mismatch, execute an already-authorized managed-task route when
   available. Return `BLOCKED_RECEIVER_REROOT_REQUIRED` only when no capable
   authorized route exists or the new binding cannot be established.

This resolver is discovery of the commissioned source, not permission to use an
alternate branch, recreated copy, context pack, or summary as review evidence.
It does not weaken exact hash/revision pins, dirty-state rules or write guards;
it prevents both an unrelated launch checkout from being mistaken for the
target and a valid external controller from blocking solely on its launch path.

Rerun and patch prompts must also name the prior artifact, prior hash or revision, frozen decisions, mutable fields, and unresolved finding being retried.

## Source-Heavy Prompt Economy

Preflight is allowed to continue into the next step when it is limited to
authority reads, path existence checks, hashes, branch state, and target-scope
checks. Do not split a prompt solely because preflight exists.

Split or stop before the work becomes source-heavy. A prompt is source-heavy
when it requires public web/source research, multiple external page opens,
case-by-case evidence ledgers, post-window comparisons, review of several large
artifacts, or any other source-loading unit that can materially fill live
context before its output is sealed.

For source-heavy work:

- define the source-loading unit before research starts, normally one case, one
  artifact, one review target, or one bounded evidence question;
- write and hash the unit artifact before moving to the next unit;
- if context compacts before the current unit artifact is written and hashed,
  stop as `BLOCKED_COMPACTION_BEFORE_ARTIFACT_SEAL` and treat any outputs from
  that unit as contaminated scratch until archived or rerun cleanly;
- do not carry full source text, full source ledgers, full artifact prose, or
  long readbacks in chat after the unit artifact exists;
- keep chat checkpoints to receipt-level facts: artifact path, SHA256, status,
  blocker/leakage state, and a short summary needed by the next step;
- synthesize later packets from explicit compact summary sections, artifact
  paths, hashes, and statuses, not by rereading full source-heavy artifacts.

Highest-token actions to carve out: external web page opens, search result pages, full artifact readbacks, pasted source-ledger rows, pasted Evidence Units, multi-case or multi-target accumulation in one live thread. Prefer artifact-local detail plus compact chat receipts.

## Output Modes

- `chat-only`: return analysis, options, recommendations, and blocked assumptions without writing files.
- `file-write`: write only authorized Forseti documentation or overlay files;
  report changed files and validation evidence. For substantial
  decision-bearing artifacts, chat closeout must include a concise headed human
  summary before the artifact receipt.
- `review-report`: perform read-only review unless a patch-execution lane is explicitly assigned; write reports under `docs/review-outputs/` or a typed child folder, then return the compact YAML review summary in chat only after the report write succeeds. If the required report write fails, return `status: failed`, `review_location: chat_only_current_thread`, and `recommendation: blocked` in chat without `report_path`, name the failed path, and include enough human-readable failure detail to route.
- `paste-ready-chat`: return one prompt, wrapper, handoff, or review request
  body in chat for copying into another model, agent, thread, or worktree. For a
  canonical prompt artifact the durable artifact of record is the filed
  `docs/prompts/**` file (see "Author Through The Prompt Orchestrator"); the chat
  body is a copy for pasting, not a substitute for filing. For a lane-scoped
  execution prompt, `paste-ready-chat` may be the prompt body that is attached to
  the overall lane PR body/comment or kept in ignored `docs/_inbox/` scratch; it
  does not create source authority and must not produce a standalone prompt PR.
  Any surrounding Chief Architect, planning, overlay gate, or routing decision
  should still use the human-readable chat shape from
  `.agents/workflow-overlay/communication-style.md`.
- `patch-queue`: produce stable patch units, target files, authority basis, and validation gates. Applying patches requires separate execution authority.

The general human-summary / agent-detail / optional courier-state chat shape is owned by `.agents/workflow-overlay/communication-style.md`. This file owns output-mode exceptions to that shape:

- `review-report` may use YAML-only chat only after the required durable report has been successfully written; failed durable writes must use `review_location: chat_only_current_thread`, `status: failed`, `recommendation: blocked`, name the failed path, and include enough human-readable routing detail.
- `file-write` may return a compact path/hash/status receipt when the durable artifact carries the human-readable value; substantial decision-bearing writes must close with a headed human summary first (recommendation, why it matters, material boundaries, next authorized step), then receipt. If the write fails or the chat carries a decision, return readable blocker detail. Doctrine-changing file writes must include a `direction_change_propagation` receipt or blocker from `.agents/workflow-overlay/source-of-truth.md`.
- `paste-ready-chat` may prioritize the paste-ready body when that body is the deliverable; do not use this mode to hide a Chief Architect, planning, scoping, overlay gate, or completion decision.
- `patch-queue` may use stable structured units, but applying patches requires separate execution authority and readable blocker routing.

## Prompt Validation Gates

Authoring-route precondition: the prompt, handoff, wrapper, rerun, or patch
prompt must have applied the prompt contract at the correct depth (see "Author
Through The Prompt Orchestrator") — the **Forseti Prompt Preflight** core for a
routine prompt, the **Lane-Scoped Delegated Patch Prompt Default** for an
eligible current-lane commission, or the full `workflow-prompt-orchestrator`
contract for a prompt matching the **Full orchestration** predicate above. An
artifact that skipped the applicable contract is a prompt-quality
defect; reconstruct it at the correct depth before use. A durable start receipt
is required only for the full-orchestration cases.

Before using a generated Forseti prompt, apply these gates:

1. Applicable preflight complete: `AGENTS.md` and
   `.agents/workflow-overlay/README.md` were read or supplied in the current
   task context. Routine prompts carry the six-field core and no start receipt;
   eligible compact delegated prompts carry that core, one fresh target-state
   read, and the eight commission fields above; escalated prompts carry the
   portable start receipt and fields above.
   Repository-state fields are stated only when material.
   Modified or untracked controlling sources block strict readiness,
   acceptance, validation, proof, `PASS`, or `ADEQUATE_NOW` claims unless owner
   acceptance or controlling authority is explicit.
2. Artifact roles bound: every prompt role maps to `.agents/workflow-overlay/artifact-roles.md` or another accepted overlay file.
3. Source resolution clean: external workflow sources do not provide Forseti authority; installed skills are deployment copies; `jb` project policy is not imported.
4. Writable-root binding present when repository state matters: same-lane prompts point to the active one-time binding without repeating its root/capability recital; new/external receivers and materially changed bindings carry the single `receiver_binding`, and a not-yet-created managed receiver also carries the exact one-task `receiver_creation_authorization`. Collaboration remains same-root, unknown receivers remain preparation-only, and a command `workdir` is never a reroot. A delegated review-and-patch courier remains operator-courier-only, direct-repo, and different-vendor, with no Codex-managed fallback. A prompt fails this gate when it invents task-creation authority, applies external two-root discovery to a wrongly launched Codex task, claims dispatch readiness before a new binding exists, or repeats capability ceremony as if it were required for an unchanged active binding.
5. Output mode explicit: exactly one output mode is named, with write destination and report destination if applicable.
6. Required checks named: validation gates can fail and include pass, fail, blocked, and not-run semantics.
7. Source-capsule budget satisfied: source capsules stay within
   `.agents/workflow-overlay/source-loading.md` budgets, or the prompt narrows
   the task, splits the source-loading unit, or moves to a new-thread handoff.
8. Source-gated method sequencing satisfied when triggered: prompts that
   orchestrate workflow methods as an explicit reasoning pipeline distinguish
   `REFERENCE-LOAD` from `APPLY`, include a `SOURCE_CONTEXT_READY` /
   `SOURCE_CONTEXT_INCOMPLETE` gate, and do not ask for method-derived
   conclusions before source readiness. An eligible lane-scoped delegated patch
   prompt may use its targeted review-lane or skill pointer without the magic
   phrase, while still requiring the receiver to read the real target sources
   before findings.
9. Thread operating target continuity satisfied: when a same-workstream prompt
   chain has a visible active `thread_operating_target`, the generated prompt
   either carries it forward verbatim with continuity disclosure or explains a
   valid omission, change, retirement, blocker, conflict, or owner omission.
   The target remains thread-local orientation only and must not be treated as
   authority, evidence, readiness, approval, lifecycle completion, sequencing
   authority, routing state, durable memory, or edit permission.
10. Retrieval metadata bounded: new or materially touched durable prompt
   artifacts use retrieval metadata only for source loading and do not create
   authority, validation proof, approval, readiness, lifecycle completion,
   deployment/install/resolver status, or edit permission.
11. Review doctrine satisfied (per Review Prompt Defaults above):
   (a) invoke `workflow-adversarial-artifact-review` after source readiness or block strict claims as advisory-only;
   (b) findings-first output by default; bind any formal verdict, severity contract, blocked/ready status, validation/readiness claim, mandatory remediation, patch queue, or executor-ready handoff;
   (c) include `minimum_closure_condition` and `next_authorized_action` for actionable findings; define closure conditions as required end states, not implementation instructions;
   (d) label optional hardening optional and non-required; exclude `patch_queue_entry` unless the lane is patch-queue or patch/integration execution;
   (e) preserve Chief Architect consumption order for CA-facing reviews; do not add a synthesis lane;
   (f) do not recommend, prescribe, rank, or imply a runtime model;
   (g) for intent-bearing targets, anchor decision criteria to a bound fitness reference or require the review to name its absence as `no checkable success bar bound`;
   (h) record `reviewed_by` and `authored_by` on every new or materially touched review output — operator/CA-supplied, `unrecorded` allowed, never fabricated; a present `unrecorded` value is a visible measurement gap, not a captured measurement;
   (i) coverage-first find stage: reviewers report every issue found with severity and confidence labels; importance/confidence filtering happens at adjudication, not at find time; steelman-defeated candidates surface in `considered_and_defended`.
12. Doctrine propagation satisfied: prompt, handoff, wrapper, review,
   output-mode, or execution-contract changes that alter durable doctrine carry
   a `direction_change_propagation` receipt or
   `direction_change_propagation_blocker` under
   `.agents/workflow-overlay/source-of-truth.md`, or block strict completion,
   readiness, validation, `PASS`, `ADEQUATE_NOW`, acceptance, and
   alignment-complete claims.
13. Rerun economy satisfied: retry prompts preserve frozen decisions and avoid scope reset.

## Prompt Verdicts

- `PASS`: all required prompt gates are satisfied.
- `PASS_WITH_WARNINGS`: prompt may be used, but named assumptions or unknowns must travel with it.
- `BLOCKED`: required authority, role binding, source, or preflight data is missing.
- `FAILED`: the prompt violates a hard constraint, imports forbidden policy, or changes output mode without authority.

## Anti-Import Rules

- Do not copy `jb` prompt templates, skill files, GAP/CV Engine policy, compiler paths, handoff rules, product-lead rules, or repo-local lifecycle mechanics.
- Do not claim `workflow-product-ultraplan`, `workflow-feature-ultraplan`, or `workflow-prompt-orchestrator` are executable unless a real resolver-visible `SKILL.md` exists and Forseti source-resolution/adoption checks pass.
- Generic layout ideas may be reused only after binding to Forseti paths, artifact roles, output modes, and validation gates.

## Direction Change Propagation

```yaml
# handoff transport/publication split 2026-07-14 (owner-requested correction).
direction_change_propagation:
  doctrine_changed: >
    Handoff-only packets now become dispatch-ready through an exact,
    actual-route-verified commit pointer before couriering, while PR creation is
    reserved for independently justified publication on main rather than packet
    discovery or transport.
  trigger: workflow_authority
  related_triggers: [output_authority, lifecycle_boundary]
  controlling_sources_updated:
    - AGENTS.md
    - .agents/workflow-overlay/prompt-orchestration.md
    - .agents/workflow-overlay/source-of-truth.md
    - docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
  downstream_surfaces_checked:
    - CLAUDE.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/decision-routing.md
    - .agents/workflow-overlay/validation-gates.md
    - .agents/workflow-overlay/safety-rules.md
    - .agents/workflow-overlay/communication-style.md
    - .agents/hooks/check_handoff_pointers.py
    - .agents/hooks/README.md
    - docs/workflows/forseti_repo_map_v0.md
  intentionally_not_updated:
    - path: CLAUDE.md
      reason: >
        It remains a shim importing AGENTS.md and must not duplicate the new
        kernel pointer.
    - path: .agents/workflow-overlay/source-loading.md
      reason: >
        Source packs and confirm-don't-trust loading are unchanged; this rule
        governs how a packet reaches the receiver before source loading begins.
    - path: .agents/workflow-overlay/decision-routing.md
      reason: >
        It still owns receiver-mechanism and write-root selection. The new
        exact-byte transport proof is the prompt/handoff owner's downstream use
        of that selected mechanism, not a competing receiver selector.
    - path: .agents/workflow-overlay/validation-gates.md and .agents/hooks/check_handoff_pointers.py
      reason: >
        The existing gate correctly checks durable in-repo pointer resolution
        and explicitly cannot observe chat, PR comments, or receiver access.
        Extending it would create a fake actual-route check; resident dispatch
        verification remains in prompt-orchestration.md.
    - path: docs/workflows/forseti_repo_map_v0.md
      reason: >
        The map already routes prompt/handoff mechanics and developer workflow
        to the changed controlling files; no file family or owner moved.
    - path: historical prompts, handoffs, and review outputs
      reason: >
        Forward-only doctrine change; completed lane evidence is not rewritten.
  stale_language_search: >
    rg -n -i "handoff.{0,80}(standalone|whole).{0,30}PR|handoff.{0,80}(push|PR preparation)|PR.{0,80}(discover|transport).{0,40}handoff|commit.{0,40}handoff.{0,40}(landed|publication)"
    AGENTS.md CLAUDE.md .agents/workflow-overlay .agents/hooks
    docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
    docs/workflows/forseti_repo_map_v0.md
  stale_language_search_result: >
    Executed 2026-07-14 after the live-authority edits. Hits were the new
    handoff-only push condition, this receipt's query, and the retained prior
    receipt describing the compatible no-standalone-doc-PR rule; no checked
    live surface still requires a PR merely for packet discovery or transport.
  non_claims:
    - not validation or readiness
    - not proof that a receiver actually has repository access
    - not publication or landing authority
    - not a weakening of normal implementation, doctrine, or code PR flow

# whale-first token/latency economy fixes 2026-07-12 (owner-approved insights follow-up).
direction_change_propagation:
  doctrine_changed: >
    Four owner-approved efficiency rules: the AGENTS.md kernel now bans
    uncommissioned adversarial self-review of an agent's own diff (CI plus any
    commissioned review are the defect gate) and presumes untracked files are
    authored artifacts requiring provenance confirmation before destructive
    branch/worktree/PR actions; the lane-scoped filing rule now explicitly
    covers handoff packets and closeout docs (no standalone doc PRs by
    default); and a repo-constant Windows/PowerShell `environment_baseline`
    is bound in the shared preflight defaults and pointed at by the compact
    delegated prompt default.
  trigger: workflow_authority
  related_triggers: [review_authority]
  controlling_sources_updated:
    - AGENTS.md
    - .agents/workflow-overlay/prompt-orchestration.md
    - docs/prompts/templates/shared/forseti_preflight_defaults_v0.md
    - docs/decisions/dcp_receipts_archive_v0.md
  downstream_surfaces_checked:
    - CLAUDE.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/review-lanes.md
    - .agents/workflow-overlay/delegated-review-patch.md
    - .agents/workflow-overlay/communication-style.md
    - .agents/workflow-overlay/validation-gates.md
    - .agents/workflow-overlay/safety-rules.md
    - .agents/workflow-overlay/source-loading.md
    - docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
    - docs/workflows/forseti_repo_map_v0.md
  intentionally_not_updated:
    - path: CLAUDE.md
      reason: >
        It remains a shim importing AGENTS.md and must not duplicate kernel
        rules.
    - path: .agents/workflow-overlay/review-lanes.md
      reason: >
        Commissioned review lanes and CA adjudication of a self-review are
        unchanged; the kernel ban covers only uncommissioned self-review of an
        agent's own diff.
    - path: .agents/workflow-overlay/delegated-review-patch.md
      reason: >
        Its fallback to source-read-only review plus CA self-review is a
        commissioned review act and remains valid; de-correlation doctrine is
        unchanged.
    - path: .agents/workflow-overlay/source-of-truth.md
      reason: >
        Checkpoint-artifact lifecycle (non-authoritative, single-consumption)
        is unchanged; the filing extension only decides which PR carries a
        committed handoff doc.
    - path: docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
      reason: >
        It already rides planning/scoping artifacts with their work unit; the
        handoff/closeout extension is same-direction and owned by the filing
        section here.
    - path: .agents/workflow-overlay/safety-rules.md
      reason: >
        The protected-action guard and deletion-evidence gate still enforce
        destructive-command safety; the untracked-files presumption is
        upstream always-loaded kernel behavior, not a guard change.
    - path: docs/workflows/forseti_repo_map_v0.md
      reason: no path, owner, or retrieval route changed.
  stale_language_search: >
    rg -n -i "self.review|untracked|standalone.{0,40}PR|python3|drive-letter"
    AGENTS.md .agents/workflow-overlay docs/prompts/templates
    docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
  stale_language_search_result: >
    Executed 2026-07-12 after edits, before commit. All self-review hits are
    commissioned lanes (CA adjudication in communication-style.md and this
    file; the delegated-review-patch fallback), compatible with the
    uncommissioned-only ban. Untracked hits are state-classification
    vocabulary and the same-direction deletion-refusal safety in the dev
    workflow doctrine; no surface labels untracked files disposable.
    Standalone-PR hits are the existing planning-artifact and prompt filing
    rules plus this edit; no surface mandates bash or python3 for Windows
    work.
  non_claims:
    - not validation or readiness
    - no numeric token or latency savings claim
    - not a weakening of commissioned review, CI gates, the deletion-evidence
      gate, or the protected-action guard
```

Older receipts archived verbatim in `docs/decisions/dcp_receipts_archive_v0.md`.
