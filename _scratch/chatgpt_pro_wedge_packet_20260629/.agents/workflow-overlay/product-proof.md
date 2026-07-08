# Product Proof

```yaml
retrieval_header_version: 1
artifact_role: Orca overlay authority
scope: Buyer-proof semantics, trust-objection handling, pull signals, zero-spoiler backtest behavior, and product-proof non-claims.
use_when:
  - Creating or reviewing Orca product-proof artifacts.
  - Creating or reviewing Orca case-study, backtest, preflight, or calibration artifacts.
  - Defining customer discovery, buyer qualification, memo/deck readback, kill, continue, or graduation rules.
  - Checking whether historical case or consulting-case material leaks recommendations, actions, outcomes, or result quality before a blind judgment.
  - Checking whether proof artifacts confuse objections with disqualifiers.
authority_boundary: retrieval_only
```

This file owns reusable Orca product-proof semantics. Prompt mechanics still
belong in `prompt-orchestration.md`; review lane behavior still belongs in
`review-lanes.md`; validation checks still belong in `validation-gates.md`.

For Judgment Spine work, claim-tier and closeout-state architecture is controlled by
`orca/product/spines/judgment/claim_ladder/judgment_spine_evidence_ladder_architecture_v0.md`. Product-proof
artifacts may use Product-Learning evidence as design input, but they must not
reuse Product-Learning evidence as Buyer-Proof evidence unless the buyer-proof
promotion gate in that artifact is satisfied. Buyer-proof artifacts that make
or block a proof, readiness, validation, scoring, fixture, blind-use, or
judgment-quality claim must name the ladder-owned `closeout_state` inline or
co-reference a durable claim-classification record.

## Trust Objection Versus Refusal

Buyer skepticism is not a disqualifier by default.

Classify public-signal trust state as:

- `trust_open`: the buyer already sees public signals as potentially relevant.
- `trust_objection`: the buyer is skeptical but willing to evaluate evidence
  quality, examples, numbers, mechanism, case logic, a proof memo, or a
  decision artifact.
- `trust_refusal`: the buyer states public signals cannot affect the decision
  regardless of evidence quality, examples, numbers, mechanism, case logic, or
  proof experience.

Only `trust_refusal` disqualifies or blocks memo or deck production.

`trust_objection` is proof material. Capture it, test it, and read it back. It
may proceed through discovery and memo production when other qualification and
gate criteria pass. Executive deck production may proceed only when the memo
and evidence appendix pass the same gates and the deck is tied to qualified
live-decision circulation.

Preferred qualification language:

```text
Buyer is willing to evaluate whether public-signal evidence can affect the
decision after the method, evidence quality, examples, numbers, case logic,
proof memo, or decision artifact are explained.
```

Preferred disqualifier language:

```text
Categorical trust refusal: buyer says public-signal evidence cannot affect this
decision regardless of evidence quality, explanation, examples, numbers, case
logic, proof memo, or decision artifact.
```

## Kill Criteria Discipline

Kill criteria must not fire on initial skepticism. They may fire only when the
buyer refuses the evidence type, the proof experience fails to overcome the
objection, or the result shows the public-signal basis cannot affect the target
decision.

Treat trust objections as learning signals:

- what public evidence the buyer would trust;
- what evidence the buyer would discount;
- what mechanism, example, number, or case logic would make the evidence usable;
- whether the proof memo, evidence appendix, or executive deck changes the
  trust posture.

## Pull Versus Praise

Buyer pull means observable decision or budget-adjacent behavior, not approval
language.

Praise, curiosity, generic deck interest, or generic research requests are not
pull. Pull requires behavior such as a live decision, decision-owner readback,
internal circulation, decision change, fixed-scope paid decision sprint signal,
procurement path, budget-owner meeting, or urgent referral to another live
decision owner.

A decision-owner request for an executive deck for internal decision
circulation may count as pull only when it is tied to a qualified live
decision, actual decision use, and budget-adjacent behavior. A deck request
detached from those conditions is presentation interest, not pull.

## Judgment Spine Claim-Tier Boundary

Judgment Spine artifacts must classify their claim tier and `closeout_state`
before making proof, readiness, validation, scoring, fixture-admission,
blind-use, or judgment-quality claims.

Use these tiers:

- `product_learning`: internal learning about packet usability, operator
  friction, narrative clarity, and product experience. Manual subscription/chat
  advisory output belongs here unless a stronger gate is separately satisfied.
- `buyer_proof`: qualified buyer/live-decision proof using a memo plus evidence
  appendix, buyer readback, and pull-versus-praise classification.
- `judgment_quality`: harness-grade evidence from frozen packet, structural
  no-tools execution, sealed blind judgment, scoring, and calibration gates.

