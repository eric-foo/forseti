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

- Artifact review: read-only review of docs, decisions, prompts, and migration artifacts. Reviewers may write reports only under `docs/review-outputs/` unless a prompt authorizes a different Forseti-owned report path.
- Adversarial artifact review: read-only adversarial review of docs, decisions,
  prompts, product-proof artifacts, and migration artifacts. Reports should go
  under `docs/review-outputs/adversarial-artifact-reviews/` unless a prompt
  names another Forseti-owned report path. Formal adversarial artifact review must
  invoke `workflow-adversarial-artifact-review` after source context is ready.
  If that skill is unavailable, unresolved, or not applied, the run may return
  only a blocked or advisory-only result and must not emit strict review
  claims.
- Prompt review: read-only review of prompt artifacts, thin wrappers, source maps, output modes, and validation gates. Reports go under `docs/review-outputs/` unless the prompt names another Forseti-owned report path.
- Patch-queue review: read-only review that produces ordered patch units. Applying those patches requires a separate patch or integration execution assignment.
- Patch or integration execution: applies accepted documentation patches inside Orca and reports changed files plus validation.
- Skill adoption review: deferred until a later turn authorizes adoption or shadow validation.
- Delegated review-and-patch (provisional, opt-in): a distinct Chief Architect-commissioned bounded-executor convention for hardening high-stakes authored artifacts, defined in `.agents/workflow-overlay/delegated-review-patch.md`. It is NOT one of the source-read-only review lanes and NOT machine-routable; in its default `repo` access mode the delegate patches the named target, while in its `no_repo` access mode the delegate is read-only/advisory (returns findings; the CA applies the patch, with a required de-correlated post-patch re-review) — the convention still owns it either way. The reviewer-read-only rule and the review-lane model-neutrality below are unchanged.

## Review Doctrine

Orca review mechanics are Forseti-owned here: findings-first review output,
advisory critique from visible evidence, and strict authority boundaries for
formal review claims. Forseti-local overlay files own concrete lane names,
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
- Review outputs record two provenance fields, operator/tooling-supplied and
  set by the operator/CA on the durable review record (including when ingesting
  a no-repo or portable reviewer's returned findings -- the reviewer is not
  required to self-emit them): `reviewed_by` (the model and version that
  performed the review) and `authored_by` (the model and version that authored
  the artifact under review), for example `claude-opus-4.8`, `gpt-5.5`. Each is
  a required (present) field on new or materially touched review outputs (not
  backfilled); its value is `unrecorded` when the identity was not supplied, and
  it is never fabricated. These are factual provenance records -- the
  ordinary-review analogue of the delegated-review-patch actor/model-family
  receipt -- and must never be used to select, recommend, rank, or imply a
  runtime model; the model-neutrality rule above is unchanged.
- The purpose of `reviewed_by` / `authored_by` is to make reviewer attribution
  and same-family-vs-cross-family coverage measurable. Same-vs-cross is computed
  by relating the two families, so it is measured only when both fields carry
  real values: a present `unrecorded` value satisfies the schema but records a
  visible measurement gap, not a captured measurement, and is never treated as
  success. The measurement is realized only when tooling actually populates the
  real values.
- **Two-bar de-correlation (review tier; family = vendor).** A **cross-vendor**
  delegate (different vendor / model lineage, e.g., Claude <-> GPT; vendor =
  upstream developer/provider, not host / reseller / wrapper) is the **discovery**
  bar, required to claim the no-new-seam standard for a full or doctrine-surface
  pass. A **same-vendor** delegate (typically a lower/mechanical tier, e.g.,
  Opus -> Sonnet) is the **bounded sanity / verification** tier: it **may only
  claim bounded verification/sanity, never discovery / no-new-seam** -- appropriate
  for a bounded authored change or a post-patch recheck, run **advisory** (findings
  adjudicated by the CA). Tier is not family; the de-correlation definition is
  owned by `.agents/workflow-overlay/delegated-review-patch.md`. **When the
  same-vendor bar is chosen, the review record must record `de_correlation_bar`**
  (`cross_vendor_discovery` | `same_vendor_sanity` | `self_fallback`) **plus, for
  `same_vendor_sanity`, a `same_vendor_rationale`** (why the cross-vendor bar was
  not needed: e.g., bounded change; no doctrine/seam surface; no no-new-seam
  claim) -- recorded alongside `reviewed_by` / `authored_by` so a missing
  justification is mechanically detectable.

## Template Retrieval Binding

