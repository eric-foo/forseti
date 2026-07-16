# Delegated Review-and-Patch For High-Stakes Authored Artifacts (Provisional)

```yaml
retrieval_header_version: 1
artifact_role: Forseti overlay authority
scope: >
  Provisional delegated review-and-patch convention for high-stakes authored
  Forseti artifacts, plus the overlay-interface fields a future skill implementation may read.
use_when:
  - A Chief Architect is deciding whether to commission a delegated
    review-and-patch hardening pass on a high-stakes authored artifact.
  - Checking the overlay-interface fields (status, operating-contract pointer,
    protected paths, model ladder, preflight, source context, output
    destinations) this convention exposes.
authority_boundary: retrieval_only
```

**Routine read shape** (owned by `.agents/workflow-overlay/source-loading.md`,
Targeted Read Protocol): commissioning reads "When it applies", "The loop",
"Access selection rule", "De-correlation", and the "Overlay Interface" block;
code-diff commissioning also reads "Code-diff target kind — the
`delegated_code_review_and_patch` sibling target kind"; return adjudication reads
"Adjudication closeout"; a full-file read is for editing this convention or
resolving a novel dispute about it.

**Status — provisional convention.** This is an experimental operating
convention replicated into Forseti from jb's provisional convention (jb branch
`lane/delegated-review-patch-convention`, commit `345397b`), adopted on limited
cross-project evidence (see *Evidence* below). It is not bound Forseti review
doctrine and not a machine-routable review lane: it carries no strict, formal,
or operational lane authority, and `.agents/workflow-overlay/review-lanes.md`
"Current Lanes" intentionally does not bind it yet. Treat it as guidance the
Chief Architect may choose to commission, refined as it is used; promote it to a
bound lane only after more uses and a separate Forseti overlay binding decision.

**What it is — and what it is not.** This is a distinct commissioned,
bounded-executor lane with an integrated hardening review — not one of the
source-read-only review lanes in `.agents/workflow-overlay/review-lanes.md`.
Those lanes and the `AGENTS.md` reviewer-thread rule are unchanged: a reviewer
still does not edit sources, and "Reviewer threads are source-read-only unless
explicitly assigned patch execution" still holds. The actor here is an executor
the Chief Architect has commissioned with a bounded patch scope; its review is
the internal analysis it uses to decide its own patches. Patch authority comes
from the executor rule "edit only inside accepted scope" — the commission is the
accepted scope.

**When it applies — by commission, not by category.** This lane is available
only under an explicit Chief Architect commission that (1) names the single
target artifact file, (2) states why ordinary source-read-only review is
insufficient, and (3) declares the bounded patch scope. Absent such a commission
it does not apply. It is intended for high-stakes *authored* artifacts —
doctrine, operating contracts, and eval/scoring/validation instruments — where
the author encodes guardrails and can reintroduce the exact failure mode those
guardrails exist to prevent; but the category alone never triggers it. Trivial
edits, routine prose, mechanical patches, and ordinary review continue to use
the cheap inline path — the author edits directly, or the standard
source-read-only review lane applies. This is never a mandatory front door.

**Direct invocation is courier-prompt authoring only.** An explicit user request
such as `delegate patch`, `write the delegate patch prompt`, or an invocation of
the delegated-review-patch skill requests one paste-ready commission for the
operator to courier. It does **not** authorize the authoring agent to discover a
controller, create or dispatch a task, fork a thread, spawn a subagent, send the
prompt, or execute the review. The rendered prompt binds an unknown future
receiver as `receiver_to_bind` until the operator-selected controller proves
different-vendor lineage and direct repository access. If no eligible controller
is available, the prompt remains unexecuted; never substitute a same-vendor
model, self-review, no-repo reviewer, or Codex managed task. A separate explicit
execution request may start only a receiver that already satisfies the same
different-vendor plus direct-repo eligibility; it does not relax this authoring
default or create fallback authority.

