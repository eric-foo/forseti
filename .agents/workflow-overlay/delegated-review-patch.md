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

**Citations.** The delegate's citations are neutral in tone — factual source
evidence, no advocacy or editorializing — but decision-sufficient in substance,
so the Chief Architect's veto stays informed rather than blind. The delegate's
argument belongs in the verdict and residual, not the citations. Neutral tone is
not thinness: thin citations would push the Chief Architect back onto its own
priors and defeat the de-correlation.

**De-correlation — observable criterion and fallback.** The commission must
record the author model family and the delegate model family; the lane is
satisfied only when they differ, and when the Chief Architect authors with an
Opus-class model the delegate must be a different, non-Opus family. A
same-family or self pass does not satisfy it. If de-correlation cannot be
established (for example, no different-family model is available), do not claim
this lane: fall back to the standard source-read-only review lane plus Chief
Architect self-review, and record the limitation.

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

## Overlay Interface (fields a future skill implementation may read)

This is the seam to handoff 2 (a skill implementation, authored separately - not in
this overlay binding). The fields below defer to existing Orca overlay authority
and do not fork or restate it.

```yaml
delegated_review_patch_overlay_interface:
  status: provisional_opt_in   # available only by explicit CA commission; not a bound review lane; not mandatory
  operating_contract_pointer: .agents/workflow-overlay/delegated-review-patch.md
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
      author model family != delegate model family, recorded in the commission;
      an Opus-class author requires a non-Opus delegate. A who-constraint only.
    concrete_model_ids: none_bound_in_overlay   # operator/tooling decision; the overlay does not prescribe, rank, or imply runtime models
    fallback: >
      if no different-family model is available, do not claim this lane; fall
      back to source-read-only review + CA self-review and record the limitation.
  preflight_schema:
    - orca_start_preflight (.agents/workflow-overlay/source-loading.md)
    - Required Preflight Fields (.agents/workflow-overlay/prompt-orchestration.md)
  source_context_fields:
    - Source-Gated Method Contract REFERENCE-LOAD / SOURCE-LOAD / SOURCE_CONTEXT_READY (.agents/workflow-overlay/prompt-orchestration.md)
    - source packs and read budgets (.agents/workflow-overlay/source-loading.md)
  output_destinations:
    delegate_return: unified diff + neutral source citations + verdict + residual-risk note (paste-ready courier to the commissioning Chief Architect)
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
direction_change_propagation:
  doctrine_changed: >
    Orca now carries a provisional, opt-in Delegated Review-and-Patch convention:
    under an explicit Chief Architect commission, a de-correlated executor may run
    a combined review-and-patch hardening pass on a single named high-stakes
    authored artifact, with the CA adjudicating the returned diff before anything
    is kept. It is not a bound review lane and creates no strict claims.
  trigger: review_authority
  related_triggers:
    - workflow_authority
  controlling_sources_updated:
    - .agents/workflow-overlay/delegated-review-patch.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/review-lanes.md
    - AGENTS.md
    - CLAUDE.md
    - docs/workflows/orca_repo_map_v0.md
  downstream_surfaces_checked:
    - .agents/workflow-overlay/prompt-orchestration.md
    - .agents/workflow-overlay/validation-gates.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/communication-style.md
    - .agents/workflow-overlay/safety-rules.md
  intentionally_not_updated:
    - path: .agents/workflow-overlay/prompt-orchestration.md
      reason: >
        Model-neutrality, review-prompt findings-first defaults, strict-claim
        gates, and preflight fields are unchanged. The convention defers to them
        and adds a who-constraint, not review-lane model routing.
    - path: .agents/workflow-overlay/validation-gates.md
      reason: >
        The convention claims no validation or readiness and creates no new
        validation gate; existing gates are unchanged.
    - path: .agents/workflow-overlay/source-loading.md
      reason: >
        Preflight receipt and source packs are referenced, not changed.
    - path: .agents/workflow-overlay/safety-rules.md
      reason: >
        The protected-path list defers to safety-rules as the authority rather
        than forking a new forbidden-edit set; no safety rule changes.
  stale_language_search: >
    rg -n "source-read-only|Reviewer threads are source-read-only|runtime model|model-neutral|reviewer still does not edit|patch authority"
    .agents/workflow-overlay/review-lanes.md
    .agents/workflow-overlay/prompt-orchestration.md
    AGENTS.md CLAUDE.md
  stale_language_search_result: >
    Run during this binding. Hits are the existing reviewer-read-only rule and
    the existing model-neutrality rule. The convention is consistent with both:
    the delegate is a commissioned executor (not a read-only reviewer), and
    de-correlation is a commission who-constraint, not review-lane model routing.
    No prior text claimed authored artifacts may never be patched or that no
    commissioned-executor path exists, so no language was made stale.
  non_claims:
    - not validation
    - not readiness
    - not formal review authority
    - not a mandatory or machine-routable review lane
    - not runtime model routing
    - not jb authority import
```