Orca does not bind executor or reviewer lanes to runtime model identifiers.
Prompt authors may retrieve templates by registry ID from
`.agents/workflow-overlay/template-registry.md`, but a template target is prompt
posture only. It does not select, rank, recommend, or require the runtime model.
Model-target templates (`_generic/`) were retired 2026-06-13 (unused; owner decision);
only model-neutral templates remain registered.

```yaml
template_retrieval_binding:
  status: active
  registry: .agents/workflow-overlay/template-registry.md
  template_ids_authority: registry_registered_templates
  template_ids:
    shared-behavior-contract: model-neutral template include
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

Template retrieval does not produce language such as "run this on [model]",
"recommended model", or "reviewer model". It does not create implementation
permission, prompt-routing authority, validation success, executor-ready
instructions, or a paste-ready handoff. Executor-ready prompts and routed
handoffs remain prompt-orchestration work.

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

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Review outputs now record two required (present), model-neutral provenance fields -- reviewed_by and
    authored_by (the reviewing model+version and the reviewed-artifact author model+version) -- set by the
    operator/CA on the durable record, value unrecorded allowed (a visible measurement gap, never fabricated,
    never a success path), forward-only. Same-family-vs-cross-family is computed by relating the two.
    Observed records, not model routing/recommendation; review-lane model-neutrality is unchanged.
  trigger: review_authority
  related_triggers: [output_authority]
  controlling_sources_updated:
    - .agents/workflow-overlay/review-lanes.md
    - .agents/workflow-overlay/prompt-orchestration.md
    - .agents/workflow-overlay/communication-style.md
  downstream_surfaces_checked:
    - {path: docs/prompts/templates/portable/adversarial_artifact_review_portable_method_v0.md, note: pin-only re-pin of the review-lanes derived_from hash; distilled method body unchanged}
    - {path: .agents/workflow-overlay/validation-gates.md, note: F4 single-source decision; no duplicate enforcement gate added}
  intentionally_not_updated:
    - {path: .agents/workflow-overlay/validation-gates.md, reason: F4 single-source; the Review Doctrine here is read by every Orca agent, so no duplicate gate was added}
    - {path: .agents/workflow-overlay/retrieval-metadata.md, reason: review-output fields, not universal durable-artifact header fields}
    - {path: .agents/workflow-overlay/delegated-review-patch.md, reason: its actor/model-family receipt already records author and controller families; these are the consistent ordinary-review analogue}
    - {path: docs/decisions/adversarial_review_routing_policy_v0.md, reason: routing tiers declined (Pile 3); this records measurement, not routing}
  stale_language_search: >
    reviewed_by / authored_by are net-new field names; no prior overlay text stated review outputs do not
    record reviewer/author identity, so no language was made stale, and the model-neutrality rule is
    unchanged and explicitly reconciled in the new bullets.
  non_claims:
    - not validation
    - not readiness
    - not model routing/recommendation
    - not a kept change until committed and the same-family post-patch blast-radius re-review resolves
```

## Direction Change Propagation — De-correlation Family = Vendor (Two-Bar)

```yaml
direction_change_propagation:
  doctrine_changed: >
    De-correlation "family" is now defined as VENDOR / model lineage (Claude vs GPT), NOT tier.
    Cross-VENDOR is the discovery bar (required to claim the no-new-seam standard for full or
    doctrine-surface passes); a SAME-VENDOR lower/mechanical-tier delegate (e.g., Opus -> Sonnet)
    is the bounded sanity/verification tier, run advisory. The same-vendor tier is generalized
    beyond the no_repo post-patch recheck to any bounded authored change. When the same-vendor
    bar is chosen, the review record must state why cross-vendor was not needed. Owner-decided 2026-06-10.
  trigger: review_authority
  controlling_sources_updated:
    - .agents/workflow-overlay/delegated-review-patch.md  # de_correlation_criterion + de-correlation paragraph + no_repo wording -> vendor
    - .agents/workflow-overlay/review-lanes.md            # two-bar rule + same-vendor justification requirement
  downstream_surfaces_checked:
    - {path: .agents/workflow-overlay/prompt-orchestration.md, note: model-neutrality unchanged; no edit}
  non_claims:
    - CROSS-VENDOR review resolved (GPT-5.5 Thinking / OpenAI: 1 major + 2 minor refinements accepted + applied -- vendor-key definition, same-vendor claim-ceiling, named de_correlation_bar field); not a kept change until the same-vendor bounded post-patch recheck resolves AND it is committed
    - resolves the prior internal contradiction (de_correlation_criterion "Opus->non-Opus" vs no_repo "same-family lower-tier"); family is now unambiguously vendor
    - not model routing/recommendation; a who-constraint only
```