**The loop.** The Chief Architect authors or specifies the artifact, then
commissions a single combined review-and-patch pass from a de-correlated model
(see *De-correlation* below), bounded to the named target file. The delegate:
(1) reviews the artifact for material failure modes; (2) patches the target file
directly within the commissioned scope; (3) treats all canonical,
compiler-emitted, test, hash-pinned, and other protected or generated paths as
read-only — it flags issues there, it does not patch them; (4) returns a unified
diff, source citations for each change, a verdict, and a residual-risk note. The
Chief Architect then adjudicates the returned diff before any of it is accepted
or kept — the diff and verdict are claims to adjudicate, not premises to
inherit. The delegate's citations and changes are decision input only; the Chief
Architect reserves final authority over what is kept and may veto any change it
judges to add no benefit or net-negative value, even when individually
defensible.

**Delegate lifecycle hard stop.** The delegate may make only the commissioned
working-tree edits inside the named patch scope. It does not commit, push, open
or update a PR, merge, stash, reset, clean up a worktree, run repository hygiene,
or otherwise advance lifecycle state. Those actions remain with the Chief
Architect after adjudication. A prompt that omits this stop is incomplete.

**Adjudication closeout.** The delegated return is not complete merely because
it names a verdict, diff, findings, or residual risk. The return/courier prompt
must instruct the commissioning Chief Architect to close the adjudication with
`.agents/workflow-overlay/communication-style.md` -> **Review Adjudication Next
Step**: first adjudicate the findings, diff, verdict, and residuals as claims;
close any self-closable material issue -- one whose closure sits inside the
adjudicator's own authority and the commissioned scope, such as applying the
adjudicator's own modify/reject adjudications to the target -- in the same
turn; route a smallest-complete closure step only for an issue that genuinely
needs another review round, another lane, an architecture pass, or an owner
decision; once clean, batch admin/lifecycle follow-ups into exactly one land
step with no deep-thinking; then, when a visible active goal,
`thread_operating_target`, or accepted next objective exists, deep-think the 1-5
material next moves that best advance it. When none exists, record
`no_visible_active_goal` rather than inventing a roadmap. The land/closure step
plus this goal-conditioned material-move check are a required same-turn tail;
do not defer the check to another turn. This is an adjudicator obligation, not
permission for the delegate to decide what is kept or widen review scope.

**Delegated review-output finalization gate.** Any delegated review output
written under `docs/review-outputs/` blocks final chat closeout until, after the
final report write, `python .agents/hooks/check_review_output_provenance.py --strict <report-path>`
exits 0. If the report is changed after that command, rerun it and report only
the final observed result. Embedded live diffs must be inside a proper
standalone `diff` fence and must be generated/read back as real multiline text,
not hand-collapsed into prose. Future-tense placeholders such as "must be
checked after this report is written" are not allowed in the durable report.
This gate is mechanical shape/integrity only: it is not approval, validation,
readiness, review quality, or acceptance of the delegated findings.

**Access selection rule.** Delegated review-and-patch is `repo` only. The
delegate must have direct repository/worktree access and patch the named target
inside that repository. `no_repo` is not a weaker execution mode for this lane;
it is ineligible. When repository access is unavailable, author a different,
read-only review prompt under the ordinary review contract or leave the delegated
patch prompt unexecuted. Do not relabel advisory findings plus home-lane patching
as delegated patch authorship.

**Couriered multi-round review loops.** The authoring agent may mechanically
verify that an accepted diff applied cleanly and that named validation passed,
but it must not commission a same-vendor model as a delegated-patch closure
reviewer. If independent closure review is required, author another courier
prompt for an eligible different-vendor controller with direct repo access. If
that controller is unavailable, report the review as not run; do not manufacture
a lower-tier or same-family substitute.

**Citations.** The delegate's citations are neutral in tone — factual source
evidence, no advocacy or editorializing — but decision-sufficient in substance,
so the Chief Architect's veto stays informed rather than blind. The delegate's
argument belongs in the verdict and residual, not the citations. Neutral tone is
not thinness: thin citations would push the Chief Architect back onto its own
priors and defeat the de-correlation.

