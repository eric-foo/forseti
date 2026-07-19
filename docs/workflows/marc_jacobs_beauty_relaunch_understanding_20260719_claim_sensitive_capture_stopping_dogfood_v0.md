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
closeout_date: "2026-07-19"
closeout_state: COMPLETE
collector_result: SEALED_COMPLETE_WITH_ACCEPTED_RESIDUALS
collector_base_commit: ead7e5f398667e0bf1ee033e8494bd0a19bc8113
collector_blindness: OPERATIONAL_PASS
current_policy_closure:
  checkpoint_id: CP4
  method: expected_decision_value_stop
  result: closed
checkpoint_packets:
  - checkpoint_id: CP0
    path: docs/review-inputs/marc_jacobs_beauty_relaunch_claim_sensitive_stop_20260719/cp0.md
    sha256: 12374C51610E779649CE75C3035339A8C2CA785C4D8EEDA5D44E7A0078131E44
    included_observation_ids: [OBS-001]
    included_receipt_ids: [CAP-R0-001]
  - checkpoint_id: CP1
    path: docs/review-inputs/marc_jacobs_beauty_relaunch_claim_sensitive_stop_20260719/cp1.md
    sha256: F9230F022DD08C827E8011A6306D65E95AB4EF8826533A4348C8A406374407B9
    included_observation_ids: [OBS-001, OBS-002]
    included_receipt_ids: [CAP-R0-001, CAP-R1-001, CAP-R1-002]
  - checkpoint_id: CP2
    path: docs/review-inputs/marc_jacobs_beauty_relaunch_claim_sensitive_stop_20260719/cp2.md
    sha256: DF0AB359B54FD0EC99EFB6893A5C534BC685B090562B9B1EBDBF16DFC9BCCB0C
    included_observation_ids: [OBS-001, OBS-002, OBS-003, OBS-004, OBS-005]
    included_receipt_ids: [CAP-R0-001, CAP-R1-001, CAP-R1-002, CAP-R2-001, CAP-R2-002, CAP-R2-003]
  - checkpoint_id: CP3
    path: docs/review-inputs/marc_jacobs_beauty_relaunch_claim_sensitive_stop_20260719/cp3.md
    sha256: E4C414700261D6146E3C51E91A6AE5BE29676A87905D888DAF000E8BEC608B02
    included_observation_ids: [OBS-001, OBS-002, OBS-003, OBS-004, OBS-005, OBS-006, OBS-007, OBS-008]
    included_receipt_ids: [CAP-R0-001, CAP-R1-001, CAP-R1-002, CAP-R2-001, CAP-R2-002, CAP-R2-003, CAP-R3-BATCH]
  - checkpoint_id: CP4
    path: docs/review-inputs/marc_jacobs_beauty_relaunch_claim_sensitive_stop_20260719/cp4.md
    sha256: FFF8C984C1C6965AF143BEEACFC7F082000F6FCADF908A654F7138EEFD54BF4E
    included_observation_ids: [OBS-001, OBS-002, OBS-003, OBS-004, OBS-005, OBS-006, OBS-007, OBS-008, OBS-009]
    included_receipt_ids: [CAP-R0-001, CAP-R1-001, CAP-R1-002, CAP-R2-001, CAP-R2-002, CAP-R2-003, CAP-R3-BATCH]
policy_a_stop: CP4
policy_b_stop: CP4
arm_separation: none
later_evidence_comparison:
  state: no_post_stop_evidence
  reason: Policy B stopped only at the final CP4 packet and therefore avoided no later acquisition.
effort_comparison:
  evaluator_returns: 10
  checkpoints_per_arm: 5
  acquisition_avoided_by_policy_b: none
  material_overclaim_prevented_relative_to_policy_a: none
  net_operating_value: negative_added_replay_ceremony_without_observed_benefit
