# Prompt Orchestration

```yaml
retrieval_header_version: 1
artifact_role: Orca overlay authority
scope: Prompt artifact families, output modes, preflight fields, and prompt validation gates.
use_when:
  - Creating or reviewing Orca prompt artifacts.
  - Checking prompt output mode, preflight, or review-report rules.
authority_boundary: retrieval_only
```

This file defines Orca's lightweight prompt-orchestration layer: Orca-owned prompt mechanics, output modes, preflight, and validation gates, without importing `jb` project policy and preserving Orca's explicit-authorization boundary for implementation and runtime work.

## Source Boundary

Orca-specific facts, product constraints, artifact paths, review lanes, validation gates, and safety rules must come from `AGENTS.md`, this overlay, or accepted Orca docs named in `.agents/workflow-overlay/source-of-truth.md`. Prompt mechanics come from those same sources; see Required Preflight Fields below for the field-level authority list.

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

`prompt_orchestrator.yaml`, `product-ultraplan.yaml`, and `feature-ultraplan.yaml` are non-executable queue records unless later accepted source creates real workflow skills and Orca validates adoption. Do not create `SKILL.md`, install skills, or copy `jb` templates from Orca prompt-orchestration work.

## Prompt Orchestrator Binding

```yaml
prompt_orchestrator:
  source_loading_policy: .agents/workflow-overlay/source-loading.md
```

All Orca prompt-orchestrator work must use the source-loading policy above; do not substitute generic, `jb`, plugin, or installed-skill defaults.

## Source-Gated Method Contract

Repo-aware prompts that combine workflow methods with task sources must separate
method reference loading from method application.

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

Required sequence for repo-aware prompts:

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

Subagents, model-facing prompts, and blind contestant prompts must satisfy the
same contract. Do not send a subagent only the method and question when the task
requires source-backed reasoning; provide the same source pack or a bounded
source capsule, or require the subagent to perform its own source-readiness
gate.

For an orientation or research subagent whose output returns to an agent, bind
the return shape, not just the source side. Require a terse, schema-bound verdict
— the exact fields named in the dispatch prompt, one line per field, a `file:line`
cite for every load-bearing claim, and `unknown` for an absent field — not a
prose dump. Source-readiness stays governed by the rule above and
`.agents/workflow-overlay/source-loading.md` (the load-side owner); here the
spawning CA names that load in the dispatch, escalates minimally, and validates
the return on receipt: reject or re-prompt a non-conforming or citation-less
reply rather than consuming it. "Returns to an agent" covers any output an agent
will act on, summarize, or route — even output later shown to a human; the only
exception is a deliverable meant directly for a human with no agent acting on it.
The return dimension is distinct from subagent source-readiness (above) and from
forked-context runtime-payload safety (`decision-routing.md`).

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

Orca-local prompt templates live under `docs/prompts/templates/`.
The active Orca template registry is
`.agents/workflow-overlay/template-registry.md`.

The registry binds template kinds, template targets, output modes, and template
paths for Orca. Template targets are prompt-shaping labels only; they are not
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

Always author Orca prompts, handoffs, wrappers, rerun prompts, and patch prompts
**through `workflow-prompt-orchestrator`**. Hand-drafting bypasses source-loading
and the preflight/routing contract and is a prompt-quality defect even when the
surface text looks complete — the defect is the skipped contract. If
`workflow-prompt-orchestrator` is not resolver-available, apply this file's
contract in full or return a visible blocker; this routing default does not claim
the skill is an adopted or resolver-validated executable.

## Default Path Assignment

The user is not responsible for naming routine Orca artifact paths.

When a user asks for a prompt artifact without naming a path, choose the
narrowest accepted Orca folder from `.agents/workflow-overlay/artifact-folders.md`
and the Supported Prompt Families table above, and create a deterministic,
descriptive versioned filename. Example: a review prompt goes to
`docs/prompts/reviews/<descriptive_slug>_prompt_vN.md` with a downstream report
at `docs/review-outputs/adversarial-artifact-reviews/<descriptive_slug>_review_vN.md`
(or `docs/review-outputs/<descriptive_slug>_review_vN.md` when no narrower child
folder is bound) unless the user explicitly requests chat-only review.

Repo-aware prompts handed to another model, agent, thread, or worktree must
state both:

- the prompt artifact path the reviewer or downstream agent should treat as
  the input prompt source; and
- the exact output artifact path the reviewer or downstream agent should write,
  when the output mode writes a durable artifact.

Ask the user for a path only when the destination cannot be determined from the
artifact role, accepted folders, requested workflow, or collision state. If a
chosen path already exists, choose the next version suffix or return a visible
collision blocker when versioning would change the intended target.

## Full Prompt Versus Thin Wrapper

A full prompt is the durable artifact. It must include:

