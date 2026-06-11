# Orca Claim Defense Doctrine v0 (Judgment-Quality Standard — claims policy)

```yaml
retrieval_header_version: 1
artifact_role: Product doctrine (external-claims policy; owner-signed operative)
scope: >
  Binds how Orca talks about its judgment evidence externally: the claim spine
  (built-to vs proven-at; the Judgment-Quality Standard frame; grader
  positioning), the per-tier approved/forbidden wording table (allowlist-first,
  activation keyed to the evidence ladder's closeout receipts), debunking
  triage by attack class, the adjudicate-critique-as-review process, and the
  receipts inventory. Subordinate to the evidence ladder and the pre-sale
  execution evidence tier policy; mints no tiers and ships no claim.
use_when:
  - Drafting, reviewing, or approving ANY externally visible sentence about Orca's judgment evidence.
  - Responding to external criticism, skepticism, or a debunking attempt.
  - Checking what may be said at the current evidence tier, and what activates later.
authority_boundary: retrieval_only
open_next:
  - docs/product/judgment_spine/judgment_spine_evidence_ladder_architecture_v0.md   # controls tier semantics
  - docs/decisions/judgment_spine_pre_sale_execution_evidence_tier_policy_v0.md     # controls execution-surface semantics
stale_if:
  - The owner amends or revokes the signed wording table (changes land as dated amendments, never silent rewrites).
  - The evidence ladder or tier policy changes (the table re-derives from them).
  - The public Judgment-Quality Standard document is authored (it becomes the external face; this stays the internal policy).
```

## Status

`OWNER_SIGNED_OPERATIVE` — a doc-local label. The owner signed 2026-06-11
(in-thread, post-review adjudication; recorded word: "Signed"). The wording
table below is now the operative external-claims policy; claims policy remains
owner-owned and later changes land as dated amendments, never silent rewrites.
Activation reality check at sign-off: the current claim cap is
product_learning, so Row 1 is the only live row; Rows 2–3 still activate only
on their named ladder receipts.

Authorization basis: owner direction in-thread 2026-06-11 — brand-the-standard
adopted ("that's the best way to do things"); attainment-claim path rejected
after pushback; grader positioning ("the judge decider... like PSA") adopted;
`/fused` authoring authorized. A delegated adversarial review is the
recommended pre-sign-off hardening (commissioned at authoring closeout).

Review completed 2026-06-11 (cross-vendor: `reviewed_by:
gpt-5_codex_exact_runtime_version_unexposed`, `de_correlation_bar:
cross_vendor_discovery`): 3 major findings, all proposed patches adjudicated
and KEPT by the commissioning home model — AR-01 attainment-leak phrase
replaced, AR-02 `Independence` triage class added, AR-03 receipts honesty
split (prospective vs retro-known/quarantined). Report:
`docs/review-outputs/adversarial-artifact-reviews/orca_claim_defense_doctrine_adversarial_artifact_review_v0.md`.
Owner signed 2026-06-11, after this review's adjudication (dated amendment
above).

## The Claim Spine

1. **Built-to vs proven-at.** Orca markets being *built to* the Orca
   Judgment-Quality Standard now; *proven at* a rung is claimable only when the
   ladder's receipt for that rung exists. The four words "built to" / "proven
   at" carry the entire external posture; no sentence may blur them.
2. **The standard is the asset.** Orca defines and operates the evidence
   standard for judgment claims; competitors must respond to our definition.
   The marketable claim is the standard's existence, rigor, and our visible
   discipline under it — never an attainment we have not receipted.
3. **Grader positioning.** Orca is the grader, not the contestant — the PSA
   posture: PSA does not claim to own the best cards; it owns the grade the
   market trusts. Two leak-checks travel with the analogy wherever it is used:
   (a) PSA grades third parties' assets; today Orca grades its own calls — the
   integrity substitute is the receipts machinery, and, once sealed calls
   mature, the stronger fact that **outcomes grade the sealed calls, not Orca**
   (reality as co-grader); (b) grading *others'* judgment (vendors', buyers'
   internal calls) is a future business question the positioning keeps open,
   not a claim or commitment now.
