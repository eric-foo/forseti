# Engagement Logic Registry v0

```yaml
retrieval_header_version: 1
artifact_role: Product artifact
scope: Core Spine engagement interpretation and cross-layer public-reaction engagement handling.
use_when:
  - Interpreting public engagement signals as qualitative resonance weight without collapsing them into a demand score.
  - Checking how Capture, Projection, Cleaning, Data Lake, and Judgment should handle source-visible engagement facts.
  - Preventing public-reaction counts from becoming demand proof, credibility, or Action Ceiling by shortcut.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/foundation/product_contract/core_spine_v0_information_production_foundation_v0.md
  - forseti/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md
stale_if:
  - Judgment ownership of Signal Integrity, Signal Use, Decision Strength, or Action Ceiling changes.
  - Cleaning gains a persisted engagement-context schema or Data Lake writer.
  - The owner authorizes numeric engagement weighting or a scoring engine.
```

- Status: PROPOSED_FREEZE
- Artifact type: Product artifact
- Scope: Core Spine engagement interpretation skeleton
- Source basis: current owner direction, `docs/decisions/turn_08_product_thesis_v0.md`, `forseti/product/README.md`
- Implementation authorized: no

## Purpose

This registry defines how Forseti interprets public engagement signals without
collapsing them into a single demand score.

Core rule:

> Source-visible public engagement should be treated as qualitative resonance
> weight by default, attached to the specific claim, frame, pain, objection, or
> artifact receiving the engagement. Direction, audience fit, baseline context,
> manipulation risk, and ambiguity decide how much weight it carries.

Do not ask only whether the signal is real demand. No engagement pattern is
automatically demand, and no noisy pattern is automatically worthless.

## Product Boundary

The registry is a judgment artifact, not an implementation design. It does not
authorize scrapers, bot detection systems, data pipelines, dashboards, scoring
engines, or automation.

Use it to classify and reason about evidence in decision memos (Memo), backtests (Case),
competitive intelligence, source-quality review, and satellite proof plans.

## Public Reaction Engagement Rule

Public-reaction engagement means source-visible reaction facts such as upvotes,
helpful votes, likes, views, shares, comment counts, reply counts, source-native
scores, pinned/hearted/official-response markers, visible sort order, and
source-exposed ranking or recency posture.

Forseti must preserve those facts when they are visible and relevant to a public
reaction source. They can change what a later operator should inspect: a
23-upvote detailed objection is not the same signal surface as a 0-upvote
drive-by objection. That difference should be interpreted as resonance context:
not automatic truth, but not merely a neutral attention sticker.

Layer split:

- Capture preserves route-visible public-reaction facts, source order, timing,
  hierarchy, and missingness when the source exposes them.
- Projection may carry those facts into mechanical rows with raw anchors and
  loss/residual notes; it must not create demand, credibility, or action labels.
- Cleaning may produce an `engagement_context` working view that makes the
  reaction structure inspectable: high-engagement units, low-engagement repeated
  units, disagreement/counter-units, source order, metric posture, residuals,
  and raw-pull triggers.
- Data Lake stores raw engagement facts as Bronze and mechanical
  `engagement_context` outputs as Silver when Cleaning lake wiring exists.
- Judgment alone decides what the engagement context means for Signal
  Integrity, Signal Use, Decision Strength, Action Ceiling, demand support,
  credibility, independence, artificial amplification, or exclusion.

Non-claims:

- Engagement context is not proof or a numeric score boost, but source-visible
  public reaction should be seen as qualitative resonance weight unless
  discounted by direction, audience-fit weakness, source baseline, manipulation
  risk, or ambiguity.
- High engagement does not prove demand, credibility, independence, buyer pull,
  or willingness to pay.
- Low or missing engagement does not make a signal worthless by default.
- No public-reaction engagement pattern clears Commit, Scale, buyer proof, or a
  demand gate without separate costly behavior, audience fit, independence, and
  counterevidence review under the owning Judgment or proof contract.
## Core Spine Relationship

This registry is a rubric for Core Spine primitives, not a separate product
surface.

