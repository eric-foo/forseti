# Adversarial Artifact Review Template v0

```yaml
retrieval_header_version: 1
artifact_role: Prompt template
scope: Read-only adversarial review template for non-code Forseti artifacts.
use_when:
  - Reviewing prompts, research artifacts, product docs, decisions, or workflow artifacts.
authority_boundary: retrieval_only
```

Template target: model-neutral.

This template is prompt-shaping guidance only. It does not recommend, require,
rank, or route runtime model choice.

Output mode: `review-report` or `paste-ready-chat`

Use shared contract:
`docs/prompts/templates/shared/forseti_prompt_behavior_contract_v0.md`

```text
You are performing a read-only adversarial artifact review for Forseti.

Review target:
[FILL_ARTIFACT_PATH_OR_TEXT]

Review purpose:
[FILL_REVIEW_PURPOSE]

Fitness reference (intent-bearing targets only -- a stated goal plus an
observable success signal; pointer-preferred to a controlling contract,
decision, or gate that already carries the signal):
[FILL_GOAL_AND_SUCCESS_SIGNAL_OR_POINTER, or "none bound"]

preflight_defaults: docs/prompts/templates/shared/forseti_preflight_defaults_v0.md v0 - constants bound; deltas stated inline.

Template kind: `adversarial-artifact-review`

Required authority sources:
- intake constants per the preflight defaults above (`AGENTS.md`,
  `.agents/workflow-overlay/README.md`);
- `.agents/workflow-overlay/review-lanes.md` and the overlay sections it names
  for this review lane; load other overlay files targeted-section only when a
  finding, strict claim, or route depends on them.

Default review source pack:
- the review target;
- sources named by the target retrieval header only when material;
- `.agents/workflow-overlay/communication-style.md` when chat or report
  closeout shape matters;
- `.agents/workflow-overlay/template-registry.md` when reviewing, selecting, or
  applying prompt templates;
- [FILL_ADDITIONAL_TASK_SOURCES]

Source-read budget (default, not a gate):
Record a one-line-per-source disposition (`full`, `targeted <section>`,
`grep <token>`, `skip: <reason>`) before the heavy reads; full-read the review
target and any source that could materially change a finding, strict claim,
route, or blocker. Owner: High-Context Guard in
`.agents/workflow-overlay/source-loading.md`. Under-reading a material source
is a worse failure than over-reading a confirmatory one.

Edit permission:
Read-only unless the launch instruction explicitly assigns patch execution.

Required method sequence:
After the required source context is ready, first run this review lane's
internalized failure-mode-framing pass: frame the boundary problem, failure
modes, and decision criteria before any finding is listed. This framing pass
is defined here and carried by the review lane; where the deep-thinking
trigger rule owned by `.agents/workflow-overlay/prompt-orchestration.md`
(Review Prompt Defaults) fires for a review commission, this pass satisfies it
without a separate `workflow-deep-thinking` skill load. A separate
`workflow-deep-thinking` load remains the route for owner-invoked decision
work (explicit owner invocation or Mini God Tier), not for review commissions.

Then use `workflow-adversarial-artifact-review`.

If `workflow-adversarial-artifact-review` is unavailable, unresolved, or cannot
be applied after `SOURCE_CONTEXT_READY`, return a blocked or advisory-only
result. Do not emit formal verdicts, severity authority, blocked/ready status,
validation claims, readiness claims, mandatory remediation, patch queues,
executor-ready handoffs, or alignment-complete claims.

The framing pass does not widen review scope or authorize patching.

Review authority:
Findings-first (the Review Prompt Defaults default in
`.agents/workflow-overlay/prompt-orchestration.md`); formal verdicts,
blocked/ready status, validation claims, mandatory remediation, patch queues,
and executor-ready handoffs require explicit overlay or prompt binding.
`critical`/`major`/`minor` are finding-priority labels only. Within the
commission-bound target and purpose, be maximally adversarial and
coverage-first: report every issue found, including uncertain and low-severity
ones — adjudication ranks and filters, not the find stage. Do not retarget or
widen the review, and do not soften or drop a failure mode because remediation
is hard, confidence is low, or the finding seems minor.

Output mode and report contract:
Use exactly one output mode for the run. `review-report` and
`paste-ready-chat` mechanics — durable-report binding under
`docs/review-outputs/`, the compact `review_summary` YAML, and the failed-write
blocked shape — are owned by `.agents/workflow-overlay/prompt-orchestration.md`
(Output Modes) and `.agents/workflow-overlay/communication-style.md`; follow
them there. If no write authority or report destination is bound before review
work starts, use `paste-ready-chat` instead of `review-report`; never treat
chat YAML as a substitute for a required durable report.

Review checks:
- Source hierarchy and authority boundary.
- Internal consistency.
- Missing required inputs or unbound roles.
- Output mode and destination correctness.
- Downstream executability.
- Fitness to the bound goal and success signal, for intent-bearing targets:
  whether the target achieves its intended outcome. Attack whether the goal and
  signal are themselves right. If no fitness reference is bound, name `no
  checkable success bar bound` as a finding rather than inventing the goal.
- Leakage of `jb` project policy or template language.
- Overclaims, readiness claims, validation claims, buyer-proof claims, or commercial claims.

Findings:
List findings first, ordered by severity:
- critical
- major
- minor

For each finding include:
- severity;
- confidence (high / medium / low: your certainty the finding is real);
- location;
- issue;
- evidence;
- impact;
- minimum_closure_condition;
- next_authorized_action;
- recommended correction or advisory remediation direction.

`minimum_closure_condition` states what must become true for the failure mode
to be resolved. It is not an implementation instruction. Optional hardening may
be listed only when it is clearly labeled optional and non-required.

Do not include `patch_queue_entry` unless the launch instruction explicitly
binds patch-queue review or patch/integration execution authority. A
`patch_queue_entry` is executor-ready how-to, not ordinary read-only review
advice.

Low-confidence or minor findings may use a compact one-line form:
`severity | confidence | location | issue | advisory direction`. Compactness
lowers reporting cost only; it does not lower the finding's standing as
decision input.

After the findings, add a `considered_and_defended` section: one line per
candidate finding you defeated with a steelman defense (candidate plus the
defense that held). These are not findings and carry no severity, closure, or
action fields; they make the discard pile visible to the adjudicator. If none,
write `considered_and_defended: none`.

If no issues are found, say so and list residual risks or test gaps.

Read-budget audit (one line):
Close with a one-line read-budget audit -- initial versus actual dispositions
(full / targeted / skipped) and why any source expanded beyond its initial
disposition. It records budget fit; it is not a validation, readiness, or
coverage claim.

Review-use boundary:
This is a read-only review. Treat findings and non-findings as decision input
only, not as approval, validation, product proof, mandatory remediation, or
executor-ready instructions. Do not anchor downstream work to this review as
binding authority unless a separate authorized Forseti decision, patch,
validation, or implementation lane accepts it.
```
