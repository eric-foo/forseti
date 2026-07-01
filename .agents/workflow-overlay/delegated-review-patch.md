# Delegated Review-and-Patch For High-Stakes Authored Artifacts (Provisional)

```yaml
retrieval_header_version: 1
artifact_role: Orca overlay authority
scope: >
  Provisional delegated review-and-patch convention for high-stakes authored
  Orca artifacts, plus the overlay-interface fields a future skill implementation may read.
use_when:
  - A Chief Architect is deciding whether to commission a delegated
    review-and-patch hardening pass on a high-stakes authored artifact.
  - Checking the overlay-interface fields (status, operating-contract pointer,
    protected paths, model ladder, preflight, source context, output
    destinations) this convention exposes.
authority_boundary: retrieval_only
```

**Status — provisional convention.** This is an experimental operating
convention replicated into Orca from jb's provisional convention (jb branch
`lane/delegated-review-patch-convention`, commit `345397b`), adopted on limited
cross-project evidence (see *Evidence* below). It is not bound Orca review
doctrine and not a machine-routable review lane: it carries no strict, formal,
or operational lane authority, and `.agents/workflow-overlay/review-lanes.md`
"Current Lanes" intentionally does not bind it yet. Treat it as guidance the
Chief Architect may choose to commission, refined as it is used; promote it to a
bound lane only after more uses and a separate Orca overlay binding decision.

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
step with no deep-thinking and deep-think the 1-5 material next moves that need
judgment. The land step plus the material moves are a required tail of the
adjudication closeout, not an optional pass -- an adjudication that ends at the
verdict without them is incomplete. This is a prompt-return obligation for the
adjudicator, not permission for the delegate to decide what is kept or to widen
review scope.

**Access selection rule.** `repo` is the default access mode. Use `no_repo` only when the commission explicitly records `access: no_repo` and records why repository access is unavailable or intentionally excluded. Cross-vendor, external, couriered, paste-ready-chat, or portable-method dispatch does **not** imply `no_repo`; a de-correlated controller with repo/worktree access still runs repo mode. If access is missing from an otherwise inferable commission, the route-out prompt marks `access: operator_to_fill` but names `repo` as the default, not `no_repo`.

**Access modes — `repo` (default) and `no_repo`.** The commission records `access: repo | no_repo` — an operator/commission access constraint, not a model choice. In **`repo`** mode the loop above runs as written: the de-correlated delegate patches the named target and returns a diff. In **`no_repo`** mode the delegate has no repo access and **does not patch**; it runs advisory-only and returns findings (not a diff), and the **CA applies** accepted changes within the bounded scope. `no_repo` preserves de-correlated *review* but **not** de-correlated *patch authorship*, so it is **strictly weaker than `repo` mode** and **requires a bounded post-patch re-review** before keep — closure-of-findings plus any new blocker/major in the touched delta. The no-repo review method is target-kind specific: `authored_artifact` uses the portable review method (registry id `portable-adversarial-artifact-review-method`), while `delegated_code_review_and_patch` uses a repo-blind code-review package/prompt that preserves `workflow-code-review` method requirements as far as no-repo access permits. Because the post-patch recheck is a narrow, near-mechanical verification against the findings' explicit closure conditions rather than open seam-discovery, it runs as a **same-family, different (lower / mechanical-tier) model** (a who-constraint, not a runtime-model recommendation), **not** a cross-family pass. **Cross-family de-correlation is reserved for discovery** (the original full adversarial review) and is **required to claim** the *survives-an-adversarial-review-with-no-new-seam* standard; a bounded same-family recheck does not by itself support that claim. The recheck is CA-adjudicated before anything is kept. The no_repo package ships the review target as a **verbatim file attachment** with an independently confirmable file hash (embedded-in-markdown copies are not byte-confirmable); and the package assembler/CA runs the target-kind method's **freshness gate** before bundling, recording the result in the commission. The standard no_repo package shape is a **self-contained bundle**: the verbatim target attachment(s) plus a guardrail-complete `README` that carries the method, the authority excerpts, and the target's contract, delivered with a **thin-wrapper** chat prompt that points the reviewer at the in-bundle `README` — the wrapper still carries the cross-vendor who-constraint, which must not migrate silently into the bundle. When the reviewer cannot read in-bundle files, fall back to **inlining** the method block in the chat prompt; never ship a wrapper that points at a `README` a repo-blind reviewer cannot open. The de-correlation who-constraint, CA adjudication, `NEEDS_ARCHITECTURE_PASS`, and the strict-claim boundary are otherwise unchanged.

**Citations.** The delegate's citations are neutral in tone — factual source
evidence, no advocacy or editorializing — but decision-sufficient in substance,
so the Chief Architect's veto stays informed rather than blind. The delegate's
argument belongs in the verdict and residual, not the citations. Neutral tone is
not thinness: thin citations would push the Chief Architect back onto its own
priors and defeat the de-correlation.