- the retrieval header from `.agents/workflow-overlay/retrieval-metadata.md`
  when the prompt is new or materially touched;
- objective and intended decision;
- Orca source hierarchy and required reads;
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

## Review Prompt Defaults

All Orca review prompts must include `workflow-deep-thinking` before the
relevant review skill, such as `workflow-adversarial-artifact-review` or
`workflow-code-review`, under the Source-Gated Method Contract. The reviewer
may `REFERENCE-LOAD` the methods before source loading, but must not `APPLY`
deep-thinking or the review method until the required source context is ready.

The deep-thinking step should frame the boundary problem, failure modes, and
decision criteria before findings are listed. It does not widen the review
scope, authorize patching, or turn a narrow review into product planning.

Review prompts should still return the requested review output shape. Deep
thinking improves the reviewer's risk framing; the final answer remains a
review report with findings, non-findings, not-proven boundaries, and next
authorized step.

Review prompts, wrappers, handoffs, and closeouts must not recommend,
prescribe, rank, or imply runtime model choice for review lanes. They may route
by review lane, method/skill, target, authority, output mode, destination, and
prompt-template target only. Template targets are prompt-shaping guidance;
runtime model choice for review work is outside Orca review-lane authority.

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

Every Orca adversarial artifact review prompt must invoke
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
for severity labels, it must either use an Orca-bound severity set such as
`critical`, `major`, and `minor` for finding priority only, or define the
prompt-specific severity contract.

Actionable review findings should include:

- `minimum_closure_condition`: what must become true before the finding can be
  treated as closed. It states the required end state, not how to implement it;
- `next_authorized_action`: what the current lane may do next under its
  authority.

Within the commission-bound target and purpose, adversarial review prompts
should ask reviewers to be maximally adversarial about material
decision-relevant failure modes. Optional hardening may be named only when
clearly labeled optional and non-required.

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
reconciliation unless Orca later binds one explicitly.

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

## Required Preflight Fields

Every repo-aware Orca prompt must include or reference the
`orca_start_preflight` receipt owned by
`.agents/workflow-overlay/source-loading.md`. Prompt authors may record the
fields in that receipt or in adjacent preflight prose, but the prompt must make
the start state checkable. Repo-constant fields (workspace path, required reads,
external source boundary, retrieval header defaults) may be referenced via
`docs/prompts/templates/shared/orca_preflight_defaults_v0.md` instead of
restated; required per-prompt deltas listed in that artifact must still be
stated explicitly in every prompt that references it.

Every repo-aware Orca prompt must state:

- whether `AGENTS.md` and `.agents/workflow-overlay/README.md` were read or
  supplied in the current task context;
- selected source pack from `.agents/workflow-overlay/source-loading.md`, or a
  bounded custom source pack;
- `repo_map_decision: loaded | not_needed | unavailable`, plus `repo_map_reason`. Source-loading (`.agents/workflow-overlay/source-loading.md`) owns the read-pack rule; this field records the prompt author's routing decision and must not make the repo map a mandatory read;
- workspace path or repository identifier;
- expected branch, detached revision, or commit hash when source stability matters;
- dirty-state allowance and whether untracked files are in scope;
- controlling-source state when strict claims depend on Orca overlay,
  source-loading, repo-map, prompt-policy, validation, or artifact-role files:
  clean, modified, untracked, stale, or not checked;
- whether the work changes product doctrine, architecture doctrine, workflow
  authority, validation philosophy, review authority, output authority, or a
  lifecycle boundary, and if so which propagation surfaces must be checked
  before closeout;
- target files or directories;
- source hierarchy for the task;
- edit permission: `read-only`, `patch-only`, or `docs-write`;
- output mode: `chat-only`, `file-write`, `review-report`,
  `paste-ready-chat`, or `patch-queue`;
- required validation gates and where evidence is recorded;
- external source boundary, including the rule that external workflow source is read-only from Orca work and `jb` is not Orca authority.

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
- `file-write`: write only authorized Orca documentation or overlay files;
  report changed files and validation evidence. For substantial
  decision-bearing artifacts, chat closeout must include a concise headed human
  summary before the artifact receipt.
- `review-report`: perform read-only review unless a patch-execution lane is explicitly assigned; write reports under `docs/review-outputs/` or a typed child folder, then return the compact YAML review summary in chat only after the report write succeeds. If the required report write fails, return `status: failed`, `review_location: chat_only_current_thread`, and `recommendation: blocked` in chat without `report_path`, name the failed path, and include enough human-readable failure detail to route.
- `paste-ready-chat`: return one prompt, wrapper, handoff, or review request
  body in chat for copying into another model, agent, thread, or worktree. The
  pasted body may be the artifact, but any surrounding Chief Architect,
  planning, overlay gate, or routing decision should still use the human-readable
  chat shape from `.agents/workflow-overlay/communication-style.md`.
