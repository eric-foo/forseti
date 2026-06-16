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

**Access modes — `repo` (default) and `no_repo`.** The commission records `access: repo | no_repo` — an operator/commission access constraint, not a model choice. In **`repo`** mode the loop above runs as written: the de-correlated delegate patches the named target and returns a diff. In **`no_repo`** mode the delegate has no repo access and **does not patch**; it runs advisory-only via the portable review method (registry id `portable-adversarial-artifact-review-method`), returns findings (not a diff), and the **CA applies** accepted changes within the bounded scope. `no_repo` preserves de-correlated *review* but **not** de-correlated *patch authorship*, so it is **strictly weaker than `repo` mode** and **requires a bounded post-patch re-review** before keep — closure-of-findings plus any new blocker/major in the touched delta. Because that recheck is a narrow, near-mechanical verification against the findings' explicit closure conditions rather than open seam-discovery, it runs as a **same-family, different (lower / mechanical-tier) model** (a who-constraint, not a runtime-model recommendation), **not** a cross-family pass. **Cross-family de-correlation is reserved for discovery** (the original full adversarial review) and is **required to claim** the *survives-an-adversarial-review-with-no-new-seam* standard; a bounded same-family recheck does not by itself support that claim. The recheck is CA-adjudicated before anything is kept. The package ships the review target as a **verbatim file attachment** with an independently confirmable file hash (embedded-in-markdown copies are not byte-confirmable); and the package assembler/CA runs the portable method's **freshness gate** (hash-compare its `derived_from` pins to live sources; re-derive on mismatch) before bundling, recording the result in the commission. The default package shape is a **self-contained bundle**: the verbatim target attachment(s) plus a guardrail-complete `README` that carries the method, the authority excerpts, and the target's contract, delivered with a **thin-wrapper** chat prompt that points the reviewer at the in-bundle `README` — the wrapper still carries the cross-vendor who-constraint, which must not migrate silently into the bundle. When the reviewer cannot read in-bundle files, fall back to **inlining** the method block in the chat prompt; never ship a wrapper that points at a `README` a repo-blind reviewer cannot open. The de-correlation who-constraint, CA adjudication, `NEEDS_ARCHITECTURE_PASS`, and the strict-claim boundary are otherwise unchanged.

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
is not a single high-stakes authored artifact - for example a multi-file
implementation/code diff - do not stretch this convention to fit it. Route via
prompt-orchestrator to the appropriate review prompt, normally read-only
implementation/code review unless a separate patch-execution commission is
explicitly bound.

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
  incomplete_commission_route_out:
    owner: workflow-prompt-orchestrator
    output_mode: paste-ready-chat
    use_when: >
      Target and review purpose are inferable, but operator-owned route fields
      are missing; emit an operator-fill route-out prompt instead of an inert
      blocker.
    non_eligible_target_boundary: >
      Multi-file implementation/code diffs are routed to the appropriate review
      prompt, normally read-only code review, unless patch execution is
      separately commissioned.
  protected_path_list:
    authority: .agents/workflow-overlay/safety-rules.md   # defer to it; do not fork or restate the forbidden-edit set
    rule: >
      The delegate may patch ONLY the single CA-named target file. Everything
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
      upstream model developer/provider, NOT hosting platform / API reseller /
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
    values: [repo, no_repo]   # default repo; operator/commission access constraint, NOT model routing
    no_repo: >
      delegate advisory-only via portable-adversarial-artifact-review-method (returns findings, not a diff);
      CA applies the patch; REQUIRED post-patch re-review before keep, BOUNDED to closure-of-findings + new
      blocker/major in the touched delta and run by a SAME-VENDOR different/lower (mechanical-tier) model, NOT
      cross-vendor (the recheck is verification, not discovery); cross-vendor de-correlation is reserved for the
      discovery pass and is required to claim the no-new-seam standard; review target shipped as a
      hash-confirmable verbatim attachment; assembler/CA runs the portable-method freshness gate pre-bundle and records the result. Default package shape: a self-contained bundle (verbatim target attachment(s) + a guardrail-complete README carrying the method/authority/contract) delivered with a thin-wrapper chat prompt pointing at the in-bundle README; the wrapper still carries the cross-vendor who-constraint; inline the method in chat when the reviewer cannot read in-bundle files.
  preflight_schema:
    - orca_start_preflight (.agents/workflow-overlay/source-loading.md)
    - Required Preflight Fields (.agents/workflow-overlay/prompt-orchestration.md)
  source_context_fields:
    - Source-Gated Method Contract REFERENCE-LOAD / SOURCE-LOAD / SOURCE_CONTEXT_READY (.agents/workflow-overlay/prompt-orchestration.md)
    - source packs and read budgets (.agents/workflow-overlay/source-loading.md)
  output_destinations:
    delegate_return: unified diff + neutral source citations + verdict + residual-risk note (paste-ready courier to the commissioning Chief Architect)
    prompt_orchestrator_route_out: paste-ready-chat route-out prompt with operator_to_fill fields when target/purpose are inferable but commission fields are unbound
    durable_review_report: docs/review-outputs/ or docs/review-outputs/adversarial-artifact-reviews/ when a durable report is commissioned
    patch_application: the single CA-named target file in-repo, under the commission (patch / integration execution authority per .agents/workflow-overlay/review-lanes.md)
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
# repo-mode discovery discharges a downstream independent-review gate; added 2026-06-13 (CA + owner decision).
direction_change_propagation:
  doctrine_changed: >
    The repo-mode delegated review-and-patch loop -- cross-vendor delegate runs full-artifact discovery and
    authors the bounded fix; CA adjudicates and independently verifies via class-sweep + byte/scope checks --
    SATISFIES a cross_vendor_discovery independent-review requirement for the patched artifact, so a separate
    standalone post-patch re-scan is not additionally required to clear a downstream leakage gate.
    Proportionality is owner-set by assurance tier (buyer-proof may still require a separate pass;
    product-learning / N-case batch may rely on the delegated pass); the one non-independent sliver (the
    delegate's own edited lines) must be mechanically verifiable and the limitation recorded. Contrasts
    no_repo, which still requires the bounded same-vendor post-patch recheck. Validation/who-constraint
    framing only; not runtime-model routing.
  trigger: review_authority
  related_triggers: [validation_philosophy]
  controlling_sources_updated:
    - .agents/workflow-overlay/delegated-review-patch.md
  downstream_surfaces_checked:
    - path: .agents/workflow-overlay/review-lanes.md
      note: >
        two-bar rule is consistent (it already names cross_vendor_discovery as the discovery bar); a one-line
        cross-ref that the bar can be DELIVERED via the repo-mode delegated loop is recommended and deferred to
        a low-risk follow-up, not required (no stale routing without it).
    - path: docs/product/judgment_spine/conductor_construction_integrity_probe_addendum_v1.md
      note: >
        the R6 pre-freeze leakage gate is the consuming gate; conductor v1 is PROPOSED/pending ratification, so
        not edited mid-flight -- reconcile (R6 independent leakage review is satisfiable via the delegated loop)
        at its next revision/ratification.
    - path: .agents/workflow-overlay/validation-gates.md
      note: no new validation gate; this clarifies when an existing independent-review requirement is met.
  intentionally_not_updated:
    - path: AGENTS.md
      reason: the delegated-review-patch pointer already routes here; no top-level rule change.
  receipt_section_hygiene: >
    This file's inline receipt section now exceeds the <=2-most-recent-inline limit (source-of-truth.md DCP
    contract; it already held 4 before this change). Rotation of the older receipts to
    docs/decisions/dcp_receipts_archive_v0.md plus the required archive-pointer line is owed as a separate
    low-risk hygiene pass; deferred here to keep this doctrine change focused and reviewable.
  non_claims:
    - not validation
    - not readiness
    - not a bound/mandatory/machine-routable review lane (the convention stays provisional)
    - not runtime model routing
