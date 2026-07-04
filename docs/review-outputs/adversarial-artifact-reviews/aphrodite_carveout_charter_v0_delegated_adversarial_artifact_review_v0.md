# Aphrodite Carveout Charter v0 Delegated Adversarial Artifact Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review report
scope: >
  Delegated adversarial artifact review-and-patch return for the Aphrodite
  carveout charter v0 and the D8 waitlist-fields amendment in the Forseti
  company/brand architecture ADR.
use_when:
  - Adjudicating the delegated review-and-patch return for PR #656.
  - Checking the bounded patch, findings, citations, verdict, and residual risk
    before deciding what, if anything, to keep.
authority_boundary: retrieval_only
reviewed_by: gpt-5-codex
provided_by_vendor_family: OpenAI
authored_by: claude-fable-5
author_home_family: Anthropic
de_correlation_bar: cross_vendor_discovery
controller_role: external-controller-courier
repo: github.com/eric-foo/orca
branch: claude/sleepy-bassi-2dec16
head: 17778ec1e95d41392cf80e5dbfa758791cf9707e
source_context: SOURCE_CONTEXT_READY
stale_if:
  - orca/product/spines/creator_signal/aphrodite_carveout_charter_v0.md changes.
  - docs/decisions/forseti_company_brand_architecture_v0.md changes in the D8 amendment scope.
  - Any controlling record named in the commission supersedes the reviewed text.
```

## Findings

Review frame: the boundary problem was whether a DRAFT strategy register and a narrow ADR amendment routed to controlling records without importing validation, willingness-to-pay, buyer-proof, readiness, or build authority. Material failure modes were absolute moat language, incomplete proof-gate restatement, numeric claim strength drift, and D8 wording that could pull a later Aphrodite surface forward. Decision criteria were source consistency, claim-tier discipline, DECIDE/DEFAULT/DEFER register integrity, residual honesty, and receipt accuracy.

### AR-01 - major - [charter]

Location: `orca/product/spines/creator_signal/aphrodite_carveout_charter_v0.md` strategy one-sentence and moat boundary.

Issue: The original one-sentence strategy said the asset was one "nobody can copy," while the same charter's honest boundary says a funded competitor could replicate the corpus in months and the product architecture frames the defensible moat as capture history and time-series advantage, not impossibility.

Evidence: `orca/product/spines/creator_signal/aphrodite_carveout_charter_v0.md:120` states a funded competitor could replicate the corpus in months; `orca/product/spines/creator_signal/creator_signal_product_architecture_v0.md:54` to `:59` frames the moat as a longitudinal vertical evidence graph and capture-history advantage; patched charter language at `orca/product/spines/creator_signal/aphrodite_carveout_charter_v0.md:77` to `:80` now says hard to copy on a useful timeline.

Impact: A cold reader could treat the charter as claiming a validated or absolute competitive barrier, contradicting the artifact's own honest boundary.

minimum_closure_condition: The strategy summary must express defensibility as time-and-depth advantage, not absolute non-copyability.

next_authorized_action: CA adjudicates the patched wording as decision input and either keeps, modifies, or rejects it.

### AR-02 - major - [charter]

Location: `orca/product/spines/creator_signal/aphrodite_carveout_charter_v0.md` phase table and buyer-proof grammar paragraph.

Issue: The original charter compressed the house graduation grammar into the repeat/pull thresholds alone. The buyer-proof packet requires all graduation criteria to be met and accepted, including repeatability without software, non-bespoke deck behavior, strongest-value discipline, no dashboard/source-system dependency, and intact non-claims.

Evidence: `orca/product/spines/product_lead/buyer_proof/orca_buyer_proof_packet_v0.md:561` to `:570` lists the full graduation criteria; `orca/product/spines/product_lead/buyer_proof/orca_buyer_proof_packet_v0.md:499` to `:501` says a fixed-scope paid sprint is only a hypothesis, not WTP proof; `.agents/workflow-overlay/product-proof.md:84` to `:90` says pull requires observable budget-adjacent behavior, not approval language. Patched charter lines `orca/product/spines/creator_signal/aphrodite_carveout_charter_v0.md:86` and `:182` to `:194` now distinguish the minimum repeat/pull anchor from the full graduation gate.

Impact: The old text could let a later lane graduate the carveout on two thresholds while silently dropping controlling proof criteria.

minimum_closure_condition: The charter must route to the full house graduation grammar and label the repeat/pull threshold as a minimum anchor, not the complete gate.

next_authorized_action: CA adjudicates the patched gate wording as decision input and either keeps, modifies, or rejects it.

### AR-03 - minor - [charter]

Location: `orca/product/spines/creator_signal/aphrodite_carveout_charter_v0.md` accepted residuals table.

Issue: The residual table repeated `~90-95%` / `~20-30%` capture values without carrying the local hypothesis-tier label in the row itself. The section title and register already mark every capture number as hypothesis-tier, but the table row is the scannable surface most likely to be quoted alone.

Evidence: `orca/product/spines/creator_signal/aphrodite_carveout_charter_v0.md:196` to `:199` says capture numbers are hypothesis-tier; `docs/decisions/orca_mini_god_tier_doctrine_v0.md:98` to `:103` says percent language is target calibration only and not a numeric achievement claim without independent evidence; patched row `orca/product/spines/creator_signal/aphrodite_carveout_charter_v0.md:267` now labels the estimate as hypothesis-tier.

Impact: Low but real claim-tier leakage risk when the residual table is consumed out of context.

minimum_closure_condition: Numeric capture-value/cost estimates in the residual row must carry their hypothesis-tier status locally.

next_authorized_action: CA adjudicates the patched row as decision input and either keeps, modifies, or rejects it.

### AR-04 - major - [adr-d8]

Location: `docs/decisions/forseti_company_brand_architecture_v0.md` D8 amendment and appended DCP receipt.

Issue: The original D8 amendment described waitlist fields on the Aphrodite pre-launch holding surface as if D8 item 1 alone authorized that surface. D8 item 3 names the only near-term holding page as forsetihq.com, and D8 item 6 defers Aphrodite design to the Vetting v0 trigger. The amendment needed to preserve the optional fields while making the Aphrodite surface conditional on separate authorization.

Evidence: `docs/decisions/forseti_company_brand_architecture_v0.md:247` to `:250` names the forsetihq.com holding page as the only near-term surface; `docs/decisions/forseti_company_brand_architecture_v0.md:266` to `:270` says Aphrodite design fires at the Vetting v0 trigger, not before; patched amendment lines `docs/decisions/forseti_company_brand_architecture_v0.md:278` to `:292` now condition the later Aphrodite surface on separate authorization; patched DCP receipt lines `docs/decisions/forseti_company_brand_architecture_v0.md:443` to `:448` carries the same scope.

Impact: The old text could be read as moving a gate or authorizing an Aphrodite holding surface earlier than D8 permits.

minimum_closure_condition: The D8 amendment must preserve optional role/decision-type fields without moving Aphrodite design, build, or publish gates.

next_authorized_action: CA adjudicates the patched amendment and receipt as decision input and either keeps, modifies, or rejects them.

## Diff

```diff
diff --git a/docs/decisions/forseti_company_brand_architecture_v0.md b/docs/decisions/forseti_company_brand_architecture_v0.md
index 2d218857..eb5a39d8 100644
--- a/docs/decisions/forseti_company_brand_architecture_v0.md
+++ b/docs/decisions/forseti_company_brand_architecture_v0.md
# [adr-d8]
@@ -277,10 +277,12 @@ concrete web foundation; it changes no gate and launches nothing.

 Owner-ratified in-thread ("Add the two fields (Recommended)", 2026-07-04,
 Aphrodite carveout charter session). The waitlist capture element of the D8