4. **Announcement discipline — two phrasings, never conflated.**
   - `Rung cleared:` attainment progressed under an unchanged bar (e.g., the
     first `completed_judgment_quality_evidence` receipt). Additive; receipt
     attached.
   - `Standard vN+1:` the bar itself changed (key changes, new controls).
     Dated changelog entry; the standard versions like the scoring key —
     pinned, dated, never silently rewritten.
   Saying "we improved our standard" when the fact is "we now meet it" (or the
   reverse) is the one blur that re-opens the moved-goalposts attack.
5. **Allowlist-first.** For any attainment-adjacent sentence, the approved
   column below is exhaustive: wording not listed does not ship — it escalates
   to the owner, and if adopted, lands here as a dated amendment first.

## Per-Tier Wording Table (OPERATIVE — owner-signed 2026-06-11)

Row activation is keyed to the evidence ladder's closeout receipts, never to
internal confidence. Tier semantics are CITED from the ladder; this table
defines nothing.

### Row 1 — NOW (claim cap: product_learning; basis: ladder `completed_product_learning_evidence` at best)

APPROVED:
- "Built to the Orca Judgment-Quality Standard." / "Built to a
  judgment-quality standard."
- "We publish and operate an evidence standard for judgment claims — most
  vendors don't define one."
- "Here is our evidence ladder, our controls, our ledgers — and exactly what
  we don't claim yet, and why. Audit us."
- "Judgment-evidence discipline: every claim is framed, labeled, and limited
  by its receipt."
- "Backtest results labeled product-learning, with prospective cases run under
  pre-declared ledgers, pinned scoring keys, and per-model recognition checks;
  retro-known cases disclosed as such and quarantined/reported, not laundered
  into clean evidence."
- Grader-positioning language per spine item 3, with both leak-checks intact.

FORBIDDEN (until the named receipt exists):
- "We have judgment quality" / "proven judgment quality" / "judgment quality
  achieved / validated / certified" — any attainment reading.
- "Sealed results" / "out-of-sample results" (none exist yet).
- Any results sentence without its tier label.
- "Blind," "no-tools," or isolation claims for any run on an advisory
  chat/manual surface (tier policy: those surfaces cannot by themselves
  support probe-pass, blind-use, product-proof, or judgment-quality claims;
  gate-bearing claims require the gate-bearing execution tier and its
  requirements).
- Unqualified "proven / validated / certified" anywhere near "judgment."

### Row 2 — activates on a `completed_buyer_proof_evidence` receipt

ADDS (with buyer consent and the receipt attached):
- "A qualified decision owner used Orca's memo for a live allocation
  decision."
- Pull-signal and proof-memo-fit language as the buyer-proof receipt supports.

STILL FORBIDDEN: every Row-1 forbidden item that lacks its receipt — buyer
proof cannot by itself support clean no-tools evidence, fixture admission, or
a judgment-quality claim (ladder, buyer_proof `cannot_support_by_itself`).

### Row 3 — activates on a `completed_judgment_quality_evidence` receipt (controlling harness contract)

ADDS:
- "Proven at the Standard's judgment-quality rung: sealed blind run, scored
  under the pinned key, outcome reveal and calibration record — receipts
  attached."
- The `Rung cleared:` announcement per spine item 4.

STILL FORBIDDEN even then (ladder, judgment_quality `cannot_support_by_itself`):
- "Buyers validated it" / willingness-to-pay proof / product or commercial
  readiness — by itself, the JQ receipt supports none of these.

## Debunking Triage (attack classes; answer per class, never across)

| Class | Sounds like | Correct response | Never |
| --- | --- | --- | --- |
| Provenance | "contaminated / cherry-picked / tuned after results" | The one receipt that kills it (see inventory), within days | Argue without artifacts |
| Method | "your scoring key / rubric is wrong" | Openness: the key is versioned and pinned; disagreement is recorded AS evidence (e.g., the floor-4 contest); invite the specific critique into the next dated key proposal | Defend the key as beyond critique |
| Independence | "you grade yourselves / no independent auditor" | Name the self-grading caveat directly: today the integrity substitute is receipts machinery, and sealed-call maturity adds reality as co-grader; do not claim third-party certification | Borrow PSA's third-party-independence credibility |
| Overclaim | "you said more than you have" | Quote the claim's tier label and this table; if we actually overclaimed: concede, correct in place, dated amendment | Reinterpret our own words after the fact |
| Category | "LLMs can't judge" | Reframe to the measurable contract — calls versus outcomes under the Standard; decline the philosophy debate | Argue in the abstract |