capture_root_closeout:
  recorded_locator_prefix: .acquisition/
  acquisition_time_root: C:\tmp\forseti-marc-jacobs-stopping-dogfood\.acquisition
  current_bound_root: C:\tmp\forseti-marc-jacobs-stopping-dogfood\_acquisition
  move_timing: after_collection_and_evaluator_replay
  preserved_file_count: 78
  packet_manifest_count: 15
  packet_ids_unchanged: true
  checkpoint_bytes_changed: false
  placement_effect: worktree_scratch_excluded_from_repo_artifacts
dogfood_disposition: REVISE_AND_RETEST
phase_acquisition_seal:
  path: docs/workflows/forseti_beauty_marc_jacobs_beauty_relaunch_understanding_acquisition_seal_v0.md
  seal_state: ACQUISITION_COMPLETE_WITH_ACCEPTED_RESIDUALS
  acquisition_gate: passed
  deliver_allowed: true
next_cycle_state: READY_FOR_DELIVER_IN_SEPARATE_FRESH_CONTEXT
```

## Decisive failure-scenario verification

| Scenario | Pre-registered result | Closeout check |
|---|---|---|
| Acquisition blocks before current-policy closure | `REVISE_AND_RETEST` | Rule resolves without promotion; not triggered in this run. |
| Arms do not separate | `REVISE_AND_RETEST` when no material safety benefit exists | Triggered; the observed disposition is `REVISE_AND_RETEST`. |
| Later evidence reverses the Policy B claim or changes its asserted mechanism | `REJECT` | Rule resolves to rejection; no post-stop evidence existed in this run. |
| An arm permits prevalence or comparison without a defined sample, denominator, and comparable method | `REJECT` | Rule resolves to rejection; neither arm crossed this boundary. |
| Policy B preserves or escalates severe negative evidence later than Policy A, or treats it as representative | `REJECT` | Rule resolves to rejection; no severe negative naturally occurred. |
| Collector or evaluator receives forbidden policy, future evidence, cross-arm evidence, or uses out-of-packet material | `REJECT` | Rule resolves to rejection; no leakage was observed under the operational-blindness limit below. |

## Blindness and parity record

```yaml
collector:
  task: collect_marc_jacobs_cycle
  fork_turns: none
  policy_received: current production closure only
  source_read_manifest_returned: true
  forbidden_path_exposure: >
    The commission board exposed the dogfood filename as an open_next pointer;
    the collector reported that it did not follow, search, or open that path.
  out_of_policy_evidence: none_observed
evaluators:
  policy_a_task: evaluate_policy_a
  policy_b_task: evaluate_policy_b
  fork_turns: none
  same_runtime: true
  packet_delivery: inline_only
  filesystem_or_web_authority: prohibited
  out_of_packet_citations: none_observed
  cross_arm_visibility: none
  future_packet_after_stop: none
blindness_limit: >
  Operational rather than filesystem-enforced; a shared worktree means the
  absence of exposure is supported by bounded dispatches and returned behavior,
  not an OS access-control boundary.