-web foundation — on the forsetihq.com holding page (D8 item 3) and on the
-Aphrodite pre-launch holding surface (D8 item 1) — may collect two **optional**
-self-reported fields alongside email: **role** and **decision type**. Purpose:
-passive buyer-lane sequencing signal for the Aphrodite carveout
+web foundation may collect two **optional** self-reported fields alongside
+email on the forsetihq.com holding page (D8 item 3), and on a later Aphrodite
+pre-launch holding surface only if/when that surface is separately authorized
+under D8's Vetting-v0/public-launch sequencing (D8 items 1 and 6): **role**
+and **decision type**. Purpose: passive buyer-lane sequencing signal for the
+Aphrodite carveout
 (`orca/product/spines/creator_signal/aphrodite_carveout_charter_v0.md`,
 register row R-2).

# [adr-d8]
@@ -438,8 +440,9 @@ direction_change_propagation:
 # D8 amendment 2026-07-04 (waitlist role fields; ratified in the Aphrodite carveout charter session).
 direction_change_propagation:
   doctrine_changed: >
-    D8 amended: the waitlist capture on both holding surfaces may collect two
-    optional self-reported fields (role, decision type) alongside email, as
+    D8 amended: waitlist capture may collect two optional self-reported fields
+    (role, decision type) alongside email on the Forseti holding page, and on
+    any later separately authorized Aphrodite pre-launch holding surface, as
     passive buyer-lane sequencing signal for the Aphrodite carveout. Optional
     only; same privacy-notice posture; no other D8 element, gate, or
     authorization changes.