**De-correlation — observable criterion and fallback.** "Family" here means
**vendor / model lineage** (e.g., Claude vs GPT), **not tier**. **Vendor** = the upstream model
developer/provider (e.g., Anthropic, OpenAI) — **not** the hosting platform, API
reseller, deployment surface, or wrapper/fine-tune owner; **unknown or undisclosed
lineage cannot satisfy the cross-vendor (discovery) bar** and falls to the
same-vendor/sanity tier. The commission
must record the author vendor and the delegate vendor; the **cross-vendor
discovery** bar is satisfied only when they **differ**. A same-vendor delegate —
**even a different or lower tier** (e.g., an Opus author with a Sonnet delegate)
— does **not** satisfy cross-vendor de-correlation; it is the **same-vendor
verification/sanity tier** (see the two-bar rule in
`.agents/workflow-overlay/review-lanes.md`), not a discovery pass. A self pass
never satisfies it. If a cross-vendor delegate cannot be established, do not
claim the discovery (no-new-seam) bar: use the same-vendor sanity tier, or fall
back to source-read-only review plus Chief Architect self-review, and record the
limitation.

This is a who-constraint recorded in the commission, not a model-quality
recommendation and not runtime model routing. It does not belong in review
prompts as model-selection advice, and it does not alter Orca review-lane
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
Route the request through `workflow-prompt-orchestrator` and return a
`paste-ready-chat` route-out prompt with the missing operator fields clearly
marked `operator_to_fill`. Block instead only when the target or review purpose
cannot be inferred, when prompt-orchestrator cannot be applied under
`.agents/workflow-overlay/prompt-orchestration.md`, or when the user asks for
strict execution or patching without a bound commission. If the inferred target
is a multi-file implementation/code diff rather than a single authored artifact,
do not force it into the default authored-artifact mode: route it to the
**`delegated_code_review_and_patch`** sibling mode below, which keeps the code
review lane as its review method and bounds the patch to an explicitly named
file set. When no patch authority is commissioned, route via prompt-orchestrator
to read-only implementation/code review instead; patch authority is never
assumed from the target category.

**Code-diff target kind — the `delegated_code_review_and_patch` sibling mode.**
The default loop above targets a single *authored* artifact and uses the
delegate's own adversarial analysis as the review. A bounded multi-file
implementation/code diff is handled by this **sibling mode**: the same
commissioned convention with exactly two binding deltas. Everything else —
explicit commission, the de-correlation who-constraint and two-bar rule, the
`repo` / `no_repo` access-mode obligations, CA adjudication of the returned diff
before any keep, the `NEEDS_ARCHITECTURE_PASS` escalation, the strict-claim
boundary, and the no-runtime-model-recommendation rule — is inherited unchanged.
The code-review method remains the method in both access modes; `no_repo` only
changes repository access and patch authorship.

1. **The review method is the code review lane, not artifact review.** The
   delegate's review portion is `workflow-code-review` run under the Review
   Prompt Defaults (`workflow-deep-thinking` first, then the Source-Gated Method
   Contract in `.agents/workflow-overlay/prompt-orchestration.md`) — not the
   `portable-adversarial-artifact-review-method`. The code review lane stays the
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
  under `.agents/workflow-overlay/safety-rules.md` and `AGENTS.md`; this mode
  supplies the *shape*, never a standing authorization, and never bypasses the
  implementation-authorization boundary. By commission, not by category — the
  code-diff category alone never triggers this mode; an un-commissioned diff
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
buyer-proof, not zero. This **contrasts `no_repo`**, which still requires the
bounded same-vendor post-patch recheck because the CA, not the delegate, authored
the patch (patch-time de-correlation is lost there, preserved here).

## Overlay Interface (fields a future skill implementation may read)

This is the seam to handoff 2 (a skill implementation, authored separately - not in
this overlay binding). The fields below defer to existing Orca overlay authority
and do not fork or restate it.

