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

Required authority sources:
- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/artifact-roles.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/validation-gates.md`

Default review source pack:
- the review target;
- sources named by the target retrieval header only when material;
- `.agents/workflow-overlay/communication-style.md` when chat or report
  closeout shape matters;
- `.agents/workflow-overlay/template-registry.md` when reviewing, selecting, or
  applying prompt templates;
- [FILL_ADDITIONAL_TASK_SOURCES]

Source-read budget (default, not a gate):
Before the heavy reads, record a one-line-per-source disposition in your
source-read ledger: `full`, `targeted <section>`, `grep <token>`, or
`skip: <reason>`.
Default to targeted-section or grep-to-claim reads for confirmatory
sources; use full reads for the review target (or bound target excerpt) and
whenever a source could materially change a finding, non-finding, strict claim,
route, or blocker. This is the High-Context Guard in
`.agents/workflow-overlay/source-loading.md` applied to review; it is not a cap
on thoroughness -- expand to a full read the moment a source could materially
change the current review judgment, noting why. Under-reading a material source
is a worse failure than over-reading a confirmatory one.

Edit permission:
Read-only unless the launch instruction explicitly assigns patch execution.

Required skill invocation:
Use `workflow-deep-thinking` first.

Then use `workflow-adversarial-artifact-review`.

If `workflow-adversarial-artifact-review` is unavailable, unresolved, or cannot
be applied after `SOURCE_CONTEXT_READY`, return a blocked or advisory-only
result. Do not emit formal verdicts, severity authority, blocked/ready status,
validation claims, readiness claims, mandatory remediation, patch queues,
executor-ready handoffs, or alignment-complete claims.

The deep-thinking step should frame the boundary problem, failure modes, and
decision criteria before findings are listed. It does not widen review scope or
authorize patching.

Review authority:
Use findings-first review output by default. Formal verdicts, blocked/ready
status, validation pass/fail claims, approval, readiness, mandatory
remediation, patch queues, and executor-ready handoffs require explicit Forseti
overlay or prompt binding. In this template, `critical`, `major`, and `minor`
severity labels are finding-priority labels only; they are not approval,
rejection, readiness, validation, or mandatory-remediation authority.

Review target and review purpose are commission-bound. Within that
commission-bound target and purpose, be maximally adversarial and
coverage-first: report every issue you find, including uncertain and
low-severity ones. Do not filter for importance or confidence at this stage --
a downstream adjudication pass ranks and filters findings. Materiality,
severity, and confidence are labels you attach, never thresholds for
reporting. Do not retarget or widen the review, and do not soften or drop a
failure mode because remediation would be difficult, confidence is low, or the
finding seems minor.

Output mode and report contract:
Use exactly one output mode for the run.

If output mode is `review-report`, bind a durable report destination under
`docs/review-outputs/` or a typed child folder before review work starts. The
human-readable review belongs in that durable report. Chat YAML is courier
output only and is valid only after the required durable report has been
successfully written.

After a successful report write, return the compact `review_summary` YAML from
`.agents/workflow-overlay/communication-style.md` with `status: completed` and
`report_path` pointing to the written report.

If the required report cannot be written after `review-report` is selected,
do not use `report_path` and do not treat chat YAML as a substitute report.
Return a failed blocked `review_summary` with `status: failed`,
`review_location: chat_only_current_thread`, and `recommendation: blocked`;
name the failed path and include enough human-readable failure detail in
`summary` or `next_action` to route the issue. Do not add extra YAML keys.

If no write authority or report destination is bound before review work starts,
use `paste-ready-chat` instead of `review-report`.

For `paste-ready-chat` reviews, start with the compact `review_summary` YAML
shape from `.agents/workflow-overlay/communication-style.md`, using
`review_location: chat_only_current_thread` and no `report_path`. Then provide
human-readable findings in prose. Courier YAML preserves routing state; it is
not a substitute for the review findings. Do not use `paste-ready-chat` to
replace a required `review-report` durable destination after review work
starts.

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
