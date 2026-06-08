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

This file defines Orca's lightweight prompt-orchestration layer. It binds
Orca-owned prompt mechanics without importing `jb` project policy, while
preserving Orca's explicit-authorization boundary for implementation and
runtime work.

## Source Boundary

Prompt mechanics come from Orca-owned source documents and queue records:

- prompt artifact creation and thin-wrapper prompts;
- worktree preflight and hash pins;
- explicit output mode;
- source hierarchy and hard constraints;
- required checks, verdicts, and rerun economy.

Orca-specific facts, product constraints, artifact paths, review lanes, validation gates, and safety rules must come from `AGENTS.md`, this overlay, or accepted Orca docs named in `.agents/workflow-overlay/source-of-truth.md`.

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

Orca prompt-orchestrator work must use the source-loading policy above when
choosing source packs, read budgets, source-heavy split points, and source
capsule boundaries. Do not substitute generic, `jb`, plugin, or installed-skill
source-loading defaults for Orca prompt-orchestrator work.

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

## Thread Operating Target Continuity

When a workflow prompt, wrapper, rerun, review prompt, patch prompt, or handoff
continues the same workstream with a visible active `thread_operating_target`,
preserve that target verbatim near the top of the generated prompt and include
a compact continuity disclosure.

A visible active `thread_operating_target` is not required for every prompt. It
is required only to carry the target forward or explain omission when the
generated prompt continues the same workstream or claims to optimize for the
same anchor goal.

Use this disclosure shape:

```yaml
thread_operating_target_continuity:
  carried_forward: yes | no
  reason: same_workstream | different_workstream | no_visible_active_target | retired_or_blocked | owner_omitted | conflict
  changed_from_input: no | yes
  lifecycle_status:
  if_changed_reason:
```

Treat `thread_operating_target` as thread-local orientation only. It is not
source authority, validation evidence, readiness, approval, lifecycle
completion, durable goal state, artifact authority, workflow sequencing
authority, automatic routing, cross-thread memory, registry state, or
permission to edit protected paths.

A `thread_operating_target` may be retired only by explicit owner intent,
achieved output that satisfies the current `output_fit_check`, or a visible
blocker that makes continued optimization invalid or impossible. Retirement
must be explicit. If retirement is due to a blocker, name the blocker and what
remains allowed. Downstream lanes may recommend retirement but must not retire
the target unless their prompt or owner authority explicitly grants that
action.

If a prompt claims to optimize for an anchored goal but omits a visible active
`thread_operating_target` without explaining why it was not carried forward,
treat that as a prompt-quality defect.

## Project Template Registry

Orca-local prompt templates live under `docs/prompts/templates/`.
The active Orca template registry is
`.agents/workflow-overlay/template-registry.md`.

The registry binds template kinds, template targets, output modes, and template
paths for Orca. A template target may be model-named because the prompt shape is
different for different receivers, but it is not runtime model routing. Check
the registry before using any generic prompt-orchestration template.

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

For goal-fitness-judged source-changing work -- work whose correctness is judged
by achieving an upstream goal (proofs, fixtures, calibration gates, plans,
operating structures, runbooks) rather than by internal or technical consistency
alone -- a concrete goal and observable success signal must be bound before
source-changing edits begin. This is the scoped fused/scoping fitness gate.
Technical or consistency-judged work (schema reconciliation, citation/grounding
fixes, mechanical patches, vocabulary-enforcement edits, provenance corrections)
is exempt. When the classification is ambiguous, prefer binding a pointer when
cheap but do not block absent the trigger; name the ambiguity. Owning decision:
`docs/decisions/work_unit_fitness_reference_v0.md`.

Prompt templates may also use `paste-ready-chat` when the intended output is a
single prompt, wrapper, or handoff body meant to be pasted into another model,
agent, thread, or worktree.

## Default Path Assignment

The user is not responsible for naming routine Orca artifact paths.

When a user asks for a prompt, review prompt, handoff, rerun, patch prompt, or
other repo-aware prompt artifact without naming a path, the prompt-authoring
agent must choose the narrowest accepted Orca folder from
`.agents/workflow-overlay/artifact-folders.md` and create a deterministic,
descriptive versioned filename.

Default destinations:

- review prompts: `docs/prompts/reviews/<descriptive_slug>_prompt_vN.md`;
- product-planning prompts: `docs/prompts/product-planning/<descriptive_slug>_prompt_vN.md`;
- feature-planning prompts: `docs/prompts/feature-planning/<descriptive_slug>_prompt_vN.md`;
- deep-thinking prompts: `docs/prompts/deep-thinking/<descriptive_slug>_prompt_vN.md`;
- handoff prompts: `docs/prompts/handoffs/<descriptive_slug>_prompt_vN.md`;
- rerun prompts: `docs/prompts/reruns/<descriptive_slug>_prompt_vN.md`;
- patch prompts: `docs/prompts/patches/<descriptive_slug>_prompt_vN.md`;
- thin wrappers: `docs/prompts/wrappers/<descriptive_slug>_wrapper_vN.md`.