diff --git a/orca/product/spines/creator_signal/aphrodite_carveout_charter_v0.md b/orca/product/spines/creator_signal/aphrodite_carveout_charter_v0.md
index 33bf2238..43a46ebe 100644
--- a/orca/product/spines/creator_signal/aphrodite_carveout_charter_v0.md
+++ b/orca/product/spines/creator_signal/aphrodite_carveout_charter_v0.md
# [charter]
@@ -74,16 +74,16 @@ not move.

 ## 2. Strategy

-**One sentence: quietly build an evidence asset nobody can copy, prove one
-buyer will pay for a decision made from it, productize only what repeats — and
-keep the whole customer line a trigger-gated option whose downside is capped
-because the data asset compounds regardless.**
+**One sentence: quietly build an evidence asset that becomes hard to copy on a
+useful timeline, prove one buyer will pay for a decision made from it,
+productize only what repeats — and keep the whole customer line a trigger-gated
+option whose downside is capped because the data asset compounds regardless.**

 | Phase | What happens | Gate to enter | Customer-facing? |
 | --- | --- | --- | --- |
 | **0 — Foundation (now)** | Feed the evidence asset (registry growth, depth capture, ontology); strategy on paper; stay dark | — (current state) | No. Only the ratified holding page + waitlist (with role/decision-type fields per the D8 amendment, 2026-07-04) |
 | **1 — Prove payment** | One paid design-partner **Vetting Sprint** per buyer; readback; WTP evidence is the primary output | Foundation exit gate (deferred decision — register row D-1) fires Vetting v0; buyer probes separately owner-gated | Gated, design-partner only |
-| **2 — Productize repeats** | Pricing/packaging/SaaS decisions; external claim schema lock | ≥2 independent qualified buyers at Grade A/B + ≥1 paid-sprint-level pull (house graduation grammar) | Gated |
+| **2 — Productize repeats** | Pricing/packaging/SaaS decisions; external claim schema lock | Full house graduation grammar adapted at sprint time; minimum repeat/pull anchor = ≥2 independent qualified buyers at Grade A/B + ≥1 paid-sprint-level pull | Gated |
 | **3 — Public launch** | Own domain, handles, formal trademark clearance, marketing posture | Owner decision; bundle per brand ADR D8 | Yes |

 Sequencing authority is unchanged: foundation-first per the product
# [charter]
@@ -184,11 +184,14 @@ Proof semantics are consumed, not redefined, from
 `orca/product/spines/product_lead/buyer_proof/orca_buyer_proof_packet_v0.md`
 (adapted to this product at sprint time — the parent's demand-substrate gate
 does not transfer; the pull/praise, trust-objection/refusal, kill-discipline,
-and graduation grammar do): pull is paid-path behavior, never praise; graduate
-on ≥2 independent qualified decision owners at Grade A/B plus ≥1
-paid-sprint-level pull; park on majority forbidden-feature pull, repeated
-trust refusal, or a dry bounded batch. Every claim in this charter's scope is
-capped at `product_learning` tier until receipts exist.
+and graduation grammar do): pull is paid-path behavior, never praise. The
+≥2 independent qualified decision owners at Grade A/B plus ≥1
+paid-sprint-level pull threshold is the minimum repeat/pull anchor, not the
+full graduation gate; at sprint adaptation the packet's repeatability,
+no-dashboard/no-source-system, no-bespoke-value, and non-claim criteria still
+have to hold. Park on majority forbidden-feature pull, repeated trust refusal,
+or a dry bounded batch. Every claim in this charter's scope is capped at
+`product_learning` tier until receipts exist.

 ## 6. Capture policy (hypothesis-tier; numbers are capture-lane calibration, not commitments)

# [charter]
@@ -261,7 +264,7 @@ trigger. Without this table the MGT label would be hype.
 | --- | --- | --- | --- |
 | Single lead buyer lane (brands) instead of a parallel 3-lane probe | Cheapest discriminating path; probes are owner-gated anyway | Lead lane could be wrong | First bounded batch runs dry → open next lane (D-5) |
 | No numeric foundation gate pre-committed | Numbers would be unvalidated guesses; the practice-run rehearsal is the real test either way | Capture lane lacks a hard numeric finish line | First rehearsal failure mints evidence-based numbers (D-1) |
-| Stratified (not full) transcript corpus | ~90–95% of decision value at ~20–30% of capture cost; analytics are view-weighted | Organic mentions in unsampled median videos missed | Metadata scan on all videos mitigates; sprint-specific needs pulled on demand |
+| Stratified (not full) transcript corpus | Hypothesis-tier estimate: ~90–95% of decision value at ~20–30% of capture cost; analytics are view-weighted | Organic mentions in unsampled median videos missed | Metadata scan on all videos mitigates; sprint-specific needs pulled on demand |
 | Page-1 comments only | Engagement-ranked page carries the decision signal | Superfan skew; drift; moderation invisible | Named-limitation display; re-probe on trigger |
 | No pricing menu / tiers | One unit must sell before a ladder exists | Cannot quote beyond the sprint | First paid conversation → commercial-frame pass (D-2) |
 | No freshness SLA | Single-operator manual posture is the verified state | Staleness at readback | Refresh-before-readback rule now; SLA only when a customer requires one |
