# Marc Jacobs Beauty Relaunch Understanding — Claim-Sensitive Capture Stopping Dogfood v0

```yaml
retrieval_header_version: 1
artifact_role: Commission-local dogfood pre-registration and closeout
scope: >
  Pre-registered shadow comparison of current Scanning closure against a
  claim-sensitive capture-stopping candidate during the Marc Jacobs Beauty
  relaunch Understanding cycle.
use_when:
  - Running or auditing the Marc Jacobs Beauty claim-sensitive stopping dogfood.
  - Replaying the pre-registered policies against chronological checkpoint packets.
authority_boundary: retrieval_only
open_next:
  - docs/research/forseti_beauty_marc_jacobs_beauty_relaunch_understanding_commission_board_v0.md
  - forseti/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md
  - forseti/product/spines/scanning/scan_core/forseti_scanning_intelligent_walk_mgt_operating_model_v0.md
downstream_consumers:
  - owner dogfood adjudication
  - de-correlated adversarial reviewer only if promoted
stale_if:
  - A referenced locator or hash stops resolving.
```

## Pre-registration state

```yaml
dogfood_id: marc_jacobs_beauty_relaunch_claim_sensitive_stop_20260719
cycle_id: marc_jacobs_beauty_relaunch_understanding_20260719
commission_id: marc_jacobs_beauty_relaunch_understanding_csb_20260719
canonical_phase: Understanding
turn: Acquire & Seal
state: PRE_REGISTERED_NOT_RUN
owner_acceptance:
  source: current owner task
  observed_date: "2026-07-19"
  accepted_candidate: Marc Jacobs Beauty relaunch
baseline_revision: d5d31006231fc2fe4ba004ad3f075629b7bb115b
comparison_claim: product_learning_only
```

This artifact must be committed before external acquisition. Its first commit
is the anti-hindsight seal. Later results append to this file; they do not
rewrite the question, policies, checkpoint triggers, or disposition criteria.

## Bound commission

```yaml
subject:
  brand: Marc Jacobs Beauty
  operating_partner_context: Coty
mode: forward
commission_profile: company_competitive_intelligence
as_of_date: "2026-07-19"
time_posture: recency_first
phase_question: >
  What does current public evidence show about how the relaunched Marc Jacobs
  Beauty proposition is expressed across owned claims, assortment, Sephora
  presentation, and early user experience, and where do those surfaces align,
  conflict, or remain unproven?
intended_use: >
  Decision-neutral Understanding evidence plus a shadow claim-sensitive
  capture-stopping dogfood; no demand, prevalence, recommendation, GTM, or
  competitor verdict.
heritage_boundary: >
  Heritage is contextual only when a current source invokes it; historical
  reconstruction is not load-bearing.
```

## Ordered information jobs and routes

| order | ID | information job | route | required result |
| ---: | --- | --- | --- | --- |
| 0 | R0 | Establish subject identity and the current relaunch frame: proposition, partnership, launch scope, prices, assortment, and named channels. | Coty announcement first; current Marc Jacobs surfaces as linked or discovered. | Direct current first-party observation, contradiction, or typed blocking result. |
| 1 | R1 | Establish how the current owned proposition is expressed through assortment, product claims, packaging, textures, and experience language. | Current Marc Jacobs Beauty brand and product pages under the Source Capture Playbook. | Attributable observations with current-page limits; no inferred performance. |
| 2 | R2 | Test retail translation and early dated product experience. | Canonical Sephora retail/PDP and review routes. | Retail observations and row-level dated review evidence or typed gaps; no delivery, local-stock, representative-demand, or prevalence inference. |
| 3 | R3 | Test early community alignment, conflict, corrections, and counterevidence. | Mandatory bounded Reddit native scout, then canonical preservation for selected threads; TikTok only for a unique non-dominated job. | Attributable experience evidence, contradiction, or typed gap with claim class preserved. |
| 4 | R4 | Test independent corroboration, source syndication, hidden venues, and contradictions. | Bounded editorial/trade reads, exact queries, and category-aware discovery. | Independent observation, syndication limitation, decisive negative, contradiction, or typed gap. |
| 5 | R5 | Determine whether another non-dominated path could still change the permitted claim or material qualification. | Current Scanning expected-decision-value closure authority. | Current-policy closure or visible blocked/incomplete state. |

Quora is recorded as `not_required_no_decision_material_job`; it has no
non-substitutable job in this commission. Ulta is outside scope. Sephora's
current route may support a US/USD storefront observation but not a delivery
destination or local-stock claim while delivery location remains unpinned.

## Reference horizon

The real collector runs only under current Scanning closure:

> Continue while the best remaining non-dominated move has a credible chance of
> changing the permitted claim, material qualification, contradiction state, or
> gap enough to justify marginal cost, latency, access risk, and duplication.

The reference horizon is the evidence actually captured before that policy
closes or visibly blocks. It is comparison evidence, not ground truth. The
collector does not extend acquisition to improve the dogfood and does not see
Policy B or evaluator decisions.

## Pre-registered checkpoints

| checkpoint | trigger |
| --- | --- |
| CP0 | R0 identity and current relaunch-frame acquisition closes or visibly blocks |
| CP1 | R1 owned-proposition acquisition closes or visibly blocks |
| CP2 | R2 Sephora retail/PDP/review acquisition closes or visibly blocks |
| CP3 | R3 Reddit/community acquisition closes or visibly blocks |
| CP4 | R4 corroboration/contradiction work completes and R5 current-policy closure is assessed |

