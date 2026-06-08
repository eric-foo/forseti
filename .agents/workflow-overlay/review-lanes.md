# Review Lanes

```yaml
retrieval_header_version: 1
artifact_role: Orca overlay authority
scope: Orca review lanes, reviewer permissions, and executor boundaries.
use_when:
  - Selecting or checking an Orca review lane.
  - Confirming whether a reviewer may write reports or apply patches.
  - Resolving review prompt template retrieval without turning templates into model routing.
authority_boundary: retrieval_only
```

## Current Lanes

- Artifact review: read-only review of docs, decisions, prompts, and migration artifacts. Reviewers may write reports only under `docs/review-outputs/` unless a prompt authorizes a different Orca-owned report path.
- Adversarial artifact review: read-only adversarial review of docs, decisions,
  prompts, product-proof artifacts, and migration artifacts. Reports should go
  under `docs/review-outputs/adversarial-artifact-reviews/` unless a prompt
  names another Orca-owned report path. Formal adversarial artifact review must
  invoke `workflow-adversarial-artifact-review` after source context is ready.
  If that skill is unavailable, unresolved, or not applied, the run may return
  only a blocked or advisory-only result and must not emit strict review
  claims.
- Prompt review: read-only review of prompt artifacts, thin wrappers, source maps, output modes, and validation gates. Reports go under `docs/review-outputs/` unless the prompt names another Orca-owned report path.
- Patch-queue review: read-only review that produces ordered patch units. Applying those patches requires a separate patch or integration execution assignment.
- Patch or integration execution: applies accepted documentation patches inside Orca and reports changed files plus validation.
- Skill adoption review: deferred until a later turn authorizes adoption or shadow validation.
- Delegated review-and-patch (provisional, opt-in): a distinct Chief Architect-commissioned bounded-executor convention for hardening high-stakes authored artifacts, defined in `.agents/workflow-overlay/delegated-review-patch.md`. It is NOT one of the source-read-only review lanes and NOT machine-routable; in its default `repo` access mode the delegate patches the named target, while in its `no_repo` access mode the delegate is read-only/advisory (returns findings; the CA applies the patch, with a required de-correlated post-patch re-review) — the convention still owns it either way. The reviewer-read-only rule and the review-lane model-neutrality below are unchanged.

## Review Doctrine

Orca review mechanics are Orca-owned here: findings-first review output,
advisory critique from visible evidence, and strict authority boundaries for
formal review claims. Orca-local overlay files own concrete lane names,
destinations, result vocabulary, severity labels, validation gates, patch
routing, and Chief Architect consumption rules.

- Review target and review purpose are commission-bound. A reviewer must not
  silently retarget a review, widen the target, or treat an adjacent artifact as
  the actual review object unless the prompt or current user instruction binds
  that change.
- Within the commission-bound target and purpose, adversarial reviewers should
  be maximally adversarial about material decision-relevant failure modes. This
  does not widen the target; it means the reviewer should not soften or skip a
  material failure mode merely because remediation would be awkward.
- For intent-bearing review targets -- artifacts whose correctness is judged by
  fitness to an upstream goal (proofs, fixtures, calibration gates, plans,
  operating structures, runbooks, product-proof artifacts) rather than by
  internal or technical consistency alone -- the decision criteria the review
  applies should be anchored to a bound `fitness_reference`: a stated goal plus
  an observable success signal, pointer-preferred (cite the controlling upstream
  contract, decision, or gate that already carries the signal; write compact
  prose only when none exists). The fitness reference is an added alignment axis
  the reviewer must also attack -- the reviewer asks whether the goal and signal
  are themselves right -- never a pass-if-matches bar. It does not narrow the
  commission-bound adversarial posture and creates no approval, validation, or
  readiness.
- If an intent-bearing target arrives with no bound fitness reference, the
  review names the gap (`no checkable success bar bound`) as a finding rather
  than silently inventing the goal. This is review-side back-pressure, not new
  verdict authority, and it stays findings-first.
- The fitness-reference rule applies to adversarial artifact review. Code or
  implementation review is not extended here; its fitness bar (spec, tests,
  ground-truth substrate) is governed separately. The authoring home for the
  goal and success signal is framing/scoping (reuse `workflow-goal-framing`
  output); this doctrine routes that output and does not relocate or fork it.
  Owning decision: `docs/decisions/work_unit_fitness_reference_v0.md`.
- Review lanes emit findings by default. Formal verdicts, severity taxonomies,
  blocked/ready status, validation pass/fail claims, approval, readiness,
  mandatory remediation, and executor-ready patch queues are strict-shaped
  outputs and require Orca overlay or prompt binding.
- Orca adversarial artifact reviews may use `critical`, `major`, and `minor`
  severity labels for finding priority when the prompt or template names those
  labels. Those labels do not by themselves create approval, rejection,
  readiness, validation, or mandatory remediation authority.