```

Both arms received the same packet hash at every shared checkpoint. Their
wrappers differed only by the bound policy. No arm stopped before CP4, so both
received CP0 through CP4 and no post-stop dispatch occurred.

## Policy A returns

```yaml
checkpoint_id: CP0
decision: continue
permitted_claim_class: existence
permitted_claim: As of 2026-05-20, Coty publicly framed the Marc Jacobs Beauty relaunch around Joyride Sensoriality and bold self-expression, with a named seven-product opening assortment, stated US prices of $26–$42, tactile packaging, and staged distribution.
next_capture_job: R1 — capture current owned assortment, product claims, packaging, textures, and experience language.
severe_negative_action: none
material_uncertainty: Retail translation, current owned product-level expression, early user experience, independent corroboration, contradictions, prevalence, representative demand, and local availability remain unestablished.
rationale: The single first-party observation supports only attributable existence claims and leaves R1–R5 as distinct non-duplicative paths with plausible decision value.
```

```yaml
checkpoint_id: CP1
decision: continue
permitted_claim_class: existence
permitted_claim: Current Marc Jacobs-owned surfaces express the relaunched proposition through a seven-product assortment, shade breadth, packaging and texture language, and product-specific long-wear or experience claims.
next_capture_job: R2 — capture Sephora presentation and dated product-review evidence.
severe_negative_action: none
material_uncertainty: Exact PDP fidelity is access-limited; retail translation, dated experience, independent testing, contradictions, syndication, recurrence, and prevalence remain unestablished.
rationale: R2 is a distinct high-value route because it directly addresses retail translation and early experience.
```

```yaml
checkpoint_id: CP2
decision: continue
permitted_claim_class: existence
permitted_claim: Sephora translates the owned proposition through maximalist, playful, multi-use, and long-wearing language; dated review rows provide attributable examples of alignment and conflicts involving wear duration, shade representation, packaging, creasing, pigment, breakage, and value.
next_capture_job: R3 — run the bounded Reddit scout and preserve selected community threads.
severe_negative_action: continue_investigation
material_uncertainty: Review rows establish examples only, not recurrence, mechanism, defect rates, prevalence, or comparative performance; review incentives, delivery location, and local stock remain unresolved.
rationale: R3 could independently corroborate, contradict, or explain the retailer-hosted observations.
```

```yaml
checkpoint_id: CP3
decision: continue
permitted_claim_class: recurrence_or_mechanism
permitted_claim: Within the bounded retailer and selected-community evidence, short blush wear, packaging hand-feel concerns, and product- or shade-specific performance conflicts recur across multiple attributable observations; this recurrence does not establish prevalence, defect rates, or line-wide performance.
next_capture_job: R4 — capture independent hands-on sources and trace launch-copy syndication.
severe_negative_action: none
material_uncertainty: Independent corroboration is absent; the sample has no denominator, syndication may mimic corroboration, mechanisms remain unproven, and the formula/manufacturer inference is unverified.
rationale: R4 could materially confirm, contradict, or reclassify the recurring patterns and distinguish original testing from syndicated language.
```

```yaml
checkpoint_id: CP4
decision: stop
permitted_claim_class: recurrence_or_mechanism
permitted_claim: Current public evidence shows a coherent maximalist, sensorial, tactile proposition across Coty, Marc Jacobs, and Sephora; bounded external evidence aligns on some product- and shade-specific texture, blendability, and durability experiences while independently and repeatedly conflicting on blush wear, packaging hand-feel, shade representation, eyeliner performance, Heart On longevity or taste, and Money Shot condition or texture.
next_capture_job: none
severe_negative_action: none
material_uncertainty: Exact owned PDP preservation is partial; Sephora delivery and local stock are unpinned; early external experience is nonrepresentative; formula equivalence is unverified; prevalence, defect rates, representative demand, and uniform line-wide performance remain unsupported.
rationale: All commissioned requirements are answered or typed as gaps, and no remaining path has expected decision value above its cost and duplication.
```

## Policy B returns

```yaml
checkpoint_id: CP0
decision: continue
permitted_claim_class: existence
permitted_claim: Coty publicly framed the Marc Jacobs Beauty relaunch around Joyride Sensoriality and bold self-expression, with a named seven-product opening assortment, stated US pricing, tactile packaging, partnership attribution, and staged distribution.
next_capture_job: R1 — capture current owned assortment, product claims, packaging, textures, and experience language.
severe_negative_action: none
material_uncertainty: The packet contains one attributable first-party instance; retail translation, experience, independent corroboration, recurrence, mechanism, prevalence, comparison, and local availability remain unestablished.
rationale: R1 can materially confirm or contradict expression of the launch proposition across owned surfaces.
```

```yaml
checkpoint_id: CP1
decision: continue
permitted_claim_class: existence
permitted_claim: Current Coty and Marc Jacobs first-party surfaces express a seven-product relaunch proposition involving sensoriality, self-expression, shade breadth, tactile packaging, textures, and product-specific long-wear or experience claims.
next_capture_job: R2 — capture Sephora retail presentation and dated product-review evidence.
severe_negative_action: none
material_uncertainty: The evidence remains first-party and does not independently establish recurrence, mechanism, performance, customer experience, prevalence, comparison, or exact Joystick PDP fidelity.
rationale: R2 can test external retail translation and introduce dated user-experience evidence; another exact owned-PDP attempt is lower value.
```

```yaml
checkpoint_id: CP2
decision: continue
permitted_claim_class: existence
permitted_claim: Sephora currently translates the relaunch with maximalist, playful, upgraded, multi-use, and long-wearing language, while attributable dated review rows contain favorable reports and specific counterexamples involving shorter wear, shade mismatch, packaging, breakage, creasing, pigment, and value.
next_capture_job: R3 — capture bounded independent community threads.
severe_negative_action: none
material_uncertainty: Retail copy may be brand-supplied; delivery and local stock are unpinned; reviewer examples do not establish recurrence, mechanism, defect rates, prevalence, concentration, or comparison.
rationale: R3 could corroborate, qualify, or contradict the retailer-hosted examples; current evidence permits existence claims only.
```

```yaml
checkpoint_id: CP3
decision: continue
permitted_claim_class: recurrence_or_mechanism
permitted_claim: Across the bounded retailer-review and community evidence, short blush wear, packaging hand-feel concerns, and product- or shade-specific performance conflicts recur; multiple attributable users also report Money Shot arriving dried, shrunken, tiny, patchy, or goopy. These are bounded repeated observations, not prevalence or defect-rate findings.
next_capture_job: R4 — capture independent hands-on sources and trace launch-copy syndication.
severe_negative_action: none
material_uncertainty: The evidence has no denominator and does not establish prevalence, concentration, defect rates, line-wide comparison, or causal mechanism; the formula/manufacturer inference remains unverified.
rationale: Independent hands-on evidence could materially strengthen, narrow, or overturn the recurrence claim and distinguish corroboration from copied launch language.
```

```yaml
checkpoint_id: CP4
decision: stop
permitted_claim_class: recurrence_or_mechanism
permitted_claim: Current public evidence shows a coherent maximalist, sensorial, tactile proposition across Coty, Marc Jacobs, and Sephora surfaces. Independent external evidence supports some product- and shade-specific alignment on texture, blendability, and durability, while independently and repeatedly showing conflicts involving blush wear, packaging hand-feel, shade representation, eyeliner performance, Heart On longevity or taste, and Money Shot condition or texture. No uniform line-wide performance, prevalence, defect-rate, representative-demand, delivery, or local-stock claim is supported.
next_capture_job: none
severe_negative_action: none
material_uncertainty: Exact owned PDP preservation remains partial; Sephora delivery and local availability remain unpinned; early external experience is nonrepresentative; product, shade, tester, and method dependence remain material; the formula-equivalence inference is unverified and excluded.
rationale: All commissioned jobs are complete, independent sources corroborate and qualify the bounded recurrence findings, and remaining paths are blocked, dominated, or lack unique decision value.
```

## Comparison and disposition

The arms did not separate. Both continued at CP0, CP1, CP2, and CP3, then
stopped at CP4. Both moved from existence to a bounded recurrence claim at CP3
and preserved the same no-prevalence boundary. Their CP4 claims are materially
equivalent.

Policy A used `continue_investigation` at CP2 despite the packet explicitly
stating that no severe negative had appeared; Policy B used `none`. This is a
minor field-choice difference, not a stopping, claim-safety, or
severity-handling benefit because the evidence was material but non-severe.

No later evidence existed after Policy B's stop. Policy B avoided no route or
batch, prevented no material overclaim relative to Policy A, and added five
evaluation decisions. The net operating value condition therefore fails.

Disposition: `REVISE_AND_RETEST`.

The normal acquisition seal remains independent and passing. This dogfood does
not receive adversarial review and changes no production contract. The next
authorized cycle act is a separately commissioned, fresh-context Understanding
Deliver turn.