Each packet contains only receipts and observations available through that
boundary. The coordinator records its locator, SHA-256, included receipt IDs,
and included observation IDs. Both arms receive byte-identical packet bytes.
Checkpoint order and inclusion cannot change after evidence is seen.

## Policy A — current Scanning closure

Continue while a non-dominated acquisition move has enough expected decision
value to justify its marginal cost, latency, access risk, and duplication.
Close when every material requirement is answered, contradicted, honestly held
as a typed gap, or lacks a remaining non-dominated path whose expected decision
value materially exceeds those costs.

## Policy B — claim-sensitive candidate

Policy B applies Policy A plus all of the following:

1. One attributable instance can establish existence only.
2. Recurrence or mechanism requires independent corroboration until another
   plausible capture would not materially change the claim, mechanism, or
   material qualification.
3. Prevalence, concentration, or comparison requires a defined sample,
   denominator, and comparable method; otherwise it remains unestablished.
4. Severe negative evidence accelerates preservation, investigation, and any
   load-bearing owner escalation. It never establishes representativeness by
   severity alone.
5. Stop only when further plausible capture would not change the permitted
   claim and the remaining paths are blocked or dominated.

## Cold collector and evaluator protocol

The collector receives the validated CSB, normal Scanning/Capture authority,
route order, and Policy A only. It must not read this dogfood artifact,
checkpoint material, Policy B, or evaluator work. It returns a source-read
manifest. Exposure invalidates the experiment but does not erase legitimately
captured evidence.

After the collector closes or visibly blocks:

1. Create checkpoint packets from the chronological receipts.
2. Spawn two fresh same-runtime evaluators with no inherited conversation.
3. Give both the same inline evidence packet and SHA-256; wrappers differ only
   by Policy A versus Policy B.
4. Require evaluation from the supplied packet only. An out-of-packet citation,
   unauthorized read, or future evidence invalidates the affected arm.
5. Send checkpoints sequentially. After `stop` or `blocked`, send no later
   checkpoint to that evaluator.
6. Preserve every return.

Each evaluator returns:

```yaml
checkpoint_id:
decision: stop | continue | blocked
permitted_claim_class: existence | recurrence_or_mechanism | prevalence_or_comparison
permitted_claim:
next_capture_job:
severe_negative_action: preserve_and_escalate | continue_investigation | none
material_uncertainty:
rationale:
```

## Success contract

No combined numeric score is permitted.

| signal | pass condition | forbidden success | evidence |
| --- | --- | --- | --- |
| Intake and anti-hindsight integrity | The forward, recency-first CSB validates and this pre-registration is committed before acquisition. | Live acquisition before the commission and policies are sealed. | Validator output, commit, chronological receipts. |
| Collector blindness | The cold collector uses only the normal contract and records a clean source-read manifest. | Collector exposure to Policy B, checkpoints, or evaluator decisions. | Dispatch, source-read manifest, authored-source references. |
| Evaluator parity and isolation | Both arms receive identical packet bytes at every shared checkpoint and no later packet after stopping. | Different evidence, future evidence, cross-arm leakage, or out-of-packet research. | SHA-256, dispatch record, complete returns. |
| Safe stop or safer claim boundary | Policy B stops safely earlier with material avoided work, or states a materially safer claim later evidence confirms. | Credit for evading or materially weakening the commissioned answer. | Stop point, later-evidence delta, claim comparison. |
| Severe-negative handling | Naturally occurring severe evidence is preserved and escalated no later under Policy B. | Severity treated as prevalence or a severe example manufactured for the test. | Observation time and arm action. |
| Claim-class discipline | Policy B never turns existence or recurrence into prevalence/comparison without sampling basis. | Comparative or prevalence meaning hidden behind qualifiers. | Packet and evaluator return. |
| Reproducibility | A cold reader can reconstruct a stop from packet, policy, remaining jobs, and route dominance/block state. | Hidden context or later evidence required. | Packet, policy, rationale. |
| Net operating value | Avoided acquisition or a materially prevented overclaim exceeds replay ceremony. | Savings produced by incomplete acquisition or weaker commissioned output. | Route/batch delta and effort record. |

## Disposition

```yaml
PROMOTE_FOR_ADVERSARIAL_REVIEW:
  requires:
    - every applicable hard success signal holds
    - no rejection condition fires
    - material operating benefit is observed
REVISE_AND_RETEST:
  when:
    - collector blocks
    - no meaningful early checkpoint exists
    - arms do not separate
    - the relevant evidence class does not occur
    - benefit does not exceed ceremony
REJECT:
  when:
    - later evidence materially reverses the Policy B claim
    - a material contradiction or mechanism is missed
    - unsupported prevalence or comparison is permitted
    - severe evidence is mishandled
    - collector or evaluator blindness is breached
    - claim inflation occurs
```

Promotion authorizes only a de-correlated adversarial review against the full
receipts. It does not authorize a Scanning, Intelligence Cycle, validator,
schema, registry, or mandatory-workflow change.

## Closeout

```yaml
closeout_state: NOT_RUN
collector_result: pending
current_policy_closure: pending
checkpoint_packets: []
policy_a_returns: []
policy_b_returns: []
later_evidence_comparison: pending
effort_comparison: pending
dogfood_disposition: pending
phase_acquisition_seal: pending
```

No acquisition or evaluator result is claimed at pre-registration.