## Adjudicate Critique As Review

External criticism is processed as an unsolicited adversarial review:

1. Log each distinct claim the critic makes.
2. Classify each by the triage classes above.
3. Adjudicate each: right / partly right / wrong.
4. Where right: concede precisely and fast; dated amendment to the affected
   record; if a shipped claim was wrong, correct it in place. A precise
   concession is a product demo — for a judgment company, visible updating IS
   judgment; defensiveness is the anti-demo.
5. Where wrong: one-line rebuttal with the receipt, not an essay.
6. Record the exchange. Norm (not yet an ops SLA): receipts answer in days;
   a debunking answered in hours with artifacts dies, the same one answered in
   weeks with prose becomes the story.

## Receipts Inventory (attack family -> the artifact that answers it)

| Attack | Receipt |
| --- | --- |
| "Tuned the key after seeing results" | Scoring-key SHA256 pins recorded in the batch ledger for prospective batch runs; retro-known dev cases are disclosed as retro/quarantined and cannot carry clean evidence |
| "Cherry-picked the cases" | Pre-declared ledger for prospective cases; all-results reporting rule; swaps and retro-known/quarantined cases recorded as findings |
| "The model knew the outcome" | Per-case-and-model recognition probes on record; contaminated arms reported as data; (future) sealed outcome-free calls |
| "Moved the goalposts" | Versioned standard; dated-amendment-only rule on ledgers and doctrine |
| "Nothing is verifiable" | The audit invitation plus the receipts above; diligence access posture is owner-gated per engagement |

## Amendment - Org-Motion Backtest Bias Defenses (2026-06-11, owner direction, in-thread)

The owner directed, in-thread 2026-06-11, recording the org-motion backtest's
anti-bias mechanisms as defense receipts. These **extend** (do not rewrite) the
Debunking Triage and Receipts Inventory above. Source artifacts:
`docs/decisions/judgment_spine_backtest_batch1_ledger_declaration_v0.md` (the
Org-Motion Batch Pre-Commitment amendment) and the proposed conductor addendum
`docs/product/judgment_spine/conductor_construction_integrity_probe_addendum_proposal_v0.md`
(outcome-blind construction + JSG-05 probe refinement; pending sign-off +
delegated review).

| Attack (Provenance / Independence class) | Receipt |
| --- | --- |
| "You cherry-picked the case where org-motion happened to work" | The org-motion **batch pre-commitment**: the case set and the run-on-all rule are fixed *before* each case's gate-0 reveals alignment; **all** results reported (incl. feasibility failures and non-moves). A single favorable case is disclosed AS a favorable-by-selection anecdote, never promoted; the defensible claim is a pre-committed K-of-N hit-rate. |
| "You steered the packets toward the org-motion conclusion" | **Outcome-blind construction**: the with/without packets and any anonymization are built by an actor not holding the sealed outcome; org-motion enters as raw job-list facts, never an editorialized read. The outcome-aware facilitator only reveals/calibrates. |
| "Your recognition probe manufactured the recognition it measured" | **Passive-first, non-inducing probe**: contamination is detected primarily by reading the sealed judgment for outcome-knowledge it could not have from the packet; the light familiarity probe is dropped (false-positive-prone); active "name the case" recall is a post-seal forensic only, never a pre-judgment prime. |

These are product-learning-tier process receipts; they harden the *method*, not
the claim cap (Row 1 still governs what may be said). The conductor-addendum
receipts count as *ratified* only on that addendum's sign-off + delegated review.

## Subordination

The evidence ladder and the tier policy control all tier and execution-surface
semantics. This doctrine cites them and defines neither; on any conflict, this
doctrine loses and is amended. Row activation happens only on the ladder's
named closeout receipts. Mints no tiers, relabels no current state, and never
re-tiers an existing artifact.