```

## Per-Change Citations

- C-01 [charter]: The patched strategy line at `orca/product/spines/creator_signal/aphrodite_carveout_charter_v0.md:77` to `:80` aligns with the honest-boundary language at `:120` to `:123` and the product architecture's capture-history moat at `orca/product/spines/creator_signal/creator_signal_product_architecture_v0.md:54` to `:59`.
- C-02 [charter]: The patched phase/gate text at `orca/product/spines/creator_signal/aphrodite_carveout_charter_v0.md:86` and `:182` to `:194` aligns with buyer-proof graduation criteria at `orca/product/spines/product_lead/buyer_proof/orca_buyer_proof_packet_v0.md:561` to `:570` and pull semantics at `.agents/workflow-overlay/product-proof.md:84` to `:90`.
- C-03 [charter]: The patched residual row at `orca/product/spines/creator_signal/aphrodite_carveout_charter_v0.md:267` keeps local consistency with `:196` to `:199` and the Mini God Tier percent-language guard at `docs/decisions/orca_mini_god_tier_doctrine_v0.md:98` to `:103`.
- C-04 [adr-d8]: The patched amendment at `docs/decisions/forseti_company_brand_architecture_v0.md:278` to `:292` and receipt at `:443` to `:448` align with D8's near-term surface and design-order boundaries at `:247` to `:250` and `:266` to `:274`.

## Receipt Checks

- `rg -in "aphrodite" --glob "!docs/_inbox/**" --glob "!orca/product/spines/creator_signal/aphrodite_carveout_charter_v0.md" .` returned hits in the expected live file families: the brand ADR, the Creator Signal README, the Forseti web-foundation handoff, and the captured evidence datapoint.
- `rg -in "waitlist" docs/decisions/forseti_company_brand_architecture_v0.md docs/workflows/forseti_web_foundation_design_lane_handoff_v0.md` returned the expected ADR D6/D8/amendment/receipt hits plus the point-in-time web-foundation handoff hits.

## Verdict

Overall verdict: patched with major findings for CA adjudication; no `NEEDS_ARCHITECTURE_PASS` condition was found.

[charter] sub-verdict: the charter is materially safer after patching the absolute moat language, the compressed proof-gate wording, and the numeric residual label. It remains a DRAFT strategy register and does not become ratified, validated, buyer-proof, WTP-proven, ready, or implementation-authorizing by this review.

[adr-d8] sub-verdict: the D8 amendment is materially safer after making the Aphrodite pre-launch surface conditional on the already-ratified D8 sequencing and aligning the appended DCP receipt.

## Residual Risk

The owner-ratification quotes in the charter were checked as artifact text, not against the original chat transcript, because the commission's source pack did not include the transcript. No off-scope patch was attempted. The DCP receipt searches were cheap-checkable and were rerun after the patch; they support the receipt shape but do not validate owner intent, product proof, readiness, or acceptance.

## Blockers And Off-Scope Flags

No blocker remained after source loading. No off-scope protected, canonical, generated, runtime, test, or overlay path was edited. The report itself was written under the commissioned review-output path.

review_use_boundary: >
  Findings, citations, verdicts, and the patched diff are decision input only; they are not approval, validation, mandatory remediation, or executor-ready patch authority. The commissioning CA decides what, if anything, is kept.

DELEGATED_ARTIFACT_REVIEW_RETURN_FOR_HOME_MODEL

Here is the delegated artifact review result. Adjudicate it under the delegated-review-patch return contract.

- original commission or review target: Aphrodite carveout charter v0 plus the D8 waitlist-fields amendment scope in the Forseti company/brand ADR.
- reviewed artifact and bounded patch scope: [charter] full file; [adr-d8] D8 amendment section and appended DCP receipt only.
- findings and source evidence: AR-01 through AR-04 above.
- proposed artifact patch or exact suggested edits: the working-tree diff in this report.
- citations: C-01 through C-04 above.
- reviewer verdict: patched with major findings for CA adjudication; no `NEEDS_ARCHITECTURE_PASS`.
- residual risk: owner-word transcript not independently checked; no validation, readiness, buyer-proof, WTP, or acceptance claim.
- blockers, off-scope flags, and not-proven boundaries: no remaining blockers; no off-scope edits; all findings are decision input only.

Commissioning CA: adjudicate the findings, diff, verdict, and residuals as claims per `.agents/workflow-overlay/communication-style.md` → Review Adjudication Next Step. Nothing is kept before adjudication.