**De-correlation — observable criterion and no fallback.** "Family" here means
**vendor / model lineage** (e.g., Claude vs GPT), **not tier**. **Vendor** = the upstream model
developer/provider (e.g., Anthropic, OpenAI) — **not** the hosting platform, API
reseller, deployment surface, or wrapper/fine-tune owner; **unknown or undisclosed
lineage cannot satisfy the delegated-review-and-patch bar**. The commission
must record the author vendor and the delegate vendor; the **cross-vendor
discovery** bar is satisfied only when they **differ**. A same-vendor delegate —
**even a different or lower tier** (e.g., an Opus author with a Sonnet delegate)
— is **ineligible** for this commissioned lane, including under a `sanity`,
`verification`, `fallback`, or lower-tier label. A self pass is likewise
ineligible. The general two-bar vocabulary in
`.agents/workflow-overlay/review-lanes.md` remains available for ordinary
review outside this lane; it cannot be used to convert a delegated patch
commission into same-vendor review. If a cross-vendor repo delegate cannot be
established, leave the courier prompt unexecuted or route a separately named
read-only review. Never claim or perform a delegated patch fallback.

This is a who-constraint recorded in the commission, not a model-quality
recommendation and not runtime model routing. It does not belong in review
prompts as model-selection advice, and it does not alter Forseti review-lane
model-neutrality: `.agents/workflow-overlay/review-lanes.md` and
`.agents/workflow-overlay/prompt-orchestration.md` still forbid review lanes,
review prompts, wrappers, handoffs, and closeouts from recommending,
prescribing, ranking, or implying runtime model choice. Model choice remains an
operator, tooling, and commission decision; this convention names model
*families* only to express the difference constraint, never to select or rank a
runtime model.

**Escalation.** When the artifact's problem is design-level rather than
patch-level, the delegate returns `NEEDS_ARCHITECTURE_PASS`, stops patching, and
returns findings only; any partial diff is quarantined and is not kept.
Escalation routes the artifact back to an architecture pass; it never forces a
patch onto a broken design, and a partial patch must never survive by inertia.

**Why.** De-correlation catches the author's own blind spots that self-review
structurally misses. Combining review and patch into one commissioned pass, with
the Chief Architect adjudicating the resulting diff, collapses the
Chief-Architect-thread context bursts that a review -> adjudicate -> instruct ->
patch -> re-read round-trip would otherwise spend; the saving scales with context
size times the round-trips collapsed. A cheap de-correlated pass before the Chief
Architect commits prevents an expensive wasted run on a correlated error.

**Strict-claim boundary.** A delegated diff plus verdict is decision input only.
Formal `PASS`, severity authority, readiness, and validation status still follow
the Review Doctrine in `.agents/workflow-overlay/review-lanes.md` and the prompt
validation gates in `.agents/workflow-overlay/prompt-orchestration.md`; this
convention creates none of them.

**Incomplete commission route-out.** When the user invokes this convention but
the commission is missing operator-owned fields (for example delegate vendor,
controller identity, access mode, report destination, or provenance values),
do not end on an inert blocker if the target and review purpose are inferable.
Route under `.agents/workflow-overlay/prompt-orchestration.md`: an eligible
current-lane, operator-couriered prompt uses **Lane-Scoped Delegated Patch Prompt
Default** and is carried in the lane PR/comment or ignored scratch; a prompt
matching the **Full orchestration** predicate in
`.agents/workflow-overlay/prompt-orchestration.md` uses the full
`workflow-prompt-orchestrator` contract. Missing
operator-owned values are clearly marked `operator_to_fill`; delegation or patch
authorization alone does not trigger the full route. Block only when the target,
review purpose, patch authority, or safe target state cannot be inferred, or
when the applicable prompt contract cannot be applied. If the inferred target
is a multi-file implementation/code diff rather than a single authored artifact,
do not force it into the authored-artifact target kind: route it to the
**`delegated_code_review_and_patch`** sibling target kind below, which keeps the code
review lane as its review method and bounds the patch to an explicitly named
file set. When no patch authority is commissioned, route via prompt-orchestrator
to read-only implementation/code review instead; patch authority is never
assumed from the target category.