| Registry concern | Core Spine primitive |
| --- | --- |
| Pattern, source, and timestamp | Evidence Unit (EvidenceUnit) |
| Incentives, copied language, bot-like activity, and manipulation risk | Signal Integrity |
| Strong for, weak for, and decision use | Signal Use Classification |
| Corroboration, discount factors, audience fit, costly behavior, and action implication | Decision Strength |
| Backtest interpretation and later outcome (Outcome) | Backtesting and Outcome Memory |

## Engagement Pattern Schema

Each engagement pattern should be captured with these fields:

| Field | Meaning |
| --- | --- |
| Pattern | What was observed. |
| Strong for | What the signal can support. |
| Weak for | What the signal should not prove by itself. |
| Possible meanings | Competing interpretations. |
| Corroboration needed | What would upgrade confidence. |
| Discount factors | What reduces weight. |
| Decision use | Recommendation verbs this signal may affect. |

Every captured pattern should preserve the `resonance_direction`
(`positive`, `negative`, `mixed`, or `unclear`), a visible-context
`audience_fit` read (`high`, `medium`, `low`, or `unknown`), and the available
baseline context (`above_typical`, `typical`, `below_typical`, or `unknown`)
when those facts are source-visible or mechanically derivable. These are
qualitative judgment aids, not a scoring schema.

## Initial Pattern Registry

| Pattern | Strong for | Weak for | Corroboration needed | Discount factors | Decision use |
| --- | --- | --- | --- | --- | --- |
| Reward-driven comments | Campaign mechanics, incentive design, competitor channel testing, audience responsiveness | Organic demand, willingness to pay | Non-incentivized repeats, downstream clicks, search lift, detailed discussion, costly behavior | Giveaway prompt, low-detail comments, same wording, low-history accounts | Monitor, test channel, discount demand claim |
| Affiliate push | Distribution strategy, creator economics, acquisition motion, competitor priorities | Unbiased advocacy, product-market pull | Non-affiliate mentions, buyer-side discussion, conversion hints, persistent independent demand | Disclosure gaps, commission incentives, copied talking points | Monitor competitor, test channel, discount advocacy |
| Like or comment spike | Attention, timing, reach, content resonance | Purchase intent, durable demand | Detailed comments, search lift, follow-on discussion, repeat exposure, costly behavior | Paid boost, creator prompt, trend timing, low audience fit | Monitor, test message, investigate |
| Burst after creator or brand prompt | Mobilization capacity, audience responsiveness, campaign mechanics | Independent market pull | Persistence after burst, independent reposts, cross-channel discussion, buyer-visible repeats | Prompt dependency, short half-life, reward framing | Monitor, test campaign, discount demand |
| Praise comments | Positioning resonance, emotional language, perceived benefit, social proof | Deep pain, willingness to pay, switching intent | Specific reasons, comparisons, repeat use, objections, costly behavior | Generic praise, parasocial dynamics, fan community, incentive context | Test message, harvest language, investigate |
| High comments with low detail | Attention, social proof, curiosity, controversy | Strong demand, precise buyer pain | Detailed objections, questions, use cases, external repeats, behavior after attention | Meme dynamics, low-effort replies, prompt farming | Monitor, investigate, discount demand |
| Copied phrase | Message propagation, meme spread, campaign coordination, narrative pollution | Independent demand | Original source mapping, varied phrasing, unrelated-source repeats, target-audience use | Syndication, templated comments, affiliate scripts, SEO copying | Monitor narrative, discount independence |
| Bot-like activity | Manipulation risk, artificial amplification, competitor tactics, evidence pollution | Customer pull, buyer belief by itself | Account history, timing clusters, cross-source comparison, downstream organic discussion | Thin accounts, identical timing, unnatural ratios, irrelevant audience | Discount signal, flag risk, investigate competitor |
| Negative complaint cluster | Objection evidence, unmet need, switching risk, product gap | Market size, WTP by itself | Repeated independent complaints, detailed stakes, workarounds, churn or switching evidence | Review bombing, competitor seeding, single incident, copied complaint | Test, reposition, fix, monitor |
| Question-heavy discussion | Curiosity, confusion, onboarding friction, latent demand | Purchase readiness by itself | Repeat questions from target audience, follow-up action, comparison behavior | Low-intent audience, novelty, unclear source context | Clarify positioning, test offer, monitor |
| Workaround sharing | Costly behavior, unmet need, workflow pull | Broad market demand by itself | Multiple independent workarounds, repeated pain, adoption of workaround, buyer fit | Hobbyist-only context, edge cases, stale examples | Test, invest, reposition |
| Competitor campaign repetition | Competitor intent, positioning test, distribution focus, narrative strategy | Customer demand by itself | Landing page changes, ad copy, creator mix, audience response, independent pickup | Coordinated paid push, low engagement quality, affiliate distortion | Competitive response, monitor, defend |