```

```yaml
# incomplete commission route-out fallback bound 2026-06-16 (CA decision).
direction_change_propagation:
  doctrine_changed: >
    Incomplete delegated-review-patch commissions now route through
    workflow-prompt-orchestrator as paste-ready route-out prompts when target
    and purpose are inferable, with missing operator-owned fields marked
    operator_to_fill; multi-file implementation/code diffs are routed to the
    appropriate review prompt instead of being stretched into this convention.
  trigger: review_authority
  related_triggers: [workflow_authority, output_authority]
  controlling_sources_updated:
    - .agents/workflow-overlay/delegated-review-patch.md
  receipt_storage_updated:
    - docs/decisions/dcp_receipts_archive_v0.md
  downstream_surfaces_checked:
    - .agents/workflow-overlay/prompt-orchestration.md
    - .agents/workflow-overlay/review-lanes.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/skill-adoption.md
    - AGENTS.md
  intentionally_not_updated:
    - path: .agents/workflow-overlay/prompt-orchestration.md
      reason: >
        Already owns prompt-orchestrator authoring, paste-ready-chat output,
        repo-aware prompt preflight, and source-gated review method sequencing;
        this patch routes to that owner instead of duplicating its contract.
    - path: .agents/workflow-overlay/review-lanes.md
      reason: >
        Already defines delegated review-and-patch as provisional, opt-in, and
        not machine-routable; the non-eligible target boundary belongs in the
        convention file rather than in the general lane index.
    - path: workflow-delegated-review-patch skill source and plugin cache
      reason: >
        External/user/plugin skill source is protected and not Orca project
        authority. This Orca behavior is bound in the overlay; reusable upstream
        skill-source changes require a separate skill-governance/deployment turn.
    - path: AGENTS.md
      reason: >
        Already routes delegated review-and-patch to the owning overlay file; a
        root restatement would fork the rule.
  stale_language_search: >
    rg -n "incomplete commission|operator_to_fill|prompt_orchestrator_route_out|multi-file implementation|code diff|machine-routable|workflow-prompt-orchestrator"
    .agents/workflow-overlay AGENTS.md
    plus targeted checks for protected external skill-source boundaries and
    prompt-orchestrator review defaults.
  stale_language_search_result: >
    Executed 2026-06-16. Live hits are the new route-out fallback and interface
    fields in delegated-review-patch.md; existing prompt-orchestrator ownership
    in AGENTS.md and prompt-orchestration.md; existing delegated-review-patch
    non-machine-routable text in delegated-review-patch.md and review-lanes.md;
    and existing skill-adoption/source-of-truth text that protects external,
    user-level, plugin, and installed skill source from ordinary Orca work. No
    checked live surface instructed agents to hand-draft route-out prompts,
    force multi-file code diffs into delegated review-and-patch, or edit
    external reusable skill source in this Orca overlay turn.
  non_claims:
    - not validation
    - not readiness
    - not a bound/mandatory/machine-routable review lane (the convention stays provisional)
    - not runtime model routing
    - not reusable skill-source deployment
```

Older receipts archived verbatim in `docs/decisions/dcp_receipts_archive_v0.md`.
