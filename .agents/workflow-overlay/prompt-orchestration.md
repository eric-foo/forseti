# Prompt Orchestration

```yaml
retrieval_header_version: 1
artifact_role: Forseti overlay authority
scope: Prompt artifact families, output modes, preflight fields, and prompt validation gates.
use_when:
  - Creating or reviewing Forseti prompt artifacts.
  - Checking prompt output mode, preflight, or review-report rules.
authority_boundary: retrieval_only
```

This file defines Forseti's lightweight prompt-orchestration layer: Forseti-owned prompt mechanics, output modes, preflight, and validation gates, without importing `jb` project policy and preserving Forseti's explicit-authorization boundary for implementation and runtime work.

**Routine read shape** (owned by `.agents/workflow-overlay/source-loading.md`,
Targeted Read Protocol): for routine prompt authoring, read the "Forseti Prompt
Preflight" section below plus the single section for your prompt family; a
full-file read is for fused, delegated-review-patch, and novel or cross-lane
prompt authoring.

## Forseti Prompt Preflight

Routine Forseti prompts apply this core inline — no skill reload. For an
ordinary, already-scoped, single-target prompt, this core is the complete
preflight contract; it does not inherit the Escalated Preflight Fields or require
a `forseti_start_preflight` receipt. Review Prompt Defaults and Output Modes still
govern when their task-specific triggers apply. State, per prompt:

1. **Output mode** — exactly one of `chat-only` · `file-write` · `review-report` · `paste-ready-chat` · `patch-queue`, plus its write/report destination.
2. **Template kind** — the bound template from `.agents/workflow-overlay/template-registry.md`, or `none`; template targets are prompt-shaping labels, never runtime-model routing.
3. **Edit permission · targets · branch** — `read-only` | `docs-write` | `patch-only` | `implementation-authorized`; target files or dirs; workspace, branch, and dirty-state allowance when repository state matters.
4. **Reviews** — findings-first by default; bind any formal verdict, severity, or patch queue explicitly; no runtime-model recommendation, ranking, or implication.
5. **Doctrine change** — work that changes product, architecture, workflow, validation, review, or output doctrine, or a lifecycle boundary, carries a `direction_change_propagation` receipt or blocker (`.agents/workflow-overlay/source-of-truth.md`).
6. **Destinations** — the input prompt source the receiver treats as run-authoritative (canonical artifact path, lane PR body/comment, or ignored scratch path), and the exact output-artifact path it writes when the mode writes a durable artifact.

Repo-constant fields (workspace path, required reads, external-source boundary,
retrieval-header defaults) may be referenced via
`docs/prompts/templates/shared/forseti_preflight_defaults_v0.md` when escalated
preflight applies. Routine prompts state only the core above; do not add unused
field placeholders or a start receipt for form completeness. Fused,
delegated-review-patch, and novel/cross-lane prompts author through
`workflow-prompt-orchestrator` and use the escalated contract below.

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
surface. The contract is applied at two depths:

- **Routine prompts** apply the **Forseti Prompt Preflight** core (above) inline — no
  skill reload. The core fully satisfies the contract for an ordinary,
  already-scoped, single-target prompt; it owes no escalated fields or durable
  start receipt solely because it is repo-aware.
- **Fused, delegated-review-patch, and novel or cross-lane prompts** author through
  the full **`workflow-prompt-orchestrator`** skill, which owns prompt
  source-loading and the full preflight/routing contract. **A prompt is never
  routine — always use the full skill — when it is doctrine-changing,
  delegated-review-patch, patch-queue or executor-ready, source-heavy,
  multi-target, cross-lane, reusable/canonical, or first-of-kind for its task.**
  Ordinary single-target read-only review prompts may use the routine path when
  they satisfy the Forseti Prompt Preflight core and Review Prompt Defaults and
  none of those escalation triggers apply.

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
  plus the downstream artifact the prompt asks the receiver to write.
- If a lane-scoped prompt later becomes reusable, doctrine-bearing, or otherwise
  source-like, promote it through the canonical `docs/prompts/**` path in the
  same lane PR when that lane owns the change, or in a dedicated prompt PR only
  when the prompt artifact itself is the work unit.