- `patch-queue`: produce stable patch units, target files, authority basis, and validation gates. Applying patches requires separate execution authority.

The general human-summary / agent-detail / optional courier-state chat shape is owned by `.agents/workflow-overlay/communication-style.md`. This file owns output-mode exceptions to that shape:

- `review-report` may use YAML-only chat only after the required durable report has been successfully written; failed durable writes must use `review_location: chat_only_current_thread`, `status: failed`, `recommendation: blocked`, name the failed path, and include enough human-readable routing detail.
- `file-write` may return a compact path/hash/status receipt when the durable artifact carries the human-readable value; substantial decision-bearing writes must close with a headed human summary first (recommendation, why it matters, material boundaries, next authorized step), then receipt. If the write fails or the chat carries a decision, return readable blocker detail. Doctrine-changing file writes must include a `direction_change_propagation` receipt or blocker from `.agents/workflow-overlay/source-of-truth.md`.
- `paste-ready-chat` may prioritize the paste-ready body when that body is the deliverable; do not use this mode to hide a Chief Architect, planning, scoping, overlay gate, or completion decision.
- `patch-queue` may use stable structured units, but applying patches requires separate execution authority and readable blocker routing.

## Prompt Validation Gates

Authoring-route precondition: the prompt, handoff, wrapper, rerun, or patch
prompt must have been authored through `workflow-prompt-orchestrator` (see
"Author Through The Prompt Orchestrator"). A hand-drafted artifact that skipped
the orchestrator — and therefore source-loading and this preflight/routing
contract — is a prompt-quality defect; reconstruct it through the orchestrator,
or apply this file's contract in full and record that, before use.

Before using a generated Orca prompt, apply these gates:

1. Start preflight complete: `AGENTS.md` and
   `.agents/workflow-overlay/README.md` were read or supplied in the current
   task context; source pack, edit permission, target scope, and dirty-state
   check are recorded according to `.agents/workflow-overlay/source-loading.md`.
   Modified or untracked controlling sources block strict readiness,
   acceptance, validation, proof, `PASS`, or `ADEQUATE_NOW` claims unless owner
   acceptance or controlling authority is explicit.
2. Artifact roles bound: every prompt role maps to `.agents/workflow-overlay/artifact-roles.md` or another accepted overlay file.
3. Source resolution clean: external workflow sources do not provide Orca authority; installed skills are deployment copies; `jb` project policy is not imported.
4. Worktree preflight present: workspace, revision, dirty-state allowance, target scope, and edit permission are explicit when repository state matters.
5. Output mode explicit: exactly one output mode is named, with write destination and report destination if applicable.
6. Required checks named: validation gates can fail and include pass, fail, blocked, and not-run semantics.
7. Source-capsule budget satisfied: source capsules stay within
   `.agents/workflow-overlay/source-loading.md` budgets, or the prompt narrows
   the task, splits the source-loading unit, or moves to a new-thread handoff.