Route-out is authoring only: it returns the paste-ready prompt to the operator
and does not inspect local controller availability or dispatch any receiver.
The prompt records `delivery: operator_courier_only`, `access: repo`,
`delegate_eligibility: different_vendor_lineage_with_direct_repo_access`, the
observed author vendor, and either a different observed delegate vendor or
`delegate_vendor: operator_to_fill`. `operator_to_fill` is preparation state,
not evidence that the eligibility condition passed.

**Code-diff target kind — `delegated_code_review_and_patch`.**
The default loop above targets a single *authored* artifact and uses the
delegate's own adversarial analysis as the review. A bounded multi-file
implementation/code diff is handled by this **sibling target kind**: the same
commissioned convention with exactly two binding deltas. Everything else —
explicit commission, the de-correlation who-constraint and two-bar rule, the
`repo` / `no_repo` access-mode obligations, CA adjudication of the returned diff
before any keep, the `NEEDS_ARCHITECTURE_PASS` escalation, the strict-claim
boundary, and the no-runtime-model-recommendation rule — is inherited unchanged.
The code-review method remains the method in both access modes; `no_repo` only
changes repository access and patch authorship.

1. **The review method is the code review lane, not artifact review.** The
   delegate's review portion is `workflow-code-review` run under the Review
   Prompt Defaults. Commissioning, adversarial wording, patch authorization, or
   a bounded multi-file target alone does not add `workflow-deep-thinking` or
   the Source-Gated Method Contract. Those apply only when their independent
   triggers in `.agents/workflow-overlay/prompt-orchestration.md` fire — for
   example owner invocation or Mini God Tier, doctrine/authority change,
   source-heavy or materially ambiguous work, or substantial seam risk whose
   framing could change the route. The code review lane stays the
   review method for code; this convention only adds commissioned bounded patch
   authorship plus CA adjudication on top of it, and never replaces, weakens, or
   relabels code review, nor merges it with artifact review (those remain
   separate lanes per `.agents/workflow-overlay/review-lanes.md`). The
   `fitness_reference` rule stays artifact-review-only; code's fitness bar —
   spec, tests, ground-truth substrate — governs here.
2. **The target is an explicitly named multi-file set, not one file.** The
   commission names the bounded set of code files in scope (one or more). That
   named set replaces the single-file bound as the only patchable surface;
   everything outside it — all other code, all canonical / generated / hash-pinned
   paths, and every path the safety rules forbid — stays read-only / flag-only.
   The named set is the whole patch scope and **cannot silently widen**: touching
   a file the commission did not name requires a re-commission, never a
   delegate-side expansion.

Two obligations are stated explicitly here because code carries them:

- **Validation/test obligations are named and can fail.** The commission names
  the tests and gates the touched code must satisfy (tests inside the touched set
  are part of the named target). The delegate runs them and reports real results;
  a failing test or gate is surfaced, never masked or routed around, and the
  returned diff asserts no `PASS`, readiness, or settled status — failure
  visibility holds exactly as under the executor rule.
- **Patch authority stays subordinate to implementation authorization.** A
  commissioned code patch is an explicit bounded source-changing authorization
  under `.agents/workflow-overlay/safety-rules.md` and `AGENTS.md`; this target kind
  supplies the *shape*, never a standing authorization, and never bypasses the
  implementation-authorization boundary. By commission, not by category — the
  code-diff category alone never triggers this target kind; an un-commissioned diff
  routes to read-only code review.