The `docs/prompts/**` PostToolUse hook (`check_prompt_provenance.py`) fires only
for canonical filed prompt writes and injects the preflight — output mode, edit
permission, source pack / required reads, the Source-Gated Method Contract, and
the doctrine-change receipt. Lane-scoped prompts use an accepted PR-carried or
scratch-carried path, so the author must carry the same preflight fields in the
prompt body or PR comment; missing preflight remains a prompt-quality defect.

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
Do not create a standalone prompt PR for that default.

Repo-aware prompts handed to another model, agent, thread, or worktree must
state both:

- the input prompt source the reviewer or downstream agent should treat as
  authoritative for that run: a canonical prompt artifact path, a lane PR
  body/comment location, or an ignored `docs/_inbox/` scratch path; and
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

Forseti review prompts must include `workflow-deep-thinking` before the
relevant review skill when the review is adversarial, formal-verdict,
doctrine- or authority-changing, delegated, patch-authorized, source-heavy,
high-ambiguity, high-stakes, or otherwise likely to fail from weak failure-mode
framing. Routine single-target read-only reviews may omit deep-thinking when the
commission is already scoped, non-doctrine, and technical-consistency judged.

When deep-thinking is invoked, the reviewer may `REFERENCE-LOAD` the methods
before source loading, but must not `APPLY` deep-thinking or the review method
until the required source context is ready. The step frames the boundary problem,
failure modes, and decision criteria before findings are listed. It does not
widen review scope, authorize patching, or turn a narrow review into product
planning.

Review prompts should still return the requested review output shape. The final
answer remains a review report with findings, non-findings, not-proven
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

Delegated review-and-patch commissions are repo-mode by default. `no_repo` is
selected only when the commission explicitly records `access: no_repo` and the
reason repository access is unavailable or intentionally excluded. Cross-vendor,
external, couriered, paste-ready, or portable delivery does not imply `no_repo`;
if the reviewing controller can inspect and patch the named repo/worktree, the
commission must assume repo access.

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

Fused, delegated-review-patch, novel, cross-lane, source-heavy, multi-target,
reusable/canonical, patch-queue, or executor-ready prompts include or reference
the `forseti_start_preflight` receipt owned by
`.agents/workflow-overlay/source-loading.md`. These cases must make their start
state portable because another actor or later lane will rely on it. Repo-constant
fields may be referenced via
`docs/prompts/templates/shared/forseti_preflight_defaults_v0.md`; required
escalated deltas in that artifact remain explicit. Routine prompts stop at the
core above.

Every escalated prompt must state:

- whether `AGENTS.md` and `.agents/workflow-overlay/README.md` were read or
  supplied in the current task context;
- selected source pack from `.agents/workflow-overlay/source-loading.md`, or a
  bounded custom source pack;
- `repo_map_decision: loaded | not_needed | unavailable`, plus `repo_map_reason`. Source-loading (`.agents/workflow-overlay/source-loading.md`) owns the read-pack rule; this field records the prompt author's routing decision and must not make the repo map a mandatory read;
- workspace path or repository identifier;
- expected branch, detached revision, or commit hash when source stability matters;
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

Repo-bound review and delegated-review prompts must treat a mismatch in the
receiver's launch checkout as a routing condition, not an immediate review
blocker. The prompt states the target identity as either an exact revision/hash
pin or required commit ancestry; exact pins remain exact, while an advancing
lane head may continue only when the prompt explicitly uses ancestry semantics.

Receiving preflight follows this order:

1. Check the launch checkout against the commissioned target.
2. On mismatch, inspect registered worktrees (`git worktree list --porcelain`
   or a harness-equivalent registry) for the named branch, detached revision, or
   required ancestry before returning a blocker.
3. When exactly one accessible worktree satisfies target identity, evaluate
   cleanliness, untracked-file allowance, target paths, and required validation
   in that worktree. Dirt in the unrelated launch/parent checkout is out of
   scope and does not fail the target's clean-tree gate.
4. Continue in the resolved worktree when the runtime can safely operate there.
   Patch-authorized work must use the harness's worktree-rooted/reroot mechanism
   before editing when cross-worktree writes are guarded; if safe rerooting is
   unavailable, return the nearest blocker with the resolved path and required
   reroot action instead of reviewing or patching a substitute checkout.
