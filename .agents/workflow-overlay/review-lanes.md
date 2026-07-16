# Review Lanes

```yaml
retrieval_header_version: 1
artifact_role: Forseti overlay authority
scope: Forseti review lanes, reviewer permissions, and executor boundaries.
use_when:
  - Selecting or checking a Forseti review lane.
  - Confirming whether a reviewer may write reports or apply patches.
  - Resolving review prompt template retrieval without turning templates into model routing.
authority_boundary: retrieval_only
```

**Routine read shape** (owned by `.agents/workflow-overlay/source-loading.md`,
Targeted Read Protocol): routine review work reads "Current Lanes" plus the
one section the task touches ("Review Doctrine" for formal lane bindings,
"Template Retrieval Binding" when retrieving a template, "Rules" for reviewer
conduct); a full-file read is for editing lane doctrine or adjudicating a
lane-authority conflict.

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
- Patch or integration execution: applies accepted documentation patches inside Forseti and reports changed files plus validation.
- Skill adoption review: deferred until a later turn authorizes adoption or shadow validation.
- Delegated review-and-patch (provisional, opt-in): a distinct Chief Architect-commissioned bounded-executor convention for hardening high-stakes authored artifacts — and, in its `delegated_code_review_and_patch` mode, bounded multi-file implementation/code diffs reviewed via the code review lane (`workflow-code-review`) — defined in `.agents/workflow-overlay/delegated-review-patch.md`. It is NOT one of the source-read-only review lanes and NOT machine-routable; in its default `repo` access mode the delegate patches the named target, while in its `no_repo` access mode the delegate is read-only/advisory (returns findings; the CA applies the patch, with a required de-correlated post-patch re-review) — the convention still owns it either way. The reviewer-read-only rule and the review-lane model-neutrality below are unchanged.

## Review Doctrine

Forseti review mechanics are Forseti-owned here: findings-first review output,
advisory critique from visible evidence, and strict authority boundaries for
formal review claims. Forseti-local overlay files own concrete lane names,
destinations, result vocabulary, severity labels, validation gates, patch
routing, and Chief Architect consumption rules.

- Review target and review purpose are commission-bound. A reviewer must not
  silently retarget a review, widen the target, or treat an adjacent artifact as
  the actual review object unless the prompt or current user instruction binds
  that change.
- Within the commission-bound target and purpose, adversarial reviewers should
  be maximally adversarial and coverage-first: report every failure mode found,
  including uncertain and low-severity ones. Materiality, severity, and
  confidence are labels the reviewer attaches to a finding, never a threshold
  for reporting it; filtering for importance belongs to the downstream
  adjudication, not the find stage. This does not widen the target; it means
  the reviewer must not soften, skip, or silently drop a failure mode because
  remediation would be awkward, confidence is low, or the finding seems minor.
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
  outputs and require Forseti overlay or prompt binding.
- Forseti adversarial artifact reviews may use `critical`, `major`, and `minor`
  severity labels for finding priority when the prompt or template names those
  labels. Those labels do not by themselves create approval, rejection,
  readiness, validation, or mandatory remediation authority.
- Findings carry a `confidence` label (`high` / `medium` / `low`) alongside
  severity: the reviewer's own certainty that the finding is real. Like
  severity, it is a priority label only and creates no approval, rejection,
  readiness, or remediation authority. Low confidence is never a reason to
  omit a finding; low-confidence or minor findings may use a compact one-line
  form instead of the full finding shape.
- A candidate finding the reviewer defeats with a steelman defense is not
  silently discarded: it is listed one line each in a `considered_and_defended`
  section (candidate plus the defense that held). These entries are not
  findings and carry no severity, closure, or action fields; they exist so the
  adjudicator can see the discard pile instead of inheriting the reviewer's
  self-filter.
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
  remains Chief Architect adjudication unless a later Forseti overlay decision
  explicitly binds another owner.
- Review lane routing must never recommend, prescribe, rank, or imply runtime
  model choice. Review lanes may bind review type, method/skill, target,
  authority, output mode, destination, and prompt-template target. Runtime
  model choice is outside Forseti review-lane authority and remains an
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
  This general same-vendor sanity tier does not satisfy an explicitly
  commissioned delegated review-and-patch lane. That narrower convention
  requires a different-vendor controller with direct repo access and forbids
  same-vendor substitution; same-vendor sanity remains available only for
  ordinary bounded review outside that commissioned lane.