- Actionable review findings should state the `minimum_closure_condition`:
  what must become true before the failure mode can be treated as resolved. The
  closure condition states the required end state, not how to implement it.
- Actionable review findings should state the `next_authorized_action`: what
  the current review authority allows next, such as owner decision, rerun,
  patch authorization request, or no action.
- Optional hardening may be identified only when clearly labeled optional and
  non-required. Optional hardening is not a blocker, mandatory remediation,
  patch authority, or readiness condition.
- `patch_queue_entry` means executor-ready how-to. It is allowed only in a
  patch-queue review or separately authorized patch/integration execution lane.
  Ordinary read-only artifact, adversarial artifact, prompt, and implementation
  reviews must not emit `patch_queue_entry`; they may provide advisory
  remediation direction only.
- Chief Architect consumption of review reports follows this order:
  commission -> target -> authority -> decision criteria -> evidence ->
  reviewer verdict or recommendation. Reviewer verdicts and recommendations
  are decision input, not the first anchor.
- No synthesis lane is added by this doctrine. Multi-review reconciliation
  remains Chief Architect adjudication unless a later Orca overlay decision
  explicitly binds another owner.
- Review lane routing must never recommend, prescribe, rank, or imply runtime
  model choice. Review lanes may bind review type, method/skill, target,
  authority, output mode, destination, and prompt-template target. Runtime
  model choice is outside Orca review-lane authority and remains an
  operator/tooling decision.

## Template Retrieval Binding

Orca no longer binds executor or reviewer lanes to runtime model identifiers.
Prompt authors may retrieve templates by registry ID from
`.agents/workflow-overlay/template-registry.md`, but a template target is prompt
posture only. It does not select, rank, recommend, or require the runtime model.

```yaml
template_retrieval_binding:
  status: active
  registry: .agents/workflow-overlay/template-registry.md
  template_ids_authority: registry_registered_templates
  template_ids:
    shared-behavior-contract: model-neutral template include
    generic-gpt55: GPT-5.5 prompt posture
    generic-claude-sonnet46: Claude Sonnet 4.6 prompt posture
    generic-claude-opus47: Claude Opus 4.7 prompt posture
    generic-claude-opus: Claude Opus legacy prompt posture
    research-evidence-lane-o3: o3 / o3-deep-research prompt posture
    research-synthesis-gpt55: GPT-5.5 prompt posture
    adversarial-artifact-review: model-neutral review template
    thin-wrapper: model-neutral wrapper template
  authority_order:
    - current_turn_explicit_user_instruction
    - template_registry_entry
    - accepted_orca_handoff_or_prior_thread_state
    - reusable_workflow_kernel_advisory_template_guidance
  conflict_rule: use the highest listed source that explicitly selects a prompt template target, without expanding source-changing authority or runtime model choice.
```

Template retrieval may support language such as "use the Opus 4.7-style
adversarial review template" or "adapt this for the Sonnet 4.6 prompt posture."
It must not produce language such as "run this on Opus", "recommended model",
or "reviewer model". It does not create implementation permission,
prompt-routing authority, validation success, executor-ready instructions, or
a paste-ready handoff. Executor-ready prompts and routed handoffs remain
prompt-orchestration work.

## Rules

- Reviewer threads are source-read-only unless explicitly assigned patch execution.
- Review prompts must explicitly trigger `workflow-deep-thinking` before the
  relevant review skill so the reviewer frames failure modes before listing
  findings. This does not expand review scope or authorize patching.
- Adversarial artifact review prompts must explicitly invoke
  `workflow-adversarial-artifact-review` after source readiness. If the skill is
  unavailable or not invoked, the prompt must block strict review claims or
  return advisory-only critique with the missing skill invocation named.
- Review prompts and review reports should close with a review-use boundary,
  not an expanded product-proof non-claims catalog unless the review target
  itself requires product-proof claim checking. The boundary is: review
  findings are decision input only; they are not approval, validation,
  mandatory remediation, or executor-ready patch authority until separately
  accepted or authorized.
- Adversarial artifact review prompts should request the compact
  `review_summary` YAML shape from
  `.agents/workflow-overlay/communication-style.md` before detailed findings,
  and should return a courier-ready fenced YAML block plus a short findings
  summary in chat.
- Reviews of new or materially touched durable human-authored workflow
  artifacts should check `.agents/workflow-overlay/retrieval-metadata.md`
  when retrieval metadata is in scope. Retrieval metadata defects are routing
  and authority-hygiene issues; they do not create approval, validation proof,
  readiness, lifecycle completion, or edit permission.
- Executor threads must not report success without file and validation evidence.
- Installed global `review`, implementation/code review, and artifact review remain separate lanes until Orca accepts more specific routing.
- Runtime model recommendations for review lanes: forbidden. Template target
  retrieval is allowed only as prompt-shaping guidance.
- Prompt output contracts are bound in `.agents/workflow-overlay/prompt-orchestration.md`.