```yaml
delegated_review_patch_overlay_interface:
  status: provisional_opt_in   # available only by explicit CA commission; not a bound review lane; not mandatory
  operating_contract_pointer: .agents/workflow-overlay/delegated-review-patch.md
  target_kinds:
    authored_artifact: >
      Default mode; a single CA-named authored artifact (doctrine, operating
      contract, eval/scoring/validation instrument). Review method is the
      delegate's own adversarial analysis (portable-adversarial-artifact-review-method
      in no_repo). Single-file patch bound.
    delegated_code_review_and_patch: >
      Sibling mode for a bounded multi-file implementation/code diff. Review
      method is the code review lane (workflow-code-review, deep-thinking first,
      source-gated), NOT artifact review and never a merge of the two. Target is
      an explicitly named file set (one or more) that CANNOT silently widen;
      everything outside it is read-only / flag-only. Validation/test obligations
      are named and can fail. Patch authority is an explicit commission
      subordinate to the implementation-authorization boundary in safety-rules.md
      / AGENTS.md, never assumed from the category. All other convention machinery
      (commission, de-correlation / two-bar, access-mode obligations, CA
      adjudication before keep, NEEDS_ARCHITECTURE_PASS, strict-claim boundary,
      no runtime-model recommendation) is inherited unchanged. no_repo changes
      repository access and patch authorship, not the code-review method.
  incomplete_commission_route_out:
    owner: workflow-prompt-orchestrator
    output_mode: paste-ready-chat
    use_when: >
      Target and review purpose are inferable, but operator-owned route fields
      are missing; emit an operator-fill route-out prompt instead of an inert
      blocker.
    code_diff_target_routing: >
      A multi-file implementation/code diff is handled by the
      delegated_code_review_and_patch sibling mode (target_kinds above) when patch
      authority is commissioned; an un-commissioned diff routes to read-only code
      review. Patch authority is never assumed from the target category.
  protected_path_list:
    authority: .agents/workflow-overlay/safety-rules.md   # defer to it; do not fork or restate the forbidden-edit set
    rule: >
      The delegate may patch ONLY the CA-named target — the single authored file
      in the default mode, or the explicitly named multi-file set in
      delegated_code_review_and_patch (which cannot silently widen). Everything
      else is read-only / flag-only: all other Orca sources; canonical, frozen,
      or hash-pinned decisions, product contracts, manifests, and
      provenance/review-output ledgers; other `.agents/workflow-overlay/` files;
      `AGENTS.md` and `CLAUDE.md` when they are not the named target; and every
      path the safety rules forbid editing (`jb`, external workflow source,
      installed / user-level / plugin skills, and external reference folders).
  model_ladder:
    ownership: operator_and_commission   # NOT Orca review-lane authority; review-lane model-neutrality preserved
    rungs: author -> de_correlated_controller -> cheap_executor
    de_correlation_criterion: >
      family = vendor / model lineage (Claude vs GPT), NOT tier. Vendor = the
      upstream model developer/provider, NOT hosting platform / API reseller or
      wrapper or fine-tune owner; unknown or undisclosed lineage cannot satisfy
      cross-vendor. Cross-vendor de-correlation (author vendor != delegate vendor,
      recorded in the commission) is the DISCOVERY bar, required to claim the
      no-new-seam standard. A same-vendor delegate (typically a different/lower
      tier, Opus -> Sonnet) may only claim bounded verification/sanity, never
      discovery/no-new-seam. A who-constraint only.
    concrete_model_ids: none_bound_in_overlay   # operator/tooling decision; the overlay does not prescribe, rank, or imply runtime models
    fallback: >
      if no different-family model is available, do not claim this lane; fall
      back to source-read-only review + CA self-review and record the limitation.
  access_modes:
    default: repo
    values: [repo, no_repo]   # operator/commission access constraint, NOT model routing
    selection_rule: >
      repo is the default. no_repo requires an explicit commission value plus the
      reason repository access is unavailable or intentionally excluded.
      Cross-vendor, external, couriered, paste-ready-chat, or portable-method
      dispatch does not imply no_repo; a controller with repo/worktree access
      remains repo mode.
    no_repo: >
      delegate advisory-only (returns findings, not a diff); authored_artifact uses
      portable-adversarial-artifact-review-method, while delegated_code_review_and_patch uses a
      repo-blind code-review package/prompt that preserves workflow-code-review method requirements as far as
      no-repo access permits; CA applies the patch; REQUIRED post-patch re-review before keep, BOUNDED to closure-of-findings + new
      blocker/major in the touched delta and run by a SAME-VENDOR different/lower (mechanical-tier) model, NOT
      cross-vendor (the recheck is verification, not discovery); cross-vendor de-correlation is reserved for the
      discovery pass and is required to claim the no-new-seam standard; review target shipped as a
      hash-confirmable verbatim attachment; assembler/CA runs the target-kind method's freshness gate pre-bundle and records the result. Default package shape: a self-contained bundle (verbatim target attachment(s) + a guardrail-complete README carrying the method/authority/contract) delivered with a thin-wrapper chat prompt pointing at the in-bundle README; the wrapper still carries the cross-vendor who-constraint; inline the method in chat when the reviewer cannot read in-bundle files.
  preflight_schema:
    - orca_start_preflight (.agents/workflow-overlay/source-loading.md)
    - Required Preflight Fields (.agents/workflow-overlay/prompt-orchestration.md)
  source_context_fields:
    - Source-Gated Method Contract REFERENCE-LOAD / SOURCE-LOAD / SOURCE_CONTEXT_READY (.agents/workflow-overlay/prompt-orchestration.md)
    - source packs and read budgets (.agents/workflow-overlay/source-loading.md)
  output_destinations:
    delegate_return: >
      unified diff + neutral source citations + verdict + residual-risk note,
      plus an adjudicator next-moves tail that points the commissioning Chief
      Architect to communication-style.md -> Review Adjudication Next Step
      (paste-ready courier; delegate does not decide what is kept)
    prompt_orchestrator_route_out: paste-ready-chat route-out prompt with operator_to_fill fields when target/purpose are inferable but commission fields are unbound
    durable_review_report: docs/review-outputs/ or docs/review-outputs/adversarial-artifact-reviews/ when a durable report is commissioned
    patch_application: the CA-named target in-repo — single authored file, or the named multi-file set in delegated_code_review_and_patch — under the commission (patch / integration execution authority per .agents/workflow-overlay/review-lanes.md)
```