## Template Retrieval Binding

Forseti does not bind executor or reviewer lanes to runtime model identifiers.
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
    - accepted_forseti_handoff_or_prior_thread_state
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
- The deep-thinking trigger rule for review prompts is owned solely by
  `.agents/workflow-overlay/prompt-orchestration.md` (Review Prompt Defaults);
  do not restate or fork it here. Where that rule fires for a review
  commission, the review lane's internalized failure-mode framing satisfies it
  without a separate `workflow-deep-thinking` load.
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
- While the temporary Batch 0 pilot is active, the Chief Architect closing a
  material adversarial review must write the process-economics receipt required
  by `.agents/workflow-overlay/batch0-process-pilot.md` after adjudication. The
  receipt is measurement only and changes no review verdict or authority.
- Executor threads must not report success without file and validation evidence.
- Installed global `review`, implementation/code review, and artifact review remain separate lanes until Forseti accepts more specific routing.
- Runtime model recommendations for review lanes: forbidden. Template target
  retrieval is allowed only as prompt-shaping guidance.
- Prompt output contracts are bound in `.agents/workflow-overlay/prompt-orchestration.md`.

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

## Direction Change Propagation — Coverage-First Find Stage

```yaml
# coverage-first find stage bound 2026-07-04 (owner decision).
direction_change_propagation:
  doctrine_changed: >
    Adversarial review find stage is now coverage-first: reviewers report every
    failure mode found, including uncertain and low-severity ones; materiality,
    severity, and the new confidence label (high/medium/low) are priority
    labels only, never reporting thresholds; importance filtering moves to the
    adjudication pass; steelman-defeated candidates surface one-line in a
    considered_and_defended section instead of being silently dropped;
    low-confidence or minor findings may use a compact one-line form.
    Findings-first authority, severity vocabulary, model-neutrality, and CA
    adjudication ownership are unchanged. Motivation: current models follow
    find-time importance/confidence bars literally, silently depressing recall;
    the existing mandatory CA adjudication is the correct filter stage.
  trigger: review_authority
  related_triggers: [output_authority]
  controlling_sources_updated:
    - .agents/workflow-overlay/review-lanes.md
    - .agents/workflow-overlay/prompt-orchestration.md
  downstream_surfaces_checked:
    - {path: docs/prompts/templates/review/adversarial_artifact_review_v0.md, note: coverage-first block, confidence field, compact one-line form, considered_and_defended section added}
    - {path: docs/prompts/templates/portable/adversarial_artifact_review_portable_method_v0.md, note: re-derived in the same pass; both derived_from hashes re-pinned}
    - {path: docs/decisions/adversarial_review_routing_policy_v0.md, note: prompt-filter recall confound added to section 7 as a named limitation and cross-family-arm charge}
    - {path: .agents/workflow-overlay/communication-style.md, note: review_summary shape unchanged; blocking/advisory split already carries priority}
    - {path: .agents/workflow-overlay/delegated-review-patch.md, note: defers the review method to the kernel lanes and this doctrine; inherits coverage-first; no edit}
  intentionally_not_updated:
    - {path: workflow-adversarial-artifact-review kernel skill, reason: plugin-owned under the Protected Skill Boundary; its downgrade-or-drop rule is reconciled template-side (considered_and_defended entries are not findings); a true skill fix is a separate skill-governance action}
    - {path: workflow-code-review kernel skill, reason: its demote-to-risk / not-proven channel is already coverage-preserving}
    - {path: .agents/workflow-overlay/validation-gates.md, reason: F4 single-source; the Review Doctrine here is the read path}
    - {path: docs/prompts/reviews/ and docs/review-inputs/ and docs/hygiene/registration_integrity_review_README.md and docs/review-outputs/, reason: already-dispatched commission prompts, shipped no-repo bundles, and historical review reports quoting the prior doctrine are lane records, not rewritten; future bundles re-derive via the portable-method freshness gate}
  stale_language_search: >
    rg -ni "material,? decision-relevant" .agents docs AGENTS.md
  stale_language_search_result: >
    Executed 2026-07-04 after edits. Remaining hits are the intentional
    historical quotation inside the new routing-policy section-7 confound
    bullet, already-dispatched commission prompts under docs/prompts/reviews/,
    shipped no-repo bundle READMEs (docs/review-inputs/*,
    docs/hygiene/registration_integrity_review_README.md), and historical
    review reports under docs/review-outputs/ -- all kept as historical lane
    records. The portable method's stance line was rewritten in this same
    pass. No live overlay, template, or preflight-checklist surface still
    states the materiality reporting threshold.
  non_claims:
    - not validation, not readiness
    - not runtime model routing or recommendation
    - no recall-improvement efficacy claim until measured
```