5. Block only when the target worktree is absent, ambiguous, inaccessible, has
   disallowed dirt, fails the exact revision or required-ancestry check, fails a
   pinned target hash, or cannot be safely rerooted for authorized writes.

This resolver is discovery of the commissioned source, not permission to use an
alternate branch, recreated copy, context pack, or summary as review evidence.
It does not weaken exact hash/revision pins or dirty-state rules; it prevents an
unrelated launch checkout from being mistaken for the commissioned target.

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
routine prompt, or the full `workflow-prompt-orchestrator` skill for a fused,
delegated-review-patch, or novel/cross-lane prompt. An artifact that skipped the
applicable contract is a prompt-quality defect; apply the core for a routine
prompt or reconstruct an escalated prompt through the orchestrator before use.
A durable start receipt is required only for the escalated cases.

Before using a generated Forseti prompt, apply these gates:

1. Applicable preflight complete: `AGENTS.md` and
   `.agents/workflow-overlay/README.md` were read or supplied in the current
   task context. Routine prompts carry the six-field core and no start receipt;
   escalated prompts carry the portable start receipt and fields above.
   Repository-state fields are stated only when material.
   Modified or untracked controlling sources block strict readiness,
   acceptance, validation, proof, `PASS`, or `ADEQUATE_NOW` claims unless owner
   acceptance or controlling authority is explicit.
2. Artifact roles bound: every prompt role maps to `.agents/workflow-overlay/artifact-roles.md` or another accepted overlay file.
3. Source resolution clean: external workflow sources do not provide Forseti authority; installed skills are deployment copies; `jb` project policy is not imported.
4. Worktree preflight present: workspace, exact-revision or required-ancestry expectation, dirty-state allowance, target scope, and edit permission are explicit when repository state matters; a launch-checkout mismatch routes through registered-worktree resolution before it can become a blocker.
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
# same-turn self-closure and required next-moves tail 2026-07-02 (CA decision).
direction_change_propagation:
  doctrine_changed: >
    Review adjudication closeout is hardened for one-turn completion: a
    self-closable material issue (closure within the adjudicator's own authority
    and the commissioned scope, such as applying the adjudicator's own
    modify/reject adjudications to the target) is closed in the same turn
    instead of ending the turn on a closure route; the material-move deep-think
    widens from 1-3 to 1-5; and the land-step plus material-moves tail becomes a
    required closeout element (1-5 named steps, or an explicit "none" with a
    one-line reason), so an adjudication that stops at the verdict is malformed.
  trigger: review_authority
  related_triggers: [output_authority, workflow_authority]
  controlling_sources_updated:
    - .agents/workflow-overlay/communication-style.md
    - .agents/workflow-overlay/prompt-orchestration.md
    - .agents/workflow-overlay/delegated-review-patch.md
    - docs/prompts/templates/review/delegated_review_return_adjudication_v0.md
  downstream_surfaces_checked:
    - path: .agents/workflow-overlay/review-lanes.md
      note: >
        Lane authority, findings-first defaults, and the head deep-thinking-first
        rule are unchanged; this edit tightens the adjudicator's closeout
        mechanics only and stays deferred here for shape.
    - path: AGENTS.md
      note: >
        Already routes delegated-review-patch and review/prompt doctrine to the
        owning overlay files; no root restatement added.
    - path: docs/workflows/orca_repo_map_v0.md
      note: >
        Index lines for the overlay files and the template stay accurate; this
        is an in-file doctrine edit, not a structural or navigation change.
  intentionally_not_updated:
    - path: .agents/workflow-overlay/review-lanes.md
      reason: >
        Its findings fields and lane rules already defer the closeout tail to
        communication-style.md; dual-homing the tail would fork the owner.
  stale_language_search: >
    rg -n "1-3 material|until the review is clean|only after a clean adjudication|only if no unresolved material issue|only when status is clean"
    .agents docs/prompts/templates AGENTS.md docs/workflows
  stale_language_search_result: >
    Executed 2026-07-02 after edits. In the declared scope the remaining hits
    are the retained non-self-closable bullet in communication-style.md, the
    historical 2026-06-30 inline receipt in delegated-review-patch.md, and the
    quoted search literals inside these receipts; no live doctrine or template
    surface still gates the material-moves tail on a pre-closure clean state,
    caps material moves at 1-3, or leaves the tail optional. A wider sweep of
    docs/prompts/reviews and docs/prompts/patches found the old wording only in
    three already-executed commission dispatch prompts, kept as historical lane
    records and not rewritten.
  non_claims:
    - not validation
    - not readiness
    - not a bound/mandatory/machine-routable review lane
    - not runtime model routing