8. Source-gated method sequencing satisfied: prompts that mention workflow
   methods or skills distinguish `REFERENCE-LOAD` from `APPLY`, include a
   `SOURCE_CONTEXT_READY` / `SOURCE_CONTEXT_INCOMPLETE` gate, and do not ask for
   method-derived conclusions before source readiness.
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
   (h) record `reviewed_by` and `authored_by` on every new or materially touched review output — operator/CA-supplied, `unrecorded` allowed, never fabricated; a present `unrecorded` value is a visible measurement gap, not a captured measurement.
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
- Do not claim `workflow-product-ultraplan`, `workflow-feature-ultraplan`, or `workflow-prompt-orchestrator` are executable unless a real resolver-visible `SKILL.md` exists and Orca source-resolution/adoption checks pass.
- Generic layout ideas may be reused only after binding to Orca paths, artifact roles, output modes, and validation gates.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Orca prompt authoring now has an explicit routing rule: all prompt, handoff,
    wrapper, rerun, and patch-prompt authoring must go through
    workflow-prompt-orchestrator (the prompt-orchestration owner that applies
    source-loading and the preflight/routing contract); hand-drafting any of them
    is a prompt-quality defect, and AGENTS.md now carries the up-front trigger
    pointing here.
  trigger: workflow_authority
  controlling_sources_updated:
    - .agents/workflow-overlay/prompt-orchestration.md
    - AGENTS.md
  downstream_surfaces_checked:
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/skill-adoption.md
    - .agents/workflow-overlay/template-registry.md
    - .agents/workflow-overlay/validation-gates.md
    - docs/prompts/templates/_generic/
  intentionally_not_updated:
    - path: .agents/workflow-overlay/README.md
      reason: >
        The overlay index already names prompt-orchestration.md as the owner of
        prompt artifact, wrapper, preflight, and output-mode rules; the routing
        rule lives in that owner file and needs no index restatement.
    - path: .agents/workflow-overlay/validation-gates.md
      reason: >
        Its Prompt Orchestration Gates already defer to prompt-orchestration.md
        as the prompt-mechanics owner; single-source is preserved by adding the
        enforcement precondition in that owner file, not by duplicating it here.
    - path: .agents/workflow-overlay/skill-adoption.md
      reason: >
        Its caution that workflow-prompt-orchestrator adoption needs a resolver
        recheck is unchanged and is explicitly preserved by the new rule's
        fallback clause; the routing default does not assert strict adoption.
    - path: .agents/workflow-overlay/template-registry.md
      reason: >
        It governs template-target retrieval, not prompt-authoring routing; the
        new rule does not change template fallback behavior.
    - path: .agents/workflow-overlay/source-of-truth.md
      reason: >
        Source hierarchy and the propagation contract are unchanged; the only hit
        is an unrelated historical rg pattern in a prior receipt.
    - path: docs/prompts/templates/_generic/
      reason: >
        Model-target templates retired 2026-06-13 (unused; owner decision); no
        longer a live surface. Prior receipt preserved for history only.
  stale_language_search: >
    rg -i -n "prompt-orchestrator|hand-draft|hand-drafted|route through" .agents docs AGENTS.md
    (run 2026-06-09 on main @ cc93187 in the worktree)
  stale_language_search_result: >
    Executed 2026-06-09. No surface stated an opposing rule (no surface permits
    hand-drafting prompts or bypassing source-loading). Existing prompt-orchestrator
    hits are the binding, the Anti-Import adoption caution, the skill-adoption
    recheck note, template-target references, and an unrelated historical rg pattern
    in source-of-truth.md — none conflicts with or duplicates the new routing rule.
  non_claims:
    - not validation
    - not readiness
    - not a claim that workflow-prompt-orchestrator is an adopted or resolver-validated executable
    - not implementation authorization
    - not source promotion
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    Model-target template retrieval retired (unused; no-runtime-model-routing
    rules retained and tightened); preflight defaults artifact
    (docs/prompts/templates/shared/orca_preflight_defaults_v0.md) blessed for
    referencing repo-constant preflight fields, with required per-prompt deltas
    still mandatory in every referencing prompt.
  trigger: workflow_authority
  controlling_sources_updated:
    - .agents/workflow-overlay/prompt-orchestration.md
    - .agents/workflow-overlay/template-registry.md
    - .agents/workflow-overlay/review-lanes.md
    - docs/prompts/templates/shared/orca_preflight_defaults_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/safety-rules.md
    - .agents/workflow-overlay/artifact-roles.md
    - docs/prompts/templates/README.md
  intentionally_not_updated:
    - path: AGENTS.md
      reason: >
        No model-target retrieval rule lives in AGENTS.md; the overlay-routing
        trigger is unchanged; no edit needed.
    - path: .agents/workflow-overlay/README.md
      reason: >
        The overlay index names template-registry.md as the template owner;
        retirement lives there; no index restatement needed.
    - path: .agents/workflow-overlay/source-of-truth.md
      reason: >
        Source hierarchy and propagation mechanics are unchanged; no model-target
        retrieval rule lives here.
    - path: .agents/workflow-overlay/safety-rules.md
      reason: >
        No model-target retrieval or _generic path referenced here; unaffected.
    - path: .agents/workflow-overlay/artifact-roles.md
      reason: >
        No model-target retrieval or _generic path referenced here; unaffected.
    - path: docs/prompts/templates/README.md
      reason: >
        Updated in 1e to remove _generic reference and note retirement; no
        further change needed.
  stale_language_search: >
    rg -i -n "generic-gpt|generic-claude|model-named template|template target" .agents docs AGENTS.md
    (run 2026-06-13 post-edit in worktree orca-template-retire-wt)
  stale_language_search_result: >
    Executed 2026-06-13. Live-overlay hits: template-registry.md and
    review-lanes.md and prompt-orchestration.md carry "template target" as
    allowed model-neutral terminology (prompt-shaping label, not routing) —
    these are the no-routing rules themselves, not stale doctrine.
    Non-live hits: docs/prompts/product-planning/ (1 hit — historical template
    basis note in a prior authored prompt, not a routing instruction);
    docs/research/judgment-spine/ (1 hit — research artifact with explicit
    "not a runtime model claim" disclaimer); docs/review-outputs/ (multiple
    hits — historical review records citing prior template IDs, archives only).
    No live-doctrine surface retains an instruction that routes agents to a
    model-target template or implies runtime model selection.
  non_claims:
    - not validation
    - not readiness
    - not source promotion
    - not implementation authorization
```

Older receipts archived verbatim in `docs/decisions/dcp_receipts_archive_v0.md`.
