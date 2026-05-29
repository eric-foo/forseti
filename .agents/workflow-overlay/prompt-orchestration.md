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
reusable mechanics from `agent-workflow` to Orca-owned paths without importing
`jb` project policy, while preserving Orca's explicit-authorization boundary
for implementation and runtime work.

## Source Boundary

Reusable mechanics may come from `agent-workflow` source documents and queue records:

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

`prompt_orchestrator.yaml`, `product-ultraplan.yaml`, and `feature-ultraplan.yaml` are non-executable queue records unless later accepted source creates real workflow-kernel skills and Orca validates adoption. Do not create `SKILL.md`, install skills, or copy `jb` templates from Orca prompt-orchestration work.

## Project Template Registry

Orca-local prompt templates live under `docs/prompts/templates/`.
The active Orca template registry is
`.agents/workflow-overlay/template-registry.md`.

The registry binds template kinds, model variants, output modes, and template
paths for Orca. Check it before falling back to generic `agent-workflow`
prompt-orchestrator templates.

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

Prompt templates may also use `paste-ready-chat` when the intended output is a
single prompt, wrapper, or handoff body meant to be pasted into another model,
agent, thread, or worktree.

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

All Orca review prompts must explicitly trigger `workflow-deep-thinking`
before the relevant review skill, such as `workflow-adversarial-artifact-review`
or `workflow-code-review`.

The deep-thinking step should frame the boundary problem, failure modes, and
decision criteria before findings are listed. It does not widen the review
scope, authorize patching, or turn a narrow review into product planning.

Review prompts should still return the requested review output shape. Deep
thinking improves the reviewer's risk framing; the final answer remains a
review report with findings, non-findings, not-proven boundaries, and next
authorized step.

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
- workspace path or repository identifier;
- expected branch, detached revision, or commit hash when source stability matters;
- dirty-state allowance and whether untracked files are in scope;
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
- external source boundary, including the rule that `agent-workflow` is read-only reusable source and `jb` is not Orca authority.

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
- `file-write`: write only authorized Orca documentation or overlay files; report changed files and validation evidence.
- `review-report`: perform read-only review unless a patch-execution lane is explicitly assigned; write reports under `docs/review-outputs/` or a typed child folder, then return the compact YAML review summary in chat only after the report write succeeds. If the required report write fails, return `status: failed`, `review_location: chat_only_current_thread`, and `recommendation: blocked` in chat without `report_path`, name the failed path, and include enough human-readable failure detail to route.
- `paste-ready-chat`: return one prompt, wrapper, handoff, or review request
  body in chat for copying into another model, agent, thread, or worktree. The
  pasted body may be the artifact, but any surrounding Chief Architect,
  planning, phase-gate, or routing decision should still use the human-readable
  chat shape from `.agents/workflow-overlay/communication-style.md`.
- `patch-queue`: produce stable patch units, target files, authority basis, and validation gates. Applying patches requires separate execution authority.

The general human-summary / agent-detail / courier-YAML chat shape is owned by
`.agents/workflow-overlay/communication-style.md`. This file owns output-mode
exceptions to that shape:

- `review-report` may use YAML-only chat only after the required durable report
  has been successfully written. Failed durable writes must not use
  `report_path`; they must use `review_location: chat_only_current_thread`,
  `status: failed`, `recommendation: blocked`, name the failed path, and give
  enough human-readable routing detail in the allowed summary fields.
- `file-write` may return a compact path/hash/status receipt after the durable
  artifact is written when that artifact carries the human-readable value. If
  the write fails or the chat itself carries a decision, return readable
  blocker detail instead of treating a receipt as a substitute artifact. If the
  file-write changes doctrine, the closeout must include a
  `direction_change_propagation` receipt or
  `direction_change_propagation_blocker` from
  `.agents/workflow-overlay/source-of-truth.md`.
- `paste-ready-chat` may prioritize the paste-ready body when that body is the
  deliverable. Do not use this mode to hide a Chief Architect, planning,
  scoping, phase-gate, or completion decision inside machine-only structure.
- `patch-queue` may use stable structured units, but applying patches still
  requires separate execution authority and readable routing of blockers.

## Prompt Validation Gates

Before using a generated Orca prompt, apply these gates:

1. Start preflight complete: `AGENTS.md` and
   `.agents/workflow-overlay/README.md` were read or supplied in the current
   task context; source pack, edit permission, target scope, and dirty-state
   check are recorded according to `.agents/workflow-overlay/source-loading.md`.
2. Artifact roles bound: every prompt role maps to `.agents/workflow-overlay/artifact-roles.md` or another accepted overlay file.
3. Source resolution clean: agent-workflow material is source guidance only; installed skills are deployment copies; `jb` project policy is not imported.
4. Worktree preflight present: workspace, revision, dirty-state allowance, target scope, and edit permission are explicit when repository state matters.
5. Output mode explicit: exactly one output mode is named, with write destination and report destination if applicable.
6. Required checks named: validation gates can fail and include pass, fail, blocked, and not-run semantics.
7. Retrieval metadata bounded: new or materially touched durable prompt
   artifacts use retrieval metadata only for source loading and do not create
   authority, validation proof, approval, readiness, lifecycle completion,
   deployment/install/resolver status, or edit permission.
8. Doctrine propagation satisfied: prompt, handoff, wrapper, review,
   output-mode, or execution-contract changes that alter durable doctrine carry
   a `direction_change_propagation` receipt or
   `direction_change_propagation_blocker` under
   `.agents/workflow-overlay/source-of-truth.md`, or block strict completion,
   readiness, validation, `PASS`, `ADEQUATE_NOW`, acceptance, and
   alignment-complete claims.
9. Rerun economy satisfied: retry prompts preserve frozen decisions and avoid scope reset.

## Prompt Verdicts

- `PASS`: all required prompt gates are satisfied.
- `PASS_WITH_WARNINGS`: prompt may be used, but named assumptions or unknowns must travel with it.
- `BLOCKED`: required authority, role binding, source, or preflight data is missing.
- `FAILED`: the prompt violates a hard constraint, imports forbidden policy, or changes output mode without authority.

## Anti-Import Rules

- Do not copy `jb` prompt templates, skill files, GAP/CV Engine policy, compiler paths, handoff rules, product-lead rules, or repo-local lifecycle mechanics.
- Do not claim `workflow-product-ultraplan`, `workflow-feature-ultraplan`, or `workflow-prompt-orchestrator` are executable unless a real `agent-workflow` `SKILL.md` exists and Orca source-resolution/adoption checks pass.
- Generic layout ideas may be reused only after binding to Orca paths, artifact roles, output modes, and validation gates.