**Repo-mode discovery discharges a downstream independent-review gate.** When a
cross-vendor delegate runs the `repo`-mode loop — full-artifact adversarial
discovery (loop step 1, not only the patched lines) plus authorship of the
bounded fix — and the CA adjudicates and independently verifies closure (a
class-level sweep for the finding's leak class plus byte/scope checks), that pass
**satisfies** a `cross_vendor_discovery` independent-review requirement for the
*patched* artifact (for example, a pre-freeze leakage gate). A separate
standalone post-patch re-scan is **not** additionally required to clear that gate.
The one non-independent sliver — the delegate's own edited lines — must be
mechanically verifiable (e.g. a class sweep), and the CA records that limitation
on the durable disposition. *Proportionality, owner-set by assurance tier:* a
higher tier (e.g. buyer-proof) may still require a separate independent pass;
product-learning / N-case-batch tiers may rely on the delegated pass. *Residual,
named:* a **novel** leak class shared across vendors and absent from the swept
set is caught by neither the class sweep (which catches known systematic classes)
nor batch averaging (which cancels random misses) — bounded and acceptable below
buyer-proof, not zero. `no_repo` is outside this lane because it loses delegated
patch authorship; it must route to an ordinary read-only review rather than a
same-vendor or home-authored patch fallback.

## Overlay Interface (fields a future skill implementation may read)

This is the seam to handoff 2 (a skill implementation, authored separately - not in
this overlay binding). The fields below defer to existing Forseti overlay authority
and do not fork or restate it.

```yaml
delegated_review_patch_overlay_interface:
  status: provisional_opt_in   # available only by explicit CA commission; not a bound review lane; not mandatory
  operating_contract_pointer: .agents/workflow-overlay/delegated-review-patch.md
  project_prompt_routing_binding: >
    Forseti prompt-routing depth is owned by prompt-orchestration.md. A
    resolver-loaded generic skill's always-full-orchestrator default is replaced
    by Lane-Scoped Delegated Patch Prompt Default when that predicate is
    satisfied; all review, de-correlation, scope, validation, escalation,
    adjudication, and lifecycle safeguards remain binding.
  direct_invocation_contract: >
    "delegate patch" and equivalent direct invocations author exactly one
    paste-ready operator-courier prompt. They never discover, create, spawn,
    dispatch, or execute a receiver. The prompt is preparation-only until a
    different-vendor controller with direct repo access binds and verifies it;
    no same-vendor, unknown-lineage, no_repo, self, or Codex-managed fallback is
    valid.
  prompt_orchestrator_available:
    full_renderer: workflow-prompt-orchestrator
    compact_renderer: .agents/workflow-overlay/prompt-orchestration.md#lane-scoped-delegated-patch-prompt-default
    selection_rule: >
      Use compact_renderer when its project predicate is satisfied; otherwise
      use full_renderer. Either renderer satisfies the strict commission prompt
      availability field without changing the installed skill artifact.
  target_kinds:
    authored_artifact: >
      Default target kind; a single CA-named authored artifact (doctrine, operating
      contract, eval/scoring/validation instrument). Review method is the
      delegate's own adversarial analysis. Direct repository access and a
      single-file patch bound are required.
    delegated_code_review_and_patch: >
      Sibling target kind for a bounded multi-file implementation/code diff.
      Review method is the code review lane (workflow-code-review), NOT artifact
      review and never a merge of the two. Deep-thinking and source-gated
      sequencing apply only when independently triggered by prompt-orchestration.
      Target is
      an explicitly named file set (one or more) that CANNOT silently widen;
      everything outside it is read-only / flag-only. Validation/test obligations
      are named and can fail. Patch authority is an explicit commission
      subordinate to the implementation-authorization boundary in safety-rules.md
      / AGENTS.md, never assumed from the category. All other convention machinery
      (commission, de-correlation / two-bar, access-mode obligations, CA
      adjudication before keep, NEEDS_ARCHITECTURE_PASS, strict-claim boundary,
      no runtime-model recommendation) is inherited unchanged. Direct repository
      access is required; no_repo is outside this target kind.
  incomplete_commission_route_out:
    owner: .agents/workflow-overlay/prompt-orchestration.md
    output_mode: paste-ready-chat
    use_when: >
      Target and review purpose are inferable, but operator-owned route fields
      are missing; emit an operator-fill route-out prompt instead of an inert
      blocker.
    default_route: >
      Eligible current-lane operator-couriered prompts use Lane-Scoped Delegated
      Patch Prompt Default: one fresh target-state read and a compact pointer-first
      commission returned to the operator without dispatch. Full
      workflow-prompt-orchestrator applies only when an escalation condition or
      owner-invoked Mini God Tier is present and still returns a courier prompt;
      orchestration depth never grants dispatch authority.
    code_diff_target_routing: >
      A multi-file implementation/code diff is handled by the
      delegated_code_review_and_patch sibling target kind (target_kinds above) when patch
      authority is commissioned; an un-commissioned diff routes to read-only code
      review. Patch authority is never assumed from the target category.
  protected_path_list:
    authority: .agents/workflow-overlay/safety-rules.md   # defer to it; do not fork or restate the forbidden-edit set
    rule: >
      The delegate may patch ONLY the CA-named target — the single authored file
      in the authored-artifact target kind, or the explicitly named multi-file set in
      delegated_code_review_and_patch (which cannot silently widen). Everything
      else is read-only / flag-only: all other Forseti sources; canonical, frozen,
      or hash-pinned decisions, product contracts, manifests, and
      provenance/review-output ledgers; other `.agents/workflow-overlay/` files;
      `AGENTS.md` and `CLAUDE.md` when they are not the named target; and every
      path the safety rules forbid editing (`jb`, external workflow source,
      installed / user-level / plugin skills, and external reference folders).
  delegate_lifecycle_hard_stop: >
    Delegate may edit only the commissioned named target set. No commit, push,
    PR creation/update, merge, stash, reset, worktree cleanup, repository hygiene,
    or other lifecycle action; the CA owns all keep and land decisions after
    adjudication.
  model_ladder:
    ownership: operator_and_commission   # NOT Forseti review-lane authority; review-lane model-neutrality preserved
    rungs: author -> de_correlated_controller -> cheap_executor
    de_correlation_criterion: >
      family = vendor / model lineage (Claude vs GPT), NOT tier. Vendor = the
      upstream model developer/provider, NOT hosting platform / API reseller or
      wrapper or fine-tune owner; unknown or undisclosed lineage cannot satisfy
      cross-vendor. Cross-vendor de-correlation (author vendor != delegate vendor,
      recorded in the commission) is the DISCOVERY bar, required to claim the
      no-new-seam standard and to execute this lane. A same-vendor delegate is
      ineligible, including for bounded verification/sanity or closure recheck.
      A who-constraint only.
    concrete_model_ids: none_bound_in_overlay   # operator/tooling decision; the overlay does not prescribe, rank, or imply runtime models
    fallback: >
      none. If no different-vendor repo controller is available, leave the
      courier prompt unexecuted or route a separately named read-only review;
      never substitute same-vendor sanity or self-review into this lane.
  access_modes:
    default: repo
    values: [repo]
    selection_rule: >
      Direct repository/worktree access is required. no_repo routes to an
      ordinary read-only review prompt and must not be labeled delegated patch.
  preflight_schema:
    default: >
      Forseti Prompt Preflight core plus one fresh target-state read and
      Lane-Scoped Delegated Patch Prompt Default
      (.agents/workflow-overlay/prompt-orchestration.md).
    escalated: >
      forseti_start_preflight plus Escalated Preflight Fields only when a full
      orchestration condition or owner-invoked Mini God Tier applies.
  source_context_fields:
    - Default commission points to the targeted convention and relevant review lane; the receiver reads the real diff and target sources.
    - Source-Gated Method Contract and source packs/read budgets apply only when their independent triggers fire.
  output_destinations:
    delegate_return: >
      unified diff + neutral source citations + verdict + residual-risk note,
      plus an adjudicator next-moves tail that points the commissioning Chief
      Architect to communication-style.md -> Review Adjudication Next Step
      (paste-ready courier; delegate does not decide what is kept)
    commission_route_out: >
      one paste-ready operator-courier prompt by default; filed canonical prompt artifact or
      full-orchestrator output only when its routing conditions apply; use
      operator_to_fill for inferable but genuinely operator-owned values; never
      dispatch from the authoring invocation
    durable_review_report: optional only when separately commissioned or required by the owner-invoked Mini God Tier target; otherwise chat or lane PR/comment is the return
    patch_application: the CA-named target in-repo — single authored file, or the named multi-file set in delegated_code_review_and_patch — under the commission (patch / integration execution authority per .agents/workflow-overlay/review-lanes.md)
```

## Evidence And Non-Claims

**Evidence.** Replicated from jb's provisional convention, itself adopted on
limited in-session evidence — roughly two uses during jb's 2026-06-05
eval-contract hardening, where a de-correlated pass caught failure modes the
author had reintroduced against its own guardrails. Those are first-hand process
observations in jb; the limitation is their small number, not their validity,
and they are jb-side evidence, not a Forseti-measured result. The evidence
corroborates the pattern; it does not validate it.

**Non-claims.** This convention is provisional. It is not validation, not
readiness, not formal review authority, not a mandatory or machine-routable
review lane, not patch authorization beyond an explicit bounded CA commission,
and not runtime model routing. It does not import jb project authority, paths, or
lifecycle mechanics into Forseti; jb is cited only as cross-project provenance.

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
  receipt_storage_updated:
    - docs/decisions/dcp_receipts_archive_v0.md
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

# courier-only cross-vendor delegated patch route 2026-07-16 (owner correction).
direction_change_propagation:
  doctrine_changed: >
    Explicit delegate-patch invocations now author one operator-courier prompt
    only. The lane requires a different-vendor controller with direct repo
    access and has no same-vendor, no_repo, self, unknown-lineage, Codex-managed,
    task-creation, or automatic-dispatch fallback.
  trigger: review_authority
  related_triggers: [workflow_authority, validation_philosophy, lifecycle_boundary]
  controlling_sources_updated:
    - .agents/workflow-overlay/delegated-review-patch.md
    - .agents/workflow-overlay/prompt-orchestration.md
    - .agents/workflow-overlay/review-lanes.md
    - .agents/workflow-overlay/validation-gates.md
    - .agents/hooks/check_prompt_output_mode.py
    - docs/decisions/overlay_enforcement_placement_classification_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/decision-routing.md
    - .agents/workflow-overlay/safety-rules.md
    - .agents/hooks/check_prompt_provenance.py
    - .agents/hooks/pre_push_guard.py
    - .github/workflows/ci.yml
    - forseti-harness/tests/unit/test_ci_hook_wiring.py
    - docs/workflows/forseti_repo_map_v0.md
  intentionally_not_updated:
    - path: AGENTS.md
      reason: >
        The kernel already gives project-owned prompt and delegated-review
        overlay authority precedence; duplicating the invocation rule there
        would create a second owner.
    - path: installed or plugin workflow-delegated-review-patch skills
      reason: >
        Installed skills are protected deployment copies. The Forseti overlay
        precedence bridge is the writable project authority and now overrides
        the generic fallback explicitly.
    - path: .agents/hooks/README.md
      reason: >
        Existing active-lane overlap exclusion remains in force; the checker
        entry already points to the owning validation and placement sources.
    - path: docs/workflows/forseti_repo_map_v0.md
      reason: >
        No owner, path, or T1 retrieval route changed.
  stale_language_search: >
    rg -n -i "same.vendor|same.family|no_repo|create.*task|managed.worktree|delegate patch|operator_courier_only"
    .agents/workflow-overlay docs/prompts/templates AGENTS.md
  stale_language_search_result: >
    Executed 2026-07-16 after the correction. Live delegated-review-patch and
    lane-scoped prompt owners now require operator-courier-only, different-vendor,
    direct-repo execution and explicitly reject same-vendor, no_repo,
    Codex-managed, and task-creation fallback. Remaining same-vendor hits in
    review-lanes.md are the ordinary-review two-bar rule plus historical DCP
    receipts and now state that the tier cannot satisfy delegated patch. The
    general managed-receiver clause remains live only for non-delegated explicit
    implementation commissions. No prompt template contains the rejected
    delegated-patch fallback.
  non_claims:
    - not validation
    - not readiness
    - not runtime model routing
    - not proof of vendor identity or direct-write capability
    - not task-creation or dispatch authority
```

Older receipts archived verbatim in `docs/decisions/dcp_receipts_archive_v0.md`.