## Direction Change Propagation — Deep-Thinking Trigger Single Owner + Review-Internalized Framing

```yaml
direction_change_propagation:
  doctrine_changed: >
    The deep-thinking trigger rule for review prompts has exactly one owner:
    prompt-orchestration.md (Review Prompt Defaults). The stale review-lanes
    copy -- which still triggered workflow-deep-thinking for adversarial,
    formal-verdict, delegated, patch-authorized, and high-stakes reviews and
    so forked the PR #883 (2026-07-12) narrowing -- is replaced by a pointer.
    Where the owning rule fires for a review commission, the review lane's own
    internalized failure-mode-framing discipline (the adversarial review skill
    carries it; the review templates define the framing pass) satisfies the
    requirement without a second workflow-deep-thinking skill load; a separate
    workflow-deep-thinking load remains the route for owner-invoked decision
    work. The PR #883 narrowing itself is unchanged.
  trigger: review_authority
  related_triggers: [workflow_authority]
  controlling_sources_updated:
    - .agents/workflow-overlay/prompt-orchestration.md  # Review Prompt Defaults remains the single owner; framing-pass wording folded into the review lane
    - .agents/workflow-overlay/review-lanes.md          # stale broad-trigger copy replaced with a pointer to the owner
  downstream_surfaces_checked:
    - {path: .agents/workflow-overlay/decision-routing.md, note: one routing clarification added in the same pass -- an explicit /fused invocation supersedes the AGENTS.md five-phase fast path for that work unit, while a continuation that only executes already-cleared fused lanes runs under the fast path; no trigger or router structure changed}
    - {path: .agents/workflow-overlay/delegated-review-patch.md, note: already consistent with the narrowing ("a bounded multi-file target alone does not add workflow-deep-thinking"); no edit}
    - {path: AGENTS.md, note: routes review depth to the overlay; no deep-thinking trigger copy; no edit}
  intentionally_not_updated:
    - {path: docs/prompts/templates/review/adversarial_artifact_review_v0.md, reason: "Line 72 still instructs 'Use workflow-deep-thinking first.' A template rewrite is outside this commissioned file scope and re-derives the portable-method hash; flagged as the known remaining sequencing surface for a separate template pass."}
    - {path: docs/decisions/adversarial_review_routing_policy_v0.md, reason: "Section describing the registry template's trigger-then-review structure is a dated decision record quoting the template; it follows the template surface above."}
    - {path: docs/review-outputs/ and docs/prompts/reviews/, reason: "Historical review reports and already-dispatched commission prompts are lane records, not rewritten."}
  stale_language_search: >
    rg -ni "workflow-deep-thinking.{0,100}before the relevant review|trigger `?workflow-deep-thinking|Use `workflow-deep-thinking` first"
    .agents AGENTS.md CLAUDE.md docs/prompts/templates docs/decisions
  stale_language_search_result: >
    Executed 2026-07-16 after edits. No overlay, AGENTS.md, or CLAUDE.md hit
    remains. Two hits remain outside the commissioned scope and are named in
    intentionally_not_updated: the review template's "Use workflow-deep-thinking
    first" line and the routing-policy decision record describing that template
    structure. Historical review outputs were not searched as lane records.
  non_claims:
    - not validation or readiness
    - does not change any batch0/batch1 pilot trigger or threshold
    - does not weaken the PR #883 narrowing (its "alone does not trigger" sentence is preserved verbatim)
    - not a template rewrite; the template sequencing surface remains open and named
```