## Non-Claims

Not validation, readiness, buyer proof, or judgment-quality evidence. Ships no
external claim by itself; every shipped claim still needs its receipt and its
tier label. Not the public Judgment-Quality Standard document (that artifact is
born at its recorded trigger: before Orca's first externally published
evidence claim). Not marketing copy. The PSA analogy is positioning language,
not a certification-business commitment. The wording table was owner-signed
2026-06-11 (see Status); before that date the no-external-claims posture stood.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    The Orca claim-defense doctrine (built-to vs proven-at claim spine,
    per-tier wording table, debunking triage, adjudicate-critique-as-review,
    receipts inventory) advanced from PROPOSED_PENDING_OWNER_SIGNOFF to
    owner-signed operative external-claims policy on 2026-06-11.
  trigger: product_doctrine
  related_triggers: []
  controlling_sources_updated:
    - docs/product/product_lead/orca_claim_defense_doctrine_v0.md
    - docs/hygiene/queue.md                                  # row ORCA-HYGIENE-014 closed at sign-off
    - docs/workflows/orca_repo_map_v0.md                     # product-anchor row added (committed 9e93538)
    - docs/decisions/orca_product_thesis_consumer_demand_v0.md  # evidence-basis status cell refreshed to the now-true label
  downstream_surfaces_checked:
    - docs/product/judgment_spine/judgment_spine_evidence_ladder_architecture_v0.md
    - docs/decisions/judgment_spine_pre_sale_execution_evidence_tier_policy_v0.md
    - docs/research/judgment-spine/ideal_judgment_quality_run_and_current_position_v0.md
    - .agents/workflow-overlay/product-proof.md
    - docs/prompts/reviews/orca_claim_defense_doctrine_adversarial_artifact_review_prompt_v0.md
    - docs/review-outputs/adversarial-artifact-reviews/orca_claim_defense_doctrine_adversarial_artifact_review_v0.md
  intentionally_not_updated:
    - path: docs/product/judgment_spine/judgment_spine_evidence_ladder_architecture_v0.md
      reason: >
        Controls tier semantics and is senior to this doctrine; subordination
        is one-way and sign-off changes nothing the ladder owns.
    - path: docs/decisions/judgment_spine_pre_sale_execution_evidence_tier_policy_v0.md
      reason: >
        Controls execution-surface semantics; unchanged for the same
        subordination reason.
    - path: docs/research/judgment-spine/ideal_judgment_quality_run_and_current_position_v0.md
      reason: >
        Its dated claims-posture note already routes external wording here
        without restating table status; the route is unchanged by sign-off.
    - path: .agents/workflow-overlay/product-proof.md
      reason: >
        Owns claim-tier classification mechanics, not wording policy; no
        conflict found (grep for claim/wording/external rules, 2026-06-11) and
        no overlay pointer is needed — discovery runs through the repo-map
        product-anchor row.
    - path: docs/prompts/reviews/orca_claim_defense_doctrine_adversarial_artifact_review_prompt_v0.md
      reason: >
        Documents the dispatched pre-review state by design (pins the
        pre-review hash); historical artifact, not a live routing surface.
    - path: docs/review-outputs/adversarial-artifact-reviews/orca_claim_defense_doctrine_adversarial_artifact_review_v0.md
      reason: >
        Review records are never rewritten; its PROPOSED reference describes
        the target as reviewed, which stays historically true.
  stale_language_search: >
    rg -in "PROPOSED_PENDING_OWNER_SIGNOFF|pending owner sign-off|awaiting
    owner sign-off" docs/
  stale_language_search_result: >
    Executed 2026-06-11 after the sign-off edits. Every remaining hit is
    either another artifact's own genuinely-pending status (ICP wedge
    decision, consumer-demand product thesis, finder frame references in the
    charter recommendation and spine CA prompt) or the review report's
    historical statement about the pre-patch target. No live surface still
    describes the claim-defense doctrine as proposed or pending.
  non_claims:
    - not validation
    - not readiness
    - not buyer proof
    - not judgment-quality evidence
    - sign-off adopts wording policy only; every shipped claim still requires its tier receipt and label
```