For a review prompt, the prompt-authoring agent must also assign the downstream
review-report destination unless the user explicitly requests chat-only review.
Use the narrowest accepted report folder, normally
`docs/review-outputs/adversarial-artifact-reviews/<descriptive_slug>_review_vN.md`
for adversarial artifact reviews and `docs/review-outputs/<descriptive_slug>_review_vN.md`
when no narrower child folder is bound.

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

### Template Retrieval Versus Model Routing

Prompt authors may select registered templates such as `generic-gpt55`,
`generic-claude-sonnet46`, or `generic-claude-opus47` when the user asks for a
GPT-, Sonnet-, or Opus-style prompt. This retrieves prompt structure and
prompting posture only.

Template retrieval must not:

- claim a prompt will run on a particular model;
- recommend a runtime model;
- rank models;
- bind reviewer or executor selection;
- create implementation, validation, readiness, or lifecycle authority.

When a user names a model family as shorthand for style, interpret it as a
template target unless the user explicitly asks to route execution. If the
requested template target is missing from the registry or its file does not
exist, report the missing template target instead of substituting runtime model
routing.

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
the start state checkable.

Every repo-aware Orca prompt must state:

- whether `AGENTS.md` and `.agents/workflow-overlay/README.md` were read or
  supplied in the current task context;
- selected source pack from `.agents/workflow-overlay/source-loading.md`, or a
  bounded custom source pack;
- `repo_map_decision: loaded | not_needed | unavailable`, plus
  `repo_map_reason`, stating why this task does or does not need repo-map
  routing. Source-loading remains the owner of the actual read-pack rule; this
  field records the prompt author's repo-map decision and must not make
  `docs/workflows/orca_repo_map_v0.md` a mandatory read for every prompt;
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

The highest-token actions to carve out are external web page opens, search
result pages with noisy snippets, full artifact readbacks, pasted source-ledger
rows, pasted Evidence Units, and multi-case or multi-target accumulation in one
live thread. Prefer artifact-local detail plus compact chat receipts.

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

The general human-summary / agent-detail / optional courier-state chat shape is
owned by `.agents/workflow-overlay/communication-style.md`. This file owns
output-mode exceptions to that shape:

- `review-report` may use YAML-only chat only after the required durable report
  has been successfully written. Failed durable writes must not use
  `report_path`; they must use `review_location: chat_only_current_thread`,
  `status: failed`, `recommendation: blocked`, name the failed path, and give
  enough human-readable routing detail in the allowed summary fields.
- `file-write` may return a compact path/hash/status receipt after the durable
  artifact is written when that artifact carries the human-readable value and no
  material decision needs to be understood from chat. Substantial
  decision-bearing file writes must close with clear headed human summary first,
  then path/hash/status receipt. The summary should state the recommendation or
  verdict, why it matters, material boundaries or deferred items, and the exact
  next authorized step without pasting the full artifact, source ledger, option
  table, or evidence body. YAML is not required by default for `file-write`
  closeouts; use it when the user asks for it, an output contract needs
  machine-shaped fields, or lane switching / handoff routing would materially
  benefit from compact courier YAML. If the write fails or the chat itself
  carries a decision, return readable blocker detail instead of treating a
  receipt as a substitute artifact. If the file-write changes doctrine, the
  closeout must include a `direction_change_propagation` receipt or
  `direction_change_propagation_blocker` from
  `.agents/workflow-overlay/source-of-truth.md`.
- `paste-ready-chat` may prioritize the paste-ready body when that body is the
  deliverable. Do not use this mode to hide a Chief Architect, planning,
  scoping, overlay gate, or completion decision inside machine-only structure.
- `patch-queue` may use stable structured units, but applying patches still
  requires separate execution authority and readable routing of blockers.

## Prompt Validation Gates

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
11. Review doctrine satisfied: adversarial artifact review prompts invoke
   `workflow-adversarial-artifact-review` after source readiness or block strict
   claims as advisory-only; review prompts and review templates use
   findings-first output by default; bind any formal verdict, severity
   contract, blocked/ready status, validation claim, readiness claim, mandatory
   remediation, patch queue, or executor-ready handoff; include
   `minimum_closure_condition` and `next_authorized_action` for actionable
   findings; define closure conditions as required end states rather than
   implementation instructions; label optional hardening as optional and
   non-required; exclude `patch_queue_entry` unless the lane is patch-queue or
   patch/integration execution; preserve the Chief Architect consumption order
   when the review is CA-facing; do not recommend, prescribe, rank, or imply a
   runtime model for review lanes; treat model-named template targets as
   template retrieval only; do not add a synthesis lane; and, for
   intent-bearing review targets, anchor the decision criteria to a bound
   fitness reference (goal plus observable success signal) or require the
   review to name its absence as `no checkable success bar bound`; and record
   `reviewed_by` and `authored_by` (the reviewing model+version and the reviewed
   artifact's author model+version) as present fields on every new or materially
   touched review output, operator/CA-supplied with `unrecorded` allowed and
   never fabricated, observed provenance facts that do not select, recommend, or
   rank a runtime model, where a present `unrecorded` value is a visible
   measurement gap rather than a captured measurement.
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
