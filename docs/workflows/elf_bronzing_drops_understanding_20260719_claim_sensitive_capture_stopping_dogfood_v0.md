# e.l.f. Bronzing Drops Understanding Cycle — Claim-Sensitive Capture Stopping Dogfood v0

```yaml
retrieval_header_version: 1
artifact_role: Commission-local dogfood pre-registration and closeout
scope: >
  Pre-registered shadow comparison of current Scanning closure against a
  claim-sensitive capture-stopping candidate during the e.l.f. Bronzing Drops
  Understanding cycle.
use_when:
  - Executing or auditing this cycle's Acquire & Seal turn.
  - Constructing the two blinded stopping-policy replays after acquisition.
  - Deciding whether the candidate rule deserves adversarial review.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md
  - forseti/product/spines/scanning/README.md
  - forseti/product/spines/scanning/scan_core/forseti_scanning_intelligent_walk_mgt_operating_model_v0.md
branch_or_commit: 9e5050071607492ce2b50e59a00c74d7273d3a24
downstream_consumers:
  - Acquire & Seal collector
  - Policy A and Policy B cold evaluators
  - owner adjudication and, only if promoted, adversarial review
stale_if:
  - The owner changes the company, decision, cutoff rule, intended use, or claim ceiling.
  - Scanning acquisition-closure authority changes before collection begins.
  - Any evidence is acquired before this pre-registration is committed.
```

## Pre-registration state

```yaml
dogfood_id: elf_bronzing_drops_claim_sensitive_stop_20260719
cycle_id: elf_bronzing_drops_understanding_20260719
commission_id: elf_bronzing_drops_understanding_csb_20260719
canonical_phase: Understanding
turn: Acquire & Seal
state: PRE_REGISTERED_NOT_RUN
owner_acceptance:
  source: current owner task
  observed_date: 2026-07-19
  accepted_candidate: e.l.f. Cosmetics Bronzing Drops
baseline_revision: 9e5050071607492ce2b50e59a00c74d7273d3a24
comparison_claim: product_learning_only
```

This artifact is committed before external acquisition. Its first commit is
the anti-hindsight seal. Later results append to this file; they do not rewrite
the question, policies, checkpoint rule, reference horizon, or disposition
criteria below.

## Forseti start preflight

```yaml
forseti_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom
  edit_permission: implementation-authorized
  target_scope:
    - one live Understanding cycle
    - one commission-local dogfood artifact
    - normal cycle acquisition artifacts and receipts
  dirty_state_checked: yes
  blocked_if_missing:
    - owner-accepted Decision Frame
    - clean cycle worktree
    - committed pre-registration
    - current CSB, Scanning, Capture, and source-family authority
```

## Accepted Decision Frame

```yaml
subject:
  company: e.l.f. Cosmetics
  focal_intervention: Bronzing Drops launch and accessible-value positioning
decision_under_test: >
  Whether observable pre-launch community demand supported launching a bronzing
  drops product with accessible-value positioning.
owner_proxy: e.l.f. product and brand leadership
phase_question: >
  What public evidence establishes the pre-launch input, its translation into
  the Bronzing Drops launch, the mechanism-aligned post-launch response, and
  the rival explanations that bound any material-contribution inference?
intended_use: >
  First same-decision company-intelligence proving run and a shadow test of
  claim-sensitive acquisition stopping; not a recommendation, buyer decision,
  outreach plan, or generic company report.
cutoff_rule: >
  The moment immediately before the earliest first-party public launch
  announcement for Bronzing Drops. The collector must resolve and record the
  exact timestamp from first-party evidence as acquisition job R0 before
  evaluating any later evidence.
reveal_rule: >
  Evidence published after the cutoff may be used only as the post-decision
  reveal for decision translation, response, outcome, and rival assessment.
claim_ceiling: MATERIAL_CONTRIBUTION_SUPPORTED
fallback_claims:
  - INPUT_USE_ESTABLISHED
  - CONTRIBUTION_PLAUSIBLE_NOT_ESTABLISHED
hold_condition: >
  Hold if the pre-cutoff demand input, decision translation, mechanism-aligned
  response, or rival-driver assessment lacks a non-proxy evidence path strong
  enough for the claim being considered.
```

`MATERIAL_CONTRIBUTION_SUPPORTED` is a bounded causal inference, never an exact
causal-magnitude claim. The Understanding deliverable remains decision-neutral.

## Atomic information jobs and route order