## Evidence And Non-Claims

**Evidence.** Replicated from jb's provisional convention, itself adopted on
limited in-session evidence — roughly two uses during jb's 2026-06-05
eval-contract hardening, where a de-correlated pass caught failure modes the
author had reintroduced against its own guardrails. Those are first-hand process
observations in jb; the limitation is their small number, not their validity,
and they are jb-side evidence, not an Orca-measured result. The evidence
corroborates the pattern; it does not validate it.

**Non-claims.** This convention is provisional. It is not validation, not
readiness, not formal review authority, not a mandatory or machine-routable
review lane, not patch authorization beyond an explicit bounded CA commission,
and not runtime model routing. It does not import jb project authority, paths, or
lifecycle mechanics into Orca; jb is cited only as cross-project provenance.

## Direction Change Propagation

```yaml
# review adjudication next-moves tail bound 2026-06-30 (CA decision).
direction_change_propagation:
  doctrine_changed: >
    Delegated review-and-patch returns now explicitly carry the existing Review
    Adjudication Next Step tail: the return/courier prompt instructs the
    commissioning Chief Architect, after adjudicating the verdict/diff/findings,
    to batch admin/lifecycle follow-ups into one no-deep-thinking land step and
    deep-think only the 1-3 material next moves that need judgment. This hardens
    the delegated-review seam without moving the admin/material shape out of
    communication-style.md or changing prompt-orchestration.md's review prompt
    default.
  trigger: review_authority
  related_triggers: [workflow_authority, output_authority]
  controlling_sources_updated:
    - .agents/workflow-overlay/delegated-review-patch.md
  downstream_surfaces_checked:
    - path: .agents/workflow-overlay/communication-style.md
      note: >
        Already owns the exact Review Adjudication Next Step shape; no copy or
        fork added here beyond a pointer.
    - path: .agents/workflow-overlay/prompt-orchestration.md
      note: >
        Already requires every review prompt and review-return/courier prompt to
        instruct the adjudicator to run the next-moves pass after the verdict.
        No edit.
    - path: .agents/workflow-overlay/review-lanes.md
      note: >
        Review-lane findings still own minimum_closure_condition and
        next_authorized_action; this patch only binds the delegated return's
        adjudication closeout tail. No edit.
    - path: AGENTS.md
      note: >
        Already routes delegated-review-patch and prompt artifacts to the owning
        overlay/prompt-orchestration sources; no root restatement added.
    - path: docs/workflows/orca_repo_map_v0.md
      note: >
        Its delegated-review-patch index line remains accurate; no new section
        or artifact path was added.
  intentionally_not_updated:
    - path: .agents/workflow-overlay/communication-style.md
      reason: >
        The admin/material next-step shape already exists there and remains the
        single owner.
    - path: .agents/workflow-overlay/prompt-orchestration.md
      reason: >
        The review prompt default already carries the review-return/courier
        prompt obligation; duplicating the shape there would fork the owner.
  stale_language_search: >
    rg -ni "Review Adjudication Next Step|next-moves pass|admin/lifecycle|delegate_return|operator_closeout_source|review-return"
    .agents docs/prompts/templates docs/workflows AGENTS.md
  stale_language_search_result: >
    Executed 2026-06-30. communication-style.md owns the shape; prompt-orchestration.md
    already binds review prompts and review-return/courier prompts; delegated-review-patch.md
    was the only live overlay seam whose delegate_return output still stopped at
    diff/citations/verdict/residual-risk without naming the adjudicator next-moves
    tail. No prompt template or repo-map contradiction found.
  non_claims:
    - not validation
    - not readiness
    - not a bound/mandatory/machine-routable review lane
    - not runtime model routing
    - not standing implementation/code-patch authorization
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

```

Older receipts archived verbatim in `docs/decisions/dcp_receipts_archive_v0.md`.