# resolve-first repo-bound review target routing 2026-07-12 (owner-requested process improvement).
direction_change_propagation:
  doctrine_changed: "Repo-bound review and delegated-review preflight now resolves a launch-checkout mismatch against registered target worktrees before blocking, while preserving exact revision pins, target cleanliness rules, and the protected-path reroot guard."
  trigger: "workflow_authority"
  related_triggers:
    - "review_authority"
  controlling_sources_updated:
    - ".agents/workflow-overlay/prompt-orchestration.md"
    - "docs/prompts/templates/shared/forseti_preflight_defaults_v0.md"
    - "docs/prompts/templates/wrappers/thin_wrapper_v0.md"
    - "docs/decisions/dcp_receipts_archive_v0.md"
  downstream_surfaces_checked:
    - "AGENTS.md"
    - ".agents/workflow-overlay/delegated-review-patch.md"
    - ".agents/workflow-overlay/source-loading.md"
    - ".agents/workflow-overlay/safety-rules.md"
    - ".agents/workflow-overlay/review-lanes.md"
    - ".agents/workflow-overlay/template-registry.md"
    - ".agents/hooks/README.md"
    - ".codex/hooks/forseti_guard_codex_adapter.py"
    - "docs/workflows/forseti_repo_map_v0.md"
  intentionally_not_updated:
    - surface: "AGENTS.md"
      reason: "Its generic fresh-read lifecycle stop remains compatible, and it delegates prompt mechanics to the overlay."
    - surface: ".agents/workflow-overlay/delegated-review-patch.md"
      reason: "It already points to Escalated Preflight Fields; copying the resolver here would fork ownership."
    - surface: ".agents/workflow-overlay/source-loading.md"
      reason: "Its named-worktree targeted-read fast path is compatible; this change owns review target routing."
    - surface: ".agents/workflow-overlay/safety-rules.md and .codex/hooks/forseti_guard_codex_adapter.py"
      reason: "Non-current-worktree writes still reroot or fail closed; the resolver explicitly preserves that enforcement."
    - surface: ".agents/workflow-overlay/review-lanes.md"
      reason: "Review authority and destinations are unchanged; preflight mechanics belong to prompt orchestration."
    - surface: ".agents/workflow-overlay/template-registry.md"
      reason: "Template paths and lifecycle status are unchanged; registered templates were edited in place."
    - surface: "docs/workflows/forseti_repo_map_v0.md"
      reason: "No path or owner was added; the existing prompt-orchestration route remains authoritative."
    - surface: "installed workflow-prompt-orchestrator skill"
      reason: "The installed generic deployment copy is outside Forseti authority; the active project overlay owns target resolution."
    - surface: "historical executed prompts under docs/prompts/reviews"
      reason: "They are execution records, not reusable control surfaces, so they are not rewritten retroactively."
  stale_language_search: "rg -n -i 'mismatch.*(?:stop|block)|wrong revision|alternate checkout|clean tree required|launch checkout|registered worktree|exact-revision|required-ancestry|exact revision.*ancestry' AGENTS.md .agents/workflow-overlay docs/prompts/templates docs/workflows/forseti_repo_map_v0.md .codex/hooks.json .codex/hooks .agents/hooks/README.md"
  stale_language_search_result: "Executed 2026-07-12. Hits were the compatible AGENTS lifecycle line, the new owner and template pointers, and guard reroot enforcement; no live surface retained an immediate blocker before registered-worktree discovery. Historical executed prompts were intentionally excluded."
  non_claims:
    - "not validation"
    - "not readiness"
    - "not permission to weaken exact revision or hash pins"
    - "not permission to edit a non-current worktree"
    - "not substitute-source authority"
    - "not a retroactive rewrite of historical prompts"
```

Older receipts archived verbatim in `docs/decisions/dcp_receipts_archive_v0.md`.