The collector follows this order. A route may be skipped only with a recorded
dominance rationale; a required job may close only under current Scanning
authority. Source families are routes to evidence, never the facts themselves.

| order | ID | information job | route and authority | required result |
| ---: | --- | --- | --- | --- |
| 0 | R0 | Bind the earliest first-party public launch announcement and exact cutoff. Preserve launch wording, date/time, product, price, and named channels. | Company-owned newsroom, product, investor, and social surfaces under the Source Capture Playbook. | Direct first-party locator or a typed blocking result. No later evidence is evaluated until the cutoff is bound. |
| 1 | R1 | Establish whether attributable community demand for this intervention was observable before the cutoff. | Scanning broad scout followed by public TikTok and Reddit routes where relevant; other public community surfaces only when they perform a non-substitutable job. | Attributable pre-cutoff evidence, contradiction, or typed gap. A single instance establishes existence only. |
| 2 | R2 | Establish decision translation: product form, launch timing, accessible-value positioning, price, claims, and channel placement. | Company-owned launch/product surfaces first; then retailer PDPs named or linked by first-party evidence. Retail capture must resolve through `retail_storefront_pin_registry_v0.md`. | Direct observation, bounded inference, contradiction, or typed gap. Retail geography and availability are never inferred from hostname or USD alone. |
| 3 | R3 | Establish mechanism-aligned response after launch without converting comments or reviews into representative demand. | Retail review/PDP capture plus public TikTok/Reddit or other community evidence selected by Scanning. | Attributable response evidence with source independence and time posture preserved; prevalence remains unestablished without a defined denominator and comparable method. |
| 4 | R4 | Establish observable launch resonance and any company or partner attribution. | Company investor/newsroom material, named retailer/partner material, and independent trade/news sources. | Direct outcome evidence, attributed statement, contradiction, or typed gap; no revenue, sell-through, or causal-magnitude inference from proxy evidence. |
| 5 | R5 | Test rival contributors and disconfirming evidence: distribution, promotion, creator activity, novelty, availability, seasonality, existing brand strength, and unrelated portfolio effects. | Targeted first-party, retailer, creator/social, search/discovery, and independent trade routes chosen for the named rival. | Each material rival supported, contradicted, or honestly held as a gap. |
| 6 | R6 | Check whether another non-dominated acquisition path could still change the permitted claim, material qualification, rival assessment, or hold state. | Current Scanning closure authority. | Current-policy closure or visible blocked/incomplete state. |

Route-specific boundaries:

- TikTok capture opens
  `forseti/product/spines/capture/core/source_families/social_media/tiktok/README.md`
  and its lane spec. A new subject has no inherited live-capture success.
- Reddit capture opens
  `forseti/product/spines/capture/core/source_capture_toolbox/reddit_capture_operator_playbook_v0.md`.
- Retail capture opens
  `forseti/product/spines/capture/core/source_families/retail_pdp/retail_storefront_pin_registry_v0.md`.
  Ulta is currently unpinned and may not be presented as US-pinned; use requires
  the canonical source-specific route and a fresh supported result. Silent
  substitution is prohibited.
- All source access stays inside the current Source Capture Playbook and
  source-access boundary. A safety, access, budget, or policy stop is a visible
  gap or block, not acquisition closure.

## Reference horizon

The real collector runs only under current Scanning closure:

> Continue while the best remaining non-dominated move has a credible chance of
> changing the action, claim ceiling, rival assessment, material qualification,
> or hold condition enough to justify marginal cost, latency, access risk, and
> duplication.

The reference horizon is the evidence actually captured before that current
policy reaches closure. It is a fuller observed comparison set, not ground
truth. The collector does not extend acquisition to improve the dogfood and
does not see either evaluator's decisions.

If acquisition stops on a cap, safety boundary, access failure, or unresolved
required route while a material path remains, the cycle and dogfood are
`INCONCLUSIVE_CAPTURE_BLOCKED`.

## Pre-registered checkpoints

Checkpoints are generated only at these natural boundaries:

| checkpoint | trigger |
| --- | --- |
| CP0 | R0 cutoff and first-party launch record bound |
| CP1 | R1 pre-cutoff community-demand acquisition closed or visibly blocked |
| CP2 | R2 decision-translation acquisition closed or visibly blocked |
| CP3 | R3 mechanism-aligned response acquisition closed or visibly blocked |
| CP4 | R4 outcome/attribution acquisition closed or visibly blocked |
| CP5 | R5 rival and contradiction checks complete; R6 current-policy closure assessed |