## Engagement Quality Ladder

Engagement is not a single linear score. These levels describe what an observed
signal may support. The ladder is a judgment rubric, not a core primitive and
not a scoring engine.

| Level | Name | Question |
| --- | --- | --- |
| 1 | Visibility | Did the signal exist and become visible to a relevant audience or analyst before the decision date? |
| 2 | Attention | Did people notice, click, like, comment, watch, share, or discuss it? |
| 3 | Resonance direction | Is the visible reaction positive, negative, mixed, or unclear toward the specific claim, frame, pain, objection, or artifact? |
| 4 | Interpretive detail | Did people explain why they care, what they compare it to, or what problem it touches? |
| 5 | Independent repetition | Does similar meaning appear across unrelated sources rather than copied phrasing? |
| 6 | Audience fit | Do the reacting sources match the buyer, user, influencer, competitor, or market observer relevant to the decision? |
| 7 | Baseline context | Is the reaction above, typical, or below the source object's normal engagement pattern? |
| 8 | Persistence | Does the signal survive beyond a burst, launch, giveaway, paid push, or trend cycle? |
| 9 | Costly behavior | Do people spend money, switch, apply, build workarounds, complain with stakes, churn, waitlist, create content, or commit time? |
| 10 | Decision pressure | Is the signal strong enough to justify monitor, test, delay, kill, reposition, defend, or invest? |

## Signal Use Classification

Every engagement signal should be classified by decision use:

- demand evidence;
- attention evidence;
- resonance evidence;
- resonance-direction evidence;
- positioning evidence;
- objection evidence;
- competitor-strategy evidence;
- distribution evidence;
- manipulation-risk evidence;
- social-proof evidence;
- buyer-belief evidence;
- weak or noisy evidence;
- exclusion evidence.

The same signal may support several uses with different confidence levels.

## Required Splits

Forseti must keep these distinctions visible:

- attention versus demand;
- repeated language versus independent demand;
- artificial amplification versus useless evidence;
- competitor intent versus buyer pull;
- buyer-visible belief versus analyst-discoverable intelligence;
- praise versus willingness to pay;
- campaign success versus product truth;
- marketing demo value versus internal product evidence.

## Backtesting Use

Backtests should use this registry to ask whether the engagement interpretation
would have helped before the outcome was known.

Internal backtests must freeze the evidence window before the outcome date and
separate pre-window evidence from post-window knowledge. Marketing demos may
use cherry-picked cases, but those cases must not train the internal evidence
standard unless they pass leakage controls.

## Open Questions

- Exact confidence vocabulary: UNKNOWN - requires owner input.
- Exact qualitative resonance-weight method beyond the default qualifiers:
  UNKNOWN - requires owner input.
