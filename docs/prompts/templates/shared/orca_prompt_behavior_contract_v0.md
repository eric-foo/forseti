# Orca Prompt Behavior Contract v0

```yaml
retrieval_header_version: 1
artifact_role: Prompt template
scope: Shared Orca behavior contract for project-local prompt templates.
use_when:
  - A prompt template needs common Orca source, boundary, and non-claim rules.
authority_boundary: retrieval_only
```

Use this contract only when a prompt explicitly references it.

## Source Authority

- Current user instruction for the turn wins.
- Orca `AGENTS.md` and `.agents/workflow-overlay/` own Orca project facts.
- Orca docs under `docs/` are subordinate to the overlay when conflicts appear.
- `agent-workflow` may provide reusable mechanics only.
- `jb` paths, product rules, lifecycle mechanics, templates, validation habits,
  and handoffs are not Orca authority.

## Source-Gated Method Use

When a prompt references workflow methods or skills and also requires Orca
source context, follow `.agents/workflow-overlay/prompt-orchestration.md`'s
Source-Gated Method Contract.

- `REFERENCE-LOAD` method instructions before source loading only as procedural
  guidance.
- Do not `APPLY` any method to analyze, frame, critique, rank, synthesize,
  decide, recommend, or produce findings before source readiness.
- `SOURCE-LOAD` the task sources under the prompt's source pack.
- Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` with material
  gaps before applying methods.
- After source readiness, `APPLY` the methods to the loaded source context and
  verify conclusions against that context.

Avoid vague sequencing such as "use these skills" before source loading. Use
explicit reference-load and apply wording when method order matters.

## Output Discipline

- Name exactly one output mode.
- For decision-bearing chat, follow the chat-output topology in
  `.agents/workflow-overlay/communication-style.md`: human summary first,
  agent-readable detail second, and compact courier state last only when useful
  or required. Use clear headed prose by default; YAML is not required unless
  the user requests it, the output mode requires machine-shaped fields, or
  lane switching / handoff routing would materially benefit from compact
  courier YAML.
- Use `.agents/workflow-overlay/prompt-orchestration.md` for output-mode
  exceptions, including `review-report`, `file-write`, `paste-ready-chat`, and
  `patch-queue`.
- For substantial decision-bearing `file-write` artifacts, require a concise
  headed human summary plus artifact receipt. Do not let "do not paste the full
  artifact" collapse into path/hash/status-only chat.
- Keep missing source fields as `not_found`, `not_bound`, or `UNKNOWN - requires owner input`.
- Do not turn evidence collection into synthesis unless the prompt is a synthesis template.
- Do not claim validation, readiness, approval, deployment, install, resolver, buyer validation, willingness to pay, implementation readiness, feature readiness, or commercial readiness unless an accepted Orca source and current evidence explicitly bind that claim.
- For review prompts and reports, prefer a review-use boundary over a broad
  non-claims catalog: the review is decision input only and must not be treated
  as approval, validation, mandatory remediation, or executor-ready authority
  without separate acceptance. Add product-proof non-claims only when the review
  target or source authority makes those claims in scope.
- Review prompts should be findings-first by default. Formal verdicts,
  blocked/ready status, validation pass/fail claims, approval, readiness,
  mandatory remediation, patch queues, and executor-ready handoffs require Orca
  overlay or prompt binding. Actionable findings should state
  `minimum_closure_condition` and `next_authorized_action`. Do not request or
  emit `patch_queue_entry` unless a patch-queue review or patch/integration
  execution lane is explicitly bound.
- Adversarial artifact review prompts must invoke
  `workflow-adversarial-artifact-review` after `SOURCE_CONTEXT_READY`. If that
  skill is unavailable, unresolved, or not applied, the output must be blocked
  or advisory-only and must not emit strict review claims.
- In adversarial artifact reviews, `minimum_closure_condition` states what must
  become true for a failure mode to be resolved, not how to implement the fix.
  Optional hardening may be named only when labeled optional and non-required.
- CA-facing review prompts and handoffs should preserve Orca's review
  consumption order: commission, target, authority, decision criteria,
  evidence, then reviewer verdict or recommendation. Do not create a synthesis
  lane unless a later Orca overlay decision binds one.

## Source-Heavy Work

For public web or source-heavy tasks:

- define the unit of work before source loading starts;
- keep evidence URLs stable and citeable;
- avoid long pasted source text;
- separate evidence, synthesis, backtestability, and anonymous marketing claims;
- stop rather than continue if source loading becomes unbounded.

## Report Shape

Prefer compact outputs that preserve:

- objective;
- scope and date boundary;
- source list or source URL table;
- missing-field labels;
- blocker states;
- non-claims or review-use boundary;
- next authorized step.

Compactness means omit unnecessary fields and full source echoes. It does not
mean hiding a decision-bearing answer in YAML-only or agent-only structure.
Artifact-native tables, paste-ready prompt bodies, and post-artifact receipts
remain valid when the output mode permits them. For substantial file-written
decision artifacts, post-artifact receipts must be preceded by enough headed
human summary for the owner to understand the result without opening the file.