Lower-tier evidence may inform the design of a higher-tier artifact, but it
must not carry its claim upward. Manual advisory output does not become buyer
proof merely because it is persuasive, and buyer pull does not become
judgment-quality evidence merely because the buyer finds the memo useful.

Classification must either appear in the artifact itself or co-reference a
durable `judgment_spine_claim_classification` record that names source-quality
state, execution-quality state, `closeout_state`, claim cap, missing or failed
gate, and receipt artifact or gap. A buyer-proof memo, deck, or readback
artifact without inline classification or a durable co-reference is not
buyer-proof-ready.

## Zero-Spoiler Backtest Behavior

All Orca case-study and historical backtest work must preserve blind judgment
until the owner or participant has made the judgment call.

Participant-facing case packets, preflights, source lists, prompts, summaries,
and reports must not reveal:

- the actual decision made;
- consulting-firm recommendation or action;
- implementation status;
- post-cutoff facts;
- later outcome, result quality, success/failure label, or outcome metrics;
- source titles, snippets, URLs, or filenames that leak any of the above.

Participant-facing material may include only clean pre-cutoff evidence, the
decision question, role frame, constraints, admissible uncertainty, and explicit
unknowns. It must ask what should be done, not tell or imply what happened.

Keep these lanes separate:

- `participant_packet`: pre-cutoff evidence only; no recommendation reveal and
  no outcome facts.
- `facilitator_ledger`: sealed non-participant material for consulting-page
  recommendation/action claims, actual public decision records, and post-cutoff
  outcome evidence.
- `blind_judgment`: owner or participant decision captured before any reveal.
- `outcome_calibration`: post-reveal comparison after the blind judgment is
  sealed.

For consulting-firm case studies, never treat consulting-page success claims as
ground truth. Separate:

- consulting-page narrative;
- independent pre-decision evidence;
- actual public decision record;
- independent post-outcome evidence;
- Orca/user blind judgment.

Preflight may check whether post-outcome evidence appears available, but any
participant-visible preflight result must express that only as a non-spoiling
admissibility state. It must not disclose what the action, recommendation,
implementation, or outcome was.

If spoiler material is introduced into participant-facing text before the blind
judgment is sealed, mark that packet or preflight as contaminated. Do not
repair it by deleting sentences in place for participant use; rebuild a clean
zero-spoiler packet from pre-cutoff sources and keep the contaminated material
out of the participant path.

## Product-Proof Non-Claims

Product-proof artifacts must preserve these non-claims unless a later accepted
Orca source explicitly changes them:

- no buyer validation;
- no buyer-proof evidence unless the buyer-proof receipt is complete and the
  Judgment Spine closeout state permits the claim;
- no willingness-to-pay proof;
- no repeatability proof;
- no product readiness;
- no feature readiness;
- no implementation readiness;
- no commercial readiness;
- no Core Spine v0 validation.

Customer discovery, memo usefulness, deck usefulness, or a single strong buyer
signal does not authorize feature planning, implementation planning,
source-system design, automation, dashboards, source maps, data-spine work, or
readiness claims.

## Direction Change Propagation - Judgment Spine Closeout-State Alignment

```yaml
direction_change_propagation:
  doctrine_changed: >
    Product-proof work that makes or blocks Judgment Spine proof, readiness,
    validation, scoring, fixture, blind-use, or judgment-quality claims now
    must apply the ladder-owned closeout_state requirement.
  trigger: validation_philosophy
  controlling_sources_updated:
    - .agents/workflow-overlay/product-proof.md
    - .agents/workflow-overlay/validation-gates.md
    - orca/product/spines/judgment/claim_ladder/judgment_spine_evidence_ladder_architecture_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/source-loading.md
    - docs/workflows/orca_repo_map_v0.md
  intentionally_not_updated:
    - path: orca/product/spines/judgment/conductor/judgment_quality_promotion_operating_model_v0.md
      reason: >
        Deferred by owner decision; this patch aligns existing proof and gate
        surfaces without creating the later thin operating-model spine.
    - path: Daimler-specific run, prompt, source, and decision artifacts
      reason: >
        This is case-agnostic proof-boundary doctrine. Daimler case artifacts
        require a separate case-specific receipt or closeout decision.
  stale_language_search: >
    rg -n "closeout_state|no_durable_evidence|weakest-cleared-gate|buyer-proof"
    .agents/workflow-overlay/product-proof.md
    .agents/workflow-overlay/validation-gates.md
    orca/product/spines/judgment/claim_ladder/judgment_spine_evidence_ladder_architecture_v0.md
    .agents/workflow-overlay/source-loading.md
    docs/workflows/orca_repo_map_v0.md
  non_claims:
    - not validation
    - not readiness
    - not buyer proof
    - not judgment-quality proof
    - not implementation authorization
```