- Exact backtest case-selection policy: UNKNOWN - requires owner input.
- Exact satellite-specific engagement patterns: UNKNOWN - requires owner input.
## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Public-reaction engagement is now interpreted as qualitative resonance weight
    by default, attached to the specific claim/frame/pain/objection/artifact that
    received the reaction. Direction, visible audience fit, source baseline,
    manipulation risk, and ambiguity shape or discount that weight. This remains
    below proof: engagement/resonance alone does not prove demand, credibility,
    independence, buyer pull, costly behavior, buyer proof, Commit/Scale, graph
    weight, or Action Ceiling.
  trigger: product_doctrine
  related_triggers:
    - architecture_doctrine
    - workflow_authority
  reviewed_by: >
    Cross-vendor delegated adversarial artifact review
    docs/review-outputs/adversarial-artifact-reviews/engagement_resonance_weight_propagation_delegated_adversarial_artifact_review_patch_v0.md.
    Home-model adjudication accepted/applied AR-01 (restatement
    desynchronization) and AR-02 (archive-pointer receipt hygiene); no
    critical/major findings.
  controlling_sources_updated:
    - forseti/product/shared/engagement_registry/engagement_logic_registry_v0.md
    - forseti/product/spines/foundation/product_contract/core_spine_v0_information_production_foundation_v0.md
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md
    - docs/decisions/cleaning_spine_data_lake_representation_defer_v0.md
    - forseti/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md
    - forseti/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_readme_v0.md
    - forseti/product/spines/cleaning/contracts/core_spine_v0_corroboration_vs_amplification_discipline_v0.md
    - forseti/product/spines/commission_signal_board/prompts/forseti_commission_signal_board_prompt_structure_v0.md
    - forseti/product/spines/commission_signal_board/authority/forseti_commission_signal_board_prompt_structure_rules_v0.md
    - forseti/product/spines/commission_signal_board/dispatch_rules/forseti_demand_gate_run_commission_criteria_v0.md
    - forseti/product/spines/scanning/README.md
    - forseti/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md
    - forseti/product/spines/scanning/scan_core/orca_demand_scan_core_spec_v0.md
    - forseti/product/spines/foundation/demand_read_taxonomy/forseti_demand_read_taxonomy_v0.md
    - forseti/product/spines/foundation/demand_read_taxonomy/forseti_demand_read_taxonomy_adjudication_v0.md
    - forseti/product/spines/judgment/demand_read/core/judgment_spine_demand_read_machinery_architecture_v0.md
    - forseti/product/spines/judgment/demand_read/c3_verdict_action/judgment_spine_c3_verdict_action_ceiling_contract_v0.md
    - forseti/product/spines/judgment/demand_read/grading/judgment_spine_demand_read_grading_rubric_v0.md
    - forseti/product/spines/judgment/demand_read/integrity/judgment_spine_manufactured_demand_detection_design_v0.md
    - forseti/product/spines/judgment/demand_read/core/judgment_spine_first_demand_read_scope_v0.md
    - forseti/product/spines/product_lead/buyer_proof/forseti_buyer_proof_packet_v0.md
    - forseti/product/spines/product_lead/proof_charter/forseti_product_proof_lead_charter_v0.md
    - forseti/product/spines/product_lead/offer/forseti_offer_hypothesis_v0.md
    - docs/decisions/forseti_product_thesis_consumer_demand_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/validation-gates.md
    - .agents/workflow-overlay/artifact-roles.md
    - .agents/workflow-overlay/retrieval-metadata.md
    - .agents/workflow-overlay/review-lanes.md
  intentionally_not_updated:
    - path: orca-harness/
      reason: >
        This is doctrine propagation only. It does not authorize runtime
        Cleaning, lake writers, crawlers, scoring engines, dashboards, or
        enforcement code.
    - path: forseti/product/spines/capture/core/source_families/
      reason: >
        Source-family playbooks preserve visible metrics and source context. The
        stale-language sweep found no live contradiction requiring broad edits;
        interpretation remains owned by the engagement registry and downstream
        Judgment/Product Lead surfaces.
    - path: docs/prompts/reviews/ and docs/review-outputs/
      reason: >
        Historical prompts and review outputs are point-in-time records. They
        were not rewritten unless they become active reusable templates in a
        later prompt/review lane.
  stale_language_search: >
    rg -i -n "Engagement context is not a score boost|attention and routing cue|weak/attention-only|attention-only input|engagement-only cap|engagement volume alone|engagement-only memo|attention-only evidence|engagement-only evidence|engagement-only cannot|engagement-only signal|attention/engagement volume alone|attention/engagement volume standing alone|convergence asserted on engagement volume|engagement-only caps"
    orca/product docs/decisions -g "*.md"
  stale_language_search_result: >
    Executed during this patch after propagation. The only hit was this receipt's
    own stale_language_search query line. No live doctrine prose in orca/product
    or docs/decisions retained the searched stale phrases. Historical
    prompt/review artifacts were intentionally excluded from the live
    stale-language sweep.
  non_claims:
    - not validation
    - not readiness
    - not buyer proof
    - not demand proof
    - not a numeric score or scoring engine
    - not runtime implementation or enforcement
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    Public-reaction engagement facts now have a cross-layer handling rule:
    Capture preserves visible metrics/context, Projection may carry mechanical
    rows, owner-authorized Cleaning may produce mechanical engagement_context,
    Data Lake places raw facts in Bronze and mechanical context in Silver, and
    Judgment alone interprets meaning or action effect.
  trigger: product_doctrine
  related_triggers:
    - architecture_doctrine
    - workflow_authority
  reviewed_by: >
    Cross-vendor delegated adversarial artifact review
    docs/review-outputs/adversarial-artifact-reviews/public_reaction_engagement_context_delegated_adversarial_artifact_review_patch_v0.md.
    Home-model adjudication accepted/applied AR-02 (Cleaning authorization
    posture) and AR-03 (canonical metric_posture vocabulary), deferred AR-01 and
    AR-04, and dropped/batched AR-05.
  controlling_sources_updated:
    - forseti/product/shared/engagement_registry/engagement_logic_registry_v0.md
    - forseti/product/spines/capture/core/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md
    - forseti/product/shared/projection_doctrine/core_spine_v0_projection_doctrine_v0.md
    - forseti/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
    - forseti/product/spines/foundation/product_contract/core_spine_v0_information_production_foundation_v0.md
    - forseti/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md
    - forseti/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_readme_v0.md
    - forseti/product/spines/cleaning/contracts/core_spine_v0_corroboration_vs_amplification_discipline_v0.md
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md
    - docs/decisions/cleaning_spine_data_lake_representation_defer_v0.md
    - forseti/product/spines/commission_signal_board/prompts/forseti_commission_signal_board_prompt_structure_v0.md
    - forseti/product/spines/commission_signal_board/authority/forseti_commission_signal_board_prompt_structure_rules_v0.md
    - forseti/product/spines/scanning/README.md
    - forseti/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/validation-gates.md
    - .agents/workflow-overlay/prompt-orchestration.md
    - forseti/product/spines/judgment/demand_read/core/judgment_spine_demand_read_machinery_architecture_v0.md
    - forseti/product/spines/judgment/demand_read/c2_weighting/judgment_spine_c2_ledger_read_contract_v0.md
  intentionally_not_updated:
    - path: orca-harness/cleaning/
      reason: >
        This turn reflects future behavior in durable documents only. Runtime
        enforcement through Cleaning models, projection adapters, and tests is a
        separate explicitly bounded implementation unit.
    - path: forseti/product/spines/product_lead/buyer_proof/forseti_buyer_proof_packet_v0.md
      reason: >
        Existing buyer-proof language already rejects engagement volume as a
        proof or Commit-grade floor-clearance shortcut. This patch points the
        cross-layer handling rule through the engagement registry and Judgment
        foundation rather than duplicating buyer-proof gates.
  stale_language_search: >
    rg -n "engagement|upvote|helpful|likes|views|comment count|score_state|Commit|Scale"
    forseti/product/shared/engagement_registry
    forseti/product/spines/capture
    forseti/product/spines/cleaning
    forseti/product/shared/projection_doctrine
    forseti/product/spines/data_lake
    forseti/product/spines/commission_signal_board
    forseti/product/spines/scanning
    forseti/product/spines/foundation/product_contract
    AND post-review adjudication query
    rg -n "metric_posture|metric posture|preserved, unavailable|unavailable_with_reason|not_attempted|owner-authorized|standing automation|lake writer"
    forseti/product/shared/engagement_registry
    forseti/product/spines/cleaning
    forseti/product/spines/foundation/product_contract
  stale_language_search_result: >
    Executed during the patch. Live edited surfaces now route public-reaction
    engagement through the registry, Capture preservation, Projection/Cleaning
    mechanical context, Data Lake medallion placement, CSB/Scanning attention
    routing, and Judgment-owned interpretation. Existing no-score/no-proof
    boundaries were preserved. Post-review adjudication executed 2026-06-26:
    Cleaning and Information Production Foundation now share canonical
    metric_posture vocabulary; Cleaning engagement_context now states the
    owner-authorized/deferred posture and non-authorization of Cleaning build,
    lake writer, standing automation, or cross-packet derivation.
  non_claims:
    - not validation
    - not readiness
    - not implementation authorization
    - not a scoring engine
    - not buyer proof
```

Older receipts archived verbatim in `docs/decisions/dcp_receipts_archive_v0.md`.