Each replay packet contains only receipts and observations available through
that boundary. The coordinator records its locator, SHA-256, included receipt
IDs, and included observation IDs. Both arms receive byte-identical packets.
Checkpoint order and inclusion may not be changed after evidence is seen.

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
   load-bearing owner-unblock escalation. It never establishes
   representativeness by severity alone.
5. Stop only when further plausible capture would not change the permitted
   claim and the remaining paths are blocked or dominated.

## Cold evaluator protocol

After the collector completes or visibly blocks:

1. Spawn two fresh same-family evaluators with no inherited conversation.
2. Give both the same bounded source capsule, evaluator contract, and CP0 packet.
   The sole experimental difference is Policy A versus Policy B.
3. If an evaluator returns `continue`, send the next checkpoint using the same
   agent. If it returns `stop` or `blocked`, send no later packet.
4. Evaluators never see each other, later packets, the final evidence set,
   historical e.l.f. conclusions, or the comparison result.
5. The coordinator preserves every return. No output is dropped because it is
   awkward, repetitive, or unfavorable.

Each return must use:

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

| signal | given | when | then | forbidden success | evidence |
| --- | --- | --- | --- | --- | --- |
| Input parity and blindness | Two cold same-family evaluators and one ordered checkpoint series | replay begins | both receive byte-identical evidence packets and neither sees later evidence or the other arm | comparing arms that saw different evidence or leaked future observations | packet hashes, dispatch prompts, full arm returns |
| Safe stopping or safer claim boundary | Policy B reaches a stop before current-policy closure or applies a materially safer permitted claim | later captured evidence is revealed | the later set does not materially reverse the claim, expose a missed contradiction, or change the supported mechanism | credit for merely weakening or evading the commissioned answer | stop checkpoint, later-evidence delta, claim comparison |
| Severe-negative handling | A severe attributable negative appears naturally | each policy encounters it | Policy B preserves and escalates no later than Policy A while keeping representativeness separate | treating severity as prevalence or inventing a severe example | timestamped observation and arm action |
| Claim-class discipline | Evidence supports existence or recurrence without a defensible denominator/comparator | evaluator states the permitted claim | Policy B does not state prevalence, concentration, rate, or comparison | qualifier wording that still performs the prohibited comparative claim | packet evidence and evaluator return |
| Reproducibility | An evaluator records a stop | a cold reader receives the same packet and policy | the stop rationale resolves to visible facts, remaining jobs, and dominance/block state | rationale dependent on hidden context or later evidence | replay packet, policy, rationale |
| Net operating value | A safe earlier stop or material overclaim prevention occurs | acquisition and evaluation effort are compared | the avoided acquisition or prevented defect materially exceeds the added replay ceremony | counting work saved by an incomplete or weaker answer | route/batch delta and evaluator/coordinator effort record |

Wrong-cause controls:

- A later material reversal, missed contradiction, missed mechanism, delayed
  severe-evidence action, or unsupported prevalence/comparison is `REJECT`.
- A blocked collector, no meaningful pre-closure checkpoint, no arm separation,
  absent natural evidence class, or benefit smaller than ceremony is
  `REVISE_AND_RETEST` / inconclusive, never a pass.
- No severe, mild, comparative, or contradictory example is manufactured.
- One run is product-learning evidence only and never universal validation.

## Pre-registered disposition

```yaml
PROMOTE_FOR_ADVERSARIAL_REVIEW:
  requires:
    - every applicable hard success signal holds
    - no rejection condition fires
    - material operating benefit is observed
REVISE_AND_RETEST:
  when:
    - no safety failure occurs
    - benefit, separation, or a relevant natural evidence class is inconclusive
REJECT:
  when:
    - any material miss, reversal, claim inflation, blindness breach, or severe-evidence handling failure occurs
```

Promotion authorizes only a de-correlated adversarial review of this artifact
and its full receipts. It does not authorize a Scanning, Intelligence Cycle,
validator, schema, registry, or mandatory-workflow change.

## Closeout — intentionally empty before acquisition

```yaml
collector_result: NOT_RUN
current_policy_closure: NOT_RUN
checkpoint_packets: []
policy_a_returns: []
policy_b_returns: []
later_evidence_comparison: NOT_RUN
effort_comparison: NOT_RUN
dogfood_disposition: NOT_RUN
```
